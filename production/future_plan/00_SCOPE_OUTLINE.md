# KrishokChat — Production & Future Scope Outline

**Status:** RESEARCH / PLANNING DOCUMENT — nothing here changes code until a task executes it.
**Date:** 2026-08-23
**Audience:** the researcher (approver) + future executing agents.
**Companion docs:** `docs/PRODUCTION_ROLLOUT_PLAN.md` (Phase 0 hardening, done), `docs/production_readiness_roadmap.md` (Tier 0/1/2), `docs/competitive-landscape.md`, `docs/business_model_implementation_plan.md`, `docs/refactor/PROJECT_HANDOFF.md`.

---

## 0. Why this document exists

The prior planning docs answered *"how do we harden and deploy the current system safely?"* (Phase 0 is done; Tier 1 tasks are drafted). They did **not** answer the question the researcher is now asking:

> *"If we deploy for real farmers and go for government funding, what should we actually build so that at least ONE thing works fully and is genuinely usable — better than iFarmer / Plantix in a practical, defensible sense — instead of 100 half-features?"*

This document is the **capability-scope map**. It catalogues every credible angle (usability, edge optimization, disease coverage, personalization, proactive advisory, admin/operator roles, frontend, and paper novelty), each with:
- **Farmer profit** (why a Bangladeshi farmer benefits),
- **Our profit** (funding / paper / moat),
- **Effort** (cheap win vs large lift),
- **Novelty** (does a competitor already do this?),
- **Evidence** (sourced from the three research passes on 2026-08-23).

It is deliberately a *menu with a recommended order*, not an implementation plan. It does **not** violate any AGENTS.md hard rule; it does **not** commit to building anything. See §10 for the recommended "one thing that works fully" spine.

---

## 1. The core strategic finding (read this first)

Three independent research passes converge on one uncomfortable, useful truth:

