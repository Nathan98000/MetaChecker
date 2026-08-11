# Truth notes — hahn-2024-exercise-intake

Hahn H, Friedel M, Niessner C, Zipfel S, Mack I. Int J Behav Nutr Phys Act (2024) 21:76.
DOI 10.1186/s12966-024-01620-8. PROSPERO CRD42022324259. 28-page PDF, printed folios match PDF pages 1:1.

## Reconciliation (pass A vs pass B), 2026-08-11

### Construction method

Truth v0 was built from two blind, independent extraction passes over the same source PDF
(`pass-a-raw.md`, `pass-b-raw.md`, both 2026-08-11), reconciled value-by-value into
`analyses.csv`, `study_labels.csv`, `published_effects.csv`, `contradictions.csv`.
Body text, Table 1, and all figure captions are machine-readable text; **Figs 1–9 and the
Table 2 grid have NO extractable text layer** — every forest-plot number in the truth files
was read from rendered page images at high zoom (pass A: 3–9x with targeted re-zooms;
pass B: 6–10x with zoomed crop verification), independently by each pass.

### Numeric disagreements between passes

**ZERO.** Every effect, CI bound, SE, weight, sample size, pooled estimate, heterogeneity
statistic (Tau², Chi², df, I², P, Z), and source page was compared value-by-value across the
two passes; all agree exactly. This includes the three figure-internal oddities, which both
passes read identically and independently:

- Fig 4 Thivel 2015 swapped values (rugby 142.95 / [-520.18, 40.18]; 75% 99.03 / [-589.10, -200.90]);
- Fig 5 Varley Campbell + Snack variant (98.8 / [-276.64, 110.64]);
- Fig 6 Thivel 2013 variant (115.24 / [254.13, 705.87]).

### Non-numeric disagreements (all adjudicated)

1. **Ajibewa 2017 NW 25% stretching, label page list**: pass A gave 22,24,26 (omitting p23),
   contradicting pass A's own Fig 4 extraction, which contains the row (F4.01). Adopted pass B:
   22;23;24;26.
2. **Fearnbach 2016 OB 45min cycling, label page list**: pass B included p25, but Fig 6 is the
   high-intensity figure and neither pass's Fig 6 extraction contains a Fearnbach 2016 row
   (the arm is low/moderate intensity). Adopted pass A: 22;23;24;26.
3. **Figure encoding mechanism**: pass A says the figures are vector Form XObjects with no
   raster images; pass B says they are embedded raster images. Both agree there is no text
   layer, which is what matters for provenance; the mechanism is left unresolved (immaterial
   to values).
4. **Fig 4 overall diamond position**: "drawn below subtotals" (A) vs "drawn above the axis"
   (B) — same object, phrasing only; both agree no Total values are printed.
5. **Fig 6 subgroup header dash**: pass A wrote "High Intensity Exercise - Normalweight"
   (hyphen), pass B used an en dash in its analyses section. Hyphen adopted; exact printed
   glyph not re-verified.

### Extra findings adopted at reconciliation

- **From pass A only**: country-percentage arithmetic errors (HAH-CON-09); 13/43 vs 14
  pooled high-intensity arms (HAH-CON-13); Table 2 "DS" column undefined + overall RoB
  memberships (HAH-CON-14); Fig 3 caption "low or moderate" wording (HAH-CON-16); Fig 1
  "Records identified from*" typo (folded into HAH-CON-11); explicit direction-convention
  verification (below).
- **From pass B only**: Saunders 2013 label vs 2014 reference (HAH-CON-12); Thivel 2012
  Table 1 fat%/protein% copy error, likely target of the publisher correction (HAH-CON-10);
  Thivel 2013 "30min" label vs 3 x 10 min bouts (HAH-CON-15); AMBIGUOUS framing of the
  Ajibewa 26-vs-25 discrepancy (HAH-CON-07); the 478-vs-578 control-total explanation used
  for guard row HAH-CON-08.

### Direction convention

Plotted MD = **Control − Exercise** (positive = "HIgher EI in CON" [sic]); pass A verified
arithmetically against Table 1 means (Thivel 2013: CON 1787 − EX 1307 = 480; Fearnbach 2016:
1116 − 1037 = 79). The abstract's "MD = 23.31 [-27.54, 74.15] kcal" is easily misread as EX−CON.

### Shared-control splitting (documented identically by both passes)

