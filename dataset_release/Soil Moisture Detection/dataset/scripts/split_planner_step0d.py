"""
Step 0d: Train/Val/Test Split Planner
======================================
Generates leakage-aware split assignments.

Run from: dataset/scripts/
Input:    dataset/preprocessed/image_manifest.csv, series_map.json
Output:   dataset/preprocessed/split_assignment.csv
"""

import csv
import json
import random
from pathlib import Path
from collections import Counter, defaultdict

# ── Path Configuration ─────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
PREPROCESSED_DIR = DATASET_DIR / "preprocessed"
MANIFEST_PATH = PREPROCESSED_DIR / "image_manifest.csv"
SERIES_MAP_PATH = PREPROCESSED_DIR / "series_map.json"
OUTPUT_PATH = PREPROCESSED_DIR / "split_assignment.csv"

# Split ratios
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
RANDOM_SEED = 42


def load_data():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    series_map = {}
    if SERIES_MAP_PATH.exists():
        with open(SERIES_MAP_PATH, "r", encoding="utf-8") as f:
            for s in json.load(f):
                for fname in s["filenames"]:
                    series_map[fname] = s["series_id"]
    return records, series_map


def assign_splits(records, series_map):
    random.seed(RANDOM_SEED)
    groups = defaultdict(list)
    for rec in records:
        sid = series_map.get(rec["filename"], f"singleton_{rec['filename']}")
        groups[sid].append(rec)

    group_list = list(groups.items())
    random.shuffle(group_list)

    total = len(records)
    train_target = int(total * TRAIN_RATIO)
    val_target = int(total * VAL_RATIO)

    splits = {"train": [], "val": [], "test": []}
    counts = {"train": 0, "val": 0, "test": 0}

    for gid, grecs in group_list:
        gsize = len(grecs)
        if counts["train"] < train_target:
            chosen = "train"
        elif counts["val"] < val_target:
            chosen = "val"
        else:
            chosen = "test"
        if chosen == "train" and counts["train"] + gsize > train_target * 1.2:
            chosen = "val" if counts["val"] < val_target else "test"
        splits[chosen].extend(grecs)
        counts[chosen] += gsize

    return splits


def main():
    if not MANIFEST_PATH.exists():
        print(f"ERROR: {MANIFEST_PATH} not found. Run Step 0a first.")
        return

    records, series_map = load_data()
    print(f"Loaded {len(records)} images, {len(set(series_map.values()))} series")

    splits = assign_splits(records, series_map)

    output_rows = []
    for split_name in ["train", "val", "test"]:
        for rec in splits[split_name]:
            output_rows.append({
                "filename": rec["filename"],
                "split": split_name,
                "series_id": series_map.get(rec["filename"], ""),
                "kpa_raw": rec["kpa_raw"],
                "kpa_bin": rec["kpa_bin"],
                "anomalies": rec.get("anomalies", ""),
            })

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "filename", "split", "series_id", "kpa_raw", "kpa_bin", "anomalies"
        ])
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nSTEP 0d COMPLETE")
    for sn in ["train", "val", "test"]:
        cnt = len(splits[sn])
        pct = cnt / len(records) * 100
        print(f"  {sn.upper():>5}: {cnt:>4} ({pct:>5.1f}%)")

    # Leakage check
    leaked = set()
    for sid in set(series_map.values()):
        sfiles = [r for r in output_rows if r["series_id"] == sid]
        if len(set(r["split"] for r in sfiles)) > 1:
            leaked.add(sid)
    print(f"  Leakage: {'PASS' if not leaked else f'FAIL ({len(leaked)} series)'}")
    print(f"  Output:  {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
