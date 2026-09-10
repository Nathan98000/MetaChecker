"""Strict schema validation for vision output (Phase 1b)."""

import json

from app.domain.forest_schema import validate_response

GOOD = json.dumps(
    {
        "region_readable": True,
        "columns_seen": ["Study or Subgroup", "HR (95% CI)", "% Weight"],
        "rows": [
            {
                "row_kind": "STUDY_ROW",
                "study_label": "Hong (2015)",
                "effect_value": "1.38",
                "ci_lower": "1.02",
                "ci_upper": "1.85",
                "weight": "5.67",
            },
            {
                "row_kind": "OVERALL_SUMMARY",
                "study_label": "Overall  (I-squared = 78.5%, p = 0.000)",
                "effect_value": "1.69",
                "ci_lower": "1.42",
                "ci_upper": "2.01",
                "weight": "100.00",
            },
            {"row_kind": "HETEROGENEITY", "note": "I-squared = 78.5%, p = 0.000"},
        ],
    }
)


def test_valid_response_accepted():
    result = validate_response(GOOD)
    assert result.ok, result.errors
    assert len(result.rows) == 3
    assert result.rows[1]["row_kind"] == "OVERALL_SUMMARY"


def test_markdown_fences_are_tolerated():
    result = validate_response(f"```json\n{GOOD}\n```")
    assert result.ok


def test_non_json_rejected():
    result = validate_response("The forest plot shows 22 studies with HR 1.69.")
    assert not result.ok
    assert "not valid JSON" in result.errors[0]


def test_unknown_row_field_rejected():
    bad = json.dumps({"rows": [{"row_kind": "STUDY_ROW", "confidence": "high"}]})
    result = validate_response(bad)
    assert not result.ok  # the model may not invent fields (incl. confidence)


def test_invalid_row_kind_rejected():
    bad = json.dumps({"rows": [{"row_kind": "POOLED"}]})
    result = validate_response(bad)
    assert not result.ok


def test_numeric_types_rejected_values_must_be_verbatim_strings():
    bad = json.dumps({"rows": [{"row_kind": "STUDY_ROW", "effect_value": 1.69}]})
    result = validate_response(bad)
    assert not result.ok


def test_abstention_is_legal():
    ok = json.dumps(
        {"rows": [{"row_kind": "STUDY_ROW", "study_label": "Jin (2017)", "effect_value": "UNRESOLVED"}]}
    )
    result = validate_response(ok)
    assert result.ok


def test_unreadable_region_is_legal():
    ok = json.dumps({"region_readable": False, "rows": []})
    result = validate_response(ok)
    assert result.ok
    assert result.meta["region_readable"] is False


def test_partial_garbage_rows_fail_whole_response():
    mixed = json.dumps(
        {"rows": [
            {"row_kind": "STUDY_ROW", "study_label": "A", "effect_value": "1.0"},
            {"row_kind": "STUDY_ROW", "made_up_field": "x"},
        ]}
    )
    result = validate_response(mixed)
    assert not result.ok  # strict: structural errors are retry-worthy
