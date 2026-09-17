"""Typed internal contracts shared by application services and adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.enums import (
    AnswerabilityLevel,
    PipelineStage,
    ResolutionTier,
    SafetyCategory,
    StageStatus,
    VerificationConfidence,
)
from app.domain.intent import Intent


@dataclass(frozen=True)
class AgriculturalState:
    """Stateful representation of the ongoing agronomic conversation.

    Prevents blind conversation history dumping to the LLM by maintaining
    an explicit structured semantic frame.
    """

    active_crop: str | None = None
    active_problem: str | None = None
    active_stage: str | None = None
    growth_stage: str | None = None
    location: str | None = None
    confirmed_slots: tuple[str, ...] = ()
    missing_slots: tuple[str, ...] = ()



@dataclass(frozen=True)
class QueryContext:
    crop: str | None = None
    disease: str | None = None
    history: tuple[dict[str, str], ...] = ()
    # P2: optional one-line farmer/crop-stage context (e.g. "ফসল: আলু ·
    # বর্তমান পর্যায়: কন্দ স্ফীতি ..."). Absent (None) → prompts/retrieval are
    # byte-identical to the pre-P2 pipeline (locked by a regression test).
    farmer_context: str | None = None


@dataclass(frozen=True)
class SafetyDecision:
    category: SafetyCategory
    confidence: float
    reason: str = ""
    matched_rules: tuple[str, ...] = ()
    requires_escalation: bool = False
    response: str | None = None
    # True when the classifier provider was unreachable/invalid and the
    # fail-closed LOW_CONFIDENCE decision is an outage, not a real judgment.
    # The pipeline may then replay a curated safe_agri demo-cache answer;
    # real terminal decisions never replay.
    classifier_outage: bool = False
    # R5: advisory routing hint produced alongside the safety decision.
    # None on terminal decisions (no routing needed) and classifier outages.
    # Never influences safety category — additive and advisory only.
    intent: Intent | None = None

    @property
    def terminal(self) -> bool:
        return self.category is not SafetyCategory.SAFE_AGRI


@dataclass(frozen=True)
class RetrievedSource:
    id: str
    score: float
    title_en: str = ""
    title_bn: str = ""
    content_en: str = ""
    content_bn: str = ""
    source: str = ""
    citation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GenerationResult:
    answer: str
    used_source_ids: tuple[str, ...] = ()
    model: str = ""
    mode: str = ""
    error: str | None = None


@dataclass(frozen=True)
class VerifierClaim:
    """One atomic claim verdict from the hardened verifier (P1).

    verdict: ``grounded`` | ``unsupported`` | ``no_dosage``.
    ``no_dosage`` claims carry no measurable quantity and are informational.
    """

    text: str
    verdict: str
    reason: str = ""


@dataclass(frozen=True)
class VerificationResult:
    confidence: VerificationConfidence
    flags: tuple[str, ...] = ()
    unverified_claims: tuple[str, ...] = ()
    # P1 hardening: per-claim verdicts, annotate-and-drop output, counts.
    claims: tuple[VerifierClaim, ...] = ()
    sanitized_answer: str | None = None
    checked_count: int = 0
    grounded_count: int = 0
    unsupported_count: int = 0


@dataclass(frozen=True)
class PipelineEvent:
    stage: PipelineStage
    status: StageStatus
    detail: str | None = None
    event_type: str = "stage"
    text: str | None = None


@dataclass(frozen=True)
class QAResult:
    query: str
    category: SafetyCategory
    answer: str
    sources: tuple[RetrievedSource, ...] = ()
    confidence: VerificationConfidence = VerificationConfidence.LOW_CONFIDENCE
    trace: tuple[PipelineEvent, ...] = ()
    verifier_flags: tuple[str, ...] = ()
    verifier_claims: tuple[VerifierClaim, ...] = ()
    model: str = ""
    error: str | None = None
    # P5: refusal transparency — which deterministic rule fired (e.g.
    # coverage_training) and the safety decision reason, surfaced to the UI.
    matched_rules: tuple[str, ...] = ()
    safety_reason: str | None = None
    # R3: how the answer was produced (resolution tier, five-tier ladder).
    # Default is grounded_generation — the only tier that can have been cached
    # before R3 landed (only verified safe_agri T3 answers were ever cached).
    resolution_tier: ResolutionTier = ResolutionTier.GROUNDED_GENERATION
    # Stage 2 KAERA / PRISM: 5-level answerability scale & progressive help
    answerability_level: AnswerabilityLevel = AnswerabilityLevel.A2_STRONG_EVIDENCE
    progressive_guidance: dict[str, Any] | None = None

