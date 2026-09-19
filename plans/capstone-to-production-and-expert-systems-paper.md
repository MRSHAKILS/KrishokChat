# Capstone → Production + Expert Systems Journal — Incremental Execution Plan

**Repo:** `KrishokTech Advisory System` (`main` branch, origin `RaiyaanReza/KrishokTech-Agricultural-Advisory-System`)
**Date:** 2026-08-21
**Author:** blueprint pipeline (research → design → review)
**Statue:** ADVISORY — no code changes until a step's agent executes it
**Companion SSOTs:** `AGENTS.md` · `docs/refactor/ARCHITECTURE.md` · `docs/refactor/PROJECT_HANDOFF.md` · `docs/PRODUCTION_ROLLOUT_PLAN.md` · `docs/production_readiness_roadmap.md` · `paper/system_evolution_plan_2026/` · `docs/PAPER_POLICY.md`

> **One-line objective:** Transform the finished 7-day capstone demo into (a) a production-grade single-box service and (b) a submission-ready *Expert Systems* (Wiley) research paper — **incrementally, without ever breaking the demo**, verified after every step with three live servers.

---

## 0. Pre-Flight Context (what the planner read)

| Source | Signal |
|--------|--------|
| `ARCHITECTURE.md` | Layered `api → application → ports → infrastructure` with composition root in `container.py`. Safety before retrieval, fail-closed, one FastAPI + one Next process. Legacy `agents/` + `services/advisory/` are shims, do not extend. |
| `PROJECT_HANDOFF.md` | **Phase 0 (P0-1..P0-14) DONE**: `/readyz`, SSE heartbeat, error envelope, `DOCS_ENABLED`, local concurrency, cache versioning, audit/sqlite, sessions/sqlite, telemetry, failover, versioning+keys, CI+golden. **273 passed / 7 skipped / 79 subtests**, golden **50/50** (46+4 injections), `pnpm build` 21 routes. Remaining = Tier 1 (`T1-01..T1-05`) + P1 market/deployment work. |
| `PRODUCTION_ROLLOUT_PLAN.md` | Phase 0 done; Phase 1 = deployment kit / runtime upgrade / observability / security / data / model serving / frontend prod / compliance; Phase 2 = AI ops; Phase 3 = BD market. |
| `production_readiness_roadmap.md` | Tier 0 = safe now (done), Tier 1 = needs amendment, Tier 2 = research lane. Task docs in `docs/production_readiness/tasks/`. |
| Live tree audit (2026-08-21) | **Debt hotspots**: duplicate `krishoktech.f16.gguf` ≈ `model.gguf` (2.6 GB), 3× `Modelfile`, 3 demo media files duplicated at root + `frontend/public/`, 37 loose `scripts/*` + 26 `backend/scripts/*` + 27 `backend/ml_assets/rag_index/scripts/`, typo folder `capstone/poster deisgn`, spaces-in-path `dataset_release/Soil Moisture Detection/`, backend root stray `uvicorn-*.log` files, latex aux (`*.aux/.log/.dvi/.out/.nav/.snm/.toc`) committed in `capstone/`, untracked `scripts/test_soil*.py`. |
| `paper/system_evolution_plan_2026/` | Full 4→8 week research evolution: current scientific position, competitive landscape, 3 system concepts, evaluation matrix, verifier/abstention/dialect protocols, claim ledger, local-model amendment (14), auth amendment (15), premium lane (16). |
| `paper/done papers/` | Authoritative sources; `arXiv:2606.29243 v1` is **deprecated** per `PAPER_POLICY.md`. |
| Journal target | **Expert Systems** (Wiley) — system-track: requires reproducible benchmark, ablation, error analysis, safety evaluation, real data, ethics/limitations, artifact availability. |

### The 3-server verification invariant (used after EVERY step)

No step is green until **all three servers stay up and answer** from the **same working tree**:

| Server | URL | Probe | Must be |
|--------|-----|-------|---------|
| **Backend** | `http://localhost:8000` | `GET /health` → `{"status":"ok"}` + `GET /readyz` → `ready` or `degraded` (never 500) | 200 |
| **Frontend** | `http://localhost:3000` (and `:3100` if running) | `GET /` + `GET /chat` + `GET /detect` | 200 |
| **Local LLM** | `http://127.0.0.1:11434` or `:11435` (`LOCAL_LLM_BASE_URL`) | `ollama list` or `GET /api/tags` shows `krishoktech-4b` *if* local lane is enabled; otherwise **stub lane** must stay green without it | optional but never red |

Plus offline gates: `uv run pytest -q` + `pnpm build` + `python backend/scripts/replay_golden.py --assert-invariants` (50/50).

---

## 1. Design Principles for This Transition

1. **Demo never breaks.** Additive-only, switch-gated, one bounded commit per step. Default = current demo behavior. Revert = flip switch or `git revert <sha>`.
2. **One step = one PR = one agent = one gate.** No interleaving. No "while I'm here…" scope creep.
3. **Hygiene first, then structure, then production, then paper.** Cheap, safe deletions and renames land before any behavioral change. Paper work runs in parallel lane, never touching `backend/app/application` or routes.
4. **Three-server check after every step.** Live backend + frontend + local model probe, plus offline suite. Gate fails → STOP, do not expand scope.
5. **No fabrication.** Every metric, claim, figure comes from `backend/ml_assets/**` or a logged experiment. `TODO` > fake number.
6. **Incremental load.** ≤ 3 files of blast radius per hygiene step; production steps behind feature flags with separate latency budget.

