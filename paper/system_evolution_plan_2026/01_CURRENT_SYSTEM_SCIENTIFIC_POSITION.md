# Current System Scientific Position

## Research objective

Test whether structured claim verification with calibrated abstention reduces unsupported high-risk Bengali agricultural advice, and whether dialect-aware normalization improves retrieval without changing safety intent.

## Primary hypothesis

A structured verifier over `crop, disease, action, chemical/intervention, amount, unit, denominator, interval, safety_condition, source_id` will detect unsupported dosage relations more accurately than lexical matching, while calibrated abstention will reduce high-risk error at an explicit coverage cost. A separate normalization study will determine whether retrieval gains preserve safety decisions across standard Bangla, regional varieties, and Banglish.

## Contribution classes

| Class | Included | Excluded from research claims |
|---|---|---|
| Research | Structured Bengali agricultural claim schema; expert-labeled verification set; verifier comparison; risk-coverage calibration; dialect/orthography retrieval and safety evaluation | Existing four-stage orchestration by itself |
| Software engineering | New verifier contract/adapter, evidence-preserving vision fallback, experiment harness, manifests, hashes | Port interfaces, SSE, JSONL logging as novelty |
| UI/product | Trace stepper, speech input, weather, helpline utility, local chat persistence | Any claim that these features improve safety or farmer outcomes without a controlled study |

## Implemented facts

| Fact | Evidence | Confidence |
|---|---|---|
| Active backend authority follows application/domain/ports/infrastructure boundaries. | `backend/app/application/**`, `domain/**`, `ports/**`, `infrastructure/**`; handoff docs | High |
| QA applies safety classification before retrieval and stops terminal categories. | `backend/app/application/qa_pipeline.py:103-119` | High |
| Runtime retrieval uses BM25 only. | `backend/app/application/container.py:33-36` | High |
| JSON and SSE share the same `QAPipeline`; SSE exposes stage and token events. | `qa_pipeline.py:81-240`; architecture contract | High |
| Sessions are in-memory with TTL; audit is local JSONL. | `container.py:37-41`; infrastructure adapters | High |
| The verifier normalizes numerals/units and checks dosage substrings against concatenated sources. It does not verify semantic claims or relations. | `backend/app/infrastructure/verification/dosage.py` | High |
| Vision applies an image-quality gate, crop classification, routed disease classification, and QA advisory. It returns no boxes. | `backend/app/application/vision_pipeline.py` | High |
| Vision fallback can assign `verified` to `solution_bn` while leaving `treatment_sources` empty. | `vision_pipeline.py:280-294` | High; must fix |
| Benchmark endpoint is a placeholder. | `backend/app/api/benchmark.py` | High |
| Model adapters are replaceable. | `backend/app/ports/llm.py`; `infrastructure/llm/factory.py` | High |

## Planned or unverified claims

| Statement | Status | Required evidence |
|---|---|---|
| Hybrid BM25+dense retrieval is active. | False for current runtime | Container wiring and reproducible retrieval evaluation |
| A local fine-tuned Gemma model is loaded and performs at a stated level. | Unverified | Model hash, serving config, test manifest, outputs, metrics |
| Dataset counts, node counts, benchmark splits, or model results from local PDFs. | TODO/unverified | Reproducible PDF extraction plus artifact reconciliation |
| Safety data exist under root `dataset_release`. | Not found | Repository-wide location audit, schema/count/hash report |
| Vision treatment content is source-verified. | False for fallback path | Stable source identifier and verifier passage through fallback |
| Frontend utilities improve usability, trust, or outcomes. | Unmeasured | Controlled human study |

## Assumptions

1. Experts can adjudicate agricultural claim relations and safety conditions.
2. Existing provenance-bearing sources can identify evidence at passage level.
3. Dialect variants can be paired by intent; native speakers must certify authenticity.
4. The study will not make causal deployment or agronomic outcome claims.
5. Compute, annotation budget, and hardware remain unknown until Stage 0.

## Success criteria

- Produce a frozen, expert-annotated claim-verification test set with agreement statistics.
- Compare lexical, LLM judge, NLI/structured, and hybrid verifiers under one split and manifest.
- Report claim and relation precision/recall/F1, unsupported high-risk claim rate, calibration, and risk-coverage curves.
- Report standard/dialect/Banglish retrieval and safety metrics for raw and normalized queries.
- Prove intent preservation and measure normalization-induced safety regressions.
- Reproduce every reported number from hashed inputs, code revision, seed, configuration, and output artifact.
- Fix the source-empty vision fallback before any end-to-end safety claim.