Methods, p.3, verbatim: "In studies with multiple intervention arms the sample size of the
shared group was split according to the Cochrane Handbook [51] and Rücker et al. [55] to
avoid 'double-counting' of participants (unit-of-analysis error). For the meta-analysis,
41 study arms were eligible." Every forest-plot caption (pp.22–26) repeats: "In multi-arm
trials, the sample size of the shared control group was divided to prevent double counting."
Crossover MD/SE per the Cochrane Handbook; correlation coefficient 0.5 imputed where paired
data were insufficient (sensitivity 0.3/0.7 in Supporting Information S2, not in this PDF).

Split-arithmetic examples (Table 1 n → per-arm forest-plot control n), verified by both passes:

- Ajibewa NW n=26, 3 arms → 8/8/8 in Fig 2 (exercise printed 25, not 26 — HAH-CON-07);
  Fig 4: 2 arms share the low/mod subgroup → 12/12, lone high-intensity arm unsplit at 25.
- Ajibewa OB 13 → 4/4/4 (Fig 2); 6/6 + 13 (Fig 4).
- Nemet 22 per weight group, 3 arms → 7/7/7 (Fig 2); 11/11 + 22 (Fig 4); 22 (Fig 6, one arm).
- Bozinovski 29 → 14/14. Thivel 2012 15 → 7/7 (Fig 2) but 15/15 in Fig 4 (arms fall in
  different subgroups; SEs recomputed to 163.63/179.19). Thivel 2015 14 → 7/7.
  Fillon 2020 18 → 9/9; Fillon Mathieu 15 → 7/7; Masurier 20 → 10/10; Saunders 20 → 10/10.
- Splits round down (26→24, 13→12, 29→28, 15→14), so the Fig 2 control sum (478) undercounts
  enrolled controls; SEs are correspondingly recomputed per analysis (see Fig 4 variant rows
  in published_effects.csv). This is why control totals legitimately differ across figures
  (478 vs 578 vs 219) — guard row HAH-CON-08, not an error.

### Sanity checks (passed before finalizing)

- Fig 2 weights sum to 100.0; control n sums to 478 and exercise n to 780, matching the
  Abstract/Results text ("exercise n = 780 and control n = 478").
- Row counts per figure: Fig 2 = 41 study rows; Fig 3 = 27; Fig 4 = 27 + 14; Fig 5 = 16 + 25;
  Fig 6 = 5 + 9; Fig 7 = 22 + 19.
- Fig 3 weights (which differ from Fig 2) are recorded in published_effects F3-ROWS;
  Fig 5 and Fig 7 study-row weights are identical to Fig 2.

### File contents

- `analyses.csv` — 14 rows (A1, A2, A3a/A3b/A3tot, A4a/A4b/A4tot, A5a/A5b/A5tot,
  A6a/A6b/A6tot). A3tot (Fig 4 overall total) is UNRESOLVED: diamond drawn, no values printed.
- `study_labels.csv` — 85 rows: 41 verbatim forest-plot arm labels (misspellings preserved),
  22 Table 1 forms, 22 Table 2 forms.
- `published_effects.csv` — 92 rows: full Fig 2 (41 + total + heterogeneity); Fig 3 summary +
  total; Fig 4's 16 variant rows + summary of the 25 Fig-2-identical rows + 2 subtotals +
  UNRESOLVED total + subgroup test; Fig 5 summary + Varley Campbell + Snack variant +
  2 subtotals + total; Fig 6 in full (14 rows carry a mix of Fig 2 and Fig 4-style values,
  so no summary shorthand is safe) + 2 subtotals + total; Fig 7 summary + 2 subtotals + total.
  SEs recorded in the `se` column (these plots print SE — unusual and valuable);
  n_exercise → n_treatment. All version=AS_PUBLISHED, source_type=FOREST_PLOT.
- `contradictions.csv` — 16 rows (HAH-CON-01…16), union of both passes' findings.
  HAH-CON-07 is AMBIGUOUS; HAH-CON-08 is an explained/not-an-error guard row.

### Publisher correction

The only trace in the PDF is the p.1 copyright line "© The Author(s) 2024, corrected
publication 2024". No erratum text or corrected-Table-1 reference appears anywhere in the
file (both passes). The Thivel 2012 fat%/protein% duplication (HAH-CON-10) is the likely
target. When the correction document is obtained, affected values get AS_CORRECTED rows with
`supersedes` set, per corpus conventions.

### Status

**DRAFT** — pending researcher spot-check and sign-off.
