from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from app.domain.contracts import QAResult


class VisionStatus(StrEnum):
    DIAGNOSED = "diagnosed"
    HEALTHY = "healthy"
    NOT_RECOGNIZED = "not_recognized"
    UNCERTAIN = "uncertain"
    OUT_OF_DISTRIBUTION = "out_of_distribution"
    REQUIRES_SECOND_IMAGE = "requires_second_image"
    NO_DISEASE_MODEL = "no_disease_model"
    MODEL_ERROR = "model_error"
    INVALID_IMAGE = "invalid_image"


class VisionStage(StrEnum):
    INTAKE = "intake"
    CROP_CLASSIFICATION = "crop_classification"
    DISEASE_CLASSIFICATION = "disease_classification"
    ADVISORY = "advisory"


@dataclass(frozen=True)
class VisionModelSpec:
    key: str
    path: Path
    class_names: tuple[str, ...]
    task: str = "classify"
    details_path: Path | None = None


@dataclass(frozen=True)
class VisionPrediction:
    label: str
    confidence: float
    top3: tuple[dict[str, str | float], ...] = ()


@dataclass(frozen=True)
class ImageQuality:
    accepted: bool
    width: int
    height: int
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class VisionGateConfig:
    # Calibrated from empirical sweep across 436 real test artifacts (Layer E02)
    crop_confidence_threshold: float = 0.90
    crop_margin_threshold: float = 0.20
    crop_ood_threshold: float = 0.40
    disease_confidence_threshold: float = 0.80
    disease_margin_threshold: float = 0.15
    # Module 1B: Known botanical confusion pair risk gating
    enable_confusion_risk_gating: bool = True
    confusion_crops: tuple[str, ...] = ("potato", "solanacea", "wheat", "corn")


@dataclass(frozen=True)
class VisionTraceEvent:
    stage: VisionStage
    status: str
    detail: str | None = None


@dataclass(frozen=True)
class VisionResult:
    status: VisionStatus
    crop: str | None = None
    crop_confidence: float = 0.0
    crop_source: str = "model"  # "model" | "user"
    disease: str | None = None
    disease_confidence: float = 0.0
    top3_crops: tuple[dict[str, str | float], ...] = ()
    top3_diseases: tuple[dict[str, str | float], ...] = ()
    disease_info: dict | None = None
    treatment_advice: str | None = None
    treatment_confidence: str | None = None
    treatment_sources: tuple[str, ...] = ()
    verifier_flags: tuple[str, ...] = ()
    trace: tuple[VisionTraceEvent, ...] = ()
    quality: ImageQuality | None = None
    clarification_prompt_bn: str | None = None
    suggested_crops: tuple[str, ...] = ()
    requires_second_image: bool = False
    error: str | None = None
