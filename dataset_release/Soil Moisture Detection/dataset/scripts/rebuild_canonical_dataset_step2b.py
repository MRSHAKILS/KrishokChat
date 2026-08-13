"""
rebuild_canonical_dataset_step2b.py
Replace our entire manifest with the canonical data from:
  - correct_image/ (722 corrected images)
  - TraceData.xlsx (full metadata including soil_type, crop, dates)

This is THE canonical dataset. All previous raw/clean analysis was pre-correction.
"""
import csv, json, shutil, sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import time

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl required")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
RAW_DIR = DATASET_DIR / "raw"
CLEAN_DIR = DATASET_DIR / "clean"
PREPROC_DIR = DATASET_DIR / "preprocessed"
UPDATED_DIR = DATASET_DIR / "updated_dataset"
CORRECT_DIR = UPDATED_DIR / "correct_image"

print("=" * 60)
print("REBUILDING CANONICAL DATASET FROM correct_image/ + TraceData.xlsx")
print("=" * 60)

# ============================================================
# 1. Load TraceData metadata
# ============================================================
xlsx_path = UPDATED_DIR / "TraceData.xlsx"
wb = openpyxl.load_workbook(xlsx_path)
ws = wb["Sheet1"]
headers = [cell.value for cell in ws[1]]

trace_data = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    id_val, fname, kpa, land_type, soil_type, rain_date, rain_time, crop, growth_stage, date_val, time_val, loc = row
    if fname is None:
        continue
    fname = str(fname).strip()
    trace_data[fname] = {
        "image_id": str(id_val).strip() if id_val else "",
        "kpa": str(kpa) if kpa is not None else "",
        "land_type": str(land_type).strip() if land_type else "",
        "soil_type": str(soil_type).strip() if soil_type else "",
        "rain_date": str(rain_date).strip() if rain_date else "",
        "rain_time": str(rain_time).strip() if rain_time else "",
        "crop": str(crop).strip() if crop else "",
        "growth_stage": str(growth_stage).strip() if growth_stage else "",
        "date": str(date_val).strip() if date_val else "",
        "time": str(time_val).strip() if time_val else "",
        "location": str(loc).strip() if loc else "",
    }

print(f"\nTraceData entries: {len(trace_data)}")

# ============================================================
# 2. Load correct_image files
# ============================================================
correct_images = {}
for f in CORRECT_DIR.glob("*.jpg"):
    correct_images[f.name] = f

print(f"correct_image files: {len(correct_images)}")

# ============================================================
# 3. Match and merge
# ============================================================
# Strategy: correct_image filenames match TraceData FILE_NAME exactly
matched = []
unmatched_images = []
unmatched_metadata = []

for fname, fpath in sorted(correct_images.items()):
    meta = trace_data.get(fname, {})
    
    # Parse kPa from filename
    import re
    kpa_match = re.search(r'(\d+\.?\d*)Kpa', fname)
    kpa_from_file = float(kpa_match.group(1)) if kpa_match else 0.0
    
    # Use kPa from metadata if available (more reliable)
    kpa_str = meta.get("kpa", "")
    try:
        kpa_val = float(kpa_str) if kpa_str else kpa_from_file
    except ValueError:
        kpa_val = kpa_from_file
    
    # Determine kPa bin
    if kpa_val >= 100:
        kpa_bin = ">100"
    elif kpa_val >= 20:
        kpa_bin = "20-30"
    elif kpa_val >= 10:
        kpa_bin = "10-20"
    else:
        kpa_bin = "0-10"
    
    # Extract image ID
    id_match = re.match(r'P(\d+)', fname)
    id_num = int(id_match.group(1)) if id_match else 0
    image_id = f"P{id_num:04d}" if id_match else fname.replace(".jpg", "")
    
    # Build record
    record = {
        "image_id": image_id,
        "filename": fname,
        "kpa_raw": str(kpa_val),
        "kpa_bin": kpa_bin,
        "land_type": meta.get("land_type", ""),
        "soil_type": meta.get("soil_type", ""),
        "crop": meta.get("crop", ""),
        "growth_stage": meta.get("growth_stage", ""),
        "rain_date": meta.get("rain_date", ""),
        "rain_time": meta.get("rain_time", ""),
        "capture_date": meta.get("date", ""),
        "capture_time": meta.get("time", ""),
        "location": meta.get("location", ""),
        "file_size": fpath.stat().st_size,
    }
    
    if meta:
        matched.append(record)
    else:
        unmatched_metadata.append(record)
        matched.append(record)  # Still include, just with missing metadata

