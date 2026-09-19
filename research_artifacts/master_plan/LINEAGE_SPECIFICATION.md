# KrishokTech Master Knowledge & Dataset Lineage Specification

**Venue Target:** Wiley *Expert Systems* (ISSN: 1468-0394)  
**Document Status:** Frozen Architectural Reference  
**Purpose:** Unambiguously define and deconflict all data, document, node, and tuple layers across the KrishokTech research ecosystem.

---

## 1. Six-Layer Knowledge Lineage Architecture

To ensure total scientific clarity during peer review, every number and resource reference in the manuscript must map to exactly one layer in the following hierarchy:

```
[Layer 1] Official Agricultural Publications (284 manuals / circulars)
    │
    ▼
[Layer 2] Curated Agronomic Source Documents (750+ section chapters)
    │
    ▼
[Layer 3] Hierarchical Knowledge Retrieval Nodes (2,882 nodes / 290 core BARI)
    │
    ▼
[Layer 4] Extracted Evidence Spans (Character-offset text passages)
    │
    ▼
[Layer 5] Typed Relational Claim Tuples (ClaimSafe-BN 11-slot schema)
    │
    ▼
[Layer 6] Runtime Advisory & Provenance Receipts (Certified / Refused actions)
```

---

## 2. Formal Layer Definitions

### Layer 1: Official Agricultural Publications
* **Definition:** Physical and digital government-authorized agricultural manuals, pest management circulars, variety release bulletins, and crop calendars published by national institutes.
* **Authoritative Institutions:**
  1. **BARI:** Bangladesh Agricultural Research Institute, Gazipur (*Handbook on Agricultural Technologies*, Plant Pathology guides).
  2. **BRRI:** Bangladesh Rice Research Institute, Joydebpur (*Adhunik Dhaner Chash*).
  3. **DAE:** Department of Agricultural Extension, Ministry of Agriculture (*Pesticide Technical Bulletin*, *Fall Armyworm Management Guidelines*).
* **Total Volume:** **284 official publications** (covering 129 core production manuals and 155 specialized pesticide/disease bulletins).

### Layer 2: Curated Source Documents
* **Definition:** Digitized, OCR-cleaned, and sectioned markdown documents organized by crop, growth stage, pest taxonomy, and soil category.
* **Scope:** Covers Potato, Rice, Maize, Wheat, Brinjal, Jute, Mustard, and Lentil production in Bangladesh agro-ecological zones (AEZs).

### Layer 3: Hierarchical Knowledge Retrieval Nodes
* **Definition:** The discrete passage units indexed for dense (FAISS), sparse (BM25), and hybrid semantic retrieval.
* **Corpus Breakdown:**
  - **Full AgriTrust Retrieval Corpus:** **2,882 knowledge nodes** (used in the comprehensive retrieval diagnosis study).
  - **Core BARI Cereal/Horticultural Subset:** **290 foundational nodes** (used in initial instruction-tuning benchmarks).
  - **Current Production Corpus:** **2,135 active verified knowledge nodes** loaded into the single-process backend RAG index.

### Layer 4: Extracted Evidence Spans
* **Definition:** Exact text snippets bounded by character offsets `[start_char, end_char]` within a knowledge node that substantiate an agronomic claim.
* **Provenance Requirement:** Every evidence span is bound to an immutable `source_node_id`, `publication_year`, `institution_code`, and cryptographic SHA-256 digest.

### Layer 5: Typed Relational Claim Tuples (`ClaimSafe-BN`)
* **Definition:** Structured mathematical objects formalizing agricultural chemical advice across 11 typed slots:
  $$\mathcal{C} = \langle c, p, s, a, f, d_{\min}, d_{\max}, u, v, \tau, \phi, \rho \rangle$$
  - $c \in \mathcal{V}_{\text{crop}}$: Host crop variety.
  - $p \in \mathcal{V}_{\text{pathogen}}$: Target pathogen / insect pest.
  - $s \in \mathcal{V}_{\text{stage}}$: Crop growth stage (e.g., seedling, vegetative, tuberization).
  - $a \in \mathcal{V}_{\text{active}}$: Chemical active ingredient.
  - $f \in \mathcal{V}_{\text{form}}$: Formulation type (e.g., 80 WP, 50 WDG, 45 SC).
  - $[d_{\min}, d_{\max}] \subset \mathbb{R}^+$: Permissible dosage concentration bounds.
  - $u \in \{\text{g}, \text{ml}, \text{kg}\}$: Measurement unit.
  - $v \in \mathbb{R}^+$: Solvent denominator volume (standardized to 1\,L water).
  - $\tau \in \mathbb{N}^+$: Application interval in days.
  - $\phi \in \mathbb{N}^+$: Pre-harvest interval (PHI) in days.
  - $\rho \in \{+1, -1\}$: Regulatory polarity (+1 = approved, -1 = banned/restricted).

### Layer 6: Runtime Advisory Records & Provenance Receipts
* **Definition:** System outputs delivered to smallholder farmers or extension agents, classified into one of three certified states:
  $$\text{Action} \in \{\text{CERTIFY}, \text{ABSTAIN}, \text{ESCALATE}\}$$
  Accompanied by a verifiable provenance badge containing evidence spans, matched slot values, and the active resolution tier (T0–T4).

---

## 3. Cross-Paper Dataset Mapping Table

| Resource Identifier | Lineage Origin | Scope & Size | Function in v2 Manuscript |
|---|---|---|---|
| **KrishokTech-SFT-145K** | Paper 1 (Resource) | 145,500 QA pairs | Contextualizes limitations of pure instruction tuning. |
| **Farmer-1001 Benchmark** | Paper 1 (Resource) | 1,001 authentic farmer queries | Evaluates ecological validity under real-world colloquial language. |
| **AgriTrust Retrieval Corpus** | Paper 2 (Retrieval) | 2,882 nodes (284 publications) | Frozen retrieval environment for hybrid/dense retrieval tests. |
| **ClaimSafe-BN (v2)** | Paper 3 (This Work) | 20,112 curated queries (60/20/20) | Primary benchmark for selective risk, calibration, and dialect testing. |
| **Relational Misbinding Attack Suite** | Paper 3 (This Work) | 10,000+ programmatic attacks | Adversarial stress test for relational binding verification. |
| **Golden CI Invariant Suite** | Paper 3 (This Work) | 542 unit + 50 golden cases | Verifies 100% fail-closed runtime invariance in continuous integration. |
