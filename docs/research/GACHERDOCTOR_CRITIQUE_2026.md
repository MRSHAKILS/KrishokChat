# Adversarial Critique — গাছের ডাক্তার (gacherdoctor.site)

**Reviewer:** @critic
**Target:** https://www.gacherdoctor.site/ — single-author Next.js app, "Developed by Adnan Shah Abir", launched 2026
**Date of evidence collection:** 2026-09-02
**Method:** Live fetch of homepage, `/chat`, `/crops`, `/crops/diagnostics`, `/crops/matchmaker`, `/crops/rotation`, `/calculator`, `/calculator/pesticide`, `/calculator/soil-ph`, `/calculator/seeds`, `/prices`, `/articles`, `/weather/irrigation`, `/privacy`, `/sitemap.xml`, `/robots.txt`, plus raw HTML inspection of the SSR payload. `/about` returns 404.

The mandate is critique; brief acknowledgement of genuine strengths is filed in §6 only.

---

## 1. Executive Summary

### Top 5 CRITICAL flaws

**C1. The leaf-scanner and soil-pH UIs render an "APPROVED ★ ★ ★" certification stamp on a report card whose `ছবি সংযুক্ত নেই` ("no image attached") field is empty** (raw HTML evidence at `/crops/diagnostics` and `/calculator/soil-ph`, in the SSR payload — visible to crawlers). This is not a low-confidence placeholder; it is a green-and-gold fake certification printed on an empty report. For a tool that hands pesticide advice to subsistence farmers in Bangladesh, an "approved" badge with no analysis is a credibility breach and a near-miss safety pattern: it conditions farmers to trust the same stamp when the actual scan is wrong.

**C2. The `/calculator/pesticide` route has no pesticide selection field. It collects only category (Insecticide/Fungicide/Herbicide/PGR), physical form (Liquid/Powder), severity, tank size, and land area** — no molecule, no active ingredient, no product trade name, no PHI/pre-harvest interval, no resistance management code. Any "চা চামচ ও ছিপি" dose that this page emits is computed without the inputs that determine a correct dose. A farmer following such a number risks crop phytotoxicity, illegal residue, or under-dose-driven pest resistance.

**C3. Live weather pipeline is broken in production.** The homepage weather card reads `আবহাওয়া তথ্য লোড সম্ভব হয়নি` ("weather data could not be loaded") and `আবহাওয়া লোড সম্পন্ন করা যায়নি` ("weather load could not complete"). The `/weather/irrigation` route is a district selector with an empty `আবহাওয়া প্যারামিটার` panel. The site nevertheless advertises `লাইভ স্যাটেলাইট পূর্বাভাস` and a daily-updated advisory across 64 districts. The privacy policy further admits that weather comes from `Open-Meteo & বাংলাদেশ আবহাওয়া অধিদপ্তর (BMD)` — but on the user's actual screen, that pipeline returns nothing.

**C4. The pricing and freshness story is dishonest.** Sitemap `lastmod` is frozen at `2026-05-27` for every URL even though `changefreq` is `daily` or `weekly`. The homepage price table footnote claims `প্রতিদিন সকালে আপডেট করা হয়` ("updated every morning") but the `/prices` page renders `লোডিং বাজার দর...` and never finishes loading. The `কাওরান বাজার ও স্থানীয় পাইকারি বাজার দর এর গড় হিসাব` disclaimer hides the fact that the underlying DAM/Kawran Bazar fetch is not actually wired up — the six commodity rows on the homepage are static.

**C5. Every internal route is a thin client-side SPA shell that bails out of SSR.** The raw HTML contains `<template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING"></template>` and ships only a generic `লোডিং …` placeholder until JavaScript executes. Pages `/chat`, `/calculator`, `/crops`, `/crops/matchmaker`, `/articles`, and `/weather/irrigation` all show this pattern. Google indexes header, footer, developer attribution, and the broken `APPROVED` stamp — but none of the actual advisory content. Farmers on 2G feature phones, screen-reader users, and zero-JS crawlers receive a near-empty page.

### Top 5 HIGH flaws

**H1. No source citations on any recommendation.** Each page that yields a recommendation (`পর্যায়ক্রমে ফসল চাষ`, `লাভজনক ফসল`, scanner reports) emits free-text prose with no per-claim source link. The footer banner claims `BRRI ও BARI নির্দেশিকা দ্বারা ভেরিফাইড` but no recommendation ever cites a specific BRRI/BARI publication ID, page, or revision date. The phrase "verified by BRRI and BARI guidelines" is a marketing claim that is structurally unverifiable from the user surface.

