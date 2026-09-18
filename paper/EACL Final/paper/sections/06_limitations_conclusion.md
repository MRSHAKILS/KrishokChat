# 6 Limitations and conclusion

## Limitations

1. N03 small n: 38 answers with per-type n 8-33; per-type rates with Wilson CIs, no pooling, no claim beyond dosage-claim sentences.
2. Crop-router label mismatch: family truth vs 10-species predictions with top-1 0.0259 kept as mismatch diagnostic only with species breakdown; router accuracy unclaimed on that metric.
3. Rice INT8 rejected on a 2.5pp drop past the 2.0pp gate; artifact exists but is never deployed and never cited as usable.
4. Potato/brassica INT8 sets too small (n=15/51); diagnostic-only, with quantitative INT8 accuracy claimed for wheat only.
5. Corn and chilli unmeasured for lack of local labeled photos; no claim of any kind for either model.
6. INT8 not faster here (higher latency than FP32); size story only with no speed claim.
7. N07 implicit-crop miss (farmer_q_63, counted as miss); badge scoped to explicit-text contradiction at 53/54 farmer and 400/400 PRISM, 453/454 combined.
8. N08 perfect-gold fence; simulation of perfect routing, not classifier performance, with no absent-crop generalization.
9. N09 seeded-memory conformance (clarification 0.86, overall 0.458); conformance, not independent accuracy, with follow-up UNTESTED and safety as precheck-only lower bound.
10. N11 cost unmeasured with 60-row answer review pending; halt plus latency operating point only with no coverage or quality superiority claim.
11. Single-reviewer labels for 200 crop slots plus agent autopsies; second human pass is the stated upgrade path and hazard numbers stay labeled single-reviewer.
12. Live-generation tokens recorded (n=58 grounded rows: input p50 1111, output p50 221) with money cost not computed; tokens reported and cost arithmetic uses the disclosed tier-mix basis only.
13. Dense retrieval unevaluated; all retrieval numbers are BM25-only and dense stays out of scope as fallback.
14. Live LLM latency excluded from overhead p50s; all p50 figures exclude generation unless labeled live (N11 p50 4218.6 ms).
15. N03 generation buffered pre-rule with 71 rows verified intact; per-record rule enforced in N05/N11 runners going forward.
16. SMS dose fields do not survive truncation (0/84); enforcement plus purity claimed, packer pending, field survival never claimed.
17. Off-topic refusal absent in the deterministic path (0/30); split reported with injections 10/10 blocked and production LLM branch unmeasured here.
18. Bangla-native injection residual 0.10 [5.5, 17.4] on n=100 with embedded 4/10 and roleplay 2/10 (E03 n=30 plus N12 n=70); reported as residual risk with localized weakness that motivates the downstream verifier wall.

## Conclusion

KrishokChat is designed for the phone, the network, and the budget the farmer already has. The phone holds a 284.0 MB minimal install (95.64 MB unique ONNX) with on-device models measured in-browser on a subset. The network is assumed absent. BM25 hits 0.94 from cache with precache on and deltas marked SIMULATED.

Long answers collapse to 160-character SMS or to a 16123 referral when safety requires it. The budget is explicit. Turns at zero LLM are 7.8% at a modeled 0.1798 USD per 1k. Clarification is p50 89 tokens against context p50 2146 with no blended figure.

Det halt is 0.38 (N01b) with 25/0 discordant fence movement and a 0.95% vs 36.19% safety gap, all shown with limits in-cell. Visitors leave with operating points they can rerun, not summaries they must trust.
