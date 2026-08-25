"""R6: QA Capability — wraps the core QAPipeline under the Capability port."""

from __future__ import annotations

from typing import Any

from app.application.qa_pipeline import QAInput, QAPipeline
from app.domain.enums import ResolutionTier
from app.domain.intent import Intent
from app.ports.capability import (
    Capability,
    CapabilityContext,
    CapabilityDescriptor,
    CapabilityResult,
    CapabilityUnavailable,
)


class QACapability:
    """Core Bengali agricultural Q&A capability wrapping the 5-tier QAPipeline."""

    id: str = "qa_advisory"
    name_bn: str = "কৃষি প্রশ্নোত্তর ও পরামর্শ"
    name_en: str = "Agricultural Q&A Advisory"
    description_bn: str = "৫-স্তর রেজোলিউশন ল্যাডার (ফ্যাক্ট বেস + বিএম২৫ রিট্রিভাল + জেনারেটিভ মডেল) ভিত্তিক পূর্ণাঙ্গ কৃষি পরামর্শ।"
    requires: frozenset[str] = frozenset({"corpus", "facts"})
    status: str = "active"

    def __init__(self, pipeline: QAPipeline) -> None:
        self._pipeline = pipeline

    @property
    def available(self) -> bool:
        # Always available when pipeline is wired (retriever or resolver present)
        return self._pipeline is not None

    def descriptor(self) -> CapabilityDescriptor:
        return CapabilityDescriptor(
            id=self.id,
            name_bn=self.name_bn,
            name_en=self.name_en,
            description_bn=self.description_bn,
            requires=self.requires,
            available=self.available,
            status=self.status,
        )

    def can_handle(self, intent: Intent | None) -> float:
        # Default handler for standard queries, dosage questions, general management
        if intent is None:
            return 0.8
        kind = getattr(intent, "kind", "")
        if kind in ("dosage", "disease_management", "general_management", "crop_recommendation"):
            return 0.95
        if kind in ("banned_chemical", "poisoning_risk"):
            return 0.2  # Safety escalation capability has higher priority
        return 0.8

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        if not self.available:
            raise CapabilityUnavailable("QAPipeline is not available")

        qa_input = QAInput(
            query=ctx.query,
            context=ctx.query_context,
            model=ctx.extra.get("model"),
        )
        qa_res = await self._pipeline.run(qa_input)

        return CapabilityResult(
            capability_id=self.id,
            answer=qa_res.answer,
            resolution_tier=qa_res.resolution_tier,
            provenance={
                "category": qa_res.category.value,
                "sources_count": len(qa_res.sources),
                "model": qa_res.model,
                "top_source": qa_res.sources[0].model_dump() if qa_res.sources else None,
            },
            cost_estimate_usd=None,
            metadata={"decision": qa_res.decision.model_dump() if qa_res.decision else None},
        )
