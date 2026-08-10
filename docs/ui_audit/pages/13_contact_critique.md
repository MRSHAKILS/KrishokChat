# Page Critique: Contact & Emergency Helplines (`/contact`)

**Target Route**: `/contact`  
**Source Code**: [frontend/src/app/(marketing)/contact/page.tsx](file:///d:/KrishokChat%20Advisory%20System/frontend/src/app/%28marketing%29/contact/page.tsx)  
**Screenshot**: ![13_contact.png](file:///d:/KrishokChat%20Advisory%20System/docs/ui_audit/screenshots/13_contact.png)  

---

## 📸 Visual Overview & Impression
`/contact` handles emergency contacts, feedback submissions, and direct phone dial triggers.

---

## 🔍 Detailed Analysis & Critique

### 1. Direct Phone Dial Buttons
- **Touch Target**: Ensure telephone link buttons (`tel:16123`) are large, full-width touch cards (`h-14`) with phone icon animations for easy one-tap calling on mobile.

### 2. Missing Navigation Link
- **Navbar Bug**: `/contact` is missing from the global header.
- **Fix**: Add `/contact` to `navbar.tsx`.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add `/contact` link to global navbar.
- [ ] Enlarge phone dial buttons for emergency helplines.
