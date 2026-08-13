"""S03a assemble_table_records — Phase 1c deterministic table/RevMan assembly.

Converts TEXT_SPANS into structured scientific records using geometry and
rule-based parsing ONLY (no AI): the baseline shows text-encoded tables carry
~100% of their values natively; the missing capability is association.

Supported line shapes (v1):
- RevMan forest-table rows:   "<label> ... n mean(sd) n mean(sd) w% e [lo , hi]"
  → effect+CI from the trailing bracket group, weight from the % token,
    row_kind from label prefixes (Total/Subtotal/Heterogeneity/Test for).
- Effect-column tables:       "<label> ... a/b c/d  x (y to z)  x (y to z) ..."
  → one record per "value (lo to hi)" group; effect_measure attributed by the
    x-range of header spans when a header line is found ("Peto odds ratio",
    "Risk difference (95% CI)", ...).

Provenance: every captured cell keeps the bbox of the span(s) it came from —
cell-level, not just row-level. acquisition_method = LAYOUT_EXTRACTION.
Anything the rules cannot parse is left unparsed (no guessing); AI
interpretation of genuinely ambiguous tables is a later, separate stage.
"""

import re

from sqlalchemy import select

from app.db.models import Document, Job, ParseArtifact
from app.pipeline.registry import StageContext, StageResult, stage

PARSER_ID = "layout_table_assembler"
PARSER_VERSION = "1"
STAGE_ID = "assemble_table_records"

DASHES = dict.fromkeys(map(ord, "−–—‐‑"), "-")

NUM = r"-?\d+(?:\.\d+)?"
BRACKET_CI = re.compile(rf"({NUM})\s*\[\s*({NUM})\s*,\s*({NUM})\s*\]")
PAREN_CI = re.compile(rf"({NUM})\s*\(\s*({NUM})\s+to\s+({NUM})\s*\)")
UC_CELL = re.compile(r"\bUC\b")
WEIGHT = re.compile(rf"({NUM})\s*%")
EVENTS = re.compile(r"\b(\d+)/(\d+)\b")
MEAN_SD = re.compile(rf"({NUM})\s*\(\s*({NUM})\s*\)")

TOTAL_PREFIXES = ("total", "subtotal", "all trials combined", "overall")
META_PREFIXES = ("heterogeneity", "test for overall effect", "test for subgroup")

MEASURE_HEADERS = [
    ("peto odds ratio", "Peto OR"),
    ("odds ratio", "OR"),
    ("relative risk", "RR"),
    ("risk ratio", "RR"),
    ("risk difference", "RD"),
    ("std. mean difference", "SMD"),
    ("standardised mean difference", "SMD"),
    ("mean difference", "MD"),
    ("hazard ratio", "HR"),
]


def norm_text(text: str) -> str:
    return text.translate(DASHES)


def _split_columns(spans: list[dict], page_width: float) -> list[list[dict]]:
    """Detect a two-column layout via a span-crossing test: split at the
    boundary that almost no span straddles (robust to narrow gutters, unlike
    midpoint histograms). Multi-column merging glued prose onto table cells
    (Yang Table 2, 2026-08-13)."""
    if len(spans) < 20:
        return [spans]
    best_boundary, best_crossers = None, len(spans)
    x = 0.30 * page_width
    while x <= 0.70 * page_width:
        crossers = sum(1 for s in spans
                       if s["bbox_native"][0] < x - 2 and s["bbox_native"][2] > x + 2)
        if crossers < best_crossers:
            best_crossers, best_boundary = crossers, x
        x += 5.0
    if best_boundary is None or best_crossers > max(2, 0.02 * len(spans)):
        return [spans]
    left = [s for s in spans
            if (s["bbox_native"][0] + s["bbox_native"][2]) / 2 < best_boundary]
    right = [s for s in spans
             if (s["bbox_native"][0] + s["bbox_native"][2]) / 2 >= best_boundary]
    if min(len(left), len(right)) < len(spans) * 0.15:
        return [spans]
    # Splitting is only meaningful when at least one side is genuine prose
    # flow (a body-text column). Pure-table pages (RevMan forests, effect
    # tables) present a low-crossing internal gutter too — splitting them
    # severs label cells from value cells (Cooney regression, 2026-08-13).
    def prose_lines(side_spans):
        count = 0
        for line in _build_column_lines(side_spans):
            words = [w for w in line["text"].split() if re.fullmatch(r"[A-Za-z][A-Za-z'\-]{2,}", w)]
            if len(words) >= 6:
                count += 1
        return count
    if max(prose_lines(left), prose_lines(right)) < 5:
        return [spans]
    return [left, right]


