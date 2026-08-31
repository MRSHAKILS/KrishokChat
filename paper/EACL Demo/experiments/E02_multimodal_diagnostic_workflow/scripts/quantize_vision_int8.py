"""V5 - INT8 static quantization via ONNX Runtime, with a held-out evaluation split.

Ultralytics' own INT8 path (``export(quantize=8)`` -> ``onnx_int8_quantize``) cannot run on
this machine: its calibration loader is ``Exporter.get_int8_calibration_dataloader``, which
calls ``check_cls_dataset(self.args.data)`` and needs a real classification dataset with a
val split. The training datasets were Kaggle / Google-Drive paths and are not present. So
quantization is done directly with ``onnxruntime.quantization.quantize_static`` over a
hand-written ``CalibrationDataReader`` on the local labelled images.

Two correctness properties this script enforces, because getting either wrong produces a
number that looks fine and is meaningless:

* **Calibration and evaluation images are disjoint.** The manifest is split per class
  (stratified, deterministic by SHA-256 ordering) into a calibration split and a held-out
  eval split. Both splits' image hashes are recorded. INT8 accuracy is only ever computed
  on held-out images.
* **Only weighted ops are quantized.** ``nodes_to_exclude`` keeps every non
  ``Conv``/``Gemm``/``MatMul`` node in float, following ultralytics' own comment: a single
  INT8 scale spanning wide-range and 0-1 tensors rounds scores to zero, and excluding by
  node rather than ``op_types`` still calibrates every tensor, which avoids an ORT crash on
  the uncalibrated attention softmax. These are yolo26 models with attention.

Sanity gate: an INT8 artifact whose held-out top-1 drops more than ``--max-drop-pp``
against FP32, or whose agreement with FP32 collapses, is reported as ``rejected`` and is
**not** presented as a usable artifact. A broken INT8 number is worse than none.

Run:
    .\\backend\\.venv\\Scripts\\python.exe "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/quantize_vision_int8.py"

Flags:
    --calibration-fraction F  share of each class used for calibration (default 0.5)
    --max-calibration N       cap calibration images per model (default 300)
    --min-eval-for-claim N    held-out n below which an accuracy claim is not reportable (default 100)
    --max-drop-pp X           held-out top-1 drop that rejects the artifact (default 2.0)
    --latency-runs N          timed runs per model (default 200)
    --threads N               intra_op_num_threads (default 1)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
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
    percentiles,
    preprocess_numpy,
    provenance,
    sha256_of,
    write_json,
)

MANIFEST = EXPERIMENT_DIR / "vision_eval_manifest.json"
ONNX_DIR = VISION_DIR / "onnx"
INT8_DIR = VISION_DIR / "onnx_int8"
REPORT = EXPERIMENT_DIR / "vision_int8_report.json"

ALL_MODELS = ("crop_classifier",) + DISEASE_MODEL_KEYS


def mcnemar_exact(only_a: int, only_b: int) -> dict[str, Any]:
    n = only_a + only_b
    if n == 0:
        return {"discordant_pairs": 0, "p_value": None, "interpretation": "identical predictions; no test defined"}
    larger = max(only_a, only_b)
    tail = sum(math.comb(n, k) for k in range(larger, n + 1)) * (0.5**n)
    p_value = min(1.0, 2.0 * tail)
    return {
        "discordant_pairs": n,
        "only_fp32_correct": only_a,
        "only_int8_correct": only_b,
        "p_value": round(p_value, 6),
        "test": "two-sided exact binomial McNemar (paired: same held-out images through both precisions)",
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
    return ort.InferenceSession(str(path), sess_options=options, providers=["CPUExecutionProvider"])


def _stratified_split(
    rows: list[dict[str, Any]], fraction: float, cap: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Deterministic per-class split. Ordering is by SHA-256 so it never depends on the
    filesystem, and every class contributes to calibration before any class contributes
    twice (the cap is applied round-robin, not by truncating the head of the list)."""
    by_class: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_class.setdefault(row["label"], []).append(row)

    calibration_pool: dict[str, list[dict[str, Any]]] = {}
    evaluation: list[dict[str, Any]] = []
    for label in sorted(by_class):
        ordered = sorted(by_class[label], key=lambda item: item["sha256"])
        take = max(1, int(round(len(ordered) * fraction))) if len(ordered) > 1 else 0
        calibration_pool[label] = ordered[:take]
        evaluation.extend(ordered[take:])

    calibration: list[dict[str, Any]] = []
    index = 0
    while len(calibration) < cap:
        added = False
        for label in sorted(calibration_pool):
            bucket = calibration_pool[label]
            if index < len(bucket):
                calibration.append(bucket[index])
                added = True
                if len(calibration) >= cap:
                    break
        if not added:
            break
        index += 1
    return calibration, evaluation


