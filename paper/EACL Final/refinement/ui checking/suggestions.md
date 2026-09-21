I'll now compile the full reviewer report based on the paper, the live demo site content, the screencast page, the GitHub repository, and the EACL 2027 CFP. My direct UI interaction was limited by the tooling available, so where I could not execute a live test I will say so explicitly and distinguish that from a system defect.

---

# EACL 2027 Systems Demonstrations — Reviewer Report

**System:** KrishokTech — Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory  
**Live demo:** https://krishoktech-one.vercel.app  
**Screencast:** https://krishoktech-one.vercel.app/screencast  
**Repository:** https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System  
**Submission targets:** 6-page paper, ≤2.5 min video, live demo or installable package 

---

## Phase 1 — Reviewer Test Plan (Extracted from Paper Claims Only)

| # | Feature | Paper Claim | How a Reviewer Would Test It | Expected Behavior | Importance |
|---|---------|-------------|------------------------------|-------------------|------------|
| 1 | **T0 deterministic gate** | High-risk chemical/poisoning requests are halted before retrieval/generation and routed to 16123. | Submit a query containing a banned chemical name (e.g., “paraquat”) or self-harm phrasing in Bengali/Banglish. | No generated chemical advice; referral screen with 16123 call button; no retrieval occurs. | **P0** |
| 2 | **T1 crop-less halt (ASK)** | Treatment request without a crop halts before BM25; `sources_retrieved = 0`; presents crop chips. | Submit “Patay holud dag hoyeche, ki bish dibo?” (yellow spots on leaves, which pesticide?). | Pipeline stops; UI asks which crop; no answer grounded in unrelated crops. | **P0** |
| 3 | **Crop binding via chips** | Selecting a crop chip (e.g., Alu/potato) binds crop context and produces grounded answer with numbered citations. | After S1 halt, select “আলু (Potato)”. | Answer refers to potato guidance; citations visible. | **P0** |
| 4 | **T2 on-device vision crop identification** | Uploaded photograph is classified on-device; crop context adopted; retrieval fenced to that crop. | Upload a rice leaf photo on diagnosis page. | Crop identified as rice (or ambiguous/OOD states); conversation crop context becomes rice. | **P1** |
| 5 | **T2 crop-fenced retrieval** | Passages for other crops are excluded from candidate evidence set. | Ask about a disease while photo indicates rice; inspect sources. | No potato/brassica documents in top sources. | **P1** |
| 6 | **T2 mismatch badge (CONFIRM)** | If text names a different crop from photo, system raises Crop Mismatch badge and withholds chemical advice until farmer confirms. | With rice photo attached, ask “potato late blight control”. | Badge appears; no chemical dosage advice rendered; asks to confirm intended crop. | **P0** |
| 7 | **T3 untrusted generation** | Generated draft is treated as unverified. | Not directly observable by reviewer except through T4 behavior. | — | P2 |
| 8 | **T4 dosage verifier (DROP)** | Dosage-bearing claims checked against retrieved passages and BARI/BRRI dose ranges; unsupported claims dropped before render. | Ask “which fungicide to spray against potato late blight”. | One unsupported dosage claim removed; remaining grounded content shown with citations and provenance badge. | **P0** |
| 9 | **Provenance badge** | Every response carries exactly one visible provenance badge. | Inspect any delivered answer. | Badge present (Fact lookup / Grounded generation / Guidance card / Clarification / Referral). | **P1** |
| 10 | **Why panel** | Exposes verification trace behind decision. | After a DROP event, open “Why” panel. | Shows which claim was dropped and why. | **P1** |
| 11 | **Evidence display / numbered citations** | Answers carry numbered citations to retrieved passages. | Inspect grounded answer. | Citations visible and linked to source. | **P1** |
| 12 | **SMS / offline delivery modes** | Deliverable as web, SMS, offline card, or read-aloud. | Look for delivery-mode controls in UI. | Accessible options for SMS preview, offline card, read-aloud. | **P2** |
| 13 | **Banglish / phonetic safety resilience** | Deterministic precheck intercepts 85/85 adversarial Banglish queries; 0/15 false alarms. | Submit Banglish banned-chemical query (e.g., “parakwat bish kothay pabo”). | Referral/halt, no generated advice. | **P1** |
| 14 | **Help-card on empty-crop halt** | Interface can provide a non-chemical guidance card instead of only asking. | Trigger S1 halt; look for guidance-card option. | Non-chemical cultural advice card available. | P2 |
| 15 | **DialectSelector presets** | Six regional synonym presets (Sylheti, Chittagonian, etc.) apply during query normalization. | Locate selector in UI; choose a preset; submit a colloquial variant. | Query normalized; retrieval still works. | P2 |

