"""Wheat disease test matrix — PARALLEL version (8 workers).

Runs all 800 wheatBT test images through /api/detect concurrently.
"""
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx

TEST = Path(r"D:\KrishokChat Advisory System\backend\ml_assets\vision\test_images\wheat_disease")
BASE_URL = "http://localhost:8000"
WORKERS = 8


def normalize(name: str) -> str:
    return name.replace(" ", "_").replace("-", "_").lower()


def test_one(cls_dir: Path, img: Path) -> dict:
    try:
        with open(img, "rb") as f:
            files = {"file": (img.name, f, "image/jpeg")}
            r = httpx.post(f"{BASE_URL}/api/detect", files=files, timeout=90)
        if r.status_code != 200:
            return {"folder": cls_dir.name, "image": img.name, "error": f"HTTP {r.status_code}"}
        d = r.json()
        return {
            "folder": cls_dir.name,
            "image": img.name,
            "disease": d.get("disease", ""),
            "conf": d.get("disease_confidence"),
            "info": bool(d.get("disease_info")),
        }
    except Exception as e:
        return {"folder": cls_dir.name, "image": img.name, "error": str(e)}


def main() -> int:
    jobs = []
    for cls_dir in sorted(TEST.iterdir()):
        if not cls_dir.is_dir():
            continue
        for img in sorted(cls_dir.iterdir()):
            if img.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                jobs.append((cls_dir, img))

    print(f"Total jobs: {len(jobs)} with {WORKERS} workers", flush=True)
    rows = []
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(test_one, c, i): (c, i) for c, i in jobs}
        for fut in as_completed(futs):
            r = fut.result()
            rows.append(r)
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(jobs)}", flush=True)

    by_folder: dict[str, dict] = defaultdict(lambda: {"correct": 0, "total": 0, "no_info": 0})
    for r in rows:
        s = by_folder[r["folder"]]
        s["total"] += 1
        if "error" in r:
            continue
        if normalize(r["disease"]) == normalize(r["folder"]):
            s["correct"] += 1
        if not r["info"]:
            s["no_info"] += 1

    print("\n=== WHEAT PER-CLASS ===")
    for folder in sorted(by_folder):
        s = by_folder[folder]
        print(f"{folder:22s} {s['correct']}/{s['total']} correct ({s['correct']/max(s['total'],1):.1%})  no_info={s['no_info']}")

    total = sum(s["total"] for s in by_folder.values())
    correct = sum(s["correct"] for s in by_folder.values())
    no_info = sum(s["no_info"] for s in by_folder.values())
    print("\n=== WHEAT SUMMARY ===")
    print(f"Total: {total}  Correct: {correct} ({correct/max(total,1):.1%})  Missing info: {no_info}")

    out = TEST / "wheat_matrix_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"total": total, "correct": correct, "by_folder": {k: v for k, v in by_folder.items()}, "rows": rows}, f, ensure_ascii=False, indent=1)
    print(f"Saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())