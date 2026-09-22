# 4 Evaluation

Table 2 reports ground-truth rows only. Each cell carries its limit. Costs are MODELED, network deltas are SIMULATED, and live LLM latency is UNMEASURED except where labeled live. No blended token saving is claimed. Pilot rows are labeled PILOT and never headlined.

## C1: halt before retrieval

| Measure | Result | Limit in-cell |
|---|---|---|
| Det halt, 200 farmer queries (N01b) | 0.38 (76 halted) | Single-reviewer labels; no gate-silent mappable set in real data |
| Extractor detail (N01b) | Agreement 0.52; miss 0.475; FP 0.005; hazard mapped 0.1607 [8.69, 27.81]; firewall case farmer_q_593 | Single-reviewer; hazard is mapped subset only |
| Pilot halt/pass (E09) | 100/100 ambiguous halt; 140/140 specified pass | PILOT; supports design, not headliner |
| Conformance (N09) | Clarification 0.86; overall 0.458 | Design conformance, not independent accuracy; follow-up UNTESTED |
| Token metering (N02) | Clarification p50 89 vs retrieval-context p50 2146; live input p50 1111, output p50 221 | No blended saving claimed |
| Live vs det, 200 queries (N11) | Live halt 0.10 vs det halt 0.38; agreement 0.68; live latency p50 4218.6 ms; quality 19/60 medium-plus | Cost unmeasured; no coverage-superiority claim |

The headliner is the farmer det halt 0.38 (N01b). The pilot (E09) shows the gate behaves as designed under clean prompts. N02 shows why halting matters for cost: a clarification turn is p50 89 tokens where a retrieval context would be p50 2146 tokens, without combining the two into one percentage. N11 frames the operating point: the live model halts less often and answers in seconds, while the deterministic gate halts more often in milliseconds, with no claim that either covers more needs.

## C2: fence and badge

| Measure | Result | Limit in-cell |
|---|---|---|
| Per-crop top-1 (N04) | Potato 0.9504; rice 0.9625; wheat 0.9413; brassica 0.9729; corn 0.9723; chilli 0.9907; ONNX agreement 1.0 within 5e-05 | All 6 disease models measured on full test sets (N=4,294); router exact-match 0.0259 is diagnostic ONLY |
| Router family-mapped (N04) | 433/437 at 0.9908 [97.67, 99.64] | Frozen pre-run mapping; wheat-800 excluded as out-of-space |
| INT8 (N04) | Wheat, potato, and brassica reportable (drops <= 0.09pp <= 2.0pp gate); rice rejected on 2.5pp drop | Size story only; never speedup |
| Browser WASM (N04) | Crop-classifier p50 51.3 ms, p95 52.9 ms; wheat p50 16.7 ms, p95 17.6 ms | Single-thread SIMD without COOP/COEP; 2-of-6-model subset |
| Fence (N08) | Open wrong-crop 0.3625 vs fenced 0.30; discordant 25/0; McNemar p 5.96e-08; purity open 0.6472 vs fenced 0.7353 | Perfect-gold simulation upper bound, not classifier performance |
| Badge (N07) | 53/54 farmer and 400/400 PRISM, 453/454 combined; 0 false halts; PRISM CI [99.05, 100.0]; sole miss farmer_q_63 implicit | Explicit-text contradiction only |
| Divergence (E08) | 68/80 at 0.85 | Divergence, not badge rate; prompted judge |

Fencing cuts wrong-crop advice in simulation with all discordant movement in the safe direction (25/0). Purity is reported per arm (0.6472 open, 0.7353 fenced) with no pooled value. Badge capture is reported split (53/54 farmer, 400/400 PRISM) before the combined 453/454, with scope held to explicit contradiction.

## C3: two walls and four renderings

| Measure | Result | Limit in-cell |
|---|---|---|
| Safety, 420 live calls (E03+N12) | BAA 0.95% [0.26, 3.41] vs unc 36.19% [29.99, 42.88]; Bangla BAA 0.10 [5.5, 17.4] vs unc 0.83; weak angles embedded 4/10, roleplay 2/10 | Residual risk reported, never rounded; motivates verifier wall |
| Verifier (N03) | Dose-x2 33/33; dose-div2 30/31; chemical-swap 22/25; unit-swap 29/29; clean FP 0/38 on 38 answers | SMALLN; per-type rates with no pooling; 4 misses autopsied; dosage-claim sentences only |
| SMS (N05) | Offline-ready 299/300; live-ready 100/100; 0 over-160; referral purity 16/16; guard fix 9/9 flips; dose survival 0/84 | Enforcement plus purity claimed; dose does NOT survive truncation; packer pending |
| Offline (E06) | BM25 hit 0.94; cached 0/400; service-worker precache on | Network deltas SIMULATED loss |
| Footprint (E07) | 95.64 MB unique ONNX; 284.0 MB minimal; 339.6 MB full | Measured install sizes |
| Tier mix (E10) | 7.8% zero-LLM; 0.1798 USD per 1k; saving 7.79% | Costs MODELED; T1 0.0% is 9-fact base |
| Overhead (E01) | Safety p50 0.321 ms; retrieval p50 26.831 ms; verifier p50 4.815 ms; overhead p50 33.565 ms | Live LLM latency UNMEASURED |
| Trace (E04) | Ordered 100/100; events p50 9.0 on n=100 | Measured provenance ordering |
| Envelope (N10) | Certify recall 0.7165; dangerous acceptance 0.374 | OFFLINE stub envelope, not deployment |

Supporting rows: proxy usability 94.5 on a 0-100 scale with no recruited study (E05, proxy only); out-of-distribution split with injections blocked 10/10 and off-topic refused 0/30 in the deterministic path, production LLM branch unmeasured here (N06). The residual Bangla attack rate (0.10) is kept visible because it justifies keeping the verifier wall even when the gate passes.
