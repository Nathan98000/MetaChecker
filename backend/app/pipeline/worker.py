"""Worker loop: claim → run stage → complete/fail.

Single worker process with short DB transactions (doc 00 O4): stage handlers
do their heavy work (PDF parsing, later OCR/LLM calls) outside any open
write transaction; the queue commits state transitions atomically.
"""

import logging
import threading
from pathlib import Path

from sqlalchemy.orm import Session, sessionmaker

from app.core.ids import uuid7
from app.pipeline import queue
from app.pipeline.registry import StageContext, get_handler

log = logging.getLogger("metaaudit.worker")


def process_one(
    session: Session, documents_dir: Path, *, worker_id: str, lease_seconds: float = 60.0
) -> bool:
    """Claim and run a single job. Returns False when the queue is idle."""
    job = queue.claim(session, worker_id=worker_id, lease_seconds=lease_seconds)
    if job is None:
        return False
    try:
        handler = get_handler(job.stage_id)
        result = handler(StageContext(session=session, documents_dir=documents_dir), job)
        if result.issue_type:
            from app.domain import workflow

            workflow.open_issue(
                session,
                project_id=job.project_id,
                issue_type=result.issue_type,
                work_item_ref=job.work_item_ref,
                stage_id=job.stage_id,
                detail=str(result.detail.get("reason", ""))[:1000],
            )
        queue.complete(session, job, stage_state=result.state, detail=result.detail)
    except Exception as exc:  # infrastructure failure → retry/backoff
        log.exception("stage %s failed for %s", job.stage_id, job.work_item_ref)
        session.rollback()
        queue.fail(session, job, exc)
    return True


def drain(session: Session, documents_dir: Path, *, worker_id: str = "sync") -> int:
    """Process jobs until the queue is idle (used by tests and dev API)."""
    n = 0
    while process_one(session, documents_dir, worker_id=worker_id):
        n += 1
    return n


class WorkerThread(threading.Thread):
    def __init__(
        self,
        session_factory: sessionmaker,
        documents_dir: Path,
        *,
        poll_seconds: float = 0.5,
        lease_seconds: float = 60.0,
    ):
        super().__init__(daemon=True, name="metaaudit-worker")
        self.session_factory = session_factory
        self.documents_dir = documents_dir
        self.poll_seconds = poll_seconds
        self.lease_seconds = lease_seconds
        self.worker_id = f"worker-{uuid7()[:8]}"
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        while not self._stop.is_set():
            with self.session_factory() as session:
                busy = process_one(
                    session,
                    self.documents_dir,
                    worker_id=self.worker_id,
                    lease_seconds=self.lease_seconds,
                )
            if not busy:
                self._stop.wait(self.poll_seconds)
