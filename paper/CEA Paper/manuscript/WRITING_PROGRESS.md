# CEA Paper — Writing Progress Ledger (crash-safe state file)

> **PURPOSE:** This file is the single persistent memory for the CEA paper writing task.
> If the agent session is compacted or restarted, READ THIS FILE FIRST, then resume at
> the first unchecked item in §6 Task Board.
> Update this file after **every** completed step. Never delete history, only append/tick.

**Task owner:** Researcher (user) · **Agent role:** expert researcher + PhD supervisor
**Started:** 2026-08-27
**Last updated:** 2026-08-28 (ledger reconciled with artifacts actually on disk)

---

## 1. The Assignment (verbatim intent)

1. Read the plans in `D:\KrishokChat Advisory System\paper\planning` (4 files).
2. Read the results/experiments in `D:\KrishokChat Advisory System\paper\CEA Paper\experiments`
   — **DO NOT re-verify**; results are already verified and clean. Just read and analyse.
3. Do the analysis (what story do the numbers support?).
4. **First** produce the best-possible paper-writing outline and save it as
   `D:\KrishokChat Advisory System\paper\CEA Paper\manuscript\writing_outline.md`.
   - Existing 18-section format may be right or wrong — decide independently.
   - Plan all figures / diagrams / charts / tables.
   - For any diagram that needs external image generation, give the user a ready GPT prompt.
5. **Then** write the full paper section by section into
   `D:\KrishokChat Advisory System\paper\CEA Paper\manuscript`.
6. Report back with a submission-ready paper.

**Hard constraints from user:**
- Do NOT wander into irrelevant folders. Only `paper/planning` + `paper/CEA Paper`.
- Do NOT over-think verification of experiment results — they are frozen and clean.
- Keep documenting state continuously (this file) because of compaction risk.

**Hard constraints from AGENTS.md (project):**
- Rule 5: **never fabricate a number.** Every quantitative claim must trace to
  `paper/CEA Paper/experiments/results.yaml` or a layer `results.yaml`/`results.json`.
  If missing → explicit `TODO` placeholder.
- Rule 9: arXiv:2606.29243 is **DEPRECATED** — never cite, link, or reuse its numbers.
  Authoritative prior papers are referenced by filename only.
- Paper track only: never touch `backend/`, `frontend/`, `supabase/`, `deploy/`.

---

## 2. Target venue facts (locked)

| Item | Value |
|---|---|
| Journal | *Computers and Electronics in Agriculture* (Elsevier) |
| Article type | Full Original Research Paper |
| Length target | ~9,000–12,000 words main text |
| Working title | *Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support* |
| Format | LaTeX, `elsarticle` class, modular `sections/*.tex` + `tables/*.tex` |
| Driver file | `manuscript/krishokchat_cea_main.tex` |
| Bib file | `manuscript/krishokchat_cea.bib` |

---

## 3. Files that exist right now (pre-work inventory)

### 3.1 Planning inputs (read-only)
- `paper/planning/paper_cea.md` — 5,007 lines. **The master CEA design brief.** Highest priority.
- `paper/planning/innovation_plan.md` — 85 KB.
- `paper/planning/paper_eacl.md` — 81 KB (sister EACL/NLP paper — used only for scope separation).
- `paper/planning/paper_planning.md` — 69 KB.

### 3.2 Results inputs (read-only)
- `paper/CEA Paper/experiments/results.yaml` — 5,174 lines, 187 KB. **MASTER SSOT.**
- 38 layer folders `E02 … E40`, each with `README.md`, `results.yaml`, `results.json`, `scripts/`.
- Some layers have `traces.jsonl` (raw per-case traces).

### 3.3 Existing manuscript skeleton (to be replaced/rewritten)
- `manuscript/krishokchat_cea_main.tex` (5.5 KB driver)
- `manuscript/sections/01…18_*.tex` — mostly thin stubs (some 600–6,000 bytes)
- `manuscript/tables/tab1…tab10_*.tex` — 10 pre-formatted tables
- `drafts/01…18_*.md` — short outline notes (~1 KB each)

