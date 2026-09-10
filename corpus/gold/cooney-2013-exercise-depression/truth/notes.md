# Truth provenance — cooney-2013-exercise-depression

Status: **DRAFT** (researcher spot-check and sign-off pending)

Source: PMC deposit PMC9721454.pdf (132 pages), Cooney GM et al., "Exercise for
depression", Cochrane Database of Systematic Reviews 2013, Issue 9, CD004366,
DOI 10.1002/14651858.CD004366.pub6. All `source_page` values are 1-based pages
of this PDF (printed Cochrane page = PDF page − 3 for the main sequence).

## Construction

- Pass A and Pass B (`pass-a-raw.md`, `pass-b-raw.md`): two independent blind
  extraction passes, 2026-08-11. Both used the PyMuPDF text layer and both
  cross-verified the text-layer numbers against rendered page images of the
  truthed pages (RevMan forest tables in this deposit are typeset text with
  graphical overlays; no OCR was needed for any truthed cell).
- Reconciliation (this file + the four CSVs): value-by-value diff of both
  passes across all rows of Analyses 1.1, 1.3 and 1.2, the analysis-level
  values, the study-label sets, the review-level summary numbers, and the full
  analysis inventory. Performed 2026-08-11.

## Numeric disagreements between passes

**ZERO.** Every truthed numeric value agreed between Pass A and Pass B:

- Analysis 1.1: all 35 study rows (N, Mean(SD), effect, CI, weight), total row,
  heterogeneity/test lines — identical.
- Analysis 1.2: all 8 study rows, total row, heterogeneity/test lines — identical.
- Analysis 1.3: all 29 study rows (n/N cells, RR, CI, weight), total row,
  total-events line, heterogeneity/test lines — identical.
- Analysis-level values (pooled effects, CIs, I2, Tau2, Chi2, df, Z, P) — identical.
- Study-label sets (35 / 8 / 29 labels and their subset relations) — identical.
- Review-level summary numbers (39/2326, 37, 35/1356-vs-1353, 464, 377, 189,
  300/298, 18, SOF values) — identical, including both passes independently
  finding the same internal contradictions.

Non-numeric / metadata discrepancies between the passes (not truth-cell values;
logged for completeness, none affects a CSV cell):

1. TOC analysis count in the document survey: Pass A says "24 analyses",
   Pass B says "23". Both passes' inventories list the **same 23 analyses**
   (1.1–1.4, 2.1–2.3, 3.1, 4.1–4.3, 5.1–5.5, 6.1–6.7); resolved as 23
   (Pass A survey sentence was a miscount).
2. Figure 3 page span: Pass A "p24-25" vs Pass B "p24". Untruthed content;
   left unadjudicated (figure likely spans the page break).
3. Comparison 3 summary-table page: Pass A "p109" vs Pass B "p110". Untruthed
   content; left unadjudicated (table sits at the p109/p110 boundary).
4. Minor forest page-range boundaries in the inventory: 5.5 "p118-120" (A) vs
   "p118-119" (B); 6.7 "p123" (A) vs "p123-124" (B). Page-break boundary
   differences on untruthed analyses; left unadjudicated.

## Certainty adjudication

- All truthed cells: **KNOWN** (both passes; no unreadable cells, zero
  UNRESOLVED rows).
- Multi-arm arm selection (which arms feed the Analysis 1.3 randomised
  denominators, e.g. Klein 1985 15/27 vs 16/24, Krogh 2009 48/55): printed
  cells KNOWN; arm attribution **AMBIGUOUS** — recorded as COO-CON-7 with
  row-level cross-references, matching Pass B's split and Pass A's oddity log.
- Blumenthal 1999 follow-up SD-vs-SE suspicion (Analysis 1.2 "10.6 (0.8)" /
  "11 (0.8)"): cells recorded verbatim as KNOWN; the suspicion itself is
  **AMBIGUOUS** (COO-CON-9) — it cannot be resolved from this PDF.

## Sanity checks (recomputed at reconciliation)

- Analysis 1.1: Σ N exercise = 711, Σ N control = 642; 711+642 = **1353** =
  printed total; study weights sum **100.03** (RevMan rounding).
- Analysis 1.2: 194 + 183 = **377** = printed total; weights sum **100.00**.
- Analysis 1.3: Σ denominators 696 + 667 = **1363** = printed total;
  Σ numerators 610 + 577 = printed "Total events"; weights sum **100.00**.
- Stated k vs plot rows: 35/35, 8/8, 29/29 — all match.

## Subset rationale (which analyses were truthed, and why)

Both passes independently chose the same three targets for structural
diversity; their reasoning agreed:

- **T1 = Analysis 1.1** (35 studies, 1353): the review's primary/headline
  continuous SMD random-effects forest — mandated target. Flat (no subgroups),
  spans a page break (p105–106), carries the 1353-vs-1356 count contradiction
  (COO-CON-1) and the I2 62.78%-vs-63% precision difference (COO-CON-3).
