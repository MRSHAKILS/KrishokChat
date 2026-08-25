"""P2: fail-open loader for the crop-calendars artifact.

Same contract as the weather snapshot: a missing or broken file disables the
feature (returns None) — callers surface an honest "unavailable", never a 500.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.domain.crop_calendar import CropCalendarLibrary

logger = logging.getLogger("krishokchat.agronomy")


def load_crop_calendars(path: str | Path) -> CropCalendarLibrary | None:
    try:
        with open(path, encoding="utf-8") as fh:
            artifact = json.load(fh)
    except FileNotFoundError:
        logger.warning("crop calendars not found at %s — stage feature disabled", path)
        return None
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("crop calendars unreadable at %s (%s) — stage feature disabled", path, exc)
        return None
    if not artifact.get("crops"):
        logger.warning("crop calendars at %s carried no crops — stage feature disabled", path)
        return None
    return CropCalendarLibrary(artifact)
