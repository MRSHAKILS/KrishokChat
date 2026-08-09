"""Ultralytics classification adapter. No HTTP or FastAPI types cross this boundary."""

from __future__ import annotations

import threading

import numpy as np
from PIL import Image
from ultralytics import YOLO

from app.domain.vision import VisionModelSpec, VisionPrediction
from app.ports.vision import VisionInferenceError


class UltralyticsClassificationRunner:
    def __init__(self) -> None:
        self._models: dict[str, YOLO] = {}
        self._lock = threading.Lock()

    def _model(self, spec: VisionModelSpec) -> YOLO:
        if spec.key not in self._models:
            with self._lock:
                if spec.key not in self._models:
                    if not spec.path.exists():
                        raise VisionInferenceError(f"Model artifact not found: {spec.path}")
                    self._models[spec.key] = YOLO(str(spec.path))
        return self._models[spec.key]

    def predict(self, spec: VisionModelSpec, image: Image.Image) -> VisionPrediction:
        if spec.task != "classify":
            raise VisionInferenceError(
                f"Unsupported artifact task '{spec.task}' for {spec.key}; classification adapter refuses to fabricate boxes"
            )
        try:
            result = self._model(spec)(image, verbose=False)[0]
            if getattr(result, "probs", None) is None:
                raise VisionInferenceError(f"Model {spec.key} returned no classification probabilities")
            probabilities = result.probs.data.detach().cpu().numpy().astype(float)
        except VisionInferenceError:
            raise
        except Exception as exc:
            raise VisionInferenceError(f"Vision inference failed for {spec.key}: {exc}") from exc
        if probabilities.size == 0:
            raise VisionInferenceError(f"Model {spec.key} returned empty probabilities")
        order = np.argsort(probabilities)[::-1]
        def label(index: int) -> str:
            return spec.class_names[index] if index < len(spec.class_names) else str(index)
        top = int(order[0])
        top3 = tuple(
            {"class": label(int(index)), "confidence": round(float(probabilities[int(index)]), 4)}
            for index in order[:3]
        )
        return VisionPrediction(label=label(top), confidence=round(float(probabilities[top]), 4), top3=top3)
