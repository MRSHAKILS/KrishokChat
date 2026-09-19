const { chromium } = require('playwright');
const path = require('path');

const OUT_DIR = path.resolve('d:/KrishokChat Advisory System/paper/EACL Final/paper/screenshots');

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();

  console.log('Navigating to /detect...');
  await page.goto('http://localhost:3000/detect', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  // Upload potato leaf image
  const potatoImgPath = path.resolve('d:/KrishokChat Advisory System/demo-assets/images/potato/late_blight.jpg');
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(potatoImgPath);
  console.log('Uploaded potato leaf image');

  // Click detect button
  const detectBtn = page.locator('button:has-text("নির্ণয় করুন")').first();
  await detectBtn.waitFor({ state: 'visible', timeout: 10000 });
  await detectBtn.click();
  console.log('Clicked নির্ণয় করুন button');

  // Wait for diagnosis result to appear
  await page.waitForSelector('text=নাবি ধসা, text=আলু', { timeout: 30000 });
  console.log('Diagnosis completed: Potato Late Blight');
  await page.waitForTimeout(2000);

  // Open advisory panel
  console.log('Opening advisory panel...');
  const followUpBtn = page.locator('button:has-text("নিয়ে প্রশ্ন করুন"), button[aria-label="এআই কৃষি সহকারী ওপেন করুন"]').first();
  await followUpBtn.click();
  await page.waitForSelector('text=প্রসঙ্গ:', { timeout: 10000 });
  await page.waitForTimeout(1000);

  // Type question about Rice
  const advisoryInput = page.locator('textarea, input[type="text"]').last();
  await advisoryInput.fill('ধানের পাতায় বাদামি দাগ হয়েছে, কী কীটনাশক দিবো?');
  const sendAdvisoryBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').last();
  await sendAdvisoryBtn.click();
  console.log('Sent contradictory query');

  // Wait for clarification response to arrive and render completely
  await page.waitForSelector('text=আপনি আলু গাছের ছবি দিয়েছেন', { timeout: 30000 });
  await page.waitForTimeout(2000);

  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot4_mismatch_badge.png'),
    fullPage: false
  });
  console.log('Successfully re-captured screenshot4_mismatch_badge.png');

  await browser.close();
}

run().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
