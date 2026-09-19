# KrishokTech — Literature Review Scope & Angles Master List

**Generated:** 2026-08-12
**Purpose:** Definitive list of every literature-review angle needed to position KrishokTech
as a **system / application / industry-track** paper (ACL System Demonstrations, EMNLP
Industry, AAAI Demo, IJCAI, KDD Applied Data Science, CIKM Applied Research, NeurIPS
Datasets & Benchmarks, WACV, ICT4D). Latest papers through **August 2026** are the
priority; each scout was told to focus on 2025 → 2026-08.

---

## Project Context (what we're positioning)

KrishokTech is a safety-aware, retrieval-grounded, Bengali agricultural advisory system
for smallholder farmers in Bangladesh. Research artifacts:

| Component | Details |
|---|---|
| **Bengali hybrid-RAG Q&A** | BM25 (k1=2.2, b=0.4) + FAISS dense (mE5-small, 384-d), 2,120 knowledge nodes from 13 Bangladeshi institutions (BARC, BARI, DAE, CABI…), source-cited grounded answers |
| **Safety-aware agentic pipeline** | Safety/Router → Retrieval → Generation → Verifier; 6-way classification (`safe_agri`, `banned_or_restricted_chemical`, `self_harm_or_poisoning_risk`, `off_topic`, `prompt_injection`, `low_confidence`); canned redirect to Krishi Call Center 16123; local JSONL audit trail → safety metrics panel |
| **Low-resource safety dataset** | 20,112 records (T3 refusal 3,216 + T4 requery 16,896), 6 Bangla dialects, 12 categories, 75 crops, 110-word genuine dialect map; published on HuggingFace `RaiyanKhaan/krishokChat` |
| **Vision pipeline** | Crop classifier (6 families) → per-crop disease classifier (rice 8 / corn 4 / potato 3 / brassica 11 / wheat 11 = 35 disease classes), all `task: classify` (no detection claims); Bengali disease knowledge map; verified 88% wheat accuracy, 99.8% info coverage |
| **LLM adapters** | Replaceable port: OpenRouter/Gemini, local fine-tuned Gemma 4B 4-bit via Ollama (GGUF), stub |
| **Frontend** | Next.js 16, SSE streaming with agent-trace stepper, safety metrics + research/benchmark panels (precomputed) |
| **Authoritative papers** | *KrishokTech: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory* (EACL 2026, 85,979 instances, 4 tracks, 6 dialects) + *AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval* (2,882-node KG, 900-query retrieval benchmark); local copies in `paper/done papers/`; root `LITERATURE_REVIEW.md` covers RAG/trust/ethics only |

---

## The 9 Research Clusters and All Their Angles

### CLUSTER 1 — Agentic RAG + Verifier Systems (system-track core)
- 1.1 Multi-agent / agentic RAG pipelines: orchestration, tool-use, agent trace UX (2025–2026)
- 1.2 Verifier / grounding agents: claim-level verification, faithfulness checks, dosage/critical-info interception (2025–2026)
- 1.3 Adaptive retrieval, knowledge boundary, confidence-gated retrieval (2025–2026)
- 1.4 How prior **system demo / application papers** at ACL/EMNLP/NAACL presented agentic RAG systems (structure, evaluation, figures)

### CLUSTER 2 — LLM Safety & Guardrails for Low-Resource Languages
- 2.1 Multilingual safety classifiers / guardrail models (Llama Guard 3/4, ShieldGemma 2, Aegis…) — coverage and gaps for Bengali (2025–2026)
- 2.2 Multilingual safety benchmarks (2025–2026): which include Bengali? Which don't? (gap evidence)
- 2.3 Epistemic safety: "I don't know" refusal behavior, uncertainty communication, calibration (2025–2026)
- 2.4 Prompt injection defense in RAG/agent pipelines (2025–2026)
- 2.5 Domain-specific safety: agrochemical misuse, self-harm/poisoning framing, helpline redirection patterns (2025–2026)

### CLUSTER 3 — Low-Resource NLP, Bengali & Dialects
- 3.1 Bengali LLM landscape 2025–2026: BanglaLLM, MuRIL successors, mT5-class, Bangla instruction tuning
- 3.2 Dialect handling: dialectal datasets, normalization (BUNO), code-mixing (Banglish), 6-dialect coverage vs literature
- 3.3 Synthetic data generation for low-resource languages (LLM-generated datasets, quality control, human-in-loop validation) 2025–2026
- 3.4 Bengali evaluation benchmarks: BanglaNLG, BanglabERT leaderboards, LLM eval for Bengali (2025–2026)

