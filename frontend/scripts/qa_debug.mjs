// Debug: check what the QA endpoint returns via curl-like fetch
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Intercept API responses
page.on('response', async (response) => {
  const url = response.url();
  if (url.includes('/api/qa')) {
    console.log(`\nAPI Response: ${url}`);
    console.log(`Status: ${response.status()}`);
    try {
      const body = await response.text();
      console.log(`Body (first 500): ${body.substring(0, 500)}`);
    } catch (e) {
      console.log('Could not read body');
    }
  }
});

try {
  await page.goto('http://localhost:3100', { waitUntil: 'networkidle', timeout: 15000 });
  await page.locator('text=প্রশ্ন করুন').click();
  await page.waitForTimeout(500);
  await page.locator('input[placeholder*="প্রশ্ন"]').fill('আলুর দেরি ব্লাইট রোগের প্রতিকার কি?');
  await page.locator('text=জিজ্ঞাসা').click();
  await page.waitForTimeout(15000);
} catch (e) {
  console.log('Error:', e.message);
}
await browser.close();
