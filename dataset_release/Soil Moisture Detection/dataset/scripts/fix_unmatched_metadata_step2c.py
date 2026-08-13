"""
fix_unmatched_metadata_step2c.py
Investigate 8 images missing from TraceData.xlsx but present in correct_image/.
Check trace_deta_analysis.xlsx, look for nearby IDs, and rebuild series.
"""
import csv, sys
from pathlib import Path
from collections import defaultdict, Counter
try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl required")
    sys.exit(1)

DATASET_DIR = Path(__file__).resolve().parent.parent
UPDATED_DIR = DATASET_DIR / "updated_dataset"
PREPROC_DIR = DATASET_DIR / "preprocessed"

unmatched_ids = ["P0171", "P0172", "P0183", "P0184", "P0339", "P0340", "P0670", "P0671"]

print("=" * 60)
print("INVESTIGATING 8 UNMATCHED IMAGES")
print("=" * 60)

# ============================================================
# 1. Check trace_deta_analysis.xlsx for these IDs
# ============================================================
xlsx2 = UPDATED_DIR / "trace_deta_analysis.xlsx"
wb2 = openpyxl.load_workbook(xlsx2)
for sheet_name in wb2.sheetnames:
    ws = wb2[sheet_name]
    headers = [cell.value for cell in ws[1]]
    print(f"\n--- Sheet: {sheet_name} (columns: {len(headers)}) ---")
    print(f"  Headers: {headers}")
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is not None:
            rid = str(row[0]).strip()
            if rid in unmatched_ids:
                print(f"  FOUND: {dict(zip(headers, row))}")

# ============================================================
# 2. Check TraceData.xlsx for ALL P01xx, P03xx, P06xx
# ============================================================
print(f"\n{'='*60}")
print("CHECKING NEARBY IDS IN TRACEDATA.XLSX")
xlsx1 = UPDATED_DIR / "TraceData.xlsx"
wb1 = openpyxl.load_workbook(xlsx1)
ws1 = wb1["Sheet1"]
headers1 = [cell.value for cell in ws1[1]]
all_ids_trace = []
for row in ws1.iter_rows(min_row=2, values_only=True):
    if row[0] is not None:
        all_ids_trace.append(str(row[0]).strip())

# Check continuity around each unmatched ID
for uid in unmatched_ids:
    num = int(uid.replace("P", ""))
    print(f"\n{uid} (ID {num}):")
    for offset in [-3, -2, -1, 0, 1, 2, 3]:
        check_id = f"P{num+offset:04d}"
        if check_id in all_ids_trace:
            print(f"  Neighbor {check_id:>8s}: FOUND in TraceData")
        else:
            print(f"  Neighbor {check_id:>8s}: MISSING from TraceData")

# ============================================================
# 3. Load series from canonical manifest
# ============================================================
manifest_path = PREPROC_DIR / "image_manifest_canonical.csv"
with open(manifest_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

rows.sort(key=lambda r: int(r["image_id"].replace("P", "")))

# Rebuild series
series_list = []
current_series = []
for r in rows:
    img_id = int(r["image_id"].replace("P", ""))
    if not current_series:
        current_series = [r]
    else:
        prev = current_series[-1]
        prev_id = int(prev["image_id"].replace("P", ""))
        prev_kpa = float(prev["kpa_raw"])
        curr_kpa = float(r["kpa_raw"])
        if img_id == prev_id + 1 and abs(curr_kpa - prev_kpa) <= 1.0:
            current_series.append(r)
        else:
            series_list.append(current_series)
            current_series = [r]
if current_series:
    series_list.append(current_series)

# Assign series
for i, series in enumerate(series_list):
    sid = f"S{i+1:04d}"
    for r in series:
        r["series_id"] = sid
        r["series_size"] = len(series)

# ============================================================
# 4. Print series containing unmatched images
# ============================================================
print(f"\n{'='*60}")
print("SERIES CONTAINING UNMATCHED IMAGES")
for uid in unmatched_ids:
    for r in rows:
        if r["image_id"] == uid:
            sid = r.get("series_id", "?")
            print(f"\n  {uid}: Series={sid}, kpa={r['kpa_raw']}")
            # Print neighbors
            for r2 in rows:
                if r2.get("series_id") == sid:
                    st = r2["soil_type"] or "?"
                    print(f"    {r2['image_id']:>8s} kpa={r2['kpa_raw']:>5s} soil={st:<12s} crop={r2['crop'] or '?':<15s}")
            break

# ============================================================
# 5. Infer metadata from nearest matched neighbor
# ============================================================
print(f"\n{'='*60}")
print("INFERRING METADATA FROM NEAREST MATCHED NEIGHBORS")
for uid in unmatched_ids:
    num = int(uid.replace("P", ""))
    neighbors = []
    for r in rows:
        if r["image_id"] != uid and r["soil_type"]:
            rnum = int(r["image_id"].replace("P", ""))
            dist = abs(rnum - num)
            neighbors.append((dist, r))
    
    # Find nearest neighbor with metadata
    neighbors.sort()
    nearest = None
    for dist, r in neighbors[:10]:  # Top 10
        if r["soil_type"]:
            nearest = r
            break
    
    if nearest:
        print(f"\n  {uid} (kpa={float(r['kpa_raw']):.1f}):")
        print(f"    Nearest neighbor: {nearest['image_id']} (dist={nearest.get('kpa_raw','?')})")
        print(f"    Inferred soil_type: {nearest['soil_type']}")
        print(f"    Inferred land_type: {nearest['land_type']}")
        print(f"    Inferred crop: {nearest['crop']}")
        print(f"    Inferred growth_stage: {nearest['growth_stage']}")

print(f"\n{'='*60}")
print("DONE - Check trace_deta_analysis.xlsx sheets for more data")
print("If metadata not found, nearest-neighbor inference is best option")
