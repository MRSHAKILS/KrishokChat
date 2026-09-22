# KrishokTech — EACL 2027 System Demonstration Track

This directory contains the complete publication package, experimental records, results Single Source of Truth (SSOT), and manuscript sources for the EACL 2027 System Demonstration submission:

> **KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory**  
> *Khan Raiyan Ibne Reza, Sanjana Aktar Maria, Shakil Ahmed, Sumaiya Tabassum Nimi*  
> Department of Computer Science and Engineering, North South University, Dhaka, Bangladesh  
> Interactive Demo: [https://krishoktech.vercel.app](https://krishoktech.vercel.app) | Screencast: [https://krishoktech.vercel.app/screencast](https://krishoktech.vercel.app/screencast)

---

## Directory Structure

```text
EACL Final/
├── paper/                      # Publication Manuscripts and Visual Assets
│   ├── latex/                  # Production LaTeX Package
│   │   ├── main.tex            # Canonical master LaTeX source
│   │   ├── main.pdf            # Compiled publication PDF
│   │   ├── krishoktech_eacl.bib# Verified bibliography
│   │   ├── acl.sty             # ACL / EACL official style file
│   │   └── acl_natbib.bst      # ACL Natbib citation style
│   ├── draft/                  # Markdown Manuscript Drafts
│   │   └── turn_1.md           # Full verified markdown draft with all tables & inputs
│   └── screenshots/            # High-Resolution Visuals & System UI States
│       ├── fig2_main_interface.png
│       ├── screenshot1_halt_clarification.png
│       ├── screenshot2_resumed_retrieval.png
│       ├── screenshot3_photo_crop_scope.png
│       ├── screenshot4_mismatch_badge.png
│       ├── screenshot5_grounded_answer.png
│       ├── screenshot7_16123_safety_referral.png
│       ├── screenshot8_offline_mode.png
│       └── screenshot9_sms_tts.png
├── results/                    # Results Single Source of Truth (SSOT)
│   └── paper_results.yaml      # All frozen metrics, sample sizes, and 95% CIs
├── experiments/                # Experimental Registries, Logs, and Traces
│   ├── LIMITATIONS.md          # Frozen 18-row system limitations ledger
│   ├── ground_truth.yaml       # Gold ground-truth labels and evaluation keys
│   ├── E01–E10/                # Core evaluation runs (latency, safety, footprint, etc.)
│   └── N01–N12/                # Confirmatory N-track experimental runs & autopsies
├── refinement/                 # Multi-Stage Manuscript Audits & Refinements
│   ├── step_1.md               # Stage 1: Diagnostic audit & citation reconciliation
│   ├── step_2.md               # Stage 2: Structural redesign & positioning plan
│   └── step_3.md               # Stage 3: Manuscript synthesis & evidence integration
└── plans/                      # Strategic Planning Documents & Roadmaps
    ├── roadmap.md              # Long-term research and evaluation roadmap
    ├── story_plan.md           # Narrative and positioning arcs
    └── problems_we_solved.md   # Core technical challenges solved
```

---

## Key Artifacts & Verification

- **LaTeX Master:** [`paper/latex/main.tex`](file:///d:/KrishokTech%20Advisory%20System/paper/EACL%20Final/paper/latex/main.tex) (compiles with `pdflatex` + `bibtex`, 0 errors, 0 undefined citations).
- **Compiled PDF:** [`paper/latex/main.pdf`](file:///d:/KrishokTech%20Advisory%20System/paper/EACL%20Final/paper/latex/main.pdf).
- **Markdown Draft:** [`paper/draft/turn_1.md`](file:///d:/KrishokTech%20Advisory%20System/paper/EACL%20Final/paper/draft/turn_1.md).
- **Evidence SSOT:** [`results/paper_results.yaml`](file:///d:/KrishokTech%20Advisory%20System/paper/EACL%20Final/results/paper_results.yaml).
- **Limitations Ledger:** [`experiments/LIMITATIONS.md`](file:///d:/KrishokTech%20Advisory%20System/paper/EACL%20Final/experiments/LIMITATIONS.md).
