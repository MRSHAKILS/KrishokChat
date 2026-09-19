# Manuscript — Expert Systems (Wiley) SSOT

**SSOT:** `paper/manuscript/expert-systems-skeleton.md` (frozen 2026-08-21, R1)
**Legacy skeleton:** `paper/manuscript/T25_paper_skeleton_v1.md` — kept for history; not the submission structure.
**Frozen claim ledger:** `paper/manuscript/CLAIM_LEDGER_FREEZE.md` (copy of `paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/12_CLAIM_LEDGER.md` at 2026-08-21)

## Authority

- Execution package: `paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/` (moved to `archive/` 2026-08-21 — read-only history, still authoritative for adjudicated decisions)
- Thesis: `03_THESIS_DECISION.md` (in the package above) — evidence-linked, relation-aware selective certification under BM25-only runtime + safety-constrained dialect/Banglish normalization
- Blueprint: `paper/archive/system_evolution_plan_2026/10_PAPER_BLUEPRINT.md` (mapped to Wiley sections in the skeleton)
- Contributions: `09_PAPER_CONTRIBUTION_CONTRACT.md` (C1–C4) + `12_CLAIM_LEDGER.md` (S/F/U) + `docs/PAPER_POLICY.md`
- **Venue locked 2026-08-21: Wiley *Expert Systems* journal.** The ACL SysDemo framing in `paper/literature review/10_SYNTHESIS_GAPS_POSITIONING.md` is superseded history.
- **2026-08-27 note (venue decision pending, nothing unlocked):** a CEA (*Computers and Electronics in Agriculture*) systems-pivot was analyzed in `experiments/IMPLEMENTATION_AND_AGGREGATION_PLAN.md` with new planned layers E14–E20 traced in `experiments/registry.yaml`. Until the author explicitly re-locks the venue, this Wiley SSOT and the frozen claim ledger remain binding.
- Wiley structure source (verified 2026-08-21): `https://onlinelibrary.wiley.com/page/journal/14680394/homepage/forauthors.html` — abstract ≤250 words (structured or unstructured), keywords 4–7, title without abbreviations, short running title ≤40 chars, last paragraph of Introduction describes paper structure.

## How to use

