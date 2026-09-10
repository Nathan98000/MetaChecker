"""Cross-representation reconciliation (Phase 1d, doc 00 A4/A24; researcher
directive items 14-15).

Compares independent source assertions of the same quantity (forest plot vs
table vs text) WITHOUT collapsing them: both assertions and the relationship
are preserved, because agreement within a publication corroborates only what
the publication reports — not that the underlying value is correct.

Field relationship vocabulary:
  CORROBORATED                              exact after verbatim normalization
  EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION deterministic recorded transform
  ROUNDING_MATCH                            one side rounds to the other at
                                            its printed precision
  CONTRADICTION                             none of the above
  ONE_SIDED                                 only one representation states it

Row status = worst field status. No winner is ever chosen (§41).
"""

import re
import unicodedata
from dataclasses import dataclass, field

DASHES = dict.fromkeys(map(ord, "−–—‐‑"), "-")

ORDER = ["CORROBORATED", "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION",
         "ROUNDING_MATCH", "ONE_SIDED", "CONTRADICTION"]

# Supported deterministic transforms (id, forward description)
TRANSFORMS = [
    ("percent_to_proportion_v1", 0.01),
    ("proportion_to_percent_v1", 100.0),
]


def norm_str(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").translate(DASHES)
    return re.sub(r"[\s%]", "", value)


def parse_num(value: str) -> float | None:
    s = norm_str(value)
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def decimals(value: str) -> int:
    s = norm_str(value)
    return len(s.split(".")[1]) if "." in s else 0


def compare_field(a: str | None, b: str | None) -> dict:
    """Compare two verbatim value strings → {status, transform_id?}."""
    a_present = bool((a or "").strip()) and norm_str(a) != "UNRESOLVED"
    b_present = bool((b or "").strip()) and norm_str(b) != "UNRESOLVED"
    if not a_present or not b_present:
        return {"status": "ONE_SIDED"}
    if norm_str(a) == norm_str(b):
        return {"status": "CORROBORATED"}

    na, nb = parse_num(a), parse_num(b)
    if na is None or nb is None:
        return {"status": "CONTRADICTION"}

    # supported deterministic transformations (recorded)
    for transform_id, factor in TRANSFORMS:
        if nb != 0 and abs(na * factor - nb) <= 10 ** (-decimals(b)) * 0.5001:
            return {"status": "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION",
                    "transform_id": transform_id}

    # rounding: the more-precise side rounds to the less-precise side at its
    # printed precision
    da, db = decimals(a), decimals(b)
    if da != db:
        coarse, fine = (na, nb) if da < db else (nb, na)
        places = min(da, db)
        if abs(round(fine, places) - coarse) < 10 ** (-places) * 0.0001:
            return {"status": "ROUNDING_MATCH"}
    return {"status": "CONTRADICTION"}


FIELDS = ["effect_value", "ci_lower", "ci_upper", "standard_error", "weight",
          "n_treatment", "n_control", "events_treatment", "events_control"]


@dataclass
class Assertion:
    """One representation's claim about one row. Never mutated, never merged."""
    representation: str          # FOREST_PLOT | TABLE | TEXT | SUPPLEMENT
    study_label: str
    row_kind: str
    values: dict                 # field -> verbatim string
    provenance: dict = field(default_factory=dict)  # page, bbox, artifact ref


def _compare_under_transform(a: str, b: str, factor: float) -> str:
    na, nb = parse_num(a), parse_num(b)
    if na is None or nb is None:
        return "CONTRADICTION"
    tolerance = 10 ** (-decimals(b)) * 0.5001
    return "CORROBORATED" if abs(na * factor - nb) <= tolerance else "CONTRADICTION"


def reconcile_pair(a: Assertion, b: Assertion) -> dict:
    fields_out = {}
    for f in FIELDS:
        result = compare_field(a.values.get(f), b.values.get(f))
        if result["status"] != "ONE_SIDED" or a.values.get(f) or b.values.get(f):
            fields_out[f] = result

    # Row-level unit context: if ≥2 fields agree under one specific transform,
    # the whole row is in that unit relationship — every other numeric field
    # must be re-evaluated UNDER that transform. A field that only matches via
    # a different accidental relationship (e.g. a rounding coincidence across
    # a percent/proportion boundary) is a CONTRADICTION in row context.
    transform_votes: dict[str, int] = {}
    for v in fields_out.values():
        if v.get("transform_id"):
            transform_votes[v["transform_id"]] = transform_votes.get(v["transform_id"], 0) + 1
    dominant = max(transform_votes, key=transform_votes.get) if transform_votes else None
    if dominant and transform_votes[dominant] >= 2:
        factor = dict(TRANSFORMS)[dominant]
        for f, v in fields_out.items():
            if v["status"] in ("ONE_SIDED",) or v.get("transform_id") == dominant:
                continue
            status = _compare_under_transform(a.values.get(f), b.values.get(f), factor)
            if status == "CORROBORATED":
                fields_out[f] = {"status": "EQUIVALENT_AFTER_SUPPORTED_TRANSFORMATION",
                                 "transform_id": dominant}
            else:
                fields_out[f] = {"status": "CONTRADICTION",
                                 "note": f"fails under row transform {dominant}; "
                                         f"prior per-field status was {v['status']}"}
    statuses = [v["status"] for v in fields_out.values()]
    # Row status = WORST comparable field status; one-sided extras never
    # upgrade or downgrade a row on their own.
    comparable = [s for s in statuses if s != "ONE_SIDED"]
    overall = max(comparable, key=ORDER.index) if comparable else "ONE_SIDED"
    return {
        "study_label": a.study_label,
        "overall": overall,
        "fields": fields_out,
        "assertion_a": {"representation": a.representation, "values": a.values,
                        "provenance": a.provenance},
        "assertion_b": {"representation": b.representation, "values": b.values,
                        "provenance": b.provenance},
    }


def label_key(label: str) -> str:
    s = unicodedata.normalize("NFKD", (label or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\b(19|20)(\d{2})[a-z]?\b", r"\1\2", s)      # keep years
    s = re.sub(r"\bet al\.?\b", "", s)                       # drop 'et al'
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return s


def reconcile_rows(rows_a: list[Assertion], rows_b: list[Assertion]) -> list[dict]:
    """Pair rows across representations by normalized label (duplicates pair
    greedily by best field agreement) and reconcile each pair."""
    results = []
    used_b: set[int] = set()
    for a in rows_a:
        candidates = [
            (i, b) for i, b in enumerate(rows_b)
            if i not in used_b and label_key(b.study_label) == label_key(a.study_label)
            and b.row_kind == a.row_kind
        ]
        if not candidates:
            continue
        scored = []
        for i, b in candidates:
            r = reconcile_pair(a, b)
            agree = sum(1 for f in r["fields"].values() if f["status"] == "CORROBORATED")
            scored.append((agree, i, r))
        agree, i, best = max(scored, key=lambda t: t[0])
        used_b.add(i)
        results.append(best)
    return results
