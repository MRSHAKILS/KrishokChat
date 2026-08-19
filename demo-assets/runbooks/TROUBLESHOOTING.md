# Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Every question returns "জ্ঞানভান্ডারে নেই" + 16123 | LLM provider unreachable (fail-closed) | Check `OPENROUTER_API_KEY`, network. Cached demo questions still replay. |
| Normal questions refused while the provider is up | Stale code (pre-2026-08 classifier threshold) | Pull latest `safety.py`; the confidence demotion was removed (model confidence is unreliable). |
| `/api/detect` returns 400 | Non-image upload | Use a real photo; `expected/invalid-image.txt` is the negative test. |
| Tomato photo returns no diagnosis | No tomato/solanacea disease model is registered | That is the designed boundary — say so honestly. |
| Demo cache never hits | Cache file missing or old keys | `demo-assets/cached_responses.json` must exist with corpus-versioned keys (`\|\|\|<corpus>\|<query>`). Regenerate by re-answering curated questions with `DEMO_MODE=true`. |
| Local model option errors | `llama-server` not running / files missing | Start `scripts/start_krishokchat_local.ps1`; never use the truncated f16 GGUF. |
| Bengali mojibake in console | Windows cp1252 | `$env:PYTHONIOENCODING="utf-8"` before running Python. |
| `/api/safety/metrics` empty | No audit entries yet | Ask a few questions first; metrics come from the local audit log only. |
| Frontend build fails | Node/pnpm mismatch | `pnpm install` (pnpm 11.1.1); Next.js 16.3.0 requires modern Node. |

## Audit trail
Every classification decision (query, category, action, timestamp) appends to
`backend/app/logs/safety_audit.jsonl` — local file only, never external.