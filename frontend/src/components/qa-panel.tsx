"use client";

import { useState, useRef, useEffect } from "react";
import { streamQuestion, QAResponse, AgentStageEvent } from "@/lib/api";
import { AgentTrace } from "@/components/agent-trace";

const CATEGORY_BADGE: Record<string, string> = {
  safe_agri: "bg-green-100 text-green-800",
  banned_or_restricted_chemical: "bg-red-100 text-red-800",
  self_harm_or_poisoning_risk: "bg-red-200 text-red-900",
  off_topic: "bg-gray-100 text-gray-600",
  prompt_injection: "bg-orange-100 text-orange-800",
  low_confidence: "bg-yellow-100 text-yellow-800",
  blocked: "bg-red-100 text-red-800",
};

export function QAPanel({ detectedCrop, detectedDisease }: { detectedCrop?: string | null; detectedDisease?: string | null }) {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<QAResponse | null>(null);
  const [trace, setTrace] = useState<AgentStageEvent[]>([]);
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [trace, result]);

  function applyEvent(ev: AgentStageEvent) {
    setTrace((prev) => {
      const idx = prev.findIndex((p) => p.stage === ev.stage);
      if (idx >= 0) { const next = [...prev]; next[idx] = ev; return next; }
      return [...prev, ev];
    });
  }

  async function submit() {
    if (!query.trim() || streaming) return;
    setStreaming(true);
    setResult(null);
    setTrace([{ stage: "safety", status: "start" }]);
    try {
      const final = await streamQuestion(query, applyEvent, detectedCrop, detectedDisease);
      if (final) setResult(final);
    } catch (e: any) {
      setResult({ query, category: "low_confidence", answer: `Error: ${e.message}`, sources: [], confidence: "error", agent_trace: [{ stage: "safety", status: "complete" }, { stage: "retrieval", status: "complete" }, { stage: "generation", status: "complete" }, { stage: "verifier", status: "complete" }] });
    }
    setStreaming(false);
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="আপনার কৃষি সংক্রান্ত প্রশ্ন লিখুন (বাংলায়)..."
          className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
        />
        <button onClick={submit} disabled={streaming || !query.trim()}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 text-sm font-medium">
          {streaming ? "..." : "জিজ্ঞাসা"}
        </button>
      </div>

      {(trace.length > 0 || streaming) && (
        <div className="bg-gray-50 rounded-lg p-3">
          <AgentTrace events={trace} />
        </div>
      )}

      {result && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <div className="flex items-center gap-2">
            <span className={`text-xs font-bold px-2 py-0.5 rounded ${CATEGORY_BADGE[result.category] || "bg-gray-100"}`}>
              {result.category.replace(/_/g, " ")}
            </span>
            <span className="text-xs text-gray-400">confidence: {result.confidence}</span>
          </div>
          <div className="text-sm text-gray-800 whitespace-pre-wrap leading-relaxed">{result.answer}</div>
          {result.sources.length > 0 && (
            <details className="text-xs text-gray-500 pt-2 border-t">
              <summary className="cursor-pointer font-medium">{result.sources.length}টি উৎস দেখুন</summary>
              <div className="mt-2 space-y-1">
                {result.sources.map((s) => (
                  <div key={s.id} className="bg-gray-50 p-2 rounded">
                    <div className="font-medium">{s.id}</div>
                    {s.source && <div className="text-gray-400">{s.source}</div>}
                  </div>
                ))}
              </div>
            </details>
          )}
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
