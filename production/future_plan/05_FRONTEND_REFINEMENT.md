# 05 — Frontend / UX Refinement

**Parent:** `00_SCOPE_OUTLINE.md` (§7, spine step 5)
**Status:** PLANNING — no code changes.
**User reality:** low-literacy, rural, cheap phone, flaky connection, non-Dhaka dialect.

The frontend already has a mature "কৃষি পত্রক" Field-Notebook design system, 24 routes, PWA icons, Bengali-first farmer surfaces (G0–G9), and an animated agent-trace stepper. These are **refinements**, not rebuilds.

---

## 1. Scopes

| # | Scope | Farmer profit | Effort | Pairs with |
|---|---|---|---|---|
| **F1** | **WCAG 2.2 pass for low-literacy** (44–48px touch targets, `aria-live` on stream, plain-language Bengali, pause control on >3s audio) | Usable by low-literacy, older farmers | Cheap–Medium | — |
| **F2** | **PWA install + offline shell UX** (install prompt, offline banner, "reconnecting…" SSE state) | Feels like a real app; works offline | Medium | U2 (edge) |
| **F3** | **On-device diagnosis UX** (instant local result; "uploading only because unsure" transparency) | Speed + trust + visible data-saving | Medium | U1/U3 (edge) |
| **F4** | **Bengali font optimization** (`next/font` Hind Siliguri / Noto Sans Bengali; never subset to Latin) | Correct rendering, faster on 3G | Cheap | — |
| **F5** | **Personalized home** (my crops, my stage, my alerts) | The app knows me | Medium | P1/P2 |
| **F6** | **Voice-first affordances** (big mic button; audio replay per advisory — Folon does this) | Low-literacy accessibility | Medium | U5 (voice) |

---

## 2. The two UX differentiators nobody in BD ships

- **Voice in / voice out** (Bengali ASR + TTS): measurably beats text for low-literacy farmers — **87.3% vs 62.1%** decision accuracy ([FarmSaarthi](https://www.jetir.org/papers/JETIR2604936.pdf)). Bengali STT `bn-BD` exists (Google); TTS via ElevenLabs / `bn-IN`. Server-side (see `01_EDGE_OPTIMIZATION.md` §5).
- **Dialect-tolerant input** (Chittagonian / Sylheti / Noakhali) using the existing **110-word dialect map** — the #1 documented accessibility failure that nobody solves. Even 16123 human agents mostly serve Dhaka dialect.

---

## 3. Keep as the demo centerpiece

The **agent-trace UI + safety panel** (Checking safety → Retrieving → Generating → Verifying) is the transparency the Plantix literature explicitly calls for and what reads well to non-technical judges. It already exists — keep it, polish the animation, wire the safety panel to real audit counts (A2).

---

## 4. Suggested build order

1. **F4** font optimization (cheap, immediate rendering/perf win).
2. **F1** WCAG/low-literacy pass.
3. **F2 + F3** offline + on-device UX (pairs with edge U1/U2/U3).
4. **F5** personalized home (pairs with P1/P2).
5. **F6** voice affordances (pairs with U5).

## 5. Guardrails

- Locked stack: Next.js App Router + TS, Tailwind + shadcn/ui, Motion, Vercel AI SDK. No substitutions.
- Auth surfaces never force redirects/popups/degradation on anonymous visitors.
- Follow `DESIGN.md` / the existing Field-Notebook system; don't invent a new visual identity.
- Accessibility-compliant output required.
