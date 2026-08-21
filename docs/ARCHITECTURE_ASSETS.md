# Architecture Assets — Canonical Map

**Date:** 2026-08-21  
**SSOT for asset provenance:** this file + `backend/ml_assets/README.md` + per-artifact `verification_report_live.md`.

> Every large binary below is **gitignored** and verified via hash / `verification_report_live.md`. Do not commit `*.pt`, `*.onnx`, `*.gguf`, `*.faiss` blobs. Only small manifests (`.json`, `.pkl` indexes <20 MB) are tracked where noted.

## 1. RAG Corpus & Indexes — `backend/ml_assets/rag_index/`

| Asset | Path | Size | Git | Provenance | Verifier |
|-------|------|------|-----|------------|----------|
| **Knowledge nodes (clean)** | `processed/knowledge_nodes_clean.jsonl` | ~? (2120 nodes) | tracked | 2,946 MD sources → cleaned → `manifest.json` + `provenance/manifest_*.json` | `logs/cleaning_report.json`, `logs/refinement_log.json` |
| **BM25 corpus tokens** | `indexes/bm25_corpus_tok.pkl` | 4.7 MB | tracked | Built from clean nodes via `tools/rag/02_build_bm25.py` | `logs/bm25_build_report.json` |
| **BM25 index** | `indexes/bm25_index.pkl` | 17 MB | tracked | `rank-bm25` `k1=2.2 b=0.4` | same |
| **Dense embeddings** | `indexes/embeddings.npy` | 8.7 MB | tracked | mE5-small 384d via `tools/rag/03_build_embeddings*` | `eval/quality_summary.json` |
| **FAISS index** | `indexes/nodes.faiss` | 8.7 MB | tracked | `IndexFlatIP` exact | `indexes/index_sha256.txt` (109 B) |
| **Node IDs** | `indexes/node_ids.json` | 52 KB | tracked | Maps FAISS row → node id | — |
| **Term map** | `indexes/term_map.json` | ? | tracked | Bengali query expansion | `tools/rag/05_build_term_map.py` |
| **Index SHA256** | `indexes/index_sha256.txt` | 109 B | tracked | Pins index version for `CORPUS_VERSION` | `P0-7` cache versioning |
| **Eval artifacts** | `eval/*.json(l)` | 0.5–5 MB | tracked | `farmer_benchmark_1000.jsonl`, `coverage_gaps_v1.json`, `golden_retrieval_probe.json` | never computed live |
| **Source MD** | `source_md/{BARC,BARI,BRRI,DAE,…}` | 2,946 MD | tracked | 13 institutions (BARC/BARI/DAE/CABI…) | `provenance/` manifests |
| **Manifest** | `manifest.json` | 2.5 KB | ignored | Build metadata | — |
| **Raw nodes** | `raw/knowledge_nodes.json` | ? | .gitkeep only | Raw before cleaning | — |

**Build pipeline (tools/rag/):** `01_clean_and_normalize` → `02_build_bm25` → `03_build_embeddings` → `05_build_term_map` → `06_build_faiss` → `07_hybrid_smoke` → `08_build_golden_set` → `11_publish_golden_stats` (→ `frontend/src/lib/golden_stats.json`). All via `tools/README.md`.

## 2. Vision Models — `backend/ml_assets/vision/`

All checkpoints verified as `task: classify` (see `verification_report_live.md` + `verification_report.json`). **Do not claim bounding boxes.**

| Model | Path | Classes | Size | Git | Provenance |
|-------|------|---------|------|-----|------------|
| **crop_classifier** | `vision/crop_classifier/model.pt` | 6 families (Brassica/Corn/GourdGuava/Potato/Solanacea/Wheat) | ~? | ignored (`*.pt`) | `class_names.json` + `verification_report_live.md` |
| **rice_disease** | `vision/rice_disease/model.pt` | 8 (BLB/Brown Spot/Healthy/Leaf Blast/…) | ~? | ignored | `class_names.json` + `disease_details.json` |
| **corn_disease** | `vision/corn_disease/model.pt` | 4 | ~? | ignored | `class_names.json` |
| **potato_disease** | `vision/potato_disease/model.pt` | 3 (Early/Late/Healthy) | ~? | ignored | `class_names.json` |
| **brassica_disease** | `vision/brassica_disease/model.pt` | 11 (cabbage×4/cauliflower×7) | ~? | ignored | `class_names.json` |
| **wheat_disease** | `vision/wheat_disease/model.pt` | 11 | 9.4 MB | ignored | `class_names.json` + `metadata.json` + live sweep 44/50 (88%) |
| **test_images** | `vision/test_images/**` | ~? | ignored? (large) | 437-image library sweep: 436/437 got Bengali disease info (99.8%) | `test_images/test_matrix_results.json` |

**ONNX export path** (`backend/ml_assets/yolo/*.onnx`) exists for future detection but **no detection weights are checked in** — `yolo/` is `.gitkeep` only.

**Tools:** `tools/vision/01_verify_models.py`, `02_test_endpoints.py`, `03_test_matrix.py`, `04_test_wheat_matrix.py` → `docs/vision-pipeline/`.

## 3. Soil Moisture — `backend/ml_assets/soil/` + `dataset_release/`

