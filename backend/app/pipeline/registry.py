"""Stage registry.

A stage handler is `fn(ctx, job) -> StageResult`. Handlers must be idempotent:
running the same job twice must not duplicate scientific records (outputs are
upserted under natural unique keys). Handlers signal domain conclusions via
StageResult; they raise only for retryable infrastructure failure.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from sqlalchemy.orm import Session

from app.db.models import Job


@dataclass
class StageContext:
    session: Session
    documents_dir: Path


@dataclass
class StageResult:
    state: str  # doc 04 §3 vocabulary
    detail: dict = field(default_factory=dict)
    issue_type: str | None = None  # open a workflow issue alongside the state


Handler = Callable[[StageContext, Job], StageResult]

_REGISTRY: dict[str, Handler] = {}


def stage(stage_id: str) -> Callable[[Handler], Handler]:
    def register(fn: Handler) -> Handler:
        _REGISTRY[stage_id] = fn
        return fn

    return register


def get_handler(stage_id: str) -> Handler:
    return _REGISTRY[stage_id]


def known_stages() -> list[str]:
    return sorted(_REGISTRY)
