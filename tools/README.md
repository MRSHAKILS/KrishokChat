# Tools — Script Taxonomy

All offline, demo, and build scripts consolidated from three former homes:
`scripts/` (root) + `backend/scripts/` + `backend/ml_assets/{rag_index,vision}/scripts/`.

> **Rule:** `backend/scripts/` keeps only **runtime-adjacent** scripts that import `app.*` (`replay_golden.py`, `test_*` that hit the container). Everything else lives here, behind no import.

## Layout

| Folder | Source | Purpose | How to run |
|--------|--------|---------|------------|
| `tools/build/` | `scripts/build_rag_index.py`, `export_yolo_models.py`, `scripts/prewarm_demo_cache.py` | Build RAG index, export YOLO ONNX, prewarm demo cache | `python tools/build/build_rag_index.py` / `python backend/scripts/prewarm_demo_cache.py` |
| `tools/demo/` | `scripts/capture_*.js`, `perfect_*.py`, `render_demo_video.py`, `verify_demo_assets.py`, `debug_stream.py`, `test_detection.py`, `test_qa_cases.py` etc | Demo capture, perfect screenshots, stream debug, manual QA probes | `node tools/demo/capture_key_workflows.js` / `python tools/demo/perfect_detect.py` |
| `tools/poster/` | `scripts/generate_*`, `write_poster.py`, `prepare_hf_staging.py`, `upload_folder_hf.py` | Poster/brochure generation, scientific figures, HF staging | `python tools/poster/generate_architecture_fig.py` |
| `tools/ops/` | `scripts/start_*.ps1`, `local_model.ps1`, `supabase_test_user.ps1` | One-command ops: start prod, local model, Supabase test user | `powershell -File tools/ops/start_prod.ps1` |
| `tools/soil/` | `scripts/build_soil_release.py` | Soil dataset release builder | `python tools/soil/build_soil_release.py` |
| `tools/rag/` | `backend/ml_assets/rag_index/scripts/` (29 files, `00_*` … `14_*`) | RAG corpus preprocessing, BM25/FAISS build, term map, golden set, coverage analysis | `python tools/rag/02_build_bm25.py` |
| `tools/vision/` | `backend/ml_assets/vision/scripts/` (4 files) | Vision model verification & test matrices | `python tools/vision/01_verify_models.py` |
| `backend/scripts/` | **stays** | Runtime-adjacent: `replay_golden.py`, `test_bm25_retrieval.py`, `test_full_pipeline.py` etc (import `app.*`) | `uv run python backend/scripts/replay_golden.py` |
| `scripts/` | **stays (minimal)** | Only `Modelfile` (canonical per H4, hardlinked to `backend/ml_assets/gemma/Modelfile`) | `ollama create krishoktech-4b -f scripts/Modelfile` |

## Migration notes (Hygiene → Structure)

* **H1-H7** (hygiene) saved 1.32 GB + deduped media/GGUF/Modelfile.
* **S1** (this step) moved 67 files via `git mv` (no content change) — 33 from `scripts/`, 29 from `backend/ml_assets/rag_index/scripts/`, 4 from `backend/ml_assets/vision/scripts/`, plus `prewarm_demo_cache.py`.
* **S2** (next) will rename `tools/rag/00_*` → descriptive names (`00_analyze_refined.py` → `analyze_refined_corpus.py` etc) and keep a map in `tools/rag/README.md`.

## Verification after S1

```powershell
uv run python -m compileall -q app
uv run pytest tests/test_storage_sqlite.py tests/test_health_readiness.py -q
uv run python backend/scripts/replay_golden.py  # 50/50
pnpm --dir frontend build  # if frontend changed
```

All moved scripts still run from their new paths; old paths are gone (no shim — update any docs that reference them).
