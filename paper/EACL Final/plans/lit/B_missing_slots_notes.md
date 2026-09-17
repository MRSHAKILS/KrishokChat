# Beat B Literature Notes — Slots, Clarification, Selective Answering, Cost-Gated NLU

**Research pass:** 1  
**Cutoff:** 2026-09-17  
**Purpose:** evidence ledger for the Beat B story. This is not paper prose.

## A. Closest prior systems (agricultural)

| Work | What it establishes | Boundary for our claim |
|---|---|---|
| Krishi Sathi, `arXiv:2508.03719` | Intent bank + 2–5 slots/intent, Mistral slot extraction, 2–3 turn clarification before RAG over 150k docs, IFT Param model, EN+HI ASR/TTS, 2 crops (onion, grape) | Slot-filling + clarification in agri QA is prior art. Distinguish by: pre-retrieval halt with measured hazard/cost effect; deterministic-vs-LLM NLU comparison; Bengali; 9-crop coverage; graded A1–A5 fallback |
| Farmer.Chat, `arXiv:2409.08916` | Intent classification + query rephrasing + retrieval + LLM rerank + generation; follow-ups drive ~45% peak interactions; 15k users / 300k queries | Intent-then-retrieve is established. No published halt-before-retrieval rate, hazard delta, or token delta for the gate itself |
| KrishokBondhu, `arXiv:2510.18355` | Bengali voice RAG, fuzzy matching + ambiguity prompts + dialogue tracking, Gemma 3-4B, 72.7% high-quality | Ambiguity prompts exist but are unevaluated as a safety mechanism; no gating metrics |
| Hossain et al., `arXiv:2601.02065` | bn→en translation retrieval, keyword injection, OOD rejection, <20s latency | OOD rejection exists as a feature; no slot-gating measurement |
| Digital Green DG-Eval, `arXiv:2603.03294` | Atomic fact verification + contradiction detection vs Golden Facts; LoRA recall 26.2→50.3% | Downstream verification precedent; our gate is *upstream* of retrieval — complementary, cite as the second half of defense-in-depth |
| Farmer.Chat RLHF, DOI 10.37433/aad.v7i2.625 | 25k expert-reviewed Q&A, Golden pairs, per-crop gains | Preference alignment improves answers; does not replace a missing-slot gate |

## B. Failure-mode literature (why halting matters)

| Work | Finding to cite |
|---|---|
| Yang et al., `arXiv:2403.11858` | Pest-management LLM judge: 72% action-necessity accuracy, high recall + high false positives — **over-advising is the dominant mode** |
| IPM-AgriGPT, *Mathematics* 13(4):566 (2025) | Safety scores highest, effectiveness (correct dosing) lowest — models sound safe while dosing wrong |
| Silva et al., `arXiv:2310.06225` | GPT-4 93% CCA, 97% with RAG — the RAG-without-verification ceiling later work attacks |
| MDPI *Sustainability* 17(23):10466 (2025) | Models over-diagnose healthy plants, recommend unnecessary treatments |
| `arXiv:2603.21359` | Bengali dialectal QA degrades with divergence (Chittagong 5.44 vs Tangail 7.68) — external support for our 0.80 dialectal arm |

## C. Follow-up literature to dig (not yet read — marked for next pass)

1. **Selective prediction / learning-to-defer / abstention** — the general-ML framing of "don't answer when uncertain." Needed so the paper can say "selective answering under domain shift" instead of inventing terminology. Candidates: selective classification with coverage guarantees; learning-to-defer with experts; *not yet verified — do not cite until read*.
2. **Task-oriented dialogue clarification policy** — when to ask vs answer (information-gain / minimum-necessary-question policies). Needed to frame MNC properly. *Not yet verified.*
3. **Cascade inference / FrugalGPT-style routing** — cheap-first model cascades with cost/quality trade-offs. Needed for the matcher-vs-LLM cost argument. *Not yet verified.*
4. **Cross-encoder vs zero-shot LLM reranking for RAG** (EACL Industry 2026: zero-shot LLMs beat cross-encoders) — relevant if we add a rerank arm later. *Noted only.*

## D. Conclusions

1. Slots + clarification are established; **halt-before-retrieval with measured hazard + cost consequence is not**.
2. Over-advising dominates agri-LLM failures — prevention upstream of retrieval is the right layer.
3. The matcher-vs-LLM head-to-head (deterministic 1.00 @ ~3ms vs LLM 0.80 @ ~4.2s) is, to our current knowledge, an unreported comparison in agricultural QA — verify in the next pass before claiming.
4. A5 (refuse + 16123 with zero retrieval) has no verified competitor — keep as part of the ladder story.

## E. Citation-use rules

- Cite Krishi Sathi for the slot-filling precedent *and* its limits (EN/HI, 2 crops, no hazard measurement).
- Cite Farmer.Chat follow-ups as interaction precedent, not as a gate.
- Cite Yang 2024 + IPM-AgriGPT for the over-advising failure mode.
- Do not cite selective-prediction or cascade papers until actually read.
- Label E09 as "template-constructed stratified suite" wherever its numbers appear.
