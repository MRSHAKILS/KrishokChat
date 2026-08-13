# T12 Lexical Baseline — Reproduction Report v1

**Task:** P2 T12 (lexical baseline) — offline reproduction of the CURRENT verifier.
**Status:** COMPLETE — fixture parity passed; baseline frozen for T15 comparison.
**Date:** 2026-08-13 · **Run id:** `T12-20260812T200711Z`
**Manifest:** `research_artifacts/manifests/T12_baseline_run_manifest_v1.json`
**Authority:** `11_FINAL_IMPLEMENTATION_SPEC.md` row T12; scoped AGENTS.md rule 12
("reproduce the current lexical verifier without silent fixes").

## Method (faithfulness)

- The runner **imports the exact runtime module**
  `backend/app/infrastructure/verification/dosage.py` (no copy, no reimplementation):
  verdicts come from the real `DosageVerifier.verify()`; per-claim membership reuses
  the module's own `_normalize`/`_claims`. Drift is impossible by construction.
- Evidence mode (scoping decision, recorded in the manifest): each frozen record is
  verified against its **own generating source passage** (`source_md`, full content)
  as `content_bn`. This isolates generation+verification from retrieval (E4 handles
  retrieval separately). Unreachable passages → no sources → runtime no-source branch.
- Deterministic: verifier is pure/deterministic; record order = frozen split order.

## Results (frozen T09 splits, 11,224 records, 0 failures)

| Split | Records | Verified | Flagged-unverified | Low-confidence | With claims | Evidence attached |
|---|---|---|---|---|---|---|
| train | 6,805 | 6,565 | 240 | 0 | 644 | 6,805 |
| dev | 2,152 | 2,107 | 45 | 0 | 136 | 2,152 |
| test | 2,267 | 2,213 | 54 | 0 | 214 | 2,267 |
| **total** | **11,224** | **10,885** | **339** | **0** | **994** | **11,224** |

- All 11,224 source passages reachable and hashed; `runs/T12_failure_log_v1.jsonl` is
  empty (0 entries).
- **Flagged rate ≈ 3.0%** of records; **only ≈ 8.9% of answers contain
  regex-extractable dosage claims** (amount+unit patterns) — the lexical matcher's
  surface is narrow by design (captured behavior, not a defect to fix).

## Claim-level statistics

- 2,502 total claim occurrences from 77 distinct claim strings across all records.
- 1,521 in evidence (60.8%), 981 not in evidence (39.2%).
- Top claim strings: `2 g` (189), `3 g` (175), `1 kg` (159), `1 ml` (156),
  `100 kg` (91), `5 g` (89).

## Inspected flag example (train, cell `0b7fb62e02e4_pest`)

- Q: "গাজর খেতাত পোকা দমন, কিলা করুম?" — A contains dosage `5 ml`; the record's own
  passage does not contain `5 ml` (normalized), so the claim is flagged.
- Interpretation for T17/T10: answers can draw on passages beyond the record's own
  `source_md`; flagging against the own-passage is the conservative reading. Whether
  such flags are true ungroundedness is exactly what expert gold (T10) adjudicates.
  No baseline verdict is treated as ground truth.

## Captured behaviors pinned (unit tests)

`research_artifacts/tests/test_lexical_baseline.py` — 19 tests, all pass:

1. **Parity block** — byte-identical to `backend/tests/test_pipeline.py::VerifierTests`
   (Bengali numeral match; ungrounded dosage flag). Backend suite re-run:
   `VerifierTests + PipelineTests` 6/6 pass (runtime unchanged).
2. **Bengali digit fixtures** — all ten digits, decimal, comma-decimal (`,`→`.`).
3. **Bengali unit aliases** — মিলিলিটার/মিলি/মিলিগ্রাম/গ্রাম/কেজি/লিটার, case-insensitive.
4. **Fractions** — আধা/অর্ধেক + চামচ/কাপ extract and match; mismatch flags.
5. **Branch order (captured)** — unverified claims checked BEFORE the no-source
   branch: claims with no sources → `flagged-unverified`; only no-claims+no-sources
   reaches `low_confidence`.
6. **Boundaries** — bare amounts without a unit are not claims; comma-separated
   quantities normalize to dot and match.

## Outputs (all hashed in the run manifest)

| File | Records | SHA-256 (first 12) |
|---|---|---|
| `runs/T12_lexical_baseline_predictions_v1.jsonl` | 11,224 | see manifest |
| `runs/T12_failure_log_v1.jsonl` | 0 | see manifest |
| `manifests/T12_baseline_run_manifest_v1.json` | — | see manifest |

## Gate result

**GO** — fixture parity passes (19/19 research tests; 6/6 captured runtime parity);
full failure log recorded (empty); inputs/outputs hashed; runtime module untouched.
The baseline is now frozen for the T15 structured-verifier comparison. No silent
improvements were made to the baseline during reproduction.