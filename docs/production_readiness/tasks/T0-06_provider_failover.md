# T0-06 — Provider Failover Chain + Circuit Breaker

- **Status:** DONE (2026-08-17)
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** nothing (benefits from T0-05 telemetry for measuring provider health, not required)
- **Blocks:** nothing
- **Amendment:** none required

## Goal

Wrap the existing LLM adapters in a config-driven failover chain with a per-provider circuit breaker. If the primary provider hangs or errors, the pipeline falls through the chain; if **all** providers fail, behavior is exactly today's fail-closed path (safe canned response / `low_confidence`). With a single provider configured, behavior is byte-identical to today (no wrapper active).

## Read first

- `backend/app/ports/` — the exact `LLMClient` port interface (methods, signature, exception types).
- `backend/app/infrastructure/llm/` — every adapter (openrouter, gemini, ollama, local/stub) + any existing retry/cooldown logic (the config has `gemini_key_cooldown_seconds` — reuse its pattern).
- `backend/app/core/config.py` — provider settings, timeouts (30s / 3 retries), and where a new `LLM_FAILOVER_CHAIN` setting fits.
- `backend/app/application/container.py` — where the LLM client is constructed and injected.

## Invariants (do not break)

- Fail-closed semantics preserved: total failure ⇒ the same safe response path as today. **Never** let a fallback chain answer a query the primary would have refused.
- The safety classifier call itself is NOT part of the failover chain (it has its own lightweight lane — keep it that way).
- Individual provider adapters are not modified (only wrapped).
- No new threads/processes; breaker state is in-memory (fine for a single process).
- With `LLM_FAILOVER_CHAIN` unset or single-provider, the container builds the exact client built today.

## Design

- `backend/app/infrastructure/llm/failover.py`:
  - `CircuitBreaker`: `consecutive_failures`, `max_failures` (setting), `cooldown_until` (epoch). Trips after `max_failures` consecutive failures; allows a probe attempt after cooldown; resets on success.
  - `FailoverLLMClient(LLMClient)`: holds ordered `(provider_name, client, breaker)`; on call, iterate: skip tripped breakers; call next on failure; on success reset breaker and return. If none succeed, raise the last error (or a dedicated `AllProvidersFailed` error the application layer already maps to fail-closed — verify what the app catches today).
- Config:
  - `LLM_FAILOVER_CHAIN` — comma-separated provider names in fallback order (e.g. `openrouter,gemini,ollama`); empty default = current single-provider behavior.
  - `LLM_CIRCUIT_MAX_FAILURES` default `3`
  - `LLM_CIRCUIT_COOLDOWN_SECONDS` default `30`
  - `.env.example` entries with one-line comments.
- Container: build `FailoverLLMClient` only when the chain has ≥ 2 entries; otherwise construct the single adapter exactly as today (guard: if the chain names a provider that isn't configured, log a warning and skip it — never crash startup).

## Scope — create

- `backend/app/infrastructure/llm/failover.py`
- `backend/tests/test_llm_failover.py` (breaker trips after N failures; cooldown probe; fallback on failure; all-fail raises; single-provider chain returns the plain client behavior)

## Scope — modify

- `backend/app/core/config.py` (three settings)
- `backend/app/application/container.py` (LLM client construction)
- `.env.example`

## Do not touch

- Any provider adapter (`infrastructure/llm/*` except the new file)
- The safety classifier call site and canned response paths
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

1. Config rollback: `LLM_FAILOVER_CHAIN=` (empty) → restart → single-provider behavior.
2. Commit revert: `git revert <commit>`.

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_llm_failover.py -v` — green.
2. Integration (stub lanes): chain `stub_fail,stub_ok` → query answered by `stub_ok`; chain `stub_fail,stub_fail` → fail-closed response exactly as today.
3. Real provider: chain `openrouter` (single) → live QA identical to pre-change behavior.
4. Config guard: chain naming a nonexistent provider → startup warning, no crash, falls back to remaining configured providers.
5. `uv run python -m compileall -q backend/app` — clean.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. `.env.example` updated; commit message notes open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- What exception the application layer catches for LLM failure today (must map `AllProvidersFailed` to the same path).
- Whether the safety classifier shares the LLM port (if it does, it must stay OUT of the failover wrapper — verify during `Read first`).