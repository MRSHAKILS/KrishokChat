# EACL Demo Section 04: Empirical Usability & System Evaluation (Draft Skeleton) — REVISED 2026-08-30: previous N=60 table was FABRICATED, see STATE.md S3

## 4.1 System Usability Scale (SUS) Evaluation
- NO FORMAL RECRUITED STUDY. E05 harness self-labels SIMULATED with n_evaluators: 3, mean_sus_score: 82.5.
- Previous N=60 (35 Bogura /15 SAAO /10 BARI-BRRI), 84.6/100, 95.0%, 4.72 trust were fabricated and removed per AGENTS.md rule 5.
- TODO: IRB-approved recruited evaluation pending. Do not cite SUS.

## 4.2 Latency & Throughput Profile
- Correct framing: T1+T2 deterministic 51.04%, T0+T4 safety/refusal 10.48%, T3 LLM-dependent 38.48% (T0+T1+T2 57.44%, not 61.52%).
- Per-stage latency via stage_timer NOT YET MEASURED over held-out Bengali set. Previous 320ms TTFT and 546.2ms weighted mean (mislabeled as Tier-3 p50) are unsourced; left as TODO until live llama-server available.
- Vision classification IS measured: see E02 reports (results_real_pt_baseline.json, results_real_onnx_parity.json).

## 4.3 Safety Verification Reliability
- E03 measured 210 real API calls (7x30x2 arms) with 0.95% overall ASR but 6.67% bangla_native_injection leak — real and must be reported, not 0/1400.
- Previous 10,000 misbinding 100.0% detection was unsourced for this track.