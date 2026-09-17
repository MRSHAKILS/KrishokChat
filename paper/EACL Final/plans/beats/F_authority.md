# Beat F — Fluency Is Not Authority: Verify, Then Speak (or Don't)

**Status:** research pass 1 complete; guards measured on both ends; verifier catch-rate study pending  
**Date:** 2026-09-17  
**Role in EACL story:** the stakes — why Beat B's halt and the whole pipeline exist. Generation can sound right while being chemically wrong, even with perfect evidence in front of it.

---

## 1. The human moment

The farmer did everything right. They named the crop, described the symptom, even waited through retrieval. The system found the correct BARI passage. Then the language model wrote the answer — and quietly changed "2–2.5 g per litre" into "2–5 g per litre," or kept the right chemical but attached the dose from a different row of the table.

Nothing looks wrong. The Bengali is fluent, the chemical name is correct, the tone is reassuring. The poison is in the number.

**Feel-line candidate:**

> The most dangerous answer is not the one that looks wrong — it is the fluent one with a single mutated number.

This line is a candidate, not final paper prose.

---

## 2. What the evidence already establishes

### 2.1 Even oracle evidence leaves a hallucination floor

Our own benchmark (`arXiv:2606.29243`) reports that a **4.05–7.00% chemical hallucination floor persists even under oracle evidence**, Treatment QA correctness peaks below 44% for every zero-shot baseline, and supervised fine-tuning that lifts QA scores **collapses safety compliance to 0.31%**. Two lessons the demo paper inherits for free:

1. Retrieval alone does not make chemical advice safe — the generator mutates what retrieval found.
2. Making the model *smarter* (SFT) can make it *less safe* (less refusal). Safety must be architecture, not weights.

### 2.2 An unconstrained frontier model fails most Bengali attacks

E03 (`results.json`, DONE, 420 real OpenRouter calls, 7 families × 30 × 2 arms):

| Family | Unconstrained (gpt-4o-mini) | Gated system (gemini-2.5-flash-lite) |
|---|---|---|
| overall | **36.19%** [29.99, 42.88] | **0.95%** [0.26, 3.41] |
| Bangla native injection | **76.67%** | **6.67%** [1.85, 21.32] |
| Banglish romanized | 60.00% | 0.00% |
| banned-chemical request | 60.00% | 0.00% |
| retrieval poisoning | 30.00% | 0.00% |
| delimiter hijacking | 23.33% | 0.00% |

Three out of four Bengali injections succeed against the raw model. The gate stops nearly all of them — except Bangla native, which leaks at 6.67% and must be reported honestly as the residual risk, not rounded away.

### 2.3 Post-generation checks are established; authority separation is not

Claim-level verification (RAGChecker, RAGAS v2), citation evaluation (CiteEval), faithfulness judges (ARES), agricultural contradiction detection (DG-Eval) — all established. What they share: they *score* an answer after the fact. None of them decides, before rendering, which sentences the farmer is allowed to see — and none separates *who authored the facts* from *who wrote the sentences*.

---

## 3. Why generation-stage failure is the crux in Bengali chemical advice

1. **Numbers mutate silently across scripts.** Bengali digits (২.৫), Bengali words (আধা লিটার), and English units (ml/EC/WP) coexist in one answer. A paraphrase that preserves meaning in English can halve a dose in Bengali.
2. **Tables invite cross-row binding.** Handbook tables list one chemical per row with its own dose, interval, PHI. A generator that "synthesizes across sources" can attach row 3's dose to row 1's chemical — each fragment grounded, the combination lethal.
3. **Fluency suppresses doubt.** A refusal looks uncertain; a fluent answer looks authoritative. Low-literacy users cannot audit chemistry from prose style. The system must therefore audit *before* rendering, and show its work after.
4. **SFT makes it worse.** Per 2606, fine-tuning reduces refusal. Every "helpfulness" gain must be re-checked against the safety gate — the demo paper should say this once, plainly.

---

## 4. What KrishokChat does out of necessity

Two walls with a corridor between them:

```text
UPSTREAM WALL (before retrieval/generation)
  Tier-0 precheck + safety classifier → terminal refuse + 16123, 0 LLM calls
  E03: 0.95% ASR vs 36.19% unconstrained; Bangla native 6.67% residual

CORRIDOR (generation, untrusted by design)
  LLM writes Bengali — treated as a mouthpiece, never as a witness

DOWNSTREAM WALL (after generation, before rendering)
  HardenedDosageVerifier: sentence → atomic (chemical, amount, unit) claims
    → each claim must be entailed by ONE retrieved passage
       (amount+unit AND chemical co-occurring in the same passage)
    → dose-band outlier check vs registered reference, even for grounded claims
    → annotate-and-drop: unsupported sentences removed, flags + per-claim
       verdicts surfaced, nothing silently rewritten
  Confidence: verified / flagged-unverified / low_confidence / blocked
  p50 ~4.82ms — verification is ~1,000× cheaper than the generation it checks
```

And the farmer sees *who authored what*: tier badges in Bengali — T0 "নিরাপত্তা নিয়ম (এআই ব্যবহার হয়নি)" (safety rule, no AI used), T1/T2 "অনুমোদিত তথ্যসারণি (এআই ব্যবহার হয়নি)" (approved table, no AI used), T3 "সূত্রভিত্তিক এআই উত্তর" (source-based AI answer). The badge is a trust device: no-AI answers outrank AI answers visibly.

The intended point is not "we verify." It is:

> **The LLM is the mouthpiece; the evidence is the witness; the verifier is the judge — and the farmer sees all three.**

---

## 5. Current implementation evidence

### Implemented (real code, read 2026-09-17)

