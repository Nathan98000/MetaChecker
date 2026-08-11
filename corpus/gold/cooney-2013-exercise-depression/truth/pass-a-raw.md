# PASS A — GOLD TRUTH EXTRACTION (RAW)
# Cooney 2013 "Exercise for depression" — PMC deposit PMC9721454.pdf
# Extracted 2026-08-11. Method: PyMuPDF text layer, cross-verified row-by-row against
# rendered page images (2x zoom) for all truthed pages (PDF p105, p106, p107).
# All page numbers are 1-based pages of THIS PDF (132 pages). Printed Cochrane page = PDF page - 3
# (printed p.1 = PDF p.4; SOF pages use their own landscape numbering).

## 0. DOCUMENT SURVEY (what the PDF actually contains)

- 132-page PMC deposit of the full Cochrane review. The Data and Analyses section is COMPLETE:
  all 24 analyses listed in the TOC are present as full forest plots (vector-drawn graphics with
  the numeric table in the selectable text layer — NOT rasterized). Nothing is omitted or
  compressed; per-page raster images are only the Cochrane logo/branding (5 decorative images
  on every page, sizes 402x612 / 706x281).
- Main-text figures: Figure 1 study flow diagram (p19), Figure 2 'Risk of bias' graph (p23),
  Figure 3 'Risk of bias' summary (p24-25), Figure 4 funnel plot for Analysis 1.1 (p26).
  There are NO forest plots in the main text; all forests live in DATA AND ANALYSES (p104-123).
- Section starts: ABSTRACT p4; PLAIN LANGUAGE SUMMARY p5; SUMMARY OF FINDINGS p7 (SOF main
  comparison p7-8, SOF 2 p9, SOF 3 p10, SOF 4 p11-12); RESULTS p18; DISCUSSION p30;
  REFERENCES p34; CHARACTERISTICS OF STUDIES p49; DATA AND ANALYSES p104; ADDITIONAL TABLES
  p124; APPENDICES p127; back matter through p132.
- Forest-plot text layer verified against rendered images: column order on page is
  Study | N | Mean(SD) [exercise] | N | Mean(SD) [control] | plot | Weight | Effect[CI].
  Dichotomous analyses use n/N | n/N. Text-layer numbers matched the images exactly on all
  three truthed analyses.

## REVIEW-LEVEL SUMMARY NUMBERS (verbatim, with pages)

- "Thirty-nine trials (2326 participants) fulfilled our inclusion criteria, of which 37 provided data for meta-analyses." (Abstract, p5)
- "We included 37 trials in our meta-analyses. The remaining two trials could not be included for the reasons stated above (Greist 1979; McCann 1984)." (p27)
- "Thirty-five trials (1356 participants) included a comparison of exercise with a 'control' intervention." (p27; abstract p5 likewise says "35 trials (1356 participants)")
- Headline pooled effect, exercise vs control post-treatment: "the pooled SMD for the primary outcome of depression at the end of treatment was -0.62 (95% confidence interval (CI) -0.81 to -0.42)" ... "There was moderate heterogeneity (I2 = 63%)." (Abstract p5). Effects text p27: "-0.62 (95% confidence interval (CI) -0.81 to -0.42) (Analysis 1.1) ... There was substantial heterogeneity (I2 = 63%)."
- Methodologically robust trials only: "six trials (464 participants) ... pooled SMD ... was not statistically significant (-0.18, 95% CI -0.47 to 0.11)." (Abstract p5; = Analysis 6.6)
- Follow-up: "eight trials (377 participants) providing long-term follow-up data on mood found a small effect in favour of exercise (SMD -0.33, 95% CI -0.63 to -0.03)." (Abstract p5; = Analysis 1.2)
- Acceptability: "For acceptability of treatment (assessed by number of drop-outs during the intervention), the risk ratio was 1.00 (95% CI 0.97 to 1.04)." (Abstract p5; = Analysis 1.3, "Twenty-nine studies (1363 participants)" per p27)
- Exercise vs psychological therapy: "Seven trials compared exercise with psychological therapy (189 participants), and found no significant difference (SMD -0.03, 95% CI -0.32 to 0.26)." (Abstract p5)
- Exercise vs pharmacological: "Four trials (n = 300) compared exercise with pharmacological treatment and found no significant difference (SMD -0.11, -0.34, 0.12)." (Abstract p5; note Effects text p28 says "four trials (298 participants)")
- Exercise vs bright light: "One trial (n = 18) reported that exercise was more effective than bright light therapy (MD -6.40, 95% CI -10.20 to -2.60)." (Abstract p5)
- SOF main comparison (p7-8): symptoms of depression 1353 (35 studies), GRADE moderate, "SMD -0.62 (95% CI: -0.81 to -0.42)"; long-term 377 (8 studies), GRADE low, "SMD -0.33 (95% CI: -0.63 to -0.03)"; acceptability 1363 (29 studies), "RR 1 (95% CI: 0.97 to 1.04)", assumed risk 865 per 1000, corresponding 865 per 1000 (839 to 900).

## 1. ANALYSES (truthed targets)

Format: analysis_id | outcome | comparison | subgroup | effect_measure | model | n_studies | n_participants | pooled_effect | ci_lower | ci_upper | i2 | p_or_z | source_page | source