DATA_LINE = None  # set below (depends on regexes defined later in module)


def _is_data_line(text: str) -> bool:
    return bool(BRACKET_CI.search(text) or PAREN_CI.search(text)
                or PAREN_DASH_CI.search(text) or RANGE_ROW.search(text)
                or STUDY_HEADER.search(text) or SUMMARY_HEADER.search(text))


def _has_own_label(text: str) -> bool:
    """Line starts with an alphabetic label token (a self-contained row)."""
    first = text.strip().split(" ", 1)[0]
    return bool(re.match(r"[A-Za-z≤≥<>≤≥]", first)) and len(first) >= 2


def build_lines(page: dict) -> list[dict]:
    """Cluster spans into visual lines — column-aware, but PER LINE.

    A page can be two-column prose AND contain full-width tables (Cooney
    p106: footnotes beside RevMan rows). Global split severs table rows
    (label left, values right); global no-split glues prose onto table cells
    (Yang p4). Resolution: build both versions; for each y-band where the
    unsplit line carries a data pattern, keep the split lines only if a
    single side holds a complete row (own label + pattern); otherwise keep
    the unsplit line whole."""
    width = page.get("width") or max(
        (s["bbox_native"][2] for s in page["spans"]), default=595)
    columns = _split_columns(page["spans"], width)
    unsplit = _build_column_lines(page["spans"])
    if len(columns) == 1:
        return unsplit

    split_lines = []
    for column_spans in columns:
        split_lines.extend(_build_column_lines(column_spans))
    split_lines.sort(key=lambda l: (l["y"], l["spans"][0]["bbox_native"][0]))

    chosen: list[dict] = []
    consumed_split: set[int] = set()
    for line in unsplit:
        overlapping = [i for i, sl in enumerate(split_lines)
                       if abs(sl["y"] - line["y"]) <= 3.0]
        if _is_data_line(line["text"]):
            complete_sides = [i for i in overlapping
                              if _is_data_line(split_lines[i]["text"])
                              and _has_own_label(split_lines[i]["text"])]
            if complete_sides:
                for i in overlapping:
                    if i not in consumed_split:
                        consumed_split.add(i)
                        chosen.append(split_lines[i])
            else:
                chosen.append(line)
                consumed_split.update(overlapping)
        else:
            for i in overlapping:
                if i not in consumed_split:
                    consumed_split.add(i)
                    chosen.append(split_lines[i])
    return sorted(chosen, key=lambda l: (l["y"], l["spans"][0]["bbox_native"][0]))


def _build_column_lines(spans: list[dict]) -> list[dict]:
    spans = sorted(spans, key=lambda s: (s["bbox_native"][1], s["bbox_native"][0]))
    lines: list[dict] = []
    for span in spans:
        y_mid = (span["bbox_native"][1] + span["bbox_native"][3]) / 2
        placed = None
        for line in lines:
            if abs(line["y"] - y_mid) <= 3.0:
                placed = line
                break
        if placed is None:
            lines.append({"y": y_mid, "spans": [span]})
        else:
            placed["spans"].append(span)
    lines.sort(key=lambda l: l["y"])
    # merge orphan wrapped-cell fragments upward: a short, purely numeric-ish
    # line whose spans sit horizontally inside the previous line's extent and
    # vertically adjacent belongs to that line ("1.12" / "-1.40" split cells)
    merged: list[dict] = []
    for line in lines:
        if merged:
            prev = merged[-1]
            gap = line["y"] - prev["y"]
            prev_x0 = min(s["bbox_native"][0] for s in prev["spans"])
            prev_x1 = max(s["bbox_native"][2] for s in prev["spans"])
            is_fragment = (
                len(line["spans"]) <= 2
                and 0 < gap <= 10.0
                and all(NUMERICISH_SPAN.match(norm_text(s["text"].strip()))
                        for s in line["spans"])
                and all(s["bbox_native"][0] >= prev_x0 - 2 and s["bbox_native"][2] <= prev_x1 + 2
                        for s in line["spans"])
                and len(prev["spans"]) >= 2
            )
            if is_fragment:
                prev["spans"].extend(line["spans"])
                continue
        merged.append(line)
    for line in merged:
        line["spans"].sort(key=lambda s: s["bbox_native"][0])
        line["text"] = norm_text(" ".join(s["text"].strip() for s in line["spans"]).strip())
    return merged