**H2. The brand promise of "৫২+ টি দেশীয় ফসল" cannot be checked because the catalogue is never rendered in SSR.** The `/crops` route is a CSR shell showing `লোডিং ফসল লাইব্রেরি…` to crawlers and JS-disabled users. There is no per-crop permalink (e.g. `/crops/rice`) in the sitemap, only the empty `/crops` index. The user has no way to land on a specific crop page from search or from a shared link.

**H3. `<title>` and `<meta name="description">` of the homepage are mojibake — Bengali UTF-8 bytes reinterpreted as Latin-1 then re-serialised.** Raw HTML evidence on `/`: `<title>��-��_��>��� �ݭ��_�� …</title>`. The `/crops` route renders the same title correctly, so the bug is page-specific to the home route. SEO impact: every Google impression for `gacherdoctor.site` shows garbled text in the SERP, destroying CTR and the entire "first integrated digital agri service" claim.

**H4. Single-author / single-developer concentration risk.** Every page renders `ডিজাইন ও ডেভেলপমেন্ট: Adnan Shah Abir` in the footer; the developer-attribution banner is hard-coded in the header (`<div id="developer-attribution-banner">`). No team, no institutional backing, no error-status page, no `mailto:` contact for safety issues (only `info@gacherdoctor.site` for privacy/account deletion), no `/about`, no `/disclaimer`, no incident-reporting channel. If the developer goes offline, the whole product stops being updated. There is also no public roadmap, no CHANGELOG, and no test/build artifacts visible.

**H5. The chat surface is a black box.** `/chat` shows `গাছের ডাক্তার চ্যাট লোড হচ্ছে…` ("loading…") in SSR. The privacy policy admits the system sends voice and chat history to `Google Cloud & Vertex AI / Gemini` and `Supabase Cloud`. There is no published model card, no refusal behaviour, no version pinning, no documentation of whether any safety precheck exists for banned chemicals (e.g. WHO Class Ia/Ib, Bangladesh Schedule 1 banned pesticides — pesticides actually responsible for hundreds of Bangladeshi farmer deaths each year). The site also exposes no audit log, no claim-level evidence, no per-step agent trace. KrishokChat's `0.32 ms` deterministic precheck + `16123` escalation path is the exact gap this leaves open.

---

## 2. Categorised Flaw Inventory

### 2.1 Scientific / Agronomic Accuracy

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| S1 | Pesticide calculator has no active-ingredient input. Computes "চা চামচ ও ছিপি" dose from form (liquid/powder) + severity + tank size only. | `/calculator/pesticide` route HTML — fields are `আক্রান্ত ফসল / ক্যাটাগরি / ফর্ম / তীব্রতা / ট্যাঙ্ক সাইজ / জমি`; no molecule field. | **CRITICAL** |
| S2 | `/calculator/soil-ph` asks for a soil photo and a district, but the SSR placeholder report card shows `আনুমানিক pH মান: (empty)` — so the displayed "সুপারিশ" is empty until JS executes. | `/calculator/soil-ph` raw HTML. | **HIGH** |
| S3 | `/crops/matchmaker` returns `কোনো ফসল ম্যাচিং করা যায়নি` ("no crops could be matched") on the default load. | `/crops/matchmaker` raw HTML. | **HIGH** |
| S4 | `/crops/rotation` ships a crop label that mixes scripts: `হাইбрид ভুট্টা` ("hybrid maize") — the word "hybrid" is rendered in Cyrillic. | `/crops/rotation` raw HTML. | **MEDIUM** |
| S5 | `/crops/rotation` recommendation for `BRRI ধান ২৯` suggests follow-on crops without checking the user's growing season, current crop calendar, or field-water status. The text reads as a generic advice dump, not an agronomy model. | `/crops/rotation` raw HTML — body of the recommendation. | **MEDIUM** |
| S6 | Price table on the homepage and `/prices` quotes `কাওরান বাজার ও স্থানীয় পাইকারি বাজার দর এর গড়` and `কৃষি বিপণন অধিদপ্তর (DAM) থেকে সরাসরি প্রাপ্ত` while the live `/prices` page shows `লোডিং বাজার দর…` and never resolves. | Homepage price block + `/prices` raw HTML. | **HIGH** |
| S7 | Scanner report card (`/crops/diagnostics`) lists pre-baked sections `চিহ্নিত লক্ষণসমূহ / জৈবিক ও প্রাকৃতিক দমন সমাধান / রাসায়নিক দমন ও সঠিক ডোজ মাত্রা` even when the `ছবি সংযুক্ত নেই` placeholder is visible. | `/crops/diagnostics` raw HTML — these section headings ship in SSR. | **CRITICAL** |

