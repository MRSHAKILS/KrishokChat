"""Build the soil moisture dataset release package for KrishokChat.

Produces (from the frozen source project on E:\CSE498R):
  dataset_release/soil_moisture/            — canonical release folder
    ├── image_manifest.csv / split_assignment.csv / dataset_summary.json
    ├── anomalies.json / series_map.json / exif_metadata.json
    ├── reports/PHASE0_AUDIT_REPORT.md / preprocessing_report.md
    ├── model_status.json                    — honest, frozen model benchmark table
    ├── README.md                            — dataset card (already written by hand)
    ├── samples_manifest.json                — 12 stratified samples → display copy
    └── thumbnails/                          — 12 sample JPEGs (≈600px long edge)

And the frontend display copy (what the UI actually serves):
  frontend/public/assets/soil_samples/       — preview_grid.jpg + thumbnails

Sampling strategy: 2 images per soil type (6 types × 2 = 12), spread across the
kPa range so the grid visually spans wet → dry. Pure, deterministic, frozen.

Usage:
  .venv\\Scripts\\python.exe scripts\\build_soil_release.py [--source <dir>]
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = Path(r"E:\CSE498R\Soil Moisture Detection\dataset")

SOIL_TYPES = ["Doash", "Atel", "Bele_Doash", "Atel_Doash", "Poli", "Bele"]
SAMPLE_PER_TYPE = 2
THUMB_EDGE = 600
GRID_COLS = 3
GRID_CELL = 220


def pick_samples(manifest: list[dict]) -> list[dict]:
    """Deterministic stratified pick: 2 per soil type, spread over kPa."""
    samples: list[dict] = []
    for soil in SOIL_TYPES:
        rows = [r for r in manifest if r["soil_type"] == soil]
        # Spread across the kPa range: sort by kpa, take even indices.
        rows.sort(key=lambda r: float(r["kpa_raw"]))
        step = max(1, len(rows) // SAMPLE_PER_TYPE)
        picked = [rows[i * step] for i in range(SAMPLE_PER_TYPE) if i * step < len(rows)]
        # Fall back if the type is small (Bele=32) and indices collide.
        while len(picked) < SAMPLE_PER_TYPE and len(rows) > len(picked):
            picked.append(rows[len(picked) - 1])
        samples.extend(picked)
    return samples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    args = parser.parse_args()

    src = Path(args.source)
    pre = src / "preprocessed"
    correct = src / "updated_dataset" / "correct_image"
    reports = src / "reports"

    release = PROJECT_ROOT / "dataset_release" / "soil_moisture"
    thumbs = release / "thumbnails"
    reports_out = release / "reports"
    display = PROJECT_ROOT / "frontend" / "public" / "assets" / "soil_samples"
    for d in (release, thumbs, reports_out, display):
        d.mkdir(parents=True, exist_ok=True)

    # 1. Frozen artifacts — copy verbatim.
    for name in [
        "image_manifest.csv",
        "split_assignment.csv",
        "dataset_summary.json",
        "anomalies.json",
        "series_map.json",
        "exif_metadata.json",
    ]:
        shutil.copy2(pre / name, release / name)
    for name in ["PHASE0_AUDIT_REPORT.md", "preprocessing_report.md"]:
        shutil.copy2(reports / name, reports_out / name)

    # 2. model_status.json — the honest, frozen benchmark table.
    model_status = {
        "status": "in_development",
        "releaseable": False,
        "note": "All regression models underperform the mean predictor (negative R^2). "
        "The dataset is the released asset; the model stays locked until a validated "
        "artifact exists (target: positive R^2 on the held-out series).",
        "baseline": {"strategy": "predict_mean", "rmse_kpa": 4.60, "r2": 0.0},
        "models": [
            {"model": "RandomForest (MobileNet features)", "rmse_kpa": 4.7633, "r2": -1.138, "params": "best_hyperparams_grid"},
            {"model": "XGBoost (MobileNet features)", "rmse_kpa": 4.8289, "r2": -1.198, "params": "best_hyperparams_grid"},
            {"model": "Ensemble (5 CNNs, weighted)", "rmse_kpa": 5.0766, "r2": -1.429, "params": "ensemble_weights_grid"},
            {"model": "CNN-Small (tuned)", "rmse_kpa": 5.1597, "r2": -1.509, "params": "cnn_small_2026-07-10"},
            {"model": "ResNet-18 (tuned)", "rmse_kpa": 5.2145, "r2": -1.563, "params": "resnet18_2026-07-10"},
            {"model": "EfficientNet-B0 (tuned)", "rmse_kpa": 5.4730, "r2": -1.822, "params": "efficientnet_b0_2026-07-10"},
            {"model": "MobileNet-V3-Large (tuned)", "rmse_kpa": 5.4880, "r2": -1.836, "params": "mobilenet_v3_2026-07-10"},
            {"model": "DenseNet-121 (tuned)", "rmse_kpa": 5.6140, "r2": -1.973, "params": "densenet121_2026-07-10"},
        ],
        "source": "kaggle output/soild_moisture_experiments_frozen_fixed.ipynb (2026-07-11)",
    }
    (release / "model_status.json").write_text(
        json.dumps(model_status, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3. Stratified sample thumbnails + preview grid.
    manifest = [
        {k: (r[k] if k in r else "") for k in
         ["image_id", "filename", "kpa_raw", "kpa_bin", "soil_type", "land_type", "crop", "growth_stage"]}
        for r in __import__("csv").DictReader((pre / "image_manifest.csv").open(encoding="utf-8-sig"))
    ]
    samples = pick_samples(manifest)
    samples_manifest = []
    grid = Image.new("RGB", (GRID_COLS * GRID_CELL, (len(samples) // GRID_COLS) * GRID_CELL), "#f2ebdc")
    draw = ImageDraw.Draw(grid)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = font_small = ImageFont.load_default()

    for i, row in enumerate(samples):
        img_path = correct / row["filename"]
        if not img_path.exists():
            print(f"  ! missing {img_path} — skipping")
            continue
        with Image.open(img_path) as im:
            im = im.convert("RGB")
            # Center-crop to square per the orientation note, then scale.
            w, h = im.size
            side = min(w, h)
            im = im.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
            im.thumbnail((THUMB_EDGE, THUMB_EDGE))
            thumb_name = f"{row['image_id']}_{row['soil_type']}_{row['kpa_raw']}kpa.jpg"
            thumb_path = thumbs / thumb_name
            im.save(thumb_path, "JPEG", quality=82)
            im.save(display / thumb_name, "JPEG", quality=82)

            col = i % GRID_COLS
            r = i // GRID_COLS
            x, y = col * GRID_CELL, r * GRID_CELL
            cell = im.copy()
            cell.thumbnail((GRID_CELL - 16, GRID_CELL - 44))
            grid.paste(cell, (x + 8, y + 8))
            label = f"{row['soil_type']} · {row['kpa_raw']} kPa"
            draw.text((x + 10, y + GRID_CELL - 34), label, fill="#1a1611", font=font_small)
            draw.text((x + 10, y + GRID_CELL - 16), row["crop"], fill="#5b5146", font=font_small)

            samples_manifest.append(
                {
                    "image_id": row["image_id"],
                    "filename": thumb_name,
                    "soil_type": row["soil_type"],
                    "kpa": float(row["kpa_raw"]),
                    "kpa_bin": row["kpa_bin"],
                    "land_type": row["land_type"],
                    "crop": row["crop"],
                    "growth_stage": row["growth_stage"],
                }
            )

    grid_path = release / "preview_grid.jpg"
    grid.save(grid_path, "JPEG", quality=85)
    shutil.copy2(grid_path, display / "preview_grid.jpg")
    (release / "samples_manifest.json").write_text(
        json.dumps({"count": len(samples_manifest), "samples": samples_manifest}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Release written to {release}")
    print(f"  artifacts: 6 frozen files + 2 reports + model_status.json")
    print(f"  samples:   {len(samples_manifest)} thumbnails + preview_grid.jpg")
    print(f"  display:   {display}")


if __name__ == "__main__":
    main()