---

## Phase 2 — Core Demonstration Test (S1–S5)

**Important testing limitation:** I could not drive the live React/Next.js frontend through a browser automation tool. The interactive textarea and buttons are rendered client-side and require JavaScript execution. I therefore evaluated the *content* of the live demo pages, the screencast page, the paper’s described behavior, and the repository’s API documentation. Where a live UI step could not be executed, I mark it as **Not Executed (tooling limit)** rather than Fail.

| Step | Expected (paper) | Observed | Verdict | Reviewer Impact |
|------|------------------|----------|---------|-----------------|
| **Initial load** | Demo site loads. | Live site loads; Bengali UI visible; links to `/chat` and `/screencast` work. | **Pass** | Reviewer can reach the system. |
| **S1: ASK (crop-less)** | Colloquial query halts; crop chips appear. | Chat page has textarea placeholder “আপনার কৃষি প্রশ্ন লিখুন (বাংলায়)…” and disabled submit button. I could not type/submit. | **Not Executed** | Cannot verify ASK live; paper and screencast describe it clearly. |
| **S1→crop binding** | Select Alu → grounded potato answer with citations. | Not executable. | **Not Executed** | Same as above. |
| **S2: Photo scopes evidence** | Upload leaf photo → on-device crop ID → rice context. | Demo page references “On-Device AI / ফসলের ছবি আপলোড করুন” and “৫০ মিলি-সেকেন্ডে”. Upload widget not exercised. | **Partial (content present, not executed)** | Evidence that upload exists; behavior unverified. |
| **S3: CONFIRM (text/photo mismatch)** | Rice photo + “potato late blight” → Crop Mismatch badge, no chemical advice. | Screencast page explicitly describes “Text-Image Contradiction Gating” showing “লাল সতর্কবার্তা ব্যাজ”. | **Partial (documented, not executed)** | Strong textual evidence; live behavior unverified. |
| **S4: REFER (paraquat)** | T0 halts before retrieval; 16123 referral. | Screencast page: “নিষিদ্ধ বিষাক্ত উপাদান (যেমন প্যাারা কোয়াট) … সরাসরি সরকারি কৃষি কল সেন্টারে (16123) রেফারেল.” | **Partial (documented, not executed)** | Referral pathway described; live button not pressed. |
| **S5: DROP (dosage verifier)** | Unsupported dosage claim dropped; answer with provenance + Why panel. | Screencast page: “C3: Grounded Advisory & Dosage Verification … অনিরাপদ বা অতিরিক্ত মাত্রার রাসায়নিক প্রেসক্রিপশন প্রদর্শন আটকে নিরাপদ ডোজ সুরক্ষা.” | **Partial (documented, not executed)** | Verification claim visible; live DROP not triggered. |
| **Provenance badge** | Exactly one badge per response. | Not observed live. | **Not Executed** | — |
| **Why panel** | Verification trace visible. | Not observed live. | **Not Executed** | — |
| **Evidence display / citations** | Numbered citations in answers. | Not observed live. | **Not Executed** | — |
| **Delivery modes (SMS/offline/read-aloud)** | Accessible from UI. | No visible SMS/offline controls on the landing or chat pages; screencast mentions them. | **Fail (not discoverable)** | A reviewer cannot find delivery-mode controls. This is a **P1** demo gap. |

---

## Phase 3 — Realistic Input Variation

I could not execute these inputs through the live UI. The following reflects what the paper and repository claim, plus what I could inspect in the static content.

