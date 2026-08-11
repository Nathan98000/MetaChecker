# Pass B — Independent gold-standard truth extraction
# Cooney 2013 "Exercise for depression" (PMC9721454.pdf)
# Extracted 2026-08-11. All strings VERBATIM from the PDF text layer unless noted.
# Page references: "PDF pN" = 1-based page of this PDF file; "printed N" = folio number in the page footer (offset: PDF = printed + 3 for body pages).

## 0. DOCUMENT SURVEY (pages 1-20 + full scan)

- PDF: 132 pages total. Text layer is present and clean throughout (extraction via PyMuPDF; no OCR needed).
- p1: title page. p2-3: TABLE OF CONTENTS (printed i-ii) including the full "Data and analyses" listing (23 analyses across 6 comparisons).
- p4-6: Abstract + Plain language summary (printed 1-3). p7-12: Summary of findings tables 1-4 (printed 4-9).
- Figures (raster/vector images with caption text): Figure 1 study flow diagram (PDF p19, printed 16); Figure 2 'Risk of bias' graph (PDF p23, printed 20); Figure 3 'Risk of bias' summary (PDF p24, printed 21); Figure 4 funnel plot of Analysis 1.1 (PDF p26, printed 23). These four figures are IMAGES; their numeric content is not in the text layer.
- DATA AND ANALYSES section: PDF p104-124 (printed 101-121). IMPORTANT: this PMC deposit does NOT omit the analysis forests. Every one of the 23 analyses listed in the TOC is present as a RevMan-style forest table whose cell values (N, Mean(SD) or n/N, weight, effect [CI], heterogeneity, Z) are in the TEXT LAYER; only the graphical squares/CI whiskers are drawn graphics. Axis tick labels ("Favours exercise 5 2.5 -5 -2.5 0 Favours control") appear in scrambled order in the text layer — a text-extraction ordering artifact, not a content defect.
- No forest plot appears in the main "Figures" series; forests exist only as Analysis tables.
- Comparison summary tables (Outcome or subgroup title | No. of studies | No. of participants | Statistical method | Effect size) precede each comparison's forests: Comp 1 p104-105, Comp 2 p108, Comp 3 p110, Comp 4 p110, Comp 5 p111-113, Comp 6 p120.

## 1. ANALYSES (truthed targets)

Format: analysis_id | outcome | comparison | subgroup | effect_measure | model | n_studies | n_participants | pooled_effect | ci_lower | ci_upper | i2 | p_or_z | source_page (PDF, 1-based) | source

A1 | Reduction in depression symptoms post-treatment | Exercise versus 'control' | (none; flat) | Std. Mean Difference (IV, Random, 95% CI) | Random | 35 | 1353 | -0.62 | -0.81 | -0.42 | 62.78% | Z=6.22(P<0.0001) | 104-106 | Comparison 1 summary table (p104, printed 101: "35 | 1353 | Std. Mean Difference (IV, Random, 95% CI) | -0.62 [-0.81, -0.42]") + Analysis 1.1 forest table (p105-106, printed 102-103); Heterogeneity line verbatim: "Heterogeneity: Tau2=0.19; Chi2=91.35, df=34(P<0.0001); I2=62.78%"

A2 | Reduction in depression symptoms follow-up | Exercise versus 'control' | (none; flat) | Std. Mean Difference (IV, Random, 95% CI) | Random | 8 | 377 | -0.33 | -0.63 | -0.03 | 48.71% | Z=2.18(P=0.03) | 105-106 | Comparison 1 summary table (p105, printed 102: "8 | 377 | Std. Mean Difference (IV, Random, 95% CI) | -0.33 [-0.63, -0.03]") + Analysis 1.2 forest table (p106, printed 103); Heterogeneity line verbatim: "Heterogeneity: Tau2=0.09; Chi2=13.65, df=7(P=0.06); I2=48.71%"

A3 | Completed intervention or control | Exercise versus 'control' | (none; flat) | Risk Ratio (M-H, Random, 95% CI) | Random | 29 | 1363 | 1.00 | 0.97 | 1.04 | 0% | Z=0.28(P=0.78) | 105-107 | Comparison 1 summary table (p105, printed 102: "29 | 1363 | Risk Ratio (M-H, Random, 95% CI) | 1.00 [0.97, 1.04]") + Analysis 1.3 forest table (p106-107, printed 103-104); forest pooled row verbatim "1[0.97,1.04]"; Heterogeneity line verbatim: "Heterogeneity: Tau2=0; Chi2=20.7, df=28(P=0.84); I2=0%"; "Total events: 610 (Exercise), 577 (Control)"

