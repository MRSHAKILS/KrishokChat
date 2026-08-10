# Page Critique: Research Overview (`/research`)

**Target Route**: `/research`  
**Source Code**: [frontend/src/app/(marketing)/research/page.tsx](file:///d:/KrishokChat%20Advisory%20System/frontend/src/app/%28marketing%29/research/page.tsx)  
**Screenshot**: ![07_research.png](file:///d:/KrishokChat%20Advisory%20System/docs/ui_audit/screenshots/07_research.png)  

---

## 📸 Visual Overview & Impression
The Research Overview page acts as the academic hub summarizing the research motivation, key contributions, benchmark publications, and sub-pages (`/research/benchmark`, `/research/methodology`, `/research/safety`).

---

## 🔍 Detailed Analysis & Critique

### 1. Navigation Sub-Tabs
- **Usability Concern**: Users browsing `/research` must manually find links to `/research/benchmark`, `/research/methodology`, and `/research/safety`.
- **Fix**: Add a sticky sub-navigation tab bar at the top of all `/research/*` sub-pages:
  `[ 📘 Overview ]` `[ 🔬 Methodology ]` `[ 📊 Benchmark ]` `[ 🛡️ Safety Pipeline ]`

### 2. Publication Citations & Download Links
- **Paper Preprints**: Research publications cite EACL and SIGIR-AP papers.
- **Visual Polish**: Add clean PDF download pills and BibTeX copy buttons for evaluators and researchers.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add sub-navigation sticky tab bar across all research sub-routes (`/research/*`).
- [ ] Add one-click BibTeX copy buttons and paper PDF badges.
