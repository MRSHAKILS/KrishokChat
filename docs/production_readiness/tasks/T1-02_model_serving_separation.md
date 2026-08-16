# T1-02 — Model Serving Separation (Vision ONNX Path + Model Registry)

- **Status:** BLOCKED — amendment review required (see below)
- **Tier:** 1 (post-capstone)
- **Depends on:** nothing (ONNX export script already exists: `scripts/export_yolo_models.py`)
- **Blocks:** deployment sizing (T1-03)
- **Amendment:** REVIEW REQUIRED — the local-LLM sidecar is already sanctioned by amendment `14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`; this task extends that pattern and must confirm it. No new hard-rule change expected.

## Goal

Stop bundling the ~3 GB training stack (torch + torchvision + ultralytics + sentence-transformers) into the API process: the chat path must never import torch; vision runs fully on the ONNX exports; and model artifacts become registry-verified (sha256 + GGUF metadata checks) so a wrong/truncated artifact can never silently serve a demo or production run.

## Read first

- `backend/app/services/yolo_service.py` (or the vision adapter under `infrastructure/vision/`) — where ultralytics is imported.
- `scripts/export_yolo_models.py` — current export flow and which `.pt` → `.onnx` pairs exist under `backend/ml_assets/yolo/`.
- `backend/app/core/config.py` — model path settings.
- `backend/ml_assets/` — what artifacts exist (yolo, classifier, rag_index, gemma GGUF).
- The paper planning docs' model-verification practice (GGUF metadata checks / claim ledger) — mirror it in code here.

## Invariants (do not break)

- The checked-in artifacts are `task: classify` — never claim bounding-box detection (AGENTS.md artifact-reality note).
- The classifier-first → crop-specific routing flow is unchanged.
- ONNX inference must produce identical top-1 results to the `.pt` path on the same inputs (regression test on fixture images).
- The locked Ultralytics/ONNX direction stays (AGENTS.md §3) — this task completes it, doesn't replace it.
- If any `.pt` lacks an `.onnx` export, the vision adapter falls back to the current behavior with a warning — never a crash.

## Design

- **Lazy loading:** move `import ultralytics`/`torch` inside the vision adapter's initialization (imported only when a vision request arrives); the chat/QA import graph must not touch them. Verify with a fresh interpreter import test.
- **ONNX-first:** vision adapter prefers `ml_assets/yolo/<crop>.onnx` (onnxruntime); `.pt` becomes the fallback. Export any missing ONNX files (rerun the existing export script; confirm the ONNX runtime version against a fresh internet search — AGENTS.md §2.7).
- **Model registry:** `backend/ml_assets/model_registry.json` — entries: name, path, sha256, task (`classify`), source, verified date. `backend/scripts/verify_model_artifacts.py` recomputes hashes and (for GGUF) checks metadata fields; exits non-zero on mismatch. Wire it as a startup check that **warns, not crashes** (demo protection) and as a CI job.
- **Sidecar note:** the local-LLM lane already runs as `llama-server` under the sanctioned amendment — document the process boundary in this task's README note; do not run a second server here.

## Scope — create

- `backend/scripts/verify_model_artifacts.py`
- `backend/ml_assets/model_registry.json`
- `backend/tests/test_vision_onnx.py` (ONNX top-1 equals .pt top-1 on fixture images; registry hashes match; chat import graph contains no torch/ultralytics)

## Scope — modify

- vision adapter (`infrastructure/vision/`) — lazy imports + ONNX-first
- `backend/app/core/config.py` (+ `VISION_BACKEND=onnx|auto` default `auto`), `.env.example`
- CI workflow (T0-08) — add artifact-verification job

## Do not touch

- Classifier/crop-routing logic, QA pipeline, safety pipeline
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`

## Rollback

1. `VISION_BACKEND=pt` (or `auto` falling back) → restart → current behavior.
2. Commit revert (bounded).

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_vision_onnx.py -v` — green.
2. `uv run python backend/scripts/verify_model_artifacts.py` — passes; then corrupt one hash entry → exits non-zero (prove the gate bites).
3. Fresh interpreter: `uv run python -c "import app.main; import sys; assert 'torch' not in sys.modules"` — passes.
4. Classify endpoint: same fixture image → same top-1 crop via ONNX path.
5. Chat QA smoke unchanged; memory footprint reduced (measure RSS before/after if convenient; note in commit).

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Registry entries note verification date and source; commit message lists open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Any `.pt` without an ONNX export (export them or document the fallback).
- onnxruntime version confirmation via internet search before adding.