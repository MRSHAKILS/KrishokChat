# E08 — Cross-Modal Contradiction

**Status:** REAL_MEASURED (+ cross-track baselines) · **Results:** `results_divergence.json`, `results_baselines_E31.json` (frozen copies)

Local harness: **68/80 = 85.0%** visible divergence under conflicting crop hints (non-divergent = unroutable-hint fallback to image output, a safe default). Baselines (CEA E31, disclosed reuse): unconstrained models clarify 13–20% and poison the wrong crop 54–55%; the BAA gate (B6, CEA-held) clarifies 100% with 0% CUAR. N07 re-runs the gate locally for a demo-track artifact.
