# Manuscript — Expert Systems (Wiley) SSOT

**SSOT:** `paper/manuscript/expert-systems-skeleton.md` (frozen 2026-08-21, R1)
**Legacy skeleton:** `paper/manuscript/T25_paper_skeleton_v1.md` — kept for history; not the submission structure.
**Frozen claim ledger:** `paper/manuscript/CLAIM_LEDGER_FREEZE.md` (copy of `paper/system_evolution_plan_2026/execution_planning_2026_08_12/12_CLAIM_LEDGER.md` at 2026-08-21)

## Authority

- Execution package: `paper/system_evolution_plan_2026/execution_planning_2026_08_12/`
- Thesis: `03_THESIS_DECISION.md` — evidence-linked, relation-aware selective certification under BM25-only runtime + safety-constrained dialect/Banglish normalization
- Blueprint: `paper/system_evolution_plan_2026/10_PAPER_BLUEPRINT.md` (mapped to Wiley sections in the skeleton)
- Contributions: `09_PAPER_CONTRIBUTION_CONTRACT.md` (C1–C4) + `12_CLAIM_LEDGER.md` (S/F/U) + `docs/PAPER_POLICY.md`
- Wiley structure source (verified 2026-08-21): `https://onlinelibrary.wiley.com/page/journal/14680394/homepage/forauthors.html` — abstract ≤250 words (structured or unstructured), keywords 4–7, title without abbreviations, short running title ≤40 chars, last paragraph of Introduction describes paper structure.

## How to use

1. Edit only `expert-systems-skeleton.md` for the manuscript. Keep every empirical number as `TODO (gate: G#)` until a run/artifact ID from `CLAIM_LEDGER_FREEZE.md` is available.
2. Do **not** edit `CLAIM_LEDGER_FREEZE.md` without a dated amendment (update this README, `MEMORY.md`, and the skeleton's Appendix C).
3. At assembly (R6), the custom writer (`~/.config/opencode/agents/writer.md` 8-phase loop) consumes the skeleton + manifests from `research_artifacts/` and produces the full draft via Understand→Plan→Draft→3 reviewers→Merge→Rewrite×3→Polish.

## Enforcement — `docs/PAPER_POLICY.md` (`arXiv:2606.29243` ban)

**Rule (non-negotiable):** `arXiv:2606.29243` (v1, "Citation-Grounded Dataset and Benchmark") is deprecated and INVALID. Do not cite, quote, link, summarize, or reuse any number/claim from it in this manuscript, docs, or commit messages. The authoritative papers are `paper/done papers/KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf` and `paper/done papers/AgriTrust.pdf` (reference by filename/path only).

### Local check (run before every paper commit)

```powershell
# PowerShell — must return no output
Select-String -Pattern "2606\.29243" -Path "paper/manuscript/*","paper/**/*.md","docs/**/*.md","frontend/**/*.ts","frontend/**/*.tsx" -Recurse 2>$null
# POSIX / CI
grep -R "2606\.29243" paper/ docs/ frontend/ 2>/dev/null; test $? -ne 0
```

### CI gate

`.github/workflows/ci.yml` job `paper-policy` runs the same grep and **fails the build** on any hit. `.pre-commit-config.yaml` also includes a local `forbid-arxiv-v1` hook (see `repos: local` entry). If either gate fails, fix the reference (replace with authoritative-paper filename or remove the claim) — do not suppress the check.

### Checklist (run before any submission/commit that mentions research claims)

- [ ] `grep -R "2606.29243" paper/ docs/ frontend/ backend/` returns nothing
- [ ] No file references "Citation-Grounded Dataset and Benchmark" as KrishokChat's paper
- [ ] Any paper link in UI/docs points to `paper/done papers/` or a real public ID (`TODO` if none)
- [ ] All research stats trace to the updated papers or to verified local artifacts (`backend/ml_assets/`, `dataset_release/`, `research_artifacts/`)

## Wiley skeleton layout

`expert-systems-skeleton.md` follows Wiley Expert Systems order: Title → Abstract (250 words) → Keywords (4–7) → 1 Introduction → 2 Related Work (gaps table) → 3 System Architecture (Figure 1: 4-stage pipeline) → 4 Methods (safety / retrieval / verifier / vision / calibration / normalization) → 5 Experiments (benchmark + E1–E9 matrix + human study) → 6 Results → 7 Discussion → 8 Limitations → 9 Ethics → 10 Reproducibility → References → Appendices (G0–G9 checklist, file map, claim-ledger freeze ref). Content is skeleton bullets/placeholders, not full prose.

## Tag

R1 freeze is checkpointed after `structure-clean-2026-08-21`. Next: R2 (dataset & benchmark freeze) and R3 (vision & RAG ablation) in parallel, then R4 (human & dialect study).
