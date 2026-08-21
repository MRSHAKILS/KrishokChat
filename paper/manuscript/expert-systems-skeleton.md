# Expert Systems (Wiley) — Frozen Skeleton v1 (R1)

**Status:** FROZEN SKELETON — NOT a submission. No empirical claim in this file is promoted.
**Freeze date:** 2026-08-21
**Authority:** `paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/` (adjudication package; moved to `archive/` 2026-08-21) + `docs/PAPER_POLICY.md`
**Thesis (frozen, `03_THESIS_DECISION.md`):** Evidence-linked, relation-aware selective certification for Bengali agrochemical advice under a BM25-only runtime, with dialect/Banglish normalization evaluated as a safety-constrained robustness axis.
**Supersedes (structure only):** `paper/manuscript/T25_paper_skeleton_v1.md` remains for history; this file is the single Wiley SSOT per R1.

> **Number rule (applies to the whole manuscript):** every empirical number is `TODO (gate: G#)` until a run/artifact ID from the frozen claim ledger (`paper/manuscript/CLAIM_LEDGER_FREEZE.md`, source `12_CLAIM_LEDGER.md`) is attached and, for PDF-derived numbers, reconciled by T05 (G0/G1). Do not promote a TODO by repeating it in prose.

**Wiley source (verified 2026-08-21):** `https://onlinelibrary.wiley.com/page/journal/14680394/homepage/forauthors.html` — Expert Systems requires an abstract of **≤250 words** (structured: Introduction/Objectives/Method/Results/Evaluation/Conclusion — or unstructured) containing major keywords, and **4–7 keywords** in the main document and submission system. Title must not contain abbreviations; a short running title of ≤40 characters is required. The final paragraph of the Introduction must describe the paper's structure (e.g., “This paper is structured as follows…”). References, tables (with titles/footnotes), figure legends, and appendices follow the main text. Wiley offers Free Format submission, but the sections above are required at publication. Confirmed via web search `Author Guidelines - Expert Systems - Wiley Online Library` (same URL) on 2026-08-21; page is Cloudflare-protected and was cross-checked via search snippet highlighting the 250-word/4-7-keyword requirements.

---

## Front Matter (Wiley title page)

- **Title:** [TODO: descriptive title without abbreviations, with major keywords — e.g., KrishokChat: Evidence-Linked Relation Verification and Calibrated Selective Certification for Bengali Agricultural Advice] `TODO`
- **Running title:** [≤40 characters] `TODO`
- **Authors & affiliations:** [TODO — full names, institutional affiliations, present address footnote if needed, corresponding author contact] `TODO`
- **Funding / Acknowledgments / Conflict of Interest:** [Wiley requires these as separate statements] `TODO`
- **Data Availability / Code Availability:** [Link to `dataset_release/safety/`, `dataset_release/soil_moisture/`, `backend/ml_assets/rag_index/provenance/`, `research_artifacts/runs/` hashes; Hugging Face + GitHub release per R7] `TODO (G1/G9)`
- **ORCID / Author contributions:** `TODO`

---

## Abstract (≤250 words, structured or unstructured; no undefined acronyms)

**Placeholder skeleton — do not write full prose until G3/G4/G5/G6 pass. Check word count at assembly.**

- Context/safety failure: substring dosage matching cannot distinguish crop/formulation/denominator/interval/PHI/prohibition/source scope → risk when agrochemical dosage advice is unsupported.
- Objectives/gaps: (Gap A) structured dosage verification + calibrated abstention under BM25-only runtime; (Gap B) dialect/Banglish-sensitive retrieval with safety-preserving normalization.
- Method: ClaimSafe-BN schema + deterministic parser/normalizer + structured relation matcher + calibrated selective-certification policy; paired safety-constrained normalization protocol (raw / Unicode / reviewed dictionary); classification-only vision fallback repair.
- Results: `TODO (G4/G5/G6/G7)` — dangerous non-abstention, risk–coverage, Recall@10 with safety-flip non-inferiority, subgroup/variety breakdown, latency.
- Conclusion: one sentence linking each contribution to a run/artifact ID.
- Must contain major keywords; keep acronyms to a minimum.

**Word-count placeholder:** `[TODO — count words, must be ≤250 at submission]`

---

## Keywords (4–7)

`TODO — 4–7 keywords, complement title/abstract; examples (final list frozen at assembly):` Bengali agricultural advisory; retrieval-augmented generation; evidence-linked verification; selective certification; calibrated abstention; dialect robustness; safety evaluation

---

## 1 Introduction

