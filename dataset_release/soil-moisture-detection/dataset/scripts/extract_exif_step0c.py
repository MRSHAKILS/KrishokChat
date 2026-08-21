"""
Step 0c: EXIF Metadata Extraction
===================================
Extracts image dimensions and EXIF data from clean images.

Run from: dataset/scripts/
Input:    dataset/clean/
Output:   dataset/preprocessed/exif_metadata.json
"""

import os
import json
from pathlib import Path
from PIL import Image

# ── Path Configuration ─────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
CLEAN_DIR = DATASET_DIR / "clean"
OUTPUT_PATH = DATASET_DIR / "preprocessed" / "exif_metadata.json"


def get_exif_data(image_path: Path) -> dict:
    """Extract EXIF data from an image file."""
    try:
        img = Image.open(image_path)
    except Exception as e:
        return {"error": str(e)}

    data = {
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "mode": img.mode,
        "file_size_bytes": os.path.getsize(image_path),
    }

    info = img._getexif()
    if info is None:
        data["has_exif"] = False
        return data

    data["has_exif"] = True
    from PIL.ExifTags import TAGS
    for tag_id, value in info.items():
        tag_name = TAGS.get(tag_id, str(tag_id))
        if isinstance(value, bytes):
            try:
                value = value.decode("utf-8", errors="replace")
            except Exception:
                value = str(value)
        elif isinstance(value, tuple):
            value = str(value)
        data[tag_name] = value

    return data


def main():
    if not CLEAN_DIR.exists():
        print(f"ERROR: {CLEAN_DIR} not found. Run Step 0b first.")
        return

    files = sorted([
        f for f in os.listdir(CLEAN_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    print(f"Extracting metadata from {len(files)} images in {CLEAN_DIR}")

    results = {}
    errors = []
    exif_count = 0

    for i, fname in enumerate(files, 1):
        data = get_exif_data(CLEAN_DIR / fname)
        if "error" in data:
            errors.append({"filename": fname, "error": data["error"]})
        elif data.get("has_exif"):
            exif_count += 1
        results[fname] = data
        if i % 100 == 0:
            print(f"  Processed {i}/{len(files)}...")

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    print(f"\nSTEP 0c COMPLETE")
    print(f"  Total:       {len(files)}")
    print(f"  With EXIF:   {exif_count}")
    print(f"  Errors:      {len(errors)}")
    print(f"  Output:      {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
