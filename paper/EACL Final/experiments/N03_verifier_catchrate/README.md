# N03 — Verifier Catch-Rate (LOCKED, critic-audited + extended)

**Status:** REAL_MEASURED_SMALLN · **Results:** `results_catchrate.json` (13 answers) + `results_catchrate_ext.json` (25 answers)

- Generation: 71 live dosage elicitations → 13 scored; extension (53 farmer dosage rows/52 unique queries + 142 paraphrases, deduped to 114 unique questions) → 25 more scored. Total **38 dose-bearing answers**; exclusions counted by tier (37 refusal + 33 doseless + 8 clarification + 7 guard + 4 guidance).
- Catch, combined (claim-anchored, validity-gated, strict==precise): dose_x2 **33/33**, dose_div2 **30/31**, chemical_swap **22/25**, unit_swap **29/29**; clean FP **0/38**. 4 misses autopsied (brand/generic duality, fertilizer-list edges, rate collisions). CIs in spec; no pooling.
- Version history: v1 lowercase-chem artifact → v2 case-preserved → v3 claim-anchored → v4 validity-gated + precise-fixed → v5 extension. Superseded files live in `results/archive/` (never cite).
