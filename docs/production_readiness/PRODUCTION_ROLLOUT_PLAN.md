# KrishokChat — Production Rollout Plan

**Status:** ADVISORY PLAN — nothing here changes code until a task executes it.
**Date:** 2026-08-17
**Audience:** the researcher (approver) + future executing agents.
**Companion docs:** `docs/production_readiness_roadmap.md` (Tier 0/1/2 system, amendment process), `docs/production_readiness/README.md` (execution rules), `docs/business_model_implementation_plan.md`.

> This plan answers: *"if we take KrishokChat to production now, what do we do, one by one?"* All internet research was done today (Aug 2026) by five parallel research agents; key sources are cited inline. Items in **Phase 0** are local-only, additive, reversible, need **no researcher intervention**, and respect every hard rule in `AGENTS.md`. Phases 1–3 need your decisions (Section 7).

---

## 0. Principles

1. **The demo never breaks.** Every change is additive, switch-gated with the current behavior as default, and committed as one bounded commit that a revert can undo. The golden replay (46/46) + full test suite (246 passed) are the gate on every step.
2. **Tier conflicts go through amendments.** Any work that conflicts with a hard rule (e.g., auth gating, multi-tenancy) waits for a dated amendment in `docs/production_readiness/amendments/` — exactly as the roadmap already defines.
3. **No fabrication.** Every number below is either verified in this repo or sourced from today's research (links inline). Anything unverified is flagged.
4. **Lean.** One engineer, low budget. Research consensus: a single VPS runs this stack for $25–60/mo; a GPU only becomes necessary at ~10 concurrent users.

---

## 1. Current state (verified against code, 2026-08-17)

### Already solid (Tier 0 complete)
| Capability | Where |
|---|---|
| Layered ports/adapters architecture | `backend/app/{application,domain,ports,infrastructure}` |
| Fail-closed safety router (6 categories, 16123 redirect), verifier with dosage claims | `safety.py`, `qa_pipeline.py` |
| Replaceable LLM client (OpenRouter/Gemini/Ollama) + separate local/remote timeouts | `infrastructure/llm/factory.py`, `config.py` |
| Provider failover chain + circuit breaker (off by default) | T0-06 |
| API versioning `/api/v1/*` + API-key auth + rate limiting + pagination (off by default) | T0-07 |
| SQLite foundation (WAL, migrations), audit + sessions adapters, telemetry, request-IDs, JSON logging | T0-01…T0-05 |
| CI (3 jobs), pytest 246 passed / 7 skipped, golden replay 46/46 | `.github/workflows/ci.yml`, `scripts/replay_golden.py` |
| Precomputed RAG indexes (BM25+dense, RRF), auto BM25 fallback | `infrastructure/retrieval/` |
| `/health` liveness, scoped CORS (`cors_origins`), Supabase auth lane (additive, non-gating) | `main.py`, `config.py` |

