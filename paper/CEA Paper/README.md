# Computers and Electronics in Agriculture (CEA) Paper Workspace

**Target Journal:** *Computers and Electronics in Agriculture* (Elsevier, Impact Factor: 7.7, CiteScore: 12.2, Q1)  
**Article Type:** Full Original Research Paper (approx. 9,000–12,000 words)  
**Status:** In Active Preparation — Experimental Infrastructure & Skeleton Ready  
**Last Audited:** 2026-08-27  

---

## 1. Project Identity & Research Motive

- **Title:** *Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support*
- **Short Title:** *Bounded-Authority Bengali Agricultural Advisory*
- **Central Hypothesis:** Separating **factual authority** from **linguistic realization** and enforcing an 11-slot fail-closed single-record certification rule guarantees that generative models cannot hallucinate or misbind hazardous agricultural parameters while maintaining high operational coverage and deployment efficiency.

---

## 2. Project Progress & Status Tracker

| Area / Component | Total Units | Completed | Remaining | Progress Status |
|---|:---:|:---:|:---:|:---:|
| **Manuscript LaTeX Skeletons** | 18 Sections | 18 Skeletons | 0 | 100% (Structured & Modular) |
| **LaTeX Table Definitions** | 10 Tables | 10 Tables | 0 | 100% (Pre-formatted Tab 1–10) |
| **Section Markdown Drafts** | 18 Drafts | 18 Outlines | 0 | 100% (Outlines & Objectives Ready) |
| **BibTeX Literature Database** | 18 Citations | 18 Citations | 0 | 100% (Verified 2025–2026 References) |
| **Completed Experiment Layers** | 27 Layers | 27 Layers | 0 | **100% Done, Verified & Folderized** |
| **Planned / Rigor Experiment Layers** | 12 Layers | 0 Layers | 12 Layers | **Skeletons, Specs & Runners Ready** |
| **Master Results Single Source of Truth** | 1 Unified YAML | 1 YAML | 0 | **100% Generated & Verified** |

---

## 3. Detailed Experiment Portfolio (39 Total Layers)

### A. Completed & Verified Experiments (24 Layers — Ready in `experiments/`)

Every completed experiment below is fully folderized under `paper/CEA Paper/experiments/<layer>/` with its **exact execution script** in `scripts/`, **exact measured results** in `results.yaml` & `results.json`, and **comprehensive documentation** in `README.md`:

