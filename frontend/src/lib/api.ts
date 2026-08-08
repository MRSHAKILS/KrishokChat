const API_BASE = "";

export interface ClassifyResponse {
  crop: string;
  confidence: number;
  top3: { class: string; confidence: number }[];
  has_disease_model: boolean;
}

export interface DiseaseInfo {
  class_name: string;
  description_bn?: string;
  solution_bn?: string;
}

export interface DetectResponse {
  crop: string;
  crop_confidence: number;
  disease: string;
  disease_confidence: number;
  disease_info: DiseaseInfo | null;
  top3_diseases: { class: string; confidence: number }[];
}

export interface AgentStageEvent {
  stage: "safety" | "retrieval" | "generation" | "verifier";
  status: "start" | "complete" | "skip";
  detail?: string | null;
}

export interface QAResponse {
  query: string;
  category: string;
  answer: string;
  sources: { id: string; score: number; answer?: string | null; source?: string | null }[];
  confidence: string;
  agent_trace: AgentStageEvent[];
}

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

export async function askQuestion(query: string): Promise<QAResponse> {
  const res = await fetch(`${API_BASE}/api/qa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error(`qa failed: ${res.status}`);
  return res.json();
}

export async function streamQuestion(
  query: string,
  onEvent: (e: AgentStageEvent) => void,
): Promise<QAResponse> {
  const res = await fetch(`${API_BASE}/api/qa/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
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
        try { onEvent(JSON.parse(t.slice(5).trim())); } catch { /* ignore */ }
      }
    }
  }
  if (!final) throw new Error("no final response");
  return final;
}

export interface SafetyMetrics {
  total_queries: number;
  by_category: Record<string, number>;
  flagged_count: number;
  recent: { query: string; category: string; timestamp: string }[];
}

export async function getSafetyMetrics(): Promise<SafetyMetrics> {
  const res = await fetch(`${API_BASE}/api/safety/metrics`);
  if (!res.ok) throw new Error(`metrics failed: ${res.status}`);
  return res.json();
}