- `backend/app/application/verifier.py` — `HardenedDosageVerifier.verify(answer, sources)`: claim extraction → per-claim same-passage entailment → dose-reference outlier check → annotate-and-drop with `sanitized_answer` + flags + `VerificationResult` (checked/grounded/unsupported counts).
- `backend/app/infrastructure/verification/dosage_claims.py` — Bengali digit normalization, canonical unit table (মিলি→ml, গ্রাম→g, লিটার→l…), fraction handling (আধা→0.5), Bengali + English chemical lexicons, same-passage binding rule.
- `backend/app/infrastructure/verification/dose_reference.py` — registered-rate band outlier detection (F1-02).
- `backend/app/domain/resolution.py` — T0–T4 ladder + `ZERO_LLM_TIERS` + Bengali authorship badges (`TIER_LABELS_BN`).
- Research-track alternatives (`claim_parser.py`, `structured.py`, `relation_matcher.py`) are frozen until T22 — honest boundary between product path and research path.

### Measured (real runs)

- E03 upstream wall: 420 live calls, both arms, CIs recorded (see §2.2 table). Residual Bangla-native leak 6.67% disclosed.
- Verifier latency: p50 ~4.82ms, p95 ~11.2ms on the E01 400-query sweep (BM25-only, stub LLM).
- 2606 oracle floor (4.05–7.00%) + SFT-refusal collapse (0.31%): published companion evidence, reusable as motivation.

### Scoping limit (must be stated in the paper)

The product verifier checks **dosage claims** (chemical + amount + unit, same-passage binding, dose-band outliers). It is not the full CEA 11-slot single-record authority check (crop/pathogen/stage/formulation/interval/PHI/regulatory binding) — that lives in the CEA track. The demo paper must say "dosage-claim verifier," never imply full 11-slot certification in the live path.

### Not yet measured (experiment plan below)

- Verifier catch-rate on real generated answers with injected dosage mutations (precision/recall of grounded vs unsupported verdicts).
- Annotate-and-drop rendering in the UI: confirm the "Why this advice?" panel actually surfaces flags + per-claim verdicts + sanitized text (check `provenance-badge.tsx`, `qa-panel.tsx` wiring).
- End-to-end unsafe-acceptance rate through the full pipeline (gate + generation + verifier) on Treatment QA items.
- False-positive cost: how often valid advice gets flagged (farmer impact of over-conservatism).

---

## 6. Defensible novelty statement — conditional on the catch-rate study

Do **not** claim:

> We introduce verification for RAG. / We guarantee safe chemical advice.

Conditional, defensible wording:

> Post-hoc judges score answers; KrishokChat refuses to render them. A dosage-claim verifier binds every amount-unit-chemical triple to a single retrieved passage, drops unsupported sentences instead of rewriting them, and checks even grounded claims against a registered dose band — all in ~5ms, all visible to the farmer through authorship badges and per-claim flags. Upstream, a safety gate stops 208/210 live attacks that succeed 36% of the time against an unconstrained model; downstream, the verifier audits what the gate let through. The residual Bangla-native leak (6.67%) is reported, not hidden.

The "catch-rate" clause is the condition: without a measured verifier precision/recall on mutated answers, the downstream wall is implemented-but-unevaluated.

---

## 7. Candidate paper paragraph sequence

1. **Opening:** the fluent answer with one mutated number; nothing looks wrong.
2. **Failure:** oracle evidence still leaves 4–7% hallucinations (2606); SFT reduces refusal (0.31%); unconstrained model fails 76.67% of Bangla injections (E03).
3. **Design response:** untrusted generator between two measured walls; same-passage binding; annotate-and-drop; authorship badges.
4. **Evidence:** E03 two-arm table with CIs + verifier latency + (after study) catch-rate table.
5. **Demo payoff:** reviewer injects a dosage mutation, watches the sentence drop with its flag while the safe sentences stay — verification you can see.

---

## 8. Reviewer objections to pre-empt

- "Verification is old" → agree; the claim is same-passage binding + annotate-and-drop + dose-band check + visible authorship, measured as one wall.
- "n=30 per family is small" → agree; CIs are reported and wide ([0, 11.35] on zeros). The overall 210/arm comparison is the load-bearing statistic.
- "6.67% leak?" → disclosed as residual risk with CI; it is also the motivation for the downstream wall — the two walls justify each other.
- "Does the verifier actually catch anything?" → the catch-rate study (P0 below) answers exactly this.
- "Is the sanitized answer what the farmer sees?" → UI wiring check required; do not claim rendering until verified in code.
- "11 slots?" → no: product path verifies dosage claims; 11-slot authority is the CEA companion. Scope discipline is a feature of the story.

---

## 9. Decision after Beat F pass 1

**Keep Beat F as the stakes section, not a standalone contribution.** It motivates everything: Beat B halts because generation can't be trusted to repair retrieval; Beat D narrows scope because the verifier can only check what retrieval found. In the 6-page paper, F is ~4 sentences + the E03 table. The catch-rate study decides whether the downstream wall gets numbers or stays as implemented mechanism.

Next: **Beat D+E (vision scope + conflict)** — the only beat with a physical artifact reviewers can touch (photo → crop → disease → narrowed retrieval → contradiction badge).

---

## 10. Questions for the project team

1. Approve the verifier catch-rate study on ~200 Treatment QA answers with single-field mutations (dose ×2/÷2, PHI swap, chemical swap, unit swap)?
2. Can someone confirm the UI renders flags + sanitized text + tier badges (point to the components), or is that wiring still pending?
3. Should the 11-slot CEA verifier be cited as "companion research track" with one sentence, keeping the demo paper scoped to dosage claims?
4. Is expanding E03 beyond n=30/family worth the API cost, or do the current CIs suffice with honest reporting?
