from __future__ import annotations

from typing import Protocol

from PIL import Image

from app.domain.vision import VisionModelSpec, VisionPrediction


class VisionInferenceError(RuntimeError):
    """Provider-neutral vision inference failure."""


class VisionModelRegistry(Protocol):
    @property
    def crop_classifier(self) -> VisionModelSpec: ...

    def disease_candidates(self, crop: str) -> tuple[VisionModelSpec, ...]: ...

    def disease_info(self, model_key: str, label: str) -> dict | None: ...

    def is_healthy(self, label: str) -> bool: ...


class VisionRunner(Protocol):
    def predict(self, spec: VisionModelSpec, image: Image.Image) -> VisionPrediction: ...
