# Pipeline State Machine

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 01 §5 (execution model), doc 00 (A4, A11, A12, A19–A23, O3)

---

## 1. Three levels of state

- **Job state** (infrastructure): whether work ran.
- **Stage state** (per work item): what a successful/failed run concluded (§60).
- **Workflow issue** (researcher-facing, A4/O3): a persistent, reviewable
  record that an audit step cannot currently be completed.

Job/stage records are internal (surfaced only under Advanced/Technical
Details); `workflow_issue` is what the researcher sees. Keeping all three
separate is what prevents "the API call failed" from ever being recorded as a
domain fact or counted as an audit finding (A4, §60).

## 2. Job lifecycle (A11: at-least-once, leases, idempotency)

```text
            ┌────────┐
 enqueue →  │ QUEUED │   (dedup on idempotency_key: an identical pending/
            └───┬────┘    completed job is reused, not duplicated)
                ▼
            ┌────────┐  lease expiry (crash/timeout)
            │RUNNING │ ────────────────────────────► re-claimable (attempt+1)
            └───┬────┘
      ┌─────────┼──────────┐
      ▼         ▼          ▼
 ┌─────────┐ ┌───────┐ ┌─────────┐
 │SUCCEEDED│ │FAILED │ │CANCELLED│
 └─────────┘ └───┬───┘ └─────────┘
                 ▼
        retry w/ backoff until max_attempts → FAILED_PERMANENT
                                              (opens workflow_issue)
```

- Execution is **at-least-once**; handlers are idempotent (upsert keyed by
  natural key + input hash), so re-runs after lease expiry are safe. No
  exactly-once claims (A11).
- `job.idempotency_key` is stable and content-derived, e.g.
  `parse_document:{document_hash}:{parser_version}`.
- Claiming: lease with `lease_owner`/`lease_expires_at` (SQLite-compatible;
  the same abstraction maps to `SKIP LOCKED` on PostgreSQL).
- One worker process with bounded async concurrency (doc 00 O4); fan-out
  parents aggregate child counts for progress ("37 of 52", §20).

## 3. Stage-state vocabulary (per work item, per stage)

The §60 set plus `PENDING`:

```text
PENDING · SUCCESS · PARTIAL_SUCCESS · NEEDS_REVIEW · NO_MATCH ·
DOCUMENT_UNREADABLE · UNSUPPORTED_FORMAT · INSUFFICIENT_DATA · AMBIGUOUS ·
API_FAILURE
```

Semantics guardrails:

- `PARTIAL_SUCCESS` means "this is what could and could not be extracted" and
  always carries a detail payload listing both (A12). Example: native parsing
  succeeded but GROBID enrichment was unavailable → `PARTIAL_SUCCESS`, never
  `UNSUPPORTED_FORMAT`.
- `API_FAILURE` is retryable infrastructure state; it never produces a domain
  row and surfaces to the researcher only as a `workflow_issue` if persistent.
- `NO_MATCH` is a domain conclusion from a successful run.

## 4. Workflow issues (A4, O3)

```text
workflow_issue
  issue_type   -- PRIMARY_STUDY_UNAVAILABLE | DOCUMENT_UNREADABLE |
               -- API_FAILURE | IDENTITY_UNRESOLVED | SUPPLEMENT_MISSING
  work_item_ref, stage_id, detail, first_seen, last_seen
  state        -- OPEN | RESOLVED (auto on later stage success) | DISMISSED
```

At most one OPEN issue per (work item × issue_type); resolution is automatic
when the underlying stage later succeeds; resolved issues persist in history.
Issues are counted separately from audit findings everywhere (dashboard,
report, exports) — A4.

## 5. Stage graph

```text
S01 ingest_document         document → sha, pages
S02 parse_document          document → parse_artifacts (orchestrated stack, A12)
S03 identify_analyses       meta parse → analysis rows (+ orientation fields A10)
S04 register_study_labels   parse → study_label_mentions
S05 build_study_registry    mentions → studies, memberships
S06 crosscheck_study_set    mentions × analyses → internal-consistency findings
                            (in-scope per A19: counts, table/plot/reference
                             agreement — no external-literature checks)
S07 extract_stated_rules    Methods/protocol/supplement → stated_rule rows (A20)
S08 extract_published       tables/forest/text → published_effects
                            + analysis_effect_membership (A7)
S09 resolve_bibliographic   publication → candidates/resolution (cited works only)
S10 discover_oa             publication → oa_locations
S11 acquire_primary         publication → documents
S12 parse_primary           document → parse_artifacts
S13 identify_structure      primary parse → samples, arms, sample_arm_membership,
                            measures/outcomes, timepoints (A13, A17)
S14 extract_primary_values  publication → primary_values (candidates, §31)
S15 map_arms                published labels × primary arms → arm_mapping (A6)
S16 detect_families         publications/samples → overlap claims (§25, §43)
S17 check_rule_consistency  stated_rules × observed selections →
                            POSSIBLE-level findings (A20, O2)
S18 recalculate_effects     selected values → reconstructed_effects
S19 build_correspondence    published × reconstructed → effect_correspondence
                            (incl. composite calculations for non-1:1, A23/O5)
S20 audit_study_level       comparisons via correspondences (A8 3-question)
S21 extract_method          meta parse → analysis_method
S22 reconstruct_pool        member effects → pooled results (method variants
                            tried when method UNRESOLVED, O1)
S23 audit_pool              published pool × ours → comparisons
S24 generate_findings       comparisons/claims/contradictions → audit_findings
                            (SYSTEM_FLAGGED, A24); step failures → workflow_issues
S25 run_qc_checks           whole project → QC findings/issues (§54)
S26 export                  project → audit_workbook.xlsx / csv / json / archive
```

Every stage declares input-stage dependencies and is independently rerunnable
(§61). Reruns with unchanged input hash are cache hits; changed inputs
supersede outputs via new revisions, never deletes.

## 6. Work-item granularity (resumability, §61)

| Stage | Work item |
|---|---|
| S01–S02, S11–S12 | one document |
| S03, S06–S07, S21–S23, S25–S26 | one project / one analysis |
| S04–S05, S08 | one parse artifact / table / figure |
| S09–S10, S13–S14, S16 | one publication |
| S15, S17–S20 | one effect / one correspondence / one study-analysis pair |

Stopping at publication 73 of 180 in S09 leaves 107 child jobs `QUEUED`;
resumption is the default behavior, not a feature.

## 7. Review gates and verifiability

- Stages never block on humans: they emit `NEEDS_REVIEW` states, findings
  (`SYSTEM_FLAGGED`), and issues; downstream stages consume reviewed/HIGH
  inputs and propagate input quality (doc 03) otherwise.
- S18/S20 respect A22: when the meta-analysis reports author-supplied or
  otherwise non-public data and reconstruction from public documents fails or
  differs, the outcome is `SOURCE_DATA_NOT_PUBLICLY_VERIFIABLE` ("cannot be
  independently verified from available source documents") — not a
  discrepancy finding.
- A researcher resolution (verify/correct/resolve identity) enqueues dependent
  recomputation automatically; identity changes go through
  `identity_resolution_event` (A5) and trigger re-runs of S05–S06 dependents.
