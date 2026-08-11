# SRS Review: Ambiguities, Contradictions, and Decisions

Status: **Researcher-reviewed 2026-08-11** — resolutions below incorporate the
researcher's decisions on A1–A18 and additions A19–A24. This document is the
master record; downstream docs (01–09) conform to it.
SRS version reviewed: 1.1

## Decision criterion

Every decision is judged first against the product's central purpose:

> The application audits **published** meta-analyses: were the studies and data
> actually included handled correctly, and were the study-level and pooled
> calculations performed correctly?
> **Identifying eligible studies the meta-analysis failed to find or include is
> out of scope** (see A19 and the Scope Boundary section).

Secondary priorities, in order: avoid false audit findings · complete
provenance · explicit uncertainty · straightforward researcher verification ·
statistical reproducibility · researcher-friendly UI · extensibility without
premature complexity. Implementation convenience never outranks audit validity.

---

## A1. Deployment model — ACCEPTED (local-first) WITH MODIFIED IMPLEMENTATION

Local-first, single-researcher, privacy-conscious, hostable later — but ordinary
users must never install or manage PostgreSQL, Docker, Java, or GROBID. The
normal experience must eventually be: *install app → open app → upload
meta-analysis → begin audit*, with no command line.

- **Database: SQLite (embedded) for the first local release**, unless
  benchmarking demonstrates inadequacy. WAL mode; short transactions.
- Migration path preserved via: migrations (Alembic), repository/data-access
  abstractions, UUID identifiers, project-scoped records. PostgreSQL remains
  available for development and a future hosted deployment.
- Docker Compose etc. are development tools only, never end-user requirements.
  The shipped application packages or auto-manages its local dependencies
  (see doc 01 §2a packaging).
- **Packaging shell (decided 2026-08-11): Tauri-style native desktop shell.**
  The app installs and opens like a normal desktop application; the researcher
  never starts a server, opens Terminal, manages Docker, or navigates to
  localhost. Frontend/backend boundaries stay clean (HTTP API contract) so a
  hosted deployment remains possible later.

## A2 + A3. Status, confidence, verification, extraction method — REPLACED

The earlier proposal made `REPORTED` vs `EXTRACTED` depend on the reading
channel (embedded text vs OCR/vision). Rejected: how a value was *read* is a
separate concept from whether the source *states* it. Four orthogonal
dimensions on every important value:

**1. Scientific basis** — what the value's epistemic standing is:

```text
SOURCE_REPORTED   the source explicitly contains the value/claim — regardless
                  of whether we read it via embedded text, table extraction,
                  OCR, vision, or an LLM
DERIVED           deterministically calculated from other stored values
INFERRED          not explicitly stated; inferred from context or structure
UNRESOLVED        system cannot determine the value or choose among candidates
```

**2. Acquisition method** — how it was obtained (recorded separately):

```text
EMBEDDED_TEXT | LAYOUT_EXTRACTION | TABLE_PARSER | OCR | VISION | LLM |
BIBLIOGRAPHIC_API | MANUAL_ENTRY | CALCULATION
```

So a forest-plot value read by a vision model is
`scientific_basis = SOURCE_REPORTED, acquisition_method = VISION,
confidence = MEDIUM, review_state = REVIEW_REQUIRED` — an accurate epistemic
description.

**3. Confidence** — `HIGH | MEDIUM | LOW`, assigned only by explicit
evidence-based rules; store `confidence_rule_id` **and**
`confidence_rule_version`. An LLM is never asked to supply its own
authoritative confidence.

**4. Review state**:

```text
NOT_REVIEWED | REVIEW_REQUIRED | VERIFIED | CORRECTED |
MARKED_UNCERTAIN | EXCLUDED
```

Human verification/correction lives *here* (and in the revision history), not
in scientific basis: verifying a value does not change what kind of claim it
is — it adds verification to it.

**Derived-value propagation:** calculated values retain complete input lineage
(doc 03) **plus an input-quality summary** so "Hedges' g calculated entirely
from verified source values" is distinguishable from "Hedges' g calculated
using one inferred SD". The summary is computed from the lineage, never a
replacement for it — original input states are always recoverable.

