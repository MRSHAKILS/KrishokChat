const path = require('path');
const fs = require('fs');
const { chromium } = require(path.join(__dirname, '../frontend/node_modules/playwright'));

const BASE_URL = 'http://localhost:3000';
const OUT_DIR_POSTER = path.join(__dirname, '../capstone/poster deisgn/latex/img');
const OUT_DIR_DEMO = path.join(__dirname, '../demo-assets/screenshots');

async function capturePerfectDetect() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1100 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  console.log('Capturing Detect Workflow...');
  await page.goto(`${BASE_URL}/detect`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(1000);

  // Set crop hint to Rice if dropdown exists
  const cropSelect = await page.$('select');
  if (cropSelect) {
    await cropSelect.selectOption({ label: 'ধান' }).catch(() => {});
  }

  const sampleImagePath = path.join(__dirname, '../demo-assets/images/rice/brown_spot.jpg');
  const fileInput = await page.$('input[type="file"]');
  if (fileInput && fs.existsSync(sampleImagePath)) {
    await fileInput.setInputFiles(sampleImagePath);
    await page.waitForTimeout(1500);

    const diagnoseBtn = await page.$('button:has-text("নির্ণয় করুন"), button:has-text("Diagnose")');
    if (diagnoseBtn) {
      console.log('Clicking diagnose button...');
      await diagnoseBtn.click();
      
      // Wait for the diagnosis card to appear
      await page.waitForSelector('text=চিকিৎসা, text=রোগ নির্ণয়, text=Brown Spot, text=ধান', { timeout: 15000 }).catch(() => {});
      await page.waitForTimeout(3000);
    }
  }

  await page.screenshot({ path: path.join(OUT_DIR_DEMO, '04_detect_diagnosis.png') });
  await page.screenshot({ path: path.join(OUT_DIR_POSTER, 'shot_detect.png') });
  console.log('Detect captured.');

  await browser.close();
}

capturePerfectDetect().catch(console.error);
