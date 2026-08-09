"""Compatibility shim for legacy scripts.

The authoritative implementation is ``app.application.safety.SafetyClassifier``.
New code must inject the classifier through ``AppContainer`` instead of importing this
module directly.
"""

from __future__ import annotations

import asyncio

from app.application.safety import SafetyClassifier
from app.core.config import settings
from app.domain.contracts import QueryContext
from app.domain.safety_policy import precheck
from app.infrastructure.llm.factory import create_llm_client


def _precheck(query: str) -> dict | None:
    match = precheck(query)
    if not match:
        return None
    category, rules = match
    return {
        "category": category.value,
        "confidence": 1.0,
        "reasoning": "Deterministic safety rule matched",
        "matched_rules": list(rules),
    }


def classify_query(query: str, crop: str | None = None, disease: str | None = None) -> dict:
    decision = asyncio.run(
        SafetyClassifier(create_llm_client(settings, role="intent")).classify(
            query,
            QueryContext(crop=crop, disease=disease),
        )
    )
    return {
        "category": decision.category.value,
        "confidence": decision.confidence,
        "reasoning": decision.reason,
        "matched_rules": list(decision.matched_rules),
        "requires_escalation": decision.requires_escalation,
        "canned_response": decision.response,
    }
