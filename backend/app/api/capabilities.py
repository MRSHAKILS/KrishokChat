"""R6: API endpoint for capability introspection."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.dependencies import get_container
from app.application.capabilities.registry import CapabilityRegistry
from app.application.container import AppContainer

router = APIRouter(tags=["capabilities"])


@router.get("/capabilities")
async def get_capabilities(
    container: AppContainer = Depends(get_container),
) -> dict[str, Any]:
    """Return all registered system capabilities with dynamic availability."""
    registry = container.capabilities
    descriptors = registry.list_descriptors() if registry else []
    return {
        "capabilities": [
            {
                "id": d.id,
                "name_bn": d.name_bn,
                "name_en": d.name_en,
                "description_bn": d.description_bn,
                "requires": sorted(list(d.requires)),
                "available": d.available,
                "status": d.status,
            }
            for d in descriptors
        ]
    }
