# KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory
## EACL 2026 System Demonstrations — Paper Outline & Screenshot Inventory

### 1. Paper Overview & Structural Budget
- **Target Venue:** EACL 2026 System Demonstrations Track
- **Page Limit:** 6 pages of content + unlimited references & appendix
- **Core Premise:** Agricultural advisory must not treat large language models as unconstrained decision-makers. KrishokTech employs a deterministic-first, evidence-bounded pipeline that halts underspecified queries pre-retrieval, enforces crop-fenced retrieval, highlights multimodal contradictions, verifies dosage claims, and provides multi-channel constrained delivery.

---

### 2. Section Breakdown & Page Allocation

| Page | Section | Core Content & Demonstration Focus | Primary Figures / Tables |
|---|---|---|---|
| **p. 1** | **§1. Introduction** | Agricultural context in Bangladesh (DAE, 85% smallholders, 1:900-2,000 ratio), the linguistic gap in rural Bengali (colloquial vs standard), risk of LLM hallucinations in crop chemical dosage. Core contributions (deterministic pre-retrieval gate, PRISM-RAG, multimodal fence, fail-closed verifier). | **Fig. 1**: Complete system architecture and decision flow |
| **p. 2** | **§2. System Architecture** | 5-tier decision ladder: T0 deterministic safety check (0.32 ms), T1 slot extractor & pre-retrieval gate (halts crop-less queries), T2 crop-fenced PRISM-RAG retrieval, T3 untrusted generation, T4 fail-closed dosage verifier & provenance badges. Constrained delivery channels (Web, 160-char SMS, offline PWA, 16123 helpline). | **Tab. 1**: Honesty matrix comparing KrishokTech against Farmer.Chat, KrishokBondhu, Krishi Sathi, My Climate CoPilot |
| **p. 3** | **§3. Demonstration & User Interaction** | Detailed walkthrough of farmer-facing interface and 6 demonstration scenarios: (S1) Incomplete crop-less treatment query, (S2) Multimodal on-device leaf scoping, (S3) Cross-modal contradiction handling, (S4) Evidence conflict resolution, (S5) Grounded advisory with provenance badges, (S6) Multi-channel delivery (SMS, TTS, Offline, 16123). | **Fig. 2**: Main application interface overview<br>**Fig. 3**: Interactive clarification intercept & resumed retrieval |
| **p. 4** | **§3. Demonstration (cont.) & §4. Empirical Evaluation** | Completion of demo scenarios (S4-S6) and quantitative evaluation of decision boundaries: Pre-retrieval gate operating point (76/200 halted, 0 sources retrieved, 89-token median clarification vs 2,146 retrieval tokens). | **Fig. 4**: Multimodal consistency & mismatch badge<br>**Fig. 5**: Grounded answer & constrained delivery channels |
| **p. 5** | **§4. Empirical Evaluation (cont.)** | Crop-fence upper-bound simulation ($n=400$, wrong-crop advice drops 36.25% → 30.00%, McNemar $p=5.96\times 10^{-8}$), text-image mismatch accuracy (453/454), live safety guard evaluation (attack success 0.95% vs 36.19%), dosage mutation detection (114/118), SMS length enforcement (399/400 $\le 160$ chars). | **Fig. 6**: Pre-retrieval gate evaluation<br>**Fig. 7**: Crop-fence simulation<br>**Fig. 8**: Safety verification & delivery metrics |
| **p. 6** | **§5. Related Work & §6. Limitations & Conclusion** | Positioning against conversational agricultural assistants, retrieval over low-resource language variation, multimodal QA, and fail-closed safety. Explicit 18-point limitations disclosure (single-reviewer annotations, gold routing upper bound, residual attacks). Conclusion on constraint-first design. | **Tab. 2**: Operational capabilities matrix |
| **p. 7+** | **References & Appendix** | Bibliography, formal prompt templates, ONNX asset manifests, artifact SHA-256 hashes, full failure trace taxonomy. | Appendix flowcharts & verification tables |

---

### 3. Screenshot Inventory & Figure Composites Mapping

All screenshots are captured from the active running system (`http://localhost:3000` & `http://localhost:8000`) at native 2x DPI with zero watermarks, debug borders, or artificial mockups.

