"""V2 - measure the REAL ``.pt`` serving path (accuracy, latency, routing).

This is what the deployed backend actually does today:
``app/infrastructure/vision/ultralytics_classifier.py`` calls ``YOLO(model.pt)``. No ONNX
file is loaded anywhere in the running system, so this baseline is required under every
claim option in ``state/TASK_VISION_ONNX.md`` - including Option A.

Two measurements, deliberately separated:

1. **Per-model classification** - drives ``UltralyticsClassificationRunner`` +
   ``ArtifactVisionRegistry`` directly, bypassing FastAPI, so the number isolates model
   inference. Reports top-1 / top-3, per-class P/R/F1, confusion matrix, and
   single-image latency percentiles after warm-up.
2. **End-to-end routing** - drives ``VisionPipeline.detect()`` over the same manifest to
   capture what the paper actually wants to describe: the full tri-state crop gate
   (OOD threshold, confidence threshold 0.60, margin threshold, confusion-family risk),
   per-disease calibrated thresholds (base 0.55), second-image recovery, the
   ``VisionStatus`` distribution, and hint-on vs hint-off behavior. (The wheat->rice
   mitigation is a dead branch under the current 10-class router — counted, not firing.)
   A deterministic stub LLM is injected so no live model server is needed; ``crop_hint``
   on and off are reported separately because the hint path bypasses the crop classifier
   entirely.

Every number here is measured in this run. Unmeasurable quantities (corn) are emitted as
``{"status": "unmeasured", ...}`` per AGENTS.md rule 5.

Run:
    .\\backend\\.venv\\Scripts\\python.exe "paper/EACL Demo/experiments/E02_multimodal_diagnostic_workflow/scripts/run_real_e02a_pt_baseline.py"

Optional flags:
    --limit-per-class N   cap images per class (smoke runs only; recorded in output)
    --latency-runs N      timed single-image inferences per model (default 200)
    --skip-pipeline       classification only, no VisionPipeline.detect() pass
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import tempfile
import time
from collections import Counter, defaultdict
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

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
    provenance,
    sha256_of,
    write_json,
)

ensure_backend_importable()

from PIL import Image  # noqa: E402

MANIFEST = Path(r"D:\KrishokChat Advisory System\paper\EACL Demo\experiments\E02_multimodal_diagnostic_workflow\vision_eval_manifest.json")
OUTPUT = Path(r"D:\KrishokChat Advisory System\paper\EACL Final\experiments\results\n04_pt_baseline_20260917.json")

WARMUP_RUNS = 10
DEFAULT_LATENCY_RUNS = 200


# --------------------------------------------------------------------------------------
# Deterministic stub LLM (test-only double, mirrors backend/tests/test_smoke_qa_pipeline.py)
# --------------------------------------------------------------------------------------
class StubLLM:
    """Offline AnswerGenerator port double. Never used in production."""

    name = "e02-offline-stub"

    async def generate(self, query: str, context, sources: list[Any]) -> Any:
        from app.application.generation import REFERRAL, GenerationResult

        if not sources:
            return GenerationResult(answer=REFERRAL, model=self.name, mode="no_sources", error="No sources")
        return GenerationResult(
            answer="[offline stub advisory: grounded in retrieved sources]",
            used_source_ids=tuple(source.id for source in sources),
            model=self.name,
            mode="grounded",
        )

    async def stream(self, query: str, context, sources: list[Any]) -> AsyncIterator[str]:
        from app.application.generation import REFERRAL

        yield "[offline stub advisory: grounded in retrieved sources]" if sources else REFERRAL

    async def generate_from_text(self, answer: str, sources: list[Any], *, mode: str) -> Any:
        from app.application.generation import REFERRAL, GenerationResult

        return GenerationResult(
            answer=answer.strip() or REFERRAL,
            used_source_ids=tuple(source.id for source in sources),
            model=self.name,
            mode=mode,
        )


class _DeterministicSafety:
    """Real ``precheck`` rules, no LLM call. Keeps the safety stage honest and offline."""

    async def classify(self, query: str, context) -> Any:
        from app.domain.contracts import SafetyDecision
        from app.domain.enums import SafetyCategory
        from app.domain.safety_policy import precheck

        match = precheck(query)
        if match:
            category, rules = match
            return SafetyDecision(
                category=category,
                confidence=1.0,
                reason="Deterministic safety rule matched",
                matched_rules=rules,
                requires_escalation=category is SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
                response=None,
            )
        return SafetyDecision(
            category=SafetyCategory.SAFE_AGRI,
            confidence=1.0,
            reason="no deterministic rule matched",
            matched_rules=(),
            requires_escalation=False,
            response=None,
        )


# --------------------------------------------------------------------------------------
# Metrics (computed, never tabulated)
# --------------------------------------------------------------------------------------
def _classification_metrics(labels: list[str], truth: list[str], predicted: list[str], top3: list[list[str]]) -> dict[str, Any]:
    n = len(truth)
    correct = sum(1 for t, p in zip(truth, predicted) if t == p)
    top3_correct = sum(1 for t, candidates in zip(truth, top3) if t in candidates)

    matrix = {t: {p: 0 for p in labels} for t in labels}
    for t, p in zip(truth, predicted):
        if t in matrix and p in matrix[t]:
            matrix[t][p] += 1

    per_class: dict[str, Any] = {}
    macro_f1: list[float] = []
    for label in labels:
        tp = sum(1 for t, p in zip(truth, predicted) if t == label and p == label)
        fp = sum(1 for t, p in zip(truth, predicted) if t != label and p == label)
        fn = sum(1 for t, p in zip(truth, predicted) if t == label and p != label)
        support = tp + fn
        precision = tp / (tp + fp) if (tp + fp) else None
        recall = tp / support if support else None
        if precision is not None and recall is not None and (precision + recall) > 0:
            f1: float | None = 2 * precision * recall / (precision + recall)
        elif support == 0 and (tp + fp) == 0:
            f1 = None
        else:
            f1 = 0.0
        if support:
            macro_f1.append(f1 if f1 is not None else 0.0)
        per_class[label] = {
            "support": support,
            "predicted_as": tp + fp,
            "precision": round(precision, 4) if precision is not None else None,
            "recall": round(recall, 4) if recall is not None else None,
            "f1": round(f1, 4) if f1 is not None else None,
        }

    return {
        "n": n,
        "top1_correct": correct,
        "top1_accuracy": round(correct / n, 4) if n else None,
        "top3_correct": top3_correct,
        "top3_accuracy": round(top3_correct / n, 4) if n else None,
        "macro_f1": round(sum(macro_f1) / len(macro_f1), 4) if macro_f1 else None,
        "per_class": per_class,
        "confusion_matrix": matrix,
    }


def _load_manifest() -> dict[str, Any]:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}; run build_vision_eval_manifest.py first")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


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


# --------------------------------------------------------------------------------------
# Measurement 1: per-model classification
# --------------------------------------------------------------------------------------
def measure_disease_models(rows: list[dict[str, Any]], runner, registry, latency_runs: int) -> dict[str, Any]:
    results: dict[str, Any] = {}
    specs = registry.disease_models

    for model_key in DISEASE_MODEL_KEYS:
        model_rows = [row for row in rows if row.get("disease_model") == model_key]
        labels = list(class_names(model_key))
        if not model_rows:
            results[model_key] = {
                "status": "unmeasured",
                "reason": "no local labelled test images",
                "n_classes": len(labels),
                "train_imgsz": checkpoint_imgsz(model_key),
            }
            print(f"  {model_key:9s} UNMEASURED (no local labelled test images)")
            continue

        spec = specs[model_key]
        truth: list[str] = []
        predicted: list[str] = []
        top3: list[list[str]] = []
        confidences: list[float] = []
        per_image: list[dict[str, Any]] = []
        errors: list[str] = []

        # Warm-up: the first YOLO() call builds the graph lazily and dominates a cold p50.
        warm_image = Image.open(REPO_ROOT / model_rows[0]["path"]).convert("RGB")
        for _ in range(WARMUP_RUNS):
            runner.predict(spec, warm_image)

        for row in model_rows:
            image = Image.open(REPO_ROOT / row["path"]).convert("RGB")
            try:
                prediction = runner.predict(spec, image)
            except Exception as exc:  # noqa: BLE001 - recorded, never silently dropped
                errors.append(f"{row['path']}: {exc}")
                continue
            candidates = [str(entry["class"]) for entry in prediction.top3]
            truth.append(row["label"])
            predicted.append(prediction.label)
            top3.append(candidates)
            confidences.append(prediction.confidence)
            per_image.append(
                {
                    "path": row["path"],
                    "truth": row["label"],
                    "predicted": prediction.label,
                    "confidence": prediction.confidence,
                    "correct": row["label"] == prediction.label,
                }
            )

        metrics = _classification_metrics(labels, truth, predicted, top3)

        # Latency on a single fixed image, single-batch: the production request shape.
        timings: list[float] = []
        for _ in range(latency_runs):
            start = time.perf_counter()
            runner.predict(spec, warm_image)
            timings.append((time.perf_counter() - start) * 1000.0)

        thresholded = sum(1 for value in confidences if value >= 0.55)
        results[model_key] = {
            "status": "measured",
            "runtime": "pytorch .pt via ultralytics YOLO()",
            "artifact": str((model_dir(model_key) / "model.pt").relative_to(REPO_ROOT)).replace("\\", "/"),
            "artifact_sha256": sha256_of(model_dir(model_key) / "model.pt"),
            "train_imgsz": checkpoint_imgsz(model_key),
            "n_classes": len(labels),
            "accuracy": metrics,
            "confidence": {
                "mean": round(sum(confidences) / len(confidences), 4) if confidences else None,
                "min": round(min(confidences), 4) if confidences else None,
                "max": round(max(confidences), 4) if confidences else None,
                "at_or_above_disease_threshold_0_55": thresholded,
                "fraction_at_or_above_threshold": round(thresholded / len(confidences), 4) if confidences else None,
            },
            "latency_single_image": {
                "warmup_runs": WARMUP_RUNS,
                "timed_runs": latency_runs,
                "image": model_rows[0]["path"],
                **percentiles(timings),
            },
            "inference_errors": errors,
            "per_image": per_image,
        }
        print(
            f"  {model_key:9s} n={metrics['n']:<4d} top1={metrics['top1_accuracy']} "
            f"top3={metrics['top3_accuracy']} macroF1={metrics['macro_f1']} "
            f"p50={results[model_key]['latency_single_image']['p50_ms']}ms"
        )
    return results


def measure_crop_classifier(rows: list[dict[str, Any]], runner, registry, latency_runs: int) -> dict[str, Any]:
    """Crop-level accuracy: manifest family truth vs current species predictions.

    The frozen manifest labels crops at FAMILY level (Potato/Rice/Brassica/...) while the
    current 10-class checkpoint predicts SPECIES (Cabbage/Chili/...). Exact-match top-1 over
    all rows therefore measures label-space agreement, NOT router quality. The species-level
    per_crop_family_predictions breakdown is the informative figure; Wheat rows (no router
    class) are out-of-space by construction.
    """
    labels = list(class_names("crop_classifier"))
    spec = registry.crop_classifier

    in_space = [row for row in rows if row.get("expected_crop_label")]
    out_space = [row for row in rows if row.get("expected_crop_label") is None]

    warm_image = Image.open(REPO_ROOT / in_space[0]["path"]).convert("RGB")
    for _ in range(WARMUP_RUNS):
        runner.predict(spec, warm_image)

    truth: list[str] = []
    predicted: list[str] = []
    top3: list[list[str]] = []
    per_family: dict[str, Counter[str]] = defaultdict(Counter)
    errors: list[str] = []

    for row in in_space:
        image = Image.open(REPO_ROOT / row["path"]).convert("RGB")
        try:
            prediction = runner.predict(spec, image)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{row['path']}: {exc}")
            continue
        truth.append(row["expected_crop_label"])
        predicted.append(prediction.label)
        top3.append([str(entry["class"]) for entry in prediction.top3])
        per_family[row["crop_family"]][prediction.label] += 1

    out_of_space_predictions: Counter[str] = Counter()
    for row in out_space:
        image = Image.open(REPO_ROOT / row["path"]).convert("RGB")
        try:
            prediction = runner.predict(spec, image)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{row['path']}: {exc}")
            continue
        out_of_space_predictions[prediction.label] += 1

    timings: list[float] = []
    for _ in range(latency_runs):
        start = time.perf_counter()
        runner.predict(spec, warm_image)
        timings.append((time.perf_counter() - start) * 1000.0)

    return {
        "status": "measured",
        "runtime": "pytorch .pt via ultralytics YOLO()",
        "artifact": str((model_dir("crop_classifier") / "model.pt").relative_to(REPO_ROOT)).replace("\\", "/"),
        "artifact_sha256": sha256_of(model_dir("crop_classifier") / "model.pt"),
        "train_imgsz": checkpoint_imgsz("crop_classifier"),
        "label_space": labels,
        "label_space_note": (
            "Manifest truth is family-level; current checkpoint predicts 10 species-level "
            "labels (Cabbage..Tomato incl. Rice; no Wheat/Corn class). Exact-match top-1 mixes "
            "label spaces — see per_crop_family_predictions for the species breakdown and "
            "out_of_label_space for Wheat rows. Do not report top-1 as router quality."
        ),
        "in_label_space": _classification_metrics(labels, truth, predicted, top3),
        "per_crop_family_predictions": {family: dict(counts) for family, counts in sorted(per_family.items())},
        "out_of_label_space": {
            "n": len(out_space),
            "families": sorted({row["crop_family"] for row in out_space}),
            "prediction_distribution": dict(out_of_space_predictions),
            "note": "Wheat rows have no correct answer in the current 10-species router space (no Wheat class); distribution only",
        },
        "latency_single_image": {
            "warmup_runs": WARMUP_RUNS,
            "timed_runs": latency_runs,
            "image": in_space[0]["path"],
            **percentiles(timings),
        },
        "inference_errors": errors,
    }


# --------------------------------------------------------------------------------------
# Measurement 2: end-to-end VisionPipeline routing
# --------------------------------------------------------------------------------------
def build_vision_pipeline():
    from app.application.qa_pipeline import QAPipeline
    from app.application.verifier import HardenedDosageVerifier
    from app.application.vision_pipeline import VisionPipeline
    from app.infrastructure.audit.jsonl import JSONLAuditSink
    from app.infrastructure.retrieval.bm25 import BM25Retriever
    from app.infrastructure.sessions.memory import InMemorySessionStore
    from app.infrastructure.vision.registry import ArtifactVisionRegistry
    from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner

    backend = REPO_ROOT / "backend"
    index = backend / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
    corpus = backend / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
    if not index.exists() or not corpus.exists():
        raise SystemExit(f"missing BM25 index/corpus: {index} / {corpus}")

    audit_path = Path(tempfile.gettempdir()) / "krishokchat_e02_pt_baseline_audit.jsonl"
    qa = QAPipeline(
        safety=_DeterministicSafety(),
        retriever=BM25Retriever(index_path=index, corpus_path=corpus),
        generator=StubLLM(),
        verifier=HardenedDosageVerifier(),
        audit=JSONLAuditSink(audit_path),
        sessions=InMemorySessionStore(max_turns=10, ttl_seconds=1800),
        top_k=5,
    )
    registry = ArtifactVisionRegistry(VISION_DIR)
    runner = UltralyticsClassificationRunner()
    pipeline = VisionPipeline(
        registry=registry,
        runner=runner,
        qa=qa,
        audit=JSONLAuditSink(audit_path),
    )
    return pipeline, registry, runner, index, corpus, audit_path


async def _detect_all(pipeline, rows: list[dict[str, Any]], *, crop_hint: bool) -> dict[str, Any]:
    from app.domain.vision import VisionStatus

    status_counts: Counter[str] = Counter()
    per_family_status: dict[str, Counter[str]] = defaultdict(Counter)
    latencies: list[float] = []
    disease_correct = 0
    disease_scored = 0
    crop_rewrites = 0
    crop_source_counts: Counter[str] = Counter()
    below_crop_threshold = 0
    below_disease_threshold = 0
    no_disease_model_expected_correct = 0
    no_disease_model_expected_total = 0
    rows_out: list[dict[str, Any]] = []

    hint_for_family = {"Potato": "potato", "Rice": "rice", "Cabbage": "brassica", "Cauliflower": "brassica"}

    for row in rows:
        image = Image.open(REPO_ROOT / row["path"]).convert("RGB")
        hint = hint_for_family.get(row["crop_family"]) if crop_hint else None
        if crop_hint and hint is None:
            continue
        start = time.perf_counter()
        result = await pipeline.detect(image, crop_hint=hint)
        elapsed = (time.perf_counter() - start) * 1000.0
        latencies.append(elapsed)

        status = result.status.value
        status_counts[status] += 1
        per_family_status[row["crop_family"]][status] += 1
        crop_source_counts[result.crop_source] += 1

        if result.status is VisionStatus.NOT_RECOGNIZED:
            if result.disease is None:
                below_crop_threshold += 1
            else:
                below_disease_threshold += 1

        if row.get("has_disease_model") is False:
            no_disease_model_expected_total += 1
            if result.status is VisionStatus.NO_DISEASE_MODEL:
                no_disease_model_expected_correct += 1

        if row.get("disease_model") and result.disease is not None:
            disease_scored += 1
            if result.disease == row["label"]:
                disease_correct += 1

        # The wheat->rice mitigation rewrites the reported crop when the rice model wins.
        if not crop_hint and row["crop_family"] == "Rice" and result.crop == "Rice":
            crop_rewrites += 1

        rows_out.append(
            {
                "path": row["path"],
                "truth_label": row["label"],
                "crop_family": row["crop_family"],
                "crop_hint": hint,
                "status": status,
                "crop": result.crop,
                "crop_confidence": result.crop_confidence,
                "crop_source": result.crop_source,
                "disease": result.disease,
                "disease_confidence": result.disease_confidence,
                "treatment_confidence": result.treatment_confidence,
                "latency_ms": round(elapsed, 3),
            }
        )

    return {
        "crop_hint": "on" if crop_hint else "off",
        "crop_hint_note": (
            "crop_hint bypasses the 10-class crop classifier entirely; hint-on and hint-off "
            "numbers are not comparable and are reported separately"
        ),
        "n": len(rows_out),
        "status_distribution": dict(status_counts),
        "status_by_crop_family": {family: dict(counts) for family, counts in sorted(per_family_status.items())},
        "crop_source_distribution": dict(crop_source_counts),
        "threshold_effects": {
            "crop_threshold": 0.60,
            "disease_threshold": 0.55,
            "not_recognized_at_crop_stage": below_crop_threshold,
            "not_recognized_at_disease_stage": below_disease_threshold,
        },
        "routed_disease_accuracy": {
            "n_with_disease_prediction": disease_scored,
            "correct": disease_correct,
            "accuracy": round(disease_correct / disease_scored, 4) if disease_scored else None,
            "note": "end-to-end: includes crop routing errors, so lower than per-model accuracy",
        },
        "no_disease_model_handling": {
            "n_expected": no_disease_model_expected_total,
            "n_correct": no_disease_model_expected_correct,
            "accuracy": (
                round(no_disease_model_expected_correct / no_disease_model_expected_total, 4)
                if no_disease_model_expected_total
                else None
            ),
        },
        "wheat_rice_mitigation": {
            "rice_images_reported_as_rice": crop_rewrites,
            "note": (
                "LEGACY dead branch (vision_pipeline.py): the wheat->rice rewrite fires only when "
                "the classifier predicts Wheat, which the current 10-class router cannot output. "
                "Counted value reflects normal Rice->rice routing, not mitigation fires. Removal "
                "pending P0-11 review."
            ),
        },
        "latency_end_to_end": {
            "includes": "crop classify + disease classify + BM25 retrieval + stub LLM + verifier",
            "excludes": "real LLM generation (offline stub) and FastAPI/HTTP overhead",
            **percentiles(latencies),
        },
        "per_image": rows_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit-per-class", type=int, default=None)
    parser.add_argument("--latency-runs", type=int, default=DEFAULT_LATENCY_RUNS)
    parser.add_argument("--skip-pipeline", action="store_true")
    args = parser.parse_args()

    manifest = _load_manifest()
    rows = _select(manifest["images"], args.limit_per_class)
    print(f"manifest rows: {len(manifest['images'])}, selected: {len(rows)}")

    pipeline, registry, runner, index, corpus, audit_path = build_vision_pipeline()

    print("per-model classification (.pt serving path):")
    disease = measure_disease_models(rows, runner, registry, args.latency_runs)
    crop = measure_crop_classifier(rows, runner, registry, args.latency_runs)
    print(f"  crop      n={crop['in_label_space']['n']} top1={crop['in_label_space']['top1_accuracy']}")

    routing: dict[str, Any]
    if args.skip_pipeline:
        routing = {"status": "skipped", "reason": "--skip-pipeline"}
    else:
        print("end-to-end VisionPipeline.detect() ...")
        hint_off = asyncio.run(_detect_all(pipeline, rows, crop_hint=False))
        print(f"  hint off: n={hint_off['n']} statuses={hint_off['status_distribution']}")
        hint_on = asyncio.run(_detect_all(pipeline, rows, crop_hint=True))
        print(f"  hint on : n={hint_on['n']} statuses={hint_on['status_distribution']}")
        routing = {"crop_hint_off": hint_off, "crop_hint_on": hint_on}

    payload = {
        "layer": "E02_multimodal_diagnostic_workflow",
        "artifact": "results_real_pt_baseline",
        "schema_version": 1,
        "supersedes": "results.json / results.yaml (constant-table simulation, see state/STATE.md section 2)",
        "provenance": provenance(
            Path(__file__),
            inputs={
                "vision_eval_manifest.json": MANIFEST,
                "bm25_index.pkl": index,
                "knowledge_nodes_clean.jsonl": corpus,
            },
        ),
        "run_config": {
            "limit_per_class": args.limit_per_class,
            "latency_runs": args.latency_runs,
            "warmup_runs": WARMUP_RUNS,
            "skip_pipeline": args.skip_pipeline,
            "images_selected": len(rows),
            "task": "classify",
            "task_note": "classification only; no detection artifact exists, so no boxes are produced or implied",
            "llm": "offline deterministic stub (no live model server); advisory text is not evaluated here",
            "retrieval": "BM25 only (dense retrieval needs OPENROUTER_API_KEY)",
            "audit_sink": str(audit_path),
        },
        "crop_classifier": crop,
        "disease_models": disease,
        "end_to_end_routing": routing,
    }
    write_json(OUTPUT, payload)
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