### Verified gaps (local analysis + today's research)
- **Python 3.11 is near EOL** — current stable is 3.14.7, maintained 3.13.15 (python.org). Upgrade is a Phase-1 decision.
- Backend bundles **torch + ultralytics + sentence-transformers (~3 GB)** even for text-only requests (roadmap §2 already notes this).
- No `/readyz` readiness check (only `/health`); no startup config validation warnings.
- **No SSE heartbeat** in `/api/qa/stream` — every proxy hop with an idle timeout (Next proxy `proxyTimeout: 300000`, Caddy/Nginx later) can drop a quiet generation. (Research: heartbeat ≤15–30s is mandatory once proxies sit in front — tianpan.co 2026-06.)
- No consistent JSON error envelope; FastAPI defaults can leak stack traces when `debug` is mis-set.
- `/docs`, `/redoc`, `/openapi.json` always exposed.
- **Local lane has no concurrency cap** — several parallel `model=krishokchat-4b` requests would thrash CPU (research: CPU cannot sustain >2–4 concurrent generations at 5 tok/s).
- Demo cache key lacks corpus/model versioning (research: versioned cache namespace — invalidate on corpus rebuild).
- `.env.example` is good but missing newer fields (SOIL_RELEASE_DIR, ML_ASSETS_DIR, RAG_* paths, SUPABASE_JWKS_URL, DOCS_ENABLED, READINESS_STRICT, LOCAL_LLM_MAX_CONCURRENCY, CORPUS_VERSION, …).
- No dependency audit artifacts (pip-audit / npm audit), 10 stray `print(` in backend.
- Frontend: no `output: "standalone"`, no bundle budget in CI, no security headers config, no PWA, no error monitoring, no `next/font` Bengali optimization confirmed, rewrites-based API proxy works but has no heartbeat.
- No log rotation / retention policy for the audit JSONL + SQLite; no backup routine.
- Secrets live in plain `.env` (fine for dev; prod needs encrypted store) — research: SOPS+age is the zero-infra ladder (novvista.com/2026).
- **Bangladesh legal update:** the Data Protection Act 2023 was superseded by the **Personal Data Protection Ordinance 2025 (No. 61 of 2025)**, gazetted 2025-11-06, effective immediately except the fines regime (≈May 2027). Fines eventually 1–5% of annual BD turnover (bdlaws.minlaw.gov.bd/act-1574.html). Compliance items are in Phases 1–3.
- Golden suite is QA-pair-heavy; research (GaRAGe, ACL 2025) says frontier systems over-answer — **add unanswerable/refusal/injection cases**.
- No injection red-team suite in CI; indirect prompt injection via retrieved docs is OWASP GenAI LLM Top 10 2026 #1 (genai.owasp.org).

---

## 2. Phase 0 — LOCAL SAFE HARDENING (no intervention needed — executable now)

> **Status: COMPLETE (P0-1 … P0-14, all committed, all gates green).**
> 273 passed / 7 skipped / 79 subtests; golden replay 50/50 invariants PASS
> (46 original + 4 prompt-injection); `pnpm build` clean. Details + open
> questions: `docs/refactor/PROJECT_HANDOFF.md` "Phase 0" entry.

Every item: additive, single bounded commit, default behavior unchanged, verified by full suite + build + golden replay. Order = impact.

### P0-1  Readiness endpoint `/readyz` — ✅ `bc28bbe` (tests in `test_health_readiness.py`)
- Add `GET /readyz` next to `/health`: checks RAG index files exist, dense index available or BM25 fallback, SQLite DB writable, local GGUF/LoRA presence (informational), configured providers have keys. Returns `{status, checks[], degraded[]}` — **always 200 by default** (demo-safe); `READINESS_STRICT=true` turns failures into 503 (for load balancers later).
- Files: `backend/app/api/extras.py` or new `backend/app/api/health.py` + tests + `.env.example` (`READINESS_STRICT=false`).

### P0-2  SSE heartbeat — ✅ `cfa0f15` (test_sse_heartbeat.py)
- Emit `: keepalive\n\n` comment every ~15s in `/api/qa/stream` (and any other stream endpoints). Survives every proxy idle timeout on the path; invisible to the SSE parser.
- Files: `qa.py` stream generator + test that counts heartbeat lines.

### P0-3  Error envelope + prod-safe exceptions — ✅ `456fa04` (test_exception_envelope.py)
- Global exception handlers: unhandled errors → `{error: "internal_error", request_id}` (no traceback when `debug=false`); keep FastAPI validation errors as-is; ensure `X-Request-ID` is echoed on error responses.
- Files: `backend/app/main.py` (or `api/middleware/errors.py`) + tests.

### P0-4  Config surface audit + startup validation — ✅ `c5f1dcb` (test_bootstrap_checks.py)
- Sync `.env.example` with every `Settings` field (including the missing ones listed in §1). Add startup validation that logs WARNINGs (never fails the demo) when: RAG index/corpus paths missing, dense index missing, DB dir unwritable, local model files absent, provider keys absent while provider requires one.
- Files: `config.py`, `.env.example`, small `core/bootstrap_checks.py` + tests.

### P0-5  Docs toggle — ✅ `bd8059f`
- `DOCS_ENABLED=true` default; when false, hide `/docs`, `/redoc`, `/openapi.json` (404). One line in `create_app`.
- Files: `main.py`, `.env.example` + test.

