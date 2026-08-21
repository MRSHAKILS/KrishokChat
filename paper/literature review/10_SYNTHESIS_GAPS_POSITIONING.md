# SYNTHESIS — Verified Research Gaps, Conventions & Paper Positioning for KrishokChat

> **⚠️ VENUE LOCKED (2026-08-21): Wiley *Expert Systems* journal.**
> The R1 freeze (`paper/manuscript/expert-systems-skeleton.md` + `CLAIM_LEDGER_FREEZE.md`) is the **single SSOT**.
> This document's original ACL SysDemo / broad "first system" framing (§1 anchor, §4 positioning, §4 track-ladder) is **superseded and kept for history only**. Where this file and the R1 skeleton disagree, the skeleton wins. Specifically:
> - **Thesis** = the narrow R1 combination (structured relation verifier + calibrated selective certification + safety-constrained dialect normalization), NOT the broad "first safety-audited pipeline" claim (which is forbidden, F08).
> - **No "first system" claims** (F08). **No farmer-benefit / trust / usability claims** (F12).
> - The Gaps A–F below remain useful *motivation and literature scaffolding*, but the paper's contributions are C1–C4 in the skeleton, mapped to experiments E1/E2/E4/E5.
> - The 20,112-record safety dataset (Gap B) is a **supporting evaluation resource**, not the headline; it is now recovered on-disk with hashes (`12_ASSET_VERIFICATION.md` §4).

**Generated:** 2026-08-12 · **Compiled from:** 9 parallel @scout literature reviews (2025 → Aug 2026) + formal gap objects in `11_RESEARCH_GAPS_competitive_matrix.md`
**Scope:** system/application/industry-track acceptance (ACL SysDemo, EMNLP/ACL Industry, AAAI-IAAI, IJCAI demo, KDD ADS, CIKM Applied, NeurIPS D&B)

---

## 1. The single most important finding (read this first)

**The team's own papers are the anchor of this space**: *KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory* (Reza, Nimi & Shahid, EACL 2026) and its retrieval companion *AgRiTrust* (Reza, Maria & Nimi) — local copies in `paper/done papers/`; datasets on Hugging Face (`RaiyanKhaan/krishokChat`, `RaiyanKhaan/AgriTrust-RAG`). The benchmark paper's own measured conclusions — closed-book knowledge insufficient at any scale, a 4.05–7.00% chemical hallucination floor persisting even under oracle evidence, and farmer-language transfer largely unsolved (Gemini-2.5-FL 0.220 Token F1 on the Farmer Benchmark) — are the strongest possible empirical justification for the **system paper**: the follow-on that implements the RAG + verifier pipeline the benchmark proved necessary.

**Action:** the system paper cites the two papers as prior work of this line, reuses their released evaluation resources (Farmer Benchmark 350-query eval split, AgRiTrust 900-query retrieval set), and presents itself as the "pipeline-level" extension: retrieval measured, generation measured, verifier unmeasured. No reviewer collision if positioned correctly.

---

## 2. Verified research gaps (each is a defensible novelty claim)

### GAP A — No agricultural advisory system performs claim-level verification with numeric-dosage drift detection (Clusters 1, 4, 7)
- Medical verifiers exist (MedRAGChecker KG+NLI, ClinicBot numeric string-match, atomic fact-checking) — English clinical only.
- Agricultural systems (Farmer.Chat, KrishokBondhu, cross-lingual 2601.02065) stop at retrieval + generation; no dosage-token interception anywhere.
- IPM-AgriGPT measures *effectiveness (dosing)* as the worst axis (0.392–0.499 vs safety 0.723); Bayer E.L.Y. exists because models fail dosing.
- **KrishokChat lever:** dosage whitelist + RT4CHART-style claim verification with per-claim entailed/contradicted/baseless labels over Bengali agri queries. Unoccupied cell.

### GAP B — No refusal/selective-answering benchmark for low-resource, safety-critical domains; no multi-dialect Bangla safety dataset (Clusters 2, 3)
- RefusalBench/RAGREFUSE/AbstentionBench are English/generic; IndicSafe/IndicGuard/LinguaSafe cover Bengali as one standard-script row.
- IndicSafe cross-language agreement 12.8%; IndicJR romanization changes jailbreak rates by 0.34 — quantified motivation.
- **KrishokChat lever:** 20,112-record, 6-dialect (110-word genuine map) refusal+requery dataset = first mover. Prime candidate for NeurIPS D&B + system-paper evaluation backbone.

