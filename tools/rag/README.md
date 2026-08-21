# RAG Tools — Corpus & Index Pipeline

Formerly `backend/ml_assets/rag_index/scripts/` (moved in S1, renamed in S2).

## Rename Map (S2)

| Old (`00_*`) | New (descriptive) | Purpose |
|--------------|-------------------|---------|
| `00_analyze_refined.py` | `analyze_refined.py` | Analyze refined corpus quality/coverage |
| `00_count.py` | `count.py` | Count nodes / corpus stats |
| `00_count_simple.py` | `count_simple.py` | Simple count (quick) |
| `00_full_audit.py` | `full_audit.py` | Full audit of corpus + indexes |
| `00_language_report.py` | `language_report.py` | Bengali/Banglish language distribution |
| `00_quality_check.py` | `quality_check.py` | Quality gates (normalization, dedupe) |
| `00_show_examples.py` | `show_examples.py` | Show example nodes |
| `00_show_status.py` | `show_status.py` | Show corpus/index status |
| `00_smoke_test.py` | `smoke_test.py` | Quick RAG smoke test |
| `00_test_keys.py` | `test_keys.py` | Test API keys / env |

> All moves via `git mv`, 100% rename, no content change. Old names were numeric prefixes that hid purpose.

## Remaining Pipeline (kept numbered for order)

| File | Purpose |
|------|---------|
| `01_clean_and_normalize.py` | Clean & normalize raw knowledge nodes |
| `02_build_bm25.py` | Build BM25 sparse index |
| `03_build_embeddings.py` | Build dense embeddings (local) |
| `03_build_embeddings_api.py` | Build embeddings via API |
| `03_refine_nodes_gemini.py` | Refine nodes with Gemini |
| `04_merge_refined.py` | Merge refined nodes |
| `05_build_term_map.py` | Build term/dialect map |
| `06_build_faiss.py` | Build FAISS dense index |
| `07_hybrid_smoke.py` | Hybrid (BM25+dense) smoke test |
| `08_build_golden_set.py` | Build golden eval set |
| `08_quality_spot_check.py` | Quality spot check |
| `09_run_golden_eval.py` | Run golden evaluation |
| `10_scoring_sheet.py` | Scoring sheet |
| `11_publish_golden_stats.py` | Publish golden stats to `frontend/src/lib/golden_stats.json` |
| `12_probe_retrieval_scores.py` | Probe retrieval scores |
| `13_coverage_gap_analysis.py` | Coverage gap analysis |
| `14_derive_dialect_map.py` | Derive dialect map |
| `_common.py` | Shared helpers |
| `_inspect.py` | Inspect utilities |

## How to run

```powershell
# From repo root, examples:
python tools/rag/count.py
python tools/rag/02_build_bm25.py
python tools/rag/06_build_faiss.py
python tools/rag/smoke_test.py
```

All scripts are offline — they read `backend/ml_assets/rag_index/` and write to `indexes/` / `eval/` / `logs/`. No live LLM or web calls unless noted (`03_refine_nodes_gemini.py`, `03_build_embeddings_api.py`).

## Verification after S2

```powershell
uv run python -m compileall -q app
uv run pytest tests/test_storage_sqlite.py -q
uv run python backend/scripts/replay_golden.py  # 50/50
```

Renames are `git mv` only — no content change, so no behavior change.
