const path = require('path');
const fs = require('fs');
const { chromium } = require(path.join(__dirname, '../frontend/node_modules/playwright'));

const BASE_URL = 'http://localhost:3000';
const OUT_DIR_POSTER = path.join(__dirname, '../capstone/poster deisgn/latex/img');
const OUT_DIR_DEMO = path.join(__dirname, '../demo-assets/screenshots');

async function captureSafetyProof() {
  const browser = await chromium.launch({ headless: true });
  
  // 1. Capture the Chemical Safety Sandbox on /research/safety
  console.log('--- 1. Capturing Chemical Safety Sandbox ---');
  const context1 = await browser.newContext({
    viewport: { width: 1440, height: 1050 },
    deviceScaleFactor: 2,
  });
  const page1 = await context1.newPage();
  
  try {
    await page1.goto(`${BASE_URL}/research/safety`, { waitUntil: 'networkidle', timeout: 30000 });
    await page1.waitForTimeout(1500);

    // Click on Archetype 2: "২. নিষিদ্ধ রাসায়নিক প্রশ্ন (Banned Chemical)"
    const bannedTab = await page1.$('button:has-text("নিষিদ্ধ রাসায়নিক"), button:has-text("Banned Chemical")');
    if (bannedTab) {
      console.log('Clicking banned chemical archetype tab...');
      await bannedTab.click();
      await page1.waitForTimeout(1000);

      // Click run simulator button if present
      const runBtn = await page1.$('button:has-text("সিমুলেশন চালান"), button:has-text("Run"), button:has-text("চালান")');
      if (runBtn) {
        await runBtn.click();
        await page1.waitForTimeout(4500);
      }
    }

    // Capture focused screenshot of the sandbox area or full page
    const sandboxElem = await page1.$('#sandbox, section:has-text("পাইপলাইন সিমুলেটর"), div:has-text("নিষিদ্ধ রাসায়নিক")');
    if (sandboxElem) {
      await sandboxElem.screenshot({ path: path.join(OUT_DIR_DEMO, '09_chemical_safety_sandbox_card.png') });
    }
    await page1.screenshot({ path: path.join(OUT_DIR_DEMO, '09_chemical_safety_sandbox_full.png') });
    console.log('Chemical safety sandbox captured.');
  } catch (e) {
    console.error('Safety sandbox error:', e.message);
  }

  // 2. Capture the Live Chat Chemical Safety Rejection on /chat
  console.log('--- 2. Capturing Live Chat Chemical Safety Rejection ---');
  const context2 = await browser.newContext({
    viewport: { width: 1300, height: 880 },
    deviceScaleFactor: 2,
  });
  const page2 = await context2.newPage();
  
  try {
    await page2.goto(`${BASE_URL}/chat`, { waitUntil: 'networkidle', timeout: 30000 });
    await page2.waitForTimeout(1500);

    const input = await page2.$('textarea, input[placeholder*="প্রশ্ন"]');
    if (input) {
      await input.fill('ধানের জমিতে ঘাস মারার জন্য প্যারাকুয়াট কি অতিরিক্ত মাত্রায় ছিটানো যাবে?');
      await page2.waitForTimeout(500);
      const sendBtn = await page2.$('button:has-text("জিজ্ঞাসা করুন"), button:has-text("পাঠান"), button[type="submit"]');
      if (sendBtn) {
        console.log('Sending chemical query in chat...');
        await sendBtn.click();
        await page2.waitForTimeout(6000); // Wait for safety refusal response
      }
    }

    await page2.screenshot({ path: path.join(OUT_DIR_DEMO, '10_chemical_safety_chat_rejection.png') });
    await page2.screenshot({ path: path.join(OUT_DIR_POSTER, 'shot_safety_rejection.png') });
    console.log('Live chat safety rejection captured.');
  } catch (e) {
    console.error('Chat safety error:', e.message);
  }

  await browser.close();
  console.log('All safety verification screenshots captured successfully!');
}

captureSafetyProof().catch(console.error);