print(f"Matched with metadata: {len(matched) - len(unmatched_metadata)}")
print(f"Unmatched metadata: {len(unmatched_metadata)}")
if unmatched_metadata:
    for r in unmatched_metadata[:5]:
        print(f"  {r['filename']}")

# ============================================================
# 4. Compute stats
# ============================================================
print(f"\n{'='*60}")
print("CANONICAL DATASET STATISTICS")
print(f"{'='*60}")

# kPa distribution
kpa_vals = [float(r["kpa_raw"]) for r in matched]
print(f"\nkPa range: {min(kpa_vals):.1f} - {max(kpa_vals):.1f}")
print(f"Mean: {sum(kpa_vals)/len(kpa_vals):.2f}")
print(f"Median: {sorted(kpa_vals)[len(kpa_vals)//2]:.2f}")

kpa_bins = Counter(r["kpa_bin"] for r in matched)
print(f"\nkPa bin distribution:")
for b in ["0-10", "10-20", "20-30", ">100"]:
    print(f"  {b}: {kpa_bins.get(b, 0)}")

# Soil type x kPa bin
print(f"\nSOIL_TYPE x kPa BIN:")
soil_bins = defaultdict(lambda: defaultdict(int))
for r in matched:
    st = r["soil_type"] or "UNKNOWN"
    kb = r["kpa_bin"]
    soil_bins[st][kb] += 1

soil_types = sorted(soil_bins.keys())
header = f"{'SOIL_TYPE':<20s}" + "".join(f"{b:>8s}" for b in ["0-10","10-20","20-30",">100"]) + f"{'TOTAL':>8s}"
print(header)
print("-" * len(header))
for st in sorted(soil_types):
    total = sum(soil_bins[st][b] for b in ["0-10","10-20","20-30",">100"])
    vals = [str(soil_bins[st][b]) for b in ["0-10","10-20","20-30",">100"]]
    print(f"{st:<20s}" + "".join(f"{v:>8s}" for v in vals) + f"{total:>8d}")

