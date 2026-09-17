# E06 — Offline Delivery

**Status:** REAL_MEASURED (deterministic) + SIMULATED (network lane) · **Results:** `results_offline.json`, `results_network_sim.json` (frozen copies)

Deterministic: cache 0/400, BM25 0.94, SW precache true — offline works because retrieval needs no network, not because the cache hits. Network lane (+13.25pp / +30.0pp) combines real BM25 hits with simulated packet drop: always cited with the "simulated loss" qualifier.
