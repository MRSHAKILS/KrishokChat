/* =========================================================================
   API client + types — single source of truth for the backend contract.
   Mirrors backend/app/models/schemas.py. Do not duplicate these types elsewhere.
   ========================================================================= */

const API_BASE = "";

function createTimedSignal(parent: AbortSignal | undefined, timeoutMs: number) {
  const controller = new AbortController();
  const abort = () => controller.abort();
  parent?.addEventListener("abort", abort, { once: true });
  const timeout = window.setTimeout(abort, timeoutMs);
  return {
    signal: controller.signal,
    dispose: () => {
      window.clearTimeout(timeout);
      parent?.removeEventListener("abort", abort);
    },
  };
}

/* ---------- Types ------------------------------------------------------ */

export interface AgentStageEvent {
  stage: string;
  status: "start" | "complete" | "skip" | "error" | string;
  detail?: string | null;
}

export interface SourceNode {
  id: string;
  score: number;
  crop_bn?: string | null;
  crop_en?: string | null;
  disease_bn?: string | null;
  question?: string | null;
  answer?: string | null;
  treatment?: string | null;
  source?: string | null;
  publisher?: string | null;
  publisher_bn?: string | null;
  title_bn?: string | null;
  title_en?: string | null;
  citation?: string | null;
  expert_verified?: boolean;
}

export interface QAResponse {
  query: string;
  category: string;
  answer: string;
  sources: SourceNode[];
  confidence: string; // verified | flagged-unverified | low_confidence | blocked
  agent_trace: AgentStageEvent[];
  verifier_flags: string[];
  model?: string | null;
  matched_rules?: string[];
  safety_reason?: string | null;
}

export interface ClassifyResponse {
  crop: string;
  confidence: number;
  status: string; // diagnosed | not_recognized | model_error | invalid_image
  top3: { class: string; confidence: number }[];
  has_disease_model: boolean;
  quality_warnings: string[];
  agent_trace: AgentStageEvent[];
  error?: string | null;
}

export interface DiseaseInfo {
  class_name?: string;
  description_bn?: string;
  cause_bn?: string;
  solution_bn?: string;
  [k: string]: unknown;
}

export interface DetectResponse {
  status: string; // diagnosed | healthy | not_recognized | no_disease_model | model_error | invalid_image
  detection_mode: string; // "classification" (boxes empty until a real detector exists)
  crop: string | null;
  crop_confidence: number;
  crop_source: string; // "model" | "user"
  disease: string | null;
  disease_confidence: number;
  boxes: { x: number; y: number; width: number; height: number; label: string; confidence: number }[];
  disease_info: DiseaseInfo | null;
  top3_crops: { class: string; confidence: number }[];
  top3_diseases: { class: string; confidence: number }[];
  treatment_advice: string | null;
  treatment_confidence: string | null;
  treatment_sources: string[];
  verifier_flags: string[];
  agent_trace: AgentStageEvent[];
  quality_warnings: string[];
  error?: string | null;
}

export interface SafetyMetrics {
  total_queries: number;
  by_category: Record<string, number>;
  flagged_count: number;
  verifier?: {
    checked: number;
    grounded: number;
    unsupported: number;
    pass_rate: number | null;
  };
  refusals?: { answered_without_sources: number };
  router?: { blocked: number; refusal_rate: number | null; refusal_rules?: Record<string, number> };
  retrieval?: {
    answered: number;
    hit_rate: number | null;
    avg_top1_score: number | null;
    avg_sources: number | null;
  };
  recent: {
    query: string;
    category: string;
    timestamp: string;
    action?: string;
    retrieval_hit?: boolean;
    verifier_passed?: boolean | null;
  }[];
}

/* ---------- QA --------------------------------------------------------- */