---

## 2. Dependency Graph & Parallelism

```
H1 ─┐
H2 ─┤
H3 ─┤──► H8 (hygiene checkpoint) ─► S1 ─► S2 ─► S3 ─► S6 (structure checkpoint) ─┐
H4 ─┤                                                      ├─► P1 ─► P2 ─► P3 ─► P6 ─► P10 (prod checkpoint)
H5 ─┤                                                      │    (P4,P5 parallel after P2)
H6 ─┤                                                      │
H7 ─┘                                                      └─► R1 ─► R2 ─► R3 ─► R4 ─► R5 ─► R6 ─► R7 (paper checkpoint)
                                                                    (R2,R3 parallel; R5 after R4)
```

*Legend:* `H` = Hygiene, `S` = Structure, `P` = Production (Tier 1 + Phase-1 deployment), `R` = Research/Paper. No cross-lane file overlap until checkpoints, so lanes can interleave with care but default is serial within a lane.

---

## 3. Full Step Catalog (26 steps, 4 phases)

### PHASE H — HYGIENE & DE-RISK (cheap, safe, no behavior change)

| Step | Title | Parallel? | Model |
|------|-------|-----------|-------|
| **H1** | Purge stray runtime logs & ignored artifacts from working tree | serial (first) | default |
| **H2** | De-duplicate GGUF: single canonical `krishoktech.f16.gguf` + symlink/hardlink alias | after H1 | default |
| **H3** | De-duplicate demo media: single source in `demo-assets/`, alias in `frontend/public/` | after H1 | default |
| **H4** | Consolidate 3× `Modelfile` → one canonical + docs pointer | after H1 | default |
| **H5** | Archive latex build litter (`*.aux/.log/.dvi/.out/.nav/.snm/.toc`) + typo folder `poster deisgn` | after H1 | default |
| **H6** | Normalize `dataset_release/` path with spaces → `soil-moisture-detection` via `git mv` + shim | after H1 | default |
| **H7** | Sweep `__pycache__`/`.pytest_cache` local litter + extend `.gitignore` + move untracked soil scripts | after H1 | default |
| **H8** | **Hygiene checkpoint:** full verification (3 servers + suite + golden) + tag `hygiene-clean` | after H1..H7 | default |

### PHASE S — STRUCTURE REFINEMENT (folderization, still no behavior change)

| Step | Title | Parallel? | Model |
|------|-------|-----------|-------|
| **S1** | Consolidate `scripts/` sprawl → documented `tools/` taxonomy (moves, not rewrites) | after H8 | strongest |
| **S2** | Consolidate `backend/scripts/` + `backend/ml_assets/rag_index/scripts/` naming (`00_*` → descriptive) + index | after S1 | default |
| **S3** | Promote `frontend/public/assets` naming: fix `researchers image` (space) → `researchers` + redirect | after H8 | default |
| **S4** | Document canonical asset map (`docs/ARCHITECTURE_ASSETS.md`) + artifact pointer file | after S1..S3 | default |
| **S5** | Add repo hygiene tooling: `.editorconfig`, `.pre-commit-config.yaml` (lint only, not enforcing CI yet) | after S4 | default |
| **S6** | **Structure checkpoint:** verify no import path changed + 3-server + suite + golden | after S1..S5 | default |

### PHASE P — PRODUCTION HARDENING (Tier 1 + Phase-1 deployment kit — behavior is flag-gated)

| Step | Title | Depends | Amendment? | Model |
|------|-------|---------|------------|-------|
| **P1** | `T1-04` Privacy & retention operator (DPO 2025 alignment, purge script opt-in, masking) | S6 | needs `amendment: privacy_governance` | strongest |
| **P2** | `T1-01` Multi-tenancy + RBAC foundation (additive, anonymous demo untouched) | P1, needs `T0-01` done | needs `amendment: multitenancy_rbac` | strongest |
| **P3** | `T1-02` Model-serving separation (registry + ONNX path, still classification-only until verified detection) | P2 | needs `amendment: model_serving_separation` | strongest |
| **P4** | `T1-03` Deployment kit (Dockerfile + compose + Caddy + GHCR + SSH deploy + rollback) — **parallel after P2** | P2 | needs `amendment: deployment_kit` | default |
| **P5** | `T1-05` Safety depth (multi-turn safety context + red-team CI + verifier-flag review lane) — **parallel after P2** | P2 | needs `amendment: safety_depth` | strongest |
| **P6** | Frontend production build hardening (`output: standalone`, headers already done, bundle budget, PWA shell) | P2 | no (additive) | default |
| **P7** | Runtime upgrade: Python 3.13 + Node 24 + pinned dep verification per AGENTS §2.7 | P6 | no | default |
| **P8** | Observability lane: OTel manual spans per stage + token/cost dashboards (Phoenix recommended) | P2 | no | default |
| **P9** | Secrets & backup: SOPS+age for GH Actions, `pg_dump` + SQLite rotation drills | P4 | no | default |
| **P10** | **Prod checkpoint:** load-test 2–4 concurrent, failover drill, restore drill, golden+red-team CI green | P1..P9 | — | default |

