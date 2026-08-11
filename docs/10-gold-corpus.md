# Gold-Standard Benchmark Corpus

Status: **Approved with development/holdout split (researcher decision
2026-08-11).** All OA links were verified live; accessibility of primaries was
spot-checked (3–5 per candidate), not exhaustively confirmed.

## Development vs holdout split

**Development corpus (7)** — used for truth-set construction, baselining, and
parser tuning: C1 Cooney, C2 Nissen, C3 Prochaska, C4 Macnamara, C5 Hahn,
C6 Yang, C8 Driessen. Together these cover every required characteristic:
continuous/SMD (C1, C5, C8), binary (C2, C3), correlation (C4), TTE/generic IV
(C6), multi-arm/shared-control (C5, C1), documented corrections including a
calculation-level error (C2 erratum, C4 corrigendum, C5 correction),
author-supplied/non-public data (C8, C2), and hard tables/plots across seven
publisher layouts.

**Holdout corpus (3)** — kept outside routine development and tuning; used
only to test whether extraction improvements generalize:

- **C7 Singh 2011** (binary, Peto, zero-event exclusion): near-neighbor of
  development paper C3 but unseen — tests generalization to a very similar
  binary-safety paper, and later the C3↔C7 divergence diagnosis on a paper the
  system was never tuned on.
- **C9 Goyal 2014** (continuous, hard author-manuscript layout, many
  outcomes × timepoints): the hardest continuous layout stays unseen.
- **C10 Smith & Silva 2011** (correlation, 184-study appendix tables): its
  ground truth comes from the independent Maassen et al. 2020 audit rather
  than from us, so holdout evaluation carries no leakage from our own
  truth-construction conventions.

Rules: holdout papers are not parsed during development except in scheduled
evaluation runs; no error analysis of holdout failures feeds tuning decisions
directly (findings there become new *development* fixtures only if a matching
weakness can be reproduced on development papers). Do not repeatedly optimize
against every paper in the development corpus either — per-paper overfitting
is checked by the holdout gap.

The set deliberately includes hard cases — documented errata, zero-cell
pathology, author-supplied data, dissertation-heavy reference lists — because
the corpus exists to expose weaknesses, not to flatter the system.

---

## Tier 1

### C1. Cooney et al. 2013 — Exercise for depression (Cochrane)
- **Citation:** Cooney GM et al. Exercise for depression. Cochrane Database Syst Rev 2013(9):CD004366. DOI: 10.1002/14651858.CD004366.pub6
- **Domain:** Exercise / adult depression · **Type:** Continuous, SMD (pooled −0.62 [−0.81, −0.42])
- **Studies:** 39 trials (37 in meta-analyses)
- **Why:** Canonical RevMan format — standardized forest plots with per-arm n/mean/SD, so per-study SMDs and pooled results should reproduce near-exactly. Exercises multi-arm handling (4-arm SMILE trial) and scale-direction conventions. The published Ekkekakis 2015 critique (DOI: 10.1016/j.mhpa.2014.12.001) documents disputed inclusion/extraction choices an auditor should surface.
- **Primaries:** Mixed, ~half freely accessible (Veale 1992 PMC; Mather 2002 Cambridge Core; Blumenthal 2007 UNC repository; Blumenthal 1999 paywalled).
- **Erratum:** None; published methodological critique instead. **Author-supplied data:** minor (standard Cochrane correspondence).
- **Difficulty:** PDF easy but very long (~150 pp); many analyses to disambiguate.
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9721454/

