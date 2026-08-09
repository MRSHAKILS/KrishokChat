"""Artifact-backed vision registry.

The registry is derived from the checked-in class maps instead of duplicating labels in
Python. This prevents a model/class-index mismatch from being hidden in routing code.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from app.domain.vision import VisionModelSpec


def _class_names(path: Path) -> tuple[str, ...]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return tuple(str(data[str(index)]) for index in range(len(data)))
    if isinstance(data, list):
        return tuple(str(item) for item in data)
    raise ValueError(f"Unsupported class map format: {path}")


def _tokens(value: str) -> set[str]:
    return {token for token in re.split(r"[^a-z0-9]+", value.lower()) if len(token) > 1}


class ArtifactVisionRegistry:
    def __init__(self, vision_dir: Path) -> None:
        self.vision_dir = vision_dir
        classifier_dir = vision_dir / "crop_classifier"
        self._crop_classifier = self._spec(classifier_dir, required=True)
        self._disease: dict[str, VisionModelSpec] = {}
        self._details_cache: dict[str, dict] = {}
        for directory in sorted(vision_dir.iterdir()):
            if not directory.is_dir() or directory.name == "crop_classifier":
                continue
            if (directory / "model.pt").exists() and (directory / "class_names.json").exists():
                self._disease[directory.name.removesuffix("_disease").lower()] = self._spec(directory)

    @property
    def crop_classifier(self) -> VisionModelSpec:
        return self._crop_classifier

    @property
    def disease_models(self) -> dict[str, VisionModelSpec]:
        return dict(self._disease)

    def disease_candidates(self, crop: str) -> tuple[VisionModelSpec, ...]:
        key = crop.strip().lower().replace(" ", "")
        aliases = {"gourdguava": "", "solanacea": "", "maize": "corn"}
        mapped = aliases.get(key, key)
        spec = self._disease.get(mapped)
        return (spec,) if spec else ()

    def is_healthy(self, label: str) -> bool:
        normalized = label.lower().replace("_", "").replace(" ", "").replace("-", "")
        return normalized in {"healthy", "healthyleaf"} or normalized.endswith("healthy") or normalized.endswith("healthyleaf")

    def disease_info(self, model_key: str, label: str) -> dict | None:
        spec = self._disease.get(model_key)
        if not spec or not spec.details_path or not spec.details_path.exists():
            return None
        if model_key not in self._details_cache:
            self._details_cache[model_key] = json.loads(spec.details_path.read_text(encoding="utf-8"))
        target = _tokens(label.split("__")[-1])
        if not target:
            return None
        best: tuple[float, dict] | None = None
        for section in self._details_cache[model_key].values():
            if not isinstance(section, dict):
                continue
            for entry in section.get("classes", []):
                if not isinstance(entry, dict):
                    continue
                candidate = _tokens(str(entry.get("class_name", "")).split("(", 1)[0])
                if not candidate:
                    continue
                overlap = len(target & candidate) / len(target)
                if overlap >= 0.5 and (best is None or overlap > best[0]):
                    best = (overlap, entry)
        return best[1] if best else None

    @staticmethod
    def _spec(directory: Path, *, required: bool = False) -> VisionModelSpec:
        model_path = directory / "model.pt"
        class_path = directory / "class_names.json"
        if required and not model_path.exists():
            raise FileNotFoundError(f"Missing crop classifier weights: {model_path}")
        metadata_path = directory / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
        return VisionModelSpec(
            key=directory.name.removesuffix("_disease").lower(),
            path=model_path,
            class_names=_class_names(class_path),
            task=str(metadata.get("task", "classify")),
            details_path=(directory / "disease_details.json") if (directory / "disease_details.json").exists() else None,
        )
