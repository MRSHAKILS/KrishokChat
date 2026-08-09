from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from app.domain.contracts import QAResult


class VisionStatus(StrEnum):
    DIAGNOSED = "diagnosed"
    HEALTHY = "healthy"
    NOT_RECOGNIZED = "not_recognized"
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
class VisionTraceEvent:
    stage: VisionStage
    status: str
    detail: str | None = None


@dataclass(frozen=True)
class VisionResult:
    status: VisionStatus
    crop: str | None = None
    crop_confidence: float = 0.0
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
    error: str | None = None
