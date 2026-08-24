# 04 — Admin / Operator / Extension-Officer Roles

**Parent:** `00_SCOPE_OUTLINE.md` (§6, spine step "Trust")
**Status:** PLANNING — no code changes.
**Purpose:** make the system credible for government / B2B — the funding pitch.

---

## 1. The anchor: Bangladesh's own SAAO infrastructure

DAE's **QIS platform** has onboarded 8,000+ Sub-Assistant Agriculture Officers (target 14,000); its "Farmers' Prescription" gives personalized dose/mineral/timing advice via audio/video ([TechnoVista QIS](https://technovista.com.bd/quality-information-system/)). This is both the credible **integration target** and the pattern to emulate — not compete blindly against.

Partial infra already exists in KrishokChat: admin console (G0–G9), broadcast notifications, audit panel, telemetry (T0-05).

---

## 2. Scopes

| # | Scope | Our profit | Effort | Status |
|---|---|---|---|---|
| **A1** | **Verifier-flagged-answer human-review queue** | Operator credibility; matches DG real-time feedback loops | Cheap–Medium | Design drafted as **T1-05** |
| **A2** | **Safety-metrics audit panel** (per-category classification breakdown) | The poster/demo trust story; powers "meaningful use" impact narrative | **Done** | Live in `/admin` |
| **A3** | **Broadcast agro-advisory / outbreak alerts** (admin → farmers) | B2G credibility; mirrors BAMIS 64-district broadcast + Wheat Blast EWS | Partial | Broadcast notifications shipped (G0–G9); extend to weather-triggered (PR1) |
| **A4** | **Extension-officer (SAAO) dashboard** (monitor, dispatch, escalate to 16123) | Credible B2B/marketplace path (intermediaries pay, farmers don't) | Large | Overlaps QIS — frame as roadmap/partnership, not a 7-day build |
| A5 | **Feedback loop** (farmers/officers flag wrong answers → retraining signal) | Closes the loop; drives adoption | Medium | — |
| A6 | **Usage analytics** (query volume, refusal rate, retrieval hit rate) | Impact evidence for funders | Partial | Telemetry (T0-05) exists |

---

## 3. Monetization reality (why admin/operator matters for revenue)

From competitive research: **farmers do not pay** for advisory (PxD; mKisan saw 30% churn on price). Durable revenue lanes:

- **Freemium** (advisory free; premium features for power users — no default gating).
- **B2B** — agro-dealers, SAAOs, NGOs pay for the tooling.
- **B2G** — DAE / 16123 integration.
- **Dataset / API licensing** — the safety + audit engine is the least-commoditized asset.

The admin/operator layer is what makes the B2B and B2G lanes real. See `docs/business_model_implementation_plan.md`.

---

## 4. Suggested build order

1. **A1 review queue** (T1-05) — cheap, high credibility (spine "Trust" step).
2. Extend **A3 broadcast** to weather-triggered late-blight alerts (pairs with PR1).
3. **A5 feedback loop** on flagged answers.
4. (Roadmap) **A4 SAAO dashboard** — frame as DAE/QIS partnership, not a prototype build.

## 5. Guardrails

- Admin APIs verify `profiles.role='admin'` **server-side, fail-closed**, every request (per AGENTS.md amendment 02).
- No role-based multi-tenancy, no per-tenant isolation, no paywalls.
- Audit log stays **local only** — never to an external service.
- Anonymous / demo path unaffected.
