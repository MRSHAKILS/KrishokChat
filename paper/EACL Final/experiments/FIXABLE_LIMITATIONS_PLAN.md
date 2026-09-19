# Plan for Addressing Fixable Limitations (EACL 2027 System Demonstrations)
**Created**: 2026-09-19  
**Status Ledger**: Tracking 18 Limitations from `LIMITATIONS.md` — Marked as Done, In Progress, Fixable, or Blocked.

---

## Overview & Execution Strategy

Our goal is to systematically evaluate, verify, and resolve all limitations that can be empirically fixed using our compute resources, local datasets, and pipeline code. Every resolution must adhere to:
1. Strict empirical verification (no unmeasured claims).
2. Large, statistically robust test sets (no small test sets that draw reviewer complaints).
3. Zero-token-loss & money protection rules (local CPU inference, no paid API leaks).
4. Synchronized updates across all artifacts: `LIMITATIONS.md`, `paper_results.yaml`, `registry.yaml`, `verification_report.json`, LaTeX paper (`main.tex`), and draft (`turn_1.md`).

---

## Limitations Status & Action Matrix

| # | Limitation | Category | Current Status | Action Plan & Feasibility |
|---|---|---|---|---|
| **1** | N03 small n (38 answers; per-type n 8–33) | Small Sample | ⚠️ **UNDONE (Fixable with Effort)** | Run additional dosage verifier evaluations on larger synthetic benchmark set (n ≥ 100). |
| **2** | Crop-router label mismatch (family vs 10-species; top-1 0.0259) | Label Alignment | 🔒 **BLOCKED / DISCLOSED** | Architectural mismatch between 6-family router and 10 species. Preregistered family mapping (99.08%) already reported. |
| **3** | Rice INT8 rejected (2.5pp drop > 2.0pp gate) | Gate Failure | 🔒 **BLOCKED / DESIGN DECISION** | Gate worked as intended (rejected >2.0pp degradation). Keep as safety disclosure. |
| **4** | Potato/brassica INT8 sets too small (n=15/51) | Small Sample | ✅ **DONE / RESOLVED** | Evaluated on full test sets: Potato n=1170 (drop 0.09pp), Brassica n=443 (drop 0.00pp). Both pass <= 2.0pp gate (n >= 100). |
| **5** | **Corn/chilli unmeasured (no local labeled images)** | **Missing Evaluation** | ✅ **DONE / RESOLVED** | Evaluated on full test sets: Corn n=940 (top-1 97.23%), Chilli n=861 (top-1 99.07%). 100.00% ONNX/PT agreement. |
| **6** | **INT8 latency characterized across 1--4 threads** | **Hardware Characterization** | ✅ **DONE / RESOLVED** | Benchmarked across 1, 2, 4 threads across 4 models (`n04_int8_threads_benchmark.json`). Characterized: lack of AVX-512 VNNI on x86 causes 1.5--2.0x software emulation overhead; INT8 validated strictly as 3.7x storage reduction (0.00pp drop), not speedup. |
| **7** | N07 implicit-crop miss (farmer_q_63) | Scope Definition | 🔒 **BLOCKED / DISCLOSED** | Scoped to explicit-text contradiction; single miss disclosed. |
| **8** | N08 perfect-gold fence | Methodology | 🔒 **BLOCKED / DISCLOSED** | Methodology simulation; disclosed. |
| **9** | N09 seeded-memory conformance | Methodology | 🔒 **BLOCKED / DISCLOSED** | Conformance check; disclosed. |
| **10** | N11 cost unmeasured; 60-row answer review pending | Analysis Gap | ⚠️ **UNDONE (Fixable)** | Compute monetary cost using Tier-Mix price basis; complete 60-row manual rubric scoring. |
| **11** | Single-reviewer labels (200 crop slots) | Reviewer Agreement | ⚠️ **UNDONE (Needs 2nd Reviewer)** | Requires independent second human annotator for inter-annotator agreement (Cohen's Kappa). |
| **12** | **Live-generation monetary cost computed** | **Calculation Gap** | ✅ **DONE / RESOLVED** | Computed on n=58 grounded calls under openrouter/gemini-2.5-flash-lite basis ($0.10/$0.40 per 1M): $0.0001995 per turn (p50), $0.1839/1k under 7.8% zero-LLM mix (+2.3% vs $0.1798 modeled). |
| **13** | Dense retrieval unevaluated (BM25-only) | Scope Definition | 🔒 **BLOCKED / DESIGN CHOICE** | System is intentionally BM25-first for low-resource deterministic guarantees. |
| **14** | Live LLM latency excluded from overhead p50s | Scope Definition | 🔒 **BLOCKED / DISCLOSED** | Overhead p50 specifically measures precheck+retrieval+verification pipeline without variable cloud LLM latency. |
| **15** | N03 generation buffered pre-rule | Historical Audit | ✅ **DONE / RESOLVED** | Verified intact (71 rows); streaming rule enforced in N05/N11. |
| **16** | **SMS dose truncation resolved via deterministic 11-slot packer** | **Missing Feature** | ✅ **DONE / RESOLVED** | Deterministic 11-slot SMS template compressor (E15 Arm A) implemented in `backend/app/domain/sms_compressor.py`. Achieves 100.0% survival (1,000/1,000 tuples) in E15 and 98.5% (65/66) on live gold benchmark queries without 160c violations. |
| **17** | **Off-topic refusal characterized (0/30 det vs 25/30 [83.3%] LLM)** | **Missing Test** | ✅ **DONE / RESOLVED** | Evaluated 30 off-topic queries through live LLM NLU (`google/gemini-2.5-flash-lite`): 25/30 refused (83.33% [66.4, 92.7]); 5/5 weather queries pass to safe_agri by design. |
| **18** | Bangla-native injection residual (10.0% [5.5, 17.4]) | Security Boundary | 🔒 **BLOCKED / DISCLOSED** | Real residual risk disclosed to motivate the downstream verifier wall. |

---

## Detailed Roadmap

### Phase 1: Corn & Chilli Vision Evaluation (Limitation #5) — *ACTIVE*
1. Count and inspect all images in `D:\499A Dataset\Corn\test` and `D:\499A Dataset\Solanaceae\test`.
2. Inspect input shapes, normalization, and class mappings of `corn.onnx` and `chilli.onnx`.
3. Execute full inference on all test images (no small sub-sampling).
4. Calculate Top-1 Accuracy, per-class metrics, and Wilson 95% Confidence Intervals.
5. If results meet acceptance threshold (e.g., ≥ 0.88–0.90):
   - Update `paper_results.yaml`
   - Update `LIMITATIONS.md` (remove row 5)
   - Update `registry.yaml`
   - Update `verification_report.json`
   - Update `main.tex` and `turn_1.md`
   - Recompile LaTeX.

### Phase 2: SMS Dose Preservation Compressor (Limitation #16) — *NEXT*
- Implement deterministic dose-preserving text compressor in `backend/app/domain/renderers/sms.py` (or similar).
- Test on 84 dosage queries and measure survival rate (target: >95%).

### Phase 3: Off-Topic Refusal Benchmark (Limitation #17) — *NEXT*
- Run 30 standard out-of-domain / off-topic queries through the full pipeline.
- Verify Tier 1 NLU refusal / out-of-domain classification.

### Phase 4: Full Potato/Brassica INT8 Evaluation (Limitation #4)
- Run INT8 evaluation on full held-out test sets (n ≥ 100) from `D:\499A Dataset\`.
