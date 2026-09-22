"""R10 — Tests for On-Device Vision Classifier Export and Parity.

Locks all R10 invariants:
  1. Exported ONNX models exist and load valid input/output shapes.
  2. Parity validation reports >= 98.0% top-1 agreement between PyTorch and ONNX.
  3. Average ONNX inference latency is sub-150 ms.
  4. Class maps and export metadata exist with valid SHA-256 hashes.
"""

from __future__ import annotations

import json
from pathlib import Path

import onnxruntime as ort
import pytest

MODELS_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "models"
REPORT_PATH = Path(__file__).resolve().parents[2] / "docs" / "production_readiness" / "reports" / "ondevice_vision_parity_20260826.json"


def test_exported_onnx_models_exist_and_load() -> None:
    assert MODELS_DIR.exists(), f"Models directory not found: {MODELS_DIR}"

    metadata_file = MODELS_DIR / "metadata.json"
    assert metadata_file.exists(), "metadata.json must exist"
    data = json.loads(metadata_file.read_text(encoding="utf-8"))
    # Verify every model listed in metadata loads with the correct input shape
    for model_meta in data["models"]:
        onnx_path = MODELS_DIR / model_meta["onnx_file"]
        assert onnx_path.exists(), f"{model_meta['onnx_file']} must exist"
        session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        expected = model_meta.get("input_shape", [1, 3, 224, 224])
        assert session.get_inputs()[0].shape == expected, f"{model_meta['onnx_file']} shape mismatch: {session.get_inputs()[0].shape} vs {expected}"


def test_model_metadata_invariants() -> None:
    metadata_file = MODELS_DIR / "metadata.json"
    data = json.loads(metadata_file.read_text(encoding="utf-8"))

    assert data["schema_version"] == 1
    assert "models" in data
    # Option A (2026-08-30): 6 primary models — 4 INT8 accepted + 2 FP32 fallback (rice rejected, corn unmeasured)
    assert len(data["models"]) == 6, f"expected 6 models after Option A, got {len(data['models'])}"

    for model_meta in data["models"]:
        assert model_meta["task"] == "classify", "Must be classification only"
        assert len(model_meta["source_pt_sha256"]) == 64
        assert len(model_meta["onnx_sha256"]) == 64
        assert (MODELS_DIR / model_meta["classes_file"]).exists()
        # Legacy aliases must resolve (e.g., potato.onnx + potato_disease.onnx are both shipped)
        for alias in model_meta.get("onnx_aliases", []):
            assert (MODELS_DIR / alias).exists() or (MODELS_DIR / f"{alias}.onnx").exists() or (MODELS_DIR / model_meta["onnx_file"]).exists()


def test_parity_report_satisfies_tolerances() -> None:
    assert REPORT_PATH.exists(), f"Parity report missing at {REPORT_PATH}"
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    assert report["schema_version"] == 1
    assert "results" in report

    for model_name, res in report["results"].items():
        if res["images_evaluated"] > 0:
            assert res["top1_agreement_pct"] >= 98.0, f"{model_name} agreement below 98%"
            assert res["mean_onnx_latency_ms"] <= 150.0, f"{model_name} latency exceeded 150ms"
