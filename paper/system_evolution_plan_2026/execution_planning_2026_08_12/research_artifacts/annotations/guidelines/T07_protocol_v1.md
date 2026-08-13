# T07 Protocol v1 — Frozen Research Protocol

**Version:** v1
**Date:** 2026-08-12
**Status:** FROZEN DRAFT — pending expert sign-off item (see §9)
**Authority:** `execution_planning_2026_08_12/` package; supersedes parent-plan decisions on any conflict
**Inputs:** `03_THESIS_DECISION.md`, `04_HYPOTHESES.md`, `05_MINIMUM_EXPERIMENT_MATRIX.md`, `06_CLAIM_SCHEMA_AND_VERIFIER.md`, `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`, `11_FINAL_IMPLEMENTATION_SPEC.md`, T05 ledger, T06 spec

## 1. Frozen Thesis
Evidence-linked, relation-aware selective certification for Bengali agrochemical advice under a BM25-only runtime, with dialect/Banglish normalization evaluated as a safety-constrained robustness axis (OPTION B: Keep A, modify B).

## 2. Scope and Constraints (immutable)

- Runtime retrieval is **BM25 only**. No dense/hybrid retrieval for this thesis.
- The verifier is **deterministic-first**: parser/normalizer + structured relation matcher + deterministic safety policy. NLI is optional, offline, secondary-only.
- **No LLM judge is gold.** Fixed LLM judge is a secondary baseline with exact model/version, prompt, raw output, failure logs, and cost recorded.
- **No learned normalizer by default.** Only after the dictionary baseline misses the frozen development target AND all gates in `07_ABSTENTION_AND_DIALECT_PROTOCOL.md` §Learned-Normalizer Gate pass.
- Existing runtime ports (safety-before-retrieval, BM25, verifier port, fail-closed, local-only audit) must not change during research; research runs are offline harnesses.
- Vision fallback source-empty advice must never be marked `verified` (T06 remediation enforced before any integrated safety claim).

## 3. Unit of Analysis and Claim Schema

Follow `06_CLAIM_SCHEMA_AND_VERIFIER.md` exactly. One item = query + answer + retrieved passages + stable evidence IDs + one or more atomic claims + expert relation labels + safety criticality + release action. Split compound advice before labeling.

Schema JSON Schema (machine-readable): `research_artifacts/datasets/frozen/T07_claim_schema_v1.json`.

Missing-value rules: JSON `null` only for true absence/non-applicability; `unknown` for present-but-unresolved; never `0`/empty string/defaults for missing numerics. Any missing `source_id`, evidence span, chemical identity, amount-attached unit, required denominator, material interval, PHI, polarity, or applicability blocks certification for a safety-critical claim.

## 4. Relation Types (frozen enum)

Relations: `supported` | `contradicted` | `partially_supported` | `unsupported` | `ambiguous` | `not_applicable` exactly as defined in `06_CLAIM_SCHEMA_AND_VERIFIER.md` §Frozen Relation Types.

Safety-critical certification rule: only `supported` (all required fields + evidence) may certify. All others abstain or trigger the safe referral path.

## 5. Data Partitions and Splits

| Partition | Use | Prohibited use |
|---|---|---|
| Train | Fit parser resources / dictionaries only when required | Threshold selection; final reporting |
| Development | Select parser version, calibration family, threshold, justified margins | Reporting as final test evidence |
| Test | One frozen confirmatory evaluation | Any change after freeze |
| Adversarial | Stress negation, unit swaps, denominators, intervals, PHI, source conflict, transliteration, code-mixing, harmful intent; report separately | Mixing with test; selecting primary threshold |

Split rule (immutable): group by **source document, intent family, and transformation lineage**. All dialect/Banglish/adversarial forms of one intent stay in ONE split. Near-duplicate check required.

## 6. Primary Endpoints and Margins

Frozen with T07 (see `research_artifacts/manifests/T07_endpoints_margins_multiplicity_latency_v1.md`):