A1.1 | Reduction in depression symptoms post-treatment | Exercise versus 'control' | (none — no subgroups in this analysis) | Std. Mean Difference (IV, Random, 95% CI) | Random | 35 | 1353 | -0.62 | -0.81 | -0.42 | 62.78% (forest); "63%" in Abstract/Effects text | Z=6.22(P<0.0001); heterogeneity Chi2=91.35, df=34(P<0.0001), Tau2=0.19 | 104-106 (summary table p104 row "-0.62 [-0.81, -0.42]"; forest p105-106) | Comparison 1 table + Analysis 1.1 forest; text layer, image-verified
A1.3 | Completed intervention or control | Exercise versus 'control' | (none) | Risk Ratio (M-H, Random, 95% CI) | Random | 29 | 1363 | 1.00 (forest total prints "1[0.97,1.04]") | 0.97 | 1.04 | 0% | Z=0.28(P=0.78); heterogeneity Chi2=20.7, df=28(P=0.84), Tau2=0 | 105 (summary table row "1.00 [0.97, 1.04]"), 106-107 (forest) | Comparison 1 table + Analysis 1.3 forest; text layer, image-verified
A1.2 | Reduction in depression symptoms follow-up | Exercise versus 'control' | (none) | Std. Mean Difference (IV, Random, 95% CI) | Random | 8 | 377 | -0.33 | -0.63 | -0.03 | 48.71% (forest); "49%" in Effects text p27 | Z=2.18(P=0.03); heterogeneity Chi2=13.65, df=7(P=0.06), Tau2=0.09 | 105 (summary table row "-0.33 [-0.63, -0.03]"), 106 (forest) | Comparison 1 table + Analysis 1.2 forest; text layer, image-verified

Note on n_participants for A1.1: forest total 711 + 642 = 1353; Comparison-1 summary table (p104) and SOF (p7) say 1353; Abstract (p5) and Effects text (p27) say 1356. Recorded 1353 as the analysis-level truth; discrepancy logged in section 4.

## 2. PUBLISHED_EFFECTS

Format: effect_id | analysis_id | row_kind | study_label | n_treatment | mean_sd_treatment | n_control | mean_sd_control | effect | ci_lower | ci_upper | weight_pct | source_page | source_type | figure_or_analysis_ref | certainty | note

### Analysis 1.1 — Exercise vs 'control', depression symptoms post-treatment (SMD, Random). 35 study rows + total. Axis: "Favours exercise" -5..5 "Favours control".

