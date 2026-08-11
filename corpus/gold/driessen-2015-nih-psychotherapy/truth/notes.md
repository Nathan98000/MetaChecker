# Truth notes — driessen-2015-nih-psychotherapy

Driessen E, Hollon SD, Bockting CLH, Cuijpers P, Turner EH (2015). Does Publication Bias
Inflate the Apparent Efficacy of Psychological Treatment for Major Depressive Disorder?
A Systematic Review and Meta-Analysis of US National Institutes of Health-Funded Trials.
PLoS ONE 10(9): e0137864. doi:10.1371/journal.pone.0137864. PMC4589340.
23-page PDF; printed folios "N / 23" match PDF pages 1:1.

## Reconciliation (pass A vs pass B), 2026-08-11

### Construction method

Truth v0 was built from two blind, independent extraction passes over the same source PDF
(`pass-a-raw.md`, `pass-b-raw.md`), reconciled value-by-value into `analyses.csv`,
`study_labels.csv`, `published_effects.csv`, `contradictions.csv`. Body text, Table 1 and
Table 2 are machine-readable PDF text (pass A: PyMuPDF, verified against layout; pass B:
pdfminer with per-line x/y coordinate reconstruction). **Figures 1–7 are embedded raster
images with NO text layer** — every forest-plot number in the truth files was read visually
from page images, independently by each pass (pass A: native-resolution page images ~2220 px
wide plus enlarged crops of every unpublished block and low-confidence cell; pass B:
extracted raster JPEGs with content-based figure assignment). The figures print decimal
commas (CMA European-locale output, e.g. "0,39"); both passes transcribed with decimal
points, noted here and in DRI-CON-09. Reconciliation itself was performed programmatically:
all 113 figure rows were parsed from both raw files and compared field-by-field (g, CI
bounds, relative weight, SE, variance, Z, p, analysis assignment, row kind, source page).

### Numeric disagreements between passes

**ZERO.** Every value was compared and the two passes agree exactly on all of:

- all 113 forest-plot rows across Figs 2–7 (Hedges' g, lower/upper CI, relative weight,
  SE, variance, Z, p for each of the 98 value-bearing rows; both passes independently
  recorded the same 6 rows as fully suppressed and the same 5 rows as values-shown/
  name-withheld);
- all 18 pooled estimates and 6 Q-between contrasts in Table 2 (g, CI, Q, df, I2 and its
  95% CI, Z and significance marks, delta-g, delta-g%, Qbetw, p) including the "-456%" cell;
- all 12 NPT/NComp participant totals and the text-quoted n's (336, 1767, 164, 617, 231,
  1675, 85, 812);
- the pill-placebo pools quoted in text (-0.09 [-0.59~0.40] k=1; 0.34 [0.14~0.53] k=5;
  0.19 [-0.21~0.59] k=6; "45% decrease");
- the hidden-row residual weights derived by subtraction (Fig 2: 15.64 combined for two
  rows; Fig 3: ~33.43; Fig 4: ~8.10; Fig 6: ~44.53; Fig 7: ~21.06);
- publication-rate and quality statistics (13/55 = 23.6%, CI 13%–37%; 42/57 = 73.7% /
  15/57 = 26.3%; 74.5%/25.5% sensitivity; 84,6% [sic]; 10/53 = 18.9%; 18.2% vs 22.2%,
  p = 1.00; 63.6% vs 55.6%, p = .72; 56.8% vs 55.6%, p = 1.00; 38.6% vs 77.8%, p = .06;
  25.0% vs 77.8%, p = .005; 31.9 (SD 22.2) vs 41.9 (SD 42.5), t(54) = 0.79, p = .44;
  totals 4581 + 839 = 5420);
- Fig 1 PRISMA counts (4073; 3841; 232; 176 with subcounts 40/61/16/19/16/22/2; 56; 57;
  42/13/2);
- every source page.

### Structural differences between passes, and how normalized

1. **Q-between contrasts.** Pass A enumerated each published-vs-unpublished subgroup
   contrast as its own analysis row (A04, A08, A12, A16, A20, A24); pass B folded Qbetw/p
   into the source note of the combined ("ALL") row. Normalized to pass A's structure:
   one row per pooled estimate plus a separate `*-QBET` row per contrast
   (effect_measure "Q-between (subgroup contrast)", Qbetw in the `q` column), 6 rows.
