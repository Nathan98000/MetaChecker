# PASS B — INDEPENDENT GOLD-STANDARD EXTRACTION (raw)
Source PDF: /Users/nathann/Downloads/Projects/Meta-analysis Checker/corpus/gold/driessen-2015-nih-psychotherapy/source/PMC4589340.pdf
Extraction date: 2026-08-11. Extractor: Pass B (independent; no other truth files consulted).

Method notes:
- Body text, Table 1 and Table 2 are machine-readable PDF text (verified via pdfminer text + per-line x/y coordinate reconstruction).
- Figs 1–7 are raster JPEG images embedded in the PDF; all figure content was read visually from the extracted images (image reading, not text). Image-to-figure assignment was made by content: page 13 top image = Fig 2, page 13 bottom = Fig 3, page 14 top = Fig 4, page 14 bottom = Fig 5, page 15: the image containing PT1 vs ADM rows = Fig 6 and the image containing PT1+ADM vs ADM rows = Fig 7 (per the captions printed on page 15).
- Figures use decimal commas (e.g., "0,39"); transcribed below with decimal points.
- Forest-plot columns per study row: Hedges's g | Standard error | Variance | Lower limit | Upper limit | Z-Value | p-Value | Relative weight. No per-study Ns are printed in any forest plot.

======================================================================
## 1. ANALYSES
Format: analysis_id | outcome | subgroup | effect_measure | model | n_studies_reported | pooled_effect | ci_lower | ci_upper | i2_or_het | p_value | source_page | source

A1-UNPUB | depressive severity, post-treatment | PT vs. Controls (all) — Unpublished | Hedges' g | random effects (CMA 2.2.064; fully random subgroup analysis pooling study-to-study variance across subgroups) | 6 | 0.20 | -0.11 | 0.51 | Q=5.22, df=5, I2=4 (95%CI 0~63) | Z=1.28 (ns) | 12 (also 1, 13) | Table 2; abstract p1; text p12; Fig 2 subtotal p13
A1-PUB | depressive severity, post-treatment | PT vs. Controls (all) — Published | Hedges' g | random effects | 20 | 0.52 | 0.37 | 0.68 | Q=39.04**, df=19, I2=51 (95%CI 7~70) | Z=6.64** | 12 (also 1, 13) | Table 2; abstract p1; text p12; Fig 2 subtotal p13
A1-ALL | depressive severity, post-treatment | PT vs. Controls (all) — Published + unpublished | Hedges' g | random effects | 26 | 0.39 | 0.08 | 0.70 | Q=49.82**, df=25, I2=50 (95%CI 12~67) | Z=2.47* | 12 (also 1, 13) | Table 2 (Δg=-0.13, Δg%=-25%, Qbetw=3.34, p=.07); abstract p1; text p12; Fig 2 overall p13
A1a-UNPUB | depressive severity, post-treatment | PT vs. no-treatment controls — Unpublished | Hedges' g | random effects | 2 | 0.77 | -0.07 | 1.61 | Q=1.02, df=1, I2=2 (95%CI "-") | Z=1.79 | 12 (also 13) | Table 2; text p13; Fig 3 subtotal p13
A1a-PUB | depressive severity, post-treatment | PT vs. no-treatment controls — Published | Hedges' g | random effects | 5 | 1.01 | 0.63 | 1.40 | Q=8.39, df=4, I2=52 (95%CI 0~81) | Z=5.20** | 12 (also 13) | Table 2; text p13; Fig 3 subtotal p13
A1a-ALL | depressive severity, post-treatment | PT vs. no-treatment controls — Published + unpublished | Hedges' g | random effects | 7 | 0.97 | 0.62 | 1.32 | Q=9.88, df=6, I2=39 (95%CI 0~73) | Z=5.47** | 12 (also 13) | Table 2 (Δg=-0.04, Δg%=-4%, Qbetw=0.28, p=.60); text p13; Fig 3 overall p13
A1b-UNPUB | depressive severity, post-treatment | PT vs. treatment controls — Unpublished | Hedges' g | random effects | 4 | 0.11 | -0.12 | 0.35 | Q=1.59, df=3, I2=0 (95%CI 0~68) | Z=0.96 | 12 (also 13, 14) | Table 2; text p13; Fig 4 subtotal p14
A1b-PUB | depressive severity, post-treatment | PT vs. treatment controls — Published | Hedges' g | random effects | 15 | 0.37 | 0.25 | 0.48 | Q=11.83, df=14, I2=0 (95%CI 0~46) | Z=6.35** | 12 (also 13, 14) | Table 2; text p13; Fig 4 subtotal p14
A1b-ALL | depressive severity, post-treatment | PT vs. treatment controls — Published + unpublished | Hedges' g | random effects | 19 | 0.26 | 0.02 | 0.51 | Q=17.08, df=18, I2=0 (95%CI 0~43) | Z=2.10* | 12 (also 13, 14) | Table 2 (Δg=-0.11, Δg%=-29%, Qbetw=3.65, p=.06); text p13; Fig 4 overall p14
A2-UNPUB | depressive severity, post-treatment | PT vs. other PT — Unpublished | Hedges' g | random effects | 2 | -0.05 | -0.49 | 0.38 | Q=2.61, df=1, I2=62 (95%CI "-") | Z=-0.24 | 12 (also 14) | Table 2; text p14; Fig 5 subtotal p14
A2-PUB | depressive severity, post-treatment | PT vs. other PT — Published | Hedges' g | random effects | 12 | 0.17 | -0.04 | 0.38 | Q=13.74, df=11, I2=20 (95%CI 0~59) | Z=1.60 | 12 (also 14) | Table 2; text p14; Fig 5 subtotal p14
A2-ALL | depressive severity, post-treatment | PT vs. other PT — Published + unpublished | Hedges' g | random effects | 14 | 0.13 | -0.06 | 0.31 | Q=18.17, df=13, I2=28 (95%CI 0~61) | Z=1.34 | 12 (also 14) | Table 2 (Δg=-0.04, Δg%=-24%, Qbetw=0.82, p=.37); text p14; Fig 5 overall p14
A3-UNPUB | depressive severity, post-treatment | PT vs. antidepressant medication — Unpublished | Hedges' g | random effects | 3 | -0.21 | -0.53 | 0.11 | Q=2.24, df=2, I2=11 (95%CI 0~76) | Z=-1.30 | 12 (also 15) | Table 2; text p15; Fig 6 subtotal p15
A3-PUB | depressive severity, post-treatment | PT vs. antidepressant medication — Published | Hedges' g | random effects | 15 | 0.01 | -0.13 | 0.16 | Q=22.67, df=14, I2=38 (95%CI 0~65) | Z=0.20 | 12 (also 15) | Table 2; text p15; Fig 6 subtotal p15
A3-ALL | depressive severity, post-treatment | PT vs. antidepressant medication — Published + unpublished | Hedges' g | random effects | 18 | -0.05 | -0.25 | 0.15 | Q=26.39, df=17, I2=36 (95%CI 0~62) | Z=-0.50 | 12 (also 15) | Table 2 (Δg=-0.07, Δg%=-456%, Qbetw=1.60, p=.21); text p15; Fig 6 overall p15
A4-UNPUB | depressive severity, post-treatment | PT + antidepressant medication vs. medication only — Unpublished | Hedges' g | random effects | 2 | 0.37 | -0.14 | 0.89 | Q=2.20, df=1, I2=54 (95%CI "-") | Z=1.42 | 12 (also 15, 16) | Table 2; text pp15-16; Fig 7 subtotal p15
A4-PUB | depressive severity, post-treatment | PT + antidepressant medication vs. medication only — Published | Hedges' g | random effects | 9 | 0.22 | -0.00 | 0.44 | Q=10.63, df=8, I2=25 (95%CI 0~65) | Z=1.96 | 12 (also 15, 16) | Table 2; text p16; Fig 7 subtotal p15
A4-ALL | depressive severity, post-treatment | PT + antidepressant medication vs. medication only — Published + unpublished | Hedges' g | random effects | 11 | 0.24 | 0.04 | 0.45 | Q=14.59, df=10, I2=31 (95%CI 0~65) | Z=2.36* | 12 (also 15, 16) | Table 2 (Δg=+0.02, Δg%=+11%, Qbetw=0.28, p=.59); text p16; Fig 7 overall p15

Text-only pools (details in S1 Table, which is NOT contained in this PDF; only point estimates/CIs quoted in body text):
APLAC-UNPUB | depressive severity, post-treatment | PT vs. pill-placebo control — Unpublished | Hedges' g | random effects | 1 | -0.09 | -0.59 | 0.40 | NR | NR | 14 | text p14 ("The pooled mean effect size of psychological treatment relative to pill-placebo control condition was g = -0.09 (-0.59~0.40) in 1 unpublished study"); S1 Table referenced
APLAC-PUB | depressive severity, post-treatment | PT vs. pill-placebo control — Published | Hedges' g | random effects | 5 | 0.34 | 0.14 | 0.53 | NR | NR | 14 | text p14; S1 Table referenced
APLAC-ALL | depressive severity, post-treatment | PT vs. pill-placebo control — Published + unpublished | Hedges' g | random effects | 6 (1+5) | 0.19 | -0.21 | 0.59 | NR | NR | 14 | text p14 ("a 45% decrease in effect size point estimate to g = 0.19 (-0.21~0.59)"); S1 Table referenced

