#!/usr/bin/env node
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { writeFile } from "node:fs/promises";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../..");
const PUBLIC = path.join(REPO, "frontend", "public");
const ORT_DIST = path.join(REPO, "frontend", "node_modules", "onnxruntime-web", "dist");
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "results_real_browser_latency.json");

function mime(p) {
  if (p.endsWith(".wasm")) return "application/wasm";
  if (p.endsWith(".mjs") || p.endsWith(".js")) return "application/javascript";
  if (p.endsWith(".json")) return "application/json";
  if (p.endsWith(".onnx")) return "application/octet-stream";
  return "text/plain";
}

function startStatic(port = 0) {
  return new Promise((resolve) => {
    const srv = createServer(async (req, res) => {
      let url = decodeURIComponent(req.url.split("?")[0]);
      let filePath;
      if (url.startsWith("/models/")) filePath = path.join(PUBLIC, url);
      else if (url.startsWith("/ort/")) filePath = path.join(ORT_DIST, url.slice(5));
      else if (url === "/" || url === "/blank") {
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(`<!doctype html><html><body>blank</body></html>`);
        return;
      } else {
        res.writeHead(404); res.end("not found"); return;
      }
      try {
        const st = await stat(filePath);
        if (st.isDirectory()) { res.writeHead(404); res.end("dir"); return; }
        const data = await readFile(filePath);
        res.writeHead(200, { "Content-Type": mime(filePath), "Content-Length": data.length, "Access-Control-Allow-Origin": "*" });
        res.end(data);
      } catch {
        res.writeHead(404); res.end("not found");
      }
    });
    srv.listen(port, "127.0.0.1", () => resolve(srv));
  });
}

async function main() {
  const srv = await startStatic(0);
  const addr = srv.address();
  const base = `http://127.0.0.1:${addr.port}`;
  console.log(`static ${base} -> PUBLIC/models + ORT_DIST`);

  let playwright;
  try {
    const { createRequire } = await import("node:module");
    const require = createRequire(path.join(REPO, "frontend", "package.json"));
    playwright = require("playwright");
  } catch (e) {
    console.log("playwright not available:", e.message);
    srv.close();
    const placeholder = {
      benchmark_name: "EACL_E02_BROWSER_WASM_LATENCY",
      execution_status: "UNMEASURED",
      reason: "playwright not available: " + e.message,
      note: "Do NOT reuse Python ORT-CPU numbers. Run pnpm dev + Playwright for real browser WASM.",
      run_at_utc: new Date().toISOString(),
    };
    await writeFile(OUT, JSON.stringify(placeholder, null, 2) + "\n", "utf-8");
    return;
  }

  const chromium = playwright.chromium || playwright.default?.chromium;
  if (!chromium) {
    console.log("no chromium");
    srv.close();
    return;
  }
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`${base}/blank`, { waitUntil: "domcontentloaded" });
  const result = await page.evaluate(async (base) => {
    const ort = await import(`${base}/ort/ort.wasm.bundle.min.mjs`);
    const env = ort.env || ort.default?.env;
    if (env?.wasm) { env.wasm.numThreads = 1; env.wasm.simd = true; }
    const models = [
      { key: "crop_classifier", file: "crop_classifier.onnx", shape: [1,3,224,224] },
      { key: "potato", file: "potato.onnx", shape: [1,3,224,224] },
      { key: "wheat", file: "wheat.onnx", shape: [1,3,224,224] },
      { key: "brassica", file: "brassica.onnx", shape: [1,3,256,256] },
      { key: "rice", file: "rice.onnx", shape: [1,3,320,320] },
      { key: "corn", file: "corn.onnx", shape: [1,3,256,256] },
    ];
    const out = {};
    for (const m of models) {
      const url = `${base}/models/${m.file}`;
      const session = await ort.InferenceSession.create(url, { executionProviders: ["wasm"], graphOptimizationLevel: "all" });
      const inputName = session.inputNames[0];
      const size = m.shape.reduce((a,b)=>a*b,1);
      const data = new Float32Array(size);
      for (let i=0;i<size;i++) data[i]=Math.random();
      const tensor = new ort.Tensor("float32", data, m.shape);
      for (let i=0;i<5;i++) await session.run({[inputName]: tensor});
      const N=20;
      const times=[];
      for (let i=0;i<N;i++) {
        const t0=performance.now();
        await session.run({[inputName]: tensor});
        times.push(performance.now()-t0);
      }
      times.sort((a,b)=>a-b);
      const p50=times[Math.floor(times.length*0.5)];
      const p95=times[Math.floor(times.length*0.95)];
      out[m.key] = { p50_ms: Math.round(p50*100)/100, p95_ms: Math.round(p95*100)/100, n: N, shape: m.shape, input: inputName };
    }
    return { models: out, envWasm: env?.wasm ? { numThreads: env.wasm.numThreads, simd: env.wasm.simd, crossOriginIsolated: self.crossOriginIsolated } : null };
  }, base);

  await browser.close();
  srv.close();

  const report = {
    benchmark_name: "EACL_E02_BROWSER_WASM_LATENCY",
    execution_status: "DONE_REAL",
    run_at_utc: new Date().toISOString(),
    static_server: base,
    note: "Browser WASM single-thread (numThreads 1, SIMD true, crossOriginIsolated false). Inference-only (random tensor, preprocessing excluded). Python ORT-CPU is session.run only as well — comparable but distinct runtime (CPUExecutionProvider vs WASM). Do not reuse Python numbers as browser numbers, but both are now measured.",
    result,
  };
  await writeFile(OUT, JSON.stringify(report, null, 2) + "\n", "utf-8");
  console.log(`[OK] wrote ${OUT}`, JSON.stringify(result, null, 2).slice(0, 800));
}

main().catch(async e => {
  console.error(e);
  try {
    const { writeFile } = await import("node:fs/promises");
    const path = await import("node:path");
    const { fileURLToPath } = await import("node:url");
    const OUT2 = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "results_real_browser_latency.json");
    await writeFile(OUT2, JSON.stringify({ benchmark_name: "EACL_E02_BROWSER_WASM_LATENCY", execution_status: "ERROR", error: String(e), run_at_utc: new Date().toISOString() }, null, 2) + "\n", "utf-8");
  } catch {}
});
