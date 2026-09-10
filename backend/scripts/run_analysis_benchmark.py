"""Analysis-identification benchmark: detected analyses vs truth analyses.csv.

Runs parse → assembly → vision(replay) → identify_analyses per development
paper and matches detected analyses to truth by pooled values (effect + CI,
verbatim-normalized; the strongest available key). Reports per paper:
detection precision/recall, pooled-value accuracy (matched by construction),
heterogeneity (I²) accuracy, effect-measure accuracy, model accuracy,
member-count agreement vs the truth's n_studies_reported, and false analyses.
Text-borne truth analyses (no table/figure pooled row anywhere — e.g. Nissen
subgroup ORs reported only in prose, Macnamara correlations) are counted in a
separate NOT_STRUCTURED bucket rather than as misses of the structural
channel. BENCHMARK_AGAINST_PREFREEZE_TRUTH.

Usage: .venv/bin/python scripts/run_analysis_benchmark.py
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

from app.adapters.llm.fake import ReplayVisionProvider
from app.db import models
from app.db.base import Base, make_engine, make_session_factory
from app.domain.documents import ingest_document
from app.pipeline import queue, stages  # noqa: F401
from app.pipeline.stages import (
    assemble_tables,
    detect_figures,
    extract_figure_vision as vision,
    identify_analyses,
    parse_document as parse_stage,
)
from app.pipeline.worker import drain

ROOT = Path(__file__).resolve().parents[2]
GOLD = ROOT / "corpus" / "gold"
FIXTURES = ROOT / "corpus" / "vision-fixtures"
DASHES = dict.fromkeys(map(ord, "−–—‐‑"), "-")

DEV_PAPERS = [
    "yang-2018-sii", "prochaska-2012-varenicline", "macnamara-2014-practice",
    "hahn-2024-exercise-intake", "driessen-2015-nih-psychotherapy",
    "cooney-2013-exercise-depression", "nissen-2007-rosiglitazone",
]
VISION_PAPERS = {"yang-2018-sii", "prochaska-2012-varenicline",
                 "hahn-2024-exercise-intake", "driessen-2015-nih-psychotherapy"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").translate(DASHES)
    s = re.sub(r"\s+", "", s).rstrip("%")
    if re.fullmatch(r"-?\d+,\d+", s):
        s = s.replace(",", ".")
    return s


def num(s: str) -> float | None:
    try:
        return float(norm(s))
    except (TypeError, ValueError):
        return None


def values_match(a: str, b: str) -> bool:
    if norm(a) == norm(b) and norm(a):
        return True
    na, nb = num(a), num(b)
    return na is not None and nb is not None and na == nb


def run_pipeline(paper_dir: Path, use_vision: bool) -> list[dict]:
    pdfs = sorted((paper_dir / "source").glob("*.pdf"))
    if not pdfs:
        return []
    if use_vision:
        vision.configure(ReplayVisionProvider(FIXTURES),
                         model_role="OVERRIDE", model_id="claude-sonnet-5")
    with tempfile.TemporaryDirectory() as tmp:
        engine = make_engine(Path(tmp) / "b.sqlite3")
        Base.metadata.create_all(engine)
        sf = make_session_factory(engine)
        with sf() as session:
            project = models.Project(name=f"abench:{paper_dir.name}")
            session.add(project)
            session.commit()
            doc, _ = ingest_document(session, Path(tmp) / "docs", project_id=project.id,
                                     filename=pdfs[0].name, content=pdfs[0].read_bytes())
            mods = [parse_stage, detect_figures, assemble_tables]
            if use_vision:
                mods.append(vision)
            mods.append(identify_analyses)
            for mod in mods:
                queue.enqueue(session, project_id=project.id, stage_id=mod.STAGE_ID,
                              work_item_ref=doc.id,
                              idempotency_key=mod.idempotency_key(doc.sha256))
            session.commit()
            drain(session, Path(tmp) / "docs")
            artifact = session.scalar(
                select(models.ParseArtifact).where(
                    models.ParseArtifact.document_id == doc.id,
                    models.ParseArtifact.kind == "ANALYSES",
                ))
            return artifact.payload["analyses"] if artifact else []


def score(paper: str, detected: list[dict], truth: list[dict]) -> dict:
    def is_structured(t: dict) -> bool:
        """Structured = the truth locates this analysis in a table or figure;
        prose-only pooled sentences are the text channel's (future) job."""
        located = (t.get("source_figure") or "").strip() or (t.get("source_table") or "").strip()
        # supplement-only sources (S1 Table etc.) are not in the PDF at all
        if re.search(r"\bS\d|supplement", located, re.IGNORECASE):
            return False
        return bool(located) and num(t.get("pooled_effect")) is not None \
            and (t.get("pooled_ci_lower") or "").strip()

    known = [t for t in truth
             if (t.get("certainty") or "KNOWN").upper() == "KNOWN" and is_structured(t)]
    text_only = [t for t in truth if t not in known]
    s = {"paper": paper, "truth_structured": len(known), "truth_other": len(text_only),
         "detected": len(detected), "matched": 0, "i2_ok": 0, "i2_present": 0,
         "measure_ok": 0, "model_ok": 0, "member_count_ok": 0, "member_truth_stated": 0,
         "false_analyses": 0, "missed": [], "false_examples": []}
    used = set()
    for t in known:
        best = None
        for i, d in enumerate(detected):
            if i in used:
                continue
            p = d.get("pooled") or {}
            if values_match(p.get("effect_value"), t.get("pooled_effect")) and \
               values_match(p.get("ci_lower"), t.get("pooled_ci_lower")) and \
               values_match(p.get("ci_upper"), t.get("pooled_ci_upper")):
                best = i
                break
        if best is None:
            if len(s["missed"]) < 6:
                s["missed"].append(f"{t.get('analysis_id')} {t.get('outcome','')[:40]} "
                                   f"{t.get('pooled_effect')}[{t.get('pooled_ci_lower')},{t.get('pooled_ci_upper')}]")
            continue
        used.add(best)
        d = detected[best]
        s["matched"] += 1
        t_i2 = re.sub(r"[^\d.]", "", t.get("i2") or "")
        if t_i2:
            s["i2_present"] += 1
            d_i2 = (d.get("heterogeneity") or {}).get("i2", "")
            if d_i2 and num(d_i2) is not None and num(t_i2) is not None and \
               abs(num(d_i2) - num(t_i2)) < 0.005 * max(num(t_i2), 1):
                s["i2_ok"] += 1
        t_measure = (t.get("effect_measure") or "").upper()
        d_measure = (d.get("effect_measure") or "").upper()
        aliases = {"M-H OR": "OR", "PETO ODDS RATIO": "PETO OR",
                   "RISK DIFFERENCE (M-H)": "RD", "RISK DIFFERENCE (MANTEL-HAENSZEL, %)": "RD"}
        t_measure = aliases.get(t_measure, t_measure)
        if t_measure and d_measure:
            s["measure_ok"] += (t_measure == d_measure or t_measure.split()[0] in d_measure
                                or d_measure in t_measure)
        t_model = (t.get("model") or "").upper()
        if t_model in ("RANDOM", "FIXED"):
            s["model_ok"] += (d.get("model") == t_model)
        t_n = re.sub(r"[^\d]", "", (t.get("n_studies_reported") or "").split("(")[0][:6])
        if t_n:
            s["member_truth_stated"] += 1
            s["member_count_ok"] += (d.get("member_count") == int(t_n))
    # Unmatched detections are "extra (unverified)" — most development truth
    # sets deliberately cover a SUBSET of each paper's analyses (e.g. Cooney
    # truths 3 of 23), so an unmatched detection is usually an untruthed
    # analysis, not a fabrication. Only human review can grade extras; they
    # are surfaced, never scored as correct.
    truth_keys = {(norm(t.get("pooled_effect")), norm(t.get("pooled_ci_lower")))
                  for t in known}
    for i, d in enumerate(detected):
        if i in used:
            continue
        p = d.get("pooled") or {}
        if (norm(p.get("effect_value") or ""), norm(p.get("ci_lower") or "")) not in truth_keys:
            s["false_analyses"] += 1
            if len(s["false_examples"]) < 5:
                s["false_examples"].append(
                    f"{d.get('description','')[:50]} {p.get('effect_value')}[{p.get('ci_lower')},{p.get('ci_upper')}]")
    return s


