# KrishokChat Refactor Plan

## Current-state diagnosis

The repository contains useful working pieces, but the request path is not currently one
pipeline. The main problems are structural rather than cosmetic:

| Severity | Finding | Evidence | Consequence |
|---|---|---|---|
| Critical | `/api/qa` duplicates the pipeline instead of calling `agents/orchestrator.py`. | `backend/app/api/qa.py` and `backend/app/agents/orchestrator.py` | Fixes in one path do not reach the other; streaming and non-streaming behavior diverge. |
| Critical | Safety behavior can fail open. | `backend/app/services/advisory/intent_classifier.py` defaults to `safe_agri` on provider failure; `qa.py` allows `low_confidence` through. | A classifier/provider failure can reach retrieval/generation without a reliable safety decision. |
| High | Two unrelated model integrations are active. | `safety_agent.py` uses Gemini; `intent_classifier.py` uses OpenRouter; `generator.py` uses Gemini; `generation_agent.py` is a source-extraction fallback. | Model replacement is hard and behavior depends on which route happens to call which module. |
| High | Blocking work runs in async request handlers. | `time.sleep`, sync `httpx.post`, synchronous BM25 and Ultralytics calls | Concurrent requests can stall the FastAPI event loop. |
| High | Protocol and path boundaries are mixed. | `sys.path.insert`, hard-coded `D:\KrishokChat Advisory System` paths, direct env loading in services | The backend is not portable and cannot be safely tested from another working directory. |
| High | The verifier is not a reliable groundedness check. | ASCII-only dosage regex and raw token-overlap heuristic | Bengali numerals/units are missed and ordinary Bengali answers can be flagged for irrelevant overlap. |
| High | Vision route is a monolithic router/service and currently performs classification, not normalized detection boxes. | `vision_orchestrator.py` | Later UI changes will be coupled to model internals; the documented `/api/detect` contract is ahead of the implementation. |
| Medium | Benchmark endpoint is still a placeholder. | `backend/app/api/benchmark.py` | Research page cannot consume checked-in benchmark artifacts. |
| Medium | No real backend test suite exists. | `backend/tests/` absent; scripts are ad-hoc | Regressions are likely when agents modify neighboring files. |
| Security | A live provider credential was present in the local backend environment while this audit was performed. | `backend/.env.local` | Rotate that credential immediately if it has ever been shared, logged, or committed. Do not copy it into any source or report. |

## Target module layout

```text
backend/app/
├── main.py                         # app factory + lifespan only
├── api/                            # thin HTTP/SSE adapters
│   ├── qa.py
│   ├── vision.py
│   ├── benchmark.py
│   └── dependencies.py
├── application/                    # use cases; no provider imports
│   ├── container.py
│   ├── qa_pipeline.py
│   └── vision_pipeline.py
├── domain/                         # enums, internal result contracts, policies
│   ├── contracts.py
│   ├── enums.py
│   └── safety_policy.py
├── ports/                          # Protocol interfaces
│   ├── llm.py
│   ├── retriever.py
│   ├── verifier.py
│   ├── audit.py
│   ├── session.py
│   └── vision.py
├── infrastructure/                 # replaceable adapters
│   ├── llm/
│   │   ├── openai_compatible.py
│   │   ├── gemini.py               # transitional adapter only
│   │   └── factory.py
│   ├── retrieval/bm25.py
│   ├── verification/dosage.py
│   ├── audit/jsonl.py
│   ├── sessions/memory.py
│   └── vision/ultralytics.py
├── models/schemas.py               # public Pydantic HTTP schemas
└── core/config.py                  # settings and resolved paths
```

The existing `agents/` and `services/advisory/` modules are compatibility shims during
migration. They must not remain two independently authoritative implementations.

## Ordered implementation milestones

## Implemented in this refactor pass

- Added typed domain contracts and a single safety policy with Bengali/Banglish deterministic
  prechecks and reviewed terminal responses.