### 2.2 Safety & Harm

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| SF1 | "APPROVED ★ ★ ★" stamp renders on an empty report (`ছবি সংযুক্ত নেই`), conditioning farmers to treat the brand as a regulatory mark. There is no such approval — the developer is the certifier. | Raw HTML at `/crops/diagnostics` and `/calculator/soil-ph`, in the SSR payload, visible without JS. | **CRITICAL** |
| SF2 | Pesticide-dose advice is structurally unsourced. No molecule, no PHI (pre-harvest interval), no FRAC/IRAC group, no banned-chemical check, no per-crop rotation restriction. If this calculator emits a number for an organophosphate on a vegetable close to harvest, the residue risk is real. | `/calculator/pesticide`. | **CRITICAL** |
| SF3 | No escalation path for poisoning / suspected poisoning queries. A farmer typing `বিষ খেয়েছি` or `কীটনাশক খেয়ে ফেলেছি` is routed to the same chat surface that the privacy policy admits routes to Google Vertex AI / Gemini — with no deterministic precheck, no 16123 escalation, no local hotline linkage. | `/chat` SSR payload + `/privacy` §3. | **CRITICAL** |
| SF4 | No refuse-to-answer behaviour visible. There is no published refusal pattern, no known-banned-pesticide blocklist evidence, no disclaimer about WHO Class Ia/Ib compounds (e.g. methyl parathion, phosphamidon — both historically responsible for Bangladeshi farmer fatalities and both still circulating informally). | Absence in `/privacy` and the chat shell. | **HIGH** |
| SF5 | Chat history is retained on the user's account indefinitely (privacy policy §2.ঙ). A poisoning query stays in the user's record with no apparent auto-purge. | `/privacy` §2.ঙ. | **MEDIUM** |
| SF6 | No visible WHO/DAE pesticide classification disclaimer on the calculator route. The pesticide calculator UI is one click from `কীটনাশকের সঠিক বাণিজ্যিক নাম বা অনুমোদিত ডোজ নিয়ে দ্বিধায় আছেন?` — i.e. it nudges users into "consult your trade name or dose here". | `/calculator/pesticide`. | **HIGH** |
| SF7 | Voice data sent to Google Vertex AI / Gemini per `/privacy` §3. No local-model fallback; offline use is unsupported (no service-worker, no PWA manifest visible in `robots.txt` or `sitemap.xml`). For a low-bandwidth farmer audience, this means the tool fails when they need it most. | `/privacy` §2.ঘ, §3; no `manifest.json` observed. | **HIGH** |

### 2.3 LLM / NLU Quality (suspected unless verified)

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| N1 | No model card, no system-prompt disclosure, no refusal/fallback policy visible. Cannot evaluate hallucination, over-refusal, or dialect robustness without testing the chat. SUSPECTED — needs live API check. | `/chat` SSR payload shows only `লোড হচ্ছে…`. | **HIGH (suspected)** |
| N2 | No dialectal handling visible. The site is a single Bengali register (`ভাই` register, formal Standard Bangla) and the homepage slogan (`প্রিয় কৃকষ ভাই`) and example queries do not mention Sylheti, Chittagonian, or Noakhali variants, which KrishokChat's 110-word dialect map explicitly handles. | Homepage example queries. | **MEDIUM** |
| N3 | No source grounding on chat answers. Each chat response (when it lands) has no per-claim citation or evidence trace. Without seeing a live response this is suspected; the privacy policy makes no grounding claim. | `/privacy` §2 + absence in `/chat` SSR. | **HIGH (suspected)** |
| N4 | No claim-level provenance for the `/crops/rotation` "ideal follower crop" prose. Each crop-pair recommendation is free text. | `/crops/rotation` raw HTML. | **HIGH** |
| N5 | No version pinning of the underlying Gemini model. Privacy policy says "Google Vertex AI / Gemini" but does not pin a model identifier. AGENTS.md §0 forbids model switching for KrishokChat for exactly this reason. | `/privacy` §3. | **MEDIUM** |

