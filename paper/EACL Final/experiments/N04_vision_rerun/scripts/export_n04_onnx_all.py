"""V3 - deterministic FP32 ONNX export for all six classification models.

Fixes the two real defects in ``backend/scripts/export_vision_ondevice.py``:

1. It hardcodes ``imgsz=224``. Older checkpoints trained rice at 320 and corn and
   brassica at 256. Exporting those at 224 produces a model that runs but is quietly less
   accurate than the ``.pt`` it came from. Here ``imgsz`` is read per model from the
   checkpoint's ``train_args`` and the exported graph's input shape is asserted against it.
   (Current 2026-09-17 checkpoints: all 224 except brassica/corn at 256; rice is 224 with
   10 classes — the old 320/8-class rice checkpoint no longer exists on disk.)
2. It exports only two of the six models.

Output location decision (recorded in the report, per ``TASK_VISION_ONNX.md`` V3):
FP32 exports are written to ``backend/ml_assets/vision/onnx/`` - a build-artifact location
adjacent to the ``.pt`` sources. ``frontend/public/models/`` is left untouched by this
script; the browser-facing copy and its ``metadata.json`` are regenerated wholesale in V6
once the artifacts to ship (FP32 or INT8) have been accepted on measured evidence. This
avoids the failure mode of a ``metadata.json`` describing files that no longer exist.

Re-exporting produces different bytes than the 2026-08-25 files even with identical
settings (nondeterministic graph node ordering), which is exactly why the existing two are
not overwritten in place.

Run:
    .\\backend\\.venv\\Scripts\\python.exe "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/export_vision_onnx_all.py"

Flags:
    --models a,b,c   export a subset (default: all six)
    --opset N        pin the ONNX opset (default: ultralytics' own choice, recorded either way)
"""

from __future__ import annotations

import argparse
import ast
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _vision_common import (  # noqa: E402
    DISEASE_MODEL_KEYS,
    EXPERIMENT_DIR,
    REPO_ROOT,
    VISION_DIR,
    checkpoint_imgsz,
    class_names,
    model_dir,
    provenance,
    sha256_of,
    write_json,
)

ALL_MODELS = ("crop_classifier",) + DISEASE_MODEL_KEYS
ONNX_DIR = VISION_DIR / "onnx"
REPORT = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\n04_onnx_export_report_20260917.json")


def _relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT)).replace("\\", "/")


def _onnx_metadata(path: Path) -> dict[str, str]:
    import onnx

    model = onnx.load(str(path), load_external_data=False)
    return {entry.key: entry.value for entry in model.metadata_props}


def _onnx_io(path: Path) -> dict[str, Any]:
    import onnx

    model = onnx.load(str(path), load_external_data=False)

    def shape_of(value) -> list[Any]:
        dims: list[Any] = []
        for dim in value.type.tensor_type.shape.dim:
            dims.append(dim.dim_value if dim.HasField("dim_value") else (dim.dim_param or "dynamic"))
        return dims

    return {
        "opset": [{"domain": entry.domain or "ai.onnx", "version": entry.version} for entry in model.opset_import],
        "producer": f"{model.producer_name} {model.producer_version}".strip(),
        "inputs": [{"name": value.name, "shape": shape_of(value)} for value in model.graph.input],
        "outputs": [{"name": value.name, "shape": shape_of(value)} for value in model.graph.output],
    }


def _embedded_names(metadata: dict[str, str]) -> tuple[str, ...] | None:
    raw = metadata.get("names")
    if not raw:
        return None
    try:
        parsed = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return None
    if isinstance(parsed, dict):
        return tuple(str(parsed[key]) for key in sorted(parsed, key=lambda item: int(item)))
    if isinstance(parsed, (list, tuple)):
        return tuple(str(item) for item in parsed)
    return None


