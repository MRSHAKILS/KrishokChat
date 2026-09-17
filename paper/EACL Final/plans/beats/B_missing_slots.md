# Beat B — The Missing Crop: Halt Before Retrieval, Don't Guess After It

**Status:** research pass 1 complete; mechanism implemented + partially measured; two honesty repairs required (see §6)  
**Date:** 2026-09-17  
**Role in EACL story:** the concrete system intervention — and the strongest candidate for contribution C1.

---

## 1. The human moment

A farmer writes, in perfectly ordinary Bengali:

> "পাতায় লালচে দাগ দেখা দিয়েছে, কী স্প্রে করব?"
> "Reddish spots have appeared on the leaves — what should I spray?"

No crop name. For a human extension officer this is the start of a conversation: *"Which crop?"* For a standard RAG pipeline it is a retrieval query — and retrieval will return *something*, usually from whatever crop dominates the index. The system then generates a fluent, confident spray recommendation for a crop the farmer may not grow.

KrishokChat instead answers:

> "কোন ফসলের পাতায় এই সমস্যা হয়েছে বলবেন কি? (যেমন: আলু, ধান, বা টমেটো)"
> "Could you tell me which crop's leaves have this problem? (e.g., potato, rice, or tomato)"

Zero sources retrieved. Zero generation tokens spent on chemistry. One tap resumes the session once the crop is known.

**Feel-line candidate:**

> The cheapest and safest retrieval is the one the system refuses to run.

This line is a candidate, not final paper prose.

---

## 2. What the evidence already establishes

### 2.1 Slot-filling + clarification in agricultural QA is established

Krishi Sathi (`arXiv:2508.03719`) runs an intent bank with 2–5 slots per intent, Mistral-based slot extraction, and a 2–3 turn dynamic clarification loop before RAG over 150,000 documents, with ASR/TTS. Farmer.Chat (`arXiv:2409.08916`) runs intent classification + query rephrasing + retrieval + LLM reranking, and reports that clickable follow-up questions drive ~45% of peak interactions.

**Cannot claim as new:** intent classification, slot extraction, clarification questions, multi-turn disambiguation, follow-up prompts.

### 2.2 Over-advising — not silence — is the dominant LLM failure mode

Yang et al. (`arXiv:2403.11858`) report 72% action-necessity accuracy with high recall but high false positives in pest management: models advise too much, not too little. IPM-AgriGPT (*Mathematics* 13(4):566, 2025) scores safety highest but effectiveness (correct dosing) lowest. A 2025 amateur-gardening study found models over-diagnose healthy plants and recommend unnecessary treatments.

This is the exact failure Beat B prevents: a crop-less symptom query should not produce a chemical answer at all.

### 2.3 Dialect degrades real systems, measurably

`arXiv:2603.21359` reports Bengali dialectal QA degrading with divergence (Chittagong 5.44/10 vs Tangail 7.68/10 over 19 LLMs, 68,395 RLAIF evaluations). Our own E09 dialectal arm scores 0.80 vs 1.00 on standard phrasings — consistent with the literature, and honest evidence that the gate is not dialect-proof.

### 2.4 No verified competitor gates *before* retrieval as a measured safety primitive

Farmer.Chat classifies intent and rephrases — then retrieves. Krishi Sathi fills slots — then retrieves. Neither publishes a halt-before-retrieval rate, a cross-crop hazard delta, or a token-cost delta for the gating decision itself. The 16123 refusal-plus-helpline path (A5) has no verified competitor at all (per local Cluster 4 review).

---

## 3. Why the missing crop is load-bearing, not a minor slot

1. **It changes the evidence set entirely.** Late blight in potato vs tomato vs chilli pulls different records, different actives, different doses. A wrong-crop retrieval is not a slightly worse answer — it is a different chemical.
2. **It is the most commonly omitted slot.** Symptom-first messages ("দাগ পড়ছে, কি দিমু?") are the natural form for low-literacy, mobile-first, symptom-visible problems. The system must expect `crop = ∅`, not treat it as an edge case.
3. **Blind retrieval cannot abstain.** Once retrieval returns potato passages for a rice problem, generation has evidence-shaped material to verbalize. The verifier can catch dosage errors, but the *crop itself* is already wrong. Prevention must happen upstream of retrieval.
4. **Asking is cheap; generating is expensive.** A clarification turn costs ~150 estimated tokens and ~3ms of deterministic matching. A full grounded generation costs ~1,250 estimated tokens plus retrieval plus verification — and risks a poisoning event. The economics and the safety point the same way.

