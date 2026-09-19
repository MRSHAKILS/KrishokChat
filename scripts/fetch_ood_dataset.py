"""
Fetch 100 OOD leaf images from 5 open-source HuggingFace datasets (Project-AgML mirror of Mendeley/Kaggle originals).
- Saves to experiments/ood_test/ood_100/{mango,banana,jute,sugarcane,tea}/
- Manifest CSV + JSONL
- Licensed for research: CC BY 4.0 (jute, banana, sugarcane, tea) + CC BY-NC 3.0 (mango) — citation required.
Run: python scripts/fetch_ood_dataset.py
"""
from pathlib import Path
import random
import csv
import json
from datasets import load_dataset
from PIL import Image

ROOT = Path("D:/KrishokChat Advisory System/experiments/ood_test/ood_100")
ROOT.mkdir(parents=True, exist_ok=True)

# Config: (category, hf_dataset, hf_config_or_none, num_images, citation)
PLAN = [
    ("mango", "Project-AgML/MangoLeafBD_disease_classification", None, 20,
     "MangoLeafBD (Mendeley doi:10.17632/hxsnvwty3r.1, 4000 imgs, CC BY-NC 3.0) - 7 mango diseases from Bangladesh orchards"),
    ("banana", "Project-AgML/banana_leaf_disease_classification", None, 20,
     "Banana leaf disease (1288 imgs, CC BY 4.0) - healthy/segatoka/xamthomonas, Bangladesh. HF mirror of Kaggle/Mendeley"),
    ("jute", "Project-AgML/jute_disease_classification", None, 20,
     "Jute diseases (1390 imgs, CC BY 4.0) - Dieback/Holed/Mosaic/Stem Soft Rot/Fresh, Bangladesh"),
    ("sugarcane", "Project-AgML/sugarcane_leaf_disease_classification", None, 20,
     "Sugarcane leaf disease (6748 imgs, 11 classes, CC BY 4.0) - Maharashtra/Bangladesh collections"),
    ("tea", "Project-AgML/teaLeafBD_disease_classification", None, 20,
     "teaLeafBD (5278 imgs, 7 classes, CC BY 4.0, Mendeley doi:10.17632/744vznw5k2.4) - tea leaf diseases Bangladesh"),
]

# deterministic sampling
RNG = random.Random(42)

manifest_rows = []
jsonl_path = ROOT / "manifest.jsonl"
csv_path = ROOT / "manifest.csv"

if jsonl_path.exists():
    jsonl_path.unlink()
if csv_path.exists():
    csv_path.unlink()

for category, hf_id, hf_config, n, citation in PLAN:
    print(f"\n=== {category.upper()} : {hf_id} ===")
    cat_dir = ROOT / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    # load
    if hf_config:
        ds = load_dataset(hf_id, hf_config, split="train")
    else:
        ds = load_dataset(hf_id, split="train")
    print(f" dataset length: {len(ds)}")
    label_names = None
    try:
        feat = ds.features.get("label")
        if hasattr(feat, "names") and feat.names:
            label_names = feat.names
    except:
        pass
    indices = RNG.sample(range(len(ds)), n)
    for idx, ds_idx in enumerate(indices):
        row = ds[ds_idx]
        img = row["image"]
        if isinstance(img, Image.Image):
            pil = img.convert("RGB")
        else:
            pil = Image.fromarray(img).convert("RGB") if hasattr(img, "shape") else img
        label_id = row.get("label", "")
        label_name = label_names[label_id] if label_names and isinstance(label_id, int) and label_id < len(label_names) else str(label_id)
        safe_label = label_name.replace(" ","_").replace("/","_")
        fname = f"{category}_{idx:02d}_orig{ds_idx:04d}_{safe_label}.jpg"
        fpath = cat_dir / fname
        pil.save(fpath, "JPEG", quality=92)
        rel = fpath.relative_to(ROOT).as_posix()
        rec = {
            "category": category,
            "hf_dataset": hf_id,
            "hf_index": int(ds_idx),
            "label_id": int(label_id) if isinstance(label_id, int) else str(label_id),
            "label_name": label_name,
            "file": rel,
            "abs_path": str(fpath),
            "citation": citation,
            "license": "CC BY 4.0 (except mango CC BY-NC 3.0)",
        }
        manifest_rows.append(rec)
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"  saved {rel} [{label_name}] size={pil.size}")

print(f"\n=== Wrote {len(manifest_rows)} records ===")
with open(csv_path, "w", newline="", encoding="utf-8") as cf:
    w = csv.DictWriter(cf, fieldnames=list(manifest_rows[0].keys()))
    w.writeheader()
    w.writerows(manifest_rows)
print(f"CSV: {csv_path}")
print(f"JSONL: {jsonl_path}")

from collections import Counter
c = Counter(r["category"] for r in manifest_rows)
print("Per category:", dict(c))
for cat in sorted(ROOT.iterdir()):
    if cat.is_dir():
        files = list(cat.glob("*.jpg"))
        tot = sum(f.stat().st_size for f in files)
        print(f"{cat.name}: {len(files)} files, {tot/1024:.1f} KB total")