- **T2 = Analysis 1.3** (29 studies, 1363): by far the largest dichotomous
  analysis in the review (alternatives: 2.2 k=4, 4.2 k=3). Adds: events/total
  n/N cells instead of Mean(SD), M-H weighting, log-scaled axis (0.5–2) with
  arrow-clipped CIs, a "Total events" line absent from continuous forests,
  null pooled effect printed as bare "1", a differently-labelled pooled row
  ("Total (95% CI)" vs "Total ***"), weights spanning 0.11%–22.56%, I2=0%,
  a two-page span (p106–107), and randomised-N denominators that deliberately
  disagree with the completer Ns of 1.1 (COO-CON-7) — a rich trap for auditors.
- **T3 = Analysis 1.2** (8 studies, 377): the review's only true follow-up
  analysis (Comparison 6 items are sensitivity re-runs of post-treatment data,
  not follow-up), forming the natural post-treatment/follow-up pair with 1.1.
  Adds: a strict subset of 1.1's studies with different Ns/means for the same
  labels (e.g. Blumenthal 1999: 55/48 post vs 29/29 follow-up), data sourced
  from companion publications (Babyak 2000, Singh 2001), a different axis
  range, borderline-significant pool (Z=2.18, P=0.03), moderate I2 (48.71%),
  and the suspected SE-as-SD cells (COO-CON-9) — tests whether an auditor
  links rather than conflates the paired analyses.
- Together the three cover: continuous SMD + dichotomous RR; IV random +
  M-H random; I2 of 0% / 48.71% / 62.78%; single-page and cross-page forests;
  and the review's central published claims (headline −0.62, acceptability
  RR 1.00, follow-up −0.33).

## Review-level headline rows in analyses.csv

Besides the three truthed analyses, `analyses.csv` carries four rows for the
abstract's headline numbers that map cleanly onto single published analyses
(A2.1 psychological therapies, A3.1 bright light, A4.1 pharmacological,
A6.6 robust-trials sensitivity). These are sourced from the Abstract text;
their forests are NOT truthed row-by-row. Everything else lives in the
inventory below.

## Full analysis inventory (all 23 analyses; * = truthed)

id | title (verbatim incl. typos) | k | n | measure/model | pooled effect as printed | PDF pages

