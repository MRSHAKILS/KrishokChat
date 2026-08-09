from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.application.container import AppContainer


def get_container(request: Request) -> AppContainer:
    container = getattr(request.app.state, "container", None)
    if container is None:
        raise RuntimeError("Application container has not been initialized")
    return container


ContainerDep = Annotated[AppContainer, Depends(get_container)]
