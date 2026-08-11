# Truth Set v1 — Researcher Spot-Check Package

Seed: 20260811 (regenerate identically with `make_spotcheck.py --seed 20260811`)

For each item: open the source PDF at the stated page/figure and confirm
the truth value matches the printed source exactly (verbatim, at printed
precision). Mark ✓ / ✗ / note. Contradiction items: confirm both sides
are printed as recorded — you are confirming the *documentation*, not
resolving the contradiction.

## yang-2018-sii

_41 effect rows, 19 analyses, 10 documented contradictions → 19 value checks + 10 contradiction confirmations._

| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |
|---|---|---|---|---|---|---|
| ☐ | E41 | (no Overall row printed):  | 6 | Figure 5 | (no Overall row printed) | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | E02 | Loll (2016): effect=1.84, ci_lower=1.35, ci_upper=2.50, weight_pct=5.60 | 4 | Figure 2 | Loll (2016) | interpretation noted: values KNOWN; which of Loll[15]/Loll[16] AMBIGUOUS |
| ☐ | E13 | Loll (2016): effect=1.80, ci_lower=1.23, ci_upper=2.62, weight_pct=5.14 | 4 | Figure 2 | Loll (2016) | interpretation noted: second Loll row; attribution AMBIGUOUS |
| ☐ | E17 | Hu (2014): effect=2.56, ci_lower=1.17, ci_upper=5.76, weight_pct=2.81 | 4 | Figure 2 | Hu (2014) | interpretation noted: one of two Hu cohorts; attribution AMBIGUOUS |
| ☐ | E18 | Hu (2014): effect=2.10, ci_lower=1.14, ci_upper=3.85, weight_pct=3.72 | 4 | Figure 2 | Hu (2014) | interpretation noted: second Hu cohort; attribution AMBIGUOUS |
| ☐ | E20 | Geng (2016): effect=1.30, ci_lower=1.05, ci_upper=1.62, weight_pct=6.14 | 4 | Figure 2 | Geng (2016) | interpretation noted: one of two Geng cohorts; attribution AMBIGUOUS |
| ☐ | E21 | Geng (2016): effect=1.24, ci_lower=1.01, ci_upper=1.53, weight_pct=6.18 | 4 | Figure 2 | Geng (2016) | interpretation noted: second Geng cohort; attribution AMBIGUOUS |
| ☐ | E24 | Hu (2014): effect=2.32, ci_lower=1.28, ci_upper=4.23, weight_pct=21.64 | 6 | Figure 5 | Hu (2014) | interpretation noted: cohort attribution AMBIGUOUS |
| ☐ | E25 | Hu (2014): effect=1.92, ci_lower=1.04, ci_upper=3.54, weight_pct=20.61 | 6 | Figure 5 | Hu (2014) | interpretation noted: cohort attribution AMBIGUOUS |
| ☐ | E31 | Lolli (2016): effect=1.71, ci_lower=1.71, ci_upper=2.21, weight_pct=24.25 | 6 | Figure 5 | Lolli (2016) | interpretation noted: printed lower CI equals point estimate; plotted whisker extends below marker — l |
| ☐ | E11 | Ha (2016): effect=0.93, ci_lower=0.59, ci_upper=1.45, weight_pct=4.68 | 4 | Figure 2 | Ha (2016) | random sample (FOREST_PLOT) |
| ☐ | E21 | Geng (2016): effect=1.24, ci_lower=1.01, ci_upper=1.53, weight_pct=6.18 | 4 | Figure 2 | Geng (2016) | random sample (FOREST_PLOT) |
| ☐ | E15 | Gardini (2016): effect=2.99, ci_lower=1.34, ci_upper=6.68, weight_pct=2.79 | 4 | Figure 2 | Gardini (2016) | random sample (FOREST_PLOT) |
| ☐ | E03 | Passardi (2016): effect=0.84, ci_lower=0.53, ci_upper=1.31, weight_pct=4.66 | 4 | Figure 2 | Passardi (2016) | random sample (FOREST_PLOT) |
| ☐ | E24 | Hu (2014): effect=2.32, ci_lower=1.28, ci_upper=4.23, weight_pct=21.64 | 6 | Figure 5 | Hu (2014) | random sample (FOREST_PLOT) |
| ☐ | E01 | Hong (2015): effect=1.38, ci_lower=1.02, ci_upper=1.85, weight_pct=5.67 | 4 | Figure 2 | Hong (2015) | random sample (FOREST_PLOT) |
| ☐ | E32 | Yang (2017): effect=1.55, ci_lower=0.98, ci_upper=2.46, weight_pct=18.09 | 6 | Figure 5 | Yang (2017) | random sample (FOREST_PLOT) |
| ☐ | E05 | wang (2017): effect=1.55, ci_lower=1.21, ci_upper=1.99, weight_pct=5.96 | 4 | Figure 2 | wang (2017) | random sample (FOREST_PLOT) |
| ☐ | E40 | Subtotal (RFS): effect=1.66, ci_lower=1.07, ci_upper=2.59, weight_pct=25.87 | 6 | Figure 5 | Subtotal (RFS) | random pooled-row check (row_kind guard) |

**Contradictions to confirm (both sides as printed):**

- ☐ **YAN-CON-1** [INTERNAL] HCC subgroup upper CI: Table 2 prints 1.59-2.38; Abstract and Results text print 1.59-2.80 — A: `2.38` (Table 2, PDF p.4) vs B: `2.80` (Abstract p.1 / Results p.3)
- ☐ **YAN-CON-2** [INTERNAL] Every OS partition's subgroup HRs fall below the overall pooled HR 1.69 (Asian 1.26/Caucasian 1.55; <=255 1.14/>255 1.31; <=560 1.21/>560 1.32) — arithmetically impossible for a pa — A: `1.69 (1.42-2.01) overall` (Figure 2 p.4) vs B: `e.g. Asian 1.26 (1.12-1.40) + Caucasian 1.55 (0.84-2.27)` (Table 2 p.4)
- ☐ **YAN-CON-3** [INTERNAL] p-values inconsistent with CIs in Table 2: Caucasian CI 0.84-2.27 crosses 1 with P=0.009; Sample<=255 CI 0.89-1.39 with P<0.001; Cutoff<=560 CI 1.00-1.43 with P<0.001 — A: `P=0.009 / P<0.001` (Table 2 p.4) vs B: `CIs crossing/touching 1` (Table 2 p.4)
- ☐ **YAN-CON-4** [INTERNAL] Figure 5 bottom panel (DFS/CSS/RFS) lacks an Overall row and x-axis labels; subtotal weights sum to 100.01 implying an unprinted combined pool across three different outcomes — A: `subtotals 25.38+48.76+25.87` (Figure 5 p.6) vs B: `(no overall row)` (Figure 5 p.6)
- ☐ **YAN-CON-5** [INTERNAL] Abstract/Discussion claim separate significance for SCLC, NSCLC, Acral Melanoma (each p<0.001) but Table 2 pools them as one 'Other' subgroup with a single p — separate estimates n — A: `three p<0.001 claims` (Abstract p.1) vs B: `Other: 1.77 (1.30-2.41), one p<0.001` (Table 2 p.4)
- ☐ **YAN-CON-6** [INTERNAL] 'P for subgroup difference' <0.001 for every Table 2 block while meta-regression on same data reports no significant moderators (pEthnicity=0.777, pcutoff=0.139, etc.) — A: `<0.001 (all blocks)` (Table 2 p.4) vs B: `meta-regression ps 0.139-0.777` (Results text p.3)
- ☐ **YAN-CON-7** [INTERNAL] Study-label inconsistencies: 'Loll' (Table 1, Figure 2) vs 'Lolli' (Figure 5, references); lowercase 'wang (2017)' vs capital 'Wang (2017)' as sole discriminator; duplicate unlabel — A: `Loll (2016)` (Figure 2 p.4) vs B: `Lolli (2016)` (Figure 5 p.6)
- ☐ **YAN-CON-8** [INTERNAL] Lolli (2016) PFS row printed '1.71 (1.71, 2.21)' — lower CI equals point estimate; plotted whisker extends below marker (likely figure typo) — A: `1.71 (1.71, 2.21)` (Figure 5 p.6) vs B: `whisker extends below marker` (Figure 5 p.6 (visual))
- ☐ **YAN-CON-9** [INTERNAL] Conroy (2017) OS CI severely asymmetric: 1.63 (1.15, 4.19) — A: `1.63 (1.15, 4.19)` (Figure 2 p.4) vs B: `` ()
- ☐ **YAN-CON-10** [EXTERNAL_CRITIQUE] Possible citation misalignment: Table 1 Liu[11] cites a C-reactive-protein/albumin-ratio paper, Gao[10] cites a myeloid-derived-suppressor-cell paper — neither obviously an SII pro — A: `Liu[11] / Gao[10]` (Table 1 p.3) vs B: `reference titles` (References p.8)

