const { chromium } = require('playwright');
const path = require('path');

const OUT_DIR = path.resolve('d:/KrishokChat Advisory System/paper/EACL Final/paper/screenshots');

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 850 },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();

  console.log('Navigating to http://localhost:3000/detect ...');
  await page.goto('http://localhost:3000/detect', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  // 1. Click sample button "ধানের পাতার নমুনা নিন"
  console.log('Clicking sample button...');
  const sampleBtn = page.locator('button:has-text("ধানের পাতার নমুনা নিন")').first();
  await sampleBtn.waitFor({ state: 'visible', timeout: 10000 });
  await sampleBtn.click();
  await page.waitForTimeout(2000);

  // 2. Click "নির্ণয় করুন"
  console.log('Clicking নির্ণয় করুন button...');
  const detectBtn = page.locator('button:has-text("নির্ণয় করুন")').first();
  await detectBtn.waitFor({ state: 'visible', timeout: 10000 });
  await detectBtn.click();

  // 3. Wait for diagnosis result to appear
  console.log('Waiting for diagnosis card...');
  const diagCard = page.getByText('মুছুন').or(page.getByText('রোগ বিশ্লেষণ প্রবাহ')).or(page.getByText('আক্রান্ত ফসল'));
  await diagCard.first().waitFor({ state: 'visible', timeout: 35000 });
  console.log('Diagnosis card appeared!');
  await page.waitForTimeout(3000);

  // Capture Screenshot 3: Photo & Crop Scoping
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot3_photo_crop_scope.png'),
    fullPage: false
  });
  console.log('Successfully captured screenshot3_photo_crop_scope.png');

  // 4. Open Slide-Over Advisory
  console.log('Opening advisory drawer...');
  const followUpBtn = page.locator('button:has-text("নিয়ে প্রশ্ন করুন"), button[aria-label="এআই কৃষি সহকারী ওপেন করুন"]').first();
  await followUpBtn.waitFor({ state: 'visible', timeout: 10000 });
  await followUpBtn.click();
  await page.waitForSelector('text=এআই কৃষি পরামর্শদাতা', { timeout: 10000 });
  await page.waitForTimeout(1500);

  // 5. Ask contradictory query (Query asks about Potato, while image is Rice)
  console.log('Typing contradictory query into advisory drawer...');
  const advisoryInput = page.locator('textarea, input[type="text"]').last();
  await advisoryInput.fill('আলুর নাবি ধসা রোগ দমনে কী বিষ দিবো?');
  await page.waitForTimeout(500);

  const sendBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').last();
  await sendBtn.click();
  console.log('Contradictory query sent. Waiting for cross-modal conflict response...');

  // 6. Wait for mismatch clarification response
  const conflictMsg = page.getByText('অমিল পরিলক্ষিত').or(page.getByText('ধান গাছের ছবি')).or(page.getByText('আলু (Potato)'));
  await conflictMsg.first().waitFor({ state: 'visible', timeout: 40000 });
  await page.waitForTimeout(3000);

  // Capture Screenshot 4: Cross-modal Mismatch Badge
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot4_mismatch_badge.png'),
    fullPage: false
  });
  console.log('Successfully captured screenshot4_mismatch_badge.png');

  await browser.close();
}

run().catch(err => {
  console.error('Error during capture:', err);
  process.exit(1);
});