**Purpose:** establish the safety-critical failure mode, two frozen gaps, four contributions, and Bangladesh deployment constraints.

**Skeleton bullets (expand to prose last):**

- Farmers in Bangladesh receive advice via Krishi Call Center (16123) and, increasingly, LLM assistants; dosage-bearing advice is only safe when every element (chemical, formulation, dose, denominator, interval, PHI, applicability, polarity) is supported by a trusted source.
- Substring-level dosage matching (current `DosageVerifier`, S02) cannot make that distinction; medical/claim-verification literature provides no agricultural relation verifier for Bengali dosage advice.
- Gap A: typed evidence relations + calibrated abstention under BM25-only runtime (S01/S11 note: hybrid RRF is now default per S11 — reconcile in Methods whether thesis runtime is frozen BM25 baseline or current hybrid; `TODO (G0)`).
- Gap B: dialect/Banglish normalization must be evaluated jointly for retrieval benefit *and* safety-intent preservation (F09).
- Contributions (frozen, `09_PAPER_CONTRIBUTION_CONTRACT.md`):
  1. **ClaimSafe-BN** — frozen Bengali agrochemical claim resource linking atomic fields, applicability, polarity, uncertainty, and expert relation labels to stable `source_id` + exact `evidence_span` (C1).
  2. **Deterministic-first structured verifier** — parser/normalizer + relation matcher + fail-closed policy vs captured lexical baseline (C2; E1/E3).
  3. **Calibrated selective-certification policy** — development-only threshold exposing risk–coverage tradeoff (C3; E2).
  4. **Paired safety-constrained normalization protocol** — raw/Unicode/dictionary (+ optional learned) with safety/slot invariance (C4; E4–E6; E5 interaction).
- Rejected claims (F08/F12): no first-system, no semantic current verifier, no hybrid novelty, no farmer-outcome/trust/usability claims.
- Bangladesh constraints: local-only audit, fail-closed, helpline 16123 escalation.
- **Structure paragraph (Wiley requirement — keep verbatim at assembly):** “This paper is structured as follows. Section 2 reviews related work and the competitive gaps. Section 3 describes the system architecture. Section 4 details methods (safety, retrieval, verification, calibration, normalization, vision). Section 5 presents the experiment protocol. Section 6 reports results. Section 7 discusses findings. Section 8 states limitations, Section 9 ethics, and Section 10 reproducibility.”

**Empirical anchors (all TODO):** dataset sizes `TODO (G1)`, verifier results `TODO (G4)`, agreement `TODO (G3)`, calibration `TODO (G5)`.

---

## 2 Related Work

**Required structure:** five-group taxonomy per `02_LANDSCAPE_GAPS_COMPETITIVE.md`; closest-system matrix (Table 1) with re-validated URLs at submission.

### 2.1 Five-group taxonomy — gaps table

| Group | Representative systems | What they establish | What remains open (gap) |
|---|---|---|---|
| Verification and selective answering | Farmer.Chat, DG-Eval, RAGChecker/RAGAS, medical claim verifiers | Claim decomposition, generic NLI, medical abstention | No agricultural relation verifier for Bengali dosage-bearing advice; no calibrated abstention under a BM25-only runtime |
| Bengali dialect and retrieval | KrishokBondhu, cross-lingual Bengali agricultural RAG, BhasaBodh/BUNO | Bengali RAG exists; normalization/romanization baselines | No dialect→retrieval measurement for Bangla agriculture; no dialectal safety benchmark |
| Agricultural advisory and escalation | Farmer.Chat field studies, ICT4D systems | Domain comparators, expert ground truth, Bangladesh constraints | No typed dosage verifier; no calibrated risk policy |
| Vision and multimodal routing | Crop-disease vision literature | Classification-only routing norms | Source-grounded treatment evidence in vision fallback (secondary scope) |
| Systems evidence and compute | Industry-track conventions | Component evaluation, latency accounting, artifact release norms | — |

### 2.2 Closest-system matrix (Table 1) — placeholder

- Rows: Farmer.Chat, KrishokBondhu, Cross-lingual Bengali Agricultural RAG, My Climate CoPilot, DG-Eval, RAGChecker/RAGAS, ClinicBot/MedRAGChecker, BhasaBodh/BUNO, current KrishokChat runtime (`02_LANDSCAPE_GAPS_COMPETITIVE.md:32-46`).
- Columns: task, language support, verification mechanism, retrieval, abstention, evidence span, safety handling.
- Source for external facts: `paper/literature review/*` + URLs in `02_NOVELTY_ATTACK.md`; **re-validate every URL before submission** `TODO (G0)`.
- Positioning statement (frozen): paper claims a *measured* relation-verification and abstention protocol + intent-preserving dialect evaluation; does **not** claim multi-agent orchestration, trace UI, generic RAG, or detection/localization.

