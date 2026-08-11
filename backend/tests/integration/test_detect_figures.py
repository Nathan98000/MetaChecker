"""Figure-region detection (Phase-1 increment 1a) against real corpus PDFs
and synthetic fixtures."""

from pathlib import Path

import pymupdf
import pytest

from app.pipeline.stages.detect_figures import detect_regions

CORPUS = Path(__file__).resolve().parents[3] / "corpus" / "gold"


def _open(path: Path) -> pymupdf.Document:
    return pymupdf.open(str(path))


def test_synthetic_page_with_image_region():
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((72, 60), "Some body text before the figure", fontsize=11)
    # draw a large vector "figure" (axis + boxes), no text inside
    for y in range(200, 420, 24):
        page.draw_line(pymupdf.Point(100, y), pymupdf.Point(480, y), width=1)
        page.draw_rect(pymupdf.Rect(280 + (y % 48), y - 4, 292 + (y % 48), y + 4), fill=(0, 0, 0))
    page.draw_line(pymupdf.Point(290, 190), pymupdf.Point(290, 430), width=1)
    page.insert_text((100, 450), "Figure 2 Forest plot of the association", fontsize=9)

    regions = detect_regions(doc)
    doc.close()
    assert len(regions) >= 1
    figure = max(regions, key=lambda r: r["area_fraction"])
    assert figure["kind"] in ("VECTOR_CLUSTER", "MIXED")
    assert figure["needs_vision"] is True
    assert figure["caption"] and figure["caption"].startswith("Figure 2")
    x0, y0, x1, y1 = figure["bbox_norm"]
    assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1


def test_text_only_page_has_no_large_regions():
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    for i in range(30):
        page.insert_text((72, 60 + i * 22), f"Body paragraph line {i} with content", fontsize=11)
    regions = detect_regions(doc)
    doc.close()
    assert all(r["area_fraction"] < 0.1 for r in regions)


@pytest.mark.parametrize(
    "slug,figure_pages",
    [
        ("yang-2018-sii", {4, 6}),                # Figures 2 and 5 (raster)
        ("prochaska-2012-varenicline", {10, 11}),  # Figs 2 and 3 (raster)
        ("hahn-2024-exercise-intake", {22, 23, 24, 25, 26}),  # Figs 2-7
    ],
)
def test_detects_forest_plot_regions_in_corpus(slug, figure_pages):
    pdfs = sorted((CORPUS / slug / "source").glob("*.pdf"))
    if not pdfs:
        pytest.skip(f"corpus PDF for {slug} not present")
    doc = _open(pdfs[0])
    regions = detect_regions(doc)
    doc.close()

    detected_vision_pages = {
        r["page_number"] for r in regions if r["needs_vision"] and r["area_fraction"] > 0.05
    }
    # every truth forest-plot page must be flagged as needing vision
    missing = figure_pages - detected_vision_pages
    assert not missing, f"forest-plot pages not flagged for vision: {missing}"