### C2. Nissen & Wolski 2007 — Rosiglitazone and MI (NEJM)
- **Citation:** NEJM 356:2457–2471. DOI: 10.1056/NEJMoa072761
- **Domain:** Diabetes/CV drug safety · **Type:** Binary, Peto OR (MI OR 1.43 [1.03–1.98])
- **Studies:** 42 trials (per-outcome zero-event exclusions)
- **Why:** The strongest true-positive fixture available: a **formal erratum with itemized numeric corrections** (NEJM 2007;357:100, DOI: 10.1056/NEJMx070038 — corrected patient totals, Table 1 subtotals, Table 4 event counts). The print PDF carries pre-erratum numbers while the web version is corrected — a version-reconciliation trap. Rare events, many zero cells, method sensitivity documented by Diamond et al. (Ann Intern Med 2007). Primaries include sponsor trial-register CSRs and FDA documents (26 of 35 register trials unpublished) — exercises source resolution and A22 boundaries.
- **Primaries:** DREAM (Lancet, OA), ADOPT (NEJM, free), GSK register CSR PDFs verified downloadable; FDA briefing docs via archives.
- **Difficulty:** High — 42-row multi-page tables, no per-study forest plot.
- **OA:** https://www.nejm.org/doi/full/10.1056/NEJMoa072761 (free; PDF behind bot protection, browser needed)

### C3. Prochaska & Hilton 2012 — Varenicline CV events (BMJ)
- **Citation:** BMJ 344:e2856. DOI: 10.1136/bmj.e2856
- **Domain:** Smoking cessation drug safety · **Type:** Binary, risk difference primary (0.27% [−0.10, 0.63]) with Peto OR/MH RR comparisons
- **Studies:** 22 RCTs, incl. 8 double-zero trials retained in RD but dropped by relative measures
- **Why:** Paired "answer key" with C7 (Singh 2011): same drug, overlapping trials, opposite conclusion, fully documented reasons (summary-statistic choice, zero-event handling, event windows). Supplementary per-trial 2×2 tables. Cross-metric consistency checking (RD vs OR vs RR on the same data) is exactly what the audit engine must do.
- **Primaries:** Gonzales 2006 JAMA free; Rigotti 2010 PMC; Pfizer register/FDA sources.
- **Erratum:** None; the paper *is* the documented reanalysis. **Difficulty:** moderate (RD-scale forest plots, percentage units).
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC3344735/

### C4. Macnamara et al. 2014 — Deliberate practice (Psych Science)
- **Citation:** Psychological Science 25(8):1608–1618. DOI: 10.1177/0956797614535810
- **Domain:** Expertise/skill psychology · **Type:** Correlation (r; random effects; r̄ .35→.38 post-correction)
- **Studies:** 88 studies, 157 effect sizes, N=11,135
- **Why:** A **published corrigendum with a complete before/after results table** (2018, DOI: 10.1177/0956797618769891): the authors misapplied a dependent-samples N-adjustment formula. With the open-data spreadsheet (OSF: osf.io/rhfsk), the benchmark can score reproduction of both the wrong and corrected pooled values — a documented calculation-level (not extraction-level) error, which C2's transcription-level erratum doesn't cover. The Ericsson inclusion/coding dispute (2016, 2019) adds documented extraction ambiguity.
- **Primaries:** Mixed; several verified OA (Gobet & Campitelli via Brunel; Howard 2011 Wiley bronze).
- **Difficulty:** Moderate — effects live in supplement/spreadsheet, no forest plot.
- **OA:** author-archived PDF (incl. corrigendum): https://hhs.purdue.edu/skill-learning-and-performance-lab/wp-content/uploads/sites/43/2024/08/macnamara-et-al-2014-deliberate-practice-and-performance-in-music-games-sports-education-and-professions-a-meta-analysis.pdf

### C5. Hahn et al. 2024 — Exercise and energy intake in children (IJBNPA)
- **Citation:** Int J Behav Nutr Phys Act 21:76. DOI: 10.1186/s12966-024-01620-8
- **Domain:** Pediatric exercise/nutrition · **Type:** Continuous, mean difference (kcal)
- **Studies:** 22 RCTs contributing **41 arms** vs shared controls
- **Why:** Exact multi-arm/shared-control target: Methods explicitly describe Cochrane-Handbook control-group splitting to avoid double counting — the auditor must reproduce the splitting arithmetic per comparison. Has a **publisher correction** (DOI: 10.1186/s12966-024-01651-1, Table 1) providing a documented original-vs-corrected pair.
- **Primaries:** Mixed (Thivel 2013 paywalled; several PMC).
- **Difficulty:** Moderate — 41-row forest plots; split-n reconstruction requires cross-referencing Table 1 + correction.
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11247817/ (CC BY)

