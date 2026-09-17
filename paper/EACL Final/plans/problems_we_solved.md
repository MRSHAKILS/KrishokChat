# Problems We Solved — The Compressed Story (3 Contributions)

**Status:** synthesis v1 — derived from beats A, B, F, D+E, C+G (2026-09-17)  
**Rule:** every row below must survive the question "so what did the farmer get that no other system gives?"  
**Paper budget:** these three contributions + honesty notes are ALL the novelty the 6 pages may claim.

---

## C1 — Halt before retrieval: the missing crop stops the pipeline, not the answer

| | |
|---|---|
| **Problem** | A crop-less symptom query ("পাতায় দাগ, কী স্প্রে করব?") makes blind retrieval return *something* — usually from the index-dominant crop — and generation verbalizes it fluently. Over-advising, not silence, is the documented dominant failure (Yang 2024; IPM-AgriGPT). |
| **Prior-art failure** | Krishi Sathi and Farmer.Chat classify intent/slots and then retrieve. Neither publishes a halt rate, a hazard delta, or a cost delta for the gating decision itself. |
| **Our mechanism** | Deterministic extractor → `crop = ∅` on treatment intent → A4 clarification with **zero retrieval**; A3 non-chemical guidance; A5 refuse + 16123. Matcher-first; live LLM only when needed. |
| **Measured effect** | E09 n=400: 100/100 halted, 140/140 passed, 70/70 refused, 0% leak. Matcher 1.00 @ ~3ms vs live-LLM NLU 0.80 @ ~4.2s (n=60). Blind-arm hazard delta + metered tokens: P0 repairs in flight. |
| **Feel** | The cheapest and safest retrieval is the one the system refuses to run. |

## C2 — Fence + badge: the photo narrows the evidence; the contradiction stops it

| | |
|---|---|
| **Problem** | Text-only retrieval poisons the wrong crop; vision-only diagnosis never sees text disagreement ("begun" text + potato-blight photo). |
| **Prior-art failure** | AgroGPT/PlantVillage diagnose; nobody publishes retrieval fencing or text-vs-image conflict rates for Bengali advisory. |
| **Our mechanism** | Tri-state gated crop router → per-crop disease models → crop pre-binds the advisory query; text-vs-image mismatch → badge + confirm-crop before any chemical; Bengali recovery prompts at every degradation. |
| **Measured effect** | Per-model top-1 0.90–0.94; 100% ONNX parity n=1,237; INT8 gated (crop+wheat reportable); WASM 26–265ms real-browser; 68/80 divergence. E02 re-run + badge-rate/fence studies: P0/P1 in flight. |
| **Feel** | The photo is a fence around the evidence — and when words jump the fence, the system says so. |

## C3 — Two walls, one mouthpiece, four renderings

| | |
|---|---|
| **Problem** | Oracle evidence still leaves 4–7% chemical hallucinations (2606); SFT collapses refusal to 0.31%; unconstrained model fails 76.67% of Bangla injections (E03). Fluency lies, especially about numbers. |
| **Prior-art failure** | Judges score answers post-hoc (RAGChecker, CiteEval, DG-Eval). Nobody drops sentences pre-render with same-passage binding + dose-band check + visible authorship — and nobody's refusal dials a real helpline. |
| **Our mechanism** | Upstream gate (E03: 0.95% vs 36.19%) → untrusted generator → dosage-claim verifier (same-passage binding, annotate-and-drop, ~5ms) → authorship badges → one decision rendered as full answer / SMS / offline / 16123 referral. |
| **Measured effect** | E03 both arms with CIs; verifier latency measured; catch-rate study P0 in flight; tier mix n=1000 (7.8% zero-LLM, modeled 7.79% savings disclosed); offline BM25 0.94 + SW precache; 284MB minimal. |
| **Feel** | The LLM is the mouthpiece; the evidence is the witness; the verifier is the judge — and the farmer sees all three. |

---

## Kill-list (what did NOT survive, and why)

| Killed | Reason | Where it lives now |
|---|---|---|
| Beat A as a 4th contribution ("dialect-aware retrieval") | Components established; our intervention unmeasured; companion paper owns the diagnosis | Motivation section only (2–3 sentences + 2608 citation) |
| "First Bengali agri-RAG / first multimodal / first voice" | KrishokBondhu, Farmer.Chat, Krishi Sathi predate us on each axis | Never claimed; competitors cited as precedent |
| Full 11-slot authority in the live path | Product verifier checks dosage claims; 11-slot is the CEA companion | Scope sentence + CEA citation |
| "Guaranteed SMS dose survival" | Mechanism is truncation; survival unmeasured | P0 survival study decides the final sentence |
| Measured network-retention numbers | Simulated loss lane | Labeled simulation; throttle lane optional P1 |
| INT8 "for all models" | Only crop+wheat reportable; rice rejected; corn unmeasured | Gated reporting; re-run confirms |
| Any SUS / user-study score | No recruited study ran | Observability proxy labeled as proxy; IRB study = future work |
| E09 blind 38.5% as in-run baseline | Hardcoded constant | P0 blind-arm replacement |
| E09 88% tokens as metered | (1250−150)/1250 assumption | P0 metering replacement |
| E08 README 100% + run_e21.py | Wrong script documented | P0 rewrite + relocation |
| $2.30/92% cost figure | Unsourced — DELETED everywhere 2026-09-17, never cite |
| Voice ASR/TTS, admin editor, gap-loop, A/B sandbox, provenance graph | Unimplemented or unevaluated | Future work at most; never main text |
| New 8-form × 200-intent annotation as primary evidence | Demo track accepts released benchmarks; 1 week left | Optional P2 only |

---

## Honesty ledger (every paper number carries one of these labels)

- **MEASURED:** gating rates, E03 both arms, verifier latency, vision accuracy/parity (post re-run), tier mix, offline determinism, footprint.
- **MODELED (disclosed):** token/cost savings — until metering lands.
- **SIMULATED (labeled):** network retention lane.
- **IMPLEMENTED (unevaluated):** verifier catch-rate, SMS survival, badge trigger rate — until their studies land.
- **PROJECTION:** fact-base expansion savings; never a result.
- **CUT:** SUS, 38.5-as-baseline, 100% E08, 11-slot live, voice claims.
