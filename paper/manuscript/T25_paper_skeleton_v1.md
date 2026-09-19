# T25 — Paper Skeleton (Non-Empirical Draft v1)

**Status:** DRAFT SKELETON — NOT ready for submission.
**Date:** 2026-08-13
**Authority:** `paper/system_evolution_plan_2026/execution_planning_2026_08_12/` (frozen adjudication package).
**Thesis (frozen, `03_THESIS_DECISION.md`):** Evidence-linked, relation-aware selective certification for Bengali agrochemical advice under a BM25-only runtime, with dialect/Banglish normalization evaluated as a safety-constrained robustness axis.

> **Rule for this file:** every empirical number is a `TODO (gate: <G#>)` placeholder. Nothing here is a claim. Numbers become claims only when a run/artifact ID from the claim ledger (`12_CLAIM_LEDGER.md`) is attached, and every PDF-derived number is reconciled by T05 (G0/G1). Do not promote a TODO by repeating it in prose.

---

## 1. Introduction

**Purpose:** establish the safety-critical failure mode (unsupported/contradicted agrochemical dosage advice in Bengali), the two frozen research gaps (Gap A: structured dosage verification + calibrated abstention; Gap B: dialect-sensitive retrieval with safety-preserving normalization), and the four contributions.

**Draft (non-empirical prose, to be tightened at assembly):**

> Farmers in Bangladesh receive crop-protection advice through a national helpline (Krishi Call Center — 16123) and, increasingly, through LLM-based agricultural assistants. Advice that names a pesticide, formulation, dose, and safety interval is only safe when every element of the recommendation is supported by a trusted source. Substring-level dosage matching — the mechanism used by the current runtime — cannot distinguish a matching number from the wrong crop, formulation, denominator, interval, PHI, prohibition, or source scope.
>
> We present [SYSTEM NAME: TODO] a safety-first Bengali agricultural advisory system whose retrieval and generation pipeline is already deployed and whose verification layer is the subject of this study. The runtime enforces safety classification before retrieval, uses BM25 as its only retriever, and audits every decision locally. On top of this captured runtime we build and evaluate:
>
> 1. **ClaimSafe-BN** — a frozen Bengali agrochemical claim resource linking atomic fields, applicability, polarity, uncertainty, and expert relation labels to stable source IDs and exact evidence spans (Contribution 1).
> 2. **A deterministic-first structured verifier** — parser/normalizer plus relation matcher, compared against the captured lexical baseline under expert gold (Contribution 2).
> 3. **A calibrated selective-certification policy** — a frozen development-time threshold that exposes the risk–coverage tradeoff instead of hiding it in one categorical label (Contribution 3).
> 4. **A paired safety-constrained normalization protocol** — measuring how reviewed dictionary normalization of standard Bangla, regional forms, and Banglish changes BM25 retrieval *and* relation certification, requiring safety and slot invariance (Contribution 4).

**Empirical anchors (all TODO):** dataset sizes `TODO (G1)`, model results `TODO (G4)`, agreement `TODO (G3)`, calibration outcomes `TODO (G5)`.

## 2. Related Work

**Structure:** five-group taxonomy per `02_LANDSCAPE_GAPS_COMPETITIVE.md`; closest-system matrix (Table 1).

| Group | Representative systems | What they establish | What remains open |
|---|---|---|---|
| Verification and selective answering | Farmer.Chat, DG-Eval, RAGChecker/RAGAS, medical claim verifiers | Claim decomposition, generic NLI, medical abstention | No agricultural relation verifier for Bengali dosage-bearing advice; no calibrated abstention under a BM25-only runtime |
| Bengali dialect and retrieval | KrishokBondhu, cross-lingual Bengali agricultural RAG, BhasaBodh/BUNO | Bengali RAG exists; normalization/romanization baselines exist | No dialect→retrieval measurement for Bangla agriculture; no dialectal safety benchmark |
| Agricultural advisory and escalation | Farmer.Chat field studies, ICT4D systems | Domain comparators, expert ground truth, Bangladesh constraints | No typed dosage verifier; no calibrated risk policy |
| Vision and multimodal routing | Crop-disease vision literature | Classification-only routing norms | Source-grounded treatment evidence in vision fallback (secondary scope; see `05_vision_crop_disease.md`) |
| Systems evidence and compute | Industry-track conventions | Component evaluation, latency accounting, artifact release norms | — |

**Closest-system matrix (Table 1):** external facts trace to the literature package; **re-validate every URL before submission** `TODO (G0)`. Rows: Farmer.Chat, KrishokBondhu, Cross-lingual Bengali Agricultural RAG, My Climate CoPilot, DG-Eval, RAGChecker/RAGAS, ClinicBot/MedRAGChecker, BhasaBodh/BUNO, current KrishokTech runtime (`02_LANDSCAPE_GAPS_COMPETITIVE.md:32-46`).

