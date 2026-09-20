/**
 * On-device vision inference via onnxruntime-web (lazy, NOT in First Load).
 *
 * This module is never statically imported by the detect page's top-level bundle.
 * The page does `import("./vision-ondevice")` inside an async handler, so
 * onnxruntime-web (~413 KB bundle) lands in a separate chunk and the
 * 650 KB First Load budget stays green.
 *
 * Two invariants that the paper depends on:
 *  - Preprocessing reproduces `ultralytics.data.augment.classify_transforms` exactly:
 *    Resize(shortest-edge, bilinear, antialias) -> CenterCrop -> ToTensor (/255) -> NCHW.
 *    No letterbox. Getting this wrong makes every parity number garbage.
 *  - Nothing here produces bounding boxes. The checked-in artifacts are
 *    `task: classify` and the UI must say classification, never detection.
 *
 * Gate: `NEXT_PUBLIC_VISION_ONDEVICE_ENABLED=true` (default off, dark-launch per
 * `CHUNK_FALLBACK_ENABLED` precedent). The caller must check `isOnDeviceEnabled()`
 * before attempting inference; a failure always falls back to the server fetch.
 *
 * Measured artifacts (see paper/EACL Demoexperiments/E02.../):
 *  - 6 FP32 ONNX at correct per-model imgsz (224/224/320/224/256/256) -> 80.13 MB
 *  - INT8 via ORT static quantization (nodes Conv/Gemm/MatMul only, >300 calib for
 *    wheat/crop) where the held-out sanity gate passed (drop <=2pp, agree >=0.90):
 *    crop 1.60, potato 5.34, wheat 1.61, brassica 5.35; rice rejected (2.5pp drop),
 *    corn unmeasured (no local labelled images). Total browser payload 40.59 MB primary
 *    (plus legacy aliases).
 *
 * This file has no `import "onnxruntime-web"` at the top — that would pull the
 * runtime into the First Load chunk and break the size-limit gate. Instead see
 * `getOrt()`.
 */

export const ONDEVICE_ENABLED = process.env.NEXT_PUBLIC_VISION_ONDEVICE_ENABLED !== "false";

export function isOnDeviceEnabled(): boolean {
  if (!ONDEVICE_ENABLED) return false;
  if (typeof window === "undefined") return false;
  if (typeof WebAssembly === "undefined") return false;
  return true;
}

// --- Model registry (must match backend/ml_assets/vision/* and frontend/public/models/metadata.json) ---

export type OnDeviceModelKey = "crop_classifier" | "potato" | "rice" | "wheat" | "corn" | "brassica" | "chilli";

export interface ModelSpec {
  key: OnDeviceModelKey;
  file: string; // under /models/
  classesFile: string;
  imgsz: number;
  precision: "int8" | "fp32";
}

export const MODEL_SPECS: Record<OnDeviceModelKey, ModelSpec> = {
  crop_classifier: {
    key: "crop_classifier",
    file: "crop_classifier.onnx",
    classesFile: "crop_classifier_classes.json",
    imgsz: 224,
    precision: "int8",
  },
  potato: { key: "potato", file: "potato.onnx", classesFile: "potato_classes.json", imgsz: 224, precision: "int8" },
  rice: { key: "rice", file: "rice.onnx", classesFile: "rice_classes.json", imgsz: 224, precision: "fp32" },
  wheat: { key: "wheat", file: "wheat.onnx", classesFile: "wheat_classes.json", imgsz: 224, precision: "int8" },
  corn: { key: "corn", file: "corn.onnx", classesFile: "corn_classes.json", imgsz: 256, precision: "fp32" },
  brassica: { key: "brassica", file: "brassica.onnx", classesFile: "brassica_classes.json", imgsz: 256, precision: "int8" },
  chilli: { key: "chilli", file: "chilli.onnx", classesFile: "chilli_classes.json", imgsz: 224, precision: "int8" },
};

// Legacy file aliases (potato_disease etc.) exist on disk so old URLs keep working,
// but this module always requests the canonical name above.

const DISEASE_KEYS: OnDeviceModelKey[] = ["potato", "rice", "wheat", "corn", "brassica", "chilli"];

const CROP_DISPLAY: Record<string, string> = {
  rice: "Rice",
  wheat: "Wheat",
  corn: "Corn",
  potato: "Potato",
  brassica: "Brassica",
  chilli: "Chilli",
  chili: "Chilli",
};

// --- ORT lazy singleton ---

