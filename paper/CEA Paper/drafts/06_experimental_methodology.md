# Section 06: Experimental Methodology (Draft Skeleton)

## 6.1 Scientific Principles & Reproducibility Protocol
- Frozen test sets on disk, pre-registered random seeds (20260827), 95% Wilson confidence intervals.
- Strict data-split separation: D_train, D_dev (calibration), D_test (naturalistic), D_redteam (adversarial).

## 6.2 Benchmark Suites
- Adversarial Misbinding Suite (10,000 cases).
- 11-Slot Hazard Prevention Suite (10,000 cases).
- Multi-Register Bengali Benchmark (4,000 cases: Standard, Dialects, Banglish, Farmer Voice).
- Security Injection Suite (1,400 cases).
- Rural Network Degradation Suite (1,000 queries across 4 profiles).

## 6.3 Evaluated Baselines (B0–B6)
- Table 4: B0 (LLM-Only), B1 (Vanilla RAG), B2 (Guarded RAG), B3 (RAG + LLM Judge), B4 (Deterministic), B5 (BAA Proposed), B6 (Evidence-Constrained Multi-Doc RAG).

## 6.4 Agronomist Expert Evaluation Protocol
- Triple-blind study with 5 practicing agronomists/DAE officers.
- Inter-rater agreement measured via Gwet's AC1 (target >= 0.85).