**Positioning statement (frozen):** the paper claims a measured relation-verification and abstention protocol for Bengali agricultural advice, paired with an intent-preserving dialect normalization evaluation. It does **not** claim novelty from multiple agents, a trace UI, generic RAG, or classification-only vision (`02_LANDSCAPE_GAPS_COMPETITIVE.md:48-50`; forbidden claims F08 in `12_CLAIM_LEDGER.md`).

## 3. Current System and Problem Formulation

**Content (architecture facts from the captured runtime — safe claims S01–S10 in `12_CLAIM_LEDGER.md`):**

- Safety classification precedes retrieval; terminal outcomes fail closed (S03).
- BM25 is the only retriever (S01); no dense/hybrid index is active (F01).
- The current verifier is a normalized lexical dosage matcher (S02) — NOT semantic, relation-aware, or calibrated (F02).
- JSON and SSE endpoints share one QA pipeline (S04).
- Vision artifacts perform classification only, return no boxes (S05); the source-empty fallback defect was specified (T06) and remediated (T21) — never marked `verified` with empty sources (S06 fixed; E7).
- The benchmark endpoint is a placeholder; research metrics are generated offline (S07).
- Local LoRA adapter artifact exists with recorded hashes and metadata (S08); no performance claim is made (F06).
- Local PDF numbers: `TODO (G1)` — reconciled counts only (T05 v1: `research_artifacts/reports/data_audit/T05_CLAIM_LEDGER_v1.md`).

**Problem formulation (frozen):** given a generated answer, a set of retrieved source passages, and a claim schema with typed relations (chemical, formulation, amount, unit, denominator, interval, PHI, applicability, polarity, source conflict), a certification decision is a function of parsed evidence. The research questions are H1–H5 (`04_HYPOTHESES.md`), evaluated under expert gold with a frozen test split.

## 4. ClaimSafe-BN: Schema, Extraction, Verification, Aggregation, Calibration

**Schema (frozen at T07):** atomic fields, applicability, polarity, uncertainty, expert relation labels, stable `source_id`, exact `evidence_span` — JSON Schema `research_artifacts/datasets/frozen/T07_claim_schema_v1.json`; label manual `research_artifacts/annotations/guidelines/T07_label_manual_v1.md`; risk taxonomy `T07_risk_taxonomy_v1.md`.

**Extraction:** deterministic parser over Bengali/English numeral, unit, denominator, interval, PHI, polarity, and applicability patterns — candidate implementation `backend/app/infrastructure/verification/{normalization,claim_parser,relation_matcher,structured}.py` (T15; dead code w.r.t. runtime; `dosage.py` untouched).

**Verification:** deterministic-first relation matching with fail-closed policy; optional NLI as a bounded secondary resolver only (E8, optional); LLM judge is never gold (F10).

**Aggregation and calibration:** risk-coverage policy fit on development data only, frozen before test access (G5; E2; `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`).

**No results in this section.** All outcome numbers: `TODO (G4/G5)`.

## 5. DialectSafe-RAG: Paired Construction, Normalization Conditions, Threat Model

**Paired construction (frozen, T11/T13 pending native review):** parallel standard Bangla, regional variety, and Banglish forms per intent; all forms of one intent in one split (AGENTS rule 14); native-review gate for authenticity and intent equivalence (G6).

**Normalization conditions:** raw → Unicode/grapheme-only → reviewed dictionary; optional learned candidate only after all gates (E9, optional; U08).

**Threat model (frozen, `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`):** normalization may change negation, chemical identity, dosage slots, or harmful intent; retrieval-only reporting is insufficient (F09). Primary endpoint: Recall@10 subject to harmful-to-benign safety-flip non-inferiority (H4); factorial interaction with verifier condition (H5/E5).

**No results in this section.** All outcome numbers: `TODO (G6/G7)`.

## 6. Benchmark and Protocol

**Frozen facts (safe to state):**

- Annotation protocol v1: `research_artifacts/annotations/guidelines/T07_protocol_v1.md`; agreement gate alpha ≥ 0.70 (T07 defaults; pending expert sign-off — `TODO (G2/G3)`).
- Pilot items (24, dev-only): `research_artifacts/annotations/pilot/T08_pilot_items_v1.jsonl`.
- Splits: source/intent/transformation-lineage grouped, seed 20260813, 60/20/20 by group; leakage check 0 hits; dry-run reproduction verified; hashes in `research_artifacts/datasets/frozen/T09_split_manifest_v1.json` and `T09_artifact_hashes_v1.json`.
- Baseline: captured lexical verifier reproduced offline with fixture parity (T12); structured candidate with 26 fail-closed tests (T15).
- Experiment matrix E1–E7 minimum set; statistics prespecified (paired McNemar, paired clustered bootstrap, Holm correction; `05_MINIMUM_EXPERIMENT_MATRIX.md`).
- Every run requires a manifest with input/output hashes, split IDs, seed, code revision, configuration, model/provider/version, hardware, failures (`06_EVALUATION_BENCHMARK_PLAN.md`; AGENTS rule 7).

**Numbers in this section must be re-read from manifests at assembly — do not copy from this skeleton:** `TODO (G1/G4)`.

## 7. Results

**Fully TODO. Table slots:**

