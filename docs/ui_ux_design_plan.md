# UI/UX Design Masterplan — Bangladesh Agri Advisory Platform
*Design planning to hand to Google Stitch, then to your vibe-coding agents*

---

## 0. The design thesis

Judges will spend 3–4 minutes with you, but this platform will also sit in front of "normal viewers all day" at the venue — people who won't hear your pitch, will just click around. For that audience, **the UI has to argue your case by itself**, with no narration. That reframes the whole job: you're not designing a chatbot with some extra pages bolted on, you're designing an **advisory product** — something that looks and feels like it belongs next to a bank's or telco's farmer-facing app, not like a hackathon demo of an LLM.

The single biggest lever for that perception: **stop presenting the model's output as chat bubbles and start presenting it as advisory reports.** A diagnosis with a confidence score, a treatment table, a source citation, a "verified against our knowledge base" badge — that reads as a *system*. A gray bubble that says "You should apply X fungicide" reads as *a chatbot*, no matter how good the model is. Every page spec below is written with that principle in mind.

---

## 1. Brand identity

### Visual direction
Avoid the default 2026 AI-app look (dark mode, purple/blue gradients, glassmorphism, generic robot/circuit iconography) — it's what every Stitch/v0 output defaults to unless you steer it, and it signals "generic wrapper," which is the opposite of what a first-of-its-kind Bangladesh research platform should signal.

Instead, commit to an identity grounded in the actual subject matter:
- **Palette:** paddy-field green as the primary (not a generic SaaS green — lean toward a deeper, slightly muted green, like young rice) + a warm soil/terracotta accent for alerts and CTAs + a soft off-white/rice-paper background rather than pure white or dark mode. This is a daytime, outdoor, agricultural product — it should not look like a fintech dashboard.
- **Typography:** a proper Bengali display typeface (e.g. Tiro Bangla or Hind Siliguri for body text) paired with a clean Latin sans for numbers/English — and treat Bengali as the *primary* language throughout, with English as secondary, not the other way around. This alone differentiates you from 95% of AI demos a jury will see that day.
- **Imagery:** real field/crop photography (yours, from your dataset work, or your own photos) over generic icons wherever a page needs a hero image. Authentic imagery from actual Bangladeshi farmland is a differentiator no generic template can match.
- **Iconography:** simple line icons, agriculture-specific where possible (leaf, droplet, thermometer, sprout) rather than generic tech icons.
- **Motion:** purposeful, not decorative — a scanning animation while detection runs, a step-by-step reveal for the agent trace, gentle count-up animations for benchmark stats. No animation without a job to do.

### UI Modes and Constraints
- **Two UI Modes:** Support a "Farmer Mode" (simple, large text, high contrast, trust badges, call buttons, agent trace hidden by default) and a "Research/Demo Mode" (shows detailed agent trace, retrieval sources, verifier results, and audit info).
- **Offline / Low-Data Mode:** For Bangladesh's connectivity constraints, use PWA techniques, cached UI, client-side image compression before upload, and local form validation. Provide a graceful offline fallback message.

### The "advisory, not chatbot" component vocabulary
Design (and later ask Stitch/agents to build) these as first-class, reusable components — they're what makes every module feel like one coherent system rather than separate demos glued together:
- **Advisory Card** — a structured result block: title, confidence/verified badge, short summary, expandable detail, source citation, "consult 16123" footer link when relevant.
- **Agent Trace Stepper** — the small animated sequence showing pipeline stages (Checking safety → Retrieving sources → Generating answer) from `AGENTS.md` Section 4. Reuse this everywhere the pipeline runs, not just the chat page.
- **Source Chip** — a small pill showing which knowledge-base node(s) backed an answer, tappable to reveal the underlying text.
- **Confidence Badge** — color-coded (verified/grounded vs. low-confidence/unverified) — this is your Verifier Agent made visible, and it's a strong trust signal for viewers who understand nothing about RAG.

---

## 2. Full site map

More pages than just chat + detection, because a jury (and passers-by) forming an opinion in minutes needs a story arc to walk through, and idle viewers need something to explore:

| # | Page | Purpose |
|---|---|---|
| 1 | **Home / Landing** | The 15-second pitch. What this is, why it's first-of-its-kind, quick links into every module. |
| 2 | **Advisory Chat** | Core feature — Bengali agri Q&A, grounded + safety-checked (built in Task 01/02). |
| 3 | **Disease Detection** | Upload/capture a leaf photo → crop classifier → crop-specific YOLO → diagnosis advisory card. |
| 4 | **Weather Advisory** | Location-based forecast translated into farming guidance (spray/irrigation timing), not a raw weather widget. |
| 5 | **Market Prices** | Crop price trends, presented as a "should I sell now" advisory, not a raw price table. |
| 6 | **Find Help Nearby** | Krishi Call Center (16123) front and center, plus nearby agri input shops / extension offices on a map. |
| 7 | **Research & Benchmarks** | The credibility page — your actual research: dataset scale, benchmark numbers, model comparisons, paper references. |
| 8 | **About / Vision** | Short, for idle browsers — who built this, why, what's next. |