### Review-level summary numbers (verbatim quotes)
- Abstract, Main results (PDF p5, printed 2): "Thirty-nine trials (2326 participants) fulfilled our inclusion criteria, of which 37 provided data for meta-analyses."
- Abstract (PDF p5): "For the 35 trials (1356 participants) comparing exercise with no treatment or a control intervention, the pooled SMD for the primary outcome of depression at the end of treatment was -0.62 (95% confidence interval (CI) -0.81 to -0.42)... There was moderate heterogeneity (I2 = 63%)."
- Abstract (PDF p5): "the six trials (464 participants) with adequate allocation concealment, intention-to-treat analysis and blinded outcome assessment, the pooled SMD for this outcome was not statistically significant (-0.18, 95% CI -0.47 to 0.11)."
- Abstract (PDF p5): "eight trials (377 participants) providing long-term follow-up data on mood found a small effect in favour of exercise (SMD -0.33, 95% CI -0.63 to -0.03)."
- Abstract (PDF p5): "For acceptability of treatment (assessed by number of drop-outs during the intervention), the risk ratio was 1.00 (95% CI 0.97 to 1.04)."
- Abstract (PDF p5): "Seven trials compared exercise with psychological therapy (189 participants)... (SMD -0.03, 95% CI -0.32 to 0.26). Four trials (n = 300) compared exercise with pharmacological treatment and found no significant difference (SMD -0.11, -0.34, 0.12). One trial (n = 18) reported that exercise was more effective than bright light therapy (MD -6.40, 95% CI -10.20 to -2.60)."
- Results text (PDF p27, printed 24): "We included 37 trials in our meta-analyses. The remaining two trials could not be included... (Greist 1979; McCann 1984)." / "Thirty-five trials (1356 participants) included a comparison of exercise with a 'control' intervention." / "There was substantial heterogeneity (I2 = 63%)." / "Twenty-nine studies (1363 participants) reported how many completed the exercise and control arms (Analysis 1.3). The risk ratio (RR) was 1.00 (95% CI 0.97 to 1.04)."
- Summary of findings table 1 (PDF p7, printed 4): symptoms of depression post-treatment "1353 (35 studies)", "SMD -0.62 (95% CI: -0.81 to -0.42)"; long-term "377 (8 studies)", "SMD -0.33 (95% CI: -0.63 to -0.03)"; adverse events "0 (6 studies)" [row truncated at page break in extraction].
- Publication bias (PDF p26, printed 23): "There is evidence of bias (Begg P value = 0.02, Egger P value = 0.002) (funnel plot for Analysis 1.1, exercise versus control, Figure 4)".

## 2. PUBLISHED_EFFECTS

Format: effect_id | analysis_id | row_kind | study_label | n_treatment | mean_sd_treatment | n_control | mean_sd_control | effect | ci_lower | ci_upper | weight_pct | source_page | source_type | figure_or_analysis_ref | certainty | note

### Analysis 1.1 — Exercise versus 'control', Reduction in depression symptoms post-treatment (SMD, IV Random). Column header verbatim: "Study or subgroup | Exercise | Control | Std. Mean Difference | Weight | Std. Mean Difference / N | Mean(SD) | N | Mean(SD) | Random, 95% CI | | Random, 95% CI"

