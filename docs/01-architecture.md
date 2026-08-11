# System Architecture

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: [00-ambiguities-and-decisions.md](00-ambiguities-and-decisions.md)

---

## 1. Shape of the system

Local-first, single-researcher application (A1). The end-user experience is an
installed desktop application — *install → open → upload meta-analysis → begin
audit* — with no command line, no Docker, no database administration, and no
Java. Internally:

```text
┌─────────────────────────────────────────────────────────────┐
│  Researcher UI (Next.js frontend in an app shell/browser)   │
│  dashboard · evidence viewer · review queue · audit results │
└───────────────▲─────────────────────────────────────────────┘
                │ HTTP / SSE (loopback only)
┌───────────────┴─────────────────────────────────────────────┐
│  API server — FastAPI (Python)                              │
│  · REST resources over the data model                       │
│  · SSE progress streams (§20)                               │
│  · enqueues pipeline jobs, never runs them inline           │
└───────┬────────────────────────────────┬────────────────────┘
        │                                │
┌───────▼────────────┐          ┌────────▼────────────────────┐
│  Embedded database │          │  Worker (single process,    │
│  SQLite (WAL)      │◄────────►│  bounded async concurrency) │
│  · data model      │          │  · consumes job table       │
│  · provenance      │          │  · runs pipeline stages     │
│  · job queue       │          │  · writes results + states  │
│  · caches          │          └────────┬────────────────────┘
└────────────────────┘                   │ adapter calls only
┌────────────────────┐          ┌────────▼────────────────────┐
│  Document store    │          │  External adapters          │
│  (content-addressed│          │  Crossref · OpenAlex ·      │
│   files on disk)   │          │  Unpaywall · PubMed · LLM · │
└────────────────────┘          │  GROBID (optional, local)   │
                                └─────────────────────────────┘
```

### 1a. Database strategy (A1)

- **SQLite embedded** for the first local release: zero user administration,
  single project file directory, trivially backed up/deleted (§58).
- Kept portable to PostgreSQL: Alembic migrations, repository/data-access
  layer (no raw-SQL leakage into domain code), UUIDv7 ids, `project_id` on
  every table, no SQLite-only SQL in repositories.
- PostgreSQL remains a supported dev/CI target (the test matrix runs both) so
  the hosted path stays proven. SQLite is reconsidered only on *measured*
  database limitations (write contention, transaction latency, DB-bound
  throughput, reliability, or a hosted architecture) — CPU-heavy parallel
  parsing/OCR is not by itself a trigger; that work runs outside DB
  transactions (doc 00 O4, revised).

### 1b. Packaging (A1)

- Development: `docker compose` / local venv — developers only.
- Shipped app: **Tauri desktop shell (decided)** — the shell supervises the
  bundled Python API+worker as a sidecar process and hosts the UI; install →
  open → upload → audit, with no server-starting, Terminal, Docker, or
  localhost navigation by the user. Python runtime, parsers, and OCR are
  bundled or auto-provisioned; GROBID is an optional enhancement the app can
  download/manage itself, never a prerequisite (A12). The UI talks to the
  backend only through the HTTP API contract, so a hosted deployment stays
  possible later.
- The UI never surfaces infrastructure vocabulary (doc 00 UI requirement).

## 2. Repository layout (monorepo)

```text
backend/
  app/
    api/              # FastAPI routers (thin; no business logic)
    core/             # config, logging, errors, model-role config (A16)
    db/               # SQLAlchemy models, Alembic migrations, repositories
    domain/           # entities + services (pure Python, no FastAPI imports)
    pipeline/         # stages, state machine, job runner
    parsing/          # parser ORCHESTRATION layer (A12) over adapters
    adapters/
      llm/            # LLMProvider impls + model-role router (A16)
      bibliographic/  # CrossrefProvider, OpenAlexProvider, PubMedProvider
      openaccess/     # UnpaywallProvider, OpenAlexOAProvider
      parsers/        # PyMuPdfParser, GrobidParser, OcrParser
    provenance/       # locators, revisions, four-dimension status model (A2/A3)
    audit/            # comparison (3-question model, A8), findings (A4, A24)
    export/           # audit_workbook.xlsx (A14), csv, json, archive
  statengine/         # SEPARATE package: deterministic statistics.
                      # Zero dependencies on app/, no AI imports, no I/O.
  tests/
    unit/  integration/  statistical/  adversarial/  benchmark/
frontend/
corpus/
  gold/  adversarial/
docs/
docker-compose.yml    # DEV ONLY (postgres variant, grobid)
```

## 3. Non-negotiable architectural rules

1. **Scope boundary** (A19): no component searches external literature or
   assesses search completeness. There is no code path for discovering
   studies outside the published review's study set; bibliographic adapters
   resolve *cited* works only.