### P0-6  Local-lane concurrency cap — ✅ `98e77b9` (test_local_lane_concurrency.py; wait-queued, not 429)
- `asyncio.Semaphore(LOCAL_LLM_MAX_CONCURRENCY=2)` around local generations only (model=krishokchat-4b); saturated requests get `429` + `Retry-After` (or wait-queued — pick simplest: 429). Remote lane untouched.
- Files: `qa_pipeline.py`/container wiring + config + tests.

### P0-7  Cache key versioning — ✅ `19fc060`
- Add `CORPUS_VERSION` (default `"2026-08"`) to the demo-cache key (`key_for(query, crop, disease, model, corpus_version)`); bump invalidates all cached answers on corpus rebuild. Golden replay must still pass (replay uses its own fixture).
- Files: `infrastructure/cache/demo.py`, `qa_pipeline.py`, config + tests.

### P0-8  Frontend security + asset caching headers — ✅ `d8d1dd0` (no custom Cache-Control: Next 16 serves its own immutable static headers)
- `next.config.ts` `headers()`: `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY`, `Permissions-Policy` minimal; `Cache-Control: public, max-age=31536000, immutable` for `/_next/static/*` (content-hashed). **No CSP yet** — speech/SSE break risk; revisit in Phase 1 with research findings.
- Files: `frontend/next.config.ts` + build verification.

### P0-9  Dependency audit report — ✅ `35c3097` (backend 0 vulns / 134 pkgs; frontend 1 high transitive build-time `nanoid` via postcss — unreachable, Phase 1 W-6)
- Run `pip-audit` (or `uv`-equivalent) + `npm audit --omit=dev`; write `docs/production_readiness/dependency_audit_2026-08-17.md` with findings. Fix only clearly-safe patches, **after verifying the new version on the internet** (AGENTS §2.7). No fixes → report only.

