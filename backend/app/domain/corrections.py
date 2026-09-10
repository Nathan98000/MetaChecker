"""Researcher correction workflow over extracted records (docs 03/A18, §21).

Extracted rows live in parse artifacts; the first researcher action on a cell
(verify or correct) materializes it as a DataPoint whose revision #1 is the
VERBATIM extracted value with full source provenance (locator with the cell's
bbox, extraction record with the acquisition method). Corrections then append
revisions through the provenance service — originals unlosable, review events
logged, undo = restore.

Cell identity is content-derived (document, page, row label, field, original
value, occurrence index) so it is stable across re-parses that don't change
the value, and deliberately NOT stable across value-changing re-extraction —
a changed extraction is a new fact, not the old cell.
"""

import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError, not_found
from app.db.models import (
    DataPoint,
    Document,
    ExtractedCell,
    ExtractionRecord,
    SourceLocator,
    ValueRevision,
)
from app.domain import provenance

CORRECTABLE_FIELDS = {
    "effect_value", "ci_lower", "ci_upper", "weight",
    "events_treatment", "events_control", "n_treatment", "n_control",
    "study_label",
}


def cell_key(document_id: str, page: int, row_label: str, field: str,
             original_value: str, occurrence: int = 0) -> str:
    h = hashlib.sha256()
    for part in (document_id, str(page), row_label or "", field,
                 original_value or "", str(occurrence)):
        h.update(part.encode())
        h.update(b"\x00")
    return h.hexdigest()


def _materialize(
    session: Session, doc: Document, *, key: str, field: str, row: dict,
) -> ExtractedCell:
    existing = session.scalar(
        select(ExtractedCell).where(
            ExtractedCell.document_id == doc.id, ExtractedCell.cell_key == key
        )
    )
    if existing is not None:
        return existing

    bbox = (row.get("cell_bboxes") or {}).get(
        "effect" if field != "study_label" else "label"
    ) or row.get("line_bbox")
    locator = SourceLocator(
        project_id=doc.project_id,
        document_id=doc.id,
        page_number=row.get("page_number"),
        source_type=row.get("source_type") or (
            "FOREST_PLOT" if row.get("acquisition_method") == "VISION" else "TABLE"),
        row_label=row.get("study_label"),
        source_text=str(row.get(field) or ""),
        bbox_native=bbox,
    )
    session.add(locator)
    method = row.get("acquisition_method") or "LAYOUT_EXTRACTION"
    extraction = ExtractionRecord(
        project_id=doc.project_id,
        acquisition_method=method,
        extractor_id="layout_table_assembler" if method == "LAYOUT_EXTRACTION"
        else "vision_forest_extractor",
        extractor_version="1",
        model_id=row.get("model_id"),
    )
    session.add(extraction)
    session.flush()

    original = row.get(field)
    dp = provenance.create_data_point(
        session,
        project_id=doc.project_id,
        quantity_kind={"effect_value": "EFFECT_SIZE", "ci_lower": "CI_LOWER",
                       "ci_upper": "CI_UPPER", "weight": "WEIGHT",
                       "study_label": "LABEL"}.get(field, field.upper()),
        value_text=str(original) if original is not None else "",
        value_numeric=None,
        scientific_basis="SOURCE_REPORTED",
        acquisition_method=method,
        source_locator_id=locator.id,
        extraction_record_id=extraction.id,
        confidence="MEDIUM" if method == "VISION" else "HIGH",
        confidence_rule_id="vision_uncorroborated_v1" if method == "VISION"
        else "layout_extraction_v1",
        confidence_rule_version="1",
    )
    cell = ExtractedCell(
        project_id=doc.project_id, document_id=doc.id, cell_key=key,
        field=field, row_label=row.get("study_label") or "", data_point_id=dp.id,
    )
    session.add(cell)
    session.flush()
    return cell


def correct_cell(session: Session, document_id: str, *, key: str, field: str,
                 row: dict, corrected_value: str, note: str | None) -> dict:
    if field not in CORRECTABLE_FIELDS:
        raise AppError(
            code="FIELD_NOT_CORRECTABLE",
            what_happened=f"'{field}' cannot be corrected here.",
            what_it_means="Only extracted data cells support corrections.",
            next_steps=["Correct one of the value fields instead."],
        )
    doc = session.get(Document, document_id)
    if doc is None:
        raise not_found("document")
    cell = _materialize(session, doc, key=key, field=field, row=row)
    revision = provenance.correct_value(
        session, cell.data_point_id,
        value_text=corrected_value, value_numeric=None, note=note,
    )
    return {"data_point_id": cell.data_point_id, "revision_no": revision.revision_no}


def verify_cell(session: Session, document_id: str, *, key: str, field: str,
                row: dict, note: str | None) -> dict:
    doc = session.get(Document, document_id)
    if doc is None:
        raise not_found("document")
    cell = _materialize(session, doc, key=key, field=field, row=row)
    revision = provenance.verify_value(session, cell.data_point_id, note=note)
    return {"data_point_id": cell.data_point_id, "revision_no": revision.revision_no}


def overlay_for_document(session: Session, document_id: str) -> dict[str, dict]:
    """cell_key → current researcher state, for overlaying onto records."""
    cells = session.scalars(
        select(ExtractedCell).where(ExtractedCell.document_id == document_id)
    ).all()
    overlay: dict[str, dict] = {}
    for cell in cells:
        dp = session.get(DataPoint, cell.data_point_id)
        head = session.get(ValueRevision, dp.current_revision_id)
        first = provenance.get_revisions(session, dp.id)[0]
        overlay[cell.cell_key] = {
            "field": cell.field,
            "data_point_id": dp.id,
            "review_state": head.review_state,
            "current_value": head.value_text,
            "original_value": first.value_text,
            "corrected": head.value_text != first.value_text,
        }
    return overlay
