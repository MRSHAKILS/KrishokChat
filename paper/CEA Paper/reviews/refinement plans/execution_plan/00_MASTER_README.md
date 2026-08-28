# CEA Paper Repair — Master Execution Plan Index
**Project:** Bounded-Authority Agricultural Advisory (KrishokChat / BAA)  
**Venue:** Computers and Electronics in Agriculture (Elsevier, Q1)  
**Plan authored:** 2026-08-28  
**Executor:** Gemini 2.5 Flash  
**Supervisor:** Research author — reviews and approves every task before next begins

**Author decisions LOCKED (2026-08-28):**
- `Q1 = NO` → E13 study never happened. Delete all references. T0-1 = BRANCH B.
- `Q2 = YES` → Runnable system exists. T0-2 = BRANCH A. Phase 4 (X2) is active.

---

## ⛔ ANTI-LAZINESS PROTOCOL — GEMINI MUST FOLLOW THIS EXACTLY

This section is read first and obeyed without exception. Violating any rule means the task is NOT complete even if you think it is.

### RULE 1: PROVE YOUR WORK WITH SHELL OUTPUT

After every file edit, you MUST run the STOP CONDITION grep/check and paste its EXACT output in your report. "I deleted the section" is not verification. The grep result IS the verification. If the grep is non-empty when it should be empty, you have not finished — fix it before reporting done.

### RULE 2: REPORT FORMAT IS MANDATORY

Every task report must follow this EXACT format:

```
## TASK [ID] REPORT

**Files modified:**
- [exact absolute path] — [what was changed, one line]

**STOP CONDITION check:**
[paste exact shell output of the grep/check command]

**Result:** PASS / FAIL
[If FAIL: describe what still needs fixing. Do not mark done if FAIL.]

**Observations (problems noticed outside task scope):**
[List separately — do not fix, just note]
```

If you submit a report without pasting the actual grep output, the task is automatically rejected.

### RULE 3: READ BEFORE YOU EDIT

Before editing any file, paste the current content of the target lines (5-line window minimum around the edit point). This proves you read the actual file and are not guessing at line numbers.

### RULE 4: ONE TASK PER SESSION. NO EXCEPTIONS.

If T0-1 is the task, you execute T0-1 and stop. You do NOT also do T0-2 "while you're in there." If you attempt multiple tasks in one session, the entire session output is discarded and the task is repeated.

### RULE 5: DO NOT INVENT NUMBERS

If a number is removed and nothing replaces it from a real YAML, leave a clearly visible placeholder:
`[REMOVED — see T0-X — no real measurement available]`

Do NOT soften language to keep a claim. A weaker honest claim is always better than a stronger dishonest one.

### RULE 6: CHAIN-BREAKER

If an experiment produces a result that contradicts the original claim: **narrow the claim**. Do not run the experiment again with different parameters to get a "better" result. Report the real finding.

### RULE 7: QUARANTINE ≠ DELETE

Files in `05_PHASES3_TO_9.md §08` (quarantine list) get a withdrawal header added to the top — they are NEVER deleted. The audit trail must be preserved.

---

## CONFIRMED DECISIONS

```
Q1 = NO  → T0-1 = BRANCH B (delete all E13 references)
Q2 = YES → T0-2 = BRANCH A (keep §7.1, delete B6 row only, mark as pending X2)
```

---

## FILE INDEX

| File | Contents | Who reads |
|---|---|---|
| `01_SITUATION_AND_AUTHOR_DECISIONS.md` | Evidence classification table, confirmed decisions | Author + Gemini |
| `02_PHASE0_CLEANUP.md` | T0-1 through T0-8 — deletions | Gemini |
| `03_PHASE1_REFRAMING.md` | T1-1 through T1-6 — reframing | Gemini |
| `04_PHASE2_EXPERIMENTS.md` | T2-1 through T2-5 — real experiments | Gemini |
| `05_PHASES3_TO_9.md` | T3, T4, T5, quarantine list, keep list | Gemini |

---

## EXECUTION ORDER

```
[LOCKED DECISIONS already answered — do not re-ask]
        │
        ↓
02_PHASE0_CLEANUP.md
   T0-1 (Branch B — E13 delete) ─── STOP. Author approves.
   T0-2 (Branch A — E27 pending X2) ─── STOP. Author approves.
   T0-3 (E32-E39 delete) ─── STOP. Author approves.
   T0-4 (E29/E30/E31 BAA rows) ─── STOP. Author approves.
   T0-5 (§17 rewrite) ─── STOP. Author approves.
   T0-6 (60k/36 layers delete) ─── STOP. Author approves.
   T0-7 (§14.4 delete) ─── STOP. Author approves.
   T0-8 (manifest fix) ─── STOP. Author approves.
        │
        ↓
03_PHASE1_REFRAMING.md
   T1-1 through T1-6 (one per session)
        │
        ↓
04_PHASE2_EXPERIMENTS.md
   T2-1 → T2-2 → T2-3 → T2-4 → T2-5 (one per session)
        │
        ↓
05_PHASES3_TO_9.md (Phase 3)
   T3-1 → T3-2 → T3-3 (abstract ALWAYS last)
        │
        ↓
05_PHASES3_TO_9.md (Phase 4 — X2 active because Q2=YES)
   T4-1 (n=300 end-to-end benchmark)
   T4-2 (register Hit@1)
        │
        ↓
05_PHASES3_TO_9.md (Phase 5 — submission gate)
   T5-1 → T5-2 → T5-3
```

---

## WHAT THE PAPER LOOKS LIKE AFTER FULL EXECUTION

**Central result:** Exhaustive coverage of 11 mutation classes × 40+ base agronomic records.  
BAA rejects every case. B5 fails on exactly the 4 missing-slot classes.

**Supporting results (all real):**
- Per-slot ablation (real measured values replacing E03 literals)
- Benign-mutation false-rejection rate
- Baseline failure characterisation (E27/E29/E30/E31 baseline halves — real API traces)
- Tamper detection E23, intent router E25, network model E14

**Conditionally restored (Q2=YES → Phase 4 active):**
- CL-3 end-to-end benchmark: n=300 from X2 — real numbers, whatever they are

**Honestly removed (Q1=NO):**
- CL-4 expert validation (E13 study did not happen)
- E27 B6 row (restored only when X2 completes)
- E32–E39, E03, "36 layers", "60,000 cases", §14.4 extrapolation, "mathematically impossible"
