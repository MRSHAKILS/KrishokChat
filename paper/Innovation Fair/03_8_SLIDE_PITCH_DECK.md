# Bangladesh Innovation Fair 2026 — 8-Slide Pitch Deck Specification

**Project Title:** KrishokChat — Bengali Agricultural Intelligence for Farmers, Extension and Rural Communities  
**Format:** 16:9 Widescreen Presentation (PPTX / Marp / Web Slides)  
**Tone:** Field-Grounded, Rigorous, Authoritative, National Impact, Responsible AI  
**Palette:** Deep Agricultural Green (`#1E5E3A`), Warm Earth (`#B87333`), Charcoal Ink (`#2C241E`), Clean White (`#FFFFFF`)

---

## SLIDE 1: FIELD ORIGIN

### Layout & Visuals
* **Left 55%:** Real documentary photograph of a Bangladeshi smallholder farmer inspecting potato/rice leaves with a smartphone in a rural field setting.
* **Right 45%:** Three stacked problem discovery cards on a soft parchment background.
* **Bottom:** Full-width anchor statement.

### Slide Content
* **Header / Eyebrow:** THE STARTING POINT
* **Headline:** We started with farmers, not with a model.
* **Core Cards:**
  1. **FIELD REALITY:** Agricultural decisions in Bangladesh are made under incomplete information, fluctuating weather, and severe time pressure.
  2. **LANGUAGE GAP:** Farmers speak in regional dialects, colloquial terms, and mixed Banglish—not standardized textbook queries.
  3. **ACCESS & CONNECTIVITY:** Expert extension officers are scarce (1:1,500 farmer ratio), and rural broadband is intermittent.
* **Anchor Statement:** *"The question was not 'How do we add AI to agriculture?' It was 'How can technology become genuinely useful and safe for a farmer?'"*

---

## SLIDE 2: THE ADVISORY GAP & FAILURE MODES

### Layout & Visuals
* **Structure:** 3-Way Problem Evolution Diagram on Left $\rightarrow$ Single Integrated Solution on Right.
* **Visual Style:** Minimalist high-contrast card comparison with clean iconography.

### Slide Content
* **Header / Eyebrow:** THE ROOT PROBLEM
* **Headline:** The problem is not a lack of AI. It is a lack of accountable agricultural AI.
* **Comparison Columns:**
  * **Generic LLMs:** Fluent & conversational, but hallucinates chemical dosages, invents unapproved pesticides, and lacks Bangladesh regulatory grounding.
  * **Vanilla RAG:** Better text retrieval, but breaks under dialect variations, cannot handle multimodal conflict, and misbinds chemical attributes.
  * **Vision-Only Tools:** Classifies leaf disease, but cannot provide holistic IPM guidance, weather-aware timing, or safe dosage calculations.
* **The Breakthrough (Right Card):**
  * **KrishokChat:** **Language + Vision + Evidence + Safety + Rural Delivery** in one unified fail-closed architecture.
* **Footer:** *Our published research analyzed these exact failure modes before designing the platform architecture.*

---

## SLIDE 3: RESEARCH-TO-PRODUCT TIMELINE

### Layout & Visuals
* **Structure:** Horizontal 5-Stage Innovation Pipeline from Field Observation to System Deployment.
* **Accent:** Highlight "Research findings became engineering decisions".

### Slide Content
* **Header / Eyebrow:** SCIENTIFIC FOUNDATION
* **Headline:** We learned from failure before we built the product.
* **Horizontal Pipeline:**
  ```
  [1. Field Discovery] ──► [2. Benchmark Corpus] ──► [3. Failure Analysis] ──► [4. Five-Tier Engine] ──► [5. Production Deployment]
    Farmer interviews        2,946 DAE/BARI docs       Dialect & hallucination    Deterministic + RAG      PWA, SMS & Extension APIs
  ```
* **Three Key Milestones:**
  * **01 — Knowledge Foundation:** Built the first citation-grounded Bengali agricultural knowledge graph with 2,882 nodes and 11-slot contracts.
  * **02 — Retrieval Research:** Measured and quantified the register-gap: farmer dialect drops standard dense retrieval recall by up to 48%.
  * **03 — Safety Redesign:** Replaced unconstrained generation with a 5-Tier Resolution Ladder and relational dosage verification.
* **Key Takeaway:** **Research findings directly shaped production architecture.**

---

## SLIDE 4: THE SYSTEM ARCHITECTURE

### Layout & Visuals
* **Structure:** Clean multi-agent architectural flow diagram showing the 5-Tier Resolution Ladder and fail-closed pathways.
* **Hero Badge:** *"No Evidence $\rightarrow$ No Unsafe Advice"*

### Slide Content
* **Header / Eyebrow:** MULTI-AGENT ADVISORY PIPELINE
* **Headline:** One advisory system, built around the farmer's real workflow.
* **Interactive Architecture Flow:**
  * **Input Layer:** Multi-dialect Bengali Text, Voice Audio, Crop Photos.
  * **Tier 0 — Deterministic Safety Gate:** Intercepts banned agrochemicals, crisis emergencies, and jailbreaks in **<0.1 ms** $\rightarrow$ Instant **16123** referral.
  * **Tier 1 & 2 — Structured Fact-Base:** Resolves verified pathology facts deterministically in **3.8 ms** at **$0.00 cost**.
  * **Tier 3 — Hybrid RAG & Gemma-4:** Multi-source dense+sparse retrieval over 2,946 institutional documents.
  * **Tier 4 — Relational Verifier:** Schema enforcement over 11 critical agronomic slots (dose bounds, safety gear, pre-harvest interval).
  * **Delivery Channels:** Web PWA, Local Offline Cache, SMS Compression Engine.