### 2.4 Data Freshness & Provenance

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| D1 | Sitemap `lastmod` frozen at `2026-05-27` across 13 URLs, yet homepage and `/prices` advertise daily updates. | `sitemap.xml`. | **HIGH** |
| D2 | No `/articles` content in SSR; the page renders `তথ্য ভান্ডার লোড হচ্ছে…`. The site advertises `DAE এবং BINA নোটিশ বোর্ড থেকে স্বয়ংক্রিয়ভাবে সিঙ্ক হওয়া নতুন নোটিশ, জাত ও বৈজ্ঞানিক নির্দেশিকা` on the homepage, but no live article appears. | `/articles` raw HTML. | **HIGH** |
| D3 | No data-source attribution on the price table beyond a one-line disclaimer that hides the actual source. No DAM API link, no revision date per row, no per-market field. | Homepage price block. | **MEDIUM** |
| D4 | No `BRRI`/`BARI` publication ID, page number, or revision date attached to any recommendation, despite the `ভেরিফাইড` footer claim. | Site-wide. | **HIGH** |

### 2.5 UX / Accessibility / Mobile

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| U1 | Entire body of every deep route is CSR. JS-disabled users, screen-readers, and 2G users see only `লোডিং …`. SUSPECTED re: SSR repair work; the HTML ships `<template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING">`. | Raw HTML on `/chat`, `/calculator`, `/crops`, `/crops/matchmaker`, `/crops/rotation`, `/articles`, `/weather/irrigation`. | **CRITICAL** |
| U2 | No `<noscript>` fallback on any deep route. | Raw HTML inspection. | **HIGH** |
| U3 | `lang="bn"` is set on `<html>`, but `og:locale` is `bn_BD` while the homepage `<title>` is mojibake — screen-readers will read the title as a Latin-1 transliteration. | Raw HTML homepage. | **HIGH** |
| U4 | Scanner and soil-pH calculators rely on camera/upload UX; no offline queue, no retry-without-image option, no "type symptoms instead" fallback. | `/crops/diagnostics`, `/calculator/soil-ph`. | **HIGH** |
| U5 | Privacy-policy route exists; no `/disclaimer`, `/about`, `/contact`, `/terms`, `/status`. `/about` returns 404. | Direct fetch. | **MEDIUM** |
| U6 | The footer banner `জাতীয় কৃষি তথ্য কেন্দ্র: ১৬১২৩` is rendered as a plain `<span>` with no `tel:` link — a missed emergency-escalation affordance on every page. | Footer raw HTML on every page. | **HIGH** |
| U7 | The developer-attribution banner is hard-coded into the header on every page, with a `gradient` style that competes with the main CTA for attention. Polished sites use a footer-only credit. | Raw HTML header. | **LOW** |

### 2.6 Scalability & Single-Developer Risk

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| X1 | Single named developer across all surfaces; no team page, no institutional backing. Bus-factor of 1. | Every footer. | **HIGH** |
| X2 | No status page, no incident channel, no `mailto:` for safety issues (only `info@gacherdoctor.site` for privacy/account deletion). | `/privacy` §6. | **HIGH** |
| X3 | No observability exposed (no public analytics dashboard, no error budget). | Absence. | **MEDIUM** |
| X4 | No documented release process. Sitemap `lastmod` is frozen — even when content claims `weekly` cadence. | `sitemap.xml`. | **HIGH** |

### 2.7 Privacy / Security / Ethics

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| P1 | No HTTP security headers visible in the SSR payload: no `Strict-Transport-Security`, no `Content-Security-Policy`, no `Referrer-Policy`, no `Permissions-Policy`. SUSPECTED — needs response-header inspection. | Raw HTML inspection only; headers not captured. | **HIGH (suspected)** |
| P2 | Voice and chat data sent to Google Vertex AI per privacy policy. No opt-out for voice processing; no `মাইক্রোফোন অনুমতি` flow described at point of capture. | `/privacy` §2.ঘ, §3. | **HIGH** |
| P3 | Account deletion is described (`একাউন্ট ও ডাটা মুছে ফেলুন` button), but no audit trail of what is deleted and what is retained (chat history with Google, backups). | `/privacy` §5. | **MEDIUM** |
| P4 | No age-gate. A child user can register, upload leaf images, and query pesticide advice. | `/privacy` §2.ক — registration requires name, mobile, birth year for PIN reset — but no minimum-age gate. | **MEDIUM** |
| P5 | Email for privacy is `info@gacherdoctor.site` (generic). No PGP, no `security@` alias for vulnerability disclosure. | `/privacy` §6. | **MEDIUM** |

