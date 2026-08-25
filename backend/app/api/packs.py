"""R9: API endpoint for offline fact pack manifest introspection."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter

logger = logging.getLogger("krishokchat.packs")

router = APIRouter(tags=["packs"])

MANIFEST_PATHS = [
    Path(__file__).resolve().parents[3] / "frontend" / "public" / "packs" / "manifest.json",
    Path(__file__).resolve().parents[2] / "frontend" / "public" / "packs" / "manifest.json",
]


def _load_manifest() -> dict[str, Any]:
    for p in MANIFEST_PATHS:
        if p.exists():
            try:
                with open(p, encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception as exc:
                logger.warning("Error reading pack manifest at %s: %s", p, exc)
    return {"schema_version": 1, "updated_at": "", "packs": []}


@router.get("/packs/manifest")
async def get_packs_manifest() -> dict[str, Any]:
    """Return manifest of available client-side offline fact packs."""
    return _load_manifest()
