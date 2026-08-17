from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

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
# T0-07: optional API-key auth + rate limiting, attached ONLY to the /api/v1
# surface via per-include dependencies (default-off — anonymous demo untouched).
from app.api.middleware.api_key import build_v1_guard_state, rate_limit, require_api_key
from app.core.config import settings
from app.core.logging import setup_logging

# T0-07: every router mounted under /api/* today is mirrored under /api/v1/*.
# /api/v1 is the stable, versioned API contract; the legacy paths remain as
# compatibility aliases. Add a new router to BOTH mounts.
V1_ROUTERS = (
    qa_router,
    vision_router,
    soil_router,
    benchmark_router,
    extras_router,
    auth_router,
    history_router,
    speech_router,
)


def _v1_path(path: str) -> str:
    """Map a legacy absolute path onto the v1 namespace.

    FastAPI's ``include_router(prefix=...)`` only prepends — it cannot
    rewrite an absolute path — so each route is re-registered with the
    leading ``/api`` segment replaced by ``/api/v1`` (e.g. ``/api/qa`` ->
    ``/qa`` under the ``/api/v1`` prefix). Non-``/api`` paths (e.g. the auth
    router's ``/auth/me``) keep their segment and land at ``/api/v1/auth/me``.
    """
    if path == "/api":
        return ""
    if path.startswith("/api/"):
        return path[len("/api"):]
    return path


def _mount_v1(application: FastAPI, router: APIRouter) -> None:
    """Mirror ``router`` under ``/api/v1`` with the optional guard attached.

    The same endpoint functions serve both surfaces; only the paths differ.
    The v1 mount is the ONLY place the API-key + rate-limit dependencies
    attach (per-include ``dependencies=`` — the legacy mounts below never
    carry them, so anonymous demo traffic is byte-identical).
    """
    v1 = APIRouter()
    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue
        v1.add_api_route(
            path=_v1_path(route.path),
            endpoint=route.endpoint,
            methods=list(route.methods),
            response_model=route.response_model,
            status_code=route.status_code,
            include_in_schema=route.include_in_schema,
            name=route.name,
        )
    application.include_router(
        v1,
        prefix="/api/v1",
        dependencies=[Depends(require_api_key), Depends(rate_limit)],
    )


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

    # T0-07: /api/v1 is the stable versioned API contract; the legacy mounts
    # above stay as compatibility aliases. The optional API-key + rate-limit
    # guard attaches ONLY here (per-include dependencies). Both switches
    # default off, so with a fresh .env this block changes nothing.
    guard_state = build_v1_guard_state(app_settings)
    application.state.api_key_store = guard_state["api_key_store"]
    application.state.rate_limiter = guard_state["rate_limiter"]
    for router in V1_ROUTERS:
        _mount_v1(application, router)

    @application.get("/health")
    async def health_check():
        return {"status": "ok", "version": app_settings.app_version}

    return application


app = create_app()
