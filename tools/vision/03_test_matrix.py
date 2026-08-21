"""Full test matrix: every image in the agri-ai-platform test library.

Runs /api/classify + /api/detect on every image, then produces a per-class
accuracy report. This is the empirical source of truth for routing decisions.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import httpx

LIBRARY = Path(__file__).resolve().parent.parent / "test_images" / "full_library"
BASE_URL = "http://localhost:8000"

# Expected crop family for each disease class (from the library folder names)
FAMILY_MAP = {
    "Cabbage": "Brassica", "Cauliflower": "Brassica",
    "Rice": "Rice",
    "Potato": "Potato",
    "Corn": "Corn", "Maize": "Corn",
    "Tomato": "Solanacea", "Chili": "Solanacea", "Eggplant": "Solanacea", "Brinjal": "Solanacea",
    "Gourd": "GourdGuava", "Guava": "GourdGuava",
    "Wheat": "Wheat",
}


def family_of(folder: str) -> str | None:
    for prefix, fam in FAMILY_MAP.items():
        if folder.startswith(prefix + "__") or folder == prefix:
            return fam
    return None


def main() -> int:
    if not LIBRARY.is_dir():
        print(f"Library not found: {LIBRARY}")
        return 1

    rows = []
    fails = 0
    for cls_dir in sorted(LIBRARY.iterdir()):
        if not cls_dir.is_dir():
            continue
        expected_family = family_of(cls_dir.name)
        for img in sorted(cls_dir.iterdir()):
            if img.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            try:
                with open(img, "rb") as f:
                    files = {"file": (img.name, f, "image/jpeg")}
                    resp = httpx.post(f"{BASE_URL}/api/detect", files=files, timeout=60)
                if resp.status_code != 200:
                    raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                data = resp.json()
                rows.append({
                    "folder": cls_dir.name,
                    "image": img.name,
                    "expected_family": expected_family,
                    "crop": data.get("crop"),
                    "crop_conf": data.get("crop_confidence"),
                    "disease": data.get("disease"),
                    "disease_conf": data.get("disease_confidence"),
                    "has_info": bool(data.get("disease_info")),
                })
                if not data.get("disease_info"):
                    fails += 1
            except Exception as e:
                rows.append({
                    "folder": cls_dir.name, "image": img.name,
                    "expected_family": expected_family,
                    "error": str(e),
                })
                fails += 1
            print(f"  [{cls_dir.name}] {img.name} -> crop={rows[-1].get('crop')} "
                  f"disease={rows[-1].get('disease')} info={rows[-1].get('has_info')}",
                  flush=True)

    print("\n=== SUMMARY ===")
    by_folder: dict[str, list] = defaultdict(list)
    for r in rows:
        by_folder[r["folder"]].append(r)

    correct_family = 0
    correct_disease = 0
    with_info = 0
    total = len(rows)
    fam_tbl = defaultdict(lambda: [0, 0])
    for folder, items in by_folder.items():
        exp = family_of(folder)
        for r in items:
            if "error" in r:
                continue
            if exp and r.get("crop") == exp:
                correct_family += 1
                fam_tbl[folder][0] += 1
            fam_tbl[folder][1] += 1
            if r.get("disease", "").replace(" ", "_").lower() in folder.lower() or \
               folder.lower() in r.get("disease", "").lower():
                correct_disease += 1
            if r.get("has_info"):
                with_info += 1

    print(f"Total images: {total}")
    print(f"Correct crop family: {correct_family}/{total} ({correct_family / max(total,1):.1%})")
    print(f"Correct disease match: {correct_disease}/{total} ({correct_disease / max(total,1):.1%})")
    print(f"With disease_info: {with_info}/{total} ({with_info / max(total,1):.1%})")
    print(f"Errors: {fails}")

    print("\n=== PER-CLASS FAMILY ACCURACY ===")
    for folder in sorted(fam_tbl):
        ok, n = fam_tbl[folder]
        print(f"  {folder}: {ok}/{n} ({ok / max(n,1):.1%})")

    out = LIBRARY.parent / "test_matrix_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"total": total, "rows": rows}, f, ensure_ascii=False, indent=1)
    print(f"\nSaved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