**Figure/Table callouts:** Table 1 (closest-system matrix), Table 2 (dataset composition — deferred to §5).

---

## 3 System Architecture

**Purpose:** factual description of the captured runtime; safe claims S01–S17 only.

**Figure 1 (required):** 4-stage safety-aware pipeline — `User query → [1] Safety/Router (before retrieval) → [2] Retrieval (BM25; hybrid RRF per S11 — annotate) → [3] Generation (Gemma-4 4-bit / local GGUF + fallback) → [4] Verifier (lexical baseline; structured candidate offline) → Response/Audit`. Terminal outcomes fail closed. See `08_FINAL_SYSTEM_ARCHITECTURE_CONTRACT.md` + `ARCHITECTURE.md` canonical QA flow. Render via `tools/rag/generate_architecture_fig.py` or `capstone/`.

**Architecture facts (cite ledger + manifest):**

- Safety classification precedes retrieval; `banned_or_restricted_chemical` / `self_harm_or_poisoning_risk` → canned referral with Krishi Call Center 16123; terminal outcomes never reach retrieval (S03).
- Retrieval: captured runtime BM25-only (S01); current default hybrid RRF (BM25 + BGE-M3 FAISS, 2,135 nodes, sha256 `0f6f…cb524`) is S11 — clarify which artifact the thesis evaluates vs. ablation.
  - Expansion hit rate: 0.6% on 1,000 farmer queries (S11); 33.49% on T09 dialect split (F17 scope note — do not compare directly).
  - RRF top-1 scores are quantized; raw retrieval scores do not separate answerable/unanswerable (S15/F16).
- Generation: one QA pipeline shared by JSON + SSE (S04); provider failover chain (T0-06) — safety classifier keeps direct client.
- Verifier: captured `DosageVerifier` = normalized lexical dosage matcher (S02), not semantic/relation-aware/calibrated (F02). Structured candidate lives in `backend/app/infrastructure/verification/{normalization,claim_parser,relation_matcher,structured}.py` (T15, offline).
- Vision: artifacts are classification-only, `detection_mode: classification`, `boxes: []` (S05); fallback defect (S06, verified `+` empty sources) specified in T06 and remediated in T21 — never `verified` with empty sources; E7 fixture.
- Benchmark: `GET /api/benchmark` serves **precomputed** `golden_stats_v1.json` (S12); live computation absent.
- Local GGUF: `krishokchat.f16.gguf` artifact present with hashes (S08); no performance claim (F06).
- Coverage gate D1a (S17): six keyword families → `low_confidence` refusal; golden re-run 14/14 refused, 0/32 answerable refused — keyword-scoped, not semantic.
- Audit: local-only JSONL + SQLite sink (T0-01/T0-02), exactly one record per request; no external telemetry.

**Problem formulation (frozen):** given `query`, `answer`, `retrieved passages` (stable `source_id` + exact `evidence_span`), and claim schema (chemical, formulation, amount, unit, denominator, interval, PHI, applicability, polarity, source conflict), certification is a function of parsed evidence. Hypotheses H1–H5 (`04_HYPOTHESES.md`) under expert gold with frozen test split.

---

## 4 Methods

### 4.1 Safety — Router and Deterministic Pre-check

- Six categories: `safe_agri`, `banned_or_restricted_chemical`, `self_harm_or_poisoning_risk`, `off_topic`, `prompt_injection`, `low_confidence` (AGENTS §4).
- Deterministic pre-check (keyword/regex families including coverage gate D1a) → structured LLM classification; parse/provider failure → `low_confidence` (fail-closed).
- Retrieval only on `safe_agri`; all other categories receive canned/referral responses and audit logging.
- Multi-turn safety context and red-team CI belong to P lane (T1-05), not this skeleton.

### 4.2 Retrieval

- **Adjudicated runtime:** BM25 (`rank-bm25`) over precomputed index (`backend/ml_assets/rag_index/`); hash pinned in manifests; `CORPUS_VERSION` in cache keys (P0-7).
- **Current production default:** Hybrid RRF (S11) — BM25 + BGE-M3 dense FAISS, reciprocal-rank fusion. Ablation compares BM25 vs dense vs hybrid at `k=5` (R2).
- No live web scraping / live index building (AGENTS §2.2).
- Retrieve `k` passages with stable IDs; retrieval errors → empty result + controlled referral (fail-closed).

