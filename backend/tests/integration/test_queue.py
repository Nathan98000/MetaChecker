"""Durable queue: at-least-once, idempotency, interruption, issue lifecycle
(doc 08 §2)."""

import datetime as dt

from sqlalchemy import select

from app.db.models import DocumentPage, Job, ParseArtifact, StageState, WorkflowIssue
from app.domain.documents import ingest_document
from app.pipeline import queue
from app.pipeline.registry import StageContext, stage
from app.pipeline.stages import parse_document as parse_stage
from app.pipeline.worker import drain, process_one
from tests.conftest import make_pdf


def _enqueue_parse(session, documents_dir, project, content=None):
    doc, _ = ingest_document(
        session,
        documents_dir,
        project_id=project.id,
        filename="meta.pdf",
        content=content or make_pdf(),
    )
    job = queue.enqueue(
        session,
        project_id=project.id,
        stage_id=parse_stage.STAGE_ID,
        work_item_ref=doc.id,
        idempotency_key=parse_stage.idempotency_key(doc.sha256),
        input_hash=doc.sha256,
    )
    session.commit()
    return doc, job


def test_enqueue_deduplicates_on_idempotency_key(session, documents_dir, project):
    doc, job1 = _enqueue_parse(session, documents_dir, project)
    job2 = queue.enqueue(
        session,
        project_id=project.id,
        stage_id=parse_stage.STAGE_ID,
        work_item_ref=doc.id,
        idempotency_key=parse_stage.idempotency_key(doc.sha256),
    )
    session.commit()
    assert job1.id == job2.id
    assert session.scalars(select(Job)).all().__len__() == 1


def test_duplicate_execution_does_not_duplicate_records(
    session, documents_dir, project
):
    doc, job = _enqueue_parse(session, documents_dir, project)
    drain(session, documents_dir)

    # Force the same job to run again (simulates at-least-once redelivery)
    job = session.get(Job, job.id)
    job.state = "QUEUED"
    job.available_at = dt.datetime.now(dt.timezone.utc)
    session.commit()
    drain(session, documents_dir)

    artifacts = session.scalars(
        select(ParseArtifact).where(ParseArtifact.document_id == doc.id)
    ).all()
    pages = session.scalars(
        select(DocumentPage).where(DocumentPage.document_id == doc.id)
    ).all()
    assert len(artifacts) == 1  # no duplicated scientific records
    assert len(pages) == 1


def test_interrupted_job_is_reclaimed_after_lease_expiry(
    session, documents_dir, project
):
    doc, job = _enqueue_parse(session, documents_dir, project)

    # Worker A claims, then "crashes" (never completes)
    claimed = queue.claim(session, worker_id="worker-A", lease_seconds=0.0)
    assert claimed.id == job.id
    assert claimed.state == "RUNNING"

    # After lease expiry, worker B can reclaim and finish the same job
    assert process_one(session, documents_dir, worker_id="worker-B") is True
    job = session.get(Job, job.id)
    assert job.state == "SUCCEEDED"
    state = session.scalar(select(StageState).where(StageState.work_item_ref == doc.id))
    assert state.state == "SUCCESS"


def test_permanent_failure_opens_workflow_issue_and_success_resolves_it(
    session, documents_dir, project
):
    calls = {"n": 0}

    @stage("always_fails_then_succeeds")
    def flaky(ctx: StageContext, job):  # noqa: ARG001
        calls["n"] += 1
        raise RuntimeError("simulated infrastructure failure")

    job = queue.enqueue(
        session,
        project_id=project.id,
        stage_id="always_fails_then_succeeds",
        work_item_ref="item-1",
        idempotency_key="flaky:item-1",
        max_attempts=2,
    )
    session.commit()

    # Exhaust retries (backoff makes the job unavailable; fast-forward it)
    for _ in range(2):
        assert process_one(session, documents_dir, worker_id="w") is True
        j = session.get(Job, job.id)
        if j.state == "QUEUED":
            j.available_at = dt.datetime.now(dt.timezone.utc)
            session.commit()

    j = session.get(Job, job.id)
    assert j.state == "FAILED_PERMANENT"
    issue = session.scalar(
        select(WorkflowIssue).where(WorkflowIssue.work_item_ref == "item-1")
    )
    assert issue is not None and issue.state == "OPEN"
    assert issue.issue_type == "API_FAILURE"

    # A later successful run of the same stage auto-resolves the issue (O3)
    from app.pipeline import registry

    @stage("always_fails_then_succeeds")
    def now_succeeds(ctx, job):  # noqa: ARG001
        from app.pipeline.registry import StageResult

        return StageResult(state="SUCCESS")

    j.state = "QUEUED"
    j.attempt = 0
    j.available_at = dt.datetime.now(dt.timezone.utc)
    session.commit()
    process_one(session, documents_dir, worker_id="w")

    issue = session.scalar(
        select(WorkflowIssue).where(WorkflowIssue.work_item_ref == "item-1")
    )
    assert issue.state == "RESOLVED"
    assert issue.resolved_at is not None


def test_unreadable_pdf_yields_stage_state_and_issue_not_finding(
    session, documents_dir, project
):
    doc, _ = _enqueue_parse(session, documents_dir, project, content=b"not a pdf at all")
    drain(session, documents_dir)
    state = session.scalar(select(StageState).where(StageState.work_item_ref == doc.id))
    assert state.state == "DOCUMENT_UNREADABLE"
    issue = session.scalar(
        select(WorkflowIssue).where(WorkflowIssue.work_item_ref == doc.id)
    )
    assert issue is not None
    assert issue.issue_type == "DOCUMENT_UNREADABLE"


def test_reparse_never_modifies_source_document(session, documents_dir, project):
    content = make_pdf()
    doc, _ = _enqueue_parse(session, documents_dir, project, content=content)
    drain(session, documents_dir)
    from app.domain.documents import read_verified

    assert read_verified(documents_dir, doc) == content  # hash re-verified
