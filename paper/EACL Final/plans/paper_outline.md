# Paper Outline — 6 pages + refs/appendix (EACL System Demonstrations)

**Budgets:** ≤6 pages body · unlimited refs/appendix · live URL + ≤2:30 screencast required (desk-reject gate).

## Page plan

| Pages | Section | Content source |
|---|---|---|
| 0.8 | Abstract + Introduction | problems_we_solved C1–C3 + hook numbers (38% halt, 0.95% vs 36.19%, 25/0 fence) |
| 1.0 | System: pipeline + tiers + badges | resolution.py T0–T4, TIER_LABELS_BN, verifier, router, vision pipeline |
| 1.2 | Demo scenarios S1–S5 | N01b halt chips, N04 photo→card, N07 badge, E03 refuse+16123, N05 SMS/offline |
| 1.6 | Evaluation | Tab.2 = ground_truth.yaml key rows (E09-pilot labeled pilot; N01b, E03+CIs, N03+CIs, N08, N07, N04 scoped, E01/E06/E07/E10) |
| 0.6 | Related work | 4-row matrix (Farmer.Chat / KrishokBondhu / Krishi Sathi / CoPilot) + first-X disclaimers |
| 0.4 | Limitations | LIMITATIONS.md (18 rows, copy, don't soften) |
| 0.2 | Conclusion | One-para close: phone/network/budget design |
| Refs | ~20 entries | companions (2606/2608), closest systems, eval methods |
| Appx | Flowcharts, hash table (artifact_hashes.md), artifact index | Already existing |

## Figure/table slots (5 total)
1. Fig.1 — 5-stage pipeline (safety → extract/gate → scoped retrieval → verify → 4 renderings)
2. Fig.2 — two screenshots (workspace + Why/trace panel)
3. Tab.1 — capabilities × evidence status (the honesty table)
4. Tab.2 — compact results (ground truth key rows only)
5. Appendix figs — slot + multimodal flowcharts (exist)

## Screencast (150 s)
0:00–0:10 hook · 0:10–0:40 S1 halt→chips→resume · 0:40–1:05 S2 photo fence → card · 1:05–1:25 S3 badge · 1:25–1:45 S4 refuse + 16123 · 1:45–2:10 S5 SMS/offline · 2:10–2:25 trace/Why + badges · 2:25–2:30 URL. One continuous capture, Bengali UI.

## Desk-reject gate (all must be true at submit)
Live URL serves S1–S5 · video ≤2:30 linked · PDF ≤6 pages, clean checkout build, `acl.sty` present · license stated · zero kill-list claims · every number labeled measured/modeled/simulated/pending-with-fallback.