### 4.3 Verifier — ClaimSafe-BN + Structured Matcher

**Schema (frozen T07, `06_CLAIM_SCHEMA_AND_VERIFIER.md`):**

- Atomic fields: `claim_id`, `crop`, `disease/pest`, `action`, `chemical/intervention`, `formulation`, `amount`, `unit`, `denominator`, `interval/frequency`, `PHI/safety condition`, `source_id`, `evidence_span` (offsets + text + source hash), `polarity` (`affirmed`/`negated`/`conditional`/`prohibited`), `applicability` (structured predicate), `uncertainty`, `relation`, `safety_critical`.
- Missing-value rule: `null` = true absence/non-applicability; `unknown` = present but unresolved (never `0`/empty string).
- Normalized vs original text preserved; Bengali digits → ASCII for comparison.
- **Relations (frozen enum):** `supported`, `contradicted`, `partially_supported`, `unsupported`, `ambiguous`, `not_applicable`.
- **Source conflict policy:** match against every candidate span; `ambiguous` + abstain when authoritative spans conflict on material field.
- **Safety-critical criteria:** any error that could change chemical identity, banned status, formulation, dose/denominator/mixture, interval/PHI, PPE/weather/water/livestock/human exposure, applicability, polarity, or poisoning response → only `supported` with all fields certifies.
- Artifacts: JSON Schema `research_artifacts/datasets/frozen/T07_claim_schema_v1.json`, label manual `T07_label_manual_v1.md`, risk taxonomy `T07_risk_taxonomy_v1.md`.

**Extraction (T15):** deterministic parser over Bengali/English numeral, unit, denominator, interval, PHI, polarity, applicability patterns; candidate `backend/app/infrastructure/verification/{claim_parser,normalization,relation_matcher,structured}.py` (dead code w.r.t. runtime; `dosage.py` untouched as lexical baseline).

**Verification:** deterministic-first relation matching with fail-closed policy; hard gates (missing `source_id`/span, required field, dimensional mismatch, contradiction, unresolved conflict) force `abstain`; optional NLI as bounded secondary resolver only (E8, cannot override hard safety rules); LLM judge never gold (F10).

**Aggregation and calibration:** claim relations → answer action (`certify`/`abstain`/`blocked`/`out_of_scope`); calibrator fit on **development only**, frozen before test access (`07_ABSTENTION_AND_DIALECT_PROTOCOL.md`; G5; E2).

**No results in this subsection.** `TODO (G4/G5)`.

### 4.4 Selective Certification (Abstention)

- Score from explicit extraction/match features; at most prespecified calibration families compared on dev; grouped CV within dev if sample permits.
- Threshold `t` frozen via constrained objective (risk at frozen coverage target, or min risk subject to coverage floor; cost ratio frozen after expert review — T07).
- Metrics: `coverage(t)`, `selective risk(t)` = dangerous certification errors / certified answers; false abstention vs dangerous non-abstention; AURC, ECE, Brier (secondary); risk–coverage curves (Figure 3).
- Invalidation: any test-informed threshold/parser/dictionary/prompt change invalidates confirmatory run.
- Latency: per-stage p50/p95 recorded; candidate exceeding T07 budget remains offline.

### 4.5 Normalization — DialectSafe-RAG Paired Protocol

- Paired construction (T11/T13, `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`): one `intent_id` → standard Bangla + native-reviewed regional/Banglish forms judged intent-equivalent; all forms in one source/intent/transformation split; native-review gate for authenticity (G6).
- Frozen slots before transformation: crop, target, chemical/intervention, formulation, amount, unit, denominator, interval/frequency, PHI/safety condition, polarity, harmful intent.
- Conditions: `raw` → `unicode` (grapheme-only) → `dictionary` (Unicode + reviewed lexical mappings with risk-term protection) → `learned_optional` only after dev gate (F17: dictionary derived deterministically from T09 splits, 16-pair map; 0.03% → 33.49% expansion on T09 dialect population; Banglish uncovered).
- Threat model: normalization may corrupt negation, chemical identity, dosage slots, or harmful intent; retrieval-only reporting insufficient (F09). Primary endpoint: Recall@10 subject to harmful-to-benign safety-flip non-inferiority (H4); factorial interaction with verifier (H5/E5).
- Dictionary: every mapping records source/canonical/variety/reviewer/version/examples/safety-flag/allowed context; audit diff + mapping IDs; ambiguous/safety-bearing → exact-context or no-op; unknown input unchanged.

### 4.6 Vision — Crop/Disease Routing + Evidence Grounding