- Added provider ports and a composition root with independent intent/generation model
  adapters. `ollama`, `openrouter`, `gemini`, and fail-closed `stub` are available.
- Replaced the duplicated QA route logic with one `QAPipeline` used by both JSON and SSE
  endpoints.
- Moved BM25, audit JSONL, in-memory sessions, and dosage verification behind adapters.
- Replaced legacy agent/service implementations with compatibility shims so old scripts do
  not silently select a second provider or safety policy.
- Added six backend contract/unit tests covering terminal safety, fail-closed parsing,
  shared pipeline execution, audit cardinality, Bengali dosage normalization, and API shape.
- Added the first modular vision workflow: artifact-derived registry, quality gate,
  classification routing, disease-details matching, grounded advisory handoff, verifier
  result propagation, and vision audit trace.

The benchmark milestone below remains deliberately separate because its endpoint is still
a placeholder. The vision workflow is now implemented as a classification-based pipeline;
inventing ONNX boxes or localization metrics would violate the project's no-fabrication rule.

### Milestone 1 — Contracts and safety boundary

- Add typed internal contracts and centralized safety categories/responses.
- Add a single classifier port with deterministic prechecks and fail-closed parsing.
- Add provider factory and settings-driven model selection.
- Add unit tests for every safety category, malformed JSON, provider timeout, and context
  that attempts to override a blocked query.

**Gate:** all non-`safe_agri` decisions stop before retrieval. No provider failure can
produce `safe_agri`.

### Milestone 2 — One QA application pipeline

- Move query augmentation into a pure `QueryBuilder`.
- Make BM25 retrieval an injected adapter and load it once at startup/lazily behind a lock.
- Make answer generation an injected adapter with a strict source-only prompt.
- Make verification a separate service with Bengali numeral/unit normalization.
- Make both `/api/qa` and `/api/qa/stream` call this same use case.
- Record one audit event in a `finally`-guarded request boundary.

**Gate:** non-streaming and streaming return the same final response for the same fake
dependencies; trace stages reflect the actual path, including skips.

### Milestone 3 — Vision application pipeline

- Move model paths and class names into a validated registry generated from the actual
  `class_names.json` artifacts.
- Separate image decoding/quality checks, classifier inference, disease inference, and
  treatment lookup.
- Keep the current `.pt` models supported; add ONNX only when the exported artifact is
  actually present and verified.
- Return honest `not_recognized`, `healthy`, `no_model`, and `diagnosed` states. Never
  fabricate bounding boxes for classification models.

**Gate:** each result state has a fixture test, and missing/low-confidence models fail with
an explicit state rather than a confident disease label.

### Milestone 4 — Research/benchmark read service

- Read only precomputed JSON artifacts from `ml_assets/rag_index`.
- Validate the artifact shape and report `unavailable` for missing metrics.
- Never calculate or invent metrics during an API request.

**Gate:** API output can be reproduced from checked-in artifact files.

### Milestone 5 — Contract tests and operational hardening

- Add `pytest` tests when the dependency policy permits; until then use stdlib `unittest`
  tests that run with the existing environment.
- Add API tests with fake adapters, SSE parser tests, and a no-network test mode.
- Run compile, import, typecheck, lint, and a smoke test in one documented command.
- Update the root README with the actual run path and model-provider replacement instructions.

**Gate:** an engineer can replace the LLM adapter without touching a router, schema, or
retrieval implementation.

## Agent operating rules for future work

1. One agent owns one milestone and one directory boundary.
2. Before editing, the agent must read `docs/refactor/ARCHITECTURE.md` and the relevant
   public schema.
3. No agent may add a second LLM call, fallback provider, or cache without naming it in the
   application contract and adding a test for the failure path.
4. No prompt text is an enforcement mechanism. Safety stops, source availability gates,
   and verifier outcomes must be code decisions.
5. New endpoints require a schema, dependency boundary, negative-path test, and README note.
