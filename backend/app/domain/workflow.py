"""Workflow-issue lifecycle (doc 00 A4/O3, doc 04 §4).

Issues are the researcher-facing projection of persistent step failures.
At most one OPEN issue per (work item × issue type); auto-resolved when the
underlying stage later succeeds; history preserved. Never audit findings.
"""

import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import WorkflowIssue


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def open_issue(
    session: Session,
    *,
    project_id: str,
    issue_type: str,
    work_item_ref: str,
    stage_id: str | None = None,
    detail: str | None = None,
) -> WorkflowIssue:
    existing = session.scalar(
        select(WorkflowIssue).where(
            WorkflowIssue.work_item_ref == work_item_ref,
            WorkflowIssue.issue_type == issue_type,
            WorkflowIssue.state == "OPEN",
        )
    )
    if existing is not None:
        existing.last_seen = _now()
        existing.detail = detail or existing.detail
        return existing
    issue = WorkflowIssue(
        project_id=project_id,
        issue_type=issue_type,
        work_item_ref=work_item_ref,
        stage_id=stage_id,
        detail=detail,
    )
    session.add(issue)
    session.flush()
    return issue


def resolve_issues_for(
    session: Session, *, work_item_ref: str, stage_id: str | None = None
) -> int:
    """Auto-resolve OPEN issues for a work item after a successful stage run."""
    query = select(WorkflowIssue).where(
        WorkflowIssue.work_item_ref == work_item_ref,
        WorkflowIssue.state == "OPEN",
    )
    if stage_id is not None:
        query = query.where(WorkflowIssue.stage_id == stage_id)
    resolved = 0
    for issue in session.scalars(query):
        issue.state = "RESOLVED"
        issue.resolved_at = _now()
        resolved += 1
    return resolved
