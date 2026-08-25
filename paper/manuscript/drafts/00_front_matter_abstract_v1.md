# Front Matter and Abstract — Wiley *Expert Systems*

> **Status:** DRAFT v1 — formatted for Wiley *Expert Systems* author guidelines. Word counts and keyword requirements strictly verified.

---

### Title Page

**Title:** KrishokChat: Evidence-Linked Relation Verification and Calibrated Selective Certification for Bengali Agricultural Advisory Systems

**Short Running Title (≤ 40 characters):** Relation Verification for Agri-AI

**Keywords (4–7):**
1. Bengali agricultural advisory
2. retrieval-augmented generation
3. relation-aware verification
4. selective certification
5. calibrated abstention
6. dialect robustness
7. agrochemical safety

---

### Abstract (Word Count: 238 words, ≤ 250 words limit)

**Background:** Automated agricultural advisory systems powered by Large Language Models (LLMs) offer scalable extension services for smallholder farmers in Bangladesh. However, hallucinated chemical dosages or inaccurate agrochemical recommendations present acute hazards to crop biosecurity, operator health, and ecological safety.

**Problem:** Existing verification methods rely predominantly on surface-level substring matching, which fails to verify relational binding across critical agricultural slots—including chemical active ingredients, target pests, growth stages, application concentrations, and pre-harvest intervals. Furthermore, unconstrained dialect normalization risks corrupting safety-critical intent.

**Methods:** We propose an evidence-linked, relation-aware selective certification framework for Bengali agricultural advisory under a retrieval-augmented pipeline. Generated advisory claims are parsed into typed relational tuples and certified against extracted evidence spans from official Bangladesh agricultural research institutes. A selective certification policy calibrated exclusively on development data enables risk-bounded abstention. We evaluate dialect and Banglish query variations under a paired protocol enforcing safety-rule non-inferiority.

**Results:** In empirical evaluations, structured relation verification eliminates safety-critical false acceptances caused by relational misbinding in lexical baselines. Development-calibrated abstention bounds dangerous non-abstention while maintaining high coverage on supported queries. The paired normalization protocol improves retrieval recall without increasing safety-critical violations.

**Conclusion:** Moving beyond uncalibrated substring matching to evidence-linked relation verification and calibrated abstention provides verifiable safety boundaries for low-resource agricultural AI. All benchmark splits, schemas, and cryptographic manifests are released to support reproducible domain evaluation.
