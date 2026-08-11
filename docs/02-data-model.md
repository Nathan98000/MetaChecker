# Relational Data Model

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 00 (A2–A8, A13, A17–A23), doc 03 (provenance).

Conventions: all tables have `id UUIDv7 PK`, `project_id FK`, `created_at`;
target DB is SQLite (WAL) behind repositories, PostgreSQL-portable (A1). JSONB
(SQLite: JSON text) only for locators/candidate payloads/context — never for
quantitative values used in calculations. `†` marks append-only tables.

---

## 1. Entity overview

```text
project
 └─ meta_analysis_publication ── document(s)
     ├─ stated_rule (A20: eligibility & selection rules)
     └─ analysis (parent/child for subgroups, A7)
         └─ analysis_effect_membership ── published_effect
 study ◄── study_membership ── publication
   │        (grouping revised via identity_resolution_event†, A5)
   ├─ sample ──┐
   │           ├─ sample_arm_membership (A13)
   ├─ arm ─────┘
   ├─ outcome ── measure (A17)
   └─ timepoint
 primary_value (candidate data from primary studies)
 calculation† ─ calculation_input†
 reconstructed_effect ── effect_correspondence (A23) ── published_effect
 audit_comparison ─ audit_finding ─ finding_evidence      (A4, A8, A24)
 workflow_issue                                            (A4)
 value_revision† · extraction_record† · source_locator†
 job · stage_state · external_call_log† · cache_entry · review_event†
```

## 2. Documents and parsing

**document** — any stored file (meta-analysis PDF, primary article, supplement,
protocol, registration, correction; §29). `sha256`, `role` enum, `origin`
(`UPLOADED | AUTO_RETRIEVED`), retrieval provenance. Immutable.

**document_page** — width/height/rotation per page (needed to render
normalized bboxes, A9).

**parse_artifact†** — output of one parser in the orchestration stack (A12):
`document_id, parser_id, parser_version, kind` (`TEXT_SPANS | TABLE |
FIGURE_REGION | REFERENCE_LIST | SECTION_MAP`), `payload`, `input_hash`.
Multiple parsers may produce artifacts for the same document; none is
privileged as truth (A12). Tables keep full structure (§27).

## 3. Bibliographic entities

**meta_analysis_publication** — the audited publication.

**publication** — a primary-literature report *cited by the review*:
citation fields, `doi/pmid/openalex_id`, `citation_as_reported` (verbatim),
`resolution_state`, `match_confidence`; **publication_candidate** rows for
unresolved matches. Scope note (A19): publications enter this table only via
the meta-analysis's own references/tables/supplements — there is no discovery
of outside literature.

**oa_location** — §28 fields. Failed lookups write `external_call_log` +
`workflow_issue`, never a domain row (§60, A4).

**study** — grouping entity: `label`, `stable_code`. No citation fields.

**study_membership** — `study_id, publication_id, basis, confidence,
review_state`, `superseded_by`.

**identity_resolution_event†** (A5) — every identity change:
`op ∈ {MERGE, SPLIT, REASSIGN_PUBLICATION, REASSIGN_SAMPLE, UNDO}`,
`inputs/outputs (ids), actor, timestamp, rationale, reverses_event_id NULL`.
Reversible, provenance-preserving, shown in review history. Extraction records
and effect rows always keep the verbatim printed study label, so regrouping
never rewrites evidence.

**study_label_mention†** — every printed study-label occurrence with locator;
the substrate for internal study-set consistency checks (§24, A19-in-scope).

## 4. Study structure (populated at primary-parsing stage)

**sample** — participant pool: `study_id, description, n_recruited,
recruitment_period, sites, registration_id`.

**arm** — `study_id, label, kind` (`INTERVENTION | CONTROL | OTHER`),
`description`. **No FK to sample** (A13).

**sample_arm_membership** (A13) — explicit association:
`sample_id, arm_id, n NULL, analysis_population NULL, site NULL,
subgroup NULL, context, provenance refs`. Handles multi-site, ITT/completer,
factorial, subsets, subgroup-specific analyses.

**sample_overlap_claim** — pair of samples, evidence, `state`
(`SUGGESTED | CONFIRMED | REJECTED`) — a reviewable assertion, never a boolean
truth (A13, §25).

**measure** (A17) — measurement instrument: `name` ("BDI-II"),
`higher_is_better ∈ {TRUE, FALSE, UNKNOWN}` (default UNKNOWN,
researcher-editable). **outcome** — `reported_outcome` (verbatim),
`normalized_outcome` ("Depression"), `measure_id NULL`. Direction attaches to
the measure, not the concept.

**timepoint** — `reported_label` (verbatim), `normalized_kind`, `time_value,
time_unit NULL`.

## 5. Stated rules (A20)

**stated_rule** — structured, provenance-backed representation of the review's
published rules: `rule_kind ∈ {ELIGIBILITY_CRITERIA, DATA_SELECTION,
EFFECT_MEASURE, TIMEPOINT_SELECTION, OUTCOME_SELECTION, MULTIPLE_OUTCOME_HANDLING,
MULTIPLE_ARM_HANDLING, ADJUSTED_VS_UNADJUSTED_PREFERENCE,
ITT_VS_COMPLETER_PREFERENCE}`, `rule_text` (verbatim), `structured_form`
(machine-usable representation where extractable), `source_locator_id`
(Methods / protocol / preregistration / supplement), plus the standard
basis/confidence/review fields. Rule-vs-implementation checks compare
`stated_rule` against observed selections and emit **possible**-level findings
only (doc 00 O2; A24).

## 6. Analyses and effects