A1.1-R01 | 1.1 | STUDY | Blumenthal 1999 | 55 | 8.7 (6.9) | 48 | 7.8 (6.5) | 0.14 | -0.25 | 0.52 | 4.23% | 105 | text layer (vector forest), image-verified | Analysis 1.1 | KNOWN |
A1.1-R02 | 1.1 | STUDY | Blumenthal 2007 | 51 | 9.2 (6.1) | 49 | 11.1 (7) | -0.29 | -0.68 | 0.11 | 4.21% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R03 | 1.1 | STUDY | Blumenthal 2012a | 35 | 6.4 (5.3) | 21 | 10 (5.3) | -0.67 | -1.23 | -0.12 | 3.59% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R04 | 1.1 | STUDY | Bonnet 2005 | 5 | 24.5 (10.9) | 6 | 10.5 (5.8) | 1.51 | 0.09 | 2.93 | 1.37% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | only study row favouring control with CI excluding 0
A1.1-R05 | 1.1 | STUDY | Brenes 2007 | 14 | 7.8 (4.3) | 12 | 10.9 (5.8) | -0.6 | -1.39 | 0.2 | 2.77% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R06 | 1.1 | STUDY | Chu 2008 | 15 | 5.8 (3.4) | 12 | 10.6 (5.7) | -1.02 | -1.84 | -0.21 | 2.69% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R07 | 1.1 | STUDY | Doyne 1987 | 14 | 8.2 (5.3) | 11 | 15.3 (6.3) | -1.19 | -2.06 | -0.32 | 2.53% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R08 | 1.1 | STUDY | Dunn 2005 | 16 | 10 (5.5) | 13 | 14 (4.9) | -0.74 | -1.5 | 0.02 | 2.87% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R09 | 1.1 | STUDY | Epstein 1986 | 7 | 9 (10.9) | 10 | 16.3 (7.4) | -0.77 | -1.78 | 0.24 | 2.15% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R10 | 1.1 | STUDY | Foley 2008 | 8 | 10.8 (9.3) | 5 | 13.6 (10.2) | -0.27 | -1.4 | 0.85 | 1.89% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R11 | 1.1 | STUDY | Fremont 1987 | 18 | 10 (9.8) | 16 | 8 (7.1) | 0.23 | -0.45 | 0.9 | 3.15% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R12 | 1.1 | STUDY | Gary 2010 | 20 | 8.4 (5.6) | 15 | 9.3 (4.9) | -0.17 | -0.84 | 0.51 | 3.17% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R13 | 1.1 | STUDY | Hemat-Far 2012 | 10 | 16.6 (6.9) | 10 | 22.8 (4.9) | -0.99 | -1.93 | -0.05 | 2.32% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R14 | 1.1 | STUDY | Hess-Homeier 1981 | 5 | 9.8 (6.9) | 6 | 16.2 (8.4) | -0.75 | -2 | 0.5 | 1.64% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | CI prints as [-2,0.5]
A1.1-R15 | 1.1 | STUDY | Hoffman 2010 | 37 | 16.4 (10.2) | 39 | 21.2 (12) | -0.43 | -0.88 | 0.03 | 3.98% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | spelled "Hoffman 2010" here; "Hoﬀman 2010" (ligature) in body text
A1.1-R16 | 1.1 | STUDY | Klein 1985 | 14 | 1 (0.9) | 8 | 0.8 (0.5) | 0.24 | -0.64 | 1.11 | 2.52% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | means on a different (small-range) scale than most rows
A1.1-R17 | 1.1 | STUDY | Knubben 2007 | 20 | 11.2 (4) | 18 | 15.5 (6.1) | -0.83 | -1.49 | -0.16 | 3.19% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R18 | 1.1 | STUDY | Krogh 2009 | 48 | 12.1 (6.4) | 42 | 10.6 (5.6) | 0.25 | -0.17 | 0.66 | 4.13% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | biggest-dose arm used (multi-arm trial; see section 4)
A1.1-R19 | 1.1 | STUDY | Martinsen 1985 | 24 | 12.1 (7.1) | 19 | 22.8 (11.4) | -1.14 | -1.79 | -0.48 | 3.24% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R20 | 1.1 | STUDY | Mather 2002 | 43 | 12.6 (7) | 43 | 13.7 (6) | -0.17 | -0.59 | 0.26 | 4.1% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | weight printed with 2 sig figs ("4.1%")
A1.1-R21 | 1.1 | STUDY | McNeil 1991 | 10 | 11.1 (3) | 10 | 14.7 (3.7) | -1.02 | -1.97 | -0.08 | 2.31% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R22 | 1.1 | STUDY | Mota-Pereira 2011 | 19 | 12.5 (1.7) | 10 | 13.6 (1.3) | -0.67 | -1.46 | 0.12 | 2.77% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R23 | 1.1 | STUDY | Mutrie 1988 | 9 | 9.5 (4.3) | 7 | 21.4 (5.3) | -2.39 | -3.76 | -1.02 | 1.44% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | largest effect in analysis
A1.1-R24 | 1.1 | STUDY | Nabkasorn 2005 | 21 | 14.4 (4.1) | 28 | 17.5 (4.2) | -0.73 | -1.31 | -0.14 | 3.48% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R25 | 1.1 | STUDY | Orth 1979 | 3 | 7 (6.6) | 2 | 16.5 (2.1) | -1.25 | -3.71 | 1.21 | 0.56% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | smallest trial (n=5)
A1.1-R26 | 1.1 | STUDY | Pilu 2007 | 10 | 8.1 (5.2) | 20 | 16.7 (9.1) | -1.04 | -1.85 | -0.23 | 2.71% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R27 | 1.1 | STUDY | Reuter 1984 | 9 | 5.1 (4.8) | 9 | 18.6 (7.7) | -2 | -3.19 | -0.82 | 1.77% | 105 | text layer, image-verified | Analysis 1.1 | KNOWN | effect prints as "-2[-3.19,-0.82]"
A1.1-R28 | 1.1 | STUDY | Schuch 2011 | 15 | 5.9 (4.5) | 11 | 9.5 (3.6) | -0.83 | -1.65 | -0.01 | 2.69% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R29 | 1.1 | STUDY | Setaro 1985 | 25 | 62 (6.5) | 25 | 69.9 (4) | -1.44 | -2.07 | -0.81 | 3.33% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN | means on a much larger scale (MMPI-D-type) than other rows
A1.1-R30 | 1.1 | STUDY | Shahidi 2011 | 20 | 11.1 (6.2) | 20 | 15.2 (6.1) | -0.65 | -1.29 | -0.02 | 3.29% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R31 | 1.1 | STUDY | Sims 2009 | 23 | 15.1 (8.5) | 22 | 20.6 (11.8) | -0.53 | -1.12 | 0.07 | 3.45% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R32 | 1.1 | STUDY | Singh 1997 | 17 | 9.8 (2.4) | 15 | 13.8 (2) | -1.75 | -2.59 | -0.92 | 2.64% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R33 | 1.1 | STUDY | Singh 2005 | 18 | 8.5 (5.5) | 19 | 14.4 (6) | -1 | -1.69 | -0.31 | 3.11% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN | effect prints as "-1[-1.69,-0.31]"
A1.1-R34 | 1.1 | STUDY | Veale 1992 | 36 | 13.9 (12.8) | 29 | 17.8 (10.2) | -0.33 | -0.82 | 0.17 | 3.84% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R35 | 1.1 | STUDY | Williams 2008 | 17 | 8.4 (5.8) | 12 | 11.8 (8.1) | -0.48 | -1.23 | 0.27 | 2.9% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN |
A1.1-R36 | 1.1 | OVERALL_TOTAL | Total *** | 711 | | 642 | | -0.62 | -0.81 | -0.42 | 100% | 106 | text layer, image-verified | Analysis 1.1 | KNOWN | 711+642=1353
A1.1-R37 | 1.1 | HETEROGENEITY | Heterogeneity / test rows | | | | | | | | | 106 | text layer, image-verified | Analysis 1.1 | KNOWN | verbatim: "Heterogeneity: Tau2=0.19; Chi2=91.35, df=34(P<0.0001); I2=62.78%" ; "Test for overall effect: Z=6.22(P<0.0001)"

