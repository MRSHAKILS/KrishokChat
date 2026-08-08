// Full integration: upload image -> detect -> show info in browser
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const IMG = path.join('D:\\KrishokChat Advisory System\\backend\\ml_assets\\vision\\test_images\\wheat_disease\\Leaf Rust\\yellow_rust_test_0.png');
const BASE = 'http://localhost:3100';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const errors = [];
page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
page.on('pageerror', err => errors.push(err.message));

try {
  await page.goto(BASE, { waitUntil: 'networkidle', timeout: 15000 });

  // Upload image
  const input = page.locator('input[type="file"]');
  await input.setInputFiles(IMG);
  await page.waitForTimeout(1000);

  // Check preview appears
  const preview = await page.locator('img[alt="preview"]').count();
  console.log('Preview shown:', preview > 0);

  // Check buttons appear
  const classifyBtn = await page.locator('text=ফসল শনাক্ত করুন').count();
  const detectBtn = await page.locator('text=রোগ নির্ণয় করুন').count();
  console.log('Classify button:', classifyBtn > 0);
  console.log('Detect button:', detectBtn > 0);

  // Click detect
  await page.locator('text=রোগ নির্ণয় করুন').click();
  await page.waitForTimeout(8000); // wait for API call + response

  // Check result
  const cropBadge = await page.locator('text=Wheat').count();
  const diseaseName = await page.locator('text=Leaf Rust').count();
  const description = await page.locator('text=বিবরণ').count();
  const solution = await page.locator('text=প্রতিকার').count();

  console.log('Crop badge (Wheat):', cropBadge > 0);
  console.log('Disease (Leaf Rust):', diseaseName > 0);
  console.log('Description section:', description > 0);
  console.log('Solution section:', solution > 0);

  // Check if solution content is visible
  const solutionContent = await page.locator('text=প্রতিরোধী জাত').count();
  console.log('Solution content visible:', solutionContent > 0);

  console.log('Console errors:', errors.length);
  if (errors.length > 0) errors.slice(0, 5).forEach(e => console.log('  -', e));

  if (cropBadge > 0 && diseaseName > 0) {
    console.log('\nIntegration test PASSED');
  } else {
    console.log('\nIntegration test FAILED');
  }
} catch (e) {
  console.log('Integration test FAILED:', e.message);
}
await browser.close();