### PHASE R — EXPERT SYSTEMS PAPER (parallel lane, never blocks demo)

| Step | Title | Depends | Model |
|------|-------|---------|-------|
| **R1** | Freeze paper SSOT: `paper/manuscript/` skeleton + claim ledger + `docs/PAPER_POLICY.md` enforcement | S6 | strongest |
| **R2** | Dataset & benchmark freeze: provenance manifests + 20k safety set + retrieval eval (hybrid/BM25/dense) — **parallel** | R1 | strongest |
| **R3** | Vision & RAG ablation matrix: run & log all experiments declared in `05_MINIMUM_EXPERIMENT_MATRIX.md` — **parallel** | R1 | strongest |
| **R4** | Human & dialect study: Bengali dialect + safety-judgment calibration set (per `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`) | R2,R3 | default |
| **R5** | Results synthesis: figures, tables, error analysis, limitations, reproducibility package | R4 | strongest |
| **R6** | Manuscript draft: full Expert Systems draft via custom writer 8-phase loop (Understand→Plan→Draft→3 reviewers→Merge→Rewrite×3→Polish) | R5 | strongest |
| **R7** | **Paper checkpoint:** internal review + artifact audit (reproducibility zip, HF dataset card, code release checklist) | R6 | strongest |

> **Total: 26 steps.** Longest serial chain: `H1→H8→S1→S2→S4→S6→P1→P2→P6→P7→P10` (11 steps). Paper lane `R1..R7` overlaps `P` after `S6` to compress calendar time without coupling.

---

## 4. Step Briefs (cold-start executable — every step lists its own context, tasks, verification, rollback)

### H1 — Purge stray runtime logs

**Context:** `backend/uvicorn-live.*`, `backend/uvicorn-startup.*`, `backend/app/logs/llama-server.*` litter the working tree outside the gitignored `backend/app/logs/` contract. They are ignored by `.gitignore: *.log` but pollute `git status --ignored` and confuse fresh agents. No code imports them.

**Tasks:**
- [ ] Delete `backend/uvicorn-live.log`, `uvicorn-live.out.log`, `uvicorn-live.err.log`, `uvicorn-startup.log`, `uvicorn-startup-err.log` (if present).
- [ ] Truncate or rotate `backend/app/logs/safety_audit.jsonl` ONLY if > 50 MB for hygiene measurement (keep `.gitkeep`, never delete the file itself).
- [ ] Verify `.gitignore` already covers `*.log` and `backend/app/logs/*` + `!backend/app/logs/.gitkeep` (no new rule needed; document if missing).

**Verification:**
```powershell
git status --ignored --short | Select-String "uvicorn"
# expect: no output (files gone)
uv run pytest -q  # 273 passed / 7 skipped
pnpm --dir frontend build  # 21 routes
python backend/scripts/replay_golden.py --assert-invariants  # 50/50
curl http://localhost:8000/health; curl http://localhost:8000/readyz; curl http://localhost:3000/ -I
```

**Exit:** stray logs gone, `git status` clean (except intentional untracked), all gates green.

**Rollback:** `git restore .` — files were ignored, no commit needed.

---

### H2 — De-duplicate GGUF

**Context:** `backend/ml_assets/gemma/krishoktech.f16.gguf` and `backend/ml_assets/gemma/model.gguf` are byte-identical (SHA256 `1D6273...84673`, 1.36 GB each = 2.6 GB waste). `config.py: gguf_path` defaults to `model.gguf`; `scripts/local_model.ps1` and `Modelfile` reference either. Large files are gitignored (`backend/ml_assets/gemma/*.gguf`) so change is local-only.

**Tasks:**
- [ ] Choose canonical: **`krishoktech.f16.gguf`** (descriptive) — keep it, remove `model.gguf` as a real file.
- [ ] Recreate `model.gguf` as a **hardlink** (or symlink on NTFS) to `krishoktech.f16.gguf` for backward compat: `fsutil hardlink create model.gguf krishoktech.f16.gguf` (preferred — same inode, no extra space).
- [ ] Verify hardlink: `fsutil hardlink list krishoktech.f16.gguf` must show both names; hashes still equal.
- [ ] Add note to `backend/ml_assets/gemma/README.md` (create if missing): "canonical is `krishoktech.f16.gguf`; `model.gguf` is a hardlink alias for legacy `gguf_path` default."
- [ ] Do NOT change `config.py` default yet (defer to S1 to avoid behavior change in hygiene phase).

**Verification:**
```powershell
Get-FileHash backend/ml_assets/gemma/krishoktech.f16.gguf
Get-FileHash backend/ml_assets/gemma/model.gguf
fsutil hardlink list backend/ml_assets/gemma/krishoktech.f16.gguf
# hashes equal, hardlink count = 2
uv run pytest -q; pnpm --dir frontend build; python backend/scripts/replay_golden.py --assert-invariants
# 3-server probe
```

**Rollback:** `del model.gguf; copy krishoktech.f16.gguf model.gguf` (re-duplicate).

---

### H3 — De-duplicate demo media

