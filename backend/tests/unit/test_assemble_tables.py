"""Deterministic table/RevMan assembly (Phase 1c) — permanent fixtures per
the §23 list: RevMan text forests, effect-column tables, pooled rows, UC
cells, summary-table exclusion, percent values, superscript stripping."""

from app.pipeline.stages.assemble_tables import parse_page


def _page(lines: list[list[tuple[str, float, float]]], page_number=1):
    """Build a TEXT_SPANS-shaped page from (text, x, y) span tuples."""
    spans = []
    for line in lines:
        for text, x, y in line:
            spans.append({"text": text, "bbox_native": [x, y, x + max(8, 6 * len(text)), y + 9]})
    return {"page_number": page_number, "width": 595, "height": 842, "spans": spans}


REVMAN = _page([
    [("Study or subgroup", 40, 100), ("Exercise", 200, 100), ("Control", 280, 100),
     ("Std. Mean Difference", 360, 100), ("Weight", 470, 100)],
    [("Blumenthal 1999", 40, 120), ("55", 200, 120), ("8.7 (6.9)", 230, 120),
     ("48", 300, 120), ("7.8 (6.5)", 330, 120), ("4.23%", 470, 120), ("0.14[-0.25,0.52]", 510, 120)],
    [("Veale 1992", 40, 140), ("36", 200, 140), ("13.9 (12.8)", 230, 140),
     ("29", 300, 140), ("17.8 (10.2)", 330, 140), ("3.84%", 470, 140), ("-0.33[-0.82,0.17]", 510, 140)],
    [("Total (95% CI)", 40, 160), ("711", 200, 160), ("642", 300, 160),
     ("100%", 470, 160), ("-0.62[-0.81,-0.42]", 510, 160)],
    [("Heterogeneity: Tau²=0.27; Chi²=91.4, df=34(P<0.0001); I²=62.78%", 40, 180)],
])


def test_revman_rows_assembled_with_kinds_and_weights():
    records = parse_page(REVMAN)
    by_label = {r["study_label"]: r for r in records}
    b = by_label["Blumenthal 1999"]
    assert (b["effect_value"], b["ci_lower"], b["ci_upper"]) == ("0.14", "-0.25", "0.52")
    assert b["weight"] == "4.23"
    assert b["row_kind"] == "STUDY_ROW"
    assert b["effect_measure"] == "SMD"
    assert by_label["Veale 1992"]["effect_value"] == "-0.33"
    total = by_label["Total (95% CI)"]
    assert total["row_kind"] == "OVERALL_TOTAL"
    assert total["effect_value"] == "-0.62"
    # heterogeneity line produces no STUDY_ROW
    assert all(r["row_kind"] != "STUDY_ROW" or "Heterogeneity" not in r["study_label"]
               for r in records)


EFFECT_COLUMNS = _page([
    [("Study", 40, 90), ("Events/randomised", 150, 90), ("Allocation", 260, 90)],
    [("Peto odds ratio", 320, 104), ("Odds ratio", 400, 104),
     ("Relative risk", 460, 104), ("Risk difference (%)", 530, 104)],
    [("Fagerstrom et al", 40, 120), ("24", 130, 120), ("0/214", 150, 120), ("1/218", 200, 120),
     ("1:1", 260, 120), ("0.14 (0.00 to 6.95)", 300, 120), ("0.34 (0.14 to 8.34)", 390, 120),
     ("0.34 (0.01 to 8.29)", 455, 120), ("-0.46 (-1.73 to 0.81)", 525, 120)],
    [("Rennard et al", 40, 140), ("44", 125, 140), ("0/493", 150, 140), ("0/166", 200, 140),
     ("3:1", 260, 140), ("UC", 320, 140), ("UC", 400, 140), ("UC", 460, 140),
     ("0 (-0.87 to 0.87)", 525, 140)],
    [("All trials combined", 40, 160), ("34/5431", 150, 160), ("18/3801", 200, 160),
     ("1.58 (0.90 to 2.76)", 300, 160), ("1.41 (0.82 to 2.42)", 390, 160),
     ("1.40 (0.82 to 2.39)", 455, 160), ("0.27 (-0.10 to 0.63)", 525, 160)],
])


def test_effect_columns_ordered_attribution_and_uc():
    records = parse_page(EFFECT_COLUMNS)
    fagerstrom = [r for r in records if r["study_label"] == "Fagerstrom et al"]
    assert len(fagerstrom) == 4  # superscript "24" stripped from the label
    by_measure = {r["effect_measure"]: r for r in fagerstrom}
    assert by_measure["Peto OR"]["effect_value"] == "0.14"
    assert by_measure["RR"]["ci_lower"] == "0.01"      # RR vs OR disambiguated
    assert by_measure["OR"]["ci_lower"] == "0.14"
    assert by_measure["RD"]["effect_value"] == "-0.46"
    assert fagerstrom[0]["events_treatment"] == "0/214"
    assert fagerstrom[0]["events_control"] == "1/218"

    rennard = [r for r in records if r["study_label"] == "Rennard et al"]
    ucs = [r for r in rennard if r["effect_value"] == "UC"]
    assert len(ucs) == 3  # abstention cells preserved, never guessed
    rd = [r for r in rennard if r["effect_measure"] == "RD"][0]
    assert (rd["effect_value"], rd["ci_lower"]) == ("0", "-0.87")

    pooled = [r for r in records if r["study_label"] == "All trials combined"]
    assert all(r["row_kind"] == "OVERALL_TOTAL" for r in pooled)


def test_summary_table_rows_are_not_study_rows():
    page = _page([
        [("Outcome or subgroup title", 40, 100), ("No. of studies", 300, 100)],
        [("2 Reduction in depression", 40, 120), ("8", 300, 120), ("377", 340, 120),
         ("-0.33 [-0.63, -0.03]", 420, 120)],
    ])
    records = parse_page(page)
    assert not any(r["row_kind"] == "STUDY_ROW" for r in records)


def test_cell_bbox_provenance_present():
    records = parse_page(REVMAN)
    study = [r for r in records if r["row_kind"] == "STUDY_ROW"][0]
    assert study["cell_bboxes"].get("label")
    assert study["cell_bboxes"].get("effect")
    assert study["line_bbox"][0] < study["line_bbox"][2]
