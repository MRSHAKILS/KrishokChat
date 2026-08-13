"""
preprocess_resize_step2e.py
Center-crop every canonical image to a square, resize to 224x224, and save
to dataset/preprocessed/images_224/. Also writes a training manifest that
EXCLUDES contaminated images (P0029 foot, P0166 hand) and a matching split.

Output:
  dataset/preprocessed/images_224/<filename>      # 224x224 squared images
  dataset/preprocessed/train_manifest.csv         # 720 rows (722 - 2 contaminated)
  dataset/preprocessed/train_split.csv            # split without contaminated IDs

Usage:
  python dataset/scripts/preprocess_resize_step2e.py
"""

from pathlib import Path
import csv
import os

import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
PREPROC_DIR = DATASET_DIR / "preprocessed"
CLEAN_DIR = DATASET_DIR / "clean"
OUT_DIR = PREPROC_DIR / "images_224"

TARGET_SIZE = 224
CONTAMINATED = {"P0029", "P0166"}  # foot, hand — exclude from training

OUT_DIR.mkdir(parents=True, exist_ok=True)


def center_crop_square(img: Image.Image) -> Image.Image:
    """Crop to the largest centered square, then resize to TARGET_SIZE."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    return img


def main():
    manifest_path = PREPROC_DIR / "image_manifest.csv"
    split_path = PREPROC_DIR / "split_assignment.csv"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = list(csv.DictReader(f))
    with open(split_path, "r", encoding="utf-8") as f:
        split_rows = list(csv.DictReader(f))
    split_map = {r["image_id"]: r["split"] for r in split_rows}

    train_manifest = []
    train_split = []
    skipped = []

    for row in manifest:
        image_id = row["image_id"]
        fn = row["filename"]
        src = CLEAN_DIR / fn

        if not src.exists():
            print(f"  WARNING: {fn} not found in clean/ — skipping")
            skipped.append(image_id)
            continue

        if image_id in CONTAMINATED:
            print(f"  EXCLUDED (contaminated): {image_id} ({fn})")
            skipped.append(image_id)
            continue

        img = Image.open(src).convert("RGB")
        sq = center_crop_square(img)
        sq.save(OUT_DIR / fn, "JPEG", quality=95)

        # Copy row into training manifest
        new_row = dict(row)
        new_row["split"] = split_map.get(image_id, "")
        train_manifest.append(new_row)
        train_split.append({"image_id": image_id,
                            "split": split_map.get(image_id, ""),
                            "series_id": row["series_id"]})

    # Write training manifest
    train_manifest_path = PREPROC_DIR / "train_manifest.csv"
    with open(train_manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(train_manifest[0].keys()))
        writer.writeheader()
        writer.writerows(train_manifest)

    # Write training split
    train_split_path = PREPROC_DIR / "train_split.csv"
    with open(train_split_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["image_id", "split", "series_id"])
        writer.writeheader()
        writer.writerows(train_split)

    # Report split counts
    from collections import Counter
    counts = Counter(r["split"] for r in train_split)
    print(f"\nDone.")
    print(f"  Preprocessed images: {len(train_manifest)} -> {OUT_DIR}")
    print(f"  Excluded: {len(skipped)} ({skipped})")
    print(f"  Train split: {dict(counts)}")
    print(f"  Wrote: {train_manifest_path.name}, {train_split_path.name}")


if __name__ == "__main__":
    main()
