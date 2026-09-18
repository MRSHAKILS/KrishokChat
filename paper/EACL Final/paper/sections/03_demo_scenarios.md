# 3 Demo scenarios (S1-S5)

S1: halt, chips, resume. The visitor types a crop-less treatment question in Bengali. The extractor returns empty crop, retrieval stays at zero sources, and the screen shows chips for rice, potato, and other crops with non-chemical guidance alongside. Selecting a chip resumes fenced retrieval with the chosen crop bound to the query.

Scope is shown in-cell. Det halt is 0.38 (N01b) on 200 farmer queries (single-reviewer labels). Pilot is 100/100 halts and 140/140 passes (PILOT, E09). Conformance is 0.86 with overall 0.458 as design conformance, not independent accuracy, with follow-up UNTESTED (N09). Metering is p50 89 tokens against context p50 2146 with no blended saving (N02). Live comparison is halt 0.10 vs det halt 0.38 at agreement 0.68, latency p50 4218.6 ms, quality 19/60 medium-plus, cost unmeasured with no coverage claim (N11).

S2: photo fence to card. The visitor uploads a potato leaf photo and adds a short Bengali note. The router assigns the photo to the potato model, the crop pre-binds retrieval, and the answer card lists evidence passages from potato sources only.

Scope is shown in-cell. Per-model top-1 is potato 0.90, rice 0.9625, wheat 0.9413, and brassica 0.9118 with ONNX agreement 1.0 within 5e-05; corn and chilli are unmeasured (N04). Router exact-match 0.0259 is diagnostic only. Family-mapped accuracy is 433/437 at 0.9908 [97.67, 99.64] with wheat-800 excluded. WASM timing is crop-classifier p50 51.3 ms (p95 52.9 ms) and wheat p50 16.7 ms (p95 17.6 ms), single-thread SIMD without COOP/COEP, 2-of-6-model subset. INT8 is size only: wheat reportable, rice rejected on 2.5pp drop, potato/brassica diagnostic-only.

S3: mismatch badge. The visitor pairs a rice photo with text naming potato treatment. The system keeps the photo crop, shows a badge that text and photo disagree, and asks for confirm-crop before any chemical. No chemical renders until confirmation.

Scope is shown in-cell. Badge capture is 53/54 farmer pairs and 400/400 PRISM pairs, 453/454 combined, with 0 false halts and explicit-text contradiction only (N07). The sole miss is farmer_q_63, an implicit crop. Divergence display is 68/80 at 0.85, which is divergence and not badge rate, with a prompted judge (E08).

S4: refuse with 16123. The visitor types a banned-chemical or poisoning request in Bengali, including injection-style wording. The upstream gate refuses, drops the dosage sentence, and renders a referral card with the 16123 helpline as terminal state.

Scope is shown in-cell. Attack success is 0.95% [0.26, 3.41] against 36.19% [29.99, 42.88] over 420 live calls. Bangla residual is 0.10 [5.5, 17.4] with embedded 4/10 and roleplay 2/10 as residual risk (E03+N12). Verifier per-type catches are 33/33, 30/31, 22/25, and 29/29 with 0/38 clean false positives on 38 answers, no pooling, dosage-claim sentences only (N03, SMALLN). Deterministic split is injections blocked 10/10 with off-topic refused 0/30; production LLM branch is unmeasured here (N06).

S5: SMS and offline. The visitor toggles SMS or offline mode on a verified answer. SMS shows a capped 160-character card; offline shows a cached card with service-worker precache.

Scope is shown in-cell. SMS is 299/300 offline-ready and 100/100 live-ready with 0 over-160, referral purity 16/16, and guard fix 9/9 flips (N05). Dose fields survive 0/84, so enforcement plus purity is claimed and dose survival is not. Offline BM25 hit is 0.94 with 0/400 cached; network deltas are SIMULATED loss (E06). Footprint is 95.64 MB unique ONNX, 284.0 MB minimal, and 339.6 MB full (E07). Tier mix is 7.8% zero-LLM at modeled 0.1798 USD per 1k (MODELED) (E10). Overhead p50 is 33.565 ms (safety 0.321 ms, retrieval 26.831 ms, verifier 4.815 ms) with live LLM latency UNMEASURED (E01). Envelope recall is 0.7165 with dangerous acceptance 0.374 as an OFFLINE stub, not deployment (N10).