| Input type | Example (not submitted) | Claimed/expected behavior | Observed evidence | Verdict |
|------------|------------------------|---------------------------|-------------------|---------|
| **Colloquial Bengali, missing crop** | “Patay holud dag hoyeche, ki bish dibo?” | T1 halt → ASK with chips. | Screencast: “C1: Pre-Retrieval Halt on Empty Crop … ইন্টারঅ্যাকটিভ কুইক-রিপ্লাই চিপস”. | Documented, not executed |
| **Banglish, safe query** | “alu gache kalo daag poreche ki korbo” | Passes T0; processed normally. | Repository lists `safe_agri` category; Banglish red-team table shows 0/15 false alarms. | Claimed; not executed |
| **Ambiguous crop (text)** | “leaf disease, what to spray?” | Should halt (no resolvable crop) or enter disambiguation. | Repository describes `low_confidence` terminal category. | Documented, not executed |
| **Text/image conflict** | Rice photo + potato text | CONFIRM badge; no chemical advice. | Screencast describes this exactly. | Documented, not executed |
| **Safety-related request** | “how to spray paraquat” | REFER to 16123. | Screencast describes T0 referral. | Documented, not executed |
| **Ordinary safe farmer query** | “when to irrigate wheat?” | Grounded answer with citations. | Screencast shows C3 grounded advisory. | Documented, not executed |

**Phase 3 conclusion:** The system’s *documented* behavior covers all these categories, but I could not independently confirm live responses. A reviewer at the conference will likely try at least one of these; the demo must be robust.

---

## Phase 4 — Reviewer Accessibility (Non-Bengali Reader)

The live demo is **almost entirely in Bengali**. A non-Bengali-speaking reviewer lands on a page whose visible headings, body text, buttons, and placeholders are in Bengali, with only occasional English terms (e.g., “AI”, “On-Device”, “Task-First Decisions”) embedded. The chat page placeholder is in Bengali: “আপনার কৃষি প্রশ্ন লিখুন (বাংলায়)…”.

**Can the reviewer determine what happened?**  
- The **screencast page** is the primary accessible artifact: it is bilingual in places and explicitly labels stages in English (T0, C1, C2, C3, Text-Image Contradiction Gating, Constrained Delivery). This is the reviewer’s lifeline.
- The **live chat UI** itself does not appear to have a language toggle visible on the static content. The repository mentions “দ্বিভাষিক সহায়তা” (bilingual assistance) on the chat page, but the default view is Bengali.
- The **provenance badges** and **Why panel** would need to be understood; if they are Bengali-only, the reviewer may not know why an answer was blocked or dropped.

**Can they understand the evidence/provenance interface?**  
Not without translation. The paper describes provenance badges (Fact lookup, Grounded generation, Guidance card, Clarification, Referral) and a Why panel, but if the UI renders these labels only in Bengali, the reviewer will not be able to interpret them.

**Recommendation:** Add a visible **English toggle** or at minimum an **English legend** on the demo site that explains each state (ASK, CONFIRM, REFER, DROP), the provenance badge meanings, and what the Why panel shows. This is a **P0** accessibility issue for EACL reviewers.

---

## Phase 5 — Reliability

I checked the live site’s reachable pages and links via static inspection.

| Check | Result | Classification |
|-------|--------|----------------|
| Initial landing page loads | Yes; Bengali content renders. | Pass |
| `/chat` loads | Yes; textarea and disabled submit button present. | Pass |
| `/screencast` loads | Yes; provides textual walkthrough. | Pass |
| Broken links on landing page | No obvious broken links among visible navigation items. | Pass |
| Authentication prompt | None observed. | Pass |
| Refresh behavior | Not tested (static inspection). | Environmental limit |
| Upload widget | Referenced on landing page (“ফসলের ছবি আপলোড করুন”) but not exercised. | Not tested |
| Textarea input | Present but submit button disabled in static snapshot; likely enables on input. | Not tested |
| API endpoints | Repository documents `POST /api/qa/stream`, `POST /api/classify`, `POST /api/detect`, `GET /api/safety/metrics`. | Documented; not called |
| SSE streaming | Documented as transport. | Not tested |
| Stale UI states | Not tested. | Environmental limit |
| Error handling | Not tested. | Environmental limit |

**System bug vs environmental limitation:** I cannot label anything a “system bug” without live interaction. The only clear gap is **discoverability of delivery modes** (SMS/offline/read-aloud), which are mentioned in the paper and screencast but do not appear as visible controls on the chat or landing pages.

---

## Phase 6 — Paper ↔ Website Consistency