def _calibration_reader(rows: list[dict[str, Any]], imgsz: int, input_name: str):
    from onnxruntime.quantization import CalibrationDataReader

    class Reader(CalibrationDataReader):
        def __init__(self) -> None:
            self.index = 0

        def get_next(self):
            if self.index >= len(rows):
                return None
            row = rows[self.index]
            self.index += 1
            with Image.open(REPO_ROOT / row["path"]) as handle:
                tensor = preprocess_numpy(handle, imgsz)
            return {input_name: tensor}

        def rewind(self) -> None:
            self.index = 0

    return Reader()


def _evaluate(session, input_name: str, rows: list[dict[str, Any]], labels: tuple[str, ...], imgsz: int):
    predictions: list[str] = []
    truth: list[str] = []
    for row in rows:
        with Image.open(REPO_ROOT / row["path"]) as handle:
            tensor = preprocess_numpy(handle, imgsz)
        probabilities = np.asarray(session.run(None, {input_name: tensor})[0]).reshape(-1)
        predictions.append(labels[int(np.argmax(probabilities))])
        truth.append(row["_truth"])
    return truth, predictions


def quantize_model(
    model_key: str,
    rows: list[dict[str, Any]],
    *,
    labels: tuple[str, ...],
    imgsz: int,
    args,
) -> dict[str, Any]:
    import onnx
    from onnxruntime.quantization import quantize_static

    fp32_path = ONNX_DIR / f"{model_key}.onnx"
    if not fp32_path.exists():
        return {"status": "unmeasured", "reason": f"missing {fp32_path.name}; run export_vision_onnx_all.py"}
    if not rows:
        return {
            "status": "unmeasured",
            "reason": "no local labelled test images: cannot calibrate and cannot evaluate",
            "n_classes": len(labels),
            "train_imgsz": imgsz,
        }

    calibration, evaluation = _stratified_split(rows, args.calibration_fraction, args.max_calibration)
    if not calibration or not evaluation:
        return {
            "status": "unmeasured",
            "reason": (
                f"cannot form disjoint calibration/eval splits from {len(rows)} images "
                "(refusing to calibrate and evaluate on the same data)"
            ),
            "n_images": len(rows),
        }

    INT8_DIR.mkdir(parents=True, exist_ok=True)
    int8_path = INT8_DIR / f"{model_key}_int8.onnx"

    graph = onnx.load(str(fp32_path)).graph
    exclude = [node.name for node in graph.node if node.op_type not in {"Conv", "Gemm", "MatMul"}]
    input_name = _session(fp32_path, args.threads).get_inputs()[0].name

    print(f"  {model_key:16s} calib={len(calibration)} eval={len(evaluation)} quantizing ...", end="", flush=True)
    quantize_static(
        str(fp32_path),
        str(int8_path),
        _calibration_reader(calibration, imgsz, input_name),
        nodes_to_exclude=exclude,
    )

    fp32_session = _session(fp32_path, args.threads)
    int8_session = _session(int8_path, args.threads)

    truth, fp32_predictions = _evaluate(fp32_session, input_name, evaluation, labels, imgsz)
    _, int8_predictions = _evaluate(int8_session, input_name, evaluation, labels, imgsz)

    n = len(truth)
    fp32_correct = sum(1 for t, p in zip(truth, fp32_predictions) if t == p)
    int8_correct = sum(1 for t, p in zip(truth, int8_predictions) if t == p)
    agree = sum(1 for a, b in zip(fp32_predictions, int8_predictions) if a == b)
    only_fp32 = sum(1 for t, a, b in zip(truth, fp32_predictions, int8_predictions) if a == t and b != t)
    only_int8 = sum(1 for t, a, b in zip(truth, fp32_predictions, int8_predictions) if b == t and a != t)

    warm_tensor = preprocess_numpy(Image.open(REPO_ROOT / evaluation[0]["path"]), imgsz)
    for _ in range(args.warmup):
        int8_session.run(None, {input_name: warm_tensor})
        fp32_session.run(None, {input_name: warm_tensor})

    int8_timings: list[float] = []
    for _ in range(args.latency_runs):
        start = time.perf_counter()
        int8_session.run(None, {input_name: warm_tensor})
        int8_timings.append((time.perf_counter() - start) * 1000.0)
    fp32_timings: list[float] = []
    for _ in range(args.latency_runs):
        start = time.perf_counter()
        fp32_session.run(None, {input_name: warm_tensor})
        fp32_timings.append((time.perf_counter() - start) * 1000.0)

    fp32_accuracy = fp32_correct / n
    int8_accuracy = int8_correct / n
    drop_pp = (fp32_accuracy - int8_accuracy) * 100
    agreement = agree / n
    int8_stats = percentiles(int8_timings)
    fp32_stats = percentiles(fp32_timings)

    rejected = drop_pp > args.max_drop_pp or agreement < 0.90
    reportable = n >= args.min_eval_for_claim

    per_class_calibration: dict[str, int] = {}
    for row in calibration:
        per_class_calibration[row["label"]] = per_class_calibration.get(row["label"], 0) + 1

    record: dict[str, Any] = {
        "status": "rejected" if rejected else "measured",
        "int8_artifact": str(int8_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "int8_sha256": sha256_of(int8_path),
        "fp32_artifact": str(fp32_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "fp32_sha256": sha256_of(fp32_path),
        "imgsz": imgsz,
        "n_classes": len(labels),
        "quantization": {
            "method": "onnxruntime.quantization.quantize_static",
            "reason_not_ultralytics": (
                "ultralytics export(quantize=8) needs check_cls_dataset(data=) with a val split; "
                "the Kaggle/Drive training datasets are not on this machine"
            ),
            "nodes_excluded": len(exclude),
            "nodes_total": len(graph.node),
            "nodes_quantized_op_types": ["Conv", "Gemm", "MatMul"],
            "exclusion_rationale": (
                "one INT8 scale spanning wide-range and 0-1 tensors rounds scores to zero; "
                "excluding by node rather than op_types still calibrates every tensor, avoiding an "
                "ORT crash on the uncalibrated attention softmax (ultralytics onnx_int8_quantize)"
            ),
        },
        "calibration_split": {
            "n": len(calibration),
            "per_class": per_class_calibration,
            "fraction_requested": args.calibration_fraction,
            "cap": args.max_calibration,
            "recommended_minimum": 300,
            "meets_recommended_minimum": len(calibration) >= 300,
            "limitation": (
                None
                if len(calibration) >= 300
                else f"{len(calibration)} calibration images is below the 300 ultralytics recommends"
            ),
            "sha256": [row["sha256"] for row in calibration],
        },
        "held_out_eval_split": {
            "n": n,
            "disjoint_from_calibration": True,
            "sha256": [row["sha256"] for row in evaluation],
        },
        "accuracy_held_out": {
            "fp32_top1": round(fp32_accuracy, 4),
            "int8_top1": round(int8_accuracy, 4),
            "drop_pp": round(drop_pp, 4),
            "agreement_rate": round(agreement, 4),
            "paired_table": {
                "only_fp32_correct": only_fp32,
                "only_int8_correct": only_int8,
                "both_or_neither": n - only_fp32 - only_int8,
            },
            "mcnemar": mcnemar_exact(only_fp32, only_int8),
            "claim_reportable": reportable,
            "claim_reportable_criterion": f"held-out n >= {args.min_eval_for_claim}",
            "claim_reportable_note": (
                None
                if reportable
                else f"held-out n={n} is too small to support a published accuracy claim; treat as diagnostic only"
            ),
        },
        "latency_single_image": {
            "int8": int8_stats,
            "fp32": fp32_stats,
            "speedup_p50_fp32_over_int8": (
                round(fp32_stats["p50_ms"] / int8_stats["p50_ms"], 3) if int8_stats["p50_ms"] else None
            ),
            "config": {
                "provider": "CPUExecutionProvider",
                "intra_op_num_threads": args.threads,
                "batch": 1,
                "warmup_runs": args.warmup,
                "timed_runs": args.latency_runs,
            },
        },
        "size": {
            "fp32_mb": round(fp32_path.stat().st_size / (1024 * 1024), 3),
            "int8_mb": round(int8_path.stat().st_size / (1024 * 1024), 3),
            "compression_ratio": round(fp32_path.stat().st_size / int8_path.stat().st_size, 3),
        },
    }
    if rejected:
        record["rejection_reason"] = (
            f"held-out top-1 drop {drop_pp:.2f} pp (limit {args.max_drop_pp}) "
            f"and/or FP32 agreement {agreement:.4f} below 0.90. "
            "This artifact must not be presented as usable."
        )
    print(
        f" {'REJECTED' if rejected else 'ok'} fp32={fp32_accuracy:.4f} int8={int8_accuracy:.4f} "
        f"drop={drop_pp:.2f}pp agree={agreement:.4f} "
        f"{record['size']['int8_mb']}MB ({record['size']['compression_ratio']}x) "
        f"p50={int8_stats['p50_ms']}ms"
    )
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration-fraction", type=float, default=0.5)
    parser.add_argument("--max-calibration", type=int, default=300)
    parser.add_argument("--min-eval-for-claim", type=int, default=100)
    parser.add_argument("--max-drop-pp", type=float, default=2.0)
    parser.add_argument("--latency-runs", type=int, default=200)
    parser.add_argument("--warmup", type=int, default=20)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--models", type=str, default=",".join(ALL_MODELS))
    args = parser.parse_args()

    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}; run build_vision_eval_manifest.py first")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["images"]

    selected = [name.strip() for name in args.models.split(",") if name.strip()]
    print(f"INT8 static quantization, threads={args.threads}")

    models: dict[str, Any] = {}
    for model_key in selected:
        if model_key == "crop_classifier":
            model_rows = [
                {**row, "_truth": row["expected_crop_label"], "label": row["expected_crop_label"]}
                for row in rows
                if row.get("expected_crop_label")
            ]
        else:
            model_rows = [{**row, "_truth": row["label"]} for row in rows if row.get("disease_model") == model_key]
        models[model_key] = quantize_model(
            model_key,
            model_rows,
            labels=class_names(model_key),
            imgsz=checkpoint_imgsz(model_key),
            args=args,
        )
        if models[model_key]["status"] == "unmeasured":
            print(f"  {model_key:16s} UNMEASURED ({models[model_key]['reason']})")

    usable = [key for key, entry in models.items() if entry["status"] == "measured"]
    reportable = [
        key
        for key, entry in models.items()
        if entry["status"] == "measured" and entry["accuracy_held_out"]["claim_reportable"]
    ]
    payload = {
        "layer": "E02_multimodal_diagnostic_workflow",
        "artifact": "vision_int8_report",
        "schema_version": 1,
        "provenance": provenance(Path(__file__), inputs={"vision_eval_manifest.json": MANIFEST}),
        "run_config": vars(args),
        "output_dir": str(INT8_DIR.relative_to(REPO_ROOT)).replace("\\", "/"),
        "summary": {
            "models_accepted": usable,
            "models_rejected": [key for key, entry in models.items() if entry["status"] == "rejected"],
            "models_unmeasured": [key for key, entry in models.items() if entry["status"] == "unmeasured"],
            "accuracy_claim_reportable": reportable,
            "accuracy_claim_note": (
                "models outside 'accuracy_claim_reportable' have a held-out split too small to "
                "support a published accuracy number; their INT8 artifacts may still be shipped, "
                "but the paper must not quote their accuracy"
            ),
            "total_int8_mb": round(
                sum(models[key]["size"]["int8_mb"] for key in usable),
                3,
            ),
            "total_fp32_mb": round(
                sum(models[key]["size"]["fp32_mb"] for key in usable),
                3,
            ),
        },
        "models": models,
    }
    write_json(REPORT, payload)
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
