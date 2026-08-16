from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.container import build_container
from app.api.qa import router as qa_router
from app.api.benchmark import router as benchmark_router
from app.api.vision import router as vision_router
from app.api.soil import router as soil_router
from app.api.extras import router as extras_router
from app.api.auth import router as auth_router
from app.api.history import router as history_router
from app.api.speech import router as speech_router
# T0-04: request-ID middleware (echo/generate X-Request-ID) + JSON app logging.
from app.api.middleware.request_id import RequestIDMiddleware
from app.core.config import settings
from app.core.logging import setup_logging


def create_app(config=None) -> FastAPI:
    """Create an app with an isolated composition root for tests and deployments."""
    app_settings = config or settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # T0-04: JSON-structured app logging before the container starts emitting.
        setup_logging(app_settings.log_level)
        app.state.container = build_container(app_settings)
        app.state.settings = app_settings
        yield

    application = FastAPI(
        title=app_settings.app_name,
        description="Safety-aware Bengali agricultural AI assistant",
        version=app_settings.app_version,
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # T0-04: request-ID middleware — echo/generate the configured header, store
    # it in a contextvar for log records. Pure pass-through; registered after
    # CORS so it sits outermost and every request (incl. preflight) gets an ID.
    application.add_middleware(
        RequestIDMiddleware,
        header_name=app_settings.request_id_header,
    )
    application.include_router(qa_router)
    application.include_router(vision_router)
    application.include_router(soil_router)
    application.include_router(benchmark_router)
    application.include_router(extras_router)
    application.include_router(auth_router)
    application.include_router(history_router)
    application.include_router(speech_router)

    @application.get("/health")
    async def health_check():
        return {"status": "ok", "version": app_settings.app_version}

    return application


app = create_app()
