# Model Runtime Runbook

## Lanes
| Lane | Provider | Model | When used |
|------|----------|-------|-----------|
| Online (default) | OpenRouter (OpenAI-compatible) | `google/gemini-2.5-flash-lite` (configurable) | intent, rewrite, generation; dense embeddings via API |
| Local (optional) | llama.cpp `llama-server` on `127.0.0.1:11435` | `krishokchat-4b` = external `gemma-4-E4B-it-Q4_K_M.gguf` + `krishokchat-5362-adapter.gguf` LoRA | generation lane when the user selects krishokchat-4b |
| Vision | in-process ONNX (exported from Ultralytics `.pt`) | crop classifier + 5 disease classifiers | `/api/detect` |
| Retrieval | precomputed disk index | BM25 + BAAI/bge-m3 dense (1024-d, 2,135 nodes) | loaded at startup, never built at request time |

## Start the local lane
1. `scripts/start_krishokchat_local.ps1` (starts `llama-server.exe` on 11435
   with `--alias krishokchat-4b`).
2. Requires: the external Q4_K_M base GGUF + converted LoRA adapter GGUF
   (paths in the script), `llama.cpp` build.
3. Verify: `curl http://127.0.0.1:11435/v1/models` → model listed.

## Do NOT
- Serve `backend/ml_assets/gemma/krishokchat.f16.gguf` — it is **truncated**
  (checked-in artifact, do-not-serve status).
- Claim scientific evaluation results for the local runtime — it is verified
  as a demo runtime only (amendment 14, 2026-08-12).

## Config
`backend/.env` (or `.env.local`): `LLM_PROVIDER=openrouter`, `OPENROUTER_API_KEY`,
`DEMO_MODE=true`, `CORPUS_VERSION=2026-08`. `DEMO_MODE=false` disables the demo
answer cache entirely (fully live pipeline).