2. **AI proposes, code computes** (§5). Model output is written as candidate
   extraction records with `scientific_basis`/`acquisition_method` recorded;
   no arithmetic is ever accepted from a model; concrete model IDs are always
   stored (A16).
3. **Append-only evidence** (§7, A18). Documents, locators, and extraction
   records are immutable; change happens as new `value_revision` rows.
4. **Provenance or it doesn't exist** (§6). Schema constraints make an
   unprovenanced quantitative value uncommittable.
5. **Workflow failure ≠ audit finding** (A4, §60). Adapter/stage failures
   become `workflow_issue` records, never `audit_finding` rows and never
   domain facts ("no OA version exists").
6. **Everything replaceable** (§59): adapters behind interfaces with
   fake/replay implementations; no parser is the unquestioned source of truth
   (A12); model roles are configuration (A16).
7. **Resumable by construction** (§61): durable jobs, at-least-once execution,
   idempotent handlers keyed by stable idempotency keys (A11).
8. **Conservative findings** (A24): automated results are `SYSTEM_FLAGGED`
   evidence; confirmation is a researcher act wherever interpretation is
   required.

## 4. Key technology choices (ADR summary)

| Decision | Choice | Rationale | Alternatives rejected |
|---|---|---|---|
| Backend language | Python 3.12 | §64; scientific ecosystem | Node (weaker stats ecosystem) |
| API framework | FastAPI + Pydantic v2 | typed schemas = API contract | Django (heavier) |
| DB | **SQLite (WAL) embedded; PostgreSQL-portable via repositories/Alembic** (A1) | zero end-user administration; privacy; easy delete/backup | Postgres-first (end-user install burden) |
| ORM/migrations | SQLAlchemy 2 + Alembic | portable across SQLite/PG | raw SQL |
| Job queue | DB-backed durable queue, **at-least-once + idempotent handlers**, lease/retry/checkpoint (A11) | resumability needs durable state anyway; abstraction allows PG/Redis later | Celery+Redis (end-user infra); "exactly-once" claims (unachievable) |
| Worker model | single worker process, bounded async concurrency (doc 00 O4) | SQLite single-writer; stages are mostly I/O-bound | multi-process pool (revisit on PG) |
| PDF parsing | **orchestration layer** over PyMuPDF baseline + optional GROBID + OCR fallback (A12) | no single source of truth; benchmark-selected | GROBID-only (Java dependency, single oracle) |
| Statistics | hand-implemented in `statengine` (numpy/scipy), validated vs R `metafor` (§65) | formula-level provenance | calling R in production |
| LLM | `LLMProvider` + **model-role router** (`FAST/DEFAULT_EXTRACTION/COMPLEX_EXTRACTION/ESCALATION`), roles assigned by gold-corpus benchmarks; concrete model ID recorded per call (A16) | benchmark-driven, no hard-coded model duties | fixed model-per-task wiring |
| Frontend | Next.js + TypeScript, TanStack Query, SSE | §64; researcher UI | — |
| PDF display | PDF.js + overlay from normalized bboxes (A9) | robust highlighting across renderers | server-rendered images |
| IDs | UUIDv7 | sortable; PG-migration & merge safe | serial ints |

## 5. Pipeline execution model

A *stage* is a function `run(work_item) -> StageResult` registered with
`stage_id`, input kind, **idempotency key template** (e.g.
`parse_document:{document_hash}:{parser_version}`), and `version`. Worker loop:

```text
claim job (lease with expiry) → check idempotency key/input hash
  → run stage → write results + state transition in one transaction
  → emit progress event (SSE)
```

- At-least-once semantics: a crashed worker's lease expires and the job is
  re-claimed; handlers are idempotent (upsert by natural key + input hash), so
  re-execution is safe (A11).
- Stage `version` participates in the input hash: version bumps recompute
  instead of hitting stale cache (§62).
- Fan-out jobs give per-item progress ("37 of 52", §20) and default
  resumability (§61).
- Stage failures write stage states and, where researcher-visible, open
  `workflow_issue` records (one per work item × issue type, auto-resolved on
  later success — doc 00 O3).

## 6. Security & privacy posture (§58)

- One HTTP client wrapper logs every external call (destination, purpose,
  payload size) to `external_call_log`; Settings renders "what left this
  machine".
- LLM calls send minimal spans/regions where the stage permits; whole-document
  sends are marked as such.
- API keys in OS keychain/env, never in DB or exports.
- Project deletion removes DB rows and content-addressed files with zero
  refcount.

## 7. What the API server never does

- Run pipeline work inline; perform statistics (that is `statengine` via
  workers); talk to external services directly; or expose internal vocabulary
  to the primary UI (doc 00 UI requirement).
