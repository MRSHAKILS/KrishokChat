"""
analyze_soil_types_step3a.py
Properly analyze the soil type taxonomy.
Pure types (Doash, Atel, Bele, Poli) vs composite types (Bele_Doash, Atel_Doash).
Check if composites are transition zones, mixtures, or mislabeled.
"""
import csv, json, re, sys
from pathlib import Path
from collections import defaultdict, Counter

DATASET_DIR = Path(__file__).resolve().parent.parent
PREPROC_DIR = DATASET_DIR / "preprocessed"
CLEAN_DIR = DATASET_DIR / "clean"
UPDATED_DIR = DATASET_DIR / "updated_dataset"

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl required")
    sys.exit(1)

print("=" * 60)
print("SOIL TYPE ANALYSIS")
print("=" * 60)

# ============================================================
# 1. Load canonical manifest
# ============================================================
manifest_path = PREPROC_DIR / "image_manifest.csv"
with open(manifest_path, "r") as f:
    rows = list(csv.DictReader(f))

print(f"\nLoaded {len(rows)} images")

# ============================================================
# 2. Raw soil type counts
# ============================================================
soil_counts = Counter(r["soil_type"] for r in rows)
print(f"\n--- Raw soil type counts ---")
for st, count in sorted(soil_counts.items(), key=lambda x: -x[1]):
    print(f"  {st:<20s} {count:4d} images")

# ============================================================
# 3. Check if composites are transitions between pure types
# ============================================================
print(f"\n--- Composite type analysis ---")

# Bele_Doash: is it physically between Bele and Doash areas?
# Atel_Doash: is it physically between Atel and Doash areas?
# Check by looking at kPa, land_type, crop distributions for each

composite_analysis = {}
for comp in ["Bele_Doash", "Atel_Doash"]:
    comp_rows = [r for r in rows if r["soil_type"] == comp]
    
    # Extract parent types
    if comp == "Bele_Doash":
        parents = ["Bele", "Doash"]
    else:
        parents = ["Atel", "Doash"]
    
    parent_rows = {}
    for p in parents:
        parent_rows[p] = [r for r in rows if r["soil_type"] == p]
    
    print(f"\n  === {comp} ({len(comp_rows)} images) ===")
    
    # Compare kPa distributions
    print(f"\n  kPa distribution:")
    for label, group in [("Composite", comp_rows)] + [(p, parent_rows[p]) for p in parents]:
        kpas = [float(r["kpa_raw"]) for r in group]
        if not kpas:
            continue
        bins = Counter()
        for k in kpas:
            if k < 10: bins["0-10"] += 1
            elif k < 20: bins["10-20"] += 1
            else: bins["20-30"] += 1
        print(f"    {label:<15s} n={len(group):3d}  "
              f"kPa range {min(kpas):5.1f}-{max(kpas):5.1f}  "
              f"mean={sum(kpas)/len(kpas):5.2f}  "
              f"median={sorted(kpas)[len(kpas)//2]:5.2f}  "
              f"bins={dict(bins)}")
    
    # Compare land type distributions
    print(f"  Land type:")
    for label, group in [("Composite", comp_rows)] + [(p, parent_rows[p]) for p in parents]:
        land_counts = Counter(r["land_type"] for r in group if r["land_type"])
        print(f"    {label:<15s} {dict(land_counts)}")
    
    # Compare crop distributions
    print(f"  Top crops:")
    for label, group in [("Composite", comp_rows)] + [(p, parent_rows[p]) for p in parents]:
        crop_counts = Counter(r["crop"] for r in group if r["crop"]).most_common(5)
        print(f"    {label:<15s} {dict(crop_counts)}")

    # Compare growth stages
    print(f"  Growth stages:")
    for label, group in [("Composite", comp_rows)] + [(p, parent_rows[p]) for p in parents]:
        stage_counts = Counter(r["growth_stage"] for r in group if r["growth_stage"]).most_common(5)
        print(f"    {label:<15s} {dict(stage_counts)}")

# ============================================================
# 4. Check image features by soil type (brightness/contrast/RGB)
# ============================================================
print(f"\n--- Image features by soil type ---")
try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("  SKIP: PIL/numpy not available")
    pass
else:
    # Sample up to 50 images per soil type
    soil_samples = defaultdict(list)
    for r in rows:
        st = r["soil_type"]
        if len(soil_samples[st]) < 50:
            soil_samples[st].append(r)
    
    for st in sorted(soil_samples):
        samples = soil_samples[st]
        brightnesses = []
        contrasts = []
        for r in samples:
            img_path = CLEAN_DIR / r["filename"]
            if not img_path.exists():
                continue
            try:
                img = Image.open(img_path).convert("L")
                arr = np.array(img).astype(np.float32)
                brightnesses.append(arr.mean())
                contrasts.append(arr.std())
            except:
                continue
        
        if brightnesses:
            print(f"  {st:<20s} n_samples={len(brightnesses):3d}  "
                  f"brightness={np.mean(brightnesses):5.1f}±{np.std(brightnesses):4.1f}  "
                  f"contrast={np.mean(contrasts):5.1f}±{np.std(contrasts):4.1f}")

# ============================================================
# 5. PCA / clustering on RGB to see if composites separate
# ============================================================
print(f"\n--- Visual separability check (RGB) ---")
try:
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
except ImportError:
    print("  SKIP: sklearn/numpy not available")
    pass