2. **Analysis IDs.** Pass A used flat IDs A01–A31; pass B used semantic IDs
   (A1-UNPUB/A1-PUB/A1-ALL, APLAC-*, SENS-*). Pass B's semantic scheme adopted;
   the A→B mapping was applied programmatically when merging figure rows.
3. **Study labels.** Pass A recorded forest-plot labels with Table-1 cross-links and
   listed unpublished Table-1-only identifiers in a summary paragraph; pass B enumerated
   all 57 Table 1 grant/PI rows separately, with verbatim comparison strings and the
   PUBLISHED/UNPUBLISHED section membership. Union adopted: 37 forest-plot published
   labels + 4 named unpublished labels + 4 anonymized-row entries + 1 hidden-rows entry
   + all 57 Table 1 rows, with pass A's cross-links carried into the notes.
4. **source_type vocabulary.** Pass A wrote PAGE_IMAGE, pass B wrote IMAGE. Normalized to
   the README vocabulary `FOREST_PLOT` for all figure rows; the raster/no-text-layer
   provenance is recorded here and in the meta notes instead.
5. **Suppressed-row encoding.** Pass A wrote "(suppressed)", pass B wrote "UNRESOLVED" in
   the value cells. Normalized to empty value cells with certainty=UNRESOLVED and an
   explanatory note stating exactly what is and is not recoverable per row.
6. **Page-15 figure order.** Pass A described the printed layout (Fig 7 above Fig 6);
   pass B described the reversed embedded-image storage order and assigned figures by
   content. Same phenomenon; merged into DRI-CON-10.
7. **Anonymized-row labels.** Pass A "[unnamed unpublished]" vs pass B "[no study name
   printed]" — normalized to "[unnamed unpublished]" in published_effects.csv with
   row_label "(blank study-name cell)".

### Adjudicated conflicts (non-numeric)

1. **Wright, 2014 = study [39]?** Pass A asserted the Fig 5 "Wright, 2014" row is study
   [39] (Frank R21MH061948, the trial published only in aggregate whose per-trial data were
   obtained from the PI). Pass B declined to identify the row, noting the paper never
   explicitly places [39] in Fig 5. Adjudicated as **AMBIGUOUS** (DRI-CON-19): the
   name/year match makes pass A's linkage plausible, and it is recorded in the notes of
   F5-12 and the study_labels rows, but it is not promoted to KNOWN.
2. **"Six" studies absent from all forest plots.** Pass A's oddity O6 lists six published
   Table 1 studies appearing in no figure (Freedland #11, Glick #12, Jacobson #20,
   Miller #26, Simon #34, Talbot #37). Cross-checking pass A's own label/cross-link table
   against both passes' complete figure extractions shows **Manber (#25, ref [55],
   PT+ADM vs CTRL-NS+ADM)** is also absent from every figure — arguably a seventh.
   DRI-CON-04 keeps pass A's six in the description (as extracted) and flags Manber in
   the note as a reconciliation observation. Whether any of these entered only S1 Table
   analyses is UNRESOLVED (S1 Table is a DOCX supplement, not part of this PDF).

### Extra findings adopted per pass

- **From pass A only:** six published studies absent from all forest plots/Table 2
  (DRI-CON-04); partial-anonymization inconsistency incl. the Blum/Fig 5 observation
  (DRI-CON-12); "no failure" outcome label (DRI-CON-20); "Waters, in press" vs 2015
  reference (DRI-CON-21); I2 CI printed "-" for the three k=2 subgroups (DRI-CON-15);
  the 45:14 NPT/NComp split (DRI-CON-16); nonpublication-rate variants incl. the
  prospective "20%" (DRI-CON-17); Fig 2/3 Wright 2005 "Combined" comparison cell
  (DRI-CON-23); the Thase = pill-placebo-unpublished (APLAC-UNPUB) match; the explicit
  cross-representation consistency check (Table 2 = figure diamonds = body text for every
  pooled estimate — no discrepancy anywhere); the page map and S1 Table inventory.
