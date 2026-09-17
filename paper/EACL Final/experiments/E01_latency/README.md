# E01 — Latency Breakdown

**Status:** REAL_MEASURED · **Result:** `results.json` (frozen copy)

Per-stage latency via `telemetry.stage_timer` on 400 held-out Bengali queries: safety p50 0.32ms, retrieval (BM25-only) p50 26.8ms, verifier p50 4.82ms, system overhead p50 33.6ms. Generation is stubbed — live LLM latency is UNMEASURED and must never be implied.

**Reproduce:** `run_real_e01_latency.py` (path + git HEAD in `spec.yaml`), cwd=`backend`, seed 42.
