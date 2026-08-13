"""
Step 0b: Filename Normalization
================================
Fixes filename anomalies and creates clean_images/ with normalized names.

Run from: dataset/scripts/
Input:    dataset/raw/
Output:   dataset/clean/
"""

import os
import re
import csv
import shutil
from pathlib import Path

# ── Path Configuration ─────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
RAW_DIR = DATASET_DIR / "raw"
CLEAN_DIR = DATASET_DIR / "clean"
LOG_PATH = DATASET_DIR / "preprocessed" / "rename_log.csv"

# Duplicate handling
DUP_SUFFIXES = ["", "b", "c", "d"]
DUP_IDS = {"P0176": 2, "P0187": 2, "P0342": 2, "P0677": 2}

# Outlier files to flag
OUTLIER_FILES = {"P0114_101Kpa.jpg"}


def normalize_pressure_string(raw_str: str) -> str:
    """Normalize pressure portion of filename."""
    normalized = raw_str.replace(",", ".")
    if normalized == "985":
        normalized = "9.85"
    normalized = normalized.replace("Kp.", "Kpa.").replace("Kp.jpg", "Kpa.jpg")
    match = re.search(r"([\d.]+)", normalized)
    if match:
        try:
            val = float(match.group(1))
            before = normalized[:match.start()]
            after = normalized[match.end():]
            return f"{before}{val:.1f}{after}"
        except ValueError:
            pass
    return normalized


def build_clean_name(original: str, dup_counter: dict) -> str:
    """Build a clean, normalized filename."""
    parts = original.split("_", 1)
    image_id = parts[0]
    dup_counter[image_id] = dup_counter.get(image_id, 0) + 1
    suffix_idx = dup_counter[image_id] - 1
    if suffix_idx < len(DUP_SUFFIXES) and image_id in DUP_IDS:
        clean_id = f"{image_id}{DUP_SUFFIXES[suffix_idx]}" if suffix_idx > 0 else image_id
    else:
        clean_id = image_id

    if len(parts) > 1:
        kpa_part = normalize_pressure_string(parts[1])
    else:
        kpa_part = "unknown.jpg"
    return f"{clean_id}_{kpa_part}"


def main():
    CLEAN_DIR.mkdir(exist_ok=True)

    files = sorted([
        f for f in os.listdir(RAW_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    print(f"Processing {len(files)} images from {RAW_DIR}")

    rename_log = []
    flagged = []
    dup_counter = {}

    for fname in files:
        src = RAW_DIR / fname
        clean_name = build_clean_name(fname, dup_counter)

        if fname in OUTLIER_FILES:
            clean_name = f"_FLAGGED_{clean_name}"
            flagged.append(fname)

        dst = CLEAN_DIR / clean_name
        shutil.copy2(src, dst)

        rename_log.append({
            "original": fname,
            "clean": clean_name,
            "changed": fname != clean_name,
            "flagged": fname in OUTLIER_FILES,
        })

    # Write log
    LOG_PATH.parent.mkdir(exist_ok=True)
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["original", "clean", "changed", "flagged"])
        writer.writeheader()
        writer.writerows(rename_log)

    changed = [r for r in rename_log if r["changed"]]
    print(f"\nSTEP 0b COMPLETE")
    print(f"  Copied:      {len(rename_log)} images")
    print(f"  Renamed:     {len(changed)}")
    print(f"  Flagged:     {len(flagged)}")
    print(f"  Output:      {CLEAN_DIR}")
    print(f"  Log:         {LOG_PATH}")


if __name__ == "__main__":
    main()
