# T1-04 — Privacy, Retention, and Licensing

- **Status:** BLOCKED — amendment review required (see below)
- **Tier:** 1 (post-capstone)
- **Depends on:** T0-01, T0-02 (audit DB — retention purge target), T1-03 (deployment — where the policy runs)
- **Blocks:** the B2B sales conversation (data-processing terms)
- **Amendment:** REVIEW REQUIRED — no hard-rule change expected; but the researcher must approve the retention defaults and the license choice (a legal call, not an engineering one). Record the decision in an amendment-style note so future agents don't relitigate it.

## Goal

Turn the "audit log + helpline registrations" data into a governed asset: a retention policy with automated purge, PII redaction on stored queries/logs, a privacy policy page, a license file, and a data-processing-terms template for the B2B lane. The privacy-first posture already exists (local-only audit, no external telemetry) — this task makes it documented, enforced, and sellable.

## Read first

- `backend/app/infrastructure/audit/` (jsonl + sqlite adapters) — where records are written/read.
- `backend/app/infrastructure/sessions/` — session data (contains query text).
- `backend/app/api/` — registration/helpline endpoints (names/phones stored locally).
- `frontend/src/app/` — layout/routes to add a `/privacy` page consistent with the design system.
- `docs/business_model_implementation_plan.md` — B2B framing for the DPA template.

## Invariants (do not break)

- Audit/session behavior unchanged while the policy is off (new settings default to "no retention limit" = today's behavior) — demo unaffected.
- Purge is configurable, off by default, and idempotent; it runs on startup and (optionally) on a timer — never a background thread if the single-process rule applies (use startup + on-write checks).
- PII redaction is applied at **write time** (or read time for the analytics surface) — queries are never logged with phone numbers/names; redaction is regex + allow-list based, tested, and documented as best-effort (never claimed perfect).
- The license choice is the researcher's; the task only wires it (LICENSE file, `pyproject.toml`/`package.json` metadata) and never invents one.
- Privacy page is static, matches the site's existing design conventions, and links from the footer — no new dependencies.

## Design

- Settings: `AUDIT_RETENTION_DAYS=0` (0 = keep forever, today's behavior), `SESSION_RETENTION_DAYS=30` (sessions already have TTL; align), `PII_REDACTION_ENABLED=true` (write-time redaction for audit query text; safe default since it only affects stored text, not responses).
- Purge: in the SQLite audit adapter, `DELETE FROM audit_records WHERE timestamp < ?` run at startup and on each write batch when retention > 0 (cheap, bounded); JSONL adapter gets a rotation note (rotate + purge on startup when enabled) — keep it simple.
- Redaction: `backend/app/core/redaction.py` — phone regex (Bangladeshi `+880`/`01` patterns), email regex, name-adjacent patterns; unit-tested; applied in the audit assembly point (T0-05 fields).
- Privacy page: `frontend/src/app/privacy/page.tsx` (+ footer link) — states what is stored (queries, sessions, optional helpline registration), retention defaults, local-only processing, contact path. No fabrication: only what the code actually does.
- License: `LICENSE` at repo root (researcher's pick — e.g. MIT for code; dataset remains CC-BY-4.0 per the paper/docs); metadata in `pyproject.toml` + `frontend/package.json`.
- `deploy/DPA_template.md` — plain-language data-processing terms for B2B tenants (what data, purpose, retention, deletion rights, subprocessors: none).

## Scope — create

- `backend/app/core/redaction.py` + `backend/tests/test_redaction.py`
- `frontend/src/app/privacy/page.tsx` (+ footer link edit)
- `LICENSE` (researcher-approved), `deploy/DPA_template.md`

## Scope — modify

- `backend/app/infrastructure/audit/sqlite.py` (retention purge, additive)
- audit assembly point (T0-05) — redaction hook
- `backend/app/core/config.py` (three settings), `.env.example`
- `backend/pyproject.toml` + `frontend/package.json` (license metadata only)

## Do not touch

- QA/safety pipeline, responses to users (redaction affects stored text only)
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`

## Rollback

1. Settings rollback: retention → 0, redaction → false → today's behavior.
2. Commit revert (bounded).

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_redaction.py -v` — green (phone/email/name patterns; Bengali digits too).
2. Retention: set `AUDIT_RETENTION_DAYS=1`, insert old + new rows, run purge → only old rows gone.
3. Live QA with redaction on: stored audit query text contains no phone/email; user-visible answer unchanged.
4. `pnpm build` — green with the new privacy page; footer link present.
5. License + DPA files reviewed by the researcher (approval recorded in the commit).

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Researcher's approval recorded for license + retention defaults; commit message notes open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- License choice (researcher decides; default proposal: MIT code + CC-BY-4.0 dataset already declared).
- Whether helpline registration data needs a separate retention window (propose 365 days; researcher approves).