**Context:** Identical files at `D:/KrishokTech Advisory System/krishoktech_demo.gif` (20.7 MB) + `frontend/public/krishoktech_demo.gif` (same hash `DAF8A...30606`), same for `.mp4` and `.webp`. Root copies are legacy README embeds; frontend copies are served assets. `demo-assets/cached_responses.json` is already canonical for cache.

**Tasks:**
- [ ] Canonical source = `demo-assets/` — ensure `krishoktech_demo.{gif,mp4,webp}` live there (move root copies if not already there).
- [ ] Replace `frontend/public/krishoktech_demo.*` with **hardlinks** (or copy + note) to `demo-assets/` originals — saves ~42 MB and keeps both URLs working. Alternative: single source + `frontend/public` as hardlink (chosen — no build step change).
- [ ] Update `README.md` media paths to point to `demo-assets/` (keep relative links working on GitHub).
- [ ] Delete root duplicates after hardlink verified.

**Verification:**
```powershell
Get-FileHash demo-assets/krishoktech_demo.gif; Get-FileHash frontend/public/krishoktech_demo.gif
# hashes equal
pnpm --dir frontend build; curl http://localhost:3000/krishoktech_demo.gif -I  # 200
```

**Rollback:** `copy demo-assets/krishoktech_demo.* frontend/public/` + restore root.

---

### H4 — Consolidate Modelfiles

**Context:** Three files: `scripts/Modelfile` (1657 B), `backend/ml_assets/gemma/Modelfile` (same), `backend/ml_assets/gemma/Modelfile.krishoktech` (1416 B). Only one is needed; others drift.

**Tasks:**
- [ ] Canonical = `scripts/Modelfile` (repo-wide tooling location referenced by `scripts/local_model.ps1`).
- [ ] Diff `scripts/Modelfile` vs `backend/ml_assets/gemma/Modelfile` vs `Modelfile.krishoktech` — merge any delta into canonical, add header comment `# Canonical Modelfile — other copies are hardlink aliases, do not edit separately`.
- [ ] Replace `backend/ml_assets/gemma/Modelfile` and `Modelfile.krishoktech` with hardlinks to `scripts/Modelfile`.

**Verification:** diff empty, `ollama create` dry-run still resolves.

---

### H5 — Archive latex build litter + typo folder

**Context:** `capstone/Final Poster/latex/*.aux/.log/.dvi/.out` and `capstone/poster deisgn/latex/*.aux/.log/.nav/.snm/.toc` etc are committed build artifacts (should be gitignored). Also folder name `poster deisgn` is a typo that breaks scripts and confuses agents.

**Tasks:**
- [ ] Extend `.gitignore` with LaTeX litter: `*.aux`, `*.log` (already has `*.log`), `*.dvi`, `*.out`, `*.nav`, `*.snm`, `*.toc`, `*.fls`, `*.fdb_latexmk`.
- [ ] `git rm --cached` all committed `*.aux/.log/.dvi/.out/.nav/.snm/.toc` under `capstone/`.
- [ ] `git mv "capstone/poster deisgn" capstone/poster-design` — update any `scripts/write_poster.py`, `scripts/generate_*poster*.py` path literals that reference the old name (search `poster deisgn`).
- [ ] Keep `*.pdf` outputs (poster PDFs are deliverables).

**Verification:**
```powershell
git ls-files | Select-String "\.(aux|dvi|nav|snm|toc)$"  # expect: empty
Test-Path "capstone/poster-design"  # True
uv run pytest -q; pnpm --dir frontend build
```

**Rollback:** `git revert <sha>` — renames are tracked.

---

### H6 — Normalize dataset path with spaces

**Context:** `dataset_release/Soil Moisture Detection/` contains spaces, breaking shell quoting and `Path()` joins. Official release lives in `dataset_release/soil_moisture/` (small, committed); the spaced folder is gitignored (`dataset_release/Soil Moisture Detection/dataset/raw/` etc per `.gitignore:72-75`) but still pollutes the tree and `glob`.

**Tasks:**
- [ ] `git mv` or local `Move-Item` the directory to `dataset_release/soil-moisture-detection/` (kebab-case). Since its contents are gitignored, this is a local filesystem move — update `.gitignore` lines 72-75 to the new path.
- [ ] Add a **shim**: leave a one-line `README.md` at the old path location with `Moved to ../soil-moisture-detection/` for one release, then remove.
- [ ] Search `dataset_release/**/Soil Moisture` references in `scripts/build_soil_release.py`, docs, and `frontend/public/assets/soil_samples` — update to new path.

**Verification:**
```powershell
Test-Path "dataset_release/soil-moisture-detection"  # True
Select-String -Pattern "Soil Moisture Detection" -Recurse  # expect: 0 hits after update
```

**Rollback:** `Move-Item soil-moisture-detection "Soil Moisture Detection"` + revert `.gitignore`.

---

### H7 — Sweep pycache + untracked soil scripts

**Context:** `backend/tests/scripts/test_soil.py` and `test_soil_all.py` are untracked (`?? scripts/test_soil*.py` in `git status`). `__pycache__` and `.pytest_cache` are ignored but accumulate locally.

