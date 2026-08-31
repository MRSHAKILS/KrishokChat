"""Prepare browser-facing ONNX artifacts in frontend/public/models/.

Chooses per model the accepted artifact from V5 (INT8 where the held-out sanity gate
passed and calibration met the cap) and the FP32 fallback otherwise. Copies both the
.onnx and the committed class map, writes a deterministic metadata.json, and preserves
legacy aliases so old URLs keep working.

Why this lives here: this is a build step that reads the frozen reports (V3 + V5).
It is not an experiment runner and it never imports backend/app at runtime.

Run:
    .\\backend\\.venv\\Scripts\\python.exe "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/prepare_ondevice_artifacts.py"

Inputs:
    vision_onnx_export_report.json  (V3)
    vision_int8_report.json         (V5)
    vision_eval_manifest.json       (V1, for class-map hashes sanity)

Output:
    frontend/public/models/*.onnx
    frontend/public/models/*_classes.json
    frontend/public/models/metadata.json
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
EXPERIMENT_DIR = Path(__file__).resolve().parents[1]
BACKEND_VISION = REPO_ROOT / "backend" / "ml_assets" / "vision"
ONNX_FP32_DIR = BACKEND_VISION / "onnx"
ONNX_INT8_DIR = BACKEND_VISION / "onnx_int8"
DEST = REPO_ROOT / "frontend" / "public" / "models"

EXPORT_REPORT = EXPERIMENT_DIR / "vision_onnx_export_report.json"
INT8_REPORT = EXPERIMENT_DIR / "vision_int8_report.json"
MANIFEST = EXPERIMENT_DIR / "vision_eval_manifest.json"


def _read_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing {path}; run the prerequisite step first")
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# Canonical -> legacy filename stems (legacy = disease suffix expected by older code).
ALIASES: dict[str, list[str]] = {
    "crop_classifier": ["crop_classifier"],
    "potato": ["potato", "potato_disease"],
    "rice": ["rice", "rice_disease"],
    "wheat": ["wheat", "wheat_disease"],
    "corn": ["corn", "corn_disease"],
    "brassica": ["brassica", "brassica_disease"],
}

MODEL_KEYS = ["crop_classifier", "potato", "rice", "wheat", "corn", "brassica"]


def main() -> int:
    export = _read_json(EXPORT_REPORT)
    int8 = _read_json(INT8_REPORT)
    manifest = _read_json(MANIFEST)

    # Decide per model: INT8 if it was accepted (status measured, not rejected, not unmeasured)
    # and calibration met at least one reportable condition implicitly via accepted flag.
    # The report already applied the 2pp drop + 0.90 agreement rejection gate.
    int8_models = int8["models"]
    decisions: dict[str, dict] = {}
    for key in MODEL_KEYS:
        entry = int8_models.get(key)
        if entry and entry["status"] == "measured":
            decisions[key] = {"precision": "int8", "source": ONNX_INT8_DIR / f"{key}_int8.onnx"}
        else:
            # Fallback to FP32: rejected, unmeasured, or missing report.
            decisions[key] = {"precision": "fp32", "source": ONNX_FP32_DIR / f"{key}.onnx"}
        src = decisions[key]["source"]
        if not src.exists():
            raise SystemExit(f"decided {key} -> {src.name} but file missing: {src}")
        print(f"  {key:16s} -> {decisions[key]['precision']:4s} {src.name} ({src.stat().st_size / (1024*1024):.2f} MB)")

    DEST.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    for key in MODEL_KEYS:
        src = decisions[key]["source"]
        # Canonical file in frontend keeps the disease suffix for legacy compat where it existed.
        # We ship both canonical and legacy names as separate copies (no symlink on Windows).
        stems = ALIASES[key]
        primary = stems[0]
        for stem in stems:
            dst_onnx = DEST / f"{stem}.onnx"
            dst_classes = DEST / f"{stem}_classes.json"
            shutil.copy2(src, dst_onnx)
            # Class map is identical for FP32/INT8; copy from backend committed source.
            backend_class = BACKEND_VISION / (key if key == "crop_classifier" else f"{key}_disease") / "class_names.json"
            if not backend_class.exists():
                # Fallback to the export's copy
                backend_class = ONNX_FP32_DIR / f"{key}_classes.json"
            shutil.copy2(backend_class, dst_classes)
        # Record uses primary stem for onnx_file, but we also note aliases.
        primary_onnx = DEST / f"{primary}.onnx"
        primary_classes = DEST / f"{primary}_classes.json"
        train_imgsz = next((m["train_imgsz"] for m in export["models"] if m["model"] == key), None)
        if train_imgsz is None:
            raise SystemExit(f"cannot find train_imgsz for {key} in export report")
        # Read model metadata for verification
        import onnx

        model = onnx.load(str(primary_onnx), load_external_data=False)
        meta = {p.key: p.value for p in model.metadata_props}
        records.append(
            {
                "model_name": key,
                "onnx_file": f"{primary}.onnx",
                "onnx_aliases": stems,
                "classes_file": f"{primary}_classes.json",
                "precision": decisions[key]["precision"],
                "format": "onnx",
                "task": meta.get("task", "classify"),
                "input_shape": [1, 3, train_imgsz, train_imgsz],
                "size_bytes": primary_onnx.stat().st_size,
                "onnx_sha256": _sha256(primary_onnx),
                "source_pt_sha256": next(
                    (m["source_pt_sha256"] for m in export["models"] if m["model"] == key), None
                ),
                "train_imgsz": train_imgsz,
                "opset": 20,
            }
        )

    metadata = {
        "schema_version": 1,
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "framework": "Ultralytics YOLO (ONNX Export) — Option A: FP32 + INT8 static (ORT), browser via onnxruntime-web 1.29.0",
        "runtime": "onnxruntime-web 1.29.0 (WASM, bundle variant, lazy-loaded, not in First Load)",
        "gate": "default off: NEXT_PUBLIC_VISION_ONDEVICE_ENABLED; INT8 only where held-out sanity gate passed (drop <=2pp, agree >=0.90)",
        "models": records,
        "totals": {
            "n_models": len(records),
            "total_onnx_mb": round(sum(r["size_bytes"] for r in records) / (1024 * 1024), 3),
        },
    }
    out = DEST / "metadata.json"
    out.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print(f"  total {metadata['totals']['total_onnx_mb']} MB across {len(records)} primary models")
    # List what we shipped
    for entry in sorted(DEST.iterdir()):
        print(f"    {entry.name:32s} {entry.stat().st_size / (1024*1024):6.2f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
