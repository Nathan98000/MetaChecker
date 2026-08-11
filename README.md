# Meta-Analysis Audit Tool

A local, researcher-friendly application for auditing published meta-analyses:
were the right data extracted from the included studies, were study-level
effects calculated correctly, and do the pooled results reproduce?

**Scope:** the tool audits the studies *included* in a published meta-analysis
and what was done with them. It does not assess whether additional eligible
studies were omitted from the review (see `docs/00-ambiguities-and-decisions.md`, A19).

## Layout

```text
docs/        design documentation (read docs/README.md first)
backend/     Python API + worker (FastAPI, SQLite, SQLAlchemy/Alembic)
frontend/    researcher UI (Next.js, static export)
src-tauri/   desktop shell (Tauri; supervises the backend as a child process)
corpus/      gold-standard + adversarial benchmark corpora (in progress)
```

## Development setup

Backend (Python 3.12):

```bash
cd backend && python3.12 -m venv .venv && .venv/bin/pip install -e ".[dev]"
```

Run the test suite (includes provenance invariants, queue crash-recovery, the
HTTP vertical slice, and the SQLite concurrency measurement):

```bash
cd backend && .venv/bin/python -m pytest tests -q
```

Run the app in development (two options):

```bash
# Option 1 — desktop shell (spawns the backend itself):
cd src-tauri && cargo run

# Option 2 — browser dev mode:
cd backend && .venv/bin/python -m uvicorn app.api.main:create_app --factory --port 8977
cd frontend && npm install && npm run dev   # then open http://localhost:3000
```

Database migrations:

```bash
cd backend && .venv/bin/alembic upgrade head
```

Data location: `METAAUDIT_DATA_DIR` (defaults to `backend/var/data` in dev;
the desktop shell uses the platform app-data directory). Original documents
are stored content-addressed and never modified; deleting a project removes
its data.

## Status

Foundation + vertical slice complete (see `docs/09-milestone-plan.md`):
project creation, immutable document ingestion, append-only provenance,
durable at-least-once job queue, PDF text-span extraction with normalized
bounding boxes, and the click-through evidence viewer. Packaging of the
backend as a bundled sidecar binary is tracked in the packaging cross-cutting
track and not yet done — `cargo run` currently expects the dev venv at
`backend/.venv`.