export async function askQuestion(
  query: string,
  opts?: { crop?: string | null; disease?: string | null; session_id?: string | null },
): Promise<QAResponse> {
  const res = await fetch(`${API_BASE}/api/qa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      crop: opts?.crop ?? null,
      disease: opts?.disease ?? null,
      session_id: opts?.session_id ?? null,
    }),
  });
  if (!res.ok) throw new Error(`qa failed: ${res.status}`);
  return res.json();
}

export async function streamQuestion(
  query: string,
  onEvent: (e: AgentStageEvent) => void,
  onToken?: (text: string) => void,
  opts?: {
    crop?: string | null;
    disease?: string | null;
    session_id?: string | null;
    history?: Array<{ role: string; content: string }>;
    model?: string | null;
    signal?: AbortSignal;
    timeoutMs?: number;
  },
): Promise<QAResponse> {
  const request = createTimedSignal(opts?.signal, opts?.timeoutMs ?? 120_000);
  try {
    const res = await fetch(`${API_BASE}/api/qa/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        crop: opts?.crop,
        disease: opts?.disease,
        session_id: opts?.session_id,
        history: opts?.history,
        model: opts?.model,
      }),
      signal: request.signal,
    });
    if (!res.ok) throw new Error(`qa stream failed: ${res.status}`);
    const reader = res.body?.getReader();
    if (!reader) throw new Error("no response body");
    const decoder = new TextDecoder();
    let buf = "";
    let final: QAResponse | null = null;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split("\n");
      buf = lines.pop() || "";
      for (const line of lines) {
        const t = line.trim();
        if (!t) continue;
        if (t.startsWith("final:")) {
          final = JSON.parse(t.slice(6).trim());
        } else if (t.startsWith("data:")) {
          try {
            onEvent(JSON.parse(t.slice(5).trim()));
          } catch {
            /* A malformed progress event must not discard the final answer. */
          }
        } else if (t.startsWith("token:")) {
          try {
            onToken?.(JSON.parse(t.slice(6).trim()).text);
          } catch {
            /* A malformed token must not discard the final answer. */
          }
        }
      }
    }
    if (!final) throw new Error("no final response");
    return final;
  } finally {
    request.dispose();
  }
}

/* ---------- Vision ---------------------------------------------------- */

export async function classifyCrop(file: File): Promise<ClassifyResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/api/classify`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`classify failed: ${res.status}`);
  return res.json();
}

export async function detectDisease(
  file: File,
  opts?: { cropHint?: string; signal?: AbortSignal; timeoutMs?: number },
): Promise<DetectResponse> {
  const form = new FormData();
  form.append("file", file);
  if (opts?.cropHint) {
    form.append("crop_hint", opts.cropHint);
  }
  const request = createTimedSignal(opts?.signal, opts?.timeoutMs ?? 90_000);
  try {
    const res = await fetch(`${API_BASE}/api/detect`, {
      method: "POST",
      body: form,
      signal: request.signal,
    });
    if (!res.ok) throw new Error(`detect failed: ${res.status}`);
    return res.json();
  } finally {
    request.dispose();
  }
}

/* ---------- Soil moisture (dataset + locked analyzer) ------------------ */

export interface SoilTypeStat {
  key: string; // "Doash"
  usda: string; // "Loam"
  count: number;
}

export interface SoilSample {
  image_id: string;
  filename: string;
  soil_type: string;
  kpa: number;
  land_type: string;
  crop: string;
  growth_stage: string;
}

export interface SoilModelResult {
  model: string;
  rmse_kpa: number;
  r2: number;
}

export interface SoilDatasetInfo {
  available: boolean;
  total_images: number;
  kpa_range: number[];
  kpa_bins: Record<string, number>;
  soil_types: SoilTypeStat[];
  land_types: Record<string, number>;
  crops: Record<string, number>;
  growth_stages: Record<string, number>;
  series_count: number;
  splits: Record<string, number>;
  metadata_matched: number;
  metadata_inferred: number;
  corrections: number;
  collection: Record<string, string>;
  model_status: string; // "in_development" | "released"
  model_results: SoilModelResult[];
  samples: SoilSample[];
}

export interface SoilAnalyzeResponse {
  status: string; // locked | invalid_image | analyzed (future)
  error?: string | null;
  dataset: SoilDatasetInfo | null;
  agent_trace: AgentStageEvent[];
}

export async function getSoilDataset(): Promise<SoilDatasetInfo> {
  const res = await fetch(`${API_BASE}/api/soil/dataset`);
  if (!res.ok) throw new Error(`soil dataset failed: ${res.status}`);
  return res.json();
}

export async function analyzeSoil(
  file: File,
  opts?: { signal?: AbortSignal; timeoutMs?: number },
): Promise<SoilAnalyzeResponse> {
  const form = new FormData();
  form.append("file", file);
  const request = createTimedSignal(opts?.signal, opts?.timeoutMs ?? 60_000);
  try {
    const res = await fetch(`${API_BASE}/api/soil/analyze`, {
      method: "POST",
      body: form,
      signal: request.signal,
    });
    if (!res.ok) throw new Error(`soil analyze failed: ${res.status}`);
    return res.json();
  } finally {
    request.dispose();
  }
}

/* ---------- Voice (P5: read-aloud TTS + optional server ASR) ---------- */

/** Synthesize MP3 for a short Bengali answer via the backend edge-tts proxy.
    Throws on any failure so callers can fall back to browser speechSynthesis. */
export async function synthesizeSpeech(
  text: string,
  opts?: { voice?: string; signal?: AbortSignal; timeoutMs?: number },
): Promise<Blob> {
  const request = createTimedSignal(opts?.signal, opts?.timeoutMs ?? 15_000);
  try {
    const res = await fetch(`${API_BASE}/api/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, voice: opts?.voice ?? "bn-BD-NabanitaNeural" }),
      signal: request.signal,
    });
    if (!res.ok) throw new Error(`tts failed: ${res.status}`);
    return res.blob();
  } finally {
    request.dispose();
  }
}