def pct(n, d):
    return f"{100*n/d:.0f}%" if d else "—"


def main() -> None:
    results = []
    for paper in DEV_PAPERS:
        paper_dir = GOLD / paper
        truth_path = paper_dir / "truth" / "analyses.csv"
        if not truth_path.exists() or not list((paper_dir / "source").glob("*.pdf")):
            print(f"skip {paper}")
            continue
        with truth_path.open() as f:
            truth = list(csv.DictReader(f))
        detected = run_pipeline(paper_dir, use_vision=paper in VISION_PAPERS)
        s = score(paper, detected, truth)
        results.append(s)
        print(f"{paper}: {s['matched']}/{s['truth_structured']} structured analyses matched, "
              f"{s['false_analyses']} false, {s['truth_other']} text-only out of scope")

    stamp = dt.date.today().isoformat()
    out = ROOT / "corpus" / "baseline"
    (out / f"analysis_benchmark_{stamp}.json").write_text(json.dumps(
        {"run_at": dt.datetime.now(dt.timezone.utc).isoformat(),
         "truth_state": "BENCHMARK_AGAINST_PREFREEZE_TRUTH",
         "identifier": f"{identify_analyses.PARSER_ID} v{identify_analyses.PARSER_VERSION}",
         "results": results}, indent=2))
    lines = [
        f"# Analysis-Identification Benchmark — {stamp}",
        "",
        "**BENCHMARK_AGAINST_PREFREEZE_TRUTH** · deterministic structural",
        "identifier v1 (tables + RevMan headers + figure summary rows; vision",
        "channel via recorded fixtures). Text-borne analyses (prose-only pooled",
        "values) are a separate bucket — out of the structural channel's scope,",
        "never silently claimed.",
        "",
        "| Paper | Struct. truth | Recall | Precision | I² ok | Measure | Model | k agrees | Extra (unverif.) | Text-only (o.o.s.) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for s in results:
        m = s["matched"]
        lines.append(
            f"| {s['paper']} | {s['truth_structured']} | {pct(m, s['truth_structured'])} "
            f"| {pct(m, s['detected'] - 0 if s['detected'] else 0) if s['detected'] else '—'}"
            f" | {pct(s['i2_ok'], s['i2_present'])} | {pct(s['measure_ok'], m)} "
            f"| {pct(s['model_ok'], m)} | {pct(s['member_count_ok'], s['member_truth_stated'])} "
            f"| {s['false_analyses']} | {s['truth_other']} |")
    lines += ["", "## Missed / false examples", ""]
    for s in results:
        if s["missed"] or s["false_examples"]:
            lines.append(f"### {s['paper']}")
            lines += [f"- missed: {e}" for e in s["missed"]]
            lines += [f"- extra: {e}" for e in s["false_examples"]]
            lines.append("")
    (out / f"analysis_benchmark_{stamp}.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out}/analysis_benchmark_{stamp}.md")


if __name__ == "__main__":
    main()
