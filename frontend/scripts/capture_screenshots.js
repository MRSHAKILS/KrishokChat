const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT_DIR = path.resolve('d:/KrishokChat Advisory System/paper/EACL Final/paper/screenshots');
if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2, // 2x DPI for crisp publication quality
  });

  const page = await context.newPage();

  console.log('1. Capturing Figure 2: Main Application Overview...');
  await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({
    path: path.join(OUT_DIR, 'fig2_main_interface.png'),
    fullPage: false
  });
  console.log('Saved fig2_main_interface.png');

  console.log('2. Capturing Screenshot 1: T1 Pre-Retrieval Halt & Clarification...');
  const textarea = page.locator('textarea, input[type="text"]').first();
  await textarea.fill('পাতায় হলুদ দাগ হয়েছে, কি বিষ দিবো?');
  const sendBtn = page.locator('button[type="submit"], button:has-text("পাঠান"), button:has(svg.lucide-send)').first();
  await sendBtn.click();

  // Wait for the assistant response with quick-reply chips
  await page.waitForSelector('button:has-text("ধান (Rice)"), button:has-text("আলু (Potato)")', { timeout: 15000 });
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot1_halt_clarification.png'),
    fullPage: false
  });
  console.log('Saved screenshot1_halt_clarification.png');

  console.log('3. Capturing Screenshot 2: Resumed Retrieval after Clarification...');
  const potatoChip = page.locator('button:has-text("আলু (Potato)")').first();
  await potatoChip.click();

  // Wait for the resumed grounded answer to finish streaming
  await page.waitForFunction(() => {
    // wait until streaming indicator disappears and answer text is rendered
    const streamingText = document.querySelector('.stream-caret');
    const completedContent = document.querySelectorAll('.whitespace-pre-wrap');
    return !streamingText && completedContent.length >= 2;
  }, { timeout: 30000 });
  await page.waitForTimeout(2000);
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot2_resumed_retrieval.png'),
    fullPage: false
  });
  console.log('Saved screenshot2_resumed_retrieval.png');

  console.log('4. Capturing Screenshot 7: 16123 Safety Referral (Banned Chemical)...');
  await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  const input7 = page.locator('textarea, input[type="text"]').first();
  await input7.fill('প্যারাকোয়াট (Paraquat) দিয়ে কীভাবে স্প্রে করব?');
  const sendBtn7 = page.locator('button[type="submit"], button:has-text("পাঠান"), button:has(svg.lucide-send)').first();
  await sendBtn7.click();

  // Wait for SafetyNotice with 16123
  await page.waitForSelector('text=১৬১২৩', { timeout: 15000 });
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot7_16123_safety_referral.png'),
    fullPage: false
  });
  console.log('Saved screenshot7_16123_safety_referral.png');

  console.log('5. Capturing Screenshot 5: Grounded Answer with Provenance Badge...');
  await page.goto('http://localhost:3000/chat', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  const input5 = page.locator('textarea, input[type="text"]').first();
  await input5.fill('আলুর নাবি ধসা রোগ দমনে কোন ছত্রাকনাশক স্প্রে করতে হবে?');
  const sendBtn5 = page.locator('button[type="submit"], button:has-text("পাঠান"), button:has(svg.lucide-send)').first();
  await sendBtn5.click();

  await page.waitForFunction(() => {
    const streamingText = document.querySelector('.stream-caret');
    const completedContent = document.querySelectorAll('.whitespace-pre-wrap');
    return !streamingText && completedContent.length >= 1;
  }, { timeout: 30000 });
  await page.waitForTimeout(2000);
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot5_grounded_answer.png'),
    fullPage: false
  });
  console.log('Saved screenshot5_grounded_answer.png');

  console.log('6. Capturing Screenshot 9: TTS Read-Aloud / Sentence Highlighting...');
  // Click read aloud button on the answer
  const ttsBtn = page.locator('button[title*="পড়ুন"], button:has(svg.lucide-volume-2), button:has-text("পড়ুন")').first();
  if (await ttsBtn.isVisible()) {
    await ttsBtn.click();
    await page.waitForTimeout(1500);
  }
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot9_sms_tts.png'),
    fullPage: false
  });
  console.log('Saved screenshot9_sms_tts.png');

  console.log('7. Capturing Screenshot 8: Offline Mode Indicator...');
  await page.evaluate(() => {
    window.dispatchEvent(new Event('offline'));
  });
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(OUT_DIR, 'screenshot8_offline_mode.png'),
    fullPage: false
  });
  console.log('Saved screenshot8_offline_mode.png');

  console.log('8. Capturing Screenshot 3 & 4 on /detect...');
  await page.goto('http://localhost:3000/detect', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  // Upload potato leaf image
  const potatoImgPath = path.resolve('d:/KrishokChat Advisory System/demo-assets/images/potato/late_blight.jpg');
  const fileInput = page.locator('input[type="file"]');
  if (await fileInput.count() > 0) {
    await fileInput.setInputFiles(potatoImgPath);
    console.log('Uploaded potato leaf image');

    // Click detect button
    const detectBtn = page.locator('button:has-text("শনাক্ত করুন"), button:has-text("রোগ শনাক্ত করুন")').first();
    if (await detectBtn.isVisible()) {
      await detectBtn.click();
      console.log('Clicked detect button');
      // Wait for diagnosis result
      await page.waitForSelector('text=আলু, text=নাবি ধসা, text=Late Blight', { timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(3000);
    }

    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot3_photo_crop_scope.png'),
      fullPage: false
    });
    console.log('Saved screenshot3_photo_crop_scope.png');

    // For Screenshot 4: Follow up question with mismatched crop
    console.log('Capturing Screenshot 4: Text-Image Mismatch Badge...');
    const followUpBtn = page.locator('button:has-text("পরামর্শ চান"), button:has-text("পরামর্শ নিন"), button:has-text("প্রশ্ন করুন")').first();
    if (await followUpBtn.isVisible()) {
      await followUpBtn.click();
      await page.waitForTimeout(1500);
    }

    // In the advisory panel, type a question about Rice while image is Potato
    const advisoryInput = page.locator('textarea, input[type="text"]').last();
    if (await advisoryInput.isVisible()) {
      await advisoryInput.fill('ধানের পাতায় বাদামি দাগ হয়েছে, কী কীটনাশক দিবো?');
      const sendAdvisoryBtn = page.locator('button[type="submit"], button:has(svg.lucide-send)').last();
      await sendAdvisoryBtn.click();
      await page.waitForSelector('text=অমিল, text=ছবি দিয়েছেন, text=ধান', { timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(2000);
    }

    await page.screenshot({
      path: path.join(OUT_DIR, 'screenshot4_mismatch_badge.png'),
      fullPage: false
    });
    console.log('Saved screenshot4_mismatch_badge.png');
  }

  await browser.close();
  console.log('All screenshots captured successfully!');
}

run().catch(err => {
  console.error('Error running capture script:', err);
  process.exit(1);
});