**Tasks:**
- [ ] Move `scripts/test_soil.py` + `test_soil_all.py` → `backend/tests/test_soil_probe.py` or `backend/scripts/` as appropriate, or delete if superseded by `backend/tests/test_soil.py` (check diff first).
- [ ] `Remove-Item -Recurse -Force backend/**/__pycache__`, `.pytest_cache` (local only, ignored).
- [ ] Verify `.gitignore` already has `__pycache__/`, `*.py[cod]`, `.pytest_cache/` (it does).

**Verification:** `git status --short` shows only intentional untracked moved files; suite green.

---

### H8 — Hygiene checkpoint

**Gate (must be 100% before S1):**
```powershell
git status --ignored --short  # only .venv/, backend/data/, ml_assets/*.gguf etc ignored
uv run pytest -q              # 273 passed / 7 skipped / 79 subtests
python backend/scripts/replay_golden.py --assert-invariants  # 50/50
pnpm --dir frontend build     # 21 routes, zero type errors
# 3-server live probe (run while backend+frontend+llama are up):
curl http://localhost:8000/health
curl http://localhost:8000/readyz
curl http://localhost:3000/ -I
curl http://localhost:3000/chat -I
curl http://localhost:3000/detect -I
# optional: ollama list | Select-String krishoktech-4b
```
- [ ] Tag: `git tag hygiene-clean-2026-08-21 && git push origin hygiene-clean-2026-08-21`

---

### S1 — Consolidate `scripts/` sprawl → `tools/` taxonomy

**Context:** Three script homes with overlapping purpose: `scripts/` (37 files — capture, poster, soil, build), `backend/scripts/` (26), `backend/ml_assets/rag_index/scripts/` (27 with `00_*` prefixes). No index; fresh agents guess where to run what. Nothing may break imports (scripts use `sys.path` relative to old locations).

**Tasks:**
- [ ] Create `tools/` taxonomy (all moves via `git mv`, keep old path as shim for one release if imported):
  ```
  tools/
  ├── rag/              ← from backend/ml_assets/rag_index/scripts/
  ├── vision/           ← from backend/ml_assets/vision/scripts/
  ├── demo/             ← capture_*.js, perfect_*.py, render_demo_video.py
  ├── poster/           ← generate_*poster*.py, write_poster.py, latex/
  ├── ops/              ← start_*.ps1, local_model.ps1, supabase_test_user.ps1
  └── soil/             ← build_soil_release.py
  ```
- [ ] Keep `backend/scripts/` for **runtime-adjacent** scripts that import `app.*` (`replay_golden.py`, `test_*.py` that hit the container) — move only the non-runtime capture/poster scripts out.
- [ ] Add `tools/README.md` table: script | purpose | how to run | env needed.
- [ ] Update `README.md` "Scripts" section + `docs/` references to new paths. Add `tools/ ->` alias comments at old locations for one release if needed.

**Verification:** `uv run pytest -q` + `pnpm build` + golden + 3-server probe. No `ModuleNotFoundError`.

**Rollback:** `git revert <sha>` — all moves are tracked.

---

### S2 — Normalize rag script naming

**Context:** `backend/ml_assets/rag_index/scripts/00_analyze_refined.py`, `00_count.py`, `00_full_audit.py` etc — numeric prefixes hide purpose and sort arbitrarily.

**Tasks:**
- [ ] Rename `00_*` → descriptive names (`analyze_refined_corpus.py`, `count_nodes.py`, …) while keeping a `00_` → new-name map in `tools/rag/README.md`.
- [ ] Update any `scripts/replay_golden.py` or docs that invoke them by name.

**Verification:** `Get-ChildItem tools/rag | Sort Name` is alphabetical by purpose; no broken import.

---

### S3 — Fix `frontend/public/assets/researchers image` space

**Tasks:**
- [ ] `git mv "frontend/public/assets/researchers image" frontend/public/assets/researchers`
- [ ] Search `researchers image` in `frontend/src/**` (e.g., `frontend/src/lib/constants.ts`, team pages) → update import paths.
- [ ] Add redirect note for one release if old URL was ever public.

---

### S4 — Asset map document

**Tasks:**
- [ ] Create `docs/ARCHITECTURE_ASSETS.md`: table of every large asset (RAG index, vision `model.pt`, soil `effnet*.pt`, GGUF) with path, size, git status (ignored vs tracked), provenance, and verifier (`backend/ml_assets/vision/verification_report_live.md`).
- [ ] Create `backend/ml_assets/README.md` pointer: "Large binaries are gitignored; see `docs/ARCHITECTURE_ASSETS.md` for provenance."

---

### S5 — Repo hygiene tooling (non-enforcing)

**Tasks:**
- [ ] Add `.editorconfig` (LF, UTF-8, 2-space TS, 4-space Python).
- [ ] Add `.pre-commit-config.yaml` (trailing-whitespace, end-of-file, `check-yaml`, no `no-commit-to-branch` enforcement yet).
- [ ] Do NOT wire into CI yet — keep this advisory for one release.

---

### S6 — Structure checkpoint

**Gate:** same as H8. Additionally: `Select-String -Pattern "poster deisgn|researchers image|Soil Moisture Detection" -Recurse` → 0 hits. Tag `structure-clean-2026-08-21`.

---

### P1 — Privacy & retention operator (T1-04)