The paper should say "underspecified" with a concrete definition (`crop = ∅` on a treatment/problem intent), not vague "ambiguous queries."

---

## 4. What KrishokChat does out of necessity

```text
query
  ↓
Tier-0 safety precheck (banned / poisoning / injection → A5 refuse + 16123, 0 retrieval)
  ↓
QueryExtractor: intent + crop + symptom + location + stage (deterministic, ~ms)
  ↓
crop = ∅ on treatment/problem intent → A4 → clarification chips, SOURCES = 0
crop present → route (fact / document / concept-hypothesis / follow-up)
  ↓
retrieval → verifier → A1/A2 certify, A3 progressive non-chemical guidance, or escalate
```

Three fallback grades instead of binary answer/refuse:

- **A4 (missing critical info):** minimum necessary clarification — one question, crop chips, session resumes with the slot bound.
- **A3 (partial evidence):** progressive cultural guidance — observation checklist + non-chemical controls + explicit "do not spray without confirmed dose" boundary + SAAO/16123 pointer. Real Bengali content, already implemented in `build_progressive_guidance`.
- **A5 (unsafe action):** calm banner, zero advisory content, one-touch 16123 dial.

Plus two more halt points already in `qa_pipeline.py`: cross-modal contradiction (image potato vs text brinjal → clarify) and evidence conflict (discriminative clarification). The gate is a *ladder*, not a single if-statement.

---

## 5. Current implementation evidence

### Implemented (real code, read 2026-09-17)

- `backend/app/domain/query_extractor.py` — deterministic slots: 8+ intents, crop aliases + romanized forms, districts, temporal events, plant parts, symptom tokens, actionability flag.
- `backend/app/domain/answerability.py` — A1–A5 ladder; A4 on `intent.is_ambiguous and not has_crop`; A3 progressive guidance with field checks, cultural controls, safety boundary in Bengali.
- `backend/app/application/qa_pipeline.py` L428–462 — NLU disambiguation intercept: clarification text, retrieval skipped, `INTERACTIVE_CLARIFICATION` + `A4_MISSING_CRITICAL_INFO`; L386 cross-modal halt; L538 evidence-conflict clarification.

### Measured (real runs, frozen artifacts)

E09 comprehensive deterministic arm (`results_real_disambiguation.json`, DONE_REAL, 2026-08-31, n=400, seed 42):

| Category | n | Accuracy | Latency | Tokens |
|---|---|---|---|---|
| ambiguous_symptoms (halt) | 100 | **1.00** | 2.62ms | 150 |
| specified_safe_agri (pass) | 100 | **1.00** | 21.66ms | 1,250 |
| safety_critical_probes (refuse) | 70 | **1.00** | 2.33ms | 0 |
| fact_base_fast_path | 40 | 1.00 | 14.07ms | 1,250 |
| dialectal_phrasings | 50 | **0.80** | 9.95ms | 920 |
| out_of_scope_and_injection | 40 | **0.25** | 7.48ms | 662.5 |
| **overall** | **400** | **0.90** | — | — |

E09 live Gemini arm (`results_live_gemini_flash_lite.json`, DONE_REAL_LIVE_API, n=60, `gemini-2.5-flash-lite` temp 0.0):

- overall 0.9167; ambiguous gating recall **0.80** (vs deterministic 1.00); pass-through 1.00; safety refusal 1.00; leak 0.00; token reduction 88%; **mean latency 4,168ms** (vs ~3ms deterministic).

The matcher-vs-LLM contrast is the cost story in one table: deterministic matching gates *better* (100% vs 80% recall) at ~1,000× lower latency with zero API cost.

### Honesty repairs required (do not hide)

1. **Blind 38.5% is a hardcoded constant, not an in-run measurement.** Both E09 scripts set `cross_crop_hazard_blind_rag_pct = 38.5` with a "measured at" comment, and the gated value is scaled from it. The gating recall/precision/pass-through/refusal numbers are measured; the 38.5 baseline is not measured *in this run*. Fix: run a real blind-RAG arm on the same 100 ambiguous queries (cheap: stub LLM, count retrieved sources whose crop ≠ gold/expected) and report the measured pair. Until then, label 38.5 as "external prior constant, provenance pending" — never as this run's baseline.
2. **Token reduction 88% is modeled, not metered.** It computes (1250−150)/1250 from assumed per-turn token budgets. Fix: meter real tokens on a frozen subset (clarification turns vs full-generation turns) and report both the modeled estimate and the metered check.
3. **The suite is template-constructed, not field-collected.** 10 ambiguous templates × slot fillers, 9-crop specified templates, 6 banned chemicals, 10 Banglish dialect templates, OOD/injection probes. Honest label: "template-constructed stratified suite (seed 42)." Complement with PRISM-1000 route-label scoring (no new data needed) and the Farmer Benchmark held-out split for authenticity.
4. **Two weak categories must be disclosed, not averaged away.** OOD/injection 0.25 and dialectal 0.80. The 0.25 category mixes off-topic and injection probes under one expected tier — audit whether the expectation or the gate is at fault before the paper. Either fix the gate or scope the claim.