E1.1-01 | A1 | STUDY | Blumenthal 1999 | 55 | 8.7 (6.9) | 48 | 7.8 (6.5) | 0.14 | -0.25 | 0.52 | 4.23% | 105 | text layer | Analysis 1.1 | KNOWN | effect cell verbatim "0.14[-0.25,0.52]"
E1.1-02 | A1 | STUDY | Blumenthal 2007 | 51 | 9.2 (6.1) | 49 | 11.1 (7) | -0.29 | -0.68 | 0.11 | 4.21% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-03 | A1 | STUDY | Blumenthal 2012a | 35 | 6.4 (5.3) | 21 | 10 (5.3) | -0.67 | -1.23 | -0.12 | 3.59% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-04 | A1 | STUDY | Bonnet 2005 | 5 | 24.5 (10.9) | 6 | 10.5 (5.8) | 1.51 | 0.09 | 2.93 | 1.37% | 105 | text layer | Analysis 1.1 | KNOWN | only strongly positive (favours control) study row
E1.1-05 | A1 | STUDY | Brenes 2007 | 14 | 7.8 (4.3) | 12 | 10.9 (5.8) | -0.6 | -1.39 | 0.2 | 2.77% | 105 | text layer | Analysis 1.1 | KNOWN | effect cell verbatim "-0.6[-1.39,0.2]"
E1.1-06 | A1 | STUDY | Chu 2008 | 15 | 5.8 (3.4) | 12 | 10.6 (5.7) | -1.02 | -1.84 | -0.21 | 2.69% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-07 | A1 | STUDY | Doyne 1987 | 14 | 8.2 (5.3) | 11 | 15.3 (6.3) | -1.19 | -2.06 | -0.32 | 2.53% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-08 | A1 | STUDY | Dunn 2005 | 16 | 10 (5.5) | 13 | 14 (4.9) | -0.74 | -1.5 | 0.02 | 2.87% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-09 | A1 | STUDY | Epstein 1986 | 7 | 9 (10.9) | 10 | 16.3 (7.4) | -0.77 | -1.78 | 0.24 | 2.15% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-10 | A1 | STUDY | Foley 2008 | 8 | 10.8 (9.3) | 5 | 13.6 (10.2) | -0.27 | -1.4 | 0.85 | 1.89% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-11 | A1 | STUDY | Fremont 1987 | 18 | 10 (9.8) | 16 | 8 (7.1) | 0.23 | -0.45 | 0.9 | 3.15% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-12 | A1 | STUDY | Gary 2010 | 20 | 8.4 (5.6) | 15 | 9.3 (4.9) | -0.17 | -0.84 | 0.51 | 3.17% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-13 | A1 | STUDY | Hemat-Far 2012 | 10 | 16.6 (6.9) | 10 | 22.8 (4.9) | -0.99 | -1.93 | -0.05 | 2.32% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-14 | A1 | STUDY | Hess-Homeier 1981 | 5 | 9.8 (6.9) | 6 | 16.2 (8.4) | -0.75 | -2 | 0.5 | 1.64% | 105 | text layer | Analysis 1.1 | KNOWN | CI lower verbatim "-2" (no decimals)
E1.1-15 | A1 | STUDY | Hoffman 2010 | 37 | 16.4 (10.2) | 39 | 21.2 (12) | -0.43 | -0.88 | 0.03 | 3.98% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-16 | A1 | STUDY | Klein 1985 | 14 | 1 (0.9) | 8 | 0.8 (0.5) | 0.24 | -0.64 | 1.11 | 2.52% | 105 | text layer | Analysis 1.1 | KNOWN | scale magnitude differs from other rows (score ~1)
E1.1-17 | A1 | STUDY | Knubben 2007 | 20 | 11.2 (4) | 18 | 15.5 (6.1) | -0.83 | -1.49 | -0.16 | 3.19% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-18 | A1 | STUDY | Krogh 2009 | 48 | 12.1 (6.4) | 42 | 10.6 (5.6) | 0.25 | -0.17 | 0.66 | 4.13% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-19 | A1 | STUDY | Martinsen 1985 | 24 | 12.1 (7.1) | 19 | 22.8 (11.4) | -1.14 | -1.79 | -0.48 | 3.24% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-20 | A1 | STUDY | Mather 2002 | 43 | 12.6 (7) | 43 | 13.7 (6) | -0.17 | -0.59 | 0.26 | 4.1% | 105 | text layer | Analysis 1.1 | KNOWN | weight verbatim "4.1%" (one decimal)
E1.1-21 | A1 | STUDY | McNeil 1991 | 10 | 11.1 (3) | 10 | 14.7 (3.7) | -1.02 | -1.97 | -0.08 | 2.31% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-22 | A1 | STUDY | Mota-Pereira 2011 | 19 | 12.5 (1.7) | 10 | 13.6 (1.3) | -0.67 | -1.46 | 0.12 | 2.77% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-23 | A1 | STUDY | Mutrie 1988 | 9 | 9.5 (4.3) | 7 | 21.4 (5.3) | -2.39 | -3.76 | -1.02 | 1.44% | 105 | text layer | Analysis 1.1 | KNOWN | largest effect magnitude in plot
E1.1-24 | A1 | STUDY | Nabkasorn 2005 | 21 | 14.4 (4.1) | 28 | 17.5 (4.2) | -0.73 | -1.31 | -0.14 | 3.48% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-25 | A1 | STUDY | Orth 1979 | 3 | 7 (6.6) | 2 | 16.5 (2.1) | -1.25 | -3.71 | 1.21 | 0.56% | 105 | text layer | Analysis 1.1 | KNOWN | smallest trial (n=5 total)
E1.1-26 | A1 | STUDY | Pilu 2007 | 10 | 8.1 (5.2) | 20 | 16.7 (9.1) | -1.04 | -1.85 | -0.23 | 2.71% | 105 | text layer | Analysis 1.1 | KNOWN |
E1.1-27 | A1 | STUDY | Reuter 1984 | 9 | 5.1 (4.8) | 9 | 18.6 (7.7) | -2 | -3.19 | -0.82 | 1.77% | 105 | text layer | Analysis 1.1 | KNOWN | effect verbatim "-2[-3.19,-0.82]"
E1.1-28 | A1 | STUDY | Schuch 2011 | 15 | 5.9 (4.5) | 11 | 9.5 (3.6) | -0.83 | -1.65 | -0.01 | 2.69% | 106 | text layer | Analysis 1.1 | KNOWN | row continues on next PDF page
E1.1-29 | A1 | STUDY | Setaro 1985 | 25 | 62 (6.5) | 25 | 69.9 (4) | -1.44 | -2.07 | -0.81 | 3.33% | 106 | text layer | Analysis 1.1 | KNOWN | mean magnitude ~62-70 (different scale)
E1.1-30 | A1 | STUDY | Shahidi 2011 | 20 | 11.1 (6.2) | 20 | 15.2 (6.1) | -0.65 | -1.29 | -0.02 | 3.29% | 106 | text layer | Analysis 1.1 | KNOWN |
E1.1-31 | A1 | STUDY | Sims 2009 | 23 | 15.1 (8.5) | 22 | 20.6 (11.8) | -0.53 | -1.12 | 0.07 | 3.45% | 106 | text layer | Analysis 1.1 | KNOWN |
E1.1-32 | A1 | STUDY | Singh 1997 | 17 | 9.8 (2.4) | 15 | 13.8 (2) | -1.75 | -2.59 | -0.92 | 2.64% | 106 | text layer | Analysis 1.1 | KNOWN |
E1.1-33 | A1 | STUDY | Singh 2005 | 18 | 8.5 (5.5) | 19 | 14.4 (6) | -1 | -1.69 | -0.31 | 3.11% | 106 | text layer | Analysis 1.1 | KNOWN | effect verbatim "-1[-1.69,-0.31]"
E1.1-34 | A1 | STUDY | Veale 1992 | 36 | 13.9 (12.8) | 29 | 17.8 (10.2) | -0.33 | -0.82 | 0.17 | 3.84% | 106 | text layer | Analysis 1.1 | KNOWN |
E1.1-35 | A1 | STUDY | Williams 2008 | 17 | 8.4 (5.8) | 12 | 11.8 (8.1) | -0.48 | -1.23 | 0.27 | 2.9% | 106 | text layer | Analysis 1.1 | KNOWN | weight verbatim "2.9%"
E1.1-36 | A1 | OVERALL_TOTAL | Total *** | 711 | (blank) | 642 | (blank) | -0.62 | -0.81 | -0.42 | 100% | 106 | text layer | Analysis 1.1 | KNOWN | row label verbatim "Total ***"; effect cell verbatim "-0.62[-0.81,-0.42]"
E1.1-37 | A1 | HETEROGENEITY | (heterogeneity/overall-test lines) | | | | | | | | | 106 | text layer | Analysis 1.1 | KNOWN | verbatim: "Heterogeneity: Tau2=0.19; Chi2=91.35, df=34(P<0.0001); I2=62.78%" and "Test for overall effect: Z=6.22(P<0.0001)"

