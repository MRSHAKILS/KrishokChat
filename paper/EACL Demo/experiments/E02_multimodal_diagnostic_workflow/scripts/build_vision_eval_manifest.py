"""V1 - build the labelled vision evaluation manifest. No inference happens here.

Walks the committed labelled image trees and emits one row per image with its
ground-truth label, the disease model that owns that label, the expected
crop-classifier label, image dimensions, and file SHA-256.

Design decisions that matter for honesty (see ``state/TASK_VISION_ONNX.md`` V1):

* Folder names are asserted against each model's ``class_names.json`` verbatim.
  A mismatch is a hard failure, never a fuzzy match.
* ``corn_disease`` has zero local labelled images, so corn accuracy is emitted as
  ``unmeasured`` and no downstream table may show a corn number.
* The crop classifier has no Rice class. Rice rows are marked
  ``crop_label_in_space: false`` so a crop-level accuracy number can state its
  6-label space instead of hiding rice as a model error.
* Crops with no disease model (Tomato, Chili, Eggplant, Gourd, Guava) are the
  correct ``NO_DISEASE_MODEL`` negative set and are flagged as such.

Run:
    .\\backend\\.venv\\Scripts\\python.exe "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/build_vision_eval_manifest.py"
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image

from _vision_common import (  # noqa: E402
    CROP_PREFIX_MAP,
    DISEASE_MODEL_KEYS,
    EXPERIMENT_DIR,
    IMAGE_SUFFIXES,
    REPO_ROOT,
    TEST_IMAGES,
    class_names,
    checkpoint_imgsz,
    model_dir,
    provenance,
    sha256_of,
    write_json,
)

OUTPUT = EXPERIMENT_DIR / "vision_eval_manifest.json"


def _relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT)).replace("\\", "/")


def _image_rows(root: Path, *, split: str) -> list[dict[str, Any]]:
    """One row per image under ``root``, label taken from the immediate parent folder."""
    rows: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        try:
            with Image.open(path) as handle:
                width, height = handle.size
                mode = handle.mode
        except OSError as exc:
            rows.append(
                {
                    "path": _relative(path),
                    "split": split,
                    "status": "unreadable",
                    "reason": str(exc),
                }
            )
            continue
        rows.append(
            {
                "path": _relative(path),
                "split": split,
                "label": path.parent.name,
                "width": width,
                "height": height,
                "mode": mode,
                "bytes": path.stat().st_size,
                "sha256": sha256_of(path),
            }
        )
    return rows


def _assert_labels_match(model_key: str, folder_labels: set[str]) -> None:
    """Fail loudly on any label the model does not actually predict."""
    known = set(class_names(model_key))
    unknown = folder_labels - known
    if unknown:
        raise SystemExit(
            f"{model_key}: folder labels not present in class_names.json: {sorted(unknown)}\n"
            f"  model classes: {sorted(known)}\n"
            "  Fix the folder names or the class map. Do not fuzzy-match."
        )


def build() -> dict[str, Any]:
    wheat_root = TEST_IMAGES / "wheat_disease"
    library_root = TEST_IMAGES / "full_library"
    if not wheat_root.is_dir() or not library_root.is_dir():
        raise SystemExit(f"Missing labelled image trees under {TEST_IMAGES}")

    # --- wheat: 11 folders matching the wheat model's 11 classes exactly ---
    wheat_rows = _image_rows(wheat_root, split="wheat_disease")
    wheat_labels = {row["label"] for row in wheat_rows if "label" in row}
    _assert_labels_match("wheat", wheat_labels)
    for row in wheat_rows:
        if "label" not in row:
            continue
        row["disease_model"] = "wheat"
        row["crop_family"] = "Wheat"
        row["expected_crop_label"] = "Wheat"
        row["crop_label_in_space"] = True

    # --- full_library: Crop__Disease folders across 9 crop families ---
    library_rows = _image_rows(library_root, split="full_library")
    unmapped: set[str] = set()
    per_model_labels: dict[str, set[str]] = {}
    for row in library_rows:
        if "label" not in row:
            continue
        label = row["label"]
        prefix = label.split("__", 1)[0]
        if prefix not in CROP_PREFIX_MAP:
            unmapped.add(prefix)
            continue
        model_key, crop_label = CROP_PREFIX_MAP[prefix]
        row["crop_family"] = prefix
        row["disease_model"] = model_key
        row["expected_crop_label"] = crop_label
        row["crop_label_in_space"] = crop_label is not None
        row["has_disease_model"] = model_key is not None
        if model_key is None:
            # Correct NO_DISEASE_MODEL outcome, not an error to be scored.
            row["expected_vision_status"] = "no_disease_model"
        else:
            per_model_labels.setdefault(model_key, set()).add(label)
    if unmapped:
        raise SystemExit(f"full_library folders with unmapped crop prefix: {sorted(unmapped)}")
    for model_key, labels in per_model_labels.items():
        _assert_labels_match(model_key, labels)

    # --- smoke folders: unlabelled single images, explicitly excluded from scoring ---
    smoke_rows: list[dict[str, Any]] = []
    for name in ("crop_classifier", "potato_disease", "rice_disease", "brassica_disease"):
        root = TEST_IMAGES / name
        if not root.is_dir():
            continue
        for path in sorted(root.iterdir()):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            with Image.open(path) as handle:
                width, height = handle.size
            smoke_rows.append(
                {
                    "path": _relative(path),
                    "split": "smoke",
                    "folder": name,
                    "label": None,
                    "scored": False,
                    "reason": "smoke image: folder name is a model name, not a ground-truth class",
                    "width": width,
                    "height": height,
                    "bytes": path.stat().st_size,
                    "sha256": sha256_of(path),
                }
            )

    scored_rows = [row for row in wheat_rows + library_rows if row.get("label")]

    # --- per-model coverage, including the unmeasurable case ---
    coverage: dict[str, Any] = {}
    for model_key in DISEASE_MODEL_KEYS:
        rows = [row for row in scored_rows if row.get("disease_model") == model_key]
        model_classes = class_names(model_key)
        if not rows:
            coverage[model_key] = {
                "status": "unmeasured",
                "reason": "no local labelled test images",
                "n_classes": len(model_classes),
                "classes": list(model_classes),
                "train_imgsz": checkpoint_imgsz(model_key),
                "n_images": 0,
            }
            continue
        per_class: dict[str, int] = {}
        for row in rows:
            per_class[row["label"]] = per_class.get(row["label"], 0) + 1
        missing = [name for name in model_classes if name not in per_class]
        coverage[model_key] = {
            "status": "measurable",
            "n_classes": len(model_classes),
            "n_images": len(rows),
            "train_imgsz": checkpoint_imgsz(model_key),
            "images_per_class": {name: per_class.get(name, 0) for name in model_classes},
            "classes_with_no_images": missing,
            "min_images_per_covered_class": min(per_class.values()),
            "calibration_note": (
                "ultralytics recommends >300 images for INT8 calibration; "
                f"this model has {len(rows)} labelled images in total"
            ),
        }

    no_model_rows = [row for row in scored_rows if row.get("has_disease_model") is False]
    no_model_families: dict[str, int] = {}
    for row in no_model_rows:
        family = row["crop_family"]
        no_model_families[family] = no_model_families.get(family, 0) + 1

    crop_space_counts: dict[str, int] = {}
    out_of_space = 0
    for row in scored_rows:
        label = row.get("expected_crop_label")
        if label is None:
            out_of_space += 1
        else:
            crop_space_counts[label] = crop_space_counts.get(label, 0) + 1

    payload: dict[str, Any] = {
        "layer": "E02_multimodal_diagnostic_workflow",
        "artifact": "vision_eval_manifest",
        "schema_version": 1,
        "provenance": provenance(Path(__file__)),
        "source_roots": {
            "wheat_disease": _relative(wheat_root),
            "full_library": _relative(library_root),
        },
        "model_artifacts": {
            key: {
                "model_pt": _relative(model_dir(key) / "model.pt"),
                "model_pt_sha256": sha256_of(model_dir(key) / "model.pt"),
                "class_names_sha256": sha256_of(model_dir(key) / "class_names.json"),
                "train_imgsz": checkpoint_imgsz(key),
                "n_classes": len(class_names(key)),
            }
            for key in ("crop_classifier",) + DISEASE_MODEL_KEYS
        },
        "totals": {
            "scored_images": len(scored_rows),
            "wheat_split_images": len([row for row in wheat_rows if row.get("label")]),
            "full_library_images": len([row for row in library_rows if row.get("label")]),
            "smoke_images_excluded": len(smoke_rows),
            "unreadable_images": len([row for row in wheat_rows + library_rows if row.get("status") == "unreadable"]),
        },
        "crop_classifier_label_space": {
            "labels": list(class_names("crop_classifier")),
            "note": (
                "No Rice class exists. vision_pipeline.py:158-165 documents the live-verified "
                "consequence: rice leaves classify as Wheat, and routing mitigates by also running "
                "the rice disease model. Rice is an out-of-label-space case, not a model error."
            ),
            "images_per_expected_label": crop_space_counts,
            "images_outside_label_space": out_of_space,
        },
        "disease_model_coverage": coverage,
        "no_disease_model_set": {
            "note": "correct NO_DISEASE_MODEL outcome; must not be scored as a disease error",
            "n_images": len(no_model_rows),
            "families": no_model_families,
        },
        "corroborating_artifact": {
            "path": _relative(TEST_IMAGES / "test_matrix_results.json"),
            "sha256": sha256_of(TEST_IMAGES / "test_matrix_results.json"),
            "trust": "corroboration only; the paper's number must come from a fresh run",
        },
        "images": scored_rows,
        "smoke_images": smoke_rows,
    }
    return payload


def main() -> int:
    payload = build()
    write_json(OUTPUT, payload)
    totals = payload["totals"]
    print(f"wrote {OUTPUT}")
    print(f"  scored images      : {totals['scored_images']}")
    print(f"  wheat split        : {totals['wheat_split_images']}")
    print(f"  full_library       : {totals['full_library_images']}")
    print(f"  smoke (excluded)   : {totals['smoke_images_excluded']}")
    for key, entry in payload["disease_model_coverage"].items():
        if entry["status"] == "measurable":
            print(
                f"  {key:9s} measurable n={entry['n_images']:<4d} "
                f"classes={entry['n_classes']} imgsz={entry['train_imgsz']} "
                f"missing={len(entry['classes_with_no_images'])}"
            )
        else:
            print(f"  {key:9s} UNMEASURED  ({entry['reason']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
