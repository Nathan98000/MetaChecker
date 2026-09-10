"""Researcher correction workflow over extracted records (§21, A18):
lazy materialization preserves the verbatim original as revision #1;
corrections append; undo restores; overlay reflects state."""

import pytest
from fastapi.testclient import TestClient

from app.api.main import create_app
from app.core.config import Settings
from tests.conftest import make_pdf
import pymupdf


def make_table_pdf() -> bytes:
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((40, 90), "Study or subgroup Exercise Control Std. Mean Difference Weight", fontsize=9)
    page.insert_text((40, 120), "Blumenthal 1999", fontsize=9)
    page.insert_text((200, 120), "55 8.7 (6.9)", fontsize=9)
    page.insert_text((300, 120), "48 7.8 (6.5)", fontsize=9)
    page.insert_text((430, 120), "4.23%", fontsize=9)
    page.insert_text((480, 120), "0.14[-0.25,0.52]", fontsize=9)
    page.insert_text((40, 140), "Total (95% CI)", fontsize=9)
    page.insert_text((480, 140), "-0.62[-0.81,-0.42]", fontsize=9)
    data = doc.tobytes()
    doc.close()
    return data


@pytest.fixture()
def client(tmp_path):
    settings = Settings(data_dir=tmp_path / "data", run_worker=False)
    app = create_app(settings)
    with TestClient(app) as c:
        yield c


def _setup_document(client) -> str:
    project_id = client.post("/projects", json={"name": "Correction test"}).json()["id"]
    doc_id = client.post(
        f"/projects/{project_id}/documents",
        files={"file": ("m.pdf", make_table_pdf(), "application/pdf")},
    ).json()["document"]["id"]
    client.post("/dev/drain")
    return doc_id


def test_correct_preserves_original_and_overlays(client):
    doc_id = _setup_document(client)
    records = client.get(f"/documents/{doc_id}/records").json()["records"]
    idx = next(i for i, r in enumerate(records) if r["study_label"] == "Blumenthal 1999")
    assert records[idx]["effect_value"] == "0.14"
    assert records[idx]["review"] == {}  # untouched

    r = client.post(f"/documents/{doc_id}/cells/correct", json={
        "record_index": idx, "field": "effect_value",
        "corrected_value": "0.41", "note": "digits transposed in extraction",
    })
    assert r.status_code == 200
    dp_id = r.json()["data_point_id"]

    # overlay shows the correction; extracted value remains visible as original
    records = client.get(f"/documents/{doc_id}/records").json()["records"]
    review = records[idx]["review"]["effect_value"]
    assert review["corrected"] is True
    assert review["current_value"] == "0.41"
    assert review["original_value"] == "0.14"
    assert review["review_state"] == "CORRECTED"

    # full provenance chain: revision 1 = verbatim original, SOURCE_REPORTED
    chain = client.get(f"/datapoints/{dp_id}/provenance").json()
    revisions = chain["revisions"]
    assert revisions[0]["value_text"] == "0.14"
    assert revisions[0]["scientific_basis"] == "SOURCE_REPORTED"
    assert revisions[0]["source"]["document_id"] == doc_id
    assert revisions[1]["value_text"] == "0.41"
    assert revisions[1]["review_state"] == "CORRECTED"

    # undo = restore revision 1 (appends; nothing destroyed)
    client.post(f"/datapoints/{dp_id}/restore", json={"revision_no": 1})
    records = client.get(f"/documents/{doc_id}/records").json()["records"]
    review = records[idx]["review"]["effect_value"]
    assert review["current_value"] == "0.14"
    assert review["corrected"] is False
    chain = client.get(f"/datapoints/{dp_id}/provenance").json()
    assert len(chain["revisions"]) == 3  # original, correction, restore


def test_verify_marks_cell_without_changing_value(client):
    doc_id = _setup_document(client)
    records = client.get(f"/documents/{doc_id}/records").json()["records"]
    idx = next(i for i, r in enumerate(records) if r["study_label"] == "Blumenthal 1999")
    r = client.post(f"/documents/{doc_id}/cells/verify", json={
        "record_index": idx, "field": "effect_value",
    })
    assert r.status_code == 200
    records = client.get(f"/documents/{doc_id}/records").json()["records"]
    review = records[idx]["review"]["effect_value"]
    assert review["review_state"] == "VERIFIED"
    assert review["corrected"] is False
    assert review["current_value"] == "0.14"


def test_empty_correction_rejected(client):
    doc_id = _setup_document(client)
    r = client.post(f"/documents/{doc_id}/cells/correct", json={
        "record_index": 0, "field": "effect_value", "corrected_value": "  ",
    })
    assert r.status_code == 400
    assert "corrected value" in r.json()["what_happened"].lower() or \
        "value" in r.json()["what_happened"].lower()
