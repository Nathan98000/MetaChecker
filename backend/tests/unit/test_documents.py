"""Immutable document identity (doc 02 §2)."""

import hashlib

import pytest

from app.core.errors import AppError
from app.domain.documents import document_path, ingest_document, read_verified


def test_ingest_is_content_addressed_and_deduplicated(session, project, documents_dir):
    content = b"%PDF-1.4 test content"
    doc1, created1 = ingest_document(
        session, documents_dir, project_id=project.id, filename="a.pdf", content=content
    )
    doc2, created2 = ingest_document(
        session, documents_dir, project_id=project.id, filename="b.pdf", content=content
    )
    session.commit()
    assert created1 and not created2
    assert doc1.id == doc2.id  # identical bytes → one document row
    assert doc1.sha256 == hashlib.sha256(content).hexdigest()


def test_stored_file_matches_uploaded_bytes(session, project, documents_dir):
    content = b"%PDF-1.4 original evidence"
    doc, _ = ingest_document(
        session, documents_dir, project_id=project.id, filename="a.pdf", content=content
    )
    session.commit()
    assert read_verified(documents_dir, doc) == content


def test_modification_of_stored_file_is_detected(session, project, documents_dir):
    content = b"%PDF-1.4 original evidence"
    doc, _ = ingest_document(
        session, documents_dir, project_id=project.id, filename="a.pdf", content=content
    )
    session.commit()
    path = document_path(documents_dir, doc)
    path.chmod(0o644)
    path.write_bytes(b"%PDF-1.4 TAMPERED")
    with pytest.raises(AppError) as err:
        read_verified(documents_dir, doc)
    assert err.value.code == "DOCUMENT_STORE_CORRUPTED"


def test_store_file_is_readonly(session, project, documents_dir):
    doc, _ = ingest_document(
        session, documents_dir, project_id=project.id, filename="a.pdf", content=b"%PDF-1.4 x"
    )
    session.commit()
    mode = document_path(documents_dir, doc).stat().st_mode & 0o777
    assert mode == 0o444