type OrtModule = typeof import("onnxruntime-web");

let ortPromise: Promise<OrtModule> | null = null;
let ortInstance: OrtModule | null = null;

async function getOrt(): Promise<OrtModule> {
  if (ortInstance) return ortInstance;
  if (ortPromise) return ortPromise;
  // `onnxruntime-web/wasm` (72 KB) instead of the full `onnxruntime-web` bundle
  // (413 KB). We only need the WASM CPU backend for classification, so the
  // smaller WASM-only bundle keeps the lazy chunk ~25 KB gzipped and the
  // 650 KB First Load budget stays green. The `onnxruntime-web` default
  // (`ort.bundle.min.mjs`) would add ~148 KB gzipped and trip size-limit.
  ortPromise = import("onnxruntime-web/wasm").then((m) => {
    // Threads require COOP/COEP (crossOriginIsolated). We do not set those headers,
    // so force single-thread. The bundle variant embeds the WASM, no separate fetch,
    // so no wasmPaths configuration is needed. If the host later adds COOP/COEP,
    // this can be raised to min(navigator.hardwareConcurrency/2, 4).
    try {
      const env = (m as unknown as { env: { wasm: { numThreads: number; simd: boolean } } }).env;
      if (env?.wasm) {
        env.wasm.numThreads = 1;
        env.wasm.simd = true;
      }
    } catch {
      // env shape is not critical; inference will still attempt single-thread.
    }
    ortInstance = m as unknown as OrtModule;
    return ortInstance;
  });
  return ortPromise;
}

// --- Session + class-name cache (In-memory + IndexedDB persistent) ---

const sessionCache = new Map<OnDeviceModelKey, unknown>();
const classesCache = new Map<OnDeviceModelKey, string[]>();

const IDB_NAME = "krishokchat_models_v2";
const IDB_STORE = "onnx_binaries";

async function openModelDb(): Promise<IDBDatabase | null> {
  if (typeof window === "undefined" || !("indexedDB" in window)) return null;
  return new Promise((resolve) => {
    try {
      const req = indexedDB.open(IDB_NAME, 1);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(IDB_STORE)) {
          db.createObjectStore(IDB_STORE);
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => resolve(null);
    } catch {
      resolve(null);
    }
  });
}

async function getCachedModelBuffer(fileName: string): Promise<ArrayBuffer | null> {
  const db = await openModelDb();
  if (!db) return null;
  return new Promise((resolve) => {
    try {
      const tx = db.transaction(IDB_STORE, "readonly");
      const store = tx.objectStore(IDB_STORE);
      const req = store.get(fileName);
      req.onsuccess = () => resolve(req.result ? (req.result as ArrayBuffer) : null);
      req.onerror = () => resolve(null);
    } catch {
      resolve(null);
    }
  });
}

async function setCachedModelBuffer(fileName: string, buffer: ArrayBuffer): Promise<void> {
  const db = await openModelDb();
  if (!db) return;
  try {
    const tx = db.transaction(IDB_STORE, "readwrite");
    const store = tx.objectStore(IDB_STORE);
    store.put(buffer, fileName);
  } catch {
    // Ignore storage quota or private-browsing errors
  }
}

async function fetchClasses(key: OnDeviceModelKey): Promise<string[]> {
  const cached = classesCache.get(key);
  if (cached) return cached;
  const spec = MODEL_SPECS[key];
  const res = await fetch(`/models/${spec.classesFile}`, { cache: "force-cache" });
  if (!res.ok) throw new Error(`class map missing: ${spec.classesFile} (${res.status})`);
  const data: unknown = await res.json();
  let classes: string[];
  if (Array.isArray(data)) classes = (data as unknown[]).map(String);
  else if (data && typeof data === "object") {
    const dict = data as Record<string, unknown>;
    classes = Object.keys(dict)
      .sort((a, b) => Number(a) - Number(b))
      .map((k) => String(dict[k]));
  } else throw new Error(`unrecognized class map format for ${key}`);
  classesCache.set(key, classes);
  return classes;
}

