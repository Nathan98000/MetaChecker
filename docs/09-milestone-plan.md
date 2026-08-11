# Milestone Implementation Plan

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Follows §67 phase order; adds deliverables and exit criteria. Each phase ends
with automated tests + (from Phase 4) benchmark evaluation; no phase advances
on a single working example (§67).

---

## Phase 0 — Foundation
**Build:** monorepo scaffold; **SQLite (WAL) embedded database** behind
repositories + Alembic, with PostgreSQL in the dev/CI matrix (A1); full doc
02/03 core schema (data_point, value_revision with four-dimension model A2/A3,
source_locator with normalized bboxes A9, extraction_record, calculation +
input-quality summary, document, job with idempotency keys/leases A11,
stage_state, workflow_issue A4, review_event, identity_resolution_event A5);
content-addressed document store; durable at-least-once job queue + single
worker with async concurrency (O4); structured logging; §19 error framework;
interface Protocols (doc 06) with fakes; `statengine` skeleton; CI.
**Exit:** provenance invariants pass (doc 08 §2); crash/lease-expiry resume
test passes; findings-vs-issues separation enforced in schema and API stubs.

## Phase 1 — Meta-Analysis PDF Parsing
**Build:** parser orchestration layer (A12): PyMuPDF baseline (spans+bboxes,
sections, references, tables, figure regions, multi-column), optional
auto-managed GROBID enrichment, OCR fallback; `PARTIAL_SUCCESS` semantics with
could/could-not detail; minimal UI: project creation, upload, parse status,
page viewer.
**Exit:** adversarial layout fixtures pass or degrade correctly; GROBID-absent
runs report `PARTIAL_SUCCESS`, never `UNSUPPORTED_FORMAT`.

## Phase 2 — Analysis Identification + Stated Rules
**Build:** analysis detection with subgroup hierarchy (A7) and orientation
fields (A10); `analysis_effect_membership` scaffolding; **stated-rule
extraction (A20)** from Methods/supplement (protocol/prereg docs attachable);
analyses + rules review screens (edit/split/merge).
**Exit:** gold-corpus analyses and rules identified with reviewable accuracy;
edits write revisions + review events.

## Phase 3 — Included-Study Registry (in-scope per A19)
**Build:** study-label mention harvesting across references, tables, forest
plots, text, supplements; study/membership construction;
`identity_resolution_event` operations (merge/split/reassign/undo, A5) with
UI; **internal study-set consistency checks** (§24: counts, table vs plot vs
references) emitting SYSTEM_FLAGGED findings; duplicate/ambiguity flags —
never auto-merged (§25). No external-literature discovery of any kind (A19).
**Exit:** benchmark included-study identification precision/recall; seeded
internal-inconsistency fixture detected; identity operations reversible in
tests.

## Phase 4 — Published Data Extraction
**Build:** table-based effect extraction; forest-plot subsystem (§26 ladder)
with row_kind classification; published effects + memberships fully
provenanced (four dimensions recorded per value); candidate values (§31);
versioned confidence rules v1 (A3); EvidencePanel with normalized-bbox
highlighting; review queue v1 (findings + workflow items, typed A4);
record-level validation (§33); model-role router with initial assignments +
concrete-model-ID logging (A16).
**Exit — first usable internal-consistency audit:** upload → review analyses/
rules/studies/effects → see internal contradictions → inspect provenance of
every number. Benchmark extraction + false-confidence metrics tracked; first
model-role benchmark run recorded.

## Phase 5 — Bibliographic Resolution & OA (cited works only, A19)
**Build:** Crossref/OpenAlex/PubMed adapters; candidate scoring & storage;
disambiguation UI; Unpaywall/OpenAlex OA discovery; legal auto-retrieval +
manual upload + related documents (§29); caching + external-call logging;
persistent failures → workflow_issues.
**Exit:** publication-matching accuracy benchmarked; API_FAILURE vs NO_MATCH
behavior verified.
**→ Ship first major release (§68):** including `audit_workbook.xlsx` (A14)
with README carrying the A21 scope note, Analyses, Studies, Publications,
Published_Effects, Extraction_Log, Review_Log sheets (§49–50), and the
audit-coverage panel (A21) in the UI.

