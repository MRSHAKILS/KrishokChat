# Business Model — Frontend Implementation Plan

## Context

The IC judging criteria weight **Business Model / Economics (20)** and **Market Readiness (20)**. The poster carries a three-lane framework (freemium+B2B, B2G 16123 partnership, dataset+API licensing), drawn from `docs/competitive-landscape.md` §c. The website currently has **no business/pricing/monetization page** — the only existing business concept is a future "premium lane" (saved history gated behind Supabase auth). This plan implements a top-notch, production-grade business model surface on the website using the existing "কৃষি পত্রক" Field-Notebook design system.

## Source of truth (no fabrication)

Every claim must trace to `docs/competitive-landscape.md` §c or `RESEARCH_STATS` in `frontend/src/lib/constants.ts`:

| Lane | Who pays | Value | Evidence (cited) | Moat |
|---|---|---|---|---|
| 1. Freemium + B2B | Farmers free; agro-dealers, SAAOs, extension officers pay | Free advisory + diagnosis; paid audit/analytics dashboard | PxD 7.8M users; ACI IDSS/Fosholi €3.5M 2025 target | The audit engine is the least-commoditized trust asset |
| 2. B2G Government Partnership | DAE / a2i via 16123 Krishi Call Center | AI front-end to 16123 (triage + escalation, not competition) | 16123 received 92,094 calls FY2025-26 | The safety/audit layer is unique globally — no Plantix/Farmer.Chat/KissanAI equivalent |
| 3. Dataset + API Licensing | Third-party researchers, agri-fintech, NGOs | 85,979 benchmark + 722-image soil dataset (CC-BY-4.0); advisory API | Published CC-BY-4.0; two papers under review | The only provenance-traced Bengali agri benchmark |

**Hard constraint (AGENTS.md §2.5):** no invented TAM/SAM/SOM or revenue projections. Qualitative lanes with comparator evidence only.

## What we build

### 1. New route: `/business` (Bengali: "ব্যবসায়িক মডেল")

**File:** `frontend/src/app/(marketing)/business/page.tsx` — a full, dedicated business-model page in the `(marketing)` route group (same `max-w-6xl px-5` container).

**Sections (top → bottom):**

1. **Hero** — eyebrow + H1 "কীভাবে টেকসই হবে কৃষক চ্যাট?" + one-paragraph framing: research prototype → path to sustainability. Anchor stat: "৪.৭ কোটি কৃষক পরিবার · ১৬১২৩ = ৯২,০৯৪ কল/বছর" (the market).
2. **Three Revenue Lanes** — interactive tabbed explorer (mirrors the existing `CapabilityHub` pattern on the landing page). Tab list (3 lanes) + `AnimatePresence` panel swap. Each lane panel shows: who pays, value proposition, evidence chip, moat callout.
3. **The Moat** — a visual: the audit/safety engine at the center, with three revenue streams radiating out. SVG or CSS-built radial diagram. One-line caption: "The safety/audit engine is the least-commoditized asset — simultaneously the demo centerpiece, the trust story, and the monetization moat."
4. **Value Flow** — a horizontal flow diagram: Farmers (free) → [Audit Engine core] → three revenue streams (B2B / B2G / API). SVG with animated draw-in on scroll.
5. **Market Readiness** — two-column: "এখনই প্রস্তুত" (ready now) / "পরবর্তী পদক্ষেপ" (next steps). Checkmarks for ready items, roadmap items for next.
6. **Roadmap** — 5 ongoing items (TTS, dialect coverage, soil-model refinement, B2B pilot, full business evaluation).
7. **CTA** — "অংশীদারিত্বে আগ্রহী?" → `/contact`.

### 2. Landing page teaser section

**File:** `frontend/src/components/landing/business-model-section.tsx` — a compact 3-card teaser inserted into `frontend/src/app/(marketing)/page.tsx` **after `InstitutionalTrustSection` and before `AgriFAQSection`**. Each card = one lane (name, who pays, one-line value, evidence). CTA button → `/business`. Uses the same `stagger`/`enter` motion vocabulary as the rest of the landing page.