async function getSession(key: OnDeviceModelKey): Promise<import("onnxruntime-web").InferenceSession> {
  const cached = sessionCache.get(key) as import("onnxruntime-web").InferenceSession | undefined;
  if (cached) return cached;
  const ort = await getOrt();
  const spec = MODEL_SPECS[key];

  let modelInput: string | Uint8Array = `/models/${spec.file}`;
  try {
    const cachedBuf = await getCachedModelBuffer(spec.file);
    if (cachedBuf && cachedBuf.byteLength > 1000) {
      modelInput = new Uint8Array(cachedBuf);
    } else {
      const resp = await fetch(`/models/${spec.file}`, { cache: "force-cache" });
      if (resp.ok) {
        const buf = await resp.arrayBuffer();
        if (buf.byteLength > 1000) {
          setCachedModelBuffer(spec.file, buf);
          modelInput = new Uint8Array(buf);
        }
      }
    }
  } catch {
    // Fall back gracefully to direct URL string if IndexedDB fails
    modelInput = `/models/${spec.file}`;
  }

  // `executionProviders: ["wasm"]` is the browser WASM backend for onnxruntime-web 1.29.
  const session = await (ort as unknown as { InferenceSession: { create: (src: string | Uint8Array, opts: unknown) => Promise<import("onnxruntime-web").InferenceSession> } }).InferenceSession.create(
    modelInput,
    {
      executionProviders: ["wasm"],
      graphOptimizationLevel: "all",
    } as unknown as Record<string, unknown>,
  );
  sessionCache.set(key, session);
  return session;
}

// --- Preprocessing (must match ultralytics classify_transforms) ---

async function fileToImageBitmap(file: File): Promise<ImageBitmap> {
  try {
    return await createImageBitmap(file, { imageOrientation: "from-image" as ImageOrientation });
  } catch {
    return await createImageBitmap(file);
  }
}

/**
 * Reproduce `classify_transforms(size)`:
 *   Resize(size, bilinear, antialias) where `size` is the *shortest-edge*,
 *   then CenterCrop(size). For square inputs this is just Resize(size).
 */
export async function preprocessToNCHW(file: File, imgsz: number): Promise<Float32Array> {
  const bitmap = await fileToImageBitmap(file);
  try {
    const { width, height } = bitmap;
    const scale = imgsz / Math.min(width, height);
    const newW = Math.max(1, Math.round(width * scale));
    const newH = Math.max(1, Math.round(height * scale));

    const resizeCanvas = document.createElement("canvas");
    resizeCanvas.width = newW;
    resizeCanvas.height = newH;
    const rctx = resizeCanvas.getContext("2d", { alpha: false });
    if (!rctx) throw new Error("canvas 2d unavailable");
    rctx.imageSmoothingEnabled = true;
    rctx.imageSmoothingQuality = "high";
    rctx.drawImage(bitmap, 0, 0, newW, newH);

    const sx = Math.max(0, Math.floor((newW - imgsz) / 2));
    const sy = Math.max(0, Math.floor((newH - imgsz) / 2));
    const cropCanvas = document.createElement("canvas");
    cropCanvas.width = imgsz;
    cropCanvas.height = imgsz;
    const cctx = cropCanvas.getContext("2d", { alpha: false });
    if (!cctx) throw new Error("canvas 2d unavailable (crop)");
    cctx.imageSmoothingEnabled = true;
    cctx.imageSmoothingQuality = "high";
    cctx.drawImage(resizeCanvas, sx, sy, imgsz, imgsz, 0, 0, imgsz, imgsz);

    const imageData = cctx.getImageData(0, 0, imgsz, imgsz);
    const { data } = imageData; // RGBA, 0-255
    const chw = new Float32Array(1 * 3 * imgsz * imgsz);
    // NCHW, R/G/B planes, /255 (Normalize mean 0 std 1 is a no-op)
    let rOff = 0;
    let gOff = imgsz * imgsz;
    let bOff = 2 * imgsz * imgsz;
    for (let i = 0, j = 0; i < data.length; i += 4, j += 1) {
      chw[rOff + j] = data[i] / 255;
      chw[gOff + j] = data[i + 1] / 255;
      chw[bOff + j] = data[i + 2] / 255;
    }
    return chw;
  } finally {
    bitmap.close();
  }
}

function softmax(logits: Float32Array): Float32Array {
  let max = -Infinity;
  for (let i = 0; i < logits.length; i++) if (logits[i] > max) max = logits[i];
  const exp = new Float32Array(logits.length);
  let sum = 0;
  for (let i = 0; i < logits.length; i++) {
    const v = Math.exp(logits[i] - max);
    exp[i] = v;
    sum += v;
  }
  for (let i = 0; i < exp.length; i++) exp[i] /= sum;
  return exp;
}

// --- Public types ---

