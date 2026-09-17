# Beat B Experiment Plan — Slot Gating on Real Queries (v2, real-data)

**Status:** E09-400 demoted to PILOT; headline evidence = real runs below  
**Priority:** P0 · **Doctrine:** `REAL_DATA_DOCTRINE.md` (no templates as headline, floors in §4)

## 1. Research questions (unchanged, stricter evidence)

- **RQ-B1:** Gate halt/pass/refuse rates on real queries with expected-action labels.
- **RQ-B2:** Cross-crop hazard prevented vs a real blind-RAG arm on identical queries.
- **RQ-B3:** Real tokens/latency saved (metered, not assumed).
- **RQ-B4:** Deterministic matcher vs live-LLM NLU head-to-head at equal n.
- **RQ-B5:** Generalization beyond any constructed suite (farmer subset).

## 2. Primary evidence path (all real)

### G1 — PRISM-1000 full run (CPU-cheap, n=1000)
Run the frozen gate + router over all 1,000 PRISM rows; score predicted action/route vs `expected_route` + `needs_clarification`. Requires P0-7 provenance audit first. Metrics: clarification recall/precision, pass-through, safety-gate recall, confusion matrix, per-register breakdown (A–J), latency p50/p95, Wilson CIs. Floor: full set, no sampling.

### G2 — Authentic farmer evidence without annotators (doctrine §5)
No crowd labels. Three layers: (a) behavioral rates over Farmer-1000 (clarify/pass/refuse/verifier-flag distributions by source — descriptive, never "accuracy"); (b) team dual-review of stratified 100 (source × outcome strata; agreement reported, author review disclosed); (c) LLM-judge slot-preservation counts on normalizations, calibrated on ≥50 team-reviewed samples, non-safety metrics only.

### G3 — Paired blind-RAG arm (the 38.5 replacement)
PRISM rows WITH `true_crop`: B(100 colloquial) + C(100 dialect) + D(100 Banglish) + I(100 ambiguous) = **400 paired**, register-varied, zero humans needed. Blind arm: gate bypassed, top-5 over frozen 2,135-node index. Hazard = fraction with ≥1 top-5 source whose crop label ≠ gold crop (frozen source→crop mapping, freeze BEFORE running). Gated arm measured identically. Report paired delta with McNemar + CIs. Separately, F-row descriptive (no labels needed): distinct-crop spread in blind top-5 on 100 crop-less queries — the hazard made visible. No constants anywhere.

### G4 — Metered tokens + latency (real strings, full sets)
On G1+G2 runs: record actual clarification-template tokens vs actual retrieval-context + generation + verifier tokens (project tokenizer, real strings), plus stage timers. Report p50/p95 savings and the modeled-vs-metered comparison. Live-generation tokens metered on the T3 subset via API usage records.

### G5 — Matcher vs live-LLM NLU at equal n (real API)
Expand the live arm from n=60 to n=400 (same 400 as a frozen G-subset): gating recall, pass-through, refusal, per-query latency, API cost. Head-to-head table with CIs. API spend approved.

## 3. E09-400 disposition

Kept as **PILOT**: method reference + per-record diagnostic value. Its rates may appear in an appendix row labeled "template-constructed pilot (seed 42)" — never in Tab.2, never in the abstract. The OOD-0.25 audit (P0-6) still runs, because the category design flaw (mixed off-topic/injection under one tier) must not repeat in real labeling — the G2 codebook splits them by construction.

## 4. E03 expansion (P1, real API)

Current 420 calls (7×30×2) stay as v1 with CIs. Expansion to n=100/family (700/arm, 1,400 calls) runs if API budget/timeline allows; decision by Day 4. Bangla-native family oversampled first if partial (it's the residual-risk family).

## 5. Gates

- **Gate 0:** PRISM audit done; G2 codebook frozen; blind-arm hazard definition + crop-label mapping frozen; tokenizer fixed; hashes recorded.
- **Gate 1:** G1 full run → G3 paired arm (same frozen system, no tuning between arms) → G4 metering from stored strings.
- **Gate 2:** G2 labeling (annotators) → frozen-system scoring → κ + metrics.
- **Gate 3:** G5 live arm at n=400 → head-to-head table.
- **Gate 4:** paper decision per arm using fallback sentences (critic review §5) where an arm misses.

## 6. Status marks

- [x] Doctrine + floors fixed (no-annotator protocol per demo precedent)
- [x] E09-400 demoted to PILOT (kept, labeled)
- [x] PRISM label audit for N01: 700/1000 rows carry true_crop; blind set = B+C+D+I (400 paired); F rows = descriptive spread stat
- [ ] P0-7 PRISM audit → unlocks G1
- [ ] G1 full run (n=1000)
- [ ] G3 paired blind arm (n≥300) + McNemar
- [ ] G4 metering (real strings) + modeled-vs-metered
- [ ] G2 authentic layer: behavioral rates (Farmer-1000) + team dual-review 100 + calibrated LLM-judge counts (no crowd labels per doctrine §5)
- [ ] G5 live arm n=400 + cost log
- [ ] P0-6 OOD audit (design lesson for G2 codebook)
- [ ] E03 expansion decision (Day 4)
