"""S04a reconcile_representations — Phase 1d cross-representation audit.

Pairs structured rows from independent extraction channels (TABLE_RECORDS ×
FOREST_PLOT_ROWS) for a document and records their relationships. Both
assertions and full provenance are preserved (agreement corroborates what the
publication reports, not underlying correctness). CONTRADICTION rows become
audit_finding records (SYSTEM_FLAGGED, POSSIBLE — never auto-confirmed, A24);
formatting differences that normalize deterministically produce no finding.
"""

from sqlalchemy import select

from app.audit.reconcile import Assertion, reconcile_rows
from app.db.models import AuditFinding, Document, Job, ParseArtifact
from app.pipeline.registry import StageContext, StageResult, stage

STAGE_ID = "reconcile_representations"
PARSER_ID = "cross_representation_reconciler"
PARSER_VERSION = "1"


def idempotency_key(sha256: str) -> str:
    return f"{STAGE_ID}:{sha256}:{PARSER_VERSION}"


def _table_assertions(artifact: ParseArtifact) -> list[Assertion]:
    out = []
    for r in artifact.payload.get("records", []):
        out.append(Assertion(
            representation="TABLE",
            study_label=r.get("study_label", ""),
            row_kind=r.get("row_kind", "STUDY_ROW"),
            values={
                "effect_value": r.get("effect_value"),
                "ci_lower": r.get("ci_lower"), "ci_upper": r.get("ci_upper"),
                "weight": r.get("weight"),
                "events_treatment": r.get("events_treatment"),
                "events_control": r.get("events_control"),
            },
            provenance={"page": r.get("page_number"), "line_bbox": r.get("line_bbox"),
                        "cell_bboxes": r.get("cell_bboxes"),
                        "method": r.get("acquisition_method")},
        ))
    return out


def _vision_assertions(artifact: ParseArtifact) -> list[Assertion]:
    out = []
    for result in artifact.payload.get("results", []):
        page = result["region"]["page_number"]
        for r in result.get("rows", []):
            out.append(Assertion(
                representation="FOREST_PLOT",
                study_label=r.get("study_label", ""),
                row_kind={"STUDY_ROW": "STUDY_ROW",
                          "OVERALL_SUMMARY": "OVERALL_TOTAL",
                          "SUBGROUP_SUMMARY": "SUBGROUP_TOTAL"}.get(
                              r.get("row_kind", ""), r.get("row_kind", "")),
                values={k: r.get(k) for k in
                        ("effect_value", "ci_lower", "ci_upper", "standard_error",
                         "weight", "n_treatment", "n_control",
                         "events_treatment", "events_control")},
                provenance={"page": page, "region_bbox": result["region"].get("bbox_norm"),
                            "method": "VISION", "model_id": result.get("model_id")},
            ))
    return out


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

    table = latest("TABLE_RECORDS")
    vision = latest("FOREST_PLOT_ROWS")
    if table is None and vision is None:
        return StageResult(state="INSUFFICIENT_DATA",
                           detail={"reason": "no structured records to reconcile"})
    if table is None or vision is None:
        return StageResult(
            state="PARTIAL_SUCCESS",
            detail={"extracted": [], "not_extracted": [
                "only one representation channel has records; reconciliation "
                "needs at least two"]},
        )

    results = reconcile_rows(_table_assertions(table), _vision_assertions(vision))
    contradictions = [r for r in results if r["overall"] == "CONTRADICTION"]

    input_hash = f"{doc_row.sha256}:{table.id}:{vision.id}:{PARSER_VERSION}"
    existing = ctx.session.scalar(
        select(ParseArtifact).where(
            ParseArtifact.document_id == doc_row.id,
            ParseArtifact.kind == "RECONCILIATION",
            ParseArtifact.input_hash == input_hash,
        )
    )
    if existing is None:
        ctx.session.add(ParseArtifact(
            project_id=doc_row.project_id, document_id=doc_row.id,
            parser_id=PARSER_ID, parser_version=PARSER_VERSION,
            kind="RECONCILIATION", payload={"pairs": results},
            input_hash=input_hash,
        ))
        for c in contradictions:
            bad_fields = [f for f, v in c["fields"].items() if v["status"] == "CONTRADICTION"]
            ctx.session.add(AuditFinding(
                project_id=doc_row.project_id,
                finding_kind="CONTRADICTION",
                taxonomy_code="INTERNAL_INCONSISTENCY",
                severity="REVIEW",
                certainty="POSSIBLE",
                title=f"{c['study_label']}: {', '.join(bad_fields)} differ between "
                      f"table and forest plot",
                description=(
                    "Two representations of the same row disagree. Neither side "
                    "has been assumed correct; both are preserved with their "
                    "source locations."),
                document_id=doc_row.id,
                evidence=c,
                detected_by=f"{STAGE_ID} v{PARSER_VERSION}",
            ))

    corroborated = sum(1 for r in results if r["overall"] == "CORROBORATED")
    return StageResult(
        state="SUCCESS",
        detail={"pairs": len(results), "corroborated": corroborated,
                "contradictions": len(contradictions),
                "extracted": ["cross-representation reconciliation"]},
    )