def _bbox_union(bboxes: list[list[float]]) -> list[float]:
    return [
        min(b[0] for b in bboxes), min(b[1] for b in bboxes),
        max(b[2] for b in bboxes), max(b[3] for b in bboxes),
    ]


def _find_token_bbox(line: dict, token: str) -> list[float] | None:
    """bbox of the span(s) whose text contains the token (cell provenance)."""
    token = token.strip()
    hits = [s["bbox_native"] for s in line["spans"] if token in norm_text(s["text"])]
    if hits:
        return hits[0]
    # token may be split across spans; fall back to the line's numeric area
    return None


def classify_label(label: str) -> str:
    low = label.strip().lower()
    if any(low.startswith(p) for p in META_PREFIXES):
        return "HETEROGENEITY"
    if any(low.startswith(p) for p in TOTAL_PREFIXES):
        return "OVERALL_TOTAL" if not low.startswith("subtotal") else "SUBGROUP_TOTAL"
    return "STUDY_ROW"


STUDY_HEADER = re.compile(r"study\s+or\s+sub\s*group|^\s*study\b.*event", re.IGNORECASE)
# subgroup-analysis tables: a header naming an effect measure plus a CI column
# (e.g. Yang Table 2: "Variables No. of studies HR 95%CI I2(%) Ph"), or a bare
# measure-word column header on its own short line (Nissen: "Odds Ratio")
SUBGROUP_HEADER = re.compile(
    r"\b(HR|OR|RR|RD|SMD|MD)\b.{0,40}95\s*%?\s*CI", re.IGNORECASE)
BARE_MEASURE_HEADER = re.compile(
    r"^\s*(peto\s+odds\s+ratio|odds\s+ratio|hazard\s+ratio|risk\s+ratio|"
    r"relative\s+risk|risk\s+difference)\s*(\(95%\s*CI\))?\s*$", re.IGNORECASE)
# paren-dash CI: "1.43 (1.03-1.98)" (Nissen tables); the interior dash
# distinguishes it from single-value parens like "(0.57)" event percentages
PAREN_DASH_CI = re.compile(
    rf"({NUM})\s*\(\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*\)")
# dash-range CI following an effect value: "2.11 1.59-2.38" (subgroup tables);
# both bounds non-negative to avoid eating subtractions/negative effects
RANGE_ROW = re.compile(rf"({NUM})\s+(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)(?!\d*%)")
SUMMARY_HEADER = re.compile(r"outcome\s+or\s+sub\s*group", re.IGNORECASE)
NUMERICISH_SPAN = re.compile(
    rf"^[\s\d\.\(\)\[\],%:/\-]+$|^{NUM}$|^\d+/\d+$"
)
CELL_TOKEN = re.compile(rf"\bUC\b|({NUM})\s*\(\s*({NUM})\s+to\s+({NUM})\s*\)")


def header_measures(line_text: str) -> list[str]:
    """Ordered effect-measure columns named in a header line (longest match
    first at each position, so 'Peto odds ratio' never double-counts 'odds
    ratio')."""
    low = norm_text(line_text).lower()
    found: list[tuple[int, str]] = []
    consumed: list[tuple[int, int]] = []
    for needle, measure in MEASURE_HEADERS:  # ordered longest/most-specific first
        start = 0
        while True:
            i = low.find(needle, start)
            if i < 0:
                break
            if not any(a <= i < b for a, b in consumed):
                found.append((i, measure))
                consumed.append((i, i + len(needle)))
            start = i + len(needle)
    return [m for _, m in sorted(found)]


