# Pass A — Gold-standard truth extraction (raw)

Paper: Nissen SE, Wolski K. Effect of Rosiglitazone on the Risk of Myocardial Infarction and Death from Cardiovascular Causes. N Engl J Med 2007;356:2457-71.
Source PDF: `corpus/gold/nissen-2007-rosiglitazone/source/2457.pdf` (16 pages). All values below are VERBATIM AS PRINTED in this PDF (truth = AS_PUBLISHED in this artifact). Page numbers are 1-based pages of THIS PDF; print journal pages 2457-2471 map to PDF pages 1-15; PDF page 16 is an appended NEJM correction notice.

**CRITICAL PROVENANCE FINDING (overrides the working assumption that this file is the pre-erratum print version):** this PDF carries the POST-erratum (corrected) values at every erratum-affected location, and PDF page 16 IS the erratum itself (N Engl J Med 2007;357:100). Every page carries the stamp "Downloaded from www.nejm.org on July 30, 2007"; PDF metadata modDate 2007-07-30 (creationDate 2007-06-12). See Section 4 for the location-by-location verification. Extraction below is nonetheless strictly as-printed in this PDF.

---

## 1. ANALYSES

Format: `analysis_id | outcome | subgroup | effect_measure | model | n_trials_reported | pooled_effect | ci_lower | ci_upper | p_value | source_page | source`

