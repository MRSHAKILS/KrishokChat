# Page Critique: Crop Disease Advisory Workflow (`/detect`)

**Target Route**: `/detect`  
**Source Code**: [frontend/src/app/(app)/detect/page.tsx](file:///d:/KrishokTech%20Advisory%20System/frontend/src/app/%28app%29/detect/page.tsx)  
**Screenshot**: ![03_detect.png](file:///d:/KrishokTech%20Advisory%20System/docs/ui_audit/screenshots/03_detect.png)  

---

## 📸 Visual Overview & Impression
`/detect` is the cornerstone feature of the application. It provides a dual-column layout: image upload & classification on the left, and context-aware chat on the right.

---

## 🔍 Detailed Analysis & Critique

### 1. Artifact Reality Alignment & Detection Bounding Boxes
- **Crucial Rule Compliance**: The checked-in vision models are verified as `task: classify`. The UI correctly refrains from drawing fake bounding boxes on uploaded images.
- **Visual Enhancement Needed**: When a crop disease is diagnosed (e.g. Potato Late Blight), display a clear **Confidence Badge** (e.g. `৯৪.২% নিশ্চিত`) and a crop-specific warning pill (e.g. 🥔 **আলু পাতা ধসা রোগ**).

### 2. Sample Demo Images for Quick Testing
- **Current Friction**: First-time users or demo evaluators opening `/detect` must find and upload a local leaf image manually.
- **Fix**: Add a **"পরীক্ষা করার জন্য নমুনা ছবি পছন্দ করুন" (Try Sample Leaf Photos)** strip right below the upload zone with 3 pre-loaded sample images:
  1. 🥔 potato_late_blight.jpg
  2. 🌾 rice_blast.jpg
  3. 🍅 tomato_leaf_curl.jpg

### 3. Split Screen Mobile Layout
- **Mobile Usability**: On small mobile devices (375px width), the stacked view places the full image intake, pipeline rail, diagnosis card, treatment advice, AND full chat window vertically. This requires excessive scrolling.
- **Fix**: On mobile (`sm:` and smaller), implement a top **Tab Toggle**: `[ 📷 রোগ নির্ণয় ]` vs `[ 💬 পরামর্শ চ্যাট ]` with a notification dot indicating when context transfers from diagnosis to chat.

### 4. Treatment Dosage & Chemical Safety Callouts
- Treatment cards often specify pesticide quantities (e.g., "প্রতি লিটার পানিতে ২ গ্রাম ম্যানকোজেব").
- **Safety Requirement**: Add a prominent warning banner on dosage cards: ⚠️ **কীটনাশক ব্যবহারের পূর্বে স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন অথবা ১৬১২৩ নম্বরে কল করুন।**

---

## 🛠️ Actionable UI Engineer Fix Checklist
- [ ] Add 3 quick-click sample crop leaf images to `IntakeZone` for instant demo testing.
- [ ] Implement mobile tab switcher (`[📷 রোগ নির্ণয়]` vs `[💬 পরামর্শ]`) to prevent infinite vertical scrolling on mobile.
- [ ] Add explicit pesticide dosage safety disclaimer linking to Krishi Helpline (16123).
- [ ] Show Bengali confidence percentages with color-coded badges (Green >85%, Yellow 60-85%, Red <60%).
