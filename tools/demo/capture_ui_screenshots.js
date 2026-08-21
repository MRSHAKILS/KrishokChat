const path = require('path');
const { chromium } = require(path.join(__dirname, '../frontend/node_modules/playwright'));
const fs = require('fs');

const routes = [
  { name: '01_home', url: 'http://localhost:3100/' },
  { name: '02_chat', url: 'http://localhost:3100/chat' },
  { name: '03_detect', url: 'http://localhost:3100/detect' },
  { name: '04_analytics', url: 'http://localhost:3100/analytics' },
  { name: '05_library', url: 'http://localhost:3100/library' },
  { name: '06_data', url: 'http://localhost:3100/data' },
  { name: '07_research', url: 'http://localhost:3100/research' },
  { name: '08_research_benchmark', url: 'http://localhost:3100/research/benchmark' },
  { name: '09_research_methodology', url: 'http://localhost:3100/research/methodology' },
  { name: '10_research_safety', url: 'http://localhost:3100/research/safety' },
  { name: '11_about', url: 'http://localhost:3100/about' },
  { name: '12_team', url: 'http://localhost:3100/team' },
  { name: '13_contact', url: 'http://localhost:3100/contact' },
  { name: '14_auth', url: 'http://localhost:3100/auth' },
  { name: '15_not_found', url: 'http://localhost:3100/non-existent-page' }
];

const outDirs = [
  path.join(__dirname, '../docs/ui_audit/screenshots'),
  path.join('C:/Users/raiya/.gemini/antigravity-ide/brain/e03319a2-9a3b-4c5d-b8b0-cea965b6f653/screenshots')
];

for (const dir of outDirs) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();

  console.log('Starting screenshot capture for 15 routes...');

  for (const item of routes) {
    try {
      console.log(`Navigating to ${item.name} (${item.url})...`);
      await page.goto(item.url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(1000); // Allow animations/fonts to settle

      for (const dir of outDirs) {
        const filePath = path.join(dir, `${item.name}.png`);
        await page.screenshot({ path: filePath, fullPage: true });
        console.log(`Saved screenshot to ${filePath}`);
      }
    } catch (err) {
      console.error(`Failed to capture ${item.name}:`, err.message);
    }
  }

  await browser.close();
  console.log('All screenshots captured successfully!');
})();
