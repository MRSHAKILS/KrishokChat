# Beat A — Bengali Farmer Language Is a Retrieval-Scope Problem

**Status:** research pass 1 complete; intervention evidence pending  
**Date:** 2026-09-17  
**Role in EACL story:** motivating failure mechanism for clarification, scope reduction, and safe routing — not a standalone “dialect retrieval” novelty claim yet.

---

## 1. The human moment

A farmer does not usually begin with the name of a disease from an official handbook. They may write only a symptom, use a regional expression, mix Banglish with Bengali, or omit the crop entirely:

> “পাতায় দাগ পড়ছে, কি দিমু?”  
> “There are spots on the leaves; what should I apply?”

For a farmer, this may be enough context to start a conversation. For retrieval, it is not enough to identify one authoritative treatment record. “দাগ” (spot) can correspond to different diseases, crops, and interventions. A fluent model can fill in the missing context, but that makes a guess look like evidence.

**Feel-line candidate:**

> The first failure is not that the system cannot answer Bengali; it is that the farmer’s short, ordinary description does not yet define a safe retrieval scope.

This line is a candidate, not final paper prose.

---

## 2. What the evidence already establishes

### 2.1 Register mismatch is a measured retrieval failure

The companion retrieval study, *Where Does Retrieval Fail?* (`arXiv:2608.14886`), evaluates Bengali agricultural retrieval over provenance-linked knowledge nodes. It reports a strong query-category gap:

- dense R@10: **0.093** on colloquial farmer queries;
- dense R@10: **0.970** on formal safety queries;
- BM25 R@10: **0.506** on Bengali queries;
- hybrid RRF R@10: **0.539** overall in that study.

The paper also reports that only **3.5%** of gold entity names appear verbatim in farmer queries and that farmer-query/document lexical overlap is very low. These numbers motivate the problem but do **not** prove that register alone causes the gap: farmer and safety subsets also differ in task, content, entity density, and wording.

### 2.2 Bengali agricultural transfer remains difficult after evidence access

The companion benchmark, *KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory* (`arXiv:2606.29243`), reports persistent farmer-language transfer difficulty and a chemical hallucination floor even under oracle evidence. The benchmark also distinguishes controlled dialect-expanded surfaces from a smaller authentic farmer benchmark.

This matters for the system story: retrieval repair cannot be judged only by whether a relevant passage appears. The system must preserve the information needed to identify a safe agricultural relation.

### 2.3 Existing work covers the components

The following are established and cannot be claimed as standalone novelty:

- BM25 plus dense or hybrid retrieval;
- dialect or romanization normalization;
- Unicode normalization;
- query expansion;
- intent and slot routing;
- asking for missing information;
- Bengali agricultural RAG;
- visible evidence or provenance.

Relevant sources include BUNO (`2024.lrec-main.1479`), BhasaBodh (`2025.banglalp-1.9`), Krishi Sathi (`arXiv:2508.03719`), the Bengali translation-centric agricultural RAG (`arXiv:2601.02065`), Farmer.Chat (`arXiv:2409.08916`), KrishokBondhu (`arXiv:2510.18355`), and My Climate CoPilot (`2025.acl-demo.7`).

The defensible system contribution must therefore be the **operational combination and measurement** of interpretation, retrieval scope, safety preservation, and visible fallback — not the existence of a normalizer or a hybrid index.

---

## 3. Why the failure is especially consequential in Bengali agricultural advice

This should be written precisely, not as a stereotype about Bengali farmers.

1. **Lexical mismatch:** official documents use formal disease, chemical, and agronomic terms; farmer queries often describe observable symptoms.
2. **Register and dialect variation:** the same intent may appear in regional Bangla, colloquial forms, spelling variants, or Banglish.
3. **Short and underspecified messages:** low-literacy or mobile-first interaction can produce brief symptom-only questions. The missing crop is not a minor slot; it changes which evidence is relevant.
4. **Safety-bearing ambiguity:** a plausible normalization can alter a crop, disease, chemical, dosage, unit, interval, pre-harvest interval, or harmful/benign polarity.
5. **Retrieval asymmetry:** an authoritative corpus may contain the correct fact, but a retriever can fail to place it in the candidate scope. Generation cannot safely repair an evidence omission.

The paper should say “queries may be short, colloquial, dialectal, or underspecified,” not imply that all Bengali farmers write in one way or that illiteracy alone explains the behavior.

---

## 4. What KrishokChat does out of necessity

Beat A connects several existing components into a causal sequence:

```text
farmer wording
    ↓
lightweight interpretation / slot check
    ├── required crop missing → clarify before retrieval
    ├── recognizable colloquial symptom → bounded concept hypotheses
    ├── crop supplied by text or image → restrict candidate scope
    └── uncertainty remains → retrieve conservatively or abstain
    ↓
retrieval trace: raw query → interpreted terms → route → candidate evidence
    ↓
verification and delivery decision
```

The intended point is not “we normalize Bengali.” It is:

> **the system treats language interpretation as a control point for retrieval scope, cost, and safety.**

This allows the EACL paper to connect:

- pre-intent/slot extraction to unnecessary retrieval and generation avoidance;
- concept normalization to candidate-evidence discovery;
- image conditioning to retrieval-space reduction;
- clarification to safe handling of unresolved scope;
- provenance and verifier output to the final trust boundary.

