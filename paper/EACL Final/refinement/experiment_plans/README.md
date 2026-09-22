# Experiment Plans — EACL 2027 Demo (KrishokTech)

Written 22 Sep 2026, after the paper revision and the N08b fence audit. Each plan is
**execution-level**: another agent can run it without this conversation.

## Selection rule
Only experiments that (a) **add a positive, citable result**, (b) run in **≤ 2 h**, and
(c) need **no new human labels and no paid API calls**. Experiments that mainly expose
new weaknesses were excluded (see `../experiment_suggestions.md` for the full list).

## Run order

| # | Plan | Time | Cost | Expected gain for the paper | Paper sections touched |
|---|------|------|------|-----------------------------|------------------------|
| X1 | [T0 + guarded-prompt pipeline ASR (replay)](X1_pipeline_asr_replay.md) | 20 min | $0, no LLM calls | Full-pipeline ASR below 10.71% on the deployed model | Abstract?, Tab. 1, §5.3, Limitations, Ethics, App. E |
| X2 | [Hard crop filter + N08 re-run](X2_hard_crop_filter.md) | 45 min | $0 | Cross-crop retrieval 30% → ~0% with coverage reported | Abstract, §3.2, Tab. 1, §5.2, Limitations, App. E |
| X3 | [SMS chemical-name slot](X3_sms_chemical_slot.md) | 45 min | $0 | Chemical-name survival 34/100 → higher, dose kept | §5.3 (SMS), App. B, App. E |
| X4 | [Authorization conformance replay](X4_conformance_replay.md) | 1.5 h | $0 (stub LLM) | "0 generator calls before authorization on N cases" | §3 intro, §5 (new sentence), App. A, App. E |
| X5 | [Frozen-generator evidence update](X5_evidence_update_demo.md) | 45 min | $0 | Concrete proof that knowledge updates need no retraining | §1/§3.2 (one clause), App. B |

Stop after any plan if time runs out: each one is independent, and the current paper is
accurate without them.

## Shared rules (apply to every plan)
1. **Freeze first.** Record git HEAD, index hash, input hash in the result JSON before running.
2. **Never edit frozen results** (`results.json`, `results_*.json` of earlier experiments). Write new files only.
3. **Independent checks.** Do not score a component with the same rule it implements (X2 needs
   the extra checks listed there).
4. **Report every denominator** and every failure/timeout.
5. **Paper edits** go only in `paper/EACL Final/paper/latex/main.tex`; recompile and confirm the
   main text still ends on page 6 (Ethics must start on page 7).
6. **If a result is worse than expected, do not hide it:** use the fallback wording in the plan.
7. Commit result files + script together; do not commit caches, venvs or build files.

## Environment (verified 22 Sep 2026)
- Repo root: `D:\Web Dev\krishokchat` (branch `master` → `origin/main`).
- Backend needs **Python ≥ 3.11** (`enum.StrEnum`). On Windows use `backend\.venv\Scripts\python.exe`.
  On Linux: `pip install uv && uv python install 3.12 && uv venv -p 3.12 v12 && uv pip install numpy rank-bm25 bnunicodenormalizer`.
- Put `backend/` on `sys.path` (see `N08_fence_study/scripts/audit_n08_residual.py` for a working header).
- **PRISM benchmark is not in the working tree.** Restore it from git history:
  `git show 3b200e3^:research_artifacts/datasets/prism_benchmark/prism_benchmark_1000.jsonl > prism.jsonl`
  Its SHA-256 matches the frozen N08 input (`948123aa…`) only with CRLF line endings; the content is identical.
- Frozen BM25 index: `backend/ml_assets/rag_index/indexes/bm25_index.pkl` (SHA-256 `2ab484ac…`, matches N08).
- Crop mapping rule: `source_crops()` in `N01_blind_arm/scripts/run_n01_blind_arm.py` (copied in the N08b audit).

## Known issue to fix while touching N08
`run_n08_fence.py` line `open_pure = fenced_pure = []` makes both arms append to **one list**,
so purity means from a re-run are wrong. The locked `results.json` (0.6472 / 0.7353) came from an
earlier version. X2 recomputes purity with separate lists.

## Paper-update map (where results land)
| Location in `main.tex` | Label / anchor | Updated by |
|---|---|---|
| Abstract | `\begin{abstract}` | X1, X2 |
| Table 1 | `tab:headline` | X1, X2 |
| §3 intro | `sec:system` | X4 |
| §3.2 | `sec:system_retrieval` | X2, X5 |
| §5.2 | `sec:eval-fence` | X2 |
| §5.3 | `sec:eval-safety` | X1, X3 |
| Limitations | `sec:limitations` | X1, X2, X3 |
| Ethics — Pesticide paragraph | `Pesticide and Dosage Guidance` | X1 |
| App. A | `app:architecture` | X4 |
| App. B | `app:delivery` | X3, X5 |
| App. E tables | `tab:evidence_a`, `tab:evidence_b` | all |
