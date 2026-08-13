# /data Page — Full UI Review & Redesign Proposal

**Scope:** `frontend/src/app/(marketing)/data/page.tsx` (351 lines) + `frontend/public/assets/knowledge_graph_gpt.jpg`
**Status:** ✅ **IMPLEMENTED 2026-08-13** (all phases P1–P5). This document remains as the design record.
**Date:** 2026-08-13

---

## 1. Executive summary

The page's **content is real** (node counts sum to 2,882 = `RESEARCH_STATS.knowledgeNodes`, provenance, sample node, CC-BY-4.0) but its **presentation is generic**: icon-tile stat cards, a decorative AI-generated JPG presented as "the knowledge graph", hand-rolled bars with a hardcoded denominator, a click interaction that reveals a filler sentence, and a 12-row key/value dump. It reads like a template, which is exactly the impression we cannot afford on the demo.

**What it should be:** the research credibility page — every number a real chart, every interaction showing real data, images sized properly and zoomable, grid systems with visible calculation (indexed sections, aligned baselines, grouped tables).

**Assets already available (zero new dependencies needed):**
- `recharts@3.10.1` installed and already used on the landing page (`page.tsx` lines 276–308: PieChart + Tooltip, vertical BarChart + Tooltip) — same patterns apply here.
- `motion` stagger/enter vocabulary in `src/lib/motion.ts` (already imported).
- `RESEARCH_STATS` in `src/lib/constants.ts` — single source for 13 of the page's numbers.

---

## 2. Section-by-section audit

### B. Dataset stats (lines 80–106) — 8 icon-tile stat cards
**Findings (P1):**
- 3 of 8 values are hardcoded in the page (`১,০২২`, `৯১৫`, `৭০৪`) instead of constants — inconsistent sourcing.
- Icon + number + tiny label is the most generic pattern on the web; zero information about *relationships* (e.g., image-linked 1,022 = 35.5% of 2,882).
- `gap-px bg-bone` "hairline" grid is fine, but cells have no hierarchy; all 8 compete equally.

**Proposal:**
- Keep the hairline grid (professional, already good) but upgrade cells: **value + sparkline** for the 6 time/ratio-able stats, and **ratio sub-labels** (e.g., "৩৫.৫% of নোড").
- Add a **count-up animation** on view (rAF hook, ~40 lines, no deps) — numbers tween from 0 with `dur.slow` easing; respects `prefers-reduced-motion`.
- Move the 3 hardcoded values into `RESEARCH_STATS` (imageLinkedNodes `"১,০২২"`, uniqueCrops `"৯১৫"`, diseaseVariants `"৭০৪"`).

### C. Knowledge graph (lines 108–176) — the weakest section
**Findings (P0 — this is the "generic bullshit"):**
- `knowledge_graph_gpt.jpg` (1368×768, 94 KB, AI-generated) is rendered `w-full object-cover` with **no aspect-ratio constraint and no zoom**. On a 1152 px container it's a flat decorative banner; the alt text claims it's the graph itself. It is not — it's an illustration.
- Category bars: denominator hardcoded to `695` (the Variety count), so every bar is relative to the wrong maximum; no value labels; label column fixed at `w-32` (long names wrap/truncate on mobile).
- Clicking a category expands a **generic sentence** ("এই ক্যাটাগরিতে সম্পর্কিত জ্ঞান নোড রয়েছে") — no real data, reads as a placeholder.

**Proposal:**
1. **Replace the JPG with a real rendered graph.** Draw the 13-category taxonomy as an **SVG radial/layered diagram** using real counts: center node (২,৮৮২ নোড) → 6 category clusters (695/570/430/380/280/527) with proportional arc lengths. Animated: arcs sweep in with `flowDraw`-style stroke draw (pattern already in `lib/motion.ts`), stagger 0.07. Pure SVG + motion — no deps. Honest: it's a *schematic* of the taxonomy, labeled as such ("স্কিম্যাটিক — ২,৮৮২ নোড, ৬ ক্লাস্টার").
   - Keep the JPG available behind a toggle (or drop it) — see guardrails §6.