Global elements present on every page: a persistent nav (icon + label, mobile-friendly), a Bengali/English toggle, and a small fixed "16123 — talk to a human expert" affordance (footer or corner) — this single detail does a lot of work signaling responsible design to reviewers.

---

## 3. Page-by-page detailed spec

### 3.1 Home / Landing
**Purpose:** the argument, made visually, in one screen before any scrolling.
**Key components:** hero section with a real field photo, one strong headline (in Bengali, with English subhead) stating the "first-of-its-kind for Bangladesh" claim, three module-entry cards (Chat / Detect / Advisory tools) with icons and one-line descriptions, a stats strip (dataset size, number of treatments in knowledge base, number of crops covered) animated as count-ups on scroll.
**States:** none dynamic — this page is static/marketing, keep it simple and fast-loading.
**Stitch prompt guidance:** generate this alongside the other core screens in one multi-screen Stitch session so the hero styling, card styling, and stat-strip styling define the tokens the rest of the app inherits.

### 3.2 Advisory Chat
**Purpose:** the core, novel feature — already functionally working from Task 01; this pass is purely visual/structural.
**Key components:** message input (large, Bengali-friendly, with a mic icon reserved for future voice input), Agent Trace Stepper (hidden by default in Farmer mode, visible in Research mode), answers rendered as **Advisory Cards** (not raw chat bubbles) with explicit **Source Citations** (Knowledge Node ID, verified by, last reviewed date). Also add a rail of 4–6 suggested example questions, a "read aloud" (TTS) icon, and a **Feedback Loop** component ("Was this answer helpful?", "Was this advice safe?").
**States:** empty (show suggested questions prominently), loading (Agent Trace Stepper animates), safe-answer, flagged/redirected-to-16123 answer (visually distinct — a calmer, differently-colored card), error (model/server unreachable — should never be reached on demo day, but design it so it fails gracefully, not with a raw error).
**Stitch prompt guidance:** explicitly describe the Advisory Card and Agent Trace Stepper as reusable components in your Stitch prompt, since this page defines them for reuse on the Detection page.

### 3.3 Disease Detection
**Purpose:** the visual, immediately-legible flagship feature.
**Key components:** an upload dropzone that supports camera capture, accompanied by **Guided Image Capture** examples (showing good vs. bad photos, "take a close-up"). Include a scanning/processing animation, an annotated image result, and a diagnosis Advisory Card. The Advisory Card must show crop identified, disease name, explicit uncertainty messaging if confidence is low, treatment steps, dosage, and a Verifier/Confidence Badge. Include a feedback prompt here as well.
**States:** empty/upload prompt, processing (scanning animation), crop-not-recognized (classifier low confidence — should say so honestly, not force a guess), result.
**Stitch prompt guidance:** ask for this as one of the connected screens in the same multi-screen session as Chat, explicitly reusing the Advisory Card component so it visually matches.

### 3.4 Weather Advisory
**Purpose:** turns a raw forecast into farmer-relevant guidance — this is what makes it "advisory" rather than "we embedded a weather widget."
**Data source:** 🔎 **Open-Meteo** is the strongest fit for a 7-day prototype — it requires no API key at all (zero setup risk, nothing to break on demo day) and has good free-tier coverage for Bangladesh. If you already hold an OpenWeatherMap key from prior work, that's a fine alternative — 🔎 confirm current free-tier limits before relying on it live. Either way, cache/precompute the response for your demo location shortly before presenting, exactly like the RAG index — don't depend on a live external call succeeding at the exact moment a judge is watching.
**Key components:** a simple location selector (default to a demo district), a 3–5 day forecast strip, and — the actual value-add — 2–3 auto-generated advisory lines translating the forecast into action ("Rain expected Thursday — delay pesticide spraying" / "High humidity this week — monitor for fungal disease risk"). This translation layer is what turns a commodity weather API into a feature worth showing.
**States:** loading, loaded, fallback-to-cached-snapshot if the live call fails (silent fallback, no visible error).

### 3.5 Market Prices
**Purpose:** signals real-world usefulness beyond diagnosis — "should I sell now."
**Data source:** 🔎 Bangladesh's Department of Agricultural Marketing (DAM) publishes daily prices at `market.dam.gov.bd`, and `data.gov.bd` lists agriculture datasets, but neither currently offers a clean, stable, documented public API suitable for a live prototype call — confirm this yourself before building against it, since data portal capabilities do change. **Recommendation: don't build a live scraper against a government portal for a 7-day prototype** (fragile, and scraping a government site live during a demo is exactly the kind of risk this whole plan is trying to avoid). Instead, pull a snapshot of recent prices for 5–6 key crops once, store it as a static JSON (same pattern as your knowledge-base JSON), and present it as real data with a "data as of [date]" note — honest, safe, and still demonstrates the feature.
**Key components:** a simple line/bar chart per crop (Recharts) showing recent price trend, plus a one-line auto-generated insight ("Prices for [crop] have risen X% this month").