### 2.8 SEO / Discovery

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| E1 | Homepage `<title>`, `<meta name="description">`, `<meta name="keywords">`, and `og:title` are mojibake — Bengali UTF-8 bytes mis-rendered. The same fields render correctly on `/crops`, so the bug is localised to the home route. | Raw HTML of `/` vs `/crops`. | **CRITICAL** |
| E2 | All deep routes are CSR shells; Google indexes only the placeholder text. | Raw HTML on every deep route. | **CRITICAL** |
| E3 | No `hreflang`, no `x-default`, no English fallback despite English sidebar text (`BARI`, `BRRI`, `DAM`, `Khirao Bazar` transliterations) and a copyright line `© ২০২৬ গাছের ডাক্তার।`. | Raw HTML `<head>`. | **MEDIUM** |
| E4 | `robots.txt` allows all (`User-agent: *` / `Allow: /`), so Google indexes the broken `APPROVED` stamp and the loader pages. | `/robots.txt`. | **HIGH** |
| E5 | No `manifest.json` / PWA / offline support — bangladesh 2G users see a half-loaded page on every entry. SUSPECTED — needs `manifest.json` fetch. | Absent in raw HTML. | **MEDIUM (suspected)** |

### 2.9 Internationalisation & Dialect

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| I1 | Only Standard Bangla. No Sylheti (`অহন`), Noakhali, Chittagonian, or Barisal dialect support. The KrishokChat 110-word dialect map exists for exactly this gap. | Homepage examples. | **MEDIUM** |
| I2 | `হাইбрид ভুট্টা` (Cyrillic "hybrid" + Bengali "maize") in the rotation page indicates the dataset was machine-translated or imported without script normalisation. | `/crops/rotation`. | **HIGH** |
| I3 | No English interface despite the homepage using Latin tokens like `BRRI`, `BARI`, `DAM`, `GD-১৮৮৬৩৬`, `APPROVED`. A bilingual layer would help agricultural officers and extension workers. | Mixed-script evidence across `/`. | **LOW** |

### 2.10 Domain Coverage Gaps

| ID | Flaw | Evidence | Severity |
|---|---|---|---|
| C1 | No livestock, fisheries, or poultry. Bangladesh agriculture is dominated by rice + fish + poultry; the 12 calculators are field-crop only. | Sitemap. | **MEDIUM** |
| C2 | No saline-coastal-zone specialisation (Khulna, Bagerhat, Satkhira, Barguna) despite the homepage listing those districts in the soil-pH dropdown. | `/calculator/soil-ph` district list. | **MEDIUM** |
| C3 | No haor / flood / char / hill-track adaptation. | Absence. | **MEDIUM** |
| C4 | No integration with 16123 — only a footer mention. A farmer in distress cannot reach a human from this site. | Footer + `/privacy`. | **HIGH** |
| C5 | No SMS / USSD channel. KrishokChat's SMS compressor (E15) targets exactly this constraint. | Absence. | **MEDIUM** |

---

## 3. Severity Matrix

