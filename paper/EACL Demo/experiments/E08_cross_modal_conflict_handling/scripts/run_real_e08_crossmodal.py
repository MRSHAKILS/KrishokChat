#!/usr/bin/env python3
"""E08 real cross-modal conflict — VisionPipeline crop vs text crop.

Builds 80 contradiction cases from the V1 manifest: image crop family vs a conflicting
text crop hint (e.g., Potato image + "brinjal" text). Measures how often the pipeline
detects mismatch (disease model win, NO_DISEASE_MODEL, crop rewrite) — no hardcoded constants.
"""

from __future__ import annotations

import asyncio
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[5]
SHARED = REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

# Reuse vision manifest path
MANIFEST = REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "E02_multimodal_diagnostic_workflow" / "vision_eval_manifest.json"
OUT_DIR = HERE.parents[1]

# Map manifest crop_family to text hint that conflicts
CONFLICT_HINT = {"Potato": "brinjal", "Rice": "potato", "Cabbage": "rice", "Cauliflower": "rice", "Tomato": "potato", "Chili": "potato", "Eggplant": "potato", "Gourd": "potato", "Guava": "potato"}

def main() -> int:
    print("E08 real cross-modal — building contradiction cases from vision manifest")
    if not MANIFEST.exists():
        raise SystemExit(f"missing manifest: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    # Pick 80 random images that have a conflicting hint
    scored = manifest["images"]
    candidates = [r for r in scored if r.get("crop_family") in CONFLICT_HINT]
    rnd = random.Random(42)
    sampled = rnd.sample(candidates, min(80, len(candidates)))

    # Build offline vision + QA pipeline (QA stub, BM25)
    # VisionPipeline needs registry/runner/qa/audit
    sys.path.insert(0, str(REPO_ROOT / "backend"))
    import _qa_harness as H  # type: ignore[import]
    from app.application.vision_pipeline import VisionPipeline
    from app.infrastructure.vision.registry import ArtifactVisionRegistry
    from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner
    from app.infrastructure.audit.jsonl import JSONLAuditSink
    import tempfile
    from pathlib import Path as P

    audit_path = P(tempfile.gettempdir()) / "krishokchat_e08_audit.jsonl"
    qa_pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())
    registry = ArtifactVisionRegistry(REPO_ROOT / "backend" / "ml_assets" / "vision")
    runner = UltralyticsClassificationRunner()
    vision = VisionPipeline(registry=registry, runner=runner, qa=qa_pipeline, audit=JSONLAuditSink(audit_path))  # type: ignore[arg-type]

    from PIL import Image

    async def run_cases() -> list[dict]:
        out: list[dict] = []
        for row in sampled:
            hint = CONFLICT_HINT[row["crop_family"]]
            img = Image.open(REPO_ROOT / row["path"]).convert("RGB")
            # Image-only detection (no hint) = ground truth crop
            res_image_only = await vision.detect(img, crop_hint=None)
            # Contradiction case: image + conflicting text hint
            res_conflict = await vision.detect(img, crop_hint=hint)
            out.append({
                "path": row["path"],
                "image_crop_family": row["crop_family"],
                "conflict_hint": hint,
                "image_only_crop": res_image_only.crop,
                "image_only_disease": res_image_only.disease,
                "image_only_status": res_image_only.status.value,
                "conflict_crop": res_conflict.crop,
                "conflict_disease": res_conflict.disease,
                "conflict_status": res_conflict.status.value,
                "mismatch_detected": res_conflict.crop != res_image_only.crop or res_conflict.status != res_image_only.status,
            })
        return out

    results = asyncio.run(run_cases())
    mismatches = sum(1 for r in results if r["mismatch_detected"])
    report = {
        "benchmark_name": "EACL_E08_CROSS_MODAL_CONFLICT",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"vision_eval_manifest.json": MANIFEST}),
        "run_config": {"n": len(results), "seed": 42, "vision": "YOLO classify .pt via Ultralytics (no boxes)", "qa": "BM25-only StubLLM", "conflict_hint_map": CONFLICT_HINT},
        "mismatch_detection_rate": round(mismatches / len(results), 4) if results else None,
        "n_mismatch": mismatches,
        "status_distribution_conflict": {k: sum(1 for r in results if r["conflict_status"] == k) for k in set(r["conflict_status"] for r in results)},
        "sample": results[:15],
    }
    out_json = OUT_DIR / "results_real_crossmodal.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        import yaml
        (OUT_DIR / "results_real_crossmodal.yaml").write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    except Exception:
        pass
    print(f"[OK] wrote {out_json} — mismatch {mismatches}/{len(results)} = {report['mismatch_detection_rate']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
