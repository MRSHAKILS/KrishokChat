# KrishokTech (কৃষক চ্যাট) — Comprehensive UI/UX Audit & Action Plan

**Target Audience**: Bangladeshi Rural Farmers, Agricultural Extension Officers, and Capstone Demo Evaluators  
**Report Date**: August 2026  
**Auditor**: Senior Full-Stack & UI/UX Specialist  

---

## 📌 Executive Summary

This directory contains the exhaustive UI/UX, accessibility, visual polish, and Bangla localization critique for the **KrishokTech Bangladesh Agri-AI Advisory System**. Every page of the 15 system routes was rendered, audited via live browser execution, and analyzed with explicit focus on **Bangladeshi Farmer Usability** and **Live Investor Demo Impact**.

---

## 🗂️ Audit Directory Navigation

- [🚨 Global Design System & Cross-Cutting Bugs](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/GLOBAL_DESIGN_SYSTEM_BUGS.md)
- 📄 **Individual Page Critique Reports**:
  1. [01. Home Landing Page (`/`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/01_home_critique.md)
  2. [02. KrishokTech Assistant (`/chat`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/02_chat_critique.md)
  3. [03. Crop Disease Detection (`/detect`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/03_detect_critique.md)
  4. [04. System Analytics & Safety Audit (`/analytics`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/04_analytics_critique.md)
  5. [05. Advisory Knowledge Library (`/library`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/05_library_critique.md)
  6. [06. Datasets & Research Data (`/data`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/06_data_critique.md)
  7. [07. Research Overview (`/research`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/07_research_critique.md)
  8. [08. Evaluation Benchmark (`/research/benchmark`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/08_research_benchmark_critique.md)
  9. [09. AI Pipeline Methodology (`/research/methodology`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/10_research_methodology_critique.md)
  10. [10. Safety-Aware Guardrails (`/research/safety`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/10_research_safety_critique.md)
  11. [11. About KrishokTech (`/about`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/11_about_critique.md)
  12. [12. Research Team & Credits (`/team`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/12_team_critique.md)
  13. [13. Contact & Support (`/contact`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/13_contact_critique.md)
  14. [14. Authentication / Login (`/auth`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/14_auth_critique.md)
  15. [15. 404 Page Not Found (`/non-existent-page`)](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/pages/15_not_found_critique.md)

---

## 🎯 Priority Matrix for UI/UX Engineers

### 🔴 High Priority (P0) — Must Fix Before Investor Demo
1. **Remove Login/Registration Buttons from Global Navbar**:
   - `navbar.tsx` contains "প্রবেশ" and "নিবন্ধন" links pointing to `/auth`. The project rules strictly prohibit auth. Showing login options confuses demo viewers and farmers. Replace with a prominent, clickable **"১৬১২৩ কল করুন" (Call 16123)** Krishi Call Center button.
2. **Missing Main Navigation Links**:
   - `/analytics`, `/data`, and `/contact` are omitted from the desktop navigation header in `navbar.tsx`.
3. **Bangla Phrasing & Mixed English Terms**:
   - English technical strings like `safe_agri`, `score: 33.23`, `DAE_PEST_1206A0_001`, `Hybrid RRF`, `R@10` are visible on farmer-facing pages (`/` and `/chat`). Reframe technical codes into human-readable Bengali equivalents or relegate them to expandable developer sub-views.
4. **Voice Input Shortcut for Farmers**:
   - Rural farmers in Bangladesh frequently struggle with typing Bengali on mobile touchscreens. Add a large, visible microphone icon (Voice Input CTA) to the `/chat` input box.

### 🟡 Medium Priority (P1) — Visual Polish & Redundancy Consolidation
1. **Eliminate Duplicate Benchmark Charts**:
   - Identical datasets and charts are copied verbatim across `/`, `/data`, and `/research/benchmark`. Consolidate into reusable components with context-appropriate captions.
2. **Outdoor Sunlit Readability & Contrast**:
   - Subtle grey text (`text-ink-faint`, `text-ink-soft` on grey backgrounds `bg-paper-2/30`) fails outdoor sunlight contrast accessibility. Increase text opacity and font weight for primary body strings.
3. **Touch Target Sizing**:
   - Small button links and small input icons (under 44px) need to be padded to at least 48px to accommodate farmers with calloused hands or low-end smartphones.

### 🟢 Low Priority (P2) — Micro-Animations & Aesthetic Delights
1. **Framer Motion Step Transitions**:
   - Enhance the safety agent pipeline trace with smooth icon pulse animations when transitioning between classification steps.
2. **Interactive Weather Card**:
   - Pre-populate quick-select buttons for top agricultural districts (e.g., রাজশাহী, রংপুর, যশোর, দিনাজপুর, ময়মনসিংহ).