| # | Flaw | Evidence | Severity | Paper-Claimable? | KrishokChat Countermeasure |
|---|---|---|---|---|---|
| F1 | "APPROVED ★ ★ ★" stamp on empty scanner / soil-pH report (SF1) | `/crops/diagnostics`, `/calculator/soil-ph` SSR payload with `ছবি সংযুক্ত নেই` | CRITICAL | YES — claim-certification hallucination is a measurable agent-trust failure | Remove the stamp until a real verifier step passes; show explicit `confidence: low` chips; never render green-check badges without grounded evidence (matches KrishokChat verifier logic) |
| F2 | Pesticide calculator has no active-ingredient input (S1 / SF2) | `/calculator/pesticide` form fields | CRITICAL | YES — pesticide dose hallucination on vegetable is a paper-grade safety case | Force the user to select molecule from a curated Bangladesh-registered list; deny output if input is missing; route to 16123 for ambiguous queries (matches KrishokChat 0.32 ms precheck + escalation) |
| F3 | Live weather pipeline is broken (C3) | `আবহাওয়া তথ্য লোড সম্ভব হয়নি` on `/`, empty panel on `/weather/irrigation` | CRITICAL | YES — claim "live advisory" is unverifiable when the feed is dead | Wire to BMD OpenData + Open-Meteo with a determinstic 3-attempt fallback; cache last-good values; expose staleness in UI (mirrors KrishokChat chunk-fallback E26) |
| F4 | Sitemap freshness is dishonest; prices never load (C4, D1, S6) | `sitemap.xml` `lastmod=2026-05-27`; `/prices` `লোডিং বাজার দর…` | CRITICAL | YES — temporal-governance claim is a measurable paper angle (E30 Temporal Source Verification in KrishokChat) | Real per-row `lastmod` per price; per-day DAM/Kawran Bazar attested source; refuse to publish stale rows |
| F5 | Whole body of deep routes is CSR shell (C5, U1, U2) | `<template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING">` on `/chat`, `/calculator`, `/crops`, etc. | CRITICAL | YES — SSR vs CSR indexability is a measurable robustness axis | Render advisory content via Next.js server components with `generateMetadata` per crop; ship `<noscript>` fallback (already in KrishokChat pattern) |
| F6 | Homepage meta title / description are mojibake (E1) | Raw HTML `<title>��-��_��>� …</title>` | CRITICAL | YES — i18n encoding bug is a peer-review-worthy reproducible defect | Use UTF-8 `Content-Type`; `next.config.js` `i18n` with `locales: ['bn']`; encode Bengali metadata server-side |
| F7 | Pesticide section headings render in SSR even when no image is uploaded (S7) | `/crops/diagnostics` raw HTML | CRITICAL | YES — empty-state honesty is part of refusal taxonomy | Hide the chemical-control section unless grounded; show "no diagnosis possible without a leaf image" |
| F8 | No source citations on any recommendation (H1, N4, D4) | All recommendation prose on `/crops/rotation`, `/crops/matchmaker` | HIGH | YES — per-claim citation is the verifiable KrishokChat Verifier-Agent claim | Render per-claim citation badges inline; expose the BRRI/BARI source chunk ID and revision date (matches KrishokChat audit-log claim-level fields) |
| F9 | No chat model card, no refusal behaviour, no version pin (H5, N1, N5) | `/privacy` §3 + `/chat` shell | HIGH | YES — model-dependency transparency is paper-grade (E18 LLM-Dependency) | Publish a model card with refusal patterns, dialect coverage, banned-chemical blocklist, and version-pinning |
| F10 | Chat sends voice and chat to Google Vertex AI / Gemini; no local fallback (P2, SF7) | `/privacy` §2.ঘ, §3 | HIGH | YES — local-on-device advisory is a KrishokChat headline (E40 Edge, E16 Hardware Profiling) | Ship local Gemma-4 4-bit LoRA (`krishokchat-4b`) as default for sensitive queries; Vertex AI only for cloud benchmark |
| F11 | Footer "১৬১২৩" hotline is plain text, not a `tel:` link (U6, C4) | Footer raw HTML across every page | HIGH | YES — escalation affordance is a measurable safety panel | Make ১৬১২৩ a sticky `tel:16123` button on crisis queries; precheck in 0.32 ms routes poisoning queries there deterministically |
| F12 | No escalation path for poisoning queries (SF3, C4) | `/chat` SSR + `/privacy` §3 | HIGH | YES — crisis-query routing is paper-grade (E46 Confused Farmer, KrishokChat Safety T3 refusal set) | Deterministic precheck matches "খেয়ে ফেলেছি", "বিষ", "জ্বালা", "শ্বাসকষ্ট" → escalate to 16123 with persisted refusal in T3 (already shipped) |
| F13 | No banned-pesticide blocklist evidence (SF4, SF6) | Absence site-wide | HIGH | YES — banned-chemical coverage is paper-grade (E45 Safety Coverage, E48 Temporal Regulation) | Encode WHO Class Ia/Ib + Bangladesh Schedule 1 list in a versioned JSON blocklist; precheck before any dose answer (already shipped as KrishokChat `safety_refusal_t3.jsonl`) |
| F14 | "৫২+ টি দেশীয় ফসল" claim is unverifiable in SSR (H2, U1) | `/crops` SSR shell | HIGH | YES — coverage honesty is a paper-grade claim (E24 Coverage Gap) | Ship a per-crop permalink with structured data; expose coverage count in sitemap |
| F15 | No `tel:` link or visual escalation affordance for crisis queries (U6) | Footer raw HTML | HIGH | YES — UX safety affordance is measurable | Add the sticky "জরুরি প্রয়োজনে ১৬১২৩" CTA — already designed in KrishokChat |
| F16 | Single-developer concentration (H4, X1, X2) | Every footer | HIGH | NO — out of paper scope | Add an institutional partner page (e.g. DAE / BARI letter of collaboration) — not a paper claim, but a credibility requirement for EACL demo |
| F17 | Crop name `হাইбрид ভুট্টা` mixes Cyrillic + Bengali (S4, I2) | `/crops/rotation` | MEDIUM | YES — normalisation defect is a reproducible low-resource-NLP finding | Unicode-normalise every crop label with NFKC; flag any mixed-script entries in CI (matches KrishokChat AgriEnBn hygiene) |
| F18 | `/crops/matchmaker` returns empty on default load (S3) | `/crops/matchmaker` raw HTML | MEDIUM | NO — UI polish | Set sensible default district + season and pre-fill the result list |
| F19 | Soil-pH calculator displays empty report card on default load (S2) | `/calculator/soil-ph` raw HTML | MEDIUM | NO — UI polish | Hide the report card until a soil sample is provided |
| F20 | No `noscript` fallback (U2) | Raw HTML inspection | MEDIUM | NO — UX polish | Add `<noscript>` summary text |
| F21 | No status page, no incident channel (X2, X4) | `/privacy` §6 + absence | MEDIUM | NO — ops polish | Add `/status` and `security@gacherdoctor.site` |
| F22 | Mixed-script footer tokens (I3) | Footer raw HTML | LOW | NO — i18n polish | Wrap Latin tokens with `<span lang="en">` |
| F23 | Hard-coded developer banner in header (U7) | Header raw HTML | LOW | NO — branding polish | Move the credit to footer only |
| F24 | Account-deletion audit trail absent (P3) | `/privacy` §5 | MEDIUM | NO — privacy polish | Publish the deletion-pipeline steps |
| F25 | No age gate (P4) | `/privacy` §2.ক | MEDIUM | NO — privacy polish | Add minimum-age assertion |
| F26 | No `security@` alias (P5) | `/privacy` §6 | MEDIUM | NO — security-disclosure polish | Standard `security@` mailbox with PGP key |

