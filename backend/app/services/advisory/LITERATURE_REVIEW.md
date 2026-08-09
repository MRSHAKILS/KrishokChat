# Literature Review — Advisory Workflow Architecture

## Purpose
Produce a publishable-quality, safety-aware, Bengali agricultural advisory assistant that
grounds answers in a curated knowledge base, defers to human authority on gaps, and
exposes an inspectable agentic pipeline.

## Summary of Findings

| Pillar | What the literature shows | Design choice for this project |
|---|---|---|
| RAG-vs-LLM decision | Self-RAG, CRAG, Adaptive RAG, ConfRAG (2024) show a confidence-triggered switch between retrieval-only, LLM-only, and abstain reduces latency and hallucination. Fin-domain engines use 4-way gates. | Implement a calibrated 4-way gate: FULLY / PARTIALLY / GENERAL_GUIDANCE / REFER_EXPERT, chosen from normalized BM25 score, crop/disease match, and treatment-field presence. |
| Grounded generation | Perplexity, Bing Copilot, Attribute-First-Then-Generate tie every claim to a retrievable source; citation is a forcing function. | Retrieved KB snippets + disease_details go into the prompt; sources returned with every answer. |
| Agricultural advisors | Farmer.Chat (830k users, 5M queries), PlantVillage Nuru, ICRISAT iSAT, GAIA, Kisan Call Centre AI confirm farmers accept AI that defers to a human helpline when confidence is low. | Always surface 16123 (Bangladesh Krishi Call Center) when treatment is missing or the gate is REFER/GENERAL. |
| Ethics / calibration | NeurIPS 2024 uncertainty work, Calibration Gates, Medicolegal accountability papers: overconfident wrong advice in critical domains is the dominant harm; explicit refusal + escalation is mandatory. | Chemical-dosage hallucination is prohibited by construction (KB-only); audit log every decision. |
| Trust | Styvers calibration gap, Agronomy Journal trust surveys, 60 Decibels Farmer.Chat study: users overestimate LLM accuracy by 30-40%; transparency (gate mode, sources) builds trust; voice output is under-studied but promising. | Show gate mode, agent trace, sources; plan voice later. |
| Engineering | RAG fusion adds latency with little gain; query rewriting is highest-ROI; faithfulness target >90% (RAGAS). | BM25 + query rewriting (Bengali→English augmentation); no fusion for v1. |

## Recommended Architecture (implemented)

```
User query + (optional crop/disease context from detection)
        │
        ▼
Safety / Router Agent  ── regex precheck ── Gemini JSON classify
        │  (self-harm / banned / injection → block + 16123/999, stop)
        ▼
Filtered Retrieval     ── BM25 over knowledge_nodes_clean.jsonl
        │  (augmented with crop/disease English terms; score filter)
        ▼
Confidence Gate        ── compute_confidence_gate() → mode + instructions
        │  FULLY / PARTIALLY / GENERAL / REFER
        ▼
Grounded Generation    ── gemini-3.1-flash-lite (free keys) or 2.5-flash-lite
        │  prompt = gate-mode instructions + KB snippets + disease_details
        ▼
Verifier + Audit       ── dosage token flags, append to logs/safety_audit.jsonl
        ▼
Stream to UI (SSE)     ── stage events (safety→retrieval→generation→verifier) + final
```

## Calibration Rules (final)
- Top BM25 > 15 AND crop match AND (disease match OR no disease) AND treatment field → FULLY_GROUNDED
- Top > 15 but no treatment field (and treatment intent) → PARTIALLY_GROUNDED
- Top > 8 AND (crop OR disease match) → FULLY (safe query) or PARTIALLY (critical)
- Top > 3 → GENERAL_GUIDANCE (safe) or PARTIALLY (critical)
- Top ≤ 3 → GENERAL_GUIDANCE (safe) or REFER_EXPERT (critical)
- Empty KB + treatment intent → REFER_EXPERT always.

## References (selected)
- Self-RAG (Asai et al., 2024), CRAG (Shi et al., 2024), Adaptive RAG (Jiang et al.)
- ConfRAG (Wang et al., 2024), RAGAS (Es et al., 2024), Faithfulness >90% target
- Farmer.Chat — 60 Decibels impact study; PlantVillage Nuru; ICRISAT iSAT
- NeurIPS 2024 uncertainty quantification; Calibration Gates (Steyvers)
- Medicolegal accountability for AI in agriculture
- Perplexity / Bing Copilot attribution models
- EU AI Act — critical-domain transparency requirements
