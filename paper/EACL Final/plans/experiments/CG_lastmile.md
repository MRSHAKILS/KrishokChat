# Beat C+G Experiment Plan — Metering, Survival, and Honest Labels

**Status:** ladder measured; costs modeled; SMS/unmeasured items queued  
**Priority:** P0 SMS survival study (highest value-per-hour left); P0 token metering (shared with Beat B); rest is labeling  
**Principle:** small-honest beats big-modeled; every modeled number carries its disclosure.

## 1. Research questions

- **RQ-C1:** What share of real queries resolves without any LLM call, at what latency? (measured — tier mix + E01)
- **RQ-C2:** What does that save in real tokens/money? (modeled → metering upgrade pending)
- **RQ-C3:** Does the 160-char SMS preserve safety-bearing fields? (pending — P0 study)
- **RQ-C4:** Does offline delivery survive network loss? (BM25 determinism measured; loss-lane simulated)

## 2. What is already measured (keep, with labels)

| Result | Artifact | Label |
|---|---|---|
| Tier mix n=1000 (7.8% zero-LLM; p50 7.68ms) | tier_mix_20260825 | MEASURED mix; MODELED costs |
| Overhead p50 33.6ms (BM25-only, stub) | E01 | MEASURED (scoped) |
| Cached 0/400, BM25 0.94, SW precache | E06 deterministic | MEASURED |
| 284.0 / 339.6 MB | E07 | MEASURED |
| SMS 160-char enforcement + referral fallback | code (`extras.py:256`) | IMPLEMENTED, behavior unmeasured |

## 3. P0: SMS survival study (real endpoint, N ≥ 300)

1. Frozen N ≥ 300 real queries (200 safe-agri across crops + 50 ambiguous + 50 high-risk) through the REAL `POST /api/sms/advisory` endpoint (no mocks).
2. Run `POST /api/sms/advisory` per query; record `sms_text`, `char_count`, tier, confidence.
3. Checks: char_count ≤160 (must be 100%); referral-only on blocked/low-confidence (must be 100%); for safe answers, token survival of chemical/active, dose amount+unit, PHI/interval where present in the source answer; GSM-7 vs non-GSM character audit (expect Bengali → non-GSM; record, don't hide).
4. Report: enforcement rate, referral correctness, per-field survival rates with denominators, encoding audit.
5. If survival is weak → field-priority packer becomes the engineering fix; the paper then reports pre/post packer.

## 4. P0: token metering (shared with Beat B Repair 2)

Meter real tokens on the frozen 100-subset (clarification vs full generation) using actual strings. Replaces both Beat B's 88% assumption and this beat's ~600/250 averages with metered p50/p95. Until then, every cost sentence carries "modeled" + basis.

## 5. P1 (optional): Playwright network-throttle lane

Real browser/app run under throttled profiles (rural-edge/severe-2G shapes): delivery success, time-to-usable-answer, cache behavior. Upgrades the simulated +13.25/+30pp to measured retention. Optional because BM25 determinism + labeled simulation already suffice for a demo paper.

## 6. P1: UI/escalation check (code inspection, 1 hour)

Confirm the one-touch 16123 dial renders on refusal/unsafe banners (file:line pointers). If present, the S4/S5 vignettes may claim it; if not, claim "referral field + SMS fallback" only.

## 7. Status marks (for later agents)

- [x] Tier mix measured (n=1000) + modeling disclosure recorded
- [x] Offline determinism + footprint measured
- [x] SMS + helpline endpoints implemented (read)
- [x] SMS repairs identified (truncation vs guarantee; UCS-2 segments)
- [x] Unsourced $2.30/92% figure DELETED everywhere (2026-09-17)
- [ ] P0: SMS survival study (N=200 + encoding audit)
- [ ] P0: token metering (shared with Beat B)
- [ ] P1: throttle lane (optional)
- [ ] P1: 16123-dial UI check with pointers
- [ ] Results to `plans/experiments/results/`, old artifacts untouched
