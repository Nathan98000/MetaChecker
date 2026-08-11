"""S02c extract_figure_vision — Phase 1b vision interpretation.

Consumes the FIGURE_REGION artifact and sends ONLY regions flagged
needs_vision (bounded crops, never whole PDFs) to the configured vision
model. Produces a FOREST_PLOT_ROWS artifact per document with structured,
schema-validated rows, full provenance (concrete model id, prompt version,
region bbox), cache hits, cost accounting, and explicit failure states.

Behavior contracts:
- strict schema validation; ONE retry with the validation errors appended;
  a second failure records INVALID_OUTPUT for that region (kept as a region
  result with empty rows — abstention, not fabrication).
- transport failures (ProviderFailure) raise → at-least-once retry via the
  job queue; API failure is never a domain fact (§60).
- request cache (CacheEntry) keyed by model+prompt+image hash (§62).
- every call logged to ExternalCallLog with tokens/cost/latency (§58, §63).
- vision-only extractions carry confidence MEDIUM by rule vision_uncorroborated_v1
  (researcher directive: initial default, upgradable later by corroboration
  rules, never by the model itself).
"""

import datetime as dt
import time

import pymupdf
from sqlalchemy import select

from app.adapters.llm.provider import ProviderFailure, VisionProvider, VisionRequest
from app.db.models import CacheEntry, Document, ExternalCallLog, Job, ParseArtifact
from app.domain import forest_schema
from app.domain.documents import read_verified
from app.pipeline.registry import StageContext, StageResult, stage

PARSER_ID = "vision_forest_extractor"
PARSER_VERSION = "1"
STAGE_ID = "extract_figure_vision"
RENDER_DPI = 220
CACHE_NS = "vision_forest"

# injected at worker/benchmark setup; keeps the stage testable offline
_provider: VisionProvider | None = None
_model_role: str = "COMPLEX_EXTRACTION_MODEL"
_model_id: str = "unconfigured"


def configure(provider: VisionProvider, *, model_role: str, model_id: str) -> None:
    global _provider, _model_role, _model_id
    _provider = provider
    _model_role = model_role
    _model_id = model_id


def idempotency_key(sha256: str) -> str:
    return f"{STAGE_ID}:{sha256}:{PARSER_ID}:{PARSER_VERSION}:{_model_id}"


def _render_region(pdf: pymupdf.Document, page_number: int, bbox_native: list[float]) -> bytes:
    page = pdf[page_number - 1]
    clip = pymupdf.Rect(*bbox_native)
    pix = page.get_pixmap(dpi=RENDER_DPI, clip=clip)
    return pix.tobytes("png")


def _log_call(session, *, project_id, outcome, response=None, purpose, payload_bytes=None):
    session.add(
        ExternalCallLog(
            project_id=project_id,
            provider=_provider.provider_name if _provider else "none",
            model_role=_model_role,
            model_id=response.model_id if response else _model_id,
            stage_id=STAGE_ID,
            purpose=purpose,
            payload_bytes=payload_bytes,
            input_tokens=response.input_tokens if response else None,
            output_tokens=response.output_tokens if response else None,
            est_cost_usd=response.est_cost_usd if response else None,
            latency_ms=response.latency_ms if response else None,
            outcome=outcome,
        )
    )


