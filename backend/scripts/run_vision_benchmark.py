"""Phase-1b vision benchmark: structured forest-plot extraction vs gold truth.

Runs the real pipeline (parse → detect_figure_regions → extract_figure_vision)
per development paper, then scores the FOREST_PLOT_ROWS artifact against the
truth published_effects rows that are figure-sourced. Reports PER PAPER first,
aggregate second (researcher directive: no aggregate-only reporting).

Metrics: study-row detection precision/recall, label accuracy, numeric
exact-match, CI pairing, full row assembly, pooled-row misclassification,
false-extraction rate, abstention rate, provenance (page) accuracy, latency,
estimated cost.

Providers:
  --provider live     Anthropic (requires ANTHROPIC_API_KEY); records fixtures
                      into corpus/vision-fixtures/ for later replay
  --provider replay   recorded fixtures only (offline, deterministic)

Usage: .venv/bin/python scripts/run_vision_benchmark.py --provider live
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

from sqlalchemy import select

from app.adapters.llm.fake import RecordingVisionProvider, ReplayVisionProvider
from app.adapters.llm.router import ModelRouter
from app.db import models
from app.db.base import Base, make_engine, make_session_factory
from app.domain.documents import ingest_document
from app.pipeline import queue, stages  # noqa: F401
from app.pipeline.stages import detect_figures, extract_figure_vision as vision
from app.pipeline.stages import parse_document as parse_stage
from app.pipeline.worker import drain

ROOT = Path(__file__).resolve().parents[2]
GOLD = ROOT / "corpus" / "gold"
FIXTURES = ROOT / "corpus" / "vision-fixtures"

DASHES = dict.fromkeys(map(ord, "−–—‐‑"), "-")


def norm_value(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").translate(DASHES)
    return re.sub(r"\s+", "", value)


def norm_label(label: str) -> str:
    return re.sub(r"\s+", " ", (label or "").strip().lower())


def truth_figure_rows(paper_dir: Path) -> list[dict]:
    path = paper_dir / "truth" / "published_effects.csv"
    if not path.exists():
        return []
    with path.open() as f:
        rows = list(csv.DictReader(f))
    return [
        r for r in rows
        if (r.get("source_type") or "").upper() == "FOREST_PLOT"
        and (r.get("certainty") or "KNOWN").upper() == "KNOWN"
        and (r.get("effect") or "").strip()
    ]


def run_pipeline(paper_dir: Path, provider, model_role: str, model_id: str) -> dict:
    pdfs = sorted((paper_dir / "source").glob("*.pdf"))
    if not pdfs:
        return {"error": "no PDF"}
    vision.configure(provider, model_role=model_role, model_id=model_id)
    with tempfile.TemporaryDirectory() as tmp:
        engine = make_engine(Path(tmp) / "bench.sqlite3")
        Base.metadata.create_all(engine)
        session_factory = make_session_factory(engine)
        with session_factory() as session:
            project = models.Project(name=f"vbench:{paper_dir.name}")
            session.add(project)
            session.commit()
            doc, _ = ingest_document(
                session, Path(tmp) / "docs", project_id=project.id,
                filename=pdfs[0].name, content=pdfs[0].read_bytes(),
            )
            for mod in (parse_stage, detect_figures, vision):
                queue.enqueue(
                    session, project_id=project.id, stage_id=mod.STAGE_ID,
                    work_item_ref=doc.id, idempotency_key=mod.idempotency_key(doc.sha256),
                )
            session.commit()
            drain(session, Path(tmp) / "docs")
            artifact = session.scalar(
                select(models.ParseArtifact).where(
                    models.ParseArtifact.document_id == doc.id,
                    models.ParseArtifact.kind == "FOREST_PLOT_ROWS",
                )
            )
            calls = session.scalars(select(models.ExternalCallLog)).all()
            cost = sum(c.est_cost_usd or 0 for c in calls)
            latency = sum(c.latency_ms or 0 for c in calls)
            state = session.scalar(
                select(models.StageState).where(
                    models.StageState.stage_id == vision.STAGE_ID,
                    models.StageState.work_item_ref == doc.id,
                )
            )
            return {
                "artifact": artifact.payload if artifact else None,
                "stage_state": state.state if state else "NO_STATE",
                "cost_usd": round(cost, 4),
                "latency_ms": latency,
                "calls": len(calls),
            }


def score_paper(paper: str, artifact: dict | None, truth_rows: list[dict]) -> dict:
    scores = {
        "paper": paper,
        "truth_study_rows": 0, "truth_pooled_rows": 0,
        "extracted_study_rows": 0,
        "matched": 0, "label_exact": 0, "numeric_exact": 0, "ci_paired": 0,
        "row_assembled": 0, "pooled_misclassified": 0, "false_extractions": 0,
        "abstentions": 0, "provenance_page_correct": 0,
        "unmatched_truth_examples": [], "false_extraction_examples": [],
    }
    truth_study = [r for r in truth_rows if r.get("row_kind") == "STUDY"]
    truth_pooled = [r for r in truth_rows if r.get("row_kind") in ("OVERALL_TOTAL", "SUBGROUP_TOTAL")]
    scores["truth_study_rows"] = len(truth_study)
    scores["truth_pooled_rows"] = len(truth_pooled)
    if not artifact:
        return scores

    extracted: list[tuple[dict, int]] = []  # (row, region_page)
    for result in artifact.get("results", []):
        page = result["region"]["page_number"]
        for row in result.get("rows", []):
            extracted.append((row, page))
            scores["abstentions"] += sum(
                1 for v in row.values() if isinstance(v, str) and v.strip().upper() == "UNRESOLVED"
            )

    ex_study = [(r, p) for r, p in extracted if r.get("row_kind") == "STUDY_ROW"]
    scores["extracted_study_rows"] = len(ex_study)

    # match truth study rows to extracted rows: label + effect (verbatim-normalized)
    used = set()
    for t in truth_study:
        t_label, t_eff = norm_label(t.get("study_label")), norm_value(t.get("effect"))
        t_page = (t.get("source_page") or "").strip()
        best = None
        for i, (row, page) in enumerate(ex_study):
            if i in used:
                continue
            if norm_label(row.get("study_label", "")) == t_label and (
                norm_value(row.get("effect_value", "")) == t_eff
                or not row.get("effect_value")
            ):
                best = i
                break
        if best is None:
            # fall back to label-only match (numeric may be wrong — still a detection)
            for i, (row, page) in enumerate(ex_study):
                if i not in used and norm_label(row.get("study_label", "")) == t_label:
                    best = i
                    break
        if best is None:
            if len(scores["unmatched_truth_examples"]) < 8:
                scores["unmatched_truth_examples"].append(
                    f"{t.get('study_label')} {t.get('effect')} (p{t_page})"
                )
            continue
        used.add(best)
        row, page = ex_study[best]
        scores["matched"] += 1
        label_ok = re.sub(r"\s+", " ", (row.get("study_label") or "").strip()) == \
            re.sub(r"\s+", " ", (t.get("study_label") or "").strip())
        numeric_ok = norm_value(row.get("effect_value", "")) == t_eff
        ci_ok = (
            norm_value(row.get("ci_lower", "")) == norm_value(t.get("ci_lower", ""))
            and norm_value(row.get("ci_upper", "")) == norm_value(t.get("ci_upper", ""))
        )
        weight_ok = (not (t.get("weight_pct") or "").strip()) or (
            norm_value(row.get("weight", "")) == norm_value(t.get("weight_pct", ""))
        )
        scores["label_exact"] += label_ok
        scores["numeric_exact"] += numeric_ok
        scores["ci_paired"] += ci_ok
        scores["row_assembled"] += label_ok and numeric_ok and ci_ok and weight_ok
        scores["provenance_page_correct"] += str(page) == t_page

    # false extractions: extracted STUDY rows that match no truth study row
    truth_keys = {(norm_label(t.get("study_label")), norm_value(t.get("effect"))) for t in truth_study}
    truth_labels = {norm_label(t.get("study_label")) for t in truth_study}
    for i, (row, page) in enumerate(ex_study):
        if i in used:
            continue
        if norm_label(row.get("study_label", "")) not in truth_labels:
            scores["false_extractions"] += 1
            if len(scores["false_extraction_examples"]) < 8:
                scores["false_extraction_examples"].append(
                    f"{row.get('study_label')} {row.get('effect_value')} (p{page})"
                )

    # pooled-row misclassification: truth pooled rows extracted as STUDY_ROW
    pooled_labels = {norm_label(t.get("study_label")) for t in truth_pooled}
    for row, _ in ex_study:
        if norm_label(row.get("study_label", "")) in pooled_labels:
            scores["pooled_misclassified"] += 1
    return scores


def pct(n: int, d: int) -> str:
    return f"{100*n/d:.1f}%" if d else "—"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["live", "replay"], default="replay")
    ap.add_argument("--papers", nargs="*", default=None)
    args = ap.parse_args()

    router = ModelRouter()
    role, model_id = router.resolve_task("forest_plot_vision")
    if args.provider == "live":
        from app.adapters.llm.anthropic_provider import AnthropicVisionProvider
        provider = RecordingVisionProvider(AnthropicVisionProvider(), FIXTURES)
    else:
        provider = ReplayVisionProvider(FIXTURES)

    papers = args.papers or [
        p.name for p in sorted(GOLD.iterdir())
        if p.is_dir() and (p / "truth" / "published_effects.csv").exists()
        and json.loads((p / "truth" / "meta.json").read_text()).get("corpus_role") == "development"
    ]

    all_scores, run_meta = [], []
    for paper in papers:
        paper_dir = GOLD / paper
        truth_rows = truth_figure_rows(paper_dir)
        if not truth_rows:
            print(f"skip {paper}: no figure-sourced truth rows")
            continue
        try:
            run = run_pipeline(paper_dir, provider, role, model_id)
        except Exception as exc:  # provider/fixture failure — report, don't fake
            print(f"{paper}: PIPELINE FAILED — {exc}")
            all_scores.append(score_paper(paper, None, truth_rows) | {"error": str(exc)[:200]})
            continue
        scores = score_paper(paper, run.get("artifact"), truth_rows)
        scores |= {k: run[k] for k in ("cost_usd", "latency_ms", "calls", "stage_state")}
        all_scores.append(scores)
        run_meta.append(run)
        print(f"{paper}: matched {scores['matched']}/{scores['truth_study_rows']} "
              f"study rows, cost ${run['cost_usd']}")

    stamp = dt.date.today().isoformat()
    out_dir = ROOT / "corpus" / "baseline"
    (out_dir / f"vision_benchmark_{stamp}.json").write_text(json.dumps({
        "run_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "provider": args.provider, "model_role": role, "model_id": model_id,
        "prompt_version": "1", "papers": all_scores,
    }, indent=2))

    lines = [
        f"# Vision Benchmark — {stamp}",
        "",
        f"Provider: {args.provider} · role {role} → `{model_id}` · prompt v1",
        "",
        "## Per paper",
        "",
        "| Paper | Recall | Precision | Label | Numeric | CI pair | Row asm | Pooled misclass | False extr | Abstain | Prov. page | Cost | Latency |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for s in all_scores:
        m, ts, es = s["matched"], s["truth_study_rows"], s["extracted_study_rows"]
        lines.append(
            f"| {s['paper']} | {pct(m, ts)} | {pct(m, es)} | {pct(s['label_exact'], m)} "
            f"| {pct(s['numeric_exact'], m)} | {pct(s['ci_paired'], m)} | {pct(s['row_assembled'], m)} "
            f"| {s['pooled_misclassified']} | {s['false_extractions']} | {s['abstentions']} "
            f"| {pct(s['provenance_page_correct'], m)} | ${s.get('cost_usd', 0)} "
            f"| {s.get('latency_ms', 0)}ms |"
        )
    total = {k: sum(s[k] for s in all_scores) for k in
             ("matched", "truth_study_rows", "extracted_study_rows", "label_exact",
              "numeric_exact", "ci_paired", "row_assembled", "pooled_misclassified",
              "false_extractions")}
    lines += [
        "",
        "## Aggregate (secondary to per-paper)",
        "",
        f"- study-row recall {pct(total['matched'], total['truth_study_rows'])}, "
        f"precision {pct(total['matched'], total['extracted_study_rows'])}",
        f"- among matched: label {pct(total['label_exact'], total['matched'])}, "
        f"numeric {pct(total['numeric_exact'], total['matched'])}, "
        f"CI {pct(total['ci_paired'], total['matched'])}, "
        f"full row {pct(total['row_assembled'], total['matched'])}",
        f"- pooled misclassified {total['pooled_misclassified']}, "
        f"false extractions {total['false_extractions']}",
        "",
        "## Examples",
        "",
    ]
    for s in all_scores:
        if s["unmatched_truth_examples"] or s["false_extraction_examples"]:
            lines.append(f"### {s['paper']}")
            for e in s["unmatched_truth_examples"]:
                lines.append(f"- missed: {e}")
            for e in s["false_extraction_examples"]:
                lines.append(f"- false: {e}")
            lines.append("")
    (out_dir / f"vision_benchmark_{stamp}.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out_dir}/vision_benchmark_{stamp}.md")


if __name__ == "__main__":
    main()
