# T1-01 — Multi-Tenancy + RBAC (B2B Lane 1 Unlock)

- **Status:** BLOCKED — amendment required before any code
- **Tier:** 1 (post-capstone)
- **Depends on:** T0-01 (SQLite), T0-07 (API keys) — gates passed
- **Blocks:** the paid dealer/SAAO audit-dashboard product (business-model lane 1)
- **Amendment:** **REQUIRED** — conflicts with AGENTS.md §2.1 ("no per-tenant data isolation"). See §Amendment below.

## Goal

Add tenant-scoped audit and analytics so agro-dealers, SAAOs, and extension officers can each see **only their own** advisory traffic, with roles (farmer / dealer / SAAO / admin) and per-tenant quotas. Everything sits behind `TENANCY_ENABLED=false` (default) so the single-session demo remains byte-identical. This is the architectural unlock for the paid dashboard — the audit engine is already the moat; tenancy makes it sellable.

## Read first

- `backend/app/ports/` — audit, session, and (from T0-07) key-verification ports.
- `backend/app/infrastructure/audit/sqlite.py` (T0-02) — the `audit_records` table that gains the tenant column.
- `backend/app/api/middleware/api_key.py` (T0-07) — where a key is resolved to a client label today; this becomes tenant resolution.
- `backend/app/application/` — analytics/metrics aggregation code (must become tenant-scoped).
- `docs/production_readiness/amendments/` — the approved amendment for this task (must exist first).

## Invariants (do not break)

- `TENANCY_ENABLED=false` ⇒ zero behavior change anywhere (demo path intact).
- Tenant isolation is enforced in the **application layer** (tenant id flows through the port), never trusted from client input alone.
- Roles are additive: existing anonymous/demo users map to the farmer-equivalent role with no loss of functionality.
- Audit rows never lose data in migration (tenant column nullable, backfilled with the tenant of the writing key, or a default `demo` tenant).
- Supabase auth (if present) is not required for tenancy; tenancy works with API keys first (T0-07), Supabase JWT tenant claims later.

## Design

- Migrations (T0-01 runner):
  - `tenants(id TEXT PK, name TEXT, plan TEXT, quota_per_day INTEGER, created_at TEXT)`
  - `api_keys(key_hash TEXT PK, tenant_id TEXT FK, label TEXT, enabled INTEGER, created_at TEXT)` — keys stored hashed; the env-literal keys from T0-07 become bootstrap seeds
  - `audit_records` gains `tenant_id TEXT NULL` + index on `(tenant_id, category, timestamp)`
- Application layer:
  - `TenantContext` (port + a contextvar set by middleware from the verified key/JWT)
  - role checks via a `require_role(...)` dependency: dealer/SAAO see tenant-scoped analytics; admin sees all; farmer sees own sessions only
  - all metrics/analytics queries accept an optional tenant filter that is **always applied** when `TENANCY_ENABLED=true`
- Quotas: per-tenant daily advisory count enforced where audit rows are written (increment + check), 429-equivalent business response when exceeded.
- Admin surface: a minimal read-only tenant list endpoint (`GET /api/v1/admin/tenants`) — no admin panel UI in this task (AGENTS.md §2.1 stays for UI).

## Amendment

The amendment file must state:
- rule changed: AGENTS.md §2.1 sentence "no per-tenant data isolation"
- new wording: per-tenant isolation permitted **only when `TENANCY_ENABLED=true`**, default false, demo unaffected
- why now: business-model lane 1 requires tenant isolation to be sellable
- what stays forbidden: no role-based UI, no per-tenant Supabase schemas, no tenant UI in the demo path
- revert condition: any demo regression ⇒ flip `TENANCY_ENABLED=false` and file a follow-up

## Scope — create

- `backend/app/application/tenancy.py` (TenantContext, role checks, quota service)
- migrations (tenants, api_keys, audit tenant column)
- `backend/tests/test_tenancy.py` (tenant A cannot read tenant B rows; role denial; quota exceeded; `TENANCY_ENABLED=false` → identical behavior)

## Scope — modify

- `backend/app/api/middleware/api_key.py` (T0-07) — resolve key → tenant
- analytics/metrics aggregation (tenant filter, additive)
- `backend/app/core/config.py` (+ `TENANCY_ENABLED`, `TENANCY_DEFAULT_QUOTA`), `.env.example`

## Do not touch

- Demo routes, safety pipeline, ports contracts, frontend
- `backend/app/agents/`, `backend/app/services/advisory/`

## Rollback

1. `TENANCY_ENABLED=false` → restart → demo identical.
2. Commit revert (bounded to tenancy files).

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_tenancy.py -v` — green.
2. With tenancy on: key A writes 5 rows, key B queries → sees zero of A's rows; admin sees all.
3. Quota: set quota 1 → second advisory of the day returns the business-limit response.
4. With tenancy off: full demo smoke identical to pre-change (diff metrics + QA responses).
5. `uv run python -m compileall -q backend/app` — clean.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Amendment approved and referenced; commit message notes open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Which roles the pilot tenants actually need (start with dealer + SAAO + admin; farmer stays anonymous-equivalent).
- Whether Supabase JWT tenant claims should be wired now or keys-only first (keys-only is acceptable; document).