---

## 4. Analysis notes accumulated so far

### 4.1 From `paper_cea.md` (lines 1–1599 read)
Central thesis to build the paper on:
> In safety-sensitive agricultural advisory, the component that generates fluent language
> must not be the component that holds factual authority. Separating **factual authority**
> from **linguistic realization**, and selectively routing among deterministic resolution,
> grounded generation, abstention, and escalation, improves safety while retaining coverage
> and efficiency.

Four novelty layers:
1. **Bounded factual authority** — 11-slot single-record certification
   `C = <crop, problem, stage, active, formulation, dose, unit, volume, interval, PHI, regulatory>`.
2. **Selective resolution** — action set `{CERTIFY, GENERATE_THEN_VERIFY, ABSTAIN, ESCALATE}`.
3. **Cross-layer failure containment** (not repair-by-another-model).
4. **Deployment constraints as reliability constraints** (edge, offline, SMS, network).

Certification predicate (goes in Problem Formulation):
`Certify(C)=1` iff `ValidSource(e) ∧ Current(e) ∧ Authorized(e) ∧ Entails(e,C) ∧ Completeness(C) ∧ g(x) ≥ θ`
with **all required safety fields bound to the same evidence record**.

Two kinds of correctness to introduce explicitly: **linguistic correctness** vs
**decision/factual correctness**. Thesis: a system can be linguistically good and factually unsafe.

Primary endpoints (do NOT use "accuracy" as umbrella):
- **CUAR** = unsafe cases certified / unsafe cases  ← primary safety endpoint
- **CAC** = certified responses correct / certified responses ← primary advisory endpoint
- **Coverage** = non-abstained / answerable
- **AA** (appropriate abstention) = correct abstentions / cases requiring abstention
- Per-critical-field accuracy (all 11 slots reported individually)

Baseline ladder (must be 7, B0–B6):
- B0 LLM-only · B1 Vanilla RAG · B2 RAG+generic safety guard · B3 RAG+post-hoc LLM judge
- B4 Structured deterministic resolver (no generation) · B5 Full bounded-authority system
- **B6 Evidence-constrained RAG *without* single-record binding** ← isolates the actual contribution

Claims that are FORBIDDEN (reviewer traps):
- "first Bengali agricultural RAG" (Farmer.Chat, KrishokBondhu exist)
- "first agricultural multimodal RAG" (SMART exists)
- "first rule-first agricultural advisory" (expert systems are old)
- "first time-aware agricultural RAG" (TARAG exists)
- "zero-risk" → must be "zero dangerous acceptance **observed on the specified test suite**, with CI"

Positioning literature to cite (from brief): TARAG (temporal agri RAG), SMART (structured
multimodal + human-in-loop), goat-farming domain-first RAG, DSSAT-LM (LLM + crop simulation),
AgroTutor (offline agri DSS), Farmer.Chat (deployed multilingual agri GenAI), SafeRAG (RAG security).

Repositioning instructions captured:
- E17: call it "retrieval-space reduction and register-robust routing", NOT "dialect immunity".
- E21: split endpoint into input robustness / retrieval robustness / advisory correctness.
- E18: report `T1+T2 = 51.04%` as *deterministic advisory coverage*, `T0+T4 = 10.48%` as
  *safety/refusal handling*, `T3 = 38.48%` as *LLM-dependent traffic*. Do NOT say
  "61.52% answered without LLM".
- E25: demote — 78.4% joint EM shows routing is imperfect, which *motivates* absorbing
  routing uncertainty architecturally.
- E19: it is proof-of-mechanism on a small graph; do not oversell scalability.
- E15 SMS: supporting result only ("authority boundary survives constrained output channels").
- E22/E07–E08 security: promote to a real security-robustness subsection.
- E23: frame as **deployment-integrity** experiment, not a crypto experiment.
- E4 calibration: compare at **fixed risk budgets** (≤0.5%, ≤1%, ≤2% coverage), not
  "we beat conformal". Threshold chosen on dev, frozen for test.
