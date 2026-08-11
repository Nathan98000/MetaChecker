# Truth provenance — nissen-2007-rosiglitazone

Status: DRAFT (researcher sign-off pending)

## Construction
- Pass A (`pass-a-raw.md`) and Pass B (`pass-b-raw.md`): two independent full
  reads of `source/2457.pdf` (16 pages, 100% native text layer, no figures),
  2026-08-11, blind to each other. Both used PyMuPDF text extraction with
  coordinate-verified cell ordering for the rotated Tables 1-2, and both
  re-verified all sums arithmetically.
- Reconciliation 2026-08-11: cell-by-cell diff of both passes, followed by
  programmatic regeneration of all four CSVs with 28 built-in sanity checks
  (all PASS; see "Sanity checks" below).

## Numeric disagreements between passes
**ZERO.** Every printed numeric value — all 17 pooled effects/CIs/P values,
all 42 Table 1 enrollment pairs, all 42x4 Table 3 event cells, all Table 3/4
totals and denominators, both Table 1 subtotals, and both pre-erratum
subtotal values on p16 — was extracted identically by both passes.

## Non-numeric / derived disagreements (all adjudicated, none silent)
1. **Analysis count: A=17 vs B=18.** Pass B listed Table 5's "Combined
   comparator drugs" rows (MI-COMBINED, CVD-COMBINED) as separate analyses;
   pass A folded them into the overall analyses. Adjudicated by enumeration
   of distinct pooled estimates: the Table 5 combined rows print values
   identical to the Abstract/Results/Table 4 "Overall" rows (1.43 1.03–1.98
   P 0.03; 1.64 0.98–2.74 P 0.06) and describe the same analysis, so final
   count = **17 analyses** (A01–A17), with Table 5 cited as an additional
   source location on A01/A02.
2. **Pass A bookkeeping error in the CV-death exclusion list.** Pass A's
   Section 3b list of zero-CV-death trials included 49653/132 and stated
   "18 trials + the 2 all-zero trials = 19" (arithmetically 20). Pass A's own
   Table 3 row for 49653/132 prints CV death 1/0, contradicting its list.
   Adjudicated to Pass B's 19-trial list (which omits 49653/132 and includes
   the 2 all-zero trials), verified two ways: (a) against every Table 3 zero
   cell, (b) 42−19=23 matches Methods and the Table 4 CV-death denominators
   6,845/3980 reproduce exactly. Final list recorded in NIS-CON-4.
3. **Certainty on 49653/330:** pass A marked both table rows KNOWN, pass B
   marked its merged row AMBIGUOUS. Resolved as in yang-2018-sii: each
   printed value is KNOWN per its table; the cross-table discrepancy is
   carried as contradiction NIS-CON-1, not as row-level ambiguity.
4. **DREAM/ADOPT source pages:** pass B additionally listed PDF p16 (both
   trials are named in the correction notice); pass A did not. Union adopted.
5. **Erratum location count: A=13 vs B=12.** Pass A split the Table 1 total
   into rosiglitazone/control rows; pass B kept one "totals" location.
   Adjudicated to B's 12-location enumeration (NIS-ERR-01..12).

## Version-inversion finding (CRITICAL)
The corpus premise assumed this file was the pre-erratum June 14, 2007 print.
Both passes independently established the opposite:
- Every page bears "Downloaded from www.nejm.org on July 30, 2007"; PDF
  metadata modDate 2007-07-30 (creationDate 2007-06-12).
