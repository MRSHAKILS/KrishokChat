# ML Assets — Storage Contract

This directory is the **single source of truth** for all model weights, indexes, and frozen datasets. Large binaries are **gitignored** — only small manifests and verified reports are tracked. See `docs/ARCHITECTURE_ASSETS.md` for the full canonical map.

## Layout

```
ml_assets/
├── advisory/          # Bengali disease knowledge map (tracked, small)
│   └── disease_knowledge_map.json
├── classifier/        # crop classifier weights (ignored, .gitkeep)
├── gemma/             # local LLM — GGUF is ignored, Modelfile is tracked
│   ├── krishokchat.f16.gguf   (ignored, canonical, 1.36 GB, hardlinked to model.gguf)
│   ├── model.gguf             (ignored, hardlink alias for config default)
│   ├── Modelfile              (tracked, hardlinked to scripts/Modelfile)
│   ├── Modelfile.krishokchat  (tracked, archived variant FROM gemma3:4b)
│   └── README.md              (this repo: H2 docs)
├── rag_index/         # RAG corpus + indexes (tracked: .pkl/.faiss/.json <20 MB)
│   ├── processed/     # knowledge_nodes_clean.jsonl (2120 nodes)
│   ├── indexes/       # bm25_*.pkl, embeddings.npy, nodes.faiss, term_map.json
│   ├── eval/          # farmer_benchmark_1000.jsonl, coverage gaps, golden probe
│   ├── source_md/     # 2,946 MD from 13 institutions (BARC/BARI/DAE/CABI…)
│   └── provenance/    # manifest_node_to_qa.json, manifest_md_to_qa.json
├── soil/              # 5-fold EfficientNet-B0 .pt (ignored, 5×16.9 MB) + OOF csv
├── vision/            # per-crop .pt (ignored) + verification_report_live.md
│   ├── crop_classifier/
│   ├── rice_disease/ corn_disease/ potato_disease/ brassica_disease/ wheat_disease/
│   └── test_images/   # 437-image library sweep
└── yolo/              # .gitkeep only — no detection weights checked in
```

## Git Contract

| Pattern | Git | Why |
|---------|-----|-----|
| `*.pt`, `*.onnx`, `*.gguf`, `*.safetensors`, `*.faiss` (>50 MB) | **ignored** | Large binaries — verify via `verification_report_live.md`, not git |
| `*.pkl`, `*.npy`, `*.faiss` (<20 MB), `*.json`, `*.csv` | **tracked** where small & reproducible | `backend/ml_assets/rag_index/indexes/` etc |
| `*.log`, `__pycache__/`, `.pytest_cache/`, `backend/data/` | ignored | Runtime litter |
| `**/.gitkeep` | tracked | Keeps empty dirs visible |

**Hardlinks (H2-H3, zero extra space):**
* `gemma/model.gguf ↔ krishokchat.f16.gguf` (2 entries, SHA `1D6273…`, `fsutil hardlink list`)
* `demo-assets/krishokchat_demo.* ↔ frontend/public/krishokchat_demo.*` (2 entries each)

**Truncation warning:** `gemma/krishokchat.f16.gguf` is truncated and must not be served (see `docs/refactor/PROJECT_HANDOFF.md` + amendment 14). Verified runtime uses external Q4_K_M base + LoRA via `tools/ops/start_krishokchat_local.ps1`.

## Verification

```powershell
# From repo root:
uv run python -m compileall -q app
uv run pytest backend/tests/test_storage_sqlite.py -q
python backend/scripts/replay_golden.py  # 50/50
curl http://localhost:8000/health; curl http://localhost:8000/readyz
```

## Pointers

* **Full map:** `docs/ARCHITECTURE_ASSETS.md`
* **RAG pipeline:** `tools/rag/README.md` + `tools/README.md`
* **Vision pipeline:** `docs/vision-pipeline/` + `tools/vision/`
* **Soil release:** `dataset_release/soil_moisture/` (frozen, 722 imgs) + `dataset_release/soil-moisture-detection/` (kebab, 956 MB raw, ignored)
