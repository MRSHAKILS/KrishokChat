# Paper Outline — 6 Pages, 1 Week, Demo Track

**Status:** synthesis v1 (2026-09-17) · **Venue:** EACL System Demonstrations · **Budget:** ≤6 pages + refs/appendix + live URL + ≤2.5-min screencast  
**Demo-track doctrine:** usefulness + integration novelty + reusability + clarity. Not SOTA-beating. Reviewers ask: does it work live, what's new vs existing systems, can I try it, is the evaluation honest.

---

## 1. Page budget

| Section | Pages | Paragraphs | Content |
|---|---|---|---|
| Title/authors/abstract | 0.3 | 1 | Hook (crop-less query → halt; fluent number → dropped; photo → fence), C1–C3 in one sentence each, artifact link |
| 1. Introduction | 0.7 | 5 | P1 problem (Bengali smallholder, fluency≠authority) · P2 why normal stacks fail (2608 gap, 2606 floor, E03 76.67% — 3 numbers max) · P3 integration thesis · P4 contributions C1–C3 · P5 artifact + demo map |
| 2. System | 1.3 | 7 | Fig.1 pipeline (5 stages, one figure) · safety→extract→gate ladder (C1) · hybrid retrieval scoped by text/image crop (C2) · verifier + badges (C3) · dual Farmer/Expert view · delivery renderings (app/SMS/offline/16123) · Tab.1 capability→evidence-status table |
| 3. Demonstration scenarios | 1.2 | 5 vignettes + Fig.2 | S1 crop-less halt + chips · S2 photo fence → Safe Action Card · S3 contradiction badge · S4 banned-query refuse + 16123 · S5 SMS/offline render. Fig.2: two screenshots (workspace + Why/trace). Each vignette ≤8 lines |
| 4. Evaluation | 1.7 | 6 + Tab.2 | Tab.2 compact results (gating, E03 pair with CIs, verifier latency + catch-rate if landed, vision accuracy/parity, tier mix, offline/footprint) · P1 gating (E09 + blind-arm + metering) · P2 safety walls (E03 + verifier) · P3 vision (E02 re-run + E08) · P4 cost/delivery (tier mix modeled-disclosed + SMS survival if landed) · P5 limitations (OOD 0.25, dialect 0.80, 6.67% leak, stub-LLM scope) · P6 reproducibility (hashes, splits, code) |
| 5. Related work | 0.4 | 2 | P1 agri advisory systems (Farmer.Chat, KrishokBondhu, Krishi Sathi, Hossain) — what they lack (gate rates, fence, walls) · P2 verification/retrieval/dialects (RAGChecker, CiteEval, GaRAGe, BUNO/BhasaBodh, 2608/2606 companions) |
| 6. Conclusion | 0.2 | 1 | One-para close: designed for the phone/network/budget at hand + field-study future |
| References | unlimited | — | ~20: companions, closest systems, eval methods |
| Appendix | unlimited | — | Flowcharts, E09 category table, artifact hashes, map versions, CIs |

**Total: 5.8 pages.** Flowcharts live ONLY in the appendix. No second architecture figure. No 11-slot derivation. No CI tables beyond E03.

## 2. Figure/table slots (5 total, frozen)

1. **Fig.1** — end-to-end pipeline (safety → extract/gate → scoped retrieval → verify → 4 renderings). Vector/TikZ.
2. **Fig.2** — two screenshots: farmer workspace (chips + Safe Action Card) + Why/trace panel.
3. **Tab.1** — capabilities × status (implemented/measured/modeled/pending) — the honesty table reviewers love.
4. **Tab.2** — results compact (see §4 above). One table, not five.
5. **Appendix figs** — slot-disambiguation + multimodal flowcharts (already exist).

## 3. One-week experiment freeze (feasible with CPU power; no annotation)

| # | Task | Effort | Owner | Gates |
|---|---|---|---|---|
| P0-1 | B blind-RAG arm on CAT1-100 (replace 38.5) | hours | agent | freeze hazard def first |
| P0-2 | Token metering, frozen 100-subset (replace 88% assumption) | hours | agent | shared B + C+G |
| P0-3 | F catch-rate study, ~200 × mutations | ~1 day | agent | freeze mutation set first |
| P0-4 | E02 re-run on current checkpoints + parity + INT8 + WASM | ~1 day CPU | agent | inventory + hashes first |
| P0-5 | CG SMS survival N=200 + encoding audit | hours | agent | — |
| P0-6 | OOD-category audit (split + re-label or gate fix) | hours | agent | — |
| P0-7 | PRISM provenance audit (script review) | hours | agent | — |
| P0-8 | Embeddings provenance audit / checkpoint regen | hours | agent | — |
| P0-9 | UI-wiring checks (flags, badges, 16123 dial) with pointers | 2 hrs | agent | — |
| P0-10 | E08 README rewrite + stray script relocation + 12/80 analysis | hours | agent | — |
| P0-11 | Stale vision comments + STATE correction; wheat-mitigation decision | 1 hr | human/agent | — |
| P1-1 | PRISM-1000 route scoring (confusion matrix) | ~1 day | agent | after P0-7 |
| P1-2 | Badge-rate study (text×image pairs) | ~1 day | agent | after P0-4 |
| P1-3 | Fence study (scope delta with/without image) | ~1 day | agent | after P0-4 |
| P1-4 | End-to-end 100-item probe | ~1 day | agent | after P0-3 |
| CUT | Paired 8×200 annotation, E03 expansion, live-400, throttle lane, recovery/OOD char. | — | — | P2, only if week allows |

**Writing runs in parallel:** §§1–3 + appendix scaffolding start immediately on existing numbers; §4 fills as P0s land; abstract written last.

## 4. Screencast (150 s) + live gate

0:00–0:10 hook · 0:10–0:40 S1 halt→chips→resume · 0:40–1:05 S2 photo fence → card · 1:05–1:25 S3 badge · 1:25–1:45 S4 refuse + 16123 · 1:45–2:10 S5 SMS/offline · 2:10–2:25 trace/Why + badges · 2:25–2:30 URL. One continuous capture, Bengali UI, no cinematic editing.

**Desk-reject gate (must all be true):** live URL serves the S1–S5 path · video ≤2:30 linked · PDF ≤6 pages builds clean · license stated · no SUS/11-slot/voice claims in text.

## 5. Definition of done

6-page PDF + live demo + video + every number labeled (measured/modeled/simulated) + all P0s landed or explicitly marked pending-with-prose-fallback + zero killed claims resurrected.
