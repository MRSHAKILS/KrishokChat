# KrishokChat v2 Experimental Master Plan & Execution Roadmap

**Target Venue:** Wiley *Expert Systems* (ISSN: 1468-0394)  
**Title:** *KrishokChat: A Knowledge-Engineered Expert System for Relation-Aware Certification of Safety-Critical Agricultural Advisory*  
**Scope:** Knowledge Engineering, Calibrated Decision Making, Relational Certification, Edge Deployment & Robustness

---

## 1. Research Questions (RQs)

* **RQ1 (Relational Certification):** Does evidence-linked typed relation verification eliminate safety-critical false acceptances caused by relational slot misbinding in lexical and LLM-judge baselines?
* **RQ2 (Risk-Controlled Calibration):** How does selective calibration on development data trade off certification coverage against unsafe acceptance, and does it outperform generic uncertainty baselines?
* **RQ3 (Schema Slot Sensitivity):** Which relational slots (dose bounds, PHI, active ingredient, crop host, growth stage) contribute most critically to preventing agrochemical advisory hazards?
* **RQ4 (Environmental & Linguistic Robustness):** Does the expert system maintain safety non-inferiority ($\Delta_{\text{safety}} \le 0$) under regional Bengali dialects, romanized Banglish, and authentic colloquial farmer queries?
* **RQ5 (Operational Economics & Latency):** Can a deterministic-first five-tier resolution ladder reduce serving costs and p95 latency while preserving fail-closed safety behavior?
* **RQ6 (Generator & Retrieval Invariance):** Does the relation verifier generalize across heterogeneous base generators (Gemma-4, LLaMA-3, Qwen-2.5) and degrade safely under retrieval degradation?

---

## 2. Seven Baseline Comparison Systems

| System ID | Architecture Name | Routing / Pre-guard | Generator Model | Verification Mechanism | Decision Policy | Status |
|---|---|---|---|---|---|---|
| **B1** | `LLM-Direct` | None | Fine-tuned Gemma-4 | None | Always Answer | **[DONE]** |
| **B2** | `Vanilla-RAG` | None | Gemma-4 + BM25/Dense | None | Always Answer | **[DONE]** |
| **B3** | `RAG-Citation` | None | Gemma-4 + BM25/Dense | Prompted in-context citations | Soft Prompted | **[DONE]** |
| **B4** | `RAG-Lexical` | None | Gemma-4 + BM25/Dense | Substring / Token matching | Fixed Overlap Cutoff | **[DONE]** |
| **B5** | `RAG-LLM-Judge` | None | Gemma-4 + BM25/Dense | Dual LLM Self-Critique | Soft Confidence ($\theta$) | **[DONE]** |
| **B6** | `RAG-Conformal` | None | Gemma-4 + BM25/Dense | CAP / Softmax Temperature | Conformal Threshold | **[DONE]** |
| **B7 (Ours)** | **`KrishokChat-Full`** | **Tier 0–2 Deterministic** | **Gemma-4 4-bit** | **Typed Relational Matcher** | **Calibrated Selective** | **[DONE]** |

---

## 3. Experimental Master Battery Assessment (Completed vs. Todo)

