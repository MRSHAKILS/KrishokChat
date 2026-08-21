# Paper Blueprint

## Working thesis

Safety-critical Bengali agricultural RAG needs typed evidence relations and calibrated abstention, while dialect normalization must be evaluated jointly for retrieval benefit and safety-intent preservation.

## Claim hierarchy

### Primary claims

1. A structured agricultural relation verifier changes unsupported high-risk claim detection relative to lexical and judge baselines.
2. Calibrated abstention exposes the error-coverage tradeoff instead of hiding it in one accuracy number.
3. Dialect and Banglish transformations change retrieval and safety behavior, and normalization can help one while harming the other.

### Secondary claims

- The modules fit an existing safety-first application architecture without adding agent orchestration.
- The repaired vision path preserves treatment evidence status.
- Expert analysis identifies failure categories specific to Bengali agricultural dosage relations.

Do not claim improved farmer outcomes, deployment impact, semantic verification by current code, active hybrid retrieval, local Gemma performance, or object detection.

## Section plan

1. **Introduction:** high-risk dosage relation failure; two research gaps; contributions.
2. **Related work:** five-group taxonomy from `02_LANDSCAPE_GAPS_COMPETITIVE.md`.
3. **Current system and problem formulation:** evidence-safe current flow and constraints.
4. **ClaimSafe-BN:** schema, extraction, verification, aggregation, calibration.
5. **DialectSafe-RAG:** paired construction, normalization conditions, threat model.
6. **Benchmark and protocol:** annotation, splits, baselines, metrics, statistics, reproducibility.
7. **Results:** verifier, risk-coverage, dialect retrieval, safety preservation, latency.
8. **Human evaluation:** expert study; optional farmer study clearly separated.
9. **Error analysis:** extraction, relation, evidence, normalization, safety flips, subgroup failures.
10. **Limitations and ethics:** expert subjectivity, dialect coverage, corpus bounds, helpline limits, no causal claims.
11. **Conclusion:** only claims established by frozen results.

## Planned figures and tables

- Figure 1: current versus proposed bounded pipeline.
- Figure 2: structured claim and evidence relation example.
- Figure 3: risk-coverage and calibration curves.
- Figure 4: paired dialect/normalization evaluation design.
- Table 1: closest-system competitive matrix.
- Table 2: dataset composition after Stage 0 verification.
- Table 3: verifier baselines and primary metrics.
- Table 4: field ablations.
- Table 5: retrieval and safety by variety/condition.
- Table 6: human agreement and expert evaluation.
- Table 7: latency, compute, failures, and coverage.

## Evidence gates

| Gate | Requirement | Blocks |
|---|---|---|
| G0 | PDF and artifact claim ledger complete | Any team-paper numerical claim |
| G1 | Dataset locations/counts/hashes reconciled | Dataset composition table |
| G2 | Schema and primary endpoints frozen | Annotation and model comparison |
| G3 | Expert pilot and agreement reviewed | Gold-label claim |
| G4 | Baselines run from manifests | Improvement claim |
| G5 | Threshold frozen on development data | Selective-answering claim |
| G6 | Native authenticity/intent audit complete | Dialect and normalization claim |
| G7 | Paired statistics and error analysis complete | Comparative claim |
| G8 | Source-empty vision status fixed | End-to-end evidence-safety claim |
| G9 | Independent reproduction complete | Submission/release |

## Citation policy

Use stable URLs already recorded in the literature package, then revalidate them before submission. Cite the two authoritative team papers by their local filenames until bibliographic metadata are extracted and reconciled. Keep every PDF-derived number as `TODO/unverified` until G0 and G1 pass.