- Two-stage classification: crop classifier → crop-specific disease classifier (Ultralytics `.pt` → ONNX); `detection_mode: classification`, `boxes: []`.
- Treatment advice (when available): enters same QA use case with system-generated query, marked `channel: vision_advisory`; falls under same verifier or explicit `uncertified/abstained` outcome.
- Repaired fallback (T06→T21, E7): source-empty `solution_bn` never receives `verified`; blocked/missing-source/verifier-exception/unavailable-model fixtures covered.
- No localization metrics claimed unless a verified detection artifact lands.

### 4.7 Telemetry & Audit (Stage Latency, Tokens, Cost)

- Audit schema is additive: `stage_timings_ms`, `tokens` (`token_usage` column in SQLite), `provider`, `cost_estimate` (always `null` — no price table), `request_id` (T0-04 contextvar), `cached`, `safety.category`, `retrieval.hit`, `verifier`.
- OTel per-stage spans (P8) were **deferred 2026-08-21** — NOT shipped in the evaluated runtime (dependency absent; no spans wired). Stage-latency evidence comes solely from audit `stage_timings_ms` (T0-05). Any future OTel lane is production tooling only and adds no claim to this manuscript.

---

## 5 Experiments

**Prespecified matrix (`05_MINIMUM_EXPERIMENT_MATRIX.md`; protocol `06_EVALUATION_BENCHMARK_PLAN.md:100-103`; `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`).**

### 5.1 Benchmark and Protocol

- **Annotation protocol v1:** `research_artifacts/annotations/guidelines/T07_protocol_v1.md`; agreement gate α ≥ 0.70; two independent annotators + lead adjudicator; adjudication lineage preserved.
- **Pilot:** 24 dev-only items `research_artifacts/annotations/pilot/T08_pilot_items_v1.jsonl`.
- **Splits:** source/intent/transformation-lineage grouped, seed `20260813`, 60/20/20 by group; leakage check 0 hits; dry-run reproduction verified; hashes in `T09_split_manifest_v1.json` + `T09_artifact_hashes_v1.json`.
- **Baselines:** captured lexical verifier reproduced offline with fixture parity (T12); structured candidate with 26 fail-closed tests (T15).
- **Experiment IDs E1–E7** (minimum; E8/E9 optional), statistics prespecified: paired McNemar, paired clustered bootstrap, Holm correction, grouped bootstrap by intent/source for calibration.
- **Every run requires a manifest:** paths, SHA-256, split IDs, lineage, seed, code revision, dirty-tree flag, config, model/provider/version, dependencies, hardware, failures, output hashes.
- **Dataset composition (Table 2):** counts from manifests only — reconciled totals `TODO (G1)` (e.g., `85,979; 7,437; 323; 6×4,275` in T05 v1 are historical, not frozen). Record method: path + count query + hash.
- **Revalidation checkpoint (G0):** re-read authoritative PDFs (`paper/done papers/*.pdf`) and `02_NOVELTY_ATTACK.md` URLs at assembly — no PDF-derived number without T05 reconciliation.

### 5.2 Experiment Matrix (populate with run/artifact IDs at assembly)