### 3.6 Find Help Nearby
**Purpose:** the "we're not trying to replace human expertise, we're extending it" statement — genuinely important for how reviewers will judge responsibility/safety framing, and it's also where your Safety/Router Agent's escalation path becomes visible as a real, browsable feature rather than just a fallback message.
**Key components:** the Krishi Call Center number (16123) as a large, prominent tap-to-call element at the top; below it, a map showing nearby agricultural input shops or extension offices — 🔎 if using Google Places API (since you mentioned having API keys), search current Places API pricing/quota before wiring this in live, and consider caching results for your demo location rather than calling live.
**Note:** this page doubles as the visible destination for the "flagged" path in the Advisory Chat — link them together (a flagged chat answer's card should have a button straight to this page).

### 3.7 Research & Benchmarks
**Purpose:** the credibility layer for reviewers who want to know this isn't just a slick UI over a generic model.
**Key components:** dataset scale stats (treatment count, knowledge nodes, crops covered), a model comparison table/chart (your fine-tuned model vs. baselines, from your existing evaluation work), and short cards referencing your related papers (KrishokChat, ChitraMiti, etc.) by name and one-line description — this is where "first of its kind for Bangladesh" gets substantiated with actual numbers, not just claimed.
**Key components (visual):** Recharts bar/line charts for benchmark comparisons, a simple stat-grid.

### 3.8 About / Vision
**Purpose:** low-effort, exists mainly so idle browsers get context if the chat/detect pages don't hook them immediately. One paragraph, your name/affiliation, a short "what's next" line. Don't over-invest here.

---

## 4. How to actually build it: Stitch workflow

1. **One multi-screen Stitch session, not eight separate ones.** Since Stitch (as of the 2026 update) generates several connected screens from one prompt and keeps them visually consistent automatically, describe Home, Chat, Detection, and Weather together in a single prompt — these four define your core visual language (Advisory Card, Agent Trace Stepper, color/type tokens). Generate Market Prices, Find Help, Research, and About in a second pass, explicitly telling Stitch to match the established system (Stitch supports extracting/reusing a design system across projects for exactly this).
2. **Be specific in your Stitch prompt** about the things that make this non-generic: mention the palette direction (paddy green + terracotta, not purple gradients), Bengali-first typography, real photography over icons for hero sections, and the Advisory Card concept by name so it treats that as a genuine reusable component, not a one-off chat bubble.
3. **Export the `DESIGN.md`** the moment you're happy with the direction — this becomes the design contract in `AGENTS.md`. Don't wait until every screen is perfect; export early and let your coding agents start structural work while you keep refining visuals in Stitch in parallel.
4. **Iterate with Direct Edits in Stitch for small fixes** (spacing, copy, colors) rather than full re-prompts once the structure is right — full re-prompts risk breaking the cross-screen consistency you just established.
5. Expect a gap between Stitch's output and production-ready code — treat its export as a very strong starting point and design reference, not a drop-in final component library. Your agents will still need to rebuild pages properly in your actual Next.js + shadcn/ui stack, using Stitch's screens and `DESIGN.md` as ground truth.

---

## 5. Execution order for vibe-coding agents

Do not build pages in the order they appear in the site map — build in the order that protects your demo:

1. **Retrofit design onto Advisory Chat first.** It's already functionally working from Task 01 — this is the highest-leverage design pass because it's your headline feature. Build the Advisory Card, Agent Trace Stepper, and Source Chip components here first; every later page reuses them.
2. **Disease Detection second** — your other flagship, most visually impressive feature.
3. **Home/Landing third** — now that Chat and Detection exist, the landing page's module cards and stats have something real to point to.
4. **Weather Advisory and Find Help Nearby fourth** — these round out the "advisory system, not chatbot" story and are lower risk (simpler data, less demo-critical if slightly rough).
5. **Market Prices and Research/Benchmarks fifth** — high credibility value but lowest demo-time risk if they're the least polished; viewers browsing after the pitch will still find real substance here even if it's simpler visually.
6. **About/Vision last**, or cut entirely if day 7 runs short — it costs you nothing to skip.

Each page should be handed to an agent as its own scoped task, referencing: this design spec's relevant section, the exported `DESIGN.md`, and the shared component list already built by earlier tasks (don't let a later agent reinvent the Advisory Card).

---

## 6. Design review checklist (run this before calling any page done)

- Does this page look like it belongs to the *same product* as the others (color, type, spacing, component reuse) — not just "on brand" in isolation?
- Is any LLM output presented as a structured Advisory Card, never a raw text/chat bubble?
- Does every async action have a real loading state (Agent Trace Stepper or equivalent) — no blank screens while waiting?
- Does every external-data page (Weather, Market Prices, Find Help) degrade gracefully to cached/precomputed data rather than showing a visible error if a live call fails?
- Is Bengali the primary language on-screen, with English secondary, everywhere — not just on the landing page?
- Would a non-technical person, given 20 seconds alone with this page and no explanation, understand what it does?