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
from app.core.config import settings


def create_app(config=None) -> FastAPI:
    """Create an app with an isolated composition root for tests and deployments."""
    app_settings = config or settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.container = build_container(app_settings)
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
    application.include_router(qa_router)
    application.include_router(vision_router)
    application.include_router(soil_router)
    application.include_router(benchmark_router)
    application.include_router(extras_router)
    application.include_router(auth_router)
    application.include_router(history_router)

    @application.get("/health")
    async def health_check():
        return {"status": "ok", "version": app_settings.app_version}

    return application


app = create_app()
