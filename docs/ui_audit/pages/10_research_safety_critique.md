# Page Critique: Safety-Aware Guardrails (`/research/safety`)

**Target Route**: `/research/safety`  
**Source Code**: [frontend/src/app/(marketing)/research/safety/page.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/research/safety/page.tsx)  
**Screenshot**: ![10_research_safety.png](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/screenshots/10_research_safety.png)  

---

## 📸 Visual Overview & Impression
`/research/safety` is a key poster feature demonstrating the 4-agent safety architecture, safety classification taxonomy, and direct redirection to the Bangladesh government **Krishi Call Center (16123)**.

---

## 🔍 Detailed Analysis & Critique

### 1. 16123 Helpline Callout Card
- **Positive Feature**: Prominently highlights the 16123 national helpline for banned chemicals or self-harm/poisoning risks.
- **Visual Enhancement**: Make the **16123 Call Card** fixed or highlighted with a pulsing ring animation to draw immediate attention.

### 2. Taxonomy Category Examples
- **Banned Chemical Taxonomy**: List specific prohibited pesticides in Bangladesh (e.g. অ্যালড্রিন, ডিলড্রিন, এন্ড্রিন, এন্ডোসালফান) so evaluators see authentic context.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add pulsing animation ring to 16123 Helpline action card.
- [ ] Include real banned pesticide examples in Bangladesh context.
