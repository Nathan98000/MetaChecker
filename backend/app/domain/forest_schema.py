"""Structured forest-plot extraction schema + strict validation (Phase 1b).

The vision model must return JSON matching this schema. Validation is strict:
unknown keys, wrong types, or invalid row_kind values are ERRORS, not silently
coerced — a model that free-styles gets rejected and retried, never trusted.
Values are verbatim strings ("1.69", "-0.43", "UC"); "UNRESOLVED" is an
explicit, legal abstention for any unreadable cell. The model never assigns
confidence (§12); it only reports what it can and cannot read.
"""

import json
import re
from dataclasses import dataclass, field

ROW_KINDS = {"STUDY_ROW", "SUBGROUP_SUMMARY", "OVERALL_SUMMARY", "HETEROGENEITY", "OTHER"}

ROW_FIELDS = {
    "study_label",
    "subgroup",
    "effect_measure",
    "effect_value",
    "ci_lower",
    "ci_upper",
    "standard_error",
    "weight",
    "n_treatment",
    "n_control",
    "events_treatment",
    "events_control",
    "row_kind",
    "note",
}
REQUIRED_ROW_FIELDS = {"row_kind"}
TOP_FIELDS = {"rows", "columns_seen", "axis_labels", "region_readable", "reading_notes"}

PROMPT_ID = "forest_plot_rows"
PROMPT_VERSION = "1"

PROMPT = """You are reading ONE figure region cropped from a published meta-analysis PDF. \
It is likely a forest plot (or part of one). Transcribe it into JSON.

Rules — these are strict:
1. Output ONLY a JSON object, no prose, no markdown fences.
2. Schema:
{
  "region_readable": true|false,
  "columns_seen": ["..."],            // column headers exactly as printed
  "axis_labels": ["..."],             // axis tick labels / direction labels if printed
  "reading_notes": "...",             // optional; anything ambiguous
  "rows": [
    {
      "row_kind": "STUDY_ROW" | "SUBGROUP_SUMMARY" | "OVERALL_SUMMARY" | "HETEROGENEITY" | "OTHER",
      "study_label": "...",           // verbatim, preserve misspellings/case/spacing
      "subgroup": "...",              // the subgroup section this row sits under, if any
      "effect_measure": "...",        // e.g. "HR", "MD", "RD", "SMD" if the figure says
      "effect_value": "...",          // verbatim string, e.g. "-0.43"
      "ci_lower": "...", "ci_upper": "...",
      "standard_error": "...", "weight": "...",
      "n_treatment": "...", "n_control": "...",
      "events_treatment": "...", "events_control": "...",
      "note": "..."
    }
  ]
}
3. Every visually distinct data line becomes one row. Classify row_kind carefully: \
subtotal/pooled diamonds are SUBGROUP_SUMMARY or OVERALL_SUMMARY, never STUDY_ROW. \
Heterogeneity/test lines (Tau², Chi², I², Z) are HETEROGENEITY with the statistics in "note". \
Never assume every aligned row is a study.
4. Transcribe verbatim at printed precision. Do NOT normalize signs, decimals, or spelling.
5. If a cell is unreadable or absent, write "UNRESOLVED" — never guess. \
If the whole region is not interpretable (not a data figure, too blurry), set "region_readable": false with empty rows.
6. Omit fields that the figure simply does not have columns for; include every field the figure shows."""


@dataclass
class ValidationResult:
    ok: bool
    rows: list[dict] = field(default_factory=list)
    meta: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def _strip_fences(text: str) -> str:
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    return match.group(1) if match else text


def validate_response(text: str) -> ValidationResult:
    errors: list[str] = []
    try:
        payload = json.loads(_strip_fences(text))
    except json.JSONDecodeError as exc:
        return ValidationResult(ok=False, errors=[f"not valid JSON: {exc}"])
    if not isinstance(payload, dict):
        return ValidationResult(ok=False, errors=["top level is not an object"])

    unknown_top = set(payload) - TOP_FIELDS
    if unknown_top:
        errors.append(f"unknown top-level fields: {sorted(unknown_top)}")
    if "rows" not in payload or not isinstance(payload.get("rows"), list):
        errors.append("missing or non-list 'rows'")
        return ValidationResult(ok=False, errors=errors)

    rows: list[dict] = []
    for i, row in enumerate(payload["rows"]):
        if not isinstance(row, dict):
            errors.append(f"row {i}: not an object")
            continue
        unknown = set(row) - ROW_FIELDS
        if unknown:
            errors.append(f"row {i}: unknown fields {sorted(unknown)}")
            continue
        missing = REQUIRED_ROW_FIELDS - set(row)
        if missing:
            errors.append(f"row {i}: missing required {sorted(missing)}")
            continue
        if row["row_kind"] not in ROW_KINDS:
            errors.append(f"row {i}: invalid row_kind {row['row_kind']!r}")
            continue
        bad_types = [k for k, v in row.items() if not isinstance(v, str)]
        if bad_types:
            errors.append(f"row {i}: non-string values for {sorted(bad_types)}")
            continue
        rows.append(row)

    meta = {
        "region_readable": bool(payload.get("region_readable", True)),
        "columns_seen": payload.get("columns_seen", []),
        "axis_labels": payload.get("axis_labels", []),
        "reading_notes": payload.get("reading_notes", ""),
    }
    # strict: any structural error fails the whole response (retry-worthy);
    # abstentions inside rows ("UNRESOLVED") are fine.
    return ValidationResult(ok=not errors, rows=rows, meta=meta, errors=errors)