### Analysis 1.3 — Exercise vs 'control', Completed intervention or control (Risk Ratio, M-H Random). 29 study rows + total. Axis: "Favours control" 0.5..2 "Favours exercise". Dichotomous cells are events/total (n/N); Mean(SD) columns not applicable.

A1.3-R01 | 1.3 | STUDY | Blumenthal 1999 | 44/55 | | 41/48 | | 0.94 | 0.79 | 1.12 | 2.96% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R02 | 1.3 | STUDY | Blumenthal 2007 | 45/51 | | 42/49 | | 1.03 | 0.88 | 1.2 | 3.99% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R03 | 1.3 | STUDY | Blumenthal 2012a | 36/37 | | 23/24 | | 1.02 | 0.92 | 1.12 | 9.36% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R04 | 1.3 | STUDY | Bonnet 2005 | 3/5 | | 4/6 | | 0.9 | 0.36 | 2.24 | 0.11% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN | CI arrow-clipped both sides in plot graphic
A1.3-R05 | 1.3 | STUDY | Chu 2008 | 15/18 | | 12/18 | | 1.25 | 0.85 | 1.84 | 0.62% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R06 | 1.3 | STUDY | Dunn 2005 | 15/16 | | 9/13 | | 1.35 | 0.92 | 1.99 | 0.63% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R07 | 1.3 | STUDY | Foley 2008 | 8/10 | | 5/13 | | 2.08 | 0.98 | 4.42 | 0.16% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN | upper CI beyond axis (arrow)
A1.3-R08 | 1.3 | STUDY | Fremont 1987 | 18/21 | | 31/40 | | 1.11 | 0.87 | 1.41 | 1.58% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN | control n/N (31/40) identical to the "Cognitive therapy" arm in Analysis 2.2 — see section 4
A1.3-R09 | 1.3 | STUDY | Gary 2010 | 20/20 | | 15/17 | | 1.13 | 0.93 | 1.38 | 2.37% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R10 | 1.3 | STUDY | Hemat-Far 2012 | 10/10 | | 10/10 | | 1 | 0.83 | 1.2 | 2.77% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN | effect prints as "1[0.83,1.2]"
A1.3-R11 | 1.3 | STUDY | Hoffman 2010 | 37/40 | | 39/40 | | 0.95 | 0.86 | 1.05 | 8.99% | 106 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R12 | 1.3 | STUDY | Klein 1985 | 15/27 | | 16/24 | | 0.83 | 0.54 | 1.29 | 0.48% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN | same n/N pair also appears in Analysis 2.2 — see section 4
A1.3-R13 | 1.3 | STUDY | Knubben 2007 | 19/20 | | 16/18 | | 1.07 | 0.88 | 1.29 | 2.51% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R14 | 1.3 | STUDY | Krogh 2009 | 48/55 | | 42/55 | | 1.14 | 0.96 | 1.37 | 2.9% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN | denominators are randomised N (55/55) vs completer N in 1.1 (48/42)
A1.3-R15 | 1.3 | STUDY | Martinsen 1985 | 20/24 | | 17/19 | | 0.93 | 0.74 | 1.18 | 1.65% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R16 | 1.3 | STUDY | Mather 2002 | 43/43 | | 42/43 | | 1.02 | 0.96 | 1.09 | 22.56% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN | largest weight in analysis
A1.3-R17 | 1.3 | STUDY | McNeil 1991 | 10/10 | | 10/10 | | 1 | 0.83 | 1.2 | 2.77% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R18 | 1.3 | STUDY | Mota-Pereira 2011 | 19/22 | | 10/11 | | 0.95 | 0.74 | 1.22 | 1.47% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R19 | 1.3 | STUDY | Mutrie 1988 | 9/9 | | 7/7 | | 1 | 0.8 | 1.26 | 1.76% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R20 | 1.3 | STUDY | Nabkasorn 2005 | 21/28 | | 28/31 | | 0.83 | 0.65 | 1.06 | 1.56% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R21 | 1.3 | STUDY | Orth 1979 | 3/3 | | 2/2 | | 1 | 0.53 | 1.87 | 0.23% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R22 | 1.3 | STUDY | Pilu 2007 | 10/10 | | 20/20 | | 1 | 0.86 | 1.16 | 4.37% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R23 | 1.3 | STUDY | Schuch 2011 | 15/15 | | 11/11 | | 1 | 0.86 | 1.16 | 4.25% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN | same RR/CI as Pilu 2007 but different weight
A1.3-R24 | 1.3 | STUDY | Shahidi 2011 | 20/23 | | 20/24 | | 1.04 | 0.82 | 1.33 | 1.61% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R25 | 1.3 | STUDY | Sims 2009 | 21/23 | | 22/22 | | 0.92 | 0.79 | 1.06 | 4.13% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R26 | 1.3 | STUDY | Singh 1997 | 17/17 | | 15/15 | | 1 | 0.89 | 1.12 | 6.66% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R27 | 1.3 | STUDY | Singh 2005 | 18/20 | | 19/20 | | 0.95 | 0.79 | 1.13 | 2.93% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R28 | 1.3 | STUDY | Veale 1992 | 36/48 | | 29/35 | | 0.91 | 0.72 | 1.13 | 1.87% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R29 | 1.3 | STUDY | Williams 2008 | 15/16 | | 20/22 | | 1.03 | 0.86 | 1.24 | 2.75% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN |
A1.3-R30 | 1.3 | OVERALL_TOTAL | Total (95% CI) | 696 | | 667 | | 1 | 0.97 | 1.04 | 100% | 107 | text layer, image-verified | Analysis 1.3 | KNOWN | 696+667=1363; "Total events: 610 (Exercise), 577 (Control)"
A1.3-R31 | 1.3 | HETEROGENEITY | Heterogeneity / test rows | | | | | | | | | 107 | text layer, image-verified | Analysis 1.3 | KNOWN | verbatim: "Heterogeneity: Tau2=0; Chi2=20.7, df=28(P=0.84); I2=0%" ; "Test for overall effect: Z=0.28(P=0.78)"

