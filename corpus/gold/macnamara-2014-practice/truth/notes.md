# Truth provenance — macnamara-2014-practice

Status: DRAFT (researcher sign-off pending)

## Construction
- Pass A: independent full read of the 14-page composite PDF (corrigendum pp.1–3 + article), 2026-08-11.
- Pass B: independent duplicate pass, same instructions, blind to pass A.
- Reconciliation: logged below after both passes.

## Key structural facts (pass A)
- PDF pages 8 and 11 contain DUAL TEXT LAYERS: original 2014 results text AND
  the 2018 corrected text overlay on the same physical pages. Any text miner
  sees contradictory values on one page; the corrigendum (pp.1–3) is the
  arbiter. This is a deliberate, documented adversarial property of this
  corpus entry.
- Per-study effect sizes are NOT in the PDF (Fig. 2 forest plot is graphical
  only); study-level truth lives in the authors' open data (osf.io/rhfsk) and
  supplement — study-level extraction scoring for this paper uses that file
  as a cited third-party source, not our own extraction.
- Abstract/discussion/Figure 3 retain uncorrected values (corrigendum scope);
  recorded as a known internal inconsistency of the composite document.
- Stray production header from an unrelated article on PDF p.4 (assembly
  artifact) — noted UNRESOLVED.

## Reconciliation (pass A vs pass B), 2026-08-11
- No numeric disagreements: all pooled values, CIs, I², Q statistics, and all
  ~35 corrigendum before/after pairs identical across passes.
- Pass B enumerated the three "additional models" as separate per-domain rows;
  pass A recorded them compactly. B's granularity adopted; values identical.
- Both passes independently flagged: dual text layers (pp.8, 11), abstract/
  discussion/Fig.3 retaining uncorrected values, stray Shariff header (p.4),
  per-study data NOT_IN_PDF (OSF open data is the study-level source).
- Pass B additionally noted performance-method participant counts sum to
  11,321 > 11,135, explained by the table's own footnote (samples contribute
  to multiple types) — recorded as explained, not a contradiction.

TRUTH_STATUS: PRE_FREEZE — AI double-pass reconciled, human-unverified.
Benchmarks against this state are BENCHMARK_AGAINST_PREFREEZE_TRUTH.
Researcher corrections become versioned revisions; freeze tag: gold-truth-v1.
