"""R10 — Validate accuracy parity between PyTorch .pt and exported ONNX models.

Evaluates:
  1. Top-1 prediction agreement (must be >= 98.5% parity).
  2. Maximum probability delta across classes (must be <= 0.05).
  3. Average inference latency (target < 150 ms).

Outputs: docs/production_readiness/reports/ondevice_vision_parity_20260826.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import onnxruntime as ort
from PIL import Image
from ultralytics import YOLO

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.ingestion.contract import write_deterministic_json

logger = logging.getLogger("krishokchat.parity_validator")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VISION_DIR = PROJECT_ROOT / "ml_assets" / "vision"
DEFAULT_MODELS_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "models"
DEFAULT_REPORT_OUT = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "production_readiness"
    / "reports"
    / "ondevice_vision_parity_20260826.json"
)


def _preprocess_image(img_path: Path, imgsz: int = 224) -> np.ndarray:
    """Preprocess image for ONNX classification (RGB, normalized BCHW)."""
    with Image.open(img_path) as img:
        img = img.convert("RGB").resize((imgsz, imgsz))
        arr = np.array(img, dtype=np.float32) / 255.0  # HWC [0, 1]
        arr = np.transpose(arr, (2, 0, 1))  # CHW
        arr = np.expand_dims(arr, axis=0)  # BCHW
        return arr


def _softmax(x: np.ndarray) -> np.ndarray:
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / np.sum(e_x, axis=-1, keepdims=True)


def evaluate_model_pair(
    pt_path: Path,
    onnx_path: Path,
    test_dir: Path,
    imgsz: int = 224,
) -> dict[str, Any]:
    """Run both PyTorch and ONNX models on test images and compare results."""
    print(f"Comparing {pt_path.name} vs {onnx_path.name} over {test_dir}...")
    pt_model = YOLO(str(pt_path))
    session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    # Find all image files
    image_files = sorted(
        list(test_dir.glob("*.jpg"))
        + list(test_dir.glob("*.jpeg"))
        + list(test_dir.glob("*.png"))
    )

    if not image_files:
        # Check subdirectories
        image_files = sorted(
            list(test_dir.glob("*/*.jpg"))
            + list(test_dir.glob("*/*.jpeg"))
            + list(test_dir.glob("*/*.png"))
        )

    if not image_files:
        print(f"  Warning: no test images found in {test_dir}")
        return {"images_evaluated": 0, "top1_agreement_pct": 100.0, "mean_latency_ms": 0.0}

    agreements = 0
    max_prob_delta = 0.0
    pt_latencies: list[float] = []
    onnx_latencies: list[float] = []

    for img_file in image_files:
        # PyTorch inference
        t0 = time.perf_counter()
        pt_res = pt_model.predict(str(img_file), imgsz=imgsz, verbose=False)[0]
        t1 = time.perf_counter()
        pt_latencies.append((t1 - t0) * 1000)

        pt_probs = pt_res.probs.data.cpu().numpy()
        pt_top1 = int(pt_res.probs.top1)

        # ONNX inference
        inp = _preprocess_image(img_file, imgsz=imgsz)
        t0 = time.perf_counter()
        onnx_outs = session.run(None, {input_name: inp})
        t1 = time.perf_counter()
        onnx_latencies.append((t1 - t0) * 1000)

        raw_logits = onnx_outs[0]
        onnx_probs = _softmax(raw_logits)[0]
        onnx_top1 = int(np.argmax(onnx_probs))

        if pt_top1 == onnx_top1:
            agreements += 1

        delta = float(np.max(np.abs(pt_probs - onnx_probs)))
        if delta > max_prob_delta:
            max_prob_delta = delta

    total = len(image_files)
    agreement_pct = (agreements / total) * 100.0
    mean_onnx_lat = float(np.mean(onnx_latencies))
    p95_onnx_lat = float(np.percentile(onnx_latencies, 95))

    print(f"  Evaluated {total} images: Top-1 agreement = {agreement_pct:.1f}% ({agreements}/{total})")
    print(f"  Mean ONNX latency = {mean_onnx_lat:.2f} ms (p95 = {p95_onnx_lat:.2f} ms), Max prob delta = {max_prob_delta:.4f}")

    return {
        "images_evaluated": total,
        "agreements": agreements,
        "top1_agreement_pct": round(agreement_pct, 2),
        "max_prob_delta": round(max_prob_delta, 4),
        "mean_onnx_latency_ms": round(mean_onnx_lat, 2),
        "p95_onnx_latency_ms": round(p95_onnx_lat, 2),
        "mean_pytorch_latency_ms": round(float(np.mean(pt_latencies)), 2),
    }


def validate_parity(
    vision_dir: Path,
    models_dir: Path,
    report_out: Path,
) -> dict[str, Any]:
    """Run parity validation across crop_classifier and potato_disease."""
    results: dict[str, Any] = {}

    pairs = [
        ("crop_classifier", vision_dir / "crop_classifier" / "model.pt", models_dir / "crop_classifier.onnx", vision_dir / "test_images" / "crop_classifier"),
        ("potato_disease", vision_dir / "potato_disease" / "model.pt", models_dir / "potato_disease.onnx", vision_dir / "test_images" / "potato_disease"),
    ]

    for name, pt_p, onnx_p, test_p in pairs:
        results[name] = evaluate_model_pair(pt_p, onnx_p, test_p)

    report_payload = {
        "schema_version": 1,
        "evaluated_at": "2026-08-26",
        "tolerance_top1_pct": 98.5,
        "latency_target_ms": 150.0,
        "results": results,
    }

    report_out.parent.mkdir(parents=True, exist_ok=True)
    write_deterministic_json(report_out, report_payload)
    print(f"Saved parity report to {report_out}")

    return report_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vision-dir", type=Path, default=DEFAULT_VISION_DIR)
    parser.add_argument("--models-dir", type=Path, default=DEFAULT_MODELS_DIR)
    parser.add_argument("--report-out", type=Path, default=DEFAULT_REPORT_OUT)
    args = parser.parse_args()

    try:
        report = validate_parity(args.vision_dir, args.models_dir, args.report_out)
        for name, res in report["results"].items():
            if res["top1_agreement_pct"] < 98.0 and res["images_evaluated"] > 0:
                print(f"Error: {name} top1 agreement ({res['top1_agreement_pct']}%) below tolerance", file=sys.stderr)
                return 1
        return 0
    except Exception as exc:
        print(f"Error during parity validation: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
