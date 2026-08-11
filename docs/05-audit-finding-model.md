# Audit-Finding Data Model

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 00 (A4, A8, A19, A20, A22–A24), doc 02, doc 03

Two conceptual entities (A4): **`audit_finding`** for scientifically
meaningful results, **`workflow_issue`** (doc 04 §4) for inability to complete
an audit step. Both feed one Review Queue; they are never conflated in counts,
reports, or exports. "17 audit findings" can never include an API failure.

---

## 1. `audit_finding`

```text
audit_finding
  id, project_id
  finding_kind         -- CONTRADICTION | DISCREPANCY | STUDY_IDENTITY_ISSUE |
                       -- DATA_SELECTION_ISSUE | STATISTICAL_ISSUE        (A4)
  taxonomy_code        -- §45 codes, scope-corrected (see §2 below)
  severity             -- NONE | REVIEW | MINOR | MATERIAL   (A8 Q3 — assessed
                       --   separately from numerical match; rule-versioned)
  certainty            -- CONFIRMED | LIKELY | POSSIBLE | UNABLE_TO_VERIFY (§48)
  review_status        -- SYSTEM_FLAGGED | RESEARCHER_CONFIRMED | EXPLAINED |
                       -- DISMISSED | UNRESOLVED                          (A24)
  title / description  -- plain language, non-accusatory (§48)
  analysis_id NULL, study_id NULL, publication_id NULL, effect refs NULL
  audit_comparison_id NULL
  detected_by          -- stage_id + version | RESEARCHER
  resolution_note
  taxonomy_code_original   -- preserved when researcher reclassifies (§45)
```

Conservatism rules (A24):

- Automated detection always creates findings with
  `review_status = SYSTEM_FLAGGED`; `certainty = CONFIRMED` is reachable only
  via researcher confirmation or a fully deterministic re-derivation from
  verified inputs.
- Eligibility- and rule-consistency findings (A20) are capped at
  `certainty = POSSIBLE` until researcher-reviewed (doc 00 O2) and must cite
  explicit textual evidence spans.
- A22: unreconstructable/differing values traced to author-supplied or
  non-public data are **not** findings; they are recorded as
  `SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` on the reconstructed effect and appear
  in the report under "unable to verify".

## 2. Taxonomy (§45, scope-corrected per A19)

```text
STUDY_SET_INCONSISTENCY        -- internal: table/plot/reference/count disagree
ELIGIBILITY_INCONSISTENCY      -- included study vs stated criteria (A20)
DUPLICATE_SAMPLE
CITATION_MISMATCH
SUBGROUP_ASSIGNMENT_INCONSISTENCY
SAMPLE_SIZE_DISCREPANCY
OUTCOME_MISMATCH
TIMEPOINT_MISMATCH
GROUP_MISMATCH
RULE_IMPLEMENTATION_INCONSISTENCY  -- stated rule vs observed selection (A20)
SIGN_REVERSAL
TRANSCRIPTION_DISCREPANCY
EFFECT_CALCULATION_DISCREPANCY
VARIANCE_DISCREPANCY
WEIGHTING_DISCREPANCY
POOLING_DISCREPANCY
HETEROGENEITY_DISCREPANCY
UNEXPLAINED_DISCREPANCY
```

**Removed from the SRS §45 list (A19):** `STUDY_OMISSION` and any equivalent
(`ELIGIBLE_STUDY_OMITTED`, `MISSING_ELIGIBLE_STUDY`,
`LITERATURE_COVERAGE_FAILURE`). Detecting studies absent from the published
review's study set is out of scope. The in-scope remnant of "inclusion
problems" is `STUDY_SET_INCONSISTENCY` (a study present in one internal
representation but missing from another) and `ELIGIBILITY_INCONSISTENCY`
(an *included* study apparently violating stated criteria).

## 3. `finding_evidence`

```text
finding_evidence(finding_id, role, data_point_id NULL, source_locator_id NULL,
                 stated_rule_id NULL, note)
  role -- SIDE_A | SIDE_B | RULE | CONTEXT
```