- PDF page 16 IS the erratum itself (N Engl J Med 2007;357:100, ending "The
  text and tables have been corrected on the Journal's Web site").
- Location-by-location check at all 12 erratum-listed locations: the body
  carries the CORRECTED value at every one (e.g., subtotal prints 9,507/5,960;
  Table 4 prints 44/10,285, 41/2895, 25/6,845, 12/2,635, 5/2895).

### Version handling adopted (per reconciliation directive)
- Rows extracted from this PDF's tables carry `version=AS_CORRECTED`
  (source: the table's page).
- `version=AS_PUBLISHED` (pre-erratum print) rows exist ONLY where the
  appended erratum documents the pre-erratum value: the Table 1 additional-
  trials subtotal (9502/5961) — row T1-SUBTOTAL-ADD-PRE, source_page 16,
  certainty KNOWN — plus a DERIVED pre-erratum Table 1 total
  (15,560/12,283 = documented subtotal deltas applied to the printed total),
  row T1-TOTAL-PRE, certainty AMBIGUOUS because the erratum does not state
  it. The two versions are never merged and corrected values are never
  presented as print originals.
- For the six erratum-affected Table 4 cells and the Methods sentences, the
  erratum quotes only the corrected text, so the pre-erratum values are NOT
  recoverable from this artifact (NIS-ERR-06..12 record this explicitly).
- The pooled ORs/CIs/P values were unchanged by the erratum.

### Meta note (version-pair fixture)
Acquiring the true PRINT PDF (pre-erratum, June 14, 2007 issue) remains
desirable to complete the version-pair fixture; this file alone cannot verify
which OTHER print values differed beyond what the erratum lists. Recorded in
`meta.json` as `version_pair_todo`.

## Other adjudications / conventions
- Table 3 carries two outcomes per trial but the schema has one event pair
  per row, so published_effects.csv holds one row per trial per outcome
  (T3-MI-xx / T3-CV-xx; 84 study rows), with the outcome in `subgroup`.
- Zero-cell exclusions (Methods p3 rule) are derived — the paper never names
  the excluded trials. Excluded-outcome rows carry an empty `analysis_id`
  plus an explanatory note; the 38/23 arithmetic is banked as explained-guard
  contradiction rows NIS-CON-3/NIS-CON-4 so the checker does not flag it.
- Table 4's DREAM/ADOPT single-trial rows are row_kind SUBGROUP_TOTAL
  (aggregate rows with ORs, mirroring yang-2018-sii's single-study subtotals).
- No per-trial ORs and no forest plot exist anywhere in the paper; per-trial
  effects must be recomputed from the Table 3 2x2 cells.
- Verbatim comma formatting preserved in n columns ("1,181"; "9,507";
  Table 3 values uncommaed as printed).
- All typos recorded verbatim, clustered as one contradiction row
  (NIS-CON-6): "sufonylurea", "Ramipiril" (x2), ADOPT expansion "Prevention"
  for Progression, "Evaulation".

## Sanity checks (all PASS, machine-verified at generation)
- Table 3 event column sums = printed totals: MI 86/72, CV death 39/22
  (also match Results text p3).
- Table 3 n column sums = 15,556 / 12,277 (differ from Table 1 totals by
  exactly the 49653/330 discrepancy 9/5 — NIS-CON-1).
- Table 1: registration subtotal 1,967/793; additional-trials subtotal
  9,507/5,960 (sum of its 35 rows, using Table 1's 1,181/382); total
  15,565/12,282 = 1,967+9,507+2,635+1,456 / 793+5,960+2,634+2,895.
- Table 4 denominator arithmetic: MI small 10,285/6106 = Table 3 n summed
  over the 36 MI-analysis trials; CV death small 6,845/3980 = sum over the
  21 CV-death-analysis trials (both using Table 3's 1172/377 for 49653/330);
  events 44/22 and 25/7 = Table 3 totals minus DREAM and ADOPT.
- Exclusion counts: 42−4=38 MI, 42−19=23 CV death (match Methods p2).
- Derived pre-erratum totals: 15,560/12,283.

TRUTH_STATUS: PRE_FREEZE — AI double-pass reconciled, human-unverified.
Benchmarks against this state are BENCHMARK_AGAINST_PREFREEZE_TRUTH.
Researcher corrections become versioned revisions; freeze tag: gold-truth-v1.
