"""Durable, resumable job queue (doc 00 A11; doc 04 §2).

Guarantees: durable jobs, at-least-once execution, lease-based claiming with
expiry reclaim, retry tracking with backoff, idempotency-key dedup. Handlers
must be idempotent — the queue never promises exactly-once.

SQLite-compatible: claiming uses BEGIN IMMEDIATE (single-writer) via the
session's connection; the same interface maps to SKIP LOCKED on PostgreSQL.
"""

import datetime as dt
import traceback

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Job, StageState
from app.domain import workflow


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def enqueue(
    session: Session,
    *,
    project_id: str,
    stage_id: str,
    work_item_ref: str,
    idempotency_key: str,
    input_hash: str | None = None,
    max_attempts: int = 3,
    parent_job_id: str | None = None,
) -> Job:
    """Insert a job, deduplicating on idempotency_key."""
    existing = session.scalar(select(Job).where(Job.idempotency_key == idempotency_key))
    if existing is not None:
        return existing
    job = Job(
        project_id=project_id,
        stage_id=stage_id,
        work_item_ref=work_item_ref,
        idempotency_key=idempotency_key,
        input_hash=input_hash,
        max_attempts=max_attempts,
        parent_job_id=parent_job_id,
    )
    session.add(job)
    try:
        session.flush()
    except IntegrityError:
        # Lost a race on the unique key: return the winner.
        session.rollback()
        return session.scalar(select(Job).where(Job.idempotency_key == idempotency_key))
    return job


def claim(session: Session, *, worker_id: str, lease_seconds: float) -> Job | None:
    """Claim the next runnable job: QUEUED-and-available, or RUNNING with an
    expired lease (at-least-once reclaim)."""
    now = _now()
    job = session.scalar(
        select(Job)
        .where(
            (
                (Job.state == "QUEUED") & (Job.available_at <= now)
            )
            | ((Job.state == "RUNNING") & (Job.lease_expires_at <= now))
        )
        .order_by(Job.created_at)
        .limit(1)
    )
    if job is None:
        return None
    job.state = "RUNNING"
    job.attempt += 1
    job.lease_owner = worker_id
    job.lease_expires_at = now + dt.timedelta(seconds=lease_seconds)
    session.commit()
    return job


def heartbeat(session: Session, job: Job, lease_seconds: float) -> None:
    job.lease_expires_at = _now() + dt.timedelta(seconds=lease_seconds)
    session.commit()


def complete(
    session: Session,
    job: Job,
    *,
    stage_state: str,
    detail: dict | None = None,
) -> None:
    """Record success: job terminal + stage-state upsert + issue auto-resolve,
    in one transaction."""
    job.state = "SUCCEEDED"
    job.finished_at = _now()
    job.lease_owner = None
    job.lease_expires_at = None

    existing = session.scalar(
        select(StageState).where(
            StageState.stage_id == job.stage_id,
            StageState.work_item_ref == job.work_item_ref,
        )
    )
    if existing is None:
        session.add(
            StageState(
                project_id=job.project_id,
                stage_id=job.stage_id,
                work_item_ref=job.work_item_ref,
                state=stage_state,
                detail=detail,
                job_id=job.id,
            )
        )
    else:
        existing.state = stage_state
        existing.detail = detail
        existing.job_id = job.id

    if stage_state in ("SUCCESS", "PARTIAL_SUCCESS"):
        workflow.resolve_issues_for(
            session, work_item_ref=job.work_item_ref, stage_id=job.stage_id
        )
    session.commit()


def fail(
    session: Session,
    job: Job,
    exc: BaseException,
    *,
    backoff_seconds: float = 5.0,
    issue_type: str = "API_FAILURE",
) -> None:
    """Record failure: retry with backoff, or FAILED_PERMANENT + open a
    researcher-visible workflow issue. Never writes domain rows (doc 01 §3)."""
    job.error = "".join(
        traceback.format_exception_only(type(exc), exc)
    ).strip()[:2000]
    job.lease_owner = None
    job.lease_expires_at = None
    if job.attempt >= job.max_attempts:
        job.state = "FAILED_PERMANENT"
        job.finished_at = _now()
        workflow.open_issue(
            session,
            project_id=job.project_id,
            issue_type=issue_type,
            work_item_ref=job.work_item_ref,
            stage_id=job.stage_id,
            detail=job.error,
        )
    else:
        job.state = "QUEUED"
        job.available_at = _now() + dt.timedelta(
            seconds=backoff_seconds * (2 ** (job.attempt - 1))
        )
    session.commit()
