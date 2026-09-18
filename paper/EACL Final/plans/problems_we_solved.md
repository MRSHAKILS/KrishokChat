# Problems We Solved (locked story — every row traces to ground_truth.yaml)

## C1 — Halt before retrieval (E09 pilot + N01b + N09 + N02 + N11)
**Problem:** crop-less symptom queries make blind retrieval return index-dominant-crop sources, which fluent generation verbalizes as confident wrong-crop advice.
**Prior art failure:** Krishi Sathi / Farmer.Chat classify intent, then retrieve anyway; neither publishes halt rates, hazard deltas, or cost deltas for the gating decision.
**Mechanism:** deterministic extractor → `crop = ∅` on treatment intent → clarification with zero retrieval (A4); A3 non-chemical guidance; A5 refuse + 16123.
**Measured:** E09 pilot 100/100 halts; N01b real 38% halt, extractor agree 51% / FP 0.5%; N09 clarification conformance 0.86; N02 metered clarification p50 89 vs context p50 2146; N11 live-vs-det trade-off (10% vs 38% halt, 4.2s vs ms).
**Feel:** the cheapest and safest retrieval is the one the system refuses to run.

## C2 — Fence + badge (N04 + N08 + N07 + E08)
**Problem:** text-only retrieval poisons the wrong crop; vision-only diagnosis never sees text disagreement.
**Prior art failure:** AgroGPT/PlantVillage diagnose; nobody publishes retrieval fencing or text-vs-image conflict rates for Bengali advisory.
**Mechanism:** tri-state gated crop router → per-crop disease models → crop pre-binds the advisory query; text-vs-image mismatch → badge + confirm-crop before any chemical.
**Measured:** per-model top-1 0.90–0.96 + 100% ONNX parity; fence 36.25%→30.0% (25/0, p<1e-6) + purity up; badge 53/54 farmer + 400/400 PRISM pairs halt (453/454), 0 false-halts; E08 divergence 68/80.
**Feel:** the photo is a fence around the evidence — when words jump the fence, the system says so.

## C3 — Two walls, one mouthpiece, four renderings (E03 + N03 + N05 + E06 + E07 + E10)
**Problem:** oracle evidence still leaves 4–7% chemical hallucinations (companion benchmark); SFT collapses refusal; unconstrained models fail 83% of Bangla injections (n=100).
**Prior art failure:** judges score answers post-hoc; nobody drops sentences pre-render with same-passage binding + dose-band check + visible authorship; no refusal path dials a real helpline.
**Mechanism:** upstream gate (Tier-0 + classifier) → untrusted generator → dosage-claim verifier (same-passage binding, annotate-and-drop, ~5ms) → authorship badges → one decision rendered as full answer / SMS / offline / 16123 referral.
**Measured:** E03 0.95% vs 36.19% ASR with CIs; N03 catch 33/33 + 30/31 + 22/25 + 29/29, FP 0/38, CIs in spec (small-n, no pooling); N05 SMS 0 over-limit + referral purity + guard fix proven; offline BM25 0.94; 284MB minimal.
**Feel:** the LLM is the mouthpiece; the evidence is the witness; the verifier is the judge — and the farmer sees all three.

## Kill-list (claims we refuse to make)
First-Bengali-RAG · first-multimodal · first-voice · 11-slot live certification · SUS scores · guaranteed SMS dose survival · measured network retention · INT8-for-all · INT8 speedup · voice/ASR claims · $2.30/92% figure (deleted) · 38.5% baseline (retired) · 88% tokens (retired) · E08 100% (was README error, fixed) · pooled purity 0.6924 (corrected to per-arm) · "proven equivalent" (p=1.0 is no-observed-difference only).
