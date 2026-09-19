# Beat C+G — Advice That Can't Arrive Is Useless; Advice That Can't Pay for Itself Dies

**Status:** research pass 1 complete; ladder + endpoints implemented; costs modeled (not metered); SMS field-survival unmeasured; two technical repairs flagged  
**Date:** 2026-09-17  
**Role in EACL story:** the deployment soul and the paper's close — reliability under money, connectivity, and literacy constraints, treated as design, not trivia.

---

## 1. The human moment

The farmer has a feature phone, not a smartphone. The village has 2G that drops every evening. Each API call costs money somebody doesn't have. The correct advice, generated brilliantly in a Dhaka lab, arrives as a loading spinner — or never arrives at all.

Meanwhile the one number that is free and always works is printed on fertilizer bags across the country: **16123**, the national Krishi Call Center. And the one channel that reaches every phone ever sold fits 160 characters.

KrishokTech treats these facts as architecture: spend nothing when a rule suffices, survive disconnection by construction, compress advice into an SMS without inventing it, and when the system cannot speak safely, hand the farmer to a human — by name and number, not by error message.

**Feel-line candidate:**

> We design for the phone the farmer has, the network the village has, and the budget nobody has.

This line is a candidate, not final paper prose.

---

## 2. What the evidence already establishes

### 2.1 Tiered resolution with measured mix

The 2026-08-25 tier-mix report (`docs/production_readiness/reports/tier_mix_20260825.md`, n=1000 farmer-benchmark queries):

| Tier | Share | LLM calls | p50 |
|---|---|---|---|
| T0 deterministic guard | 5.6% | 0 | 0.48ms |
| T1 structured fact | 0.0% | 0 | — |
| T2 templated advisory | 2.2% | 0 | 0.47ms |
| T3 grounded generation | 92.2% | 1–2 | 7.95ms (retrieval+stub; live LLM unmeasured) |
| T4 honest refusal | 0.0% | 0–1 | — |

Zero-LLM resolution: **7.8%**. Overall p50 **7.68ms** / p95 14.59ms (stub generation excluded).

### 2.2 Costs are modeled — honestly labeled as modeled

The same report states its basis outright: *"production inference adapters currently run without active token-metering hooks in batch mode; costs are modeled from benchmark token averages (~600 prompt / ~250 generation tokens for T3)."*

- Pessimistic baseline (100% T3): $0.195/1k queries.
- Measured mix (7.8% zero-LLM): **$0.1798/1k → 7.79% reduction**.
- Projected fact-base expansion (~35% zero-LLM): $0.1188/1k → ~39.1% — a **projection**, not a result.

Price basis: `gemini-2.5-flash-lite`. The honest story is small today (7.79%) and grows with the fact base. (An unsourced "$2.30 / 92%" figure was deleted everywhere 2026-09-17.)

### 2.3 Last-mile endpoints are implemented

- **SMS gateway** (`POST /api/sms/advisory`, `extras.py:256`): runs the full QA pipeline with `channel="sms"`; blocked/low-confidence → strict 16123-referral SMS; safe answers → `INSTITUTION পরামর্শ: <body> | হেল্পলাইন: ১৬১২৩` packed to ≤160 chars, `gsm_segments=1`.
- **Helpline referral** is a response field (`helpline_referral="16123"`) plus the A5/T0 banner path — a pipeline terminal state, not a footer link.
- **Offline PWA**: `sw.js` exists with precache (verified in E06: 4,901 bytes, precache true); BM25 path makes zero network calls by construction; E06 deterministic: cached 0/400 (100-key demo cache, honest miss), BM25 hit 0.94.
- **Footprint**: minimal self-contained 284.0 MB, full 339.6 MB (E07, SHA-256 deduplicated).

### 2.4 The competitive last-mile slot is open

