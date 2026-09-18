# 5 Related work

Bengali farm advisory has strong deployed systems. We credit what each established and name what each leaves unmeasured that our demo measures. We make no priority claim about language, mode, or deployment.

| System | Approach and credit | What it leaves unmeasured that we measure |
|---|---|---|
| Farmer.Chat | Conversational advisory with intent handling and retrieval over curated content; strong field deployment and follow-up dialogue | Publishes no halt rate for crop-less treatment queries, no hazard delta for halted vs retrieved paths, and no token delta for clarification vs retrieval context |
| KrishokBondhu | Crop and symptom guidance tuned for local practice with helpline linkage; valued extension reach | Reports no text-vs-photo conflict rate, no badge capture with false-halt count, and no fence delta with discordant analysis |
| Krishi Sathi (advisory variant) | Intent classification followed by retrieval and generation; broad crop coverage | Classifies then retrieves in all cases, so gating has no zero-retrieval operating point with measured halt, cost, and hazard numbers |
| Krishi Sathi (diagnosis variant) | Photo-based disease scoring that aids visual triage | Keeps diagnosis separate from advisory retrieval, so photo-as-fence with pre-bound queries and explicit-contradiction badge scope is absent |
| MyCC with AIEP | Cloud advisory with evaluation setup and post-hoc answer judging | Judges answers after rendering, while we drop unsupported dosage sentences pre-render with same-passage binding and report per-type catch with clean false-positive count plus SMS enforcement and referral purity |

Across these systems, refusal often ends the turn. Our S4 ends refusal at a dialable national helpline (16123) as terminal state and measures referral purity (16/16, N05). Offline and SMS behavior is commonly described without numbers. Our S5 reports SMS caps (0 over-160), dose survival loss (0/84), BM25 hit with cache state (0.94, 0/400), and footprint sizes, with network deltas marked SIMULATED and costs marked MODELED. Where prior art optimizes answer quality, we publish the operating limits alongside: single-reviewer labels, SMALLN verifier counts with no pooling, perfect-gold fence as upper bound, and Bangla residual risk that motivates keeping both walls.
