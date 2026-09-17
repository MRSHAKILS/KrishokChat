# Critic Review — 7-Day Practical Verdict (2026-09-17)

**Reviewer role:** adversarial EACL System Demonstrations reviewer, pre-submission, hard 1-week deadline.  
**Scope:** files listed in the dispatch brief (roadmap, problems_we_solved, paper_outline, beats, datasets_inventory).  
**Labels:** `[FILE]` = verified in our files. `[REC]` = reviewer recommendation. No new numbers, no new citations.  
**Full report saved verbatim below; execution follows Lane A→B→C (§6).**

---

## 1. Feasibility: P0-1..P0-11 + P1-1..P1-4 in 7 Days

### Verdict: no, not as written.

`[FILE]` The freeze lists 11 P0 items plus 4 P1 items. Serial load is 8–9 work-days in a 7-day window. The "hours" tags undercount review, re-run, and write-up time. Four P1s alone need ~4 days.

### Cut / reorder — three lanes

**Lane A — must land (Days 1–4):** P0-11 (STATE + comment repair) · P0-10 (E08 README + relocate run_e21.py + 12/80 analysis) · P0-1 + P0-2 as ONE harness (blind arm + metering, shared queries) · P0-4 narrowed (accuracy + FP32 parity only; INT8/WASM only if first pass passes) · P0-9 (UI wiring pointers) · P0-5 lite (SMS N=200 + encoding audit).

**Lane B — land if Lane A clears (Days 4–5):** P0-6 (OOD audit) · P0-3 lite (catch-rate on 100 mutated answers, 4 types) · P0-7 lite (PRISM script review, no re-generation).

**Lane C — defer:** P0-8 full embedding regen (freeze with BM25-only label instead) · P1-1..P1-4 (each needs a P0 first) · all CUT items stay cut.

### Minimum viable evidence set (if only half lands)

1. E09 gating rates (100/100, 140/140, 70/70) + matcher-vs-LLM contrast (1.00 @ ~3ms vs 0.80 @ ~4.2s, n=60).
2. E03 pair: 36.19% vs 0.95% with CIs + 6.67% leak disclosed.
3. Vision narrowed: per-model top-1 + 100% parity on current checkpoints; else E08 68/80 alone with re-validation pending.
4. Tier mix (7.8% zero-LLM), E01 overhead, E06 BM25 0.94, E07 footprint.
5. Honesty table (Tab.1) + live URL + 150-s screencast.

---

## 2. Track Fit

Framing fits (usefulness + integration + reusability + clarity). C1 clearest measured effect; C2 most filmable; C3 closes deployment. S1–S5 map to reviewer clicks; Tab.1 matches what demo reviewers reward.

**Oversold:** "two walls" implies a method — keep "dosage-claim verifier" everywhere, 11 slots to one companion sentence. Fence needs scope-delta number or stays architecture + divergence. 7.79% too small to carry C3 — present as measured floor with 9-fact base. Catch-rate prose stays conditional.

**Undersold:** real-browser WASM split · matcher-vs-LLM contrast (put in abstract) · Bengali authorship badges · 16123 as terminal state (name in S4 + S5) · BM25-first offline determinism with stub qualifier.

## 3. Desk-Reject / Trust-Killing Risks (22 items, severity ranked)

CRITICAL: R1 8.0 vs 6 pages · R2 dead URL / missing >2:30 video · R3 38.5% as in-run baseline · R18 6.67% leak rounded to zero (ethics).
HIGH: R4 88% as metered · R5 E08 100% README · R6 class-count mismatch · R7 GSM-segment math · R8 SMS guarantee vs truncation · R9 network deltas as field data · R10 stub latency implied as live · R11 dense provenance · R12 SUS implied · R13 11-slot implied live · R19 corpus-unit confusion · R20 license/build/imgsz.
MED: R14 unimplemented features shown · R15 $2.30/92% revived · R16 INT8-for-all · R17 OOD/dialect averaged away · R21 PRISM pre-audit citation · R22 stray run_e21.py.

Fix order: page cut, URL/video/license/build, blind-arm label, E08 repair, class-count reconciliation, leak disclosure.

