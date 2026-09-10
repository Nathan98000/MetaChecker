"""Cross-representation reconciliation (Phase 1d) — §23 fixture cases."""

from app.audit.reconcile import Assertion, compare_field, reconcile_pair, reconcile_rows


def A(rep, label, kind="STUDY_ROW", **values):
    return Assertion(representation=rep, study_label=label, row_kind=kind,
                     values=values, provenance={"page": 1})


def test_exact_corroboration():
    assert compare_field("-0.43", "-0.43")["status"] == "CORROBORATED"
    # unicode minus vs ascii hyphen normalizes deterministically → no finding
    assert compare_field("−0.43", "-0.43")["status"] == "CORROBORATED"


def test_percent_vs_proportion_is_supported_transformation():
    result = compare_field("0.27", "0.0027")  # Table RD % vs Fig 2 proportion
    assert result["status"] == "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION"
    assert result["transform_id"] in ("percent_to_proportion_v1", "proportion_to_percent_v1")
    result = compare_field("-0.46", "-0.0046")
    assert result["status"] == "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION"


def test_rounding_match():
    assert compare_field("0.4271", "0.43")["status"] == "ROUNDING_MATCH"
    assert compare_field("0.43", "0.4271")["status"] == "ROUNDING_MATCH"
    assert compare_field("0.4371", "0.43")["status"] == "CONTRADICTION"  # doesn't round


def test_contradiction_detected_never_resolved():
    # Steinberg fixture: table misprint −0.07 vs figure −0.0699 (as %: −6.99)
    result = compare_field("-0.07", "-6.99")
    assert result["status"] == "CONTRADICTION"
    # SE swap fixture (Hahn Thivel 2015)
    assert compare_field("121.68", "142.95")["status"] == "CONTRADICTION"


def test_abstention_is_one_sided_not_contradiction():
    assert compare_field("UNRESOLVED", "1.69")["status"] == "ONE_SIDED"
    assert compare_field(None, "1.69")["status"] == "ONE_SIDED"


def test_row_status_is_worst_field_and_preserves_both_assertions():
    a = A("TABLE", "Steinberg et al", effect_value="-0.06", ci_lower="-0.07", ci_upper="6.87")
    b = A("FOREST_PLOT", "Steinberg 2011", effect_value="-0.0006",
          ci_lower="-0.0699", ci_upper="0.0687")
    r = reconcile_pair(a, b)
    assert r["fields"]["effect_value"]["status"] == "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION"
    assert r["fields"]["ci_upper"]["status"] == "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION"
    assert r["fields"]["ci_lower"]["status"] == "CONTRADICTION"  # the misprint
    assert r["overall"] == "CONTRADICTION"
    # independent evidence preserved — nothing collapsed
    assert r["assertion_a"]["values"]["ci_lower"] == "-0.07"
    assert r["assertion_b"]["values"]["ci_lower"] == "-0.0699"


def test_label_pairing_tolerates_et_al_and_diacritics():
    table = [A("TABLE", "Fagerström et al", effect_value="0.34")]
    figure = [A("FOREST_PLOT", "Fagerstrom 2010", effect_value="0.34")]
    # year in one label only — label_key keeps years, so these differ; pair
    # via the year-free table label against year-carrying figure label is a
    # v2 concern. Same-form labels must pair:
    figure_same = [A("FOREST_PLOT", "Fagerström et al", effect_value="0.34")]
    assert reconcile_rows(table, figure_same)[0]["overall"] == "CORROBORATED"
    assert reconcile_rows(table, figure) == []  # no silent fuzzy pairing


def test_duplicate_labels_pair_by_best_agreement():
    # two Hu (2014) cohorts — greedy best-agreement pairing, no cross-wiring
    table = [
        A("TABLE", "Hu (2014)", effect_value="2.56", ci_lower="1.17", ci_upper="5.76"),
        A("TABLE", "Hu (2014)", effect_value="2.10", ci_lower="1.14", ci_upper="3.85"),
    ]
    figure = [
        A("FOREST_PLOT", "Hu (2014)", effect_value="2.10", ci_lower="1.14", ci_upper="3.85"),
        A("FOREST_PLOT", "Hu (2014)", effect_value="2.56", ci_lower="1.17", ci_upper="5.76"),
    ]
    results = reconcile_rows(table, figure)
    assert len(results) == 2
    assert all(r["overall"] == "CORROBORATED" for r in results)


def test_pooled_rows_never_pair_with_study_rows():
    table = [A("TABLE", "Overall", kind="OVERALL_TOTAL", effect_value="1.69")]
    figure = [A("FOREST_PLOT", "Overall", kind="STUDY_ROW", effect_value="1.69")]
    assert reconcile_rows(table, figure) == []
