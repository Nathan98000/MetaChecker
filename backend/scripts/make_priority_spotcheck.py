"""PRIORITY_SPOTCHECK_V1 — the ~50-75-item researcher-validation layer.

A curated subset of SPOTCHECK_V1 (which remains intact): every consequential
contradiction, every AMBIGUOUS/UNRESOLVED item, erratum-affected examples,
unusual-source cases, pooled-row guards, plus 5-8 seeded random controls per
paper stratified by source encoding. Output: corpus/gold/PRIORITY_SPOTCHECK_V1.md.

Usage: .venv/bin/python scripts/make_priority_spotcheck.py [--seed 20260811]
"""

import argparse
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLD = ROOT / "corpus" / "gold"

DEV_PAPERS = [
    "yang-2018-sii",
    "prochaska-2012-varenicline",
    "macnamara-2014-practice",
    "hahn-2024-exercise-intake",
    "driessen-2015-nih-psychotherapy",
    "cooney-2013-exercise-depression",
    "nissen-2007-rosiglitazone",
]

# encoding class per paper (baseline evidence) for stratified random controls
ENCODING = {
    "yang-2018-sii": "raster forest plot",
    "prochaska-2012-varenicline": "text table + raster forest plot",
    "macnamara-2014-practice": "dual-layer text",
    "hahn-2024-exercise-intake": "vector no-text forest plot",
    "driessen-2015-nih-psychotherapy": "raster forest plot",
    "cooney-2013-exercise-depression": "text-encoded RevMan forest table",
    "nissen-2007-rosiglitazone": "text tables (print, pre-erratum)",
}

# contradictions filtered out as non-consequential (pure typography/wording)
TRIVIAL_MARKERS = (
    "typo", "spelling", "wording", "caption", "cosmetic", "phrasing",
    "duplicated \"2\"", "capital i", "invervention", "wallking",
)


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def fmt_effect(row: dict) -> str:
    bits = []
    for key in ("effect", "ci_lower", "ci_upper", "se", "weight_pct",
                "events_treatment", "events_control"):
        v = (row.get(key) or "").strip()
        if v and v.upper() not in ("NOT_APPLICABLE", "NA"):
            bits.append(f"{key.replace('_pct','')}={v}")
    return ", ".join(bits[:5]) or "(no numeric cells)"


def item(paper, analysis, region, value, status, page, where, reason):
    return {
        "paper": paper, "analysis": analysis, "region": region, "value": value,
        "status": status, "page": page, "where": where, "reason": reason,
    }


