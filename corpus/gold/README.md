# Gold-Standard Truth Sets

Layout per paper (`corpus/gold/<slug>/`):

```text
source/                 original PDFs (legal copies only; content-addressed by
                        the app at ingest — never edited here)
truth/
  meta.json             citation, DOI, OA URL, corpus_role
                        (development | holdout), rationale
  analyses.csv          one row per pooled analysis the paper reports
  study_labels.csv      every study label as printed, per analysis
  published_effects.csv study-level rows as the paper reports them
  contradictions.csv    documented internal contradictions / known
                        discrepancies (incl. errata deltas)
  notes.md              truth provenance: who extracted (pass A / pass B),
                        reconciliation log, sign-off state
```

## Certainty states (mandatory on every truth value)

```text
KNOWN           the source states it unambiguously
AMBIGUOUS       the source permits more than one reading (say why in note)
UNRESOLVED      the source does not permit a reliable answer
NOT_APPLICABLE  the field does not apply to this row
```

Scoring rule: a system **abstention on an AMBIGUOUS/UNRESOLVED truth value is
correct behavior**, never an extraction failure. Only KNOWN values count
toward accuracy denominators; confidently extracting a value the truth marks
UNRESOLVED counts toward the false-extraction rate.

## Conventions

- Values are stored as **verbatim strings at published precision** ("0.43",
  "1.69", "44/10 285"), plus a `value_norm` numeric column where parsing is
  unambiguous. Unicode minus/hyphen variants are preserved verbatim.
- `row_kind`: STUDY | SUBGROUP_TOTAL | OVERALL_TOTAL | HETEROGENEITY |
  SUBGROUP_TEST — pooled rows must never be scored as study rows.
- `source_page` is the 1-based page of the PDF file in `source/` (not the
  journal pagination). `source_type`: TABLE | FOREST_PLOT | TEXT | SUPPLEMENT.
- Erratum-affected values appear twice: `version=AS_PUBLISHED` and
  `version=AS_CORRECTED`, with the erratum cited as the source of the latter.
- Truth files are append-only in spirit: corrections happen via new rows with
  `supersedes` set, mirroring the app's own provenance rules.

## Truth provenance

Truth v0 is constructed by two independent extraction passes (recorded in
`notes.md`) followed by reconciliation; disagreements are logged, not
silently resolved. Truth status remains `DRAFT` until researcher spot-check
and sign-off is recorded in `notes.md`. Statistical expected values for the
engine (later phases) additionally require non-AI ground truth per SRS §57.

## File schemas

`analyses.csv`:
`analysis_id, outcome, timepoint, population, comparison, subgroup_of,
effect_measure, model, n_studies_reported, pooled_effect, pooled_ci_lower,
pooled_ci_upper, i2, tau2, q, p_value, source_page, source_figure,
source_table, certainty, note`

`study_labels.csv`:
`analysis_id, study_label_verbatim, appears_in (TABLE|FOREST_PLOT|TEXT|
REFERENCES|SUPPLEMENT; semicolon-joined), source_pages (semicolon-joined),
certainty, note`

`published_effects.csv`:
`effect_id, analysis_id, row_kind, study_label, version, effect_measure,
effect, ci_lower, ci_upper, se, variance, weight_pct, n_treatment, n_control,
events_treatment, events_control, subgroup, timepoint, source_page,
source_type, source_table, source_figure, row_label, effect_norm,
ci_lower_norm, ci_upper_norm, certainty, supersedes, note`

`contradictions.csv`:
`contradiction_id, kind (INTERNAL|ERRATUM|EXTERNAL_CRITIQUE), description,
side_a_value, side_a_source, side_b_value, side_b_source, certainty, note`
