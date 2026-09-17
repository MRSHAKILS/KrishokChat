"""V4 - ONNX Runtime parity against the ``.pt`` serving path, plus CPU latency.

Claim this supports: *the serving models export to a portable runtime without accuracy
loss, at N ms CPU latency.* Nothing here needs a browser.

Preprocessing is taken from ``ultralytics.data.augment.classify_transforms`` via
``_vision_common.preprocess_numpy`` rather than reimplemented, because ultralytics
classification uses ``Resize -> CenterCrop -> /255`` with **no letterbox** and no mean/std
shift. Getting this wrong makes parity look broken for reasons unrelated to ONNX.

Reported per model:
* agreement rate (ONNX top-1 == ``.pt`` top-1) and max absolute probability delta
* ONNX top-1/top-3 accuracy alongside the V2 ``.pt`` accuracy from
  ``results_real_pt_baseline.json``
* McNemar exact paired test on the ONNX-vs-``.pt`` disagreements, because the two runtimes
  are evaluated on the *same* images; unpaired accuracy differences would overstate the
  uncertainty
* latency p50/p90/p95/p99 with ``intra_op_num_threads`` pinned and recorded, since an
  unpinned thread count makes the number irreproducible on another machine
* ``.pt`` MB vs ``.onnx`` MB per model and in total

Run:
    .\\backend\\.venv\\Scripts\\python.exe "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/run_real_e02b_onnx_parity.py"

Flags:
    --latency-runs N   timed single-image runs per model (default 200)
    --warmup N         discarded warm-up runs per model (default 20)
    --threads N        intra_op_num_threads (default 1; recorded in output)
    --limit-per-class N  cap images per class (smoke runs only; recorded)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from _vision_common import (  # noqa: E402
    DISEASE_MODEL_KEYS,
    EXPERIMENT_DIR,
    REPO_ROOT,
    VISION_DIR,
    checkpoint_imgsz,
    class_names,
    ensure_backend_importable,
    model_dir,
    percentiles,
    preprocess_numpy,
    provenance,
    sha256_of,
    write_json,
)

ensure_backend_importable()

MANIFEST = Path(r"D:\KrishokChat Advisory System\paper\EACL Demo\experiments\E02_multimodal_diagnostic_workflow\vision_eval_manifest.json")
PT_BASELINE = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\n04_pt_baseline_20260917.json")
EXPORT_REPORT = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\n04_onnx_export_report_20260917.json")
ONNX_DIR = VISION_DIR / "onnx"
OUTPUT = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\n04_onnx_parity_20260917.json")

ALL_MODELS = ("crop_classifier",) + DISEASE_MODEL_KEYS


def mcnemar_exact(only_a_correct: int, only_b_correct: int) -> dict[str, Any]:
    """Two-sided exact binomial McNemar test on paired discordant counts.

    The exact form is used rather than the chi-square approximation because the
    discordant total here is expected to be tiny (near-zero for FP32 parity), and
    chi-square is not well approximated below ~25 discordant pairs.
    """
    n = only_a_correct + only_b_correct
    if n == 0:
        return {
            "discordant_pairs": 0,
            "p_value": None,
            "interpretation": "identical predictions on every image; no paired test is defined",
        }
    larger = max(only_a_correct, only_b_correct)
    tail = sum(math.comb(n, k) for k in range(larger, n + 1)) * (0.5**n)
    p_value = min(1.0, 2.0 * tail)
    return {
        "discordant_pairs": n,
        "only_first_correct": only_a_correct,
        "only_second_correct": only_b_correct,
        "p_value": round(p_value, 6),
        "test": "two-sided exact binomial McNemar (paired; same images through both runtimes)",
        "interpretation": (
            "no statistically significant accuracy difference at alpha=0.05"
            if p_value >= 0.05
            else "statistically significant accuracy difference at alpha=0.05"
        ),
    }


def _session(path: Path, threads: int):
    import onnxruntime as ort

    options = ort.SessionOptions()
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1
    options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return ort.InferenceSession(str(path), sess_options=options, providers=["CPUExecutionProvider"])


def _select(rows: list[dict[str, Any]], limit_per_class: int | None) -> list[dict[str, Any]]:
    if limit_per_class is None:
        return rows
    seen: Counter[str] = Counter()
    kept: list[dict[str, Any]] = []
    for row in rows:
        key = f"{row.get('disease_model')}|{row['label']}"
        if seen[key] >= limit_per_class:
            continue
        seen[key] += 1
        kept.append(row)
    return kept


def _top_k(probabilities: np.ndarray, labels: tuple[str, ...], k: int = 3) -> list[str]:
    order = np.argsort(probabilities)[::-1][:k]
    return [labels[int(index)] for index in order]


def compare_model(
    model_key: str,
    rows: list[dict[str, Any]],
    runner,
    spec,
    *,
    labels: tuple[str, ...],
    imgsz: int,
    threads: int,
    latency_runs: int,
    warmup: int,
    truth_field: str,
) -> dict[str, Any]:
    onnx_path = ONNX_DIR / f"{model_key}.onnx"
    if not onnx_path.exists():
        return {"status": "unmeasured", "reason": f"missing {onnx_path.name}; run export_vision_onnx_all.py"}
    if not rows:
        return {
            "status": "unmeasured",
            "reason": "no local labelled test images",
            "n_classes": len(labels),
            "train_imgsz": imgsz,
        }

    session = _session(onnx_path, threads)
    input_name = session.get_inputs()[0].name

    agree = 0
    both_correct = only_pt = only_onnx = neither = 0
    onnx_top1 = onnx_top3 = 0
    pt_top1 = pt_top3 = 0
    max_prob_delta = 0.0
    disagreements: list[dict[str, Any]] = []
    scored = 0

    warm_image = Image.open(REPO_ROOT / rows[0]["path"]).convert("RGB")
    warm_tensor = preprocess_numpy(warm_image, imgsz)
    for _ in range(warmup):
        session.run(None, {input_name: warm_tensor})
        runner.predict(spec, warm_image)

    for row in rows:
        truth = row[truth_field]
        image = Image.open(REPO_ROOT / row["path"]).convert("RGB")

        tensor = preprocess_numpy(image, imgsz)
        onnx_probabilities = np.asarray(session.run(None, {input_name: tensor})[0]).reshape(-1).astype(np.float64)

        prediction = runner.predict(spec, image)
        pt_probabilities = np.zeros(len(labels), dtype=np.float64)
        for entry in prediction.top3:
            pt_probabilities[labels.index(str(entry["class"]))] = float(entry["confidence"])

        onnx_label = labels[int(np.argmax(onnx_probabilities))]
        pt_label = prediction.label
        scored += 1

        if onnx_label == pt_label:
            agree += 1
        else:
            disagreements.append(
                {
                    "path": row["path"],
                    "truth": truth,
                    "pt": pt_label,
                    "pt_confidence": prediction.confidence,
                    "onnx": onnx_label,
                    "onnx_confidence": round(float(onnx_probabilities.max()), 6),
                }
            )

        # Probability delta is only meaningful on the classes the .pt path reported
        # (the runner returns top-3, not the full vector).
        for entry in prediction.top3:
            index = labels.index(str(entry["class"]))
            max_prob_delta = max(max_prob_delta, abs(onnx_probabilities[index] - float(entry["confidence"])))

        onnx_hit = onnx_label == truth
        pt_hit = pt_label == truth
        onnx_top1 += int(onnx_hit)
        pt_top1 += int(pt_hit)
        onnx_top3 += int(truth in _top_k(onnx_probabilities, labels))
        pt_top3 += int(truth in [str(entry["class"]) for entry in prediction.top3])
        if onnx_hit and pt_hit:
            both_correct += 1
        elif pt_hit:
            only_pt += 1
        elif onnx_hit:
            only_onnx += 1
        else:
            neither += 1

    onnx_timings: list[float] = []
    for _ in range(latency_runs):
        start = time.perf_counter()
        session.run(None, {input_name: warm_tensor})
        onnx_timings.append((time.perf_counter() - start) * 1000.0)

    pt_timings: list[float] = []
    for _ in range(latency_runs):
        start = time.perf_counter()
        runner.predict(spec, warm_image)
        pt_timings.append((time.perf_counter() - start) * 1000.0)

    onnx_stats = percentiles(onnx_timings)
    pt_stats = percentiles(pt_timings)
    pt_file = model_dir(model_key) / "model.pt"

    agreement_rate = agree / scored
    result: dict[str, Any] = {
        "status": "measured",
        "precision": "FP32",
        "onnx_artifact": str(onnx_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "onnx_sha256": sha256_of(onnx_path),
        "pt_artifact": str(pt_file.relative_to(REPO_ROOT)).replace("\\", "/"),
        "pt_sha256": sha256_of(pt_file),
        "imgsz": imgsz,
        "n_classes": len(labels),
        "n_images": scored,
        "parity": {
            "agreement_rate": round(agreement_rate, 6),
            "n_agree": agree,
            "n_disagree": scored - agree,
            "max_abs_probability_delta": round(max_prob_delta, 6),
            "disagreements": disagreements[:50],
            "disagreements_truncated": max(0, len(disagreements) - 50),
        },
        "accuracy": {
            "onnx_top1": round(onnx_top1 / scored, 4),
            "pt_top1": round(pt_top1 / scored, 4),
            "top1_delta_pp": round((onnx_top1 - pt_top1) / scored * 100, 4),
            "onnx_top3": round(onnx_top3 / scored, 4),
            "pt_top3": round(pt_top3 / scored, 4),
            "paired_table": {
                "both_correct": both_correct,
                "only_pt_correct": only_pt,
                "only_onnx_correct": only_onnx,
                "neither_correct": neither,
            },
            "mcnemar": mcnemar_exact(only_pt, only_onnx),
        },
        "latency_single_image": {
            "onnxruntime_cpu": onnx_stats,
            "pytorch_ultralytics": pt_stats,
            "speedup_p50_pt_over_onnx": (
                round(pt_stats["p50_ms"] / onnx_stats["p50_ms"], 3)
                if onnx_stats["p50_ms"]
                else None
            ),
            "config": {
                "provider": "CPUExecutionProvider",
                "intra_op_num_threads": threads,
                "inter_op_num_threads": 1,
                "batch": 1,
                "warmup_runs": warmup,
                "timed_runs": latency_runs,
                "image": rows[0]["path"],
            },
            "note": (
                "pytorch timing includes ultralytics' own preprocessing; the ONNX timing is "
                "session.run only, with preprocessing excluded. They are not a like-for-like "
                "end-to-end comparison of the request path."
            ),
        },
        "size": {
            "pt_mb": round(pt_file.stat().st_size / (1024 * 1024), 3),
            "onnx_mb": round(onnx_path.stat().st_size / (1024 * 1024), 3),
        },
    }
    if agreement_rate < 0.99:
        result["parity"]["warning"] = (
            "agreement below 99% for an FP32 export: investigate preprocessing before "
            "reporting any number from this row"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latency-runs", type=int, default=200)
    parser.add_argument("--warmup", type=int, default=20)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--limit-per-class", type=int, default=None)
    args = parser.parse_args()

    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}; run build_vision_eval_manifest.py first")
    if not EXPORT_REPORT.exists():
        raise SystemExit(f"missing {EXPORT_REPORT}; run export_vision_onnx_all.py first")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = _select(manifest["images"], args.limit_per_class)

    from app.infrastructure.vision.registry import ArtifactVisionRegistry
    from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner

    registry = ArtifactVisionRegistry(VISION_DIR)
    runner = UltralyticsClassificationRunner()
    specs = registry.disease_models

    print(f"parity over {len(rows)} images, threads={args.threads}")
    models: dict[str, Any] = {}

    for model_key in DISEASE_MODEL_KEYS:
        model_rows = [row for row in rows if row.get("disease_model") == model_key]
        models[model_key] = compare_model(
            model_key,
            model_rows,
            runner,
            specs.get(model_key),
            labels=class_names(model_key),
            imgsz=checkpoint_imgsz(model_key),
            threads=args.threads,
            latency_runs=args.latency_runs,
            warmup=args.warmup,
            truth_field="label",
        )
        entry = models[model_key]
        if entry["status"] == "measured":
            print(
                f"  {model_key:16s} agree={entry['parity']['agreement_rate']} "
                f"onnx_top1={entry['accuracy']['onnx_top1']} pt_top1={entry['accuracy']['pt_top1']} "
                f"onnx_p50={entry['latency_single_image']['onnxruntime_cpu']['p50_ms']}ms"
            )
        else:
            print(f"  {model_key:16s} {entry['status'].upper()} ({entry['reason']})")

    crop_rows = [row for row in rows if row.get("expected_crop_label")]
    models["crop_classifier"] = compare_model(
        "crop_classifier",
        crop_rows,
        runner,
        registry.crop_classifier,
        labels=class_names("crop_classifier"),
        imgsz=checkpoint_imgsz("crop_classifier"),
        threads=args.threads,
        latency_runs=args.latency_runs,
        warmup=args.warmup,
        truth_field="expected_crop_label",
    )
    crop_entry = models["crop_classifier"]
    if crop_entry["status"] == "measured":
        crop_entry["label_space_note"] = (
            "Manifest truth is family-level; checkpoint predicts 10 species-level labels. "
            "Exact-match top-1 mixes label spaces — see the pt-baseline species breakdown. "
            "Parity (ONNX-vs-.pt agreement) is unaffected by label spaces."
        )
        print(
            f"  {'crop_classifier':16s} agree={crop_entry['parity']['agreement_rate']} "
            f"onnx_top1={crop_entry['accuracy']['onnx_top1']} pt_top1={crop_entry['accuracy']['pt_top1']}"
        )

    measured = [entry for entry in models.values() if entry.get("status") == "measured"]
    weakest = min((entry["parity"]["agreement_rate"] for entry in measured), default=None)
    payload = {
        "layer": "E02_multimodal_diagnostic_workflow",
        "artifact": "results_real_onnx_parity",
        "schema_version": 1,
        "provenance": provenance(
            Path(__file__),
            inputs={
                "vision_eval_manifest.json": MANIFEST,
                "vision_onnx_export_report.json": EXPORT_REPORT,
                "results_real_pt_baseline.json": PT_BASELINE if PT_BASELINE.exists() else MANIFEST,
            },
        ),
        "run_config": {
            "limit_per_class": args.limit_per_class,
            "latency_runs": args.latency_runs,
            "warmup": args.warmup,
            "intra_op_num_threads": args.threads,
            "task": "classify",
            "preprocessing": (
                "ultralytics classify_transforms: Resize(imgsz, bilinear, antialias) -> "
                "CenterCrop(imgsz) -> ToTensor -> Normalize(mean=0, std=1). No letterbox."
            ),
        },
        "summary": {
            "n_models_measured": len(measured),
            "n_models_unmeasured": len(models) - len(measured),
            "lowest_agreement_rate": weakest,
            "total_onnx_mb": round(sum(entry["size"]["onnx_mb"] for entry in measured), 3),
            "total_pt_mb": round(sum(entry["size"]["pt_mb"] for entry in measured), 3),
        },
        "models": models,
    }
    write_json(OUTPUT, payload)
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
