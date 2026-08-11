# Provenance and Versioning Model

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 00 (A2/A3, A9, A18, A22)

The unit of provenance is the **data point**: one value that matters to the
audit. Every such value carries the **four orthogonal dimensions** of A2/A3:
scientific basis, acquisition method, confidence, review state.

---

## 1. `data_point`

```text
data_point
  id, project_id
  quantity_kind        -- EFFECT_SIZE | SE | VARIANCE | CI_LOWER | CI_UPPER |
                       -- N | EVENTS | MEAN | SD | WEIGHT | TAU2 | I2 | Q | P | ...
  current_revision_id  -- denormalized head pointer
```

## 2. `value_revision`† (append-only; §7, §21, A18)

```text
value_revision
  id, data_point_id, revision_no
  value_text           -- verbatim string as it appeared ("<0.001", "12·4")
  value_numeric        -- exact decimal, nullable
  value_normalized     -- parsed numeric after normalization rules
  unit / scale         -- nullable

  scientific_basis     -- SOURCE_REPORTED | DERIVED | INFERRED | UNRESOLVED (A2)
  acquisition_method   -- EMBEDDED_TEXT | LAYOUT_EXTRACTION | TABLE_PARSER |
                       -- OCR | VISION | LLM | BIBLIOGRAPHIC_API |
                       -- MANUAL_ENTRY | CALCULATION                       (A2)
  confidence           -- HIGH | MEDIUM | LOW
  confidence_rule_id
  confidence_rule_version                                                  (A3)
  review_state         -- NOT_REVIEWED | REVIEW_REQUIRED | VERIFIED |
                       -- CORRECTED | MARKED_UNCERTAIN | EXCLUDED          (A3)

  source_locator_id    -- REQUIRED iff basis ∈ {SOURCE_REPORTED, INFERRED}
  extraction_record_id -- REQUIRED for machine-acquired revisions
  calculation_id       -- REQUIRED iff basis = DERIVED
  verifiability        -- NORMAL | SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE     (A22)
  supersedes_id, created_by, researcher_note
```

Rules:

- Human verification does **not** change `scientific_basis` (a verified
  source-reported value is still source-reported); it sets
  `review_state = VERIFIED` via a new revision + review event.
- The first revision of an extracted data point always carries the verbatim
  `value_text`; normalization is a subsequent revision pointing at it (§7).
- Corrections append `review_state = CORRECTED` revisions; "restore previous
  value" appends a new revision equal to an older one (§21). Only the head
  pointer moves.
- CHECK constraints enforce the locator/calculation requirements — an
  unprovenanced value cannot be committed (§6, §54).

## 3. `source_locator`† — "where did this number come from?" (§6, §11)

```text
source_locator
  id
  document_id          -- NOT NULL
  page_number
  section / source_type / table_number / figure_number
  row_label / column_label
  source_text          -- verbatim surrounding snippet
  bbox_norm            -- (x0,y0,x1,y1), origin top-left, range 0.0–1.0 (A9)
  bbox_native          -- parser-native coordinates, where available    (A9)
  parser_id, parser_version                                             (A9)
  parse_artifact_id
```

Page width/height/rotation live on `document_page`, so any renderer can map
`bbox_norm` to pixels. Locators are immutable and shareable.

## 4. `extraction_record`† — the acquisition event

```text
extraction_record
  id
  acquisition_method   -- as above (A2)
  extractor_id / extractor_version
  model_role           -- FAST_MODEL | DEFAULT_EXTRACTION_MODEL |
                       -- COMPLEX_EXTRACTION_MODEL | ESCALATION_MODEL (A16)
  model_id             -- CONCRETE model actually used, e.g. a full
                       -- versioned model string — required for AI methods (A16)
  prompt_ref / raw_response_ref   -- cached artifacts (§62), auditable
  input_hash
```

## 5. Calculation provenance (§32)

Derived revisions carry `calculation_id`; the `calculation` row carries
`formula_id, formula_version, engine_version, warnings`, and an
**`input_quality_summary`** (A2/A3): aggregate of input revisions by
`scientific_basis × review_state × confidence`, e.g.

```text
inputs: 6 total — 6 SOURCE_REPORTED, of which 5 VERIFIED, 1 NOT_REVIEWED;
        0 INFERRED
```

so the UI can say *"Hedges' g calculated entirely from verified source
values"* vs *"…using one inferred SD"*. The summary is a derived convenience;
the full lineage (`calculation_input` rows → revisions) remains authoritative
and is never collapsed away (A2/A3).

Example chain the UI can always render:

```text
SE = 0.1327  [DERIVED · CALCULATION · HIGH ·
              inputs: 2/2 SOURCE_REPORTED, 1 VERIFIED, 1 REVIEW_REQUIRED]
 └─ calculation: se_from_ci95_v1 (statengine 1.2.0)
     ├─ ci_lower = -0.68  [SOURCE_REPORTED · EMBEDDED_TEXT · VERIFIED]
     │    └─ locator: meta_analysis.pdf p.14, Figure 3, row "Smith 2018"
     └─ ci_upper = -0.16  [SOURCE_REPORTED · VISION · REVIEW_REQUIRED]
```

## 6. Confidence rules (§12) — observable evidence only, versioned (A3)

| Rule (examples) | Confidence |
|---|---|
| Machine-readable table cell, structurally unambiguous | HIGH |
| DOI exact match on resolution | HIGH |
| Derived from all-HIGH, reviewed inputs, no warnings | HIGH |
| Forest-plot value with embedded text layer | MEDIUM |
| Bibliographic match on title+authors+year, no DOI | MEDIUM |
| VISION/OCR acquisition; ambiguous structure; multiple candidates; INFERRED basis; unclear orientation/outcome/timepoint | LOW → `REVIEW_REQUIRED` |

`confidence_rule_id` + `confidence_rule_version` are stored on the revision;
rules are versioned config, so re-scoring is reproducible. LLM self-reported
confidence is never used as the rule input.

**Corroboration upgrades (researcher decision 2026-08-11):** an uncorroborated
vision-only extraction defaults to MEDIUM (`vision_uncorroborated_v1`) — an
initial default, not an architectural ceiling. Rules-based, provenance-recorded
upgrades: vision + matching text-encoded table value → potentially HIGH
(`vision_table_corroborated_v1`); two independent extraction channels agree →
potentially HIGH (`dual_channel_agreement_v1`); researcher verification →
review_state VERIFIED. Each upgrade appends a revision citing both evidence
sources. The model can never upgrade its own confidence.

## 7. Propagation and orientation

- Derived confidence = min(input confidences), further downgradable by rule
  (e.g., engine warning present). Input-quality summary computed as §5.
- Any input `review_state = EXCLUDED` marks dependents `STALE` and queues
  recomputation; prior results remain in history.
- Orientation transformations (A10) — reported ↔ canonical sign — are
  performed only inside engine calculations, so every sign change is itself a
  provenance-recorded calculation step. No source value's sign is ever
  silently altered.
- The recompute graph over `calculation_input` is the §53 evidence graph in
  relational form.
