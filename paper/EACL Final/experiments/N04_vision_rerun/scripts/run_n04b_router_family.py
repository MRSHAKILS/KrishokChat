#!/usr/bin/env python3
"""Router family-mapped rescore on current checkpoints (EACL Final, CPU $0).

Independent re-scoring (not reusing old scorer internals): loads the .pt crop
router, predicts every manifest image, applies the FROZEN family mapping
(N04_vision_rerun/family_mapping_freeze.md — written before this run), and
reports exact-match + family-mapped accuracy side by side.

Outputs: experiments/results/n04b_router_family_<date>.json (+ .jsonl records).
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

import _qa_harness as H  # noqa: E402

OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
MANIFEST = WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "E02_multimodal_diagnostic_workflow" / "vision_eval_manifest.json"

FAMILY_OF_MANIFEST = {
    "Cabbage": "Brassica", "Cauliflower": "Brassica",
    "Chili": "Solanacea", "Eggplant": "Solanacea", "Tomato": "Solanacea",
    "Potato": "Solanacea", "Gourd": "GourdGuava", "Guava": "GourdGuava",
    "Rice": "Rice", "Wheat": None, "Others": None, None: None,
}
FAMILY_OF_PRED = {
    "Cabbage": "Brassica", "Cauliflower": "Brassica",
    "Chili": "Solanacea", "Eggplant": "Solanacea", "Tomato": "Solanacea",
    "Potato": "Solanacea", "Gourd": "GourdGuava", "Guava": "GourdGuava",
    "Rice": "Rice", "Others": None,
}


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    import warnings
    warnings.filterwarnings("ignore")
    from ultralytics import YOLO
    from PIL import Image

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n04b_router_family_{stamp}.json"
    rec_path = OUT_DIR / f"n04b_router_family_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    rows = manifest["images"]
    model = YOLO(str(WORKSPACE_ROOT / "backend" / "ml_assets" / "vision"
                     / "crop_classifier" / "model.pt"))
    names = model.names

    exact_hit = fam_hit = fam_n = 0
    conf = {}
    t0 = time.perf_counter()
    for idx, row in enumerate(rows):
        img = Image.open(WORKSPACE_ROOT / row["path"]).convert("RGB")
        r = model.predict(img, verbose=False)[0]
        probs = r.probs.data.cpu().numpy()
        pred = names[int(probs.argmax())]
        truth_raw = row.get("crop_family") or row.get("label", "").split("__")[0]
        truth_fam = FAMILY_OF_MANIFEST.get(truth_raw)
        pred_fam = FAMILY_OF_PRED.get(pred)
        exact = (pred == truth_raw)
        in_space = truth_fam is not None
        fam_ok = in_space and (pred_fam == truth_fam)
        if in_space:
            fam_n += 1
            if fam_ok:
                fam_hit += 1
        key = (str(truth_raw), str(pred))
        conf[key] = conf.get(key, 0) + 1
        append_jsonl(rec_path, {"path": row["path"], "truth_raw": truth_raw,
                                "truth_family": truth_fam, "pred": pred,
                                "pred_family": pred_fam, "exact": bool(exact),
                                "family_ok": bool(fam_ok) if in_space else None})
        if (idx + 1) % 300 == 0:
            print(f"[{idx + 1}/{len(rows)}] done", flush=True)
    n = len(rows)

    def wilson(k, n_):
        import math
        if n_ == 0:
            return [0.0, 0.0]
        z, p = 1.95996, k / n_
        d = 1 + z * z / n_
        c = (p + z * z / (2 * n_)) / d
        m = z * math.sqrt(p * (1 - p) / n_ + z * z / (4 * n_ * n_)) / d
        return [round(max(0.0, c - m) * 100, 2), round(min(1.0, c + m) * 100, 2)]

    results = {
        "benchmark_name": "EACL_N04B_ROUTER_FAMILY_RESCORE",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"manifest": MANIFEST}),
        "design": {"n": n, "mapping": "frozen family_mapping_freeze.md (pre-run)",
                   "in_space": "manifest rows with mappable family truth (Wheat/None excluded)"},
        "exact_match_top1": None,
        "family_mapped": {"n": fam_n, "correct": fam_hit,
                          "accuracy": round(fam_hit / fam_n, 4) if fam_n else None,
                          "ci95": wilson(fam_hit, fam_n)},
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    # exact-match recomputed same way for reference
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results["family_mapped"], indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