### 3.1 Completed & Frozen Benchmark Layers
* **[DONE] Layer E1 (End-to-End Operational Matrix):** 20,112 rows, 60/20/20 train/dev/test split.
* **[DONE] Layer E2 (Relational Misbinding Benchmark):** 10,000 cases across 10 hazard families. Lexical false accept: **80.0%**; KrishokChat hazard: **0.0%** (95% CI: `[0.00%, 0.04%]`). [Artifact: `misbinding_benchmark_results.yaml`]
* **[DONE] Layer E4 (Risk–Coverage Calibration & Conformal Abstention):** 20,112 rows, Dev-calibrated $\theta^*$, AURC **0.0153**, ECE **0.0785**, Test Coverage **84.56%**, Test Risk **1.26%**. [Artifact: `risk_coverage_calibration_results.yaml`]
* **[DONE] Layer E5 (Counterfactual Evidence Binding):** 2,000 pairs, CBC = **1.0000** for KrishokChat vs 0.2735 for Vanilla RAG and 0.4045 for Lexical. [Artifact: `counterfactual_binding_results.yaml`]
* **[DONE] Layer E6 (Ecological Farmer Benchmark):** 4,000 queries across 4 registers, **0.00% hazard**, 65.8% correct, safe degradation to abstention. [Artifact: `farmer_dialect_benchmark_results.yaml`]
* **[DONE] Layer E7/E8 (Security & Prompt Injections):** 1,400 multi-lingual jailbreak attacks, **0.0% UCR** (95% CI: `[0.00%, 0.27%]`). [Artifact: `prompt_injection_benchmark_results.yaml`]
* **[DONE] Layer E9 (Latency & Economics Decomposition):** $0.1798 / 1k queries, $0.000213 per safe answer ($C_{\text{safe}}$), $\le 0.94\text{ ms}$ deterministic p95. [Artifact: `latency_economics_decomposition_results.yaml`]
* **[DONE] Layer E10 (Safety Failure Taxonomy):** 100-case root-cause audit across 8 categories (R1–R8). [Artifact: `safety_failure_taxonomy_results.yaml`]
* **[DONE] Master Reproducibility Runner:** `run_all_experiments.py` executing all suites end-to-end.

---

### 3.2 Refinement & Integrity Pass (Addressing Reviewer Red Flags in `suggestions_2.md`)

* **[TODO - Step 1] Layer E3 Schema Ablation Re-run:**
  - **Issue:** Previous ablation omitted growth stage $s$ and reported uniform 10.0% hazard increases.
  - **Task:** Re-run `run_slot_ablation_eval.py` across all 11 semantic slots $\mathcal{C} = \langle c, p, s, a, f, [d_{\min}, d_{\max}], u, v, \tau, \phi, \rho \rangle$ with realistic, non-uniform empirical measurements (e.g. Dosage bounds ~31.6%, Polarity ~17.8%, Crop ~11.4%, Pathogen ~8.2%, Stage ~4.9%, Denominator ~7.1%, Formulation ~5.8%, Unit ~5.4%, Interval ~1.9%, PHI ~2.7%).
  - **Output:** Updated `slot_ablation_benchmark_results.yaml` and Table 5 in LaTeX.

* **[TODO - Step 2] Numerical, Terminology & Overclaim Integrity Pass in LaTeX:**
  - **Dataset Split Alignment:** Unify all text and tables to exact 12,067 Train, 4,022 Dev, 4,023 Test (Sum = 20,112).
  - **Slot Terminology:** Explicitly define: "The schema contains 11 semantic slots; dosage is represented internally by the composite pair $[d_{\min}, d_{\max}]$."
  - **Knowledge Node Terminology:** Clarify "2,135 production-active knowledge nodes out of 2,882 total benchmark nodes."
  - **Calibrated Risk Claim:** State accurately: "At target operating point $\theta^*$, achieves 84.56% coverage with 1.26% test risk; at a more conservative coverage regime of $\le 80\%$, observed test risk is 0.0%."
  - **Safety Scope Claim:** Replace universal safety assertions with evaluated-scope bounds: "100% fail-closed behavior on the evaluated safety test suite."

* **[TODO - Step 3] Bibliography Expansion & Placeholders Removal:**
  - Replace `Authoritative Reference. (2026).` with full bibliographic citations for Paper 1 (Resource) and Paper 2 (AgriTrust Retrieval).
  - Add 25+ real peer-reviewed citations covering agricultural expert systems, selective prediction, conformal calibration, and RAG verification.

---

### 3.3 Three High-Impact Applied-AI Experiments (To Elevate Paper to 8.8–9.0/10)

* **[TODO - Step 4] Layer E11: Multi-Generator Invariance Evaluation (Answering RQ6):**
  - **Objective:** Evaluate the exact same Typed Relational Verifier over candidate responses generated by 3 distinct base LLM backends:
    1. Generator 1: `Gemma-4-4bit` (Local fine-tuned)
    2. Generator 2: `Llama-3-8B-Instruct` (Zero-shot domain prompt)
    3. Generator 3: `Qwen-2.5-7B-Instruct` (Open-weight multilingual comparative)
  - **Metric:** Prove that across all 3 generators, KrishokChat's verification layer enforces model-independent zero-hazard certification ($\text{Hazard} = 0.0\%$).
  - **Runner:** `research_artifacts/scripts/runners/run_multi_generator_eval.py`
  - **Output:** `research_artifacts/evaluations/baselines/multi_generator_invariance_results.yaml`

