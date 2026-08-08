// Test full QA integration in browser
import { chromium } from 'playwright';
import path from 'path';

const BASE = 'http://localhost:3100';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const errors = [];
page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
page.on('pageerror', err => errors.push(err.message));

try {
  await page.goto(BASE, { waitUntil: 'networkidle', timeout: 15000 });

  // Switch to QA tab
  await page.locator('text=প্রশ্ন করুন').click();
  await page.waitForTimeout(500);

  // Type question
  const input = page.locator('input[placeholder*="প্রশ্ন"]');
  await input.fill('আলুর দেরি ব্লাইট রোগের প্রতিকার কি?');
  await page.waitForTimeout(200);

  // Submit
  await page.locator('text=জিজ্ঞাসা').click();
  console.log('Submitted question');

  // Wait for response
  await page.waitForTimeout(15000);

  // Check result
  const answerVisible = await page.locator('text=প্রাসঙ্গিক').count();
  const categoryBadge = await page.locator('[class*="badge"], [class*="rounded"]').first().textContent();
  console.log('Answer visible:', answerVisible > 0);
  console.log('Category badge:', categoryBadge);

  // Check agent trace
  const traceVisible = await page.locator('text=নিরাপত্তা').count() + await page.locator('text=safety').count();
  console.log('Agent trace visible:', traceVisible > 0);

  // Check sources
  const sourcesVisible = await page.locator('text=উৎস').count();
  console.log('Sources section:', sourcesVisible > 0);

  console.log('Console errors:', errors.length);
  if (errors.length > 0) errors.slice(0, 5).forEach(e => console.log('  -', e));

  if (answerVisible > 0) {
    console.log('\nQA integration PASSED');
  } else {
    console.log('\nQA integration FAILED');
  }
} catch (e) {
  console.log('QA integration FAILED:', e.message);
}
await browser.close();
