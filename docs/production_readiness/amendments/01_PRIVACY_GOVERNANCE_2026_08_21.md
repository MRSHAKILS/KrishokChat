# Privacy, Retention & Licensing Governance Amendment — T1-04 (APPROVED 2026-08-21)

**Date:** 2026-08-21
**Status:** APPROVED 2026-08-21 — via go (researcher)
**Tier:** 1 (post-capstone) — `docs/production_readiness/tasks/T1-04_privacy_governance.md`
**Depends on:** T0-01, T0-02 (audit DB retention target), T1-03 (where policy runs)
**Blocks:** B2B data-processing terms lane
**Precedent:** `14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`, `15_SUPABASE_AUTH_AMENDMENT_2026_08_14.md`

---

## 1. Decision (what this amendment approves)

Record researcher-approved defaults for turning the existing local-only audit/helpline data into a governed, PDP-compliant asset — without changing demo behavior until explicitly enabled.

Specifically approves (T1-04 scope only):

- **Retention enforcement** — automated purge of `audit_records` / JSONL by age when enabled (additive, off by default).
- **PII redaction** — write-time redaction of phone/email/name patterns in stored audit query text (additive, best-effort, never claimed perfect).
- **Privacy page** — static `/privacy` route + footer link describing what is stored and for how long.
- **License + DPA** — `LICENSE` at repo root (researcher's pick) and `deploy/DPA_template.md` for B2B tenants.

No code lands until this file is marked **APPROVED** below.

---

## 2. Rule being changed

**No AGENTS.md §2 hard rule is repealed.** This is a governance extension of the existing audit invariant, filed as a dated Tier-1 amendment per `docs/production_readiness_roadmap.md` §5 (same process as amendments 14/15).

Existing invariant (AGENTS.md §4, Audit trail paragraph):

> "every classification decision (query, category, action taken, timestamp) gets appended to a local log (simple JSON lines file or SQLite table under `backend/app/logs/`). This log is what powers the 'safety metrics' panel ... Never log this to an external service — local file only, this is a prototype."

**Exact new wording (additive clarification to §4, effective when T1-04 lands):**

> Audit/session storage remains **local-only** (JSONL `backend/app/logs/safety_audit.jsonl` and SQLite `backend/data/krishoktech.db` via `AUDIT_BACKEND`/`SESSION_BACKEND`; never sent to an external service). When retention is enabled (`AUDIT_RETENTION_DAYS > 0`), the SQLite adapter purges rows `WHERE timestamp < now() - AUDIT_RETENTION_DAYS` on startup and on each write batch (idempotent, bounded), and the JSONL adapter rotates/prunes on startup per `docs/production_readiness/retention_policy.md`. When `PII_REDACTION_ENABLED=true`, query text is redacted at write time (BD phone `+880`/`01` patterns including Bengali digits `০-৯`, email, name-adjacent patterns; regex + allow-list, best-effort) before persisting to audit/helpline logs. Stored-text redaction never alters the user-visible answer.

`docs/production_readiness/retention_policy.md` (90-day window, operator runbook) remains the policy doc; this amendment makes the **automated enforcement** switch-gated.

---

## 3. Why now

- **Law:** Bangladesh **Personal Data Protection Ordinance 2025 (No. 61 of 2025)**, gazetted **2025-11-06** (`bdlaws.minlaw.gov.bd/act-1574.html`), in force immediately with the fines regime effective ≈ May 2027. Fines: **1–5% of annual Bangladesh turnover** for non-compliance — directly applicable to audit logs and helpline registrations that store personal data. Risk is tracked in `docs/PRODUCTION_ROLLOUT_PLAN.md` §§ 1/6 (risk #3), W4/W5/W8.
- **Current gap (verified 2026-08-21):** `backend/app/logs/safety_audit.jsonl` (~1.5 MB) and `backend/app/logs/helpline_registrations.jsonl` (stores `name` + `phone` e.g. `01711111111`, district) have **no retention, no masking, no PII scrub** (`backend/app/infrastructure/audit/`, `backend/app/logs/helpline_registrations.jsonl`). Sessions contain query text with potential PII. `AUDIT_RETENTION_DAYS=90` exists in `.env.example`/`config.py` but `retention_policy.md` states the app **never auto-deletes** — purge is manual/operator-run only. Without governance the B2B lane cannot present data-processing terms (T1-04 blocks B2B sales conversation).
- **Timing:** Phase 0 complete; Tier 1 requires a dated amendment before code. This amendment is the bounded, reversible approval gate for T1-04.

---

## 4. What stays forbidden (invariants — do not break)

- **Local-only, no external telemetry.** Audit/sessions/helpline data never leaves the host (AGENTS.md §4). No analytics sink, no third-party PII processor. `deploy/DPA_template.md` will state subprocessors: **none** (until a Tier-1 decision adds one via a new amendment).
- **Demo never gates.** With `DEMO_MODE=true` or no signed-in user, every route (`/`, `/chat`, `/api/qa`, `/api/qa/stream`, `/detect`, `/api/v1/*` aliases) behaves exactly as before. Privacy page and retention wiring are additive; no auth, no redirect, no popup (AGENTS.md §2.1, Supabase amendment 15 invariant preserved).
- **Audit/session behavior unchanged while off.** Purge is **off by default**; redaction is off (or best-effort only on stored text, never on responses) until the researcher flips the switch. Single-process rule respected — purge via startup + on-write checks, not a background thread (T1-04 invariant).
- **Port contracts, safety pipeline, and response text untouched.** Redaction affects **stored** audit `query` text only; `backend/app/agents/` and `backend/app/services/advisory/` remain shims (AGENTS.md §5.1). QA/safety/retrieval/verifier behavior unchanged.
- **No fabrication.** Privacy page states only what the code actually stores. License is the researcher's pick; do not invent one. Redaction is documented as best-effort (regex, never claimed perfect).

---

## 5. Scope (additive, bounded, reversible — one task, one commit)

Per `T1-04_privacy_governance.md` §Design / §Scope — no wider edits:

**Create:**

- `backend/app/core/redaction.py` + `backend/tests/test_redaction.py`
- `frontend/src/app/privacy/page.tsx` (+ footer link edit)
- `LICENSE` at repo root (researcher-approved; proposal: **MIT for code**, dataset stays **CC-BY-4.0** per paper/docs)
- `deploy/DPA_template.md` (plain-language DPA for B2B: what data, purpose, retention, deletion rights, subprocessors: none)

**Modify (additive only):**

- `backend/app/infrastructure/audit/sqlite.py` — retention purge (startup + write-batch) when `AUDIT_RETENTION_DAYS > 0`
- Audit assembly point (T0-05 fields) — redaction hook at write time
- `backend/app/core/config.py` + `.env.example` — three settings (see §6)
- `backend/pyproject.toml` + `frontend/package.json` — `license` metadata only (no code change)

**Do not touch:** QA/safety pipeline responses, `backend/app/agents/`, `backend/app/services/advisory/`, `capstone/`, `paper/`, `dataset_release/`, port signatures, demo cache lane.

---

## 6. Settings — defaults are today's behavior (safe default = off)

Every new path is **off or equals current behavior** until its gate passes (`docs/production_readiness/README.md` global rule).

| Setting | Code default (lands as) | When enabled | Meaning |
|---|---|---|---|
| `AUDIT_RETENTION_DAYS` | `0` | `90` | `0` = keep forever (today's behavior; `retention_policy.md` operator runbook only) — **default off**. `90` enforces the 90-day window documented in `retention_policy.md` / `PRODUCTION_ROLLOUT_PLAN.md` D8. Env var already in `.env.example`/`config.py`; T1-04 makes the app enforce it. |
| `SESSION_RETENTION_DAYS` | `30` | `30` | Aligns with existing `SESSION_TTL_SECONDS`/`SESSION_MAX_TURNS`; purge uses same startup/on-write pattern (or reuses `AUDIT_RETENTION_DAYS` if researcher prefers one knob — approve below). |
| `PII_REDACTION_ENABLED` | `false` | `true` | `false` = store query text verbatim (today). `true` = write-time redaction of BD phones (`+8801`/`01` + Bengali digits), emails, name-adjacent patterns before audit persist. Task doc proposes `true` as safe (affects stored text only); this amendment lands the code **default `false`** so the behavior change is opt-in; flip to `true` after researcher review of `test_redaction.py`. |

Task doc `T1-04` proposes `PII_REDACTION_ENABLED=true` by default (safe because it only touches stored text); the **reversible** landing choice here is `false` — flipping to `true` is a one-line `.env` change after gate 3 passes. Researcher to confirm preferred default in Approval below.

All three vars go in `.env.example` with one-line comments and in `backend/app/core/config.py` with sane defaults.

---

## 7. Revert condition (one-line, no code revert needed)

- **Config rollback (preferred):** set `AUDIT_RETENTION_DAYS=0` (or `PII_REDACTION_ENABLED=false`) and restart — behavior reverts to today's keep-forever / verbatim logging. No migration to undo (purge is `DELETE WHERE timestamp < …`, redaction is not retroactive).
- **Commit revert (bounded):** `git revert <T1-04 commit>` — commit is bounded to the files in §5 (guaranteed by task handbook); no other task's files are touched.
- **Trigger:** any demo regression under `DEMO_MODE=true` / anonymous user, or any gate failure in §8, or researcher withdraws approval — flip the switch, file a follow-up, and keep the amendment as DRAFT.

---

## 8. Verification gate (stop/go — run exactly, gate fails ⇒ STOP)

Per `T1-04_privacy_governance.md` §Verification gate (do not widen scope on failure):

1. `uv run pytest backend/tests/test_redaction.py -v` — green (phone `01`/`+880` including Bengali digits `০-৯`, email, name-adjacent; documented best-effort).
2. Retention: set `AUDIT_RETENTION_DAYS=1`, insert old + new rows, run purge → only old rows gone (`DELETE FROM audit_records WHERE timestamp < datetime('now', '-1 days')`).
3. Live QA with redaction on: stored audit `query` contains no phone/email; user-visible answer unchanged.
4. `pnpm build` — green with `/privacy` route; footer link present.
5. `LICENSE` + `deploy/DPA_template.md` reviewed by researcher; approval recorded in commit message and in §9 below.

Pre-existing gates still required: `uv run python -m compileall -q backend/app`, `uv run python -c "from app.main import app; print(app.title)"` clean, `uv run pytest -q` green, `pnpm build` green, golden replay invariants pass under both `AUDIT_RETENTION_DAYS=0` and `=90`.

---

## 9. Open questions — researcher decision (approval records the choice)

- [ ] **Retention defaults:** approve `AUDIT_RETENTION_DAYS=0` (default off; set `90` to enforce) and `SESSION_RETENTION_DAYS=30` (or unify to one knob). *(Recommended: 0 / 30 as above.)*
- [ ] **Redaction default:** approve `PII_REDACTION_ENABLED=false` at land, flip to `true` after reviewing `test_redaction.py` — or land `true` immediately (task doc proposal). *(Recommended: land `false`, flip after gate.)*
- [ ] **Helpline registration retention:** separate window? Proposal **365 days** (`T1-04` open question) vs same `AUDIT_RETENTION_DAYS`. Approve window and whether helpline storage itself should be redacted at write vs read.
- [ ] **License choice (legal call, not engineering):** pick `LICENSE` content. Proposal: **MIT for code** (repo), **CC-BY-4.0 for dataset** (already declared in paper/docs). Wire to `pyproject.toml` / `package.json` only after this choice.
- [ ] **DPA template scope:** confirm B2B data categories (audit queries, sessions, helpline registrations), purpose (advisory + safety metrics), retention, deletion rights, and that subprocessors = none.

---

## 10. Approval (sole authority: the researcher)

- [ ] **APPROVED** — proceed to T1-04 implementation under the scope/defaults above.
- [ ] **APPROVED with modifications** (note below).
- [ ] **REJECTED / DEFERRED** (note reason; task stays BLOCKED).

**Researcher:** ______________________  **Date:** __________  **Notes:** ___________________________________________________________________

On approval: mark `T1-04_privacy_governance.md` Status from `BLOCKED` → `READY`, reference this amendment from that file and from `docs/refactor/PROJECT_HANDOFF.md`, then execute exactly the scope in §5 (single bounded commit, handbook §6 definition of done).

---

## 11. Claim boundary

This amendment establishes **governance and switch-gated wiring** for retention/PII handling and the researcher-approved license/DPA choice. It does not establish that the redaction is perfect, that the 90-day window satisfies any specific regulator's interpretation, or that the DPA template is legal advice. Those determinations remain with the researcher (+ counsel if needed) under the PDP Ordinance 2025.
