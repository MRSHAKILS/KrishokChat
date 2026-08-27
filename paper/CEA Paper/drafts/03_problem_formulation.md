# Section 03: Problem Formulation & Mathematical Framework (Draft Skeleton)

## 3.1 Advisory State Formalization
- State tuple: x = <q_t (text query), I_v (image), M (metadata: time, region, soil), H (history)>.
- Action space A = {DETERMINISTIC_RESOLVE, GROUNDED_GENERATE, CONVERSATIONAL_CLARIFY, SAFE_ABSTAIN, EXPERT_ESCALATE, POLICY_BLOCK}.

## 3.2 The Critical Agricultural Tuple (11-Slot Contract)
- Tuple C = <crop, pathogen, stage, active, formulation, dose_min, dose_max, unit, volume, interval, PHI>.
- Definitions and domain constraints for each slot.

## 3.3 Evidence Authority & Mathematical Certification Rule
- Authoritative predicate: ValidSource(e) AND Current(e, M_t) AND Approved(e).
- Certification rule: Certify(C) = 1 iff exists authoritative e* that jointly entails all 11 slots of C with completeness and calibrated confidence g(x) >= theta*.

## 3.4 Outcome Variables & Primary Endpoints
- Critical Unsafe Acceptance Rate (CUAR) — Primary safety endpoint.
- Certified Advisory Correctness (CAC) — Primary agricultural endpoint.
- Advisory Coverage (kappa) — Operational utility.
- Appropriate Abstention Rate (AAR) — Fail-closed precision.
- Reference Table 1 (System reliability requirements and fail-closed responses).