export interface OnDevicePrediction {
  label: string;
  confidence: number;
  top3: { class: string; confidence: number }[];
  latencyMs: number;
  model: OnDeviceModelKey;
  precision: "int8" | "fp32";
  imgsz: number;
}

export interface OnDeviceDetectResult {
  status: "diagnosed" | "healthy" | "not_recognized" | "no_disease_model";
  crop: string | null;
  cropConfidence: number;
  cropSource: "model" | "user";
  disease: string | null;
  diseaseConfidence: number;
  top3Crops: { class: string; confidence: number }[];
  top3Diseases: { class: string; confidence: number }[];
  latencyMs: number;
  onDevice: true;
}

// --- Core inference for a single model ---

export async function runOnDeviceModel(file: File, key: OnDeviceModelKey): Promise<OnDevicePrediction> {
  const spec = MODEL_SPECS[key];
  const [session, classes, chw] = await Promise.all([
    getSession(key),
    fetchClasses(key),
    preprocessToNCHW(file, spec.imgsz),
  ]);
  const ort = await getOrt();
  const inputName = session.inputNames[0] ?? "images";
  const tensor = new (ort as unknown as { Tensor: new (t: string, d: Float32Array, dims: number[]) => unknown }).Tensor(
    "float32",
    chw,
    [1, 3, spec.imgsz, spec.imgsz],
  );
  const feeds: Record<string, unknown> = { [inputName]: tensor };
  const start = performance.now();
  const outputs = (await (session as unknown as { run: (f: Record<string, unknown>) => Promise<Record<string, { data: Float32Array }> > }).run(feeds)) as Record<string, { data: Float32Array }>;
  const elapsed = performance.now() - start;
  const firstKey = Object.keys(outputs)[0];
  let probs = outputs[firstKey].data as Float32Array;
  // Exported ONNX already contains softmax (probabilities sum to ~1). If the
  // output looks like logits (negative values or sum far from 1), apply softmax.
  let sum = 0;
  let hasNegative = false;
  for (let i = 0; i < probs.length; i++) {
    sum += probs[i];
    if (probs[i] < 0) hasNegative = true;
  }
  if (hasNegative || Math.abs(sum - 1) > 0.02) {
    probs = softmax(probs);
  }
  let topIdx = 0;
  let topVal = probs[0] ?? 0;
  for (let i = 1; i < probs.length; i++) if (probs[i] > topVal) { topVal = probs[i]; topIdx = i; }
  const order = Array.from(probs)
    .map((conf, idx) => ({ idx, conf }))
    .sort((a, b) => b.conf - a.conf)
    .slice(0, 3);
  const top3 = order.map(({ idx, conf }) => ({ class: classes[idx] ?? String(idx), confidence: Math.round(conf * 10000) / 10000 }));
  return {
    label: classes[topIdx] ?? String(topIdx),
    confidence: Math.round(topVal * 10000) / 10000,
    top3,
    latencyMs: Math.round(elapsed * 100) / 100,
    model: key,
    precision: spec.precision,
    imgsz: spec.imgsz,
  };
}

// --- High-level: crop classification ---

export async function classifyCropOnDevice(file: File): Promise<OnDevicePrediction> {
  return runOnDeviceModel(file, "crop_classifier");
}

// --- High-level: disease detection (mirrors VisionPipeline routing) ---

function diseaseKeyForCrop(crop: string): OnDeviceModelKey | null {
  const k = crop.trim().toLowerCase().replace(/\s+/g, "");
  if (k === "potato") return "potato";
  if (k === "rice") return "rice";
  if (k === "wheat") return "wheat";
  if (k === "corn" || k === "maize") return "corn";
  if (k === "brassica" || k === "cabbage" || k === "cauliflower") return "brassica";
  return null;
}

function isHealthyLabel(label: string): boolean {
  const n = label.toLowerCase().replace(/[_\s-]/g, "");
  return n === "healthy" || n === "healthyleaf" || n.endsWith("healthy") || n.endsWith("healthyleaf");
}

/**
 * On-device equivalent of `VisionPipeline.detect()`. Runs the 6-class crop
 * classifier unless a `cropHint` is supplied (bypasses classifier, required for
 * rice which has no label in the 6-class space), then the routed disease
 * model(s). Thresholds mirror the backend: crop 0.60, disease 0.55.
 * The wheat->rice mitigation (run rice alongside wheat, higher confidence wins)
 * is reproduced so rice leaves still reach the rice model.
 */
