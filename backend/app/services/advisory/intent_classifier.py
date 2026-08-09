"""Legacy advisory-intent compatibility layer.

Safety is now owned by ``app.application.safety``. This module remains only so old
offline scripts do not silently select a second provider or a fail-open policy.
"""

from __future__ import annotations

import asyncio

from app.application.safety import SafetyClassifier
from app.core.config import settings
from app.domain.contracts import QueryContext
from app.infrastructure.llm.factory import create_llm_client


def classify_intent(query: str, detected_crop: str | None = None, detected_disease: str | None = None) -> dict:
    decision = asyncio.run(
        SafetyClassifier(create_llm_client(settings, role="intent")).classify(
            query,
            QueryContext(crop=detected_crop, disease=detected_disease),
        )
    )
    if decision.category.value != "safe_agri":
        intent = decision.category.value
    else:
        lowered = query.lower()
        if any(word in lowered for word in ("প্রতিকার", "চিকিৎসা", "treatment", "cure")):
            intent = "treatment"
        elif any(word in lowered for word in ("প্রতিরোধ", "রোধ", "prevent")):
            intent = "prevention"
        elif any(word in lowered for word in ("সার", "fertilizer", "urea")):
            intent = "fertilizer"
        else:
            intent = "general_info"
    return {
        "intent": intent,
        "safety_flag": "blocked" if decision.terminal else "ok",
        "confidence": decision.confidence,
        "reasoning": decision.reason,
        "canned_response": decision.response,
    }
