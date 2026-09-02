const { chromium } = require("./node_modules/playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const base = "http://localhost:3100";

  const routes = [
    "/", "/chat", "/detect", "/analytics", "/library", "/data",
    "/research", "/research/benchmark", "/research/methodology", "/research/safety",
    "/about", "/team", "/contact", "/auth", "/account", "/privacy"
  ];
  for (const route of routes) {
    const response = await desktop.goto(base + route, { waitUntil: "domcontentloaded" });
    if (!response || response.status() >= 400) throw new Error(`${route} returned ${response && response.status()}`);
  }

  // Navbar: helpline present, OPTIONAL auth link present (additive, never blocking).
  // Analytics lives in the "প্রকল্প" dropdown — open it and verify the link.
  await desktop.goto(base + "/");
  if (await desktop.locator('header a[href^="tel:"]').count() !== 1) throw new Error("Desktop helpline missing");
  if (await desktop.locator('header a[href="/auth"]').count() < 1) throw new Error("Optional auth pill missing from navbar");
  await desktop.getByRole("button", { name: /প্রকল্প/ }).click();
  if (await desktop.locator('header a[href="/analytics"]').count() < 1) throw new Error("Analytics link missing from projects dropdown");

  // /auth: login/register form present (optional auth), anonymous demo entries still present
  await desktop.goto(base + "/auth");
  await desktop.waitForSelector('input[type="password"]', { timeout: 8000 }).catch(() => {
    throw new Error("Auth form missing");
  });
  if (await desktop.locator('a[href="/detect"]').count() < 1) throw new Error("Auth demo detect action missing");

  // Mobile detect: sample action + photo input + slide-over advisory (no tabs on mobile)
  await mobile.goto(base + "/detect");
  await mobile.waitForTimeout(800);
  const sampleBtn = await mobile.getByRole("button", { name: /নমুনা/ }).count();
  if (sampleBtn < 1) throw new Error("Verified sample action missing");
  if (await mobile.locator('input[type="file"]').count() < 1) throw new Error("Detect photo input missing on mobile");
  const advisory = mobile.locator("button", { hasText: "কৃষি বিশেষজ্ঞ" });
  if (await advisory.count() < 1) throw new Error("Slide-over advisory trigger missing on mobile");
  await advisory.first().click();
  await mobile.waitForTimeout(600);
  if (await mobile.locator("textarea").count() < 1) throw new Error("Advisory drawer did not open on mobile");

  // Mobile: login entry reachable in the header without opening the hamburger menu
  if (await mobile.locator('header a[href="/auth"]').count() < 1) throw new Error("Mobile header login entry missing");

  // Research subnav + agent explorer
  await desktop.goto(base + "/research/methodology");
  if (await desktop.locator("nav[aria-label]").count() !== 1) throw new Error("Research subnav missing");
  if ((await desktop.getByText("চার-এজেন্ট উত্তর প্রবাহ").count()) < 1) throw new Error("Agent explorer missing");

  // Benchmark best-result badge
  await desktop.goto(base + "/research/benchmark");
  const starBadges = await desktop.getByText("সেরা ফলাফল").count();
  if (starBadges < 1) throw new Error("Best-result badge missing");

  // Analytics export + category breakdown
  await desktop.goto(base + "/analytics");
  await desktop.waitForTimeout(1200);
  const analyticsButtons = await desktop.locator("button").allTextContents();
  if (!analyticsButtons.some((text) => text.includes("JSON"))) throw new Error("Analytics export action missing");
  if (await desktop.getByText("শ্রেণী অনুযায়ী প্রশ্ন").count() < 1) throw new Error("Category breakdown missing");

  // BibTeX
  await desktop.goto(base + "/research");
  if (await desktop.locator("button").filter({ hasText: /BibTeX কপি/ }).count() < 1) throw new Error("BibTeX action missing");

  // 404
  const missing = await desktop.goto(base + "/this-route-does-not-exist", { waitUntil: "domcontentloaded" });
  if (!missing || missing.status() !== 404) throw new Error("404 status verification failed");
  if (await desktop.locator('a[href="/detect"]').count() < 1) throw new Error("404 detect action missing");
  if (await desktop.locator('a[href="/"]').count() < 1) throw new Error("404 home action missing");

  console.log("ALL BROWSER SMOKE CHECKS PASSED");
  await browser.close();
})().catch((error) => {
  console.error("SMOKE TEST FAILED:", error.message);
  process.exit(1);
});
