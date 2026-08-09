/* =========================================================================
   API client + types — single source of truth for the backend contract.
   Mirrors backend/app/models/schemas.py. Do not duplicate these types elsewhere.
   ========================================================================= */

const API_BASE = "";

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
  recent: { query: string; category: string; timestamp: string }[];
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
  },
): Promise<QAResponse> {
  const res = await fetch(`${API_BASE}/api/qa/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      crop: opts?.crop,
      disease: opts?.disease,
      session_id: opts?.session_id,
      history: opts?.history,
    }),
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
          /* ignore malformed */
        }
      } else if (t.startsWith("token:")) {
        try {
          onToken?.(JSON.parse(t.slice(6).trim()).text);
        } catch {
          /* ignore */
        }
      }
    }
  }
  if (!final) throw new Error("no final response");
  return final;
}

/* ---------- Vision ---------------------------------------------------- */

export async function classifyCrop(file: File): Promise<ClassifyResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/api/classify`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`classify failed: ${res.status}`);
  return res.json();
}

export async function detectDisease(file: File): Promise<DetectResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/api/detect`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`detect failed: ${res.status}`);
  return res.json();
}

/* ---------- Metrics ---------------------------------------------------- */

export async function getSafetyMetrics(): Promise<SafetyMetrics> {
  const res = await fetch(`${API_BASE}/api/safety/metrics`);
  if (!res.ok) throw new Error(`metrics failed: ${res.status}`);
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
