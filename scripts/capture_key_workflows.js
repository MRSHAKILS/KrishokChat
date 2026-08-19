const path = require('path');
const fs = require('fs');
const { chromium } = require(path.join(__dirname, '../frontend/node_modules/playwright'));

const BASE_URL = 'http://localhost:3000';
const OUT_DIR_POSTER = path.join(__dirname, '../capstone/poster deisgn/latex/img');
const OUT_DIR_DEMO = path.join(__dirname, '../demo-assets/screenshots');

[OUT_DIR_POSTER, OUT_DIR_DEMO].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

async function run() {
  const browser = await chromium.launch({ headless: true });
  
  // High-DPI context for retina-quality screenshots
  const context = await browser.newContext({
    viewport: { width: 1440, height: 960 },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();

  // ----------------------------------------------------
  // 1. Detect Workflow: Upload image & Click Diagnose
  // ----------------------------------------------------
  console.log('--- 1. Capturing Disease Detection Result ---');
  try {
    await page.goto(`${BASE_URL}/detect`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1000);

    const sampleImagePath = path.join(__dirname, '../demo-assets/images/rice/brown_spot.jpg');
    const fileInput = await page.$('input[type="file"]');
    if (fileInput && fs.existsSync(sampleImagePath)) {
      await fileInput.setInputFiles(sampleImagePath);
      await page.waitForTimeout(1500);

      // Click the "নির্ণয় করুন" (Diagnose) button
      const diagnoseBtn = await page.$('button:has-text("নির্ণয় করুন"), button:has-text("Diagnose")');
      if (diagnoseBtn) {
        console.log('Clicking Diagnose button...');
        await diagnoseBtn.click();
        await page.waitForTimeout(6000); // Wait for vision inference + treatment library mapping
      }
    }

    await page.screenshot({ path: path.join(OUT_DIR_DEMO, '04_detect_diagnosis.png') });
    await page.screenshot({ path: path.join(OUT_DIR_POSTER, 'shot_detect.png') });
    console.log('Detect diagnosis captured.');
  } catch (e) {
    console.error('Detect error:', e.message);
  }

  // ----------------------------------------------------
  // 2. Chat Workflow: Grounded Safe Query
  // ----------------------------------------------------
  console.log('--- 2. Capturing Chat Grounded Q&A ---');
  try {
    await page.goto(`${BASE_URL}/chat`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1000);
    
    const input = await page.$('textarea, input[placeholder*="প্রশ্ন"]');
    if (input) {
      await input.fill('ধানের ব্লাস্ট রোগের লক্ষণ ও অনুমোদিত চিকিৎসা কি?');
      await page.waitForTimeout(500);
      const sendBtn = await page.$('button:has-text("জিজ্ঞাসা করুন"), button:has-text("পাঠান"), button[type="submit"]');
      if (sendBtn) {
        console.log('Sending chat query...');
        await sendBtn.click();
        // Wait for streaming answer, stepper completion, and verification
        await page.waitForTimeout(14000);
      }
    }
    
    await page.screenshot({ path: path.join(OUT_DIR_DEMO, '02_chat_grounded.png') });
    console.log('Grounded chat captured.');
  } catch (e) {
    console.error('Chat grounded error:', e.message);
  }

  // ----------------------------------------------------
  // 3. Chat Workflow: Unsafe Query & Safety Refusal
  // ----------------------------------------------------
  console.log('--- 3. Capturing Chat Safety Refusal ---');
  try {
    await page.goto(`${BASE_URL}/chat`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1000);
    
    const input = await page.$('textarea, input[placeholder*="প্রশ্ন"]');
    if (input) {
      await input.fill('প্যারাকুয়াট বিষ কীভাবে স্প্রে করব এবং মাত্রা কত?');
      await page.waitForTimeout(500);
      const sendBtn = await page.$('button:has-text("জিজ্ঞাসা করুন"), button:has-text("পাঠান"), button[type="submit"]');
      if (sendBtn) {
        console.log('Sending unsafe query...');
        await sendBtn.click();
        await page.waitForTimeout(6000); // Wait for safety classifier + canned redirect to render
      }
      
      await page.screenshot({ path: path.join(OUT_DIR_DEMO, '03_chat_safety_refusal.png') });
      await page.screenshot({ path: path.join(OUT_DIR_POSTER, 'shot_chat.png') }); // Perfect for poster safety callout
      console.log('Safety refusal captured.');
    }
  } catch (e) {
    console.error('Chat safety error:', e.message);
  }

  // ----------------------------------------------------
  // 4. Soil Diagnosis Workflow
  // ----------------------------------------------------
  console.log('--- 4. Capturing Soil Diagnosis ---');
  try {
    await page.goto(`${BASE_URL}/soil`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1000);

    const soilImagePath = path.join(__dirname, '../demo-assets/images/soil/P0001_Doash_8.0kpa.jpg');
    const fileInput = await page.$('input[type="file"]');
    if (fileInput && fs.existsSync(soilImagePath)) {
      await fileInput.setInputFiles(soilImagePath);
      await page.waitForTimeout(1000);
      const analyzeBtn = await page.$('button:has-text("বিশ্লেষণ করুন"), button:has-text("নির্ণয় করুন"), button:has-text("Analyze")');
      if (analyzeBtn) {
        await analyzeBtn.click();
        await page.waitForTimeout(5000);
      }
    }

    await page.screenshot({ path: path.join(OUT_DIR_DEMO, '05_soil_moisture.png') });
    console.log('Soil diagnosis captured.');
  } catch (e) {
    console.error('Soil error:', e.message);
  }

  // ----------------------------------------------------
  // 5. Analytics Dashboard
  // ----------------------------------------------------
  console.log('--- 5. Capturing Analytics ---');
  try {
    await page.goto(`${BASE_URL}/analytics`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(OUT_DIR_DEMO, '06_analytics_dashboard.png') });
    await page.screenshot({ path: path.join(OUT_DIR_POSTER, 'shot_analytics.png') });
    console.log('Analytics captured.');
  } catch (e) {
    console.error('Analytics error:', e.message);
  }

  await browser.close();
  console.log('Refined screenshots captured successfully!');
}

run().catch(console.error);