Sensitivity analyses referenced but with NO numeric results in this PDF (all results said to be in S1 Table):
SENS-RANK | PT vs other PT with changed psychotherapy ranks for [47] (allegiance-minimizing study) | "Changing the psychological treatment ranks did not alter the pattern of results (S1 Table)." | p14
SENS-39-UNPUB | counting study [39] (no effect-size data reported) as unpublished | "Counting this study as unpublished instead of published did not alter the pattern of results (S1 Table)." | p15; also publication-rate sensitivity p12: "published and unpublished rates of 74.5% (41/55) and 25.5% (14/55)"
SENS-GOTTLIEB-A3 | PT vs ADM including estimated Gottlieb study (g = 0.00, n = 10 per condition) | "This pattern of results was not altered when we included the estimates from the unpublished study (Gottlieb) for which the original data were not available (S1 Table)." | p15 (estimate defined p11)
SENS-GOTTLIEB-A4 | PT+ADM vs ADM including estimated Gottlieb study | "Including the estimates from one unpublished study for which the original data were not available (Gottlieb) did not alter this result pattern (S1 Table)." | p16

Participant totals per Table 2 (NPT = participants in PT or PT+ADM conditions; NComp = participants in comparison conditions), page 12:
A1: unpub 190/146, pub 959/808, all 1149/954 (text p12: unpub n=336, pub n=1767)
A1a: unpub 45/14, pub 188/122, all 233/136
A1b: unpub 145/132, pub 771/686, all 916/818
A2: unpub 78/86, pub 286/331, all 364/417 (text p14: unpub total 164, pub total 617)
A3: unpub 116/115, pub 840/835, all 956/950 (text p15: unpub n=231, pub n=1675)
A4: unpub 41/44, pub 389/423, all 430/467 (text p16: unpub n=85, pub n=812)

Other quantitative results (not pooled effect sizes):
- Non-publication rate: 13/55 = 23.6% (binomial 95% CI 13%-37%, p16); comparison: Turner et al. 31.1% (23/74; CI 21%-43%) | pp1, 7, 16
- If two never-started grants included: 42/57 = 73.7% published, 15/57 = 26.3% not | p7
- Quality: 10/53 (18.9%) low risk of bias on all 4 criteria; published 18.2% vs unpublished 22.2%, Fisher's Exact p = 1.00; ITT 63.6% vs 55.6%, p = .72; blinding 56.8% vs 55.6%, p = 1.00; sequence generation 38.6% vs 77.8%, p = .06 (trend); independent randomization 25.0% vs 77.8%, p = .005 | p16
- Mean participants per condition: unpublished 31.9 (SD = 22.2) vs published 41.9 (SD = 42.5), t(54) = 0.79, p = .44 | p16
- Total participants: 42 published studies (4581) + 11 unpublished with data (839) = 5420 | p11

======================================================================
## 2. STUDY_LABELS
Format: label_verbatim | published_or_unpublished | appears_in | source_pages
(Forest-plot labels; figures group rows under "Published" / "Unpublished" in the "Group by Published?" column.)

Arean, 2010 | Published | FOREST_PLOT (Figs 2, 4) | 13, 14
Barber, 2012 | Published | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
Beutler, 1991 | Published | FOREST_PLOT (Figs 2, 4, 5) | 13, 14
Covi, 1987 | Published | FOREST_PLOT (Fig 5) | 14
Denton, 2012 | Published | FOREST_PLOT (Fig 7) | 15
DeRubeis, 2005 | Published | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
Dimidjian, 2006 | Published | FOREST_PLOT (Figs 2, 4, 5, 6; "Subgroup within study" = Combined) | 13, 14, 15
Elkin, 1989 | Published | FOREST_PLOT (Figs 2, 4, 5, 6) | 13, 14, 15
Foley, 1989 | Published | FOREST_PLOT (Fig 5) | 14
Frank, 2011 | Published | FOREST_PLOT (Fig 6) | 15
Gallagher, 1982 | Published | FOREST_PLOT (Fig 5) | 14
Goldman, 2006 | Published | FOREST_PLOT (Fig 5) | 14
Hayden, 2012 | Published | FOREST_PLOT (Figs 2, 4) | 13, 14
Hersen, 1984 | Published | FOREST_PLOT (Fig 7) | 15
Hollon, 1992 | Published | FOREST_PLOT (Figs 6, 7) | 15
Hollon, 2014 | Published | FOREST_PLOT (Fig 7) | 15
Jacobson, 1991 | Published | FOREST_PLOT (Fig 5; Subgroup within study = Combined) | 14
Jarrett, 1999 | Published | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
Lynch, 2003 | Published | FOREST_PLOT (Fig 7) | 15
Miranda, 2003 | Published | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
Mohr, 2001 | Published | FOREST_PLOT (Figs 5, 6) | 14, 15
Murphy, 1984 | Published | FOREST_PLOT (Figs 6, 7) | 15
Murphy, 1995 | Published | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
O'Hara, 2000 | Published | FOREST_PLOT (Figs 2, 3) | 13
Reynolds, 1999 | Published | FOREST_PLOT (Fig 7) | 15
Rohan, 2007 | Published | FOREST_PLOT (Figs 2, 3) | 13
Rush, 1977 | Published | FOREST_PLOT (Fig 6) | 15
Schulberg, 1996 | Published | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
Spinelli, 2003 | Published | FOREST_PLOT (Figs 2, 4) | 13, 14
Strachowski, 2008 | Published | FOREST_PLOT (Figs 2, 3) | 13
Swartz, 2008 | Published | FOREST_PLOT (Figs 2, 4) | 13, 14
Thompson, 1987 | Published | FOREST_PLOT (Figs 2, 3, 5) | 13, 14
Thompson, 2001 | Published | FOREST_PLOT (Figs 6, 7) | 15
Waters, in press | Published | FOREST_PLOT (Figs 2, 4) | 13, 14
Weissman, 1979 | Published | FOREST_PLOT (Figs 2, 4, 6, 7) | 13, 14, 15
Wright, 2005 | Published | FOREST_PLOT (Figs 2, 3, 5) | 13, 14
Wright, 2014 | Published | FOREST_PLOT (Fig 5) | 14
Blum, unpublished | Unpublished | FOREST_PLOT (Figs 2, 3) | 13
Hauenstein, unpublished | Unpublished | FOREST_PLOT (Figs 2, 4) | 13, 14
Thase, unpublished | Unpublished | FOREST_PLOT (Figs 2, 4, 6) | 13, 14, 15
Delgado, unpublished | Unpublished | FOREST_PLOT (Fig 6) | 15
[unnamed unpublished rows] | Unpublished | FOREST_PLOT: rows with data but blank study name in Fig 2 (PT1 vs CTRL-TAU), Fig 4 (PT1 vs CTRL-TAU), Fig 5 (two rows), Fig 7 (PT1+ADM vs ADM, HAMD-Modified); plus fully blank "Unpublished" rows (no name, no data) in Figs 2 (x2), 3 (x1), 4 (x1), 6 (x1), 7 (x1) | 13, 14, 15

