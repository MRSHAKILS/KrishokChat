from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, Header, HTTPException, Request, status

from app.application.auth import AuthService
from app.application.container import AppContainer
from app.application.history import HistoryService
from app.core.config import Settings


def get_container(request: Request) -> AppContainer:
    container = getattr(request.app.state, "container", None)
    if container is None:
        raise RuntimeError("Application container has not been initialized")
    return container


ContainerDep = Annotated[AppContainer, Depends(get_container)]


def get_settings(request: Request) -> Settings:
    """The app's resolved settings (test configs override the module default)."""
    settings = getattr(request.app.state, "settings", None)
    if settings is None:
        from app.core.config import settings as default_settings

        return default_settings
    return settings


SettingsDep = Annotated[Settings, Depends(get_settings)]


def _get_auth_service(container: ContainerDep) -> AuthService:
    return getattr(container, "auth", None) or AuthService()


AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]


def optional_user(
    authorization: Annotated[str | None, Header()] = None,
    service: AuthServiceDep = None,  # type: ignore[assignment]
) -> dict[str, Any] | None:
    """Claims when a valid Bearer token is present, else None. Never blocks."""
    return service.claims_from_authorization(authorization)


def require_user(
    authorization: Annotated[str | None, Header()] = None,
    service: AuthServiceDep = None,  # type: ignore[assignment]
) -> dict[str, Any]:
    """Claims or 401. For FUTURE premium endpoints only; nothing uses it today."""
    claims = service.claims_from_authorization(authorization)
    if claims is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return claims


OptionalUserDep = Annotated[dict[str, Any] | None, Depends(optional_user)]
RequiredUserDep = Annotated[dict[str, Any], Depends(require_user)]


def _get_history_service(container: ContainerDep) -> HistoryService:
    return getattr(container, "history", None) or HistoryService(store=None)


HistoryServiceDep = Annotated[HistoryService, Depends(_get_history_service)]