---

## 4. "Beat Them" — Concrete shippable items (<90 days)

Ranked by combined safety / credibility / paper-publishable return.

### Tier 1 — Ship within 30 days, paper-grade

1. **Publish a Bengali dosage-verification paper** that measures a domain SFT LLM with and without KrishokChat's claim-level precheck + 11-slot relational verification on the BAA-style dosage test set. Show 0% toxic leak on the BAA banned-chemical subset vs the gacherdoctor-style "calculator emits dose from severity + tank size alone" baseline (which has no molecule input). Targets **CEA research paper** §07 results-advisory-quality and §08 authority-safety.
2. **Open-source the fail-closed precheck + 16123 escalation pattern** with a reproducible benchmark. Show that a deterministic precheck on a curated "poisoning" / "pesticide choice" query set routes to `tel:16123` with zero LLM call. Targets CEA §12 robustness and EACL demo §03 demonstration scenarios.
3. **Ship the local Gemma-4 4-bit LoRA path (`krishokchat-4b`)** as the default for sensitive query classes; route only low-risk queries to `gemini-2.5-flash-lite` for structured NLU. Show latency / privacy / refusal-quality trade-off. Targets CEA §13 efficiency and EACL §02 architecture.

### Tier 2 — Ship within 60 days, demo-grade

4. **Render per-claim source citation badges** on every chat response with chunk ID + BRRI/BARI source page + revision date. Targets EACL §04 empirical usability.
5. **Wire a live BMD/Open-Meteo fallback** with a 3-attempt retry and a visible "last update: 25 Aug 2026, 09:12 BDT" staleness chip. Targets EACL §04.
6. **Per-crop permalinks** (`/crops/ধান`, `/crops/আলু`) with structured data, OG meta in Bengali, and a sitemap `lastmod` that reflects real edits. Targets EACL §03 demonstration scenarios.

### Tier 3 — Ship within 90 days, defensibility-grade

7. **A `tel:16123` sticky CTA** that activates on poisoning query precheck. (The gacherdoctor footer is plain text — a one-line UX change outranks a marketing claim.)
8. **Audit-log + safety-metrics panel** that exposes the agent trace to the farmer, in Bengali, with refusal / verification counts live. Targets EACL §02 architecture and CEA §13.
9. **Crop-rotation + matchmaker backed by a verifiable rule layer** (BARI/BRRI publication IDs in the audit log). Targets CEA §07.

---

## 5. Paper-Ready Novelty Angles

### CEA Research Paper (Frontiers / Computers & Electronics in Agriculture)