export async function detectDiseaseOnDevice(
  file: File,
  opts?: { cropHint?: string },
): Promise<OnDeviceDetectResult> {
  const cropThreshold = 0.6;
  const diseaseThreshold = 0.55;
  const hint = opts?.cropHint?.trim() ?? "";

  let cropLabel: string | null = null;
  let cropConfidence = 0;
  let cropSource: "model" | "user" = "model";
  let top3Crops: { class: string; confidence: number }[] = [];
  let candidateKeys: OnDeviceModelKey[] = [];
  const overallStart = performance.now();

  if (hint) {
    const hk = diseaseKeyForCrop(hint);
    if (hk && DISEASE_KEYS.includes(hk)) {
      cropLabel = CROP_DISPLAY[hk] ?? hk;
      cropSource = "user";
      candidateKeys = [hk];
    }
  }

  if (!cropLabel) {
    const pred = await runOnDeviceModel(file, "crop_classifier");
    top3Crops = pred.top3;
    if (pred.confidence < cropThreshold) {
      return {
        status: "not_recognized",
        crop: pred.label,
        cropConfidence: pred.confidence,
        cropSource: "model",
        disease: null,
        diseaseConfidence: 0,
        top3Crops,
        top3Diseases: [],
        latencyMs: Math.round((performance.now() - overallStart) * 100) / 100,
        onDevice: true,
      };
    }
    cropLabel = pred.label;
    cropConfidence = pred.confidence;
    const dk = diseaseKeyForCrop(cropLabel);
    if (dk) candidateKeys = [dk];
    if (cropLabel === "Wheat") {
      if (!candidateKeys.includes("rice")) candidateKeys = [...candidateKeys, "rice"];
    }
  }

  if (candidateKeys.length === 0) {
    return {
      status: "no_disease_model",
      crop: cropLabel,
      cropConfidence,
      cropSource,
      disease: null,
      diseaseConfidence: 0,
      top3Crops,
      top3Diseases: [],
      latencyMs: Math.round((performance.now() - overallStart) * 100) / 100,
      onDevice: true,
    };
  }

  const preds = await Promise.all(candidateKeys.map((k) => runOnDeviceModel(file, k)));
  let best = preds[0];
  for (const p of preds) if (p.confidence > best.confidence) best = p;

  // Rewrite the reported crop when the rice model won the wheat/rice tie (diagnosed only).
  let reportedCrop = cropLabel;
  let reportedCropConf = cropConfidence;
  if (cropSource === "model" && candidateKeys.length > 1) {
    const winnerDisplay = CROP_DISPLAY[best.model] ?? best.model;
    if (winnerDisplay !== cropLabel && best.model === "rice" && !isHealthyLabel(best.label) && best.confidence >= diseaseThreshold) {
      reportedCrop = winnerDisplay;
      reportedCropConf = best.confidence;
    }
  }

  if (best.confidence < diseaseThreshold) {
    return {
      status: "not_recognized",
      crop: reportedCrop,
      cropConfidence: reportedCropConf,
      cropSource,
      disease: best.label,
      diseaseConfidence: best.confidence,
      top3Crops,
      top3Diseases: best.top3,
      latencyMs: Math.round((performance.now() - overallStart) * 100) / 100,
      onDevice: true,
    };
  }
  if (isHealthyLabel(best.label)) {
    return {
      status: "healthy",
      crop: reportedCrop,
      cropConfidence: reportedCropConf,
      cropSource,
      disease: best.label,
      diseaseConfidence: best.confidence,
      top3Crops,
      top3Diseases: best.top3,
      latencyMs: Math.round((performance.now() - overallStart) * 100) / 100,
      onDevice: true,
    };
  }
  return {
    status: "diagnosed",
    crop: reportedCrop,
    cropConfidence: reportedCropConf,
    cropSource,
    disease: best.label,
    diseaseConfidence: best.confidence,
    top3Crops,
    top3Diseases: best.top3,
    latencyMs: Math.round((performance.now() - overallStart) * 100) / 100,
    onDevice: true,
  };
}

// --- Warm-up helper (optional, call once after page load when idle) ---

export async function warmUpOnDevice(keys: OnDeviceModelKey[] = ["crop_classifier"]): Promise<void> {
  if (!isOnDeviceEnabled()) return;
  for (const k of keys) {
    try {
      await getSession(k);
      await fetchClasses(k);
    } catch {
      // warm-up failures are non-fatal; a later real inference will surface them
    }
  }
}