Table 1 grant/PI labels (rows 1-57, pages 9-11; status = table section):
1 Arean (R01MH063982) + Alexopoulos (R01MH064099) | PUBLISHED [29] | TABLE | 9
2 Barber (R01MH061410) | PUBLISHED [30] | TABLE | 9
3 Beck (R01MH019989) + Rush (R03MH027759) | PUBLISHED [31] | TABLE | 9
4 Beutler (R01MH039859) | PUBLISHED [32] | TABLE | 9
5 Covi (R01MH033585) | PUBLISHED [33] | TABLE | 9
6 Denton (K23MH063994) | PUBLISHED [34] | TABLE | 9
7 DeRubeis (R10MH055877b) + Hollon (R10MH055875) + Hollon (K02MH001697) | PUBLISHED [35] | TABLE | 9
8 DiMascio (R01MH026467) + Weissman (R01MH026466) | PUBLISHED [36-37] | TABLE | 9
9 Frank (R01MH065376) | PUBLISHED [38] | TABLE | 9
10 Frank (R21MH061948) | PUBLISHED [39] (data reported only in aggregate; see oddities) | TABLE | 9
11 Freedland (R21MH052629) | PUBLISHED [40] | TABLE | 9
12 Glick (R01MH034466) | PUBLISHED [41-42] | TABLE | 9
13 Greenberg (R01MH045040) | PUBLISHED [43] | TABLE | 9
14 Hersen (R01MH028279) | PUBLISHED [44] | TABLE | 9
15 Hollon (R01MH033209) | PUBLISHED [45] | TABLE | 9
16 Hollon (R01MH060713) + Fawcett (R01MH060768) + DeRubeis (R01MH060998) | PUBLISHED [46] | TABLE | 9
17 Imber (U01MH033753) + Watkins (U01MH033760) + Sotsky (U01MH033762) | PUBLISHED [47] | TABLE | 9
18 Jacobson (R01MH033838) | PUBLISHED [48] | TABLE | 9
19 Jacobson (R01MH055502) | PUBLISHED [49] | TABLE | 9
20 Jacobson (R37MH044063) | PUBLISHED [50] | TABLE | 9
21 Jarrett (R01MH045043) | PUBLISHED [51] | TABLE | 10
22 Keefe (R01NS046422) | PUBLISHED [52] | TABLE | 10
23 Lustman (R01DK036452) | PUBLISHED [53] | TABLE | 10
24 Lynch (R03MH057799) | PUBLISHED [54] | TABLE | 10
25 Manber (R21MH066131) | PUBLISHED [55] | TABLE | 10
26 Miller (R01MH035945) | PUBLISHED [56] | TABLE | 10
27 Miranda (R01MH056864) | PUBLISHED [57] | TABLE | 10
28 Mohr (R01MH059708) | PUBLISHED [58] | TABLE | 10
29 Murphy (R01MH032756) | PUBLISHED [59] and second RCT [60] (same grant, two published trials) | TABLE | 10
30 O'Hara (R01MH050524) | PUBLISHED [61] | TABLE | 10
31 Reynolds (R01MH37869) | PUBLISHED [28] | TABLE | 10 (note: grant number printed with 5 digits "MH37869")
32 Rohan (R03MH065946) | PUBLISHED [62] | TABLE | 10
33 Schulberg (R01MH045815c) | PUBLISHED [63] | TABLE | 10
34 Simon (R01MH068127) | PUBLISHED [64] | TABLE | 10
35 Spinelli (K20MH001276) | PUBLISHED [65] | TABLE | 10
36 Swartz (K23MH064518) | PUBLISHED [66] | TABLE | 10
37 Talbot (K23MH064528) | PUBLISHED [67] | TABLE | 10
38 Taylor (M01RR000070) | PUBLISHED [68] | TABLE | 10
39 Thompson (R01MH032157) | PUBLISHED [69] | TABLE | 10
40 Thompson (R01MH037196) | PUBLISHED [70] and second RCT [71] (same grant, two published trials) | TABLE | 10
41 Weissman (R01MH034501) | PUBLISHED [72] | TABLE | 10
42 Wright (R21MH057470) | PUBLISHED [73] | TABLE | 10
43 Battle (K23MH066402) | UNPUBLISHED | TABLE | 10
44 Blum (R01MH025258) | UNPUBLISHED | TABLE | 10
45 Chisholm (F32MH012228*) | UNPUBLISHED section; "* Trial was never started." | TABLE | 10 (footnote p11)
46 Clark (R01MH062054d) | UNPUBLISHED; footnote d: "Investigator refuses to share data for this review." | TABLE | 11
47 Delgado (R01MH048977) | UNPUBLISHED | TABLE | 11
48 Gilliam (R01NS040808) | UNPUBLISHED | TABLE | 11
49 Gottlieb (K07MH000597) | UNPUBLISHED (data not retained; excluded from main analyses) | TABLE | 11
50 Hauenstein (R18MH049101) | UNPUBLISHED | TABLE | 11
51 Miller (R01MH058866) | UNPUBLISHED | TABLE | 11
52 Monk (R34MH072838) | UNPUBLISHED | TABLE | 11
53 Stuart (R01MH059103) | UNPUBLISHED | TABLE | 11
54 Stuart (R01MH059668) | UNPUBLISHED | TABLE | 11
55 Szapocznik (R01MH037379*) | UNPUBLISHED section; "* Trial was never started." | TABLE | 11
56 Thase (R01MH041884) | UNPUBLISHED | TABLE | 11
57 Zlotnick (R21MH060216) | UNPUBLISHED | TABLE | 11

Table 1 comparisons/PT types per row (verbatim comparison strings): 1 PT vs CTRL-NS (PST); 2 PT vs ADM, PT vs CTRL-PLAC (STPP); 3 PT vs ADM (CT); 4 PT vs CTRL-NS, PT vs PT (CT, FEP); 5 PT vs PT (CBT, IPP); 6 PT+ADM vs ADM (EFT); 7 PT vs ADM, PT vs CTRL-PLAC (CT); 8 PT vs ADM, PT vs CTRL-NS, PT+ADM vs ADM (IPT); 9 PT vs ADM (IPT); 10 PT vs PT (IPT, IPT-PS); 11 PT+CTRL-NS vs CTRL-NS (CBT); 12 PT+CTRL-TAU+ADM vs CTRL-TAU+ADM (IFI); 13 PT vs PT (CCT, EFT); 14 PT+ADM vs ADM, PT+CTRL-PLAC vs PT+CTRL-PLAC (SST, STPP); 15 PT vs ADM, PT+ADM vs ADM (CT); 16 PT+ADM vs ADM (CT); 17 PT vs ADM, PT vs CTRL-PLAC, PT vs PT (CBT, IPT); 18 PT vs PT (CBT, BMT, CO); 19 PT vs ADM, PT vs CTRL-PLAC, PT vs PT (CT, BA); 20 PT+PT+PT vs PT+PT, PT+PT+PT vs PT, PT+PT vs PT (CT, P-CT, BA); 21 PT vs ADM, PT vs CTRL-PLAC (CT); 22 PT vs CTRL-NS, PT vs CTRL-TAU (SeST); 23 PT vs CTRL-NS (CBT); 24 PT+ADM vs ADM (DBT); 25 PT+ADM vs CTRL-NS+ADM (CBTI); 26 CTRL-TAU+ADM+PT vs CTRL-TAU+ADM, CTRL-TAU+ADM+PT vs CTRL-TAU+ADM+PT (CT, SST); 27 PT vs ADM, PT vs CTRL-TAU (CBT); 28 PT vs ADM, PT vs PT (CBT, CT); 29 [59] PT vs ADM, PT+ADM vs ADM (CT); [60] PT vs ADM, PT vs CTRL-NS (CBT); 30 PT vs CTRL-NT (IPT); 31 PT+ADM vs ADM, PT+CTRL-PLAC vs CTRL-PLAC (IPT); 32 PT vs CTRL-NT (CBT); 33 PT vs ADM, PT vs CTRL-TAU (IPT); 34 PT+CTRL-TAU vs CTRL-TAU (CBT); 35 PT vs CTRL-NS (IPT); 36 PT1 vs CTRL-TAU (IPT-MOMS); 37 PT1+CTRL-TAU vs CTRL-TAU (IPT); 38 PT vs CTRL-NT (CBT); 39 PT vs PT (BT, CT, STPP); 40 [70] PT vs CTRL-NT, PT vs PT (BT, CT); [71] PT vs ADM, PT+ADM vs ADM (STPP, CBT); 41 PT vs PT (IPT, IPT-CM); 42 PT vs CTRL-NT, PT vs PT (CT, C-CT); 43 PT vs CTRL-NT (IFT); 44 PT vs CTRL-NT, PT vs PT (STPP, TOP); 45 [none listed]; 46 [none listed]; 47 PT vs ADM (CT); 48 PT vs ADM (CBT); 49 PT vs ADM, PT+ADM vs ADM (CBT); 50 PT vs CTRL-NS (CBT); 51 PT+ADM vs ADM, PT+PT+ADM vs PT+ADM (CT, FT); 52 PT vs CTRL-TAU (IPT); 53 PT vs CTRL-TAU (IPT); 54 PT vs PT (S-IPT, CM-IPT); 55 [none listed]; 56 PT vs ADM, PT vs CTRL-PLAC (CBT); 57 PT+ADM vs ADM (SFT).

======================================================================
## 3. PUBLISHED_EFFECTS (all forest-plot rows, Figs 2–7)
Format: effect_id | analysis_id | row_kind | label | effect (g) | ci_lower | ci_upper | weight_pct | n_treatment | n_control | subgroup | source_page | source_type | figure_or_table | certainty | note
source_type for all figure rows: IMAGE (figures are raster JPEGs; values read visually from extracted images; original prints decimal commas).
Per-study Ns are not printed in any figure (n_treatment/n_control = NR).
Note field carries: SE / Variance / Z / p as printed; comparison; outcome.

