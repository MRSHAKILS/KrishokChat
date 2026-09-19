# Page Critique: System Analytics & Safety Audit Dashboard (`/analytics`)

**Target Route**: `/analytics`  
**Source Code**: [frontend/src/app/(app)/analytics/page.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28app%29/analytics/page.tsx)  
**Screenshot**: ![04_analytics.png](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/screenshots/04_analytics.png)  

---

## 📸 Visual Overview & Impression
The Analytics page acts as the safety metrics and live audit trail dashboard. It displays query safety category breakdowns, average response latency, grounded document retrieval distribution, and recent audit logs.

---

## 🔍 Detailed Analysis & Critique

### 1. Navigation Visibility Bug
- **Bug**: `/analytics` is completely missing from the global navbar ([navbar.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/components/navbar.tsx)). Evaluators examining the headline safety feature have no direct header link to access this dashboard.
- **Fix**: Add `/analytics` ("পরিসংখ্যান") to the desktop navigation header.

### 2. Audit Trail Log Table Presentation
- **Raw JSON / String Overflows**: Safety classification categories are displayed as raw strings (`banned_or_restricted_chemical`, `self_harm_or_poisoning_risk`, `prompt_injection`).
- **Fix**: Replace raw JSON strings with color-coded status badges:
  - `banned_or_restricted_chemical` → 🛡️ **নিষিদ্ধ রাসায়নিক (আটককৃত)** [Red Badge]
  - `self_harm_or_poisoning_risk` → 🚨 **জরুরি স্বাস্থ্য রিস্ক (১৬১২৩)** [Orange Badge]
  - `safe_agri` → ✅ **অনুমোদিত কৃষি প্রশ্ন** [Green Badge]

### 3. Metric Cards Hierarchy
- Key metric numbers (e.g. Total Queries Analyzed, Safety Interventions, Average Retrieval Time) are rendered in small text boxes.
- **Fix**: Enlarge top metric numbers with high-contrast tabular figures (`font-display text-3xl tabular text-leaf`) and add clear trend icons.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add `/analytics` link to global `Navbar`.
- [ ] Replace raw backend enum strings in audit log table with readable Bengali badges.
- [ ] Format numbers with Bengali digits or clean tabular figures.
- [ ] Add a visual export/filter bar for auditing logs by date and safety status.
