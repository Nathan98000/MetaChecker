"""FastAPI application factory.

The API is thin: routers call domain services; pipeline work is enqueued and
run by the worker thread (or drained synchronously in dev/test mode). The
Tauri shell supervises this process as a sidecar; the same app can be served
hosted later (doc 01).
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import Settings
from app.core.errors import AppError
from app.db import models  # noqa: F401 (register tables)
from app.db.base import Base, make_engine, make_session_factory
from app.pipeline import stages  # noqa: F401 (register stage handlers)
from app.pipeline.worker import WorkerThread

log = logging.getLogger("metaaudit.api")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.documents_dir.mkdir(parents=True, exist_ok=True)

    engine = make_engine(settings.db_path)
    Base.metadata.create_all(engine)  # migrations run via alembic in packaging
    session_factory = make_session_factory(engine)

    worker: WorkerThread | None = None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nonlocal worker
        if settings.run_worker:
            worker = WorkerThread(
                session_factory,
                settings.documents_dir,
                poll_seconds=settings.worker_poll_seconds,
                lease_seconds=settings.job_lease_seconds,
            )
            worker.start()
        yield
        if worker is not None:
            worker.stop()
            worker.join(timeout=5)

    app = FastAPI(title="Meta-Analysis Audit Tool", lifespan=lifespan)
    app.state.settings = settings
    app.state.session_factory = session_factory
    app.state.engine = engine

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "tauri://localhost"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError):
        return JSONResponse(status_code=exc.http_status, content=exc.to_payload())

    from app.api.routes import router

    app.include_router(router)
    return app