Contradiction/discrepancy findings require ≥2 anchors; rule-consistency
findings require the `RULE` anchor (the stated rule's locator) plus the
observed-implementation anchor. Every report line traces:
`finding → evidence → data_point/value_revision → source_locator → page+bbox`.

## 4. `finding_explanation` — candidate explanations (§35, §40)

Suggestions, never asserted facts:

```text
finding_explanation(finding_id, explanation_code, rationale, plausibility,
                    proposed_by SYSTEM|RESEARCHER, state SUGGESTED|ACCEPTED|REJECTED,
                    test_calculation_id NULL)
  explanation_code -- ROUNDING | WRONG_N | WRONG_OUTCOME | WRONG_GROUP |
                   -- WRONG_TIMEPOINT | ADJUSTED_VS_UNADJUSTED | ITT_VS_COMPLETER |
                   -- POST_VS_CHANGE | DIRECTION_REVERSED | SIGN_CONVENTION |
                   -- CLUSTER_CORRECTION | SHARED_CONTROL |
                   -- AUTHOR_SUPPLIED_DATA (→ A22 reclassification) |
                   -- METHOD_VARIANT_MATCH (O1) | TRANSCRIPTION |
                   -- INSUFFICIENT_REPORTING | OTHER
```

Deterministically testable explanations (e.g. "matches if completer N used",
"matches under DerSimonian-Laird") store the test's `calculation_id`. An
accepted `AUTHOR_SUPPLIED_DATA` explanation reclassifies the item to
`SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` rather than leaving a discrepancy (A22).

**Method-variant matches are not verification (O1).** When the publication
under-reports its method, the comparison records
`METHOD_UNSPECIFIED_VARIANT_MATCH` with every supported variant attempted, and
report language stays explicitly weaker: *"The publication did not specify the
tau² estimator sufficiently to permit unique reproduction. The published
result is reproduced within tolerance using DerSimonian–Laird"* — never
equated with *"The publication reports using DerSimonian–Laird, and that
calculation was independently reproduced"* (`METHOD_SPECIFIED_MATCH`). Only
statistically appropriate, explicitly supported variants are ever tried.

## 5. Severity model (A8 Q3)

Severity is computed *after* and *independently of* numerical matching, from
versioned rules over stored factors:

```text
severity_factors: sign_reversal, analysis_population_mismatch,
  weight_impact, pooled_estimate_impact, heterogeneity_impact,
  outcome/timepoint/group_mismatch, magnitude_vs_uncertainty,
  explained (accepted explanation present)
```

Defaults: an unexplained sign reversal or population mismatch → `MATERIAL`;
an unexplained N difference (84 vs 81) → `REVIEW` (not material until its
cause and analytical impact are known); `ROUNDING_MATCH` → `NONE`. All rules
versioned; comparisons store `severity_rule_id/version` so re-judging is
reproducible.

## 6. Source-of-discrepancy localization (§38)

Pool-level discrepancies get `finding_diagnosis(finding_id, layer, detail,
method, calculation_ids)` with `layer ∈ {STUDY_SET_AS_IMPLEMENTED,
DATA_SELECTION, EFFECT_CALCULATION, MODEL}` — computed by substitution
experiments (re-pool with published study-level values vs ours; alternative
tau²; toggle questionable memberships), each experiment a provenance-carrying
calculation. Presented with the experiment shown, never as bare assertion.
(Layer 1 concerns the *implemented* study set only — never external
literature, A19.)

## 7. Review queue (§39)

One queue over `audit_finding` + `workflow_issue` + `REVIEW_REQUIRED`
revisions, with the type boundary visible (findings vs. "steps that need
attention"). Priority order per §39; filters: severity, analysis, study, issue
type, review status. Every action writes a `review_event†`.

## 8. Rollups (§15, §47) and report language

Dashboard/audit-summary counters are SQL views — separate counters for audit
findings and workflow issues (A4). The report distinguishes *evidence of a
possible problem*, *confirmed discrepancy*, and *inability to verify* (A4,
A24), includes the A21 scope note ("search completeness and potentially
omitted eligible studies were not assessed"), and never emits
"fully verified" phrasing — only "all supported audit checks completed"
alongside the displayed scope.