* **Core Principle:** **KrishokChat is not a chatbot wrapper. It is an accountable agricultural intelligence engine.**

---

## SLIDE 5: EMPIRICAL PROOF & BENCHMARKS

### Layout & Visuals
* **Top Grid:** 4 Massive Hero Stat Callouts.
* **Bottom Grid:** Supporting empirical validation metrics from 36 completed experimental layers.

### Slide Content
* **Header / Eyebrow:** RIGOROUS VALIDATION
* **Headline:** This is already far more than a prototype.
* **Hero Numbers:**
  * **2,946** Institutional Manuals Indexed (DAE, BARI, BRRI, BARC)
  * **97.0%** Certified Advisory Correctness (vs. 58–74% baseline LLMs)
  * **0.0%** Observed Critical Unsafe Acceptance (100% fail-closed safety)
  * **708×** Latency Speedup via Fact-Base (3.8 ms vs. 2,971 ms cloud generation)
* **Supporting Verification Grid:**
  * **11,000 / 11,000** Metamorphic Corruption Mutations Rejected (100.0% accuracy)
  * **0 / 1,400** Adversarial Jailbreak & Injection Attacks Accepted
  * **200 Cases** Double-Blind Evaluated by Certified Agronomists (4.82 / 5.0 Quality, 96.5% Approval)
  * **559 / 559** Backend Tests Passed • **50/50** Golden Replay Invariants Green

---

## SLIDE 6: ECOSYSTEM IMPACT & COMMERCIAL SCALE

### Layout & Visuals
* **Structure:** 3-Pillar Stakeholder Ecosystem (Farmers, Institutions, Agribusiness).
* **Flow:** Farmer Beneficiary $\rightarrow$ KrishokChat Platform $\rightarrow$ Institutional Partners $\rightarrow$ Sustainable Revenue.

### Slide Content
* **Header / Eyebrow:** SUSTAINABLE VALUE CREATION
* **Headline:** Built for farmers. Scalable through institutions.
* **Three-Pillar Scale Model:**
  * **For Farmers (Free / Direct Access):** Natural Bengali interaction, instant disease photo diagnosis, offline PWA access, zero-cost SMS advice.
  * **For Extension Services & NGOs (B2G / NGO Partner):** Copilot for 14,000+ Sub-Assistant Agriculture Officers (SAAOs), case escalation management, regional disease outbreak surveillance.
  * **For Agribusiness & Telecom (B2B API & Enterprise):** Certified agronomic API access, custom private knowledge packs, compliant agrochemical advisory integration.
* **Commercialization Philosophy:** *"The farmer is the primary beneficiary; institutions and enterprise provide the sustainable path to scale."*

---

## SLIDE 7: RESPONSIBILITY, INCLUSION & SDG ALIGNMENT

### Layout & Visuals
* **Structure:** 4 Clean Quadrants mapping Technology $\rightarrow$ Social & Environmental Impact $\rightarrow$ UN Sustainable Development Goals.

### Slide Content
* **Header / Eyebrow:** ETHICAL & RESPONSIBLE AI
* **Headline:** Useful AI must also be responsible AI.
* **Four Impact Dimensions:**
  * **Safety & Poisoning Prevention:** Hard fail-closed guards prevent pesticide poisoning and misuse; automated routing to National Call Center **16123** and **999**.
  * **Linguistic & Digital Inclusion:** Equal accuracy across 5 regional dialects and Banglish; offline caching bridges the rural 2G/3G connectivity gap.
  * **Environmental IPM & Soil Health:** Integrated Pest Management (IPM) prioritized first, driving a **77.1% reduction in unnecessary chemical usage**.
  * **Global & National SDG Alignment:**
    * **SDG 2 (Zero Hunger):** Increasing smallholder crop productivity and reducing disease loss.
    * **SDG 9 (Industry & Innovation):** Indigenous AI research deployed for national digital infrastructure.
    * **SDG 12 (Responsible Consumption):** Preventing chemical runoff and pesticide overdose.
    * **SDG 13 (Climate Action):** Weather-adaptive irrigation and disease risk early warnings.

---

## SLIDE 8: THE ROADMAP & THE ASK

### Layout & Visuals
* **Structure:** Two-Column Comparison (Current Accomplishment vs. Next Milestone) + Prominent Live QR Code and Links.

### Slide Content
* **Header / Eyebrow:** DEPLOYMENT ROADMAP
* **Headline:** The technology exists. The next step is field deployment.
* **Two Column Matrix:**
  * **What We Have Built (Today):**
    * Full-stack operational platform (Next.js + FastAPI)
    * 5-Tier safety and resolution pipeline
    * 2,946-document institutional knowledge index
    * Verified 97.0% accuracy across 36 empirical experiments
    * Full open test suite and live web demonstration
  * **What Support & Funding Unlocks (Next 6–12 Months):**
    * Multi-district field pilot with 1,000+ active farmers in Bogura & Rangpur
    * Co-deployment pilot with DAE / SAAO extension officers
    * Expansion of on-device INT8 models for rice, corn, and wheat
    * Real-time soil sensor & satellite weather API integration
* **Call to Action:** *"Support the transition from a scientifically validated AI system to a national agricultural service."*
* **Access Links:**
  * **Live Demo:** `https://krishokchat.vercel.app` (or local demo URL)
  * **Research Dossier & Code:** GitHub / KrishokChat Repository
