const { chromium } = require("./node_modules/playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const base = "http://localhost:3100";

  const routes = [
    "/", "/chat", "/detect", "/analytics", "/library", "/data",
    "/research", "/research/benchmark", "/research/methodology", "/research/safety",
    "/about", "/team", "/contact", "/auth"
  ];
  for (const route of routes) {
    const response = await desktop.goto(base + route, { waitUntil: "domcontentloaded" });
    if (!response || response.status() >= 400) throw new Error(`${route} returned ${response && response.status()}`);
  }

  // Navbar: analytics link present, helpline present, NO auth link
  await desktop.goto(base + "/");
  if (await desktop.locator('header a[href="/analytics"]').count() !== 1) throw new Error("Analytics nav link missing");
  if (await desktop.locator('header a[href^="tel:"]').count() !== 1) throw new Error("Desktop helpline missing");
  if (await desktop.locator('header a[href="/auth"]').count() !== 0) throw new Error("Auth link remains in navbar");

  // /auth: no password field, has demo detect action
  await desktop.goto(base + "/auth");
  if (await desktop.locator('input[type="password"]').count() !== 0) throw new Error("Auth form still rendered");
  if (await desktop.locator('a[href="/detect"]').count() < 1) throw new Error("Auth demo detect action missing");

  // Mobile detect: tabs + sample action
  await mobile.goto(base + "/detect");
  if (await mobile.getByRole("tab").count() !== 2) throw new Error("Detect tab switcher missing, got " + (await mobile.getByRole("tab").count()));
  const sampleBtn = await mobile.getByRole("button", { name: /নমুনা/ }).count();
  if (sampleBtn < 1) throw new Error("Verified sample action missing");
  await mobile.getByRole("tab").nth(1).click();
  if (await mobile.locator("textarea").count() !== 1) throw new Error("Chat pane did not open on mobile");
  await mobile.getByRole("tab").nth(0).click();
  if (await mobile.locator('input[type="file"]').count() < 1) throw new Error("Detect pane did not reopen");

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
