#!/usr/bin/env node
/**
 * Browser WASM latency — Playwright measurement of on-device vision.
 * If dev server or playwright is unavailable, writes UNMEASURED placeholder
 * (honest per AGENTS.md rule 5) instead of reusing Python ORT-CPU numbers.
 */
import { writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../..");
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "results_real_browser_latency.json");
const DEV_URL = process.env.PLAYWRIGHT_URL || "http://localhost:3000";
const MODELS = ["crop_classifier", "potato", "rice", "wheat", "corn", "brassica"];

async function tryDevServer() {
  try {
    const res = await fetch(`${DEV_URL}/detect`, { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}

async function main() {
  let devOk = await tryDevServer();
  let playwrightAvailable = false;
  try {
    await import("playwright");
    playwrightAvailable = true;
  } catch {
    try {
      await import(path.join(REPO, "frontend", "node_modules", "playwright", "lib", "cjs", "index.js"));
      playwrightAvailable = true;
    } catch {}
  }
  if (!devOk || !playwrightAvailable) {
    const placeholder = {
      benchmark_name: "EACL_E02_BROWSER_WASM_LATENCY",
      execution_status: "UNMEASURED",
      reason: !devOk ? `dev server not reachable at ${DEV_URL} — run pnpm dev in frontend/ and re-run` : "playwright not available",
      note: "Do NOT reuse Python ORT-CPU latency (CPUExecutionProvider) as browser latency (WASM single-thread). Browser numbers require live chromium + WASM. Python numbers: crop 5.45ms / potato 13.36ms / rice 8.33ms / wheat 4.62ms / brassica 20.46ms (see results_real_onnx_parity.json).",
      run_at_utc: new Date().toISOString(),
      models: Object.fromEntries(MODELS.map(k => [k, {status: "unmeasured", reason: "needs live browser WASM run"}])),
    };
    await writeFile(OUT, JSON.stringify(placeholder, null, 2) + "\n", "utf-8");
    console.log(`[UNMEASURED] wrote ${OUT} — devOk=${devOk} playwright=${playwrightAvailable}`);
    return;
  }
  // If both available, we would launch chromium and measure — placeholder for now
  const placeholder = {
    benchmark_name: "EACL_E02_BROWSER_WASM_LATENCY",
    execution_status: "UNMEASURED_STUB",
    reason: "Playwright wiring present but measurement needs a sample image File injection — run with dev server and sample under paper planning",
    run_at_utc: new Date().toISOString(),
  };
  await writeFile(OUT, JSON.stringify(placeholder, null, 2) + "\n", "utf-8");
  console.log(`[STUB] wrote ${OUT}`);
}
main();