## A4. Finding vs contradiction vs workflow failure — MODIFIED

One review experience, **two conceptual entities** (doc 05):

- **`audit_finding`** — scientifically meaningful audit results. Kinds:
  `CONTRADICTION | DISCREPANCY | STUDY_IDENTITY_ISSUE | DATA_SELECTION_ISSUE |
  STATISTICAL_ISSUE`. Examples: forest plot and table report different Ns;
  reconstructed effect differs from published; apparent duplicate sample;
  wrong outcome appears selected. **No omitted-eligible-study category exists**
  (A19).
- **`workflow_issue`** — inability to complete an audit step:
  `PRIMARY_STUDY_UNAVAILABLE | DOCUMENT_UNREADABLE | API_FAILURE |
  IDENTITY_UNRESOLVED | SUPPLEMENT_MISSING`.

Both appear in the Review Queue but are never conflated: "17 audit findings"
can never include "the OA lookup API failed". The audit report distinguishes
evidence of a possible problem, confirmed discrepancy, and inability to verify.

## A5. Incremental study/publication identity — ACCEPTED, GENERALIZED

Keep immutable publications, immutable study-label mentions, reversible study
grouping, no destruction of extraction provenance. Generalize the change log to
a versioned **`identity_resolution_event`** with operations
`MERGE | SPLIT | REASSIGN_PUBLICATION | REASSIGN_SAMPLE | UNDO` — every event
reversible, timestamped, provenance-preserving, visible in review history.
Effect records always retain the exact study label printed in the source even
if canonical grouping later changes.

## A6. Arms before primary-study parsing — ACCEPTED

Published effects store `treatment_label_reported` / `comparator_label_reported`
verbatim; explicit arm mappings to primary-study Arm entities are created later
and carry their own `confidence`, `review_state`, and provenance. Labels are
never silently equated on name similarity.

## A7. Definition of an Analysis — HIERARCHY ACCEPTED; EFFECT MEMBERSHIP MODIFIED

Parent analysis with child subgroup analyses (each with its own pooled
estimate) stands. But effects are **not** attached only to the parent with
subgroup inferred from a string. Explicit many-to-many
**`analysis_effect_membership`**:

```text
analysis_id · effect_id · membership_role · subgroup_label_reported ·
included_in_pool
```

One effect can participate in the overall analysis, a subgroup analysis, and
other legitimate analyses without duplicating the effect record.

## A8. Discrepancy thresholds — REPLACED

Generic thresholds (≤5% relative etc.) rejected; N differences are not
automatically material. Three separate questions, separately stored:

1. **Explainable by published rounding?** If the reconstructed value rounds to
   the published value at the published precision → `ROUNDING_MATCH`.
2. **Genuine numerical mismatch?** Judged only by statistic-specific
   *computational* tolerances (floating-point behavior, documented numerical
   algorithms, published precision) — never by scientific-importance
   thresholds.
3. **How important is the mismatch?** Severity assessed separately from
   factors such as: sign reversal, wrong analysis population, effect on study
   weight / pooled estimate / heterogeneity, outcome/timepoint/group mismatch,
   magnitude relative to the statistic and its uncertainty, and whether the
   discrepancy is explained. `N = 84 vs 81` triggers review; it is not called
   material until the system knows why and whether it affected the analysis.

Raw quantities (`absolute_difference`, `relative_difference`,
`published_precision`, `rounding_match`) are stored independently of severity.
All classification rules are versioned.

## A9. Bounding boxes — MODIFIED

Canonical box is **normalized**: `(x0, y0, x1, y1)`, origin top-left, range
0.0–1.0 per page. Also retain page width/height/rotation, parser-native
coordinates where available, and parser identity/version — so highlighting is
robust across PDF viewers and rendering libraries.

## A10. Effect-direction convention — ACCEPTED WITH REFINEMENT

Orientation is modeled with four separate concepts:

```text
group_order                    e.g. Treatment − Control
reported_effect_orientation    how the published effect is signed
outcome_measure_direction      e.g. higher score = worse (per measure, A17)
analysis_direction_convention  e.g. negative favors treatment
```

The statistical engine may use a canonical orientation internally, but every
transformation between reported and canonical orientation is explicit and
provenance-recorded. A source value's sign is never silently altered.

