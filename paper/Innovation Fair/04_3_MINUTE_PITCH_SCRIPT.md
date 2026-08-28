# Bangladesh Innovation Fair 2026 — 3-Minute Live Pitch Script

**Presenter:** Lead Researcher & Engineer  
**Allocated Time:** 3 Minutes (180 Seconds) + 2 Minutes Q&A  
**Target Audience:** National Innovation Fair Judges, Ministry of Agriculture Representatives, Agribusiness Executives, Investors  
**Live Demo Prop:** Laptop connected to projector + Smartphone running KrishokChat PWA (simulating mobile / offline mode)

---

### Timing & Stage Cue Breakdown

| Time Elapsed | Slide # | Presentation Segment | Key Demo Action / Screen Cue |
|:---:|:---:|---|---|
| **0:00 – 0:25** | **Slide 1** | Field Origin & The Smallholder Reality | Show field photo; hold up smartphone with leaf photo |
| **0:25 – 0:50** | **Slide 2 & 3** | Why Generic AI Fails & Our Research Foundation | Show failure comparison: Hallucination vs. Evidence |
| **0:50 – 1:30** | **Slide 4** | The 5-Tier Architecture & LIVE DEMO | **Live 1-Click Demo:** (1) Late Blight Query $\rightarrow$ (2) Banned Chemical Test |
| **1:30 – 2:05** | **Slide 5** | Empirical Breakthroughs & Agronomist Review | Highlight **97.0% Accuracy** & **0.0% Hazard** stats |
| **2:05 – 2:35** | **Slide 6 & 7** | Scale, Business Model & SDG Impact | Present B2G / B2B institutional sustainability model |
| **2:35 – 3:00** | **Slide 8** | The Ask & Vision for Bangladesh | Invite judges to scan QR code & test live |

---

### Verbatim Presentation Script (English / Bilingual Delivery)

#### [0:00 – 0:25] Slide 1: Field Origin
*"Honorable judges, distinguished guests, and fellow innovators.*

*In Bangladesh, over 16 million farming families make critical agronomic decisions every day with incomplete information, limited access to extension officers, and intermittent mobile connectivity. When a potato farmer in Bogura sees black spots spreading across his crop, guessing the wrong chemical or applying an overdose doesn't just destroy his harvest—it ruins his family's livelihood.*

*We didn't start KrishokChat by asking 'How do we wrap an LLM around agriculture?' We started in the field, asking: **'How can technology become genuinely useful, safe, and accountable for a farmer?'**"*

---

#### [0:25 – 0:50] Slide 2 & 3: The Gap & Research Foundation
*"Current AI approaches fail in agriculture for three reasons: generic LLMs hallucinate toxic chemical dosages; standard RAG collapses under regional dialects; and computer vision apps diagnose diseases but cannot provide holistic, weather-safe treatment plans.*

*Before writing production code, we conducted rigorous research: building the first citation-grounded Bengali agricultural knowledge graph over 2,946 institutional documents from DAE, BARI, and BRRI. We learned how AI breaks under farmer language, and engineered our entire system around those failure modes."*

---

#### [0:50 – 1:30] Slide 4: Architecture & Live Demonstration
*(Presenter transitions smoothly to live screen on projector)*

*"KrishokChat is a coordinated 5-Tier Agricultural Intelligence Platform:*

1. **Watch this live query:** *'আলুর নাবি ধসায় কী দেব?'*  
   *(Presenter clicks or speaks query)*  
   *Within **3.8 milliseconds**, our deterministic Tier 1 Fact-Base resolves the exact authorized active ingredient—Mancozeb 80WP at 2 grams per liter—grounded directly in DAE manual page 852, with zero LLM latency and zero cloud cost.*

2. **Now watch our Fail-Closed Safety Gate:** *'ধানের মাজরা পোকা দমনে প্যারাকোয়াট কীভাবে দিব?'*  
   *(Presenter clicks Safety Challenge button)*  
   *Because Paraquat is a banned hazardous chemical in Bangladesh, our Tier 0 gate intercepts the prompt in under **0.1 milliseconds**, refuses the hazardous advice, and provides an instant one-click referral to the National Krishi Call Center **16123**.*

*Our core rule is immutable: **No evidence $\rightarrow$ No unsafe advice.**"*

---

#### [1:30 – 2:05] Slide 5: Empirical Proof
*"This is not a mock-up. It is verified across 36 empirical experimental layers:*
* In an independent double-blind benchmark evaluated by certified agricultural extension officers, KrishokChat achieved **97.0% certified advisory correctness** with **0.0% critical unsafe acceptance**, compared to 38% for standard baseline LLMs.
* In 11,000 metamorphic corruption tests, our relational schema rejected 100% of dosage tamper mutations.
* And on rural 2G edge networks with 30% packet loss, our offline-first PWA caching maintains **89% advisory availability** when cloud-only apps drop to 67%."*

---

#### [2:05 – 2:35] Slide 6 & 7: Market Sustainability & Impact
*"How do we scale sustainably?  
Farmers use KrishokChat for free via Web, offline PWA, and zero-cost SMS.  
We monetize through **Institutional B2G and B2B partnerships**:
* Serving as an intelligent digital copilot for Bangladesh's 14,000+ Department of Agricultural Extension (DAE) field officers.
* Providing certified agronomic APIs and private knowledge packs for agribusinesses and NGOs.
* Driving national SDG 2 (Zero Hunger), SDG 12 (Responsible Chemical Consumption), and reducing pesticide poisoning nationwide."*

---

#### [2:35 – 3:00] Slide 8: The Ask & Call to Action
*"The technology has been built. The 559 backend test suite is green. The empirical science is validated.  
What we need now is support to transition from controlled laboratory validation into multi-district field deployment with 1,000+ farmers across Northern Bangladesh.

Join us in building the digital brain for Bangladesh's agriculture. Please scan the QR code to test KrishokChat live right now. Thank you!"*

---

### Anticipated Judge Questions & Bulletproof Answers

**Q1: "How do you ensure farmers don't get poisoned if the AI makes a mistake?"**  
*Answer:* *"We use a 2-layer defense: First, our Tier 0 gate hard-blocks all banned and restricted chemicals deterministically before the LLM is ever called. Second, our Tier 4 Relational Verifier checks generated dosages against authorized DAE upper/lower bounds. If a claim isn't 100% entailed in our institutional source, the system refuses to certify it and routes to 16123."*

**Q2: "What if a farmer has no internet in a remote char or haor area?"**  
*Answer:* *"Our frontend is an offline-first PWA with Service Worker caching. The top 50 crop disease solutions (Tier 1/2 Fact-Base) are stored locally on the phone's browser storage. For basic non-smartphones, our backend includes an SMS compression engine that transmits verified treatments in a single 160-character text."*

**Q3: "Why not just use ChatGPT or Gemini directly?"**  
*Answer:* *"Generic LLMs lack Bangladesh-specific regulatory grounding, fail under regional dialects by up to 48%, hallucinate unapproved chemical mixtures in 15–36% of cases, and cost $1.00+ per 1k queries. KrishokChat resolves 61.5% of queries locally at $0.00 cost with 0.0% chemical hazard."*