- 1.1* | Reduction in depression symptoms post-treatment | 35 | 1353 | SMD (IV, Random) | -0.62 [-0.81, -0.42] | 105-106
- 1.2* | Reduction in depression symptoms follow-up | 8 | 377 | SMD (IV, Random) | -0.33 [-0.63, -0.03] | 106
- 1.3* | Completed intervention or control | 29 | 1363 | RR (M-H, Random) | 1.00 [0.97, 1.04] | 106-107
- 1.4 | Quality of life | 4 | — | SMD (IV, Fixed) | Subtotals only — 1.4.1 Mental 2/59 -0.24 [-0.76, 0.29]; 1.4.2 Psychological 2/56 0.28 [-0.29, 0.86]; 1.4.3 Social 2/56 0.19 [-0.35, 0.74]; 1.4.4 Environment 2/56 0.62 [0.06, 1.18]; 1.4.5 Physical 4/115 0.45 [0.06, 0.83] | 107-108
- 2.1 | Reduction in depression symptoms post-treatment (vs psychological therapies) | 7 | 189 | SMD (IV, Random) | -0.03 [-0.32, 0.26] | 108-109 (comparator column headed "Cognitive Therapy")
- 2.2 | Completed exercise or pyschological therapies [sic] | 4 | 172 | RR (M-H, Random) | 1.08 [0.95, 1.24] | 109
- 2.3 | Quality of life (vs psychological therapies) | 1 | — | MD (IV, Fixed) | Totals not selected (table prints "0.0 [0.0, 0.0]"; forest rows: Physical 0.15 [-7.4, 7.7], Mental -0.09 [-9.51, 9.33]; Gary 2010) | 109
- 3.1 | Reduction in depression symptoms post-treatment (vs bright light therapy) | 1 | 18 | MD (IV, Fixed) | -6.4 [-10.20, -2.60] (Pinchasov 2000) | 110
- 4.1 | Reduction in depression symptoms post-treatment (vs pharmacological treatments) | 4 | 300 | SMD (IV, Random) | -0.11 [-0.34, 0.12] (Effects text says 298 participants — COO-CON-4) | 110
- 4.2 | Completed exercise or antidepressants | 3 | 278 | RR (M-H, Random) | 0.98 [0.86, 1.12] (forest I2=61.09%) | 111
- 4.3 | Quality of Life (vs pharmacological treatments) | 1 | — | MD (IV, Fixed) | Subtotals only — Mental 1/25 -11.90 [-24.04, 0.24]; Physical 1/25 1.30 [-0.67, 3.27] (Brenes 2007) | 111
- 5.1 | Exercise vs control subgroup analysis: type of exercise | 35 | — | SMD (IV, Random) | Subtotals only — Aerobic 28/1080 -0.55 [-0.77, -0.34]; Mixed 3/128 -0.85 [-1.85, 0.15]; Resistance 4/144 -1.03 [-1.52, -0.53] | 113-114
- 5.2 | Exercise vs control subroup [sic] analysis: intensity | 35 | — | SMD (IV, Random) | Subtotals only — light/moderate 3/76 -0.83; moderate 12/343 -0.64; hard 11/595 -0.56; vigorous 5/230 -0.77; moderate/hard 2/66 -0.63; moderate/vigorous 2/42 -0.38 | 114-116
- 5.3 | Exercise vs control subroup analysis: number of sessions | 35 | — | SMD (IV, Random) | Subtotals only — 0-12: 5/195 -0.42; 13-24: 9/296 -0.70; 25-36: 8/264 -0.80; 37+: 10/524 -0.46; unclear 3/73 -0.89 | 116-117
- 5.4 | Exercise vs control subroup analysis: diagnosis of depression | 35 | — | SMD (IV, Random) | Subtotals only — clinical diagnosis 23/967 -0.57; cut points on a scale 11/367 -0.67; unclear 1/18 -2.00 | 117-118
- 5.5 | Exercise vs control subgroup analysis: type of control | 35 | 1353 | MD (IV, Fixed) | -1.57 [-1.97, -1.16] — placebo 2/156 -2.66; no treatment/waiting list/usual care/self monitoring 17/563 -4.75; exercise plus treatment vs treatment 6/225 -1.22; stretching/meditation/relaxation 6/219 -0.09; occupational/health education/casual conversation 4/190 -3.67 (measure switch + Discussion mislabel — COO-CON-10) | 118-120 (A) / 118-119 (B)
- 6.1 | Sensitivity: peer-reviewed journal publications and doctoral theses only | 34 | 1335 | SMD (IV, Random) | -0.59 [-0.78, -0.40] | 120-121
- 6.2 | Sensitivity: studies published as abstracts or conference proceedings only | 1 | 18 | SMD (IV, Random) | -2.00 [-3.19, -0.82] | 121
- 6.3 | Sensitivity: studies with adequate allocation concealment | 14 | 829 | SMD (IV, Random) | -0.49 [-0.75, -0.24] | 121-122
- 6.4 | Sensitivity: studies using intention-to-treat analysis | 11 | 567 | SMD (IV, Random) | table prints "-0.61 [1.00, -0.22]" [sic — sign typo, COO-CON-5]; forest total -0.61 [-1, -0.22] | 122
- 6.5 | Sensitivity: studies with blinded outcome assessment | 12 | 658 | SMD (IV, Random) | -0.36 [-0.60, -0.12] | 122-123
- 6.6 | Sensitivity: allocation concealment, intention-to-treat, blinded outcome | 6 | 464 | SMD (IV, Random) | -0.18 [-0.47, 0.11] | 123
- 6.7 | Sensitivity: Lowest dose of exercise | 35 | 1347 | SMD (IV, Fixed) | -0.44 [-0.55, -0.33] | 123 (A) / 123-124 (B)

Trials included in the review but in no meta-analysis: Greist 1979; McCann 1984
(PDF p27). Review-level: 39 trials / 2326 participants included; 37 in
meta-analyses.

## Verbatim quirks (documented, not contradictions)

- RevMan drops trailing zeros: "1[0.97,1.04]", "-2[-3.19,-0.82]",
  "-1[-1.69,-0.31]", weights "4.1%" / "2.9%"; rounding artifacts like
  "Z=3.3(P=0)" (Analysis 3.1) and "df=1(P=0)" (Analysis 1.4.2).
- Pooled-row label differs by data type: "Total ***" (continuous) vs
  "Total (95% CI)" (dichotomous).
- Typos preserved verbatim: "pyschological" (Analysis 2.2), "subroup"
  (Analyses 5.2-5.4, also in TOC); body text "Hoﬀman 2010" (ff ligature) vs
  forest "Hoffman 2010".
- Text-layer extraction artifact: forest axis tick labels extract in scrambled
  order (e.g. "Favours exercise 5 2.5 -5 -2.5 0 Favours control"); graphics
  artifact only, no truthed cell affected.

## Sign-off

- [ ] Researcher spot-check against source PDF
- [ ] Sign-off recorded here (name, date) — until then status remains DRAFT

TRUTH_STATUS: PRE_FREEZE — AI double-pass reconciled, human-unverified.
Benchmarks against this state are BENCHMARK_AGAINST_PREFREEZE_TRUTH.
Researcher corrections become versioned revisions; freeze tag: gold-truth-v1.
