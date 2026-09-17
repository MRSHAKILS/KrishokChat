# Computers and Electronics in Agriculture (CEA) Paper Workspace

**Target Journal:** *Computers and Electronics in Agriculture* (Elsevier, Impact Factor: 7.7, CiteScore: 12.2, Q1)  
**Article Type:** Full Original Research Paper (approx. 9,000–12,000 words, 18 pages in Elsevier `cas-dc` format)  
**Manuscript Title:** *Bounded-Authority Verification for Safety-Critical Pesticide Advisory in Low-Resource Bengali Agriculture*  
**Authors:** Raiyaan Reza (North South University)  
**Status:** **100% Self-Contained, Audited, and Submission-Ready**  

---

## 1. Executive Summary & Folder Self-Sufficiency

This folder (`paper/CEA Paper/`) is designed as an **individually rich, completely self-contained research and manuscript package**. If you share or archive this folder, any writer, co-author, or reviewer can independently:
1. **Review and Compile the Manuscript:** Full modular LaTeX source files (`.tex`, `.bib`, `tables/`, `sections/`, `figures/`) and freshly compiled `krishokchat_cea_main.pdf`.
2. **Audit Quantitative Claims:** Trace every single number, percentage, and confidence interval back to `manuscript/NUMBER_BANK.md`.
3. **Inspect Experiment Layers (E02–E40):** 38 individual experiment directories containing layer-specific READMEs, frozen JSON/YAML data, and Python evaluation scripts (`scripts/`).
4. **Access Peer Reviews & Writing Roadmaps:** Full 100 KB comprehensive reviewer report (`reviews/reviewer_1.md`) and editorial revision guide (`reviews/writing suggestions.md`).

---

## 2. Directory Structure & File Map

```
paper/CEA Paper/
├── README.md                      <-- This guidebook
├── manifest.yaml                  <-- Machine-readable file & artifact manifest
├── manuscript/                    <-- Active, compilable LaTeX manuscript package
│   ├── main.tex                   <-- Consolidated monolithic LaTeX manuscript (cas-dc document class)
│   ├── main.pdf                   <-- Compiled 22-page publication PDF (0 errors)
│   ├── krishokchat_cea.bib        <-- Complete verified BibTeX database (0 placeholders)
│   ├── NUMBER_BANK.md             <-- 160 KB canonical dictionary for all quantitative claims
│   ├── tables/                    <-- Reference booktabs LaTeX tables
│   ├── figures/                   <-- All 6 high-resolution publication figures (fig_1 to fig_6)
│   └── thumbnails/                <-- Elsevier CAS template visual assets
├── experiments/                   <-- Complete empirical research layer repository
│   ├── results.yaml               <-- 187 KB consolidated master results (single source of truth)
│   ├── run_all_remaining.py       <-- Master batch runner script
│   └── E02_relational_misbinding/ <-- Layer-specific folder (38 total, E02 to E40)
│       ├── README.md              <-- Layer protocol, hypotheses, and bounds
│       ├── results.yaml / .json   <-- Frozen measured metrics & 95% Wilson CIs
│       └── scripts/               <-- Standalone Python runner & evaluation script
├── reviews/                       <-- Peer review & editorial assessment package
│   ├── reviewer_1.md              <-- 100 KB in-depth CEA Reviewer 1 report & critique
│   └── writing suggestions.md     <-- 42 KB line-by-line editorial roadmap & suggestions
└── drafts/                        <-- Section-by-section markdown drafts & planning archives
    ├── 01_introduction.md ... 18_conclusion.md
    ├── PLANNING_DIGEST.md         <-- Consolidated 46 KB planning & synthesis document
    └── writing_outline.md         <-- Original structural drafting outline
```

---

## 3. How to Compile the Manuscript PDF

The manuscript uses Elsevier's official `cas-dc` double-column document class. To compile cleanly:

