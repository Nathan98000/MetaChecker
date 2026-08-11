# PRIORITY_SPOTCHECK_V1 — Researcher Validation Layer

71 items (seed 20260811). This is the efficient validation
layer on top of SPOTCHECK_V1 (which remains available in full). Open the
source PDF at the stated page and confirm the truth value/status matches
the printed source verbatim. For contradictions, confirm both sides are
printed as recorded — you are validating the documentation, not resolving
the disagreement. Mark ✓/✗ and note corrections; corrections become
versioned truth revisions (see freeze protocol at bottom).

## yang-2018-sii  _(raster forest plot)_

| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |
|---|---|---|---|---|---|---|---|
| ☐ | A4;A5;A6 | (no Overall row printed) | (no numeric cells) | UNRESOLVED | 6 | Figure 5 | UNRESOLVED row — human adjudication required |
| ☐ |  | YAN-CON-10 | A: Liu[11] / Gao[10] vs B: reference titles — Possible citation misalignment: Table 1 Liu[11] cites a C-reactive-protein/albumin-ratio paper, Gao[10] cites a myeloid- | AMBIGUOUS | Table 1 p.3 / References p.8 |  | contradiction [EXTERNAL_CRITIQUE] — confirm both sides as printed |
| ☐ |  | YAN-CON-1 | A: 2.38 vs B: 2.80 — HCC subgroup upper CI: Table 2 prints 1.59-2.38; Abstract and Results text print 1.59-2.80 | KNOWN | Table 2, PDF p.4 / Abstract p.1 / Results p.3 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | YAN-CON-2 | A: 1.69 (1.42-2.01) overall vs B: e.g. Asian 1.26 (1.12-1.40) + Caucasian 1.55 (0.84-2.27) — Every OS partition's subgroup HRs fall below the overall pooled HR 1.69 (Asian 1.26/Caucasian 1.55; <=255 1.14/>255 1.31 | KNOWN | Figure 2 p.4 / Table 2 p.4 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | YAN-CON-3 | A: P=0.009 / P<0.001 vs B: CIs crossing/touching 1 — p-values inconsistent with CIs in Table 2: Caucasian CI 0.84-2.27 crosses 1 with P=0.009; Sample<=255 CI 0.89-1.39 with  | KNOWN | Table 2 p.4 / Table 2 p.4 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | YAN-CON-4 | A: subtotals 25.38+48.76+25.87 vs B: (no overall row) — Figure 5 bottom panel (DFS/CSS/RFS) lacks an Overall row and x-axis labels; subtotal weights sum to 100.01 implying an u | KNOWN | Figure 5 p.6 / Figure 5 p.6 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | YAN-CON-5 | A: three p<0.001 claims vs B: Other: 1.77 (1.30-2.41), one p<0.001 — Abstract/Discussion claim separate significance for SCLC, NSCLC, Acral Melanoma (each p<0.001) but Table 2 pools them as | KNOWN | Abstract p.1 / Table 2 p.4 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ | A6 | Subtotal (RFS) | effect=1.66, ci_lower=1.07, ci_upper=2.59, weight=25.87 | KNOWN | 6 | Figure 5 | pooled row (SUBGROUP_TOTAL) — confirm not mistakable for a study row |
| ☐ | A1 | Ha (2016) | effect=0.93, ci_lower=0.59, ci_upper=1.45, weight=4.68 | KNOWN | 4 | Figure 2 | random control (raster forest plot) |
| ☐ | A6 | Yu (2017) | effect=1.66, ci_lower=1.07, ci_upper=2.59, weight=25.87 | KNOWN | 6 | Figure 5 | random control (raster forest plot) |
## prochaska-2012-varenicline  _(text table + raster forest plot)_

| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |
|---|---|---|---|---|---|---|---|
| ☐ | A1 | Steinberg et al | effect=−0.06, ci_lower=−0.07, ci_upper=6.87, events_treatment=1/40, events_control=1/39 | AMBIGUOUS | 9 | Table 2 | AMBIGUOUS row — human adjudication required |
| ☐ | A3 | Fagerstrom et al | effect=0.34, ci_lower=0.14, ci_upper=8.34, events_treatment=0/214, events_control=1/218 | AMBIGUOUS | 9 | Table 2 | AMBIGUOUS row — human adjudication required |
| ☐ |  | PRO-CON-4 | A: 0.14 vs B: 0.01 / 0.00 — Fagerstrom M-H OR CI printed '0.34 (0.14 to 8.34)': lower 0.14 inconsistent with RR lower 0.01 and Peto lower 0.00 on id | AMBIGUOUS | Table 2 p.9 (OR col) / Table 2 p.9 (RR/Peto cols) |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | PRO-CON-1 | A: −0.06 (−0.07 to 6.87) vs B: -0.0006 (-0.0699 to 0.0687) — Steinberg RD: Table 2 prints '−0.06 (−0.07 to 6.87)' but Fig 2 prints '-0.0006 (-0.0699 to 0.0687)' — table lower bound  | KNOWN | Table 2 p.9 / Fig 2 p.10 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | PRO-CON-3 | A: 8.13 vs B: 8.12 — Jorenby 2006 weight: Fig 2 prints 8.13; Fig 3 prints 8.12 | KNOWN | Fig 2 p.10 / Fig 3 p.11 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | PRO-CON-5 | A: P=1.00 vs B: P=0.15 — Same-analysis P values differ by test: Fig 2 overall row 'P=1.00' is the heterogeneity test; text/abstract P=0.15 is the | KNOWN | Fig 2 p.10 / Abstract p.1 / text p.3 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | PRO-CON-6 | A: Peto OR 1.72 (1.09-2.71) vs B: RD 0.27% (−0.10 to 0.63) — Companion divergence: Singh et al 2011 (CMAJ) reports Peto OR 1.72 (1.09-2.71) significant on overlapping trials; this p | KNOWN | Singh 2011 (external) / this paper p.1/3 |  | contradiction [EXTERNAL_CRITIQUE] — confirm both sides as printed |
| ☐ |  | PRO-CON-8 | A: funnel plot referenced vs B: (no figure present) — Text states 'no indication of publication bias in the funnel plot' and Methods cite Stata funnel routine, but no funnel  | KNOWN | text p.3 / whole PDF |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ | A2 | All trials combined | effect=1.40, ci_lower=0.82, ci_upper=2.39 | KNOWN | 9 | Table 2 | pooled row (OVERALL_TOTAL) — confirm not mistakable for a study row |
| ☐ | A3 | Nakamura et al | effect=1.00, ci_lower=0.04, ci_upper=24.62, events_treatment=1/465, events_control=0/154 | KNOWN | 9 | Table 2 | random control (text table + raster forest plot) |
| ☐ | A4 | Nakamura et al | effect=3.79, ci_lower=0.04, ci_upper=352.44, events_treatment=1/465, events_control=0/154 | KNOWN | 9 | Table 2 | random control (text table + raster forest plot) |
## macnamara-2014-practice  _(dual-layer text)_

| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |
|---|---|---|---|---|---|---|---|
| ☐ |  | MAC-CON-3 | A: overall r̄=.35 [.30,.39] vs B: overall r̄=.38 [.33,.42] — Corrigendum documents misapplied Cheung & Chan N-adjustment: used (N-1)/(C+1) per individual effect instead of ((N-1)/C) | KNOWN | 2014 article p.1612 / corrigendum Table 1 |  | contradiction [ERRATUM] — confirm both sides as printed |
| ☐ |  | MAC-CON-1 | A: r̄=.35, I2=84.90 vs B: r̄=.38, I2=88.54 — Composite PDF pages 8 and 11 carry DUAL text layers: original 2014 values and 2018 corrected values on the same physical | KNOWN | PDF p.8 original layer / PDF p.8 corrected overlay |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | MAC-CON-2 | A: games 26% vs B: games 24% — Abstract, General Discussion, and Figure 3 retain uncorrected domain percentages (26/21/18/4/<1%) while corrected Result | KNOWN | abstract PDF p.4 / Fig.3 PDF p.11 / corrigendum Table 1 p.1 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ | MAC-DOM-2018 | Domain moderator omnibus | pooled=Q(4) = 36.61 | CORRECTED-VERSION | 1 | corrigendum Table 1 | erratum/corrigendum-affected value — verify both versions preserved |
| ☐ | MAC-OV-2018 | Overall practice-performance | pooled=.38 | CORRECTED-VERSION | 1 | corrigendum Table 1 | erratum/corrigendum-affected value — verify both versions preserved |
| ☐ | MAC-GAMES-2018 | Games | pooled=.49 | CORRECTED-VERSION | 1 | corrigendum Table 1 | erratum/corrigendum-affected value — verify both versions preserved |
| ☐ | MAC-MUSIC-2018 | Music | pooled=.48 | CORRECTED-VERSION | 1 | corrigendum Table 1 | erratum/corrigendum-affected value — verify both versions preserved |
| ☐ | MAC-SPORTS-2018 | Sports | pooled=.45 | CORRECTED-VERSION | 1 | corrigendum Table 1 | erratum/corrigendum-affected value — verify both versions preserved |
## hahn-2024-exercise-intake  _(vector no-text forest plot)_

| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |
|---|---|---|---|---|---|---|---|
| ☐ | A3tot | (unlabeled diamond) | effect=UNRESOLVED, ci_lower=UNRESOLVED, ci_upper=UNRESOLVED | UNRESOLVED | 23 | Fig 4 | UNRESOLVED row — human adjudication required |
| ☐ | A3tot | Total energy intake (kcal) | pooled= | UNRESOLVED | 23 | Fig 4 | UNRESOLVED analysis |
| ☐ |  | HAH-CON-07 | A: n=26 vs B: n=25 — Ajibewa 2017 NW sample size: Table 1 reports n=26 but every forest plot prints intervention n=25 per NW arm (control spl | AMBIGUOUS | Table 1, p.5 / Figs 2-7, pp.22-26 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | HAH-CON-01 | A: rugby: 142.95 / [-520.18, 40.18]; 75%: 99.03 / [-589.10, -200.90] vs B: rugby: 121.68 / [-478.49, -1.51]; 75%: 142.95 / [-675.18, -114.82] — Thivel 2015 SE/CI swap in Fig 4: rugby arm printed with SE 142.95 / CI [-520.18, 40.18] and 75% arm with SE 99.03 / CI [ | KNOWN | Fig 4, PDF p.23 / Figs 2/3 p.22, Fig 5 p.24, Fig 6 p.25, Fig 7 p.26 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | HAH-CON-02 | A: 22.71 [-78.48, 123.90], I2=82% vs B: 27.25 [-69.66, 124.15], I2=80% — Fig 4 high-intensity subtotal differs from Fig 6 Total although both pool the identical 14 arms (downstream consequence  | KNOWN | Fig 4 subtotal, p.23 / Fig 6 Total, p.25 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | HAH-CON-03 | A: unlabeled diamond, no numbers printed vs B: labeled Total rows with values — Fig 4 draws an overall diamond but prints no 'Total (95% CI)' row; all other subgroup figures (5, 6, 7) print a labeled  | KNOWN | Fig 4, p.23 / Figs 5/6/7, pp.24-26 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | HAH-CON-04 | A: SE 98.8, CI [-276.64, 110.64] vs B: SE 98.81, CI [-276.66, 110.66] — Rounding variant for Varley Campbell 2017 NW + Snack between figures | KNOWN | Fig 5, p.24 / Figs 2/3/4/7, pp.22-26 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | HAH-CON-05 | A: SE 115.24, CI [254.13, 705.87] vs B: SE 115.25, CI [254.11, 705.89] — Rounding variant for Thivel 2013 OB 30min 75% between figures | KNOWN | Fig 6, p.25 / Figs 2/3/4/5/7, pp.22-26 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ | A5a | Subtotal (95% CI) | effect=-27.82, ci_lower=-83.19, ci_upper=27.54, weight=39.9 | KNOWN | 25 | Fig 6 | pooled row (SUBGROUP_TOTAL) — confirm not mistakable for a study row |
| ☐ | A1 | Fillon Mathieu 2020 OB 30min cycling, meal 1h p.ex | effect=184.00, ci_lower=-145.80, ci_upper=513.80, se=168.27, weight=1.6 | KNOWN | 22 | Fig 2 | random control (vector no-text forest plot) |
| ☐ | A1 | Bozinosvki 2009 NW 15min Treadmill | effect=18.00, ci_lower=-269.76, ci_upper=305.76, se=146.82, weight=1.9 | KNOWN | 22 | Fig 2 | random control (vector no-text forest plot) |
## driessen-2015-nih-psychotherapy  _(raster forest plot)_

| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |
|---|---|---|---|---|---|---|---|
| ☐ | A1-UNPUB | [unpublished study — name and values suppressed] | (no numeric cells) | UNRESOLVED | 13 | Fig 2 | UNRESOLVED row — human adjudication required |
| ☐ | A1-UNPUB | [unpublished study — name and values suppressed] | (no numeric cells) | UNRESOLVED | 13 | Fig 2 | UNRESOLVED row — human adjudication required |
| ☐ | A1a-UNPUB | [unpublished study — name and values suppressed] | (no numeric cells) | UNRESOLVED | 13 | Fig 3 | UNRESOLVED row — human adjudication required |
| ☐ | A1b-UNPUB | [unpublished study — name and values suppressed] | (no numeric cells) | UNRESOLVED | 14 | Fig 4 | UNRESOLVED row — human adjudication required |
| ☐ | A3-UNPUB | [unpublished study — name and values suppressed] | (no numeric cells) | UNRESOLVED | 15 | Fig 6 | UNRESOLVED row — human adjudication required |
| ☐ | A4-UNPUB | [unpublished study — name and values suppressed] | (no numeric cells) | UNRESOLVED | 15 | Fig 7 | UNRESOLVED row — human adjudication required |
| ☐ | SENS-RANK | Depressive symptom severity | pooled= | UNRESOLVED | 14 | S1 Table (not in PDF) | UNRESOLVED analysis |
| ☐ | SENS-39-UNPUB | Depressive symptom severity | pooled= | UNRESOLVED | 14-15 | S1 Table (not in PDF) | UNRESOLVED analysis |
| ☐ | SENS-GOTTLIEB-A3 | Depressive symptom severity | pooled= | UNRESOLVED | 15 | S1 Table (not in PDF) | UNRESOLVED analysis |
| ☐ | SENS-GOTTLIEB-A4 | Depressive symptom severity | pooled= | UNRESOLVED | 16 | S1 Table (not in PDF) | UNRESOLVED analysis |
| ☐ |  | DRI-CON-06 | A: 13 - 3 = 10 rated vs B: percentages imply 9 rated (and 53 total) — Unpublished quality-rating denominator inconsistency: text says quality ratings could not be retrieved for three unpubli | AMBIGUOUS | text p16 / text p16 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | DRI-CON-19 | A: Fig 5 'Wright, 2014' row = ref [39] (pass A inference from name/year match) vs B: placement not explicitly stated (pass B position) — Study [39] (Frank R21MH061948) is counted as published although it 'reported the grant-funded trial's outcomes only in a | AMBIGUOUS | Fig 5, p14; Table 1 row 10 / text p11 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | DRI-CON-22 | A: k=5 published pill-placebo studies vs B: 3 explicitly labelled CTRL-NS(PLAC) rows — Composition of the k=5 published pill-placebo pool (text p14) is not identifiable from the figures: only 3 published Fig | AMBIGUOUS | text p14 / Figs 2/4, pp13-14 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | DRI-CON-01 | A: PUBLISHED (continuation header) vs B: rows 46-57 are unpublished grants — Table 1 continuation header on page 11 prints 'PUBLISHED' although every study row on that page (46 Clark through 57 Zlo | KNOWN | Table 1, p11 / Table 1, pp10-11 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | DRI-CON-02 | A: -456% vs B: delta-g = -0.07 from a published-only baseline of g = 0.01 — Table 2 percentage-change cell for PT vs. antidepressant medication prints '-456%' | KNOWN | Table 2, p12 / Table 2, p12 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | DRI-CON-03 | A: R01MH37869 vs B: 6-digit serials elsewhere — Reynolds grant number printed 'R01MH37869' with a 5-digit serial; every other MH grant in Table 1 has 6 digits (e.g. R01 | KNOWN | Table 1 row 31, p10 / Table 1, pp9-11 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ | A2-UNPUB | Unpublished (Overall) | effect=-0.05, ci_lower=-0.49, ci_upper=0.38, se=0.22 | SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE | 14 | Fig 5 | author-supplied data — verify flagged as non-verifiable, not error |
| ☐ | A1-UNPUB | Unpublished (Overall) | effect=0.20, ci_lower=-0.11, ci_upper=0.51, se=0.16 | SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE | 13 | Fig 2 | author-supplied data — verify flagged as non-verifiable, not error |
| ☐ | A4-UNPUB | [unnamed unpublished] | effect=0.56, ci_lower=0.10, ci_upper=1.02, se=0.24, weight=78.94 | SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE | 15 | Fig 7 | author-supplied data — verify flagged as non-verifiable, not error |
| ☐ | A1a-ALL | Overall | effect=0.97, ci_lower=0.62, ci_upper=1.32, se=0.18 | KNOWN | 13 | Fig 3 | pooled row (OVERALL_TOTAL) — confirm not mistakable for a study row |
| ☐ | A3-PUB | Murphy, 1995 | effect=1.31, ci_lower=0.40, ci_upper=2.22, se=0.47, weight=2.13 | KNOWN | 15 | Fig 6 | random control (raster forest plot) |
| ☐ | A4-PUB | Hersen, 1984 | effect=-0.20, ci_lower=-0.86, ci_upper=0.47, se=0.34, weight=8.65 | KNOWN | 15 | Fig 7 | random control (raster forest plot) |
## cooney-2013-exercise-depression  _(text-encoded RevMan forest table)_

| ✓ | Analysis | Study/row | Truth value(s) | Status | Page | Where | Why selected |
|---|---|---|---|---|---|---|---|
| ☐ |  | COO-CON-7 | A: e.g. Klein 1985 N=14/8 vs B: e.g. Klein 1985 15/27 vs 16/24 — Multi-arm arm selection: the same study label carries different Ns across analyses. A1.1 uses analysed-participant Ns of | AMBIGUOUS | Analysis 1.1 forest PDF p105 / Analysis 1.3 forest PDF p107 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | COO-CON-9 | A: 10.6 (0.8) / 11 (0.8) vs B: 8.7 (6.9) / 7.8 (6.5) post-treatment — Blumenthal 1999 follow-up cells (Analysis 1.2) print Mean(SD) '10.6 (0.8)' / '11 (0.8)' — SDs an order of magnitude smal | AMBIGUOUS | Analysis 1.2 forest PDF p106 / Analysis 1.1 forest PDF p105 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | COO-CON-1 | A: 1356 vs B: 1353 — Participant count for primary Analysis 1.1: Abstract and Effects text say '35 trials (1356 participants)' while Comparis | KNOWN | Abstract PDF p5; Effects text PDF p27 / Comparison 1 table PDF p104; SOF PDF p7; Analysis 1.1 forest totals PDF p106 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | COO-CON-2 | A: moderate heterogeneity (I2 = 63%) vs B: substantial heterogeneity (I2 = 63%) — Heterogeneity qualifier for the same I2=63% in Analysis 1.1: Abstract calls it 'moderate heterogeneity', Effects text ca | KNOWN | Abstract PDF p5 / Effects text PDF p27 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | COO-CON-3 | A: 62.78% vs B: 63% — I2 precision for Analysis 1.1: forest plot prints I2=62.78% while Abstract and Effects text print 63% | KNOWN | Analysis 1.1 forest heterogeneity line PDF p106 / Abstract PDF p5; Effects text PDF p27 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ |  | COO-CON-4 | A: 298 vs B: 300 — Analysis 4.1 (exercise vs pharmacological) participant count: Effects text says 'four trials (298 participants)' while A | KNOWN | Effects text PDF p28 / Abstract PDF p5; Comparison 4 table PDF p110; Analysis 4.1 forest totals PDF p110 |  | contradiction [INTERNAL] — confirm both sides as printed |
| ☐ | A1.1 | Total | effect=-0.62, ci_lower=-0.81, ci_upper=-0.42, weight=100 | KNOWN | 106 | Analysis 1.1 | pooled row (OVERALL_TOTAL) — confirm not mistakable for a study row |
| ☐ | A1.3 | Martinsen 1985 | effect=0.93, ci_lower=0.74, ci_upper=1.18, weight=1.65, events_treatment=20 | KNOWN | 107 | Analysis 1.3 | random control (text-encoded RevMan forest table) |
| ☐ | A1.1 | Bonnet 2005 | effect=1.51, ci_lower=0.09, ci_upper=2.93, weight=1.37 | KNOWN | 105 | Analysis 1.1 | random control (text-encoded RevMan forest table) |

---
## Freeze protocol

All truth files are currently **PRE-FREEZE** (AI double-pass reconciled,
human-unverified). After completing this package: record
`Researcher spot-check: PASSED/CORRECTED <date>` in each paper's
truth/notes.md, then tag the repository `gold-truth-v1` → GOLD_TRUTH_V1.
Post-freeze corrections must be versioned revisions, never silent edits.
Benchmarks run before sign-off are labeled BENCHMARK_AGAINST_PREFREEZE_TRUTH.
