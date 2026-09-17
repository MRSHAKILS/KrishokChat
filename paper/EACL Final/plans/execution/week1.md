# Week 1 Execution Plan — Lane A First (2026-09-17)

**Doctrine:** real queries, real runs, real API where designed, CI-meaningful sizes. Money-loss rules (AGENTS.md §0.1) bind every runner: pre-flight 1-token auth test, abort on 401/403, fsync disk writes under lock, FREE_ONLY mode, pause on >20 consecutive errors, token caps (180 NLU / 500 advisory).

## 0. Verified resources (checked 2026-09-17, not assumed)

| Resource | State | Evidence |
|---|---|---|
| CPU stack | READY — faiss 1.15.0, ultralytics 8.4.116, onnxruntime 1.28.0, fastapi 0.141.1, httpx | import-tested in backend venv |
| Network (pypi) | REACHABLE (200) | httpx HEAD |
| Installer | `uv` available; backend venv has NO pip — use `uv pip install --python backend/.venv/Scripts/python.exe` | verified |
| Tokenizer | tiktoken 0.14.0 INSTALLED just now (was missing) | import-tested |
| OpenRouter key | PRESENT (sk-or-v…, 73 chars) — validity UNTESTED until pre-flight 1-token call | file check only |
| Playwright/chromium | MISSING — install only if N04 WASM re-measure clears its gate | import-tested |
| Provider usage metering | EXACT via `lane.last_usage` (never guessed) + price table | telemetry.py read |
| Disk | results are KBs; no constraint | — |
| Human reviewers (team dual-review) | INTERNAL — ~3–4 hrs total across week (stratified samples per doctrine §5) | user + 1 teammate, time-boxed |
| External annotators | NOT AVAILABLE — replaced by audited labels + team review + disclosed LLM-judge (demo-track norm; independent annotation = future work) | — |

## 1. API budget (estimate, pre-flight gated)

| Run | Calls | Est. cost (flash-lite) |
|---|---|---|
| G5 live NLU n=400 | 400 | ~$0.20 |
| N03 catch-rate (100–200 generations) | 100–200 | ~$0.30 |
| SMS-live survival (100–300 generations) | 100–300 | ~$0.40 |
| N10 end-to-end probe (100) | 100 | ~$0.20 |
| E03 expansion 100/family (1,400) | 1,400 | ~$1–3 |
| **Total week** | **~2,100–2,500** | **~$2–5** |

All CPU arms (N01/N02-offline/N04/N07/N08/N09/G1) cost $0. Total is trivial BUT every batch still opens with the 1-token auth test — no exceptions.

## 2. Day-by-day (practical risks + fallbacks inline)

### Day 1 (done today, remaining 30 min): trust repairs
- [x] E08 README ×2, stale vision comments, hashes, E21 relocated, tiktoken installed
- [ ] STATE.md §4 6-class fix + wheat-mitigation removal decision (30 min; needs USER decision: remove dead branch or keep?)
- [ ] G2 codebook v1 written (I write; annotators start on it in parallel all week)
- Practical risk: none. Fallback: n/a.

### Day 2: N01 + N02 harness (one harness, shared frozen queries)
- Queries: PRISM F(100 underspecified) + I(100 ambiguous) + B-subset with true_crop (top up to ≥300). NO farmer subset yet (waits for G2 labels).
- Source→crop mapping frozen BEFORE running (metadata-first, title-fallback, unmatched excluded with count). Practical risk: mapping coverage <90% → report coverage + strict-subset sensitivity. Fallback: critic P0-1 sentence.
- Blind arm bypasses gate → top-5 retrieval; gated arm = full pipeline (E09 harness pattern). McNemar + Wilson.
- Metering: tiktoken cl100k on real strings BOTH sides (disclosed: cl100k ≠ Gemini tokenizer) + provider-exact where API involved.
- Practical risk: pipeline import/env drift (E09 ran 2026-08-31 here — low risk); runtime minutes. Fallback: critic P0-1/P0-2 sentences.
- Done = results land in `experiments/results/` + N01/N02 specs flipped to REAL_MEASURED + ground_truth updated.

### Days 3–4: N04 re-run (accuracy + parity narrowed) + P0-9 UI checks
- Pre-step: record per-model imgsz (chilli!) + checkpoint hashes (done) + ultralytics/ORT versions.
- 1,237 images × router + routed disease models, CPU. Practical risk: version drift in ultralytics behavior (mitigated: parity check is its own safety net); chilli mapping (resolved: 8 classes, dir fixed). Time risk: LOW (10–40 min compute).
- INT8 + WASM only if accuracy/parity pass AND time allows; else prior numbers stay labeled previous-harness.
- P0-9: TestClient hits on flagged/refused/clarified queries + component pointers; screenshots deferred to capture day.
- Done = N04 results or critic P0-4 fallback; S3 prose locked to verified rendering.

### Day 5: N05 SMS + N03-lite + E03-expansion decision
- N05: enforcement/referral offline (N≥300, $0) + survival on live-generated safe subset (n≥100, pre-flight first). Encoding audit (code points, GSM-7 membership) always runs.
- N03-lite: 100 Treatment QA items × live T3 (100 API calls) + 4 mutation types + 100 controls. Practical risk: Treatment QA local availability — VERIFY FIRST at run start (2606 items vs curated_facts fallback). Full 200×6 only if smooth.
- E03 expansion GO/NO-GO (recommend GO: ~$1–3, tightens the residual-risk CI that reviewers will attack).
- Done = SMS sentence + verifier row, or fallbacks.

### Days 6–7: cut + gate (per critic Action 5)
- Page cut to 6.0, abstract last, desk-reject gate (URL serves S1–S5, video ≤2:30, clean build, license, zero killed claims, every number labeled).

## 3. Parallel human track (USER dependencies — nothing else unblocks these)

1. **Team review rota** (replaces annotator recruitment): ~3–4 hrs total — N01 50+50, N03 50+50, farmer-behavior 100, OOD-40 judgments. Samples fixed before reviewing; agreement reported.
2. **Wheat-mitigation decision:** KEEP (removal risks mid-week breakage; legacy-marked, zero numeric effect). Closed.
3. **$2.30/92% verdict:** DELETED everywhere 2026-09-17. Closed.
4. **E03-expansion GO** (Day 4; default GO unless key/budget objects).
5. **Screencast capture slot** Day 5 (frozen build + verified rendering).

## 4. Practical self-evaluation (what I actually worry about)

1. **No external bottleneck remains.** The old critical path (annotator recruitment) is gone: PRISM labels are already on disk (700/1000 with true_crop verified today), AgRiTrust qrels ship human agreement, and team dual-review totals ~3–4 hours. Everything executes with people already in the room.
2. **Source→crop mapping coverage** is the likeliest technical snag in N01. Frozen heuristic + reported coverage + strict-subset sensitivity keeps it honest either way.
3. **Treatment QA locality** for N03 is unverified — first command of that run is an availability check with a named fallback.
4. **Scope discipline under time pressure.** The week fails if Lane C work starts before Lane A closes. Lanes are ordered; P1s wait.
5. **No new features.** Code freeze holds except the wheat-branch decision and the SMS packer decision (which defaults to measure-first).
