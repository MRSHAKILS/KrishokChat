# Research / Evidence Case Cards

Everything here is **precomputed, loaded from disk — never computed live**
(AGENTS.md §2.2). Each claim below maps to a file in
`manifests/evidence_sources.json`.

| # | Case | Surface | Evidence file |
|---|------|---------|---------------|
| 1 | Benchmark panel | `/research/benchmark` (frontend) | `dataset_release/benchmark/*.csv` + `golden_qa_v1.jsonl` (50 rows) |
| 2 | Retrieval (BM25 + BGE-M3, 2135 nodes) | QA pipeline retrieval stage | `backend/ml_assets/rag_index/manifest.json` + `coverage_gaps_v1.json` (1000/1000 adequate) |
| 3 | Safety metrics | `/api/safety/metrics` | local audit log only (`backend/app/logs/safety_audit.jsonl`) — never external |
| 4 | Provenance | poster/research claims | `verification_report.json`, golden run files, `paper/done papers/*.pdf` |

Screenshot fallbacks: `screenshots/06_analytics_dashboard.png` (metrics),
`08_data_benchmark.png` (benchmark), `09_*` (safety sandbox).