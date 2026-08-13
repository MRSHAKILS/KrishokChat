"""
select_cluster_samples_step1b.py
Find representative images from each brightness cluster for visual inspection.
Outputs: cluster_samples.txt with filenames grouped by cluster.
"""
import json
import numpy as np
from pathlib import Path
from sklearn.mixture import GaussianMixture

SCRIPT_DIR = Path(__file__).resolve().parent
PREPROC_DIR = SCRIPT_DIR.parent / "preprocessed"
CLEAN_DIR = SCRIPT_DIR.parent / "clean"

# Load stats
with open(PREPROC_DIR / "image_stats.json", "r", encoding="utf-8") as f:
    stats = json.load(f)

# Focus on 10-20 kPa bin (most samples, less moisture-driven variance)
mid_range = [s for s in stats if 10 <= s["kpa_raw"] <= 20]
brightness = np.array([[s["brightness"]] for s in mid_range])

# Fit 2-cluster GMM
gmm = GaussianMixture(n_components=2, random_state=42)
labels = gmm.fit_predict(brightness)

# Assign cluster labels
for i, s in enumerate(mid_range):
    s["cluster"] = int(labels[i])

# Find most representative images for each cluster (closest to cluster mean)
cluster0_center = brightness[labels == 0].mean()
cluster1_center = brightness[labels == 1].mean()

cluster0_samples = [s for s in mid_range if s["cluster"] == 0]
cluster1_samples = [s for s in mid_range if s["cluster"] == 1]

cluster0_samples.sort(key=lambda s: abs(s["brightness"] - float(cluster0_center)))
cluster1_samples.sort(key=lambda s: abs(s["brightness"] - float(cluster1_center)))

print("=" * 70)
print("CLUSTER ANALYSIS — 10-20 kPa images")
print("=" * 70)
print(f"\nCluster 0: {len(cluster0_samples)} images, center brightness={cluster0_center:.1f}")
print("Top 8 representatives (closest to center):")
for s in cluster0_samples[:8]:
    print(f"  P{s['id_num']:04d} ({s['kpa_raw']} kPa) brightness={s['brightness']:.1f} contrast={s['contrast']:.1f}")

print(f"\nCluster 1: {len(cluster1_samples)} images, center brightness={cluster1_center:.1f}")
print("Top 8 representatives (closest to center):")
for s in cluster1_samples[:8]:
    print(f"  P{s['id_num']:04d} ({s['kpa_raw']} kPa) brightness={s['brightness']:.1f} contrast={s['contrast']:.1f}")

# Also check: do clusters correspond to different ID ranges (time/field)?
cluster0_ids = [s["id_num"] for s in cluster0_samples]
cluster1_ids = [s["id_num"] for s in cluster1_samples]
print(f"\nCluster 0 ID range: P{min(cluster0_ids)}-P{max(cluster0_ids)}")
print(f"Cluster 1 ID range: P{min(cluster1_ids)}-P{max(cluster1_ids)}")

# Check overlap in ID space
all_cluster0 = sorted([s["id_num"] for s in cluster0_samples])
all_cluster1 = sorted([s["id_num"] for s in cluster1_samples])

# Are clusters separated by ID (time)?
print(f"\nCluster 0 IDs: ...P{all_cluster0[:3]}...P{all_cluster0[-3:]}")
print(f"Cluster 1 IDs: ...P{all_cluster1[:3]}...P{all_cluster1[-3:]}")

# Check if clusters correspond to series (fields)
cluster0_series = set(s["series_id"] for s in cluster0_samples)
cluster1_series = set(s["series_id"] for s in cluster1_samples)
overlap = cluster0_series & cluster1_series
only_c0 = cluster0_series - overlap
only_c1 = cluster1_series - overlap

print(f"\nCluster 0 unique series: {sorted(only_c0)}")
print(f"Cluster 1 unique series: {sorted(only_c1)}")
print(f"Series in both clusters: {sorted(overlap)}")

# Save representative pairs at same kPa from different clusters
print("\n\n=== SAME kPa, DIFFERENT CLUSTER — visual comparison pairs ===")
from collections import defaultdict
by_kpa = defaultdict(list)
for s in mid_range:
    by_kpa[round(s["kpa_raw"])].append(s)

pairs_found = 0
for kpa_val in sorted(by_kpa.keys()):
    group = by_kpa[kpa_val]
    c0 = [s for s in group if s["cluster"] == 0]
    c1 = [s for s in group if s["cluster"] == 1]
    if c0 and c1 and pairs_found < 6:
        # Pick one from each cluster closest to center
        c0_best = min(c0, key=lambda s: abs(s["brightness"] - float(cluster0_center)))
        c1_best = min(c1, key=lambda s: abs(s["brightness"] - float(cluster1_center)))
        print(f"\nPair {pairs_found+1}: ~{kpa_val} kPa")
        print(f"  Cluster 0: P{c0_best['id_num']:04d} brightness={c0_best['brightness']:.1f}")
        print(f"  Cluster 1: P{c1_best['id_num']:04d} brightness={c1_best['brightness']:.1f}")
        pairs_found += 1

# Save detailed output
outpath = SCRIPT_DIR.parent / "reports" / "cluster_samples.txt"
with open(outpath, "w", encoding="utf-8") as f:
    f.write("CLUSTER SAMPLES FOR VISUAL INSPECTION\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Cluster 0 (darker, {len(cluster0_samples)} images):\n")
    for s in cluster0_samples[:15]:
        f.write(f"  P{s['id_num']:04d} {s['filename']} brightness={s['brightness']:.1f}\n")
    f.write(f"\nCluster 1 (brighter, {len(cluster1_samples)} images):\n")
    for s in cluster1_samples[:15]:
        f.write(f"  P{s['id_num']:04d} {s['filename']} brightness={s['brightness']:.1f}\n")
    f.write(f"\nSAME-kPa COMPARISON PAIRS:\n")
    for kpa_val in sorted(by_kpa.keys()):
        group = by_kpa[kpa_val]
        c0 = [s for s in group if s["cluster"] == 0]
        c1 = [s for s in group if s["cluster"] == 1]
        if c0 and c1:
            c0_best = min(c0, key=lambda s: abs(s["brightness"] - float(cluster0_center)))
            c1_best = min(c1, key=lambda s: abs(s["brightness"] - float(cluster1_center)))
            f.write(f"  ~{kpa_val} kPa: C0=P{c0_best['id_num']:04d} vs C1=P{c1_best['id_num']:04d}\n")

print(f"\n\nDetailed output saved to: {outpath}")