Row count check: 35 STUDY rows; sum N_treatment = 711, sum N_control = 642 (matches Total row); 711+642 = 1353 (matches comparison table and SoF, NOT abstract's 1356 — see oddity O1).

### Analysis 1.2 — Exercise versus 'control', Reduction in depression symptoms follow-up (SMD, IV Random) — chosen FOLLOW-UP analysis (T3)

E1.2-01 | A2 | STUDY | Blumenthal 1999 | 29 | 10.6 (0.8) | 29 | 11 (0.8) | -0.51 | -1.03 | 0.02 | 14.8% | 106 | text layer | Analysis 1.2 | KNOWN | follow-up N (29) differs from post-treatment N (55/48); data from separate publication Babyak 2000 per results text p27
E1.2-02 | A2 | STUDY | Fremont 1987 | 13 | 7.5 (5.4) | 13 | 9.9 (7.7) | -0.35 | -1.13 | 0.43 | 9.62% | 106 | text layer | Analysis 1.2 | KNOWN |
E1.2-03 | A2 | STUDY | Gary 2010 | 17 | 8.3 (5.2) | 14 | 8.2 (5.4) | 0.02 | -0.69 | 0.73 | 10.79% | 106 | text layer | Analysis 1.2 | KNOWN |
E1.2-04 | A2 | STUDY | Klein 1985 | 8 | 1 (0.7) | 10 | 1.5 (0.8) | -0.57 | -1.53 | 0.38 | 7.24% | 106 | text layer | Analysis 1.2 | KNOWN |
E1.2-05 | A2 | STUDY | Krogh 2009 | 46 | 11.9 (6.5) | 37 | 10 (5.6) | 0.31 | -0.13 | 0.74 | 17.19% | 106 | text layer | Analysis 1.2 | KNOWN |
E1.2-06 | A2 | STUDY | Mather 2002 | 43 | 11.4 (6.7) | 43 | 13.7 (6.4) | -0.35 | -0.78 | 0.08 | 17.46% | 106 | text layer | Analysis 1.2 | KNOWN |
E1.2-07 | A2 | STUDY | Sims 2009 | 23 | 13.8 (8) | 22 | 22.7 (11.2) | -0.9 | -1.52 | -0.29 | 12.61% | 106 | text layer | Analysis 1.2 | KNOWN | effect verbatim "-0.9[-1.52,-0.29]"
E1.2-08 | A2 | STUDY | Singh 1997 | 15 | 13 (2.2) | 15 | 14.4 (2.2) | -0.62 | -1.35 | 0.12 | 10.29% | 106 | text layer | Analysis 1.2 | KNOWN | follow-up data from separate publication Singh 2001 per results text p27
E1.2-09 | A2 | OVERALL_TOTAL | Total *** | 194 | (blank) | 183 | (blank) | -0.33 | -0.63 | -0.03 | 100% | 106 | text layer | Analysis 1.2 | KNOWN | effect cell verbatim "-0.33[-0.63,-0.03]"
E1.2-10 | A2 | HETEROGENEITY | (heterogeneity/overall-test lines) | | | | | | | | | 106 | text layer | Analysis 1.2 | KNOWN | verbatim: "Heterogeneity: Tau2=0.09; Chi2=13.65, df=7(P=0.06); I2=48.71%" and "Test for overall effect: Z=2.18(P=0.03)"

Row count check: 8 STUDY rows; 194+183 = 377 (matches comparison table, abstract, SoF).

### Analysis 1.3 — Exercise versus 'control', Completed intervention or control (Risk Ratio, M-H Random) — chosen DICHOTOMOUS analysis (T2). Column header verbatim: "Study or subgroup | Exercise | Control | Risk Ratio | Weight | Risk Ratio / n/N | n/N | M-H, Random, 95% CI | | M-H, Random, 95% CI". mean_sd columns not applicable; n columns below hold verbatim "n/N" cells.

E1.3-01 | A3 | STUDY | Blumenthal 1999 | 44/55 | n/a | 41/48 | n/a | 0.94 | 0.79 | 1.12 | 2.96% | 106 | text layer | Analysis 1.3 | KNOWN |
E1.3-02 | A3 | STUDY | Blumenthal 2007 | 45/51 | n/a | 42/49 | n/a | 1.03 | 0.88 | 1.2 | 3.99% | 106 | text layer | Analysis 1.3 | KNOWN | CI upper verbatim "1.2"
E1.3-03 | A3 | STUDY | Blumenthal 2012a | 36/37 | n/a | 23/24 | n/a | 1.02 | 0.92 | 1.12 | 9.36% | 106 | text layer | Analysis 1.3 | KNOWN | control denominator 24 (vs 21 analysed in A1.1)
E1.3-04 | A3 | STUDY | Bonnet 2005 | 3/5 | n/a | 4/6 | n/a | 0.9 | 0.36 | 2.24 | 0.11% | 106 | text layer | Analysis 1.3 | KNOWN |
E1.3-05 | A3 | STUDY | Chu 2008 | 15/18 | n/a | 12/18 | n/a | 1.25 | 0.85 | 1.84 | 0.62% | 106 | text layer | Analysis 1.3 | KNOWN |
E1.3-06 | A3 | STUDY | Dunn 2005 | 15/16 | n/a | 9/13 | n/a | 1.35 | 0.92 | 1.99 | 0.63% | 106 | text layer | Analysis 1.3 | KNOWN |
E1.3-07 | A3 | STUDY | Foley 2008 | 8/10 | n/a | 5/13 | n/a | 2.08 | 0.98 | 4.42 | 0.16% | 106 | text layer | Analysis 1.3 | KNOWN | widest CI in plot
E1.3-08 | A3 | STUDY | Fremont 1987 | 18/21 | n/a | 31/40 | n/a | 1.11 | 0.87 | 1.41 | 1.58% | 106 | text layer | Analysis 1.3 | KNOWN | control denominator 40 vs 16 analysed in A1.1 (multi-arm trial; comparator arms pooled for completion — see O4)
E1.3-09 | A3 | STUDY | Gary 2010 | 20/20 | n/a | 15/17 | n/a | 1.13 | 0.93 | 1.38 | 2.37% | 106 | text layer | Analysis 1.3 | KNOWN |
E1.3-10 | A3 | STUDY | Hemat-Far 2012 | 10/10 | n/a | 10/10 | n/a | 1 | 0.83 | 1.2 | 2.77% | 106 | text layer | Analysis 1.3 | KNOWN | effect verbatim "1[0.83,1.2]"
E1.3-11 | A3 | STUDY | Hoffman 2010 | 37/40 | n/a | 39/40 | n/a | 0.95 | 0.86 | 1.05 | 8.99% | 106 | text layer | Analysis 1.3 | KNOWN |
E1.3-12 | A3 | STUDY | Klein 1985 | 15/27 | n/a | 16/24 | n/a | 0.83 | 0.54 | 1.29 | 0.48% | 107 | text layer | Analysis 1.3 | KNOWN | denominators are randomised totals across arms (27/24) vs analysed 14/8 in A1.1 — see O4
E1.3-13 | A3 | STUDY | Knubben 2007 | 19/20 | n/a | 16/18 | n/a | 1.07 | 0.88 | 1.29 | 2.51% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-14 | A3 | STUDY | Krogh 2009 | 48/55 | n/a | 42/55 | n/a | 1.14 | 0.96 | 1.37 | 2.9% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-15 | A3 | STUDY | Martinsen 1985 | 20/24 | n/a | 17/19 | n/a | 0.93 | 0.74 | 1.18 | 1.65% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-16 | A3 | STUDY | Mather 2002 | 43/43 | n/a | 42/43 | n/a | 1.02 | 0.96 | 1.09 | 22.56% | 107 | text layer | Analysis 1.3 | KNOWN | largest weight (22.56%)
E1.3-17 | A3 | STUDY | McNeil 1991 | 10/10 | n/a | 10/10 | n/a | 1 | 0.83 | 1.2 | 2.77% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-18 | A3 | STUDY | Mota-Pereira 2011 | 19/22 | n/a | 10/11 | n/a | 0.95 | 0.74 | 1.22 | 1.47% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-19 | A3 | STUDY | Mutrie 1988 | 9/9 | n/a | 7/7 | n/a | 1 | 0.8 | 1.26 | 1.76% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-20 | A3 | STUDY | Nabkasorn 2005 | 21/28 | n/a | 28/31 | n/a | 0.83 | 0.65 | 1.06 | 1.56% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-21 | A3 | STUDY | Orth 1979 | 3/3 | n/a | 2/2 | n/a | 1 | 0.53 | 1.87 | 0.23% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-22 | A3 | STUDY | Pilu 2007 | 10/10 | n/a | 20/20 | n/a | 1 | 0.86 | 1.16 | 4.37% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-23 | A3 | STUDY | Schuch 2011 | 15/15 | n/a | 11/11 | n/a | 1 | 0.86 | 1.16 | 4.25% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-24 | A3 | STUDY | Shahidi 2011 | 20/23 | n/a | 20/24 | n/a | 1.04 | 0.82 | 1.33 | 1.61% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-25 | A3 | STUDY | Sims 2009 | 21/23 | n/a | 22/22 | n/a | 0.92 | 0.79 | 1.06 | 4.13% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-26 | A3 | STUDY | Singh 1997 | 17/17 | n/a | 15/15 | n/a | 1 | 0.89 | 1.12 | 6.66% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-27 | A3 | STUDY | Singh 2005 | 18/20 | n/a | 19/20 | n/a | 0.95 | 0.79 | 1.13 | 2.93% | 107 | text layer | Analysis 1.3 | KNOWN |
E1.3-28 | A3 | STUDY | Veale 1992 | 36/48 | n/a | 29/35 | n/a | 0.91 | 0.72 | 1.13 | 1.87% | 107 | text layer | Analysis 1.3 | KNOWN | control denominator 35 vs 29 analysed in A1.1
E1.3-29 | A3 | STUDY | Williams 2008 | 15/16 | n/a | 20/22 | n/a | 1.03 | 0.86 | 1.24 | 2.75% | 107 | text layer | Analysis 1.3 | KNOWN | control denominator 22 vs 12 analysed in A1.1
E1.3-30 | A3 | OVERALL_TOTAL | Total (95% CI) | 696 | n/a | 667 | n/a | 1 | 0.97 | 1.04 | 100% | 107 | text layer | Analysis 1.3 | KNOWN | row label verbatim "Total (95% CI)" (note: differs from "Total ***" used in continuous analyses); effect cell verbatim "1[0.97,1.04]"; "Total events: 610 (Exercise), 577 (Control)"
E1.3-31 | A3 | HETEROGENEITY | (heterogeneity/overall-test lines) | | | | | | | | | 107 | text layer | Analysis 1.3 | KNOWN | verbatim: "Heterogeneity: Tau2=0; Chi2=20.7, df=28(P=0.84); I2=0%" and "Test for overall effect: Z=0.28(P=0.78)"

Row count check: 29 STUDY rows; denominators sum 696 (Exercise) + 667 (Control) = 1363 (matches comparison table and results text); numerators sum 610 + 577 (matches "Total events" line).

Note on source_type: all cells above come from the PDF TEXT LAYER (RevMan forest tables are typeset text with graphical overlays); no page-image OCR was needed for any truthed cell.

## 3. STUDY_LABELS (union across truthed analyses; appears_in coded A1=Analysis 1.1, A2=Analysis 1.2, A3=Analysis 1.3)

Format: label_verbatim | appears_in | source_pages (PDF)

Blumenthal 1999 | A1, A2, A3 | 105, 106
Blumenthal 2007 | A1, A3 | 105, 106
Blumenthal 2012a | A1, A3 | 105, 106
Bonnet 2005 | A1, A3 | 105, 106
Brenes 2007 | A1 | 105
Chu 2008 | A1, A3 | 105, 106
Doyne 1987 | A1 | 105
Dunn 2005 | A1, A3 | 105, 106
Epstein 1986 | A1 | 105
Foley 2008 | A1, A3 | 105, 106
Fremont 1987 | A1, A2, A3 | 105, 106
Gary 2010 | A1, A2, A3 | 105, 106
Hemat-Far 2012 | A1, A3 | 105, 106
Hess-Homeier 1981 | A1 | 105
Hoffman 2010 | A1, A3 | 105, 106
Klein 1985 | A1, A2, A3 | 105, 106, 107
Knubben 2007 | A1, A3 | 105, 107
Krogh 2009 | A1, A2, A3 | 105, 106, 107
Martinsen 1985 | A1, A3 | 105, 107
Mather 2002 | A1, A2, A3 | 105, 106, 107
McNeil 1991 | A1, A3 | 105, 107
Mota-Pereira 2011 | A1, A3 | 105, 107
Mutrie 1988 | A1, A3 | 105, 107
Nabkasorn 2005 | A1, A3 | 105, 107
Orth 1979 | A1, A3 | 105, 107
Pilu 2007 | A1, A3 | 105, 107
Reuter 1984 | A1 | 105
Schuch 2011 | A1, A3 | 106, 107
Setaro 1985 | A1 | 106
Shahidi 2011 | A1, A3 | 106, 107
Sims 2009 | A1, A2, A3 | 106, 107
Singh 1997 | A1, A2, A3 | 106, 107
Singh 2005 | A1, A3 | 106, 107
Veale 1992 | A1, A3 | 106, 107
Williams 2008 | A1, A3 | 106, 107

(35 labels total. A2 subset: 8 labels. A3 subset: 29 labels = A1 minus {Brenes 2007, Doyne 1987, Epstein 1986, Hess-Homeier 1981, Reuter 1984, Setaro 1985}.)

## 4. CONTRADICTIONS / ODDITIES

O1. PARTICIPANT-COUNT MISMATCH for the primary analysis: Abstract (PDF p5) and Results text (PDF p27) say "35 trials (1356 participants)", but the Analysis 1.1 forest totals are 711 + 642 = 1353, the Comparison 1 summary table says 1353, and Summary of findings table 1 says "1353 (35 studies)". 1356 vs 1353 — internal inconsistency of 3 participants (likely 1356 = randomised into the relevant arms vs 1353 analysed; the review does not reconcile this).
O2. CI SIGN TYPO in Comparison 6 summary table (PDF p120, printed 117): Outcome 4 (ITT-only sensitivity) effect size printed as "-0.61 [1.00, -0.22]" — lower bound printed as "1.00" where it must be "-1.00" (abstract-consistent value not stated there; clearly a dropped minus sign). Recorded verbatim; do not silently correct.
O3. Comparison 5, Outcome 5 ("type of control", PDF p113, printed 110): statistical method printed as "Mean Difference (IV, Fixed, 95% CI)" with pooled -1.57 [-1.97, -1.16] over 35 studies / 1353 participants, although every other reduction-in-symptoms analysis (including its own parent outcome) uses Std. Mean Difference with a Random model. A fixed-effect MD pooled across different depression scales is a methodological oddity of the published review (and the SMD-vs-MD switch is undocumented in the text near it). Not truthed row-by-row, but flagged for the inventory.
O4. MULTI-ARM SPLIT / DENOMINATOR SHIFTS between Analysis 1.1 and Analysis 1.3 for the same trials: A1.1 uses analysed-participant Ns while A1.3 uses randomised denominators, and for multi-arm trials A1.3 pools comparator arms into "Control". Examples (A1.1 N exercise/control -> A1.3 n/N): Klein 1985 14/8 -> 15/27 vs 16/24 (three-arm trial; denominators exceed the two-arm analysed Ns); Fremont 1987 18/16 -> 18/21 vs 31/40 (control denominator 40 spans multiple comparator arms — cf. Fremont CT arm N=16 in Analysis 2.1); Veale 1992 36/29 -> 36/48 vs 29/35; Williams 2008 17/12 -> 15/16 vs 20/22; Blumenthal 2012a control 21 -> 23/24. Interpretation of exactly which arms were pooled is AMBIGUOUS from the plot alone (cells themselves are KNOWN/verbatim).
O5. Doyne 1987 is quoted in the Results text (PDF p27) as having "42% completion", yet Doyne 1987 does NOT appear as a row in Analysis 1.3 (completion analysis). Likewise Brenes 2007, Epstein 1986, Hess-Homeier 1981, Reuter 1984, Setaro 1985 are in A1.1 but absent from A1.3; the review's stated count "Twenty-nine studies (1363 participants)" matches the 29 plot rows, so this is a documented exclusion, not a row/count contradiction — but the Doyne text mention alongside its absence from the plot is an internal oddity.
O6. Krogh 2009 is a multi-arm (aerobic + strength) trial; A1.1 shows a single exercise arm N=48 (review policy: biggest 'dose' of exercise, per Abstract p4-5). A1.3 exercise denominator is 55. Which arm(s) constitute the 48/55 completion cell is not stated at the plot — AMBIGUOUS interpretation, verbatim cell KNOWN.
O7. Blumenthal 1999 follow-up row (A1.2) shows Mean(SD) "10.6 (0.8)" / "11 (0.8)" — SDs an order of magnitude smaller than its post-treatment SDs (6.9/6.5); the CI (-1.03 to 0.02) is consistent with the printed cells, but the SD=0.8 values look like SEs from the Babyak 2000 publication. Recorded verbatim; flag for checker as a plausible source-data oddity of the review itself.
O8. Text-layer axis artifacts: forest-plot axis tick labels extract in scrambled order (e.g. "Favours exercise 5 2.5 -5 -2.5 0 Favours control" for A1.1/A1.2; "Favours control 2 0.5 1.5 0.7 1 Favours exercise" for A1.3). This is an extraction-order artifact of the graphic labels, not tabular data; no truthed cell is affected.
O9. Row-label formatting inconsistency within the same PDF: continuous analyses use pooled-row label "Total ***" while dichotomous analyses use "Total (95% CI)". Also "1[0.97,1.04]" style: RevMan drops trailing ".00" (1 not 1.00, -2 not -2.00, 1.2 not 1.20) — abstract states the same pooled RR as "1.00 (95% CI 0.97 to 1.04)".
O10. TOC misspellings preserved in analysis titles: "Completed exercise or pyschological therapies" (Analysis 2.2) and "subroup" (Analyses 5.2, 5.3, 5.4). Verbatim in both TOC (p2) and section headers.
O11. Abstract says "three trials reported quality of life" but Results text (p27) says "Five trials reported quality of life at the end of treatment" and Comparison 1 table shows 4 studies in Analysis 1.4. (QoL not truthed; counted-statement inconsistency noted.)
No unreadable cells were encountered in the truthed analyses; there are zero UNRESOLVED rows in this pass.

## 5. SUBSET RATIONALE

- T2 dichotomous = Analysis 1.3 "Completed intervention or control" (29 studies, 1363 participants, RR M-H Random). It is by far the largest dichotomous analysis in the review (alternatives: Analysis 2.2 k=4, Analysis 4.2 k=3). Structural diversity it adds: n/N event cells instead of Mean(SD), Mantel-Haenszel weighting, a "Total events" line absent from continuous analyses, a null pooled effect printed without trailing zeros ("1[0.97,1.04]"), I2=0%, a differently-labelled pooled row ("Total (95% CI)"), a log-scale axis, and randomised-denominator/multi-arm-pooling behaviour that deliberately diverges from the analysed Ns of Analysis 1.1 (O4) — a rich trap set for an audit tool.
- T3 follow-up = Analysis 1.2 "Reduction in depression symptoms follow-up" (8 studies, 377 participants). It is the review's only longer-term outcome analysis (Comparison 6 items are sensitivity re-runs of post-treatment data, not follow-up). Structural diversity: same studies as A1.1 but with different Ns per row (attrition), different means from separate follow-up publications (Babyak 2000, Singh 2001), borderline-significant pool (Z=2.18, P=0.03), moderate I2 (48.71%), and the suspicious SD-vs-SE cells of O7 — ideal for testing post-treatment/follow-up linkage.
- T1 primary = Analysis 1.1 was mandated; it is a flat (no-subgroup) 35-row SMD random-effects forest spanning a page break, with the 1353-vs-1356 count contradiction (O1) against the abstract.
- Together the three truthed analyses cover: continuous SMD + dichotomous RR; random-effects IV + M-H; flat plots with high/moderate/zero heterogeneity; page-break row continuation; multi-arm splitting behaviour; and text-vs-plot count reconciliation. Subgrouped structure exists in the PDF only in Analyses 1.4 and 5.x (subtotals-only analyses) — documented in the inventory but outside the mandated three targets.

## 6. META

- Citation (verbatim, PDF p4): "Cooney GM, Dwan K, Greig CA, Lawlor DA, Rimer J, Waugh FR, McMurdo M, Mead GE. Exercise for depression. Cochrane Database of Systematic Reviews 2013, Issue 9. Art. No.: CD004366. DOI: 10.1002/14651858.CD004366.pub6."
- DOI: 10.1002/14651858.CD004366.pub6
- Editorial group: Cochrane Common Mental Disorders Group. Publication status: "New search for studies and content updated (no change to conclusions), published in Issue 9, 2013."
- Total PDF pages: 132. Footer folio offset: PDF page = printed page + 3 (e.g. printed 101 = PDF 104); TOC pages i-ii = PDF 2-3.
- Page map of truthed content (PDF 1-based):
  - p1 title; p2-3 TOC; p4-6 Abstract/PLS (printed 1-3); p7-12 Summary of findings 1-4 (printed 4-9)
  - p19 Figure 1 (flow diagram, image); p23 Figure 2 (RoB graph, image); p24 Figure 3 (RoB summary, image); p26 Figure 4 (funnel plot of Analysis 1.1, image) + publication-bias text
  - p27 Effects of interventions text (counts for Comparison 1, Analyses 1.1-1.5 narrative)
  - p104-105 Comparison 1 summary table (printed 101-102)
  - p105-106 Analysis 1.1 forest (printed 102-103; rows Blumenthal 1999-Reuter 1984 on p105, Schuch 2011-Williams 2008 + Total + heterogeneity on p106)
  - p106 Analysis 1.2 forest (printed 103, complete on one page)
  - p106-107 Analysis 1.3 forest (printed 103-104; rows Blumenthal 1999-Hoffman 2010 on p106, Klein 1985-Williams 2008 + Total + heterogeneity on p107)
  - p107-124 remaining analyses (see inventory); p124+ Additional tables; p127 Appendices; p130+ Feedback/What's new/History etc. (printed 121-129 sections per TOC)
- Analysis inventory (every analysis the PDF lists; id | title (verbatim, incl. typos) | k = No. of studies from comparison tables | PDF page of forest | truthed?):
  - 1.1 | Reduction in depression symptoms post-treatment | k=35 (n=1353) | p105-106 | TRUTHED (T1)
  - 1.2 | Reduction in depression symptoms follow-up | k=8 (n=377) | p106 | TRUTHED (T3)
  - 1.3 | Completed intervention or control | k=29 (n=1363) | p106-107 | TRUTHED (T2)
  - 1.4 | Quality of life | k=4 (Subtotals only; 5 domain subgroups 1.4.1 Mental k=2, 1.4.2 Psychological k=2, 1.4.3 Social k=2, 1.4.4 Environment k=2, 1.4.5 Physical k=4) | p107-108 | not truthed
  - 2.1 | Reduction in depression symptoms post-treatment | k=7 (n=189) | p108-109 | not truthed
  - 2.2 | Completed exercise or pyschological therapies | k=4 (n=172) | p109 | not truthed
  - 2.3 | Quality of life | k=1 (Totals not selected; 2.3.1 Physical, 2.3.2 Mental) | p109 | not truthed
  - 3.1 | Reduction in depression symptoms post-treatment (vs bright light therapy) | k=1 (n=18) | p110 | not truthed
  - 4.1 | Reduction in depression symptoms post-treatment (vs pharmacological) | k=4 (n=300) | p110 | not truthed
  - 4.2 | Completed exercise or antidepressants | k=3 (n=278) | p111 | not truthed
  - 4.3 | Quality of Life | k=1 (Subtotals only; 4.3.1 Mental n=25, 4.3.2 Physical n=25) | p111 | not truthed
  - 5.1 | Exercise vs control subgroup analysis: type of exercise | k=35 (Subtotals only; 5.1.1 Aerobic k=28, 5.1.2 Mixed k=3, 5.1.3 Resistance k=4) | p113-114 | not truthed
  - 5.2 | Exercise vs control subroup analysis: intensity | k=35 (Subtotals only; 6 intensity subgroups) | p114-116 | not truthed
  - 5.3 | Exercise vs control subroup analysis: number of sessions | k=35 (Subtotals only; 5 subgroups) | p116-117 | not truthed
  - 5.4 | Exercise vs control subroup analysis: diagnosis of depression | k=35 (Subtotals only; 3 subgroups) | p117-118 | not truthed
  - 5.5 | Exercise vs control subgroup analysis: type of control | k=35 (n=1353; MD IV Fixed -1.57 [-1.97, -1.16]; 5 subgroups) | p118-119 | not truthed (see O3)
  - 6.1 | Reduction in depression symptoms post-treatment: peer-reviewed journal publications and doctoral theses only | k=34 (n=1335) | p120-121 | not truthed
  - 6.2 | ...studies published as abstracts or conference proceedings only | k=1 (n=18) | p121 | not truthed
  - 6.3 | ...studies with adequate allocation concealment | k=14 (n=829) | p121-122 | not truthed
  - 6.4 | ...studies using intention-to-treat analysis | k=11 (n=567; effect printed "-0.61 [1.00, -0.22]" — see O2) | p122 | not truthed
  - 6.5 | ...studies with blinded outcome assessment | k=12 (n=658) | p122-123 | not truthed
  - 6.6 | ...allocation concealment, intention-to-treat, blinded outcome | k=6 (n=464) | p123 | not truthed
  - 6.7 | ...Lowest dose of exercise | k=35 (n=1347; SMD IV Fixed) | p123-124 | not truthed
- Review-level: 39 included trials, 2326 participants at randomisation; 37 trials in meta-analyses (Greist 1979 and McCann 1984 excluded from MA); update added 7 trials / 408 additional participants over the previous 32-trial version (PDF p19, printed 16).
- Extraction method: PyMuPDF text layer, page-by-page; no OCR; graphical forest glyphs not needed for any truthed cell.