### C6. Yang et al. 2018 — Systemic immune-inflammation index (J Cancer)
- **Citation:** J Cancer 9(18):3295–3302. DOI: 10.7150/jca.25691
- **Domain:** Oncology prognosis · **Type:** Time-to-event, HR generic inverse variance (OS HR 1.69 [1.42–2.01])
- **Studies:** 22 articles / 24 study units, 7,657 patients
- **Why:** Canonical generic-IV/HR case: pooled log-HRs with fixed/random switching; a mix of adjusted and KM-derived HRs (provenance heterogeneity); two articles contribute multiple cohorts (mild dependency check). Forest-plot values are typeset text, so extraction is feasible without vision models — a good early TTE case.
- **Primaries:** ~half OA (Geng 2016, Lolli 2016 PMC).
- **Erratum:** none. **Difficulty:** low-moderate.
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6160683/ (CC BY-NC)

## Tier 2

### C7. Singh et al. 2011 — Varenicline CV events (CMAJ)
- CMAJ 183(12):1359–1366. DOI: 10.1503/cmaj.110218 · Binary, Peto OR 1.72 [1.09–2.71], 14 RCTs.
- **Why:** The other half of the C3 pair; textbook Peto-bias/zero-event-exclusion case with EMA critique, CMAJ letters, and authors' reply. Auditing C3+C7 together tests whether the system can localize *why* two published analyses of overlapping trials diverge (§38 diagnosis).
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC3168618/

### C8. Driessen et al. 2015 — Publication bias in NIH-funded psychotherapy trials (PLOS ONE)
- PLoS ONE 10(9):e0137864. DOI: 10.1371/journal.pone.0137864 · Hedges' g; 55 grants, 42 published + 11 unpublished author-supplied datasets.
- **Why:** The A22 fixture: pooled analyses mix recomputable published effects with effects computed from unpublished data that **cannot** be reconstructed from any public document — the benchmark's test that `SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` is used instead of false discrepancy findings. Subgrouped journal-style forest plots (Figs 2–7).
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC4589340/

### C9. Goyal et al. 2014 — Meditation programs (JAMA Internal Medicine)
- JAMA Intern Med 174(3):357–368. DOI: 10.1001/jamainternmed.2013.13018 · SMDs; 47 RCTs; many outcome domains × timepoints.
- **Why:** Hard-layout continuous case: author-manuscript pagination, outcome-grouped compact forest plots, direction-of-benefit varying across scales (sign-convention stressor), and a free 400+ page AHRQ companion report (NBK180102) providing independent extraction tables as secondary ground truth.
- **OA:** https://pmc.ncbi.nlm.nih.gov/articles/PMC4142584/

### C10. Smith & Silva 2011 — Ethnic identity and well-being (J Counseling Psych)
- J Couns Psychol 58(1):42–60. DOI: 10.1037/a0021528 · Correlation, r=.17, **184 studies**.
- **Why:** Independently audited as MA26 in Maassen et al. 2020 (PLOS ONE, DOI: 10.1371/journal.pone.0233107): 7 of 21 sampled effect sizes had documented discrepancies, with per-effect extraction decisions published on OSF — third-party ground truth about extraction errors we didn't create ourselves. Large multi-page appendix tables, no forest plot, dissertation-heavy primaries (retrievability stressor). Larger than our preferred size band — scored on the Maassen-sampled subset plus a random sample, not all 184.
- **OA:** https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1087&context=facpub (browser-served)

**Alternate (if a Tier-2 slot needs replacing):** Kim et al. 2017 sarcopenia/cirrhosis (PLOS ONE, DOI: 10.1371/journal.pone.0186990) — HR + OR parallel pooling, CC BY.

---

## Coverage against the required characteristics

