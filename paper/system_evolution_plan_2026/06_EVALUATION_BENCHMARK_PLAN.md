# Evaluation and Benchmark Plan

## Evaluation-first principle

Freeze schemas, splits, baselines, metrics, and manifests before implementing the proposed runtime modules. The benchmark extends existing resources with claim relations and paired language varieties; it does not duplicate broad QA tracks.

## Workstream A: claim and dosage verification

### Unit of annotation

One generated or curated answer, its query, retrieved passages, stable source IDs, atomic claims, typed fields, support verdict, risk class, and required action.

Required fields:

`crop, disease, action, chemical/intervention, amount, unit, denominator, interval, safety_condition, source_id`

Verdicts: `entailed`, `contradicted`, `unsupported`, `not_applicable`, plus adjudication notes. Separate span correctness from relation correctness.

### Baselines

1. Existing lexical normalized dosage matcher.
2. LLM-as-judge with fixed prompt/model/version and no access to gold labels.
3. NLI or structured relation verifier selected after feasibility testing.
4. Hybrid lexical plus structured verifier with deterministic high-risk policy.
5. Oracle structured fields for upper-bound error decomposition, not a deployable method.

### Metrics

- Claim verdict macro/micro precision, recall, F1.
- Field and relation exact match; amount-unit-denominator-interval joint accuracy.
- Unsupported high-risk claim detection precision/recall.
- Answer-level unsafe pass-through rate and safe-answer false abstention rate.
- ECE, Brier score, reliability plot, selective risk, coverage, AURC, risk at fixed coverage.
- Per-category metrics for chemical, non-chemical intervention, interval, and safety condition.
- p50/p95 stage latency and failure rate on declared hardware.

## Workstream B: dialect and normalization

### Paired design

Create intent groups containing standard Bangla, supported regional varieties, and Banglish. Native speakers certify authenticity and intent equivalence. Split by source intent before any transformation.

### Conditions

- Raw query.
- Unicode/grapheme normalization only.
- Reviewed lexical/dictionary normalization.
- Learned/prompted normalization only if it passes the authenticity and safety gate.
- Optional hybrid retrieval only after dense artifacts and configuration are verified.

### Metrics

- Retrieval: nDCG@10, Recall@5/10/100, MRR, missing-judgment rate.
- Safety: macro-F1, per-class recall, false-safe rate, over-refusal rate.
- Normalization: intent-preservation rate, harmful-to-benign flip rate, benign-to-harmful flip rate, slot preservation for all structured fields.
- Disaggregate by variety, script, intent, risk, crop, and query completeness where sample support permits.

## Controlled experiments and claim map

| Experiment | Comparison | Claim tested |
|---|---|---|
| E1 | Lexical vs LLM vs structured vs hybrid | Structured relations improve verifier discrimination |
| E2 | Uncalibrated score vs calibrated policy | Calibration gives a measurable risk-coverage tradeoff |
| E3 | Remove denominator/interval/safety fields | Relation completeness matters for dosage safety |
| E4 | Raw vs normalization conditions | Normalization changes retrieval effectiveness |
| E5 | Raw vs normalized safety decisions | Retrieval gains do not imply safety preservation |
| E6 | Standard vs each verified variety/Banglish | Aggregate standard-Bangla results hide subgroup failures |
| E7 | BM25 vs dense vs hybrid, conditional | Fusion helps only if verified local assets reproduce it |
| E8 | Current vs repaired vision evidence fallback | No source-empty fallback receives a verified status |

## Ablations

- Remove each structured field; purpose: identify which relations drive high-risk detection.
- Vary extraction strategy and threshold; purpose: separate extraction from verification errors.
- Vary calibration family and development size; purpose: test threshold stability.
- Vary retrieval `k`; purpose: measure evidence recall versus distractor and latency effects.
- Remove normalization confidence gate; purpose: measure unsafe intent flips.
- Compare Unicode-only, dictionary, and learned normalization; purpose: localize gains.
- Vary training/annotation budget using nested subsets; purpose: report data efficiency without changing test data.
- Vary compute budget only through declared model/adapters; purpose: show whether the selected method needs unavailable hardware.

## Statistical validation

- Use paired bootstrap confidence intervals for paired retrieval and continuous quality differences at the intent/query level.
- Use McNemar tests for paired binary outcomes such as unsafe pass-through, correct refusal, and exact relation correctness.
- Use stratified bootstrap for risk-coverage summaries when subgroup sizes permit.
- Report effect sizes and confidence intervals; control multiple comparisons for the prespecified primary family.
- Measure human agreement with Krippendorff's alpha or an appropriate kappa for categorical labels, plus span/relation agreement. State missingness and adjudication rate.
- Freeze primary endpoints and hypotheses before test-set execution.

## Split, seed, and leakage controls

- Group splits by source document, intent family, and transformation lineage as applicable.
- Keep dialect variants of one intent in one split.
- Keep generated outputs from one source prompt together.
- Record all random seeds; run stochastic baselines with repeated declared seeds where compute permits.
- Check textual and semantic near-duplicates across splits.
- Treat test labels as read-only after freeze; log every post-freeze correction.

## Experiment manifest

Each run records: `run_id`, UTC timestamp, git commit, dirty-tree flag, task, dataset version, input SHA-256 hashes, split IDs, code/config hashes, model/provider/version, prompt hash, seed, hardware, dependency lock hash, thresholds, output paths, metric code version, failures, and parent run.

## Artifact layout to create during execution

```text
research_artifacts/
  manifests/
  datasets/{raw,interim,frozen}/
  annotations/{guidelines,pilot,adjudicated}/
  runs/<run_id>/
  reports/{data_audit,agreement,metrics,error_analysis}/
```

Do not place these artifacts in application runtime paths until the benchmark read service has a validated schema.
