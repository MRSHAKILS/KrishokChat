
## Session Anchored Summary (2026-08-09)

### Advisory Workflow — 5 Phases Complete

| Phase | What | Status |
|---|---|---|
| Phase 1 | Fix disease_knowledge_map nested structure | Category A=17, B=15, C=2 |
| Phase 2 | Generate 13 knowledge nodes via free Gemini keys | 13 nodes (Bengali+English) |
| Phase 3 | Merge nodes into RAG index, rebuild BM25 | 2133 nodes total |
| Phase 4 | Intent classifier (OpenRouter gemini-2.5-flash-lite) | 8 intents + safety |
| Phase 5 | Generator (free Gemini gemini-3.1-flash-lite) | Grounded Bengali responses |

### Key Files
- ackend/app/services/advisory/intent_classifier.py — OpenRouter classifier
- ackend/app/services/advisory/generator.py — Gemini free-key generator
- ackend/app/services/advisory/_extractors.py — shared utilities
- ackend/ml_assets/advisory/disease_knowledge_map.json — 34 diseases mapped
- ackend/ml_assets/advisory/generated_knowledge_nodes.jsonl — 13 generated nodes
- ackend/.env.local — OPENROUTOR_API_KEY + OPENROUTER_MODEL

### Resource Rules
- Free Gemini keys: ONLY gemini-3.1-flash-lite or gemini-3.5-flash-lite
- OpenRouter key: low-token tasks (intent classifier)
- Backend: localhost:8000 | Frontend: localhost:3000

### What's Left
- Phase 6: Frontend wiring (detection ? show info ? chat-more button)
- Frontend: tabs for disease detection + QA, agent trace animation