### Fig 2 — Psychological treatment versus control conditions (all) [analysis A1], page 13
F2-01 | A1-PUB | STUDY | Arean, 2010 | 0.39 | 0.10 | 0.67 | 8.33 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.15, Var 0.02, Z 2.62, p 0.01; PT1 vs CTRL-NS; HAMD
F2-02 | A1-PUB | STUDY | Barber, 2012 | 0.08 | -0.43 | 0.58 | 5.16 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.26, Var 0.07, Z 0.29, p 0.77; PT1 vs CTRL-NS(PLAC); Combined
F2-03 | A1-PUB | STUDY | Beutler, 1991 | 0.09 | -0.52 | 0.69 | 4.19 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.31, Var 0.09, Z 0.28, p 0.78; Combined; Combined
F2-04 | A1-PUB | STUDY | DeRubeis, 2005 | 0.45 | 0.03 | 0.88 | 6.20 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.22, Var 0.05, Z 2.10, p 0.04; PT1 vs CTRL-NS(PLAC); Response (HAMD<12) at post
F2-05 | A1-PUB | STUDY | Dimidjian, 2006 | 0.25 | -0.19 | 0.69 | 6.04 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.22, Var 0.05, Z 1.13, p 0.26; Subgroup within study = Combined; Combined; Combined
F2-06 | A1-PUB | STUDY | Elkin, 1989 | 0.30 | -0.06 | 0.65 | 7.24 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.18, Var 0.03, Z 1.63, p 0.10; Combined; Combined
F2-07 | A1-PUB | STUDY | Hayden, 2012 | 0.41 | -0.26 | 1.09 | 3.62 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.34, Var 0.12, Z 1.20, p 0.23; PT1 vs CTRL-NS; BDI
F2-08 | A1-PUB | STUDY | Jarrett, 1999 | 0.58 | 0.11 | 1.05 | 5.66 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.24, Var 0.06, Z 2.44, p 0.01; PT1 vs CTRL-NS(PLAC); Combined
F2-09 | A1-PUB | STUDY | Miranda, 2003 | 0.16 | -0.13 | 0.45 | 8.26 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.15, Var 0.02, Z 1.06, p 0.29; PT1 vs CTRL-TAU; HAMD
F2-10 | A1-PUB | STUDY | Murphy, 1995 | 0.13 | -0.65 | 0.91 | 2.93 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.40, Var 0.16, Z 0.33, p 0.74; PT1 vs CTRL-NS; Combined
F2-11 | A1-PUB | STUDY | O'Hara, 2000 | 1.14 | 0.72 | 1.56 | 6.24 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.22, Var 0.05, Z 5.30, p 0.00; PT1 vs CTRL-NT; Combined
F2-12 | A1-PUB | STUDY | Rohan, 2007 | 1.01 | 0.26 | 1.75 | 3.16 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.38, Var 0.14, Z 2.66, p 0.01; PT1 vs CTRL-NT; Combined
F2-13 | A1-PUB | STUDY | Schulberg, 1996 | 0.44 | 0.15 | 0.73 | 8.29 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.15, Var 0.02, Z 2.95, p 0.00; PT1 vs CTRL-TAU; HAMD
F2-14 | A1-PUB | STUDY | Spinelli, 2003 | 0.84 | -0.19 | 1.87 | 1.89 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.52, Var 0.28, Z 1.60, p 0.11; PT1 vs CTRL-NS; Combined
F2-15 | A1-PUB | STUDY | Strachowski, 2008 | 1.58 | 0.88 | 2.28 | 3.43 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.36, Var 0.13, Z 4.42, p 0.00; PT1 vs CTRL-NT; Combined; CI arrow beyond x-axis limit 2.00
F2-16 | A1-PUB | STUDY | Swartz, 2008 | 0.85 | 0.21 | 1.48 | 3.93 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.32, Var 0.10, Z 2.62, p 0.01; PT1 vs CTRL-TAU; Combined
F2-17 | A1-PUB | STUDY | Thompson, 1987 | 0.41 | -0.09 | 0.91 | 5.21 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.26, Var 0.07, Z 1.60, p 0.11; PT1 vs CTRL-NT; Combined
F2-18 | A1-PUB | STUDY | Waters, in press | 0.70 | 0.11 | 1.28 | 4.39 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.30, Var 0.09, Z 2.34, p 0.02; Combined; BDI
F2-19 | A1-PUB | STUDY | Weissman, 1979 | 0.88 | 0.07 | 1.70 | 2.73 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.42, Var 0.17, Z 2.12, p 0.03; PT1 vs CTRL-NS; outcome "no failure"
F2-20 | A1-PUB | STUDY | Wright, 2005 | 1.10 | 0.35 | 1.85 | 3.10 | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.38, Var 0.15, Z 2.88, p 0.00; Combined; Combined
F2-21 | A1-PUB | SUBGROUP_TOTAL | Published (Overall) | 0.52 | 0.37 | 0.68 | (blank) | NR | NR | Published | 13 | IMAGE | Fig 2 | KNOWN | SE 0.08, Var 0.01, Z 6.64, p 0.00; green diamond
F2-22 | A1-UNPUB | STUDY | [blank row, "Unpublished" only] | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | UNRESOLVED | Hidden study (no name, no values); per figure note, investigators did not permit study-level display. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F2-23 | A1-UNPUB | STUDY | Blum, unpublished | 0.50 | -0.34 | 1.33 | 10.55 | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | KNOWN | SE 0.43, Var 0.18, Z 1.17, p 0.24; Combined; SCL-90-D. Effect values exist ONLY in this paper (unpublished author-supplied data). SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F2-24 | A1-UNPUB | STUDY | Hauenstein, unpublished | 0.08 | -0.31 | 0.47 | 26.79 | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | KNOWN | SE 0.20, Var 0.04, Z 0.42, p 0.67; PT1 vs CTRL-NS; HAMD. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F2-25 | A1-UNPUB | STUDY | [blank row, "Unpublished" only] | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | UNRESOLVED | Second hidden study (no name, no values). SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F2-26 | A1-UNPUB | STUDY | [no study name printed] | 0.31 | -0.10 | 0.71 | 25.96 | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | KNOWN (values) / AMBIGUOUS (identity) | SE 0.21, Var 0.04, Z 1.48, p 0.14; PT1 vs CTRL-TAU; Combined. Name withheld. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F2-27 | A1-UNPUB | STUDY | Thase, unpublished | -0.09 | -0.59 | 0.40 | 21.06 | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | KNOWN | SE 0.25, Var 0.06, Z -0.36, p 0.72; PT1 vs CTRL-NS(PLAC); HAMD. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F2-28 | A1-UNPUB | SUBGROUP_TOTAL | Unpublished (Overall) | 0.20 | -0.11 | 0.51 | (blank) | NR | NR | Unpublished | 13 | IMAGE | Fig 2 | KNOWN | SE 0.16, Var 0.02, Z 1.28, p 0.20; green diamond
F2-29 | A1-ALL | OVERALL_TOTAL | Overall | 0.39 | 0.08 | 0.70 | (blank) | NR | NR | All | 13 | IMAGE | Fig 2 | KNOWN | SE 0.16, Var 0.02, Z 2.47, p 0.01; black diamond
(Consistency: 20 visible published rows, weights sum 100.00; 4 visible unpublished data rows sum 84.36, remainder 15.64 belongs to the 2 hidden studies; 4+2=6 = k in Table 2.)

### Fig 3 — Psychological treatment versus no-treatment control conditions [analysis A1a], page 13
F3-01 | A1a-PUB | STUDY | O'Hara, 2000 | 1.14 | 0.72 | 1.56 | 27.13 | NR | NR | Published | 13 | IMAGE | Fig 3 | KNOWN | SE 0.22, Var 0.05, Z 5.30, p 0.00; PT1 vs CTRL-NT; Combined
F3-02 | A1a-PUB | STUDY | Rohan, 2007 | 1.01 | 0.26 | 1.75 | 16.07 | NR | NR | Published | 13 | IMAGE | Fig 3 | KNOWN | SE 0.38, Var 0.14, Z 2.66, p 0.01; PT1 vs CTRL-NT; Combined
F3-03 | A1a-PUB | STUDY | Strachowski, 2008 | 1.58 | 0.88 | 2.28 | 17.19 | NR | NR | Published | 13 | IMAGE | Fig 3 | KNOWN | SE 0.36, Var 0.13, Z 4.42, p 0.00; PT1 vs CTRL-NT; Combined; CI arrow beyond 2.00
F3-04 | A1a-PUB | STUDY | Thompson, 1987 | 0.41 | -0.09 | 0.91 | 23.79 | NR | NR | Published | 13 | IMAGE | Fig 3 | KNOWN | SE 0.26, Var 0.07, Z 1.60, p 0.11; PT1 vs CTRL-NT; Combined
F3-05 | A1a-PUB | STUDY | Wright, 2005 | 1.10 | 0.35 | 1.85 | 15.82 | NR | NR | Published | 13 | IMAGE | Fig 3 | KNOWN | SE 0.38, Var 0.15, Z 2.88, p 0.00; Combined; Combined
F3-06 | A1a-PUB | SUBGROUP_TOTAL | Published (Overall) | 1.01 | 0.63 | 1.40 | (blank) | NR | NR | Published | 13 | IMAGE | Fig 3 | KNOWN | SE 0.20, Var 0.04, Z 5.20, p 0.00
F3-07 | A1a-UNPUB | STUDY | [blank row, "Unpublished" only] | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | NR | NR | Unpublished | 13 | IMAGE | Fig 3 | UNRESOLVED | Hidden study (no name, no values). SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F3-08 | A1a-UNPUB | STUDY | Blum, unpublished | 0.50 | -0.34 | 1.33 | 66.57 | NR | NR | Unpublished | 13 | IMAGE | Fig 3 | KNOWN | SE 0.43, Var 0.18, Z 1.17, p 0.24; Combined; SCL-90-D. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F3-09 | A1a-UNPUB | SUBGROUP_TOTAL | Unpublished (Overall) | 0.77 | -0.07 | 1.61 | (blank) | NR | NR | Unpublished | 13 | IMAGE | Fig 3 | KNOWN | SE 0.43, Var 0.18, Z 1.79, p 0.07
F3-10 | A1a-ALL | OVERALL_TOTAL | Overall | 0.97 | 0.62 | 1.32 | (blank) | NR | NR | All | 13 | IMAGE | Fig 3 | KNOWN | SE 0.18, Var 0.03, Z 5.47, p 0.00
(Published weights sum 100.00; hidden unpublished study carries ~33.43%.)

