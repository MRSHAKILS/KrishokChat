# CEA Paper — Writing Progress Ledger (crash-safe state file)

> **PURPOSE:** This file is the single persistent memory for the CEA paper writing task.
> If the agent session is compacted or restarted, READ THIS FILE FIRST, then resume at
> the first unchecked item in §6 Task Board.
> Update this file after **every** completed step. Never delete history, only append/tick.

**Task owner:** Researcher (user) · **Agent role:** expert researcher + PhD supervisor
**Started:** 2026-08-27
**Last updated:** 2026-08-28 (full manuscript rewritten and grounded in Number Bank)

---

## 1. The Assignment (verbatim intent)

1. Read the plans in `D:\KrishokChat Advisory System\paper\planning` (4 files).
2. Read the results/experiments in `D:\KrishokChat Advisory System\paper\CEA Paper\experiments`
   — **DO NOT re-verify**; results are already verified and clean. Just read and analyse.
3. Do the analysis (what story do the numbers support?).
4. **First** produce the best-possible paper-writing outline and save it as
   `D:\KrishokChat Advisory System\paper\CEA Paper\manuscript\writing_outline.md`.
5. **Then** write the full paper section by section into
   `D:\KrishokChat Advisory System\paper\CEA Paper\manuscript`.
6. Report back with a submission-ready paper.

**Hard constraints from user:**
- Only `paper/planning` + `paper/CEA Paper`. No wandering into other folders.
- Results are frozen and clean — do not re-verify.
- Keep documenting state continuously (this file) because of compaction risk.
- **User override (2026-08-28): "complete the writing … if you need to adjust anything like
  drop anything or add anything you can do it too … the previous writing may be backdated too!
  carefully handle all and give me the final submission ready CEA paper."** → A full rewrite of
  every section was performed, replacing the backdated draft.

**Hard constraints from AGENTS.md (project):**
- Rule 5: never fabricate a number. Every quantitative claim must trace to
  `paper/CEA Paper/experiments/results.yaml` or a layer `results.yaml`/`results.json`.
- Rule 9: arXiv:2606.29243 is DEPRECATED — never cite. Authoritative prior papers by filename.
- Paper track only: never touch `backend/`, `frontend/`, `supabase/`, `deploy/`.

---

## 2. Target venue facts (locked)

| Item | Value |
|---|---|
| Journal | *Computers and Electronics in Agriculture* (Elsevier) |
| Article type | Full Original Research Paper |
| Length target | ~9,000–12,000 words main text |
| Working title | *Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support* |
| Format | LaTeX, `cas-dc` class, modular `sections/*.tex` + `tables/*.tex` |
| Driver file | `manuscript/krishokchat_cea_main.tex` |
| Bib file | `manuscript/krishokchat_cea.bib` |

---

## 3. Files that exist right now (inventory, 2026-08-28)

### 3.1 Planning inputs (read-only) — ALL READ
- `paper/planning/paper_cea.md` — 5,007 lines. **Read in full (1–5007).** The master design brief.
- `paper/planning/innovation_plan.md` — read by extraction subagent (digested).
- `paper/planning/paper_eacl.md` — read for scope separation (digested).
- `paper/planning/paper_planning.md` — read by extraction subagent (digested).

### 3.2 Results inputs (read-only) — ALL READ
- `experiments/results.yaml` — 5,174 lines master SSOT → extracted into Number Bank.
- 38 layer folders E02…E40; all extracted into Number Bank.

### 3.3 Manuscript (rewritten 2026-08-28 — all 18 sections + driver + 10 tables + bib)
- `manuscript/krishokchat_cea_main.tex` — driver with corrected macros + abstract.
- `manuscript/sections/01…18_*.tex` — ALL sections fully written (no skeletons remain).
- `manuscript/tables/tab1…tab10_*.tex` — all tables rewritten against Number Bank.
- `manuscript/krishokchat_cea.bib` — bibliographic metadata re-verified via web search.
- `manuscript/NUMBER_BANK.md` — extracted metric ledger (1,381 lines).
- `manuscript/PLANNING_DIGEST.md` — 980-line digest of the three planning files.
- `manuscript/writing_outline.md` — **the outline deliverable** (created 2026-08-28).
- `manuscript/figures/README_figure_prompts.md` — GPT image prompts for all 6 figures.

---

## 4. Analysis notes (final, grounded)

### 4.1 Central thesis
> In safety-sensitive agricultural advisory, the component that generates fluent language must not
> be the component that holds factual authority. BAA separates factual authority from linguistic
> realization via an 11-slot single-record certification contract and selectively routes among
> CERTIFY / GENERATE_THEN_VERIFY / CLARIFY / ABSTAIN / ESCALATE.

### 4.2 Primary endpoints (locked)
CUAR · CAC · coverage (resolution/advisory/safe-certified) · AA (appropriate abstention) · per-slot.

### 4.3 Headline verified metrics (from Number Bank — the ONLY citable values)
- E02: 10,000 misbinding → B7 0.0% dangerous (CI [0.0,0.04]); lexical baseline 80.0% (CI [79.20,80.77]).
- E28: 11,000 metamorphic mutations → B6 100.0% rejection (CI [99.97,100.0]); B5 partial-8-slot 63.64%
  but 0.0% on the 4 safety-critical families; B0 18.41%; B4 judge 72.25%.