## A11. Job/queue infrastructure — MODIFIED

Durable DB-backed queue stands, but **not** described as exactly-once. Design
target: durable jobs, **at-least-once execution, idempotent handlers**,
leases/locks, retry tracking, checkpointing, safe restart. Stable idempotency
keys where appropriate, e.g. `parse_document:{document_hash}:{parser_version}`.
Under A1 the initial implementation is SQLite-compatible; the `JobQueue`
abstraction allows later PostgreSQL/Redis/other backends.

## A12. GROBID and PDF parsing — ACCEPTED WITH MODIFICATION

A **parser orchestration layer** combines: native PDF text/layout extraction,
scientific-document structure extraction, reference extraction, table
extraction, figure extraction, OCR fallback. PyMuPDF is the lightweight
baseline; GROBID provides scholarly/reference enrichment when available;
specialized extractors can be added. **No single parser is the unquestioned
source of truth** — the stack is benchmarked against the gold corpus. If
GROBID is unavailable but native parsing succeeds, the result is
`PARTIAL_SUCCESS` (with a statement of what could and could not be extracted),
never `UNSUPPORTED_FORMAT`.

## A13. Sample ↔ Arm relationship — REPLACED

No `Arm → exactly one Sample` FK: too restrictive for multi-site trials,
ITT-vs-completer populations, factorial designs, participant subsets,
subgroup-specific analyses. Samples and Arms both hang off the Study and are
linked through an explicit association, **`sample_arm_membership`**, which may
carry `N, analysis_population, site, subgroup, context, provenance`.
Sample-overlap claims remain reviewable assertions, never boolean truths.

## A14. Excel naming — ACCEPTED

`audit_workbook.xlsx` everywhere.

## A15. Time-to-event scope — ACCEPTED

Initial scope: HR, log(HR), CI, SE, generic inverse-variance synthesis.
Survival-curve digitization is not in the first major release; tracked as a
possible later capability.

## A16. LLM provider and model selection — PROVIDER ABSTRACTION ACCEPTED; ROUTING MODIFIED

Anthropic-first is acceptable, but no named model is hard-coded to a duty.
**Configurable model roles**:

```text
FAST_MODEL | DEFAULT_EXTRACTION_MODEL | COMPLEX_EXTRACTION_MODEL |
ESCALATION_MODEL
```

Concrete models are assigned to roles based on gold-corpus benchmark
performance: numerical extraction accuracy, study matching accuracy, table
interpretation, forest-plot interpretation, false-confidence rate, latency,
cost. Use the least expensive model meeting required accuracy for routine
cases; escalate difficult or low-confidence cases to a stronger model.
**Every AI extraction stores the concrete model ID actually used**, not just
the role name. Cost controls: tracking always on; optional warning threshold;
optional hard limit; default behavior prioritizes audit accuracy over token
cost.

## A17. Outcome direction — ACCEPTED WITH MODIFICATION

`higher_is_better ∈ {TRUE, FALSE, UNKNOWN}` (default UNKNOWN) attaches
primarily to the **measurement instrument / outcome measure** (e.g. BDI-II),
not only the normalized conceptual outcome (e.g. Depression). Used to help
explain sign discrepancies; never triggers a silent correction.

## A18. Value revision model — ACCEPTED

Append-only `value_revision` history; documents and locators are immutable
evidence; researcher corrections create new revisions.

---

## A19. Scope of study-inclusion auditing — OMITTED-STUDY DETECTION EXCLUDED

The application must **not** attempt to determine whether eligible studies
were missing from the meta-analysis. Excluded activities: reproducing the
literature search; searching databases for additional eligible studies;
determining whether authors failed to discover an eligible publication;
screening external literature; auditing search completeness or screening
recall.

**In scope instead** — auditing the *reported study set and its
implementation*:

- Internal study-set consistency: study in characteristics table but not
  forest plot; forest-plot study with no matching reference; "Methods says 32,
  the plotted analysis contains 31"; same underlying sample apparently counted
  twice; a study assigned to the wrong subgroup; a study present in one
  representation of an analysis but absent from another.
