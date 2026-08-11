"""REST routes for the foundation + vertical slice."""

from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import Response
from sqlalchemy import select

from app.core.errors import AppError, not_found
from app.db.models import (
    DataPoint,
    Document,
    DocumentPage,
    Job,
    ParseArtifact,
    Project,
    SourceLocator,
    StageState,
    ValueRevision,
    WorkflowIssue,
)
from app.domain import documents as docsvc
from app.domain import provenance
from app.pipeline import queue
from app.pipeline.stages import parse_document as parse_stage
from app.pipeline.worker import drain

router = APIRouter()


def _session(request: Request):
    return request.app.state.session_factory()


def _settings(request: Request):
    return request.app.state.settings


# ---- projects ----------------------------------------------------------------


@router.post("/projects")
def create_project(request: Request, body: dict):
    name = (body.get("name") or "").strip()
    if not name:
        raise AppError(
            code="NAME_REQUIRED",
            what_happened="The project needs a name.",
            what_it_means="",
            next_steps=["Enter a short name, e.g. the meta-analysis citation."],
        )
    with _session(request) as session:
        project = Project(name=name)
        session.add(project)
        session.commit()
        return {"id": project.id, "name": project.name}


@router.get("/projects")
def list_projects(request: Request):
    with _session(request) as session:
        projects = session.scalars(select(Project).order_by(Project.created_at)).all()
        return [
            {"id": p.id, "name": p.name, "created_at": p.created_at.isoformat()}
            for p in projects
        ]


@router.get("/projects/{project_id}")
def get_project(request: Request, project_id: str):
    with _session(request) as session:
        project = session.get(Project, project_id)
        if project is None:
            raise not_found("project")
        docs = session.scalars(
            select(Document).where(Document.project_id == project_id)
        ).all()
        issues = session.scalars(
            select(WorkflowIssue).where(
                WorkflowIssue.project_id == project_id,
                WorkflowIssue.state == "OPEN",
            )
        ).all()
        return {
            "id": project.id,
            "name": project.name,
            "documents": [_doc_payload(session, d) for d in docs],
            "open_workflow_issues": [
                {
                    "id": i.id,
                    "issue_type": i.issue_type,
                    "detail": i.detail,
                    "work_item_ref": i.work_item_ref,
                }
                for i in issues
            ],
        }


# ---- documents ---------------------------------------------------------------


def _doc_payload(session, doc: Document) -> dict:
    states = session.scalars(
        select(StageState).where(StageState.work_item_ref == doc.id)
    ).all()
    return {
        "id": doc.id,
        "filename": doc.filename,
        "role": doc.role,
        "sha256": doc.sha256,
        "size_bytes": doc.size_bytes,
        "page_count": doc.page_count,
        "stages": {s.stage_id: {"state": s.state, "detail": s.detail} for s in states},
    }


@router.post("/projects/{project_id}/documents")
async def upload_document(request: Request, project_id: str, file: UploadFile):
    content = await file.read()
    settings = _settings(request)
    with _session(request) as session:
        if session.get(Project, project_id) is None:
            raise not_found("project")
        doc, created = docsvc.ingest_document(
            session,
            settings.documents_dir,
            project_id=project_id,
            filename=file.filename or "document.pdf",
            content=content,
        )
        queue.enqueue(
            session,
            project_id=project_id,
            stage_id=parse_stage.STAGE_ID,
            work_item_ref=doc.id,
            idempotency_key=parse_stage.idempotency_key(doc.sha256),
            input_hash=doc.sha256,
        )
        session.commit()
        return {"document": _doc_payload(session, doc), "created": created}


@router.get("/documents/{document_id}")
def get_document(request: Request, document_id: str):
    with _session(request) as session:
        doc = session.get(Document, document_id)
        if doc is None:
            raise not_found("document")
        return _doc_payload(session, doc)


@router.get("/documents/{document_id}/file")
def get_document_file(request: Request, document_id: str):
    settings = _settings(request)
    with _session(request) as session:
        doc = session.get(Document, document_id)
        if doc is None:
            raise not_found("document")
        content = docsvc.read_verified(settings.documents_dir, doc)
        return Response(content=content, media_type="application/pdf")


@router.get("/documents/{document_id}/pages")
def get_document_pages(request: Request, document_id: str):
    with _session(request) as session:
        pages = session.scalars(
            select(DocumentPage)
            .where(DocumentPage.document_id == document_id)
            .order_by(DocumentPage.page_number)
        ).all()
        return [
            {
                "page_number": p.page_number,
                "width": p.width,
                "height": p.height,
                "rotation": p.rotation,
            }
            for p in pages
        ]


