# EACL 2027 System Demonstrations Paper Workspace

**Target Venue:** *EACL 2027 System Demonstrations* (Association for Computational Linguistics)  
**Track:** System Demonstrations (Peer-Reviewed Proceedings)  
**Format:** $\le 6$ pages (excluding references) + Live System + $\le 2.5$-minute Screencast  
**Status:** ALL 8 EXPERIMENTS EXECUTED AND VERIFIED  
**Last Audited:** 2026-08-28  **Last Executed:** 2026-08-28  

---

## 1. System Demonstration Identity & Pitch

- **Title:** *KrishokChat: A Safety-Aware Multimodal Bengali Agricultural Advisory Platform*
- **One-Sentence System Pitch:** *KrishokChat is an open, production-oriented Bengali agricultural advisory platform integrating safety screening, hybrid retrieval, grounded generation, multimodal crop-disease diagnosis, and observable verification traces into a unified decision workflow.*

### Core System Themes for EACL Reviewers
1. **Integrated NLP & Vision Decision Pipeline:** Connecting safety classification, hybrid BM25+dense retrieval, fine-tuned Gemma-4 generation, and INT8 ONNX crop/disease classification into a single observable workflow.
2. **Transparent User Observability:** Surfacing real-time agent trace steppers (Checking safety $\rightarrow$ Retrieving sources $\rightarrow$ Generating answer $\rightarrow$ Verifying bounds) and expandable "Why this advice?" panels.
3. **Low-Resource Linguistic Robustness:** End-to-end support for Standard Bengali, Sylheti/Chittagonian regional dialects, Romanized Banglish, and uncurated farmer voice queries.
4. **Constrained Deployment & Human-in-the-Loop:** Offline-first caching, deterministic 160-char SMS compression, and case-summary escalation to the national Krishi Call Center (16123).

---

## 2. Project Progress & Status Tracker

| Area / Component | Target / Scope | Completed | Remaining | Progress Status |
|---|:---:|:---:|:---:|:---:|
| **Manuscript LaTeX Skeletons** | 6 Sections ($\le 6$ pages) | 6 Skeletons | 0 | **100% Structured** |
| **LaTeX Table Definitions** | 4 Tables | 4 Tables | 0 | **100% Pre-formatted** |
| **Section Markdown Outlines** | 6 Drafts | 6 Outlines | 0 | **100% Ready** |
| **BibTeX Literature Database** | 15 Citations | 15 Citations | 0 | **100% Verified Citations** |
| **System Demo Experiments** | 8 Key Layers | 8 Layers | 0 | **100% Executed, Verified & Committed** |
| **Unified Results Ground Truth** | 1 Master YAML | 1 Master YAML | 0 | **100% Compiled & Verified** |

---

## 3. Directory Structure

```
paper/EACL Demo/
├── README.md                      # This file (venue guidelines, page budget, progress tracker)
├── manifest.yaml                  # Local artifact registry tracking all files
├── manuscript/                    # Production LaTeX submission workspace (ACL/EACL format)
│   ├── krishokchat_eacl_main.tex  # Master LaTeX driver file
│   ├── krishokchat_eacl.bib       # BibTeX bibliography
│   ├── sections/                  # 6 modular LaTeX section skeletons
│   │   ├── 01_introduction.tex
│   │   ├── 02_system_architecture.tex
│   │   ├── 03_demonstration_scenarios.tex
│   │   ├── 04_empirical_usability.tex
│   │   ├── 05_deployment_ethics.tex
│   │   └── 06_conclusion.tex
│   └── tables/                    # 4 modular LaTeX table definitions
│       ├── tab1_system_capabilities.tex
│       ├── tab2_demo_scenarios.tex
│       ├── tab3_usability_metrics.tex
│       └── tab4_deployment_footprint.tex
├── drafts/                        # 6 section draft markdown skeletons
│   ├── 01_introduction.md
│   ├── 02_system_architecture.md
│   ├── 03_demonstration_scenarios.md
│   ├── 04_empirical_usability.md
│   ├── 05_deployment_ethics.md
│   └── 06_conclusion.md
└── experiments/                   # System evaluation & benchmark battery
    ├── results.yaml               # Unified root SSOT results YAML
    ├── E01_system_latency_breakdown/
    ├── E02_multimodal_diagnostic_workflow/
    ├── E03_safety_screening_accuracy/
    ├── E04_agentic_trace_observability/
    ├── E05_human_usability_sus/
    ├── E06_offline_cache_resilience/
    ├── E07_docker_deployment_footprint/
    └── E08_cross_modal_conflict_handling/
```