### P0-10  Golden suite extension (refusal + injection cases) — ✅ `c790753` (50 items: 46 original + 4 injection; all invariants PASS)
- Add curated unanswerable / refusal / basic prompt-injection cases to the golden fixture (research: GaRAGe — systems over-answer; OWASP GenAI 2026 #1). Existing 46 must stay green; new cases must assert the fail-closed path.
- Files: golden fixtures + `replay_golden.py` documentation.

### P0-11  `print(` → logger cleanup (10 found) — ✅ no-op, justified (all 10 live in legacy CLI build/smoke scripts under `services/advisory/`; request-path code is logger-only; AGENTS.md §5.1 forbids reworking shims)
- Replace with `logger` where they sit in app code (scripts may keep them).

### P0-12  Production run scripts + README section — ✅ `c4d6549` (`scripts/start_prod.ps1` + `logrotate.krishokchat` + README "Production Deployment")
- `scripts/start_prod.ps1` (uvicorn with `--proxy-headers`, `--timeout-graceful-shutdown 30`, `--limit-concurrency`), README "Running in production" section, log rotation notes (logrotate sample for JSONL/SQLite). Not executed here — ready for Phase 1.

### P0-13  Retention policy doc — ✅ `c4d6549` (`docs/production_readiness/retention_policy.md`; `AUDIT_RETENTION_DAYS=90`, app never auto-deletes)
- One-pager: audit JSONL/SQLite retention (recommend 90d default, config `AUDIT_RETENTION_DAYS`), phone numbers (helpline registrations — masking), voice audio (never stored server-side today — keep it that way). Policy doc + optional purge script (off by default).

### P0-14  AGENTS.md/handoff notes — ✅ this commit (`PROJECT_HANDOFF.md` Phase 0 entry; full task board marked above)

> **Live verification (P0 build, 2026-08-18):** backend :8000 + frontend :3100
> exercised end-to-end — safe QA (5 sources), banned-chemical refusal, prompt-
> injection refusal, off-topic redirect, SSE agent trace (safety → retrieval →
> generation → verifier → final), photo classify (Potato 99.98%), `/api/v1/qa`
> mirror, all 17 UI routes 200 with P0-8 headers, proxied QA round-trip 9 s.
> `/api/history` 401 without a Supabase token is BY DESIGN (premium lane,
> amendment 15).
- `docs/refactor/PROJECT_HANDOFF.md` lines for Phase 0; task board marks.

**Phase 0 gate after each commit:** `uv run pytest tests -q` (246+ passed), `pnpm build`, golden replay 46/46+new.

---

## 3. Phase 1 — LAUNCH (needs your decisions; amendments where rules conflict)

### 3.1 Decisions needed first (see Section 7)
Budget, CPU vs GPU, provider, domain, telemetry backend, error monitoring, rate-limit posture, retention, Python 3.13 upgrade, Tier-1 amendments.

### W1  Deployment kit (decision: Docker vs systemd; provider)
- Dockerfiles (multi-stage; backend slim where possible), `.dockerignore`, `docker-compose.yml` (backend, frontend, caddy; llama-server on the GPU/CPU box), `Caddyfile` — auto-HTTPS, `flush_interval -1` (Caddy issue #3765 — mandatory for SSE), long read timeouts, HSTS, gzip.
- GitHub Actions CD: OIDC federation, actions pinned to SHAs, gitleaks, build → GHCR `:sha` tags → SSH → `compose pull && up -d`; rollback = previous tag; migrations run before restart (research: deploytovps/dchost patterns).
- Alternative if no Docker: systemd units + rsync symlink deploy (research: lighter, genuinely zero-downtime for `node server.js`).

### W2  Runtime upgrade
- Python 3.13 (3.11 near EOL), uvicorn 0.52.3, Node 24 LTS, Next.js 16.3.x stays. **Verify every dependency against 3.13 via official release notes before pinning** (AGENTS §2.7).

### W3  Observability (decision: Phoenix vs Langfuse vs none-yet)
- `opentelemetry-python` manual spans per pipeline stage (safety/retrieval/generation/verifier/cache hit), token + cost + latency attributes. OTel GenAI conventions are still "Development" (renames expected) — instrument against current names, tolerate renames (research: semantic-conventions-genai repo, v1.42.0+).
- Research guidance: Langfuse = best UI, MIT, but Postgres+ClickHouse+Redis+S3; Phoenix = single process, OTel-native, but ELv2. For a 2-process constraint: **Phoenix** (or manual JSONL → dashboard later).
- Metrics to track: time-to-first-token, stage latency, tokens, cost, refusal rate, retrieval hit rate, cache hit rate.

### W4  Security hardening
- TLS/HSTS via Caddy; never expose FastAPI/llama-server ports (bind 127.0.0.1).
- CORS: explicit origins only (already scoped — verify list before prod).
- Secrets: SOPS + age keys in repo, real values in GH Actions Environments; rotate OpenRouter/Gemini keys quarterly; gitleaks in CI (research: OWASP secrets cheat sheet, HashiCorp CI/CD guidance).
- API keys: `API_KEY_ENABLED=true` for machine users; `RATE_LIMIT_ANON_ENABLED=true` (60/min) for anonymous web (decision).
- Uploads: re-encode images via Pillow (strip EXIF, recompress) before ultralytics; enforce `VISION_MAX_IMAGE_BYTES` (already exists) + dimensions cap (OWASP API4).
- JWT: enforce ES256-only `alg` pinning on JWKS verification (check current impl in `auth.py`), short token lifetime.
- PII: scrub phone-number patterns at index build time; never index helpline registrations; output filter for PII (OWASP GenAI #2).
- LLM response as untrusted input: validate before render (OWASP API10 / GenAI #10).

### W5  Data & backups
- Supabase: nightly `pg_dump --format=custom` via session pooler → off-site bucket (R2/B2), monthly restore drill; PITR only if needed ($100/mo) (research: Supabase snapshots not downloadable).
- SQLite/audit: logrotate daily, 30–90d retention, off-box copy with the dump.
- RAG index = build artifact: rebuild in CI from versioned corpus, ship with release; corpus stays in git/object storage as source of truth.

### W6  Model serving (decision: CPU vs GPU)
- CPU launch (2–4 concurrent): llama-server already tuned for this repo; add `--parallel`/continuous batching per box; benchmark with `llama-batched-bench` (research: prompt-eval is the bottleneck; prefix caching cuts TTFT for shared system prompts).
- 10+ concurrent: GPU (RunPod 4090 ~$250/mo, Hetzner GEX44 €212/mo, Vast.ai market) with llama-server `-np 8–12`, quantized KV cache; vLLM only if that saturates (research: vLLM wins 3–16× at concurrency 8+).
- OpenRouter = fallback only (failover chain already exists); local-first routing cuts cost to near-zero.
- Model swap gate: golden replay + canary questions must pass before any GGUF/version change; GGUF metadata verification (rule 23 in paper AGENTS).

### W7  Frontend production build
- `output: "standalone"` + copy `public/` and `.next/static` (research: −80–90% deploy size); `next start` stays for dev.
- Bundle budget CI (`size-limit`): first-load JS < 200 KB gzip (research: 3G case study LCP 7.2s→2.1s at <100 KB).
- Bengali fonts via `next/font` (Hind Siliguri or Noto Sans Bengali, OFL, 2–3 weights, never subset to Latin) (fonts.google.com).
- PWA shell via Serwist (Next 16 official guidance, 2026-07): precache shell + fallback page; **no offline chat** (backend-dependent); never cache `sw.js`.
- SSE UX: heartbeat-aware "reconnecting…" state, auto-retry with backoff, abort on unmount.
- Error monitoring: Sentry free tier or GlitchTip self-host (~512 MB RAM, MIT) — decision; instrument SSE connect/disconnect, TTFT, aborted generations (research: skitrate 2026 comparison, selfhosting.sh).
- WCAG 2.2 pass: touch targets 44–48 px, `aria-live` on stream status, pause >3s audio, plain-language Bengali (W3C WCAG 2.2).

### W8  Bangladesh compliance (mostly you + a lawyer; agent provides checklist)
- Personal Data Protection Ordinance 2025: data mapping, consent language (Bengali), breach notification plan, retention limits, DPIA for helpline phone numbers (bdlaws.minlaw.gov.bd/act-1574.html).
- Company: RJSC Pvt Ltd (~BDT 18–25k), TIN, VAT/BIN (research: legaladvicebd).
- Google Play: developer verification (cert of incorporation + VAT cert) (support.google.com).

---

## 4. Phase 2 — AI OPERATIONS & GROWTH (30–90 days post-launch)

- **G1** Nightly canary: re-run golden + canary questions against live corpus; alert on retrieval hit-rate / refusal-rate drift (research: online drift via canary sets + sampled judging, not per-request).
- **G2** Eval pipeline: pin judge model + prompt version, temperature 0, two heterogeneous judges, small human calibration set (research: Eval-Pair Matrix — same-model judging biases groundedness).
- **G3** Red-team suite in CI: OWASP GenAI LLM Top 10 2026 cases; **indirect injection scan on retrieved content** (delimit retrieved data, re-affirm system instructions after context); evaluate Prompt Guard 2 (86M) on the input path (license/version check first; research: USENIX 2026 — direct-only injection classification misses indirect).
- **G4** Cost controls: per-user/per-IP daily token caps, spend alerts on OpenRouter, local-first routing (already the plan), token accounting dashboards (W3).
- **G5** Corpus pipeline: provenance hashes at ingestion, zero-width/variation-selector stripping, versioned rebuild in CI (OWASP RAG cheat sheet).
- **G6** Multi-tenancy / roles for the B2B lane — **T1-01 amendment territory** (already drafted in the roadmap).
- **G7** Human review lane for verifier-flagged advisories (roadmap admitted gap; decision on review UI).
- **G8** Semantic cache: research says 15–25% hit rate + wrong-answer risk — **skip unless measured need** (tianpan.co 2026-04).
- **G9** Voice/ASR ops: Groq quota management, audio retention policy (never store by default), Bengali ASR accuracy eval.

---

## 5. Phase 3 — BANGLADESH MARKET (90 days+)

- **M1** Government partnership: DAE/AIS MoU path (precedent: Syngenta–DAE MoU 2024, CABI–DAE e-Extension 2025); content licensing for DAE/BARC/BRRI/CABI sources already in the corpus — **verify license terms**; complement (not compete with) BARC Khamari + DAE Krishoker Janala (both static, no AI diagnosis).
- **M2** Krishi Call Center 16123: verified 92,094 calls FY2025–26 (Jul–Jun), peak 10,141 in Apr 2026, 25 paisa/min, 4–7 officers with a missed-call problem (bssnews, dhakatribune) — AI triage + warm handoff is a real pitch.
- **M3** Payments: UddoktaPay (~BDT 200/mo, no trade license) to bootstrap → bKash (~1.5% + BDT 1,200/yr) / Nagad (~1.45%) / SSLCommerz (2.5% + BDT 25,500 setup) when revenue justifies (developer.bka.sh, sslcommerz.com).
- **M4** SMS/USSD fallback: BTRC-listed aggregators only; GP Corporate Messaging BDT 0.30–0.50/SMS; TVAS registration for telecom-adjacent services (research: telerivet BTRC compliance guide) — addresses the 46% internet-penetration gap (GSMA).
- **M5** Low-bandwidth UX: PWA shell (W7) + optional SMS digest; mobile-first everywhere (4G covers 99% but smartphones only 72.4% of households, rural 69% — BBS 2025).
- **M6** Positioning: verified-content advisory + AI disease diagnosis + safety pipeline is an open gap vs iFarmer (agri-fintech/marketplace, $65.6M revenue 2025) and static govt apps — the business-model doc already frames this.

---

## 6. Risk register (top 10)

| # | Risk | Mitigation |
|---|---|---|
| 1 | CPU can't serve 10 concurrent users (~50 tok/s needed) | Phase-1 sizing decision; GPU upgrade path priced |
| 2 | Prompt injection (direct + indirect) | P0-10 red cases; G3 suite; retrieved-content delimiter + scan |
| 3 | Farmer PII exposure (PDP Ordinance 2025 fines 1–5% turnover) | PII scrub, retention policy, encryption at rest, breach plan (W4/W5/W8) |
| 4 | OpenRouter outage / cost spike | Failover chain (exists), local-first routing, spend alerts |
| 5 | Single-VPS SPOF | Backups off-site, image-tag rollback, /readyz for LB |
| 6 | Bengali model quality drift | Golden + canary gate on every model swap; GGUF metadata verification |
| 7 | Python 3.11 EOL + dep rot | W2 upgrade; quarterly dependency audits (P0-9 repeats) |
| 8 | Demo regression during rollout | Additive rule, one-bounded-commit rule, golden gate, Tier amendments |
| 9 | Content licensing dispute (DAE/CABI docs) | M1 license verification before commercialization |
| 10 | Streaming reliability through proxies | P0-2 heartbeat; W1 proxy config; W7 reconnect UX |

---

## 7. Decisions needed from you (to start Phase 1)

| # | Decision | Recommendation | Blocks |
|---|---|---|---|
| D1 | Monthly budget & CPU vs GPU at launch | CPU ($46/mo Hetzner CPX41) for 2–4 concurrent; GPU (~$250/mo) for 10+ | W1, W6 |
| D2 | Hosting provider | Hetzner (EU, cheapest) vs DO/Vultr SG (50–90ms BD) vs Pico Public Cloud (BD residency, pricing non-public) | W1 |
| D3 | Domain + email | — | W1 |
| D4 | Docker vs systemd deploy | Docker + GHCR sha tags (rollback story) unless you prefer minimal | W1 |
| D5 | Telemetry backend | Phoenix (single process) now; Langfuse if UI/prompt mgmt matters | W3 |
| D6 | Error monitoring | GlitchTip self-host (MIT, ~512MB) or Sentry free | W7 |
| D7 | Rate limits on for anonymous prod traffic | Yes: 60/min IP (already built, flip the switch) | W4 |
| D8 | Audit retention | 90 days default (config-gated) | P0-13, W5 |
| D9 | Python 3.13 + dep bumps | Yes, after per-dep version verification | W2 |
| D10 | Tier-1 amendments (multi-tenancy, model-serving separation, deployment kit, privacy, safety depth) | Approve when their tasks start | Phase 2+ |

---

## 8. Next action

**Phase 0 (P0-1 … P0-14) can start immediately — no intervention required.** Recommended execution: two batches of bounded commits (P0-1…P0-7 backend hardening; P0-8…P0-14 frontend/ops hygiene), each gated by `pytest` + `pnpm build` + golden replay. Then bring me the decision table (Section 7) and we open Phase 1.