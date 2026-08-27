# Revision and submission suggestions

## Blocking evidence work

1. **Reconcile E14 before submission.** The current result YAML reports 91.4% cache versus 82.0% cloud at 15% packet loss and 58.1% versus 12.8% at 30% loss. The frozen ledger and summary contain a conflicting 80.3%/58.7% pair. Regenerate one authoritative artifact, update the claim ledger, registry, summary, manuscript, and Figure 4 together.
2. **Reconcile E20 units and arithmetic.** The metrics block reports 2.86 versus 0.69 Crore BDT and 2.17 Crore savings; older notes report 28.57 versus 2.17 Crore and 22.8 Crore savings. Confirm the source price, BDT/USD conversion, annual workload, channel mix, and whether hosting is included. Until then, call E20 a scenario projection and omit the savings headline from the abstract.
3. **Reconcile E25 ledger values.** The result YAML/raw output supports 96.4% crop, 78.4% pest, 100.0% intent, and 78.4% joint exact match. The claim ledger/summary contain different component values. Amend the ledger only after the result owner accepts the raw artifact.
4. **Resolve acceptance status.** E14/E15/E17–E25 result YAMLs still show `accepted_by: PENDING`; E26 is `done_unverified`; E16 is planned/blocked. The paper must not describe the entire battery as author-accepted or fully validated.
5. **Fix E23 schema wording.** Keep tamper detection, delta size, and zero surviving deprecated records. Remove or repair the contradictory `invalidation_propagation_completeness_pct: 0.0` field.

## Experiments that would materially strengthen a future version

- A naturally paired image–query benchmark with low-light, ambiguous, unseen-crop, and out-of-distribution cases, plus independent agronomic correctness labels.
- A per-tier outcome matrix separating correct answer, safe refusal, incorrect answer, and unsafe acceptance.
- A live-lane E26 run with real generation, chunk provenance, chemical-claim stripping, and verifier checks.
- Physical low-end Android battery/thermal profiling (E16), using a named device and repeatable workload.
- Carrier-level SMS tests covering GSM encoding, delivery failure, retry, and gateway behavior.
- Full fact-pack invalidation and rollback tests, rather than the nine-fact E23 graph alone.
- Sensitivity analysis for queries/farmer/year, SMS share, LLM price, hosting, device acquisition, support, maintenance, and escalation cost.
- A pre-registered expert or field-like study of referral workload and outcome measures. Do not use this to claim farmer benefit until the study is complete.

## Cover-letter positioning

> This manuscript evaluates a bounded edge–cloud architecture for Bengali agricultural advisory under low-connectivity constraints. Its contribution is an evidence-controlled combination of metadata-gated deterministic routing, typed fail-closed certification, offline cache behavior, and GSM message-field preservation. The study reports separate measurements, simulations, and scenario projections rather than treating a zero observed failure count as a universal safety guarantee.

## Figure decision

No new physical-device or live-carrier figure should be generated: those experiments have not been run. The current five conceptual/data-driven figures are sufficient after E14 reconciliation and replacement of any interpolated or invented chart values.