| Requirement | Covered by |
|---|---|
| 1. Continuous / SMD | C1, C5, C8, C9 |
| 2. Binary | C2, C3, C7 |
| 3. Correlations | C4, C10 |
| 4. Time-to-event / generic IV | C6 (+alternate) |
| 5. Multi-arm / shared control | C5 (explicit splitting), C1 (4-arm trial), C6 (multi-cohort articles) |
| 6. Known correction/erratum | C2 (itemized erratum), C4 (corrigendum + before/after table), C5 (publisher correction) |
| 7. Author-supplied / non-public data | C8 (central), C2 (register/FDA sources), C4 (open-data re-pooling) |
| 8. Easy and difficult forest plots | easy: C1 (RevMan), C6 · hard: C8, C9 · none/table-only: C2, C4, C10 |
| 9. Complex tables | C2 (42-row multi-page), C10 (184-study appendix), C9 (evidence tables) |
| 10. Different publishers/layouts | Wiley/Cochrane, NEJM, BMJ, SAGE, BMC, Ivyspring, CMAJ, PLOS, JAMA, APA |

Documented ground-truth discrepancies (the corpus's audit "answer keys"):
C2 erratum · C4 corrigendum · C5 correction · C3↔C7 divergence · C10
Maassen-audited discrepancies · C1 Ekkekakis critique (qualitative).

## Truth-set status (2026-08-11)

| Paper | PDF acquired | Truth status |
|---|---|---|
| yang-2018-sii | ✓ | Double-pass reconciled (zero numeric disagreements); 41 effect rows, 19 analyses, 10 contradictions. DRAFT pending researcher sign-off. |
| prochaska-2012-varenicline | ✓ | Double-pass reconciled (zero numeric disagreements; glyph-verified misprints); 137 effect rows, 10 analyses, 8 contradictions. DRAFT. |
| macnamara-2014-practice | ✓ | Double-pass reconciled; 21 analyses (both versions), 4 contradictions incl. dual-text-layer property; study-level data live in authors' OSF file (not in PDF). DRAFT. |
| hahn-2024-exercise-intake | ✓ | Double-pass reconciled (zero numeric disagreements); 92 effect rows incl. re-split shared-control variants, 14 analyses, 16 contradictions (headline: Thivel 2015 SE/CI swap in Fig 4). DRAFT. |
| driessen-2015-nih-psychotherapy | ✓ | Double-pass reconciled (zero numeric disagreements); 113 effect rows incl. 19 SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE unpublished rows (6 suppressed → UNRESOLVED), 31 analyses, 23 contradictions. DRAFT. |
| cooney-2013-exercise-depression | ✓ | Truth pending (tranche 3 — needs analysis-subset scoping: ~150-page Cochrane review; propose truthing Analysis 1.1 + 2 secondary analyses rather than all). |
| nissen-2007-rosiglitazone | ✗ (NEJM PDF is browser-gated; needs manual download) | Truth pending. |
| holdout ×3 | not acquired (deliberate) | Untouched per holdout rules. |

Truth v0 provenance: two independent extraction passes per paper (blind),
reconciled with disagreements logged in each `truth/notes.md`. Passes were
performed by AI readers against the actual PDFs (text layer + rendered
figures); status stays DRAFT until researcher spot-check sign-off. Phase-1
baseline frozen at `corpus/baseline/PHASE1_BASELINE.md`.

## Truth-set construction notes

- Manual double extraction per doc 08 §4; for C2/C4/C5, truth records BOTH the
  as-published and as-corrected values with the erratum as a cited source, so
  the system is scored on *finding* the discrepancy, not just matching one
  version.
- For C8, truth marks the 11 author-supplied effects as
  `SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` — the system is penalized for calling
  them discrepancies (A22/A24 false-finding guard).
- For C10, the Maassen OSF files are imported as third-party truth for the
  sampled effect sizes (with citation), not treated as our own extraction.
- Several OA copies (NEJM, BMJ, BYU) are served only to real browsers; corpus
  acquisition will be manual download into `corpus/gold/<name>/source/`
  (legal copies only, per §66; no piracy sources).