- **From pass B only:** Table 1 page-11 continuation header "PUBLISHED" over unpublished
  rows (DRI-CON-01, coordinate-verified); Clark row entirely empty (DRI-CON-05);
  unpublished quality-rating denominator 10-vs-9 (DRI-CON-06); t(54) vs expected df = 53
  (DRI-CON-07); the 5-decimal delta computation note (DRI-CON-14); CTRL-PLAC vs
  CTRL-NS(PLAC) abbreviation inconsistency (DRI-CON-13); two grants → two published RCTs
  each, 42 grants = 44 studies (DRI-CON-18); pill-placebo k=5 composition ambiguity
  (DRI-CON-22); full 57-row Table 1 enumeration with verbatim comparison strings and
  footnotes b/c; per-figure weight-sum checks (published rows sum 100.00 everywhere except
  Fig 4's 100.01 rounding); the Methods quote on rating unpublished studies from draft
  manuscripts/PI email.

### Unpublished-data provenance (verbatim quotes)

- p1 (Abstract): "For studies that were not published, data were requested from
  investigators and included in the meta-analyses. Thirteen (23.6%) of the 55 funded
  grants that began trials did not result in publications, and two others never started."
- pp1–2 (Data Availability Statement): "All relevant data from published studies and a
  number of the unpublished studies are within the paper and its Supporting Information
  files. We cannot make the data from all unpublished studies publicly available as we
  obtained it this data from third parties (the original investigators of these studies),
  who did not provide us permission to do so. However, others can request this data from
  the relevant investigators. Contact information can be retrieved from
  "http://projectreporter.nih.gov/reporter.cfm" by entering the relevant grant number
  listed in Table 1 of this manuscript." [sic — "we obtained it this data" as printed;
  DRI-CON-08]
- p4 (Methods): "In cases of non-publication, we contacted the investigators to request
  the unpublished data and to ask why they had not been published."
- p7 (Methods, quality ratings): "Unpublished papers were rated from draft manuscripts
  whenever possible. When no drafts were available, the principal investigators of the
  unpublished studies were asked for quality criteria by email."
- p7 (Results): "Two other grant-funded studies were never started, one because of
  difficulty recruiting patients (S. Chisholm-Stockard, personal communication, March 3,
  2011) and the other because of difficulty finding psychodynamic therapists willing to
  participate in clinical research with Hispanic elders (J. Szapocznik, personal
  communication, August 30, 2010). These last two grants were excluded from further
  consideration."
- p7 (Results): "Of the 55 grants that started studies, we were able to locate published
  articles corresponding to 42 (76.4%) grants [28–73], but not for the other 13 (23.6%).
  (If the two studies that weren't started had not been excluded from consideration, the
  proportion of grants that did and did not lead to publications would have been 73.7%
  (42/57) and 26.3% (15/57), respectively). These 13 grants met our definition of
  unpublished studies. We were able to obtain the original data from 11 of these studies
  (84,6%)." [sic — comma decimal "84,6%"; DRI-CON-09]
- pp7–8 (continuation): "With respect to the remaining studies, the twelfth investigator
  was not yet ready to share her data (R. Clark). The thirteenth investigator expressed
  willingness to share data, but the data had been collected over a quarter of a century
  earlier and had not been retained, though he recalled that the sample was small (no more
  than a dozen patients per condition) and that the differences were negligible
  (G. Gottlieb, personal communication, June 10, 2012). Therefore, we excluded this study
  from the main analyses, but" [continues p11] "conducted sensitivity analyses, including
  this study in the relevant comparisons (psychological treatment alone or in combination
  versus antidepressant medication monotherapy) and estimating the study's effect size to
  be g = 0.00 with n = 10 per condition. The total number of participants over the 42
  published studies (4581) and 11 unpublished studies for which we had data (839) was
  5420."
- p11 (Table 1 footnote d, re Clark R01MH062054): "Investigator refuses to share data for
  this review."
- p11: "All but one of the published studies reported outcome data sufficient for
  calculating effect size. The remaining study [39] reported the grant-funded trial's
  outcomes only in aggregate with outcomes of other trials. We requested the data for the
  grant-funded trial from the principal investigator."