### Analysis 1.2 — Exercise vs 'control', depression symptoms follow-up (SMD, Random). 8 study rows + total. Axis: "Favours exercise" -2..2 "Favours control".

A1.2-R01 | 1.2 | STUDY | Blumenthal 1999 | 29 | 10.6 (0.8) | 29 | 11 (0.8) | -0.51 | -1.03 | 0.02 | 14.8% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN | "(0.8)" implausibly small vs post-treatment SDs (~6.9) — likely SE printed as SD; recorded verbatim. Follow-up data from separate publication (Babyak 2000, per p27)
A1.2-R02 | 1.2 | STUDY | Fremont 1987 | 13 | 7.5 (5.4) | 13 | 9.9 (7.7) | -0.35 | -1.13 | 0.43 | 9.62% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN |
A1.2-R03 | 1.2 | STUDY | Gary 2010 | 17 | 8.3 (5.2) | 14 | 8.2 (5.4) | 0.02 | -0.69 | 0.73 | 10.79% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN |
A1.2-R04 | 1.2 | STUDY | Klein 1985 | 8 | 1 (0.7) | 10 | 1.5 (0.8) | -0.57 | -1.53 | 0.38 | 7.24% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN |
A1.2-R05 | 1.2 | STUDY | Krogh 2009 | 46 | 11.9 (6.5) | 37 | 10 (5.6) | 0.31 | -0.13 | 0.74 | 17.19% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN |
A1.2-R06 | 1.2 | STUDY | Mather 2002 | 43 | 11.4 (6.7) | 43 | 13.7 (6.4) | -0.35 | -0.78 | 0.08 | 17.46% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN | largest weight
A1.2-R07 | 1.2 | STUDY | Sims 2009 | 23 | 13.8 (8) | 22 | 22.7 (11.2) | -0.9 | -1.52 | -0.29 | 12.61% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN | only study row with CI excluding 0
A1.2-R08 | 1.2 | STUDY | Singh 1997 | 15 | 13 (2.2) | 15 | 14.4 (2.2) | -0.62 | -1.35 | 0.12 | 10.29% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN | follow-up data from separate publication (Singh 2001, per p27)
A1.2-R09 | 1.2 | OVERALL_TOTAL | Total *** | 194 | | 183 | | -0.33 | -0.63 | -0.03 | 100% | 106 | text layer, image-verified | Analysis 1.2 | KNOWN | 194+183=377
A1.2-R10 | 1.2 | HETEROGENEITY | Heterogeneity / test rows | | | | | | | | | 106 | text layer, image-verified | Analysis 1.2 | KNOWN | verbatim: "Heterogeneity: Tau2=0.09; Chi2=13.65, df=7(P=0.06); I2=48.71%" ; "Test for overall effect: Z=2.18(P=0.03)"

## 3. STUDY_LABELS (truthed analyses only)

Format: label_verbatim | appears_in | source_pages

