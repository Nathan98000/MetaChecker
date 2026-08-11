"""Structured errors (SRS §19): what happened, what it means, what to do next.

These are the only errors the researcher-facing UI renders. Internal
exceptions are logged and mapped to a generic AppError so raw tracebacks never
reach the primary UI.
"""

from dataclasses import dataclass, field


@dataclass
class AppError(Exception):
    code: str
    what_happened: str
    what_it_means: str = ""
    next_steps: list[str] = field(default_factory=list)
    http_status: int = 400

    def to_payload(self) -> dict:
        return {
            "code": self.code,
            "what_happened": self.what_happened,
            "what_it_means": self.what_it_means,
            "next_steps": self.next_steps,
        }


def not_found(entity: str) -> AppError:
    return AppError(
        code="NOT_FOUND",
        what_happened=f"The requested {entity} could not be found.",
        what_it_means="It may have been deleted, or the link is out of date.",
        next_steps=["Return to the project overview."],
        http_status=404,
    )


def invalid_provenance(detail: str) -> AppError:
    return AppError(
        code="INVALID_PROVENANCE",
        what_happened="A value was submitted without valid source information.",
        what_it_means=(
            "Every value in an audit must be traceable to a source document "
            "or a recorded calculation. " + detail
        ),
        next_steps=["This indicates an application bug; the value was not saved."],
        http_status=422,
    )
