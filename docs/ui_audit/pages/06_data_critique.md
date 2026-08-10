# Page Critique: Datasets & Research Data (`/data`)

**Target Route**: `/data`  
**Source Code**: [frontend/src/app/(marketing)/data/page.tsx](file:///d:/KrishokChat%20Advisory%20System/frontend/src/app/%28marketing%29/data/page.tsx)  
**Screenshot**: ![06_data.png](file:///d:/KrishokChat%20Advisory%20System/docs/ui_audit/screenshots/06_data.png)  

---

## 📸 Visual Overview & Impression
`/data` outlines the underlying dataset statistics, knowledge graph node counts, official government publications, and multi-track benchmarks.

---

## 🔍 Detailed Analysis & Critique

### 1. Code Duplication with `/research/benchmark` and Home Page
- **Redundancy**: The pie chart displaying the 4 evaluation tracks (General QA, Table QA, Safety QA, Treatment QA) and dataset metrics are duplicated verbatim from the Home Page (`/`) and `/research/benchmark`.
- **Fix**: Replace static duplication with an interactive dataset explorer where users can filter nodes by crop (Rice, Potato, Tomato) or publication agency (DAE, BARC, BARI).

### 2. Missing Navigation Link
- **Navbar Bug**: `/data` is omitted from the top header navigation menu. Evaluators must scroll to the footer to access dataset information.
- **Fix**: Add "উপাত্ত" (`/data`) under a dedicated menu item or resources drop-down in `navbar.tsx`.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add `/data` to main header menu.
- [ ] Replace duplicated static pie charts with a dynamic knowledge node search tool.
- [ ] Add download / preview buttons for dataset sample schemas.
