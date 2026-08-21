# T15 Structured Verifier Candidate — Implementation Report v1

**Task:** P2 T15 — deterministic parser/normalizer + structured relation matcher as a
SEPARATE candidate against the T12 frozen lexical baseline.
**Status:** COMPLETE (candidate implemented; gate GO offline — no hard failure certifies).
**Date:** 2026-08-13 · **Run id:** `T15-20260812T204643Z`
**Manifest:** `research_artifacts/manifests/T15_structured_run_manifest_v1.json`
**Authority:** `11_FINAL_IMPLEMENTATION_SPEC.md` row T15; `06_CLAIM_SCHEMA_AND_VERIFIER.md`;
`T07_protocol_v1.md`; scoped AGENTS.md rule 12/15/16.

## Deliverables

| File | Description |
|---|---|
| `backend/app/infrastructure/verification/normalization.py` | Bengali→ASCII digits, unit/denominator/interval/PHI alias tables, canonical comparison form. |
| `backend/app/infrastructure/verification/claim_parser.py` | Atomic-claim extraction (sentence split with offsets), schema fields (chemical, amount+unit, denominator, interval, PHI, polarity, applicability, action, formulation), explicit parse failures. |
| `backend/app/infrastructure/verification/relation_matcher.py` | Evidence-unit parser + frozen relation decision (supported/contradicted/partially_supported/unsupported/ambiguous/not_applicable) with field traces and source-conflict policy. |
| `backend/app/infrastructure/verification/structured.py` | Orchestration + fail-closed certification policy + oracle-field mode (T17 decomposition). |
| `research_artifacts/tests/test_structured_verifier.py` | 26 fail-closed tests (see §Gate). |
| `research_artifacts/scripts/run_structured_verifier.py` | Offline runner, same frame as T12. |
| `research_artifacts/runs/T15_structured_predictions_v1.jsonl` | 11,224 per-record verdicts. |
| `research_artifacts/runs/T15_structured_claims_v1.jsonl` | 26,995 per-claim structured traces (relation, field trace, reasons, tier, spans). |
| `research_artifacts/runs/T15_failure_log_v1.jsonl` | 0 entries (all 11,224 passages reachable). |

**Runtime isolation:** the candidate is NEW dead code from the pipeline's perspective;
`dosage.py` and all runtime modules are untouched (backend suite 11/11 passes).

## Design (frozen-contract faithful)

- Relations, missing-value rules, polarity handling, and the source-conflict policy
  follow `06_CLAIM_SCHEMA_AND_VERIFIER.md` exactly; risk tiers follow
  `T07_risk_taxonomy_v1.md` (R1 = PHI/polarity; R2 = dosage or chemical; R3 = cultural/timing).
- Certification policy (fail-closed): a claim certifies only if
  relation == `supported` AND polarity == affirmed AND no parse failures AND
  (R1/R2 require a resolved chemical identity). Aggregate confidence mirrors the
  runtime enum (verified / flagged-unverified / low_confidence) and the T12 branch
  order (claims with no sources → flagged).
- Evidence mode identical to T12: the record's own generating passage (source_md).

## Results vs the T12 lexical baseline (frozen splits, n=11,224)

| Split | Records | T12 verified | T12 flagged | T15 verified | T15 flagged | T15 claims | T15 certifiable claims |
|---|---|---|---|---|---|---|---|
| train | 6,805 | 6,565 | 240 | 458 | 6,347 | 17,089 | 117 |
| dev | 2,152 | 2,107 | 45 | 119 | 2,033 | 4,564 | 47 |
| test | 2,267 | 2,213 | 54 | 193 | 2,074 | 5,342 | 15 |
| **total** | **11,224** | **10,885** | **339** | **770** | **10,454** | **26,995** | **179** |

- The structured candidate is **massively more conservative**: 6.9% verified vs 97% for
  the lexical baseline. That is the intended fail-closed direction: it certifies almost
  nothing it cannot fully support; dangerous non-abstention is ~0 by construction
  (hard failures never certify — verified by the fail-closed test batch).
- Relation mix (26,995 claims): partially_supported 11,120 (41%), unsupported 8,899
  (33%), not_applicable 3,074 (11%), ambiguous 2,278 (8%), supported 1,624 (6%).
- Tier mix: R2 20,229 · R3 3,720 · R1 3,046; 23,275 claims safety-critical.

## Dominant abstention causes (T17/T18 inputs)

On non-certifiable claims (26,816): `relation != supported` (25,371) is the umbrella;
under it: **material fields absent from evidence** (10,060 — the evidence passage does
not state the same amount/interval/denominator the answer asserts), **no evidence unit
mentions the claim chemical** (8,666 — answers name products absent from the record's
own passage; recall T12's own-passage flagging note), **parse failures** (9,904 after
tightening the trigger to quantity-intent sentences), non-affirmed polarity (3,046),
chemical identity unresolved (2,250). Sample inspection (e.g. "ক্ষতিকর মাত্রা (প্রতি
পাতায় দুটি দাগ) …") confirms these are genuine coverage limits of a deterministic
Bengali parser, not code defects: the candidate abstains rather than guessing.

## Gate result

**GO offline** — all fail-closed tests pass:
- 26 structured tests: Bengali numerals; unit/dimension mismatch; denominator
  match/mismatch/absent; interval match/mismatch; PHI match/mismatch/missing;
  polarity (negated/prohibited/conditional never certify); applicability;
  source conflict → ambiguous; missing evidence (no sources branch order);
  **hard-failure batch: none of the 9 hard-failure scenarios certify**; oracle-field
  mode forces both success and failure deterministically.
- 19 T12 lexical tests still pass (no baseline drift); backend suite 11/11 (runtime
  untouched).
- Full failure log recorded (empty); inputs/outputs/code hashed in the run manifest.

## Notes for downstream

- T17 evaluates E1/E3 on these frozen predictions + T12 predictions vs expert gold
  (T10). The near-zero certification rate means the structured-vs-lexical contrast on
  dangerous non-abstention will be dominated by abstention; E2/coverage calibration
  (T18) is where the tradeoff becomes a headline number.
- Oracle-field mode exists for extraction-vs-matching decomposition at T17.
- Open items unchanged: expert sign-off (T07 §9) still pending for confirmatory runs.