### 3. Navigation updates

- **Navbar** (`frontend/src/components/navbar.tsx`): add `{ href: "/business", label: "ব্যবসায়িক মডেল", desc: "টেকসই আয় ও অংশীদারিত্ব" }` to the `MORE` array.
- **Footer** (`frontend/src/components/layout/footer.tsx`): add `/business` to the "প্রতিষ্ঠান" section (or a new "আয়" section).

## Design system adherence (no deviations)

- **Colors:** `bg-paper`, `bg-paper-2`, `bg-bone`, `text-ink`, `text-ink-soft`, `text-ink-faint`, `text-leaf`, `text-ochre`, `text-clay`, `border-rule`. No blue, no gradients, no dark backgrounds.
- **Typography:** `font-display` (Tiro Bangla/serif) for headings, `font-body` (Noto Sans Bengali) for body. `.tabular` for numbers.
- **Radii:** mixed (4/8/12/18px) — `rounded-lg`, `rounded-xl`, `rounded-2xl`, `rounded-[24px]` for heroes.
- **Motion:** `stagger` wrapper + `enter` per block (not fade-up-everything). `AnimatePresence` for tab swaps. `ease.smooth`, `dur.normal`. `MotionConfig reducedMotion="user"` not needed (page-level).
- **Hover/press:** `.surface-lift` on cards, `.control-press` on buttons/links.
- **Components:** compose directly with Tailwind utilities + custom CSS vars (the existing marketing sections bypass shadcn primitives). Use `lucide-react` icons (Building2, ShieldCheck, Database, Landmark, Users, ArrowRight, Check, etc.).

## UX/interaction principles (production-grade)

1. **Tab swap with `AnimatePresence`** — the three lanes use the CapabilityHub pattern: tab list on top, panel below, `mode="wait"` exit/enter. Smooth, no flicker.
2. **Scroll-triggered reveals** — every section wrapped in `<motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger}>`.
3. **Hover lift** — `.surface-lift` on every card; leaf-tinted border on hover.
4. **Active press** — `.control-press` on every button/link (scale 0.975, 160ms).
5. **Focus-visible** — 2px leaf outline (already global).
6. **Responsive** — mobile: single-column stacked; desktop: grid layouts. Test at 375px and 1280px.
7. **Reduced motion** — the global `@media (prefers-reduced-motion: reduce)` collapses all transitions.
8. **No decorative animation** — every motion element carries information (a reveal, a state change, a tab swap).

## Files to create/modify

| Action | File |
|---|---|
| Create | `frontend/src/app/(marketing)/business/page.tsx` |
| Create | `frontend/src/components/landing/business-model-section.tsx` |
| Modify | `frontend/src/app/(marketing)/page.tsx` (insert `<BusinessModelSection />` after `<InstitutionalTrustSection />`) |
| Modify | `frontend/src/components/navbar.tsx` (add to `MORE` array) |
| Modify | `frontend/src/components/layout/footer.tsx` (add link) |

## Verification

- `cd frontend && pnpm build` passes with no errors.
- `/business` renders, the three tabs swap, the moat/value-flow diagrams render.
- The landing page teaser appears after the institutional section.
- Navbar dropdown shows the new item; footer shows the link.
- Mobile responsive at 375px; desktop at 1280px.
- `prefers-reduced-motion` collapses animations.

## What we explicitly do NOT build

- No payment system, no checkout, no Stripe integration (forbidden by AGENTS.md hard rule 1 at demo phase).
- No multi-tenancy, no admin panel, no role-based access.
- No invented revenue projections or TAM/SAM/SOM.
- No "Most Popular" pricing-tier card pattern (this is a research capstone, not a SaaS landing).
- No dark-mode business page (the Field-Notebook system is warm paper throughout).