Farmer.Chat rides WhatsApp/Telegram (needs mobile data + app). KrishokBondhu rides voice calls (needs airtime + server + VAPI). AIEP's five voice-first MVPs (GIZ/FAIR Forward, `arXiv:2601.11537`) report NPS ≥60 but leave sub-5s voice latency unsolved. A deterministic sub-160-char text channel that needs no data, no app, no call — generated from the certified answer object — has no verified competitor. Neither does a refusal path that dials a real national helpline.

---

## 3. Why cost + last-mile belong in an NLP paper

1. **Every LLM call is a failure of cheap reasoning.** If a rule, a table, or a chip-click resolves the turn, spending generation is waste *and* risk (Beat F: the generator mutates). The ladder makes "don't call the model" a first-class, metered decision.
2. **Offline is a safety property, not a feature.** When the network drops mid-season, a cloud-only advisor doesn't degrade — it disappears, exactly when pests don't wait. BM25-first + local vision + stub-degradation + KB fallback = advice under disconnection.
3. **Compression without authority loss is an unsolved interface.** Anyone can truncate to 160 chars; almost nobody can promise the dose survived the cut. SMS-from-certified-object is the claim — pending the survival study.
4. **Escalation is the honest terminal of selective answering.** A system that abstains into a void abandons the farmer (Beat B's A4 asks; A5 must hand over). 16123 closes the loop with a human who outranks the model.

---

## 4. What KrishokTech does out of necessity

```text
every turn enters the ladder:
  T0 rule match → answer in ~0.5ms, 0 tokens, badge "no AI used"
  T1/T2 fact rows → answer in ~0.5ms, 0 tokens (rare today: 9-fact base)
  T3 retrieval + generation → full pipeline + verifier (~34ms overhead + live LLM)
  T4/A3/A5 → refuse / guide-without-chemicals / dial 16123
        ↓
delivery adapts to the channel:
  app → full answer + Why-panel + trace + badges
  sms → 160-char pack of the SAME decided answer (never a fresh summary)
  offline → BM25 + local models + cached content; LLM steps degrade to KB fallback
  unsafe/unknown → 16123 referral, by SMS if that is the channel
```

One decision object, four renderings. The SMS is a rendering of the certified answer — that single invariant is the whole claim.

---

## 5. Current implementation evidence

### Implemented (real code, read 2026-09-17)

- `resolution.py` — T0–T4 taxonomy, `ZERO_LLM_TIERS`, Bengali authorship badges.
- `extras.py:256` SMS gateway — pipeline-backed, referral fallback, 160-char pack.
- `extras.py:146` helpline register endpoint; `helpline_referral="16123"` default.
- `sw.js` + PWA manifest + icons + `pwa-register.tsx`.
- Tier-mix runner + report (2026-08-25); E01 overhead breakdown; E06 offline deterministic; E07 footprint.

### Measured (keep, with labels)

- Tier mix n=1000 (above); E01 n=400 overhead p50 33.6ms; E06 cached 0/400 + BM25 0.94 + SW precache; E07 284.0/339.6 MB.
- E09 token/latency deltas feed this beat's cost argument (with Beat B's metering repair).

### Honesty repairs required

1. **Costs are modeled, not metered — say so every time.** The report itself discloses this; the paper must carry the disclosure ("modeled from ~600/250-token averages; metering hooks pending"). The metered-token study (Beat B Repair 2) upgrades this beat too.
2. **SMS field-survival is unmeasured — and the mechanism is truncation, not field-packing.** The endpoint packs `clean_answer[:available_chars]` under a fixed prefix/suffix. If the dose sits past the cut point, it is lost despite the docstring's "guarantee." Fix options: (a) field-priority packer (dose+chemical+PHI first, explanation last), or (b) keep truncation + run the survival study and report the rate. Until one lands, claim only "160-char enforcement with safe fallback," never "guaranteed dose survival."
3. **"1 GSM segment" is technically wrong for Bengali script.** Bengali Unicode travels as UCS-2 (70 chars/segment on real gateways); Python `len() ≤ 160` counts code points, not segments. Fix: reframe as "160-character compressed advisory" and disclose multi-segment reality — or add gateway-aware segment math. Never let a reviewer who has sent a Bengali SMS catch this.
4. **Network retention (+13.25/+30pp) is simulated loss, not field measurement.** Keep with the "simulated packet-loss" qualifier (Beat A decision); optional P1 Playwright throttle lane for a real number.
5. **Fact-base expansion savings (~39%) is a projection.** Label as scenario modeling; it motivates growing the 9-fact base, nothing more.
6. **Cached 0/400 is a finding, not an embarrassment.** The 100-key demo cache misses held-out queries completely — report it as the reason offline relies on BM25-first rather than answer caching.