/* ---------- Metrics ---------------------------------------------------- */

export async function getSafetyMetrics(): Promise<SafetyMetrics> {
  const res = await fetch(`${API_BASE}/api/safety/metrics`);
  if (!res.ok) throw new Error(`metrics failed: ${res.status}`);
  return res.json();
}

/* ---------- Models availability --------------------------------------- */

export interface ModelOption {
  id: string;
  label: string;
  description: string;
  available: boolean;
}

export async function getModels(): Promise<ModelOption[]> {
  const res = await fetch(`${API_BASE}/api/models`);
  if (!res.ok) throw new Error(`models failed: ${res.status}`);
  return res.json();
}

/* ---------- Weather (Gemini-powered, token-efficient) ------------------ */

export interface WeatherResponse {
  district: string;
  summary_bn: string;
  advice_bn: string;
  model?: string | null;
}

export async function getWeather(
  district: string,
  crop?: string | null,
): Promise<WeatherResponse> {
  const res = await fetch(`${API_BASE}/api/weather`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ district, crop: crop ?? null }),
  });
  if (!res.ok) throw new Error(`weather failed: ${res.status}`);
  return res.json();
}

/* ---------- Helpline Registration (local storage only) ---------------- */

export interface HelplineRegister {
  name: string;
  phone: string;
  district: string;
  crop?: string | null;
  notes?: string | null;
}

export interface HelplineResponse {
  status: string;
  message: string;
  registration_id?: string | null;
}

export async function registerHelpline(
  data: HelplineRegister,
): Promise<HelplineResponse> {
  const res = await fetch(`${API_BASE}/api/helpline/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`helpline register failed: ${res.status}`);
  return res.json();
}

/* ---------- Regional Dialect Translator (Gemini 2.5 Flash Lite) ---------- */

export interface DialectResponse {
  dialect: string;
  dialect_name: string;
  translated_bn: string;
}

export async function translateDialect(
  text: string,
  dialect: string,
): Promise<DialectResponse> {
  const res = await fetch(`${API_BASE}/api/dialect/translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, dialect }),
  });
  if (!res.ok) throw new Error(`dialect translate failed: ${res.status}`);
  return res.json();
}

/* ---------- Saved history (premium lane; auth via Bearer token) ---------- */

export interface SavedQuery {
  id: string;
  query_text: string;
  answer_text: string;
  sources: SourceNode[];
  category: string;
  created_at: string;
}

export interface SavedHistoryResponse {
  items: SavedQuery[];
  enabled: boolean;
}

export async function getSavedHistory(accessToken: string): Promise<SavedHistoryResponse> {
  const res = await fetch(`${API_BASE}/api/history`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!res.ok) throw new Error(`history failed: ${res.status}`);
  return res.json();
}

export async function saveAnswer(
  accessToken: string,
  data: { query_text: string; answer_text: string; sources: SourceNode[]; category: string },
): Promise<SavedQuery> {
  const res = await fetch(`${API_BASE}/api/history`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}` },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`history save failed: ${res.status}`);
  return res.json();
}

export async function deleteSavedQuery(accessToken: string, id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/history/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!res.ok && res.status !== 404) throw new Error(`history delete failed: ${res.status}`);
}