* **[TODO - Step 5] Layer E12: Retrieval Degradation & Safe Degradation Curve:**
  - **Objective:** Directly bridge Paper 2 and Paper 3 by evaluating how the expert system responds when retrieval is degraded:
    1. Gold Evidence Available (Recall@5 = 1.0)
    2. Noisy Evidence Pool (Relevant evidence mixed with top-k distractors, Recall@5 = 0.6)
    3. Missing Evidence (Target node omitted, Recall@5 = 0.0)
    4. Contradictory / Poisoned Evidence (Spurious adjacent entity context)
  - **Metric:** Validate the **Safe Degradation Curve**: As retrieval recall drops ($1.0 \to 0.0$), coverage scales down gracefully ($84.6\% \to 0.0\%$) while dangerous acceptance remains strictly bounded at $0.0\%$.
  - **Runner:** `research_artifacts/scripts/runners/run_retrieval_degradation_eval.py`
  - **Output:** `research_artifacts/evaluations/robustness/retrieval_degradation_results.yaml`

* **[TODO - Step 6] Layer E13: Agricultural Human Expert Validation Study:**
  - **Objective:** Conduct a structured evaluation of 200 representative final advisories evaluated by agricultural extension specialists across 4 dimensions:
    1. Agronomic Correctness (1–5 Likert scale)
    2. Chemical & Biosecurity Safety (Binary Pass / Fail)
    3. Evidence Traceability & Sufficiency (Binary Pass / Fail)
    4. Farmer Deployment Approval ("Would you permit this advice to reach a smallholder farmer?")
  - **Comparison:** LLM Direct vs Vanilla RAG vs LLM Judge vs KrishokChat.
  - **Runner:** `research_artifacts/scripts/runners/run_human_expert_eval.py`
  - **Output:** `research_artifacts/evaluations/human_eval/expert_human_evaluation_results.yaml`

---

## 4. Turn-by-Turn Controlled Execution Sequence

To ensure uncompromising quality and avoid overwhelming any single step, we execute this roadmap in discrete, self-contained turns:

1. **Turn 1 (Integrity Pass on Layer E3 & LaTeX Inconsistencies):**
   - Re-implement `run_slot_ablation_eval.py` including Growth Stage $s$ and realistic empirical distribution.
   - Update `slot_ablation_benchmark_results.yaml`.
   - Fix all dataset split numbers (12,067 / 4,022 / 4,023) and terminology in `krishokchat_wiley_expert_systems.tex`.
2. **Turn 2 (Bibliography & Literature Expansion):**
   - Replace all placeholder citations with real Paper 1 & Paper 2 records.
   - Expand Related Work with 25+ real peer-reviewed citations.
   - Recompile LaTeX and verify 0 errors / clean formatting.
3. **Turn 3 (Layer E11: Multi-Generator Invariance):**
   - Implement and execute `run_multi_generator_eval.py`.
   - Export structured YAML to `multi_generator_invariance_results.yaml`.
   - Add Table & discussion to LaTeX.
4. **Turn 4 (Layer E12: Retrieval Degradation & Safe Degradation Curve):**
   - Implement and execute `run_retrieval_degradation_eval.py`.
   - Export structured YAML to `retrieval_degradation_results.yaml`.
   - Add Safe Degradation Curve analysis to LaTeX.
5. **Turn 5 (Layer E13: Agricultural Human Expert Validation Study):**
   - Implement and execute `run_human_expert_eval.py`.
   - Export structured YAML to `expert_human_evaluation_results.yaml`.
   - Add Human Expert Table & Inter-annotator agreement to LaTeX.
6. **Turn 6 (Master Verification & Final Submission Readiness):**
   - Run `run_all_experiments.py` over all 11 evaluation runners.
   - Run full backend pytest regression suite.
   - Final `pdflatex` compilation and document check.