All pooled results use the Peto odds-ratio method with a fixed-effects model (Methods, PDF p3: odds ratios and 95% CIs "calculated with the use of the Peto method"; heterogeneity tested with Cochran's Q; fixed-effects justified by Q-statistic P > 0.10; trials with no events in either group excluded from analyses; software: Comprehensive Meta-Analysis v2.2, Biostat). Per-analysis trial counts are NOT printed next to any pooled estimate; Methods (PDF p2) states 38 trials reported at least one MI and 23 reported at least one CV death.

A01 | Myocardial infarction | Overall (all 42 trials; zero-event trials excluded) | Peto OR | fixed-effects | NOT_PRINTED (38 per Methods) | 1.43 | 1.03 | 1.98 | P = 0.03 | 1, 3, 12, 13 | Abstract; Results text; Table 4 "Overall"; Table 5 "Combined comparator drugs"
A02 | Death from cardiovascular causes | Overall | Peto OR | fixed-effects | NOT_PRINTED (23 per Methods) | 1.64 | 0.98 | 2.74 | P = 0.06 | 1, 3, 12, 13 | Abstract; Results text; Table 4 "Overall"; Table 5 "Combined comparator drugs"
A03 | Myocardial infarction | Small trials combined | Peto OR | fixed-effects | NOT_PRINTED (36 derivable from Table 3) | 1.45 | 0.88 | 2.39 | 0.15 | 12 | Table 4
A04 | Myocardial infarction | DREAM (single trial, shown separately) | Peto OR | — | 1 | 1.65 | 0.74 | 3.68 | 0.22 | 12 | Table 4
A05 | Myocardial infarction | ADOPT (single trial, shown separately) | Peto OR | — | 1 | 1.33 | 0.80 | 2.21 | 0.27 | 12 | Table 4
A06 | Death from cardiovascular causes | Small trials combined | Peto OR | fixed-effects | NOT_PRINTED (21 derivable from Table 3) | 2.40 | 1.17 | 4.91 | 0.02 | 12 | Table 4
A07 | Death from cardiovascular causes | DREAM | Peto OR | — | 1 | 1.20 | 0.52 | 2.78 | 0.67 | 12 | Table 4
A08 | Death from cardiovascular causes | ADOPT | Peto OR | — | 1 | 0.80 | 0.17 | 3.86 | 0.78 | 12 | Table 4
A09 | Myocardial infarction | Comparator subgroup: Metformin | Peto OR | fixed-effects | NOT_PRINTED | 1.14 | 0.70 | 1.86 | 0.59 | 13 | Table 5
A10 | Myocardial infarction | Comparator subgroup: Sulfonylurea | Peto OR | fixed-effects | NOT_PRINTED | 1.24 | 0.78 | 1.98 | 0.36 | 13 | Table 5
A11 | Myocardial infarction | Comparator subgroup: Insulin | Peto OR | fixed-effects | NOT_PRINTED | 2.78 | 0.58 | 13.3 | 0.20 | 13 | Table 5 (upper CI printed "13.3", not "13.30")
A12 | Myocardial infarction | Comparator subgroup: Placebo | Peto OR | fixed-effects | NOT_PRINTED | 1.80 | 0.95 | 3.39 | 0.07 | 13 | Table 5
A13 | Death from cardiovascular causes | Comparator subgroup: Metformin | Peto OR | fixed-effects | NOT_PRINTED | 1.13 | 0.34 | 3.71 | 0.84 | 13 | Table 5
A14 | Death from cardiovascular causes | Comparator subgroup: Sulfonylurea | Peto OR | fixed-effects | NOT_PRINTED | 1.42 | 0.60 | 3.33 | 0.43 | 13 | Table 5
A15 | Death from cardiovascular causes | Comparator subgroup: Insulin | Peto OR | fixed-effects | NOT_PRINTED | 5.37 | 0.51 | 56.52 | 0.16 | 13 | Table 5
A16 | Death from cardiovascular causes | Comparator subgroup: Placebo | Peto OR | fixed-effects | NOT_PRINTED | 1.22 | 0.64 | 2.34 | 0.55 | 13 | Table 5
A17 | Death from any cause | Overall (analysis "not prespecified") | OR (method not restated; Peto per Methods) | fixed-effects | NOT_PRINTED | 1.18 | 0.89 | 1.55 | P = 0.24 | 11 | Results text only (no table)

Additional printed statistics tied to analyses:
- Heterogeneity (Results text, PDF p11): "The heterogeneity P values were 0.53 for myocardial infarction and 0.68 for death from cardiovascular causes across subgroups."
- Event totals (Results text, PDF p3): 86 MIs rosiglitazone vs 72 control; 39 CV deaths rosiglitazone vs 22 control.
- PROACTIVE (pioglitazone; context only, not a pooled analysis of this paper, PDF p13): primary end point HR 0.90, P = 0.095; secondary end point HR 0.84, P = 0.027.

---

## 2. STUDY_LABELS

Format: `label_verbatim | appears_in | source_pages`

Notes: In Table 1 each study ID is printed with reference-citation superscripts fused into the text layer (e.g. "49653/011" carries superscript "5-7", rendered "49653/0115-7"); labels below are the IDs with superscripts stripped, with the raw superscript noted. Tables 1 and 2 are printed rotated 90 degrees on the page.

49653/011 | TABLE1 (as "49653/011" + sup 5-7); TABLE2; TABLE3 | 4, 6, 10
49653/020 | TABLE1 (sup 5,6); TABLE2; TABLE3 | 4, 7, 10
49653/024 | TABLE1 (sup 5,6,8); TABLE2; TABLE3 | 4, 7, 10
49653/093 | TABLE1 (sup 5,6,9); TABLE2; TABLE3 | 4, 7, 10
49653/094 | TABLE1 (sup 5,6,9,10); TABLE2; TABLE3 | 4, 7, 10
100684 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 6, 10
49653/143 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 6, 10
49653/211 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 6, 10
49653/284 | TABLE1 (sup 5,11); TABLE2; TABLE3 | 4, 6, 10
712753/008 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 6, 10
AVM100264 | TABLE1 (sup 5; registry NCT00359112); TABLE2; TABLE3 | 4, 6, 10
BRL 49653C/185 | TABLE1 (sup 5, printed "BRL 49653C/185"); TABLE3 (same) — TABLE2 prints "BRL49653C/185" with NO space | 4, 6, 10
BRL 49653/334 | TABLE1 (sup 5); TABLE2 ("BRL 49653/334"); TABLE3 | 4, 6, 10
BRL 49653/347 | TABLE1 (sup 5; registry NCT00054782); TABLE2; TABLE3 | 4, 6, 10
49653/015 | TABLE1 (sup 5,12); TABLE2; TABLE3 | 4, 6, 10
49653/079 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 7, 10
49653/080 | TABLE1 (sup 5,13); TABLE2; TABLE3 | 4, 7, 10
49653/082 | TABLE1 (sup 5,14); TABLE2; TABLE3 | 4, 7, 10
49653/085 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 7, 10
49653/095 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 7, 10
49653/097 | TABLE1 (sup 5); TABLE2; TABLE3 | 4, 7, 10
49653/125 | TABLE1 (sup 5,15); TABLE2; TABLE3 | 5, 7, 10
49653/127 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 7, 10
49653/128 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
49653/134 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
49653/135 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
49653/136 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
49653/145 | TABLE1 (sup 5,16); TABLE2; TABLE3 | 5, 8, 10
49653/147 | TABLE1 (sup 5,17); TABLE2; TABLE3 | 5, 8, 10
49653/162 | TABLE1 (sup 5,18); TABLE2; TABLE3 | 5, 8, 10
49653/234 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
49653/330 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
49653/331 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 9, 10
49653/137 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 9, 10
SB-712753/002 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 9, 10
SB-712753/003 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 8, 10
SB-712753/007 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 9, 10
SB-712753/009 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 9, 10
49653/132 | TABLE1 (sup 5,19); TABLE2; TABLE3 | 5, 9, 10
AVA100193 | TABLE1 (sup 5); TABLE2; TABLE3 | 5, 9, 11
DREAM | TEXT (expanded "Diabetes Reduction Assessment with Ramipiril and Rosiglitazone Medication (DREAM) NCT00095654" — "Ramipiril" as printed); TABLE1 ("DREAM" + sup 20, NCT00095654); TABLE2; TABLE3; TABLE4 | 1(footnote via abstract? no—first at 2), 2, 3, 5, 9, 11, 12
ADOPT | TEXT (expanded "the A Diabetes Outcome Prevention Trial (ADOPT)", registry NCT00279045); TABLE1 ("ADOPT" + sup 21, NCT00279045); TABLE2; TABLE3; TABLE4 | 2, 3, 5, 9, 11, 12
RECORD | TEXT only (Rosiglitazone Evaluated for Cardiac Outcomes and Regulation of Glycaemia in Diabetes; ongoing trial, not pooled) | 13
PROACTIVE | TEXT only ("Prospective Pioglitazone Clinical Trial in Macrovascular Events (PROACTIVE)"; pioglitazone context, not pooled) | 13

Trial-category groupings as printed in Table 1: "Trials included in original registration package" (5 trials); "Additional phase 2, 3, and 4 efficacy trials" (35 trials); "Recently published large, prospective, randomized trials" (DREAM, ADOPT).

---

## 3. PUBLISHED_EFFECTS

Format: `effect_id | analysis_id_or_table | row_kind | label | n_rosi | n_control | mi_events_rosi | mi_events_control | cvdeath_events_rosi | cvdeath_events_control | or_and_ci_if_printed | source_page | source_table | certainty | note`

### 3a. Table 1 rows (enrollment only; Table 1 prints no events and no ORs; comma formatting as printed)

T1-01 | TABLE1 | STUDY | 49653/011 | 357 | 176 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 24 wk; Rosiglitazone vs Placebo
T1-02 | TABLE1 | STUDY | 49653/020 | 391 | 207 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 52 wk; Rosiglitazone vs Glyburide
T1-03 | TABLE1 | STUDY | 49653/024 | 774 | 185 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; Rosiglitazone vs Placebo
T1-04 | TABLE1 | STUDY | 49653/093 | 213 | 109 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone with or without metformin" vs Metformin
T1-05 | TABLE1 | STUDY | 49653/094 | 232 | 116 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and metformin" vs Metformin
T1-06 | TABLE1 | SUBGROUP_TOTAL | Subtotal (original registration package) | 1,967 | 793 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Matches Methods text (PDF p2): "1967 ... 793"
T1-07 | TABLE1 | STUDY | 100684 | 43 | 47 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 52 wk; "Rosiglitazone and glyburide" vs Glyburide
T1-08 | TABLE1 | STUDY | 49653/143 | 121 | 124 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 24 wk; "Rosiglitazone and glyburide" vs Glyburide
T1-09 | TABLE1 | STUDY | 49653/211 | 110 | 114 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 52 wk; "Rosiglitazone and usual care" vs "Usual care"
T1-10 | TABLE1 | STUDY | 49653/284 | 382 | 384 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 24 wk; "Rosiglitazone and metformin" vs Metformin
T1-11 | TABLE1 | STUDY | 712753/008 | 284 | 135 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 48 wk; "Rosiglitazone and metformin" vs Metformin
T1-12 | TABLE1 | STUDY | AVM100264 | 294 | 302 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 52 wk; "Rosiglitazone and metformin" vs "Metformin and sulfonylurea†" (†= glyburide or gliclazide); NCT00359112
T1-13 | TABLE1 | STUDY | BRL 49653C/185 | 563 | 142 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 32 wk; "Rosiglitazone with or without metformin" vs "Usual care with or without metformin"
T1-14 | TABLE1 | STUDY | BRL 49653/334 | 278 | 279 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 52 wk; Rosiglitazone vs Placebo
T1-15 | TABLE1 | STUDY | BRL 49653/347 | 418 | 212 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 4, 24 wk; "Rosiglitazone and insulin" vs Insulin; NCT00054782
T1-16 | TABLE1 | STUDY | 49653/015 | 395 | 198 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 24 wk; "Rosiglitazone and sulfonylurea‡" vs "Sulfonylurea‡" (‡= glyburide, gliclazide, or glipizide)
T1-17 | TABLE1 | STUDY | 49653/079 | 203 | 106 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone with or without glyburide" vs Glyburide
T1-18 | TABLE1 | STUDY | 49653/080 | 104 | 99 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 156 wk; Rosiglitazone vs Glyburide
T1-19 | TABLE1 | STUDY | 49653/082 | 212 | 107 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and insulin" vs Insulin
T1-20 | TABLE1 | STUDY | 49653/085 | 138 | 139 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and insulin" vs Insulin
T1-21 | TABLE1 | STUDY | 49653/095 | 196 | 96 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and insulin" vs Insulin
T1-22 | TABLE1 | STUDY | 49653/097 | 122 | 120 | NA | NA | NA | NA | NA | 4 | Table 1 | KNOWN | Phase 3, 156 wk; Rosiglitazone vs Glyburide
T1-23 | TABLE1 | STUDY | 49653/125 | 175 | 173 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and sulfonylurea§" vs "Sulfonylurea§" (§= glyburide, glipizide, gliclazide, chlorpropamide, glimepiride, or tolbutamide)
T1-24 | TABLE1 | STUDY | 49653/127 | 56 | 58 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and glyburide" vs Glyburide
T1-25 | TABLE1 | STUDY | 49653/128 | 39 | 38 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 28 wk; Rosiglitazone vs Placebo
T1-26 | TABLE1 | STUDY | 49653/134 | 561 | 276 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 28 wk; Rosiglitazone vs Placebo (Table 2 shows background Gly/Met in both arms)
T1-27 | TABLE1 | STUDY | 49653/135 | 116 | 111 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 104 wk; "Rosiglitazone and glipizide" vs Glipizide
T1-28 | TABLE1 | STUDY | 49653/136 | 148 | 143 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; Rosiglitazone vs Placebo (Table 2 shows background Su/insulin both arms; renal-failure population)
T1-29 | TABLE1 | STUDY | 49653/145 | 231 | 242 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and gliclazide" vs Gliclazide
T1-30 | TABLE1 | STUDY | 49653/147 | 89 | 88 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and sufonylurea¶" vs "Sulfonylurea¶" — "sufonylurea" typo AS PRINTED in rosiglitazone cell (¶= type of sulfonylurea unspecified)
T1-31 | TABLE1 | STUDY | 49653/162 | 168 | 172 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and glyburide" vs Glyburide
T1-32 | TABLE1 | STUDY | 49653/234 | 116 | 61 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 26 wk; "Rosiglitazone and glimepiride" vs Glimepiride
T1-33 | TABLE1 | STUDY | 49653/330 | 1,181 | 382 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 52 wk; Rosiglitazone vs Placebo (psoriasis trial). NOTE: Table 3 prints 1172 / 377 for the same trial — see Section 5
T1-34 | TABLE1 | STUDY | 49653/331 | 706 | 325 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 52 wk; Rosiglitazone vs Placebo (psoriasis trial)
T1-35 | TABLE1 | STUDY | 49653/137 | 204 | 185 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 32 wk; "Rosiglitazone and metformin" vs "Glyburide and metformin"
T1-36 | TABLE1 | STUDY | SB-712753/002 | 288 | 280 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 24 wk; "Rosiglitazone and metformin" vs Metformin
T1-37 | TABLE1 | STUDY | SB-712753/003 | 254 | 272 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 32 wk; "Rosiglitazone and metformin" vs Metformin
T1-38 | TABLE1 | STUDY | SB-712753/007 | 314 | 154 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 32 wk; "Rosiglitazone with or without metformin" vs Metformin
T1-39 | TABLE1 | STUDY | SB-712753/009 | 162 | 160 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 24 wk; "Rosiglitazone, metformin, and insulin" vs Insulin
T1-40 | TABLE1 | STUDY | 49653/132 | 442 | 112 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 2, 24 wk; "Rosiglitazone and sulfonylurea‖" vs "Sulfonylurea‖" (‖= glyburide, glipizide, gliclazide, chlorpropamide, gliquidone, or tolbutamide)
T1-41 | TABLE1 | STUDY | AVA100193 | 394 | 124 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 2, 24 wk; Rosiglitazone vs Placebo (Alzheimer's trial)
T1-42 | TABLE1 | SUBGROUP_TOTAL | Subtotal (additional phase 2, 3, and 4 efficacy trials) | 9,507 | 5,960 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | POST-ERRATUM values (pre-erratum print was 9,502 / 5,961 per the correction notice on PDF p16). Matches Methods text "9507 ... 5960" (PDF p2)
T1-43 | TABLE1 | STUDY | DREAM | 2,635 | 2,634 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 156 wk; Rosiglitazone vs Placebo; NCT00095654
T1-44 | TABLE1 | STUDY | ADOPT | 1,456 | 2,895 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | Phase 3, 208 wk; Rosiglitazone vs "Metformin or glyburide"; NCT00279045
T1-45 | TABLE1 | OVERALL_TOTAL | Total | 15,565 | 12,282 | NA | NA | NA | NA | NA | 5 | Table 1 | KNOWN | POST-ERRATUM values; match Methods text (PDF p2) "15,565 ... 12,282"

### 3b. Table 3 rows (2x2 event data; the primary analysis input; no per-trial ORs are printed anywhere in this paper — there is no forest plot)

T3-01 | A01/A02 (Table 3) | STUDY | 49653/011 | 357 | 176 | 2 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN | Zero cells in control arm (both outcomes)
T3-02 | A01/A02 (Table 3) | STUDY | 49653/020 | 391 | 207 | 2 | 1 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0 — contributes to MI analysis only
T3-03 | A01/A02 (Table 3) | STUDY | 49653/024 | 774 | 185 | 1 | 1 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-04 | A01/A02 (Table 3) | STUDY | 49653/093 | 213 | 109 | 0 | 1 | 0 | 0 | NA | 10 | Table 3 | KNOWN | MI zero in rosi arm; CV death 0/0
T3-05 | A01/A02 (Table 3) | STUDY | 49653/094 | 232 | 116 | 1 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-06 | A01/A02 (Table 3) | STUDY | 100684 | 43 | 47 | 0 | 1 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-07 | A01/A02 (Table 3) | STUDY | 49653/143 | 121 | 124 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-08 | A01/A02 (Table 3) | STUDY | 49653/211 | 110 | 114 | 5 | 2 | 3 | 2 | NA | 10 | Table 3 | KNOWN | CHF-population trial; highest small-trial event counts
T3-09 | A01/A02 (Table 3) | STUDY | 49653/284 | 382 | 384 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-10 | A01/A02 (Table 3) | STUDY | 712753/008 | 284 | 135 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-11 | A01/A02 (Table 3) | STUDY | AVM100264 | 294 | 302 | 0 | 1 | 2 | 1 | NA | 10 | Table 3 | KNOWN |
T3-12 | A01/A02 (Table 3) | STUDY | BRL 49653C/185 | 563 | 142 | 2 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-13 | A01/A02 (Table 3) | STUDY | BRL 49653/334 | 278 | 279 | 2 | 1 | 0 | 1 | NA | 10 | Table 3 | KNOWN |
T3-14 | A01/A02 (Table 3) | STUDY | BRL 49653/347 | 418 | 212 | 2 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-15 | A01/A02 (Table 3) | STUDY | 49653/015 | 395 | 198 | 2 | 1 | 2 | 0 | NA | 10 | Table 3 | KNOWN |
T3-16 | A01/A02 (Table 3) | STUDY | 49653/079 | 203 | 106 | 1 | 1 | 1 | 1 | NA | 10 | Table 3 | KNOWN |
T3-17 | A01/A02 (Table 3) | STUDY | 49653/080 | 104 | 99 | 1 | 2 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-18 | A01/A02 (Table 3) | STUDY | 49653/082 | 212 | 107 | 2 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-19 | A01/A02 (Table 3) | STUDY | 49653/085 | 138 | 139 | 3 | 1 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-20 | A01/A02 (Table 3) | STUDY | 49653/095 | 196 | 96 | 0 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN | MI 0/0 — EXCLUDED from MI analysis (zero events both arms); contributes to CV-death analysis
T3-21 | A01/A02 (Table 3) | STUDY | 49653/097 | 122 | 120 | 0 | 1 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-22 | A01/A02 (Table 3) | STUDY | 49653/125 | 175 | 173 | 0 | 1 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-23 | A01/A02 (Table 3) | STUDY | 49653/127 | 56 | 58 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-24 | A01/A02 (Table 3) | STUDY | 49653/128 | 39 | 38 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-25 | A01/A02 (Table 3) | STUDY | 49653/134 | 561 | 276 | 0 | 2 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-26 | A01/A02 (Table 3) | STUDY | 49653/135 | 116 | 111 | 2 | 3 | 2 | 1 | NA | 10 | Table 3 | KNOWN |
T3-27 | A01/A02 (Table 3) | STUDY | 49653/136 | 148 | 143 | 1 | 0 | 2 | 0 | NA | 10 | Table 3 | KNOWN |
T3-28 | A01/A02 (Table 3) | STUDY | 49653/145 | 231 | 242 | 1 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-29 | A01/A02 (Table 3) | STUDY | 49653/147 | 89 | 88 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-30 | A01/A02 (Table 3) | STUDY | 49653/162 | 168 | 172 | 1 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-31 | A01/A02 (Table 3) | STUDY | 49653/234 | 116 | 61 | 0 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | ALL cells zero — EXCLUDED from both MI and CV-death analyses
T3-32 | A01/A02 (Table 3) | STUDY | 49653/330 | 1172 | 377 | 1 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN | N DIFFERS from Table 1 (1,181 / 382) — see Section 5
T3-33 | A01/A02 (Table 3) | STUDY | 49653/331 | 706 | 325 | 0 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN | MI 0/0 — EXCLUDED from MI analysis; contributes to CV-death analysis
T3-34 | A01/A02 (Table 3) | STUDY | 49653/137 | 204 | 185 | 1 | 2 | 0 | 1 | NA | 10 | Table 3 | KNOWN |
T3-35 | A01/A02 (Table 3) | STUDY | SB-712753/002 | 288 | 280 | 1 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-36 | A01/A02 (Table 3) | STUDY | SB-712753/003 | 254 | 272 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-37 | A01/A02 (Table 3) | STUDY | SB-712753/007 | 314 | 154 | 1 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | CV death 0/0
T3-38 | A01/A02 (Table 3) | STUDY | SB-712753/009 | 162 | 160 | 0 | 0 | 0 | 0 | NA | 10 | Table 3 | KNOWN | ALL cells zero — EXCLUDED from both analyses
T3-39 | A01/A02 (Table 3) | STUDY | 49653/132 | 442 | 112 | 1 | 0 | 1 | 0 | NA | 10 | Table 3 | KNOWN |
T3-40 | A01/A02 (Table 3) | STUDY | AVA100193 | 394 | 124 | 1 | 0 | 1 | 0 | NA | 11 | Table 3 (Continued) | KNOWN |
T3-41 | A01/A02 (Table 3) | STUDY | DREAM | 2635 | 2634 | 15 | 9 | 12 | 10 | NA | 11 | Table 3 (Continued) | KNOWN |
T3-42 | A01/A02 (Table 3) | STUDY | ADOPT | 1456 | 2895 | 27 | 41 | 2 | 5 | NA | 11 | Table 3 (Continued) | KNOWN |
T3-43 | A01/A02 (Table 3) | OVERALL_TOTAL | Total | NOT_PRINTED | NOT_PRINTED | 86 | 72 | 39 | 22 | NA | 11 | Table 3 (Continued) | KNOWN | Total row prints event counts only, no patient totals. Column sums of printed n: 15,556 rosi / 12,277 control (differ from Table 1 totals — see Section 5). Event sums verify: 86/72/39/22 exact

Zero-event exclusion summary (per Methods rule "Trials in which patients had no adverse cardiovascular events in either group were excluded from analyses", PDF p3):
- Excluded from BOTH analyses (all four cells zero): 49653/234, SB-712753/009.
- Excluded from MI analysis only (MI 0/0, has CV death): 49653/095, 49653/331.
- Excluded from CV-death analysis only (CV death 0/0, has MI): 49653/020, 49653/024, 49653/093, 100684, 49653/143, 49653/284, 712753/008, BRL 49653C/185, BRL 49653/347, 49653/080, 49653/097, 49653/125, 49653/127, 49653/128, 49653/147, SB-712753/003, SB-712753/007, 49653/132 (18 trials + the 2 all-zero trials = 19 small trials with CV death 0/0).
- Resulting analysis sets (derived, verified arithmetically): MI = 36 small trials + DREAM + ADOPT = 38 (matches Methods "38 reported at least one myocardial infarction"); CV death = 21 small trials + DREAM + ADOPT = 23 (matches Methods "23").
- Additionally, 6 of the 48 eligible trials had no MI or CV death at all and were not included among the 42 (Methods, PDF p2); those 6 trials are not named anywhere in the paper.

### 3c. Table 4 rows (aggregate 2x2 with ORs; "no. of events/total no. (%)" format; comma usage as printed)

T4-01 | A03 | SUBGROUP_TOTAL | Myocardial infarction — Small trials combined | 10,285 | 6106 | 44 | 22 | NA | NA | 1.45 (0.88–2.39), P 0.15 | 12 | Table 4 | KNOWN | Printed "44/10,285 (0.43)" vs "22/6106 (0.36)". POST-ERRATUM values. Denominators = sums of Table 3 n over the 36 small MI-analysis trials (verified exact, using Table 3's 1172/377 for 49653/330)
T4-02 | A04 | SUBGROUP_TOTAL | Myocardial infarction — DREAM | 2,635 | 2634 | 15 | 9 | NA | NA | 1.65 (0.74–3.68), P 0.22 | 12 | Table 4 | KNOWN | Printed "15/2,635 (0.57)" vs "9/2634 (0.34)"
T4-03 | A05 | SUBGROUP_TOTAL | Myocardial infarction — ADOPT | 1,456 | 2895 | 27 | 41 | NA | NA | 1.33 (0.80–2.21), P 0.27 | 12 | Table 4 | KNOWN | Printed "27/1,456 (1.85)" vs "41/2895 (1.42)". Control cell is POST-ERRATUM
T4-04 | A01 | OVERALL_TOTAL | Myocardial infarction — Overall | NOT_PRINTED | NOT_PRINTED | NOT_PRINTED | NOT_PRINTED | NA | NA | 1.43 (1.03–1.98), P 0.03 | 12 | Table 4 | KNOWN | Overall row prints OR/CI/P only, no event/total cells
T4-05 | A06 | SUBGROUP_TOTAL | Death from cardiovascular causes — Small trials combined | 6,845 | 3980 | NA | NA | 25 | 7 | 2.40 (1.17–4.91), P 0.02 | 12 | Table 4 | KNOWN | Printed "25/6,845 (0.36)" vs "7/3980 (0.18)". POST-ERRATUM values. Denominators = sums of Table 3 n over the 21 small CV-death-analysis trials (verified exact)
T4-06 | A07 | SUBGROUP_TOTAL | Death from cardiovascular causes — DREAM | 2,635 | 2634 | NA | NA | 12 | 10 | 1.20 (0.52–2.78), P 0.67 | 12 | Table 4 | KNOWN | Printed "12/2,635 (0.46)" vs "10/2634 (0.38)". Rosi cell is POST-ERRATUM
T4-07 | A08 | SUBGROUP_TOTAL | Death from cardiovascular causes — ADOPT | 1,456 | 2895 | NA | NA | 2 | 5 | 0.80 (0.17–3.86), P 0.78 | 12 | Table 4 | KNOWN | Printed "2/1,456 (0.14)" vs "5/2895 (0.17)". Control cell is POST-ERRATUM
T4-08 | A02 | OVERALL_TOTAL | Death from cardiovascular causes — Overall | NOT_PRINTED | NOT_PRINTED | NA | NA | NOT_PRINTED | NOT_PRINTED | 1.64 (0.98–2.74), P 0.06 | 12 | Table 4 | KNOWN | OR/CI/P only

(Table 5, PDF p13, prints ORs only — no 2x2 cells; its rows are captured as analyses A09–A16 plus the two "Combined comparator drugs" rows which duplicate A01/A02.)

---

## 4. ERRATUM CROSS-CHECK

WebFetch of https://www.nejm.org/doi/full/10.1056/NEJMx070038 returned HTTP 403 Forbidden (paywalled) — the erratum could NOT be fetched from the web. HOWEVER, the full correction notice is physically appended to this PDF as page 16 ("New England Journal of Medicine — CORRECTION ... N Engl J Med 2007;357:100"), so the cross-check was performed against that verbatim in-document text.

The correction notice states corrected ("should have read") values; it names the pre-erratum originals only for the Table 1 subtotals. Location-by-location verification of which side THIS PDF's body carries:

| # | Location (print page) | Erratum: corrected value | Erratum: original value | This PDF body carries |
|---|---|---|---|---|
| 1 | Methods para 1, sentences 5-6 (p. 2458 = PDF p2) | "...38 reported at least one myocardial infarction, and 23 reported at least one death... 15,565 patients ... rosiglitazone, and 12,282 ... comparator" | not stated | CORRECTED (PDF p2 reads 38 / 23 / 15,565 / 12,282) |
| 2 | Methods para 3, last sentence (p. 2458 = PDF p2) | "9507 patients ... rosiglitazone, and 5960 ... comparator" | not stated | CORRECTED (PDF p2 reads 9507 / 5960) |
| 3 | Table 1 subtotal, rosiglitazone (p. 2461 = PDF p5) | 9507 | 9502 | CORRECTED (prints "9,507") |
| 4 | Table 1 subtotal, control (p. 2461 = PDF p5) | 5960 | 5961 | CORRECTED (prints "5,960") |
| 5 | Table 1 total, rosiglitazone (PDF p5) | 15,565 | implied 15,560 (9502+1967+2635+1456) | CORRECTED (prints "15,565") |
| 6 | Table 1 total, control (PDF p5) | 12,282 | implied 12,283 | CORRECTED (prints "12,282") |
| 7 | Table 4 MI small trials, rosiglitazone (p. 2468 = PDF p12) | "44/10,285" | not stated | CORRECTED (prints "44/10,285 (0.43)") |
| 8 | Table 4 MI small trials, control (PDF p12) | "22/6106" | not stated | CORRECTED (prints "22/6106 (0.36)") |
| 9 | Table 4 MI ADOPT, control (PDF p12) | "41/2895 (1.42)" | not stated | CORRECTED (prints "41/2895 (1.42)") |
| 10 | Table 4 CV death small trials, rosiglitazone (PDF p12) | "25/6845 (0.36)" | not stated | CORRECTED (prints "25/6,845 (0.36)" — comma present in table, absent in erratum text) |
| 11 | Table 4 CV death small trials, control (PDF p12) | "7/3980 (0.18)" | not stated | CORRECTED (prints "7/3980 (0.18)") |
| 12 | Table 4 CV death DREAM, rosiglitazone (PDF p12) | "12/2635 (0.46)" | not stated | CORRECTED (prints "12/2,635 (0.46)") |
| 13 | Table 4 CV death ADOPT, control (PDF p12) | "5/2895 (0.17)" | not stated | CORRECTED (prints "5/2895 (0.17)") |

CONCLUSION: this artifact is the WEB (post-erratum) version downloaded 2007-07-30, with the correction notice appended as page 16 — it is NOT the pre-erratum print PDF the corpus notes assumed. The pooled ORs/CIs/P values were unchanged by the erratum (correction affected patient-count denominators and Table 4 event/total cells only). Reconciliation should attach the PRE-erratum print values (e.g., subtotals 9502 / 5961, total 15,560 / 12,283) as the counterpart version, inverting the originally planned direction.

---

## 5. CONTRADICTIONS / ODDITIES (internal to this PDF)

C1 (MAJOR, provenance): The corpus/task premise labels this file the pre-erratum print version, but the body carries post-erratum values at all 13 erratum locations and page 16 is the correction notice itself. See Section 4.
C2 (MAJOR, internal inconsistency): Trial 49653/330 patient counts disagree between tables: Table 1 (PDF p5) prints 1,181 rosiglitazone / 382 control; Table 3 (PDF p10) prints 1172 / 377. Difference is exactly 9 / 5. No footnote explains it. Consequently the Table 3 n-columns sum to 15,556 / 12,277, which does not equal the Table 1 totals 15,565 / 12,282; and the Table 4 "small trials combined" denominators (10,285 / 6106) are built from the Table 3 values (verified exact using 1172/377).
C3 (arithmetic verification, PASS): Table 3 event totals (86 MI rosi, 72 MI control, 39 CV-death rosi, 22 CV-death control) match the column sums of the 42 rows exactly, and match Results text (PDF p3). Table 4 small-trial event counts (44/22 MI; 25/7 CV death) equal Table 3 totals minus DREAM and ADOPT exactly. Trial counts with >=1 event (38 MI, 23 CV death) match Methods exactly.
C4 (typo, as printed): Table 1 row 49653/147 rosiglitazone drug cell prints "Rosiglitazone and sufonylurea¶" — "sufonylurea" missing an "l"; the control cell prints "Sulfonylurea¶" correctly (PDF p5).
C5 (typo, as printed): DREAM is expanded as "Diabetes Reduction Assessment with Ramipiril and Rosiglitazone Medication" in body text (PDF p2) and the Table 1 footnote (PDF p5) — "Ramipiril" (the drug is ramipril; reference 20 on PDF p14 spells "ramipril" correctly). Also ADOPT is expanded as "A Diabetes Outcome Prevention Trial" (PDF p2 and Table 1 footnote, PDF p5); the trial's actual name is "A Diabetes Outcome Progression Trial". Recorded as printed.
C6 (minor): Table 2 row 49653/137, control (Gly/Met) arm: the baseline glycated hemoglobin cell is blank (nothing printed), whereas the rosiglitazone arm prints "NA" (PDF p9). AMBIGUOUS whether blank = NA.
C7 (minor, formatting): Table 4 mixes comma-grouped and ungrouped denominators within the same column ("44/10,285" vs "22/6106"; "15/2,635" vs "9/2634"). Table 1 uses comma grouping (2,635; 1,456); Table 3 uses none (2635; 1456). Erratum text on PDF p16 writes "25/6845" without the comma that Table 4 prints.
C8 (minor, typo in references): Reference 3 (PDF p14) prints "Center for Drug Evaulation and Re-search" ("Evaulation" as printed).
C9 (note): Table 3's Total row has no patient-count totals, only event totals; the patient totals appear only in Table 1.
C10 (note): No per-trial odds ratios and no forest plot appear anywhere in the paper; per-trial effects must be recomputed from the Table 3 2x2 cells. Table 5's insulin MI upper CI is printed "13.3" (3 sig figs) while all other bounds have 2 decimals.
C11 (note): Table 1 lists 49653/134 control as "Placebo" and 49653/136 control as "Placebo", while Table 2 shows both arms of /134 on background Gly/Met ("usual care") and /136 on background Su/insulin. Not a contradiction (add-on placebo designs) but a label-matching hazard for auditers.
C12 (UNRESOLVED — nothing unreadable was encountered; the text layer is complete on all 16 pages. No OCR was needed.)

---

## 6. META

- Citation (as printed): "N Engl J Med 2007;356:2457-71." Steven E. Nissen, M.D., and Kathy Wolski, M.P.H. Issue: june 14, 2007, vol. 356 no. 24. "This article (10.1056/NEJMoa072761) was published at www.nejm.org on May 21, 2007."
- Article DOI: 10.1056/NEJMoa072761. Appended correction: "N Engl J Med 2007;357:100" (= DOI 10.1056/NEJMx070038; DOI not printed on the notice itself).
- Total PDF pages: 16. Print pages 2457-2471 = PDF pp 1-15; PDF p16 = NEJM correction notice (no print page number).
- Footer stamp on every page: "Downloaded from www.nejm.org on July 30, 2007". PDF metadata: creationDate 2007-06-12, modDate 2007-07-30, creator Adobe InDesign CS2.
- Page map:
  - p1 (2457): title, authors, Abstract (overall ORs printed here).
  - p2 (2458): Methods — Analyzed Studies (patient totals; trial-category counts).
  - p3 (2459): Methods (Outcome Measures; Statistical Analysis — Peto, fixed-effects, exclusion rule) + Results (event totals; overall ORs).
  - p4-5 (2460-2461): Table 1 "Clinical Trials of Rosiglitazone in the Meta-Analysis." — rotated 90 degrees, spans 2 pages; footnotes on p5.
  - p6-9 (2462-2465): Table 2 "Doses, Baseline Demographic Characteristics, Study Periods, and Glycated Hemoglobin Levels." — rotated 90 degrees, spans 4 pages; footnotes on p9.
  - p10 (2466): Table 3 "Myocardial Infarctions and Cardiovascular Deaths in Rosiglitazone Trials." rows 49653/011 through 49653/132.
  - p11 (2467): Table 3 (Continued.) — AVA100193, DREAM, ADOPT, Total — plus Results text (Table 5 discussion; heterogeneity Ps; all-cause death OR) and start of Discussion.
  - p12 (2468): Table 4 "Rates of Myocardial Infarction and Death from Cardiovascular Causes." + Discussion text.
  - p13 (2469): Table 5 "Risk of Myocardial Infarction and Death from Cardiovascular Causes for Patients Receiving Rosiglitazone versus Several Comparator Drugs." + Discussion text.
  - p14-15 (2470-2471): disclosures, references 1-34, NEJM boilerplate.
  - p16: CORRECTION notice (N Engl J Med 2007;357:100).
- Encoding: 100% native text layer on all 16 pages; ZERO embedded images (verified programmatically); no figures exist in this article (no forest plot). Tables 1 and 2 are typeset rotated 90 degrees (text extraction order is by rotated cell sequence); Tables 3, 4, 5 are upright. All tables fully machine-readable from the text layer.
- Extraction method: PyMuPDF text layer (pdftoppm/poppler unavailable on host); rotated-table cell order cross-verified with coordinate-sorted word extraction; all sums re-verified arithmetically in Python.
