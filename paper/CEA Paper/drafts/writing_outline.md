# writing_outline.md — CEA Paper Writing Outline (final)

**Title:** Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support

**Venue:** Computers and Electronics in Agriculture (Elsevier) — Full Original Research Paper
**Target length:** ~9,000–12,000 words main text
**Format:** LaTeX `cas-dc` (Elsevier CAS double-column), driver `krishokchat_cea_main.tex`, bib `krishokchat_cea.bib`

---

## 1. Scientific spine (the argument the paper proves)

```
Agricultural evidence is relational
   → simple retrieval/citation can misbind facts (E02: 80% lexical dangerous acceptance; E05: 72.65% vanilla RAG under counterfactual)
   → typed, single-record binding is required (E28: 100% rejection vs ≤72% for all baselines)
   → certification is deterministic, traceable, reproducible (E03: every slot contributes; E19: provenance 100%)
   → unsupported conditions fail closed to clarify/abstain/escalate (E10 taxonomy; E38 escalation)
   → selective resolution bounds the cost of this safety (E04 risk–coverage; E18 51.04% deterministic advisory; E14/E15/E23 deployment)
```

## 2. Structure (18 sections — kept, matches the plan's final blueprint)

| # | Section | RQ | Core evidence layers | Headline numbers |
|---|---------|----|----------------------|------------------|
| 1 | Introduction | — | — | — |
| 2 | Related Work | — | positioning table | — |
| 3 | Problem Formulation | — | certification predicate, endpoints | — |
| 4 | BAA Architecture | — | tiers, verifier, gates | search space −75.64% (E17) |
| 5 | Knowledge & Governance | — | schema, authority, E23/E24 | 100% tamper; 58.7→64.2% coverage |
| 6 | Methodology | — | suites, baselines, stats | — |
| 7 | Results: Advisory Quality | RQ1 | E27, E13, E06 | 97.0% CAC, 0.0% CUAR, 4.82/5, AC1=0.862 |
| 8 | Results: Authority & Safety | RQ2 | E02, E28, E05, E29, E03, E11, E30, E31, E38 | 100% misbinding rejection, 0% CUAR |
| 9 | Results: Selective Reliability | RQ3 | E04, E25, E10 | AURC 0.0153, 84.56% @ 1.26% risk |
| 10 | Results: Linguistic & Multimodal | RQ4 | E17, E21, E35*, E12, E31 | +46.9 pp dialect coverage, 0% hazard |
| 11 | Results: Temporal & Knowledge | RQ4/5 | E30, E23, E24 | 100% gazette adherence |
| 12 | Results: Security & Delivery | RQ5 | E07/E08, E15, E22, E14 | 0/1400 leaks, 100% SMS slots, 91.4% edge |
| 13 | Results: Efficiency | RQ5 | E18, E9, E20 | 51.04% det, 2.28×, $0.0767/1k |
| 14 | Discussion | — | E10, E34 | — |
| 15 | Deployment Implications | — | E14, E9, E24, E38 | — |
| 16 | Limitations | — | E27–E39 provenance, small-n layers | — |
| 17 | Reproducibility | — | registry, seeds, hashes | — |
| 18 | Conclusion | — | — | — |

*E35 is explicitly excluded from the evidence chain and disclosed in §10 as a saturated, underpowered layer.

## 5. Figures (planned)

| Fig | Content | Source | Type |
|-----|---------|--------|------|
| F1 | BAA architecture | — | conceptual (GPT-generated) |
| F2 | Evidence→certification chain | — | conceptual |
| F3 | Risk–coverage curves | E04 | chart |
| F4 | Metamorphic rejection bars | E28 | chart |
| F5 | Slot-ablation hazard | E03 | chart |
| F6 | Deployment trade-off panels | E14/E18/E9/E20 | multi-panel |

GPT prompts are in `figures/README_figure_prompts.md`.

## 6. Tables (final mapping)

| Tab | Content | Source |
|-----|---------|--------|
| 1 | Reliability requirements | problem formulation |
| 2 | Literature positioning | related work |
| 3 | Two-layer evidence schema | §5 |
| 4 | Baseline ladder | §6 |
| 5 | End-to-end advisory (E27) | results §7 |
| 6 | Authority verification (E28 metamorphic) | results §8 |
| 7 | Risk–coverage calibration (E04) | results §9 |
| 8 | Register-robust routing (E21) | results §10 |
| 9 | Deployment efficiency (E14/E15/E18/E20/E22/E23) | results §12/13 |
| 10 | Failure taxonomy (E10) | results §9 |

## 7. Design decisions taken during writing

1. **Drop from main narrative:** national 16M-farmer cost projection (suppressed to a single scenario sentence in §13); E32/E33/E35/E37 layers (null or contradictory, disclosed in §16); E26 chunk-fallback (production feature, not paper evidence); E19 graph (proof-of-mechanism only, 23 nodes).
2. **Honest framing:** never "zero-risk"; every 0.0% carries an upper CI and is scoped to the evaluated suite; BAA latency is a modeled in-process figure, not a measured distribution; E14 is simulation; E38 is confounded (model per arm); E29 n-granularity caveat disclosed.
3. **Repositioning:** E17 = "retrieval-space reduction and register-robust routing" (not "dialect immunity"); E21 split into input/retrieval/advisory endpoints; E25 demoted (78.4% joint EM motivates absorbing routing uncertainty); E23 = deployment-integrity, not cryptography.
4. **Baselines:** canonical B0–B6 ladder defined in §6; per-layer subsets noted in each results section (the layers use different subsets of the ladder).
5. **Abstract numbers** restricted to the five headline results (E27 CAC/CUAR, E02/E28 binding, E04 coverage/risk, E18 efficiency, E14 resilience).

## 8. Open items for the researcher

- Run the figure-generation prompts (GPT) and drop the images into `manuscript/figures/`.
- Confirm the author list/affiliations and funding statement.
- Add any real field pilot results before submission (currently none).
- If newer layers (E27–E39) receive verification blocks in the registry, update §17 wording accordingly.