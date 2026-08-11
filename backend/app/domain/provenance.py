"""Provenance service (doc 03).

All value mutation flows through here: first revisions carry the verbatim
value_text; corrections, verifications, and restores append revisions and
never modify history. Review events record every researcher action with the
previous revision id, so originals are unlosable by construction.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import invalid_provenance, not_found
from app.db.models import DataPoint, ReviewEvent, ValueRevision

_HUMAN_STATES = {"VERIFIED", "CORRECTED", "MARKED_UNCERTAIN", "EXCLUDED"}


def create_data_point(
    session: Session,
    *,
    project_id: str,
    quantity_kind: str,
    value_text: str,
    value_numeric: float | None,
    scientific_basis: str,
    acquisition_method: str | None,
    source_locator_id: str | None = None,
    extraction_record_id: str | None = None,
    calculation_id: str | None = None,
    confidence: str | None = None,
    confidence_rule_id: str | None = None,
    confidence_rule_version: str | None = None,
    review_state: str = "NOT_REVIEWED",
) -> DataPoint:
    if scientific_basis in ("SOURCE_REPORTED", "INFERRED") and not source_locator_id:
        raise invalid_provenance(
            f"A {scientific_basis} value requires a source location."
        )
    if scientific_basis == "DERIVED" and not calculation_id:
        raise invalid_provenance("A derived value requires its calculation record.")

    dp = DataPoint(project_id=project_id, quantity_kind=quantity_kind)
    session.add(dp)
    session.flush()
    rev = ValueRevision(
        project_id=project_id,
        data_point_id=dp.id,
        revision_no=1,
        value_text=value_text,
        value_numeric=value_numeric,
        scientific_basis=scientific_basis,
        acquisition_method=acquisition_method,
        confidence=confidence,
        confidence_rule_id=confidence_rule_id,
        confidence_rule_version=confidence_rule_version,
        review_state=review_state,
        source_locator_id=source_locator_id,
        extraction_record_id=extraction_record_id,
        calculation_id=calculation_id,
        created_by="SYSTEM",
    )
    session.add(rev)
    session.flush()
    dp.current_revision_id = rev.id
    return dp


def get_revisions(session: Session, data_point_id: str) -> list[ValueRevision]:
    return list(
        session.scalars(
            select(ValueRevision)
            .where(ValueRevision.data_point_id == data_point_id)
            .order_by(ValueRevision.revision_no)
        )
    )


def _head(session: Session, dp: DataPoint) -> ValueRevision:
    head = session.get(ValueRevision, dp.current_revision_id)
    if head is None:
        raise not_found("value revision")
    return head


def _append(
    session: Session,
    dp: DataPoint,
    base: ValueRevision,
    *,
    review_state: str,
    value_text: str | None = None,
    value_numeric: float | None = None,
    note: str | None = None,
    actor: str = "RESEARCHER",
) -> ValueRevision:
    """Append a revision derived from `base`, moving only the head pointer.

    Provenance links (locator/extraction/calculation) and scientific basis are
    carried over unchanged: human review changes review_state, never the
    epistemic category of the value (doc 00 A2/A3).
    """
    last_no = get_revisions(session, dp.id)[-1].revision_no
    rev = ValueRevision(
        project_id=dp.project_id,
        data_point_id=dp.id,
        revision_no=last_no + 1,
        value_text=value_text if value_text is not None else base.value_text,
        value_numeric=value_numeric if value_numeric is not None else base.value_numeric,
        value_normalized=base.value_normalized,
        unit=base.unit,
        scientific_basis=base.scientific_basis,
        acquisition_method=base.acquisition_method,
        confidence=base.confidence,
        confidence_rule_id=base.confidence_rule_id,
        confidence_rule_version=base.confidence_rule_version,
        review_state=review_state,
        source_locator_id=base.source_locator_id,
        extraction_record_id=base.extraction_record_id,
        calculation_id=base.calculation_id,
        verifiability=base.verifiability,
        supersedes_id=dp.current_revision_id,
        created_by=actor,
        researcher_note=note,
    )
    session.add(rev)
    session.flush()
    dp.current_revision_id = rev.id
    return rev


def verify_value(session: Session, data_point_id: str, note: str | None = None) -> ValueRevision:
    dp = session.get(DataPoint, data_point_id)
    if dp is None:
        raise not_found("value")
    prev = _head(session, dp)
    rev = _append(session, dp, prev, review_state="VERIFIED", note=note)
    session.add(
        ReviewEvent(
            project_id=dp.project_id,
            target_type="data_point",
            target_id=dp.id,
            action="VERIFY",
            previous_revision_id=prev.id,
            new_revision_id=rev.id,
            note=note,
        )
    )
    return rev


def correct_value(
    session: Session,
    data_point_id: str,
    *,
    value_text: str,
    value_numeric: float | None,
    note: str | None = None,
) -> ValueRevision:
    dp = session.get(DataPoint, data_point_id)
    if dp is None:
        raise not_found("value")
    prev = _head(session, dp)
    rev = _append(
        session,
        dp,
        prev,
        review_state="CORRECTED",
        value_text=value_text,
        value_numeric=value_numeric,
        note=note,
    )
    session.add(
        ReviewEvent(
            project_id=dp.project_id,
            target_type="data_point",
            target_id=dp.id,
            action="CORRECT",
            previous_revision_id=prev.id,
            new_revision_id=rev.id,
            note=note,
        )
    )
    return rev


def restore_revision(
    session: Session, data_point_id: str, revision_no: int, note: str | None = None
) -> ValueRevision:
    """Undo = append a new revision equal to an older one (§21)."""
    dp = session.get(DataPoint, data_point_id)
    if dp is None:
        raise not_found("value")
    prev = _head(session, dp)
    target = next(
        (r for r in get_revisions(session, dp.id) if r.revision_no == revision_no),
        None,
    )
    if target is None:
        raise not_found("revision")
    rev = _append(
        session,
        dp,
        target,
        review_state=target.review_state,
        value_text=target.value_text,
        value_numeric=target.value_numeric,
        note=note,
    )
    session.add(
        ReviewEvent(
            project_id=dp.project_id,
            target_type="data_point",
            target_id=dp.id,
            action="RESTORE",
            previous_revision_id=prev.id,
            new_revision_id=rev.id,
            note=note,
        )
    )
    return rev