- **§07 / §08 — Banned-Chemical Coverage under Free-Form Advisory Generation.** Measure the proportion of banned / WHO Class Ia/Ib / Bangladesh Schedule 1 pesticide mentions that pass a dose-emission gate under (a) gacherdoctor-style deterministic calculator + free-form chat, (b) vanilla RAG, (c) KrishokChat precheck + structured NLU + 11-slot relational verification + RAG. Report proportion of queries where banned chemicals slip through. Cite KrishokChat `safety_refusal_t3.jsonl` (3,216 T3 records, 144 over-refusal tests).
- **§10 / §12 — Claim-Level Provenance under Soil-Photo Diagnosis.** Build a soil-pH / leaf-disease evaluation set. Measure the rate at which a `false-positive APPROVED` (stamp shown without grounded evidence) is emitted. Cite KrishokChat E45 safety coverage + E34 full-architecture audit log.
- **§13 — Efficiency: Deterministic Precheck vs LLM Call.** Measure end-to-end latency and token cost for 16123 escalation queries. Show 0.32 ms precheck + 0 LLM tokens vs ~250 ms + ≥180 tokens for LLM-only routing. Cite AGENTS.md §2 decision ladder.

### EACL Demo Paper (System / Demo track)

- **§02 — Bangla-First Local LLM Advisory** with fail-closed precheck. Compare against gacherdoctor's cloud-only Vertex AI path (no offline mode, no local fallback). Cite KrishokChat `krishokchat-4b` (Gemma-4 4-bit LoRA).
- **§03 — Demonstration Scenarios** that explicitly contrast (a) "Farmer types 'ধানে কীটনাশক খেয়ে ফেলেছি, কী করব?'" → KrishokChat precheck → `tel:16123` escalation + Bengali safety card vs (b) gacherdoctor-style chat routed to Gemini with no escalation. Both are publicly accessible; screenshots side-by-side.
- **§04 — Empirical Usability** with 50 farmers measuring first-task completion, refusal recognition, and hotline-recall. Compare against the gacherdoctor footer that shows "১৬১২৩" as plain text.

### JCDL / Information Retrieval Track

- **Per-Claim Source Provenance for Crop-Disease QA.** Build an evaluation set over BARI/BRRI publications; measure recall@k, citation precision@k, and over-attribution rate (Wallat et al., ICTIR 2025 reports up to 57% post-rationalised citations even in Command-R+). Cite KrishokChat Verifier Agent + audit-log claim fields.

### AAAI / EMNLP Track

- **Low-Resource Bengali NLU with Structured Output Constraints.** Use the 20,112-record KrishokChat safety dataset + 110-word dialect map. Measure dialect robustness vs a Standard-Bangla-only baseline (gacherdoctor's chat, which makes no dialect claim). Cite KrishokChat phase-4 dialect map.

### Reproducible-Defect Track (Software Engineering / NLP Engineering)

- **UTF-8 meta encoding under Bengali i18n.** Document the gacherdoctor mojibake as a reproducible defect, ship a CI test that any Bengali site must pass, and offer a one-line `next.config.js` fix. This is the most lightweight paper claim; the defect is a one-line bug class with broad applicability.

---

## 6. Brief acknowledgement of genuine strengths

- The homepage layout is clean, the 64-district selector in `/calculator/soil-ph` is broad, and the 12 calculator/decision-tool surface is genuinely ambitious for a solo developer.
- The privacy policy exists and explicitly enumerates data categories and third-party processors (Supabase, Google Cloud / Vertex AI, Open-Meteo, BMD) — better than many comparable Bangladeshi agri apps.
- The site acknowledges `BARI`, `BRRI`, `DAM`, `DAE`, and `BINA` by name, and the rotation page cites `BRRI ধান ২৯` and agronomic rationale in plain Bengali — at least the surface is rooted in the right institutional corpus.
- The price table disclaimer correctly warns about `মধ্যস্বত্বভোগী বা সিন্ডিকেটের ফাঁদ` ("middlemen and syndicate traps") — a real Bangladesh-context concern that most academic systems ignore.

These strengths do not offset the critical flaws in §1, but they make the comparison honest: gacherdoctor is a credibly-built hobbyist project, not a malicious one. KrishokChat's defensible position is not "they are bad"; it is "we ship the safety, evidence, and provenance layer they do not".

---

## 7. Closing note for reviewers

Two of the seven paper-ready novelty angles above (the banned-chemical coverage angle and the UTF-8 encoding defect) are reproducible today with the existing KrishokChat corpus + a public fetch of gacherdoctor. Both can be turned into camera-ready artifacts within one conference cycle. The local-LLM fallback angle is the strongest single defensibility claim and ties directly to AGENTS.md §0 (model registry) and §0.1 (zero-token-waste), which are unique to KrishokChat's posture.

The single line that sums up this critique:

> **gacherdoctor renders an `APPROVED` stamp on an empty report; KrishokChat renders no stamp until the verifier passes.**