---

## 6. Defensible novelty statement

Do **not** claim:

> Cheapest/fastest/offline-capable agricultural chatbot. / Guaranteed SMS dose survival (today).

Defensible wording:

> KrishokTech treats cost and connectivity as reliability design: a five-tier ladder resolves safety and fact turns in ~0.5ms with zero LLM calls (7.8% of 1,000 farmer queries today, measured; savings modeled at 7.79% and disclosed as modeled), every turn degrades through KB fallback when the LLM is unreachable, and the same decided answer renders as full advisory, 160-character SMS, or 16123 referral — with the SMS field-survival rate under active measurement rather than assumed.

---

## 7. Candidate paper paragraph sequence

1. **Opening:** the feature phone, the dropping 2G, the budget nobody has; the lab-perfect answer that never arrives.
2. **Failure:** cloud-only advisors disappear exactly when pests don't wait; truncation invents by omission; abstention into a void abandons.
3. **Design response:** ladder (don't call the model when a rule suffices) + one-decision-four-renderings + 16123 as terminal state.
4. **Evidence:** tier-mix table (measured mix, modeled savings, disclosed) + offline determinism + footprint + SMS enforcement (survival study pending or landed).
5. **Demo payoff + close:** reviewer flips to offline/SMS view, watches the same case compress and survive — then the paper's final line: designed for the phone, network, and budget at hand.

---

## 8. Reviewer objections to pre-empt

- "7.79% is tiny" → agree; it's the measured floor with a 9-fact base, and the projection shows the mechanism scales. Small-honest beats big-modeled.
- "Costs are modeled" → disclosed in the source report; metering study upgrades it.
- "SMS truncation can lose the dose" → agree; survival study or field-priority packer decides the final claim.
- "GSM segment math is wrong" → fixed framing before submission (see repair 3).
- "Offline numbers are simulated" → BM25 determinism is measured; loss-lane is labeled simulation; throttle lane optional.
- "WhatsApp bots already reach farmers" → they need data + app + server; ours needs neither for the SMS path, and ours degrades locally.

---

## 9. Decision after Beat C+G pass 1

**Keep C+G as the paper's deployment close (half of C3), not a standalone contribution.** It needs no new annotation and little new measurement: the ladder is measured, the endpoints are implemented, and the repairs are small (metering ⊂ Beat B; SMS study ~hours; segment reframing = prose). Its job is making the reviewer *feel* why the system matters — the final paragraph of the paper lives here.

Next: **synthesis** — kill-list, `problems_we_solved.md`, `paper_outline.md`. All seven beats are now drafted (A, B, F, D+E, C+G); nothing else needs a beat file.

---

## 10. Questions resolved by the lead (no open items)

1. Token metering: shared with Beat B, running (N02 locked offline, live sides pending).
2. SMS: survival study first (N05); packer only if survival is weak.
3. SMS framing: "160-character advisory" until segment math is verified.
4. Throttle lane: optional P1; labeled simulation suffices for the demo.
5. Wheat-mitigation dead branch: KEEP (removal risks mid-week breakage; marked legacy, affects zero numbers).
