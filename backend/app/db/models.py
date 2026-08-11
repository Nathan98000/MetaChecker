"""Foundation entities (docs 02–05).

Only the tables needed for the foundation + vertical slice are defined here;
later phases add bibliographic, analysis, and audit tables via migrations.
Append-only tables (revisions, locators, extraction records, review events)
have no update paths in the domain services; documents are immutable files
addressed by content hash.
"""

import datetime as dt

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.ids import uuid7
from app.db.base import Base


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


class Project(Base):
    __tablename__ = "project"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class Document(Base):
    """An immutable stored file, addressed by sha256 in the document store."""

    __tablename__ = "document"
    __table_args__ = (UniqueConstraint("project_id", "sha256"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    filename: Mapped[str] = mapped_column(String(1000))
    role: Mapped[str] = mapped_column(String(40), default="META_ANALYSIS")
    origin: Mapped[str] = mapped_column(String(40), default="UPLOADED")
    size_bytes: Mapped[int] = mapped_column(Integer)
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class DocumentPage(Base):
    __tablename__ = "document_page"
    __table_args__ = (UniqueConstraint("document_id", "page_number"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    document_id: Mapped[str] = mapped_column(ForeignKey("document.id"), index=True)
    page_number: Mapped[int] = mapped_column(Integer)  # 1-based
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    rotation: Mapped[int] = mapped_column(Integer, default=0)


class ParseArtifact(Base):
    """Append-only output of one parser run (doc 02 §2)."""

    __tablename__ = "parse_artifact"
    __table_args__ = (
        UniqueConstraint(
            "document_id", "parser_id", "parser_version", "kind", "input_hash"
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("document.id"), index=True)
    parser_id: Mapped[str] = mapped_column(String(100))
    parser_version: Mapped[str] = mapped_column(String(40))
    kind: Mapped[str] = mapped_column(String(40))  # TEXT_SPANS | TABLE | ...
    payload: Mapped[dict] = mapped_column(JSON)
    input_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class SourceLocator(Base):
    """Immutable 'where in a source document' anchor (doc 03 §3)."""

    __tablename__ = "source_locator"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("document.id"), index=True)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    table_number: Mapped[str | None] = mapped_column(String(40), nullable=True)
    figure_number: Mapped[str | None] = mapped_column(String(40), nullable=True)
    row_label: Mapped[str | None] = mapped_column(String(500), nullable=True)
    column_label: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    bbox_norm: Mapped[list | None] = mapped_column(JSON, nullable=True)  # A9
    bbox_native: Mapped[list | None] = mapped_column(JSON, nullable=True)
    parser_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    parser_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    parse_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("parse_artifact.id"), nullable=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class ExtractionRecord(Base):
    """How a value was acquired (doc 03 §4)."""

    __tablename__ = "extraction_record"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    acquisition_method: Mapped[str] = mapped_column(String(40))
    extractor_id: Mapped[str] = mapped_column(String(100))
    extractor_version: Mapped[str] = mapped_column(String(40))
    model_role: Mapped[str | None] = mapped_column(String(40), nullable=True)
    model_id: Mapped[str | None] = mapped_column(String(100), nullable=True)  # A16
    prompt_ref: Mapped[str | None] = mapped_column(String(200), nullable=True)
    raw_response_ref: Mapped[str | None] = mapped_column(String(200), nullable=True)
    input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class Calculation(Base):
    __tablename__ = "calculation"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    formula_id: Mapped[str] = mapped_column(String(100))
    formula_version: Mapped[str] = mapped_column(String(40))
    engine_version: Mapped[str] = mapped_column(String(40))
    warnings: Mapped[list | None] = mapped_column(JSON, nullable=True)
    input_quality_summary: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class CalculationInput(Base):
    __tablename__ = "calculation_input"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    calculation_id: Mapped[str] = mapped_column(
        ForeignKey("calculation.id"), index=True
    )
    data_point_id: Mapped[str] = mapped_column(ForeignKey("data_point.id"))
    revision_id: Mapped[str] = mapped_column(ForeignKey("value_revision.id"))
    role: Mapped[str] = mapped_column(String(100))


class DataPoint(Base):
    __tablename__ = "data_point"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    quantity_kind: Mapped[str] = mapped_column(String(40))
    current_revision_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True
    )  # head pointer; FK enforced in service (row created before first revision)


class ValueRevision(Base):
    """Append-only value history (doc 03 §2). The four orthogonal dimensions
    of doc 00 A2/A3 live here. CHECK constraints make unprovenanced values
    uncommittable (§6, §54)."""

    __tablename__ = "value_revision"
    __table_args__ = (
        UniqueConstraint("data_point_id", "revision_no"),
        CheckConstraint(
            "scientific_basis IN "
            "('SOURCE_REPORTED','DERIVED','INFERRED','UNRESOLVED')",
            name="ck_basis_enum",
        ),
        CheckConstraint(
            "review_state IN ('NOT_REVIEWED','REVIEW_REQUIRED','VERIFIED',"
            "'CORRECTED','MARKED_UNCERTAIN','EXCLUDED')",
            name="ck_review_enum",
        ),
        # SOURCE_REPORTED / INFERRED require a source locator (doc 03 §2)
        CheckConstraint(
            "scientific_basis NOT IN ('SOURCE_REPORTED','INFERRED') "
            "OR source_locator_id IS NOT NULL",
            name="ck_source_requires_locator",
        ),
        # DERIVED requires a calculation
        CheckConstraint(
            "scientific_basis != 'DERIVED' OR calculation_id IS NOT NULL",
            name="ck_derived_requires_calculation",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    data_point_id: Mapped[str] = mapped_column(ForeignKey("data_point.id"), index=True)
    revision_no: Mapped[int] = mapped_column(Integer)

    value_text: Mapped[str | None] = mapped_column(Text, nullable=True)  # verbatim
    value_numeric: Mapped[float | None] = mapped_column(Numeric(asdecimal=False), nullable=True)
    value_normalized: Mapped[float | None] = mapped_column(Numeric(asdecimal=False), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(100), nullable=True)

    scientific_basis: Mapped[str] = mapped_column(String(40))
    acquisition_method: Mapped[str | None] = mapped_column(String(40), nullable=True)
    confidence: Mapped[str | None] = mapped_column(String(10), nullable=True)
    confidence_rule_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confidence_rule_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    review_state: Mapped[str] = mapped_column(String(40), default="NOT_REVIEWED")

    source_locator_id: Mapped[str | None] = mapped_column(
        ForeignKey("source_locator.id"), nullable=True
    )
    extraction_record_id: Mapped[str | None] = mapped_column(
        ForeignKey("extraction_record.id"), nullable=True
    )
    calculation_id: Mapped[str | None] = mapped_column(
        ForeignKey("calculation.id"), nullable=True
    )
    verifiability: Mapped[str] = mapped_column(String(60), default="NORMAL")  # A22
    supersedes_id: Mapped[str | None] = mapped_column(
        ForeignKey("value_revision.id"), nullable=True
    )
    created_by: Mapped[str] = mapped_column(String(40), default="SYSTEM")
    researcher_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class Job(Base):
    """Durable at-least-once job (doc 00 A11, doc 04 §2)."""

    __tablename__ = "job"
    __table_args__ = (UniqueConstraint("idempotency_key"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    stage_id: Mapped[str] = mapped_column(String(60), index=True)
    work_item_ref: Mapped[str] = mapped_column(String(200))
    idempotency_key: Mapped[str] = mapped_column(String(300))
    input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    state: Mapped[str] = mapped_column(String(20), default="QUEUED", index=True)
    attempt: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    available_at: Mapped[dt.datetime] = mapped_column(default=_now)
    lease_owner: Mapped[str | None] = mapped_column(String(100), nullable=True)
    lease_expires_at: Mapped[dt.datetime | None] = mapped_column(nullable=True)
    parent_job_id: Mapped[str | None] = mapped_column(ForeignKey("job.id"), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)
    finished_at: Mapped[dt.datetime | None] = mapped_column(nullable=True)


class StageState(Base):
    """Domain conclusion of a stage for a work item (doc 04 §3)."""

    __tablename__ = "stage_state"
    __table_args__ = (UniqueConstraint("stage_id", "work_item_ref"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    stage_id: Mapped[str] = mapped_column(String(60))
    work_item_ref: Mapped[str] = mapped_column(String(200))
    state: Mapped[str] = mapped_column(String(40))
    detail: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    job_id: Mapped[str | None] = mapped_column(ForeignKey("job.id"), nullable=True)
    updated_at: Mapped[dt.datetime] = mapped_column(default=_now, onupdate=_now)


class WorkflowIssue(Base):
    """Researcher-facing 'a step could not be completed' (doc 00 A4/O3)."""

    __tablename__ = "workflow_issue"
    __table_args__ = (
        # At most one OPEN issue per (work item × issue type) — doc 00 O3
        Index(
            "ix_workflow_issue_open_unique",
            "work_item_ref",
            "issue_type",
            unique=True,
            sqlite_where=text("state = 'OPEN'"),
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    issue_type: Mapped[str] = mapped_column(String(60))
    work_item_ref: Mapped[str] = mapped_column(String(200))
    stage_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(String(20), default="OPEN")
    first_seen: Mapped[dt.datetime] = mapped_column(default=_now)
    last_seen: Mapped[dt.datetime] = mapped_column(default=_now)
    resolved_at: Mapped[dt.datetime | None] = mapped_column(nullable=True)


class AuditFinding(Base):
    """Scientifically meaningful audit result (doc 05; kept strictly separate
    from workflow_issue). v1 scope: internal cross-representation findings."""

    __tablename__ = "audit_finding"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    finding_kind: Mapped[str] = mapped_column(String(40))  # CONTRADICTION | ...
    taxonomy_code: Mapped[str] = mapped_column(String(60))
    severity: Mapped[str] = mapped_column(String(20), default="REVIEW")
    certainty: Mapped[str] = mapped_column(String(20), default="POSSIBLE")
    review_status: Mapped[str] = mapped_column(String(30), default="SYSTEM_FLAGGED")
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text)
    document_id: Mapped[str | None] = mapped_column(ForeignKey("document.id"), nullable=True)
    evidence: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # both sides + provenance
    detected_by: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class ExternalCallLog(Base):
    """Every external service call: privacy surface (§58) + cost tracking (§63).
    Append-only. An API failure is recorded here, never as domain fact."""

    __tablename__ = "external_call_log"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str | None] = mapped_column(ForeignKey("project.id"), nullable=True, index=True)
    provider: Mapped[str] = mapped_column(String(60))
    model_role: Mapped[str | None] = mapped_column(String(40), nullable=True)
    model_id: Mapped[str | None] = mapped_column(String(100), nullable=True)  # concrete (A16)
    stage_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    purpose: Mapped[str] = mapped_column(String(200))
    payload_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    est_cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    outcome: Mapped[str] = mapped_column(String(40))  # OK | API_FAILURE | INVALID_OUTPUT | CACHE_HIT
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)


class CacheEntry(Base):
    """External-result cache (§62): keyed by content hash, timestamped,
    intentionally refreshable via `stale`."""

    __tablename__ = "cache_entry"
    __table_args__ = (UniqueConstraint("namespace", "key_hash"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    namespace: Mapped[str] = mapped_column(String(60))
    key_hash: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)
    stale: Mapped[bool] = mapped_column(default=False)


class ReviewEvent(Base):
    """Append-only researcher action log (§21; doc 02 §8)."""

    __tablename__ = "review_event"
    __table_args__ = (
        # A correction must reference what it replaced (§54, doc 02 §9)
        CheckConstraint(
            "action != 'CORRECT' OR previous_revision_id IS NOT NULL",
            name="ck_correct_requires_previous",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid7)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    actor: Mapped[str] = mapped_column(String(40), default="RESEARCHER")
    target_type: Mapped[str] = mapped_column(String(60))
    target_id: Mapped[str] = mapped_column(String(36))
    action: Mapped[str] = mapped_column(String(40))
    previous_revision_id: Mapped[str | None] = mapped_column(
        ForeignKey("value_revision.id"), nullable=True
    )
    new_revision_id: Mapped[str | None] = mapped_column(
        ForeignKey("value_revision.id"), nullable=True
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=_now)
