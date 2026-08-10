# Global Design System & Cross-Cutting UI/UX Critique

**Project**: KrishokChat — Bangladesh Agri-AI Advisory System  
**Scope**: Site-wide layout, navigation, typography, accessibility, and theme tokens  

---

## 1. Global Navigation & Auth Confusion (`navbar.tsx`)

### 🔴 Critical Issues
- **Unnecessary Auth Buttons**: [navbar.tsx:L66-L79](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/navbar.tsx#L66-L79) renders "প্রবেশ" (Login) and "নিবন্ধন" (Register) buttons on desktop, leading to `/auth`. Project directive explicitly states: *No authentication, no user accounts*. Having auth buttons misleads users into thinking account creation is required before using the AI advisory service.
- **Missing Top Navigation Links**: Pages like `/analytics`, `/data`, and `/contact` are present in the app router but missing from the desktop navbar `NAV` array in [navbar.tsx:L11-L18](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/navbar.tsx#L11-L18). Users are forced to scroll down to the footer to locate these pages.
- **Hidden Emergency Call Helpline**: The national **Krishi Call Center helpline (16123)** is currently hidden inside the mobile dropdown menu ([navbar.tsx:L136-L142](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/navbar.tsx#L136-L142)) and absent from the desktop header.

### 💡 Recommendation for `navbar.tsx`
1. Remove "প্রবেশ" and "নিবন্ধন" buttons completely.
2. Add `/analytics`, `/data`, `/contact` to the main navigation menu or a clean "সম্পদ" (Resources) dropdown menu.
3. Replace the auth buttons in the header with a prominent, high-contrast, clickable **"১৬১২৩ কল করুন"** (Call 16123) action pill with a phone icon.

---

## 2. Bangla Typography & Accessibility

### ⚠️ Contrast & Outdoor Readability
- Many body texts and captions use `text-ink-faint` or `text-ink-soft` on muted backgrounds like `bg-paper-2/30` or `bg-bone`. In direct Bangladeshi sunlight (where farmers inspect field problems on low-brightness smartphones), light grey Bengali text becomes illegible.
- **Fix**: Boost contrast by updating `text-ink-soft` to `#2d3748` (dark charcoal) and `text-ink-faint` to `#4a5568`.

### 🔤 Font & Letter Spacing (Kerning)
- Tailwind class `tracking-[0.18em]` and `tracking-[0.22em]` is applied to uppercase text across several components. While this looks modern for Latin fonts, applying tracking to Bengali script creates broken joint letters (যুক্তাক্ষর).
- **Fix**: Remove character tracking CSS (`tracking-*`) from all Bengali text nodes. Use dedicated Bengali fonts such as **Noto Serif Bengali** or **Hind Siliguri** for optimal legibility.

---

## 3. Component Duplication & Redundant Metrics

### 🔄 Identical Data Cards across 3 Pages
- Benchmark statistics, track distribution pie charts, and retrieval R@10 bar charts are copy-pasted verbatim between:
  1. `/` (Home Landing Page)
  2. `/data` (Datasets & Research Data)
  3. `/research/benchmark` (Evaluation Benchmark)
- **Fix**: Extract chart implementations into a single reusable component suite under `frontend/src/components/charts/` (e.g. `TrackDistributionChart.tsx`, `RetrievalBenchmarkChart.tsx`).

---

## 4. Farmer UX & Voice Accessibility

- **Keyboard-only Input Limitation**: Low-literacy farmers find typing complex agricultural Bengali terms (e.g., "প্লাজমোডিফোরা ব্র্যাসিকি") difficult.
- **Recommendation**: Add a prominent Voice Input (মাইক্রোফোন) button next to text input boxes on `/chat` and `/detect`. Even if simulated for the 7-day demo, a visual mic button elevates farmer accessibility.