def _interpret_region(ctx: StageContext, doc_row, region, image_png: bytes) -> dict:
    """One region → validated rows dict (with cache, retry-on-invalid)."""
    request = VisionRequest(
        prompt=forest_schema.PROMPT,
        prompt_id=forest_schema.PROMPT_ID,
        prompt_version=forest_schema.PROMPT_VERSION,
        image_png=image_png,
        model_id=_model_id,
        model_role=_model_role,
    )
    cached = ctx.session.scalar(
        select(CacheEntry).where(
            CacheEntry.namespace == CACHE_NS,
            CacheEntry.key_hash == request.cache_key(),
            CacheEntry.stale == False,  # noqa: E712
        )
    )
    if cached is not None:
        _log_call(
            ctx.session, project_id=doc_row.project_id, outcome="CACHE_HIT",
            purpose=f"forest-plot region p{region['page_number']} (cached)",
        )
        return cached.payload

    attempt_errors: list[str] = []
    prompt = request.prompt
    for attempt in (1, 2):
        req = VisionRequest(
            prompt=prompt, prompt_id=request.prompt_id,
            prompt_version=request.prompt_version, image_png=image_png,
            model_id=_model_id, model_role=_model_role,
        )
        response = _provider.interpret_image(req)  # ProviderFailure propagates
        result = forest_schema.validate_response(response.text)
        outcome = "OK" if result.ok else "INVALID_OUTPUT"
        _log_call(
            ctx.session, project_id=doc_row.project_id, outcome=outcome,
            response=response, payload_bytes=len(image_png),
            purpose=f"forest-plot region p{region['page_number']} attempt {attempt}",
        )
        if result.ok:
            payload = {
                "region": region,
                "rows": result.rows,
                "meta": result.meta,
                "model_id": response.model_id,
                "prompt_id": request.prompt_id,
                "prompt_version": request.prompt_version,
                "confidence": "MEDIUM",
                "confidence_rule_id": "vision_uncorroborated_v1",
                "confidence_rule_version": "1",
                "status": "OK",
                "raw_response": response.text,
            }
            ctx.session.add(
                CacheEntry(namespace=CACHE_NS, key_hash=request.cache_key(), payload=payload)
            )
            return payload
        attempt_errors.extend(result.errors)
        prompt = (
            forest_schema.PROMPT
            + "\n\nYour previous answer was rejected by strict validation:\n- "
            + "\n- ".join(result.errors[:10])
            + "\nReturn corrected JSON only."
        )
    # both attempts structurally invalid → explicit abstention for the region
    return {
        "region": region,
        "rows": [],
        "meta": {"region_readable": False},
        "model_id": _model_id,
        "prompt_id": request.prompt_id,
        "prompt_version": request.prompt_version,
        "status": "INVALID_OUTPUT",
        "errors": attempt_errors[:20],
    }


@stage(STAGE_ID)
def run(ctx: StageContext, job: Job) -> StageResult:
    if _provider is None:
        return StageResult(
            state="INSUFFICIENT_DATA",
            detail={"reason": "no vision provider configured (set ANTHROPIC_API_KEY or use replay)"},
            issue_type="API_FAILURE",
        )
    doc_row = ctx.session.get(Document, job.work_item_ref)
    if doc_row is None:
        return StageResult(state="INSUFFICIENT_DATA", detail={"reason": "document missing"})

    figure_artifact = ctx.session.scalar(
        select(ParseArtifact)
        .where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.kind == "FIGURE_REGION",
        )
        .order_by(ParseArtifact.created_at.desc())
    )
    if figure_artifact is None:
        return StageResult(
            state="INSUFFICIENT_DATA",
            detail={"reason": "figure regions not detected yet (run detect_figure_regions first)"},
        )

    targets = [r for r in figure_artifact.payload["regions"] if r.get("needs_vision")]
    if not targets:
        return StageResult(state="SUCCESS", detail={"regions": 0, "note": "no regions need vision"})

    content = read_verified(ctx.documents_dir, doc_row)
    pdf = pymupdf.open(stream=content, filetype="pdf")
    results, invalid = [], 0
    started = time.perf_counter()
    try:
        for region in targets:
            image_png = _render_region(pdf, region["page_number"], region["bbox_native"])
            outcome = _interpret_region(ctx, doc_row, region, image_png)
            results.append(outcome)
            if outcome["status"] != "OK":
                invalid += 1
    finally:
        pdf.close()

    input_hash = f"{doc_row.sha256}:{_model_id}:{forest_schema.PROMPT_VERSION}"
    existing = ctx.session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.parser_id == PARSER_ID,
            ParseArtifact.parser_version == PARSER_VERSION,
            ParseArtifact.kind == "FOREST_PLOT_ROWS",
            ParseArtifact.input_hash == input_hash,
        )
    )
    if existing is None:
        ctx.session.add(
            ParseArtifact(
                project_id=doc_row.project_id,
                document_id=doc_row.id,
                parser_id=PARSER_ID,
                parser_version=PARSER_VERSION,
                kind="FOREST_PLOT_ROWS",
                payload={
                    "results": results,
                    "elapsed_s": round(time.perf_counter() - started, 2),
                    "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
                input_hash=input_hash,
            )
        )

    rows_total = sum(len(r["rows"]) for r in results)
    if invalid and invalid == len(results):
        return StageResult(
            state="NEEDS_REVIEW",
            detail={"regions": len(results), "invalid": invalid, "rows": rows_total},
        )
    state = "PARTIAL_SUCCESS" if invalid else "SUCCESS"
    return StageResult(
        state=state,
        detail={
            "regions": len(results),
            "invalid": invalid,
            "rows": rows_total,
            "extracted": ["structured forest-plot rows"],
            "not_extracted": [f"{invalid} region(s) returned invalid output"] if invalid else [],
        },
    )
