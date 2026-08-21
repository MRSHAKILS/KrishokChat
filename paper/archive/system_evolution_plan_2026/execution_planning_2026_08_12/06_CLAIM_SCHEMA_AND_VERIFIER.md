# Claim Schema and Verifier Contract

## Unit of Analysis

One item contains a query, answer, retrieved passages, stable evidence identifiers, one or more atomic claims, expert relation labels, safety criticality, and a release action. Split compound advice before labeling. One atomic claim may reference multiple evidence spans when support is distributed.

## Frozen Claim Schema

| Field | Type | Definition | Missing-value rule |
|---|---|---|---|
| `claim_id` | stable string | Dataset-version-scoped atomic claim ID. | Never missing. |
| `crop` | canonical term/list | Crop or crop group to which advice applies. | `null` only when evidence and claim are crop-independent; `unknown` when text is unresolved. |
| `disease/pest` | canonical term/list | Disease, pest, symptom complex, or target condition. | `null` when not applicable; `unknown` when unresolved. |
| `action` | enum plus span | Apply, avoid, mix, spray, irrigate, wait, monitor, remove, refer, or other reviewed action. | `unknown` if asserted but extraction fails. |
| `chemical/intervention` | canonical term/list | Active ingredient, product/formulation name, biological, cultural, mechanical, or other intervention. | `null` only for claims with no intervention; `unknown` if unresolved. |
| `formulation` | normalized string | Concentration or formulation, such as WP/EC/SC and percentage where stated. | `null` when absent and not required; `unknown` if illegible/ambiguous. |
| `amount` | decimal/range/list | Numeric quantity after Bengali/ASCII digit normalization. Preserve original span. | `null` when evidence gives no amount; never infer. |
| `unit` | canonical unit | Unit attached to amount. | `null` only with no amount; `unknown` if amount exists but unit is unresolved. |
| `denominator` | structured quantity | Per water volume, land area, seed mass, plant, container, or other base. | `null` when genuinely unnecessary; `unknown` when required but unresolved. |
| `interval/frequency` | structured duration/count | Application interval, repetitions, maximum count, or timing schedule. | `null` when absent and not required; `unknown` when text implies timing but cannot resolve it. |
| `PHI/safety condition` | structured list | Pre-harvest interval (PHI), PPE, weather, water-body, livestock/human exposure, re-entry, legal/restriction, growth-stage, or escalation condition. | Empty list means no stated condition; `unknown` means a condition exists but cannot be parsed. |
| `source_id` | stable string/list | Immutable ID for the source unit or passage container. | Never missing for certifiable claims. Missing forces abstention. |
| `evidence_span` | exact offsets plus text/hash | Source-relative character offsets, quoted text, and source-content hash. | Never missing for `supported`, `contradicted`, or `partially_supported`. Missing forces `unsupported` or `ambiguous`. |
| `polarity` | enum | `affirmed`, `negated`, `conditional`, or `prohibited`. | `unknown` if unresolved; no default to affirmed. |
| `applicability` | structured predicate | Conditions under which evidence applies: crop, target, stage, geography/regulation, formulation, environment, and other qualifiers. | Empty only for unconditional evidence; `unknown` if conditions cannot be resolved. |
| `uncertainty` | structured record | Source uncertainty, extraction confidence, ambiguity reason, and annotation notes. | Empty reasons only when no uncertainty was identified; runtime numeric score is optional and never gold. |
| `relation` | frozen enum | Expert relation between the whole atomic claim and cited evidence. | Never missing in adjudicated data. |
| `safety_critical` | boolean plus reason | Whether an error could alter chemical identity, dose, exposure, legal use, timing, PHI, or harmful action. | Never missing. |

`interval/frequency` and `PHI/safety condition` are serialized with safe machine keys such as `interval_frequency` and `phi_safety_condition`; manuscripts retain the labels above.

## Frozen Relation Types

| Relation | Decision rule |
|---|---|
| `supported` | Evidence supports every material field and applicability condition; no material conflict exists. |
| `contradicted` | Evidence explicitly conflicts with at least one material field, polarity, prohibition, or applicability condition. |
| `partially_supported` | Evidence supports part of the claim but omits or fails to support at least one material component. A safety-critical missing component blocks certification. |
| `unsupported` | No cited evidence supports the material claim, or only unrelated evidence was retrieved. |
| `ambiguous` | Evidence, parsing, entity resolution, or source conflict prevents a unique relation decision. Runtime action is abstain. |
| `not_applicable` | The field or relation test does not apply to the claim type. This is not equivalent to supported. |