# New vs old kPa comparison (if old manifest exists)
old_manifest_path = PREPROC_DIR / "image_manifest.csv"
kpa_changes = []
if old_manifest_path.exists():
    old_kpa = {}
    with open(old_manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_kpa[row["image_id"]] = float(row["kpa_raw"])
    
    for r in matched:
        oid = r["image_id"]
        new_kpa = float(r["kpa_raw"])
        old_kpa_val = old_kpa.get(oid)
        if old_kpa_val is not None and abs(new_kpa - old_kpa_val) > 0.5:
            kpa_changes.append((oid, r["filename"], old_kpa_val, new_kpa))
    
    if kpa_changes:
        print(f"\nkPa VALUE CORRECTIONS (>0.5 diff from old manifest): {len(kpa_changes)}")
        for oid, fname, old, new in kpa_changes[:15]:
            print(f"  {oid} ({fname}): {old} -> {new} kPa")
        if len(kpa_changes) > 15:
            print(f"  ... and {len(kpa_changes) - 15} more")

# ============================================================
# 5. Series assignment for canonical dataset
# ============================================================
print(f"\n{'='*60}")
print("REBUILDING SERIES ASSIGNMENTS")
print(f"{'='*60}")

# Sort by ID for consecutive detection
matched.sort(key=lambda r: int(r["image_id"].replace("P", "")))

# Detect consecutive runs with same kPa
series_list = []
current_series = []
for r in matched:
    img_id = int(r["image_id"].replace("P", ""))
    
    if not current_series:
        current_series = [r]
    else:
        prev = current_series[-1]
        prev_id = int(prev["image_id"].replace("P", ""))
        prev_kpa = float(prev["kpa_raw"])
        curr_kpa = float(r["kpa_raw"])
        
        # Same series if consecutive ID AND similar kPa (within 1.0)
        if img_id == prev_id + 1 and abs(curr_kpa - prev_kpa) <= 1.0:
            current_series.append(r)
        else:
            # Finalize current series
            if len(current_series) >= 2:
                series_list.append(current_series)
            else:
                series_list.append(current_series)  # singletons too
            current_series = [r]

if current_series:
    series_list.append(current_series)

# Assign series IDs
new_series_map = []
for i, series in enumerate(series_list):
    sid = f"S{i+1:04d}"
    ids = [int(r["image_id"].replace("P", "")) for r in series]
    for r in series:
        r["series_id"] = sid
        r["series_size"] = len(series)

print(f"Total series: {len(series_list)}")
print(f"Series sizes: min={min(len(s) for s in series_list)}, max={max(len(s) for s in series_list)}, "
      f"median={sorted(len(s) for s in series_list)[len(series_list)//2]}")

# ============================================================
# 6. Write canonical manifest
# ============================================================
fieldnames = [
    "image_id", "filename", "kpa_raw", "kpa_bin",
    "soil_type", "land_type", "crop", "growth_stage",
    "rain_date", "rain_time", "capture_date", "capture_time", "location",
    "series_id", "series_size", "file_size"
]

output_path = PREPROC_DIR / "image_manifest.csv"
with open(output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for r in matched:
        writer.writerow(r)

print(f"\nWritten: {output_path} ({len(matched)} rows)")

# ============================================================
# 7. Copy correct_image/ to clean/ (replace old clean)
# ============================================================
print(f"\n{'='*60}")
print("SYNCING correct_image/ -> clean/")
print(f"{'='*60}")

# Create clean/ with correct images (backup dirs removed — see commit history)
CLEAN_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)

copied = 0
for fname, fpath in sorted(correct_images.items()):
    # Copy to clean/
    dest_clean = CLEAN_DIR / fname
    if not dest_clean.exists():
        shutil.copy2(fpath, dest_clean)
        copied += 1
    
    # Also copy to raw/ (raw should now point to canonical too)
    dest_raw = RAW_DIR / fname
    if not dest_raw.exists():
        shutil.copy2(fpath, dest_raw)
        copied += 1

print(f"Copied: {copied} files to clean/ and raw/")

# Remove old preprocessed files that are now obsolete
obsolete = [
    PREPROC_DIR / "image_manifest.csv",
    PREPROC_DIR / "image_manifest_v3.csv",
    PREPROC_DIR / "split_assignment.csv",
    PREPROC_DIR / "_deprecated_manifest_v1.csv",
    PREPROC_DIR / "_deprecated_split_v1.csv",
    PREPROC_DIR / "rename_log.csv",
    PREPROC_DIR / "image_stats.json",
]
for f in obsolete:
    if f.exists():
        f.unlink()
        print(f"Removed obsolete: {f.name}")

print(f"\n{'='*60}")
print("CANONICAL DATASET READY")
print(f"{'='*60}")
print(f"  Images: {len(matched)}")
print(f"  Location: clean/ (copied from correct_image/)")
print(f"  Manifest: preprocessed/image_manifest.csv")
print(f"  Canonical dataset built from correct_image/")
print(f"\nNext: rebuild split_assignment and start Phase 1 baselines")
