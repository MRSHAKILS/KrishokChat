/**
 * Quick smoke test for backend API endpoints.
 * Run with: npx tsx scripts/test_api.ts (or compile first)
 * We use plain fetch via Node.
 */
const BASE = "http://localhost:8000";

async function testHealth() {
  const r = await fetch(`${BASE}/health`);
  console.log("GET /health", r.status, await r.json());
}

async function testClassify() {
  // Create a tiny 1x1 PNG
  const png = Buffer.from(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M8AAAMBAQDJ/IjIAAAAAElFTkSuQmCC",
    "base64"
  );
  const blob = new Blob([png], { type: "image/png" });
  const form = new FormData();
  form.append("file", blob as any, "test.png");
  const r = await fetch(`${BASE}/api/classify`, { method: "POST", body: form });
  console.log("POST /api/classify", r.status, await r.json());
}

async function testQA() {
  const r = await fetch(`${BASE}/api/qa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: "test" }),
  });
  console.log("POST /api/qa", r.status, (await r.json()).category);
}

async function main() {
  await testHealth();
  await testClassify();
  await testQA();
}

main().catch(console.error);