### CLUSTER 4 — Agricultural AI Advisory Systems (closest-domain systems)
- 4.1 GenAI agricultural extension systems 2025–2026: Farmer.Chat successors, WAVS, AgriLLM, KisanGPT, etc.
- 4.2 Multimodal farmer-facing advisory (voice, image, WhatsApp); low-literacy UX research
- 4.3 Agricultural LLM benchmarks & evaluations (AgriEval, agronomy QA, crop-advisory evaluation) 2025–2026
- 4.4 Agricultural knowledge grounding: RAG over extension documents, knowledge nodes, provenance
- 4.5 Field deployment / impact studies in Global South agriculture (2025–2026), trust, adoption, gender

### CLUSTER 5 — Vision: Crop Disease Classification + Integration Conventions
- 5.1 Plant/crop disease classification SOTA 2025–2026: lightweight CNNs, transformer-free, YOLO-classify, mobile deployment
- 5.2 Confidence calibration, OOD rejection, thresholding, honest-failure states in medical/plant diagnosis systems
- 5.3 Multimodal vision+text disease advisory: image diagnosis → grounded text treatment (2025–2026)
- 5.4 Agri vision benchmarks & foundation models (PlantCLEF, CropNet, remote-sensing agri-models) 2025–2026

### CLUSTER 6 — System/Application/Industry-Track Publication Conventions (META-ANGLE)
- 6.1 ACL System Demonstrations 2025–2026: acceptance criteria, paper structure, demo requirements
- 6.2 EMNLP Industry Track / AAAI Demo / IJCAI demo conventions and what reviewers want
- 6.3 KDD Applied Data Science Track & CIKM Applied Research: evaluation standards for deployed systems
- 6.4 NeurIPS Datasets & Benchmarks track: dataset paper requirements, licensing, reproducibility
- 6.5 Applied-paper evaluation expectations: human evals, user studies, ablations, error analysis, cost/latency reporting
- 6.6 The novelty debate 2025–2026: how applied/system papers defend novelty vs incremental-LLM-wrapping critiques; what "systems contributions" are accepted

### CLUSTER 7 — Retrieval for Low-Resource Languages
- 7.1 Hybrid retrieval advances 2025–2026: late interaction, ColBERTv2, reranking for LRLs
- 7.2 Bangla information retrieval / dense retrieval benchmarks (2025–2026): Mr. TyDi, MIRACL, Bangla subsets
- 7.3 Query rewriting / expansion / dialect-to-canonical normalization for retrieval
- 7.4 RAG evaluation frameworks 2025–2026 (RAGAS 2.x, ARES, RAGChecker 2.0, faithfulness metrics)

### CLUSTER 8 — Edge/Compact LLMs + Streaming Systems
- 8.1 4B-class SLMs 2025–2026: Gemma 3/4, Qwen 3-4B, Phi-4 — capability vs 70B+ on structured/grounded tasks
- 8.2 Quantization (GGUF, QAT), Ollama-class local serving, on-device constraints (capstone = single laptop demo)
- 8.3 Streaming UX conventions (SSE, token streaming, stage-event traces) in system papers
- 8.4 Latency-aware design: caching, small-model routing, parallel calls (p95 budgets; demo = 3-4 min)

### CLUSTER 9 — ICT4D / Global-South Application Conventions
- 9.1 Chatbots for development (ICT4D, COMPASS) 2025–2026: what gets published, what evaluations are expected
- 9.2 Voice-first / low-literacy interfaces; readability measurement for Bangla
- 9.3 Digital public infrastructure: helpline integration (16123-equivalents), extension-officer intermediaries
- 9.4 Field evaluation methodology: RCTs, adoption studies, trust measurement instruments (2025–2026)

---

## Cross-cutting requirements for every cluster

1. **Recency:** papers from **2025 → August 2026** are mandatory focus; older only as background.
2. **Citations:** real arXiv IDs / DOIs / official pages — no invented references.
3. **Conventions:** each scout notes the *implementation/evaluation conventions* of similar accepted system/application/industry papers (what sections, what evals, what artifacts they released).
4. **Gaps:** explicit "no one has done X" statements with evidence.
5. **KrishokTech mapping:** how each finding maps to our components (pipeline, dataset, vision, UX).

## Output file map (paper/literature review/)

| File | Source |
|---|---|
| 00_SCOPE_AND_ANGLES.md | This file (master list) |
| 01_agentic_rag_verifier_systems.md | Scout 1 |
| 02_llm_safety_low_resource.md | Scout 2 |
| 03_low_resource_nlp_bengali.md | Scout 3 |
| 04_agri_ai_advisory_systems.md | Scout 4 |
| 05_vision_crop_disease.md | Scout 5 |
| 06_system_industry_track_conventions.md | Scout 6 |
| 07_retrieval_low_resource_rag_eval.md | Scout 7 |
| 08_edge_slm_streaming_systems.md | Scout 8 |
| 09_ict4d_global_south.md | Scout 9 |
| 10_SYNTHESIS_GAPS_POSITIONING.md | Synthesis (final) |