- Figure captions, Figs 2–7 (pp13–15), identical clause in each: "Not all results of the
  unpublished studies are presented at study level, because we did not have permission of
  the investigators to do so."
- p16 (Reasons for non-publication): "Of the 13 unpublished studies, only two were
  submitted for review; neither was accepted for publication. Six other studies were never
  submitted for review, although, in three instances, the investigators still hoped to do
  so. For the remaining five studies, it was unclear whether the authors tried to submit
  their findings for publication. Explanations that the investigators gave for not
  submitting manuscripts included that they did not think the findings were interesting
  enough to warrant publication, that they got distracted by other obligations or that
  they had practical problems."
- p17 (Discussion, limitation 1): "We were not able to obtain unpublished data for 2 of
  the 13 (15.4%) unpublished studies. In one case, the investigator was willing, but data
  collected in the 1980s were no longer available. However, in the other case, the
  investigator was reluctant to share her data, fearing that doing so would jeopardize her
  chances for independent publication."

Consequence for the truth set: every unpublished-study effect row and every unpublished
pooled estimate carries the note "SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE — values exist only
in this paper (author-supplied data)". Fully suppressed rows (F2-22, F2-25, F3-07, F4-18,
F6-18, F7-12) are certainty=UNRESOLVED with the recoverable-by-subtraction weight stated
per row; anonymized rows with printed values (F2-26/F4-19, F5-14, F5-15, F7-11) are
certainty=KNOWN for the values with identity explicitly UNRESOLVED in the note.

### Sanity checks (passed before finalizing)

- Figure row counts (both passes and the reconciled file): Fig 2 = 29, Fig 3 = 10,
  Fig 4 = 22, Fig 5 = 17, Fig 6 = 21, Fig 7 = 14 — total 113.
- Published relative weights sum to 100.00 in Figs 2, 3, 5, 6, 7 and 100.01 in Fig 4
  (rounding). Fig 5 unpublished weights sum exactly 100.00 (no hidden row). Visible
  unpublished sums elsewhere (84.36 / 66.57 / 91.90 / 55.47 / 78.94) fall short of 100 by
  exactly the documented hidden-row weights.
- Every analyses.csv row has a source_page (asserted programmatically).
- Every pooled diamond agrees across its three representations (figure, Table 2, body
  text) — verified by pass A, no exception found.

### File contents

- `analyses.csv` — 31 rows: 18 pooled estimates (6 comparisons x unpublished/published/
  combined), 6 Q-between contrast rows (*-QBET), 3 pill-placebo pools quoted in text
  (APLAC-*), 4 sensitivity analyses with no numeric results in the PDF (SENS-*,
  certainty=UNRESOLVED, S1 Table only).
- `study_labels.csv` — 103 rows: 37 published forest-plot labels, 4 named unpublished
  forest-plot labels, 4 anonymized-row entries, 1 hidden-rows entry, 57 Table 1 grant/PI
  labels.
- `published_effects.csv` — 113 rows (F2-01…F7-14): 76 published study rows,
  9 named-unpublished study rows, 5 anonymized unpublished study rows, 6 fully suppressed
  unpublished rows (UNRESOLVED), 12 subgroup totals, 6 overall totals. All
  version=AS_PUBLISHED, source_type=FOREST_PLOT (raster figures read from page images;
  decimal commas in source transcribed as points); per-study Ns are never printed in any
  figure (NOT_APPLICABLE).
- `contradictions.csv` — 23 rows (DRI-CON-01…23), union of both passes' oddities.
  KNOWN: 18; AMBIGUOUS: 3 (DRI-CON-06, -19, -22); UNRESOLVED: 2 (DRI-CON-04, -11).

### Status

**DRAFT** — pending researcher spot-check and sign-off.

TRUTH_STATUS: PRE_FREEZE — AI double-pass reconciled, human-unverified.
Benchmarks against this state are BENCHMARK_AGAINST_PREFREEZE_TRUTH.
Researcher corrections become versioned revisions; freeze tag: gold-truth-v1.