| ID | Priority | Question | Baselines | Variants | Split | Primary metric | Test | Required ablation | Failure mode to report |
|---|---|---|---|---|---|---|---|---|---|
| E1 | **ESSENTIAL** | Relation-aware vs lexical: safety-critical unsupported/contradicted catch | Lexical `DosageVerifier`; fixed LLM judge (secondary) | Deterministic parser + structured matcher; + optional NLI | Grouped train/dev/test; expert-adjudicated test | Dangerous non-abstention rate | Paired McNemar + bootstrap CI for Δ | Oracle vs predicted fields | Bengali aliases, ranges, implied denominators, scattered evidence |
| E2 | **ESSENTIAL** | Calibrated risk–coverage tradeoff | Uncalibrated structured; always-certify/abstain bounds | Frozen calibration families + frozen thresholds on dev | Calibrator on dev; untouched test; adversarial separate | Risk at frozen target coverage / risk | Stratified paired bootstrap for selective risk & AURC | Calibration family & dev-size stability | Sparse high-risk labels → unstable thresholds |
| E3 | **STRONG** | Which fields drive safety gains? | Full structured schema | Remove denominator / interval / PHI / applicability / polarity / source-conflict / all safety fields | Same E1 frozen test predictions | Δ dangerous non-abstention | Paired McNemar + Holm | Each removal listed | Redundant fields; parser errors dominate |
| E4 | **ESSENTIAL** | Dictionary normalization: Recall@10 vs safety invariance | Raw; Unicode-only | Reviewed dictionary; optional learned (if gated) | Paired intent groups; all varieties per intent in one split | Recall@10 with harmful→benign non-inferiority | Paired bootstrap (retrieval) + McNemar/exact (flips) | Remove safety gate; remove risk-term protection; per-variety | Dictionary misses forms or corrupts negation/chemical |
| E5 | **ESSENTIAL** | Verifier × normalization interaction | Lexical/raw | Lexical/dictionary; structured/raw; structured/dictionary | Same paired intents + E1 schema | Dangerous non-abstention interaction contrast (difference-in-differences) | Paired clustered bootstrap by intent | Condition on slot-preserved vs slot-changed | Retrieval distractors or slot corruption erase verifier benefit |
| E6 | **STRONG** | Subgroup unevenness (standard vs regional vs Banglish) | Standard Bangla raw | Each reviewed variety + Banglish under raw/dictionary | Paired by intent; cells frozen pre-test | Worst-group dangerous non-abstention / false-safe rate | Stratified bootstrap CI; descriptive below sample gate | Leave-one-variety-out | Small cells; synthetic variants |
| E7 | **STRONG** | Vision fallback: evidence + fail-closed | Captured defective fixture | Repaired source-linked path; explicit uncertified outcome | Deterministic fixtures + integrated regression | Count of source-empty `verified` | Exact assertion (no inferential test) | Missing source / verifier exception / blocked advisory | Raw `solution_bn` bypass remains reachable |
| E8 | OPTIONAL | NLI for ambiguous relations: worth cost? | Deterministic matcher | + frozen NLI tie-break | E1 split | Macro-F1 on ambiguous/partial (subject to latency budget) | Paired bootstrap + McNemar | NLI off vs NLI-ambiguous-only | Domain mismatch; nondeterminism; latency |
| E9 | OPTIONAL | Learned normalizer vs dictionary | Reviewed dictionary | One frozen learned candidate (only after dev gate) | E4 split | Recall@10 improvement subject to all safety/slot gates | Paired bootstrap + exact tests | Confidence gate + dictionary fallback | Hallucinated expansion; risk-term deletion |

- E1, E2, E4, E5 are **required** for the narrow thesis; E3/E6/E7 support mechanism/subgroup/honesty; E8/E9 may be omitted without weakening the adjudicated contract.
- **STOP conditions (`03_THESIS_DECISION.md`):** no superiority claim if E1 fails; no calibration claim if thresholds move after test access; no subgroup conclusions below sample gate; learned normalizer never defines C4.

### 5.3 Human Study

- **Expert gold (T10):** two annotators + adjudicator; Krippendorff α ≥ 0.70 gate; span/field/relation agreement; adjudication rate; frozen train/dev/test.
- **Expert end-to-end (T23):** blinded labels on integrated system; dangerous pass-through + false abstention.
- **Farmer study:** removed from minimum thesis (T24 dropped); any future farmer study clearly separated, no outcome claim (F12).
- **Dialect native review (T11/T13):** intent equivalence + authenticity agreement; rejection rates; missingness reported.
- **All results:** `TODO (G3/T10, T23, G6)`.

### 5.4 Statistics and Reproducibility Hooks

- Seed `20260813` for splits; split lineage grouping tests; near-duplicate report.
- Manifests: input/output hashes, split IDs, code revision, config, model/provider/version, dependencies, hardware, prompt hash (where applicable), failures.
- Grounding: every claim cites a run/artifact ID; inference at α = 0.05 with prespecified multiplicity control (see §5.2 tests).

---

## 6 Results

**Fully TODO — no sentence in this section may be written before its run/artifact ID exists.**

### Table/Figure slots (fill from manifests at assembly)

- **Table 3:** Verifier baselines — lexical vs structured (+ NLI / LLM judge secondary) — dangerous non-abstention, relation F1, macro-F1 on safety-critical, latency p50/p95, failures — `TODO (G4, E1)`.
- **Table 4:** Field ablations (E3) — Δ dangerous non-abstention per removal — `TODO (G4, E3)`.
- **Table 5:** Retrieval + safety by variety/condition (E4/E6) — Recall@10, MRR, hit-rate, harmful→benign flips, slot preservation, certification risk — `TODO (G6/G7, E4–E6)`.
- **Table 6:** Human agreement + expert evaluation — α/κ, adjudication rate, T23 end-to-end dangerous pass-through — `TODO (G3, T10/T23)`.
- **Table 7:** Latency, compute, failures, coverage — p50/p95 per stage, breaker, gate rates — `TODO (G4, manifests)`.
- **Figure 1:** Pipeline (current vs proposed bounded pipeline) — `08_FINAL_SYSTEM_ARCHITECTURE_CONTRACT.md`.
- **Figure 2:** Structured claim + evidence relation example (with `source_id` + exact `evidence_span`) — `06_CLAIM_SCHEMA_AND_VERIFIER.md`.
- **Figure 3:** Risk–coverage and calibration curves (E2) — dev vs test, threshold sensitivity band.
- **Figure 4:** Paired dialect/normalization design (per-intent raw/Unicode/dictionary + paired tests).