else:
    # Sample images from each soil type
    soil_samples = defaultdict(list)
    for r in rows:
        st = r["soil_type"]
        if len(soil_samples[st]) < 30:
            soil_samples[st].append(r)
    
    features = []
    labels = []
    filenames_used = []
    
    for st, samples in soil_samples.items():
        for r in samples:
            img_path = CLEAN_DIR / r["filename"]
            if not img_path.exists():
                continue
            try:
                img = Image.open(img_path)
                # Extract color moments (mean R, G, B, std R, G, B)
                arr = np.array(img).astype(np.float32)
                h, w, c = arr.shape
                line = []
                for ch in range(min(c, 3)):
                    line.append(arr[:,:,ch].mean())
                    line.append(arr[:,:,ch].std())
                # Add brightness and contrast
                gray = np.mean(arr, axis=2)
                line.append(gray.mean())
                line.append(gray.std())
                features.append(line)
                labels.append(st)
                filenames_used.append(r["filename"])
            except Exception as e:
                continue
    
    if len(features) >= 10:
        X = StandardScaler().fit_transform(np.array(features))
        pca = PCA(n_components=2)
        coords = pca.fit_transform(X)
        
        print(f"  PCA on {len(features)} images with 8 color features")
        print(f"  Explained variance: PC1={pca.explained_variance_ratio_[0]:.3f}, PC2={pca.explained_variance_ratio_[1]:.3f}")
        
        # Per soil type centroids
        type_coords = defaultdict(list)
        for coord, label in zip(coords, labels):
            type_coords[label].append(coord)
        
        print(f"\n  Centroids in PC1-PC2 space:")
        for st in sorted(type_coords):
            pts = np.array(type_coords[st])
            centroid = pts.mean(axis=0)
            spread = pts.std(axis=0)
            print(f"    {st:<20s} PC1={centroid[0]:+6.2f}±{spread[0]:.2f}  PC2={centroid[1]:+6.2f}±{spread[1]:.2f}")
        
        # Check if Bele_Doash falls between Bele and Doash
        if "Bele_Doash" in type_coords and "Bele" in type_coords and "Doash" in type_coords:
            bele_cent = np.mean(type_coords["Bele"], axis=0)
            doash_cent = np.mean(type_coords["Doash"], axis=0)
            bele_doash_cent = np.mean(type_coords["Bele_Doash"], axis=0)
            
            # Distance from composite to each parent
            d_to_bele = np.linalg.norm(bele_doash_cent - bele_cent)
            d_to_doash = np.linalg.norm(bele_doash_cent - doash_cent)
            d_parents = np.linalg.norm(bele_cent - doash_cent)
            
            print(f"\n  Bele_Doash: midpoint between Bele and Doash?")
            print(f"    Dist to Bele:  {d_to_bele:.2f}")
            print(f"    Dist to Doash: {d_to_doash:.2f}")
            print(f"    Parent dist:   {d_parents:.2f}")
            if d_to_bele < d_parents * 0.5 and d_to_doash < d_parents * 0.5:
                print(f"    VERDICT: Yes, Bele_Doash appears to be a physical transition/mixture")
            else:
                print(f"    VERDICT: Not a simple transition - has distinct visual character")
        
        if "Atel_Doash" in type_coords and "Atel" in type_coords and "Doash" in type_coords:
            atel_cent = np.mean(type_coords["Atel"], axis=0)
            doash_cent = np.mean(type_coords["Doash"], axis=0)
            atel_doash_cent = np.mean(type_coords["Atel_Doash"], axis=0)
            
            d_to_atel = np.linalg.norm(atel_doash_cent - atel_cent)
            d_to_doash = np.linalg.norm(atel_doash_cent - doash_cent)
            d_parents = np.linalg.norm(atel_cent - doash_cent)
            
            print(f"\n  Atel_Doash: midpoint between Atel and Doash?")
            print(f"    Dist to Atel:  {d_to_atel:.2f}")
            print(f"    Dist to Doash: {d_to_doash:.2f}")
            print(f"    Parent dist:   {d_parents:.2f}")
            if d_to_atel < d_parents * 0.5 and d_to_doash < d_parents * 0.5:
                print(f"    VERDICT: Yes, Atel_Doash appears to be a physical transition/mixture")
            else:
                print(f"    VERDICT: Not a simple transition - has distinct visual character")

# ============================================================
# 6. Final assessment
# ============================================================
print(f"\n{'='*60}")
print("FINAL SOIL TYPE TAXONOMY")
print(f"{'='*60}")

# Pure types
pure = {"Doash", "Atel", "Bele", "Poli"}
composites = {"Bele_Doash", "Atel_Doash"}

print(f"\nPure soil types:               {sorted(pure)}")
for st in sorted(pure):
    count = soil_counts.get(st, 0)
    print(f"  {st:<20s}: {count:4d} images")

print(f"\nComposite/transition types:    {sorted(composites)}")
for st in sorted(composites):
    count = soil_counts.get(st, 0)
    print(f"  {st:<20s}: {count:4d} images")

print(f"\nIf merged by parent:")
parent_map = {
    "Doash": "Doash",
    "Atel": "Atel",
    "Bele": "Bele",
    "Poli": "Poli",
    "Bele_Doash": "Bele_or_Doash",  # uncertain
    "Atel_Doash": "Atel_or_Doash",  # uncertain
}
merged_counts = defaultdict(int)
for st, count in soil_counts.items():
    merged_counts[parent_map.get(st, "Other")] += count
print(f"  Doash (pure + composites merging?): {merged_counts.get('Doash',0) + merged_counts.get('Bele_or_Doash',0) + merged_counts.get('Atel_or_Doash',0)}")
print(f"  But this needs the PCA verdict above to decide")

print(f"\n{'='*60}")
print("DONE - See PCA analysis for whether composites are truly transitions")