### Fig 4 — Psychological treatment versus treatment control conditions [analysis A1b], page 14
F4-01 | A1b-PUB | STUDY | Arean, 2010 | 0.39 | 0.10 | 0.67 | 15.57 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.15, Var 0.02, Z 2.62, p 0.01; PT1 vs CTRL-NS; HAMD
F4-02 | A1b-PUB | STUDY | Barber, 2012 | 0.08 | -0.43 | 0.58 | 5.02 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.26, Var 0.07, Z 0.29, p 0.77; PT1 vs CTRL-NS(PLAC); Combined
F4-03 | A1b-PUB | STUDY | Beutler, 1991 | 0.09 | -0.52 | 0.69 | 3.56 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.31, Var 0.09, Z 0.28, p 0.78; Combined; Combined
F4-04 | A1b-PUB | STUDY | DeRubeis, 2005 | 0.45 | 0.03 | 0.88 | 7.17 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.22, Var 0.05, Z 2.10, p 0.04; PT1 vs CTRL-NS(PLAC); Response (HAMD<12) at post
F4-05 | A1b-PUB | STUDY | Dimidjian, 2006 | 0.25 | -0.19 | 0.69 | 6.77 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.22, Var 0.05, Z 1.13, p 0.26; Subgroup = Combined; Combined; Combined
F4-06 | A1b-PUB | STUDY | Elkin, 1989 | 0.30 | -0.06 | 0.65 | 10.28 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.18, Var 0.03, Z 1.63, p 0.10; Combined; Combined
F4-07 | A1b-PUB | STUDY | Hayden, 2012 | 0.41 | -0.26 | 1.09 | 2.85 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.34, Var 0.12, Z 1.20, p 0.23; PT1 vs CTRL-NS; BDI
F4-08 | A1b-PUB | STUDY | Jarrett, 1999 | 0.58 | 0.11 | 1.05 | 5.94 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.24, Var 0.06, Z 2.44, p 0.01; PT1 vs CTRL-NS(PLAC); Combined
F4-09 | A1b-PUB | STUDY | Miranda, 2003 | 0.16 | -0.13 | 0.45 | 15.17 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.15, Var 0.02, Z 1.06, p 0.29; PT1 vs CTRL-TAU; HAMD
F4-10 | A1b-PUB | STUDY | Murphy, 1995 | 0.13 | -0.65 | 0.91 | 2.12 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.40, Var 0.16, Z 0.33, p 0.74; PT1 vs CTRL-NS; Combined
F4-11 | A1b-PUB | STUDY | Schulberg, 1996 | 0.44 | 0.15 | 0.73 | 15.35 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.15, Var 0.02, Z 2.95, p 0.00; PT1 vs CTRL-TAU; HAMD
F4-12 | A1b-PUB | STUDY | Spinelli, 2003 | 0.84 | -0.19 | 1.87 | 1.23 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.52, Var 0.28, Z 1.60, p 0.11; PT1 vs CTRL-NS; Combined
F4-13 | A1b-PUB | STUDY | Swartz, 2008 | 0.85 | 0.21 | 1.48 | 3.22 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.32, Var 0.10, Z 2.62, p 0.01; PT1 vs CTRL-TAU; Combined
F4-14 | A1b-PUB | STUDY | Waters, in press | 0.70 | 0.11 | 1.28 | 3.82 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.30, Var 0.09, Z 2.34, p 0.02; Combined; BDI
F4-15 | A1b-PUB | STUDY | Weissman, 1979 | 0.88 | 0.07 | 1.70 | 1.94 | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.42, Var 0.17, Z 2.12, p 0.03; PT1 vs CTRL-NS; no failure
F4-16 | A1b-PUB | SUBGROUP_TOTAL | Published (Overall) | 0.37 | 0.25 | 0.48 | (blank) | NR | NR | Published | 14 | IMAGE | Fig 4 | KNOWN | SE 0.06, Var 0.00, Z 6.35, p 0.00
F4-17 | A1b-UNPUB | STUDY | Hauenstein, unpublished | 0.08 | -0.31 | 0.47 | 36.14 | NR | NR | Unpublished | 14 | IMAGE | Fig 4 | KNOWN | SE 0.20, Var 0.04, Z 0.42, p 0.67; PT1 vs CTRL-NS; HAMD. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F4-18 | A1b-UNPUB | STUDY | [blank row, "Unpublished" only] | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | NR | NR | Unpublished | 14 | IMAGE | Fig 4 | UNRESOLVED | Hidden study (no name, no values). SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F4-19 | A1b-UNPUB | STUDY | [no study name printed] | 0.31 | -0.10 | 0.71 | 33.64 | NR | NR | Unpublished | 14 | IMAGE | Fig 4 | KNOWN (values) / AMBIGUOUS (identity) | SE 0.21, Var 0.04, Z 1.48, p 0.14; PT1 vs CTRL-TAU; Combined. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F4-20 | A1b-UNPUB | STUDY | Thase, unpublished | -0.09 | -0.59 | 0.40 | 22.12 | NR | NR | Unpublished | 14 | IMAGE | Fig 4 | KNOWN | SE 0.25, Var 0.06, Z -0.36, p 0.72; PT1 vs CTRL-NS(PLAC); HAMD. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F4-21 | A1b-UNPUB | SUBGROUP_TOTAL | Unpublished (Overall) | 0.11 | -0.12 | 0.35 | (blank) | NR | NR | Unpublished | 14 | IMAGE | Fig 4 | KNOWN | SE 0.12, Var 0.01, Z 0.96, p 0.34
F4-22 | A1b-ALL | OVERALL_TOTAL | Overall | 0.26 | 0.02 | 0.51 | (blank) | NR | NR | All | 14 | IMAGE | Fig 4 | KNOWN | SE 0.13, Var 0.02, Z 2.10, p 0.04
(Published weights sum 100.01; visible unpublished weights sum 91.90, hidden study ~8.10%.)

