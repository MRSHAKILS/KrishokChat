const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = [];
  p.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  p.on("pageerror", e => errs.push("PAGEERROR: " + e.message));

  await p.goto("http://localhost:3000", { waitUntil: "networkidle" });
  console.log("TITLE:", await p.title());
  console.log("TABS:", await p.locator('[data-slot="tabs-trigger"]').allInnerTexts());

  await p.screenshot({ path: "C:/Users/raiya/AppData/Local/Temp/opencode/s1-detect.png" });

  await p.getByRole("tab", { name: "প্রশ্ন করুন" }).click();
  await p.waitForTimeout(400);
  await p.screenshot({ path: "C:/Users/raiya/AppData/Local/Temp/opencode/s2-qa.png" });
  console.log("ERRORS:", JSON.stringify(errs));
  await b.close();
})();
