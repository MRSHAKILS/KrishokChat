# Page Critique: Home Landing Page (`/`)

**Target Route**: `/`  
**Source Code**: [frontend/src/app/(marketing)/page.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/page.tsx)  
**Screenshot**: ![01_home.png](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/screenshots/01_home.png)  

---

## 📸 Visual Overview & Impression
The landing page establishes an academic yet green agricultural aesthetic. However, for a Bangladeshi farmer, the page leans heavily toward academic metrics (R@10, Hybrid RRF, Knowledge Nodes) right near the hero section, before demonstrating basic visual crop advice or practical field utility.

---

## 🔍 Detailed Analysis & Critique

### 1. Hero Section ([page.tsx:L60-L87](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/page.tsx#L60-L87))
- **Hero Image Fallback**: In line 82, `<img src="/assets/hero_image.jpg" ... />` attempts to load an image. If the image asset fails or loads slowly on 3G rural mobile networks, the right column renders as an empty grey box (`bg-paper-2`).
- **CTA Labeling**: "শুরু করুন" (Start) leads to `/detect` while "প্রশ্ন করুন" (Ask Question) leads to `/chat`. For low-literacy farmers, visual icons (e.g. a camera badge for `/detect` and a voice bubble badge for `/chat`) are missing from CTAs.

### 2. Visual Stats & Academic Jargon ([page.tsx:L90-L148](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/page.tsx#L90-L148))
- **Untranslated Jargon**: The chart labels show "Hybrid RRF", "BM25", "Dense", "ColBERT", "R@10". A farmer visiting the site will find these terms incomprehensible.
- **Fix**: Move technical benchmark charts to `/research/benchmark`. Replace this section on the home page with visual success stories, sample crop disease photos, or a step-by-step pictorial guide.

### 3. Animated RAG Pipeline Demo ([page.tsx:L150-L261](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/page.tsx#L150-L261))
- **Raw Code IDs Exposed**: In line 235, raw document IDs like `DAE_PEST_1206A0_001` and `score: 33.23` are shown to the user.
- **Fix**: Replace raw IDs with human titles like "কৃষি সম্প্রসারণ অধিদপ্তর — বালাই ব্যবস্থাপনা গাইডলাইন (অধ্যায় ৪)".

### 4. Weather & Helpline Sections ([page.tsx:L342-L414](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/page.tsx#L342-L414))
- **Manual District Typing**: Farmers have to manually type district names (e.g., "রাজশাহী").
- **Fix**: Add quick clickable chip buttons for major agricultural districts: `[রাজশাহী]` `[রংপুর]` `[যশোর]` `[দিনাজপুর]` `[ময়মনসিংহ]`.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add camera and mic icons to Hero primary CTA buttons.
- [ ] Hide raw database document IDs (`DAE_PEST_...`) in RAG interactive demo; show human document names.
- [ ] Replace untranslated English chart terms with farmer-friendly labels or move academic charts to `/research`.
- [ ] Add quick district selector chips to the Weather Widget.
