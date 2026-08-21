# T07 Label Manual (Outline) — v1

**Date:** 2026-08-12
**Status:** FROZEN DRAFT — expert adoption pending (protocol §9)
**Protocol:** `T07_protocol_v1.md`

## Purpose

Label manual for domain-expert annotation of atomic claims, evidence relations, safety criticality, applicability, and source conflicts. Gold = independent expert labels, adjudicated. No LLM judge is gold.

## 1. Annotator Setup and Ownership

- Each label record: `annotator_id`, guideline_version, timestamp, raw_label, optional confidence/notes, adjudication lineage. Never replace raw labels with consensus only.
- Two independent expert annotators per item (pilot in T08), adjudication by a third/lead expert.
- Blinded setup: annotators see query, answer, retrieved evidence spans with stable IDs, claim segmentation. No model predictions shown during labeling.

## 2. Task Flow per Item

1. Read query, answer, and retrieved spans (only spans with stable `source_id`).
2. Split compound advice into atomic claims (one claim per action+target+quantity unit; never merge).
3. For each atomic claim, fill schema fields per `06_CLAIM_SCHEMA_AND_VERIFIER.md`.
4. Assign relation (frozen enum) to the whole atomic claim vs cited evidence.
5. Assign `safety_critical` boolean + reason.
6. Record applicability conditions and conflicts with conflicting source IDs.
7. Annotate missing values exactly (`null` vs `unknown`).

## 3. Field-by-Field Guidance (executive summary; full table in schema doc)

- `crop`, `disease/pest`: use canonical terms; `unknown` if text unresolved; `null` only if crop-independent.
- `action`: apply/avoid/mix/spray/irrigate/wait/monitor/remove/refer/other-reviewed.
- `chemical/intervention`: canonical entity; distinguish product name vs active ingredient unless reviewed dictionary links them for the formulation+jurisdiction.
- `amount/unit/denominator`: normalize digits, never infer denominator; bind ratio (2 ml ≠ 2 ml/L ≠ 2 ml/10 L).
- `interval_frequency`: any stated repetition, schedule, max count.
- `phi_safety_condition`: PHI, PPE, weather, water-body, livestock/human, re-entry, legal/restriction, growth-stage.
- `polarity`: affirmed/negated/conditional/prohibited; never default to affirmed.
- `applicability`: crop, target, stage, geography/regulation, formulation, environment qualifiers.
- `evidence_span`: source-relative character offsets + quoted text + source-content hash; required for supported/contradicted/partially_supported.

## 4. Relation Decision Rules (frozen)

| Relation | When |
|---|---|
| supported | evidence supports every material field + applicability; no material conflict |
| contradicted | explicit conflict on ≥1 material field/polarity/prohibition/applicability |
| partially_supported | supports part, omits/fails ≥1 material component (safety-critical missing comp → not certifiable) |
| unsupported | no cited evidence supports the material claim; only unrelated spans retrieved |
| ambiguous | parsing/entity/source-conflict prevents unique decision → abstain |
| not_applicable | test does not apply to claim type (≠ supported) |

## 5. Missing-Value Conventions

- `null` = true absence / non-applicability per field rule.
- `unknown` = present but unresolved.
- Safety-critical blocks: missing source_id, span, chem identity, amount-unit, required denominator, material interval, PHI, polarity, applicability → abstain.

## 6. Source Conflict Handling

- Record all conflicting source IDs + spans + dates + conflict field.
- Authoritative spans conflict on material safety field & applicability can't resolve → `ambiguous` → abstain.
- Span outside claim crop/formulation/geography/regulation → `not_applicable` (never average).
- No verifier-invented source ranking; authority/recency rules require expert sign-off (open item §7).

## 7. Safety-Critical Criteria

Claim is safety-critical when error could change: chemical/intervention or banned status; formulation/concentration; amount/unit/denominator/mixture/max; interval/count; PHI/re-entry; human/animal/pollinator/water/PPE/weather/disposal; crop/target/stage/jurisdiction applicability; polarity apply-vs-don't; poisoning/overdose/harm intent.

## 8. Agreement and Adjudication

- Pilot (T08): validate every relation, missing-value state, conflict, safety criterion.
- Agreement target: Krippendorff alpha ≥ 0.70 (or approved kappa) on primary relation labels; span/field agreement reported.
- Adjudication: lead expert resolves; records adjudication lineage; adjudication rate reported.
- Max one guideline revision if agreement gate fails; otherwise STOP.
- Independent experts only; never LLM judgment as gold.

## 9. Label Output Schema

Stable IDs for: `claim_id`, `annotator_id`, `item_id`, `run_id`, `schema_version`, `guideline_version`. Raw audit retained (original/normalized text, normalization diffs, parser traces, raw model outputs, safety decisions, test logs) per `AGENTS.md` rules.

## 10. Open Items for Expert Adoption

1. Confirm field-level priority and rule edge cases with one worked example per relation.
2. Confirm safety-critical examples corpus (e.g., banned/restricted chemicals list).
3. Confirm agreement threshold.
4. Confirm source authority/recency rules.