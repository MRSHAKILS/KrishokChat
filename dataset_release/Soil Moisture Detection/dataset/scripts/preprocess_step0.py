"""
Step 0a: Parse & Validate Dataset
==================================
Scans raw images, parses kPa from filenames, detects anomalies,
generates manifest CSV, series map, and anomaly report.

Run from: dataset/scripts/
Output to: dataset/preprocessed/
"""

import os
import re
import csv
import json
from pathlib import Path
from collections import Counter

# ── Path Configuration (relative to dataset/scripts/) ──────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent          # dataset/scripts/
DATASET_DIR = SCRIPT_DIR.parent                       # dataset/
RAW_DIR = DATASET_DIR / "raw"                          # dataset/raw/
OUTPUT_DIR = DATASET_DIR / "preprocessed"              # dataset/preprocessed/

# Pressure range bins (matching metadata.xlsx dropdown)
KP_BINS = [
    (0, 10, "0-10"),
    (10, 20, "10-20"),
    (20, 30, "20-30"),
    (30, 40, "30-40"),
    (40, 50, "40-50"),
    (50, 60, "50-60"),
    (60, 70, "60-70"),
    (70, 80, "70-80"),
    (80, 90, "80-90"),
    (90, 100, "90-100"),
]

# Known duplicate IDs and their interpretation
DUPLICATE_IDS = {
    "P0176": {
        "files": ["P0176_12.5Kpa.jpg", "P0176_12.6Kpa.jpg"],
        "action": "keep_both_rename",
        "reason": "Re-measurement, 0.1 Kpa difference"
    },
    "P0187": {
        "files": ["P0187_12.8Kpa.jpg", "P0187_12Kpa.jpg"],
        "action": "keep_both_rename",
        "reason": "Re-measurement, 0.8 Kpa difference"
    },
    "P0342": {
        "files": ["P0342_10Kpa.jpg", "P0342_13Kpa.jpg"],
        "action": "keep_both_rename",
        "reason": "3 Kpa difference - treat as separate sample"
    },
    "P0677": {
        "files": ["P0677_5Kpa.jpg", "P0677_8Kpa.jpg"],
        "action": "keep_both_rename",
        "reason": "3 Kpa difference - treat as separate sample"
    }
}


def parse_pressure_from_filename(filename: str) -> float | None:
    """Parse kPa numeric value from filename."""
    parts = filename.split("_")
    if len(parts) < 2:
        return None
    match = re.search(r"([0-9.,]+)", parts[1])
    if not match:
        return None
    num_str = match.group(1).replace(",", ".")
    if num_str == "985":
        return 9.85
    try:
        return float(num_str)
    except ValueError:
        return None


def get_kpa_bin(value: float) -> str:
    """Map a kPa value to its bin label."""
    for low, high, label in KP_BINS:
        if low <= value < high:
            return label
    if value == 100:
        return "90-100"
    return f">{KP_BINS[-1][1]}"


def detect_anomalies(filename: str) -> list[str]:
    """Return list of anomaly flags for a filename."""
    flags = []
    parts = filename.split("_")
    if len(parts) < 2:
        return ["malformed_filename"]
    kpa_part = parts[1].replace(".jpg", "")
    if "," in kpa_part:
        flags.append("comma_decimal")
    if "Kp." in filename or kpa_part.endswith("Kp"):
        flags.append("truncated_unit")
    if "985Kpa" in kpa_part:
        flags.append("missing_decimal_985")
    return flags


def find_consecutive_series(files: list[str]) -> list[dict]:
    """Identify consecutive image series for leakage-aware splitting."""
    parsed = []
    for f in files:
        parts = f.split("_")
        id_str = parts[0].replace("P", "")
        try:
            img_id = int(id_str)
        except ValueError:
            continue
        pressure = parse_pressure_from_filename(f)
        if pressure is not None:
            parsed.append((img_id, round(pressure, 2), f))
    parsed.sort(key=lambda x: x[0])

    series = []
    current = {"start": None, "end": None, "pressure": None, "files": []}
    for img_id, pressure, fname in parsed:
        if current["start"] is None:
            current = {"start": img_id, "end": img_id, "pressure": pressure, "files": [fname]}
        elif img_id == current["end"] + 1 and abs(pressure - current["pressure"]) < 0.15:
            current["end"] = img_id
            current["files"].append(fname)
        else:
            if len(current["files"]) >= 5:
                series.append(current)
            current = {"start": img_id, "end": img_id, "pressure": pressure, "files": [fname]}
    if len(current["files"]) >= 5:
        series.append(current)
    return series


