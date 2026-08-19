const path = require('path');
const fs = require('fs');
const { chromium } = require(path.join(__dirname, '../frontend/node_modules/playwright'));

const BASE_URL = 'http://localhost:3000';
const OUT_DIR_POSTER = path.join(__dirname, '../capstone/poster deisgn/latex/img');
const OUT_DIR_DEMO = path.join(__dirname, '../demo-assets/screenshots');

async function captureCroppedCard() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();
  
  await page.goto(`${BASE_URL}/research/safety`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(1000);

  const bannedTab = await page.$('button:has-text("নিষিদ্ধ রাসায়নিক"), button:has-text("Banned Chemical")');
  if (bannedTab) {
    await bannedTab.click();
    await page.waitForTimeout(1000);
  }

  // Find the interactive pipeline card
  const container = await page.$('.rounded-2xl.border.rule.bg-paper, div:has-text("৪-ধাপের নিরাপত্তা ও আরএজি সিমুলেটর")');
  if (container) {
    await container.screenshot({ path: path.join(OUT_DIR_DEMO, '09_chemical_safety_tight_card.png') });
    await container.screenshot({ path: path.join(OUT_DIR_POSTER, 'shot_safety_tight_card.png') });
    console.log('Tight card captured.');
  }

  await browser.close();
}

captureCroppedCard().catch(console.error);