**STOP/warning text to keep in draft:** no post-hoc hypothesis rewrite; no subgroup inference below frozen sample gate; any threshold change after test access invalidates E2.

---

## 7 Discussion

- Interpretation of E1–E5 under the frozen thesis; mechanism vs aggregate result.
- Why lexical matching fails on relation-specific errors (denominator, PHI, applicability) even when numeric hit-rate looks acceptable.
- Retrieval–safety tension: when dictionary expansion helps retrieval but threatens slot/polarity (F09), and how the factorial (E5) isolates interaction.
- Comparison to closest systems (Table 1) — where KrishokChat advances measurement vs literature gaps (`02_LANDSCAPE_GAPS_COMPETITIVE.md`).
- Practical implication: calibrated thresholds expose the cost tradeoff rather than hiding it in one accuracy number.
- Do **not** re-state Results numbers here without citing their table/manifest.

---

## 8 Limitations

- **Expert subjectivity & sample cells:** small-sample subgroup analysis descriptive below gate; α threshold already prespecified.
- **Dialect coverage:** single-region sources; dictionary is a reviewed lexical resource, not complete; Banglish uncovered (F17); native-review agreement reported.
- **Corpus bounds:** government publications; three-day collection window; no deployment study.
- **Helpline escalation:** 16123 referral is the defined escalation path; no outcome measurement (F12).
- **No causal/agronomic/trust/usability/deployment claims** (F12).
- **Model/artifact bounds:** local GGUF present but unevaluated (F06); vision classification-only (S05); hybrid retrieval default (S11) vs adjudicated BM25 — state which was evaluated.
- **Statistical bounds:** prespecified tests only; no undisclosed post-hoc subgroup claims.

---

## 9 Ethics

- **Audit:** local-only (JSONL + SQLite via T0-01/T0-02); no external analytics/telemetry; retention `AUDIT_RETENTION_DAYS=90` (operator-purged, app never auto-deletes; `docs/production_readiness/retention_policy.md`); PII redaction best-effort regex (`backend/app/core/redaction.py`) never claimed perfect.
- **Personal data:** no personal data released in research artifacts; phone/email redaction scoped to audit/session writes; consent/licensing review before any Hugging Face release (R7); soil dataset licensing separate (`docs/soil_moisture_integration/PLAN.md` R7, not this manuscript).
- **Safety escalation:** `banned_or_restricted_chemical` and `self_harm_or_poisoning_risk` receive short, calm redirects with Krishi Call Center 16123 + in-person medical note for emergencies; no long safety essay.
- **Human subjects:** expert/natives are reviewers, not experimental subjects in the narrow thesis; farmer study removed; any future human study requires institutional review and separate protocol.
- **Language & deployment ethics:** dialect work reports authenticity/intent agreement; no claim of complete lexical coverage; no field deployment recommendation without operational trial.

---

## 10 Reproducibility

**Every primary claim must cite a run/artifact ID and hash.**

- **Code:** `backend/app/application/qa_pipeline.py`, `backend/app/application/container.py`, `backend/app/infrastructure/retrieval/`, `backend/app/infrastructure/verification/` (deterministic parser/matcher), vision runners — pinned code revision + dirty-tree flag.
- **Data & indexes:** `backend/ml_assets/rag_index/` (BM25 pickle + corpus + tokenizer/config), `dataset_release/safety/` (**20,112 records recovered on-disk 2026-08-21: `t3_refusal.jsonl` 3,216 sha256 `27acdb64…`; `t4_requery.jsonl` 16,896 sha256 `a578023…`; + `slots.json`/`taxonomy.json`/`phase4_dialect_map.json`; HF canonical `RaiyanKhaan/krishokChat/safety_qa/`** — see `paper/literature review/12_ASSET_VERIFICATION.md` §4), `dataset_release/soil_moisture/` (722 raw images in `soil-moisture-detection/dataset/`, 13 thumbnails tracked), provenance manifests `backend/ml_assets/rag_index/provenance/` (if added in R2).
- **Splits & manifests:** `research_artifacts/datasets/frozen/T09_*`, `research_artifacts/reports/data_audit/T05_*`, `research_artifacts/reports/T12_*` / `T15_*`, per-run manifests (`06_EVALUATION_BENCHMARK_PLAN.md:100-103`).
- **Corpus versioning:** `CORPUS_VERSION` already in demo-cache keys (P0-7) + `indexes/index_sha256.txt` (R2).
- **Golden replay:** `backend/scripts/replay_golden.py --assert-invariants` — **50/50** invariants (46 + 4 injection); CI job `golden` runs it offline.
- **Seed:** `20260813` for deterministic grouped splits.
- **Hardware & dependencies:** recorded per manifest (no inference optimization claimed beyond measured p50/p95).
- **Release checklist (R7 / T26):** independent reproduction in a fresh environment regenerates primary tables; checksums + artifact index; secrets absent; redaction/license review.