def export_one(model_key: str, *, opset: int | None) -> dict[str, Any]:
    from ultralytics import YOLO

    source = model_dir(model_key) / "model.pt"
    if not source.exists():
        raise FileNotFoundError(source)
    imgsz = checkpoint_imgsz(model_key)
    expected_classes = class_names(model_key)

    print(f"  {model_key:16s} imgsz={imgsz} classes={len(expected_classes)} ...", end="", flush=True)

    model = YOLO(str(source))
    kwargs: dict[str, Any] = {"format": "onnx", "imgsz": imgsz, "dynamic": False, "simplify": True}
    if opset is not None:
        kwargs["opset"] = opset
    produced = Path(model.export(**kwargs))

    ONNX_DIR.mkdir(parents=True, exist_ok=True)
    target = ONNX_DIR / f"{model_key}.onnx"
    shutil.move(str(produced), target)
    shutil.copy2(model_dir(model_key) / "class_names.json", ONNX_DIR / f"{model_key}_classes.json")

    io = _onnx_io(target)
    metadata = _onnx_metadata(target)

    # Clause: the exported graph must actually accept the training resolution.
    input_shape = io["inputs"][0]["shape"]
    if list(input_shape) != [1, 3, imgsz, imgsz]:
        raise SystemExit(
            f"{model_key}: exported input shape {input_shape} != expected [1, 3, {imgsz}, {imgsz}]. "
            "Refusing to accept an export at the wrong resolution."
        )
    output_shape = io["outputs"][0]["shape"]
    if list(output_shape) != [1, len(expected_classes)]:
        raise SystemExit(f"{model_key}: exported output shape {output_shape} != [1, {len(expected_classes)}]")

    # Clause: class-name parity. crop_classifier and wheat_disease keep their names on
    # ck['ema'] rather than ck['model']; re-assert so a future re-export cannot drift.
    embedded = _embedded_names(metadata)
    if embedded is None:
        raise SystemExit(f"{model_key}: exported ONNX carries no embedded 'names' metadata")
    if embedded != expected_classes:
        raise SystemExit(
            f"{model_key}: embedded ONNX names differ from class_names.json\n"
            f"  onnx: {list(embedded)}\n  json: {list(expected_classes)}"
        )
    if metadata.get("task") != "classify":
        raise SystemExit(f"{model_key}: embedded task is {metadata.get('task')!r}, expected 'classify'")

    record = {
        "model": model_key,
        "status": "exported",
        "source_pt": _relative(source),
        "source_pt_sha256": sha256_of(source),
        "source_pt_bytes": source.stat().st_size,
        "onnx": _relative(target),
        "onnx_sha256": sha256_of(target),
        "onnx_bytes": target.stat().st_size,
        "onnx_mb": round(target.stat().st_size / (1024 * 1024), 3),
        "pt_mb": round(source.stat().st_size / (1024 * 1024), 3),
        "train_imgsz": imgsz,
        "input_shape": input_shape,
        "output_shape": output_shape,
        "opset": io["opset"],
        "producer": io["producer"],
        "task": metadata.get("task"),
        "n_classes": len(expected_classes),
        "class_names_parity": "verified against class_names.json",
        "classes_file": _relative(ONNX_DIR / f"{model_key}_classes.json"),
        "export_kwargs": {key: value for key, value in kwargs.items()},
    }
    print(f" ok {record['onnx_mb']} MB opset {io['opset'][0]['version']}")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", type=str, default=",".join(ALL_MODELS))
    parser.add_argument("--opset", type=int, default=None)
    args = parser.parse_args()

    selected = [name.strip() for name in args.models.split(",") if name.strip()]
    unknown = [name for name in selected if name not in ALL_MODELS]
    if unknown:
        raise SystemExit(f"unknown models: {unknown}; valid: {list(ALL_MODELS)}")

    print(f"exporting {len(selected)} model(s) to {ONNX_DIR}")
    records: list[dict[str, Any]] = []
    for model_key in selected:
        records.append(export_one(model_key, opset=args.opset))

    existing = REPO_ROOT / "frontend" / "public" / "models"
    payload = {
        "layer": "E02_multimodal_diagnostic_workflow",
        "artifact": "vision_onnx_export_report",
        "schema_version": 1,
        "provenance": provenance(Path(__file__)),
        "output_location": {
            "path": _relative(ONNX_DIR),
            "rationale": (
                "build-artifact location next to the .pt sources. frontend/public/models/ is not "
                "touched here; the browser-facing copy and its metadata.json are regenerated "
                "wholesale in V6 after measured evidence selects FP32 or INT8."
            ),
        },
        "pre_existing_frontend_exports": {
            "path": _relative(existing),
            "files": sorted(entry.name for entry in existing.iterdir()) if existing.is_dir() else [],
            "handling": (
                "left untouched by this script. Re-export is byte-nondeterministic even with "
                "identical settings, so these stay valid against the metadata.json that describes "
                "them until V6 replaces both together."
            ),
        },
        "precision": "FP32",
        "per_model_imgsz_note": (
            "imgsz is read from each checkpoint's train_args, not hardcoded. "
            "backend/scripts/export_vision_ondevice.py hardcodes 224, which is wrong for "
            "rice (320), corn (256) and brassica (256)."
        ),
        "totals": {
            "n_exported": len(records),
            "total_onnx_mb": round(sum(record["onnx_mb"] for record in records), 3),
            "total_pt_mb": round(sum(record["pt_mb"] for record in records), 3),
        },
        "models": records,
    }
    write_json(REPORT, payload)
    print(f"wrote {REPORT}")
    print(f"  total ONNX {payload['totals']['total_onnx_mb']} MB vs .pt {payload['totals']['total_pt_mb']} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
