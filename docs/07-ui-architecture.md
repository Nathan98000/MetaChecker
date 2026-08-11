# Researcher-Facing UI Architecture

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 00 (A3, A4, A21, A24, UI requirement), doc 05

Next.js + TypeScript inside the packaged app shell (doc 01 §1b). Data via
TanStack Query against the local API; live progress via SSE; PDF.js with a
highlight overlay driven by normalized bboxes (A9). No command line for any
workflow (§13, A1).

**Vocabulary rule (doc 00):** the primary UI speaks researcher language only —
Studies, Analyses, Primary Papers, Published Data, Source Data, Calculations,
Discrepancies, Needs Review, Audit Results. Database terms, job queues, parser
names, UUIDs, API payloads, raw model responses, and infrastructure never
appear outside Advanced / Technical Details / Provenance / Developer
Information panels. Progressive disclosure everywhere:
*simple summary → source evidence → technical provenance*.

---

## 1. Navigation structure

```text
/                         Project list, "New audit"
/project/:id              Dashboard (§15): counters (view-backed, §47) with
                          audit findings and workflow items SEPARATE (A4);
                          Audit-coverage panel + scope note (A21);
                          Continue Audit / Review Issues / Results / Export
/project/:id/workflow     10-step tracker (§14)
/project/:id/analyses     Detected analyses (incl. subgroup hierarchy A7),
                          edit/split/merge
/project/:id/rules        Stated rules of the review (A20): eligibility &
                          selection rules with their sources
/project/:id/studies      Study registry + internal consistency (§24);
                          identity operations (merge/split/reassign/undo, A5)
/project/:id/study/:sid   Study Audit Packet (§46)
/project/:id/effects      Published data grid, per-analysis (memberships A7)
/project/:id/papers       Primary Papers: resolution, retrieval status,
                          uploads, related documents (§29)
/project/:id/review       Review queue (§39): findings and workflow items in
                          one list, visibly typed (A4)
/project/:id/finding/:fid Discrepancy detail (§40)
/project/:id/results      Published vs reconstructed (§37) + diagnosis (§38)
/project/:id/export       Exports (audit_workbook.xlsx, CSV, JSON, archive)
/project/:id/settings     Thresholds/severity rules (A8), model & cost
                          settings (A16), privacy log (§58) — "Advanced" home
```

## 2. Audit coverage panel (A21)

On the dashboard and in every report/export summary:

```text
Audit coverage
✓ Internal consistency          ✓ Included-study eligibility
✓ Published data extraction     ◐ Primary-study data selection (43 of 49)
✓ Effect-size calculations      ○ Pooled calculations — not yet run

Scope note: This tool audits the studies included in the published
meta-analysis. It does not assess whether additional eligible studies were
omitted from the review.
```

Search completeness is the scope note — explanatory text, never a task row.
Completion language is always "All supported audit checks completed", never
"fully verified" (A21).

## 3. Core shared components

- **EvidencePanel** (§17): left, PDF page with bbox highlight; right, the
  value card (value · plain-language status · confidence). Actions:
  `Verify · Correct · Mark uncertain · Exclude · Add note` (A3 review states).
- **ProvenancePopover**: progressive disclosure of the doc 03 chain. Level 1:
  "Reported in Table 2, page 6 — read automatically, checked by you."
  Level 2: source snippet + highlight link. Level 3 (Technical details):
  revisions, acquisition method, rules/versions, model ID.
- **InputQualityBadge** (A2/A3): for calculated values — "computed entirely
  from verified source values" vs "uses 1 inferred SD", backed by the
  input-quality summary with drill-down to the lineage.
- **StatusBadge** (§16): `✓ Verified · ● Needs review · ! Discrepancy found ·
  ○ Not yet processed · ? Unable to determine` — icon + text, color as
  reinforcement only. Internal vocabularies stay behind "advanced details".
- **FindingCard** (A4/A24): kind-typed; shows `System flagged` vs
  `Confirmed by you` vs `Explained` states explicitly; candidate explanations
  listed as suggestions with their evidence, confirm/dismiss controls.
- **WorkflowItemCard** (A4): "This step couldn't be completed" framing with
  §19 error structure (what happened / what it means / what you can do:
  retry, upload manually, continue without) — visually distinct from findings.
- **ProgressStream** (§20): "37 of 52 complete"; completed items browsable
  before the stage finishes.
- **TermTooltip** (§18): plain-language stats glossary, expandable.
- **CandidatePicker** (§31, M5): side-by-side candidates with evidence;
  choosing writes a revision + review event; rivals preserved.
- **MissingDataMap** (§42): present/absent inputs + suggested next steps;
  includes the A22 state ("this value can't be checked against public
  documents — the review reports data obtained from the authors").
- **IdentityHistory** (A5): human-readable log of merge/split/reassign/undo
  events with one-click undo.

## 4. Interaction rules

- Every researcher mutation goes through the review-event API → append-only
  revisions; undo = restore prior revision (§21), surfaced per-value and
  globally.
- Findings follow A24: the UI never labels anything a confirmed error on the
  system's own authority; confirm/dismiss/explain are researcher actions.
- Review-required items are loud (§12): nav badge, highlighted rows,
  dashboard counter (split by findings vs workflow items).
- Virtualized grids with §39 filters; keyboard-first review flow
  (verify/next).
- No value is ever displayed without its status; unverified and low-confidence
  values are never styled identically to verified ones (§54).

## 5. API surface (shape)

REST resources mirror the data model (`/analyses`, `/studies`, `/effects`,
`/findings`, `/workflow-issues`, `/rules`, `/correspondences`,
`/datapoints/:id/provenance`, `/review-events`, `/identity-events`), plus
`POST /projects/:id/stages/:stage/run`, `GET /projects/:id/progress` (SSE),
`GET /projects/:id/summary`, `GET /projects/:id/coverage` (A21),
`POST /export/:format`. OpenAPI-generated types consumed by the frontend.