1. Edit only `expert-systems-skeleton.md` for the manuscript. Keep every empirical number as `TODO (gate: G#)` until a run/artifact ID from `CLAIM_LEDGER_FREEZE.md` is available.
2. Do **not** edit `CLAIM_LEDGER_FREEZE.md` without a dated amendment (update this README, `MEMORY.md`, and the skeleton's Appendix C).
3. At assembly (R6), the custom writer (`~/.config/opencode/agents/writer.md` 8-phase loop) consumes the skeleton + manifests from `research_artifacts/` and produces the full draft via Understand→Plan→Draft→3 reviewers→Merge→Rewrite×3→Polish.

## Enforcement — `docs/PAPER_POLICY.md` (`arXiv:2606.29243` ban)

**Rule (non-negotiable):** `arXiv:2606.29243` (v1, "Citation-Grounded Dataset and Benchmark") is deprecated and INVALID. Do not cite, quote, link, summarize, or reuse any number/claim from it in this manuscript, docs, or commit messages. The authoritative papers are `paper/done papers/KrishokTech__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf` and `paper/done papers/AgriTrust.pdf` (reference by filename/path only).

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
- [ ] No file references "Citation-Grounded Dataset and Benchmark" as KrishokTech's paper
- [ ] Any paper link in UI/docs points to `paper/done papers/` or a real public ID (`TODO` if none)
- [ ] All research stats trace to the updated papers or to verified local artifacts (`backend/ml_assets/`, `dataset_release/`, `research_artifacts/`)

## Wiley skeleton layout

`expert-systems-skeleton.md` follows Wiley Expert Systems order: Title → Abstract (250 words) → Keywords (4–7) → 1 Introduction → 2 Related Work (gaps table) → 3 System Architecture (Figure 1: 4-stage pipeline) → 4 Methods (safety / retrieval / verifier / vision / calibration / normalization) → 5 Experiments (benchmark + E1–E9 matrix + human study) → 6 Results → 7 Discussion → 8 Limitations → 9 Ethics → 10 Reproducibility → References → Appendices (G0–G9 checklist, file map, claim-ledger freeze ref). Content is skeleton bullets/placeholders, not full prose.

## Execution order — follow this top to bottom (the plan)

**Decisions already locked (2026-08-21):** venue = Wiley Expert Systems; retrieval = BM25-only is the evaluated thesis runtime, hybrid RRF (S11) appears only as ablation comparator; safety dataset 20,112 recovered on-disk with hashes (`paper/literature review/12_ASSET_VERIFICATION.md` §4).

### Stage A — Annotation setup (START NOW — long pole, people not compute)
| # | Task | Closes | Depends on |
|---|---|---|---|
| A1 | Recruit **2 Bengali agronomy annotators + 1 adjudicator** | enables G3/G6 | nothing |
| A2 | Expert sign-off on frozen T07 schema + label manual + risk taxonomy | G2 ⚠️ | A1 |
| A3 | Pilot: both annotators label the 24 T08 pilot items → compute Krippendorff α | gates everything below | A1, A2 |
| A4 | **Gate check: α ≥ 0.70.** If below → revise manual, re-pilot. Do not proceed on a fail. | G3 precondition | A3 |

### Stage B — Gold labels
| # | Task | Closes | Depends on |
|---|---|---|---|
| B1 | Two annotators independently label the frozen test split (T09, seed `20260813`) | G3 | A4 pass |
| B2 | Adjudication with lineage preserved; freeze gold labels + hashes | G3 ✅ | B1 |

### Stage C — Confirmatory experiments (in this order)
| # | Experiment | Closes | Depends on |
|---|---|---|---|
| C1 | **E1**: structured relation verifier vs lexical baseline vs gold (paired McNemar + bootstrap) | G4 | B2 |
| C2 | **E2**: calibrator fit on dev ONLY → freeze threshold before any test access | G5 | B2 |
| C3 | **E4**: dialect normalization paired protocol + native authenticity review | G6 | B2 (native reviewers can start at A1) |
| C4 | **E5** verifier×normalization interaction; E3/E6/E7 as support | G7 | C1–C3 |
| C5 | Paired statistics + error analysis from run manifests | G7 ✅ | C4 |

### Stage D — Writing (D1 can run in PARALLEL with A/B/C now)
| # | Task | When |
|---|---|---|
| D1 | Draft §2 Related Work + §3 Architecture + §4 Methods via custom writer (8-phase loop) — zero empirical TODOs blocking these | **now** |
| D2 | Draft §1 Introduction + Abstract skeleton + Keywords | after C1 direction is known |
| D3 | Fill §6 Results tables 3–7 + Figures 1–4 strictly from run manifests | after C5 |
| D4 | §7 Discussion + §8 Limitations + §9 Ethics | after D3 |
| D5 | Assembly (R6): abstract ≤250 words verified, keywords 4–7, structure paragraph verbatim, G0 URL re-validation | last |

### Stage E — Release gate
| # | Task | Closes |
|---|---|---|
| E1 | Independent reproduction in fresh env regenerates primary tables; checksums + artifact index; secrets absent | G9 |
| E2 | HF/GitHub release per R7 with license/consent review | submission-ready |

**STOP rules (from `03_THESIS_DECISION.md`, non-negotiable):** no superiority claim if E1 fails; no calibration claim if thresholds moved after test access; no subgroup inference below the frozen sample gate; learned normalizer never defines contribution C4.

## Tag

R1 freeze checkpointed after `structure-clean-2026-08-21`. Venue locked + dataset recovered 2026-08-21 (uncommitted). Next per plan above: **A1 (annotators) + D1 (Related Work/Architecture/Methods draft) in parallel**, then B→C→D3–D5→E.