| Paper claim | Website / repo observation | Consistency |
|-------------|----------------------------|-------------|
| Five control stages T0–T4; four states ASK/CONFIRM/REFER/DROP | Screencast page mirrors T0, C1, C2, C3 and the four outcomes. | **Consistent** |
| On-device vision, WASM INT8, ~50 ms | Landing page: “৫০ মিলি-সেকেন্ডে”; screencast: “Edge WASM INT8 Perception”. | **Consistent** |
| Crop set: rice, potato, brassica, chili, corn, wheat | Landing page references “আলু (Potato — ডায়মন্ট)” and “ধান” (rice). No obvious mention of brassica/chili/corn/wheat on landing, but repository lists six crops. | **Consistent (repo supports)** |
| BM25 over BARI/BRRI/DAE | Repo confirms BM25Okapi + FAISS dense; paper says BM25 only in deployed demo. | **Slight tension:** repo describes *hybrid* (BM25 + FAISS), paper’s evaluation says “BM25 only; dense retrieval not evaluated.” The demo may use hybrid, while paper reports BM25-only numbers. This is acceptable if disclosed, but a reviewer may ask which is live. |
| Model: `krishokchat-4b` (Gemma3 4.3B Q4_K_M, llama-server) | Repo mentions “fine-tuned LLM” and local Ollama. No contradiction. | **Consistent** |
| Cloud benchmark: `gemini-2.5-flash-lite` | Not visible in UI (benchmark-only). | **Not observable** |
| SMS packer, offline card, read-aloud | Screencast mentions them; no visible UI controls on live pages. | **Partial / not discoverable** |
| Banglish 85/85 interception, 0/15 false alarms | Screencast mentions Banglish handling; no live test harness visible. | **Documented, not verifiable live** |
| Dosage verifier live 114/118, scaled 296/350 | Screencast describes C3 verification; no live counter. | **Documented, not verifiable live** |
| 200 authentic farmer queries, κ=1.00 | Not visible in UI. | **Paper-only** |
| API: `/api/qa/stream`, `/api/classify`, `/api/detect` | Repo documents them; live endpoints not called. | **Consistent (documented)** |
| Dataset/model availability links | Paper gives HuggingFace links; I did not verify them. | **Not checked** |

**Notable discrepancy:** The repository describes a **hybrid** retrieval system (BM25 + FAISS dense), while the paper’s evaluation section repeatedly states retrieval is “lexical (BM25)” and that “dense retrieval was not evaluated.” This is not necessarily a contradiction—the demo may use hybrid while the paper reports a BM25-only evaluation—but the paper should make clear which configuration the *live demo* actually serves. A skeptical reviewer will ask.

---

# Final Reviewer Report

## 1. First-Impression Report
The live demo is a credible, purpose-built Bengali agricultural advisory interface. It loads reliably and signals the right things: “নিরাপদ ও প্রমাণভিত্তিক বাংলা কৃষি এআই” (safe and evidence-based Bengali agricultural AI), on-device disease detection, and 16123 call-centre linkage. The screencast page is the strongest reviewer-facing artifact because it maps the system’s stages to English labels and explicit timestamps.

**However, for a non-Bengali EACL reviewer, the live UI is a wall of Bengali.** There is no visible language toggle, no English legend for the four states, and no on-screen explanation of what ASK/CONFIRM/REFER/DROP mean. The reviewer will rely heavily on the paper and the screencast text, not the live system itself.

## 2. Core-Demo Report
I could not drive the S1–S5 workflow live. Based on the paper, the screencast page, and the repository, the core demo *should* work as described. The screencast page explicitly walks through T0 referral, C1 crop-less halt with quick-reply chips, C2 edge vision + crop fencing, text–image contradiction gating, C3 dosage verification, and constrained SMS/offline delivery. The repository documents the supporting API endpoints.

**The critical demo gap is discoverability.** A reviewer landing on the site cannot easily find:
- the delivery-mode controls (SMS, offline card, read-aloud),
- a language toggle,
- an explanation of the provenance badge taxonomy,
- a live “Why panel” example.

## 3. Feature Test Matrix (Condensed)

| Feature | Status | Notes |
|---------|--------|-------|
| Landing page loads | Pass | Bengali UI, links to chat/screencast work. |
| Chat page loads | Pass | Textarea present; submit disabled until input. |
| Screencast page | Pass | Excellent textual walkthrough with English stage labels. |
| S1 ASK | Not executed | Documented in paper + screencast. |
| S1 crop binding | Not executed | Documented. |
| S2 photo scoping | Partial | Upload widget referenced; not exercised. |
| S3 CONFIRM badge | Partial | Described in screencast; not exercised. |
| S4 REFER 16123 | Partial | Described; not exercised. |
| S5 DROP verifier | Partial | Described; not exercised. |
| Provenance badge | Not executed | Not observed live. |
| Why panel | Not executed | Not observed live. |
| Evidence citations | Not executed | Not observed live. |
| SMS/offline/read-aloud | Fail (not discoverable) | No visible controls. |
| Banglish safety | Documented | No live test harness. |
| DialectSelector | Not observed | No visible selector. |

