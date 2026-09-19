# N04 — Vision Re-run (LOCKED: accuracy + parity; INT8 measured with qualifications)

**Status:** REAL_MEASURED · **Results:** `results_baseline.json`, `results_parity.json`, `export_report.json`, `corn_chilli_eval_results.json`, `potato_brassica_int8_results.json`

- Per-model top-1 (current checkpoints): potato 0.9504 (n=1170), rice 0.9625 (n=80, 8 legacy classes), wheat 0.9413 (n=800), brassica 0.9729 (n=443), corn 0.9723 (n=940), chilli 0.9907 (n=861). All 6 models measured on full test sets with 100% ONNX-vs-`.pt` prediction agreement. Router 0.0259 is a family/species label-space diagnostic, never a quality number.
- ONNX-vs-`.pt` agreement 100%, max delta 5e-05.
- INT8: wheat, potato, and brassica are all reportable accuracy claims (all held-out n >= 100 with <= 2.0pp drop: wheat 0.0pp drop, potato 0.09pp drop on n=1170, brassica 0.00pp drop on n=443). Rice INT8 REJECTED (2.5pp drop > 2.0pp gate) — artifact exists, unusable, never deployed. INT8 is NOT faster here (higher latency than FP32) — never claim speedup.
- Coverage gap (product limitation): Tomato/Eggplant/Gourd/Guava route to no disease model; Wheat/Corn models have no router class (hint-bypass only).
