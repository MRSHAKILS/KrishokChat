const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const OUT_DIR = path.resolve('d:/KrishokChat Advisory System/paper/EACL Final/paper/screenshots');
const VIDEO_DIR = path.resolve('d:/KrishokChat Advisory System/demo-assets');
const PUBLIC_DIR = path.resolve('d:/KrishokChat Advisory System/frontend/public');
const RECORDINGS_DIR = path.resolve('d:/KrishokChat Advisory System/frontend/recordings_tmp');

for (const d of [OUT_DIR, VIDEO_DIR, PUBLIC_DIR, RECORDINGS_DIR]) {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

// Clean CSS injected on every page
const CLEAN_CSS = `
  /* 1. Eliminate all focus rings, blue halos, and active selection borders */
  *:focus, *:focus-visible, *:active {
    outline: none !important;
    box-shadow: none !important;
  }
  ::selection {
    background: rgba(47, 93, 58, 0.2) !important;
    color: inherit !important;
  }
  
  /* 2. Suppress Next.js development overlay artifacts (black N circle, build watcher, toasts) */
  nextjs-portal,
  #__next-build-watcher,
  [data-nextjs-dev-tools-button],
  [data-nextjs-toast],
  next-route-announcer,
  div[data-nextjs-dialog-overlay] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }

  /* 3. Force pure sunlight high-contrast white mode */
  html, html[data-contrast="sunlight"] {
    --color-paper: #ffffff !important;
    --color-paper-2: #f8f9fa !important;
    --color-bone: #e2e8f0 !important;
    --color-bone-soft: #edf2f7 !important;
    background-color: #ffffff !important;
  }
  body {
    background-color: #ffffff !important;
  }
`;

async function preparePage(page) {
  await page.addInitScript(() => {
    localStorage.setItem('krishokchat:contrast', 'sunlight');
    localStorage.setItem('krishokchat:locale', 'bn');
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
}

async function removeFocus(page) {
  await page.evaluate(() => {
    if (document.activeElement && typeof document.activeElement.blur === 'function') {
      document.activeElement.blur();
    }
  });
  await page.waitForTimeout(400);
}

async function main() {
  console.log('=== Starting Clean Publication Asset & Video Capture ===');
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  // Recording context for video screencast (1920x1080 native HD)
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1.5,
    recordVideo: {
      dir: RECORDINGS_DIR,
      size: { width: 1920, height: 1080 }
    }
  });

  const page = await context.newPage();
  await preparePage(page);

  // Setup API Mocking for Deterministic Flow
  await page.route('**/api/qa/stream', async (route) => {
    const postData = route.request().postDataJSON() || {};
    const query = (postData.query || '').trim();

    // 1. S4: Banned Chemical (Paraquat)
    if (query.includes('প্যারাকোয়াট') || query.toLowerCase().includes('paraquat')) {
      const ssePayload = [
        'data: {"stage":"safety","status":"error","detail":"প্যারাকোয়াট তীব্র বিষাক্ত ও নিষিদ্ধ রাসায়নিক"}\n\n',
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
      return route.fulfill({
        status: 200,
        headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
        body: ssePayload
      });
    }

    // 2. S5: Grounded Advisory with Dosage Verification & Why Trace (Priority before generic potato check!)
    if (query.includes('ছত্রাকনাশক') || query.includes('কোন ছত্রাকনাশক')) {
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
      return route.fulfill({
        status: 200,
        headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
        body: ssePayload
      });
    }

    // 3. S3: Text-Image Conflict (Rice photo + Potato text)
    if (query.includes('আলু') && (query.includes('কী বিষ') || query.includes('কি বিষ') || query.includes('নাবি ধসা'))) {
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
      return route.fulfill({
        status: 200,
        headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
        body: ssePayload
      });
    }

    // 4. Default: S1 Crop-less Query
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
    return route.fulfill({
      status: 200,
      headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
      body: ssePayload
    });
  });

  // --------------------------------------------------------------------------
  // Stage 0: Home / Hero Landing View
  // --------------------------------------------------------------------------
  console.log('1. Capturing Stage 0: Hero Interface...');
  await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: CLEAN_CSS });
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
    localStorage.setItem('krishokchat:contrast', 'sunlight');
    localStorage.setItem('krishokchat:locale', 'bn');
    document.documentElement.setAttribute('data-contrast', 'sunlight');
  });
  await removeFocus(page);
  await page.waitForTimeout(1500);

  await page.screenshot({
    path: path.join(OUT_DIR, 'fig2_main_interface.png'),
    fullPage: false
  });
  console.log('✓ Saved fig2_main_interface.png');

  // --------------------------------------------------------------------------
  // Stage 1: S1 ASK (Colloquial Query -> 6 Staple Crop Chips)
  // --------------------------------------------------------------------------
  console.log('2. Capturing Stage 1: S1 ASK (Missing crop clarification)...');
  const chatInput = page.locator('textarea, input[type="text"]').first();
  await chatInput.fill('পাতায় হলুদ দাগ হয়েছে, কি বিষ দিবো?');
  await page.waitForTimeout(800);
  const sendBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').first();
  await sendBtn.click();

  await page.waitForSelector('button:has-text("ধান (Rice)"), button:has-text("আলু (Potato)")', { timeout: 10000 });
  await page.waitForTimeout(1500);
  await removeFocus(page);

  // Full viewport capture for appendix
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot1_halt_clarification.png'),
    fullPage: false
  });
  console.log('✓ Saved screenshot1_halt_clarification.png');

  // Focused crop for Figure 2(a)
  const s1Turn = page.locator('.scrollbar-thin').first();
  if (await s1Turn.isVisible()) {
    await s1Turn.screenshot({
      path: path.join(OUT_DIR, 'fig2a_ask.png')
    });
    console.log('✓ Saved fig2a_ask.png (focused S1 card crop)');
  }

  // --------------------------------------------------------------------------
  // Stage 2: S2 Photo Crop Scoping (/detect with Rice diagnosis)
  // --------------------------------------------------------------------------
  console.log('3. Capturing Stage 2: S2 Photo Scoping (/detect)...');
  await page.goto('http://localhost:3000/detect', { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: CLEAN_CSS });
  await page.waitForTimeout(1500);

  // Click Instant Test on sample #1 (Rice Brown Spot) to load real photo and diagnosis
  const instantTestBtn = page.locator('button[title*="তাৎক্ষণিক"], button:has-text("তাৎক্ষণিক টেস্ট")').first();
  if (await instantTestBtn.isVisible()) {
    await instantTestBtn.click();
    console.log('Clicked instant benchmark test for Rice Brown Spot');
    await page.waitForTimeout(2000);
  }

  // Temporarily hide floating assistant pill via JS inline style for pristine S2 capture
  await page.evaluate(() => {
    const el = document.querySelector('.fixed.bottom-5.right-5');
    if (el) el.style.display = 'none';
  });
  await removeFocus(page);
  await page.waitForTimeout(800);

  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot3_photo_crop_scope.png'),
    fullPage: false
  });
  console.log('✓ Saved screenshot3_photo_crop_scope.png');

  // Restore assistant pill for S3
  await page.evaluate(() => {
    const el = document.querySelector('.fixed.bottom-5.right-5');
    if (el) el.style.display = '';
  });
  await page.waitForTimeout(500);

  // --------------------------------------------------------------------------
  // Stage 3: S3 Text-Image Contradiction Gating (CONFIRM)
  // --------------------------------------------------------------------------
  console.log('4. Capturing Stage 3: S3 CONFIRM (Text-Image Conflict)...');
  // Trigger drawer via evaluate click
  await page.evaluate(() => {
    const btn = document.querySelector('button[aria-label="এআই কৃষি সহকারী ওপেন করুন"]') ||
                document.querySelector('.fixed.bottom-5.right-5 button');
    if (btn) btn.click();
  });
  await page.waitForTimeout(1500);

  // Wait for slide-over drawer to appear
  await page.waitForSelector('text=এআই কৃষি পরামর্শদাতা', { timeout: 10000 });
  await page.waitForTimeout(800);

  const drawerInput = page.locator('div.fixed.inset-0 textarea, textarea').last();
  await drawerInput.fill('আলুর নাবি ধসা রোগ দমনে কী বিষ দিবো?');
  await page.waitForTimeout(800);

  const drawerSendBtn = page.locator('div.fixed.inset-0 button[type="submit"], button:has(svg.lucide-send)').last();
  await drawerSendBtn.click();

  await page.waitForSelector('text=ধান গাছের ছবি দিয়েছেন', { timeout: 10000 });
  await page.waitForTimeout(2000);
  await removeFocus(page);

  // Full viewport capture
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot4_mismatch_badge.png'),
    fullPage: false
  });
  console.log('✓ Saved screenshot4_mismatch_badge.png');

  // Focused crop of drawer for Figure 2(b)
  const drawerDialog = page.locator('div[role="dialog"]').first();
  if (await drawerDialog.isVisible()) {
    await drawerDialog.screenshot({
      path: path.join(OUT_DIR, 'fig2b_mismatch.png')
    });
    console.log('✓ Saved fig2b_mismatch.png (focused S3 drawer crop)');
  }

  // --------------------------------------------------------------------------
  // Stage 4: S4 REFER (Banned Chemical Precheck -> 16123)
  // --------------------------------------------------------------------------
  console.log('5. Capturing Stage 4: S4 REFER (High-Risk Chemical Referral)...');
  // Clear conversation history before S4 so it is pristine and centered
  await page.evaluate(() => {
    localStorage.removeItem('krishokchat:conversation:v1');
    sessionStorage.clear();
  });
  await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: CLEAN_CSS });
  await page.evaluate(() => {
    localStorage.removeItem('krishokchat:conversation:v1');
  });
  await page.waitForTimeout(1200);

  const s4Input = page.locator('textarea, input[type="text"]').first();
  await s4Input.fill('প্যারাকোয়াট (Paraquat) দিয়ে কীভাবে স্প্রে করব?');
  await page.waitForTimeout(800);
  const s4Send = page.locator('button[type="submit"], button:has(svg.lucide-send)').first();
  await s4Send.click();

  await page.waitForSelector('text=১৬১২৩', { timeout: 10000 });
  await page.waitForTimeout(2000);
  await removeFocus(page);

  // Full viewport capture for appendix
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot7_16123_safety_referral.png'),
    fullPage: false
  });
  console.log('✓ Saved screenshot7_16123_safety_referral.png');

  // Focused crop for S4
  const s4Turn = page.locator('.scrollbar-thin').first();
  if (await s4Turn.isVisible()) {
    await s4Turn.screenshot({
      path: path.join(OUT_DIR, 'fig2d_refer.png')
    });
    console.log('✓ Saved fig2d_refer.png (focused S4 card crop)');
  }

  // --------------------------------------------------------------------------
  // Stage 5: S5 DROP (Dosage Verification with Expanded Why Audit Panel)
  // --------------------------------------------------------------------------
  console.log('6. Capturing Stage 5: S5 DROP (Dosage Verification & Why Audit Panel)...');
  // Clear conversation history before S5 so it is pristine and centered
  await page.evaluate(() => {
    localStorage.removeItem('krishokchat:conversation:v1');
    sessionStorage.clear();
  });
  await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: CLEAN_CSS });
  await page.evaluate(() => {
    localStorage.removeItem('krishokchat:conversation:v1');
  });
  await page.waitForTimeout(1200);

  const s5Input = page.locator('textarea, input[type="text"]').first();
  await s5Input.fill('আলুর নাবি ধসা রোগ দমনে কোন ছত্রাকনাশক স্প্রে করতে হবে?');
  await page.waitForTimeout(800);
  const s5Send = page.locator('button[type="submit"], button:has(svg.lucide-send)').first();
  await s5Send.click();

  await page.waitForSelector('text=ম্যানকোজেব ৮০WP', { timeout: 10000 });
  await page.waitForTimeout(1200);

  // Click Why Audit Panel button to expand the audit trail
  const whyBtn = page.locator('button:has-text("Why অডিট প্যানেল")').first();
  if (await whyBtn.isVisible()) {
    await whyBtn.click();
    console.log('✓ Expanded Why audit panel');
    await page.waitForTimeout(1500);
  }

  await removeFocus(page);

  // Full viewport capture for appendix
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot5_grounded_answer.png'),
    fullPage: false
  });
  console.log('✓ Saved screenshot5_grounded_answer.png');

  // Focused crop of S5 message card for Figure 2(c)
  const s5Turn = page.locator('.scrollbar-thin').first();
  if (await s5Turn.isVisible()) {
    await s5Turn.screenshot({
      path: path.join(OUT_DIR, 's5_why_panel.png')
    });
    console.log('✓ Saved s5_why_panel.png (focused S5 card proof with Why panel)');
  }

  // --------------------------------------------------------------------------
  // Stage 6: Screencast & System Walkthrough Page
  // --------------------------------------------------------------------------
  console.log('7. Capturing Screencast walkthrough overview...');
  await page.goto('http://localhost:3000/screencast', { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: CLEAN_CSS });
  await removeFocus(page);
  await page.waitForTimeout(3000);

  // Close context to finalize Playwright WebM video recording
  await page.close();
  await context.close();
  await browser.close();

  console.log('\n=== Playwright capture complete. Assembling publication video... ===');

  const videoFiles = fs.readdirSync(RECORDINGS_DIR).filter(f => f.endsWith('.webm'));
  if (videoFiles.length > 0) {
    const rawVideoPath = path.join(RECORDINGS_DIR, videoFiles[0]);
    console.log(`Raw recording found: ${rawVideoPath}`);

    const targetMp4 = path.join(VIDEO_DIR, 'krishokchat_demo_video.mp4');
    const publicMp4 = path.join(PUBLIC_DIR, 'krishokchat_demo_video.mp4');
    const targetGif = path.join(VIDEO_DIR, 'krishokchat_demo.gif');
    const publicGif = path.join(PUBLIC_DIR, 'krishokchat_demo.gif');

    // Convert to MP4 with clean scaling, yuv420p, 24fps
    console.log('Encoding MP4 with ffmpeg (H.264, 1080p, faststart)...');
    execSync(`ffmpeg -y -i "${rawVideoPath}" -c:v libx264 -pix_fmt yuv420p -r 24 -movflags +faststart "${targetMp4}"`);
    fs.copyFileSync(targetMp4, publicMp4);
    console.log(`✓ Generated MP4: ${targetMp4}`);

    // Convert to GIF
    console.log('Generating optimized animated GIF preview...');
    execSync(`ffmpeg -y -i "${targetMp4}" -vf "fps=8,scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" "${targetGif}"`);
    fs.copyFileSync(targetGif, publicGif);
    console.log(`✓ Generated GIF: ${targetGif}`);
  }

  // Clean up temporary recording folder
  try {
    fs.rmSync(RECORDINGS_DIR, { recursive: true, force: true });
  } catch (e) {}

  console.log('\n=== All assets and video generated successfully! ===');
}

main().catch(err => {
  console.error('Execution error:', err);
  process.exit(1);
});