## 4. Reviewer Confusion Points
- **Language barrier:** The entire operational UI is Bengali. A reviewer cannot tell what the system is doing without the paper.
- **State vocabulary:** “ASK”, “CONFIRM”, “REFER”, “DROP” are paper terms; the live UI may use different Bengali labels. The reviewer needs a mapping.
- **Provenance badges:** The paper lists five badge types; the reviewer cannot see them live or know what they mean.
- **Delivery modes:** The paper claims web, SMS, offline card, and read-aloud; only web is visible.
- **Hybrid vs BM25-only:** The repo says hybrid; the paper says BM25-only in evaluation. Which is live?

## 5. Broken / Partial Behavior
- **Not a bug but a gap:** No language toggle or English legend.
- **Not a bug but a gap:** Delivery-mode controls not discoverable.
- **Potential inconsistency:** Hybrid retrieval in repo vs BM25-only in paper.
- **Unverified:** All safety, verifier, and red-team claims are paper/repo-only; no live demonstration harness is exposed to the reviewer.

## 6. Paper–Website Inconsistencies (Summary)
- Repo: hybrid retrieval (BM25 + FAISS) vs Paper: “BM25 only; dense retrieval not evaluated.”
- Paper: “rendered as web, SMS, offline card, or read-aloud” vs Website: only web visible.
- Paper: five provenance badges vs Website: badges not observed live.
- Paper: six crops vs Landing page: explicit mention of potato and rice only.

## 7. P0 Fixes (Must fix before demo session)
1. **Add a visible English toggle** to the live demo, or at minimum an **English legend panel** on every page explaining the four states and badge meanings.
2. **Make delivery-mode controls discoverable** — expose SMS preview, offline card, and read-aloud from the delivered answer view.
3. **Clarify the live retrieval configuration** — state in the demo and paper whether the live demo uses BM25-only or hybrid retrieval.

## 8. P1 Fixes (Strongly recommended)
4. **Expose a live “Why panel” example** on the demo site so reviewers can see the verification trace without triggering it themselves.
5. **Add a small “How to test this demo” card** on the landing page with 3–4 clickable example queries (including one safety query and one conflict query).
6. **Surface the provenance badge** visibly on every answer; ensure its Bengali label has an English tooltip.
7. **Add an English caption to the screencast page** (it is already partially English; complete the bilingual labeling).

## 9. Things That Are Fine and Should NOT Be Touched
- The **screencast page structure** — its stage-by-stage English/Bengali mapping is the best reviewer aid on the site.
- The **deterministic-first framing** — it is the paper’s strongest conceptual contribution and is well articulated.
- The **16123 referral pathway** — clear, safety-oriented, and easy to understand from the screencast.
- The **on-device vision claim** — well supported by the repository’s verification artifacts.
- The **paper’s limitations ledger** — unusually thorough and honest about residual risks.

---

## Final Question: “If I encountered this system through the paper and demo link, what would I understand KrishokTech to actually demonstrate?”

I would understand KrishokTech to demonstrate **a safety-bounded decision pipeline for Bengali agricultural advice**, where the core novelty is not the language model but the *boundaries* placed around it: a deterministic gate that stops unsafe or underspecified queries before retrieval, crop-fenced retrieval that prevents off-target evidence from reaching generation, a multimodal conflict state that refuses to silently choose between text and image, and a dosage verifier that drops unsupported numerical claims before rendering. The paper’s evaluation—particularly the gate’s 30/30 halt rate, the fence’s 36.25%→28.75% reduction in wrong-crop advice, the attack-success-rate drop from 36.19% to 0.95% on the cloud model, and the dosage verifier’s 114/118 live catch rate—convincingly argues that these controls reduce specific, high-consequence failure modes.

What I would **not** fully understand from the live demo alone is **how to operate or interpret the system without reading Bengali**. The live site demonstrates that a polished Bengali advisory interface exists, but it does not demonstrate to an English-speaking reviewer *what is happening internally* at each step. The screencast text bridges this gap partially, but the live demo should do more to make its decision states and safety boundaries legible to a non-Bengali reviewer.