"""S02b detect_figure_regions — deterministic figure-region detection.

Phase-1 increment 1a (evidence-driven: the frozen baseline shows forest-plot
values are 1–15% reachable natively because figures are raster/vector art).
This stage finds candidate figure regions and their captions so the vision
stage (increment 1b) has precise targets, instead of sending whole pages to a
model.

Detection is purely geometric (PyMuPDF):
- raster image blocks on each page,
- clusters of vector drawings large enough to be a figure,
- caption lines matching /^(Fig(ure)?\.?\s*\d+)/ near a region's bottom edge.

Output: FIGURE_REGION parse artifact (one per document) listing regions with
normalized bboxes, kind (RASTER_IMAGE | VECTOR_CLUSTER), caption text when
found, and whether the region's interior contains extractable text spans —
the evidence-quality signal that routes escalation (doc 00 A12: escalate only
when native evidence is insufficient).

Idempotent: artifact keyed by (document, parser, version, kind, input hash).
"""

import pymupdf
from sqlalchemy import select

from app.db.models import Document, Job, ParseArtifact
from app.domain.documents import read_verified
from app.pipeline.registry import StageContext, StageResult, stage

PARSER_ID = "figure_region_detector"
PARSER_VERSION = "1"
STAGE_ID = "detect_figure_regions"

MIN_REGION_FRACTION = 0.03  # region must cover ≥3% of page area
CAPTION_SEARCH_BAND = 0.12  # fraction of page height below region to search


def idempotency_key(sha256: str) -> str:
    return f"{STAGE_ID}:{sha256}:{PARSER_ID}:{PARSER_VERSION}"


def _norm(rect: pymupdf.Rect, width: float, height: float) -> list[float]:
    return [
        round(rect.x0 / width, 6),
        round(rect.y0 / height, 6),
        round(rect.x1 / width, 6),
        round(rect.y1 / height, 6),
    ]


def _cluster_rects(rects: list[pymupdf.Rect], gap: float) -> list[pymupdf.Rect]:
    """Merge overlapping/nearby rectangles into clusters (single-linkage)."""
    clusters: list[pymupdf.Rect] = []
    for rect in rects:
        grown = pymupdf.Rect(rect.x0 - gap, rect.y0 - gap, rect.x1 + gap, rect.y1 + gap)
        merged = None
        for i, c in enumerate(clusters):
            if grown.intersects(c):
                clusters[i] = c | rect
                merged = i
                break
        if merged is None:
            clusters.append(pymupdf.Rect(rect))
        else:
            # keep merging transitively
            changed = True
            while changed:
                changed = False
                for i in range(len(clusters)):
                    for j in range(i + 1, len(clusters)):
                        gi = pymupdf.Rect(
                            clusters[i].x0 - gap, clusters[i].y0 - gap,
                            clusters[i].x1 + gap, clusters[i].y1 + gap,
                        )
                        if gi.intersects(clusters[j]):
                            clusters[i] = clusters[i] | clusters[j]
                            del clusters[j]
                            changed = True
                            break
                    if changed:
                        break
    return clusters


def _find_caption(page: pymupdf.Page, region: pymupdf.Rect) -> str | None:
    band = pymupdf.Rect(
        0, region.y1, page.rect.width, min(page.rect.height, region.y1 + page.rect.height * CAPTION_SEARCH_BAND)
    )
    text = page.get_text("text", clip=band).strip()
    for line in text.splitlines():
        stripped = line.strip()
        low = stripped.lower()
        if low.startswith(("fig.", "fig ", "figure", "table")):
            return stripped[:300]
    return None


def detect_regions(pdf: pymupdf.Document) -> list[dict]:
    regions = []
    for page_index in range(pdf.page_count):
        page = pdf[page_index]
        width, height = float(page.rect.width), float(page.rect.height)
        page_area = width * height
        candidates: list[tuple[str, pymupdf.Rect]] = []

        # raster images
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") == 1:  # image block
                rect = pymupdf.Rect(block["bbox"])
                if rect.get_area() / page_area >= MIN_REGION_FRACTION:
                    candidates.append(("RASTER_IMAGE", rect))

        # vector drawing clusters
        # Hairline strokes (lines) have zero-area rects — inflate slightly so
        # they survive and cluster, rather than filtering on per-rect area.
        drawing_rects = []
        for d in page.get_drawings():
            if not d.get("rect"):
                continue
            r = pymupdf.Rect(d["rect"])
            if r.is_empty or r.is_infinite:
                r = pymupdf.Rect(r.x0 - 0.5, r.y0 - 0.5, r.x1 + 0.5, r.y1 + 0.5)
            drawing_rects.append(r)
        for cluster in _cluster_rects(drawing_rects, gap=8.0):
            if cluster.get_area() / page_area >= MIN_REGION_FRACTION:
                candidates.append(("VECTOR_CLUSTER", cluster))

        # merge raster/vector candidates that overlap into one region
        merged: list[tuple[str, pymupdf.Rect]] = []
        for kind, rect in candidates:
            placed = False
            for i, (mk, mr) in enumerate(merged):
                if rect.intersects(mr):
                    merged[i] = (mk if mk == kind else "MIXED", mr | rect)
                    placed = True
                    break
            if not placed:
                merged.append((kind, rect))

        for kind, rect in merged:
            interior_text = page.get_text("text", clip=rect).strip()
            regions.append(
                {
                    "page_number": page_index + 1,
                    "kind": kind,
                    "bbox_norm": _norm(rect, width, height),
                    "bbox_native": [rect.x0, rect.y0, rect.x1, rect.y1],
                    "caption": _find_caption(page, rect),
                    "interior_text_chars": len(interior_text),
                    # the escalation signal: a figure region with (almost) no
                    # extractable interior text needs vision interpretation
                    "needs_vision": len(interior_text) < 80,
                    "area_fraction": round(rect.get_area() / page_area, 4),
                }
            )
    return regions


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
    regions = detect_regions(pdf)
    pdf.close()

    existing = ctx.session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.parser_id == PARSER_ID,
            ParseArtifact.parser_version == PARSER_VERSION,
            ParseArtifact.kind == "FIGURE_REGION",
            ParseArtifact.input_hash == doc_row.sha256,
        )
    )
    if existing is None:
        ctx.session.add(
            ParseArtifact(
                project_id=doc_row.project_id,
                document_id=doc_row.id,
                parser_id=PARSER_ID,
                parser_version=PARSER_VERSION,
                kind="FIGURE_REGION",
                payload={"regions": regions},
                input_hash=doc_row.sha256,
            )
        )
    needs_vision = sum(1 for r in regions if r["needs_vision"])
    return StageResult(
        state="SUCCESS",
        detail={
            "regions": len(regions),
            "needs_vision": needs_vision,
            "extracted": ["figure regions", "captions", "escalation signals"],
        },
    )
