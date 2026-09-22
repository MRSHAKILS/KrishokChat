# 2 System: T0-T4 ladder with halt, fence, and verifier

KrishokTech processes each Bengali query through five stages: T0 deterministic safety precheck, T1 extractor and gate, T2 fenced retrieval, T3 untrusted generation, and T4 verifier plus rendering. T0 screens for banned chemicals, poisoning, and crisis and routes matches to the 16123 helpline without retrieval or generation (p50 0.321 ms). T1 decides whether retrieval is allowed at all.

[FIGURE Fig.1: five-stage pipeline T0-T4 with halt exits A3/A4/A5, fence input from vision, and verifier gate before four renderings.]

T1 uses a deterministic extractor for crop, symptom, and treatment intent. Treatment intent with empty crop halts retrieval and selects A4 clarification with quick-reply chips, A3 non-chemical guidance, or A5 refusal with 16123. The gate runs before any BM25 call, so halted turns retrieve zero sources. Live comparison shows det halt 0.38 (N01b) against live-model halt 0.10 at agreement 0.68, with cost unmeasured and no coverage claim (N11).

T2 runs only when the gate passes. BM25 retrieval is crop-bound: the text crop or the photo crop restricts the index before ranking (BM25-only throughout; dense retrieval unevaluated). The vision path uses a tri-state gated router to per-crop disease models (potato 0.9504, rice 0.9625, wheat 0.9413, brassica 0.9729, corn 0.9723, chilli 0.9907 top-1 across 4,294 test images; ONNX agreement 1.0 within 5e-05).

Router exact-match 0.0259 is a mismatch diagnostic only; family-mapped accuracy is 433/437 at 0.9908 [97.67, 99.64] with wheat-800 excluded as out-of-space. Browser WASM measures crop-classifier p50 51.3 ms (p95 52.9 ms) and wheat p50 16.7 ms (p95 17.6 ms) in single-thread SIMD without COOP/COEP on a 2-of-6-model subset. INT8 is a size story only: wheat, potato, and brassica are reportable (all drops <= 0.09pp <= 2.0pp gate), while rice is rejected on a 2.5pp drop. Text that contradicts the photo crop raises a badge and asks for confirm-crop before any chemical, scoped to explicit-text contradiction (N07).

T3 generates from fenced evidence only and is treated as untrusted. T4 checks every dosage-claim sentence with same-passage binding and dose-band comparison, then annotates and drops unsupported sentences (p50 4.815 ms; live LLM latency UNMEASURED). Surviving sentences carry authorship badges that separate quoted evidence from model wording and mark dropped claims.

One verified decision renders four ways: full answer, SMS capped at 160 characters, offline cached card, and 16123 referral. SMS enforcement and referral purity are measured (N05); dose fields do not survive truncation (0/84) and need a packer. Offline BM25 hit is 0.94 with 0/400 cached and service-worker precache, with network deltas SIMULATED as loss (E06). Tier mix leaves 7.8% of turns at zero LLM with modeled cost 0.1798 USD per 1k turns (MODELED; T1 0.0% reflects a 9-fact base) (E10). Provenance traces order fully (100/100, events p50 9.0) (E04).

[FIGURE Fig.2: workspace with answer card, badge strip, Why/trace panel, and SMS/offline toggle.]