---

## References

- Authoritative KrishokChat papers **by filename/path only** per `docs/PAPER_POLICY.md` (do not invent arXiv IDs/DOIs until provided):
  - `paper/done papers/KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf`
  - `paper/done papers/AgriTrust.pdf`
- Literature package URLs from `02_NOVELTY_ATTACK.md` — **full-text re-verification required at assembly (G0)**; stable URLs only.
- **Banned citation:** `arXiv:2606.29243` (“Citation-Grounded Dataset and Benchmark” v1) is **deprecated and INVALID** — `docs/PAPER_POLICY.md` — CI/local grep `2606.29243` must return empty; see `paper/manuscript/README.md`.
- Format: Wiley style (consistent author/year or numeric per journal production choice; Free Format at submission, consistent throughout; DOIs encouraged).

---

## Appendices (if relevant — Wiley permits)

- **Appendix A — Evidence Gate Checklist (G0–G9):**

| Gate | Requirement | Status (2026-08-21) | Blocking |
|---|---|---|---|
| G0 | PDF and artifact claim ledger complete | Partial — T05 v1 ledger exists; 2,946/284/19,768/17,501 still NEEDS RECONCILIATION | Team-paper numerical claims |
| G1 | Dataset locations/counts/hashes reconciled | ✅ T05 v1 (85,979; 7,437; 323; 6×4,275) — re-read at assembly; **safety 20,112 recovered + hashed on-disk 2026-08-21** (`12_ASSET_VERIFICATION.md` §4) | Dataset composition table |
| G2 | Schema and primary endpoints frozen | ⚠️ T07 v1 frozen draft — pending expert sign-off | Annotation and model comparison |
| G3 | Expert pilot and agreement reviewed | ❌ T08 scaffolded; labeling pending | Gold-label claims |
| G4 | Baselines run from manifests | ⚠️ T12 lexical ✅, T15 candidate ✅ offline; no gold comparison | Improvement claims |
| G5 | Threshold frozen on development data | ❌ | Selective-answering claims |
| G6 | Native authenticity/intent audit complete | ❌ T11/T13 pending | Dialect/normalization claims |
| G7 | Paired statistics and error analysis complete | ❌ | Comparative claims |
| G8 | Source-empty vision status fixed | ✅ T06 + T21 (19/19 suite) | End-to-end evidence-safety claims |
| G9 | Independent reproduction complete | ❌ | Submission/release |

- **Appendix B — Manuscript File Map (assembly-time):** `T05_CLAIM_LEDGER_v1.md` → §3/§5; `T07_*` → §4/§5/§6; `T08_pilot_items_v1.jsonl` → §5; `T09_split_manifest_v1.json` / `T09_leakage_report_v1.*` → §5; `T12_baseline_run_manifest_v1.json` / `T15_*` → §6/§7; `t06_*` → §3; `02_LANDSCAPE_GAPS_COMPETITIVE.md` + `paper/literature review/*` → §2; `04_HYPOTHESES.md` / `05_MINIMUM_EXPERIMENT_MATRIX.md` / `07_ABSTENTION_AND_DIALECT_PROTOCOL.md` → §3–§5.
- **Appendix C — Claim Ledger Freeze Reference:** `paper/manuscript/CLAIM_LEDGER_FREEZE.md` (2026-08-21) — S01–S17, F01–F17, U01–U10 with supersedence notes.
- **Appendix D — Additional tables, per-variety subgroup sheets, and parser failure taxonomy (if space, otherwise Supporting Information).**

---

*Frozen 2026-08-21 (R1). No empirical claim in this file is promoted; all numbers are TODO placeholders until their gate passes. This is a documentation-only SSOT — no application, planning-document, naming-cleanup, `tools/`, or P-lane code was modified.*
