import sys
from pathlib import Path

import pymupdf
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import models  # noqa: F401, E402
from app.db.base import Base, make_engine, make_session_factory  # noqa: E402
from app.pipeline import stages  # noqa: F401, E402 (register handlers)


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def engine(data_dir: Path):
    eng = make_engine(data_dir / "test.sqlite3")
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture()
def session_factory(engine):
    return make_session_factory(engine)


@pytest.fixture()
def session(session_factory):
    with session_factory() as s:
        yield s


@pytest.fixture()
def documents_dir(data_dir: Path) -> Path:
    d = data_dir / "documents"
    d.mkdir(exist_ok=True)
    return d


@pytest.fixture()
def project(session):
    p = models.Project(name="Test audit")
    session.add(p)
    session.commit()
    return p


def make_pdf(texts: list[str] | None = None) -> bytes:
    """A tiny real PDF with an embedded text layer."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    y = 72
    for text in texts or ["Smith et al. 2018", "-0.43 [-0.71, -0.15]"]:
        page.insert_text((72, y), text, fontsize=11)
        y += 20
    content = doc.tobytes()
    doc.close()
    return content


@pytest.fixture()
def pdf_bytes() -> bytes:
    return make_pdf()
