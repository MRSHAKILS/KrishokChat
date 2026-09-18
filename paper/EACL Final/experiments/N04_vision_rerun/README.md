# N04 — Vision Re-run (LOCKED: accuracy + parity; INT8 measured with qualifications)

**Status:** REAL_MEASURED_PARTIAL · **Results:** `results_baseline.json`, `results_parity.json`, `export_report.json`

- Per-model top-1 (current checkpoints): potato 0.900 (n=30), rice 0.9625 (n=80, 8 legacy classes), wheat 0.9413 (n=800), brassica 0.9118 (n=102); corn/chilli unmeasured (no local images). Router 0.0259 is a family/species label-space diagnostic, never a quality number.
- ONNX-vs-`.pt` agreement 100%, max delta 5e-05.
- INT8 (`results/n04_int8_20260917.json`): wheat is the ONLY reportable accuracy claim (held-out n≥100, 0pp drop). Crop INT8 agrees 93.77% with FP32 but its top-1 is the same label-space diagnostic — artifact produced, accuracy NOT claimed. Potato/brassica INT8 are diagnostic-only (n=15/51). Rice INT8 REJECTED (2.5pp drop > 2.0pp gate) — artifact exists, unusable, never deployed. Corn/chilli unmeasured. INT8 is NOT faster here (higher latency than FP32) — never claim speedup.
- Coverage gap (product limitation): Tomato/Eggplant/Gourd/Guava route to no disease model; Wheat/Corn models have no router class (hint-bypass only).
