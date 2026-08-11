"""Immutable document identity and storage (docs 02 §2, 01 §3).

Files live in a content-addressed store: documents/<sha256[:2]>/<sha256>.
A stored file is never rewritten; re-uploading identical bytes returns the
existing document row. Reading always re-verifies nothing was modified.
"""

import hashlib
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError, not_found
from app.db.models import Document


def _store_path(documents_dir: Path, sha256: str) -> Path:
    return documents_dir / sha256[:2] / sha256


def ingest_document(
    session: Session,
    documents_dir: Path,
    *,
    project_id: str,
    filename: str,
    content: bytes,
    role: str = "META_ANALYSIS",
    origin: str = "UPLOADED",
) -> tuple[Document, bool]:
    """Store bytes immutably; return (document, created)."""
    if not content:
        raise AppError(
            code="EMPTY_FILE",
            what_happened="The uploaded file was empty.",
            what_it_means="No document content was received.",
            next_steps=["Try uploading the PDF again."],
        )
    sha = hashlib.sha256(content).hexdigest()

    existing = session.scalar(
        select(Document).where(
            Document.project_id == project_id, Document.sha256 == sha
        )
    )
    if existing is not None:
        return existing, False

    path = _store_path(documents_dir, sha)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(content)
        tmp.rename(path)
        path.chmod(0o444)  # belt-and-braces: store files are read-only

    doc = Document(
        project_id=project_id,
        sha256=sha,
        filename=filename,
        role=role,
        origin=origin,
        size_bytes=len(content),
    )
    session.add(doc)
    session.flush()
    return doc, True


def document_path(documents_dir: Path, doc: Document) -> Path:
    path = _store_path(documents_dir, doc.sha256)
    if not path.exists():
        raise not_found("document file")
    return path


def read_verified(documents_dir: Path, doc: Document) -> bytes:
    """Read the stored file, re-verifying its content hash (immutability)."""
    content = document_path(documents_dir, doc).read_bytes()
    if hashlib.sha256(content).hexdigest() != doc.sha256:
        raise AppError(
            code="DOCUMENT_STORE_CORRUPTED",
            what_happened="A stored source document no longer matches its recorded fingerprint.",
            what_it_means=(
                "The original evidence file appears to have been modified or "
                "damaged outside the application."
            ),
            next_steps=[
                "Re-upload the original PDF.",
                "Restore the project folder from a backup.",
            ],
            http_status=500,
        )
    return content
