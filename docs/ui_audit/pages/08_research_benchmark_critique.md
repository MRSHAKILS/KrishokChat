# Page Critique: Evaluation Benchmark (`/research/benchmark`)

**Target Route**: `/research/benchmark`  
**Source Code**: [frontend/src/app/(marketing)/research/benchmark/page.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/research/benchmark/page.tsx)  
**Screenshot**: ![08_research_benchmark.png](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/screenshots/08_research_benchmark.png)  

---

## 📸 Visual Overview & Impression
`/research/benchmark` presents precomputed evaluation metrics comparing BM25, Dense Retrieval, Hybrid RRF, ColBERT, and fine-tuned Gemma-4 4-bit across multiple agricultural QA tasks.

---

## 🔍 Detailed Analysis & Critique

### 1. Table Legibility & Mobile Responsiveness
- **Horizontal Overflow**: On mobile screens (375px), large metric tables containing R@1, R@5, R@10, MRR, and MAP overflow horizontally without visible scroll indicators.
- **Fix**: Wrap table in an overflow container with subtle shadow gradients indicating scrollable columns.

### 2. Metric Legend & Highlighted Best Scores
- **Visual Polish**: Highlight the top-performing model row (Hybrid RRF / Gemma-4 4-bit) with a soft leaf green highlight background (`bg-leaf/10`) and a ⭐ **সেরা ফলাফল (Best Result)** badge.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Highlight best model score rows in metric tables with green badges.
- [ ] Fix horizontal overflow for mobile table views.
