"""S03 identify_analyses — Milestone 2: which pooled analyses does the
publication report, and which extracted rows belong to each?

Deterministic, structured-channel v1 (no AI):

- RevMan documents (Cooney): "Analysis X.Y" caption lines in the text layer
  anchor analyses; assembled TABLE_RECORDS rows are assigned to the nearest
  preceding anchor by (page, y). Pooled values come from the section's
  OVERALL_TOTAL row; heterogeneity from its statistics lines.
- Effect-column tables (Prochaska): one analysis per effect-measure column,
  pooled from that column's OVERALL_TOTAL row.
- Figure regions (vision channel): one analysis per OVERALL_SUMMARY row in a
  region (caption = description); SUBGROUP_SUMMARY rows become child analyses
  (doc 00 A7 hierarchy). STUDY rows in the region join the memberships of the
  subgroup they sit under and of the parent.

Text-borne analyses (pooled sentences with no table/figure twin — Macnamara,
Nissen) are explicitly OUT of v1 scope and reported as such; a text-channel
extractor is a later increment, not silently faked.

Output: ANALYSES parse artifact — per analysis: description, effect_measure,
model, pooled values (verbatim), heterogeneity, subgroup_of, source
provenance, member row references, channel. Researcher editing arrives with
the relational migration; this artifact is the pipeline contract.
"""

import re

from sqlalchemy import select

from app.db.models import Document, Job, ParseArtifact
from app.pipeline.registry import StageContext, StageResult, stage

PARSER_ID = "structural_analysis_identifier"
PARSER_VERSION = "1"
STAGE_ID = "identify_analyses"

REVMAN_HEADER = re.compile(r"Analysis\s+(\d+\.\d+)\.?\s*(.*)", re.IGNORECASE)

HET_PATTERNS = {
    # (?<![A-Za-z]) so "I²=" never matches inside "Chi²="
    "i2": re.compile(r"(?<![A-Za-z])I(?:²|-?squared|2)\s*[=:]\s*([\d.]+)\s*%?", re.IGNORECASE),
    "tau2": re.compile(r"Tau(?:²|2)\s*[=:]\s*([\d.]+)", re.IGNORECASE),
    "q": re.compile(r"Chi(?:²|2)\s*[=:]\s*([\d.]+)", re.IGNORECASE),
    "het_p": re.compile(r"(?:\(|,|;)\s*[Pp]\s*[=<]\s*([\d.]+)", ),
    "z": re.compile(r"Z\s*[=:]\s*([\d.]+)", ),
}

MODEL_PATTERNS = [
    (re.compile(r"random", re.IGNORECASE), "RANDOM"),
    (re.compile(r"\bfixed\b", re.IGNORECASE), "FIXED"),
]

MEASURE_IN_TEXT = [
    (re.compile(r"std\.?\s*mean\s*difference|SMD", re.IGNORECASE), "SMD"),
    (re.compile(r"mean\s*difference|\bMD\b", re.IGNORECASE), "MD"),
    (re.compile(r"peto\s+odds\s+ratio", re.IGNORECASE), "Peto OR"),
    (re.compile(r"odds\s+ratio|\bOR\b", re.IGNORECASE), "OR"),
    (re.compile(r"risk\s+ratio|relative\s+risk|\bRR\b", re.IGNORECASE), "RR"),
    (re.compile(r"risk\s+difference|\bRD\b", re.IGNORECASE), "RD"),
    (re.compile(r"hazard\s+ratio|\bHR\b", re.IGNORECASE), "HR"),
]


def _parse_het(text: str) -> dict:
    out = {}
    for key, pattern in HET_PATTERNS.items():
        m = pattern.search(text or "")
        if m:
            out[key] = m.group(1)
    return out


def _detect_model(text: str) -> str:
    for pattern, name in MODEL_PATTERNS:
        if pattern.search(text or ""):
            return name
    return "UNCLEAR"


def _detect_measure(text: str) -> str | None:
    for pattern, name in MEASURE_IN_TEXT:
        if pattern.search(text or ""):
            return name
    return None


def _revman_anchors(pages: list[dict]) -> list[dict]:
    """Find 'Analysis X.Y' caption lines: (page, y, ref, title)."""
    anchors = []
    for page in pages:
        # cluster page spans into lines cheaply: sort by y then group
        spans = sorted(page["spans"], key=lambda s: (round(s["bbox_native"][1]), s["bbox_native"][0]))
        line_map: dict[int, list] = {}
        for s in spans:
            line_map.setdefault(round(s["bbox_native"][1] / 4), []).append(s)
        for _, line_spans in sorted(line_map.items()):
            text = " ".join(s["text"].strip() for s in sorted(line_spans, key=lambda s: s["bbox_native"][0]))
            m = REVMAN_HEADER.match(text.strip())
            if m and len(m.group(2)) > 5:
                anchors.append({
                    "page": page["page_number"],
                    "y": min(s["bbox_native"][1] for s in line_spans),
                    "ref": m.group(1),
                    "title": m.group(2).strip()[:300],
                })
    return anchors


