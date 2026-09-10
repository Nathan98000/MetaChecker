"""Vision extraction stage against fake/replay providers (Phase 1b infra).

Covers: happy path, retry-on-invalid then success, double-invalid abstention,
transport failure → job retry → workflow issue, caching, cost accounting,
idempotency, and replay fixtures."""

import json

import pytest
from sqlalchemy import select

from app.adapters.llm.fake import FakeVisionProvider, ReplayVisionProvider
from app.adapters.llm.provider import ProviderFailure, VisionRequest
from app.adapters.llm.router import ModelRouter
from app.db.models import CacheEntry, ExternalCallLog, Job, ParseArtifact, WorkflowIssue
from app.domain import forest_schema
from app.domain.documents import ingest_document
from app.pipeline import queue
from app.pipeline.stages import detect_figures, extract_figure_vision as vision
from app.pipeline.stages import parse_document as parse_stage
from app.pipeline.worker import drain
from tests.conftest import make_pdf
import pymupdf


def make_forest_pdf() -> bytes:
    """Synthetic page with a vector 'forest plot' (no text inside region)."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((72, 60), "Results are shown in the figure below.", fontsize=11)
    for y in range(200, 430, 22):
        page.draw_line(pymupdf.Point(90, y), pymupdf.Point(500, y), width=1)
        page.draw_rect(pymupdf.Rect(260 + (y % 60), y - 3, 270 + (y % 60), y + 3), fill=(0, 0, 0))
    page.draw_line(pymupdf.Point(295, 190), pymupdf.Point(295, 440), width=1)
    page.insert_text((90, 460), "Figure 2 Forest plot of the association", fontsize=9)
    data = doc.tobytes()
    doc.close()
    return data


GOOD_RESPONSE = json.dumps(
    {
        "region_readable": True,
        "columns_seen": ["Study", "HR (95% CI)", "Weight"],
        "rows": [
            {"row_kind": "STUDY_ROW", "study_label": "Hong (2015)", "effect_value": "1.38",
             "ci_lower": "1.02", "ci_upper": "1.85", "weight": "5.67"},
            {"row_kind": "OVERALL_SUMMARY", "study_label": "Overall", "effect_value": "1.69",
             "ci_lower": "1.42", "ci_upper": "2.01", "weight": "100.00"},
        ],
    }
)


def _setup(session, documents_dir, project, provider):
    vision.configure(provider, model_role="COMPLEX_EXTRACTION_MODEL", model_id="claude-fable-5")
    doc, _ = ingest_document(
        session, documents_dir, project_id=project.id, filename="m.pdf", content=make_forest_pdf()
    )
    for stage_mod in (parse_stage, detect_figures):
        queue.enqueue(
            session, project_id=project.id, stage_id=stage_mod.STAGE_ID,
            work_item_ref=doc.id, idempotency_key=stage_mod.idempotency_key(doc.sha256),
        )
    session.commit()
    drain(session, documents_dir)
    queue.enqueue(
        session, project_id=project.id, stage_id=vision.STAGE_ID,
        work_item_ref=doc.id, idempotency_key=vision.idempotency_key(doc.sha256),
    )
    session.commit()
    return doc


def _rows_artifact(session, doc_id):
    return session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_id,
            ParseArtifact.kind == "FOREST_PLOT_ROWS",
        )
    )


def test_happy_path_produces_validated_rows_with_provenance(session, documents_dir, project):
    provider = FakeVisionProvider([GOOD_RESPONSE])
    doc = _setup(session, documents_dir, project, provider)
    drain(session, documents_dir)

    artifact = _rows_artifact(session, doc.id)
    assert artifact is not None
    result = artifact.payload["results"][0]
    assert result["status"] == "OK"
    assert [r["row_kind"] for r in result["rows"]] == ["STUDY_ROW", "OVERALL_SUMMARY"]
    # provenance + confidence rule (vision-only → MEDIUM, never model-assigned)
    assert result["model_id"].startswith("fake:")
    assert result["confidence"] == "MEDIUM"
    assert result["confidence_rule_id"] == "vision_uncorroborated_v1"
    assert result["prompt_version"] == forest_schema.PROMPT_VERSION
    # cost accounting
    calls = session.scalars(select(ExternalCallLog)).all()
    assert any(c.outcome == "OK" and c.output_tokens for c in calls)
    # bounded region, not whole page: image bytes went through provider
    assert provider.calls and len(provider.calls[0].image_png) > 1000


def test_invalid_then_corrected_output_retries_once(session, documents_dir, project):
    provider = FakeVisionProvider(["this is not json at all", GOOD_RESPONSE])
    doc = _setup(session, documents_dir, project, provider)
    drain(session, documents_dir)

    result = _rows_artifact(session, doc.id).payload["results"][0]
    assert result["status"] == "OK"
    assert len(provider.calls) == 2
    assert "rejected by strict validation" in provider.calls[1].prompt
    outcomes = [c.outcome for c in session.scalars(select(ExternalCallLog))]
    assert "INVALID_OUTPUT" in outcomes and "OK" in outcomes


def test_double_invalid_output_abstains_never_fabricates(session, documents_dir, project):
    provider = FakeVisionProvider(["garbage", json.dumps({"rows": [{"row_kind": "BAD"}]})])
    doc = _setup(session, documents_dir, project, provider)
    drain(session, documents_dir)

    result = _rows_artifact(session, doc.id).payload["results"][0]
    assert result["status"] == "INVALID_OUTPUT"
    assert result["rows"] == []  # abstention, not fabrication
    job = session.scalar(select(Job).where(Job.stage_id == vision.STAGE_ID))
    assert job.state == "SUCCEEDED"  # ran fine; region marked needs-review


def test_transport_failure_retries_job_then_opens_workflow_issue(
    session, documents_dir, project
):
    provider = FakeVisionProvider(
        [ProviderFailure("simulated 529"), ProviderFailure("simulated 529"),
         ProviderFailure("simulated 529")]
    )
    doc = _setup(session, documents_dir, project, provider)
    import datetime as dt
    for _ in range(3):
        drain(session, documents_dir)
        job = session.scalar(select(Job).where(Job.stage_id == vision.STAGE_ID))
        if job.state == "QUEUED":
            job.available_at = dt.datetime.now(dt.timezone.utc)
            session.commit()

    job = session.scalar(select(Job).where(Job.stage_id == vision.STAGE_ID))
    assert job.state == "FAILED_PERMANENT"
    issue = session.scalar(
        select(WorkflowIssue).where(WorkflowIssue.work_item_ref == doc.id,
                                    WorkflowIssue.issue_type == "API_FAILURE")
    )
    assert issue is not None and issue.state == "OPEN"
    assert _rows_artifact(session, doc.id) is None  # API failure ≠ domain fact


def test_cache_prevents_repeat_calls(session, documents_dir, project):
    provider = FakeVisionProvider([GOOD_RESPONSE])
    doc = _setup(session, documents_dir, project, provider)
    drain(session, documents_dir)
    assert len(provider.calls) == 1

    # force the same job to run again (at-least-once redelivery)
    import datetime as dt
    job = session.scalar(select(Job).where(Job.stage_id == vision.STAGE_ID))
    job.state = "QUEUED"
    job.available_at = dt.datetime.now(dt.timezone.utc)
    session.commit()
    drain(session, documents_dir)

    assert len(provider.calls) == 1  # cache hit, no second model call
    outcomes = [c.outcome for c in session.scalars(select(ExternalCallLog))]
    assert "CACHE_HIT" in outcomes
    artifacts = session.scalars(
        select(ParseArtifact).where(ParseArtifact.kind == "FOREST_PLOT_ROWS")
    ).all()
    assert len(artifacts) == 1  # idempotent artifact


def test_replay_provider_round_trip(tmp_path, session, documents_dir, project):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    # record a fixture by computing the request the stage will make
    vision.configure(FakeVisionProvider([GOOD_RESPONSE]),
                     model_role="COMPLEX_EXTRACTION_MODEL", model_id="claude-fable-5")
    doc = _setup(session, documents_dir, project, FakeVisionProvider([GOOD_RESPONSE]))
    drain(session, documents_dir)
    # rebuild the exact request to derive its cache key, then write fixture
    artifact = _rows_artifact(session, doc.id)
    region = artifact.payload["results"][0]["region"]
    import pymupdf as pm
    from app.domain.documents import read_verified
    pdf = pm.open(stream=read_verified(documents_dir, doc), filetype="pdf")
    png = vision._render_region(pdf, region["page_number"], region["bbox_native"])
    pdf.close()
    req = VisionRequest(
        prompt=forest_schema.PROMPT, prompt_id=forest_schema.PROMPT_ID,
        prompt_version=forest_schema.PROMPT_VERSION, image_png=png,
        model_id="claude-fable-5", model_role="COMPLEX_EXTRACTION_MODEL",
    )
    (fixture_dir / f"{req.cache_key()}.json").write_text(
        json.dumps({"text": GOOD_RESPONSE, "model_id": "claude-fable-5"})
    )
    replay = ReplayVisionProvider(fixture_dir)
    response = replay.interpret_image(req)
    assert forest_schema.validate_response(response.text).ok
    # and a missing fixture fails loudly (no silent network)
    other = VisionRequest(prompt="x", prompt_id="p", prompt_version="9",
                          image_png=b"zz", model_id="m", model_role="r")
    with pytest.raises(ProviderFailure):
        replay.interpret_image(other)


def test_model_router_resolves_and_rejects():
    router = ModelRouter()
    role, model = router.resolve_task("forest_plot_vision")
    assert role == "COMPLEX_EXTRACTION_MODEL" and model == "claude-fable-5"
    with pytest.raises(KeyError):
        router.resolve_task("nonexistent_task")


def test_stage_requests_large_output_budget_and_flags_truncation(
    session, documents_dir, project
):
    """Dense forest plots truncated at the SDK default budget (benchmark
    2026-08-13); the stage must request a large budget and treat a
    max_tokens-stopped response as invalid, never half-parse it."""
    from app.adapters.llm.provider import LLMResponse, VisionProvider

    class TruncatingProvider(VisionProvider):
        provider_name = "trunc"

        def __init__(self):
            self.calls = []

        def interpret_image(self, request):
            self.calls.append(request)
            return LLMResponse(
                text='{"rows": [{"row_kind": "STUDY_ROW", "study_label": "A"',
                model_id="trunc-model", output_tokens=request.max_tokens,
                raw_meta={"stop_reason": "max_tokens"},
            )

    provider = TruncatingProvider()
    doc = _setup(session, documents_dir, project, provider)
    drain(session, documents_dir)

    assert all(c.max_tokens >= 16000 for c in provider.calls)
    result = _rows_artifact(session, doc.id).payload["results"][0]
    assert result["status"] == "INVALID_OUTPUT"
    assert result["rows"] == []
    assert any("truncated" in e for e in result.get("errors", []))
