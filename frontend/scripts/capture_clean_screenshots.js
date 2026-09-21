const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT_DIR = path.resolve('d:/KrishokChat Advisory System/paper/EACL Final/paper/screenshots');
if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

// Clean CSS injected on every page:
const CLEAN_CSS = `
  /* Remove all focus rings, blue halos, and active button outlines */
  *:focus, *:focus-visible, *:active {
    outline: none !important;
    box-shadow: none !important;
  }
  
  /* Suppress Next.js development overlay artifacts (black N circle, portals) */
  nextjs-portal,
  #__next-build-watcher,
  [data-nextjs-dev-tools-button],
  [data-nextjs-toast],
  next-route-announcer {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
  }

  /* Force pure sunlight high-contrast white mode */
  html {
    --color-paper: #ffffff !important;
    --color-paper-2: #f9f8f5 !important;
    background-color: #ffffff !important;
  }
  body {
    background-color: #ffffff !important;
  }
`;

const RICE_SCAN_DATA = {
  result: {
    status: "diagnosed",
    detection_mode: "classification",
    crop: "ধান (Rice)",
    crop_confidence: 0.984,
    crop_source: "model",
    disease: "বাদামী দাগ রোগ (Brown Spot)",
    disease_confidence: 0.968,
    boxes: [],
    disease_info: {
      class_name: "Brown Spot",
      description_bn: "হেলমিনথোস্পোরিয়াম ওরাইজি ছত্রাকের আক্রমণে ধানের পাতায় ডিম্বাকৃতি বাদামী দাগ সৃষ্টি হয়।",
      cause_bn: "উষ্ণ ও আর্দ্র আবহাওয়া এবং মাটিতে পটাশ সারের ঘাটতি।",
      solution_bn: "অনুমোদিত ছত্রাকনাশক স্প্রে ও সুষম পটাশ সার প্রয়োগ।"
    },
    top3_crops: [{ class: "Rice", confidence: 0.984 }],
    top3_diseases: [{ class: "Brown Spot", confidence: 0.968 }],
    treatment_advice: "ধানের বাদামী দাগ রোগ দমনে ট্রাইসাইক্লাজোল বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক অনুমোদিত মাত্রায় স্প্রে করুন।",
    treatment_confidence: "verified",
    treatment_sources: ["BRRI ধান উৎপাদন নির্দেশিকা ২০২৪"],
    verifier_flags: [],
    agent_trace: [
      { stage: "intake", status: "complete", detail: "ছবি গৃহীত" },
      { stage: "crop_classification", status: "complete", detail: "ধান (৯৮.৪%)" },
      { stage: "disease_classification", status: "complete", detail: "বাদামী দাগ (৯৬.৮%)" },
      { stage: "advisory", status: "complete", detail: "ধান-নির্দিষ্ট চিকিৎসা সমন্বিত" }
    ],
    quality_warnings: []
  },
  cropHint: "ধান",
  savedAt: Date.now()
};

async function setupPage(context) {
  const page = await context.newPage();
  
  // Force sunlight contrast in localStorage
  await page.addInitScript(() => {
    localStorage.setItem('krishokchat:contrast', 'sunlight');
    document.documentElement.setAttribute('data-contrast', 'sunlight');
  });

  page.on('load', async () => {
    try {
      await page.addStyleTag({ content: CLEAN_CSS });
      await page.evaluate(() => {
        document.documentElement.setAttribute('data-contrast', 'sunlight');
      });
    } catch (e) {}
  });

  return page;
}

async function removeBlueFocus(page) {
  await page.evaluate(() => {
    if (document.activeElement && typeof document.activeElement.blur === 'function') {
      document.activeElement.blur();
    }
  });
  await page.waitForTimeout(300);
}