**The current app diagnoses leaf *diseases* and answers *reactive* questions. But the largest real losses and the worst, most dangerous pesticide misuse in Bangladesh come from (a) insect *pests* the app cannot see, and (b) problems that strike *before* a farmer thinks to ask.** Meanwhile, farmers overwhelmingly take advice from pesticide retailers who have a conflict of interest (92.5% for mango; "most" for chili/brinjal — [JAE 2025](https://www.ajol.info/index.php/jae/article/view/301277), [MIT Solve](https://solve.mit.edu/solutions/11174)).

That gap **is** the opportunity, and it happens to line up exactly with our unique asset — the **safety-aware pipeline + dosage verifier + provenance + audit trail**. Nobody in Bangladesh does conversational AI advisory with safety verification ([`docs/competitive-landscape.md`](../../docs/competitive-landscape.md)). So the winning move is not "more crops"; it is **one crop's problem solved end-to-end, correctly, safely, offline-capable, and grounded in official BD sources** — then extend.

The single most defensible spine (detailed in §10):

> **On-device disease/pest diagnosis → BD-approved dose + timing + IPM advice grounded in DAE/BARC/BRRI/BAMIS → safety verifier catches banned/overdose chemicals → 16123 redirect → weather-triggered proactive alert for the same crop.**

Everything else in this document is an extension of, or support for, that spine.

---

## 2. Practical-usability scopes (the "make it real for farmers" layer)

| # | Scope | Farmer profit | Our profit | Effort | Competitor gap? |
|---|---|---|---|---|---|
| U1 | **On-device INT8 image diagnosis** (crop + disease classifiers as `.tflite`, runs on the phone) | Works on a cheap 2–4GB phone, offline, in <150ms; only spends data when the model is *unsure* | Headline practical novelty; genuinely deployable in 2026 | Medium | **Yes** — Plantix needs internet; no BD app does on-device |
| U2 | **Offline-first PWA shell** (service worker, IndexedDB model cache, airplane-mode capable) | Usable on flaky rural 4G/3G; cached advisories + 16123 redirect work with no signal | Matches the proven BD pattern (Krishoker Janala offline, Folon modules) | Medium | Partial — govt apps offline but static, no AI |
| U3 | **Confidence-gated upload + client-side image compression** (resize→WebP, EXIF strip, only ambiguous images hit server) | Saves the farmer's data/money; faster on bad connections | Cheap bandwidth story; quantifiable demo metric ("% uploads avoided") | Cheap–Medium | **Yes** |
| U4 | **Bengali dialect-tolerant input** (Sylheti/Chittagonian/Noakhali; the existing 110-word map) | A Sylheti farmer's words are understood; 16123 agents can only serve Dhaka dialect | Documented #1 accessibility gap in BD *and* India; unmatched | Medium | **Yes** — no global player has BD dialects |
| U5 | **Voice in / voice out (Bengali ASR + TTS)** | Low-literacy farmers: voice = 87.3% vs 62.1% text decision accuracy ([FarmSaarthi](https://www.jetir.org/papers/JETIR2604936.pdf)) | "Voice + dialect + offline" are the 3 claims investors test | Large | Partial — no BD app does full voice; KissanAI/Farmer.Chat don't serve BD |
| U6 | **SMS/USSD fallback** | Reaches the ~27% of connections that are effectively 2G | Reaches the 46%-internet-gap population | Large + regulated | v2 only — needs BTRC-enrolled aggregator + short code |

**Note (edge reality check):** on-device *generative LLM* on 2–4GB phones is **hype, not deployable** in 2026 (Gemma 3 4B needs ~2.8GB peak RAM and crashes ~15% of 6GB users — [MVP Factory 2026](https://mvpfactory.io/blog/running-gemma-3-on-device-in-production-memory-budgets-quant/)). Keep generation server-side. The honest on-device wins are U1–U3 + an on-device *safety classifier* (small), not on-device chat. Full details: [`01_EDGE_OPTIMIZATION.md`](./01_EDGE_OPTIMIZATION.md).

---

## 3. Disease / crop coverage scopes (the "solve where it actually hurts" layer)

The current classifiers cover **leaf diseases only** for potato, rice, wheat, corn, brassica. The highest-value gaps are **insect pests** and **the two vegetables where farmers drown in pesticide**. Full ranked analysis + loss figures + sources: [`02_DISEASE_COVERAGE.md`](./02_DISEASE_COVERAGE.md).

| Priority | Add | Why (farmer impact) | Effort |
|---|---|---|---|
| **1** | **Maize — Fall armyworm** detection + IPM/dose | 37.7% avg loss, 35 districts, fastest-growing cereal, currently *zero* pest coverage; damage is highly visual | Medium (new classes) |
| **2** | **Potato — late-blight weather-risk forecasting** (diagnosis already exists) | 25–57% loss; largest cash crop (7.5M farmers); proven BD ROI: GEOPOTATO +USD 173–220/ha, *less* fungicide | Medium |
| **3** | **Rice — insect pests** (brown planthopper, stem borer deadheart/whitehead, rice hispa) | Rice is #1 crop; pests cause 44–62% outbreak losses; current rice model has no insects; huge IPM-resurgence upside | Medium |
| 4 | **Brinjal — shoot & fruit borer** + wilt | Up to 86% loss; worst pesticide crisis (up to 84 sprays/season) → max value from safety/dose/IPM agents | Medium |
| 5 | **Chili — anthracnose** | ~99% of chili farmers affected, near-zero disease literacy | Medium |
| 6 | **Tomato — late blight** (+ borer) | High-value; late blight *reuses* the potato *P. infestans* model + forecasting | Low marginal |
| 7 | Rice false smut / sheath rot; wheat blast forecasting; mango anthracnose; banana Panama | Complete the set / regional value | Varies |

**Cross-cutting insight:** every diagnosis must be backed by **BD-approved dose + timing + IPM**, grounded in BAMIS (which publishes exact doses + registered trade names — e.g. [BAMIS pests](https://www.bamis.gov.bd/en/pests/1/all/76/)), BRRI, BARI, and the Krishi Projukti Hatboi. This is precisely where our safety/verifier pipeline delivers differentiated value instead of just a label.

---

## 4. Personalization scopes (the "advice fits THIS farmer" layer)

Strongest causal evidence: PxD's Odisha RCT (13,675 farmers) — personalization to weather/agro-conditions produced up to **9.4% more yield** and **21% less severe crop loss**, ROI **$12–19 per $1** ([PxD Odisha](https://precisiondev.org/wp-content/uploads/2025/02/Odisha_RCT_02052025.pdf)). Full analysis: [`03_PERSONALIZATION_PROACTIVE.md`](./03_PERSONALIZATION_PROACTIVE.md).

| # | Scope | Farmer profit | Effort | Evidence |
|---|---|---|---|---|
| P1 | **Farm profile** (crop, upazila/AEZ, plot size, sowing date, soil) at registration | The minimal set that drives *all* downstream personalization | Cheap | PxD collects exactly this |
| P2 | **Crop-calendar / growth-stage-aware advice** (advice keyed to sowing date + current stage) | Right advice at the right week; matches PxD's stage-keyed design; ACI Fosholi saw 9–16% rice gains | Cheap–Medium | BAMIS crop/pest/disease-weather calendars are pre-built |
| P3 | **History-aware follow-ups** (the assistant remembers this farmer's last problems) | Continuity; no re-explaining | Medium | DG names this as next-gen; sessions adapter (T0-03) already exists |
| P4 | **Personalized reminders** (spray/fertilizer/irrigation windows) | Addresses inattention, not knowledge; evidence is *mixed* (Uganda null) | Large (scheduling infra) | Time precisely (24h-ahead beat 1h-ahead — PxD) |

**Must respect AGENTS.md hard rule 1:** anonymous/DEMO_MODE users keep working exactly as today. Profile is additive, tied to the (already-approved, non-gating) Supabase auth lane.

---

## 5. Proactive / push advisory scopes (the "catch it before the farmer asks" layer)

A pull chatbot only helps a farmer who *already knows* they have a problem. The differentiated value is proactive. The BD flagship precedent is the **Wheat Blast Early Warning System** (CIMMYT + BWMRI + BMD + DAE) — weather-model spore-risk → growth-stage-tailored fungicide advisory (+ PPE + "consult DAE") to 14,500+ officers ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12350828/)). Full analysis: [`03_PERSONALIZATION_PROACTIVE.md`](./03_PERSONALIZATION_PROACTIVE.md).

| # | Scope | Farmer profit | Effort | Competitor gap? |
|---|---|---|---|---|
| PR1 | **Weather-triggered disease-risk alert for ONE crop** (potato late blight first, then wheat blast, FAW) | Preventive spray *only when needed* → higher yield + less fungicide (GEOPOTATO proof) | Medium | **Yes** — Plantix's promised outbreak prediction is still *aspirational, not shipped* |
| PR2 | **Predictive region-arrival pest alerts** (Agrio-style) | "The pest is coming to your area next week" | Large | **Yes** globally rare |

**Data sources (all snapshot-able, so no live-scraping rule violation):** BMD WRF gridded forecasts + Agromet bulletins, BAMIS 64-district advisories with pre-built pest/disease-weather calendars, satellite (MODIS/Sentinel-1, as ACI IDSS used).

---

## 6. Admin / operator / extension-officer scopes (the "credible for govt/B2B" layer)

Bangladesh's own SAAO infrastructure is the anchor: DAE's **QIS platform** has onboarded 8,000+ SAAOs (target 14,000); its "Farmers' Prescription" gives personalized dose/mineral/timing advice via audio/video ([TechnoVista QIS](https://technovista.com.bd/quality-information-system/)). This is both the credible *integration target* and the pattern to emulate. Partial infra already exists (admin console G0–G9, broadcast notifications, audit panel). Full analysis: [`04_ADMIN_OPERATOR_ROLES.md`](./04_ADMIN_OPERATOR_ROLES.md).

| # | Scope | Our profit | Effort | Status |
|---|---|---|---|---|
| A1 | **Verifier-flagged-answer human-review queue** | Operator credibility; matches DG's real-time feedback loops; drafted as T1-05 | Cheap–Medium | Design drafted (`T1-05_safety_depth.md`) |
| A2 | **Safety-metrics audit panel** (per-category classification breakdown) | The poster/demo trust story; powers "meaningful use" impact narratives | Done (exists) | Live in `/admin` |
| A3 | **Broadcast agro-advisory / outbreak alerts** (admin → farmers) | B2G credibility; mirrors BAMIS 64-district broadcast + Wheat Blast EWS | Partial | Broadcast notifications shipped (G0–G9) |
| A4 | **Extension-officer (SAAO) dashboard** (monitor, dispatch, escalate to 16123) | The credible B2B/marketplace path (intermediaries pay, farmers don't) | Large | Overlaps QIS; frame as roadmap |
| A5 | **Feedback loop** (farmers/officers flag wrong answers → retraining signal) | Closes the loop; DG proves this drives adoption | Medium | — |
| A6 | **Usage analytics** (query volume, refusal rate, retrieval hit rate) | Impact evidence for funders | Partial | Telemetry (T0-05) exists |

**Monetization reality (from competitive research):** farmers *do not pay* for advisory (PxD, mKisan 30% churn on price). Durable revenue = **freemium + B2B (agro-dealers/SAAOs/NGOs) + B2G (DAE/16123) + dataset/API licensing**. The safety/audit engine is the least-commoditized asset to sell. See `docs/business_model_implementation_plan.md`.

---

## 7. Frontend / UX refinement scopes

The frontend already has a mature "কৃষি পত্রক" Field-Notebook design system, 24 routes, PWA icons, Bengali-first farmer surfaces (G0–G9), and an animated agent-trace stepper. Refinement opportunities: [`05_FRONTEND_REFINEMENT.md`](./05_FRONTEND_REFINEMENT.md).

| # | Scope | Farmer profit | Effort |
|---|---|---|---|
| F1 | **WCAG 2.2 pass for low-literacy** (44–48px touch targets, `aria-live` on stream, plain-language Bengali, pause >3s audio) | Usable by low-literacy, older farmers | Cheap–Medium |
| F2 | **PWA install + offline shell UX** (install prompt, offline banner, "reconnecting…" SSE state) | Feels like a real app; works offline | Medium (pairs with U2) |
| F3 | **On-device diagnosis UX** (instant local result, "uploading only because unsure" transparency) | Speed + trust + data-saving visible | Medium (pairs with U1/U3) |
| F4 | **Bengali font optimization** (`next/font` Hind Siliguri / Noto Sans Bengali, never subset to Latin) | Correct rendering, faster load on 3G | Cheap |
| F5 | **Personalized home** (my crops, my stage, my alerts) | The app knows me | Medium (pairs with P1/P2) |
| F6 | **Voice-first UI affordances** (big mic button, audio replay per advisory — Folon does this) | Low-literacy accessibility | Medium (pairs with U5) |

---

## 8. Paper-novelty scopes (the "get accepted / get funded" layer)

Frame novelty as the **combination** (safety-verifier + DAE-grounded dosage + provenance + dialect + edge), not any single well-trodden component (do **not** claim "first Bengali agri RAG" — KrishokBondhu etc. exist). Each claim is testable. Full framing + evaluation designs: [`06_PAPER_NOVELTY.md`](./06_PAPER_NOVELTY.md).

| # | Defensible claim | Evaluation to substantiate it |
|---|---|---|
| N1 | **First Bengali agri assistant with a chemical-dosage safety verifier grounded in DAE/PPW registered-pesticide data** (+ HHP/banned flags) | Held-out dosage/chemical query set; verifier precision/recall on out-of-range doses + banned mentions; contradiction rate vs baseline |
| N2 | **First to structurally guarantee citation provenance** (deterministic injection, not LLM-generated citations) | Citation-hallucination rate = 0 by construction; every claim's entity in cited passage |
| N3 | **First to pair a genuine BD dialect map with on-device edge diagnosis** | Retrieval/answer accuracy: dialect-rewritten vs Standard Bengali (report the register gap); on-device vs cloud latency/accuracy |
| N4 | **First Bengali agri pipeline with a safety/router gating retrieval BEFORE generation + local audit trail** | Classification accuracy on safety categories; over-refusal (144 tests) vs harm-catch trade-off; per-category audit breakdown |
| N5 | **First to counter documented pro-chemical bias** by grounding in DAE + surfacing IPM/non-chemical alternatives | Fraction of pesticide-query responses that surface a non-chemical/IPM option + correctly redirect banned chemicals to 16123 |

**Why these are safe:** the literature explicitly confirms these gaps are unfilled — general agri-LLMs produce "incorrect pesticide dosages" with no framework combining atomic decomposition + expert verification + safety-critical contradiction detection; independent audits show proprietary agri-AI (incl. KissanAI) has systematic pro-chemical bias ([Wyckhuys et al., WUR](https://edepot.wur.nl/721621)); Plantix *rejected* adding weather/planting-date checks and pivoted to selling pesticides ([WIRED](https://www.wired.com/story/plantix-pesticides-venture-capital-app/)).

---

## 9. What NOT to build (scope discipline)

- ❌ On-device generative Bengali LLM on 2–4GB phones (hype for this hardware — keep generation server-side).
- ❌ Self-built SMS/USSD in the prototype (regulated; needs BTRC aggregator + short code — v2 partnership).
- ❌ Object-detection claims from the current `task: classify` artifacts (AGENTS.md artifact-reality rule).
- ❌ Payment/checkout, multi-tenancy, per-tenant isolation, paywalls, live index building (AGENTS.md hard rules).
- ❌ Spreading across 10 crops shallowly. Depth on one spine beats breadth (the whole point of this document).
- ❌ Invented TAM/SAM/SOM, revenue projections, or unverified metrics (AGENTS.md §2.5).
- ❌ Claiming "first Bengali agri RAG / first fine-tuned Bengali agri model" (prior art exists).

---

## 10. Recommended spine — "the ONE thing that works fully"

If the researcher wants a single, coherent, end-to-end capability to nail first — usable by farmers *and* the paper's centerpiece — build this vertical slice for **potato late blight** (largest cash crop, proven BD ROI precedent, diagnosis already exists), then clone the pattern to maize FAW and rice pests:

```
[On-device] Farmer photographs potato leaf
     → INT8 .tflite classifier runs on the phone (offline, <150ms)      [U1]
     → confident? show diagnosis locally; unsure? upload compressed img  [U3]
     ▼
[Server] Grounded advisory: BD-approved fungicide + exact dose + timing
     from DAE/BARC/BAMIS corpus                                          [§3 grounding]
     ▼
[Safety] Verifier checks dose against PPW registered list; flags
     banned/HHP/overdose; redirects to Krishi Call Center 16123          [N1, N5]
     ▼
[Proactive] Weather-triggered late-blight risk alert (BMD/BAMIS snapshot)
     pushed to farmers in high-risk upazilas, stage-aware                [PR1]
     ▼
[Trust] Every decision logged to the audit trail; safety-metrics panel;
     verifier-flagged answers go to a human-review queue                 [A1, A2]
```

**Why this spine wins:**
- **Farmer profit:** correct dose + timing + preventive alert on a crop that loses 25–57% to one disease → real money saved, less wasted fungicide, works on a cheap phone offline.
- **Our profit:** it demonstrates N1+N2+N4+N5 (four of five novelty claims) in one flow, matches a proven BD ROI model (GEOPOTATO), and is the exact "safety + verification + provenance" story no competitor has.
- **Effort:** mostly *composition* of pieces that already exist (classifier, corpus, safety pipeline, audit, admin/broadcast) + two genuinely new pieces (on-device export U1, weather-risk rule PR1).

**Suggested build order (each a bounded, additive, reversible task per the roadmap's rules):**
1. On-device INT8 export of the existing potato + crop classifiers (U1) — validate accuracy within ~1.5%.
2. Ground the potato advisory in BD-approved dose/timing/IPM (§3) + wire the dosage verifier to the PPW/HHP list (N1).
3. Weather-triggered late-blight risk alert from a BMD/BAMIS snapshot (PR1) + broadcast via the existing admin lane (A3).
4. Farm profile (P1) + stage-aware advice (P2) so the alert targets the right farmers.
5. Confidence-gated upload + offline PWA shell (U2/U3) + frontend UX (F2/F3).
6. Extend the identical pattern to **maize FAW** and **rice insect pests** (§3 priorities 1 & 3).

---

## 11. Detail documents in this folder

| File | Contents |
|---|---|
| `00_SCOPE_OUTLINE.md` | This file — the master menu + recommended spine |
| `01_EDGE_OPTIMIZATION.md` | On-device inference, quantization, PWA, hybrid LLM reality, bandwidth, roadmap |
| `02_DISEASE_COVERAGE.md` | BD crop/disease/pest priorities, loss figures, coverage gaps, grounding sources |
| `03_PERSONALIZATION_PROACTIVE.md` | Farm profile, stage-aware advice, reminders, weather-triggered + predictive alerts |
| `04_ADMIN_OPERATOR_ROLES.md` | Review queue, dashboards, broadcast, escalation, feedback, monetization reality |
| `05_FRONTEND_REFINEMENT.md` | WCAG/low-literacy, PWA UX, voice affordances, personalized home |
| `06_PAPER_NOVELTY.md` | Five defensible claims + evaluation designs + what to avoid claiming |

**Next action for the researcher:** confirm the §10 spine (or pick a different crop/spine), then we open the first bounded task. Nothing here has changed any code.