Blumenthal 1999 | 1.1, 1.2, 1.3 | 105, 106
Blumenthal 2007 | 1.1, 1.3 | 105, 106
Blumenthal 2012a | 1.1, 1.3 | 105, 106
Bonnet 2005 | 1.1, 1.3 | 105, 106
Brenes 2007 | 1.1 | 105
Chu 2008 | 1.1, 1.3 | 105, 106
Doyne 1987 | 1.1 | 105
Dunn 2005 | 1.1, 1.3 | 105, 106
Epstein 1986 | 1.1 | 105
Foley 2008 | 1.1, 1.3 | 105, 106
Fremont 1987 | 1.1, 1.2, 1.3 | 105, 106
Gary 2010 | 1.1, 1.2, 1.3 | 105, 106
Hemat-Far 2012 | 1.1, 1.3 | 105, 106
Hess-Homeier 1981 | 1.1 | 105
Hoffman 2010 | 1.1, 1.3 | 105, 106
Klein 1985 | 1.1, 1.2, 1.3 | 105, 106, 107
Knubben 2007 | 1.1, 1.3 | 105, 107
Krogh 2009 | 1.1, 1.2, 1.3 | 105, 106, 107
Martinsen 1985 | 1.1, 1.3 | 105, 107
Mather 2002 | 1.1, 1.2, 1.3 | 105, 106, 107
McNeil 1991 | 1.1, 1.3 | 105, 107
Mota-Pereira 2011 | 1.1, 1.3 | 105, 107
Mutrie 1988 | 1.1, 1.3 | 105, 107
Nabkasorn 2005 | 1.1, 1.3 | 105, 107
Orth 1979 | 1.1, 1.3 | 105, 107
Pilu 2007 | 1.1, 1.3 | 105, 107
Reuter 1984 | 1.1 | 105
Schuch 2011 | 1.1, 1.3 | 106, 107
Setaro 1985 | 1.1 | 106
Shahidi 2011 | 1.1, 1.3 | 106, 107
Sims 2009 | 1.1, 1.2, 1.3 | 106, 107
Singh 1997 | 1.1, 1.2, 1.3 | 106, 107
Singh 2005 | 1.1, 1.3 | 106, 107
Veale 1992 | 1.1, 1.3 | 106, 107
Williams 2008 | 1.1, 1.3 | 106, 107

Set relations: all 8 studies of 1.2 are a subset of 1.1's 35. 1.3's 29 studies = 1.1's 35 minus {Brenes 2007, Doyne 1987, Epstein 1986, Hess-Homeier 1981, Reuter 1984, Setaro 1985}.

## 4. CONTRADICTIONS / ODDITIES

