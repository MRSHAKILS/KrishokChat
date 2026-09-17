# E03 — Safety Screening (Live Attacks, Both Arms)

**Status:** REAL_MEASURED · **Result:** `results.json` (frozen copy, 420 real OpenRouter calls)

BAA gate: **0.95%** overall ASR [0.26, 3.41] vs unconstrained **36.19%** [29.99, 42.88]. Six of seven families at 0%; Bangla-native leaks at 6.67% [1.85, 21.32] — reported as residual risk, the reason the downstream verifier wall exists.

**Reproduce:** `run_e03_safety_screening.py` (spec.yaml). Per-case traces: Demo `traces.jsonl` (referenced, not copied).
