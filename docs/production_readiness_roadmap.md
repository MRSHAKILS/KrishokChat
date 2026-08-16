# KrishokChat — Production Readiness Roadmap

**Status:** ADVISORY ROADMAP — nothing here changes the demo before an agent executes a task.
**Date:** 2026-08-17
**Audience:** the researcher (approver) + future executing agents.

> Read together with `docs/production_readiness/README.md` (global execution rules) and the task docs in `docs/production_readiness/tasks/`. Each task is a self-contained agent brief with its own scope, invariants, rollback, and stop/go gate.

---

## 1. Purpose

The system is architecturally sound for a capstone (layered ports/adapters, fail-closed safety, replaceable LLM, precomputed indexes, local-only audit). This roadmap converts it into a production-grade service **without ever endangering the working demo**. Two principles govern everything below:

1. **Additive-first.** Every change ships alongside the existing behavior, behind a config switch whose default is the current behavior. A mistake in any one task can never break the demo — flip the switch back or revert one bounded commit.
2. **One task, one agent, one gate.** Each task document is executable cold by a single agent, has a verification gate, and lists exactly what must not be touched.

## 2. Current-state assessment (verified against code)

**Already production-grade:**
- Layered composition root (`app/api → application → ports → infrastructure`) with enforced dependency direction (`docs/refactor/ARCHITECTURE.md`).
- Fail-closed safety invariants; safety classified before retrieval.
- Replaceable `LLMClient` port (OpenRouter / Gemini / Ollama / stub) with separate local/remote timeout budgets (`app/core/config.py`).
- Precomputed RAG indexes loaded from disk; auto BM25 fallback for the dense channel.
- Local-only JSONL audit; pydantic-settings config with `.env` precedence and maintained `.env.example`.

**Verified gaps (what this roadmap fixes):**
- Sessions are in-memory (`infrastructure/sessions/memory.py`) — lost on restart.
- Audit is a single JSONL append (`infrastructure/audit/jsonl.py`) — concurrent-write risk, no rotation, no indexed queries.
- No request IDs, no structured logging, no per-stage latency/token telemetry (`app/main.py` has only CORS + routers).
- Provider failover is config-time only; no circuit breaker or runtime fallback chain.
- API has no versioning, no API-key auth, no rate limits, no pagination on history/audit endpoints.
- `pytest` not declared in `pyproject.toml`; no CI; no license; no deployment artifacts (no Dockerfile, no `.github/`).
- API process bundles torch + ultralytics + sentence-transformers (~3 GB) even for text-only requests.
- No retention/PII policy for audit logs and helpline registrations.
- Admitted safety gaps: no multi-turn safety context, no red-team CI, no review lane for verifier-flagged advisories.

## 3. Tiers

| Tier | Meaning | When | Constraint |
|---|---|---|---|
| **Tier 0** | Hardening inside existing hard rules | Pre-capstone (safe now) | No amendment needed. Additive, switch-gated. |
| **Tier 1** | Production unlocks that conflict with a hard rule | Post-capstone only | Requires a dated amendment approved by the researcher (see §5). |
| **Tier 2** | Research/eval integrity (parallel lane) | Anytime | Part of T0-08; extended post-capstone. |

## 4. Task map and execution order

```
Phase A (independent first wave — run in parallel):
  T0-01  SQLite foundation (DB bootstrap + migrations)
  T0-04  Request-ID + structured logging middleware
  T0-08  pytest declaration + CI + golden regression gate

Phase B (depends on Phase A):
  T0-02  Audit → SQLite adapter          (needs T0-01)
  T0-03  Sessions → SQLite adapter       (needs T0-01)
  T0-05  Stage latency + token/cost telemetry  (needs T0-04)

Phase C (independent, after B for observability):
  T0-06  Provider failover chain + circuit breaker  (wants T0-05 to measure)
  T0-07  API versioning + keys + rate limits        (independent; pairs with T0-02 DB)

Post-capstone (each needs its own amendment):
  T1-01  Multi-tenancy + RBAC            (needs T0-01, T0-07)
  T1-02  Model-serving separation        (ONNX vision path + model registry)
  T1-03  Deployment kit                  (Dockerfile, supervisor, proxy, backups)
  T1-04  Privacy, retention, licensing
  T1-05  Safety depth                    (multi-turn context, red-team CI, review lane)
```

