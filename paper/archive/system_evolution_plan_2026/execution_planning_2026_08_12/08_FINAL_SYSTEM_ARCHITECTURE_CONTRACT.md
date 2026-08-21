# Final System Architecture Contract

## Non-Negotiable Boundary

Preserve the active dependency direction:

```text
HTTP routers
  -> application use cases
    -> ports
      -> infrastructure adapters
```

Preserve one FastAPI process, one `QAPipeline`, safety before retrieval, BM25 retrieval, shared JSON/SSE execution, local audit, and fail-closed errors. Do not add an agent, planner, critic, supervisor, graph retriever, service, queue, web fallback, or second active pipeline.

## Current QA Contract

| Stage | Inputs | Outputs | Dependencies | Failure action | Latency evidence | Logging | Reproducibility | Safety invariant |
|---|---|---|---|---|---|---|---|---|
| Safety | Query and optional crop/disease context | Category, confidence, terminal flag, canned response | Deterministic policy plus classifier port | Provider/parse/low-confidence failure becomes terminal `low_confidence` | Measure p50/p95; no performance claim yet | Category, action, model, error, timestamp | Record code/config/model and rule hashes | Runs before retrieval; non-safe categories stop. |
| Retrieval | Safe query and requested `k` | BM25-ranked passages with stable IDs | Existing `Retriever` port and `BM25Retriever` | Empty or error returns controlled referral; no ungrounded generation | Measure p50/p95 on declared hardware | Source IDs and retrieval failure | Hash BM25 pickle, corpus, tokenizer/config, query condition | BM25 only for adjudicated runtime. |
| Generation | Query and retrieved passages | Bengali answer text | Existing generation-model port | Controlled referral and audit | Measure p50/p95; local Gemma performance unverified | Model choice, error, channel | Record provider/model/version, prompt hash, source IDs | Generator cannot add permission to answer without evidence. |
| Current verifier | Answer and retrieved sources | Categorical verification confidence | Existing verifier port; lexical `DosageVerifier` | Error becomes `flagged-unverified` | Measure as baseline | Verifier flag and source IDs | Capture source revision and fixtures | Treat as lexical baseline, not semantic certification. |
| Response/audit | Pipeline result | Stable JSON or SSE final response | Existing serializers and local JSONL sink | Audit failure must be explicit; transport does not rerun generation | JSON/SSE parity already evidenced | Exactly one local outcome record | Preserve request/run IDs and config where research mode applies | No external telemetry. |

## Proposed Verifier Adapter Contract

### Inputs

- answer text and query;
- retrieved passages containing stable `source_id`, source hash, and exact text;
- optional crop/disease context that cannot override safety;
- frozen claim schema, entity/unit dictionaries, applicability rules, and calibration artifact;
- run context for audit and manifest IDs.

### Outputs

- atomic claims with original spans and normalized fields;
- evidence links with offsets and hashes;
- one frozen relation per claim;
- field-level match, conflict, missingness, and parser traces;
- `safety_critical` and reason;
- calibrated score where applicable;
- answer action: `certify`, `abstain`, `blocked`, or `out_of_scope`;
- latency and explicit error state.

### Dependencies

- Extend the existing domain contracts and `Verifier` port only as needed.
- Implement the deterministic parser/normalizer and structured matcher under `backend/app/infrastructure/verification/`.
- Keep policy orchestration in `backend/app/application/qa_pipeline.py` or a small application service called by it.
- Wire one selected verifier in `backend/app/application/container.py`.
- Do not place functional logic in legacy `backend/app/agents/` or `services/advisory/`.

### Failure and Safety

- Missing source IDs, evidence spans, required fields, calibration artifact, or parser resources forces abstention.
- Contradiction, dimensional mismatch, unresolved source conflict, or safety-critical ambiguity forces abstention or existing referral.
- Optional NLI timeout/error returns the deterministic result; it cannot convert a hard failure into certification.
- No LLM judge participates in runtime certification or gold labeling.

### Latency

Record extraction, evidence parsing, matching, optional NLI, calibration, and total verifier p50/p95. T07 freezes the budget before integration. A candidate that exceeds the budget remains offline regardless of accuracy.

### Logging

Extend local audit with schema version, verifier version, calibrator/threshold ID, claim IDs, relations, source IDs, span hashes, action, hard-gate reasons, and stage latency. Avoid raw private user text in release artifacts; research sets use approved, versioned records.

### Reproducibility

Pin dictionaries, unit tables, schema, parser code, calibration parameters, evidence corpus, BM25 artifacts, model comparison artifacts, dependencies, hardware, seed, and code revision. Every run emits raw outputs and a manifest. The benchmark endpoint is not the evidence source.

## Normalization Evaluation Contract

Normalization remains outside the production query path until E4/E5 pass. The offline harness accepts paired `intent_id`, raw query, condition, frozen slots, and dictionary/model version. It emits normalized query, edit trace, safety decisions before and after, retrieval rankings, verifier output, and failures. All conditions call the same safety and BM25 ports. A low-confidence or failed transformation returns raw input and logs the event.

Runtime integration of dictionary normalization is optional. It requires safety non-inferiority, stable audit diffs, rollback by configuration, and unchanged routes. A learned normalizer requires the stricter gate in `07_ABSTENTION_AND_DIALECT_PROTOCOL.md` and is not part of the default implementation.

## Vision Engineering Prerequisite

Create a failing fixture for both branches that currently copy `solution_bn`, assign `verified`, and emit no sources. Repair the path so one of these outcomes occurs:

1. the fallback has a stable source ID and exact evidence, enters the same QA/verifier use case, and receives its actual certification action; or
2. evidence is unavailable and the response is explicitly uncertified/abstained with no treatment claim presented as verified.

Do not change classification-only behavior, fabricate boxes, or add another advisory pipeline. The repair must cover missing source, blocked advisory, verifier exception, and unavailable model cases.

## Acceptance Gates

- Existing terminal safety, fail-closed, JSON/SSE parity, audit cardinality, and vision classification tests remain green.
- Offline verifier passes E1/E2 and latency gates before container wiring.
- No source-empty treatment receives `verified`.
- BM25 artifact and corpus hashes match the run manifest.
- Routes and public fields remain compatible unless a versioned additive schema change is approved.
