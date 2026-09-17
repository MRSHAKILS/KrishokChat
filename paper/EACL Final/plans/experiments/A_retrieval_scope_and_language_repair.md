# Beat A Experiment Plan — Retrieval Scope and Language Repair

**Status:** planned; primary path = existing released benchmarks; optional paired annotation = P2  
**Priority:** P0 if Beat A will be claimed as a contribution; otherwise use only the companion-study motivation.  
**Principle:** no new headline claim until the experiment runs over frozen provenance qrels.  
**Dataset policy (user decision 2026-09-17):** accepted demo papers routinely reuse released/external datasets (RAGVUE→StrategyQA; GenGO Ultra→SciTLDR/SciRIFF; NLP-KG→SciERC; OpenEval→12 benchmarks). We therefore use the released `2606.29243` benchmark and `2608.14886` AgRiTrust set as the primary backbone. Constructing a new human-validated paired set is **optional (P2)** and only if time remains.

## 0. Primary vs optional evidence paths

| Path | Dataset | Status | Gate |
|---|---|---|---|
| P1 — controlled register stress | PRISM Benchmark 1,000 (10 categories × 100, route labels) | Exists locally; **provenance audit REQUIRED** (generation script `generate_prism_benchmark.py`) | Gate 0–2 |
| P2 — authentic farmer transfer | Farmer Benchmark 1,000 (483 fb, 300 field, 217 web); official 350 held-out split | Exists locally | Gate 0–2 |
| P3 — strict retrieval qrels | AgRiTrust 900 queries / 2,882 nodes (HF `RaiyanKhaan/AgriTrust-RAG`) | NOT local; download + node cross-check pending | Gate 0–2 |
| P4 — live-system diagnostic | Local 2,135-node chunk index (BM25 + stored 1024-dim dense) | Exists locally; embeddings provenance audit REQUIRED | Gate 1 only, reported separately |
| P5 — optional paired annotation | 200 intents × 8 forms = 1,600 queries, native review | Does not exist | OPTIONAL (P2); never the primary claim |

Do not merge P1–P4 into one number. Report each path separately with its own corpus unit.

## 1. Research questions

- **RQ-A1:** Does query register change retrieval when the underlying information need and gold evidence are held constant?
- **RQ-A2:** Which language-repair intervention improves retrieval: Unicode normalization, reviewed dialect mapping, concept hypotheses, translation, hybrid retrieval, or route selection?
- **RQ-A3:** Does the intervention preserve safety-bearing semantics?
- **RQ-A4:** Does better retrieval produce a safer end-to-end advisory, or only a higher retrieval score?

## 2. Minimum defensible study

### 2.1 P1 — PRISM Benchmark 1,000 (controlled registers)

The local PRISM set already covers 8 language/register conditions × 100 queries:

- A_formal_bengali, B_colloquial_bengali, C_dialect, D_banglish, E_typo_noisy, F_underspecified, G_follow_up, H_multi_turn, I_ambiguous_disease, J_high_risk_treatment.

Each row carries `true_crop`, `true_symptom`, `expected_route`, `expected_answerability`, `needs_clarification`, and `best_clarification_question` — enough for retrieval + routing + clarification evaluation.

**Required before use:** audit `generate_prism_benchmark.py` — generation model, prompts, any human review, and whether `true_*` labels were hand-checked. Report this provenance in the paper appendix. If the audit shows LLM-only generation with no review, label the set "generated stress test" and do not call it field-collected.

### 2.2 P2 — Farmer Benchmark 1,000 (authentic transfer)

Use the official held-out split (350 queries per `2606.29243`). Sources: Facebook farmer groups, field collection, krishibangla.com. This is the authentic-farmer-language transfer test; do not merge with PRISM.

### 2.3 P3 — AgRiTrust 900 (strict retrieval qrels)

Download from HF `RaiyanKhaan/AgriTrust-RAG`; freeze. Report farmer-anchored (300), KG-grounded (400), safety-critical (200) separately. Report the 100 low-agreement farmer queries as uncertainty analysis.

### 2.4 P4 — live-system diagnostic (deployment mode)

Run the exact production retrieval path (BM25 over 2,135-node chunk index; dense via stored 1024-dim embeddings) on the Farmer Benchmark. Log the actual string passed to the retriever. Report separately from P1/P3; this is deployment evidence, not qrels evidence.

### 2.5 P5 — optional paired annotation (P2, last)

If time remains: 200 intents × 8 forms = 1,600 queries with native review. This strengthens dialect-specific claims but is **not** required for the demo paper.

## 3. Baseline and intervention ladder

| Arm | Description | Deployable? |
|---|---|---|
| A0 | BM25 on raw query | Yes |
| A1 | BM25 + Unicode/grapheme normalization | Yes if code path is frozen |
| A2 | BM25 + reviewed dialect lexicon (110-pair map) | Yes if map is frozen |
| A3 | BM25 + bounded concept hypotheses (ConceptNormalizer) | Yes if exact runtime path is used |
| A4 | Dense on raw query (stored checkpoint or BGE-M3) | Yes if checkpoint provenance verified |
| A5 | Fixed BM25+dense RRF | Yes if both channels available |
| A6 | Bengali-to-English translation retrieval baseline | Comparison only; reproduce protocol explicitly |
| A7 | Route-conditioned retrieval (AdaptiveRetrievalRouter) | Proposed policy; must log route and fallback |
| A8 | Oracle canonical query | Ceiling, not deployable |
| A9 | Oracle crop scope | Ceiling, not deployable |
| A10 | Predicted crop scope | Deployable only if prediction comes from the evaluated system |