## Missing Values

- Use JSON `null` only for true absence or non-applicability as defined per field.
- Use `unknown` for present but unresolved information.
- Do not encode missing numeric values as `0`, empty strings, or inferred defaults.
- Any missing `source_id`, evidence span, chemical identity, amount-attached unit, required denominator, material interval, PHI, polarity, or applicability condition blocks certification for a safety-critical claim.
- Preserve original text and offsets beside normalized values.

## Normalization and Units

1. Normalize Unicode and grapheme variants without changing token order or polarity.
2. Convert Bengali digits to ASCII for comparison while preserving the original span.
3. Resolve reviewed Bengali/English/Banglish unit aliases to canonical UCUM-like internal tokens where feasible.
4. Parse decimal separators, ranges, fractions, multiplication, area/volume denominators, percentages, and formulation strengths explicitly.
5. Convert units only through a frozen dimensional table. Never compare dimensionally incompatible quantities.
6. Compare ratios only after binding amount to denominator and formulation. `2 ml`, `2 ml/L`, and `2 ml/10 L` are different claims.
7. Do not infer a denominator from common agronomic practice or model memory.
8. Treat product names and active ingredients as distinct entities unless the reviewed dictionary links them for the stated formulation and jurisdiction.
9. Preserve negation, prohibition, maximum/minimum qualifiers, interval boundaries, growth stage, and PHI during normalization.
10. Emit explicit parser failures. Never silently discard unparsed safety-bearing text.

## Source Conflict Policy

- Match claims against every retrieved candidate span with stable IDs.
- If authoritative spans conflict on a material safety field and applicability cannot resolve the conflict, label `ambiguous` and abstain.
- If one source is outside the claim's crop, formulation, geography, date, or regulatory scope, mark that span `not_applicable`; do not average values.
- Record all conflicting source IDs, spans, dates where available, and the conflict field.
- Source authority and recency rules require expert approval in T07. The verifier must not invent a ranking.

## Safety-Critical Criteria

A claim is safety-critical when an error could change any of the following: allowed chemical or intervention; banned/restricted status; formulation or concentration; amount, unit, denominator, mixture ratio, or maximum; interval/frequency or application count; PHI or re-entry; human, animal, pollinator, water, PPE, weather, or disposal condition; crop, disease/pest, stage, or jurisdiction applicability; polarity such as apply versus do not apply; poisoning, overdose, or intentional harm response.

For safety-critical claims, only `supported` with all required fields and evidence may receive certification. All other relations abstain or trigger the existing safe referral path.

## Selected Verifier

**Primary hybrid verifier:** deterministic parser/normalizer plus structured relation matcher and deterministic safety policy.

The term hybrid refers to two verifier components, not hybrid retrieval. The runtime retriever remains BM25.

### Processing Contract

1. Split the answer into atomic candidate claims.
2. Parse claim fields deterministically and retain original spans.
3. Parse each retrieved evidence span through the same canonicalization tables.
4. Match entities, quantities, units, denominators, intervals, PHI, polarity, and applicability.
5. Assign the frozen relation with a trace of matched and conflicting fields.
6. Aggregate claim relations into answer certification through the fail-closed safety policy.
7. Produce a score only from explicit extraction and match features; fit any calibrator on development labels.

### Optional NLI Comparison

A frozen NLI model may run offline as a comparison or as a bounded resolver for cases already marked `ambiguous`. It cannot override a deterministic contradiction, missing evidence, dimensional mismatch, PHI conflict, or safety policy. It enters runtime only after E8 shows a prespecified gain under latency, reproducibility, and dangerous-pass-through gates.

### Gold Standard

Independent experts label spans, fields, relations, applicability, conflicts, and safety criticality. Adjudication resolves disagreements. No LLM judge serves as gold. A fixed LLM judge may appear as a secondary baseline with prompt, model, version, raw response, and failure logs.

## Rationale

- **Latency:** deterministic parsing and matching avoid another mandatory model call and support bounded p95 latency.
- **Reproducibility:** frozen dictionaries, unit tables, parser versions, evidence hashes, and rule traces regenerate decisions locally.
- **Safety:** explicit dimensions, polarity, applicability, source conflict, and missingness fail closed instead of treating semantic similarity as support.
- **Auditability:** every verdict identifies the claim fields, source IDs, spans, rules, and unresolved conditions that produced it.
