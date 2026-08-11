# Phase 1 Baseline — 2026-08-11

Pipeline: pymupdf_baseline v1 (native text spans only)

Metric: presence of KNOWN truth values, verbatim, in the extracted
text layer (ceiling for downstream numeric extraction). AMBIGUOUS/
UNRESOLVED truth rows are excluded from denominators (abstention is
correct). 'Found elsewhere' = present in document text but not on the
truth source page.

| Paper | Parse | Pages | Study values on-page | elsw. | miss. | Pooled on-page | elsw. | miss. | Labels on-page | elsw. | miss. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| macnamara-2014-practice | SUCCESS | 14 | 0/0 | 0 | 0 | 22/33 | 11 | 0 | 0/0 | 0 | 0 |
| prochaska-2012-varenicline | SUCCESS | 11 | 492/820 | 161 | 167 | 27/30 | 0 | 3 | 22/44 | 0 | 22 |
| yang-2018-sii | SUCCESS | 8 | 15/160 | 24 | 121 | 50/70 | 14 | 6 | 22/44 | 0 | 22 |

## Study values by source type (the routing signal)

| Paper | Source | on-page | elsewhere | missing |
|---|---|---|---|---|
| macnamara-2014-practice | FOREST_PLOT | 0/0 | 0 | 0 |
| prochaska-2012-varenicline | FOREST_PLOT | 4/332 | 161 | 167 |
| prochaska-2012-varenicline | TABLE | 488/488 | 0 | 0 |
| yang-2018-sii | FOREST_PLOT | 15/160 | 24 | 121 |

## Not measured (capability does not exist yet)

- analysis identification (no stage yet)
- structured forest-plot row assembly (no stage yet)
- structured table-record assembly (no stage yet)
- per-value bounding-box association (spans have bboxes; value→span linking not implemented)
- reference-list recovery (no stage yet)
- false-extraction rate for structured claims (nothing asserts structured values yet)

## Missing-value examples (first 12 per paper)

### prochaska-2012-varenicline
- Fagerström 2010/effect: '-0.0046'
- [dup]Fagerström 2010/effect: '-0.0046'
- Fagerström 2010/ci_lower: '-0.0173'
- [dup]Fagerström 2010/ci_lower: '-0.0173'
- Fagerström 2010/ci_upper: '0.0081'
- [dup]Fagerström 2010/ci_upper: '0.0081'
- Fagerström 2010/weight_pct: '5.12'
- [dup]Fagerström 2010/weight_pct: '5.12'
- Rennard 2012/effect: '0.0000'
- [dup]Rennard 2012/effect: '0.0000'
- Rennard 2012/ci_lower: '-0.0087'
- [dup]Rennard 2012/ci_lower: '-0.0087'

### yang-2018-sii
- Hong (2015)/effect: '1.38'
- [dup]Hong (2015)/effect: '1.38'
- Hong (2015)/ci_lower: '1.02'
- [dup]Hong (2015)/ci_lower: '1.02'
- Hong (2015)/ci_upper: '1.85'
- [dup]Hong (2015)/ci_upper: '1.85'
- Hong (2015)/weight_pct: '5.67'
- [dup]Hong (2015)/weight_pct: '5.67'
- Loll (2016)/ci_lower: '1.35'
- [dup]Loll (2016)/ci_lower: '1.35'
- Loll (2016)/ci_upper: '2.50'
- [dup]Loll (2016)/ci_upper: '2.50'

- skipped cooney-2013-exercise-depression: missing PDF or truth files
- skipped driessen-2015-nih-psychotherapy: missing PDF or truth files
- skipped goyal-2014-meditation: holdout — not run
- skipped hahn-2024-exercise-intake: missing PDF or truth files
- skipped nissen-2007-rosiglitazone: missing PDF or truth files
- skipped singh-2011-varenicline: holdout — not run
- skipped smith-silva-2011-ethnic-identity: holdout — not run

---

## Frozen Phase-1 baseline — interpretation (2026-08-11)

This file is the frozen pre-orchestration baseline (researcher directive:
measure before adding parsing complexity). Every parser addition must rerun
`backend/scripts/run_baseline.py` and compare against these numbers.

Headline findings:

1. **Native text extraction saturates text-encoded tables**: 488/488 (100%)
   of KNOWN table-sourced study values present on the correct page
   (Prochaska Table 2, four effect measures × 22 trials).
2. **Forest plots in both quantitative dev papers are raster images**:
   figure-sourced values are 1% (Prochaska, 4/332) and 9% (Yang, 15/160)
   reachable — and most of those hits are values that also appear in body
   text. Study labels split identically (table labels 22/22, figure labels
   0/22 per paper). Native text extraction cannot audit these figures at all.
3. **"Found elsewhere" is a real signal**: 161 Prochaska figure values are
   recoverable from the text-encoded Table 2 on a different page —
   cross-representation redundancy can substitute for figure reading when a
   table twin exists, but provenance must then point at the table, not the
   figure.
4. **Pooled analysis values are mostly text-reachable** (Macnamara 22/33
   on-page + 11 on other pages + 0 missing; Yang 50/70 + 14 elsewhere;
   Prochaska 27/30): abstracts/results text carry pooled estimates even when
   plots are images.
5. **Trivial targets excluded**: 212 Prochaska values (mostly the literal
   "0" RD cells) are too short for presence testing and are excluded from
   denominators rather than counted as fake successes.
6. **Adversarial property confirmed in the wild**: the Macnamara composite
   carries dual text layers (original + corrected values on the same pages) —
   "one text layer per page" is not a safe assumption; parse artifacts must
   preserve contradictory co-located spans.

## Addendum (same day): Hahn 2024 truth set added

Fourth development paper confirms the routing signal on a third publisher
(BMC/Springer): forest-plot-sourced values 4/368 (1%) natively reachable —
its six RevMan forest plots have no text layer at all (vector/image Form
XObjects). 99 values recoverable elsewhere (body text/Table 1 means), 265
unreachable without figure interpretation. Full run table in
baseline_2026-08-11.{md,json}. The pattern now holds across Ivyspring (Yang),
BMJ (Prochaska figures), and BMC (Hahn): native text extraction covers
text-encoded tables completely and forest plots essentially not at all.

## Addendum 2 (same day): Driessen 2015 truth set added

Fifth development paper, fourth publisher (PLOS): forest-plot values 63/410
(15%) natively on-page (PLOS raster figures; the higher rate reflects Table-2
pool values that also appear near the figures), 119 recoverable elsewhere,
228 figure-locked. Cross-publisher conclusion unchanged and now four-for-four:
text-encoded tables ≈100%, forest plots 1–15%. Driessen additionally
contributes 19 unpublished-study rows flagged
SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE (6 fully suppressed, certainty UNRESOLVED)
— the corpus's A22 abstention fixtures.

## Addendum 3 (same day): Cooney 2013 truth set added — the counter-case

Cochrane/RevMan forest "plots" are fully TEXT-ENCODED: 297/297 (100%) study
values and 72/72 labels on-page natively. Conclusion sharpened: it is figure
ENCODING, not figure format, that determines native reachability — RevMan
vector-text forests are completely readable; journal-typeset raster/vector-art
plots (Yang 1-9%, Prochaska 1%, Hahn 1%, Driessen 15%) are not. The
detect_figure_regions `needs_vision` signal (interior-text presence) routes
exactly this distinction, so Cooney-style documents will bypass vision
entirely — the escalation architecture is validated in both directions.
