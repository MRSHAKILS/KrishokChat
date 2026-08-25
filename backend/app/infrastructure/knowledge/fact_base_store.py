"""R2 — Fail-open loader for the fact-base artifact.

Same contract as ``calendar_store.load_crop_calendars`` and
``dose_reference.load_dose_reference``: a missing or corrupt artifact returns
an empty ``FactBase`` — never a 500, never a startup crash.

The loader is intentionally minimal: validation of individual rows is the
builder's job (``scripts/build_fact_base.py``).  The loader only checks that
the artifact has the expected top-level shape.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.domain.fact_base import FactBase

logger = logging.getLogger("krishokchat.knowledge")


def load_fact_base(path: str | Path) -> FactBase:
    """Load the fact-base artifact; return empty FactBase on any error.

    Never raises — an absent or corrupt file disables the T1/T2 resolver
    (R4) without affecting the T3 fallback path.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
    except FileNotFoundError:
        logger.warning("fact base not found at %s — structured resolver disabled", path)
        return FactBase.empty()
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("fact base unreadable at %s (%s) — structured resolver disabled", path, exc)
        return FactBase.empty()

    if not isinstance(payload.get("facts"), list):
        logger.warning("fact base at %s has no 'facts' list — structured resolver disabled", path)
        return FactBase.empty()

    fb = FactBase.from_artifact(payload)
    if not fb.facts:
        logger.warning("fact base at %s loaded 0 facts — check the artifact", path)
    else:
        logger.info("fact base loaded: %d facts from %s", len(fb), path)
    return fb