### GAP C — No system measures helpline escalation (16123) outcomes (Clusters 4, 9)
- KrishokBondhu mentions "expert referral" in 100% of responses but measures nothing; Farmer.Chat has no escalation layer; India KCC AI/ML is announced policy.
- **KrishokChat lever:** audit trail + referral-rate + follow-through instrumentation = first measured escalation protocol. (Needs a small field pilot to be a 2027 claim.)

### GAP D — Dialect→retrieval degradation for Bangla is completely unmeasured (Clusters 3, 7)
- MIRACL-bn is standard-language Wikipedia (BM25 0.508 / hybrid 0.654 / mE5-large 75.9 nDCG@10); BanglaCHQ-Prantik has no retrieval judgments; 2601.02065 leaves dialects to future work.
- **KrishokChat lever:** first published nDCG@10/R@100 cells for Sylheti/Chittagong/Rangpur queries with BUNO normalization ablation.

### GAP E — No Bengali agricultural SLM benchmark; no latency–grounding tradeoff for token-inefficient domains (Clusters 3, 8)
- BnMMLU has no agriculture domain; AgriEval Bengali split unreviewed; only the team's Farmer Benchmark evaluates Bengali agri at small scale (Token F1: Gemini-2.5-FL 0.220, Gemma-4-26B 0.138, KrishokChat-4B 0.117, Qwen-2.5-7B 0.084, LLaMA-3.1-8B 0.008).
- **KrishokChat lever:** stage-trace streaming UX + per-stage TTFT/TBT SLO reporting + verifier v TTFT-budget curve = first controlled agent-trace evidence (G3 in Cluster 8).

### GAP F — No tier-1 paper measures the vision→grounded-treatment loop's grounding quality (Cluster 5)
- Mondal (2505.21544) is the only vision→RAG-advice predecessor — single-crop, no grounding metric, no safety layer, no rejection.
- Supervised `classify` beats zero-shot VLMs on every task (arXiv:2512.15977) — validates the locked stack.
- **KrishokChat lever:** 35-class hierarchy with per-class calibrated rejection + verifier-audited Bengali treatment grounding (99.8% info coverage) + router-error decomposition. DR-screening reporting conventions transfer.

---

## 3. System/application-track conventions distilled (what accepted papers include)

| Convention | Evidence (verified) |
|---|---|
| **Mandatory evaluation** (any form) in ACL SysDemo; desk-reject without it | ACL 2026 CFP |
| **Human/expert evaluation expected** — LLM-as-judge alone is rejected | My Climate CoPilot 50 experts; AIEP LLM-judge-only correlates weakly; Pariksha/JuICE judge unreliability for Bengali |
| **Ablation ladder reporting**: BM25 → dense → hybrid → hybrid+normalizer → +reranker, k-sensitivity (k=5→20 faithfulness 88.1→92.2) | MIRACL, mE5, RAGChecker, EMNLP'25 |
| **Claim-level + abstention metrics**: AbstainAccuracy/F1, risk–coverage curves, RAGAS-v2-style NLI verdicts | RefusalBench, RT4CHART, RAGChecker |
| **Latency as TTFT/TBT with p50/p95/SLO attainment**, quantized-footprint hardware statements | ServeGen, T-LRU, Gemma 3/4 reports |
| **Artifacts are table stakes**: code, HF datasets under CC-BY-4.0, demo video/URL, Croissant metadata (NeurIPS D&B) | ACL SysDemo 2025/2026, NeurIPS 2025 D&B |
| **Novelty relocates to domain/engineering/usability** in applied tracks; "just a wrapper" is a documented rejection trigger demanding 30–100-input component evals | KDD ADS CFP; arXiv:2602.05128 |
| **Mixed-methods field evidence + gender-disaggregated metrics** for ICT4D-style claims | Farmer.Chat, 60dB, AIEP, COMPASS '25 |

---

## 4. Recommended paper architecture (system track)

**Positioning statement:** *"The first safety-audited, claim-verified Bengali agricultural advisory pipeline — 6-way pre-retrieval safety routing, hybrid retrieval over national-institution knowledge, verifier-gated dosage interception, and measured 16123 escalation — validated by the first multi-dialect Bengali agri-safety dataset (20,112 records)."*

