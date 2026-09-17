# Figure Generation Prompts (CEA manuscript)

All figures below require external image generation. For each, paste the prompt into
your image-generation tool (GPT-4o image generation / DALL-E 3 / Midjourney). The
manuscript already references `figures/fig1_architecture.png`; save generated images
into `manuscript/figures/` with the names below and recompile.

---

## FIGURE 1 — KrishokChat Neurosymbolic Advisory Architecture (referenced in Section 4)

**File:** `figures/fig1_architecture.png`
**Style:** clean academic system-architecture diagram, flat vector style, white
background, blue/green accent palette, no photorealism, no text gibberish — all labels
must be spelled exactly as given.

**Prompt:**
"Create a professional academic system-architecture diagram titled 'KrishokChat Neurosymbolic
Advisory Architecture'. Vertical flow from top to bottom. Top box: 'Farmer Query
(text / image / voice)'. Below it a box labeled 'Tier 0: Risk & Context Gate'
(deterministic policy: safe_agri, banned chemical, self-harm, off-topic, prompt
injection, low_confidence) with a side arrow labeled 'terminal classes -> canned safe
response / Krishi 16123'. Next box 'Tier 1: Capability & Perception Router' with a side
note 'crop classification metadata; register normalization (standard / dialect /
Banglish)'. Next box 'Tier 2: Structured Fact Authority — SQLite fact store (2,135
provenance nodes, 11-slot records, SHA-256 hashed)' with a branch arrow labeled
'deterministic resolve -> CERTIFY (no LLM)'. Next box 'Tier 3: Grounded Generative
Realization (LLM constrained to phrasing; may not mutate facts)'. Next box 'Tier 4:
Relational Verifier (11-slot single-record certification)' with three exits: 'CERTIFY ->
answer', 'CLARIFY', and 'ABSTAIN / ESCALATE -> Krishi 16123'. Add a left-side vertical
band labeled 'Audit trail: query, risk class, route, resolution tier, evidence version,
verification, latency' and a right-side band 'Offline: signed SHA-256 fact pack +
differential updates (edge/SMS)'. All labels in the prompt must appear verbatim.
```

## FIGURE 2 — Agricultural claim authority model (Section 3 / optional)

**Prompt:**
A conceptual diagram titled 'From Evidence to Certified Advisory'. Left-to-right chain:
'Source (MoA/BARI/BRRI) -> Structured Fact (typed 11-slot record, hash, version) ->
Critical Claim -> Verification (authority + currency + joint entailment) -> Certified
Answer'. Below the chain, a smaller box 'LLM = linguistic realization (may phrase, must
not alter values)' connected only to the final answer box by a thin arrow labeled
'phrasing only'. A red 'X' arrow from 'LLM' to 'Critical Claim' labeled 'no authority'.
Flat vector, white background, academic style.

---

## FIGURE 2B / SECTION 5 — Governed Knowledge Compilation & Fact Authority Pipeline

**File:** `figures/fig_governance_pipeline.png` (Source: `Governed Knowledge Compilation and Fact Authority Pipeline.png`)
**Prompt:**
"A high-resolution, clean academic vector architecture diagram titled 'KrishokChat: Governed Knowledge Compilation and Fact Authority Pipeline'. Horizontal 5-stage dataflow:
Stage 1: Accredited Institutional Corpus (2,946 Docs) — BARI, BRRI, DAE/MoA.
Stage 2: Governed Ingestion & Conflict Resolution — Staging, Semi-automated regex/rule extraction (18-25 min/profile), Double-blind expert review, Authority Precedence Rule (MoA > BARI/BRRI > Legacy > Secondary), Policy Override on superseded/banned chemicals.
Stage 3: Canonical Relational Record (Two-Layer Schema) — Layer A (11-Slot Decision Contract) + Layer B (Governance Metadata) -> Single-Record Joint Entailment.
Stage 4: Merkle-Chained Integrity & Versioning — SHA-256 Leaf Hashes to Root Hash, Ed25519 Signature + E23 Audit: 100.0% Tamper Detection, Differential Hash Deltas (791 B payload, 92.8% bandwidth reduction).
Stage 5: Governed Deployment Runtime — Signed SQLite Fact Pack (Edge / Offline WASM / Char Islands, p95 0.19 ms) -> Tier-2 Deterministic Resolver & Tier-4 Relational Verifier."

## FIGURE3 — Risk--coverage curves (Section 9)

**Prompt:** "A scientific line chart titled 'Risk--Coverage (held-out test split,
Layer E04)'. X-axis: Coverage (%), 0-100. Y-axis: Selective Risk (%), 0-16. Plot five
monotone curves labeled: 'Raw Generator Confidence' (rises steeply: at 50% coverage
6.96% risk, at 100% 16.51%), 'Lexical Overlap' (11.19% at 50%), 'LLM-Judge' (1.24% at
50%), 'Conformal Abstention' (0.05% at 50%, 7.32% at 90%), 'Calibrated Relational KrishokChat
(bold blue)' (0.0% at 50%, 0.0% at 80%, 7.21% at 90%). Mark a vertical dashed line at
84.56% coverage with an annotation 'frozen theta* = 0.2375, risk 1.26%'. Legend at
bottom-right. Academic ggplot style, white background, clean typography."

---

## FIGURE4 — Authority verification (metamorphic) summary bar chart

**Prompt:** "A grouped bar chart 'Metamorphic Rejection Rate (11,000 mutations per
system)'. X axis systems: B0 Unconstrained LLM 18.41%, B1 Lexical 36.36%, B2 Dense
37.05%, B3 Citation 57.33%, B4 LLM Judge 72.25%, B5 Partial 8-slot 63.64%, B6 11-Slot
KrishokChat 100.0%. B6 bar highlighted in green with '100%' label on top; others in gray with
confidence-interval whiskers (e.g. 18.41 [17.70, 19.14]). Academic style, white
background."

---

## FIGURE5 — Slot ablation hazard bar (Section 5)

**Prompt:** "A horizontal bar chart 'Hazard surge when a contract slot is ablated
(dangerous acceptance)'. Bars in descending order: Dosage +31.6 pp, Regulatory polarity
+17.8, Active ingredient +14.2, Host crop +11.4, Pathogen +8.2, Solvent volume +7.1,
Formulation +5.8, Unit +5.4, Stage +4.9, PHI +2.7, Interval +1.9; and a final full bar
'All typed constraints removed' = 80.0% labeled 'lexical substring collapse'. Red color
gradient, dashed line at the 0% baseline, academic style."

---

## FIGURE 6 — Deployment trade-off (latency / connectivity / LLM dependence)

**Prompt:** "A compact 2x2 panel titled 'Deployment trade-offs'. Panel A line chart:
'Advisory delivery under packet loss' — cloud-only RAG drops from 100% to 12.8% at 30%
loss; offline-first cache holds 100% -> 58.1% (legend: cloud dotted red, offline solid
green; annotation 'rural edge 91.4% vs 82.0%'). Panel B: 'Weighted mean latency' bar
chart: 1,247.93 ms vs 546.15 ms (2.28x) . Panel C: 'Zero-LLM resolution share' stacked
bar: deterministic advisory 51.04%, safety/refusal 10.48%, LLM-dependent 38.48% .
Panel D: 'SMS slot survival' grouped bars: template 100% all slots, LLM SMS ~35-64%
varies (PHI 35.6%). Academic style, white background."

---

**Notes for the researcher**
- All figures are advisory; the numbers printed in the figure should be cross-checked
  against NUMBER_BANK.md before generation.
- Figure files must be placed in `manuscript/figures/` and the driver already includes
  `\includegraphics{figures/fig1_architecture.png}` in Section 4; add the remaining
  `\begin{figure}` blocks next to the relevant results sections (Section 5 & 6 & 7) if
  you want them inline.
- If you prefer line charts drawn with matplotlib/Python, the raw data for all figures
  is in NUMBER_BANK.md / the layer results.yaml files.