- Table 3: verifier baselines and primary metrics — `TODO (G4)`.
- Table 4: field ablations — `TODO (G4, E3)`.
- Table 5: retrieval and safety by variety/condition — `TODO (G6/G7, E4–E6)`.
- Table 7: latency, compute, failures, coverage — `TODO (G4, manifests)`.

**No sentence in this section may be written before its run/artifact ID exists.** `STOP` conditions (`03_THESIS_DECISION.md`): no superiority claim if E1 fails; no calibration claim if thresholds move after test access; no subgroup conclusions below sample gate.

## 8. Human Evaluation

- Expert gold (T10): two independent annotators + lead adjudicator, Krippendorff alpha ≥ 0.70 gate, adjudication lineage preserved (AGENTS rules 6, 10).
- Expert end-to-end evaluation (T23): blinded expert labels on the integrated system; dangerous pass-through and false abstention.
- Farmer study: **removed from minimum thesis** (T24 dropped); any future farmer study is clearly separated and makes no outcome claim (F12).
- **All results: `TODO (G3/T10, T23)`.**

## 9. Error Analysis

**Method (pre-specified, frozen):** extraction vs relation error decomposition via oracle-field mode (E1 ablation); failure taxonomy from T15 abstention causes (material fields absent, chemical absent from own passage, parse failures, non-affirmed polarity, chemical identity unresolved — recorded in T15 report as **descriptive implementation observations, not paper claims** `TODO (G4)`); per-variety subgroup analysis (E6, descriptive below sample gate).

## 10. Limitations and Ethics

- Expert subjectivity and small sample cells; no inference below frozen sample gate.
- Dialect coverage: single-region sources; dictionary reviewed by native speakers, not a complete lexical resource.
- Corpus bounds: government publications; three-day collection window; no deployment study.
- Helpline limits: 16123 referral is the escalation path; no outcome measurement.
- No causal, agronomic-outcome, trust, or usability claims (F12).
- Ethics: local-only audit; no personal data released; source licensing/consent review before HF release (R7 in `docs/soil_moisture_integration/PLAN.md` applies to the separate soil dataset, not this manuscript).

## 11. Conclusion

**Write last.** May claim only what frozen results establish (blueprint §11; `10_PAPER_BLUEPRINT.md:31-35`). Placeholder sentence: `[TODO: one-paragraph summary of the four contributions, each linked to a run/artifact ID — empty until G3/G4/G5/G6/G7 pass.]`

---

## Appendix A — Evidence Gate Checklist (G0–G9)

| Gate | Requirement | Status (2026-08-13) | Blocking |
|---|---|---|---|
| G0 | PDF and artifact claim ledger complete | Partial — T05 v1 ledger exists; 2,946/284/19,768/17,501 still NEEDS RECONCILIATION | Team-paper numerical claims |
| G1 | Dataset locations/counts/hashes reconciled | ✅ T05 v1 (85,979; 7,437; 323; 6×4,275) | Dataset composition table |
| G2 | Schema and primary endpoints frozen | ⚠️ T07 v1 frozen draft — pending expert sign-off | Annotation and model comparison |
| G3 | Expert pilot and agreement reviewed | ❌ T08 pilot scaffolded; labeling pending | Gold-label claims |
| G4 | Baselines run from manifests | ⚠️ T12 lexical ✅, T15 candidate ✅ offline; no gold comparison | Improvement claims |
| G5 | Threshold frozen on development data | ❌ | Selective-answering claims |
| G6 | Native authenticity/intent audit complete | ❌ T11/T13 pending | Dialect/normalization claims |
| G7 | Paired statistics and error analysis complete | ❌ | Comparative claims |
| G8 | Source-empty vision status fixed | ✅ T06 remediated + T21 regression tests (19/19 suite) | End-to-end evidence-safety claims |
| G9 | Independent reproduction complete | ❌ | Submission/release |

## Appendix B — Manuscript File Map (assembly-time)

- `T05_CLAIM_LEDGER_v1.md` → §3, §6 numbers
- `T07_*` (protocol, schema, manual, taxonomy) → §4, §6, §8
- `T08_pilot_items_v1.jsonl` → §8
- `T09_split_manifest_v1.json` / `T09_leakage_report_v1.*` → §6
- `T12_baseline_run_manifest_v1.json` / `T12_failure_log_v1.jsonl` → §7, §9
- `T15_structured_predictions_v1.jsonl` / `T15_failure_log_v1.jsonl` → §7, §9
- `t06_vision_defect_spec_v1.md` / `t06_evidence_manifest_v1.md` → §3
- `02_LANDSCAPE_GAPS_COMPETITIVE.md` + `paper/literature review/*` → §2
- `04_HYPOTHESES.md` / `05_MINIMUM_EXPERIMENT_MATRIX.md` / `07_ABSTENTION_AND_DIALECT_PROTOCOL.md` → §3–§6

---

*Skeleton prepared 2026-08-13. No empirical claim in this file is promoted; all numbers are TODO placeholders until their gate passes. This is a new manuscript output only — no application code or planning document was modified.*