def process_dataset():
    """Main preprocessing pipeline."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. Scan raw images
    image_files = sorted([
        f for f in os.listdir(RAW_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    print(f"[1/7] Found {len(image_files)} images in {RAW_DIR}")

    # 2. Parse and validate
    records = []
    all_flags = []
    duplicate_counter = Counter()
    pressure_values = []

    for fname in image_files:
        parts = fname.split("_")
        raw_id = parts[0]
        image_id = raw_id
        duplicate_counter[raw_id] += 1
        if duplicate_counter[raw_id] > 1:
            image_id = f"{raw_id}_{duplicate_counter[raw_id]}"

        pressure = parse_pressure_from_filename(fname)
        flags = detect_anomalies(fname)
        if pressure is None:
            flags.append("unparseable_pressure")
        if pressure == 101.0:
            flags.append("outlier_101kpa")

        id_num_str = raw_id.replace("P", "")
        try:
            id_num = int(id_num_str)
        except ValueError:
            id_num = None

        kpa_bin = get_kpa_bin(pressure) if pressure is not None else "unknown"
        if pressure is not None:
            pressure_values.append(pressure)

        record = {
            "image_id": image_id,
            "original_id": raw_id,
            "filename": fname,
            "kpa_raw": round(pressure, 4) if pressure is not None else None,
            "kpa_bin": kpa_bin,
            "anomalies": "|".join(flags) if flags else "",
            "id_num": id_num,
        }
        records.append(record)
        if flags:
            all_flags.append((fname, flags))

    print(f"[2/7] Parsed {len(records)} records, {len(all_flags)} with anomalies")

    # 3. Find missing IDs
    all_id_nums = [r["id_num"] for r in records if r["id_num"] is not None]
    missing_ids = []
    if all_id_nums:
        expected = set(range(min(all_id_nums), max(all_id_nums) + 1))
        missing_ids = sorted(expected - set(all_id_nums))
    print(f"[3/7] Missing IDs in sequence: {len(missing_ids)}")

    # 4. Find consecutive series
    series = find_consecutive_series(image_files)
    series_lookup = {}
    for s in series:
        for f in s["files"]:
            series_lookup[f] = s["start"]
    print(f"[4/7] Found {len(series)} consecutive series (>=5 images)")

    # 5. Add series info
    for rec in records:
        rec["series_id"] = series_lookup.get(rec["filename"], "")
        rec["series_size"] = next(
            (len(s["files"]) for s in series if rec["filename"] in s["files"]), ""
        )

    # 6. Write manifest CSV
    csv_path = OUTPUT_DIR / "image_manifest.csv"
    fieldnames = [
        "image_id", "original_id", "filename", "kpa_raw", "kpa_bin",
        "anomalies", "id_num", "series_id", "series_size"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"[5/7] Wrote manifest: {csv_path}")

    # 7. Write anomaly report
    anomaly_path = OUTPUT_DIR / "anomalies.json"
    anomaly_data = {
        "total_images": len(records),
        "total_anomalies": len(all_flags),
        "missing_ids": [f"P{m:04d}" for m in missing_ids],
        "duplicate_ids": {k: v for k, v in DUPLICATE_IDS.items()},
        "files_with_flags": [
            {"filename": fn, "flags": fl} for fn, fl in all_flags
        ],
        "outlier_files": [fn for fn, fl in all_flags if "outlier_101kpa" in fl],
        "pressure_stats": {
            "min": round(min(pressure_values), 2) if pressure_values else None,
            "max": round(max(pressure_values), 2) if pressure_values else None,
            "mean": round(sum(pressure_values) / len(pressure_values), 2) if pressure_values else None,
            "median": round(sorted(pressure_values)[len(pressure_values) // 2], 2) if pressure_values else None,
            "unique_values": len(set(pressure_values)),
        },
        "kpa_bin_distribution": dict(Counter(
            get_kpa_bin(p) for p in pressure_values
        )),
    }
    with open(anomaly_path, "w", encoding="utf-8") as f:
        json.dump(anomaly_data, f, indent=2, ensure_ascii=False)
    print(f"[6/7] Wrote anomaly report: {anomaly_path}")

    # 8. Write series mapping
    series_path = OUTPUT_DIR / "series_map.json"
    series_list = []
    for s in series:
        series_list.append({
            "series_id": f"S{s['start']:04d}",
            "id_range": f"P{s['start']:04d}-P{s['end']:04d}",
            "pressure_kpa": s["pressure"],
            "image_count": len(s["files"]),
            "filenames": s["files"],
        })
    with open(series_path, "w", encoding="utf-8") as f:
        json.dump(series_list, f, indent=2, ensure_ascii=False)
    print(f"[7/7] Wrote series map: {series_path}")

    # Summary
    print("\n" + "=" * 60)
    print("STEP 0a COMPLETE")
    print("=" * 60)
    print(f"  Images:          {len(records)}")
    print(f"  Anomalies:       {len(all_flags)}")
    print(f"  Missing IDs:     {len(missing_ids)}")
    print(f"  Duplicate IDs:   {len(DUPLICATE_IDS)} (8 files)")
    print(f"  Outlier:         {len([f for f, fl in all_flags if 'outlier_101kpa' in fl])}")
    print(f"  Series:          {len(series)}")
    print(f"\nOutputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    process_dataset()