## prochaska-2012-varenicline

_137 effect rows, 10 analyses, 8 documented contradictions → 15 value checks + 8 contradiction confirmations._

| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |
|---|---|---|---|---|---|---|
| ☐ | T2RD-10 | Steinberg et al: effect=−0.06, ci_lower=−0.07, ci_upper=6.87, events_treatment=1/40, events_control=1/39, n_treatment=40 | 9 | Table 2 | Steinberg et al | certainty=AMBIGUOUS — must be human-adjudicated |
| ☐ | T2OR-01 | Fagerstrom et al: effect=0.34, ci_lower=0.14, ci_upper=8.34, events_treatment=0/214, events_control=1/218, n_treatment=214 | 9 | Table 2 | Fagerstrom et al | certainty=AMBIGUOUS — must be human-adjudicated |
| ☐ | F3-01 | Nides 2006: effect=0.0026, ci_lower=-0.0099, ci_upper=0.0152, weight_pct=4.53, events_treatment=1/383, events_control=0/127 | 11 | Fig 3 | Nides 2006 | random sample (FOREST_PLOT) |
| ☐ | F2-20 | Tonstad 2006: effect=0.0033, ci_lower=-0.0023, ci_upper=0.0089, weight_pct=14.35, events_treatment=2/603, events_control=0/607 | 10 | Fig 2 | Tonstad 2006 | random sample (FOREST_PLOT) |
| ☐ | F3-04 | Tonstad 2006: effect=0.0024, ci_lower=-0.0017, ci_upper=0.0066, weight_pct=14.35, events_treatment=2/603, events_control=0/607 | 11 | Fig 3 | Tonstad 2006 | random sample (FOREST_PLOT) |
| ☐ | F2-18 | Tsai 2007: effect=0.0079, ci_lower=-0.0139, ci_upper=0.0297, weight_pct=2.97, events_treatment=1/126, events_control=0/124 | 10 | Fig 2 | Tsai 2007 | random sample (FOREST_PLOT) |
| ☐ | F2-02 | Rennard 2012: effect=0.0000, ci_lower=-0.0087, ci_upper=0.0087, weight_pct=5.89, events_treatment=0/493, events_control=0/166 | 10 | Fig 2 | Rennard 2012 | random sample (FOREST_PLOT) |
| ☐ | F3-18 | Ebbert 2011: effect=0.0029, ci_lower=-0.0010, ci_upper=0.0068, weight_pct=0.90, events_treatment=0/38, events_control=0/38 | 11 | Fig 3 | Ebbert 2011 | random sample (FOREST_PLOT) |
| ☐ | T2OR-19 | Niaura et al: effect=5.06, ci_lower=0.24, ci_upper=106.30, events_treatment=2/160, events_control=0/160, n_treatment=160 | 9 | Table 2 | Niaura et al | random sample (TABLE) |
| ☐ | T2PO-19 | Niaura et al: effect=7.44, ci_lower=0.46, ci_upper=119.40, events_treatment=2/160, events_control=0/160, n_treatment=160 | 9 | Table 2 | Niaura et al | random sample (TABLE) |
| ☐ | T2OR-14 | Oncken et al: effect=1.25, ci_lower=0.06, ci_upper=26.27, events_treatment=2/518, events_control=0/129, n_treatment=518 | 9 | Table 2 | Oncken et al | random sample (TABLE) |
| ☐ | T2RR-21 | Williams et al: effect=3.01, ci_lower=0.37, ci_upper=24.75, events_treatment=6/251, events_control=1/126, n_treatment=251 | 9 | Table 2 | Williams et al | random sample (TABLE) |
| ☐ | T2RD-18 | Tsai et al: effect=0.79, ci_lower=−1.39, ci_upper=2.97, events_treatment=1/126, events_control=0/124, n_treatment=126 | 9 | Table 2 | Tsai et al | random sample (TABLE) |
| ☐ | T2OR-22 | Tashkin et al: effect=2.05, ci_lower=0.37, ci_upper=11.29, events_treatment=4/250, events_control=2/254, n_treatment=250 | 9 | Table 2 | Tashkin et al | random sample (TABLE) |
| ☐ | T2PO-23 | All trials combined: effect=1.58, ci_lower=0.90, ci_upper=2.76 | 9 | Table 2 | All trials combined | random pooled-row check (row_kind guard) |

**Contradictions to confirm (both sides as printed):**

