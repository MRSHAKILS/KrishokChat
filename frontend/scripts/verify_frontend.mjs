// Verify frontend UI with Playwright (ESM)
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const errors = [];
page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
page.on('pageerror', err => errors.push(err.message));

try {
  await page.goto('http://localhost:3100', { waitUntil: 'networkidle', timeout: 15000 });
  console.log('Title:', await page.title());

  const tabs = await page.locator('[role="tab"]').allTextContents();
  console.log('Tabs:', tabs);

  const detectText = await page.locator('text=ফসলের রোগ নির্ণয়').count();
  console.log('Detect tab content found:', detectText > 0);

  await page.locator('text=প্রশ্ন করুন').click();
  await page.waitForTimeout(500);
  const qaVisible = await page.locator('text=কৃষি পরামর্শ').count();
  console.log('QA tab visible:', qaVisible > 0);

  const inputVisible = await page.locator('input[placeholder*="প্রশ্ন"]').count();
  console.log('QA input found:', inputVisible > 0);

  console.log('Console errors:', errors.length);
  if (errors.length > 0) errors.slice(0, 5).forEach(e => console.log('  -', e));

  console.log('\nFrontend verification PASSED');
} catch (e) {
  console.log('Frontend verification FAILED:', e.message);
}
await browser.close();