def build(seed: int) -> list[dict]:
    items: list[dict] = []
    for paper in DEV_PAPERS:
        truth = GOLD / paper / "truth"
        effects = read_csv(truth / "published_effects.csv")
        analyses = read_csv(truth / "analyses.csv")
        cons = read_csv(truth / "contradictions.csv")
        if not (effects or analyses):
            continue
        rng = random.Random(f"{seed}:{paper}")

        # 1. every AMBIGUOUS / UNRESOLVED row (effects + analyses)
        for row in effects:
            c = (row.get("certainty") or "").upper()
            if c in ("AMBIGUOUS", "UNRESOLVED"):
                items.append(item(paper, row.get("analysis_id", ""), row.get("study_label", ""),
                                  fmt_effect(row), c, row.get("source_page", ""),
                                  row.get("source_figure") or row.get("source_table") or "",
                                  f"{c} row — human adjudication required"))
        for row in analyses:
            c = (row.get("certainty") or "").upper()
            if c in ("AMBIGUOUS", "UNRESOLVED"):
                items.append(item(paper, row.get("analysis_id", ""), row.get("outcome", ""),
                                  f"pooled={row.get('pooled_effect','')}", c,
                                  row.get("source_page", ""),
                                  row.get("source_figure") or row.get("source_table") or "text",
                                  f"{c} analysis"))

        # 2. consequential contradictions: skip pure-typography and
        #    explained/guard rows; prioritize erratum > ambiguous > rest, cap 6
        def consequential(c):
            text = ((c.get("description") or "") + (c.get("note") or "")).lower()
            if any(m in text for m in TRIVIAL_MARKERS) and c.get("kind") != "ERRATUM":
                return False
            if any(m in text for m in ("guard", "not-an-error", "explained by", "rounding-level")):
                return False
            return True

        ranked = sorted(
            (c for c in cons if consequential(c)),
            key=lambda c: (c.get("kind") != "ERRATUM",
                           (c.get("certainty") or "") != "AMBIGUOUS"),
        )
        for c in ranked[:6]:
            items.append(item(paper, "", c.get("contradiction_id", ""),
                              f"A: {c.get('side_a_value','')} vs B: {c.get('side_b_value','')} — "
                              f"{(c.get('description') or '')[:120]}",
                              c.get("certainty", "KNOWN"),
                              f"{c.get('side_a_source','')} / {c.get('side_b_source','')}", "",
                              f"contradiction [{c.get('kind','')}] — confirm both sides as printed"))

        # 3. erratum/correction-affected examples (cap 5 per paper)
        corrected = [r for r in analyses if r.get("analysis_id", "").endswith("-2018")
                     or "CORRECTED" in (r.get("note") or "").upper()]
        corrected += [r for r in effects if "CORRECTED" in (r.get("version") or "").upper()]
        for row in (corrected if len(corrected) <= 5 else rng.sample(corrected, 5)):
            label = row.get("study_label") or row.get("outcome") or ""
            items.append(item(paper, row.get("analysis_id", ""), label,
                              fmt_effect(row) if "effect" in row else f"pooled={row.get('pooled_effect','')}",
                              "CORRECTED-VERSION", row.get("source_page", ""),
                              row.get("source_figure") or row.get("source_table") or "",
                              "erratum/corrigendum-affected value — verify both versions preserved"))

        # 4. unusual source data: author-supplied/suppressed (representative 3)
        unusual = [r for r in effects if "NOT_PUBLICLY_VERIFIABLE" in (r.get("note") or "").upper()
                   and (r.get("certainty") or "KNOWN") == "KNOWN"]
        for row in (unusual if len(unusual) <= 3 else rng.sample(unusual, 3)):
            items.append(item(paper, row.get("analysis_id", ""), row.get("study_label", ""),
                              fmt_effect(row), "SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE",
                              row.get("source_page", ""), row.get("source_figure", ""),
                              "author-supplied data — verify flagged as non-verifiable, not error"))

        # 5. pooled-row guard (one per paper)
        pooled = [r for r in effects if r.get("row_kind") in ("OVERALL_TOTAL", "SUBGROUP_TOTAL")
                  and (r.get("certainty") or "KNOWN") == "KNOWN"]
        if pooled:
            row = rng.choice(pooled)
            items.append(item(paper, row.get("analysis_id", ""), row.get("study_label", ""),
                              fmt_effect(row), "KNOWN", row.get("source_page", ""),
                              row.get("source_figure") or row.get("source_table") or "",
                              f"pooled row ({row.get('row_kind')}) — confirm not mistakable for a study row"))

        # 6. random controls: 5 per paper, stratified across statistic presence
        study_rows = [r for r in effects if r.get("row_kind") in ("STUDY",)
                      and (r.get("certainty") or "KNOWN") == "KNOWN"
                      and not any(r is x for x in unusual)]
        with_events = [r for r in study_rows if (r.get("events_treatment") or "").strip()]
        without = [r for r in study_rows if r not in with_events]
        sample = []
        for pool, k in ((with_events, 2), (without, 3)):
            if pool:
                sample += rng.sample(pool, min(k, len(pool)))
        for row in sample[:5]:
            items.append(item(paper, row.get("analysis_id", ""), row.get("study_label", ""),
                              fmt_effect(row), "KNOWN", row.get("source_page", ""),
                              row.get("source_figure") or row.get("source_table") or "",
                              f"random control ({ENCODING.get(paper, '?')})"))
    return items


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260811)
    args = ap.parse_args()
    items = build(args.seed)

    lines = [
        "# PRIORITY_SPOTCHECK_V1 — Researcher Validation Layer",
        "",
        f"{len(items)} items (seed {args.seed}). This is the efficient validation",
        "layer on top of SPOTCHECK_V1 (which remains available in full). Open the",
        "source PDF at the stated page and confirm the truth value/status matches",
        "the printed source verbatim. For contradictions, confirm both sides are",
        "printed as recorded — you are validating the documentation, not resolving",
        "the disagreement. Mark ✓/✗ and note corrections; corrections become",
        "versioned truth revisions (see freeze protocol at bottom).",
        "",
    ]
    current = None
    for it in items:
        if it["paper"] != current:
            current = it["paper"]
            lines += [f"## {current}  _({ENCODING.get(current, '')})_", "",
                      "| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |",
                      "|---|---|---|---|---|---|---|---|"]
        lines.append(
            f"| ☐ | {it['analysis']} | {it['region']} | {it['value']} | {it['status']} "
            f"| {it['page']} | {it['where']} | {it['reason']} |"
        )
    lines += [
        "",
        "---",
        "## Freeze protocol",
        "",
        "All truth files are currently **PRE-FREEZE** (AI double-pass reconciled,",
        "human-unverified). After completing this package: record",
        "`Researcher spot-check: PASSED/CORRECTED <date>` in each paper's",
        "truth/notes.md, then tag the repository `gold-truth-v1` → GOLD_TRUTH_V1.",
        "Post-freeze corrections must be versioned revisions, never silent edits.",
        "Benchmarks run before sign-off are labeled BENCHMARK_AGAINST_PREFREEZE_TRUTH.",
    ]
    out = GOLD / "PRIORITY_SPOTCHECK_V1.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out} ({len(items)} items)")


if __name__ == "__main__":
    main()
