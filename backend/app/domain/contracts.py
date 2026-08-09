"""Typed internal contracts shared by application services and adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.enums import (
    PipelineStage,
    SafetyCategory,
    StageStatus,
    VerificationConfidence,
)


@dataclass(frozen=True)
class QueryContext:
    crop: str | None = None
    disease: str | None = None
    history: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True)
class SafetyDecision:
    category: SafetyCategory
    confidence: float
    reason: str = ""
    matched_rules: tuple[str, ...] = ()
    requires_escalation: bool = False
    response: str | None = None

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
class VerificationResult:
    confidence: VerificationConfidence
    flags: tuple[str, ...] = ()
    unverified_claims: tuple[str, ...] = ()


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
    model: str = ""
    error: str | None = None
