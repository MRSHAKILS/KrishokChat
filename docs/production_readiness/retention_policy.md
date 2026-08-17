# Audit Log Retention Policy

Status: Phase 0 (P0-13). Applies to the safety/QA audit trail produced by the
pipeline (JSONL or SQLite under `backend/app/logs/`).

## Data subject

- `safety_audit.jsonl` (default `AUDIT_BACKEND=jsonl`) — every classification
  decision: query text, category, action, verifier flags, model, request ID,
  timestamps.
- SQLite audit records (same content, `AUDIT_BACKEND=sqlite`).

The audit trail is a **local, first-party artifact**. It is never sent to an
external service (AGENTS.md §4). Queries may contain farmer-supplied personal
details (names, village names, phone numbers in free text), so the trail is
treated as potentially personal data under the Bangladesh Personal Data
Protection Ordinance 2025 (No. 61 of 2025, in force ~May 2027).

## Retention window

- `AUDIT_RETENTION_DAYS` (default **90** days) is the configured window.
- The application itself **never auto-deletes** (read-path and write-path
  behavior are unchanged by P0; deletion is an operator action).
- The retention job below is the documented way to enforce the window.

## Enforcement (operator runbook)

### JSONL backend

```
# rotate + prune once a day (logrotate or cron):
# 1. rename:  safety_audit.jsonl -> safety_audit.2026-08-17.jsonl
# 2. keep the last N day-stamped files:
find backend/app/logs -name "safety_audit.*.jsonl" -mtime +$AUDIT_RETENTION_DAYS -delete
```

### SQLite backend

```
DELETE FROM audit_records WHERE ts < datetime('now', '-' || :days || ' days');
VACUUM;
```

(Run via the sqlite3 CLI or a small script; the audit table name follows the
schema in `backend/app/infrastructure/audit/sqlite.py`.)

## What is NOT covered

- Demo cache (`demo-assets/cached_responses.json`) — curated, precomputed
  content, not user data; managed by `DEMO_CACHE_MAX_ENTRIES`.
- Backend/app JSON logs (`LOG_LEVEL` rotation is the logrotate sample in
  `docs/production_readiness/logrotate.krishokchat`).
- Session history — TTL-bounded in-app (`SESSION_TTL_SECONDS`,
  `SESSION_MAX_TURNS`); SQLite sessions table is pruned by the same daily
  window if it grows.

## Future (Phase 1, W-7)

Automated purge: a small maintenance script/CI step enforcing the window
instead of the manual runbook, plus a `/readyz`-style age check when the audit
file exceeds the window. No change to the app write path.