- **Included-study eligibility**: where information allows, compare an
  *included* study against the meta-analysis's stated eligibility criteria
  (e.g. stated "RCTs only" but an included study is observational →
  "possible eligibility inconsistency"). In scope because the study is already
  part of the published review.

**Explicit prohibition:** the system never concludes "All eligible studies
were included." It may state: "The studies included by the published
meta-analysis were audited. Search completeness and potentially omitted
eligible studies were not assessed." This limitation appears in: project audit
scope, final audit report, Excel README, and relevant UI explanations (A21).

**Removed categories:** `STUDY_OMISSION`, `ELIGIBLE_STUDY_OMITTED`,
`MISSING_ELIGIBLE_STUDY`, `LITERATURE_COVERAGE_FAILURE` — and no
literature-coverage audit level exists. (The SRS lists "eligible study
omitted" in §3.1 and `STUDY_OMISSION` in §45; this decision supersedes both.
SRS items like "study listed in one part of the publication but absent from
analysis" remain in scope as internal consistency.) Autonomous
systematic-review searching is not a later phase unless explicitly requested.

## A20. Eligibility and data-selection rules — ADDED

To audit whether included studies and their data were handled correctly, the
system must represent the meta-analysis's **stated rules**, structured and
provenance-backed:

```text
eligibility_criteria · data_selection_rules · effect_measure_rules ·
timepoint_selection_rules · outcome_selection_rules ·
multiple_outcome_handling · multiple_arm_handling ·
adjusted_vs_unadjusted_preference · ITT_vs_completer_preference
```

Extracted where available from Methods, protocol, preregistration, supplement.
These are **source-derived rules** (not an Analysis Decision Record; that
feature stays removed). The audit distinguishes *published rule* from
*observed implementation*, e.g.: rule "use longest available follow-up";
primary study has 6- and 12-month outcomes; meta-analysis used 6-month →
"possible timepoint-selection inconsistency". This is a core auditing
capability.

## A21. Audit scope visible to the user — ADDED

The UI shows which audit dimensions were actually completed:

```text
Audit coverage
✓ Internal consistency        ✓ Included-study eligibility
✓ Published data extraction   ✓ Primary-study data selection
✓ Effect-size calculations    ✓ Pooled calculations
```

Search completeness is presented as an explanatory scope note — not as an
unfinished task the user might expect to complete:

> Scope note: This tool audits the studies included in the published
> meta-analysis. It does not assess whether additional eligible studies were
> omitted from the review.

Never present "Meta-analysis fully verified"; use "All supported audit checks
completed" with the scope displayed beside it.

## A22. Data supplied outside the primary publication — ADDED

Meta-analyses may use author correspondence, unpublished data, supplementary
datasets, or IPD not recoverable from the public paper. New state:
**`SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE`**. If the meta-analysis reports
obtaining data from authors and the public primary article yields a different
or unreconstructable value, this is *not* automatically an error; record
"Published value cannot currently be independently verified from available
source documents." The researcher can add correspondence or datasets later.

## A23. Published ↔ reconstructed effect matching — ADDED

No assumed one-to-one row relationship. Published effects may combine multiple
treatment groups, pool subscales, combine outcomes, use adjusted estimates or
transformations. Explicit mapping entity **`effect_correspondence`**:

```text
published_effect_id · reconstructed_effect_id · mapping_type ·
confidence · review_state · evidence
```

supporting one-to-one, one-to-many, many-to-one. The comparison engine
operates only through these mappings.

## A24. What counts as a confirmed error — ADDED

Conservative language is mandatory. Automation may identify a *difference,
contradiction, possible incorrect selection, possible calculation error* — but
a high-severity automated discrepancy never becomes `CONFIRMED_ERROR` without
sufficient evidence and, where interpretation is required, researcher
verification. Finding review statuses:

```text
SYSTEM_FLAGGED | RESEARCHER_CONFIRMED | EXPLAINED | DISMISSED | UNRESOLVED
```

The audit engine calculates and presents evidence; the researcher makes the
final judgment. False audit findings about published research could be
consequential.

---

## UI requirement across all decisions

Local-first must not produce a developer-oriented interface. Normal use never
exposes database terminology, job queues, parser names, internal UUIDs, API
payloads, raw model responses, Docker, or command-line instructions — those
live under Advanced / Technical Details / Provenance / Developer Information.
Primary UI vocabulary: Studies, Analyses, Primary Papers, Published Data,
Source Data, Calculations, Discrepancies, Needs Review, Audit Results.
Progressive disclosure: simple summary → source evidence → technical
provenance. A normal audit requires no understanding of the implementation.

## Project scope boundary (propagated to all docs)

**IN SCOPE** — audit whether: the reported study set is internally consistent;
included studies are consistent with stated eligibility criteria; duplicate or
overlapping samples may be double-counted; correct groups, outcomes,
timepoints, sample sizes, and source values were used; study-level effects,
variances, and SEs were calculated correctly; effects were weighted correctly;
subgroup assignments are correct; the stated statistical model was implemented
correctly; pooled effects and heterogeneity were calculated correctly;
published results correspond to the underlying primary-study evidence.

**OUT OF SCOPE** — whether the literature search found every eligible study;
whether additional eligible studies existed outside the review; database
search recall; whether screening incorrectly excluded outside studies; whether
unpublished eligible studies existed; whether a new search would find more.

> Audit what the meta-analysis included and what it did with those studies.
> Do not audit whether the literature search found everything that could have
> been included.

---

## Open questions — researcher-decided 2026-08-11 (second review)

**O1. Numerical-mismatch classification when methods are under-reported —
DECIDED (modified).** Diagnostic method-variant testing is permitted, but a
variant match is **never equivalent to verifying the published calculation**.
Method-reproduction classification:

```text
METHOD_SPECIFIED_MATCH            method stated; independently reproduced
METHOD_UNSPECIFIED_VARIANT_MATCH  method under-reported; reproduced under a
                                  named supported variant — methodologically
                                  weaker than METHOD_SPECIFIED_MATCH, and
                                  reported as such
METHOD_UNSPECIFIED_NO_MATCH       method under-reported; no supported variant
                                  reproduces the value
METHOD_UNRESOLVED                 not yet determined / not attemptable
```

Report language for a variant match: "The publication did not specify the tau²
estimator sufficiently to permit unique reproduction. The published result is
reproduced within tolerance using DerSimonian–Laird." Constraints: only
statistically appropriate, explicitly supported variants are tried — never an
arbitrary search for something that matches — and **every variant attempted is
recorded** (with its calculation provenance).

**O2. Study-design classification for eligibility checks (A20/A19) —
ACCEPTED.** Eligibility-consistency findings on *included* studies may be
system-flagged but remain conservative: they require provenance,
quoted/source-located evidence, explicit inference status, and researcher
review before confirmation (`certainty = POSSIBLE` until reviewed). Never
expanded into omitted-study detection or literature-search auditing.

**O3. `workflow_issue` vs pipeline stage-state — ACCEPTED.** Stage states are
infrastructure records; `workflow_issue` is the researcher-facing projection
with explicit lifecycle rules (open on persistent failure, at most one OPEN
per work item × issue type, auto-resolve on later stage success, history
preserved). Workflow issues never become scientific audit findings.

**O4. SQLite concurrency — ACCEPTED, TRIGGER REVISED.** WAL mode; single
worker process with bounded async concurrency; expensive parsing/OCR/model
work runs **outside database transactions** (and in parallel where
appropriate); DB writes stay short and controlled. CPU-heavy parallel
computation is **not**, by itself, evidence of SQLite inadequacy. Reconsider
SQLite only on *measured* database limitations: material write contention,
unacceptable transaction latency, DB throughput becoming the pipeline
bottleneck, reliability problems, or a hosted/multi-user architecture
requiring a server database. Measurements are recorded before any database
change (a concurrency benchmark is part of the foundation verification).

**O5. Comparison semantics for non-1:1 correspondences (A23) — ACCEPTED.**
Composite transformations are first-class statistical-engine calculations with
full provenance. `effect_correspondence` supports legitimate one-to-one,
one-to-many, and many-to-one relationships; a composite reconstructed effect
identifies **all contributing values and every deterministic transformation
applied**. Component-level mismatches surface as explanations unless material
on their own.