**BGE-M3 decision (user Q4):** the API key exists and 1024-dim embeddings are already stored. Audit `embeddings.npy` provenance; regenerate as a frozen checkpoint (model string, dims, corpus hash, date, script) if unverifiable. If the API is unavailable, use the frozen checkpoint and label the run.

## 4. Required ablations

Use a cumulative ladder:

```text
raw query
  → Unicode normalization
  → reviewed dialect mapping
  → bounded concept hypotheses
  → hybrid fusion
  → predicted crop/topic scope
  → clarification or fail-closed fallback
```

For every query and arm, save:

- raw query;
- normalized/expanded query;
- matched terms and concept hypotheses;
- route and rationale;
- candidate scope size;
- top-k node IDs and scores;
- gold node rank or miss;
- whether crop came from text, image, user confirmation, prediction, or oracle;
- safety-bearing slot changes;
- latency and model/API configuration.

## 5. Metrics

### Retrieval

- strict node-level Recall@1/5/10;
- relaxed source-level Recall@k where multiple passages contain equivalent evidence;
- MRR and nDCG@10;
- per-register, per-dialect, per-script, and per-task scores;
- formal-to-target register gap;
- gold-in-candidate-scope rate;
- candidate-node count and search-space reduction.

### Interpretation fidelity

Exact match or span/slot F1 for crop, disease/pest, action, chemical, amount, unit, denominator, interval, PHI, negation, and harmful-intent class.

### Safety

- harmful-to-benign flips;
- benign-to-harmful flips;
- wrong-crop and wrong-chemical retrieval;
- unsupported dosage rate;
- safe abstention;
- dangerous non-abstention;
- claim-level citation precision/recall.

### Systems

- normalization, routing, retrieval, and total p50/p95 latency;
- memory/index size;
- LLM/API calls and token use;
- fallback and clarification rates;
- response-language correctness.

## 6. Statistical protocol

- Treat the underlying information need as the primary cluster, not each surface form as independent.
- Use 10,000-query bootstrap resamples over intent clusters.
- Use paired permutation or Wilcoxon tests for retrieval deltas.
- Correct multiple comparisons with Holm.
- Report confidence intervals and effect sizes.
- Use exact or McNemar tests for paired semantic/safety flips.
- Report the 100 low-agreement AgRiTrust queries separately as uncertainty analysis.

## 7. Known invalid or insufficient current evidence

The current E49 script must not be used as the primary Beat A result without redesign:

- heuristic crop/disease relevance rather than strict provenance qrels;
- partial disease-token matching;
- gold crop appended in filtered configurations;
- gold working memory in the full route configuration;
- dialect map not passed in the dialect lexical arm;
- title-only cross-crop checks;
- no end-to-end safety preservation audit.

E17/E21 simulation outputs also cannot support a real retrieval or safety claim. Keep them as internal diagnostics only, clearly labeled simulations.

## 8. Experiment gates

### Gate 0 — data contract

Freeze corpus, qrels, query forms, map version, and split. Compute hashes. Confirm no surface-form leakage across splits. Complete the PRISM provenance audit and the embeddings checkpoint audit (see `datasets_inventory.md`).

### Gate 1 — pipeline fidelity

Run the exact live/offline retrieval path. Log the actual string passed to the retriever. Ensure `expanded_queries` are consumed where claimed.

### Gate 2 — retrieval validity

Run A0–A7 with strict and relaxed qrels. Review 100 misses and 100 wins manually.

### Gate 3 — semantic preservation

Have native/agronomic reviewers inspect all normalization-induced slot changes and all harmful/benign flips. (If no reviewers are available, use the `expert_provided` subset of the Farmer Benchmark and disclose the limitation.)

### Gate 4 — end-to-end safety

Only if Gate 3 passes, run grounded generation + verifier on a frozen subset. Report safe coverage and dangerous acceptance with denominators.

### Gate 5 — paper decision

- If the intervention improves retrieval **and** preserves safety: Beat A may be a measured system contribution.
- If retrieval improves but safety preservation is unmeasured: Beat A remains a diagnostic/system-design motivation.
- If retrieval does not improve: retain the failure story, report the negative result if informative, and do not claim repair.

## 9. Planned status labels for the paper

- **Measured:** direct output of a frozen runner over frozen qrels.
- **Implemented:** code path exists but no valid benchmark result yet.
- **Proxy:** engineering diagnostic, not a user or safety outcome.
- **Simulated:** generated or fixed-probability scenario; not empirical system evidence.
- **Unmeasured:** no defensible result; must not be implied.

## 10. Status marks (for later agents)

- [x] Dataset-reuse policy resolved (released benchmarks = primary; annotation = optional P2)
- [x] Local datasets located and counted (PRISM 1,000; Farmer 1,000; dense 2,135×1024)
- [ ] PRISM provenance audit (generation script review)
- [ ] AgRiTrust download + node-ID cross-check
- [ ] embeddings.npy provenance audit / regenerated checkpoint
- [ ] Index + map hashes frozen
- [ ] Runner A0–A7 written against frozen contract
- [ ] Gate 0–5 executed
- [ ] Optional P5 paired annotation (only if time remains)
