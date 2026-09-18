# N08 — Fence Study (LOCKED, critic-audited)

**Status:** REAL_MEASURED · **Result:** `results.json` (400 paired queries)

Pre-binding the image-derived crop cuts wrong-crop retrieval **36.25% → 30.0%** (McNemar exact p = 5.96e-08; 25 fixed, 0 broken) and raises gold purity (**0.6472 n=380 → 0.7353 n=400**; the fence additionally eliminates empty-known top-5s, 20 open vs 0 fenced). Perfect-vision simulation (gold crop as fence) — not classifier performance, not absent-crop routing.
