# KrishokChat Backend

FastAPI backend for the safety-aware Bengali agricultural advisory prototype.

## Run

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Provider replacement

The request path depends on the `LLMClient` port, not on a provider SDK. Configure the
adapter in the repository `.env`/local environment:

```dotenv
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=my-finetuned-gemma
```

`gemini`, `openrouter`, `ollama`, and `stub` are supported by the factory. The `stub`
choice is intentionally fail-closed for safety classification and is useful for API
contract tests; it does not pretend to generate a useful answer.

## Request flow

`app/main.py` creates one application container. `app/api/qa.py` is a thin transport
adapter. `app/application/qa_pipeline.py` is the only authoritative QA workflow, and
the modules under `app/infrastructure/` implement replaceable providers for LLM,
retrieval, verification, audit, and sessions.

The old `app/agents/` and `app/services/advisory/` imports are compatibility shims for
existing offline scripts. New code must not add behavior there.

The vision path follows the same boundary: `app/api/vision.py` is transport-only,
`app/application/vision_pipeline.py` owns the crop → disease → advisory workflow, and
`app/infrastructure/vision/` owns artifact discovery and Ultralytics inference. The
current checked-in models are classification models, so the API reports classification
confidence and empty boxes rather than claiming object localization.

## Verification

```bash
uv run python -m compileall -q app
uv run python -c "from app.main import app; print(app.title, app.version)"
```

See `../docs/ARCHITECTURE_PORTS_AND_ADAPTERS.md` before changing the pipeline.
