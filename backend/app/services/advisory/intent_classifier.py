"""Legacy advisory-intent compatibility layer.

Safety is now owned by ``app.application.safety``, which (since R5) also
produces the ``Intent`` slot alongside the safety decision in a single LLM
call. This module remains only so old offline scripts can still call
``classify_intent`` without re-introducing a second LLM call.

R5 change: the function now reads ``decision.intent`` directly; it does NOT
issue its own ``classify_json`` call. The shim still wraps the existing
``SafetyClassifier`` for the full decision, but intent is extracted from
the R5-enriched decision rather than re-derived, so any safe_agri query
uses at most ONE LLM call total (zero for precheck hits).
"""

from __future__ import annotations

import asyncio

from app.application.safety import SafetyClassifier
from app.core.config import settings
from app.domain.contracts import QueryContext
from app.infrastructure.llm.factory import create_llm_client


def classify_intent(query: str, detected_crop: str | None = None, detected_disease: str | None = None) -> dict:
    """Return intent + safety metadata for offline scripts.

    R5 note: intent is now produced by the same safety call — no second
    LLM invocation. If the classifier is unavailable the outage path
    returns intent=None (decision.intent is None on the outage path).
    """
    decision = asyncio.run(
        SafetyClassifier(create_llm_client(settings, role="intent")).classify(
            query,
            QueryContext(crop=detected_crop, disease=detected_disease),
        )
    )
    # R5: read intent from decision, not from a second classify_json call.
    if decision.intent is not None:
        intent_kind = decision.intent.kind or "general_info"
    elif decision.category.value != "safe_agri":
        intent_kind = decision.category.value
    else:
        intent_kind = "general_info"

    return {
        "intent": intent_kind,
        "safety_flag": "blocked" if decision.terminal else "ok",
        "confidence": decision.confidence,
        "reasoning": decision.reason,
        "canned_response": decision.response,
    }
