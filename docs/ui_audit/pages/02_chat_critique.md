# Page Critique: KrishokChat Assistant (`/chat`)

**Target Route**: `/chat`  
**Source Code**: [frontend/src/app/(app)/chat/page.tsx](file:///d:/KrishokChat%20Advisory%20System/frontend/src/app/%28app%29/chat/page.tsx) & [frontend/src/components/qa-panel.tsx](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/qa-panel.tsx)  
**Screenshot**: ![02_chat.png](file:///d:/KrishokChat%20Advisory%20System/docs/ui_audit/screenshots/02_chat.png)  

---

## 📸 Visual Overview & Impression
`/chat` is the primary conversational interface of the application. It features real-time streaming, suggested agricultural questions, safety guardrail trace indicators, grounded source citation pills, and model selection.

---

## 🔍 Detailed Analysis & Critique

### 1. Model Selector Confusion ([qa-panel.tsx:L193-L221](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/qa-panel.tsx#L193-L221))
- **Technical Model Names**: Buttons show `Gemini 2.5 Flash-Lite (অনলাইন)` and `KrishokChat-4B (লোকাল নেই)`.
- **UX Issue**: Rural farmers do not care about underlying model IDs like "4B" or "Flash-Lite". When `KrishokChat-4B` is unavailable, disabled text (`text-ink-faint/60`) creates visual clutter without explaining why.
- **Fix**: Simplify labels to "সাধারণ এআই" (Standard AI) and "গবেষণা এআই" (Research AI). Add a subtle tooltip or help modal explaining the difference.

### 2. Suggested Questions Chips ([qa-panel.tsx:L309-L314](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/qa-panel.tsx#L309-L314))
- **Positive Feature**: Suggested questions ("ধানের মাজরা পোকা দমনে কী করব?", "আলুর ব্লাইট রোগের চিকিৎসা") provide great starting points.
- **UX Improvement**: Group suggestions into visual category tabs with icons: 🌾 **ধান (Rice)**, 🥔 **আলু (Potato)**, 🍅 **টমেটো (Tomato)**, 🧪 **কীটনাশক নিয়ম (Safety)**.

### 3. Voice Input & Mobile Keyboard Usability ([qa-panel.tsx:L225-L255](file:///d:/KrishokChat%20Advisory%20System/frontend/src/components/qa-panel.tsx#L225-L255))
- **Lack of Voice Mic**: The text input box only has a text field and a `Send` icon. Farmers using phones outdoors in sunlight prefer voice recording.
- **Fix**: Insert a mic button inside the text bar (`<Mic className="h-5 w-5 text-leaf" />`) to support speech-to-text or audio prompt demo fallback.

### 4. Safety Guardrail Trace Visuals
- When a query is checked, showing `safe_agri` or classification categories in English technical tags confuses non-technical users.
- **Fix**: Translate system internal states into friendly Bengali indicators:
  - `safe_agri` → 🟢 **কৃষি বিষয়ক প্রশ্ন (অনুমোদিত)**
  - `banned_or_restricted_chemical` → 🔴 **নিষিদ্ধ কীটনাশক সতর্কতা**
  - `self_harm_or_poisoning_risk` → ⚠️ **জরুরি স্বাস্থ্য সহায়তা (১৬১২৩)**

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add a Voice Input (Mic) button inside the chat text bar.
- [ ] Translate safety pipeline classification tags from English code names into clear Bengali badges with status colors.
- [ ] Categorize empty-state suggested questions into crop tabs (Rice, Potato, Tomato, Agrochemicals).
- [ ] Rename technical model options to intuitive user-facing terms.