## 4. Blind Spots the plan missed

1. Live-demo hardening: freeze 5 canonical inputs + expected outputs + stub fallback banner + backup offline capture.
2. Screencast production: captions, Bengali fonts, URL burn-in, English narration, 720p test.
3. Licensing + artifact freeze in one appendix table; confirm frontend models match re-run checkpoints.
4. Related-work 4-row table moved into the paper (Farmer.Chat / KrishokBondhu / Krishi Sathi / CoPilot) + first-X disclaimers.
5. Statistics: Wilson/Clopper-Pearson intervals on E09 rates, E08 68/80, re-run accuracy; n/split/seed/hash under Tab.2; never average OOD 0.25 away.
6. End-to-end ablation (−gate/−verifier/−fence) named as future work in Limitations.
7. False-positive/recovery costs: one Limitations sentence each.
8. Fact-base + latency scope: T1 0.0% explained by 9-fact base; all p50 exclude live generation — stated once.

## 5. Fallback Prose (paste-ready, one per P0 — use verbatim if the item misses)

- **P0-1:** "…the gate halts 100/100 ambiguous queries with zero retrieval; we did not measure a paired blind-retrieval hazard in-run, so we report no hazard delta and mark the prior 38.5% figure as an external constant excluded from results."
- **P0-2:** "Token savings use estimated per-turn budgets (150 vs 1250) and are labeled modeled; we report no metered token counts."
- **P0-3:** "The dosage-claim verifier is implemented with p50 ~4.82 ms on the E01 400-query sweep (BM25-only, stub LLM); its precision/recall on mutated answers is unmeasured and we claim latency plus mechanism only."
- **P0-4:** "Vision accuracy and parity figures predate the current 10-class checkpoints and are excluded from Tab.2; we report only E08 divergence 68/80 on the current stack and mark re-validation pending."
- **P0-5:** "The SMS endpoint enforces a 160-character Bengali advisory with 16123 fallback; field-level dose survival through truncation is unmeasured, so we claim enforcement only and frame length as characters, not GSM segments."
- **P0-6:** "The out-of-scope/injection category scores 0.25 on n=40 with mixed probes under one expected tier; we show the row separately and scope the gating claim to ambiguous, specified, and safety-critical categories."
- **P0-7:** "We do not cite PRISM-1000 scores; the set is LLM-assisted with unverified protocol, so all gating evidence comes from the E09 template suite."
- **P0-8:** "Dense provenance is unverified, so all retrieval evaluation uses the frozen BM25 index over 2135 chunks (hash recorded); dense remains API-gated fallback and out of scope."
- **P0-9:** "We describe badges, flags, and 16123 affordances as implemented endpoints and do not claim user-visible rendering for any element without a cited component pointer."
- **P0-10:** "Cross-modal evidence is 68/80 output divergence between image-only and conflicting-hint runs through the real `.pt` plus BM25-stub harness; we frame it as visible divergence, not a user-facing badge rate."
- **P0-11:** "The deployed classifier reads 10 classes including Rice per `class_names.json`; pipeline comments or STATE text that say 6-class are stale and excluded from normative description, with wheat-mitigation behavior marked under review."

## 6. Top 5 Actions (in order; each ends with a paper-unblocking artifact)

1. **Day 1 — freeze + repair trust** (P0-11, P0-10, hashes) → appendix hash table; writing starts on §§1–3 + appendix.
2. **Day 2 — replace dishonest constants** (P0-1 + P0-2 + P0-6, one harness) → measured hazard + metered token pairs or fallbacks.
3. **Days 3–4 — re-validate vision** (P0-4 narrowed + P0-9) → Tab.2 vision rows or fallback; S3 prose locked to what renders.
4. **Day 5 — close delivery honesty** (P0-5 lite + P0-3 lite) → SMS sentence + verifier row or fallbacks; capture 150-s screencast on frozen build.
5. **Days 6–7 — cut to 6.0 pages + pass gate** (cut list; abstract last) → live URL serves S1–S5, video linked, clean-checkout build, license stated, zero killed claims, every number labeled.
