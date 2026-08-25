"""R10 — Offline ONNX model export for on-device mobile classification.

Converts the verified PyTorch classification models:
  - backend/ml_assets/vision/crop_classifier/model.pt
  - backend/ml_assets/vision/potato_disease/model.pt

Into optimized ONNX models in frontend/public/models/ with class maps and metadata.

Invariants:
  - Classification only (task: classify) — never claims detection boxes.
  - Offline script only, never in request path.
  - Deterministic export metadata with SHA-256 digests.
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ultralytics import YOLO

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.ingestion.contract import sha256_of, write_deterministic_json

logger = logging.getLogger("krishokchat.vision_export")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VISION_DIR = PROJECT_ROOT / "ml_assets" / "vision"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "models"


def export_model(
    model_dir: Path,
    output_dir: Path,
    model_name: str,
    imgsz: int = 224,
) -> dict[str, Any]:
    """Export a single PyTorch classification model to ONNX."""
    pt_path = model_dir / "model.pt"
    classes_path = model_dir / "class_names.json"

    if not pt_path.exists():
        raise FileNotFoundError(f"Model file not found: {pt_path}")
    if not classes_path.exists():
        raise FileNotFoundError(f"Class names file not found: {classes_path}")

    pt_sha = sha256_of(pt_path)
    print(f"Exporting {model_name} from {pt_path} (sha256: {pt_sha[:12]}…)...")

    model = YOLO(str(pt_path))
    exported_path_str = model.export(format="onnx", imgsz=imgsz, dynamic=False, simplify=True)
    exported_path = Path(exported_path_str)

    target_onnx = output_dir / f"{model_name}.onnx"
    target_classes = output_dir / f"{model_name}_classes.json"

    shutil.copy2(exported_path, target_onnx)
    shutil.copy2(classes_path, target_classes)

    onnx_sha = sha256_of(target_onnx)
    size_bytes = target_onnx.stat().st_size

    print(f"  Successfully exported to {target_onnx.name} ({size_bytes / (1024 * 1024):.2f} MB, sha256: {onnx_sha[:12]}…)")

    return {
        "model_name": model_name,
        "format": "onnx",
        "task": "classify",
        "input_shape": [1, 3, imgsz, imgsz],
        "size_bytes": size_bytes,
        "source_pt_sha256": pt_sha,
        "onnx_sha256": onnx_sha,
        "onnx_file": target_onnx.name,
        "classes_file": target_classes.name,
    }


def export_all(vision_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Export crop classifier and potato disease classifier."""
    output_dir.mkdir(parents=True, exist_ok=True)

    models_to_export = [
        ("crop_classifier", vision_dir / "crop_classifier"),
        ("potato_disease", vision_dir / "potato_disease"),
    ]

    records: list[dict[str, Any]] = []
    for name, path in models_to_export:
        record = export_model(path, output_dir, name)
        records.append(record)

    now_iso = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    metadata_payload = {
        "schema_version": 1,
        "exported_at": now_iso,
        "framework": "Ultralytics YOLO (ONNX Export)",
        "models": records,
    }

    metadata_path = output_dir / "metadata.json"
    write_deterministic_json(metadata_path, metadata_payload)
    print(f"Wrote model metadata to {metadata_path}")

    return metadata_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vision-dir", type=Path, default=DEFAULT_VISION_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    try:
        export_all(args.vision_dir, args.output_dir)
        return 0
    except Exception as exc:
        print(f"Error during on-device model export: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