---

## 5. Current implementation evidence

### Implemented

- `backend/app/infrastructure/retrieval/expansion.py`: deterministic term-map expansion, longest-first matching, bounded additions and query length.
- `backend/app/domain/concept_normalizer.py`: colloquial symptom expressions mapped to canonical concepts and crop-conditioned hypotheses.
- `backend/app/application/adaptive_router.py`: fact-base, document-RAG, concept-hypothesis, and conversational follow-up routes.
- `backend/app/application/qa_pipeline.py`: retrieval trace and stage events.

### Important implementation limitations

1. `AdaptiveRoutingDecision` returns `expanded_queries`, but the live pipeline must be checked to confirm that every route actually submits those expansions to the retriever. A returned hypothesis is not evidence that the deployed path used it.
2. The current policy is deterministic and hand-written. It should not be called a learned or calibrated register router.
3. The shipped dialect map and term maps need an exact version/hash and expansion-output audit before any result is reported.
4. Unicode normalization is not equivalent to semantic dialect normalization. Do not call the current path BUNO-based unless the BUNO implementation is actually executed in the evaluated path.
5. Current E49 evaluation code uses gold metadata in some configurations and heuristic relevance checks. It is an internal diagnostic, not yet a defensible primary result.

### Measured and reusable as motivation

- `2608.14886`: register-stratified retrieval failure.
- `2606.29243`: farmer-language transfer and chemical hallucination difficulty.
- E09: real clarification/safety-gating evidence can support the later Beat B story, but it does not by itself establish a retrieval-normalization gain.

### Not yet measured for this beat

- native dialect retrieval improvement from the current map;
- retrieval gain from concept expansion under strict provenance qrels;
- safety-slot preservation after normalization;
- causal end-to-end improvement from normalization to safe advisory;
- live route behavior when dense retrieval is unavailable or restored;
- whether image-derived crop scope improves retrieval independently of oracle crop metadata.

---

## 6. Defensible novelty statement — conditional on new evidence

Do **not** claim:

> We introduce the first Bengali dialect-aware agricultural retriever.

Conditional, defensible wording:

> The companion work diagnoses register-conditioned retrieval failure in Bengali agricultural search. KrishokChat turns that failure into an auditable control problem: it preserves the farmer query, applies bounded interpretation, selects a retrieval scope or clarification path, and records whether the transformation preserved safety-bearing fields.

This becomes a contribution only if the paired intervention and safety-preservation experiments are completed.

If those experiments are not completed, Beat A remains motivation and system description; it should not appear as a measured contribution.

---

## 7. Candidate paper paragraph sequence

1. **Opening:** the farmer’s symptom-only Bengali query does not identify one safe treatment record.
2. **Failure:** standard retrieval is evaluated on formal/document language, while the companion study shows a sharp colloquial-vs-formal gap.
3. **Risk:** generation can fill a missing crop or disease fluently, but evidence access and factual authority are different problems.
4. **Design response:** KrishokChat spends cheap computation first on interpretation and scope; it clarifies when scope is unsafe, narrows retrieval when supported, and leaves an auditable trail.
5. **System demo payoff:** the reviewer can watch the raw query, route, scope, evidence, verification state, and final action rather than seeing an opaque answer.

This is the Beat A story. The final six-page paper should use no more than 2–3 sentences from it.

---

## 8. Reviewer objections to pre-empt

- Register and task are confounded in the companion retrieval paper; use paired information needs for any new claim.
- A gold crop appended to the query is an oracle arm, not a deployable intervention.
- Controlled dialect variants are not equivalent to field-collected dialect conversations.
- Retrieval recall does not imply safer chemical advice.
- A normalizer can damage negation, dosage, units, or chemical identity.
- E49’s heuristic qrels and gold metadata make its current scores unsuitable as headline results.
- E17/E21 simulation results must not be presented as real retrieval or safety measurements.
- Dense retrieval configuration and passage construction materially affect the result; disclose both.

---

## 9. Decision after Beat A pass 1

**Keep Beat A, but do not promote it to a separate contribution yet.** Use it as the motivating failure mechanism for the broader story:

> Bengali farmer language makes retrieval scope uncertain; KrishokChat spends cheap computation to determine whether it can safely narrow that scope, whether it must ask, and whether the final evidence is sufficient to speak.

The next beat should be **Beat F (fluency versus factual authority)** or **Beat B (missing slots before retrieval)**. Beat B is the immediate system intervention; Beat F supplies the high-stakes reason that the intervention matters.

---

## 10. Questions for the project team

These do not block the literature work, but they determine the experiment design:

1. Can native speakers of Sylheti, Chittagonian, Rangpuri, Noakhailli, and Barishal review paired query forms?
2. Is the project willing to freeze a new paired register set (for example, 200 intents × 8 forms) before tuning the maps?
3. Should the EACL paper evaluate retrieval over the AgRiTrust 2,882-node corpus, the current 2,946-document live index, or both as separate frozen settings?
4. Can we obtain a clean run with dense retrieval enabled, or should the system paper explicitly make BM25-first / dense-optional behavior the evaluated deployment mode?
