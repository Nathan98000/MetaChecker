"""Provenance invariants (doc 08 §2): originals unlosable, four-dimension
integrity, schema-enforced provenance requirements."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.errors import AppError
from app.db.models import DataPoint, ReviewEvent, SourceLocator, ValueRevision
from app.domain import provenance


def _locator(session, project, documents_dir=None, doc=None):
    from app.domain.documents import ingest_document

    if doc is None:
        doc, _ = ingest_document(
            session,
            documents_dir,
            project_id=project.id,
            filename="meta.pdf",
            content=b"%PDF-1.4 fake",
        )
    loc = SourceLocator(
        project_id=project.id,
        document_id=doc.id,
        page_number=14,
        source_type="FOREST_PLOT",
        source_text="-0.43 [-0.71, -0.15]",
        bbox_norm=[0.1, 0.2, 0.4, 0.22],
    )
    session.add(loc)
    session.flush()
    return loc


def _make_dp(session, project, documents_dir):
    loc = _locator(session, project, documents_dir)
    dp = provenance.create_data_point(
        session,
        project_id=project.id,
        quantity_kind="EFFECT_SIZE",
        value_text="-0.43",
        value_numeric=-0.43,
        scientific_basis="SOURCE_REPORTED",
        acquisition_method="EMBEDDED_TEXT",
        source_locator_id=loc.id,
        confidence="HIGH",
    )
    session.commit()
    return dp


def test_first_revision_is_verbatim(session, project, documents_dir):
    dp = _make_dp(session, project, documents_dir)
    revs = provenance.get_revisions(session, dp.id)
    assert len(revs) == 1
    assert revs[0].value_text == "-0.43"
    assert revs[0].revision_no == 1


def test_unprovenanced_source_value_is_rejected_by_service(session, project):
    with pytest.raises(AppError) as err:
        provenance.create_data_point(
            session,
            project_id=project.id,
            quantity_kind="EFFECT_SIZE",
            value_text="-0.43",
            value_numeric=-0.43,
            scientific_basis="SOURCE_REPORTED",
            acquisition_method="EMBEDDED_TEXT",
        )
    assert err.value.code == "INVALID_PROVENANCE"


def test_unprovenanced_source_value_is_rejected_by_schema(session, project):
    """Even bypassing the service, the CHECK constraint refuses the row."""
    dp = DataPoint(project_id=project.id, quantity_kind="EFFECT_SIZE")
    session.add(dp)
    session.flush()
    session.add(
        ValueRevision(
            project_id=project.id,
            data_point_id=dp.id,
            revision_no=1,
            value_text="-0.43",
            scientific_basis="SOURCE_REPORTED",
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_derived_requires_calculation_by_schema(session, project):
    dp = DataPoint(project_id=project.id, quantity_kind="SE")
    session.add(dp)
    session.flush()
    session.add(
        ValueRevision(
            project_id=project.id,
            data_point_id=dp.id,
            revision_no=1,
            value_text="0.1327",
            scientific_basis="DERIVED",
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_correction_preserves_original_and_logs_event(session, project, documents_dir):
    dp = _make_dp(session, project, documents_dir)
    provenance.correct_value(
        session, dp.id, value_text="-0.34", value_numeric=-0.34, note="digits transposed"
    )
    session.commit()

    revs = provenance.get_revisions(session, dp.id)
    assert [r.revision_no for r in revs] == [1, 2]
    assert revs[0].value_text == "-0.43"  # original intact
    assert revs[1].value_text == "-0.34"
    assert revs[1].review_state == "CORRECTED"
    assert revs[1].supersedes_id == revs[0].id

    event = session.scalar(select(ReviewEvent).where(ReviewEvent.action == "CORRECT"))
    assert event is not None
    assert event.previous_revision_id == revs[0].id
    assert event.new_revision_id == revs[1].id


def test_verification_does_not_change_scientific_basis(session, project, documents_dir):
    dp = _make_dp(session, project, documents_dir)
    rev = provenance.verify_value(session, dp.id)
    session.commit()
    assert rev.review_state == "VERIFIED"
    assert rev.scientific_basis == "SOURCE_REPORTED"  # A2/A3
    assert rev.source_locator_id is not None  # provenance carried over


def test_restore_appends_rather_than_rewrites(session, project, documents_dir):
    dp = _make_dp(session, project, documents_dir)
    provenance.correct_value(session, dp.id, value_text="-0.34", value_numeric=-0.34)
    provenance.restore_revision(session, dp.id, revision_no=1)
    session.commit()

    revs = provenance.get_revisions(session, dp.id)
    assert [r.revision_no for r in revs] == [1, 2, 3]
    assert revs[2].value_text == "-0.43"  # restored value
    head = session.get(DataPoint, dp.id).current_revision_id
    assert head == revs[2].id
    # full history still replayable
    assert [r.value_text for r in revs] == ["-0.43", "-0.34", "-0.43"]


def test_provenance_survives_arbitrary_action_sequence(session, project, documents_dir):
    dp = _make_dp(session, project, documents_dir)
    provenance.verify_value(session, dp.id)
    provenance.correct_value(session, dp.id, value_text="-0.35", value_numeric=-0.35)
    provenance.restore_revision(session, dp.id, revision_no=1)
    provenance.correct_value(session, dp.id, value_text="-0.36", value_numeric=-0.36)
    session.commit()
    revs = provenance.get_revisions(session, dp.id)
    assert revs[0].value_text == "-0.43"
    assert all(r.source_locator_id == revs[0].source_locator_id for r in revs)
    assert all(r.scientific_basis == "SOURCE_REPORTED" for r in revs)
