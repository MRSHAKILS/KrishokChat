"""P0-4: startup bootstrap checks — warnings only, never failures.

Runs once per process at lifespan startup. Every check is advisory: a demo
box with a misconfiguration must still boot (AGENTS.md hard rule 1 — auth and
hardening are additive and must never gate the demo), so these only emit
structured log warnings that a human or the log aggregator can act on.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.core.config import Settings

logger = logging.getLogger("krishokchat.bootstrap")


def _has_provider_key(settings: Settings) -> bool:
    if settings.openrouter_api_key:
        return True
    if settings.gemini_api_key:
        return True
    if settings.llm_api_key:
        return True
    return False


def run_bootstrap_checks(settings: Settings) -> list[str]:
    """Return human-readable warnings; log each one. Never raises."""
    warnings: list[str] = []

    if not _has_provider_key(settings) and not settings.demo_mode:
        warnings.append(
            "no LLM provider key configured (OPENROUTER_API_KEY / GEMINI_API_KEY) "
            "and DEMO_MODE is off — every query will fail closed to the referral path"
        )
    if settings.demo_mode and not _has_provider_key(settings):
        logger.info("demo mode without provider keys: curated replay only")

    ml_assets = Path(settings.ml_assets_dir)
    if not ml_assets.is_dir():
        warnings.append(f"ml_assets_dir missing: {ml_assets}")

    soil = Path(settings.soil_release_dir)
    if not soil.is_dir():
        warnings.append(
            f"soil release folder missing: {soil} (soil API reports unavailable)"
        )

    if settings.readiness_strict:
        logger.info("READINESS_STRICT=true: /readyz will 503 on failed checks")

    if settings.environment == "production" and settings.docs_enabled:
        logger.info(
            "ENVIRONMENT=production with DOCS_ENABLED=true: API docs are public"
        )

    for warning in warnings:
        logger.warning("bootstrap: %s", warning)
    return warnings
