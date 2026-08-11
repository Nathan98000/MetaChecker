"""Phase-1 baseline benchmark: current pipeline vs gold truth sets.

Runs the real pipeline (ingest → parse_document) on each development-corpus
paper that has a truth set, then scores what the CURRENT implementation can
honestly claim:

- text-layer value recovery: is each KNOWN truth value present verbatim in the
  extracted text spans on its truth source page? (This is the ceiling for any
  downstream numeric extraction working from native text.)
- study-label recovery: same, for study labels.
- page-location accuracy: found on the truth page vs only elsewhere.
- unresolved handling: AMBIGUOUS/UNRESOLVED truth rows are excluded from
  accuracy denominators (abstention is correct behavior).

Structural capabilities that DO NOT EXIST yet (analysis identification,
forest-plot row assembly, table-record assembly, per-value bounding boxes,
false-extraction rate for structured claims) are reported as NOT_IMPLEMENTED
rather than silently scored 0 — the baseline must say what wasn't measured.

Usage:  .venv/bin/python scripts/run_baseline.py [--corpus ../corpus/gold] [--out ../corpus/baseline]
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import models  # noqa: F401
from app.db.base import Base, make_engine, make_session_factory
from app.domain.documents import ingest_document
from app.pipeline import queue, stages  # noqa: F401
from app.pipeline.stages import parse_document as parse_stage
from app.pipeline.worker import drain
from sqlalchemy import select

DASHES = dict.fromkeys(map(ord, "−–—‐‑"), "-")


def norm(s: str) -> str:
    """Normalize for matching: unicode dashes → '-', drop all whitespace,
    normalize unicode forms. Verbatim precision is preserved."""
    s = unicodedata.normalize("NFKC", s or "")
    s = s.translate(DASHES)
    return re.sub(r"\s+", "", s)


def load_truth(paper_dir: Path) -> dict:
    truth = {"effects": [], "labels": [], "analyses": []}
    eff = paper_dir / "truth" / "published_effects.csv"
    lab = paper_dir / "truth" / "study_labels.csv"
    ana = paper_dir / "truth" / "analyses.csv"
    for key, path in (("effects", eff), ("labels", lab), ("analyses", ana)):
        if path.exists():
            with path.open() as f:
                truth[key] = list(csv.DictReader(f))
    return truth


def page_texts_from_artifact(session, document_id: str) -> dict[int, str]:
    artifact = session.scalar(
        select(models.ParseArtifact).where(
            models.ParseArtifact.document_id == document_id,
            models.ParseArtifact.kind == "TEXT_SPANS",
        )
    )
    if artifact is None:
        return {}
    return {
        p["page_number"]: norm("".join(s["text"] for s in p["spans"]))
        for p in artifact.payload["pages"]
    }


VALUE_FIELDS = [
    "effect",
    "ci_lower",
    "ci_upper",
    "weight_pct",
    "n",
    "n_treatment",
    "n_control",
    "events_treatment",
    "events_control",
]


def score_paper(paper_dir: Path, out: dict) -> None:
    pdfs = sorted((paper_dir / "source").glob("*.pdf")) + sorted(
        (paper_dir / "source").glob("*.PDF")
    )
    truth = load_truth(paper_dir)
    if not pdfs or not (truth["effects"] or truth["labels"]):
        out["skipped"].append(
            {"paper": paper_dir.name, "reason": "missing PDF or truth files"}
        )
        return

    with tempfile.TemporaryDirectory() as tmp:
        engine = make_engine(Path(tmp) / "bench.sqlite3")
        Base.metadata.create_all(engine)
        session_factory = make_session_factory(engine)
        with session_factory() as session:
            project = models.Project(name=f"bench:{paper_dir.name}")
            session.add(project)
            session.commit()
            doc, _ = ingest_document(
                session,
                Path(tmp) / "docs",
                project_id=project.id,
                filename=pdfs[0].name,
                content=pdfs[0].read_bytes(),
            )
            queue.enqueue(
                session,
                project_id=project.id,
                stage_id=parse_stage.STAGE_ID,
                work_item_ref=doc.id,
                idempotency_key=parse_stage.idempotency_key(doc.sha256),
            )
            session.commit()
            drain(session, Path(tmp) / "docs")
            pages = page_texts_from_artifact(session, doc.id)
            state = session.scalar(
                select(models.StageState).where(models.StageState.work_item_ref == doc.id)
            )

    all_text = "".join(pages.values())
    paper = {
        "paper": paper_dir.name,
        "pdf": pdfs[0].name,
        "parse_state": state.state if state else "NO_STATE",
        "pages_parsed": len(pages),
        "values": {"known_total": 0, "found_on_page": 0, "found_elsewhere": 0, "missing": 0},
        "pooled": {"known_total": 0, "found_on_page": 0, "found_elsewhere": 0, "missing": 0},
        "labels": {"known_total": 0, "found_on_page": 0, "found_elsewhere": 0, "missing": 0},
        "abstained_rows": 0,
        "missing_examples": [],
    }

    def check(verbatim: str, page_str: str, bucket: dict, example_ctx: str):
        target = norm(verbatim)
        if not target:
            return
        if len(target) < 3:
            # A bare "0" or "1" matches any page trivially — presence testing
            # is uninformative for such targets; tracked separately.
            paper["trivial_targets"] = paper.get("trivial_targets", 0) + 1
            return
        bucket["known_total"] += 1
        page_nums = [int(p) for p in re.findall(r"\d+", page_str or "")]
        on_page = any(target in pages.get(p, "") for p in page_nums)
        if on_page:
            bucket["found_on_page"] += 1
        elif target in all_text:
            bucket["found_elsewhere"] += 1
        else:
            bucket["missing"] += 1
            if len(paper["missing_examples"]) < 12:
                paper["missing_examples"].append(f"{example_ctx}: {verbatim!r}")

    paper["values_by_source"] = {}
    for row in truth["effects"]:
        certainty = (row.get("certainty") or "KNOWN").strip().upper()
        if certainty in ("AMBIGUOUS", "UNRESOLVED"):
            paper["abstained_rows"] += 1
            continue
        source_type = (row.get("source_type") or "UNKNOWN").strip().upper()
        by_src = paper["values_by_source"].setdefault(
            source_type,
            {"known_total": 0, "found_on_page": 0, "found_elsewhere": 0, "missing": 0},
        )
        for field in VALUE_FIELDS:
            value = (row.get(field) or "").strip()
            if value and value.upper() not in ("NOT_APPLICABLE", "NA", ""):
                ctx = f"{row.get('study_label', '?')}/{field}"
                check(value, row.get("source_page", ""), paper["values"], ctx)
                check(value, row.get("source_page", ""), by_src, f"[dup]{ctx}")

    POOLED_FIELDS = ["pooled_effect", "pooled_ci_lower", "pooled_ci_upper", "i2", "q"]
    for row in truth["analyses"]:
        certainty = (row.get("certainty") or "KNOWN").strip().upper()
        if certainty in ("AMBIGUOUS", "UNRESOLVED", "NOT_APPLICABLE"):
            paper["abstained_rows"] += 1
            continue
        for field in POOLED_FIELDS:
            value = (row.get(field) or "").strip()
            if value and value.upper() not in ("NOT_APPLICABLE", "NA", ""):
                check(
                    value,
                    row.get("source_page", ""),
                    paper["pooled"],
                    f"{row.get('analysis_id', '?')}/{field}",
                )

    for row in truth["labels"]:
        certainty = (row.get("certainty") or "KNOWN").strip().upper()
        if certainty in ("AMBIGUOUS", "UNRESOLVED"):
            paper["abstained_rows"] += 1
            continue
        label = (row.get("study_label_verbatim") or "").strip()
        if label:
            check(label, row.get("source_pages", ""), paper["labels"], "label")

    out["papers"].append(paper)


NOT_IMPLEMENTED = [
    "analysis identification (no stage yet)",
    "structured forest-plot row assembly (no stage yet)",
    "structured table-record assembly (no stage yet)",
    "per-value bounding-box association (spans have bboxes; value→span linking not implemented)",
    "reference-list recovery (no stage yet)",
    "false-extraction rate for structured claims (nothing asserts structured values yet)",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[2]
    ap.add_argument("--corpus", default=str(root / "corpus/gold"))
    ap.add_argument("--out", default=str(root / "corpus/baseline"))
    args = ap.parse_args()

    out = {
        "run_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "pipeline": f"{parse_stage.PARSER_ID} v{parse_stage.PARSER_VERSION} (native text spans only)",
        "not_implemented": NOT_IMPLEMENTED,
        "papers": [],
        "skipped": [],
    }
    for paper_dir in sorted(Path(args.corpus).iterdir()):
        if paper_dir.is_dir() and (paper_dir / "truth").exists():
            meta = paper_dir / "truth" / "meta.json"
            role = "development"
            if meta.exists():
                role = json.loads(meta.read_text()).get("corpus_role", "development")
            if role != "development":
                out["skipped"].append({"paper": paper_dir.name, "reason": "holdout — not run"})
                continue
            score_paper(paper_dir, out)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.date.today().isoformat()
    (out_dir / f"baseline_{stamp}.json").write_text(json.dumps(out, indent=2))

    lines = [
        f"# Phase 1 Baseline — {stamp}",
        "",
        f"Pipeline: {out['pipeline']}",
        "",
        "Metric: presence of KNOWN truth values, verbatim, in the extracted",
        "text layer (ceiling for downstream numeric extraction). AMBIGUOUS/",
        "UNRESOLVED truth rows are excluded from denominators (abstention is",
        "correct). 'Found elsewhere' = present in document text but not on the",
        "truth source page.",
        "",
        "| Paper | Parse | Pages | Study values on-page | elsw. | miss. | Pooled on-page | elsw. | miss. | Labels on-page | elsw. | miss. |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in out["papers"]:
        v, g, l = p["values"], p["pooled"], p["labels"]
        lines.append(
            f"| {p['paper']} | {p['parse_state']} | {p['pages_parsed']} "
            f"| {v['found_on_page']}/{v['known_total']} | {v['found_elsewhere']} | {v['missing']} "
            f"| {g['found_on_page']}/{g['known_total']} | {g['found_elsewhere']} | {g['missing']} "
            f"| {l['found_on_page']}/{l['known_total']} | {l['found_elsewhere']} | {l['missing']} |"
        )
    lines += ["", "## Study values by source type (the routing signal)", ""]
    lines += ["| Paper | Source | on-page | elsewhere | missing |", "|---|---|---|---|---|"]
    for p in out["papers"]:
        for src, b in sorted(p.get("values_by_source", {}).items()):
            lines.append(
                f"| {p['paper']} | {src} | {b['found_on_page']}/{b['known_total']} "
                f"| {b['found_elsewhere']} | {b['missing']} |"
            )
    lines += ["", "## Not measured (capability does not exist yet)", ""]
    lines += [f"- {n}" for n in NOT_IMPLEMENTED]
    lines += ["", "## Missing-value examples (first 12 per paper)", ""]
    for p in out["papers"]:
        if p["missing_examples"]:
            lines.append(f"### {p['paper']}")
            lines += [f"- {e}" for e in p["missing_examples"]]
            lines.append("")
    for s in out["skipped"]:
        lines.append(f"- skipped {s['paper']}: {s['reason']}")
    (out_dir / f"baseline_{stamp}.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out_dir}/baseline_{stamp}.md")
    for p in out["papers"]:
        v = p["values"]
        pct = 100 * v["found_on_page"] / v["known_total"] if v["known_total"] else 0
        print(f"  {p['paper']}: values on-page {v['found_on_page']}/{v['known_total']} ({pct:.0f}%)")


if __name__ == "__main__":
    main()
