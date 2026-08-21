# Skeptical Reviewer Attack

| Attack | Why it could succeed | Required mitigation |
|---|---|---|
| “This is a RAG wrapper with extra prompts.” | Current architecture uses familiar stages. | Center typed relation labels, calibrated decisions, paired dialect evaluation, and component experiments. Do not sell orchestration. |
| “The verifier only matches numbers.” | Current code does exactly that. | Name it lexical baseline; show extraction and relation errors; compare four methods. |
| “LLM judges grade their own outputs.” | Bengali judge reliability is contested in the local review. | Use independent experts as gold; report agreement; keep judge as baseline. |
| “Calibration is tuned on the test set.” | Small safety sets invite threshold leakage. | Freeze grouped splits and threshold on development only; hash the policy before test. |
| “Dialect data are synthetic caricatures.” | Word substitution does not establish authenticity. | Require native review, rejection logs, multiple reviewers where feasible, and intent/slot preservation. |
| “Normalization improves retrieval by changing meaning.” | Harmful intent or dosage slots can disappear. | Audit raw and normalized forms; measure harmful-to-benign flips; fail closed on conflict. |
| “The benchmark duplicates the team’s prior resources.” | Existing PDFs appear to include QA, safety, and retrieval resources. | Reconcile first; add only claim relations, evidence labels, paired variants, and normalization outcomes. |
| “The team-paper numbers are irreproducible.” | PDFs and literature summaries are not stable eval artifacts. | Keep numbers TODO until extraction, hashes, and artifact reconciliation; publish the ledger. |
| “Hybrid retrieval is claimed but the system uses BM25.” | Documentation and runtime differ. | State BM25-only current runtime; treat hybrid as conditional experiment. |
| “Local Gemma claims are marketing.” | Adapter construction proves no model availability or quality. | Report only hashed model/config/run evidence or omit the claim. |
| “Vision outputs verified advice without evidence.” | Current fallback assigns verified with empty sources. | Repair and regression-test before end-to-end claims; disclose the prior defect. |
| “Vision is object detection in name only.” | Routes may say detect, artifacts classify. | State classification, return no boxes, omit localization metrics. |
| “Abstention inflates safety by refusing everything.” | Safety metrics alone reward low coverage. | Report coverage, selective risk, false abstention, utility, and fixed-coverage comparisons. |
| “Expert labels are subjective.” | Agricultural advice depends on context and source interpretation. | Publish guidelines, agreement, adjudication rate, ambiguity labels, and source constraints. |
| “Small farmer study cannot support impact.” | Eight weeks cannot establish outcomes. | Limit claims to comprehension, calibrated trust, and referral recall; no causal agronomic claims. |
| “The national helpline referral is unsafe or misleading.” | Availability and capacity can vary. | Verify official details at study time; state limits; never promise service. |
| “Multiple comparisons produce selective wins.” | Many varieties, fields, and metrics exist. | Prespecify primary endpoints, control the primary test family, report all conditions. |
| “Dataset leakage inflates results.” | Parallel variants and shared documents create leakage. | Group by intent/source lineage, deduplicate, freeze test labels, log corrections. |
| “The proposed system is too complex for a small prototype.” | Two models plus normalization could increase latency and failures. | Prefer deterministic/compact components, report p50/p95, preserve fail-closed behavior, integrate only passing modules. |
| “No real novelty remains if one module fails.” | The paper bundles two hypotheses. | Preserve independent workstreams; publish negative normalization or verifier results honestly; narrow the thesis to the supported claim. |

## Red-team acceptance test

Before submission, assign an independent reviewer the evidence ledger, frozen manuscript, and artifact bundle. Ask them to trace every result to a manifest, reproduce primary tables, find any active/planned wording error, and attempt safety-intent flips through normalization. Any unresolved high-severity finding blocks submission.
