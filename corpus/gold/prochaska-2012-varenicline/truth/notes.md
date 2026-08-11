# Truth provenance — prochaska-2012-varenicline

Status: DRAFT — pass A transcribed; pass B reconciliation pending
(researcher sign-off pending)

## Construction
- Pass A: independent full read (text layer + figure images), 2026-08-11.
  137 effect rows across five representations of the same 22 trials:
  Fig 2 RD forest plot (proportions), Table 2 RD (%), RR, M-H OR, Peto OR
  columns, Fig 3 cumulative meta-analysis. UC ("unable to calculate") rows
  recorded faithfully for the 8 double-zero trials in relative-measure
  columns.
- Pass B: independent duplicate pass, blind; diff against these CSVs logged
  below when complete.

## Notable properties (pass A)
- Cross-representation redundancy (same trial in ≥4 places) makes this the
  strongest internal-consistency fixture in the corpus; pass A's cross-checks
  (arm sums 34/5431, 18/3801; 8+14=22; flow arithmetic) all reconciled.
- Four genuine internal print discrepancies found (PRO-CON-1..4), including
  the Steinberg Table-2 CI misprint and figure-vs-figure rounding/weight
  differences — natural true positives for §41 contradiction detection.
- PRO-CON-5 records a *non*-contradiction (heterogeneity P vs effect P) that
  a naive checker would false-positive on — deliberate false-finding guard.
- Unit trap: Table 2 reports RD in percent, Fig 2 in proportions (0.27 vs
  0.0027) — same analysis, different scales.

## Reconciliation (pass A vs pass B), 2026-08-11
- ZERO numeric disagreements across all 137 effect rows and 10 analyses.
  Pass B glyph-verified the two suspect table cells (Steinberg RD CI,
  Fagerström OR lower bound) directly in the PDF content stream — both are
  genuinely printed as recorded (AMBIGUOUS retained on interpretive intent).
- Pass B additions adopted: PRO-CON-7 (Hong ±9.00 vs ±9.02), PRO-CON-8
  (funnel plot referenced but absent); per-label Table-1 page split (p.7 vs
  p.8) corrected in study_labels.csv.
- Both passes independently confirmed the count cross-checks (22 trials
  everywhere; arm sums 34/5431 and 18/3801; 8 double-zero + 14 = 22).
- Figures are raster images (captions are text; plot contents are not) —
  confirmed by both passes reading figures from rendered images.

TRUTH_STATUS: PRE_FREEZE — AI double-pass reconciled, human-unverified.
Benchmarks against this state are BENCHMARK_AGAINST_PREFREEZE_TRUTH.
Researcher corrections become versioned revisions; freeze tag: gold-truth-v1.