- ☐ **PRO-CON-1** [INTERNAL] Steinberg RD: Table 2 prints '−0.06 (−0.07 to 6.87)' but Fig 2 prints '-0.0006 (-0.0699 to 0.0687)' — table lower bound almost certainly misprint for −6.99 — A: `−0.06 (−0.07 to 6.87)` (Table 2 p.9) vs B: `-0.0006 (-0.0699 to 0.0687)` (Fig 2 p.10)
- ☐ **PRO-CON-2** [INTERNAL] Nides 2006 upper CI: Fig 2 prints 0.0151; Fig 3 first row (same single-trial estimate) prints 0.0152 — A: `0.0151` (Fig 2 p.10) vs B: `0.0152` (Fig 3 p.11)
- ☐ **PRO-CON-3** [INTERNAL] Jorenby 2006 weight: Fig 2 prints 8.13; Fig 3 prints 8.12 — A: `8.13` (Fig 2 p.10) vs B: `8.12` (Fig 3 p.11)
- ☐ **PRO-CON-4** [INTERNAL] Fagerstrom M-H OR CI printed '0.34 (0.14 to 8.34)': lower 0.14 inconsistent with RR lower 0.01 and Peto lower 0.00 on identical 2x2 data — A: `0.14` (Table 2 p.9 (OR col)) vs B: `0.01 / 0.00` (Table 2 p.9 (RR/Peto cols))
- ☐ **PRO-CON-5** [INTERNAL] Same-analysis P values differ by test: Fig 2 overall row 'P=1.00' is the heterogeneity test; text/abstract P=0.15 is the effect test — confusable but not contradictory — A: `P=1.00` (Fig 2 p.10) vs B: `P=0.15` (Abstract p.1 / text p.3)
- ☐ **PRO-CON-6** [EXTERNAL_CRITIQUE] Companion divergence: Singh et al 2011 (CMAJ) reports Peto OR 1.72 (1.09-2.71) significant on overlapping trials; this paper's primary RD 0.27% (−0.10 to 0.63) non-significant; §Di — A: `Peto OR 1.72 (1.09-2.71)` (Singh 2011 (external)) vs B: `RD 0.27% (−0.10 to 0.63)` (this paper p.1/3)
- ☐ **PRO-CON-7** [INTERNAL] Hong RD CI: Table 2 prints '0 (−9.00 to 9.00)'; Fig 2 prints '(-0.0902 to 0.0902)' = ±9.02% — A: `±9.00` (Table 2 p.9) vs B: `±9.02` (Fig 2 p.10)
- ☐ **PRO-CON-8** [INTERNAL] Text states 'no indication of publication bias in the funnel plot' and Methods cite Stata funnel routine, but no funnel plot figure is included in the PDF — A: `funnel plot referenced` (text p.3) vs B: `(no figure present)` (whole PDF)

## macnamara-2014-practice

_1 effect rows, 21 analyses, 4 documented contradictions → 10 value checks + 4 contradiction confirmations._

| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |
|---|---|---|---|---|---|---|
| ☐ | MAC-OV-2018 | Overall practice-performance [] pooled=.38 CI=[.33,.42] I2=88.54 | 1 | corrigendum Table 1 | Overall practice-performance | corrigendum-affected value (before/after pair) |
| ☐ | MAC-DOM-2018 | Domain moderator omnibus [sub] pooled=Q(4) = 36.61 CI=[,] I2= | 1 | corrigendum Table 1 | Domain moderator omnibus | corrigendum-affected value (before/after pair) |
| ☐ | MAC-GAMES-2018 | Games [sub] pooled=.49 CI=[,] I2= | 1 | corrigendum Table 1 | Games | corrigendum-affected value (before/after pair) |
| ☐ | MAC-MUSIC-2018 | Music [sub] pooled=.48 CI=[,] I2= | 1 | corrigendum Table 1 | Music | corrigendum-affected value (before/after pair) |
| ☐ | MAC-SPORTS-2018 | Sports [sub] pooled=.45 CI=[,] I2= | 1 | corrigendum Table 1 | Sports | corrigendum-affected value (before/after pair) |
| ☐ | MAC-EDU-2018 | Education [sub] pooled=.22 CI=[,] I2= | 1 | corrigendum Table 1 | Education | corrigendum-affected value (before/after pair) |
| ☐ | MAC-PROF-2018 | Professions [sub] pooled=.09 CI=[,] I2= | 1 | corrigendum Table 1 | Professions | corrigendum-affected value (before/after pair) |
| ☐ | MAC-PRED-2018 | Predictability moderator [sub] pooled=Q(1) = 11.32 CI=[,] I2= | 2 | corrigendum Table 1 | Predictability moderator | corrigendum-affected value (before/after pair) |
| ☐ | MAC-QMETH-2018 | DP assessment method moderator [sub] pooled=Q(2) = 18.18 CI=[,] I2= | 2 | corrigendum Table 1 | DP assessment method moderator | corrigendum-affected value (before/after pair) |
| ☐ | MAC-PMETH-2018 | Performance assessment method moderator [sub] pooled=Q(3) = 9.75 CI=[,] I2= | 2 | corrigendum Table 1 | Performance assessment method moderator | corrigendum-affected value (before/after pair) |

**Contradictions to confirm (both sides as printed):**

