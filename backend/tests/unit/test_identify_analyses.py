"""Analysis identification (Milestone 2) — unit fixtures for the structural
identifier: RevMan sections, subgroup tables, multi-panel figure regions,
valueless-summary abstention, sequential panel grouping."""

from app.pipeline.stages.identify_analyses import identify


def _record(label, kind, effect, lo, hi, page=105, measure="SMD", **extra):
    return {"study_label": label, "row_kind": kind, "effect_measure": measure,
            "effect_value": effect, "ci_lower": lo, "ci_upper": hi,
            "weight": None, "events_treatment": None, "events_control": None,
            "page_number": page, "line_bbox": [40, 100, 500, 110],
            "cell_bboxes": {}, "acquisition_method": "LAYOUT_EXTRACTION", **extra}


def _text_page(page, lines):
    spans = []
    for i, text in enumerate(lines):
        spans.append({"text": text, "bbox_native": [40, 50 + i * 20, 400, 60 + i * 20]})
    return {"page_number": page, "width": 595, "spans": spans}


def test_revman_section_becomes_analysis_with_members():
    pages = [_text_page(105, [
        "Analysis 1.1. Comparison 1 Exercise versus control, Outcome 1 Reduction in depression.",
    ])]
    records = [
        _record("Blumenthal 1999", "STUDY_ROW", "0.14", "-0.25", "0.52"),
        _record("Veale 1992", "STUDY_ROW", "-0.33", "-0.82", "0.17"),
        _record("Heterogeneity: Tau²=0.27; Chi²=91.35, df=34(P<0.0001); I²=62.78%",
                "HETEROGENEITY", None, None, None),
        _record("Total (95% CI)", "OVERALL_TOTAL", "-0.62", "-0.81", "-0.42"),
    ]
    analyses = identify(pages, records, [])
    assert len(analyses) == 1
    a = analyses[0]
    assert a["revman_ref"] == "1.1"
    assert a["pooled"]["effect_value"] == "-0.62"
    assert a["heterogeneity"]["i2"] == "62.78"
    assert a["member_count"] == 2
    assert a["model"] == "UNCLEAR" or a["model"] in ("RANDOM", "FIXED")


def test_subgroup_table_rows_become_individual_analyses():
    records = [
        _record("Asian", "SUBGROUP_TOTAL", "1.26", "1.12", "1.40", page=4,
                measure="HR", k_studies_hint="17", i2_hint="81.4"),
        _record("Caucasian", "SUBGROUP_TOTAL", "1.55", "0.84", "2.27", page=4,
                measure="HR", k_studies_hint="5"),
    ]
    analyses = identify([], records, [])
    assert len(analyses) == 2
    asian = next(a for a in analyses if "Asian" in a["description"])
    assert asian["member_count"] == 17
    assert asian["pooled"]["ci_upper"] == "1.40"
    assert asian["heterogeneity"].get("i2") == "81.4"


def _region_result(rows, page=6):
    return {"region": {"page_number": page, "kind": "RASTER_IMAGE",
                       "bbox_norm": [0.1, 0.1, 0.9, 0.9],
                       "caption": "Figure 5 Forest plot of the association"},
            "rows": rows, "meta": {"columns_seen": ["HR (95% CI)"]}}


def test_multi_panel_region_yields_one_analysis_per_overall():
    rows = [
        {"row_kind": "STUDY_ROW", "study_label": "Hu (2014)", "effect_value": "2.32",
         "ci_lower": "1.28", "ci_upper": "4.23", "effect_measure": "HR"},
        {"row_kind": "OVERALL_SUMMARY", "study_label": "Overall (I-squared = 0.0%, p = 0.664)",
         "effect_value": "1.87", "ci_lower": "1.42", "ci_upper": "2.47"},
        {"row_kind": "STUDY_ROW", "study_label": "Chen (2017)", "effect_value": "2.72",
         "ci_lower": "2.29", "ci_upper": "3.23"},
        {"row_kind": "OVERALL_SUMMARY", "study_label": "Overall (I-squared = 89.8%, p = 0.000)",
         "effect_value": "1.61", "ci_lower": "1.11", "ci_upper": "2.35"},
    ]
    analyses = identify([], [], [_region_result(rows)])
    assert len(analyses) == 2  # one per panel overall — never merged
    assert analyses[0]["pooled"]["effect_value"] == "1.87"
    assert analyses[0]["member_count"] == 1
    assert analyses[1]["pooled"]["effect_value"] == "1.61"
    assert analyses[1]["heterogeneity"].get("i2") == "89.8"


def test_subgroup_summaries_attach_to_their_panel_overall():
    rows = [
        {"row_kind": "STUDY_ROW", "study_label": "A", "effect_value": "1.0",
         "ci_lower": "0.5", "ci_upper": "1.5", "subgroup": "Low"},
        {"row_kind": "SUBGROUP_SUMMARY", "study_label": "Subtotal", "subgroup": "Low",
         "effect_value": "1.0", "ci_lower": "0.6", "ci_upper": "1.4"},
        {"row_kind": "STUDY_ROW", "study_label": "B", "effect_value": "2.0",
         "ci_lower": "1.5", "ci_upper": "2.5", "subgroup": "High"},
        {"row_kind": "SUBGROUP_SUMMARY", "study_label": "Subtotal", "subgroup": "High",
         "effect_value": "2.0", "ci_lower": "1.6", "ci_upper": "2.4"},
        {"row_kind": "OVERALL_SUMMARY", "study_label": "Total",
         "effect_value": "1.5", "ci_lower": "1.1", "ci_upper": "1.9"},
    ]
    analyses = identify([], [], [_region_result(rows)])
    parent = next(a for a in analyses if a["pooled"]["effect_value"] == "1.5")
    subs = [a for a in analyses if a["subgroup_of"] == parent["analysis_id"]]
    assert len(subs) == 2
    assert {s["pooled"]["effect_value"] for s in subs} == {"1.0", "2.0"}


def test_valueless_summary_rows_are_abstentions_not_analyses():
    rows = [
        {"row_kind": "STUDY_ROW", "study_label": "A", "effect_value": "1.0",
         "ci_lower": "0.5", "ci_upper": "1.5"},
        {"row_kind": "OVERALL_SUMMARY", "study_label": "Total (95% CI)",
         "effect_value": "", "ci_lower": "", "ci_upper": ""},  # Fig-4-style
    ]
    analyses = identify([], [], [_region_result(rows)])
    assert analyses == []  # no numbers printed → nothing detected, no invention