| Asset | Path | Size | Git | Provenance |
|-------|------|------|-----|------------|
| **5-fold EfficientNet-B0** | `ml_assets/soil/effnetb0_fold{0..4}.pt` | 5×16.9 MB = 84.7 MB | ignored (`*.pt`) | Trained on `dataset_release/soil-moisture-detection/` (kebab, H6), `Runed_soil_effnetB0.ipynb` |
| **OOF predictions** | `ml_assets/soil/oof_predictions.csv` | 178 KB | ignored? | 5-fold OOF |
| **Scatter plot** | `ml_assets/soil/pred_vs_actual.png` | 216 KB | ignored? | — |
| **Frozen release (722 imgs)** | `dataset_release/soil_moisture/` | ~? | **tracked** (small, committed) | `reports/PHASE0_AUDIT_REPORT.md`, `reports/preprocessing_report.md`, `image_manifest.csv`, `series_map.json`, `thumbnails/` |
| **Kaggle workspace (956 MB raw)** | `dataset_release/soil-moisture-detection/` | 956 MB | **gitignored** (`dataset/raw` etc per `.gitignore`) | Raw/intermediate, not for git; official release is `soil_moisture/` |

**H6:** spaced folder `Soil Moisture Detection` → `soil-moisture-detection` (kebab-case).

## 4. Local LLM — `backend/ml_assets/gemma/`

| Asset | Path | Size | Git | Provenance | Note |
|-------|------|------|-----|------------|------|
| **Canonical GGUF** | `gemma/krishokchat.f16.gguf` | 1.36 GB | **ignored** (`*.gguf`) | SHA256 `1D627304F74520284844812600F5F0E172240C8A23C88126BA7D1C1F73B84673` | Truncated — **must not be served** (see `PROJECT_HANDOFF.md` + amendment 14) |
| **Alias** | `gemma/model.gguf` | 1.36 GB | ignored | **Hardlink** to `krishokchat.f16.gguf` (2 entries, 0 extra space, H2) | `config.py:gguf_path` default |
| **Modelfile (canonical)** | `gemma/Modelfile` | 1.9 KB | tracked | `FROM ./model.gguf`, hardlinked to `scripts/Modelfile` (H4) | `scripts/Modelfile` is SSOT |
| **Modelfile variant** | `gemma/Modelfile.krishokchat` | 2.5 KB | tracked | `FROM gemma3:4b`, archived variant | Not used by `tools/ops/local_model.ps1` |
| **Raw checkpoint** | `gemma/raw/checkpoint-4020/` | ~300 MB | ignored (`gemma/raw/`) | LoRA adapter | — |
| **Verified runtime** | — | — | — | External Q4_K_M base + LoRA via `tools/ops/start_krishokchat_local.ps1` (amendment 14), **not** the truncated `f16` | Scientific perf unevaluated |

## 5. Advisory Knowledge Map — `backend/ml_assets/advisory/`

| Asset | Path | Size | Git |
|-------|------|------|-----|
| **Disease map (Bengali)** | `advisory/disease_knowledge_map.json` | 16 KB | tracked |
| **Generated nodes** | `advisory/generated_knowledge_nodes.jsonl` | 206 KB | tracked |
| **Generation tasks** | `advisory/generation_tasks.json` | 70 KB | tracked |

Grounded in 13 institutions, used by vision pipeline for treatment advice (via `VisionPipeline` → QA pipeline).

## 6. Demo Cache — `demo-assets/`

| Asset | Path | Size | Git |
|-------|------|------|-----|
| **Cached responses** | `demo-assets/cached_responses.json` | 1.6 MB | tracked (M in soil branch) |
| **Demo media (canonical)** | `demo-assets/krishokchat_demo.{gif,mp4,webp}` | 20.7 MB + 1.0 MB + 11 KB | **tracked** (H3 deduped, hardlinked to `frontend/public/`) |
| **Soil thumbnails** | `demo-assets/images/soil/` + `thumbnails/` | ? | tracked |

`CORPUS_VERSION=2026-08` in cache keys (P0-7) — bump after index rebuild.

## 7. Git Hygiene Summary

* **Tracked (small, reproducible):** `*.json`, `*.pkl` (<20 MB), `*.faiss` (8.7 MB), `*.md`, `*.jsonl`, `*.jpg` thumbnails. Large binaries are **gitignored** and verified via `verification_report_live.md` / `PHASE0_AUDIT_REPORT.md`.
* **Ignored (large, not for git):** `*.pt`, `*.onnx`, `*.gguf`, `*.safetensors`, `*.faiss` (if >50 MB), `dataset/raw`, `gemma/raw/`, `backend/data/`, `*.log`, `__pycache__/`, `.pytest_cache/`.
* **Hardlinks (H2-H3):** `model.gguf ↔ krishokchat.f16.gguf` (2 entries), `demo-assets ↔ frontend/public` demo media (2 entries each) — zero extra working-tree space.
* **Verification:** `uv run python -m compileall -q app` + `uv run pytest` + `python backend/scripts/replay_golden.py` (50/50) + `GET /health` + `GET /readyz` after every asset move.

## 8. Pointers

* **Read first:** `AGENTS.md`, `docs/refactor/ARCHITECTURE.md`, `docs/refactor/PROJECT_HANDOFF.md`
* **Per-pipeline docs:** `docs/vision-pipeline/`, `tools/README.md`, `tools/rag/README.md`, `backend/ml_assets/gemma/README.md`
* **Asset verification:** `backend/ml_assets/vision/verification_report_live.md`, `backend/ml_assets/rag_index/eval/`, `dataset_release/soil_moisture/reports/`