def _nearest_anchor(anchors: list[dict], page: int, y: float) -> dict | None:
    best = None
    for a in anchors:
        if (a["page"], a["y"]) <= (page, y):
            if best is None or (a["page"], a["y"]) > (best["page"], best["y"]):
                best = a
    return best


def identify(text_pages: list[dict], table_records: list[dict],
             vision_results: list[dict]) -> list[dict]:
    analyses: list[dict] = []
    counter = [0]

    def new_id() -> str:
        counter[0] += 1
        return f"AN-{counter[0]:03d}"

    # ---- channel 1: RevMan sections & effect-column tables ------------------
    anchors = _revman_anchors(text_pages)
    by_section: dict[tuple, dict] = {}
    for record in table_records:
        page, y = record["page_number"], record["line_bbox"][1]
        anchor = _nearest_anchor(anchors, page, y)
        if anchor is not None:
            key = ("revman", anchor["ref"])
            section = by_section.setdefault(key, {"anchor": anchor, "records": []})
            section["records"].append(record)
        else:
            # effect-column table: group by measure
            key = ("measure", record.get("effect_measure") or "?", page // 4)
            section = by_section.setdefault(key, {"anchor": None, "records": []})
            section["records"].append(record)

    for key, section in by_section.items():
        records = section["records"]
        study_rows = [r for r in records if r["row_kind"] == "STUDY_ROW"]
        pooled = [r for r in records if r["row_kind"] in ("OVERALL_TOTAL", "SUBGROUP_TOTAL")]
        if not pooled:
            continue
        if not study_rows:
            # subgroup-analysis table: every pooled row is its own analysis
            # (k studies pooled per row; no per-study rows printed)
            for row in pooled:
                analyses.append({
                    "analysis_id": new_id(),
                    "channel": "TABLE",
                    "description": f"Subgroup analysis: {row['study_label']}"[:300],
                    "revman_ref": None,
                    "effect_measure": row.get("effect_measure"),
                    "model": "UNCLEAR",
                    "pooled": {k: row.get(k) for k in
                               ("effect_value", "ci_lower", "ci_upper", "weight")},
                    "heterogeneity": {k: v for k, v in
                                      (("i2", row.get("i2_hint")), ("het_p", row.get("p_hint")))
                                      if v},
                    "subgroup_of": None,
                    "source": {"page": row["page_number"], "line_bbox": row.get("line_bbox")},
                    "member_count": int(row["k_studies_hint"]) if row.get("k_studies_hint") else None,
                    "members": [],
                })
            continue
        overall = next((r for r in pooled if r["row_kind"] == "OVERALL_TOTAL"), pooled[-1])
        anchor = section["anchor"]
        context = (anchor["title"] if anchor else "") + " " + " ".join(
            filter(None, (r.get("effect_measure") for r in records[:3])))
        analyses.append({
            "analysis_id": new_id(),
            "channel": "TABLE",
            "description": anchor["title"] if anchor else
                f"Pooled analysis ({overall.get('effect_measure') or 'effect'} column)",
            "revman_ref": anchor["ref"] if anchor else None,
            "effect_measure": overall.get("effect_measure") or _detect_measure(context),
            "model": _detect_model(context),
            "pooled": {k: overall.get(k) for k in
                       ("effect_value", "ci_lower", "ci_upper", "weight")},
            "heterogeneity": _parse_het(" ".join(
                r["study_label"] for r in records if r["row_kind"] == "HETEROGENEITY")),
            "subgroup_of": None,
            "source": {"page": overall["page_number"], "line_bbox": overall.get("line_bbox")},
            "member_count": len(study_rows),
            "members": [{"study_label": r["study_label"], "page": r["page_number"],
                         "effect_value": r.get("effect_value")} for r in study_rows],
        })

    # ---- channel 2: figure regions (vision) ---------------------------------
    for result in vision_results:
        rows = result.get("rows", [])
        if not rows:
            continue
        region = result["region"]
        caption = region.get("caption") or ""
        study_rows = [r for r in rows if r.get("row_kind") == "STUDY_ROW"]
        subtotals = [r for r in rows if r.get("row_kind") == "SUBGROUP_SUMMARY"]
        overalls = [r for r in rows if r.get("row_kind") == "OVERALL_SUMMARY"]
        het_text = " ".join(r.get("note") or "" for r in rows if r.get("row_kind") == "HETEROGENEITY")
        het_text += " " + " ".join((r.get("note") or "") + (r.get("study_label") or "")
                                   for r in overalls + subtotals)
        if not study_rows or not (overalls or subtotals):
            continue
        context = caption + " " + " ".join(result.get("meta", {}).get("columns_seen", []))
        measure = (study_rows[0].get("effect_measure")
                   or _detect_measure(context))

        def emit(row, kind, members, parent, panel_no):
            """One analysis from one summary row — skipped when the row
            carries no pooled value (abstention, not a detection)."""
            if not (row.get("effect_value") or "").strip() or \
                    row.get("effect_value", "").strip().upper() == "UNRESOLVED":
                return None
            aid = new_id()
            label = row.get("subgroup") or row.get("study_label") or ""
            desc = caption[:200] or "Forest-plot analysis"
            if kind == "SUBGROUP_SUMMARY":
                desc = f"{desc} — subgroup: {label}"
            elif panel_no > 1:
                desc = f"{desc} — panel {panel_no}"
            analyses.append({
                "analysis_id": aid,
                "channel": "FOREST_PLOT",
                "description": desc[:300],
                "revman_ref": None,
                "effect_measure": measure,
                "model": _detect_model(context + " " + het_text),
                "pooled": {k: row.get(k) for k in
                           ("effect_value", "ci_lower", "ci_upper", "weight")},
                "heterogeneity": _parse_het((row.get("note") or "") + " " +
                                            (row.get("study_label") or "")),
                "subgroup_of": parent,
                "source": {"page": region["page_number"], "region_bbox": region.get("bbox_norm")},
                "member_count": len(members),
                "members": [{"study_label": r.get("study_label"), "page": region["page_number"],
                             "effect_value": r.get("effect_value")} for r in members],
            })
            return aid

        # Sequential walk: a region may hold several stacked panels (Yang's
        # Fig 5 = TTR + PFS + CSS/DFS/RFS). Studies accumulate; a
        # SUBGROUP_SUMMARY pools the studies since the last summary; an
        # OVERALL_SUMMARY closes a panel, becoming parent of that panel's
        # subgroup analyses.
        panel_no = 0
        pending_studies: list[dict] = []
        panel_studies: list[dict] = []
        pending_subgroup_ids: list[str] = []
        for row in rows:
            kind = row.get("row_kind")
            if kind == "STUDY_ROW":
                pending_studies.append(row)
                panel_studies.append(row)
            elif kind == "SUBGROUP_SUMMARY":
                sid = emit(row, kind, list(pending_studies), None, panel_no + 1)
                if sid:
                    pending_subgroup_ids.append(sid)
                pending_studies = []
            elif kind == "OVERALL_SUMMARY":
                panel_no += 1
                pid = emit(row, kind, list(panel_studies), None, panel_no)
                if pid:
                    for sid in pending_subgroup_ids:
                        for a in analyses:
                            if a["analysis_id"] == sid:
                                a["subgroup_of"] = pid
                pending_subgroup_ids = []
                pending_studies = []
                panel_studies = []
        # trailing subgroup summaries with no closing overall (cropped panels)
        # stay as parentless subgroup analyses — already emitted above
    return analyses


@stage(STAGE_ID)
def run(ctx: StageContext, job: Job) -> StageResult:
    doc_row = ctx.session.get(Document, job.work_item_ref)
    if doc_row is None:
        return StageResult(state="INSUFFICIENT_DATA", detail={"reason": "document missing"})

    def latest(kind: str) -> ParseArtifact | None:
        return ctx.session.scalar(
            select(ParseArtifact)
            .where(ParseArtifact.document_id == doc_row.id, ParseArtifact.kind == kind)
            .order_by(ParseArtifact.created_at.desc())
        )

    text = latest("TEXT_SPANS")
    if text is None:
        return StageResult(state="INSUFFICIENT_DATA", detail={"reason": "no TEXT_SPANS"})
    table = latest("TABLE_RECORDS")
    vision = latest("FOREST_PLOT_ROWS")

    analyses = identify(
        text.payload["pages"],
        table.payload.get("records", []) if table else [],
        vision.payload.get("results", []) if vision else [],
    )

    input_hash = f"{doc_row.sha256}:{table.id if table else '-'}:{vision.id if vision else '-'}:{PARSER_VERSION}"
    existing = ctx.session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.kind == "ANALYSES",
            ParseArtifact.input_hash == input_hash,
        )
    )
    if existing is None:
        ctx.session.add(ParseArtifact(
            project_id=doc_row.project_id, document_id=doc_row.id,
            parser_id=PARSER_ID, parser_version=PARSER_VERSION,
            kind="ANALYSES", payload={"analyses": analyses},
            input_hash=input_hash,
        ))
    if not analyses:
        return StageResult(
            state="PARTIAL_SUCCESS",
            detail={"analyses": 0,
                    "extracted": [],
                    "not_extracted": ["no structured pooled rows found; "
                                      "text-borne analyses need the text channel (v2)"]},
        )
    return StageResult(
        state="SUCCESS",
        detail={"analyses": len(analyses),
                "with_subgroups": sum(1 for a in analyses if a["subgroup_of"]),
                "extracted": ["analysis structures with memberships"]},
    )


def idempotency_key(sha256: str) -> str:
    return f"{STAGE_ID}:{sha256}:{PARSER_VERSION}"