**Sections (EMNLP Industry / ACL SysDemo shape):**
1. Problem: extension ratio 1:750–1000, 41.27% AgriEval average, 29% zero-shot factuality, <0.17 closed-book Token F1 and <44% Treatment QA Correct% on the team's own benchmark, 4.05–7.00% chemical hallucination floor even with oracle evidence
2. System: architecture + agent-trace figure; locked stack (Gemma-4B 4-bit / Flash-Lite adapters)
3. Evaluation:
   - Model: Farmer Benchmark 1,000 queries (350-query held-out eval split) + DG-Eval-style atomic facts
   - System: safety-router precision/recall per 6 classes (oversensitivity split per LinguaSafe), verifier claim-level metrics, dialect-disaggregated (vs Chittagong 5.44/10 baseline)
   - UX: stage-stepper controlled study (Gap E-G3), TTFT/TBT p50/p95 per stage
   - Process: audit trail as governance artifact; helpline referral rate
4. Related work: positioned against KrishokBondhu (2510.18355), cross-lingual RAG (2601.02065), Farmer.Chat (2409.08916)
5. Limitations (mandatory EMNLP): no causal claims, selection bias, capacity-constrained helpline

**Track ladder (2026–27 cycles):**
1. **ACL 2027 System Demonstrations** — primary (My Climate CoPilot template; 6pp + 2.5-min video + live URL)
2. **IAAI-27 Emerging Applications** — second (6pp, deployment-path friendly)
3. **AAAI-27 Demonstration** — cheap supplementary (2pp + 5-min video)
4. **EMNLP 2027 Industry** — fallback ("Emerging" category)
5. **NeurIPS 2027 D&B** — dataset paper alone (Croissant metadata + executable generation code; contamination-by-construction narrative)
6. Avoid KDD ADS / CIKM Applied until post-launch metrics exist

---

## 5. Files in this review (paper/literature review/)

| File | Content |
|---|---|
| `00_SCOPE_AND_ANGLES.md` | Master scope: 9 clusters, ~36 angles |
| `01_agentic_rag_verifier_systems.md` | Agentic RAG + verifier + refusal benchmarks (Scout 1) |
| `02_llm_safety_low_resource.md` | Guardrails, multilingual safety, Bengali gap (Scout 2) |
| `03_low_resource_nlp_bengali.md` | Bengali LLMs, dialects, synthetic data, judges (Scout 3) |
| `04_agri_ai_advisory_systems.md` | Farmer.Chat lineage, AgriEval, dosages, deployment (Scout 4) |
| `05_vision_crop_disease.md` | VLM-vs-supervised, calibration/OOD, DR-screening conventions (Scout 5) |
| `06_system_industry_track_conventions.md` | Track-by-track CFPs, novelty playbook (Scout 6) |
| `07_retrieval_low_resource_rag_eval.md` | MIRACL-bn, MILCO, dialect retrieval, CiteEval/RAGChecker (Scout 7) |
| `08_edge_slm_streaming_systems.md` | Gemma 4, BnMMLU, TTFT/TBT, latency perception (Scout 8) |
| `09_ict4d_global_south.md` | 60dB/AIEP/RCT registry, helpline constraints, ICT4D rigor (Scout 9) |
| `11_RESEARCH_GAPS_competitive_matrix.md` | Formal gap objects: calibration/abstention, taxonomy containment, safety-monotone refusal (Scout 2) |

Root files also updated by Scout 2: `LITERATURE_REVIEW.md` gained a **Competitive Matrix** (5 competitors × 6 dimensions).

---

## 6. Recommended next actions

1. **Decide the submission target** (ACL 2027 SysDemo is the strongest fit) and lock the 6-page outline from Section 4.
2. **Run the missing-evidence experiments** that convert gaps into results: (a) dialectal retrieval ablation (Gap D), (b) verifier claim-level metrics + dosage interception rate (Gap A), (c) per-stage TTFT/TBT (Gap E), (d) safety-router oversensitivity split (Gap B).
3. **Prepare dataset release rigor** per NeurIPS D&B: Croissant metadata, 13-gram decontamination, native per-dialect human validation with agreement stats, CC-BY-4.0 (already), executable generation code (T3/T4 scripts exist).
4. **Anchor the prior-work section on the two published papers** (KrishokChat benchmark, EACL 2026; AgRiTrust retrieval benchmark) with the exact numbers above and reconciled counts; position the system paper as the pipeline-level extension whose verifier layer neither paper measures.
5. **Plan a small field/UX evaluation** (farmer-panel trace-stepper study or 60dB-style log-vs-recall cross-check) to occupy Gaps C and E-G3 before the 2027 cycle deadlines.