**Context:** Bangladesh PDP Ordinance 2025 (No. 61 of 2025) requires retention limits and human-data minimization. Current audit JSONL + `helpline_registrations.jsonl` grow unbounded; no masking.

**Amendment needed:** `docs/production_readiness/amendments/01_PRIVACY_GOVERNANCE_YYYY_MM_DD.md` — researcher approval required before code.

**Tasks (flag-gated, default off):**
- [ ] Add `AUDIT_RETENTION_DAYS` purge script (opt-in cron, never auto-delete on boot) + doc `docs/production_readiness/retention_policy.md` already exists — wire it.
- [ ] Mask phone numbers in `helpline_registrations.jsonl` (store hash, display last 4).
- [ ] Add PII scrub at ingestion (index build strips phone patterns).
- [ ] Env: `AUDIT_RETENTION_DAYS=90`, `PII_MASKING=false` default (flip to true after green).

**Verification:** unit test: masked output does not contain full phone; audit metrics still correct; 3-server green.

---

### P2 — Multi-tenancy + RBAC foundation (T1-01)

**Amendment:** `02_MULTITENANCY_RBAC_...md`. Conflict with `AGENTS.md §2.1` (auth additive/optional).

**Tasks (anonymous demo untouched):**
- [ ] Add `tenants`, `memberships` tables via `storage/sqlite.py` migration (behind `MULTITENANCY_ENABLED=false`).
- [ ] Add RBAC middleware (no gate on legacy paths).
- [ ] Tests: anonymous request still 200 on `/api/qa`, tenant-scoped request isolates audit.

---

### P3 — Model-serving separation (T1-02)

**Amendment:** `03_MODEL_SERVING_SEPARATION_...md`.

**Tasks:**
- [ ] Add `model_registry.json` + ONNX export path (still reports `detection_mode: classification` until verified detection artifact lands).
- [ ] Split inference: `UltralyticsClassificationRunner` vs future `OnnxDetectionRunner` via port.

---

### P4 — Deployment kit (T1-03) — **parallel after P2**

**Amendment:** `04_DEPLOYMENT_KIT_...md`.

**Tasks:**
- [ ] `Dockerfile` (multi-stage, `python:3.11-slim` + `node:24-alpine` for frontend `standalone`), `docker-compose.yml` (backend, frontend, Caddy), `Caddyfile` (auto-HTTPS, `flush_interval -1` for SSE).
- [ ] GH Actions CD: OIDC, GHCR `:sha` tags, `compose pull && up -d`, rollback = previous tag.
- [ ] Docs: `docs/deployment/README.md`.

---

### P5 — Safety depth (T1-05) — **parallel after P2**

**Amendment:** `05_SAFETY_DEPTH_...md`.

**Tasks:**
- [ ] Multi-turn safety context (session-aware classifier, not just single query).
- [ ] Red-team CI suite: OWASP GenAI LLM Top 10 2026, indirect injection via retrieved docs, `Prompt Guard 2` eval.
- [ ] Review lane: queue for verifier-flagged advisories → human review UI.

---

### P6 — Frontend production hardening (additive, no amendment)

**Tasks:**
- [ ] `frontend/next.config.ts`: `output: "standalone"` + verified `headers()` (already P0-8).
- [ ] Bundle budget: `size-limit` in CI (first-load JS < 200 KB gzip).
- [ ] PWA shell via Serwist (precache shell only, **no offline chat**).
- [ ] SSE UX: heartbeat-aware reconnect + backoff + abort on unmount.

---

### P7 — Runtime upgrade (no amendment)

**Tasks:**
- [ ] Python `3.11 → 3.13.15` (verify each dep against 3.13 release notes per AGENTS §2.7), `uvicorn 0.52.3`, Node 24 LTS.
- [ ] Re-run `pip-audit` + `npm audit` + full suite + 3-server.

---

### P8 — Observability lane (no amendment)

> **DEFERRED 2026-08-21** — partial scaffold (no-op `tracing.py` stub + 3 unused settings + 1 unused import) was **reverted**, not finished: `opentelemetry-python` is not installed, no spans were ever wired, and the paper's latency evidence already comes from audit `stage_timings_ms` (T0-05). Revisit only if a production deployment actually needs span export; it adds nothing to the Expert Systems manuscript.

**Tasks:**
- [ ] `opentelemetry-python` manual spans per stage (safety/retrieval/generation/verifier/cache), attributes: latency, tokens, cost, refusal rate.
- [ ] Dashboard: Grafana or Phoenix single-process (chosen over Langfuse for 1-process constraint).

---

### P9 — Secrets & backup (no amendment)

**Tasks:**
- [ ] SOPS+age for GH Actions Environments; rotate OpenRouter/Gemini keys.
- [ ] Nightly `pg_dump` (Supabase pooler) + SQLite logrotate off-site; monthly restore drill.

---

### P10 — Production checkpoint

**Gate:**
```powershell
# load: 4 concurrent QA streams for 60s — p95 latency, no 500s
# failover drill: kill primary provider → breaker trips → fallback serves
# restore drill: restore audit DB from nightly dump → metrics match
uv run pytest -q  # + red-team suite
pnpm --dir frontend build
python backend/scripts/replay_golden.py --assert-invariants  # 50/50 + injection
curl https://<prod-domain>/health; curl https://<prod-domain>/readyz
```
Tag `prod-ready-2026-MM-DD`.