2. **Proper view size for any kept image:** fixed `aspect-[16/10]` frame, `object-contain` on `bg-bone`, `max-h-[480px]`, **click → lightbox modal** (motion overlay, same pattern as the command palette) with 1:1 rendering and a caption bar.
3. **Category breakdown → recharts vertical BarChart** (mirrors the landing-page pattern): real y-axis (0–695), value labels, `Cell` colors from the palette, tooltip with count + share %, animated via `isAnimationActive` + motion wrapper. Remove the hardcoded 695 denominator.
4. **Click behavior → real data:** clicking a category shows count, share %, and — for categories that have a real example (the disease category's sample node already exists in-page) — a link to it. No filler sentences.

### D. Sample knowledge node (lines 178–279)
**Findings (P2):** Content is strong. Presentation gaps: no provenance *path* visualization (doc → page → node), entity chips and chemical chips are plain, no visual link to the graph above.

**Proposal:**
- Add a **provenance strip** under the header: `DAE → Potato Disease Manuals → p. 852 → নোড` rendered as connected steps (motion `flowDraw` on reveal).
- Entity chips: give disease/pest/chemical chips distinct token colors (leaf/clay/ochre) — already partially there; formalize.
- Add a `৩ টি এনটিটি · ২ রাসায়নিক ট্রেস` micro-summary in the collapsed header row so the closed accordion still communicates value.

### E. Dataset access (lines 281–314)
**Findings (P2):** `sm:grid-cols-2` with **one card** — an awkward half-width orphan. License note is a floating line of text.

**Proposal:**
- Two full cards: Hugging Face + GitHub (link exists in `LINKS`), then the license as a proper full-width row with a small "CC" mark tile. Grid stays `sm:grid-cols-2` but with 2 real children.

### F. Data card summary (lines 316–348)
**Findings (P1):** 12 rows of key/value in a div grid; 6 values hardcoded in-page (`১,০২২ (৩৫.৫%)`, `৯১৫`, `৭০৪`, `১,০০০`, `৯০০`, `০.৭৮`); numbers left-aligned next to labels (weak alignment); no grouping.

**Proposal:**
- Convert to a **semantic `<table>`** with three grouped sections: **কর্পাস** (PDF/প্রতিষ্ঠান/নোড/ইমেজ-লিঙ্কড/এনটিটি/ট্রিপল), **বেঞ্চমার্ক** (কোয়েরি মোট/মূল্যায়নযোগ্য), **গুণমান** (κ values with progress bars — κ 0.72 → 72% bar, κ 0.78 → 78% bar, real visual calculation).
- Right-align all numbers (`tabular-nums`), left-align labels, `border-bone` row rules — a real table, not a div list.
- Sourcing: 1,000 exists as `RESEARCH_STATS.farmerQueries`; the rest must be confirmed by the researcher or explicitly marked `TODO` (honesty rule §6).

### G. Global — professional calculative grid
- **Indexed sections:** `০১ উপাত্ত পরিসংখ্যান`, `০২ জ্ঞান গ্রাফ`, `০৩ নমুনা নোড`, `০৪ অ্যাক্সেস`, `০৫ ডেটা কার্ড` — kicker line above each `h2` (`text-ochre` mono, matches library masthead system). Gives the page a calculable structure on the poster.
- **Grid spec:** sections on a 12-col mental grid — stat cards 3-col span (4-up), charts full-width with `max-w-3xl` centering, tables 2-col; consistent `space-y-8` rhythm (already applied).
- **Sticky section index** on `lg` (left rail, 3 items, active-state highlight) — optional P2.
- **Animation spec:** one motion vocabulary — section headers `enter`, charts `stagger` + draw/count-up, all `whileInView` `{ once: true, margin: "-80px" }`, all inside the reduced-motion contract (`MotionConfig reducedMotion="user"` on the page root, matching /library).

---

## 3. Verification plan (every phase)

1. `pnpm build` — TypeScript + 18/18 static pages.
2. Route smoke: `/data` 200; siblings untouched (200).
3. Bundle check: chart markers (`recharts` already present globally; new: `count-up` hook code, lightbox markers) — client chunk contains them; no new route-level 500s.
4. Backends untouched: `:8000` 404-on-root (alive), `:11435` 415 (alive). No restarts.
5. Manual: reduced-motion ON → charts static but visible; OFF → animations play.

---

## 4. Phased implementation roadmap

| Phase | Scope | Files | Deps | Risk |
|---|---|---|---|---|
| **P1** | Stat cards: count-up hook, sparklines (recharts `AreaChart` or inline SVG), 3 values → `RESEARCH_STATS` | `data/page.tsx`, `lib/constants.ts`, new `lib/use-count-up.ts` | none (recharts present) | Low |
| **P2** | KG section: real SVG radial graph + proper image frame (`aspect-[16/10]`, `object-contain`) + lightbox; recharts BarChart for categories with real y-axis + labels + real click data | `data/page.tsx` | none | Low–Med |
| **P3** | Sample node provenance strip + micro-summary; access section 2-card fix + license row | `data/page.tsx` | none | Low |
| **P4** | Data card → semantic table + grouped sections + κ progress bars; section indexing (০১–০৫) + sticky rail (optional) | `data/page.tsx` | none | Low |
| **P5** | Researcher decision: move hardcoded page values into `RESEARCH_STATS` or mark `TODO` | `lib/constants.ts`, `data/page.tsx` | none | Needs her input |

---

## 5. Honesty guardrails (applied while implementing)

1. **No fabricated numbers.** Charts use only `NODE_CATEGORIES`, `DATASET_STATS`, `RESEARCH_STATS`, and the SAMPLE_NODE. The 6 in-page hardcoded values (১,০২২/৯১৫/৭০৪/৯০০/০.৭৮) get sourced or flagged `TODO` — never invented.
2. **The JPG stays labeled as illustrative** if kept ("স্কিম্যাটিক ইলাস্ট্রেশন" caption + `_gpt` provenance note), or is replaced by the real SVG graph. It must never be implied to be the actual KG render.
3. **No backend changes.** All data is client-side static, same as today.
4. **Reduced-motion respected** everywhere; count-up and draw animations degrade to instant show.

## 6. Open questions for the researcher

**RESOLVED 2026-08-13** — all five in-page numbers verified by text extraction from `paper/done papers/AgriTrust.pdf`:
1. ✅ 1,022 image-linked (35.5%) — AgriTrust §1/§3.3 · 915 crops / 704 variants / 2,729 chemicals — §3.2 · 900 answerable — §1/§5.1 · κ=0.78 KG-grounded — §5.1. All moved into `RESEARCH_STATS`.
2. JPG kept behind proper frame + lightbox, labeled "স্কিম্যাটিক ইলাস্ট্রেশন (জেনারেটেড)" — deletion decision still open (keep: low risk).
3. Sticky section rail on `lg`: not implemented (deferred — ask researcher).