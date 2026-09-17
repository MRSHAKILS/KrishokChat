# Beat F Experiment Plan — Two Walls and a Mouthpiece

**Status:** upstream measured; downstream implemented, catch-rate pending  
**Priority:** P0 catch-rate study (decides whether the verifier gets numbers); UI-wiring check P1  
**Principle:** a wall without a measured catch-rate is a mechanism, not a result.

## 1. Research questions

- **RQ-F1:** Does the upstream gate stop live attacks vs an unconstrained model? (measured — E03)
- **RQ-F2:** Does the downstream verifier catch mutated dosage claims in generated answers? (pending — P0 study)
- **RQ-F3:** What does verification cost in latency and false positives? (latency measured; FP pending)
- **RQ-F4:** Does the farmer actually see flags/badges/sanitized text? (UI wiring check pending)

## 2. What is already measured (keep)

| Result | Artifact | Status |
|---|---|---|
| BAA 0.95% [0.26, 3.41] vs unconstrained 36.19% [29.99, 42.88], 7×30×2 arms | E03 `results.json` | MEASURED |
| Bangla native residual 6.67% [1.85, 21.32] | same | MEASURED (report as residual risk) |
| Verifier p50 ~4.82ms / p95 ~11.2ms | E01 sweep | MEASURED |
| Oracle floor 4.05–7.00%, SFT collapse 0.31% | 2606 (companion) | MEASURED (motivation) |

## 3. P0: verifier catch-rate study (real answers, real API)

**Design (real-data per doctrine):**
1. Run the frozen T3 pipeline with LIVE generation over ≥200 Treatment QA items (institutional ground truth) → **real generated answers with real retrieved sources**. API spend approved. Stub-LLM outputs are banned as catch-rate inputs.
2. Generate mutated copies of the real answers, one field each: dose ×2, dose ÷2, unit swap (ml↔g), PHI swap (14→3), chemical swap (same-class), interval swap. Keep one clean copy per item as control (≥200 controls).
3. Run `HardenedDosageVerifier.verify()` on clean + mutated answers against the original sources.
4. Report: catch-rate per mutation type, false-positive rate on clean answers, per-claim verdict confusion (grounded vs unsupported vs no_dosage), latency p50/p95.
5. Manual review of 50 catches + 50 misses to characterize failure modes (e.g., undetected chemical synonyms, unit-alias gaps).

**Acceptance:** paper may report "catches X% of single-field dosage mutations at Y% false positives" with the mutation table. If catch-rate is weak on some mutation type, report it — it scopes the "dosage-claim" label honestly.

## 4. P1: UI-wiring check (code inspection, 1 hour)

Confirm in `frontend/src/components/`: does the Why-panel render per-claim verdicts + flags + sanitized answer + tier badge for a flagged response? Record file:line pointers. If any link is missing, the paper claims "verifier flags available via API/trace" — never "farmer sees" what isn't wired.

## 5. P1: end-to-end unsafe-acceptance probe (small)

Frozen 100 Treatment QA items through the full pipeline (gate → retrieval → generation → verifier). Report: certified-correct, flagged-and-dropped, abstained, escalated, and any dangerous acceptance with denominator. This is the only number that speaks to "is the advice safe," and the paper needs it or must explicitly mark it unmeasured.

## 6. P2 (optional): E03 expansion beyond n=30/family

Current CIs are wide but honest. Expand only if API budget allows and a tighter Bangla-native interval is worth it. Default: keep n=30, report CIs.

## 7. Gates

- **Gate 0:** freeze mutation set + source set + verifier config (dose-reference version). Hash everything.
- **Gate 1:** run catch-rate study; no verifier tuning between clean and mutated arms.
- **Gate 2:** UI-wiring check recorded with pointers.
- **Gate 3:** paper decision — verifier gets numbers only if catch-rate + FP are measured; else "implemented mechanism, evaluation pending."

## 8. Status marks (for later agents)

- [x] Upstream wall measured (E03, both arms, CIs)
- [x] Verifier latency measured (E01)
- [x] Oracle-floor + SFT-collapse motivation (2606)
- [x] Scope limit recorded (dosage claims, not 11-slot)
- [ ] P0: catch-rate study (~200 items × mutations)
- [ ] P0: false-positive rate on clean answers
- [ ] P1: UI-wiring check with file:line pointers
- [ ] P1: end-to-end 100-item unsafe-acceptance probe
- [ ] P2: E03 expansion (optional)
- [ ] Results to `plans/experiments/results/`, old artifacts untouched