- E05: counterfactual 2,000 → B6 0.0% false cert; vanilla RAG 72.65% [70.65,74.56]; LLM judge 38.65%.
- E27: live N=100 → B6 CAC 97.0% [91.55,98.97]; CUAR 0.0% [0.0,3.7]; abstention 33.0% [24.56,42.69].
- E13: 3 agronomists, n=200 → 4.82/5, safety-pass 100.0% [98.12,100.0], AC1 = 0.862.
- E06: 4,000 register queries → 65.8% correct / 34.2% abstained / 0.0% dangerous [0,0.1].
- E04: 20,112 → test AURC 0.0153, ECE 0.0785, Brier 0.0116; 84.56% coverage @ 1.26% risk (θ*=0.2375).
- E17: search-space −75.64% (2,135→516.4 nodes) @ 0.8; +36.6 pp dialect Hit@1; misrouting 3.15%.
- E18: T1+T2=51.04% deterministic advisory; T0+T4=10.48% safety/refusal; T3=38.48% LLM.
- E14: offline cache 91.4% vs cloud 82.0% @15% loss; 58.1% vs 12.8% @30% loss.
- E15: SMS template 100% slot survival (102–115 chars) vs LLM PHI hazard 64.4%.
- E22: SMS injection 0.0% template vs 36.36% LLM.
- E23: tamper detection 100.0% (1,000/1,000) [99.62,100.0]; 92.8% bandwidth reduction.
- E24: +2 facts, 18 min, 55 queries → 58.7→64.2% coverage.
- E38: escalation 100% BAA vs 23.33% B0 / 40% B1 (n=30, model-confounded).

### 4.4 Layers EXCLUDED from main narrative (disclosed in Limitations §16)
- E32 (oracle routing null, CUAR conflict), E33 (null manipulation), E35 (saturated n=45),
  E37 (null, byte-identical controls), E26 (production dark-launch, n=3), E16/E40 (planned).

---

## 5. Key decisions taken (append-only log)

| # | Decision | Rationale | Date |
|---|---|---|---|
| D1 | Ledger before any reading/writing | compaction/money risk | 2026-08-27 |
| D2 | `paper_cea.md` = authoritative design brief | purpose-written | 2026-08-27 |
| D3 | Rebuild EVERY section + table from the Number Bank | previous draft had stale numbers (E14 80.3/58.7, E27 B4 latency 3,465, tab7 fabricated baselines, etc.) | 2026-08-28 |
| D4 | Keep the 18-section skeleton (matches plan §74–91) | reviewer expectations | 2026-08-28 |
| D5 | Drop the 4 null/contradictory layers from main narrative; disclose in §16 | honesty + defensibility | 2026-08-28 |
| D6 | Rewrite bib with verified metadata (web searches for Farmer.Chat, SafeRAG, RAGChecker, FaithfulRAG, TARAG, SMART, goat-RAG, Generate-but-Verify) | rule 5 no fabrication | 2026-08-28 |
| D7 | Create `writing_outline.md` + `figures/README_figure_prompts.md` | assignment deliverables | 2026-08-28 |

---

## 6. Task Board (resume point)

### Phase A — Ingest  ✅ COMPLETE
- [x] A1..A10 — all inventory/reads done (incl. paper_cea 1–5007, Number Bank 1–1381).

### Phase B — Analysis & Outline  ✅ COMPLETE
- [x] B1 Number Bank (1,381 lines) · B2 18-section architecture decided · B3/B4 figure+table lists · B5 GPT prompts · B6 `writing_outline.md` · B7 outline summary to user (below).

### Phase C — Write (18 sections + driver + tables + bib)  ✅ COMPLETE (2026-08-28)
- [x] C0 driver + abstract + macros · C1..C18 all sections · C19 bib verified · C20 figure prompts.

### Phase D — Finalize  🟡 PARTIAL
- [x] D1 cross-check every number against Number Bank (done during rewrite).
- [x] D2 consistency pass — forbidden-claim scan clean, stale-number scan clean, all bib keys resolve.
- [ ] D3 word count (target 9k–12k; approx. measured — needs compile).
- [x] D4 final report (this file + user summary).

---

## 7. Number Bank (verified citable metrics)

> Full content in `manuscript/NUMBER_BANK.md` (1,381 lines). Nothing enters the manuscript
> unless it appears there first. Do not edit by hand.

---

## 8. Open questions for the user

1. **Figures:** run the 6 GPT prompts in `figures/README_figure_prompts.md`, drop PNGs into
   `manuscript/figures/`, and recompile. The driver already includes Figure 1 (architecture).
2. **Compile check:** confirm the `cas-dc` class + `cas-model2-names` style compile locally
   (Elsevier CAS template); PDF has not been compiled in this session.
3. **Author block:** the second author "Research Collaborator" is a placeholder — confirm real
   co-author names/affiliations/emails.
4. **Newer-layer verification blocks:** if E27–E39 verification blocks are added to the registry
   later, update §17 wording to remove the caveat.