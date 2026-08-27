# Section 01: Introduction (Draft Skeleton)

## 1.1 Agricultural Advisory as a Safety-Critical Computing Challenge
- Smallholder context in Bangladesh (16M farming households, intensive cropping, low extension ratio).
- Rise of LLMs and RAG in agricultural advisory (Farmer.Chat, KrishokBondhu).
- The fundamental flaw: linguistic fluency != factual authority.
- Real-world consequences of agrochemical hallucinations (phytotoxicity, toxic residues, poisoning, economic ruin).

## 1.2 The Failure of Standard Retrieval and Post-Hoc Guardrails
- RAG limitations: multi-document context conflation, cross-row misbinding in tabular facts.
- Generative models synthesize composite recommendations combining correct crops with wrong chemicals/doses.
- Post-hoc LLM judges and toxicity filters miss subtle numerical mutations (dosage, PHI, dilution volume).

## 1.3 The Bounded-Authority Paradigm
- Core thesis: LLM as language realization component, NOT factual authority.
- Authority restricted exclusively to structured, version-controlled institutional records.
- Fail-closed decision contract: if evidence is incomplete/ambiguous, the system must abstain or escalate.

## 1.4 Research Questions (RQ1–RQ5)
- RQ1: Authority & Advisory Correctness
- RQ2: Relational Evidence Integrity
- RQ3: Selective Reliability & Uncertainty
- RQ4: Linguistic & Multimodal Robustness
- RQ5: Constrained Deployment & Efficiency

## 1.5 Principal Contributions
- Formulation of Bounded-Authority Advisory Architecture (BAA).
- Five-tier selective resolution ladder resolving >60% traffic without generative LLMs.
- Multi-axis empirical evaluation (10k misbinding, 4k multi-register, agronomist studies, offline cache, SMS).