**analysis** — one pooled estimate the publication reports (A7):
`outcome_id, timepoint_id, population, comparison_desc, subgroup_label,
parent_analysis_id NULL, effect_measure, model`, orientation fields (A10):
`group_order, reported_effect_orientation, analysis_direction_convention`;
`n_studies_reported`; published pooled numbers as data points; locator.
**analysis_method** — M11 fields, each nullable + basis (`UNRESOLVED` allowed —
feeds doc 00 O1 method-variant handling).

**published_effect** — study-level row as the meta-analysis reports it:

```text
study_id NULL, study_label_reported,
treatment_label_reported, comparator_label_reported (A6),
outcome_label_reported, timepoint_label_reported,
n_treatment_dp, n_control_dp, effect_dp, se_dp, var_dp,
ci_lower_dp, ci_upper_dp, weight_dp,
adjusted_flag, analysis_population,
row_kind (STUDY | SUBGROUP_TOTAL | OVERALL_TOTAL | HETEROGENEITY | SUBGROUP_TEST)
```

No direct `analysis_id` column; membership is explicit (A7):

**analysis_effect_membership** — `analysis_id, effect_id, membership_role,
subgroup_label_reported, included_in_pool BOOL`. One effect can belong to the
overall analysis, a subgroup analysis, and other legitimate analyses without
duplication. (QC: every `row_kind = STUDY` effect has ≥1 membership.)

**primary_value** — candidate numeric facts from primary studies (§30–31):
`publication_id, sample_id NULL, arm_id NULL, outcome_id NULL,
timepoint_id NULL, statistic` enum, `value_dp`, `analysis_population`,
`context`, `interpretation`, `is_selected BOOL` (selection is revisioned and
reviewable). Bare context-free numbers are unrepresentable (§30).

**arm_mapping** (A6) — reported labels ↔ primary arm/outcome/timepoint
entities, with confidence, review_state, provenance. Never auto-equated on
name similarity.

## 7. Calculation, correspondence, and audit

**calculation†** — engine invocation (§32): `formula_id, formula_version,
engine_version`, inputs via `calculation_input†(data_point_id, role)`, outputs
as DERIVED data points, `warnings`, and an **input_quality_summary** (A2/A3:
counts of input revisions by scientific_basis × review_state — the lineage
itself remains the source of truth).

**reconstructed_effect** — our study-level result: effect/SE/CI data points,
`calculation_id`, `status` (`RECONSTRUCTED | INSUFFICIENT_DATA | AMBIGUOUS |
SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` (A22)), `missing_data_map` (§42).

**effect_correspondence** (A23) — the only bridge the comparison engine may
use: `published_effect_id, reconstructed_effect_id, mapping_type
(ONE_TO_ONE | ONE_TO_MANY | MANY_TO_ONE), confidence, review_state, evidence`.
Composite reconstructed values for non-1:1 mappings are themselves engine
calculations (doc 00 O5).

**reconstructed_pool** — our pooled result per analysis: weights, pooled
effect, SE, CI, Q, I², tau², prediction interval — data points tied to one
calculation.

**audit_comparison** — published vs reconstructed through a correspondence
(A23). Stores the A8 three-question results *separately*:

```text
correspondence_id (or pool refs)
absolute_difference, relative_difference, published_precision
rounding_match BOOL                       -- Q1
numerical_match ∈ {MATCH, MISMATCH}       -- Q2 (computational tolerance only,
                                          --  statistic-specific, versioned)
method_reproduction ∈                     -- O1 (method-dependent comparisons)
   {METHOD_SPECIFIED_MATCH,
    METHOD_UNSPECIFIED_VARIANT_MATCH,     -- weaker than SPECIFIED_MATCH,
    METHOD_UNSPECIFIED_NO_MATCH,          --  reported as such
    METHOD_UNRESOLVED}
variants_attempted                        -- every supported variant tried,
                                          --  each with its calculation_id (O1)
tolerance_rule_id, tolerance_rule_version
severity ∈ {NONE, REVIEW, MINOR, MATERIAL} -- Q3 (assessed separately)
severity_rule_id, severity_rule_version
severity_factors                          -- sign reversal, weight impact,
                                          -- pool impact, population mismatch…
```

**audit_finding / finding_evidence / workflow_issue** — doc 05.

## 8. Workflow and infrastructure

**review_event†** — every researcher action (§21): actor, target, action
(`VERIFY | CORRECT | MARK_UNCERTAIN | EXCLUDE | NOTE | CLASSIFY | RESOLVE_IDENTITY`),
`previous_revision_id`, `new_revision_id`, note. Undo restores a prior
revision as a new revision.

**job** — `stage_id, work_item_ref, idempotency_key, parent_job_id,
input_hash, state, attempt, lease_owner, lease_expires_at, error` (A11:
at-least-once + leases; SQLite-compatible). **stage_state** — doc 04.
**cache_entry** — §62. **external_call_log†** — §58/§63 incl. `model_role` and
**concrete `model_id`** per call (A16).

## 9. Schema-enforced quality controls (§54)

- `data_point` requires locator XOR calculation provenance (CHECK).
- Every `row_kind = STUDY` published effect must gain ≥1
  `analysis_effect_membership` (QC job flags orphans).
- `review_event.previous_revision_id` NOT NULL for corrections.
- Partial unique indexes prevent duplicate published_effect per (locator row).
- Identity events must reference existing entities and be reversible
  (`UNDO` targets recorded event).
- Cross-row checks (study counts vs analysis records, shared-control flags,
  low-confidence-never-verified, membershipless effects) run as the
  ValidationEngine QC stage, emitting findings/issues per A4.
