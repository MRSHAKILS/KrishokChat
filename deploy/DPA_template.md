# KrishokChat — Data Processing Terms (Template)

> **Status:** Template for B2B tenants. This is not legal advice. Replace bracketed
> placeholders (`[ ... ]`) and have counsel review before signing. Code behavior
> described here is verified in `backend/` and `docs/production_readiness/`.

## 1. Parties and scope

- **Processor:** [Research prototype operator / deploying organization] operating the
  KrishokChat Advisory System (the “System”).
- **Controller:** [Tenant organization] subscribing to the System for agricultural
  advisory services.
- **Scope:** This template covers personal data processed when the Tenant’s users
  interact with the System via the hosted deployment. It does not cover data the
  Controller processes outside the System.

## 2. What data is processed

| Category | Example fields | Source | Storage |
|---|---|---|---|
| Audit queries | `query` text, `category`, `action`, timestamps, safety flags | User input to `/api/qa` | Local JSONL `backend/app/logs/safety_audit.jsonl` and/or SQLite `backend/data/krishokchat.db` (`audit_records`) |
| Session history | `{"role","content"}` message lists per `session_id` | User + assistant turns | In-memory or SQLite `sessions` table (same DB) |
| Helpline registrations | `name`, `phone`, `district`, `crop`, `notes` | `/api/helpline/register` opt-in form | Local JSONL `backend/app/logs/helpline_registrations.jsonl` |
| Telemetry (optional) | `stage_timings_ms`, `tokens`, `provider`, `request_id` | Pipeline instrumentation | Same audit record (`record_json` + columns) |

No other personal data is collected by the System. The System does not use
external analytics, telemetry sinks, or third-party PII processors.

## 3. Purpose and legal basis

- Provide grounded Bengali agricultural advice, safety classification, and
  verifier-audited sources.
- Produce local safety metrics (`GET /api/safety/metrics`) for demo/oversight.
- Fulfil helpline callback requests where the user voluntarily registers.

Basis: user request / legitimate interest in providing the requested advisory
service and, for helpline, explicit opt-in consent (the user submits the form).
Data is never used for advertising or sold.

## 4. Retention

| Store | Default (code) | When enabled | Enforcement |
|---|---|---|---|
| Audit (`audit_records` + JSONL) | `AUDIT_RETENTION_DAYS=0` (keep forever — today’s behavior, demo-identical) | `AUDIT_RETENTION_DAYS=90` | SQLite: `DELETE WHERE timestamp < now() - AUDIT_RETENTION_DAYS` on startup + on each write batch; JSONL: prune on startup (idempotent, no background thread) |
| Sessions | `SESSION_RETENTION_DAYS=30` (separate from `SESSION_TTL_SECONDS=1800` + `SESSION_MAX_TURNS=10`) | Same value | Lazy purge on init and on every get/append alongside TTL eviction |
| Helpline registrations | No automatic purge in code | Proposal `365 days` — approve with counsel | Operator deletes or rotates the JSONL file per schedule |

All retention paths are **off or equal to current behavior by default**; the
demo (`DEMO_MODE=true`, anonymous user) is unchanged until the operator flips
the switches. See `docs/production_readiness/retention_policy.md` for the
operator runbook and `docs/production_readiness/amendments/01_PRIVACY_GOVERNANCE_2026_08_21.md` for reversible defaults.

## 5. PII handling

- **Local-only.** Audit, session, and helpline data never leaves the host and
  is never sent to an external service (AGENTS.md §4 invariant).
- **Write-time redaction (when enabled).** With `PII_REDACTION_ENABLED=true`,
  stored audit query text is scrubbed before persisting: Bangladeshi mobile
  numbers (`+880`/`01` including Bengali digits `০-৯`), email addresses, and
  name-adjacent patterns (`নাম:` / `name:`). Regex-based, best-effort — never
  claimed perfect. User-visible answers are never altered by redaction.
- **Default:** `PII_REDACTION_ENABLED=false` (verbatim, today’s behavior).
  Flip to `true` after reviewing `backend/app/core/redaction.py` and
  `backend/tests/test_redaction.py`.

## 6. Deletion and data-subject rights

- On Controller request, the Processor will delete the Controller’s audit,
  session, and helpline records within [30] days and confirm in writing.
- Users may request deletion of their helpline registration by contacting
  `[ support email / helpline 16123 ]`.
- Audit/session deletion is a bounded `DELETE WHERE timestamp < …` — no
  background job, no external propagation. Backups, if any, are the
  Controller’s responsibility and must be handled per the same retention.

## 7. Security

- Host-level filesystem permissions on `backend/app/logs/` and `backend/data/`.
- No external PII processor; WAL-mode SQLite with per-call connections.
- Request IDs and structured JSON logging for incident traceability (no PII in
  log levels themselves beyond the scrubbed query text when redaction is on).

## 8. Subprocessors

**None.** The System processes data locally only. Adding any subprocessor
(e.g., external vector DB, analytics sink) requires a new dated amendment and
Controller consent per `docs/production_readiness/README.md`.

## 9. Breach and compliance

- Bangladesh **Personal Data Protection Ordinance 2025 (No. 61 of 2025)**,
  gazetted 2025-11-06, is the reference framework (in force ~May 2027 for
  the fines regime). The Processor provides the technical means (local-only
  storage, retention purge, PII redaction, static privacy policy at `/privacy`)
  but does not warrant regulatory compliance — Controller and counsel determine
  applicability.
- The Processor will notify the Controller without undue delay on becoming
  aware of a personal-data breach affecting Controller data.

## 10. Contact and review

- Technical contact: `[ email ]`
- Privacy page: `/privacy` (static, matches site design; linked from footer)
- This template should be reviewed annually or when retention/PII settings,
  storage backends, or subprocessors change.

---

*Template version: 2026-08-21 (T1-04). Reversible via config: set
`AUDIT_RETENTION_DAYS=0` and `PII_REDACTION_ENABLED=false` to restore today’s
keep-forever, verbatim behavior, or `git revert <T1-04 commit>` for a bounded
code revert.*
