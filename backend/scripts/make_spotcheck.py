"""Generate the researcher spot-check package for Truth Set v1 sign-off.

Selection rules (researcher directive, 2026-08-11):
- ~10-20 seeded-random rows per development paper (stratified: forest + table);
- every documented contradiction;
- every correction/erratum-affected value (AS_CORRECTED versions + pairs);
- every AMBIGUOUS or UNRESOLVED row;
- rows whose notes indicate interpretation was required (note text present).

Output: corpus/gold/SPOTCHECK_V1.md — compact review artifact with, per item:
truth value | source page | source table/figure | exact source region (row
label) | reason selected. Sign-off procedure at the end. Deterministic given
the seed, so the package is reproducible.

Usage: .venv/bin/python scripts/make_spotcheck.py [--seed 20260811] [--per-paper 15]
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
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def effect_item(row: dict, reason: str) -> dict:
    value_bits = []
    for key in ("effect", "ci_lower", "ci_upper", "se", "weight_pct",
                "events_treatment", "events_control", "n_treatment", "n_control"):
        v = (row.get(key) or "").strip()
        if v and v.upper() not in ("NOT_APPLICABLE", "NA"):
            value_bits.append(f"{key}={v}")
    return {
        "id": row.get("effect_id", "?"),
        "value": f"{row.get('study_label', '?')}: " + ", ".join(value_bits[:6]),
        "page": row.get("source_page", "?"),
        "where": row.get("source_figure") or row.get("source_table") or row.get("source_type", "?"),
        "region": row.get("row_label") or row.get("study_label", "?"),
        "reason": reason,
        "certainty": row.get("certainty", "KNOWN"),
    }


def analysis_item(row: dict, reason: str) -> dict:
    return {
        "id": row.get("analysis_id", "?"),
        "value": f"{row.get('outcome','?')} [{row.get('subgroup_of','') and 'sub'}] "
                 f"pooled={row.get('pooled_effect','')} CI=[{row.get('pooled_ci_lower','')},"
                 f"{row.get('pooled_ci_upper','')}] I2={row.get('i2','')}",
        "page": row.get("source_page", "?"),
        "where": row.get("source_figure") or row.get("source_table") or "text",
        "region": row.get("outcome", "?"),
        "reason": reason,
        "certainty": row.get("certainty", "KNOWN"),
    }


def build_paper_section(paper: str, rng: random.Random, per_paper: int) -> tuple[list[dict], dict]:
    truth = GOLD / paper / "truth"
    effects = read_csv(truth / "published_effects.csv")
    analyses = read_csv(truth / "analyses.csv")
    contradictions = read_csv(truth / "contradictions.csv")

    items: list[dict] = []
    seen_ids: set[str] = set()

    def add(item: dict):
        key = f"{item['id']}|{item['reason'][:20]}"
        if key not in seen_ids:
            seen_ids.add(key)
            items.append(item)

    # 1. Every AMBIGUOUS/UNRESOLVED row
    for row in effects:
        if (row.get("certainty") or "").upper() in ("AMBIGUOUS", "UNRESOLVED"):
            add(effect_item(row, f"certainty={row['certainty']} — must be human-adjudicated"))
    for row in analyses:
        if (row.get("certainty") or "").upper() in ("AMBIGUOUS", "UNRESOLVED"):
            add(analysis_item(row, f"certainty={row['certainty']}"))

    # 2. Every erratum/correction-affected value
    for row in effects:
        if "CORRECTED" in (row.get("version") or "").upper():
            add(effect_item(row, "erratum/correction-affected value"))
    for row in analyses:
        note_version = (row.get("note") or "") + (row.get("analysis_id") or "")
        if "CORRECTED" in note_version.upper() or row.get("analysis_id", "").endswith("-2018"):
            add(analysis_item(row, "corrigendum-affected value (before/after pair)"))

    # 3. Rows whose notes indicate interpretation rather than transcription
    #    (keyword-gated and capped — informational notes don't qualify)
    INTERPRETATION_MARKERS = (
        "ambiguous", "attribution", "differs", "misprint", "likely",
        "presumably", "contradicts", "discrepan", "variant", "swap",
        "verified at", "glyph", "recomputed", "re-split", "unsplit",
    )
    noted = [
        row for row in effects
        if (row.get("certainty") or "KNOWN") == "KNOWN"
        and any(m in (row.get("note") or "").lower() for m in INTERPRETATION_MARKERS)
    ]
    for row in noted if len(noted) <= 10 else rng.sample(noted, 10):
        add(effect_item(row, f"interpretation noted: {(row.get('note') or '')[:80]}"))

    # 4. Seeded random sample, stratified by source type
    known_rows = [r for r in effects if (r.get("certainty") or "KNOWN") == "KNOWN"
                  and r.get("row_kind") in ("STUDY", "STUDY_ROW")]
    by_type: dict[str, list[dict]] = {}
    for r in known_rows:
        by_type.setdefault(r.get("source_type", "?"), []).append(r)
    quota = max(per_paper - min(len(items), per_paper // 2), 6)
    for source_type, rows in sorted(by_type.items()):
        take = max(2, quota // max(len(by_type), 1))
        for row in rng.sample(rows, min(take, len(rows))):
            add(effect_item(row, f"random sample ({source_type})"))

    # 5. One pooled row per paper
    pooled = [r for r in effects if r.get("row_kind") in ("OVERALL_TOTAL", "SUBGROUP_TOTAL")]
    if pooled:
        add(effect_item(rng.choice(pooled), "random pooled-row check (row_kind guard)"))

    stats = {
        "effects_total": len(effects),
        "analyses_total": len(analyses),
        "contradictions": len(contradictions),
        "items": len(items),
    }
    return items, {"stats": stats, "contradictions": contradictions}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260811)
    ap.add_argument("--per-paper", type=int, default=15)
    args = ap.parse_args()

    lines = [
        "# Truth Set v1 — Researcher Spot-Check Package",
        "",
        f"Seed: {args.seed} (regenerate identically with `make_spotcheck.py --seed {args.seed}`)",
        "",
        "For each item: open the source PDF at the stated page/figure and confirm",
        "the truth value matches the printed source exactly (verbatim, at printed",
        "precision). Mark ✓ / ✗ / note. Contradiction items: confirm both sides",
        "are printed as recorded — you are confirming the *documentation*, not",
        "resolving the contradiction.",
        "",
    ]
    grand = 0
    for paper in DEV_PAPERS:
        truth_dir = GOLD / paper / "truth"
        if not (truth_dir / "published_effects.csv").exists() and not (truth_dir / "analyses.csv").exists():
            lines += [f"## {paper}", "", "_Truth set not yet constructed — excluded._", ""]
            continue
        rng = random.Random(f"{args.seed}:{paper}")
        items, extra = build_paper_section(paper, rng, args.per_paper)
        grand += len(items) + len(extra["contradictions"])
        s = extra["stats"]
        lines += [
            f"## {paper}",
            "",
            f"_{s['effects_total']} effect rows, {s['analyses_total']} analyses, "
            f"{s['contradictions']} documented contradictions → {len(items)} value checks "
            f"+ {s['contradictions']} contradiction confirmations._",
            "",
            "| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |",
            "|---|---|---|---|---|---|---|",
        ]
        for it in items:
            lines.append(
                f"| ☐ | {it['id']} | {it['value']} | {it['page']} | {it['where']} "
                f"| {it['region']} | {it['reason']} |"
            )
        if extra["contradictions"]:
            lines += ["", "**Contradictions to confirm (both sides as printed):**", ""]
            for c in extra["contradictions"]:
                lines.append(
                    f"- ☐ **{c.get('contradiction_id','?')}** [{c.get('kind','')}] "
                    f"{c.get('description','')[:180]} — A: `{c.get('side_a_value','')}` "
                    f"({c.get('side_a_source','')}) vs B: `{c.get('side_b_value','')}` "
                    f"({c.get('side_b_source','')})"
                )
        lines.append("")

    lines += [
        "---",
        "",
        "## Sign-off",
        "",
        f"Total review items: {grand}.",
        "",
        "When review is complete, record in each paper's `truth/notes.md`:",
        "`Researcher spot-check: PASSED/CORRECTED, <date>, <initials>` and set the",
        "paper's status to SIGNED_OFF. When all development papers are signed off,",
        "tag the corpus state as **GOLD_TRUTH_V1** (git tag `gold-truth-v1`).",
        "GOLD_TRUTH_V1 is immutable: any later correction creates a versioned",
        "revision (new dated notes entry + git-tracked change), never a silent edit.",
    ]
    out = GOLD / "SPOTCHECK_V1.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out} ({grand} review items)")


if __name__ == "__main__":
    main()
