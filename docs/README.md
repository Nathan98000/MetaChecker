# Foundation Design Documents

Deliverables for SRS §71 (first development task). Read in order:

| Doc | Covers (§71 item) |
|---|---|
| [00-ambiguities-and-decisions.md](00-ambiguities-and-decisions.md) | Ambiguities & contradictions (2); rationale for choices (13) |
| [01-architecture.md](01-architecture.md) | System architecture (3); ADRs (13) |
| [02-data-model.md](02-data-model.md) | Relational data model (4) |
| [03-provenance-model.md](03-provenance-model.md) | Provenance model (5) |
| [04-pipeline-state-machine.md](04-pipeline-state-machine.md) | Pipeline state machine (6) |
| [05-audit-finding-model.md](05-audit-finding-model.md) | Audit-finding data model (7) |
| [06-module-interfaces.md](06-module-interfaces.md) | Module interfaces (8) |
| [07-ui-architecture.md](07-ui-architecture.md) | Researcher UI architecture (9) |
| [08-testing-and-benchmark-strategy.md](08-testing-and-benchmark-strategy.md) | Testing strategy (10); benchmark methodology (11) |
| [09-milestone-plan.md](09-milestone-plan.md) | Milestone implementation plan (12) |
| [10-gold-corpus.md](10-gold-corpus.md) | Gold-standard benchmark corpus candidates (§55, decision of 2026-08-11) |

Status: **Researcher-reviewed 2026-08-11.** Doc 00 records the researcher's
decisions on A1–A18 plus additions A19–A24 (notably: omitted-study detection is
explicitly out of scope — the tool audits what the review included, not what
its literature search may have missed). Docs 01–09 conform to those decisions.
Open questions discovered during revision are listed at the end of doc 00
(O1–O5, provisionally resolved).

Per §71(14), broad feature implementation has not begun.
