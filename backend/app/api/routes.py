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
        import os

        from app.pipeline.stages import (
            assemble_tables,
            detect_figures,
            extract_figure_vision,
            identify_analyses,
            reconcile_representations,
        )

        stages_to_run = [parse_stage, detect_figures, assemble_tables]
        if os.environ.get("ANTHROPIC_API_KEY"):
            stages_to_run.append(extract_figure_vision)
        stages_to_run.append(reconcile_representations)
        stages_to_run.append(identify_analyses)
        for mod in stages_to_run:
            queue.enqueue(
                session,
                project_id=project_id,
                stage_id=mod.STAGE_ID,
                work_item_ref=doc.id,
                idempotency_key=mod.idempotency_key(doc.sha256),
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


# ---- published data / reconciliation / findings (internal audit v1) ---------


def _load_records(session, document_id: str) -> list[dict]:
    artifact = session.scalar(
        select(ParseArtifact)
        .where(ParseArtifact.document_id == document_id,
               ParseArtifact.kind == "TABLE_RECORDS")
        .order_by(ParseArtifact.created_at.desc())
    )
    if artifact is None:
        raise AppError(
            code="NOT_ASSEMBLED_YET",
            what_happened="Published data rows have not been assembled yet.",
            what_it_means="The document was parsed but table assembly has not run.",
            next_steps=["Run processing again, then refresh."],
            http_status=409,
        )
    return artifact.payload["records"]


def _cell_keys_for(document_id: str, records: list[dict]) -> list[dict]:
    """Per record: field → stable cell key (occurrence-disambiguated)."""
    from app.domain.corrections import CORRECTABLE_FIELDS, cell_key

    seen: dict[tuple, int] = {}
    keys = []
    for r in records:
        row_keys = {}
        for field in CORRECTABLE_FIELDS:
            value = r.get(field)
            if value is None or value == "":
                continue
            identity = (r.get("page_number"), r.get("study_label"), field, str(value))
            occurrence = seen.get(identity, 0)
            seen[identity] = occurrence + 1
            row_keys[field] = cell_key(document_id, r.get("page_number") or 0,
                                       r.get("study_label") or "", field,
                                       str(value), occurrence)
        keys.append(row_keys)
    return keys


@router.get("/documents/{document_id}/records")
def get_table_records(request: Request, document_id: str):
    """Assembled published-data rows with cell provenance, stable cell keys,
    and any researcher corrections/verifications overlaid."""
    from app.domain.corrections import overlay_for_document

    with _session(request) as session:
        records = _load_records(session, document_id)
        keys = _cell_keys_for(document_id, records)
        overlay = overlay_for_document(session, document_id)
        out = []
        for r, row_keys in zip(records, keys):
            entry = dict(r)
            entry["cell_keys"] = row_keys
            entry["review"] = {
                field: overlay[k] for field, k in row_keys.items() if k in overlay
            }
            out.append(entry)
        return {"records": out}


@router.post("/documents/{document_id}/cells/{action}")
def act_on_cell(request: Request, document_id: str, action: str, body: dict):
    """Researcher verify/correct on an extracted cell. The row is resolved
    server-side by index in the current records; corrections append revisions
    (originals preserved; undo via /datapoints/{id}/restore)."""
    from app.domain import corrections

    if action not in ("correct", "verify"):
        raise not_found("action")
    with _session(request) as session:
        records = _load_records(session, document_id)
        index = int(body.get("record_index", -1))
        field = body.get("field", "")
        if not (0 <= index < len(records)):
            raise not_found("record")
        row = records[index]
        keys = _cell_keys_for(document_id, records)[index]
        if field not in keys:
            raise AppError(
                code="NO_SUCH_CELL",
                what_happened="That cell has no extracted value to act on.",
                what_it_means="Only cells with extracted values can be verified or corrected.",
                next_steps=["Pick a populated cell."],
            )
        if action == "correct":
            value = str(body.get("corrected_value", "")).strip()
            if not value:
                raise AppError(
                    code="VALUE_REQUIRED",
                    what_happened="No corrected value was provided.",
                    what_it_means="",
                    next_steps=["Enter the value exactly as printed in the source."],
                )
            result = corrections.correct_cell(
                session, document_id, key=keys[field], field=field, row=row,
                corrected_value=value, note=body.get("note"),
            )
        else:
            result = corrections.verify_cell(
                session, document_id, key=keys[field], field=field, row=row,
                note=body.get("note"),
            )
        session.commit()
        return result


@router.get("/documents/{document_id}/analyses")
def get_analyses(request: Request, document_id: str):
    """Identified analyses with pooled values and effect-row memberships."""
    with _session(request) as session:
        artifact = session.scalar(
            select(ParseArtifact)
            .where(ParseArtifact.document_id == document_id,
                   ParseArtifact.kind == "ANALYSES")
            .order_by(ParseArtifact.created_at.desc())
        )
        return {"analyses": artifact.payload["analyses"] if artifact else []}


@router.get("/documents/{document_id}/reconciliation")
def get_reconciliation(request: Request, document_id: str):
    with _session(request) as session:
        artifact = session.scalar(
            select(ParseArtifact)
            .where(ParseArtifact.document_id == document_id,
                   ParseArtifact.kind == "RECONCILIATION")
            .order_by(ParseArtifact.created_at.desc())
        )
        return {"pairs": artifact.payload["pairs"] if artifact else []}


@router.get("/projects/{project_id}/findings")
def list_findings(request: Request, project_id: str):
    from app.db.models import AuditFinding

    with _session(request) as session:
        findings = session.scalars(
            select(AuditFinding).where(AuditFinding.project_id == project_id)
            .order_by(AuditFinding.created_at)
        ).all()
        return [
            {
                "id": f.id, "kind": f.finding_kind, "taxonomy": f.taxonomy_code,
                "severity": f.severity, "certainty": f.certainty,
                "review_status": f.review_status, "title": f.title,
                "description": f.description, "document_id": f.document_id,
                "evidence": f.evidence,
            }
            for f in findings
        ]


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