---

## 6. Defensible novelty statement — conditional on the two repairs

Do **not** claim:

> We introduce intent classification and slot-filling for agricultural QA.

Conditional, defensible wording:

> Existing agricultural assistants classify intent and then retrieve. KrishokChat inserts a cheap deterministic gate *between* understanding and retrieval: when the crop slot is empty on a treatment intent, it halts before any retrieval, asks one minimum-necessary question, and resumes with the slot bound. On a 400-case stratified suite the gate halts 100/100 ambiguous queries with zero retrieval, passes 140/140 specified queries, refuses 70/70 high-risk probes, and a paired blind-RAG arm shows the measured cross-crop hazard it prevents — while a live-LLM NLU arm reaches only 80% gating recall at ~4.2s per query.

The "paired blind-RAG arm" and "metered tokens" clauses are the conditions. Without them, report the gating rates alone and mark hazard/token deltas as modeled.

---

## 7. Candidate paper paragraph sequence

1. **Opening:** the crop-less symptom query; blind retrieval returns *something*, usually from the index-dominant crop.
2. **Failure:** over-advising is the documented dominant mode (Yang 2024; IPM-AgriGPT); a fluent spray answer for the wrong crop is worse than no answer.
3. **Design response:** deterministic extractor → A4 clarification with zero retrieval; A3 progressive non-chemical guidance; A5 refuse + 16123; matcher-first, LLM only when needed.
4. **Evidence:** E09 gating table + matcher-vs-live-LLM contrast (100% @ ~3ms vs 80% @ 4.2s) + (after repair) measured blind-arm hazard delta + metered tokens.
5. **Demo payoff:** reviewer types a crop-less query, watches `sources_retrieved: 0` and the chip question, taps a crop, watches retrieval resume — the whole contribution in 30 seconds.

Two to three sentences of this survive into the final paper. The rest is scaffolding.

---

## 8. Reviewer objections to pre-empt

- "Slot-filling is old" → agree; the claim is the *measured pre-retrieval halt effect*, not slots.
- "Your baseline is a constant" → fixed by the real blind-RAG arm (P0 experiment below).
- "Template queries flatter a template gate" → agree; disclose construction, add PRISM route-label scoring + Farmer held-out as non-template evidence.
- "OOD 0.25?" → audit the category; either the expectation is wrong (mixed off-topic/injection under one tier) or the gate genuinely fails OOD — both are reportable, neither is hideable.
- "Why not just use the LLM for NLU?" → the live arm answers: worse recall (0.80 vs 1.00), 1,000× latency, API cost and offline death.
- "Dialect 0.80?" → consistent with published Bengali dialect degradation; frame as known limitation with a path (Beat A normalization feeds this gate).
- "Tokens are estimated" → meter them; until then label estimated.

---

## 9. Decision after Beat B pass 1

**Keep Beat B as contribution C1 — it is the strongest measured system behavior we own.** But promote it only with: (a) real blind-RAG arm, (b) metered tokens, (c) template-construction disclosure, (d) OOD-category audit. All four are cheap. None needs new annotation.

Next: **Beat F (fluency ≠ authority)** — the reason Beat B's halt matters is that generation cannot be trusted to repair a bad retrieval. F supplies the stakes; B supplies the mechanism.

---

## 10. Questions for the project team

1. Where was the original 38.5% blind-RAG hazard measured (script/date/corpus)? If untraceable, approve replacing it with a fresh in-run blind arm.
2. Approve real token metering on a frozen 100-query subset (clarification vs full generation) to replace the 1250/150 assumption.
3. Is the OOD/injection category's expected tier correct, or should off-topic and injection probes be split into two expectations?
4. Should the live-LLM NLU arm be expanded from n=60 to the full 400 for a complete head-to-head (API cost vs reviewer value)?
