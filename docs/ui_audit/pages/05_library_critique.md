# Page Critique: Advisory Knowledge Library (`/library`)

**Target Route**: `/library`  
**Source Code**: [frontend/src/app/(marketing)/library/page.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28marketing%29/library/page.tsx)  
**Screenshot**: ![05_library.png](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/screenshots/05_library.png)  

---

## 📸 Visual Overview & Impression
The Library page presents the curated knowledge base compiled from government agricultural manuals, crop disease handbooks, and seasonal guidelines.

---

## 🔍 Detailed Analysis & Critique

### 1. Card Grid Layout & Visual Hierarchy
- **Text-Heavy Grid**: Crop cards and disease guide cards contain dense text paragraphs without imagery or visual icons for quick identification.
- **Fix**: Add recognizable crop icons or high-quality illustration thumbnails (e.g. Rice stalk icon for Rice guides, Potato tuber icon for Potato guides).

### 2. Search & Filtering Controls
- **Search Experience**: The search input placeholder says `অনুসন্ধান করুন...`.
- **Improvement**: Provide quick filter buttons by crop category: `[ধান]` `[আলু]` `[গম]` `[টমেটো]` `[বেগুন]` `[পোকামাকড় দমন]`.

### 3. Document Source Attribution
- **Source Badges**: Many library cards cite sources like `DAE Manual Vol 3` or `BRRI Tech Bulletin`.
- **Bangla Translation Quality**: Translate publication sources into full Bengali names: **কৃষি সম্প্রসারণ অধিদপ্তর (DAE)** and **বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI)**.

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add crop category filter chips (Rice, Potato, Wheat, Tomato, Eggplant).
- [ ] Incorporate crop icons / visual thumbnails into knowledge cards.
- [ ] Expand abbreviated agency acronyms into full Bengali titles.
