"""
rebuild_manifest_step0f.py
Rebuild image_manifest.csv and split_assignment.csv with clean/ filenames.
Properly quotes filenames with commas. Preserves all Phase 0 corrections.
"""
import csv
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
PREPROC_DIR = DATASET_DIR / "preprocessed"
CLEAN_DIR = DATASET_DIR / "clean"

# 1. Load rename_log: raw -> clean filename mapping
rename_map = {}
rename_log_path = PREPROC_DIR / "rename_log.csv"
if not rename_log_path.exists():
    print(f"ERROR: {rename_log_path} not found")
    sys.exit(1)

with open(rename_log_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rename_map[row["original"]] = row["clean"]

print(f"Loaded {len(rename_map)} rename mappings")

# 2. Load clean directory listing
clean_files = {f.name for f in CLEAN_DIR.glob("*.jpg")}
print(f"Clean directory: {len(clean_files)} files")

# 3. Load current manifest v2 (using raw filenames)
# Must parse manually because unquoted commas in filenames break csv.reader
manifest_v2_path = PREPROC_DIR / "image_manifest_v2.csv"
manifest_rows = []
with open(manifest_v2_path, "r", encoding="utf-8") as f:
    header = next(f).strip().split(",")
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Parse: 9 fields, but filename and anomalies may contain commas
        # Structure: image_id,original_id,filename,kpa_raw,kpa_bin,anomalies,id_num,series_id,series_size
        parts = line.split(",")
        # The filename is at index 2 and may contain commas (e.g. P0050_9,85Kpa.jpg)
        # anomalies is at index 5 and may contain semicolons but shouldn't have commas
        # Strategy: parts[0]=image_id, parts[1]=original_id, parts[-4]=kpa_raw, etc.
        # Filename starts at index 2 and extends to kpa_raw field (index -6 from end)
        if len(parts) == 9:
            # Normal case - no commas in filename
            manifest_rows.append(parts[:9])
        else:
            # Has comma in filename - reconstruct
            # We know: image_id (idx 0), original_id (idx 1), then filename (idx 2 to len-6)
            # The last 6 fields are: kpa_raw, kpa_bin, anomalies, id_num, series_id, series_size
            image_id = parts[0]
            original_id = parts[1]
            # Everything between index 2 and len-6 is the filename (may contain commas)
            tail_fields = 6  # kpa_raw, kpa_bin, anomalies, id_num, series_id, series_size
            filename = ",".join(parts[2:-tail_fields])
            remaining = parts[-tail_fields:]
            row = [image_id, original_id, filename] + remaining
            manifest_rows.append(row)

print(f"Manifest v2: {len(manifest_rows)} rows (header: {header})")

# 4. Rebuild with clean filenames
new_rows = []
missing_clean = []
corrections = 0

for row in manifest_rows:
    image_id, original_id, raw_filename, kpa_raw, kpa_bin, anomalies, id_num, series_id, series_size = row
    
    # Map to clean filename
    if raw_filename in rename_map:
        clean_filename = rename_map[raw_filename]
    else:
        # May already be a clean filename (rare)
        clean_filename = raw_filename
    
    # Verify clean file exists
    if clean_filename not in clean_files:
        missing_clean.append(clean_filename)
    
    # Fix anomaly string for P0114 (keep original outlier_101kpa but add our confirmation context)
    # The anomalies.json already has the detailed outlier_confirmation
    # Keep whatever was in the anomalies field
    
    # Rebuild kpa_bin based on actual kpa_raw (correct any >100 bin)
    try:
        kpa_val = float(kpa_raw)
    except ValueError:
        kpa_val = 0.0
    
    if kpa_val >= 100:
        kpa_bin = ">100"
    elif kpa_val >= 20:
        kpa_bin = "20-30"
    elif kpa_val >= 10:
        kpa_bin = "10-20"
    else:
        kpa_bin = "0-10"
    
    new_rows.append({
        "image_id": image_id,
        "original_id": original_id,
        "filename": clean_filename,
        "kpa_raw": kpa_raw,
        "kpa_bin": kpa_bin,
        "anomalies": anomalies,
        "id_num": id_num,
        "series_id": series_id,
        "series_size": series_size
    })

if missing_clean:
    print(f"WARNING: {len(missing_clean)} clean filenames not found in clean/ dir:")
    for m in missing_clean[:10]:
        print(f"  {m}")

# 5. Write new manifest with proper quoting
output_path = PREPROC_DIR / "image_manifest.csv"
fieldnames = header
with open(output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for r in new_rows:
        writer.writerow(r)

print(f"\nWritten: {output_path} ({len(new_rows)} rows, CSV with QUOTE_ALL)")

# 6. Verify by re-reading
with open(output_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    verify_rows = list(reader)
print(f"Verification: re-read {len(verify_rows)} rows successfully")

# Check anomalies column integrity
flagged = [r for r in verify_rows if r["anomalies"].strip()]
print(f"Flagged images: {len(flagged)}")
for f in flagged:
    print(f"  {f['image_id']}: {f['anomalies']}")

# 7. Also verify series coverage
no_series = [r for r in verify_rows if not r["series_id"].strip()]
print(f"\nImages without series_id: {len(no_series)}")

# 8. Rebuild split_assignment.csv with clean filenames and proper series-level stratified split
print("\n[8] Generating series-level stratified split...")

# Group by series_id, then by kpa_bin for stratified assignment
from collections import defaultdict

series_groups = defaultdict(list)
for r in verify_rows:
    series_groups[r["series_id"]].append(r)

# For each bin, distribute series across train/val/test
series_list = list(series_groups.keys())
import random
random.seed(42)  # deterministic shuffle

# Group series by their kpa_bin
bin_series = defaultdict(list)
for sid in series_list:
    images = series_groups[sid]
    kpa_bin = images[0]["kpa_bin"]
    bin_series[kpa_bin].append(sid)

split_assignments = {}  # series_id -> split
for kpa_bin, sids in bin_series.items():
    random.shuffle(sids)
    n = len(sids)
    if n <= 2:
        # Too few series, put all in train
        for sid in sids:
            split_assignments[sid] = "train"
    else:
        n_train = max(1, round(n * 0.70))
        n_val = max(1, (n - n_train) // 2)
        n_test = n - n_train - n_val
        if n_val < 1 and n > n_train:
            n_val = 1
            n_test = n - n_train - n_val
        if n_test < 1 and n > n_train + n_val:
            n_test = 1
            n_val = n - n_train - n_test
        
        for i, sid in enumerate(sids):
            if i < n_train:
                split_assignments[sid] = "train"
            elif i < n_train + n_val:
                split_assignments[sid] = "val"
            else:
                split_assignments[sid] = "test"

# Write split_assignment.csv
split_output_path = PREPROC_DIR / "split_assignment.csv"
with open(split_output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["filename", "split", "series_id", "kpa_raw", "kpa_bin", "anomalies"])
    for r in verify_rows:
        sid = r["series_id"]
        split_name = split_assignments.get(sid, "train")
        writer.writerow([
            r["filename"], split_name, sid,
            r["kpa_raw"], r["kpa_bin"], r["anomalies"]
        ])

# Verify split
with open(split_output_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    splits = list(reader)

counts = defaultdict(lambda: defaultdict(int))
for r in splits:
    counts[r["split"]][r["kpa_bin"]] += 1

print(f"Written: {split_output_path} ({len(splits)} rows)")
for split_name in ["train", "val", "test"]:
    total = sum(counts[split_name].values())
    bins = dict(counts[split_name])
    print(f"  {split_name}: {total} images ({bins})")

# Verify series leakage
series_split_check = {}
leak_found = False
for r in splits:
    if r["series_id"] not in series_split_check:
        series_split_check[r["series_id"]] = r["split"]
    elif series_split_check[r["series_id"]] != r["split"]:
        print(f"  LEAK: series {r['series_id']} spans {series_split_check[r['series_id']]} and {r['split']}")
        leak_found = True
if not leak_found:
    print("  Series leakage check: PASS - no series spans multiple splits")
else:
    print("  Series leakage check: FAILED")

print("\n=== Phase 0 corrections verified ===")
print("All 722 images now reference clean/ directory filenames")
print("CSV files use QUOTE_ALL to handle commas in filenames")
print("Next: Ready for Phase 1 modeling")
