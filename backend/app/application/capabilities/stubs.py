"""R6: Domain wrappers and reserved stubs for modular capabilities."""

from __future__ import annotations

from typing import Any

from app.domain.enums import ResolutionTier
from app.domain.intent import Intent
from app.ports.capability import (
    Capability,
    CapabilityContext,
    CapabilityDescriptor,
    CapabilityResult,
    CapabilityUnavailable,
)


class DiseaseAdvisoryCapability:
    """Vision-assisted crop disease diagnosis and advisory."""

    id: str = "disease_advisory"
    name_bn: str = "ফসলের রোগ ও পোকা নির্ণয়"
    name_en: str = "Crop Disease & Pest Diagnosis"
    description_bn: str = "ফসলের ছবি আপলোড করে এআই মডেলের মাধ্যমে রোগ শনাক্তকরণ ও প্রেসক্রিপশন।"
    requires: frozenset[str] = frozenset({"vision", "facts"})
    status: str = "active"

    def __init__(self, vision_classifier_available: bool, fact_base_available: bool) -> None:
        self._vision_available = vision_classifier_available
        self._facts_available = fact_base_available

    @property
    def available(self) -> bool:
        return self._vision_available

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
        if intent and getattr(intent, "kind", "") == "disease_management":
            return 0.9
        return 0.0

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        if not self.available:
            raise CapabilityUnavailable("Vision models are not available")
        return CapabilityResult(
            capability_id=self.id,
            answer="ছবি আপলোডের মাধ্যমে রোগ নির্ণয় সক্রিয় রয়েছে।",
            resolution_tier=ResolutionTier.TEMPLATED_ADVISORY,
        )


class SoilAdvisoryCapability:
    """Soil test analysis and fertilizer recommendations (replay-only mode)."""

    id: str = "soil_advisory"
    name_bn: str = "মাটি পরীক্ষা ও সার সুপারিশ"
    name_en: str = "Soil Test & Fertilizer Advisory"
    description_bn: str = "মাটির পুষ্টি উপাদান (N, P, K, pH) বিশ্লেষণ করে সুষম সার প্রয়োগের মাত্রা নির্ধারণ।"
    requires: frozenset[str] = frozenset({"soil"})
    status: str = "replay_only"

    def __init__(self, soil_engine_available: bool = True) -> None:
        self._available = soil_engine_available

    @property
    def available(self) -> bool:
        return self._available

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
        if intent and getattr(intent, "kind", "") == "fertilizer":
            return 0.9
        return 0.0

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        if not self.available:
            raise CapabilityUnavailable("Soil advisory engine unavailable")
        return CapabilityResult(
            capability_id=self.id,
            answer="মাটি পরীক্ষার তথ্যের ভিত্তিতে সুষম সার সুপারিশ প্রস্তুত করা হয়েছে।",
            resolution_tier=ResolutionTier.STRUCTURED_FACT,
        )


class WeatherRiskCapability:
    """Agro-meteorological late blight and climate risk alerts."""

    id: str = "weather_risk"
    name_bn: str = "আবহাওয়া ও বালাই সতর্কতা"
    name_en: str = "Agro-Weather Risk Advisory"
    description_bn: str = "তাপমাত্রা ও আর্দ্রতা পূর্বাভাস বিশ্লেষণ করে নাবি ধ্বসা রোগের আগাম সতর্কতা।"
    requires: frozenset[str] = frozenset({"weather"})
    status: str = "active"

    def __init__(self, weather_snapshot_available: bool) -> None:
        self._available = weather_snapshot_available

    @property
    def available(self) -> bool:
        return self._available

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
        if intent and getattr(intent, "kind", "") == "weather_risk":
            return 0.95
        return 0.0

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        if not self.available:
            raise CapabilityUnavailable("Weather data snapshot is unavailable")
        return CapabilityResult(
            capability_id=self.id,
            answer="আবহাওয়া পূর্বাভাস অনুযায়ী বালাই ঝুঁকি বিশ্লেষণ সম্পন্ন হয়েছে।",
            resolution_tier=ResolutionTier.STRUCTURED_FACT,
        )


class StageAdviceCapability:
    """Crop stage-specific phenological calendar advice."""

    id: str = "stage_advice"
    name_bn: str = "ফসল পর্যায়ভিত্তিক ক্যালেন্ডার"
    name_en: str = "Crop Phenological Stage Advice"
    description_bn: str = "বপন/রোপণ দিনের (DAS) ওপর ভিত্তি করে ফসল পরিচর্যার সময়োপযোগী নির্দেশনা।"
    requires: frozenset[str] = frozenset({"farm_profile", "facts"})
    status: str = "active"

    def __init__(self, calendars_available: bool) -> None:
        self._available = calendars_available

    @property
    def available(self) -> bool:
        return self._available

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
        if intent and getattr(intent, "kind", "") == "crop_stage":
            return 0.95
        return 0.0

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        if not self.available:
            raise CapabilityUnavailable("Crop calendars unavailable")
        return CapabilityResult(
            capability_id=self.id,
            answer="ফসলের বর্তমান বৃদ্ধি পর্যায় অনুযায়ী পরামর্শ প্রদান করা হয়েছে।",
            resolution_tier=ResolutionTier.TEMPLATED_ADVISORY,
        )


class SafetyEscalationCapability:
    """Deterministic safety escalation redirecting to national Krishi Call Center 16123."""

    id: str = "safety_escalation"
    name_bn: str = "জরুরি কৃষি সহায়তা (১৬১২৩)"
    name_en: str = "Safety Escalation Helpline"
    description_bn: str = "নিষিদ্ধ রাসায়নিক বা জরুরি স্বাস্থ্য ঝুঁকিতে কৃষি কল সেন্টার ১৬১২৩-এ দিকনির্দেশনা।"
    requires: frozenset[str] = frozenset()
    status: str = "active"

    @property
    def available(self) -> bool:
        return True

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
        if intent and getattr(intent, "kind", "") in ("banned_chemical", "poisoning_risk"):
            return 1.0
        return 0.0

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        return CapabilityResult(
            capability_id=self.id,
            answer="নিরাপত্তা ঝুঁকি চিহ্নিত হয়েছে। জরুরি পরামর্শের জন্য জাতীয় কৃষি কল সেন্টার ১৬১২৩ নম্বরে যোগাযোগ করুন।",
            resolution_tier=ResolutionTier.DETERMINISTIC_GUARD,
        )


class StubCapability:
    """Reserved capability stub for future roadmap modules (irrigation, market price, drone)."""

    def __init__(
        self,
        id: str,
        name_bn: str,
        name_en: str,
        description_bn: str,
        requires: frozenset[str],
    ) -> None:
        self.id = id
        self.name_bn = name_bn
        self.name_en = name_en
        self.description_bn = description_bn
        self.requires = requires
        self.status = "reserved_stub"

    @property
    def available(self) -> bool:
        return False

    def descriptor(self) -> CapabilityDescriptor:
        return CapabilityDescriptor(
            id=self.id,
            name_bn=self.name_bn,
            name_en=self.name_en,
            description_bn=self.description_bn,
            requires=self.requires,
            available=False,
            status=self.status,
        )

    def can_handle(self, intent: Intent | None) -> float:
        return 0.0

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        raise CapabilityUnavailable(f"Capability '{self.id}' is a reserved future module and is currently unavailable.")
