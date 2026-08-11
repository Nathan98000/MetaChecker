# Testing Strategy and Benchmark-Validation Methodology

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 01 (layout, seams), doc 06 (interfaces)

---

## 1. Test pyramid

```text
tests/unit/          domain services, provenance rules, confidence rules,
                     tolerance/severity rules (A8), parsers on snippets
tests/statistical/   statengine validation (§57, §65) — §3 below
tests/integration/   full pipeline against fake/replay adapters; runs on BOTH
                     SQLite (shipping config) and PostgreSQL (portability, A1);
                     resumability & idempotency under crash (A11)
tests/adversarial/   §56 corpus as permanent regression fixtures
tests/benchmark/     §55 gold corpus, scored, tracked over time; also drives
                     model-role assignment (A16)
frontend: vitest + Playwright (evidence panel, review flow, undo,
          coverage panel & scope note presence, A21)
```

CI: unit + statistical + integration + adversarial on every change; benchmark
suite on demand and release candidates; small opt-in live suite for real
adapters.

## 2. Non-negotiable invariants (schema, pipeline, scope)

- No data point committable without locator XOR calculation provenance.
- Corrections never orphan originals; after any correct/undo/restore sequence,
  revision #1 is intact and the chain replays to head (A18).
- Four-dimension integrity (A2/A3): verification changes `review_state`, never
  `scientific_basis`; property tests over random action sequences.
- Input-quality summaries always agree with recomputation from raw lineage
  (A2/A3 — the summary may never drift from the inputs).
- **At-least-once safety** (A11): kill the worker mid-stage, restart, assert
  no lost work items and no duplicated outputs (idempotency keys honored);
  lease-expiry reclaim tested explicitly.
- `API_FAILURE` produces no domain row; persistent failure produces exactly
  one OPEN `workflow_issue` per (item × type), auto-resolved on later success
  (A4, O3).
- **Findings/issues separation** (A4): no code path counts a `workflow_issue`
  in audit-finding totals; report/export snapshot tests assert the split.
- **Conservatism** (A24): no automated path sets `certainty = CONFIRMED` or a
  confirmed-error status; eligibility/rule findings are capped at `POSSIBLE`
  and carry quoted evidence spans (O2).
- **A22:** author-supplied-data cases classify as
  `SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE`, never as discrepancy findings.
- **Scope boundary** (A19): no module, prompt template, or fixture references
  external-literature search; a static check greps prompts/configs for
  banned capabilities (database search, screening recall) as a guardrail;
  no taxonomy code for omitted studies exists.
- Forest-plot subtotal rows never enter pooling inputs (`row_kind`, §26);
  membership-based pooling only (A7).
- Comparisons run only through `effect_correspondence` (A23); direct
  row-identity comparison is unconstructible in the audit API.
- Sign handling: no code path mutates a stored value's sign; orientation
  transforms appear only as engine calculation steps (A10).
- Low-confidence values never reach `VERIFIED` without a review event (§54).

## 3. Statistical validation (§57, §65)

Three independent ground-truth sources per formula, none AI-generated:

1. **Hand-verified examples** with worked arithmetic committed.
2. **Published examples** — Borenstein et al., Cochrane Handbook, Hedges &
   Olkin.
3. **Independent R implementation** (`tools/r-validation/`, metafor/meta):
   frozen expected-output CSVs across a parameter grid; Python must match
   within documented tolerances (1e-10 closed forms; documented looser
   tolerance for iterative tau² estimators). R script + lockfile committed.

Edge-case grid per family: zero events (each/both cells), n=2, unequal n,
negative/extreme effects, missing cells → INSUFFICIENT_DATA, r = ±1,
rounding-boundary inputs. Warnings asserted, never silent adjustments (§33).

**A8-specific tests:**
- Rounding-match (Q1): property tests over published-precision grids
  (0.43 vs 0.4271 → ROUNDING_MATCH; 0.43 vs 0.4362 → not).
- Computational tolerance (Q2) is statistic-specific and versioned; tests pin
  each tolerance rule version.
