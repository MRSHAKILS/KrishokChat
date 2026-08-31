"""Shared plumbing for the real E02 vision measurement runners.

Every runner in this folder must record enough provenance that a reviewer can tell
*which* artifacts produced *which* number on *which* machine. That logic lives here so
the individual runners cannot drift apart.

Hard rules inherited from ``paper/EACL Demo/state/STATE.md`` and ``AGENTS.md`` rule 5:

* No result constants. Anything that cannot be measured is emitted as
  ``{"status": "unmeasured", "reason": ...}``.
* Repo root is resolved from ``__file__``; never hardcoded.
* Vision artifacts are ``task: classify``. Nothing here produces or implies boxes.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

# scripts/ -> E02_.../ -> experiments/ -> EACL Demo/ -> paper/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[5]
BACKEND = REPO_ROOT / "backend"
VISION_DIR = BACKEND / "ml_assets" / "vision"
TEST_IMAGES = VISION_DIR / "test_images"
EXPERIMENT_DIR = Path(__file__).resolve().parents[1]

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# The six crop-classifier labels. There is deliberately no Rice class: the classifier
# was trained without one, and vision_pipeline.py compensates at routing time.
CROP_CLASSIFIER_LABELS = ("Brassica", "Corn", "GourdGuava", "Potato", "Solanacea", "Wheat")

# full_library folder prefix -> (disease model key or None, crop-classifier label or None)
# None model key means "no disease model exists for this crop" - the correct
# NO_DISEASE_MODEL negative set, not a model error.
# None crop label means "outside the classifier's 6-label space".
CROP_PREFIX_MAP: dict[str, tuple[str | None, str | None]] = {
    "Potato": ("potato", "Potato"),
    "Rice": ("rice", None),
    "Cabbage": ("brassica", "Brassica"),
    "Cauliflower": ("brassica", "Brassica"),
    "Tomato": (None, "Solanacea"),
    "Chili": (None, "Solanacea"),
    "Eggplant": (None, "Solanacea"),
    "Gourd": (None, "GourdGuava"),
    "Guava": (None, "GourdGuava"),
}


def ensure_backend_importable() -> None:
    """Make ``app.*`` importable. Backend code only resolves with backend/ on sys.path."""
    path = str(BACKEND)
    if path not in sys.path:
        sys.path.insert(0, path)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_head() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:  # pragma: no cover
        return f"unavailable: {exc}"


def library_versions() -> dict[str, str]:
    versions: dict[str, str] = {"python": sys.version.split()[0]}
    for name in ("torch", "torchvision", "ultralytics", "onnx", "onnxruntime", "numpy", "PIL"):
        try:
            module = __import__(name)
        except ImportError:
            versions[name] = "not installed"
            continue
        versions[name] = str(getattr(module, "__version__", "unknown"))
    return versions


def machine_info() -> dict[str, Any]:
    info: dict[str, Any] = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "cpu_count_logical": os.cpu_count(),
    }
    try:
        import psutil

        info["cpu_count_physical"] = psutil.cpu_count(logical=False)
        info["total_ram_bytes"] = psutil.virtual_memory().total
    except ImportError:  # pragma: no cover
        info["cpu_count_physical"] = None
    try:
        import torch

        info["cuda_available"] = bool(torch.cuda.is_available())
    except ImportError:  # pragma: no cover
        info["cuda_available"] = None
    try:
        import onnxruntime as ort

        info["onnxruntime_providers"] = list(ort.get_available_providers())
    except ImportError:  # pragma: no cover
        info["onnxruntime_providers"] = None
    return info


def provenance(script: Path, *, inputs: dict[str, Path] | None = None) -> dict[str, Any]:
    """Provenance block every result JSON must carry."""
    payload: dict[str, Any] = {
        "script": str(script.resolve().relative_to(REPO_ROOT)).replace("\\", "/"),
        "run_at_utc": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        "git_head": git_head(),
        "repo_root": str(REPO_ROOT),
        "library_versions": library_versions(),
        "machine": machine_info(),
    }
    if inputs:
        payload["input_sha256"] = {
            name: (sha256_of(path) if path.exists() else "missing") for name, path in sorted(inputs.items())
        }
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def class_names(model_key: str) -> tuple[str, ...]:
    """Class labels for a model directory, read from the committed class map."""
    directory = VISION_DIR / (model_key if model_key == "crop_classifier" else f"{model_key}_disease")
    data = json.loads((directory / "class_names.json").read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return tuple(str(data[str(index)]) for index in range(len(data)))
    return tuple(str(item) for item in data)


def model_dir(model_key: str) -> Path:
    return VISION_DIR / (model_key if model_key == "crop_classifier" else f"{model_key}_disease")


def checkpoint_imgsz(model_key: str) -> int:
    """Training ``imgsz`` recorded in the checkpoint.

    Exporting or preprocessing at any other size silently degrades accuracy, so this is
    read from the artifact rather than assumed. crop_classifier and wheat_disease carry
    ``ck['model'] is None`` and keep their weights on ``ck['ema']``; ``train_args`` is
    present on all six regardless.
    """
    import torch

    path = model_dir(model_key) / "model.pt"
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    train_args = checkpoint.get("train_args") or {}
    size = train_args.get("imgsz")
    if not isinstance(size, int):
        raise ValueError(f"{path} has no integer train_args.imgsz (got {size!r})")
    return size


DISEASE_MODEL_KEYS = ("potato", "rice", "wheat", "corn", "brassica")


def percentiles(values: Iterable[float]) -> dict[str, float | None]:
    """Latency summary. Returns None fields rather than inventing values for n < 2."""
    data = sorted(float(value) for value in values)
    if not data:
        return {key: None for key in ("n", "mean_ms", "stdev_ms", "p50_ms", "p90_ms", "p95_ms", "p99_ms", "min_ms", "max_ms")}

    def quantile(fraction: float) -> float:
        if len(data) == 1:
            return data[0]
        position = fraction * (len(data) - 1)
        low = int(position)
        high = min(low + 1, len(data) - 1)
        return data[low] + (data[high] - data[low]) * (position - low)

    return {
        "n": len(data),
        "mean_ms": round(statistics.fmean(data), 4),
        "stdev_ms": round(statistics.stdev(data), 4) if len(data) > 1 else None,
        "p50_ms": round(quantile(0.50), 4),
        "p90_ms": round(quantile(0.90), 4),
        "p95_ms": round(quantile(0.95), 4),
        "p99_ms": round(quantile(0.99), 4),
        "min_ms": round(data[0], 4),
        "max_ms": round(data[-1], 4),
    }


def preprocess_numpy(image, imgsz: int):
    """Ultralytics classification inference preprocessing, reproduced exactly.

    ``ultralytics.data.augment.classify_transforms`` is
    ``Resize(imgsz, bilinear, antialias) -> CenterCrop(imgsz) -> ToTensor() ->
    Normalize(mean=0, std=1)``, i.e. plain ``/255`` with no mean/std shift and **no
    letterbox**. Getting this wrong makes ONNX-vs-PyTorch parity look broken for reasons
    that have nothing to do with ONNX, so it is derived from the installed library
    transform rather than reimplemented by hand.

    Returns a contiguous ``float32`` NCHW array of shape ``(1, 3, imgsz, imgsz)``.
    """
    import numpy as np
    from ultralytics.data.augment import classify_transforms

    transform = classify_transforms(imgsz)
    tensor = transform(image.convert("RGB"))
    array = tensor.unsqueeze(0).numpy().astype(np.float32)
    return np.ascontiguousarray(array)


def softmax(logits):
    import numpy as np

    shifted = np.asarray(logits, dtype=np.float64) - np.max(logits)
    exponentiated = np.exp(shifted)
    return exponentiated / exponentiated.sum()