---

### R1 — Freeze paper SSOT

**Tasks:**
- [ ] `paper/manuscript/T25_paper_skeleton_v1.md` → Expert Systems skeleton (Wiley template: Abstract, Introduction, Related Work, System Architecture, Methods, Experiments, Results, Discussion, Limitations, Ethics, Reproducibility).
- [ ] Freeze `paper/system_evolution_plan_2026/execution_planning_2026_08_12/12_CLAIM_LEDGER.md` + claim schema (`06_CLAIM_SCHEMA_AND_VERIFIER.md`).
- [ ] Enforce `docs/PAPER_POLICY.md` in CI (forbid `arXiv:2606.29243` citation via grep).

---

### R2 — Dataset & benchmark freeze (**parallel**)

**Tasks:**
- [ ] Provenance manifests: `backend/ml_assets/rag_index/provenance/` + `dataset_release/safety/` 20k set (verified) + `soil_moisture/` 722 imgs.
- [ ] Retrieval eval: BM25 vs dense vs hybrid (RRF), k=5, report nDCG/MRR/hit-rate on `backend/ml_assets/rag_index/eval/` splits.
- [ ] Index versioning: `indexes/index_sha256.txt` + `CORPUS_VERSION` already P0-7.

---

### R3 — Vision & RAG ablation matrix (**parallel**)

**Tasks:**
- [ ] Execute `05_MINIMUM_EXPERIMENT_MATRIX.md`: crop classifier vs per-crop disease, k-ablation, dialect expansion on/off, verifier strict vs lenient.
- [ ] Log every run under `paper/system_evolution_plan_2026/execution_planning_2026_08_12/research_artifacts/runs/` with seed + hash.

---

### R4 — Human & dialect study

**Tasks:**
- [ ] Implement `07_ABSTENTION_AND_DIALECT_PROTOCOL.md`: 6 dialects, 12 safety categories, 9 patterns, over-refusal test (144 cases).
- [ ] Calibrate human judgment set (Bengali native speakers, inter-annotator κ) — do not fabricate scores.

---

### R5 — Results synthesis

**Tasks:**
- [ ] Figures: safety pipeline (D1), vision routing (D2), grounded data (D3), soil scatter (E), architecture (generate_architecture_fig.py).
- [ ] Tables: competitive matrix (`11_RESEARCH_GAPS_competitive_matrix.md`), ablation, safety breakdown.
- [ ] `paper/system_evolution_plan_2026/execution_planning_2026_08_12/17_FINDINGS_LOG_2026_08_14.md` → final findings.

---

### R6 — Manuscript draft (custom writer — 8-phase loop)

> Per `AGENTS.md` custom writer override: dispatch a `general` subagent with `~/.config/opencode/agents/writer.md` (8 phases: Understand→Plan→Draft→3 reviewers Technical/Story/Language→Merge→Rewrite×3→Polish).

**Tasks:**
- [ ] Feed `R1` skeleton + `R2..R5` artifacts → writer loop (max 3 rewrite cycles).
- [ ] Target: Expert Systems journal — system track, 12–15 pages double-column, 40–60 refs, reproducibility statement, data/code availability (HF + GH).

---

### R7 — Paper checkpoint (reproducibility audit)

**Gate:**
- [ ] `paper/manuscript/` compiles (LaTeX or Word per Wiley).
- [ ] Reproducibility zip: `dataset_release/safety/` + `soil_moisture/` + `rag_index/provenance/` + `research_artifacts/runs/` + `scripts/replay_golden.py` all hash-pinned.
- [ ] HF dataset card + GH release checklist (license, citation, `MODEL_CARD.md`).

---

## 5. Execution Protocol (every step, no exceptions)

### 5.1 How to run a step

```powershell
# 1. Snapshot before
git status --short
uv run pytest -q
pnpm --dir frontend build
python backend/scripts/replay_golden.py --assert-invariants

# 2. Start three servers (separate terminals, keep running during the step)
# Terminal A: backend
uv run uvicorn app.main:app --reload --port 8000
# Terminal B: frontend
pnpm --dir frontend dev  # or pnpm start for prod probe
# Terminal C: local LLM (if enabled)
ollama serve  # or llama-server --port 11435

# 3. Execute exactly one step's tasks (one commit max)

# 4. Verify after (same commands as #1 + live probes)
curl http://localhost:8000/health
curl http://localhost:8000/readyz
curl http://localhost:3000/ -I
curl http://localhost:3000/chat -I

# 5. If any gate fails → STOP, git restore / git revert, report failure, do not continue.
```

### 5.2 Agent dispatch

| Lane | Subagent | When |
|------|----------|------|
| Hygiene (`H1..H7`) | `general` | File moves/deletes — no model tier needed |
| Structure (`S1..S5`) | `general` + `explore` (to find stale imports) | `S1` uses `strongest` for taxonomy design |
| Production (`P1..P9`) | `general` per task doc | Each task doc is the subagent's brief (read `docs/production_readiness/tasks/T*`) |
| Paper (`R1..R7`) | `general` + custom `writer` for `R6` | `writer` = `general` subagent with `~/.config/opencode/agents/writer.md` |

### 5.3 Anti-patterns that FAIL the review gate

