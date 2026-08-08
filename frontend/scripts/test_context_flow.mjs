// Test: detect disease -> switch to chat -> question includes context
import { chromium } from 'playwright';
import path from 'path';

const IMG = path.join('D:\\KrishokChat Advisory System\\backend\\ml_assets\\vision\\test_images\\wheat_disease\\Leaf Rust\\yellow_rust_test_0.png');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Capture API request bodies
let qaRequestBody = null;
page.on('request', (req) => {
  if (req.url().includes('/api/qa/stream') && req.method() === 'POST') {
    qaRequestBody = req.postDataJSON();
    console.log('QA request body:', JSON.stringify(qaRequestBody));
  }
});

try {
  await page.goto('http://localhost:3100', { waitUntil: 'networkidle', timeout: 15000 });

  // Upload image
  await page.locator('input[type="file"]').setInputFiles(IMG);
  await page.waitForTimeout(1000);

  // Detect
  await page.locator('text=রোগ নির্ণয় করুন').click();
  await page.waitForTimeout(8000);

  const detectResult = await page.locator('text=Leaf Rust').count();
  console.log('Detection result (Leaf Rust):', detectResult > 0);

  // Switch to QA tab
  await page.locator('text=প্রশ্ন করুন').click();
  await page.waitForTimeout(500);

  // Check context badge
  const contextBadge = await page.locator('text=সনাক্ত').count();
  console.log('Context badge visible:', contextBadge > 0);

  // Check detected info shown
  const wheatContext = await page.locator('text=Wheat').count();
  console.log('Wheat context in QA tab:', wheatContext > 0);

  // Ask question
  await page.locator('input[placeholder*="প্রশ্ন"]').fill('এই রোগের প্রতিকার কি?');
  await page.locator('text=জিজ্ঞাসা').click();
  await page.waitForTimeout(15000);

  // Verify request included crop/disease
  if (qaRequestBody) {
    console.log('Query sent:', qaRequestBody.query);
    console.log('Crop context:', qaRequestBody.crop || 'NOT SENT');
    console.log('Disease context:', qaRequestBody.disease || 'NOT SENT');
  } else {
    console.log('QA request not captured');
  }

  const answerVisible = await page.locator('text=প্রাসঙ্গিক').count() + await page.locator('text=এই রোগের').count() + await page.locator('text=প্রতিরোধী').count() + await page.locator('text=প্রতিকার').count();
  console.log('Answer visible:', answerVisible > 0);
  if (answerVisible === 0) {
    const allText = await page.locator('body').textContent();
    console.log('Body text (last 500):', allText?.slice(-500));
  }

  if (qaRequestBody?.crop && qaRequestBody?.disease) {
    console.log('\nContext flow PASSED');
  } else {
    console.log('\nContext flow FAILED');
  }
} catch (e) {
  console.log('Context flow FAILED:', e.message);
}
await browser.close();
