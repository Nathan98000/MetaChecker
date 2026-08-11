"""Phase-1c table-assembly benchmark: deterministic layout assembly vs truth.

Scores TABLE_RECORDS against truth rows whose values are text-encoded:
- cooney: RevMan forest tables (all truth rows; category `revman_forest_table`)
- prochaska: Table 2 effect columns (category `effect_column_table`)
- nissen: 2x2 count tables once truthed (category `count_table` — v1 assembler
  does not target bare-count tables; reported for visibility, not claimed)

Metrics (per category and per paper): row detection P/R, label accuracy,
value/CI assignment, measure (column/header) assignment where truth states it,
FULL_ROW_EXACT_MATCH, false extraction rate, bbox presence (provenance).
BENCHMARK_AGAINST_PREFREEZE_TRUTH.

Usage: .venv/bin/python scripts/run_table_benchmark.py
"""

import csv
import datetime as dt
import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.db import models
from app.db.base import Base, make_engine, make_session_factory
from app.domain.documents import ingest_document
from app.pipeline import queue, stages  # noqa: F401
from app.pipeline.stages import assemble_tables, parse_document as parse_stage
from app.pipeline.worker import drain

ROOT = Path(__file__).resolve().parents[2]
GOLD = ROOT / "corpus" / "gold"
DASHES = dict.fromkeys(map(ord, "−–—‐‑"), "-")