## Phase 6 — Primary-Study Parsing
**Build:** orchestrated parsing of primary docs; structure identification as
reviewable drafts: samples, arms, `sample_arm_membership` (A13), measures with
`higher_is_better` (A17), outcomes, timepoints; supplements.
**Exit:** structure-draft accuracy on benchmark primaries reported.

## Phase 7 — Primary Data Extraction
**Build:** targeted value extraction driven by analysis needs; candidate
selection workflow; arm mapping (A6); missing-data map (§42) incl. A22
messaging for author-supplied data.
**Exit:** benchmark primary-value accuracy; context-free numbers
unrepresentable (§30) verified by schema test.

## Phase 8 — Statistical Engine
**Build:** full formula families incl. composites for correspondences (O5) and
explicit orientation transforms (A10); pooling (fixed IV, DL random effects +
alternative estimators for O1 method-variant testing; Q/I²/tau²/prediction
interval); calculation provenance + input-quality summaries; validation
engine; R cross-validation oracle (doc 08 §3).
**Exit:** statistical suite green against all three ground-truth sources; edge
cases warn, never silently fix. *(Engine work may proceed in parallel from
Phase 0; Phase 8 is its integration point.)*

## Phase 9 — Study-Level Audit
**Build:** effect reconstruction; **effect_correspondence construction (A23)**
incl. one-to-many/many-to-one composites; A8 three-question comparison
(rounding match → computational tolerance → separate severity), all rules
versioned; `SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` handling (A22); explanation
candidates incl. deterministic explanation tests and `METHOD_VARIANT_MATCH`
(O1); study audit packet (§46).
**Exit:** benchmark reconstruction + discrepancy precision/recall +
false-finding rate; seeded-error fixtures (wrong N, sign flip, ITT/completer,
combined arms) detected with correct severity behavior (84-vs-81 → REVIEW).

## Phase 10 — Meta-Analysis Reconstruction
**Build:** method extraction; independent pooling over memberships (A7);
published-vs-reconstructed pool comparison (§37); source-of-discrepancy
substitution experiments (§38) with calculation provenance.
**Exit:** benchmark pooled quantities reproduced within computational
tolerance where methods are reported; `AMBIGUOUS_METHOD` path exercised where
they are not.

## Phase 11 — Audit Findings & Reporting
**Build:** full finding generation with A24 status flow (SYSTEM_FLAGGED →
researcher confirmation) + QC sweep (§54); rule-consistency checks surfaced
(A20); review queue final (§39); discrepancy detail (§40); audit summary
(§47) with findings/issues split (A4); audit report (§48: non-accusatory,
certainty tiers, A21 scope note, "all supported audit checks completed"
phrasing); complete workbook, CSV/JSON, reproducibility archive (§52).
**Exit:** end-to-end benchmark audit produces a report whose every claim
click-throughs to evidence; report language checks pass (no "fully verified",
scope note present).

## Phase 12 — Complex Designs
**Build:** detection + flagging of multi-arm/shared-control/crossover/cluster/
repeated-measures/overlapping-sample dependencies (flag before correct);
shared-control handling; sensitivity reconstruction (§44).
**Exit:** dependency fixtures never treated as independent silently;
sensitivity runs fully provenanced.

---

## Cross-cutting tracks
- **Packaging (A1, decided):** Tauri shell with the Python backend as a
  supervised sidecar; a basic shell ships with the foundation (Phase 0
  verification includes launching as an ordinary desktop app), maintained as
  an installable bundle from Phase 4 onward; release-gate: fresh-machine
  install with zero command-line steps.
- **Corpus building:** candidate selection precedes substantial extraction
  logic (researcher decision 2026-08-11; target 6–10, see doc 10); gold truth
  (incl. stated rules and correspondences) exists before Phase 4 exit metrics.
- **Model-role benchmarking (A16):** re-run per release; assignments are
  config, concrete model IDs recorded.
- **Cost & privacy surfaces (§58, §63):** call logging from first adapter;
  Settings surfaces by Phase 5; optional warning threshold / hard limit.
- **Docs:** each phase updates the data dictionary feeding the workbook README
  (§49–50), which always carries the A21 scope note.