### Fig 5 — Psychological treatment versus other psychological treatment [analysis A2], page 14
F5-01 | A2-PUB | STUDY | Beutler, 1991 | 0.13 | -0.46 | 0.72 | 8.98 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.30, Var 0.09, Z 0.43, p 0.67; PT1 vs PT2; Combined
F5-02 | A2-PUB | STUDY | Covi, 1987 | 1.64 | 0.47 | 2.80 | 2.88 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.59, Var 0.35, Z 2.75, p 0.01; PT1 vs PT2; Remission (BDI=0-9); CI arrow beyond 2.00
F5-03 | A2-PUB | STUDY | Dimidjian, 2006 | 0.22 | -0.27 | 0.70 | 11.64 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.25, Var 0.06, Z 0.87, p 0.39; Subgroup = Combined; PT1 vs PT2; Combined
F5-04 | A2-PUB | STUDY | Elkin, 1989 | -0.12 | -0.48 | 0.23 | 16.62 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.18, Var 0.03, Z -0.67, p 0.50; PT1 vs PT2; Combined
F5-05 | A2-PUB | STUDY | Foley, 1989 | 0.06 | -0.82 | 0.94 | 4.72 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.45, Var 0.20, Z 0.13, p 0.90; PT1 vs PT2; Combined
F5-06 | A2-PUB | STUDY | Gallagher, 1982 | 0.27 | -0.58 | 1.12 | 5.00 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.43, Var 0.19, Z 0.63, p 0.53; Combined; Combined
F5-07 | A2-PUB | STUDY | Goldman, 2006 | 0.64 | -0.00 | 1.28 | 7.94 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.33, Var 0.11, Z 1.96, p 0.05; PT1 vs PT2; BDI
F5-08 | A2-PUB | STUDY | Jacobson, 1991 | -0.16 | -0.77 | 0.45 | 8.51 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.31, Var 0.10, Z -0.52, p 0.60; Subgroup = Combined; Combined; Combined
F5-09 | A2-PUB | STUDY | Mohr, 2001 | 0.51 | -0.11 | 1.14 | 8.19 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.32, Var 0.10, Z 1.60, p 0.11; PT1 vs PT2; Combined
F5-10 | A2-PUB | STUDY | Thompson, 1987 | 0.09 | -0.40 | 0.59 | 11.29 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.25, Var 0.06, Z 0.37, p 0.71; Combined; Combined
F5-11 | A2-PUB | STUDY | Wright, 2005 | -0.08 | -0.78 | 0.62 | 6.91 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.36, Var 0.13, Z -0.23, p 0.82; PT1 vs PT2; Combined
F5-12 | A2-PUB | STUDY | Wright, 2014 | 0.08 | -0.60 | 0.75 | 7.32 | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.34, Var 0.12, Z 0.23, p 0.82; PT1 vs PT2; HAMD
F5-13 | A2-PUB | SUBGROUP_TOTAL | Published (Overall) | 0.17 | -0.04 | 0.38 | (blank) | NR | NR | Published | 14 | IMAGE | Fig 5 | KNOWN | SE 0.11, Var 0.01, Z 1.60, p 0.11
F5-14 | A2-UNPUB | STUDY | [no study name printed] | 0.44 | -0.30 | 1.19 | 27.27 | NR | NR | Unpublished | 14 | IMAGE | Fig 5 | KNOWN (values) / AMBIGUOUS (identity) | SE 0.38, Var 0.14, Z 1.17, p 0.24. Name withheld. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F5-15 | A2-UNPUB | STUDY | [no study name printed] | -0.24 | -0.59 | 0.12 | 72.73 | NR | NR | Unpublished | 14 | IMAGE | Fig 5 | KNOWN (values) / AMBIGUOUS (identity) | SE 0.18, Var 0.03, Z -1.31, p 0.19. Name withheld. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F5-16 | A2-UNPUB | SUBGROUP_TOTAL | Unpublished (Overall) | -0.05 | -0.49 | 0.38 | (blank) | NR | NR | Unpublished | 14 | IMAGE | Fig 5 | KNOWN | SE 0.22, Var 0.05, Z -0.24, p 0.81
F5-17 | A2-ALL | OVERALL_TOTAL | Overall | 0.13 | -0.06 | 0.31 | (blank) | NR | NR | All | 14 | IMAGE | Fig 5 | KNOWN | SE 0.10, Var 0.01, Z 1.34, p 0.18
(Unpublished weights sum exactly 100.00: both k=2 studies shown with values but names withheld; comparison/outcome columns for these two rows are blank in the figure.)

### Fig 6 — Psychological treatment versus antidepressant medication [analysis A3], page 15
F6-01 | A3-PUB | STUDY | Barber, 2012 | -0.11 | -0.58 | 0.37 | 6.10 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.24, Var 0.06, Z -0.43, p 0.67; PT1 vs ADM; Combined
F6-02 | A3-PUB | STUDY | DeRubeis, 2005 | -0.07 | -0.41 | 0.28 | 9.12 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.18, Var 0.03, Z -0.37, p 0.71; PT1 vs ADM; Combined
F6-03 | A3-PUB | STUDY | Dimidjian, 2006 | -0.16 | -0.60 | 0.28 | 6.76 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.23, Var 0.05, Z -0.72, p 0.47; Subgroup = Combined; Combined; Combined
F6-04 | A3-PUB | STUDY | Elkin, 1989 | -0.08 | -0.44 | 0.28 | 8.70 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.18, Var 0.03, Z -0.44, p 0.66; Combined; Combined
F6-05 | A3-PUB | STUDY | Frank, 2011 | -0.10 | -0.34 | 0.15 | 12.58 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.12, Var 0.02, Z -0.78, p 0.44; PT1 vs ADM; Remission
F6-06 | A3-PUB | STUDY | Hollon, 1992 | 0.08 | -0.39 | 0.55 | 6.19 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.24, Var 0.06, Z 0.34, p 0.73; PT1 vs ADM; Combined
F6-07 | A3-PUB | STUDY | Jarrett, 1999 | -0.22 | -0.67 | 0.24 | 6.44 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.23, Var 0.05, Z -0.92, p 0.36; PT1 vs ADM; Combined
F6-08 | A3-PUB | STUDY | Miranda, 2003 | -0.24 | -0.53 | 0.05 | 10.75 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.15, Var 0.02, Z -1.59, p 0.11; PT1 vs ADM; HAMD
F6-09 | A3-PUB | STUDY | Mohr, 2001 | -0.10 | -0.76 | 0.56 | 3.71 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.34, Var 0.11, Z -0.29, p 0.77; Combined; Combined
F6-10 | A3-PUB | STUDY | Murphy, 1984 | 0.31 | -0.25 | 0.87 | 4.82 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.29, Var 0.08, Z 1.08, p 0.28; PT1 vs ADM; Combined
F6-11 | A3-PUB | STUDY | Murphy, 1995 | 1.31 | 0.40 | 2.22 | 2.13 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.47, Var 0.22, Z 2.81, p 0.00; PT1 vs ADM; Combined; CI arrow beyond 2.00
F6-12 | A3-PUB | STUDY | Rush, 1977 | 0.90 | 0.21 | 1.59 | 3.49 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.35, Var 0.12, Z 2.57, p 0.01; PT1 vs ADM; Combined
F6-13 | A3-PUB | STUDY | Schulberg, 1996 | -0.03 | -0.32 | 0.26 | 10.95 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.15, Var 0.02, Z -0.22, p 0.82; PT1 vs ADM; HAMD
F6-14 | A3-PUB | STUDY | Thompson, 2001 | 0.31 | -0.17 | 0.80 | 5.92 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.25, Var 0.06, Z 1.27, p 0.21; PT1 vs ADM; Combined
F6-15 | A3-PUB | STUDY | Weissman, 1979 | 0.24 | -0.63 | 1.10 | 2.34 | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.44, Var 0.20, Z 0.54, p 0.59; PT1 vs ADM; no failure
F6-16 | A3-PUB | SUBGROUP_TOTAL | Published (Overall) | 0.01 | -0.13 | 0.16 | (blank) | NR | NR | Published | 15 | IMAGE | Fig 6 | KNOWN | SE 0.07, Var 0.01, Z 0.20, p 0.84
F6-17 | A3-UNPUB | STUDY | Delgado, unpublished | -0.15 | -0.70 | 0.39 | 25.98 | NR | NR | Unpublished | 15 | IMAGE | Fig 6 | KNOWN | SE 0.28, Var 0.08, Z -0.56, p 0.58; PT1 vs ADM; HAMD. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F6-18 | A3-UNPUB | STUDY | [blank row, "Unpublished" only] | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | NR | NR | Unpublished | 15 | IMAGE | Fig 6 | UNRESOLVED | Hidden study (no name, no values); carries ~44.53% weight by subtraction. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F6-19 | A3-UNPUB | STUDY | Thase, unpublished | -0.51 | -1.01 | -0.01 | 29.49 | NR | NR | Unpublished | 15 | IMAGE | Fig 6 | KNOWN | SE 0.25, Var 0.06, Z -2.02, p 0.04; PT1 vs ADM; HAMD. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F6-20 | A3-UNPUB | SUBGROUP_TOTAL | Unpublished (Overall) | -0.21 | -0.53 | 0.11 | (blank) | NR | NR | Unpublished | 15 | IMAGE | Fig 6 | KNOWN | SE 0.16, Var 0.03, Z -1.30, p 0.19
F6-21 | A3-ALL | OVERALL_TOTAL | Overall | -0.05 | -0.25 | 0.15 | (blank) | NR | NR | All | 15 | IMAGE | Fig 6 | KNOWN | SE 0.10, Var 0.01, Z -0.50, p 0.62
(Published weights sum 100.00.)

