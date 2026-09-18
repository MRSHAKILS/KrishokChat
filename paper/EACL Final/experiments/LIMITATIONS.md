# Limitations Table (paper-facing — copy into methods/limitations, don't paraphrase away the numbers)

| # | Limitation | Evidence status | What we do instead |
|---|---|---|---|
| 1 | N03 small n (38 answers; per-type n 8–33) | REAL_MEASURED_SMALLN, CIs in spec | Report per-type rates with Wilson CIs; no pooling; no generalization beyond dosage-claim sentences |
| 2 | Crop-router label mismatch (family truth vs 10-species predictions; top-1 0.0259 diagnostic) | Measured + disclosed | Report 0.0259 ONLY as mismatch diagnostic with species breakdown; router accuracy unclaimed |
| 3 | Rice INT8 rejected (2.5pp drop > 2.0pp gate) | Measured | Artifact exists, never deployed, never cited as usable |
| 4 | Potato/brassica INT8 sets too small (n=15/51) | Measured | Diagnostic-only; quantitative INT8 accuracy claimed for wheat only |
| 5 | Corn/chilli unmeasured (no local labeled images) | Stated | No claim of any kind for either model |
| 6 | INT8 not faster here (higher latency than FP32) | Measured | Never claim speedup; INT8 is a size story only |
| 7 | N07 implicit-crop miss (farmer_q_63) | Measured, counted as miss | Badge claim scoped to explicit-text contradiction; 53/54 farmer + 400/400 PRISM (453/454 combined) |
| 8 | N08 perfect-gold fence | Measured, disclosed | Simulation of perfect routing, not classifier performance; no absent-crop generalization |
| 9 | N09 seeded-memory conformance | Measured, disclosed | Conformance, not independent accuracy; follow-up D untested; safety is precheck-only lower bound |
| 10 | N11 cost unmeasured; 60-row answer review pending | Stated | Operating-point comparison (halt + latency) only; no coverage/quality superiority claim |
| 11 | Single-reviewer labels (200 crop slots) + agent autopsies | Disclosed in every artifact | Second human pass listed as upgrade path; hazard numbers labeled single-reviewer |
| 12 | Live-generation token usage recorded (n=58 grounded rows: input p50 1111, output p50 221); monetary cost not computed | Measured tokens, no money claim | Report tokens; cost arithmetic uses disclosed tier-mix price basis only |
| 13 | Dense retrieval unevaluated (BM25-only throughout) | Stated | All retrieval numbers scoped BM25-only; dense is fallback, out of scope |
| 14 | Live LLM latency excluded from overhead p50s | Stated | All p50 figures exclude generation unless labeled live (N11 p50 4.2s) |
| 15 | N03 generation buffered pre-rule (71 rows verified intact) | Stated | Per-record rule enforced in N05/N11 runners going forward |
| 16 | SMS dose fields do not survive truncation (0/84) | Measured | Enforcement + purity claimed; packer pending; never claim field survival |
| 17 | Off-topic refusal absent in deterministic path (0/30) | Measured | Split reported (injections 10/10 blocked); production LLM branch unmeasured here |
| 18 | Bangla-native injection residual (10.0% [5.5, 17.4], n=100; embedded 4/10, roleplay 2/10) | Measured with CI (E03 n=30 + N12 n=70) | Reported as residual risk with localized weakness; motivates the downstream verifier wall |

Rule: every paper number must trace to ground_truth.yaml; every caveat above must survive into the manuscript. Killing a limitation row requires new measurement, not rewording.