```bash
cd "paper/CEA Paper/manuscript"
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

> **Note on Float Placement:** All figure and table environments use `[pos=t]` syntax adhering to Elsevier CAS parser specifications. Figures are positioned inline within their respective sections (§3, §4, §8, §9, §10).

---

## 4. Master Empirical Portfolio (38 Experiment Layers)

All empirical claims in the manuscript trace directly to frozen evaluations in `experiments/`:

| Layer ID | Name / Investigation Target | Key Metric(s) | Results Status | Script Location |
|---|---|---|:---:|---|
| **E02** | Relational Misbinding Attack Suite (10,000 cases) | 100.0% Rejection, 0.0% CUAR | Frozen | `E02_relational_misbinding/scripts/` |
| **E03** | 11-Slot Hazard Prevention Ablation | Hazard surges (+31.6% dosage) | Frozen | `E03_slot_ablation/scripts/` |
| **E04** | Risk--Coverage Calibration (20,112 cases) | AURC = 0.0153, 84.56% coverage @ 1.26% risk | Frozen | `E04_risk_coverage_calibration/scripts/` |
| **E05** | Counterfactual Evidence Binding (2,000 pairs) | CBC = 1.0000, 0.0% false certification | Frozen | `E05_counterfactual_binding/scripts/` |
| **E06** | Multi-Register Bengali Benchmark (4,000 cases) | 0.0% dangerous acceptance across all 4 registers | Frozen | `E06_farmer_dialect_benchmark/scripts/` |
| **E07/E08** | Prompt Injection & Context Poisoning (1,400 cases) | 0.0% attack survivability (0/1,400 leaks) | Frozen | `E07_E08_prompt_injection/scripts/` |
| **E09** | Stage-Level Latency Decomposition | 3.8 ms in-process verification vs 1,780 ms gen | Frozen | `E09_latency_economics/scripts/` |
| **E10** | Root-Cause Residual Failure Audit (100 cases) | 28% omission, 22% misbinding (0% dangerous leak) | Frozen | `E10_failure_taxonomy/scripts/` |
| **E11** | Multi-Generator Invariance (5 models) | Rejection invariance across Gemma, Llama, Mistral | Frozen | `E11_multi_generator_invariance/scripts/` |
| **E12** | Retrieval Degradation & Safe Abstention | 0.0% hazard under 100% poisoned retrieval | Frozen | `E12_retrieval_degradation/scripts/` |
| **E13** | Agronomist Human Evaluation Study (200 cases) | 4.82/5 correctness, Gwet's AC1 = 0.862 | Frozen | `E13_human_expert_validation/scripts/` |
| **E14** | Rural Cellular Network Resilience | 91.4% delivery @ 15% loss, 58.1% @ 30% loss | Frozen | `E14_network_degradation/scripts/` |
| **E15** | Deterministic 160-char SMS Compression | 100.0% safety slot retention vs 35.6% in LLM SMS | Frozen | `E15_sms_compressor/scripts/` |
| **E17** | Detection-Gated Routing Efficiency | 75.64% search space collapse, +36.6 pp dialect Hit@1 | Frozen | `E17_detection_gated_routing/scripts/` |
| **E18** | LLM Dependency Reduction | 61.52% zero-LLM resolution, 2.28x speedup | Frozen | `E18_llm_dependency_reduction/scripts/` |
| **E19** | Knowledge Graph Traversal Mechanism | 100% slot completeness in 0.0128 ms | Frozen | `E19_knowledge_graph_traversal/scripts/` |
| **E20** | Serving Economics & Channel Costs | $0.000257 app-online (89.65% cheaper than cloud) | Frozen | `E20_telecom_economics/scripts/` |
| **E21** | Dialect Hazard Routing Cross-Tab | 89.8% dialect coverage, 0.0% hazard | Frozen | `E21_dialect_hazard_routing/scripts/` |
| **E22** | Outbound SMS Injection Immunity | 0/1,400 leaks in deterministic template | Frozen | `E22_sms_injection_immunity/scripts/` |
| **E23** | Cryptographic Cache Invalidation & Tamper | 100.0% tamper detection, 92.8% bandwidth cut | Frozen | `E23_cache_invalidation_provenance/scripts/` |
| **E24** | Knowledge Authoring Growth Loop | 18 min closed Chili Anthracnose gap (3.06 q/min) | Frozen | `E24_coverage_gap_growth_loop/scripts/` |
| **E25** | Lightweight Intent Classifier | 78.4% joint match in 0.385 ms, 1.25 MB footprint | Frozen | `E25_intent_classifier_training/scripts/` |
| **E26** | Grounded Chunk Fallback Coverage | Dark-launched safe fallback for zero-source queries | Frozen | `E26_chunk_fallback_coverage_safety/scripts/` |
| **E27** | Independent Live Expert Benchmark (100 cases) | 97.0% CAC, 0.0% CUAR across live queries | Frozen | `E27_independent_expert_benchmark/scripts/` |
| **E28** | Metamorphic Single-Record Authority Testing | 11,000 cases; 100.0% rejection across 11 operators | Frozen | `E28_metamorphic_authority_testing/scripts/` |
| **E29** | Parametric Prior vs. Evidence Conflict | 100.0% evidence adherence in BAA vs 30-56% intrusion | Frozen | `E29_parametric_evidence_conflict/scripts/` |
| **E30** | Temporal Source Authority & Gazette Precedence | 100.0% current-gazette adherence vs 75% RAG leakage | Frozen | `E30_temporal_source_authority_conflict/scripts/` |
| **E31** | Multimodal Perception Conflict | 100.0% clarification triggering on visual mismatch | Frozen | `E31_multimodal_perception_uncertainty/scripts/` |
| **E32–E39** | Ablations, Normalization & Escalation Queue | Comprehensive supporting evaluations | Frozen | `E32_.../scripts/` to `E39_.../scripts/` |

---

## 5. Single Source of Truth for Quantitative Claims

Every numerical claim in the text, abstract, and tables is mapped to:
- **`manuscript/NUMBER_BANK.md`**: 160 KB indexed dictionary of frozen constants.
- **`experiments/results.yaml`**: 187 KB master YAML containing full experimental metadata, parameters, metrics, sample sizes ($n$), and 95% Wilson confidence intervals.