- E9/E16/E40: hardware numbers must be labelled as the measurement setting actually used.

### 4.2 From `paper_cea.md` (lines 1600–5007)
- **PENDING — not yet read.**

### 4.3 From `innovation_plan.md`
- **PENDING.**

### 4.4 From `paper_planning.md`
- **PENDING.**

### 4.5 From `experiments/results.yaml` (master SSOT)
- **PENDING.**

---

## 5. Key decisions taken (append-only log)

| # | Decision | Rationale | Date |
|---|---|---|---|
| D1 | Create this ledger before any reading/writing | user flagged compaction/money risk | 2026-08-27 |
| D2 | Treat `paper/planning/paper_cea.md` as the authoritative design brief | it is a purpose-written CEA design exercise | 2026-08-27 |

---

## 6. Task Board (resume point — tick as completed)

### Phase A — Ingest
- [x] A1. Inventory `paper/planning` + `paper/CEA Paper` file trees
- [x] A2. Read `CEA Paper/manifest.yaml` + `CEA Paper/README.md`
- [x] A3. Read `paper_cea.md` lines 1–1599
- [ ] A4. Read `paper_cea.md` lines 1600–5007
- [ ] A5. Read `innovation_plan.md` (skim for novelty framing + anything not in paper_cea.md)
- [ ] A6. Read `paper_planning.md` (skim)
- [ ] A7. Skim `paper_eacl.md` only to confirm CEA/EACL scope split (avoid double-submission overlap)
- [ ] A8. Read `experiments/results.yaml` in full (chunked), extracting every number into §7 Number Bank
- [ ] A9. Spot-read the layer `results.yaml` for E27, E28, E29, E30, E31, E34 (the newest live benchmarks)
- [ ] A10. Read existing `manuscript/krishokchat_cea_main.tex` + all 18 section stubs + 10 tables

### Phase B — Analysis & Outline
- [ ] B1. Build §7 Number Bank (every citable metric + provenance path)
- [ ] B2. Decide final section architecture (keep 18? restructure?) and justify
- [ ] B3. Design full figure list (F1…Fn) with data source + type + caption
- [ ] B4. Design full table list (T1…Tn) with data source + caption
- [ ] B5. Write GPT image-generation prompts for conceptual diagrams
- [ ] B6. Write `manuscript/writing_outline.md` (the deliverable)
- [ ] B7. Present outline decision summary to user

### Phase C — Write (one section at a time, tick each)
- [ ] C0. Rebuild `krishokchat_cea_main.tex` driver + abstract + highlights + keywords
- [ ] C1. Introduction
- [ ] C2. Related Work
- [ ] C3. Problem Formulation
- [ ] C4. System Architecture
- [ ] C5. Knowledge Governance
- [ ] C6. Experimental Methodology
- [ ] C7. Results — Advisory Quality
- [ ] C8. Results — Authority & Safety
- [ ] C9. Results — Selective Reliability / Calibration
- [ ] C10. Results — Robustness (linguistic + perception)
- [ ] C11. Results — Temporal & Source Authority Governance
- [ ] C12. Results — Security & Delivery Integrity
- [ ] C13. Results — Efficiency & Deployment Economics
- [ ] C14. Discussion
- [ ] C15. Deployment Implications
- [ ] C16. Limitations
- [ ] C17. Reproducibility / Data & Code Availability
- [ ] C18. Conclusion
- [ ] C19. Bibliography completion
- [ ] C20. Figure/table generation instructions handed to user

### Phase D — Finalize
- [ ] D1. Cross-check every number in manuscript against §7 Number Bank
- [ ] D2. Consistency pass (notation, acronyms, tense, forbidden-claim scan)
- [ ] D3. Word-count check vs 9,000–12,000
- [ ] D4. Final report to user

---

## 7. Number Bank (verified citable metrics)

> Format: `metric | value | source path`
> **Rule:** nothing enters the manuscript unless it appears here first.

*(to be populated in step A8)*

---

## 8. Open questions for the user

*(none yet)*
