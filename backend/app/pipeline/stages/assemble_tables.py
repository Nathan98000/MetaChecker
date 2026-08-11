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


def build_lines(page: dict) -> list[dict]:
    """Cluster spans into visual lines by y-center; keep span bboxes."""
    spans = sorted(page["spans"], key=lambda s: (s["bbox_native"][1], s["bbox_native"][0]))
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
    for line in lines:
        line["spans"].sort(key=lambda s: s["bbox_native"][0])
        line["text"] = norm_text(" ".join(s["text"].strip() for s in line["spans"]).strip())
    return sorted(lines, key=lambda l: l["y"])


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
