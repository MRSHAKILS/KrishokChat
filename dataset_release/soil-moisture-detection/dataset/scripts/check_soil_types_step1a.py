"""
check_soil_types_step1a.py
Analyze image statistics across the dataset to detect distinct soil types.
If images at similar kPa but different ID ranges have very different appearance,
that suggests multiple soil types/fields.
"""
import numpy as np
from PIL import Image
from pathlib import Path
import csv
import json

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
CLEAN_DIR = DATASET_DIR / "clean"
PREPROC_DIR = DATASET_DIR / "preprocessed"

# 1. Load manifest
manifest = []
with open(PREPROC_DIR / "image_manifest.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        manifest.append(row)

print(f"Manifest: {len(manifest)} images")

# 2. Compute per-image stats
results = []
missing = 0
for i, row in enumerate(manifest):
    fname = row["filename"]
    fpath = CLEAN_DIR / fname
    if not fpath.exists():
        missing += 1
        continue
    
    img = Image.open(fpath).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    
    stats = {
        "image_id": row["image_id"],
        "filename": fname,
        "kpa_raw": float(row["kpa_raw"]),
        "kpa_bin": row["kpa_bin"],
        "series_id": row["series_id"],
        "id_num": int(row["id_num"]),
        "r_mean": float(arr[:,:,0].mean()),
        "g_mean": float(arr[:,:,1].mean()),
        "b_mean": float(arr[:,:,2].mean()),
        "brightness": float(arr.mean()),
        "contrast": float(arr.std()),
        "r_std": float(arr[:,:,0].std()),
        "g_std": float(arr[:,:,1].std()),
        "b_std": float(arr[:,:,2].std()),
        "file_size": fpath.stat().st_size,
    }
    results.append(stats)
    
    if (i+1) % 200 == 0:
        print(f"  Processed {i+1}/{len(manifest)}")

print(f"Processed: {len(results)} images, {missing} missing")

# 3. Save stats
stats_path = PREPROC_DIR / "image_stats.json"
with open(stats_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"Saved: {stats_path} ({len(results)} images)")

# 4. Analyze: compare images at similar kPa but different ID ranges
# Group by rounded kPa
from collections import defaultdict

kpa_groups = defaultdict(list)
for r in results:
    kpa_key = round(r["kpa_raw"] * 2) / 2  # round to nearest 0.5
    kpa_groups[kpa_key].append(r)

print("\n=== Same kPa, different IDs — appearance comparison ===")
print(f"{'kPa':>6s} {'ID range':>20s} {'Brightness':>11s} {'Contrast':>9s} {'Size':>8s}")
print("-" * 60)

for kpa_key in sorted(kpa_groups.keys()):
    group = kpa_groups[kpa_key]
    if len(group) < 2:
        continue
    
    ids = [r["id_num"] for r in group]
    bvals = [r["brightness"] for r in group]
    cvals = [r["contrast"] for r in group]
    svals = [r["file_size"] for r in group]
    
    b_range = max(bvals) - min(bvals)
    id_range_str = f"P{min(ids)}-P{max(ids)}"
    
    flag = ""
    # Flag if brightness varies more than 20 within same kPa
    if b_range > 20:
        flag = " *** HIGH VARIANCE"
    
    avg_b = np.mean(bvals)
    avg_c = np.mean(cvals)
    avg_s = np.mean(svals)
    
    print(f"{kpa_key:>6.1f} {id_range_str:>20s} {avg_b:>10.1f} +/-{b_range:>3.1f} {avg_c:>8.1f} {avg_s:>7.0f}{flag}")

# 5. Soil type detection: compare color at standardized moisture bins
print("\n=== Color profile by kPa bin (all images) ===")
bins = defaultdict(list)
for r in results:
    bins[r["kpa_bin"]].append(r)

for bin_name in sorted(bins.keys()):
    group = bins[bin_name]
    r_means = [g["r_mean"] for g in group]
    g_means = [g["g_mean"] for g in group]
    b_means = [g["b_mean"] for g in group]
    
    print(f"  {bin_name:>8s} ({len(group):3d} imgs): R={np.mean(r_means):.1f}+/-{np.std(r_means):.1f}  "
          f"G={np.mean(g_means):.1f}+/-{np.std(g_means):.1f}  "
          f"B={np.mean(b_means):.1f}+/-{np.std(b_means):.1f}")

# 6. Detect if there are 2+ distinct soil types
# Approach: cluster by RGB at similar moisture and check for bimodality
print("\n=== Soil type clustering ===")
# Focus on the dominant 10-20 kPa bin which has enough samples
focus_bin = [r for r in results if 10 <= r["kpa_raw"] <= 20]
brightness_vals = np.array([r["brightness"] for r in focus_bin])

# Simple two-cluster test: would a 2-component GMM make sense?
from sklearn.mixture import GaussianMixture

for n_clusters in [1, 2, 3]:
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    gmm.fit(brightness_vals.reshape(-1, 1))
    bic = gmm.bic(brightness_vals.reshape(-1, 1))
    print(f"  GMM with {n_clusters} cluster(s): BIC={bic:.1f} (lower = better)")

# Also try on 3D RGB
rgb_vals = np.array([[r["r_mean"], r["g_mean"], r["b_mean"]] for r in focus_bin])
for n_clusters in [1, 2, 3]:
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    gmm.fit(rgb_vals)
    bic = gmm.bic(rgb_vals)
    print(f"  RGB-GMM with {n_clusters} cluster(s): BIC={bic:.1f} (lower = better)")

print("\nDone. Check preprocessed/image_stats.json for full data.")