- Method-variant handling (O1): with `analysis_method` under-reported, engine
  tries only supported, statistically appropriate variants, records every
  attempt with calculation provenance, and classifies
  `METHOD_UNSPECIFIED_VARIANT_MATCH` / `METHOD_UNSPECIFIED_NO_MATCH` —
  asserted distinct from (and never upgradeable to) `METHOD_SPECIFIED_MATCH`;
  report snapshots verify the weaker language.
- Severity (Q3) computed independently of Q1/Q2; fixture: N 84 vs 81 →
  numerical MISMATCH but severity REVIEW, not MATERIAL, until explained.

## 4. Gold-standard benchmark corpus (§55)

`corpus/gold/<name>/` per benchmark meta-analysis:

```text
source/           meta-analysis PDF (+ legal primary PDFs where possible)
truth/
  analyses.csv  studies.csv  publications.csv  memberships.csv
  stated_rules.csv (A20)  published_effects.csv  primary_values.csv
  correspondences.csv (A23)  reconstructed_effects.csv  pooled.csv
  locators.csv  findings.csv (known real discrepancies, typed per doc 05)
provenance.md     double-entry creation, disagreements logged, sign-off
```

Truth is manual double extraction, created before the system runs on it.
Initial target: **6–10 meta-analyses** (researcher decision 2026-08-11)
deliberately covering: continuous/SMD, binary, correlation, time-to-event or
generic IV; a multi-arm/shared-control dependency case; a known
correction/erratum (true-positive discrepancy); an author-supplied-data case
(A22); easy and difficult forest plots; complex tables; multiple
publishers/layouts. Prefer cases whose primary studies are legally
accessible; do not pick only easy papers — the corpus should expose
weaknesses. Each candidate's rationale is recorded. Truth includes NO
omitted-study annotations (A19).

## 5. Benchmark metrics (§55)

```text
included-study identification     precision / recall  (identifying the study
                                  set AS REPORTED BY THE REVIEW — not
                                  literature coverage, A19)
publication matching              resolved-to-correct-DOI rate
numerical extraction              exact + tolerance match, by source_type
stated-rule extraction            rule capture accuracy (A20)
outcome / timepoint matching      accuracy
correspondence construction       correct mapping-type rate (A23)
effect reconstruction             within-tolerance rate
pooled reconstruction             per quantity (est, CI, I², tau²)
discrepancy detection             precision / recall vs truth findings
FALSE-CONFIDENCE RATE             share of HIGH-confidence values that are
                                  wrong — headline safety metric
abstention quality                share of wrong values correctly marked
                                  LOW/REVIEW_REQUIRED
false-finding rate                share of system-flagged findings judged
                                  spurious on review (A24 watch metric)
```

**Model-role assignment (A16):** the same harness scores each candidate model
per role (extraction accuracy, table/forest interpretation, study matching,
false-confidence rate, latency, cost); role→model assignments are config
derived from these runs, and every benchmark report records the concrete model
IDs used.

Release gate: false-confidence rate and false-finding rate are the primary
regression criteria — improvements elsewhere do not excuse regressions here
(§70; A24).

## 6. Adversarial corpus (§56)

`corpus/adversarial/` — targeted fixtures with expected-behavior assertions:
multi-column PDFs, scanned pages, multi-page tables, same-author/year
collisions, multiple timepoints/outcomes, negative effects, unusual CI
notation, missing SDs, subgroup analyses, duplicate publications, overlapping
samples, shared controls, footnote-only values, forest plots with subtotal
rows, table-vs-plot conflicts, stated-rule vs implementation conflicts (A20),
author-supplied-data cases (A22), combined-arm published effects needing
many-to-one correspondence (A23). Every later production bug adds a fixture
before it is fixed.

## 7. Phase gating (§67)

Each phase exits only with: suites green, adversarial fixtures passing, and —
from the published-data phase onward — benchmark metrics computed and not
regressed. One working example is never sufficient (§67).
