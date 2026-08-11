"""End-to-end vertical slice over the HTTP API:
create project → upload PDF → parse → read spans with bboxes → fetch original
file → close/reopen state survives."""

import pytest
from fastapi.testclient import TestClient

from app.api.main import create_app
from app.core.config import Settings
from tests.conftest import make_pdf


@pytest.fixture()
def client(tmp_path):
    settings = Settings(data_dir=tmp_path / "data", run_worker=False)
    app = create_app(settings)
    with TestClient(app) as c:
        yield c


def test_vertical_slice(client, tmp_path):
    # 1. Create project
    r = client.post("/projects", json={"name": "Smith 2018 audit"})
    assert r.status_code == 200
    project_id = r.json()["id"]

    # 2. Upload one meta-analysis PDF
    pdf = make_pdf(["Table 2. Effect sizes", "Smith et al. 2018", "-0.43 [-0.71, -0.15]"])
    r = client.post(
        f"/projects/{project_id}/documents",
        files={"file": ("meta_analysis.pdf", pdf, "application/pdf")},
    )
    assert r.status_code == 200
    doc_id = r.json()["document"]["id"]
    assert r.json()["created"] is True

    # Duplicate upload returns the same document, creates nothing
    r = client.post(
        f"/projects/{project_id}/documents",
        files={"file": ("meta_analysis_copy.pdf", pdf, "application/pdf")},
    )
    assert r.json()["created"] is False
    assert r.json()["document"]["id"] == doc_id

    # 3. Parse (worker drained synchronously in test mode)
    r = client.post("/dev/drain")
    assert r.json()["processed"] >= 1

    # 4. Extracted content is available with normalized bboxes
    r = client.get(f"/documents/{doc_id}/text")
    assert r.status_code == 200
    pages = r.json()["pages"]
    assert len(pages) == 1
    spans = pages[0]["spans"]
    texts = [s["text"] for s in spans]
    assert any("Smith et al. 2018" in t for t in texts)
    assert any("-0.43" in t for t in texts)
    for s in spans:
        x0, y0, x1, y1 = s["bbox_norm"]
        assert 0 <= x0 <= x1 <= 1 and 0 <= y0 <= y1 <= 1

    # 5. Original file retrievable byte-identical (click-through to PDF)
    r = client.get(f"/documents/{doc_id}/file")
    assert r.content == pdf

    # 6. Stage state visible on the document
    r = client.get(f"/documents/{doc_id}")
    assert r.json()["stages"]["parse_document"]["state"] == "SUCCESS"
    assert r.json()["page_count"] == 1


def test_state_survives_reopen(tmp_path):
    """Close the app (new app instance over the same data dir) — state intact."""
    settings = Settings(data_dir=tmp_path / "data", run_worker=False)
    pdf = make_pdf()

    with TestClient(create_app(settings)) as c:
        project_id = c.post("/projects", json={"name": "Persistent"}).json()["id"]
        doc_id = c.post(
            f"/projects/{project_id}/documents",
            files={"file": ("m.pdf", pdf, "application/pdf")},
        ).json()["document"]["id"]
        c.post("/dev/drain")

    # "Reopen the application"
    with TestClient(create_app(Settings(data_dir=tmp_path / "data", run_worker=False))) as c:
        r = c.get(f"/projects/{project_id}")
        assert r.status_code == 200
        assert r.json()["documents"][0]["id"] == doc_id
        assert c.get(f"/documents/{doc_id}/text").status_code == 200
        assert c.get(f"/documents/{doc_id}/file").content == pdf


def test_scanned_pdf_reports_partial_success(client):
    """Image-only PDF → PARTIAL_SUCCESS with what could/couldn't be extracted."""
    import pymupdf

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    # draw a rectangle: page has content but no text layer
    page.draw_rect(pymupdf.Rect(72, 72, 300, 200), color=(0, 0, 0), width=2)
    pdf = doc.tobytes()
    doc.close()

    project_id = client.post("/projects", json={"name": "Scan"}).json()["id"]
    doc_id = client.post(
        f"/projects/{project_id}/documents",
        files={"file": ("scan.pdf", pdf, "application/pdf")},
    ).json()["document"]["id"]
    client.post("/dev/drain")

    stages = client.get(f"/documents/{doc_id}").json()["stages"]
    assert stages["parse_document"]["state"] == "PARTIAL_SUCCESS"
    detail = stages["parse_document"]["detail"]
    assert detail["extracted"] and detail["not_extracted"]