**Why this order:** T0-01/T0-04/T0-08 have no dependencies and unblock everything else. T0-02/T0-03 convert the two weakest storage points. T0-05 turns the audit record into real telemetry. T0-06/T0-07 are independent additive layers. Tier 1 items are large lifts that the business model implies (tenant dashboards, API licensing, deployment) but that hard rule 1 forbids at demo phase.

## 5. Amendment process (for Tier 1)

A task that conflicts with `AGENTS.md` §2 cannot start until a dated amendment exists. Pattern (follows the repo's existing amendment style, e.g. the Supabase Auth amendment):

1. Executing agent writes `docs/production_readiness/amendments/<N>_<SLUG>_<YYYY_MM_DD>.md` stating: the rule being changed, the exact new wording, why now, what stays forbidden, and the revert condition.
2. The **researcher approves** (the sole authority for AGENTS.md changes).
3. The amendment is referenced from the task doc's "Amendment" section and from `AGENTS.md` §2 only after approval.
4. Until approved, the task is BLOCKED — no code may be written.

## 6. The "no ruin" guarantees (enforced by every task doc)

1. **Additive-only** — new adapter/module lives beside the old one; old code is not deleted or rewritten in the same task.
2. **Config switch with safe default** — every new behavior is off (or set to current behavior) until its gate passes.
3. **Bounded rollback** — each task doc lists the exact revert: a config flip and/or a single bounded commit. No task may interleave two unrelated concerns, so a revert never drags in other work.
4. **Stop/go gate** — each task has exact commands and expected outputs. Gate fails → STOP, do not "fix" by expanding scope.
5. **Do-not-touch lists** — legacy `app/agents/` and `app/services/advisory/` shims, safety invariants, port contracts, and the demo cache path are explicitly off-limits in every task.
6. **Definition of done** — mirrors AGENTS.md §6: runs locally, locked stack respected, new dependency versions confirmed by an internet search (AGENTS.md §2.7), `.env.example` updated with a one-line comment, and a commit message noting open questions.

## 7. What this roadmap explicitly rejects

- Microservices, Kubernetes, message queues, 6-service Compose (AGENTS.md §2.3 — single process is correct at this scale; scaling = replicating the container behind a proxy).
- A separately trained safety classifier (deterministic pre-filter + LLM structured output is the right tradeoff until real volume).
- A rewrite of the layered architecture (correct as-is; production work is adapters + middleware + tenancy on top of existing ports).
- Live index building or cloud re-platforming of the corpus (precomputed local indexes are a feature).
- Fabricated numbers anywhere in docs or code (AGENTS.md §2.5).

## 8. Files

```
docs/production_readiness_roadmap.md          (this file)
docs/production_readiness/
├── README.md                                 global execution rules + dependency graph
├── amendments/                               (created on first Tier 1 approval — see §5)
└── tasks/
    ├── T0-01_sqlite_foundation.md
    ├── T0-02_audit_sqlite_adapter.md
    ├── T0-03_session_sqlite_adapter.md
    ├── T0-04_request_id_logging.md
    ├── T0-05_stage_latency_telemetry.md
    ├── T0-06_provider_failover.md
    ├── T0-07_api_versioning_keys_ratelimit.md
    ├── T0-08_pytest_ci_golden_gate.md
    ├── T1-01_multitenancy_rbac.md
    ├── T1-02_model_serving_separation.md
    ├── T1-03_deployment_kit.md
    ├── T1-04_privacy_governance.md
    └── T1-05_safety_depth.md
```