Directory: `paper/EACL Final/paper/screenshots/`

#### Individual Screenshots:
1. `fig2_main_interface.png` (283 KB)
   - **Description:** Complete, clean overview of the KrishokTech chat workspace showing the colloquial Bengali input field, voice input toggle, message timeline, and response provenance card.
2. `screenshot1_halt_clarification.png` (288 KB)
   - **Description:** Pre-retrieval halt on an underspecified treatment query (*"পাতায় হলুদ দাগ হয়েছে, কি বিষ দিবো?"*). The system retrieves 0 sources and presents interactive quick-reply chips: `[ ধান (Rice) ]`, `[ আলু (Potato) ]`, `[ টমেটো (Tomato) ]`, etc.
3. `screenshot2_resumed_retrieval.png` (377 KB)
   - **Description:** Resumed scoped retrieval after the farmer clicks `[ আলু (Potato) ]`. The crop slot is bound in session working memory, triggering scoped BARI Late Blight retrieval and grounded advisory generation with provenance badges.
4. `screenshot3_photo_crop_scope.png` (520 KB)
   - **Description:** Visual specimen scoping on `/detect`. The on-device ONNX vision model classifies the leaf image (Rice leaf) and binds the crop context to the advisory pipeline.
5. `screenshot4_mismatch_badge.png` (569 KB)
   - **Description:** Cross-modal mismatch warning badge triggered when the farmer's textual query (*"আলুর নাবি ধসা রোগ দমনে কী বিষ দিবো?"*) contradicts the leaf image (*Rice*). Chemical advisory is held until the user confirms the intended crop.
6. `screenshot5_grounded_answer.png` (337 KB)
   - **Description:** Grounded Bengali response with institutional source citations (BARI/BRRI), dosage verifier clearance, and sentence-level provenance badges.
7. `screenshot7_16123_safety_referral.png` (403 KB)
   - **Description:** Terminal fail-closed safety refusal on a banned chemical query (Paraquat), routing immediately to the national agricultural helpline (16123) with a *Deterministic Guard* badge.
8. `screenshot8_offline_mode.png` (427 KB)
   - **Description:** Offline hybrid fallback state showing local BM25 cached retrieval, offline indicator pill, and service-worker precached guidance.
9. `screenshot9_sms_tts.png` (427 KB)
   - **Description:** Multi-channel delivery showing 160-character SMS packing and Bengali neural voice read-aloud (`bn-BD-NabanitaNeural`) with synchronized text highlighting.

#### Publication-Ready Merged Composites:
1. `fig3_demo_halt.png` (2560x2646, 1.2 MB)
   - **Paper Figure:** Figure 3 (Interactive Clarification Intercept & Resumed Retrieval)
   - **Composition:** Vertical composite merging `screenshot1_halt_clarification.png` (top) and `screenshot2_resumed_retrieval.png` (bottom) with academic subfigure headers (a/b) and a connecting transition indicator (*"Farmer clicks quick-reply chip: [ আলু (Potato) ] — Session slot filled"*).
2. `fig4_demo_multimodal.png` (2560x2526, 1.7 MB)
   - **Paper Figure:** Figure 4 (Multimodal Verification & Cross-Modal Conflict Resolution)
   - **Composition:** Stacked composite of `screenshot3_photo_crop_scope.png` (visual specimen scoping) and `screenshot4_mismatch_badge.png` (cross-modal contradiction warning badge) with subfigure headers (a/b).
3. `fig5_demo_delivery.png` (2460x1856, 1.8 MB)
   - **Paper Figure:** Figure 5 (Grounded Advisory & Constrained Delivery Channels)
   - **Composition:** 2x2 grid composite featuring:
     - *(a) Grounded Bangla Advice with Provenance* (`screenshot5_grounded_answer.png`)
     - *(b) Fail-Closed Safety Referral (16123)* (`screenshot7_16123_safety_referral.png`)
     - *(c) Offline Hybrid Fallback Mode* (`screenshot8_offline_mode.png`)
     - *(d) SMS & Voice TTS Delivery Channels* (`screenshot9_sms_tts.png`)