1. **`E02_relational_misbinding`**: Adversarial Relational Misbinding Attack Suite (10,000 cases; 100% detection rate in 11-slot verifier).
2. **`E03_slot_ablation`**: 11-Slot Hazard Prevention Ablation (Dosage +31.6%, Reg polarity +17.8%, Active +14.2% hazard spikes).
3. **`E04_risk_coverage_calibration`**: Risk-Coverage Calibration ($AURC = 0.0153$, $ECE = 0.0785$, 84.56% coverage @ $\le 1.0\%$ risk).
4. **`E05_counterfactual_binding`**: Counterfactual Evidence Sensitivity (0.0% false certification on mutated records vs 72.65% Vanilla RAG).
5. **`E06_farmer_dialect_benchmark`**: Multi-Register Bengali Benchmark (Text-first RAG Hit@1 drops from 72.1% to 45.7% on dialects).
6. **`E07_E08_prompt_injection`**: Prompt Injection & Context Poisoning (0.0% injection survivability; 0 / 1,400 leaks).
7. **`E09_latency_economics`**: Latency Decomposition & On-Prem Economics ($0.0001994/query on-prem vs $2.30/1k Cloud API).
8. **`E10_failure_taxonomy`**: Root-Cause Failure Containment Audit (100 cases audited: 28% retrieval omission, 22% misbinding).
9. **`E11_multi_generator_invariance`**: Multi-Generator Verifier Stability (Consistent bounds across Gemma-4, Llama-3, Mistral).
10. **`E12_retrieval_degradation`**: Retrieval Degradation & Context Poisoning (CUAR remains 0.0% under 100% poisoned retrieval).
11. **`E13_human_expert_validation`**: Agronomist Human Evaluation Study (Gwet's AC1 = 0.862 across 200 expert evaluations).
12. **`E14_network_degradation`**: Rural Cellular Degradation (Offline cache delivers 91.4% @ 15% loss, 80.3% @ 30% loss).
13. **`E15_sms_compressor`**: Deterministic 160-char SMS Compression (100% parameter survival vs 64.4% PHI truncation in LLM SMS).
14. **`E17_detection_gated_routing`**: Detection-Gated Routing (75.64% search space collapse; +36.6 pp dialect Hit@1).
15. **`E18_llm_dependency_reduction`**: LLM Dependency Reduction (61.52% zero-LLM resolution; 2.28x latency speedup; $0.0768/1k).
16. **`E19_knowledge_graph_traversal`**: Deterministic Graph Traversal (100% slot completeness and provenance in 0.0195 ms p95).
17. **`E20_telecom_economics`**: Localized Telecom Economics (0.0308 BDT online vs 0.2808 BDT SMS fallback; 2.17 Cr BDT annual cost).
18. **`E21_dialect_hazard_routing`**: Dialect Hazard Routing Cross-Tab (Detection gating restores dialect coverage to 89.8% with 0.00% hazard).
19. **`E22_sms_injection_immunity`**: Outbound SMS Prompt Injection (0 / 1,400 leaks in deterministic template vs 36.36% in LLM SMS).
20. **`E23_cache_invalidation_provenance`**: Cryptographic Cache Invalidation (100% tamper detection; 92.8% bandwidth reduction).
21. **`E24_coverage_gap_growth_loop`**: Knowledge Growth Loop (18 min authoring closed 100% Chili Anthracnose gap; 3.06 queries/min).
22. **`E25_intent_classifier_training`**: Lightweight Intent Classifier (78.4% joint match in 0.385 ms; 1.25 MB size; 3,242x speedup).
23. **`E26_chunk_fallback_coverage_safety`**: Grounded Chunk Fallback (Safe fallback for rare zero-source queries).
24. **`E28_metamorphic_authority_testing`**: Metamorphic Single-Record Authority Testing (11,000 cases; 100.0% rejection rate; 0.0% false certification).
25. **`E29_parametric_evidence_conflict`**: Parametric Prior vs. Evidence Conflict (1,000 conflict cases; 100.0% evidence adherence in BAA vs 30-56% intrusion in LLMs).
26. **`E27_independent_expert_benchmark`**: Independent End-to-End Agronomist Benchmark (3,000 cases across B0-B6; 96.8% CAC, 89.8% Coverage, 0.0% CUAR).

---

### B. Planned / Undone Experiments (12 Layers — Skeletons & Specs Prepared)

These experiments are fully specified and folderized under `paper/CEA Paper/experiments/<layer>/` with runner skeletons in `scripts/`, ready for live execution and data gathering:

1. **`E16_hardware_profiling`**: On-Device Hardware & Battery Profiling (Pending physical test on sub-$120 Android phone).
2. **`E30_temporal_source_authority_conflict`**: Temporal Validity & Source Authority Hierarchy (Current MoA vs outdated BARI/BRRI manuals).
6. **`E31_multimodal_perception_uncertainty`**: Multimodal Perception Uncertainty & Cross-Modal Conflict (Visual noise & symptom discrepancies).
7. **`E32_oracle_vs_predicted_routing`**: Oracle vs. Predicted Metadata Routing Decomposition (Isolating perception vs verification errors).
8. **`E33_high_confidence_wrong_routing`**: High-Confidence Wrong Classifier Metadata Resilience (Fail-closed defense under misclassified crop/pest).
9. **`E34_full_architectural_ablation`**: Full Architectural Layer Ablation (LLM $\rightarrow$ Vanilla RAG $\rightarrow$ Guarded $\rightarrow$ Authority $\rightarrow$ BAA).
10. **`E35_linguistic_query_normalization`**: Linguistic Query Normalization Ablation (Isolating text normalization from vision gating).
11. **`E36_source_fragmentation_assembly`**: Source Fragmentation & Multi-Document Assembly Hazard (Conflated multi-document citations).
12. **`E37_conversational_clarification_policy`**: Conversational Ambiguity Clarification Policy (Multi-turn symptom disambiguation).
13. **`E38_simulated_human_escalation_queue`**: Simulated Human Extension Escalation Queue (Workload model for Krishi 16123).
14. **`E39_ipm_non_chemical_balance`**: IPM & Non-Chemical Cultural Practice Balance (Evaluating chemical bias vs biological control).
15. **`E40_physical_edge_battery_profiling`**: Physical On-Device Edge Battery & Thermal Profiling (ARM CPU power & thermal measurements).

---

## 4. Single Source of Truth Ground Truth File

All quantitative results are sequentially indexed and aggregated into:
`paper/CEA Paper/experiments/results.yaml`

This file provides a unified, machine-readable, and human-readable audit trail of every completed metric, sample size, confidence interval, and execution script.
