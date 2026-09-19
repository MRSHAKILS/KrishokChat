# Limitations Ledger (Paper-Facing)

Rule: Every paper number must trace to `ground_truth.yaml`; every caveat below must survive into the manuscript.
**Killing a limitation row requires new measurement, not rewording.**
When a limitation is empirically resolved through new measurements and verified implementations, it is retired from the active limitations ledger and documented under "Empirically Resolved & Retired Limitations".

---

## 1. Active System Limitations and Scoped Boundaries Ledger

| # | Limitation | Evidence Status | What We Do Instead / Validated Scope |
|---|---|---|---|
| 1 | N03 small $n$ (38 answers; per-type $n$ 8–33) | `REAL_MEASURED_SMALLN` | Report per-type rates with Wilson CIs; no pooling; no generalization beyond dosage-claim sentences. |
| 2 | Crop-router label mismatch (family truth vs 10-species; top-1 0.0259) | Measured + Disclosed | Report 0.0259 ONLY as mismatch diagnostic with species breakdown; router accuracy unclaimed. |
| 3 | Rice INT8 rejected (2.5pp drop > 2.0pp gate) | Measured | Artifact exists, never deployed, never cited as usable. |
| 4 | INT8 latency gap on non-VNNI x86 CPU (1.5–2.0× slower than FP32) | Measured | Lack of AVX-512 VNNI on x86 causes 1.5–2.0× software dot-product emulation overhead. Validated strictly as 3.7× storage reduction (0.00pp drop), not speedup. |
| 5 | N07 implicit-crop miss (`farmer_q_63`) | Measured | Badge claim scoped to explicit-text contradiction; 53/54 farmer + 400/400 PRISM (453/454 combined). |
| 6 | N08 perfect-gold fence | Measured | Simulation of perfect routing, not classifier performance; no absent-crop generalization. |
| 7 | N09 seeded-memory conformance | Measured | Conformance, not independent accuracy; follow-up D untested; safety is precheck-only lower bound. |
| 8 | N11 cost vs coverage trade-off (60-row answer review pending) | Stated | Operating-point comparison (halt + latency) only; no coverage/quality superiority claim. |
| 9 | Single-reviewer labels (200 crop slots) + autopsies | Disclosed | Second human pass listed as upgrade path; hazard numbers labeled single-reviewer. |
| 10 | Dense retrieval unevaluated (BM25-only throughout) | Stated | All retrieval numbers scoped BM25-only; dense is fallback, out of scope. |
| 11 | Live LLM latency excluded from overhead p50s | Stated | All p50 figures exclude generation unless labeled live (N11 p50 4.2s). |
| 12 | Bangla-native injection residual (10.0% [5.5, 17.4], $n=100$) | Measured with CI | Reported as residual risk with localized weakness (embedded 4/10, roleplay 2/10); motivates downstream verifier wall. |

---

## 2. Empirically Resolved & Retired Limitations

The following items have been empirically resolved through new measurements, verified implementations, and full test-set benchmarks, and are now reported as validated system features in Section 5:

| Original # | Limitation Topic | Resolution Evidence & Measurement | Status |
|---|---|---|---|
| **L4** | Potato/brassica INT8 sets too small ($n=15/51$) | Evaluated on full held-out test sets: Potato $n=1,170$ (drop 0.09pp), Brassica $n=443$ (drop 0.00pp). Both pass $\le 2.0$pp gate ($n \ge 100$). | ✅ **RESOLVED / RETIRED** |
| **L5** | Corn/chilli vision unmeasured (no local labeled images) | Evaluated on full test sets: Corn $n=940$ (top-1 97.23%), Chilli $n=861$ (top-1 99.07%). 100.00% ONNX/PyTorch prediction agreement. | ✅ **RESOLVED / RETIRED** |
| **L12** | Live-generation token usage recorded; monetary cost not computed | Computed exact monetary costs from provider-exact metered tokens ($n=58$ grounded calls): $0.1995/1k pure gen, $0.1839/1k under 7.8% zero-LLM mix (+2.3% vs $0.1798 modeled). | ✅ **RESOLVED / RETIRED** |
| **L15** | N03 generation buffered pre-rule | Verified 71 rows intact; strict per-record durable disk sync (`f.flush()`, `os.fsync()`) enforced in all runners. | ✅ **RESOLVED / RETIRED** |
| **L16** | SMS dose truncation dropped dosage fields (0/84) | Implemented deterministic 11-slot SMS template compressor (`backend/app/domain/sms_compressor.py`). Achieves 100.0% (1,000/1,000) tuple survival in E15 and 98.5% (65/66) on live gold benchmark queries without $>160$c violations. | ✅ **RESOLVED / RETIRED** |
| **L17** | Off-topic refusal absent in deterministic path (0/30) | Evaluated 30 queries through live production Tier-1 LLM NLU (`google/gemini-2.5-flash-lite`): 25/30 refused (83.33% [66.4, 92.7]); 5/5 weather queries pass to `safe_agri` by domain design. | ✅ **RESOLVED / RETIRED** |
