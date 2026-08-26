# KrishokChat — CEA-Pivot Implementation & Aggregation Plan

Author: research-engineering plan, 2026-08-27
Inputs: `paper/reviews/suggestions_1.md` (CEA pivot review), `paper/manuscript/` (Wiley Expert
Systems draft + frozen claim ledger), `research_artifacts/` (E02–E13 results),
`docs/production_readiness/tasks/R_SERIES_EXECUTION_INDEX.md` (R1–R12, all DONE).

---

## 1. Expert assessment — where we actually stand

**Manuscript.** A Wiley *Expert Systems* manuscript exists (`paper/manuscript/krishokchat_wiley_expert_systems.tex`,
~875 lines, compiled PDF) with a frozen claim ledger (S/F/U IDs) and a completed empirical battery
E02–E13: relational misbinding (10k adversarial cases), slot ablation, risk-coverage calibration,
counterfactual binding, farmer/dialect robustness (4k queries), prompt injection, latency/economics,
failure taxonomy, multi-generator invariance, retrieval degradation, and a 200-response human expert
study (Gwet's AC1 = 0.862). This is a real, defensible safety-grounding paper for an AI-systems venue.

**The review (suggestions_1.md)** argues that for *Computers and Electronics in Agriculture* the paper
must pivot from NLP benchmarking to systems engineering: rural network resilience, feature-phone SMS
delivery, low-end hardware profiling, BD telecom economics, and a "Detection-Gated Deterministic
Routing" (DGDR) architecture where vision detection + a knowledge graph resolve queries with zero LLM
calls and the LLM becomes an optional assembler. As a CEA-positioning argument this is correct — CEA
reviewers evaluate deployability under physical constraints, not attention mechanisms.

**Critical correction to the review.** Its "expected results tables" (92% success at 15% loss, 44.3%
zero-LLM resolution, 29.61ms on-device, 96.8% vs 91.2% intent accuracy) are **fabricated targets
presented as findings**. Under AGENTS.md rule 5 none of these can enter any manuscript as results.
Every number must be measured by the experiment specs in `specs/`. The review also proposes training a
FastText intent classifier — worthwhile only as an optional Tier-2 assist, not as a claim pillar on a
7-day-horizon-derived project.

**Our structural advantage.** The R-series (R1–R12, all done) already implemented the deterministic
half of DGDR in production code: five-tier resolution ladder (T0 kill switch → T1/T2 fact base with
zero LLM calls → T3 LLM phrasing → T4 refusal), fact base with potato late blight + maize FAW + rice
pests, structured resolver, offline fact pack, on-device ONNX classifier export, real RIMES weather,
tier-mix cost experiment. **We do not need to build DGDR; we need to measure it.** That reframing makes
E17–E19 high-feasibility: they instrument existing code rather than invent new architecture.

---

## 2. What we already have (aggregation inputs)

| Asset | Path | Role |
|---|---|---|
| E02–E13 frozen results | `research_artifacts/evaluations/**/*.yaml` | Safety-core sections (keep, retitle as "System Stress Tests") |
| 11-slot verifier + tier ladder | `backend/app/{application,domain,ports,infrastructure}/` | The system under test |
| Fact base (R2/R12) + ingestion contract | `backend/` + `docs/refactor/KNOWLEDGE_INGESTION_CONTRACT.md` | KG source for E19 |
| Offline fact pack (R9) | `backend/scripts/build_fact_pack.py` | E14 offline arm |
| On-device ONNX (R10) | `frontend/public/models/*.onnx` | E16/E17 detection arm (classifiers — no box claims) |
| Farmer benchmark 1,000 | `backend/ml_assets/rag_index/eval/farmer_benchmark_1000.jsonl` | E14/E17 workload |
| Dialect query sets (E06) | via `research_artifacts/scripts/runners/` | E17 dialect-immunity arm |
| Misbinding attack suite 10k | `research_artifacts/datasets/attacks/relational_misbinding/` | E15 tuple source |
| Golden replay gate 50/50, 410 tests | `backend/scripts/replay_golden.py` | Regression protection while adding layers |

---

## 3. Implementation phases (feasibility-ordered; canonical order incl. E21–E25 is §6)

**Phase 1 — deterministic core measurements (no hardware, ~2–3 days).**
1. **E17 detection-gated routing** (`specs/E17`): run crop/disease classifier metadata as a
   pre-retrieval filter over knowledge nodes; sweep gate confidence 0.70/0.80/0.90; measure
   search-space collapse and R@k per dialect register vs text-first. Report misrouting honestly.
2. **E19 KG traversal** (`specs/E19`): build the crop/pest/chemical/dose/phi graph from the fact base;
   measure tuple completeness by hop depth and produce a coverage-gap table (feeds fact-base
   extension instead of hiding holes).
3. **E18 zero-LLM fraction** (`specs/E18`): extend the R7 `tier_mix_experiment.py` harness with
   image-bearing queries; measure % of queries resolved with zero LLM calls and per-tier
   correctness against certified tuples.

**Phase 2 — channel resilience (~2 days).**
4. **E15 SMS compressor** (`specs/E15`): pure-python deterministic template; verify 100% survival of
   dose/PHI/tau slots at 160 chars (GSM-03.38 and transliterated variants) against 1,000 certified
   tuples; contrast arm with LLM-summarized SMS to document the truncation hazard.
5. **E14 network degradation** (`specs/E14`): toxiproxy/netem on loopback against the FastAPI backend
   under 4G/3G/Edge/2G profiles; compare cloud-only vs offline-first cache delivery success, cache-hit
   ratio, and stale-advisory safety violations (gate: zero).

**Phase 3 — economics + hardware (external inputs).**
6. **E20 telecom economics** (`specs/E20`): desk research with cited price sheets (bulk SMS ~0.20
   BDT, local VPS vs AWS); C_safe model driven by E18's measured tier mix; national-scale projection
   labeled as projection.
7. **E16 hardware profiling** (`specs/E16`): blocked on a physical sub-$120 Android device. If
   unobtainable, ship a clearly-labeled desktop latency/RAM proxy or mark as future work — never
   simulated battery numbers.

**Standing gates throughout:** full suite 410 passed / 7 skipped, golden replay 50/50, `pnpm build`
green, claim ledger updated with new S/F/U IDs after each frozen result.

---

## 4. Aggregation into the manuscript

Section mapping (per suggestions_1.md outline, corrected):

| Paper section | Sources |
|---|---|
| 1 Introduction (rural reality, contributions) | E06 dialect collapse (motivation), E18/E14 targets as contributions after measurement |
| 2 Architecture (edge client, tier ladder, SMS gateway) | R9/R10 implementation facts, E19 graph design |
| 3 Algorithms (11-slot verifier; cache invalidation; SMS compressor) | E02 suite; E15 template; new Alg: SHA-hash cache invalidation (design, implemented in offline pack updater) |
| 4 Stress-test methodology | E14–E20 specs as written |
| 5.1 Safety valve integrity | E02/E03/E05 (existing tables, retitled "System Stress Test 1/2") |
| 5.2 Network resilience | E14 results |
| 5.3 SMS fallback fidelity | E15 results |
| 5.4 Hardware reality | E16 results (or labeled proxy/future work) |
| 5.5 Dialect robustness | E06 + E17 (text-first vs detection-gated) |
| 5.6 Zero-LLM routing + economics | E18 + E09 + E20 |
| 6 Discussion (16123 / DAE integration, human-in-the-loop SAAO fallback) | existing escalation design + E13 human study |
| 7 Limitations | classification-only vision, SMS single-turn limits, E19 coverage gaps, E16 device availability |

Venue decision note: the Wiley Expert Systems draft (frozen ledger) and the CEA pivot share the safety
core; the CEA version is a systems re-frame, not a new paper. Decide target before rewriting Section 1.

---

## 5. Unique ideas beyond the review (now first-class experiment layers)

Each idea below has a spec in `specs/`, a runner folder in `scripts/`, and a results folder in
`results/` — runnable exactly like the review-derived layers:

1. **E23 — verified-invalidation audit trail:** hash-chained invalidation records over the R9
   offline pack; every cached advisory carries git-style provenance of the circular that certified
   it. Turns E14's "stale cache" metric into a provenance claim — our established differentiator.
2. **E21 — dialect immunity as a safety metric:** hazard rate conditioned on register × routing
   path (text-first vs detection-gated), Wilson CIs, failing-case ids listed per cell. Unreported in
   the Agri-LLM literature; computed from the 4,000-query E06 set. Depends on E17+E19.
3. **E24 — coverage-gap-driven fact-base growth loop:** E19 gap table ∪ C1 coverage analysis →
   author one real crop×pest extension (ingestion-contract sourced) → re-measure. Publishable as
   deployment methodology. Depends on E19.
4. **E22 — SMS as an attack surface:** E07/E08 injection suite through the compressor; the
   deterministic template has no free-text surface, so immunity should be 0.0 by construction —
   proven empirically, with the LLM-composed arm as contrast. Depends on E15.
5. **Golden-replay drift gate (protocol, not a layer):** every routing/threshold change re-runs the
   50/50 golden replay and records `golden_replay_drift` in the result YAML — enforced by
   `ACCEPTANCE_PROTOCOL.md` §6 rather than a separate experiment.

The **training experiment (E25)** — tiny supervised intent classifier on the frozen T09 split,
FastText-class + linear baseline vs LLM intent parsing — is specced as an optional Tier-2 assist:
offline research artifact only, never part of the deterministic-core claims, and any move into app
runtime requires a stack amendment per AGENTS.md §2.6.

---

## 6. Execution order (one branch per layer)

Dependency- and feasibility-ordered:

**Phase 1 (deterministic core):** E17 → E19 → E18
**Phase 2 (channel resilience + safety cross-tabs):** E15 → E22 → E14 → E21 → E23
**Phase 3 (economics + training + growth loop):** E20 → E25 → E24
**Blocked:** E16 (physical device required)
**Ready now:** E26 — R13 substrate shipped 2026-08-27 (Amendment 03 APPROVED; 4,815-chunk
index built, node→MD map 1,713/2,120, golden replay 50/50 with the flag on). Run E26 first:
it gates flipping `CHUNK_FALLBACK_ENABLED` default to ON and feeds E24's promotion queue.

Each layer follows `ACCEPTANCE_PROTOCOL.md`: spec → branch `experiment/E<NN>_<name>` → runner in
`experiments/scripts/<layer>/` → self-checks + determinism check + real-application check (backend
suite, golden replay, `pnpm build`, layer probe) → frozen YAML per `results/RESULT_SCHEMA_TEMPLATE.yaml`
→ registry status → claim-ledger entry → manuscript table. No layer may cite another layer's target
numbers; acceptance requires the author's signature in `acceptance.accepted_by`.