1. Participant count for Analysis 1.1: Abstract (p5) and Effects text (p27) say "35 trials (1356 participants)"; the Comparison-1 summary table (p104), the SOF table (p7) and the forest totals (711+642) all say 1353. Internal inconsistency of 3 participants.
2. Heterogeneity qualifier inconsistency for Analysis 1.1: Abstract (p5) calls I2=63% "moderate heterogeneity"; Effects text (p27) calls the same value "substantial heterogeneity". Forest prints I2=62.78%.
3. Analysis 4.1 participant count: Effects text (p28) says "four trials (298 participants)"; Comparison-4 table (p110), Abstract ("n = 300", p5) and forest totals (153+147=300) say 300.
4. Sign typo in Comparison-6 summary table (p120): Outcome 4 effect printed as "-0.61 [1.00, -0.22]" — lower CI missing its minus sign. The Analysis 6.4 forest total (p122) prints "-0.61[-1,-0.22]".
5. Comparison-5 subgroup participant sums: outcomes 5.1-5.4 subgroup Ns each sum to 1352 (e.g. 5.1: 1080+128+144), while Analysis 1.1 and outcome 5.5 report 1353 for the same 35 trials — a 1-participant bookkeeping discrepancy inside the summary tables (p111-113).
6. Comparison 5 Outcome 5 (type of control) switches effect measure to "Mean Difference (IV, Fixed, 95% CI)" and reports an overall pooled MD (-1.57 [-1.97, -1.16]) across trials using DIFFERENT depression scales (p113); all other comparison-5 outcomes are SMD "Subtotals only". The Discussion (p29) additionally quotes these MD values as "SMD" (e.g. "SMD -3.67, 95% CI -4.94 to -2.41") — measure mislabelling in the text.
7. Multi-arm trial handling (documented, not split rows): trials with several exercise arms contribute only the largest-'dose' arm in Analysis 1.1 — "We included the arm with the smallest dose of exercise for 10 trials (Blumenthal 2007; Chu 2008; Doyne 1987; Dunn 2005; Krogh 2009; Mutrie 1988; Orth 1979; Setaro 1985; Singh 2005; Williams 2008) for which we had used the arm with the largest clinical effect in comparison 1" (p29; smallest-dose version is Analysis 6.7). No analysis truthed here splits a trial into multiple rows; instead the same trial appears across comparisons with different arms/Ns, e.g. Blumenthal 1999 is 55 vs 48 in 1.1 but 53 vs 48 (different mean: 8.2 vs 8.7) in 4.1.
8. Cross-analysis arm reuse in Analysis 1.3: Fremont 1987 "Control" is 31/40 — numerically identical to the "Cognitive therapy" arm in Analysis 2.2 (p109); Klein 1985's 15/27 vs 16/24 also appears identically in 2.2. The dichotomous "control" denominators are randomised Ns and can exceed the continuous-analysis Ns (Fremont control N=16 in 1.1 vs 40 in 1.3; Klein exercise N=14 in 1.1 vs 27 in 1.3).
9. Note (p29): the wording "arm with the largest clinical effect" conflicts with the Methods statement that the biggest 'dose' of exercise was used (Abstract p4-5); the review itself flags this in DIFFERENCES BETWEEN PROTOCOL AND REVIEW (p132).
10. Analysis 1.2 Blumenthal 1999 cell "10.6 (0.8)" / "11 (0.8)": SD implausibly small relative to the same trial's post-treatment SDs (6.9/6.5); likely an SE deposited as SD. Recorded verbatim; flagged, not corrected.
11. RevMan rounding artifacts (verbatim, not errors to fix): "Test for overall effect: Z=3.3(P=0)" (Analysis 3.1, p110); heterogeneity "df=1(P=0)" (Analysis 1.4.2, p107); RRs printed as bare "1" ("1[0.97,1.04]").
12. Typo in analysis title (verbatim): Analysis 2.2 / Comparison-2 table "Completed exercise or pyschological therapies" (p108-109). TOC also spells "subroup" for comparison-5 outcomes 2-4 (p2).
13. Stated counts vs plot rows: all three truthed analyses match exactly (35/35, 8/8, 29/29 rows). Quality-of-life trial-count wording differs: Effects text (p27) says "Five trials reported quality of life" while Comparison-1 table lists 4 studies for outcome 4 (Hoffman 2010's QoL data are not in Analysis 1.4).
14. No unreadable cells: every truthed cell resolved (certainty KNOWN throughout); nothing UNRESOLVED.

## 5. SUBSET RATIONALE

- T2 dichotomous = Analysis 1.3 (29 studies, 1363 participants): by far the largest dichotomous analysis in the review (alternatives: 2.2 with k=4, 4.2 with k=3). It maximises structural diversity vs T1: events/total (n/N) cells instead of Mean(SD), M-H weighting, a log-scaled axis (0.5-2) with arrow-clipped CIs, a "Total events" line absent from continuous forests, null pooled effect printed as bare "1", weights spanning 0.11%-22.56%, and randomised-N denominators that deliberately disagree with the completer Ns of 1.1 (a good trap for auditors). Its two-page span (p106-107) also tests row continuation across page breaks.
- T3 follow-up = Analysis 1.2 (8 studies, 377 participants): the review's only longer-term outcome analysis (the natural post-treatment vs follow-up pair with 1.1). Structural diversity: a strict subset of 1.1's studies with different Ns/means for the same labels (e.g. Blumenthal 1999: 55/48 post vs 29/29 follow-up), a different axis range (-2..2), data sourced from companion publications (Babyak 2000, Singh 2001), and a suspected SE-as-SD cell — testing whether an auditor links rather than conflates the paired analyses.
- Together with T1 (the 35-row headline SMD forest), the subset covers: continuous SMD random-effects, dichotomous RR M-H random-effects, and follow-up SMD; single-page and cross-page forests; zero and moderate heterogeneity (I2 = 0%, 48.71%, 62.78%); and the review's central published claims (headline -0.62, acceptability RR 1.00, follow-up -0.33).

## 6. META

- Citation (verbatim, p1/p4): "Cooney GM, Dwan K, Greig CA, Lawlor DA, Rimer J, Waugh FR, McMurdo M, Mead GE. Exercise for depression. Cochrane Database of Systematic Reviews 2013, Issue 9. Art. No.: CD004366. DOI: 10.1002/14651858.CD004366.pub6."
- DOI: 10.1002/14651858.CD004366.pub6 | PMC deposit: PMC9721454 | Editorial group: Cochrane Common Mental Disorders Group | Publication status: "New search for studies and content updated (no change to conclusions), published in Issue 9, 2013."
- Total PDF pages: 132. Printed-page offset: printed p.N = PDF p.N+3 (main sequence).
- Page map (truthed content): Abstract p4-5 | SOF main comparison p7-8 (SOF2 p9, SOF3 p10, SOF4 p11-12) | Figure 1 p19; Figure 2 p23; Figure 3 p24-25; Figure 4 (funnel, Analysis 1.1) p26 | Effects of interventions p27-29 | DATA AND ANALYSES p104-123: Comparison-1 summary table p104-105; Analysis 1.1 forest p105-106; Analysis 1.2 forest p106; Analysis 1.3 forest p106-107.
- Analysis inventory (every analysis the PDF lists; id | title | k studies | n participants | measure/model | pooled effect as printed; * = truthed above):
  - 1.1* | Reduction in depression symptoms post-treatment | 35 | 1353 | SMD (IV, Random, 95% CI) | -0.62 [-0.81, -0.42] | p105-106
  - 1.2* | Reduction in depression symptoms follow-up | 8 | 377 | SMD (IV, Random, 95% CI) | -0.33 [-0.63, -0.03] | p106
  - 1.3* | Completed intervention or control | 29 | 1363 | Risk Ratio (M-H, Random, 95% CI) | 1.00 [0.97, 1.04] | p106-107
  - 1.4 | Quality of life | 4 | (blank) | SMD (IV, Fixed, 95% CI) | Subtotals only — 4.1 Mental 2/59 -0.24 [-0.76, 0.29]; 4.2 Psychological 2/56 0.28 [-0.29, 0.86]; 4.3 Social 2/56 0.19 [-0.35, 0.74]; 4.4 Environment 2/56 0.62 [0.06, 1.18]; 4.5 Physical 4/115 0.45 [0.06, 0.83] | p107-108
  - 2.1 | Reduction in depression symptoms post-treatment (vs psychological therapies) | 7 | 189 | SMD (IV, Random, 95% CI) | -0.03 [-0.32, 0.26] | p108-109 (comparator column headed "Cognitive Therapy")
  - 2.2 | Completed exercise or pyschological therapies [sic] | 4 | 172 | Risk Ratio (M-H, Random, 95% CI) | 1.08 [0.95, 1.24] | p109
  - 2.3 | Quality of life (vs psychological therapies) | 1 | (blank) | Mean Difference (IV, Fixed, 95% CI) | "Totals not selected" (table prints subgroup effects as "0.0 [0.0, 0.0]"; forest rows: Physical 0.15[-7.4,7.7], Mental -0.09[-9.51,9.33], Gary 2010) | p109
  - 3.1 | Reduction in depression symptoms post-treatment (vs bright light therapy) | 1 | 18 | Mean Difference (IV, Fixed, 95% CI) | -6.4 [-10.20, -2.60] (single study: Pinchasov 2000) | p110
  - 4.1 | Reduction in depression symptoms post-treatment (vs pharmacological treatments) | 4 | 300 | SMD (IV, Random, 95% CI) | -0.11 [-0.34, 0.12] | p110
  - 4.2 | Completed exercise or antidepressants | 3 | 278 | Risk Ratio (M-H, Random, 95% CI) | 0.98 [0.86, 1.12] (note forest I2=61.09%) | p111
  - 4.3 | Quality of Life (vs pharmacological treatments) | 1 | (blank) | Mean Difference (IV, Fixed, 95% CI) | Subtotals only — Mental 1/25 -11.90 [-24.04, 0.24]; Physical 1/25 1.30 [-0.67, 3.27] (Brenes 2007) | p111
  - 5.1 | Exercise vs control subgroup analysis: type of exercise | 35 | (blank) | SMD (IV, Random, 95% CI) | Subtotals only — Aerobic 28/1080 -0.55 [-0.77, -0.34]; Mixed 3/128 -0.85 [-1.85, 0.15]; Resistance 4/144 -1.03 [-1.52, -0.53] | p113-114
  - 5.2 | Exercise vs control subroup [sic] analysis: intensity | 35 | (blank) | SMD (IV, Random, 95% CI) | Subtotals only — light/moderate 3/76 -0.83; moderate 12/343 -0.64; hard 11/595 -0.56; vigorous 5/230 -0.77; Moderate/hard 2/66 -0.63; Moderate/vigorous 2/42 -0.38 | p114-116
  - 5.3 | Exercise vs control subroup analysis: number of sessions | 35 | (blank) | SMD (IV, Random, 95% CI) | Subtotals only — 0-12: 5/195 -0.42; 13-24: 9/296 -0.70; 25-36: 8/264 -0.80; 37+: 10/524 -0.46; unclear 3/73 -0.89 | p116-117
  - 5.4 | Exercise vs control subroup analysis: diagnosis of depression | 35 | (blank) | SMD (IV, Random, 95% CI) | Subtotals only — clinical diagnosis 23/967 -0.57; cut points on a scale 11/367 -0.67; unclear 1/18 -2.00 | p117-118
  - 5.5 | Exercise vs control subgroup analysis: type of control | 35 | 1353 | Mean Difference (IV, Fixed, 95% CI) | -1.57 [-1.97, -1.16] — placebo 2/156 -2.66; no treatment/waiting list/usual care/self monitoring 17/563 -4.75; exercise plus treatment vs treatment 6/225 -1.22; stretching/meditation/relaxation 6/219 -0.09; occupational/health education/casual conversation 4/190 -3.67 | p118-120
  - 6.1 | Sensitivity: peer-reviewed journal publications and doctoral theses only | 34 | 1335 | SMD (IV, Random, 95% CI) | -0.59 [-0.78, -0.40] | p120-121
  - 6.2 | Sensitivity: studies published as abstracts or conference proceedings only | 1 | 18 | SMD (IV, Random, 95% CI) | -2.00 [-3.19, -0.82] | p121
  - 6.3 | Sensitivity: studies with adequate allocation concealment | 14 | 829 | SMD (IV, Random, 95% CI) | -0.49 [-0.75, -0.24] | p121-122
  - 6.4 | Sensitivity: studies using intention-to-treat analysis | 11 | 567 | SMD (IV, Random, 95% CI) | table prints "-0.61 [1.00, -0.22]" [sic — sign typo]; forest total -0.61[-1,-0.22] | p122
  - 6.5 | Sensitivity: studies with blinded outcome assessment | 12 | 658 | SMD (IV, Random, 95% CI) | -0.36 [-0.60, -0.12] | p122-123
  - 6.6 | Sensitivity: allocation concealment, intention-to-treat, blinded outcome | 6 | 464 | SMD (IV, Random, 95% CI) | -0.18 [-0.47, 0.11] | p123
  - 6.7 | Sensitivity: Lowest dose of exercise | 35 | 1347 | SMD (IV, Fixed, 95% CI) | -0.44 [-0.55, -0.33] | p123
- Comparison-level summary tables ("Outcome or subgroup title | No. of studies | No. of participants | Statistical method | Effect size"): Comparison 1 p104-105; Comparison 2 p108; Comparison 3 p109; Comparison 4 p110; Comparison 5 p111-113; Comparison 6 p120.
- Trials included in review but NOT in any meta-analysis: Greist 1979; McCann 1984 (p27).