async function run() {
  console.log('Launching browser for publication-grade captures...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1366, height: 850 },
    deviceScaleFactor: 2,
  });

  // -------------------------------------------------------------
  // 1. Capture S1: ASK (Crop-less Query Halts with 6 Staple Chips)
  // -------------------------------------------------------------
  console.log('1. Capturing S1: ASK...');
  {
    const page = await setupPage(context);

    // Mock SSE response for crop-less query
    await page.route('**/api/qa/stream', async (route) => {
      const ssePayload = [
        'data: {"stage":"safety","status":"complete","detail":"নিরাপদ"}\n\n',
        'data: {"stage":"retrieval","status":"skip","detail":"ফসলের নাম অনুপস্থিত — থামানো হয়েছে"}\n\n',
        'final: ' + JSON.stringify({
          query: "পাতায় হলুদ দাগ হয়েছে, কি বিষ দিবো?",
          category: "safe_agri",
          answer: "কোন ফসলের পাতায় হলুদ দাগ হয়েছে?",
          confidence: "verified",
          sources: [],
          agent_trace: [
            { stage: "safety", status: "complete", detail: "নিরাপদ" },
            { stage: "retrieval", status: "skip", detail: "ফসলের নাম অনুপস্থিত" }
          ],
          verifier_flags: [],
          resolution_tier: "interactive_clarification"
        }) + '\n\n'
      ].join('');

      await route.fulfill({
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive'
        },
        body: ssePayload
      });
    });

    await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: CLEAN_CSS });
    await page.waitForTimeout(1000);

    const input = page.locator('textarea, input[type="text"]').first();
    await input.fill('পাতায় হলুদ দাগ হয়েছে, কি বিষ দিবো?');
    const sendBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').first();
    await sendBtn.click();

    await page.waitForSelector('button:has-text("ধান (Rice)"), button:has-text("আলু (Potato)")', { timeout: 10000 });
    await page.waitForTimeout(1000);

    await removeBlueFocus(page);
    await page.addStyleTag({ content: CLEAN_CSS });

    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot1_halt_clarification.png'),
      fullPage: false
    });
    console.log('✓ Saved screenshot1_halt_clarification.png');
    await page.close();
  }

  // -------------------------------------------------------------
  // 2. Capture S2: Photo Scopes Evidence (/detect with Rice)
  // -------------------------------------------------------------
  console.log('2. Capturing S2: Photo Scoping (/detect)...');
  {
    const page = await setupPage(context);

    // Pre-populate latest scan with verified Rice Leaf Brown Spot diagnosis
    await page.addInitScript((data) => {
      localStorage.setItem('krishokchat:latest-scan:v1', JSON.stringify(data));
    }, RICE_SCAN_DATA);

    await page.goto('http://localhost:3000/detect', { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: CLEAN_CSS });
    await page.waitForTimeout(1500);

    // Hide floating bottom-right assistant button so S2 remains pristine and un-obscured
    await page.addStyleTag({
      content: `
        .fixed.bottom-5.right-5, [aria-label="এআই কৃষি সহকারী ওপেন করুন"] {
          display: none !important;
        }
      `
    });

    await page.waitForSelector('text=ধান (Rice)', { timeout: 10000 });
    await page.waitForTimeout(1000);

    await removeBlueFocus(page);
    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot3_photo_crop_scope.png'),
      fullPage: false
    });
    console.log('✓ Saved screenshot3_photo_crop_scope.png');
    await page.close();
  }

  // -------------------------------------------------------------
  // 3. Capture S3: Text-Image Mismatch / CONFIRM
  // -------------------------------------------------------------
  console.log('3. Capturing S3: Text-Image Conflict (CONFIRM)...');
  {
    const page = await setupPage(context);

    await page.addInitScript((data) => {
      localStorage.setItem('krishokchat:latest-scan:v1', JSON.stringify(data));
    }, RICE_SCAN_DATA);

    // Mock contradictory query response in advisory drawer
    await page.route('**/api/qa/stream', async (route) => {
      const ssePayload = [
        'data: {"stage":"safety","status":"complete","detail":"নিরাপদ"}\n\n',
        'data: {"stage":"retrieval","status":"skip","detail":"টেক্সট ও ছবির ফসলে অমিল"}\n\n',
        'final: ' + JSON.stringify({
          query: "আলুর নাবি ধসা রোগ দমনে কী বিষ দিবো?",
          category: "safe_agri",
          answer: "আপনি ধান গাছের ছবি দিয়েছেন, কিন্তু বার্তায় আলু-এর কথা উল্লেখ করেছেন। আপনি কোন ফসলের সমস্যার জন্য পরামর্শ চাচ্ছেন? (ধান নাকি আলু?)",
          confidence: "verified",
          sources: [],
          agent_trace: [
            { stage: "safety", status: "complete", detail: "নিরাপদ" },
            { stage: "retrieval", status: "skip", detail: "ছবি (ধান) বনাম টেক্সট (আলু) অমিল শনাক্ত" }
          ],
          verifier_flags: ["ফসল অমিল সতর্কতা: ছবি ধান বনাম প্রশ্ন আলু"],
          resolution_tier: "interactive_clarification"
        }) + '\n\n'
      ].join('');

      await route.fulfill({
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive'
        },
        body: ssePayload
      });
    });

    await page.goto('http://localhost:3000/detect', { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: CLEAN_CSS });
    await page.waitForTimeout(1200);

    // Open advisory drawer
    const followUpBtn = page.locator('button:has-text("নিয়ে প্রশ্ন করুন"), button[aria-label="এআই কৃষি সহকারী ওপেন করুন"]').first();
    if (await followUpBtn.isVisible()) {
      await followUpBtn.click();
      await page.waitForTimeout(1000);
    }

    const advisoryInput = page.locator('textarea, input[type="text"]').last();
    await advisoryInput.fill('আলুর নাবি ধসা রোগ দমনে কী বিষ দিবো?');
    const sendBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').last();
    await sendBtn.click();

    await page.waitForSelector('text=ধান গাছের ছবি দিয়েছেন, text=আলু', { timeout: 10000 });
    await page.waitForTimeout(1500);

    await removeBlueFocus(page);
    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot4_mismatch_badge.png'),
      fullPage: false
    });
    console.log('✓ Saved screenshot4_mismatch_badge.png');
    await page.close();
  }

  // -------------------------------------------------------------
  // 4. Capture S4: REFER (Banned Chemical Precheck -> 16123)
  // -------------------------------------------------------------
  console.log('4. Capturing S4: Safety Referral (REFER)...');
  {
    const page = await setupPage(context);

    await page.route('**/api/qa/stream', async (route) => {
      const ssePayload = [
        'data: {"stage":"safety","status":"error","detail":"প্যারাকোয়াট নিষিদ্ধ রাসায়নিক সনাক্ত"}\n\n',
        'final: ' + JSON.stringify({
          query: "প্যারাকোয়াট (Paraquat) দিয়ে কীভাবে স্প্রে করব?",
          category: "banned_chemical",
          answer: "এই রাসায়নিকটি বাংলাদেশে কৃষিকাজে ব্যবহারের অনুমতি নেই বা নিষিদ্ধ। অনুমোদিত বিকল্প জানতে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
          confidence: "blocked",
          sources: [],
          agent_trace: [
            { stage: "safety", status: "error", detail: "প্যারাকোয়াট তীব্র বিষাক্ত ও নিষিদ্ধ রাসায়নিক" }
          ],
          verifier_flags: ["নিষিদ্ধ রাসায়নিক: Paraquat"],
          matched_rules: ["banned_chemical_paraquat"],
          resolution_tier: "deterministic_escalation"
        }) + '\n\n'
      ].join('');

      await route.fulfill({
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive'
        },
        body: ssePayload
      });
    });

    await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: CLEAN_CSS });
    await page.waitForTimeout(1000);

    const input = page.locator('textarea, input[type="text"]').first();
    await input.fill('প্যারাকোয়াট (Paraquat) দিয়ে কীভাবে স্প্রে করব?');
    const sendBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').first();
    await sendBtn.click();

    await page.waitForSelector('text=১৬১২৩', { timeout: 10000 });
    await page.waitForTimeout(1200);

    await removeBlueFocus(page);
    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot7_16123_safety_referral.png'),
      fullPage: false
    });
    console.log('✓ Saved screenshot7_16123_safety_referral.png');
    await page.close();
  }

  // -------------------------------------------------------------
  // 5. Capture S5: DROP (Dosage Verification with Expanded Why Panel)
  // -------------------------------------------------------------
  console.log('5. Capturing S5: Dosage Verification & Why Panel (DROP)...');
  {
    const page = await setupPage(context);

    await page.route('**/api/qa/stream', async (route) => {
      const ssePayload = [
        'data: {"stage":"safety","status":"complete","detail":"নিরাপদ"}\n\n',
        'data: {"stage":"retrieval","status":"complete","detail":"৩টি BARI উৎস"}\n\n',
        'data: {"stage":"generation","status":"complete","detail":"খসড়া প্রস্তুত"}\n\n',
        'data: {"stage":"verifier","status":"complete","detail":"মাত্রা যাচাই সম্পন্ন — ১টি অতিরিক্ত ডোজ ফিল্টার্ড"}\n\n',
        'final: ' + JSON.stringify({
          query: "আলুর নাবি ধসা রোগ দমনে কোন ছত্রাকনাশক স্প্রে করতে হবে?",
          category: "safe_agri",
          answer: "আলুর নাবি ধসা (লেট ব্লাইট) রোগ নিয়ন্ত্রণে কৃষি সম্প্রসারণ অধিদপ্তর (DAE) ও BARI নির্দেশিকা অনুসারে অনুমোদিত ছত্রাকনাশক ম্যানকোজেব ৮০WP প্রতি লিটার পানিতে ২ গ্রাম হারে মিশিয়ে বিকেলে আক্রান্ত গাছের পাতায় স্প্রে করুন [১]। স্প্রে করার পর অন্তত ৭ দিন আলু তোলা থেকে বিরত থাকুন [১]। পুষ্টি ব্যবস্থাপনায় জমিতে সুষম মাত্রায় পটাশ ও বোরন সার নিশ্চিত করুন।",
          confidence: "verified",
          sources: [
            {
              id: "BARI_POTATO_LB_852",
              score: 0.965,
              publisher: "BARI",
              publisher_bn: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট",
              title_bn: "আলুর নাবি ধসা রোগ ব্যবস্থাপনা ও অনুমোদিত বালাইনাশক তালিকা",
              citation: "BARI বালাই ব্যবস্থাপনা নির্দেশিকা ২০২৩, পৃষ্ঠা ৮৫২"
            }
          ],
          agent_trace: [
            { stage: "safety", status: "complete", detail: "নিরাপদ" },
            { stage: "retrieval", status: "complete", detail: "BARI নলেজ নোড #852" },
            { stage: "generation", status: "complete", detail: "খসড়া প্রস্তুত" },
            { stage: "verifier", status: "complete", detail: "অননুমোদিত ২০ গ্রাম/লিটার ডোজ ড্রপ করা হয়েছে (DROP)" }
          ],
          verifier_flags: ["অননুমোদিত অতিরিক্ত মাত্রা ফিল্টার্ড: ম্যানকোজেব ২০ গ্রাম/লিটার ড্রপ করা হয়েছে"],
          resolution_tier: "grounded_generation"
        }) + '\n\n'
      ].join('');

      await route.fulfill({
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive'
        },
        body: ssePayload
      });
    });

    await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: CLEAN_CSS });
    await page.waitForTimeout(1000);

    const input = page.locator('textarea, input[type="text"]').first();
    await input.fill('আলুর নাবি ধসা রোগ দমনে কোন ছত্রাকনাশক স্প্রে করতে হবে?');
    const sendBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').first();
    await sendBtn.click();

    // Wait for the answer text
    await page.waitForSelector('text=ম্যানকোজেব ৮০WP', { timeout: 10000 });
    await page.waitForTimeout(1000);

    // Click Why Panel button to expand the audit breakdown
    const whyBtn = page.locator('button:has-text("Why অডিট প্যানেল")').first();
    if (await whyBtn.isVisible()) {
      await whyBtn.click();
      await page.waitForTimeout(1200);
      console.log('Expanded Why audit panel');
    }

    await removeBlueFocus(page);

    // Full screen capture for screenshot5_grounded_answer.png
    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot5_grounded_answer.png'),
      fullPage: false
    });
    console.log('✓ Saved screenshot5_grounded_answer.png');

    // Focused crop of the assistant message card with expanded Why panel for s5_why_panel.png
    const assistantCard = page.locator('.space-y-3').first();
    if (await assistantCard.isVisible()) {
      await assistantCard.screenshot({
        path: path.join(OUT_DIR, 's5_why_panel.png')
      });
      console.log('✓ Saved s5_why_panel.png (focused Why panel proof)');
    }

    await page.close();
  }

  await browser.close();
  console.log('All publication screenshots captured with zero artifacts!');
}

run().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