- ☐ **MAC-CON-1** [INTERNAL] Composite PDF pages 8 and 11 carry DUAL text layers: original 2014 values and 2018 corrected values on the same physical page (e.g. r=.35/I2=84.90 AND r=.38/I2=88.54 both extractab — A: `r̄=.35, I2=84.90` (PDF p.8 original layer) vs B: `r̄=.38, I2=88.54` (PDF p.8 corrected overlay)
- ☐ **MAC-CON-2** [INTERNAL] Abstract, General Discussion, and Figure 3 retain uncorrected domain percentages (26/21/18/4/<1%) while corrected Results read 24/23/20/5/1% — A: `games 26%` (abstract PDF p.4 / Fig.3 PDF p.11) vs B: `games 24%` (corrigendum Table 1 p.1)
- ☐ **MAC-CON-3** [ERRATUM] Corrigendum documents misapplied Cheung & Chan N-adjustment: used (N-1)/(C+1) per individual effect instead of ((N-1)/C)+1 on averaged effects; full before/after table published — A: `overall r̄=.35 [.30,.39]` (2014 article p.1612) vs B: `overall r̄=.38 [.33,.42]` (corrigendum Table 1)
- ☐ **MAC-CON-4** [INTERNAL] Stray production header from unrelated article (Shariff et al., 10.1177/0956797614534693) embedded in PDF p.4 text layer — A: `` (PDF p.4) vs B: `` ()

## hahn-2024-exercise-intake

_92 effect rows, 14 analyses, 16 documented contradictions → 21 value checks + 16 contradiction confirmations._

| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |
|---|---|---|---|---|---|---|
| ☐ | F4-TOT | (unlabeled diamond): effect=UNRESOLVED, ci_lower=UNRESOLVED, ci_upper=UNRESOLVED | 23 | Fig 4 | (unlabeled diamond) | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | A3tot | Total energy intake (kcal) [sub] pooled= CI=[,] I2= | 23 | Fig 4 | Total energy intake (kcal) | certainty=UNRESOLVED |
| ☐ | F6-12 | Thivel 2015 OW 60min rugby: effect=-240.00, ci_lower=-478.49, ci_upper=-1.51, se=121.68, weight_pct=6.1, n_treatment=14 | 25 | Fig 6 | Thivel 2015 OW 60min rugby | interpretation noted: matches Fig 2, NOT the swapped Fig 4 values (HAH-CON-01) |
| ☐ | F4-28 | Ajibewa 2017 NW 75% jumping jacks: effect=-17.00, ci_lower=-154.32, ci_upper=120.32, se=70.06, weight_pct=3.2, n_treatment=25 | 23 | Fig 4 | Ajibewa 2017 NW 75% jumping jacks | interpretation noted: Fig 2: SE 123.84, control 8; sole NW arm in subgroup, control unsplit |
| ☐ | F4-01 | Ajibewa 2017 NW 25% stretching: effect=17.00, ci_lower=-144.13, ci_upper=178.13, se=82.21, weight_pct=2.9, n_treatment=25 | 23 | Fig 4 | Ajibewa 2017 NW 25% stretching | interpretation noted: differs from Fig 2 (SE 100.69, control 8): control re-split 2-way (12) within su |
| ☐ | F4-39 | Thivel 2015 OW 75%: effect=-395.00, ci_lower=-589.10, ci_upper=-200.90, se=99.03, weight_pct=2.6, n_treatment=14 | 23 | Fig 4 | Thivel 2015 OW 75% | interpretation noted: CONTRADICTS Figs 2/3/5/6/7 (SE 142.95, CI [-675.18, -114.82]); see HAH-CON-01 |
| ☐ | F6-11 | Thivel 2013 OB 30min 75%: effect=480.00, ci_lower=254.13, ci_upper=705.87, se=115.24, weight_pct=6.3, n_treatment=10 | 25 | Fig 6 | Thivel 2013 OB 30min 75% | interpretation noted: rounding variant: Figs 2/3/4/5/7 print SE 115.25, CI [254.11, 705.89] (HAH-CON-0 |
| ☐ | F6-10 | Thivel 2012 OB 75%: effect=222.00, ci_lower=-129.21, ci_upper=573.21, se=179.19, weight_pct=4.3, n_treatment=15 | 25 | Fig 6 | Thivel 2012 OB 75% | interpretation noted: matches Fig 4 recomputed values, not Fig 2 |
| ☐ | F6-01 | Ajibewa 2017 NW 75% jumping jacks: effect=-17.00, ci_lower=-154.32, ci_upper=120.32, se=70.06, weight_pct=8.1, n_treatment=25 | 25 | Fig 6 | Ajibewa 2017 NW 75% jumping jacks | interpretation noted: matches Fig 4 recomputed values (control unsplit), not Fig 2 |
| ☐ | F3-ROWS | (27 study rows): n_treatment=509, n_control=375 | 22 | Fig 3 | (27 study rows) | interpretation noted: study rows identical to Fig 2 except noted variants (none in Fig 3: all 27 rows  |
| ☐ | F5-VCS | Varley Campbell 2017 NW + Snack: effect=-83.00, ci_lower=-276.64, ci_upper=110.64, se=98.8, weight_pct=2.8, n_treatment=38 | 24 | Fig 5 | Varley Campbell 2017 NW + Snack | interpretation noted: rounding variant: Figs 2/3/4/7 print SE 98.81, CI [-276.66, 110.66] (HAH-CON-04) |
| ☐ | F4-38 | Thivel 2015 OW 60min rugby: effect=-240.00, ci_lower=-520.18, ci_upper=40.18, se=142.95, weight_pct=1.8, n_treatment=14 | 23 | Fig 4 | Thivel 2015 OW 60min rugby | interpretation noted: CONTRADICTS Figs 2/3/5/6/7 (SE 121.68, CI [-478.49, -1.51]); both Thivel 2015 ar |
| ☐ | F6-12 | Thivel 2015 OW 60min rugby: effect=-240.00, ci_lower=-478.49, ci_upper=-1.51, se=121.68, weight_pct=6.1, n_treatment=14 | 25 | Fig 6 | Thivel 2015 OW 60min rugby | random sample (FOREST_PLOT) |
| ☐ | F4-33 | Nemet 2010 NW 45min aerobic: effect=26.00, ci_lower=-84.37, ci_upper=136.37, se=56.31, weight_pct=3.5, n_treatment=22 | 23 | Fig 4 | Nemet 2010 NW 45min aerobic | random sample (FOREST_PLOT) |
| ☐ | F2-40 | Varley Campbell 2017 NW: effect=-55.00, ci_lower=-274.54, ci_upper=164.54, se=112.01, weight_pct=2.5, n_treatment=38 | 22 | Fig 2 | Varley Campbell 2017 NW | random sample (FOREST_PLOT) |
| ☐ | F2-14 | Fillon 2020 OB 30min cycling, meal 90min post ex: effect=250.00, ci_lower=23.98, ci_upper=476.02, se=115.32, weight_pct=2.5, n_treatment=18 | 22 | Fig 2 | Fillon 2020 OB 30min cycling, meal 90min post ex | random sample (FOREST_PLOT) |
| ☐ | F4-17 | Nemet 2010 NW 45min resistance training: effect=169.00, ci_lower=10.77, ci_upper=327.23, se=80.73, weight_pct=2.9, n_treatment=22 | 23 | Fig 4 | Nemet 2010 NW 45min resistance training | random sample (FOREST_PLOT) |
| ☐ | F5-ROWS | (40 study rows):  | 24 | Fig 5 | (40 study rows) | random sample (FOREST_PLOT) |
| ☐ | F6-10 | Thivel 2012 OB 75%: effect=222.00, ci_lower=-129.21, ci_upper=573.21, se=179.19, weight_pct=4.3, n_treatment=15 | 25 | Fig 6 | Thivel 2012 OB 75% | random sample (FOREST_PLOT) |
| ☐ | F2-41 | Varley Campbell 2017 NW + Snack: effect=-83.00, ci_lower=-276.66, ci_upper=110.66, se=98.81, weight_pct=2.8, n_treatment=38 | 22 | Fig 2 | Varley Campbell 2017 NW + Snack | random sample (FOREST_PLOT) |
| ☐ | F7-S1 | Subtotal (95% CI): effect=-1.18, ci_lower=-46.17, ci_upper=43.81, weight_pct=51.3, n_treatment=441, n_control=205 | 26 | Fig 7 | Subtotal (95% CI) | random pooled-row check (row_kind guard) |

**Contradictions to confirm (both sides as printed):**

- ☐ **HAH-CON-01** [INTERNAL] Thivel 2015 SE/CI swap in Fig 4: rugby arm printed with SE 142.95 / CI [-520.18, 40.18] and 75% arm with SE 99.03 / CI [-589.10, -200.90], while every other figure prints rugby SE  — A: `rugby: 142.95 / [-520.18, 40.18]; 75%: 99.03 / [-589.10, -200.90]` (Fig 4, PDF p.23) vs B: `rugby: 121.68 / [-478.49, -1.51]; 75%: 142.95 / [-675.18, -114.82]` (Figs 2/3 p.22, Fig 5 p.24, Fig 6 p.25, Fig 7 p.26)
- ☐ **HAH-CON-02** [INTERNAL] Fig 4 high-intensity subtotal differs from Fig 6 Total although both pool the identical 14 arms (downstream consequence of HAH-CON-01) — A: `22.71 [-78.48, 123.90], I2=82%` (Fig 4 subtotal, p.23) vs B: `27.25 [-69.66, 124.15], I2=80%` (Fig 6 Total, p.25)
- ☐ **HAH-CON-03** [INTERNAL] Fig 4 draws an overall diamond but prints no 'Total (95% CI)' row; all other subgroup figures (5, 6, 7) print a labeled Total row — A: `unlabeled diamond, no numbers printed` (Fig 4, p.23) vs B: `labeled Total rows with values` (Figs 5/6/7, pp.24-26)
- ☐ **HAH-CON-04** [INTERNAL] Rounding variant for Varley Campbell 2017 NW + Snack between figures — A: `SE 98.8, CI [-276.64, 110.64]` (Fig 5, p.24) vs B: `SE 98.81, CI [-276.66, 110.66]` (Figs 2/3/4/7, pp.22-26)
- ☐ **HAH-CON-05** [INTERNAL] Rounding variant for Thivel 2013 OB 30min 75% between figures — A: `SE 115.24, CI [254.13, 705.87]` (Fig 6, p.25) vs B: `SE 115.25, CI [254.11, 705.89]` (Figs 2/3/4/5/7, pp.22-26)
- ☐ **HAH-CON-06** [INTERNAL] Text reports 43 exercise conditions but only 41 arms enter the meta-analysis — A: `'a total number of 43 exercise conditions'` (Results, p.17) vs B: `41 arms in every forest plot; '41 study arms were eligible'` (Figs 2-7 pp.22-26; Methods p.3)
- ☐ **HAH-CON-07** [INTERNAL] Ajibewa 2017 NW sample size: Table 1 reports n=26 but every forest plot prints intervention n=25 per NW arm (control splits 8+8+8=24 in Fig 2; 12+12+25 in Fig 4) — A: `n=26` (Table 1, p.5) vs B: `n=25` (Figs 2-7, pp.22-26)
- ☐ **HAH-CON-08** [INTERNAL] Control totals differ across figures: 478 (Figs 2/5/7) vs 578 (Fig 4 subtotal sum 359+219) vs 219 (Fig 6) — A: `478` (Fig 2 p.22 / Fig 5 p.24 / Fig 7 p.26) vs B: `578 (359+219)` (Fig 4, p.23)
- ☐ **HAH-CON-09** [INTERNAL] Country-percentage arithmetic errors: Europe printed 'n = 17; 67%' but 17/22 = 77%; 'Canada and USA (both n = 2; 13%)' but 2/22 = 9% (4/22 = 18%); Israel (Nemet 2010) omitted from  — A: `67%; 13%` (study-characteristics text, p.4) vs B: `17/22 = 77%; 2/22 = 9%` (arithmetic from same page)
- ☐ **HAH-CON-10** [INTERNAL] Table 1 Thivel et al. 2012: Fat (%) CON printed '20.72 +/- 4.69', identical to Protein (%) CON, and the CON macronutrient percentages sum to ~76% — A: `Fat (%) CON 20.72 +/- 4.69` (Table 1, p.13) vs B: `Protein (%) CON 20.72 +/- 4.69 (identical value)` (Table 1, p.13)
- ☐ **HAH-CON-11** [INTERNAL] Spelling/typo cluster: forest plots print 'Bozinosvki' vs 'Bozinovski' elsewhere; column header 'Invervention' in all six forest plots; 'Saunders 2013 NW wallking + PA'; axis label — A: `Bozinosvki; Invervention; wallking; HIgher` (Figs 1-7, pp.4-26) vs B: `Bozinovski; Intervention` (Table 1 p.6, Table 2 p.28, references)
- ☐ **HAH-CON-12** [INTERNAL] Saunders labeled '2013' in forest plots, Table 1 and Table 2, but reference [70] is Br J Nutr 2014;111:747-54 (published 2014) — A: `Saunders 2013` (plots pp.22-26; Table 1 p.12; Table 2 p.28) vs B: `2014;111:747-54` (reference [70])
- ☐ **HAH-CON-13** [INTERNAL] Text says 13 of 43 conditions (30%) were high intensity, but the Fig 4/Fig 6 high-intensity subgroup contains 14 of the 41 pooled arms — A: `13 (30%)` (Results, p.17) vs B: `14 arms` (Fig 4 p.23 / Fig 6 p.25)
- ☐ **HAH-CON-14** [INTERNAL] Table 2 has six domain columns (D1, DS, D2, D3, D4, D5) but the caption defines only D1-D5; 'DS' (RoB 2 crossover Domain S, period/carryover effects) is undefined — A: `columns D1, DS, D2, D3, D4, D5` (Table 2 grid, p.28) vs B: `caption defines D1-D5 only` (Table 2 caption, p.28)
- ☐ **HAH-CON-15** [INTERNAL] Forest-plot label 'Thivel 2013 OB 30min 75%' says 30min while Table 1 describes the exercise as 3 x 10 min bouts — A: `30min` (Figs 2-7, pp.22-26) vs B: `3 x 10 min` (Table 1, p.14)
- ☐ **HAH-CON-16** [INTERNAL] Fig 3 caption says 'low or moderate risk of bias' although RoB 2 categories are low / some concerns / high ('moderate' is not a RoB 2 category) — A: `low or moderate risk of bias` (Fig 3 caption, p.22) vs B: `low / some concerns / high` (Table 2, p.28)

## driessen-2015-nih-psychotherapy

_113 effect rows, 31 analyses, 23 documented contradictions → 20 value checks + 23 contradiction confirmations._

| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |
|---|---|---|---|---|---|---|
| ☐ | F2-22 | [unpublished study — name and values suppressed]:  | 13 | Fig 2 | Unpublished | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | F2-25 | [unpublished study — name and values suppressed]:  | 13 | Fig 2 | Unpublished | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | F3-07 | [unpublished study — name and values suppressed]:  | 13 | Fig 3 | Unpublished | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | F4-18 | [unpublished study — name and values suppressed]:  | 14 | Fig 4 | Unpublished | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | F6-18 | [unpublished study — name and values suppressed]:  | 15 | Fig 6 | Unpublished | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | F7-12 | [unpublished study — name and values suppressed]:  | 15 | Fig 7 | Unpublished | certainty=UNRESOLVED — must be human-adjudicated |
| ☐ | SENS-RANK | Depressive symptom severity [sub] pooled= CI=[,] I2= | 14 | S1 Table (not in PDF) | Depressive symptom severity | certainty=UNRESOLVED |
| ☐ | SENS-39-UNPUB | Depressive symptom severity [] pooled= CI=[,] I2= | 14-15 | S1 Table (not in PDF) | Depressive symptom severity | certainty=UNRESOLVED |
| ☐ | SENS-GOTTLIEB-A3 | Depressive symptom severity [sub] pooled= CI=[,] I2= | 15 | S1 Table (not in PDF) | Depressive symptom severity | certainty=UNRESOLVED |
| ☐ | SENS-GOTTLIEB-A4 | Depressive symptom severity [sub] pooled= CI=[,] I2= | 16 | S1 Table (not in PDF) | Depressive symptom severity | certainty=UNRESOLVED |
| ☐ | F5-12 | Wright, 2014: effect=0.08, ci_lower=-0.60, ci_upper=0.75, se=0.34, weight_pct=7.32 | 14 | Fig 5 | Wright, 2014 | interpretation noted: Z 0.23, p 0.82; as printed: PT1 vs PT2; HAMD; pass A links this row to Table 1 # |
| ☐ | F5-06 | Gallagher, 1982: effect=0.27, ci_lower=-0.58, ci_upper=1.12, se=0.43, weight_pct=5.00 | 14 | Fig 5 | Gallagher, 1982 | random sample (FOREST_PLOT) |
| ☐ | F2-19 | Weissman, 1979: effect=0.88, ci_lower=0.07, ci_upper=1.70, se=0.42, weight_pct=2.73 | 13 | Fig 2 | Weissman, 1979 | random sample (FOREST_PLOT) |
| ☐ | F2-17 | Thompson, 1987: effect=0.41, ci_lower=-0.09, ci_upper=0.91, se=0.26, weight_pct=5.21 | 13 | Fig 2 | Thompson, 1987 | random sample (FOREST_PLOT) |
| ☐ | F2-23 | Blum, unpublished: effect=0.50, ci_lower=-0.34, ci_upper=1.33, se=0.43, weight_pct=10.55 | 13 | Fig 2 | Blum, unpublished | random sample (FOREST_PLOT) |
| ☐ | F6-01 | Barber, 2012: effect=-0.11, ci_lower=-0.58, ci_upper=0.37, se=0.24, weight_pct=6.10 | 15 | Fig 6 | Barber, 2012 | random sample (FOREST_PLOT) |
| ☐ | F6-07 | Jarrett, 1999: effect=-0.22, ci_lower=-0.67, ci_upper=0.24, se=0.23, weight_pct=6.44 | 15 | Fig 6 | Jarrett, 1999 | random sample (FOREST_PLOT) |
| ☐ | F7-08 | Thompson, 2001: effect=0.41, ci_lower=-0.07, ci_upper=0.88, se=0.24, weight_pct=14.10 | 15 | Fig 7 | Thompson, 2001 | random sample (FOREST_PLOT) |
| ☐ | F2-07 | Hayden, 2012: effect=0.41, ci_lower=-0.26, ci_upper=1.09, se=0.34, weight_pct=3.62 | 13 | Fig 2 | Hayden, 2012 | random sample (FOREST_PLOT) |
| ☐ | F3-10 | Overall: effect=0.97, ci_lower=0.62, ci_upper=1.32, se=0.18 | 13 | Fig 3 | Overall | random pooled-row check (row_kind guard) |

**Contradictions to confirm (both sides as printed):**

- ☐ **DRI-CON-01** [INTERNAL] Table 1 continuation header on page 11 prints 'PUBLISHED' although every study row on that page (46 Clark through 57 Zlotnick) belongs to the UNPUBLISHED section, which began at ro — A: `PUBLISHED (continuation header)` (Table 1, p11) vs B: `rows 46-57 are unpublished grants` (Table 1, pp10-11)
- ☐ **DRI-CON-02** [INTERNAL] Table 2 percentage-change cell for PT vs. antidepressant medication prints '-456%' — A: `-456%` (Table 2, p12) vs B: `delta-g = -0.07 from a published-only baseline of g = 0.01` (Table 2, p12)
- ☐ **DRI-CON-03** [INTERNAL] Reynolds grant number printed 'R01MH37869' with a 5-digit serial; every other MH grant in Table 1 has 6 digits (e.g. R01MH063982) — A: `R01MH37869` (Table 1 row 31, p10) vs B: `6-digit serials elsewhere` (Table 1, pp9-11)
- ☐ **DRI-CON-04** [INTERNAL] Six published Table 1 studies appear in NO forest plot and are not countable in any Table 2 k: Freedland (#11, ref [40]), Glick (#12, refs [41-42]), Jacobson R37MH044063 (#20, ref  — A: `listed as PUBLISHED in Table 1` (Table 1, pp9-10) vs B: `absent from Figs 2-7 and every Table 2 pool` (Figs 2-7 pp13-15; Table 2 p12)
- ☐ **DRI-CON-05** [INTERNAL] Table 1 row 46 (Clark, R01MH062054d) has no entry in 'Study comparison(s)', 'PT type(s)' or any quality-rating column; every other unpublished row lists comparisons — even Gottlieb — A: `row prints only PI and grant number` (Table 1 row 46, p11) vs B: `all other unpublished rows populated` (Table 1, pp10-11)
- ☐ **DRI-CON-06** [INTERNAL] Unpublished quality-rating denominator inconsistency: text says quality ratings could not be retrieved for three unpublished studies (implying 13-3 = 10 rated), but the printed per — A: `13 - 3 = 10 rated` (text p16) vs B: `percentages imply 9 rated (and 53 total)` (text p16)
- ☐ **DRI-CON-07** [INTERNAL] t-test degrees of freedom: p16 reports t(54) = 0.79 comparing mean participants per condition between 13 unpublished and 42 published studies; a two-sample t-test on 55 studies wou — A: `t(54)` (text p16) vs B: `expected df = 53 (13 + 42 - 2)` (derived from study counts, pp7 and 16)
- ☐ **DRI-CON-08** [INTERNAL] Data Availability Statement grammatical error: 'as we obtained it this data from third parties' — A: `we obtained it this data` (Data Availability Statement, pp1-2) vs B: `(standard grammar)` ()
- ☐ **DRI-CON-09** [INTERNAL] Decimal-comma typo '84,6%' in body text; the rest of the body text and Table 2 use decimal points, while Figs 2-7 print decimal commas throughout (CMA European-locale output) — A: `84,6%` (text p7) vs B: `decimal points elsewhere in text` (body text / Table 2)
- ☐ **DRI-CON-10** [INTERNAL] Figure order reversed on page 15: Fig 7 (PT+ADM vs ADM) is printed ABOVE Fig 6 (PT vs ADM); the caption block for Fig 7 also precedes Fig 6's in the text flow, and the embedded ima — A: `Fig 7 above Fig 6 on the page` (p15 layout and embedded-image order) vs B: `numeric figure order (6 then 7)` (figure numbering / captions)
- ☐ **DRI-CON-11** [INTERNAL] Suppressed unpublished forest-plot rows: Figs 2 (x2), 3, 4, 6 and 7 contain 'Unpublished' rows with every cell blank; visible unpublished relative weights therefore sum to <100 (Fi — A: `six fully blank study rows` (Figs 2, 3, 4, 6, 7, pp13-15) vs B: `Table 2 k counts include them` (Table 2, p12)
- ☐ **DRI-CON-12** [INTERNAL] Partial anonymization inconsistency: Blum, Hauenstein, Thase and Delgado are named with full statistics in some figures, while other unpublished rows show values without names and  — A: `named unpublished rows` (Figs 2, 3, 4, 6) vs B: `anonymized/suppressed unpublished rows` (Figs 2, 4, 5, 6, 7)
- ☐ **DRI-CON-13** [INTERNAL] Control-condition abbreviation inconsistency: Table 1 legend defines 'CTRL-PLAC = pill-placebo control condition' but the forest plots label the same condition 'CTRL-NS(PLAC)', whi — A: `CTRL-PLAC` (Table 1 legend, p11) vs B: `CTRL-NS(PLAC)` (Fig 2/Fig 4 captions, pp13-14)
- ☐ **DRI-CON-14** [INTERNAL] Table 2 note says differences were 'calculated using 5 decimals', so printed pairs such as delta-g = -0.04 with -4% (row 1a) versus delta-g = -0.04 with -24% (row 2) are not reprod — A: `-4% vs -24% for identical printed delta-g = -0.04` (Table 2, p12) vs B: `5-decimal computation note` (Table 2 footnote, p12)
- ☐ **DRI-CON-15** [INTERNAL] Table 2 I2 95% CI printed as '-' for all three k=2 unpublished subgroups (rows 1a, 2 and 4) — A: `-` (Table 2, p12) vs B: `CIs printed for all other rows` (Table 2, p12)
- ☐ **DRI-CON-16** [INTERNAL] Table 2 row 1a unpublished participant counts NPT = 45 vs NComp = 14 — a 45:14 split across only 2 studies — A: `45/14` (Table 2, p12) vs B: `(no per-study Ns printed anywhere to verify)` (Figs 2-7 print no per-study Ns)
- ☐ **DRI-CON-17** [INTERNAL] Multiple non-publication-rate variants coexist: 13/55 = 23.6% (main); 15/57 = 26.3% (counting the two never-started grants); 14/55 = 25.5% (sensitivity counting [39] as unpublished — A: `23.6% (13/55)` (abstract p1 / text p7) vs B: `26.3% (15/57); 25.5% (14/55); 20%` (text pp7, 12, 18)
- ☐ **DRI-CON-18** [INTERNAL] Grant-vs-study counting: grants #29 (Murphy R01MH032756) and #40 (Thompson R01MH037196) each produced two published trials ([59]+[60]; [70]+[71]), so 42 published grants correspond — A: `42 published grants` (text p7) vs B: `44 published studies (reconciles quality percentages, e.g. 18.2% = 8/44)` (Table 1 p10; text p16)
- ☐ **DRI-CON-19** [INTERNAL] Study [39] (Frank R21MH061948) is counted as published although it 'reported the grant-funded trial's outcomes only in aggregate with outcomes of other trials'; per-trial data were — A: `Fig 5 'Wright, 2014' row = ref [39] (pass A inference from name/year match)` (Fig 5, p14; Table 1 row 10) vs B: `placement not explicitly stated (pass B position)` (text p11)
- ☐ **DRI-CON-20** [INTERNAL] Outcome label 'no failure' printed for the Weissman, 1979 rows in Figs 2, 4, 6 and 7 — an unusual outcome descriptor — A: `no failure` (Figs 2, 4, 6, 7, pp13-15) vs B: `conventional scale names for all other rows` (Figs 2-7)
- ☐ **DRI-CON-21** [INTERNAL] 'Waters, in press' is grouped as Published in Figs 2 and 4; its reference [52] is dated 2015 (Psychother Res) — the label is frozen at 'in press' — A: `Waters, in press` (Figs 2, 4, pp13-14) vs B: `reference [52] dated 2015` (References)
- ☐ **DRI-CON-22** [INTERNAL] Composition of the k=5 published pill-placebo pool (text p14) is not identifiable from the figures: only 3 published Fig 2/Fig 4 rows are labelled CTRL-NS(PLAC) (Barber, DeRubeis,  — A: `k=5 published pill-placebo studies` (text p14) vs B: `3 explicitly labelled CTRL-NS(PLAC) rows` (Figs 2/4, pp13-14)
- ☐ **DRI-CON-23** [INTERNAL] Fig 2/Fig 3 'Wright, 2005' comparison cell prints 'Combined' although the row sits in the no-treatment-controls analysis (Fig 3) — A: `Combined` (Figs 2-3, p13) vs B: `analysis is PT vs CTRL-NT` (Fig 3 caption, p13)

## cooney-2013-exercise-depression

_78 effect rows, 7 analyses, 13 documented contradictions → 16 value checks + 13 contradiction confirmations._

| ✓ | ID | Truth value | Page | Table/Figure | Region (row) | Reason selected |
|---|---|---|---|---|---|---|
| ☐ | E61 | Krogh 2009: effect=1.14, ci_lower=0.96, ci_upper=1.37, weight_pct=2.9, events_treatment=48, events_control=42 | 107 | Analysis 1.3 | Krogh 2009 | interpretation noted: RevMan forest table, full text layer; n/N: exercise 48/55, control 42/55; denomi |
| ☐ | E77 | Total: effect=1, ci_lower=0.97, ci_upper=1.04, weight_pct=100, events_treatment=610, events_control=577 | 107 | Analysis 1.3 | Total (95% CI) | interpretation noted: RevMan forest table, full text layer; row label verbatim 'Total (95% CI)' (diffe |
| ☐ | E08 | Dunn 2005: effect=-0.74, ci_lower=-1.5, ci_upper=0.02, weight_pct=2.87, n_treatment=16, n_control=13 | 105 | Analysis 1.1 | Dunn 2005 | random sample (FOREST_PLOT) |
| ☐ | E62 | Martinsen 1985: effect=0.93, ci_lower=0.74, ci_upper=1.18, weight_pct=1.65, events_treatment=20, events_control=17 | 107 | Analysis 1.3 | Martinsen 1985 | random sample (FOREST_PLOT) |
| ☐ | E04 | Bonnet 2005: effect=1.51, ci_lower=0.09, ci_upper=2.93, weight_pct=1.37, n_treatment=5, n_control=6 | 105 | Analysis 1.1 | Bonnet 2005 | random sample (FOREST_PLOT) |
| ☐ | E61 | Krogh 2009: effect=1.14, ci_lower=0.96, ci_upper=1.37, weight_pct=2.9, events_treatment=48, events_control=42 | 107 | Analysis 1.3 | Krogh 2009 | random sample (FOREST_PLOT) |
| ☐ | E35 | Williams 2008: effect=-0.48, ci_lower=-1.23, ci_upper=0.27, weight_pct=2.9, n_treatment=17, n_control=12 | 106 | Analysis 1.1 | Williams 2008 | random sample (FOREST_PLOT) |
| ☐ | E22 | Mota-Pereira 2011: effect=-0.67, ci_lower=-1.46, ci_upper=0.12, weight_pct=2.77, n_treatment=19, n_control=10 | 105 | Analysis 1.1 | Mota-Pereira 2011 | random sample (FOREST_PLOT) |
| ☐ | E57 | Hemat-Far 2012: effect=1, ci_lower=0.83, ci_upper=1.2, weight_pct=2.77, events_treatment=10, events_control=10 | 106 | Analysis 1.3 | Hemat-Far 2012 | random sample (FOREST_PLOT) |
| ☐ | E11 | Fremont 1987: effect=0.23, ci_lower=-0.45, ci_upper=0.9, weight_pct=3.15, n_treatment=18, n_control=16 | 105 | Analysis 1.1 | Fremont 1987 | random sample (FOREST_PLOT) |
| ☐ | E66 | Mutrie 1988: effect=1, ci_lower=0.8, ci_upper=1.26, weight_pct=1.76, events_treatment=9, events_control=7 | 107 | Analysis 1.3 | Mutrie 1988 | random sample (FOREST_PLOT) |
| ☐ | E23 | Mutrie 1988: effect=-2.39, ci_lower=-3.76, ci_upper=-1.02, weight_pct=1.44, n_treatment=9, n_control=7 | 105 | Analysis 1.1 | Mutrie 1988 | random sample (FOREST_PLOT) |
| ☐ | E20 | Mather 2002: effect=-0.17, ci_lower=-0.59, ci_upper=0.26, weight_pct=4.1, n_treatment=43, n_control=43 | 105 | Analysis 1.1 | Mather 2002 | random sample (FOREST_PLOT) |
| ☐ | E30 | Shahidi 2011: effect=-0.65, ci_lower=-1.29, ci_upper=-0.02, weight_pct=3.29, n_treatment=20, n_control=20 | 106 | Analysis 1.1 | Shahidi 2011 | random sample (FOREST_PLOT) |
| ☐ | E55 | Fremont 1987: effect=1.11, ci_lower=0.87, ci_upper=1.41, weight_pct=1.58, events_treatment=18, events_control=31 | 106 | Analysis 1.3 | Fremont 1987 | random sample (FOREST_PLOT) |
| ☐ | E77 | Total: effect=1, ci_lower=0.97, ci_upper=1.04, weight_pct=100, events_treatment=610, events_control=577 | 107 | Analysis 1.3 | Total (95% CI) | random pooled-row check (row_kind guard) |

**Contradictions to confirm (both sides as printed):**

- ☐ **COO-CON-1** [INTERNAL] Participant count for primary Analysis 1.1: Abstract and Effects text say '35 trials (1356 participants)' while Comparison 1 summary table, Summary of findings table 1 and the fore — A: `1356` (Abstract PDF p5; Effects text PDF p27) vs B: `1353` (Comparison 1 table PDF p104; SOF PDF p7; Analysis 1.1 forest totals PDF p106)
- ☐ **COO-CON-2** [INTERNAL] Heterogeneity qualifier for the same I2=63% in Analysis 1.1: Abstract calls it 'moderate heterogeneity', Effects text calls it 'substantial heterogeneity' — A: `moderate heterogeneity (I2 = 63%)` (Abstract PDF p5) vs B: `substantial heterogeneity (I2 = 63%)` (Effects text PDF p27)
- ☐ **COO-CON-3** [INTERNAL] I2 precision for Analysis 1.1: forest plot prints I2=62.78% while Abstract and Effects text print 63% — A: `62.78%` (Analysis 1.1 forest heterogeneity line PDF p106) vs B: `63%` (Abstract PDF p5; Effects text PDF p27)
- ☐ **COO-CON-4** [INTERNAL] Analysis 4.1 (exercise vs pharmacological) participant count: Effects text says 'four trials (298 participants)' while Abstract (n = 300), Comparison 4 summary table and forest tot — A: `298` (Effects text PDF p28) vs B: `300` (Abstract PDF p5; Comparison 4 table PDF p110; Analysis 4.1 forest totals PDF p110)
- ☐ **COO-CON-5** [INTERNAL] Sign typo in Comparison 6 summary table: Outcome 4 (ITT-only sensitivity, Analysis 6.4) effect printed '-0.61 [1.00, -0.22]' — lower CI bound missing its minus sign; the Analysis 6 — A: `-0.61 [1.00, -0.22]` (Comparison 6 summary table PDF p120) vs B: `-0.61[-1,-0.22]` (Analysis 6.4 forest total PDF p122)
- ☐ **COO-CON-6** [INTERNAL] Comparison 5 subgroup participant sums: outcomes 5.1-5.4 subgroup Ns each sum to 1352 (e.g. 5.1: 1080+128+144) while Analysis 1.1 and outcome 5.5 report 1353 for the same 35 trials — A: `1352` (Comparison 5 summary table outcomes 5.1-5.4 PDF p111-113) vs B: `1353` (Analysis 1.1 / outcome 5.5 PDF p104 and p113)
- ☐ **COO-CON-7** [INTERNAL] Multi-arm arm selection: the same study label carries different Ns across analyses. A1.1 uses analysed-participant Ns of the biggest-dose exercise arm; A1.3 uses randomised denomin — A: `e.g. Klein 1985 N=14/8` (Analysis 1.1 forest PDF p105) vs B: `e.g. Klein 1985 15/27 vs 16/24` (Analysis 1.3 forest PDF p107)
- ☐ **COO-CON-8** [INTERNAL] Cross-analysis arm reuse between Analysis 1.3 and Analysis 2.2: Fremont 1987 'Control' 31/40 in A1.3 is numerically identical to the 'Cognitive therapy' arm in Analysis 2.2; Klein  — A: `Fremont 1987 control 31/40; Klein 1985 15/27 vs 16/24` (Analysis 1.3 forest PDF p106-107) vs B: `identical n/N cells` (Analysis 2.2 forest PDF p109)
- ☐ **COO-CON-9** [INTERNAL] Blumenthal 1999 follow-up cells (Analysis 1.2) print Mean(SD) '10.6 (0.8)' / '11 (0.8)' — SDs an order of magnitude smaller than the same trial's post-treatment SDs (6.9/6.5); valu — A: `10.6 (0.8) / 11 (0.8)` (Analysis 1.2 forest PDF p106) vs B: `8.7 (6.9) / 7.8 (6.5) post-treatment` (Analysis 1.1 forest PDF p105)
- ☐ **COO-CON-10** [INTERNAL] Effect-measure mislabelling around Analysis 5.5 (type of control): summary table prints 'Mean Difference (IV, Fixed, 95% CI)' with pooled -1.57 [-1.97, -1.16] across trials using d — A: `MD (IV, Fixed) -1.57 [-1.97, -1.16]` (Comparison 5 outcome 5 PDF p113) vs B: `quoted as 'SMD'` (Discussion PDF p29)
- ☐ **COO-CON-11** [INTERNAL] Quality-of-life trial-count inconsistency: Effects text says 'Five trials reported quality of life' while the Comparison 1 table lists 4 studies for Analysis 1.4 (Hoffman 2010's Qo — A: `Five trials` (Effects text PDF p27) vs B: `4 studies (Analysis 1.4); 'three trials' per Abstract` (Comparison 1 table PDF p104-105; Abstract PDF p5)
- ☐ **COO-CON-12** [INTERNAL] Doyne 1987 is quoted in the Effects text as having '42% completion' yet does not appear as a row in Analysis 1.3 (completion analysis); the stated count 'Twenty-nine studies (1363  — A: `Doyne 1987 '42% completion'` (Effects text PDF p27) vs B: `Doyne 1987 absent from Analysis 1.3 rows` (Analysis 1.3 forest PDF p106-107)
- ☐ **COO-CON-13** [INTERNAL] Multi-arm selection wording conflict: p29 says the 'arm with the largest clinical effect' was used in comparison 1, conflicting with the Methods/Abstract statement that the biggest — A: `arm with the largest clinical effect` (Effects/Discussion PDF p29) vs B: `biggest dose of exercise` (Abstract/Methods PDF p4-5; Differences between protocol and review PDF p132)

---

## Sign-off

Total review items: 175.

When review is complete, record in each paper's `truth/notes.md`:
`Researcher spot-check: PASSED/CORRECTED, <date>, <initials>` and set the
paper's status to SIGNED_OFF. When all development papers are signed off,
tag the corpus state as **GOLD_TRUTH_V1** (git tag `gold-truth-v1`).
GOLD_TRUTH_V1 is immutable: any later correction creates a versioned
revision (new dated notes entry + git-tracked change), never a silent edit.
