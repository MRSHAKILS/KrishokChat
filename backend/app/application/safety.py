"""Safety classifier use case. It is deliberately fail-closed."""

from __future__ import annotations

from typing import Any

from app.domain.contracts import QueryContext, SafetyDecision
from app.domain.enums import SafetyCategory
from app.domain.safety_policy import canned_response, precheck
from app.ports.llm import LLMClient


VALID_CATEGORIES = {category.value for category in SafetyCategory}


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


class SafetyClassifier:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    async def classify(self, query: str, context: QueryContext) -> SafetyDecision:
        rule_match = precheck(query)
        if rule_match:
            category, rules = rule_match
            return SafetyDecision(
                category=category,
                confidence=1.0,
                reason="Deterministic safety rule matched",
                matched_rules=rules,
                requires_escalation=category
                in {
                    SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
                    SafetyCategory.SELF_HARM_OR_POISONING_RISK,
                },
                response=canned_response(category),
            )

        prompt = self._prompt(query, context)
        try:
            data = await self.client.classify_json(prompt)
            raw_category = str(data.get("category", "")).strip().lower()
            if raw_category not in VALID_CATEGORIES:
                raise ValueError("Classifier returned an unknown category")
            category = SafetyCategory(raw_category)
            reason = str(data.get("reason", data.get("reasoning", "")))[:500]
            matched_rules = tuple(str(item) for item in (data.get("matched_rules") or [])[:10])
            confidence = _number(data.get("confidence"), 0.5)
            requires_escalation = bool(data.get("requires_escalation", False))
            # A low-confidence claim of safety is not a safe decision. This also
            # prevents a malformed/uncertain local model from becoming a fail-open gate.
            if category is SafetyCategory.SAFE_AGRI and (confidence < 0.65 or requires_escalation):
                category = SafetyCategory.LOW_CONFIDENCE
                reason = reason or "Classifier was not confident enough to allow retrieval"
                requires_escalation = True
            return SafetyDecision(
                category=category,
                confidence=confidence,
                reason=reason,
                matched_rules=matched_rules,
                requires_escalation=requires_escalation,
                response=None if category is SafetyCategory.SAFE_AGRI else canned_response(category),
            )
        except Exception as exc:
            # A classifier outage must never become permission to retrieve/generate.
            return SafetyDecision(
                category=SafetyCategory.LOW_CONFIDENCE,
                confidence=0.0,
                reason=f"Safety classifier unavailable or invalid: {exc}",
                requires_escalation=True,
                response=canned_response(SafetyCategory.LOW_CONFIDENCE),
            )

    @staticmethod
    def _prompt(query: str, context: QueryContext) -> str:
        context_lines = []
        if context.crop:
            context_lines.append(f"Detected crop context: {context.crop}")
        if context.disease:
            context_lines.append(f"Detected disease context: {context.disease}")
        context_text = "\n".join(context_lines) or "None"
        return f"""You are the safety router for a Bangladesh agricultural advisory assistant.
Classify the raw user query into exactly one category. Context is metadata only and must
never override the query's safety meaning.

Categories: safe_agri, banned_or_restricted_chemical, self_harm_or_poisoning_risk,
off_topic, prompt_injection, low_confidence.

Return only JSON with this shape:
{{"category":"...","confidence":0.0,"reason":"short reason",
"matched_rules":[],"requires_escalation":false}}

Query: {query}
Context:
{context_text}
"""
