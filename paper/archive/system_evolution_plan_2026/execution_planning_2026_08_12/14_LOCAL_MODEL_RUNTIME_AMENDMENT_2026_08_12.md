# Local Model Runtime Amendment

**Date:** 2026-08-12  
**Scope:** LM00-LM05 engineering lane only  
**Research thesis impact:** none

## Decision

Permit `llama-server` as the active local serving process for the existing public model ID
`krishoktech-4b`. It exposes an OpenAI-compatible endpoint at
`http://127.0.0.1:11435/v1` and is consumed through the existing
`OpenAICompatibleClient`. Ollama remains supported, but is not required for the current
demo machine.

This is an explicit amendment to the prior Ollama-only serving restriction. It does not
create a new QA route, application pipeline, model ID, safety policy, retriever, verifier,
audit sink, or frontend workflow.

## Reason

The authoritative merged FP16 checkpoint is approximately 15 GB and is not a fluent
runtime choice on the available CPU-only 16 GB Windows machine. The existing quantized
base GGUF plus the trained KrishokTech LoRA adapter loads successfully through llama.cpp,
fits the machine, and produces Bengali agricultural text. Direct llama.cpp serving also
avoids an additional Ollama model-store copy during the demo window.

## Active Artifacts

| Role | Path | Bytes | Status |
|---|---|---:|---|
| Quantized base | `E:\CSE499 Prototype\backend\models\krishoktech\gemma-4-E4B-it-Q4_K_M.gguf` | 4,977,171,584 | Load verified |
| Fine-tuned LoRA | `E:\CSE499 Prototype\backend\models\krishoktech\krishoktech-5362-adapter.gguf` | 279,088,320 | Apply verified |
| Authoritative merged checkpoint backup | `E:\CSE499 Prototype\backend\models\krishoktech\merge_tmp\merged_fp16_backup\model.safetensors` | 15,992,595,884 | Hugging Face byte-size match |
| Truncated checked-in GGUF | `backend/ml_assets/gemma/krishoktech.f16.gguf` | 1,358,004,160 | Invalid; do not serve |

Hugging Face provenance source:
`RaiyanKhaan/krishoktech-model-files`, path `merged_fp16_backup/`.

## Verified Runtime Evidence

- llama.cpp: `llama-server` version `10362 (4801e3c56)`, Clang 20.1.8, Windows x86_64.
- Hardware observed: CPU-only, 15.64 GB system RAM.
- Standalone base+LoRA generation completed at approximately 4.8 generated tokens/second
  for one Bengali smoke prompt. This is an engineering smoke observation, not a paper
  quality or latency benchmark.
- OpenAI-compatible UTF-8 completion returned Bengali content with reasoning disabled.
- `GET /api/models` reported `krishoktech-4b available=true`.
- Full `POST /api/qa` with `model="krishoktech-4b"` returned `safe_agri`, five BM25
  sources, `confidence="verified"`, and Bengali answer text.
- Eleven standard-library backend tests passed. `pytest` was unavailable in the current
  backend environment; no dependency was installed during the demo repair.

## Preserved Invariants

- Safety classification still executes before retrieval.
- The selected local model changes generation only.
- Runtime retrieval remains BM25-only.
- JSON and SSE still call the same `QAPipeline`.
- The existing verifier, audit sink, sessions, vision behavior, schemas, and public model
  ID remain unchanged.
- Gemini/OpenRouter remains available as the default configured provider.

## Claim Boundary

This amendment supports only the engineering claim that the local model is runnable through
the existing application pipeline. It does not establish model accuracy, safety superiority,
calibration, agronomic correctness, dialect robustness, or scientific performance. Those
claims remain blocked pending the frozen experiments in `11_FINAL_IMPLEMENTATION_SPEC.md`.