### Fig 7 — Psychological treatment combined with antidepressant medication versus antidepressant medication monotherapy [analysis A4], page 15
F7-01 | A4-PUB | STUDY | Denton, 2012 | 0.86 | -0.29 | 2.00 | 3.40 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.58, Var 0.34, Z 1.47, p 0.14; PT1+ADM vs ADM; IDS-C30; CI arrow near/beyond 2.00
F7-02 | A4-PUB | STUDY | Hersen, 1984 | -0.20 | -0.86 | 0.47 | 8.65 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.34, Var 0.11, Z -0.58, p 0.56; PT1+ADM vs ADM; Combined
F7-03 | A4-PUB | STUDY | Hollon, 1992 | 0.38 | -0.09 | 0.86 | 14.08 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.24, Var 0.06, Z 1.60, p 0.11; PT1+ADM vs ADM; Combined
F7-04 | A4-PUB | STUDY | Hollon, 2014 | -0.03 | -0.21 | 0.16 | 31.13 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.09, Var 0.01, Z -0.29, p 0.77; PT1+ADM vs ADM; Combined
F7-05 | A4-PUB | STUDY | Lynch, 2003 | 0.25 | -0.51 | 1.00 | 7.06 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.38, Var 0.15, Z 0.64, p 0.52; PT1+ADM vs ADM; Combined
F7-06 | A4-PUB | STUDY | Murphy, 1984 | 0.30 | -0.27 | 0.87 | 10.83 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.29, Var 0.09, Z 1.02, p 0.31; PT1+ADM vs ADM; Combined
F7-07 | A4-PUB | STUDY | Reynolds, 1999 | 0.30 | -0.42 | 1.01 | 7.71 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.36, Var 0.13, Z 0.81, p 0.42; PT1+ADM vs ADM; Remission
F7-08 | A4-PUB | STUDY | Thompson, 2001 | 0.41 | -0.07 | 0.88 | 14.10 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.24, Var 0.06, Z 1.68, p 0.09; PT1+ADM vs ADM; Combined
F7-09 | A4-PUB | STUDY | Weissman, 1979 | 1.08 | -0.14 | 2.29 | 3.04 | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.62, Var 0.38, Z 1.74, p 0.08; PT1+ADM vs ADM; no failure; CI arrow beyond 2.00
F7-10 | A4-PUB | SUBGROUP_TOTAL | Published (Overall) | 0.22 | -0.00 | 0.44 | (blank) | NR | NR | Published | 15 | IMAGE | Fig 7 | KNOWN | SE 0.11, Var 0.01, Z 1.96, p 0.05
F7-11 | A4-UNPUB | STUDY | [no study name printed] | 0.56 | 0.10 | 1.02 | 78.94 | NR | NR | Unpublished | 15 | IMAGE | Fig 7 | KNOWN (values) / AMBIGUOUS (identity) | SE 0.24, Var 0.06, Z 2.36, p 0.02; PT1+ADM vs ADM; HAMD-Modified; Subgroup within study = Blank. Name withheld. Values exist ONLY in this paper. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F7-12 | A4-UNPUB | STUDY | [blank row, "Unpublished" only] | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | NR | NR | Unpublished | 15 | IMAGE | Fig 7 | UNRESOLVED | Hidden study (no name, no values); ~21.06% weight by subtraction. SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE
F7-13 | A4-UNPUB | SUBGROUP_TOTAL | Unpublished (Overall) | 0.37 | -0.14 | 0.89 | (blank) | NR | NR | Unpublished | 15 | IMAGE | Fig 7 | KNOWN | SE 0.26, Var 0.07, Z 1.42, p 0.16
F7-14 | A4-ALL | OVERALL_TOTAL | Overall | 0.24 | 0.04 | 0.45 | (blank) | NR | NR | All | 15 | IMAGE | Fig 7 | KNOWN | SE 0.10, Var 0.01, Z 2.36, p 0.02
(Published weights sum 100.00.)

Heterogeneity rows: no per-figure heterogeneity rows are printed in the forest plots; all Q/df/I2 values appear only in Table 2 (page 12), captured in Section 1.

======================================================================
## 4. UNPUBLISHED-DATA PROVENANCE (verbatim quotes)

p1 (Data Availability Statement): "All relevant data from published studies and a number of the unpublished studies are within the paper and its Supporting Information files. We cannot make the data from all unpublished studies publicly available as we obtained it this data from third parties (the original investigators of these studies), who did not provide us permission to do so. However, others can request this data from the relevant investigators. Contact information can be retrieved from 'http://projectreporter.nih.gov/reporter.cfm' by entering the relevant grant number listed in Table 1 of this manuscript." [Note the typo "we obtained it this data".]

p1 (Abstract): "For studies that were not published, data were requested from investigators and included in the meta-analyses. Thirteen (23.6%) of the 55 funded grants that began trials did not result in publications, and two others never started."

p4 (Methods): "In cases of non-publication, we contacted the investigators to request the unpublished data and to ask why they had not been published."

p7 (Results): "Two other grant-funded studies were never started, one because of difficulty recruiting patients (S. Chisholm-Stockard, personal communication, March 3, 2011) and the other because of difficulty finding psychodynamic therapists willing to participate in clinical research with Hispanic elders (J. Szapocznik, personal communication, August 30, 2010). These last two grants were excluded from further consideration."

p7 (Results): "Of the 55 grants that started studies, we were able to locate published articles corresponding to 42 (76.4%) grants [28–73], but not for the other 13 (23.6%). ... These 13 grants met our definition of unpublished studies. We were able to obtain the original data from 11 of these studies (84,6%). With respect to the remaining studies, the twelfth" [continues p8]

p8 (Results, continuation): "investigator was not yet ready to share her data (R. Clark). The thirteenth investigator expressed willingness to share data, but the data had been collected over a quarter of a century earlier and had not been retained, though he recalled that the sample was small (no more than a dozen patients per condition) and that the differences were negligible (G. Gottlieb, personal communication, June 10, 2012). Therefore, we excluded this study from the main analyses, but" [continues p11]

p11 (continuation): "conducted sensitivity analyses, including this study in the relevant comparisons (psychological treatment alone or in combination versus antidepressant medication monotherapy) and estimating the study's effect size to be g = 0.00 with n = 10 per condition. The total number of participants over the 42 published studies (4581) and 11 unpublished studies for which we had data (839) was 5420."

p11 (Table 1 footnote d): "Investigator refuses to share data for this review." [applies to grant R01MH062054, PI Clark]

p7 (Methods context on unpublished quality ratings): "Unpublished papers were rated from draft manuscripts whenever possible. When no drafts were available, the principal investigators of the unpublished studies were asked for quality criteria by email."

pp13, 13, 14, 14, 15, 15 (identical note in captions of Figs 2, 3, 4, 5, 6, 7): "Note: Not all results of the unpublished studies are presented at study level, because we did not have permission of the investigators to do so."

p16 (Reasons for non-publication): "Of the 13 unpublished studies, only two were submitted for review; neither was accepted for publication. Six other studies were never submitted for review, although, in three instances, the investigators still hoped to do so. For the remaining five studies, it was unclear whether the authors tried to submit their findings for publication. Explanations that the investigators gave for not submitting manuscripts included that they did not think the findings were interesting enough to warrant publication, that they got distracted by other obligations or that they had practical problems."

p17 (Limitations): "(1) We were not able to obtain unpublished data for 2 of the 13 (15.4%) unpublished studies. In one case, the investigator was willing, but data collected in the 1980s were no longer available. However, in the other case, the investigator was reluctant to share her data, fearing that doing so would jeopardize her chances for independent publication."

FIXTURE FLAG — SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE: Every unpublished study effect size in Figs 2–7 (rows F2-22..F2-27, F3-07..F3-08, F4-17..F4-20, F5-14..F5-15, F6-17..F6-19, F7-11..F7-12) and every "Unpublished" pooled estimate (A1-UNPUB, A1a-UNPUB, A1b-UNPUB, A2-UNPUB, A3-UNPUB, A4-UNPUB, APLAC-UNPUB) is computed from author-supplied unpublished data that exists ONLY in this paper. Some rows additionally have name and/or all values withheld in the figures at the investigators' request. These cannot be verified against any public source; per the Data Availability Statement the raw data must be requested from the original investigators.

======================================================================
## 5. CONTRADICTIONS / ODDITIES

C1. TABLE 1 SECTION-HEADER ERROR (verified via text coordinates): The Table 1 continuation on page 11 carries the section header "PUBLISHED" (y=670.6, same slot as pages 9-10) even though every study row on page 11 (rows 46 Clark through 57 Zlotnick) belongs to the UNPUBLISHED section, which began on page 10 (header "UNPUBLISHED" at row 43). A reader consulting only page 11 would mislabel 12 unpublished grants as published.

C2. CLARK ROW EMPTY: Table 1 row 46 (Clark, R01MH062054d) has no entry in "Study comparison(s)", "PT type(s)" or any quality-rating column (verified by coordinate reconstruction: only PI and grant number are printed). All other unpublished rows list comparisons; even Gottlieb (data not retained) lists "PT vs ADM / PT+ADM vs ADM". UNRESOLVED whether the omission is intentional (refused data) or an error.

C3. UNPUBLISHED QUALITY-RATING DENOMINATOR: p16 says "We were not able to retrieve quality ratings for three of the unpublished studies," implying 13-3 = 10 rated; but the reported percentages imply a denominator of 9 (22.2% = 2/9; 55.6% = 5/9; 77.8% = 7/9) and "10 of the 53" implies 44 published studies + 9 unpublished rated = 53. Consistent only if one unpublished study (presumably Gottlieb, excluded from main analyses) is dropped before subtracting the 3 without ratings (12-3 = 9). AMBIGUOUS; not resolvable from the PDF.