| Endpoint | Definition | Test bound / margin |
|---|---|---|
| E1 dangerous non-abstention rate | Certified safety-critical claims labeled `contradicted`/`unsupported`/`ambiguous`/`partially_supported` (with missing material component) / certified total | Compare structured vs lexical via paired McNemar + paired bootstrap CI; superiority requires CI excludes null |
| E2 selective risk at target coverage | precedence: risk at frozen target coverage OR minimum risk subject to frozen coverage floor | risk/coverage threshold frozen dev-only; report AURC/ECE/Brier secondarily |
| E3 field-removal ablations | Δ dangerous non-abstention per removed field group | Holm-corrected paired McNemar per prespecified ablation |
| E4 Recall@10 w/ safety-flip non-inferiority | retrieval Recall@10 subject to harmful-to-benign safety-flip non-inferiority margin | equality/one-sided margin frozen; safety flip Δ not exceed margin |
| E5 interaction (verifier × normalization) | difference-in-differences contrast on dangerous non-abstention across lexical/structured × raw/dictionary, paired by intent | clustered paired bootstrap by intent; prespecified contrast |
| E6 subgroup | worst-group dangerous non-abstention/false-safe rate across varieties | stratified bootstrap CI; **descriptive only** below sample gate |
| E7 vision repair | count of source-empty advice marked verified | exact assertion = 0 |
| E8/E9 optional | see matrix; only after feasibility/gates | — |

**Cost ratio / constrained objective (frozen dev value):** dangerous non-abstention has strictly higher policy cost than false abstention. Default frozen objective in v1: **minimum test selective risk subject to coverage ≥ 0.80** (coverage floor frozen at 0.80 pending expert risk review in §9). This is the default until expert sign-off changes it through the amendment process.

## 7. Multiplicity Control

- Primary endpoint set is E1, E2, E4, E5 (minimum paper set per matrix).
- All pairwise superiority comparisons on E1 use **paired McNemar**; bootstrap CIs via **paired bootstrap by intent/source group**.
- E3 ablations and E6 subgroups: **Holm-Bonferroni correction** across prespecified comparisons.
- No post-hoc test selection. Any comparison not listed in the matrix is exploratory and labeled as such.

## 8. Latency Budget and Sample Gates

Frozen values live in `research_artifacts/manifests/T07_endpoints_margins_multiplicity_latency_v1.md`:
- Stage p50/p95 latency budget per stage (safety, retrieval, generation-constrained, verifier).
- Minimum cell size for inferential claims; below the gate report descriptively only.
- Minimum expert agreement target (Krippendorff alpha or kappa) and adjudication-rate headroom.

## 9. STOP/GO Status and Open Items

**Gate: STOP if stable evidence spans or expert support are unavailable.**

- Stable evidence spans: **GO** — T05 verified dataset files with stable hashes and split files exist; source IDs/spans are reconstructable for the dataset tracks (BM25 corpus `knowledge_nodes_clean.jsonl`).
- Expert sign-off: **STOP — NOT YET AVAILABLE.** Protocol v1 is a frozen draft pending named expert sign-off for: (1) coverage floor and cost-ratio decision, (2) source authority/recency rules, (3) relation-gold labeling manual adoption. Until sign-off, no test data is accessed and no confirmatory run executes.

**Therefore current gate status: STOP (no confirmatory run) until §9 items clear.** This protects the frozen protocol from being treated as final without domain sign-off.

## 10. Change Protocol

Any change to this freeze (endpoints, margins, schema, relations, partitions, thresholds, errors) requires a dated amendment in `MEMORY.md` containing: proposed change, evidence, affected hypotheses/experiments, invalidated runs, expert approval, and re-freeze version. Test-informed changes invalidate the confirmatory run.

## 11. Required Report Artifacts per Run

Every run records (per `06_EVALUATION_BENCHMARK_PLAN.md:100-103`): `run_id`, UTC timestamp, git commit, dirty-tree flag, task, dataset version, input SHA-256 hashes, split IDs, code/config hashes, model/provider/version, prompt hash, seed, hardware, dependency lock hash, thresholds, output paths, metric code version, failures, parent run.