def span_label(line: dict) -> str:
    """Label = leading spans up to the first data-like span; trailing 1-3
    digit superscript reference numbers stripped (years kept)."""
    parts: list[str] = []
    for span in line["spans"]:
        text = span["text"].strip()
        if parts and NUMERICISH_SPAN.match(norm_text(text)):
            break
        if not parts and NUMERICISH_SPAN.match(norm_text(text)) and len(text) <= 4:
            # leading orphan number (e.g. summary-table index) — treat as label part
            parts.append(text)
            continue
        parts.append(text)
    label = " ".join(parts).strip()
    # strip trailing superscript refs (1-3 digits); keep 4-digit years
    label = re.sub(r"\s+\d{1,3}$", "", label)
    # if the label still carries trailing data columns (merged span), cut at
    # the first number that is not a plausible year
    tokens = label.split()
    for i, token in enumerate(tokens[1:], start=1):
        if re.fullmatch(r"\d+(?:\.\d+)?", token) and not re.fullmatch(r"(19|20)\d{2}[a-z]?", token):
            tokens = tokens[:i]
            break
    return " ".join(tokens).strip()


def parse_page(page: dict) -> list[dict]:
    lines = build_lines(page)
    records: list[dict] = []
    context = None            # None | "STUDY_TABLE" | "SUMMARY_TABLE"
    context_measures: list[str] = []

    for line in lines:
        text = line["text"]
        if SUMMARY_HEADER.search(text):
            context = "SUMMARY_TABLE"
            context_measures = []
            continue
        if STUDY_HEADER.search(text):
            context = "STUDY_TABLE"
            context_measures = header_measures(text)
            continue
        if SUBGROUP_HEADER.search(text) and not BRACKET_CI.search(text) \
                and not PAREN_CI.search(text) and len(text) < 120:
            context = "SUBGROUP_TABLE"
            m = SUBGROUP_HEADER.search(text)
            context_measures = [m.group(1).upper()]
            continue
        bare = BARE_MEASURE_HEADER.match(text)
        if bare and context != "STUDY_TABLE":
            # bare measure-word column header (Nissen) — but inside an active
            # RevMan study table the same words are just column subheaders and
            # must not hijack the context (Cooney 1.3 regression, 2026-08-13)
            context = "SUBGROUP_TABLE"
            context_measures = [header_measures(text)[0]] if header_measures(text) else []
            continue
        if context == "SUBGROUP_TABLE":
            m = RANGE_ROW.search(text) or PAREN_DASH_CI.search(text)
            if m and len(text) >= 8:
                label = span_label(line)
                if label and not re.fullmatch(r"[\d\W]+", label):
                    # column hints: k = integer right before the effect;
                    # i2/p = first numbers after the CI range
                    pre = text[:m.start()].strip().split()
                    k_hint = pre[-1] if pre and re.fullmatch(r"\d{1,3}", pre[-1]) else None
                    post = re.findall(rf"{NUM}|<\s*0?\.\d+", text[m.end():])
                    kind = classify_label(label)
                    if kind == "STUDY_ROW":
                        # rows in subgroup/summary-OR tables are pooled (or
                        # per-trial aggregate) estimates, never study rows
                        kind = "SUBGROUP_TOTAL"
                    records.append({
                        "k_studies_hint": k_hint,
                        "i2_hint": post[0] if post else None,
                        "p_hint": post[1] if len(post) > 1 else None,
                        "study_label": label,
                        "row_kind": kind,
                        "effect_measure": context_measures[0] if context_measures else None,
                        "effect_value": m.group(1),
                        "ci_lower": m.group(2), "ci_upper": m.group(3),
                        "weight": None, "events_treatment": None, "events_control": None,
                        "page_number": page["page_number"],
                        "line_bbox": _bbox_union([s["bbox_native"] for s in line["spans"]]),
                        "cell_bboxes": {
                            "label": line["spans"][0]["bbox_native"] if line["spans"] else None,
                            "effect": _find_token_bbox(line, m.group(1)),
                        },
                        "acquisition_method": "LAYOUT_EXTRACTION",
                    })
                continue
            if len(text) > 150 or (not RANGE_ROW.search(text) and len(text.split()) > 20):
                context = None  # left the table (prose resumed)
                continue
        measures_here = header_measures(text)
        if len(measures_here) >= 2 and not BRACKET_CI.search(text) and not PAREN_CI.search(text):
            # secondary header row naming the effect columns (e.g. Prochaska)
            context_measures = measures_here
            if context is None:
                context = "STUDY_TABLE"
            continue
        if context != "STUDY_TABLE" or len(text) < 8:
            continue

        brackets = list(BRACKET_CI.finditer(text))
        cells = [m for m in CELL_TOKEN.finditer(text)] if not brackets else []
        if not brackets and not cells:
            continue

        label = span_label(line)
        if not label or re.fullmatch(r"[\d\W]+", label):
            continue
        row_kind = classify_label(label)
        data_start = min((m.start() for m in (brackets or cells)), default=len(text))
        weights = WEIGHT.findall(text)
        events = EVENTS.findall(text[:data_start])

        def base_record():
            return {
                "study_label": label,
                "row_kind": row_kind,
                "effect_measure": None,
                "effect_value": None, "ci_lower": None, "ci_upper": None,
                "weight": weights[0] if weights else None,
                "events_treatment": f"{events[0][0]}/{events[0][1]}" if events else None,
                "events_control": f"{events[1][0]}/{events[1][1]}" if len(events) > 1 else None,
                "page_number": page["page_number"],
                "line_bbox": _bbox_union([s["bbox_native"] for s in line["spans"]]),
                "cell_bboxes": {
                    "label": line["spans"][0]["bbox_native"] if line["spans"] else None,
                },
                "acquisition_method": "LAYOUT_EXTRACTION",
            }

        if brackets:
            # RevMan shape: single effect column "e[lo,hi]"
            for m in brackets:
                record = base_record()
                record.update(effect_value=m.group(1), ci_lower=m.group(2), ci_upper=m.group(3))
                record["effect_measure"] = context_measures[0] if len(context_measures) == 1 else (
                    context_measures[-1] if context_measures else None)
                record["cell_bboxes"]["effect"] = _find_token_bbox(line, m.group(0)) or \
                    _find_token_bbox(line, m.group(1))
                records.append(record)
        else:
            # effect-column shape: ordered cells of UC | "v (lo to hi)",
            # aligned positionally with the header's measure list
            for idx, m in enumerate(cells):
                record = base_record()
                measure = context_measures[idx] if idx < len(context_measures) and \
                    len(cells) == len(context_measures) else None
                record["effect_measure"] = measure
                if m.group(0).strip() == "UC" or m.group(1) is None:
                    record["effect_value"] = "UC"
                else:
                    record.update(effect_value=m.group(1), ci_lower=m.group(2), ci_upper=m.group(3))
                    record["cell_bboxes"]["effect"] = _find_token_bbox(line, m.group(1))
                records.append(record)
    return records


