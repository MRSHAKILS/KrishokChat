# KrishokTech-4B GGUF Integration Plan

## Scope

Enable the existing `krishoktech-4b` chat-model option gracefully. This is an engineering integration, not a research contribution. Do not implement it during planning, replace Gemini as the default, add a second QA pipeline, or alter safety, BM25 retrieval, generation grounding, verification, vision, sessions, or audit contracts.

## Existing Assets and Seams

- GGUF candidate: `backend/ml_assets/gemma/krishoktech.f16.gguf`.
- Existing public model ID: `krishoktech-4b`.
- Existing UI selector: `frontend/src/components/qa-panel.tsx`.
- Existing request field: `backend/app/models/schemas.py`.
- Existing model registry/wiring: `backend/app/application/container.py`.
- Existing OpenAI-compatible adapter: `backend/app/infrastructure/llm/openai_compatible.py` and `factory.py`.
- Existing availability endpoint: `backend/app/api/extras.py` at `GET /api/models`.
- Locked active serving path: Ollama. Installed llama.cpp is initially an inspection and smoke-test tool.

## Invariants

1. `gemini` remains the default and continues to work unchanged.
2. `krishoktech-4b` remains the only local-model ID across UI, API, audit, tests, and configuration.
3. Model selection changes only the generation adapter. The safety classifier still runs first using its configured classifier adapter.
4. Unavailable local serving disables the selector option or returns the existing controlled referral; it never falls back silently to a different model under the same ID.
5. Both JSON and SSE routes use the same `QAPipeline` and produce equivalent final contracts.
6. No model weight is copied, converted, quantized, renamed, or committed by an agent without explicit approval.
7. Do not call the artifact 4-bit or claim Gemma architecture/training provenance until metadata and provenance are recorded.

## Priority Checklist

### P0 - LM00: Freeze Artifact Identity

- [ ] Record absolute/relative path, byte size, SHA-256, modification time, and Git tracking/ignore status.
- [ ] Use installed llama.cpp GGUF tooling to record architecture, tensor types/quantization, context metadata, tokenizer, and embedded chat template.
- [ ] Reconcile the `krishoktech.f16.gguf` filename with the stated 4-bit provenance. Do not rename or requantize during this task.
- [ ] Record the exact llama.cpp binary/version and commands that work on this machine.

**Gate:** Stop if the file is unreadable, architecture is unsupported, metadata is inconsistent, or provenance cannot be tied to the fine-tuned KrishokTech checkpoint.

### P0 - LM01: Reproduce Standalone Inference

- [ ] Run a deterministic CLI smoke test with one simple Bengali agricultural prompt.
- [ ] Confirm the model emits usable Bengali and terminates correctly.
- [ ] Confirm which chat template is applied. Prefer embedded metadata; never hand-assume a Gemma template.
- [ ] Record startup time, peak memory if available, first-token latency, response latency, command, output, and failure log.

**Gate:** Do not expose the option in the app until standalone inference passes reproducibly.

### P1 - LM02: Register Through Ollama

- [ ] Confirm the current official Ollama custom-GGUF import procedure before editing setup files.
- [ ] Create/review the minimal Modelfile or registration script that references the existing GGUF without duplicating it.
- [ ] Register the stable tag `krishoktech-4b` and verify it through Ollama CLI and its local API.
- [ ] Keep llama.cpp direct serving out of the active app path unless root `AGENTS.md` is explicitly amended.

**Gate:** `krishoktech-4b` is discoverable and answers through Ollama's OpenAI-compatible endpoint after a clean restart.

### P1 - LM03: Align Configuration and Health Contract

- [ ] Correct the stale configured GGUF path only if runtime/setup code actually consumes it.
- [ ] Make local base URL, model tag, timeout, and optional API key configuration-driven; update `.env.example` comments.
- [ ] Keep `/api/models` provider-aware and non-blocking; do not hardcode an unrelated health URL inside the route.
- [ ] Report `available=true` only when the configured server is reachable and the exact stable model ID/tag exists.
- [ ] Keep labels factual: `KrishokTech-4B` and `local fine-tuned model`; add the verified base/quantization wording only after LM00.

**Gate:** Local unavailability does not affect backend startup or Gemini/default requests.

### P2 - LM04: Wire Existing Selector Without Behavioral Changes

- [ ] Reuse `generation_clients` and the existing `krishoktech-4b` request value; do not create a route or pipeline.
- [ ] Preserve frontend selector layout and existing messages. Only fix availability/disabled behavior if required.
- [ ] Ensure selected-model identity is present in the final response/audit diagnostics without exposing filesystem paths.
- [ ] Ensure model selection cannot alter terminal safety decisions or retrieve before safety classification.
- [ ] Do not touch verifier, retriever, vision, benchmark, session, or research logic.

**Gate:** The same safe query can use either available generation model while terminal unsafe queries invoke neither generator.

### P2 - LM05: Regression and Handoff

- [ ] Add backend tests for exact model lookup, unavailable local server, selected local client, no silent fallback, and terminal-safety short circuit.
- [ ] Add/retain JSON-SSE parity coverage with the selected model field.
- [ ] Verify frontend typecheck/lint and selector disabled/enabled states.
- [ ] Run the full existing backend suite and one Bengali end-to-end smoke test for each available model.
- [ ] Update setup documentation with exact start/register/check commands and rollback instructions.
- [ ] Append completion evidence to `MEMORY.md`: code revision, dirty-tree status, commands, versions, hashes, tests, failures, and gate result.

**Gate:** All previous tests pass; Gemini behavior is unchanged; stopped/unavailable local serving degrades gracefully; no source-empty or unverified answer gains a positive verification state.

## Optional Future Amendment: Direct llama.cpp Serving

Direct llama.cpp serving is not required because the current architecture already supports the GGUF through Ollama. Consider it only if measured Ollama overhead or compatibility blocks LM02. Before implementation, amend the locked stack explicitly, verify llama.cpp's current OpenAI-compatible endpoint and streaming format, then add it as another infrastructure adapter/configuration choice behind the same `krishoktech-4b` public ID. Routes, schemas, UI IDs, and pipeline order must remain unchanged.

## Agent Start Rule

An implementing agent receives exactly one `LMxx` task. It first reads root `AGENTS.md`, `docs/refactor/PROJECT_HANDOFF.md`, `docs/refactor/ARCHITECTURE.md`, this folder's `AGENTS.md`, and this file. It may edit only the files required by that task, must inspect concurrent changes first, and stops at the task gate rather than continuing to the next item.