@router.get("/documents/{document_id}/text")
def get_document_text(request: Request, document_id: str, page: int | None = None):
    """Extracted text spans with normalized bboxes (vertical slice evidence)."""
    with _session(request) as session:
        artifact = session.scalar(
            select(ParseArtifact)
            .where(
                ParseArtifact.document_id == document_id,
                ParseArtifact.kind == "TEXT_SPANS",
            )
            .order_by(ParseArtifact.created_at.desc())
        )
        if artifact is None:
            raise AppError(
                code="NOT_PARSED_YET",
                what_happened="This document has not been read yet.",
                what_it_means="Text extraction is still in progress or has not started.",
                next_steps=["Wait a moment and refresh."],
                http_status=409,
            )
        pages = artifact.payload["pages"]
        if page is not None:
            pages = [p for p in pages if p["page_number"] == page]
        return {
            "parser_id": artifact.parser_id,
            "parser_version": artifact.parser_version,
            "pages": pages,
        }


# ---- provenance (foundation subset) -----------------------------------------


@router.get("/datapoints/{data_point_id}/provenance")
def get_provenance(request: Request, data_point_id: str):
    with _session(request) as session:
        dp = session.get(DataPoint, data_point_id)
        if dp is None:
            raise not_found("value")
        revisions = provenance.get_revisions(session, data_point_id)
        payload = []
        for r in revisions:
            locator = (
                session.get(SourceLocator, r.source_locator_id)
                if r.source_locator_id
                else None
            )
            payload.append(
                {
                    "revision_no": r.revision_no,
                    "value_text": r.value_text,
                    "value_numeric": r.value_numeric,
                    "scientific_basis": r.scientific_basis,
                    "acquisition_method": r.acquisition_method,
                    "confidence": r.confidence,
                    "review_state": r.review_state,
                    "created_by": r.created_by,
                    "note": r.researcher_note,
                    "is_current": r.id == dp.current_revision_id,
                    "source": (
                        {
                            "document_id": locator.document_id,
                            "page_number": locator.page_number,
                            "bbox_norm": locator.bbox_norm,
                            "source_text": locator.source_text,
                        }
                        if locator
                        else None
                    ),
                }
            )
        return {"data_point_id": dp.id, "quantity_kind": dp.quantity_kind, "revisions": payload}


@router.post("/datapoints/{data_point_id}/correct")
def correct_datapoint(request: Request, data_point_id: str, body: dict):
    with _session(request) as session:
        rev = provenance.correct_value(
            session,
            data_point_id,
            value_text=str(body.get("value_text", "")),
            value_numeric=body.get("value_numeric"),
            note=body.get("note"),
        )
        session.commit()
        return {"revision_no": rev.revision_no, "review_state": rev.review_state}


@router.post("/datapoints/{data_point_id}/verify")
def verify_datapoint(request: Request, data_point_id: str, body: dict | None = None):
    with _session(request) as session:
        rev = provenance.verify_value(
            session, data_point_id, note=(body or {}).get("note")
        )
        session.commit()
        return {"revision_no": rev.revision_no, "review_state": rev.review_state}


@router.post("/datapoints/{data_point_id}/restore")
def restore_datapoint(request: Request, data_point_id: str, body: dict):
    with _session(request) as session:
        rev = provenance.restore_revision(
            session, data_point_id, int(body["revision_no"]), note=body.get("note")
        )
        session.commit()
        return {"revision_no": rev.revision_no, "review_state": rev.review_state}


# ---- pipeline (dev/test helpers; hidden behind Advanced in the UI) ----------


@router.post("/dev/drain")
def dev_drain(request: Request):
    settings = _settings(request)
    with _session(request) as session:
        n = drain(session, settings.documents_dir)
        return {"processed": n}


@router.get("/projects/{project_id}/jobs")
def list_jobs(request: Request, project_id: str):
    with _session(request) as session:
        jobs = session.scalars(
            select(Job).where(Job.project_id == project_id).order_by(Job.created_at)
        ).all()
        return [
            {
                "id": j.id,
                "stage_id": j.stage_id,
                "state": j.state,
                "attempt": j.attempt,
                "work_item_ref": j.work_item_ref,
                "error": j.error,
            }
            for j in jobs
        ]