C4. t-TEST DEGREES OF FREEDOM: p16 reports t(54) = 0.79 comparing mean participants per condition between unpublished and published studies. With 13 unpublished + 42 published grants = 55, a two-sample t-test would have df = 53 (df = 54 would require 56 studies). Also "Only about 75% as many patients" vs 31.9/41.9 = 76.1%. Minor internal inconsistency; UNRESOLVED.

C5. Δg% = -456% (Table 2, PT vs. antidepressant medication): arithmetically explainable (point estimate moved from g = 0.01 to g = -0.05; -0.07/0.015 at 5-decimal precision) but an extreme-looking value; verify sign conventions when auditing.

C6. Δg vs Δg% precision: Table 2 note says differences were "calculated using 5 decimals," so printed pairs like Δg = -0.04 / -4% (A1a) and Δg = -0.04 / -24% (A2) are not reproducible from the 2-decimal printed g values alone.

C7. DECIMAL-COMMA TYPO: "84,6%" (p7) uses a comma where the rest of the text uses points. Also grammar error in Data Availability: "we obtained it this data" (p1).

C8. CONTROL-CONDITION ABBREVIATION INCONSISTENCY: Table 1 legend defines "CTRL-PLAC = pill-placebo control condition", but the forest plots label the same condition "CTRL-NS(PLAC)" and Fig 2/Fig 4 captions define "CTRL-NS(PLAC) = pill-placebo control condition" while also defining "CTRL-NS = non-specific control condition (psychological placebo)". The Fig 2 caption's first definition reads "CTRL-NS = non-specific control condition (psychological placebo); CTRL-NS(PLAC) = pill-placebo control condition" — same stem used for two different conditions.

C9. HIDDEN UNPUBLISHED ROWS / WEIGHT GAPS: In Figs 2, 3, 4, 6 and 7, one or two unpublished studies appear as completely blank rows (no name, no statistics), and some rows show statistics but no study name; visible relative weights therefore do not sum to 100% within the Unpublished subgroup (e.g., Fig 2: visible 84.36%; Fig 4: 91.90%; Fig 6: 55.47%; Fig 7: 78.94%). The identities of the anonymous rows cannot be resolved from the PDF (candidate unpublished grants: Battle, Gilliam, Miller, Monk, Stuart x2, Zlotnick). UNRESOLVED by design.

C10. GRANT NUMBER FORMAT: Row 31 Reynolds grant printed "R01MH37869" (5-digit serial) whereas all other MH grants use 6 digits. Also footnote b (row 7): "Grant number reported incorrectly in the published article, but confirmed with authors"; footnote c (row 33): "Grant number omitted in published article but confirmed with authors".

C11. TWO GRANTS -> TWO PUBLISHED RCTs EACH: Table 1 rows 29 (Murphy R01MH032756: refs [59] and [60]) and 40 (Thompson R01MH037196: refs [70] and [71]) each contain two published trials, so 42 published grants correspond to 44 published studies. This reconciles quality percentages (18.2% = 8/44 etc.) but is easy to miscount as 42 studies.

C12. FIGURE ORDER ON PAGE 15: The two raster images embedded on page 15 are stored in reverse order relative to caption order (first stored image contains the Fig 7 comparison PT1+ADM vs ADM; second contains Fig 6's PT1 vs ADM). Content, not stored order, was used for figure assignment. (Layout on the rendered page presumably matches captions; extraction artifact only — noted so auditors do not mismap.)

C13. STUDY [39] (Frank R21MH061948): counted as published but "reported the grant-funded trial's outcomes only in aggregate with outcomes of other trials" (p11); its data were requested from the PI, and it appears in Fig 5 only via unpublished-style author-supplied data? UNRESOLVED which Fig 5 row (if any) carries it — the paper says a sensitivity analysis recoded it as unpublished (rates 74.5%/25.5%, p12) but its main-analysis placement among Fig 5 published rows is not explicitly identified.

C14. S1 TABLE NOT IN PDF: All sensitivity-analysis numeric results and the treatment-control-subtype pools (except the pill-placebo numbers quoted in text, p14) reside in S1 Table (DOCX supplement), which is not part of this 23-page PDF. Pill-placebo published k=5 vs the 5 CTRL-NS(PLAC)-labelled rows in Figs 2/4 (Barber, DeRubeis, Jarrett + Thase unpub) — only 3 published rows are labelled CTRL-NS(PLAC) in Fig 2/4 plus "Combined"-comparison rows; exact composition of the k=5 published pill-placebo pool is AMBIGUOUS from this PDF.

======================================================================
## 6. META

Citation (verbatim, p1): "Citation: Driessen E, Hollon SD, Bockting CLH, Cuijpers P, Turner EH (2015) Does Publication Bias Inflate the Apparent Efficacy of Psychological Treatment for Major Depressive Disorder? A Systematic Review and Meta-Analysis of US National Institutes of Health-Funded Trials. PLoS ONE 10(9): e0137864. doi:10.1371/journal.pone.0137864"
Journal: PLOS ONE 10(9): e0137864. DOI: 10.1371/journal.pone.0137864
Editor: Lin Lu, Peking University, CHINA. Received: February 17, 2015; Accepted: August 22, 2015; Published: September 30, 2015.
Total PDF pages: 23 (printed folios "1 / 23" ... "23 / 23" match PDF pages 1-23; 1-based PDF page = printed page).

Page map:
- p1: Title, authors, abstract (Background/Methods and Findings partial), citation block, Data Availability Statement
- p2: Abstract conclusion; Introduction (Turner 2008 figures: 0.41 [0.36~0.45] -> 0.31 [0.27~0.35], 24% reduction; Cuijpers 2010: 0.67 [0.60~0.75] -> 0.42 [0.33~0.51], 37% reduction)
- p3-4: Methods (grant search; matching grants to articles; assessment of study publication bias)
- p5: Methods (effect size computation, Hedges' g, random effects, CMA 2.2.064, Q/I2, subgroup Q-test)
- p6: Methods (ranking PT comparisons; quality criteria 1-2 of 4)
- p7: Methods (criteria 3-4); Results (grant flow: 4073 -> 232 -> 56 -> 57; publication rates 42/55 vs 13/55)
- p8: Fig 1 (PRISMA flow chart; raster image: 4073 identified; 3841 excluded; 232 possibly meeting; 176 excluded [No RCT 40; No MDD 61; No psychotherapy (contrast) 16; Combination 19; Duplicate listing 16; Duplicate grant for multi-site study 22; Adolescent study 2]; Included 56; +1 from literature search; Included 57; publication 42 / no publication 13 / never started 2); caption + Clark/Gottlieb text
- p9: Table 1 rows 1-20 (PUBLISHED)
- p10: Table 1 rows 21-45 (PUBLISHED through 42; UNPUBLISHED header + rows 43-45)
- p11: Table 1 rows 46-57 + footnotes/legend (continuation header erroneously "PUBLISHED"); text: totals 4581+839=5420
- p12: Sensitivity 74.5%/25.5%; Table 2 (all 18 pooled estimates + Qbetw tests); machine-readable text
- p13: Fig 2 (raster) + caption; text for A1/A1a/A1b; Fig 3 (raster) + caption
- p14: Fig 4 (raster) + caption; pill-placebo text (S1 Table); PT vs PT text; Fig 5 (raster) + caption
- p15: Fig 6 (raster) + caption; PT vs ADM text; combined-treatment text begins; Fig 7 (raster) + caption
- p16: Combined-treatment text ends; Reasons for non-publication; Quality of included studies; Discussion begins (binomial CI 13%-37%; Turner 23/74 = 31.1%, CI 21%-43%; 0.13 vs 0.07 SD adjustments)
- p17: Discussion (outcome reporting bias limitation; limitations 1-4 begin)
- p18: Discussion (limitations 5-11; non-submission discussion; NIH Public Access Policy)
- p19: Conclusion; Supporting Information (S1 Table description, DOCX); Author Contributions; References 1-12
- p20: References 13-27 (approx)
- p21: References (cont.)
- p22: References (cont.)
- p23: References end (final printed folio 23 / 23)

Figures/tables inventory: Fig 1 (p8, raster), Table 1 (pp9-11, text), Table 2 (p12, text), Fig 2 (p13, raster), Fig 3 (p13, raster), Fig 4 (p14, raster), Fig 5 (p14, raster), Fig 6 (p15, raster), Fig 7 (p15, raster), S1 Table (referenced only; DOCX supplement, not in PDF).

Machine-readability: All body text and Tables 1-2 are extractable text (pdfminer; column order scrambled in naive extraction — coordinate-based reconstruction used and verified). All figures (1-7) are raster JPEGs read visually; figure numbers in forest plots use decimal commas.