- Deleting `backend/app/logs/.gitkeep` or `backend/ml_assets/**/.gitkeep` (needed for empty dir tracking)
- Changing `ARCHITECTURE.md` port contracts without an amendment
- Moving a file that is imported by `app/application/**` without updating `container.py`
- Adding a new dependency without an internet version check (AGENTS §2.7) + `.env.example` line
- Fabricating a benchmark number (`TODO` > fake)
- Citing `arXiv:2606.29243` anywhere
- Breaking the 3-server probe to "save time"

---

## 6. Branch / PR / CI Workflow

With `git + gh` present (they are):

- **Branch per checkpoint:** `chore/hygiene-clean` → `chore/structure-clean` → `feat/prod-*` → `paper/expert-systems-*`
- **PR per step** (or batched `H1..H3` if trivial) with checklist: `[ ] pytest`, `[ ] build`, `[ ] golden 50/50`, `[ ] 3-server probe (screenshot or curl log)`
- **CI:** `.github/workflows/ci.yml` already runs `backend / frontend / golden` in parallel — must stay green. Add `latex-build` job at `R6` if manuscript is LaTeX.

Direct mode (no GH) fallback: edit-in-place, still one commit per step, same gates.

---

## 7. What This Plan Deliberately Defers

- **No microservices / K8s / queues** — single FastAPI + single Next stays (AGENTS §2.3). Scale = replicate container behind Caddy.
- **No separate safety classifier training** — deterministic pre-filter + LLM structured output is correct until volume justifies it.
- **No live index building** — precomputed RAG stays.
- **No detection artifact claim** — vision stays `task: classify` until a verified detection weight lands (per `PROJECT_HANDOFF.md` invariant).

---

## 8. Immediate Next Actions (pick one)

1. **Start `H1`** (purge stray logs) — 10-minute, zero-risk first commit. I can dispatch it now with 3-server verification.
2. **Review amendments** — researcher approves `T1-01..T1-05` amendments to unblock `P1..P5` (required before any Tier 1 code).
3. **Kick paper lane `R1`** in parallel — freeze skeleton + claim ledger while hygiene runs (no file overlap).

> Say **`go H1`** and I dispatch the first hygiene step with live 3-server checks. Say **`go R1`** to start the paper lane in parallel. Say **`tune`** to adjust step order or split a step further.

---

# G-Lane — Government-Handoff: UI Refinement + Tiers + Admin Console (added 2026-08-22)

Researcher-approved plan for the government-handoff preparation. Governed by
`docs/production_readiness/amendments/02_ADMIN_TIERS_BROADCAST_AMENDMENT_2026_08_22.md`
(APPROVED 2026-08-22). Researcher decisions: **no tier gating now**, **in-app
notifications first (Web Push deferred)**, **admin v1 = ops console**, **polish the
existing Field Notebook design** (no DESIGN.md regeneration).

Same execution protocol as §5 (snapshot → 3 servers → one bounded commit → gates →
stop on failure). Every step keeps the anonymous/DEMO_MODE path byte-identical.

| Step | Scope | Key gate |
|------|-------|----------|
| G0 | Amendment 02 + stale-doc fixes (PROJECT_HANDOFF line 48, AGENTS rule 1 path) + this lane | docs-only; `pytest -q` still green |
| G1 | UI A1–A2: de-English farmer surfaces; legibility floor (≥12px captions, ≥13px body); contrast fixes from `docs/ui_audit/GLOBAL_DESIGN_SYSTEM_BUGS.md` §2 | `pnpm build` + 390px manual pass |
| G2 | UI A3: voice round-trip — auto-fallback to backend edge-tts when browser lacks bn-BD voice; large calm Bengali notice | manual voice test + build |
| G3 | UI A4–A5: mobile auth discoverability (no popups/redirects); PWA 192/512 maskable icons | Lighthouse manifest check |
| G4 | UI A6–A7: lazy-load recharts/inspector on research routes + landing charts; fix stale `frontend/smoke-check.js` to assert optional auth | size-limit ≤ budget; smoke green |
| G5 | B1–B2: migration `002_roles_plans.sql` (profiles.role/plan + admin_actions); backend `require_admin`, `/auth/me` role/plan, `/api/v1/admin/users` GET/PATCH | `test_admin_authz.py` green; 401/403/200 |
| G6 | B3–B5: plan badge UI; test users (free/premium/admin) + `NEXT_PUBLIC_DEV_USER_SWITCHER` dev-only switcher; tests | live persona swap; full `pytest -q` green |
| G7 | C1–C2: migration `003_notifications.sql`; `GET /api/notifications` (audience-filtered) + read state; admin announcements CRUD; `/api/safety/metrics` optional limit/window | `test_notifications.py` green |
| G8 | C3: navbar bell + panel; urgent disease-alert banners on `/detect`+`/chat`; read-state sync (server for signed-in, localStorage anon) | anonymous sees `all`-audience alerts; offline tolerant |
| G9 | C4–C6: `/admin` route group (overview/users/announcements, server-side role guard, live Bengali preview); final tests + full regression | non-admin → 404-style page; every admin API 403s independently |

Deferred (design recorded in amendment 02 §5, no new approval needed): Web Push
(pywebpush + VAPID), content-library management, artifact version viewer.