@stage(STAGE_ID)
def run(ctx: StageContext, job: Job) -> StageResult:
    doc_row = ctx.session.get(Document, job.work_item_ref)
    if doc_row is None:
        return StageResult(state="INSUFFICIENT_DATA", detail={"reason": "document missing"})
    text_artifact = ctx.session.scalar(
        select(ParseArtifact)
        .where(ParseArtifact.document_id == doc_row.id, ParseArtifact.kind == "TEXT_SPANS")
        .order_by(ParseArtifact.created_at.desc())
    )
    if text_artifact is None:
        return StageResult(state="INSUFFICIENT_DATA", detail={"reason": "no TEXT_SPANS artifact"})

    all_records = []
    for page in text_artifact.payload["pages"]:
        all_records.extend(parse_page(page))

    input_hash = f"{doc_row.sha256}:{PARSER_VERSION}"
    existing = ctx.session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.parser_id == PARSER_ID,
            ParseArtifact.parser_version == PARSER_VERSION,
            ParseArtifact.kind == "TABLE_RECORDS",
            ParseArtifact.input_hash == input_hash,
        )
    )
    if existing is None:
        ctx.session.add(
            ParseArtifact(
                project_id=doc_row.project_id, document_id=doc_row.id,
                parser_id=PARSER_ID, parser_version=PARSER_VERSION,
                kind="TABLE_RECORDS", payload={"records": all_records},
                input_hash=input_hash,
            )
        )
    study_rows = sum(1 for r in all_records if r["row_kind"] == "STUDY_ROW")
    return StageResult(
        state="SUCCESS",
        detail={"records": len(all_records), "study_rows": study_rows,
                "extracted": ["layout-assembled table records"]},
    )


def idempotency_key(sha256: str) -> str:
    return f"{STAGE_ID}:{sha256}:{PARSER_ID}:{PARSER_VERSION}"
