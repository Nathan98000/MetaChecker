"""S02 parse_document — baseline PyMuPDF structural parse (doc 04 §5).

Extracts per-page geometry and text spans with normalized bounding boxes
(doc 00 A9) into a TEXT_SPANS parse artifact. This is the foundation slice's
parser; the orchestration layer (A12) grows around it in Phase 1.

Idempotent: pages are upserted by (document_id, page_number); the artifact is
keyed by (document_id, parser_id, parser_version, kind, input_hash), so
duplicate execution cannot duplicate records.
"""

import pymupdf
from sqlalchemy import select

from app.db.models import Document, DocumentPage, Job, ParseArtifact
from app.domain.documents import read_verified
from app.pipeline.registry import StageContext, StageResult, stage

PARSER_ID = "pymupdf_baseline"
PARSER_VERSION = "1"
STAGE_ID = "parse_document"


def idempotency_key(sha256: str) -> str:
    return f"{STAGE_ID}:{sha256}:{PARSER_ID}:{PARSER_VERSION}"


@stage(STAGE_ID)
def run(ctx: StageContext, job: Job) -> StageResult:
    doc_row = ctx.session.get(Document, job.work_item_ref)
    if doc_row is None:
        return StageResult(state="INSUFFICIENT_DATA", detail={"reason": "document row missing"})

    content = read_verified(ctx.documents_dir, doc_row)

    try:
        pdf = pymupdf.open(stream=content, filetype="pdf")
    except Exception as exc:
        return StageResult(
            state="DOCUMENT_UNREADABLE",
            detail={"reason": str(exc)[:500]},
            issue_type="DOCUMENT_UNREADABLE",
        )
    if pdf.needs_pass:
        return StageResult(
            state="DOCUMENT_UNREADABLE",
            detail={"reason": "PDF is password-protected"},
            issue_type="DOCUMENT_UNREADABLE",
        )

    pages_payload = []
    span_count = 0
    for page_index in range(pdf.page_count):
        page = pdf[page_index]
        rect = page.rect
        width, height = float(rect.width), float(rect.height)

        existing = ctx.session.scalar(
            select(DocumentPage).where(
                DocumentPage.document_id == doc_row.id,
                DocumentPage.page_number == page_index + 1,
            )
        )
        if existing is None:
            ctx.session.add(
                DocumentPage(
                    document_id=doc_row.id,
                    page_number=page_index + 1,
                    width=width,
                    height=height,
                    rotation=int(page.rotation),
                )
            )

        spans = []
        text_page = page.get_text("dict")
        for block in text_page.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    if not text.strip():
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    spans.append(
                        {
                            "text": text,
                            # normalized 0–1, origin top-left (A9)
                            "bbox_norm": [
                                round(x0 / width, 6),
                                round(y0 / height, 6),
                                round(x1 / width, 6),
                                round(y1 / height, 6),
                            ],
                            "bbox_native": [x0, y0, x1, y1],
                            "font_size": round(span.get("size", 0.0), 2),
                        }
                    )
        span_count += len(spans)
        pages_payload.append(
            {"page_number": page_index + 1, "width": width, "height": height, "spans": spans}
        )

    doc_row.page_count = pdf.page_count
    pdf.close()

    existing_artifact = ctx.session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.parser_id == PARSER_ID,
            ParseArtifact.parser_version == PARSER_VERSION,
            ParseArtifact.kind == "TEXT_SPANS",
            ParseArtifact.input_hash == doc_row.sha256,
        )
    )
    if existing_artifact is None:
        ctx.session.add(
            ParseArtifact(
                project_id=doc_row.project_id,
                document_id=doc_row.id,
                parser_id=PARSER_ID,
                parser_version=PARSER_VERSION,
                kind="TEXT_SPANS",
                payload={"pages": pages_payload},
                input_hash=doc_row.sha256,
            )
        )

    if span_count == 0:
        # Scanned/image-only PDF: geometry extracted, text not (OCR is a later
        # stage). Report what could and could not be extracted (A12).
        return StageResult(
            state="PARTIAL_SUCCESS",
            detail={
                "pages": doc_row.page_count,
                "spans": 0,
                "extracted": ["page geometry"],
                "not_extracted": ["text (no embedded text layer; OCR not yet run)"],
            },
        )
    return StageResult(
        state="SUCCESS", detail={"pages": doc_row.page_count, "spans": span_count}
    )
