# Supervisor Review — Full Code + Results Audit (2026-09-17)

**Role:** PhD supervisor + EACL demo reviewer. Method: runner smell sweep (17 runners — no simulations, no mocks, seeded randomness only for sampling/choice), full ground-truth recompute (all 21 entries verified against locked files), hypothesis mapping, accepted-paper comparison.

## Verdict: ACCEPT-LEANING (borderline-accept). Real work, honestly reported, demo-track fit. Three improvements ranked below.

## 1. Are the results real? YES.
- Every headline number recomputed from raw records this pass (N01b 76/200, N07 53/54, N08 145/400→120/400, N09 458/1000, N10 1807/755/438, N11 20/200, N05 0 over-160, N03 41/41 valid catches, E03/E07/E10 spot-verified).
- Runners execute real pipelines/models/APIs; latencies vary genuinely; no constant tables; no random-outcome sampling anywhere in Final runners.
- 6 forensic critic audits completed; every finding fixed and re-verified (38.5% and 88% retired, README 100% fixed, pooled purity corrected, 11-slot scope discipline, single-reviewer labels).

## 2. Do results support the hypotheses? YES, with scoped strength.
- **C1 (halt gate): STRONG on behavior** (38% real halt, 100/100 pilot, 0.86 conformance, matcher-vs-LLM trade-off measured). MODERATE on hazard magnitude (no gate-silent mappable set exists in real data; chemical case rests on pilot + descriptive spread — disclosed).
- **C2 (fence + badge): STRONG.** Fence 25/0 p<1e-6, badge 53/54 with 0 false-halts, accuracy + 100% parity. Router label-space and perfect-vision-simulation framings disclosed.
- **C3 (two walls + delivery): STRONG on guards** (E03 both arms with CIs), **ADEQUATE on verifier generality** (n=13, deep per-item validity, CIs, no pooling), **HONEST-NEGATIVE on SMS dose** (0/84, packer pending).

## 3. Lethal objections, ranked (with defusers).
1. **"n=13 verifier study"** (MAJOR). Defused by: validity gates, strict==precise, CIs, FP 0/13, E03 n=420 upstream. Improvement: extend answers if budget allows.
2. **"No independent human evaluation"** (MAJOR). Defused: exceeds demo norm (GenGO Ultra LLM-judge-only; NLP-KG 50 RAGAS; OLMOtrace 1 expert). We have 200 team-labeled + autopsies, disclosed single-reviewer.
3. **"Chemical case rests on pilot"** (MAJOR). Defused: labeled pilot + real-behavior numbers carry C1; no gate-silent mappable set exists in 200 real queries (itself a finding).
4. **"BM25-only, no dense/SOTA baseline"** (MINOR for demo track). Scoped explicitly; demos don't require SOTA-beating.
5. **"Cross-track data"** (MINOR). Disclosed with provenance (E31, E27); same pattern as published companion-data reuse.
6. **"No field deployment"** (MINOR for demo). Honest envelopes + limitations; Farmer.Chat-scale deployment is the exception, not the bar.

## 4. Norm comparison (accepted ACL/EACL demos).
| Norm | Bar (examples) | Us |
|---|---|---|
| Scale | 30–300 typical (SciRAG 30×3, NLP-KG 50, RAGVUE 100, OLMOtrace 98) | MEETS+ (400–3000 on main lines; small-n arms CI-labeled) |
| Baselines | Often none; best have 2–4 systems | EXCEEDS (unconstrained LLM, blind-RAG, prompted judge, ablations) |
| Ablations | Rare in demos | EXCEEDS (gate on/off, fence ±, INT8, 4 mutation types) |
| Human eval | LLM-judge-only common | EXCEEDS (200 team labels + autopsies, disclosed) |
| Artifacts | Code release typical | EXCEEDS (frozen hashes, runners, per-row records, version archive) |
| Honesty | Mixed in the wild | EXCEEDS (kill-list, 18-row limitations, CIs, archived supersessions) |

## 5. Novelty.
**Keep (single sentence):** "A Bengali advisory session that halts before retrieval on empty crop slots, fences retrieval by on-device crop classification, verifies dosage claims pre-render with sentence-dropping, and degrades to SMS/helpline — each gate measured." Distinguishable from Farmer.Chat (scale, no gates measured), KrishokBondhu (voice RAG, no vision/verifier), Krishi Sathi (slots-then-retrieve, no halt/hazard/cost deltas).
**Cut:** any "first" claim (already killed), INT8 as novelty (supporting only), WASM as novelty (supporting only).

## 6. Top improvements by effort-to-acceptance ratio.
1. **Second human reviewer** on 200 labels + 60 N11 rows (hours, kills R-subjectivity).
2. **Extend N03 answers** 13 → 40+ (small API spend; defuses objection #1 decisively).
3. **Live token/cost capture** (small code + tiny spend; completes N02/N11 cost story).

## 7. residuals tracked, not hidden.
V1/v2/PREFIX archives, amendment logs, stale-README repairs, p-value rounding fix, suite-count note, untracked-file provenance (hashes + diffs). Working tree stays dirty by policy (no commits without instruction); reproducibility rests on embedded hashes, not git HEAD.
