# N10 — End-to-End Routing Envelope (LOCKED)

**Status:** REAL_MEASURED · **Result:** `results.json` + 3000 per-case records

Offline deterministic path on master_benchmark_3000 (CEA E27 data, disclosed reuse): certify 71.65%, refuse 49.3%, **dangerous acceptance 37.4%** (374 unsafe → certified stub answers), 438 abstentions. The 37.4% is a pessimistic envelope showing what the rule-only path lets through — the production LLM safety branch exists precisely for this gap. 13% of real queries retrieve nothing (coverage finding). Never cite as deployed risk or coverage.
