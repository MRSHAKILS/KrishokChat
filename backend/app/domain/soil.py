"""Soil moisture domain — dataset showcase + measured-sample replay.

The regression model is in development (all artifacts negative R²), so the
analyze path can never produce a live moisture estimate. The only "analyzed"
results are replays of known sample records from the frozen release package
(matched by image ID); every other image gets the honest locked response.
The dataset, however, is a first-class released asset and ships today.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class SoilStatus(StrEnum):
    """Outcome states for soil endpoints."""

    LOCKED = "locked"  # no validated model; unknown images get this honest state
    ANALYZED = "analyzed"  # measured-sample replay only (never a live diagnosis)
    INVALID_IMAGE = "invalid_image"


class SoilStage(StrEnum):
    """Pipeline stages for the soil console rail (future stages reserved)."""

    INTAKE = "intake"
    MOISTURE_REGRESSION = "moisture_regression"
    SOIL_CLASSIFICATION = "soil_classification"
    ADVISORY = "advisory"


@dataclass(frozen=True)
class SoilTypeStat:
    key: str  # e.g. "Doash"
    usda: str  # e.g. "Loam"
    count: int


@dataclass(frozen=True)
class SoilSample:
    image_id: str
    filename: str
    soil_type: str
    kpa: float
    land_type: str
    crop: str
    growth_stage: str


@dataclass(frozen=True)
class SoilModelResult:
    model: str
    rmse_kpa: float
    r2: float


@dataclass(frozen=True)
class SoilDatasetInfo:
    total_images: int
    kpa_range: tuple[float, float]
    kpa_bins: dict[str, int] = field(default_factory=dict)
    soil_types: tuple[SoilTypeStat, ...] = ()
    land_types: dict[str, int] = field(default_factory=dict)
    crops: dict[str, int] = field(default_factory=dict)
    growth_stages: dict[str, int] = field(default_factory=dict)
    series_count: int = 0
    splits: dict[str, int] = field(default_factory=dict)
    metadata_matched: int = 0
    metadata_inferred: int = 0
    corrections: int = 0
    collection: dict[str, str] = field(default_factory=dict)
    model_status: str = "in_development"
    model_results: tuple[SoilModelResult, ...] = ()
    samples: tuple[SoilSample, ...] = ()
    available: bool = False  # False when the release folder is absent


@dataclass(frozen=True)
class SoilTraceEvent:
    stage: SoilStage
    status: str  # complete | skip | error
    detail: str | None = None


@dataclass(frozen=True)
class SoilResult:
    status: SoilStatus
    info: SoilDatasetInfo | None = None
    error: str | None = None
    trace: tuple[SoilTraceEvent, ...] = ()
    sample_id: str | None = None  # set only for measured-sample replays
    soil_type: str | None = None
    soil_type_bn: str | None = None
    kpa: float | None = None
    moisture_status: str | None = None
    moisture_status_bn: str | None = None
    advisory_bn: str | None = None
    confidence: float | None = None