TARGETS = {
    "cooney-2013-exercise-depression": {
        "category": "revman_forest_table",
        "truth_filter": lambda r: (r.get("source_type") or "").upper() == "FOREST_PLOT",
        "measure_truth": False,
    },
    "prochaska-2012-varenicline": {
        "category": "effect_column_table",
        "truth_filter": lambda r: (r.get("source_type") or "").upper() == "TABLE",
        "measure_truth": True,
    },
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").translate(DASHES)
    return re.sub(r"\s+", "", s)


def norm_label(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def run_assembler(paper_dir: Path) -> list[dict]:
    pdfs = sorted((paper_dir / "source").glob("*.pdf"))
    with tempfile.TemporaryDirectory() as tmp:
        engine = make_engine(Path(tmp) / "b.sqlite3")
        Base.metadata.create_all(engine)
        sf = make_session_factory(engine)
        with sf() as session:
            project = models.Project(name=f"tbench:{paper_dir.name}")
            session.add(project)
            session.commit()
            doc, _ = ingest_document(session, Path(tmp) / "docs", project_id=project.id,
                                     filename=pdfs[0].name, content=pdfs[0].read_bytes())
            for mod in (parse_stage, assemble_tables):
                queue.enqueue(session, project_id=project.id, stage_id=mod.STAGE_ID,
                              work_item_ref=doc.id,
                              idempotency_key=mod.idempotency_key(doc.sha256))
            session.commit()
            drain(session, Path(tmp) / "docs")
            artifact = session.scalar(
                select(models.ParseArtifact).where(
                    models.ParseArtifact.document_id == doc.id,
                    models.ParseArtifact.kind == "TABLE_RECORDS",
                )
            )
            return artifact.payload["records"] if artifact else []


def _canon_measure(name: str) -> str:
    n = (name or "").upper().replace("-", " ").strip()
    aliases = {
        "M H OR": "OR", "M H ODDS RATIO": "OR", "MANTEL HAENSZEL OR": "OR",
        "PETO ODDS RATIO": "PETO_OR", "PETO OR": "PETO_OR",
        "RD (%)": "RD", "RD (PROPORTION)": "RD", "CUMULATIVE RD": "RD",
        "RELATIVE RISK": "RR", "RISK RATIO": "RR", "RISK DIFFERENCE": "RD",
    }
    return aliases.get(n, n)


def measure_matches(truth_row: dict, record: dict) -> bool:
    """Exact measure match after canonical aliasing — substring logic is
    forbidden (it conflated M-H OR with Peto OR when point estimates
    coincided; see table benchmark 2026-08-11 debugging)."""
    t = _canon_measure(truth_row.get("effect_measure"))
    if not t:
        return True
    return _canon_measure(record.get("effect_measure")) == t


def score(paper: str, cfg: dict, records: list[dict], truth_rows: list[dict]) -> dict:
    known = [r for r in truth_rows
             if (r.get("certainty") or "KNOWN").upper() == "KNOWN"
             and (r.get("effect") or "").strip()
             and r.get("row_kind") in ("STUDY",)]
    pooled_truth = [r for r in truth_rows if r.get("row_kind") in ("OVERALL_TOTAL", "SUBGROUP_TOTAL")]
    # scope to pages the truth covers: records from untruthed analyses on other
    # pages are out of scope, neither true nor false
    truth_pages = {p.strip() for r in truth_rows for p in
                   re.findall(r"\d+", r.get("source_page") or "")}
    rec_study = [r for r in records
                 if r["row_kind"] == "STUDY_ROW" and str(r["page_number"]) in truth_pages]

    s = {"paper": paper, "category": cfg["category"],
         "truth_rows": len(known), "extracted_rows": len(rec_study),
         "matched": 0, "label_ok": 0, "value_ok": 0, "ci_ok": 0, "measure_ok": 0,
         "full_row": 0, "bbox_present": 0, "false_extractions": 0,
         "pooled_as_study": 0, "missed_examples": [], "false_examples": []}

    used = set()
    for t in known:
        t_label, t_eff = norm_label(t.get("study_label")), norm(t.get("effect"))
        cand = None
        for i, r in enumerate(rec_study):
            if i in used:
                continue
            if norm_label(r["study_label"]) == t_label and norm(r["effect_value"] or "") == t_eff \
               and measure_matches(t, r):
                cand = i
                break
        if cand is None:
            for i, r in enumerate(rec_study):
                if i not in used and norm_label(r["study_label"]) == t_label \
                   and norm(r["effect_value"] or "") == t_eff:
                    cand = i
                    break
        if cand is None:
            if len(s["missed_examples"]) < 8:
                s["missed_examples"].append(
                    f"{t.get('study_label')} {t.get('effect')} [{t.get('effect_measure','')}] p{t.get('source_page')}")
            continue
        used.add(cand)
        r = rec_study[cand]
        s["matched"] += 1
        label_ok = norm_label(r["study_label"]) == t_label
        value_ok = norm(r["effect_value"] or "") == t_eff
        ci_ok = norm(r.get("ci_lower") or "") == norm(t.get("ci_lower") or "") and \
                norm(r.get("ci_upper") or "") == norm(t.get("ci_upper") or "")
        m_ok = measure_matches(t, r) if cfg["measure_truth"] else True
        s["label_ok"] += label_ok
        s["value_ok"] += value_ok
        s["ci_ok"] += ci_ok
        s["measure_ok"] += m_ok
        s["full_row"] += label_ok and value_ok and ci_ok and m_ok
        s["bbox_present"] += bool(r.get("cell_bboxes", {}).get("effect"))

    truth_labels = {norm_label(t.get("study_label")) for t in known}
    pooled_labels = {norm_label(t.get("study_label")) for t in pooled_truth}
    for i, r in enumerate(rec_study):
        if i in used:
            continue
        rl = norm_label(r["study_label"])
        if rl in pooled_labels:
            s["pooled_as_study"] += 1
        elif rl not in truth_labels:
            s["false_extractions"] += 1
            if len(s["false_examples"]) < 8:
                s["false_examples"].append(f"{r['study_label']} {r['effect_value']} p{r['page_number']}")
    return s


def pct(n, d):
    return f"{100*n/d:.1f}%" if d else "—"


def main() -> None:
    results = []
    for paper, cfg in TARGETS.items():
        paper_dir = GOLD / paper
        if not (paper_dir / "truth" / "published_effects.csv").exists():
            continue
        with (paper_dir / "truth" / "published_effects.csv").open() as f:
            truth = [r for r in csv.DictReader(f) if cfg["truth_filter"](r)]
        records = run_assembler(paper_dir)
        s = score(paper, cfg, records, truth)
        results.append(s)
        print(f"{paper}: full-row {s['full_row']}/{s['truth_rows']}, "
              f"false {s['false_extractions']}")

    stamp = dt.date.today().isoformat()
    out = ROOT / "corpus" / "baseline"
    (out / f"table_benchmark_{stamp}.json").write_text(json.dumps(
        {"run_at": dt.datetime.now(dt.timezone.utc).isoformat(),
         "truth_state": "BENCHMARK_AGAINST_PREFREEZE_TRUTH",
         "assembler": f"{assemble_tables.PARSER_ID} v{assemble_tables.PARSER_VERSION}",
         "results": results}, indent=2))
    lines = [
        f"# Table-Assembly Benchmark — {stamp}",
        "",
        "**BENCHMARK_AGAINST_PREFREEZE_TRUTH** · deterministic layout assembly",
        f"(`{assemble_tables.PARSER_ID}` v{assemble_tables.PARSER_VERSION}), zero AI calls, zero cost.",
        "",
        "| Paper | Category | Recall | Precision | Label | Value | CI | Measure | FULL ROW | Pooled-as-study | False extr | Cell bbox |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for s in results:
        m = s["matched"]
        lines.append(
            f"| {s['paper']} | {s['category']} | {pct(m, s['truth_rows'])} "
            f"| {pct(m, s['extracted_rows'])} | {pct(s['label_ok'], m)} | {pct(s['value_ok'], m)} "
            f"| {pct(s['ci_ok'], m)} | {pct(s['measure_ok'], m)} | **{pct(s['full_row'], s['truth_rows'])}** "
            f"| {s['pooled_as_study']} | {s['false_extractions']} | {pct(s['bbox_present'], m)} |")
    lines += ["", "## Missed / false examples", ""]
    for s in results:
        if s["missed_examples"] or s["false_examples"]:
            lines.append(f"### {s['paper']}")
            lines += [f"- missed: {e}" for e in s["missed_examples"]]
            lines += [f"- false: {e}" for e in s["false_examples"]]
            lines.append("")
    (out / f"table_benchmark_{stamp}.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out}/table_benchmark_{stamp}.md")


if __name__ == "__main__":
    main()
