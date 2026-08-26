# KrishokChat v2 Experimental Master Plan

**Target Venue:** Wiley *Expert Systems* (ISSN: 1468-0394)  
**Title:** *KrishokChat: A Knowledge-Engineered Expert System for Relation-Aware Certification of Safety-Critical Agricultural Advisory*  
**Scope:** Knowledge Engineering, Calibrated Decision Making, Relational Certification, Edge Deployment & Robustness

---

## 1. Research Questions (RQs)

* **RQ1 (Relational Certification):** Does evidence-linked typed relation verification eliminate safety-critical false acceptances caused by relational slot misbinding in lexical and LLM-judge baselines?
* **RQ2 (Risk-Controlled Calibration):** How does selective calibration on development data trade off certification coverage against unsafe acceptance, and does it outperform generic uncertainty baselines?
* **RQ3 (Schema Slot Sensitivity):** Which relational slots (dose bounds, PHI, active ingredient, crop host) contribute most critically to preventing agrochemical advisory hazards?
* **RQ4 (Environmental & Linguistic Robustness):** Does the expert system maintain safety non-inferiority ($\Delta_{\text{safety}} \le 0$) under regional Bengali dialects, romanized Banglish, and authentic colloquial farmer queries?
* **RQ5 (Operational Economics & Latency):** Can a deterministic-first five-tier resolution ladder reduce serving costs and p95 latency while preserving a 100% fail-closed safety boundary?
* **RQ6 (Generator & Retrieval Invariance):** Does the relation verifier generalize across heterogeneous base generators (Gemma-4, LLaMA-3, Qwen) and degrade safely under retrieval uncertainty?

---

## 2. Seven Baseline Comparison Systems

| System ID | Architecture Name | Routing / Pre-guard | Generator Model | Verification Mechanism | Decision Policy |
|---|---|---|---|---|---|
| **B1** | `LLM-Direct` | None | Fine-tuned Gemma-4 | None | Always Answer |
| **B2** | `Vanilla-RAG` | None | Gemma-4 + BM25/Dense | None | Always Answer |
| **B3** | `RAG-Citation` | None | Gemma-4 + BM25/Dense | Prompted in-context citations | Soft Prompted |
| **B4** | `RAG-Lexical` | None | Gemma-4 + BM25/Dense | Substring / Token matching | Fixed Overlap Cutoff |
| **B5** | `RAG-LLM-Judge` | None | Gemma-4 + BM25/Dense | Dual LLM Self-Critique | Soft Confidence ($\theta$) |
| **B6** | `RAG-Conformal` | None | Gemma-4 + BM25/Dense | CAP / Temperature Scaling | Conformal Threshold |
| **B7 (Ours)** | **`KrishokChat-Full`** | **Tier 0–2 Deterministic** | **Gemma-4 4-bit** | **Typed Relational Matcher** | **Calibrated Selective** |

---

## 3. Ten Experimental Layers (E1–E10)

1. **E1 (End-to-End Operational Matrix):** Correctness, Evidence Support, Dangerous Acceptance Rate (95% Wilson CI), Safe Abstention, F1, Latency, Cost.
2. **E2 (Relational-Misbinding Stress Test):** 10-family adversarial corruption (Dose, Unit, Denominator, Crop, Pathogen, Formulation, PHI, Interval, Polarity, Cross-Row).
3. **E3 (11-Slot Schema Ablation):** Systematic deletion of slots from $\mathcal{C}$ measuring delta in Dangerous Acceptance and AURC.
4. **E4 (Calibration & Risk-Coverage Curves):** Selective risk vs coverage, AURC, ECE, Brier score, dev-to-test threshold transfer ($\theta^*$).
5. **E5 (Counterfactual Evidence Binding):** Measuring Counterfactual Binding Consistency ($CBC = P(\text{CERTIFY}|\text{true}) - P(\text{CERTIFY}|\text{counterfactual})$).
6. **E6 (Ecological Farmer Benchmark):** Evaluation on 1,001 authentic farmer queries from Paper 1.
7. **E7 (Linguistic & Dialect Robustness):** Safety non-inferiority ($\Delta_{\text{safety}} \le 0$) across Chittagong, Sylhet, Noakhali, and Banglish.
8. **E8 (Security & Prompt Injection):** Direct override, Evidence override, Bengali injection, Retrieval poisoning attack success rates.
9. **E9 (Systems Economics & Latency Decomposition):** $L_{\text{total}} = L_{\text{route}} + L_{\text{ret}} + L_{\text{gen}} + L_{\text{ver}} + L_{\text{ren}}$, Cost per Safe Answer ($C_{safe}$).
10. **E10 (Safety Failure Taxonomy):** 100-case failure categorization across Retrieval, Binding, Numerical, Regulatory, and Linguistic dimensions.

---

## 4. Figures (1–10) & Tables (1–11) Target Set

* **Fig 1:** Four-Stage Expert System Architecture & Funnel.
* **Fig 2:** Why Lexical Verification Fails (Relational Misbinding Illustration).
* **Fig 3:** Claim $\to$ Evidence Slot Alignment & Constraint Checking.
* **Fig 4:** Risk–Coverage Curves across Verification Baselines.
* **Fig 5:** Three-Way Pareto Frontier (Safety Risk vs Coverage vs Serving Cost).
* **Fig 6:** Ecological Robustness on 1,001 Farmer Queries & Dialect Registers.
* **Fig 7:** Distribution Shift & Held-out Crop/Chemical Performance.
* **Fig 8:** Counterfactual Evidence Perturbation Dynamics.
* **Fig 9:** Stage-wise Latency Breakdown (p50, p95, p99).
* **Fig 10:** Safety Failure Taxonomy & Root-Cause Distribution.

---

## 5. Structured YAML Logging Standard

All evaluation runs must output machine-readable, schema-validated YAML files containing:
- `experiment_id`: (e.g., `E2_RELATIONAL_MISBINDING`)
- `timestamp`: UTC ISO-8601
- `git_commit`: SHA hash
- `random_seed`: `20260813`
- `dataset_hash`: SHA-256
- `metrics`: Dictionary of metrics with mean, sample count, and 95% Wilson confidence intervals `[ci_lower, ci_upper]`.
- `execution_summary`: Latency (p50, p95, p99) and hardware profile.
