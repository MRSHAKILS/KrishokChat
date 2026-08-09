"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { streamQuestion, QAResponse, AgentStageEvent } from "@/lib/api";
import { AgentTrace } from "@/components/agent-trace";
import { motionTokens } from "@/lib/motionTokens";

const CATEGORY_BADGE: Record<string, { bg: string; label: string }> = {
  safe_agri: { bg: "bg-green-100 text-green-800", label: "কৃষি প্রশ্ন" },
  banned_or_restricted_chemical: { bg: "bg-red-100 text-red-800", label: "নিষিদ্ধ রাসায়ন" },
  self_harm_or_poisoning_risk: { bg: "bg-red-200 text-red-900", label: "জরুরি সহায়তা" },
  off_topic: { bg: "bg-gray-100 text-gray-600", label: "অন্যান্য" },
  prompt_injection: { bg: "bg-orange-100 text-orange-800", label: "অননুমোদিত" },
  low_confidence: { bg: "bg-yellow-100 text-yellow-800", label: "অনিশ্চিত" },
  blocked: { bg: "bg-red-100 text-red-800", label: "অবরুদ্ধ" },
};

const GATE_BADGE: Record<string, { bg: string; label: string }> = {
  FULLY_GROUNDED: { bg: "bg-green-100 text-green-800", label: "🟢 ডাটাবেস থেকে" },
  PARTIALLY_GROUNDED: { bg: "bg-yellow-100 text-yellow-800", label: "🟡 আংশিক তথ্য" },
  GENERAL_GUIDANCE: { bg: "bg-blue-100 text-blue-800", label: "🔴 সাধারণ পরামর্শ" },
  REFER_EXPERT: { bg: "bg-red-100 text-red-800", label: "⚪ বিশেষজ্ঞের পরামর্শ" },
};

export function QAPanel({ detectedCrop, detectedDisease }: { detectedCrop?: string | null; detectedDisease?: string | null }) {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<QAResponse | null>(null);
  const [trace, setTrace] = useState<AgentStageEvent[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [progress, setProgress] = useState(0);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [trace, result]);

  function applyEvent(ev: AgentStageEvent) {
    setTrace((prev) => {
      const idx = prev.findIndex((p) => p.stage === ev.stage);
      if (idx >= 0) { const next = [...prev]; next[idx] = ev; return next; }
      return [...prev, ev];
    });
    // Update progress bar based on completed stages
    setTrace((current) => {
      const done = current.filter((e) => e.status === "complete").length;
      setProgress(done / 4);
      return current;
    });
  }

  async function submit() {
    if (!query.trim() || streaming) return;
    setStreaming(true);
    setResult(null);
    setTrace([{ stage: "safety", status: "start" }]);
    setProgress(0.1);
    try {
      const final = await streamQuestion(query, applyEvent, detectedCrop, detectedDisease);
      if (final) setResult(final);
    } catch (e: any) {
      setResult({ query, category: "low_confidence", answer: `ত্রুটি: ${e.message}`, sources: [], confidence: "error", agent_trace: [] });
    }
    setStreaming(false);
    setProgress(1);
  }

  const completedStages = trace.filter((e) => e.status === "complete").length;

  return (
    <div className="space-y-4">
      {/* Progress bar */}
      <AnimatePresence>
        {(streaming || result) && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: motionTokens.duration.fast }}
            className="space-y-1"
          >
            <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-green-500 to-emerald-400 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${progress * 100}%` }}
                transition={{ duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth }}
              />
            </div>
            <div className="flex justify-between text-[10px] text-gray-400">
              <span>{completedStages}/4 ধাপ</span>
              <span>{streaming ? "প্রক্রিয়াকরণ..." : "সম্পন্ন"}</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input */}
      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="আপনার কৃষি সংক্রান্ত প্রশ্ন লিখুন (বাংলায়)..."
          className="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent transition-shadow"
        />
        <motion.button
          onClick={submit}
          disabled={streaming || !query.trim()}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          transition={{ duration: motionTokens.duration.fast }}
          className="bg-gradient-to-r from-[#1a5632] to-[#2d7d46] text-white px-5 py-2.5 rounded-xl hover:shadow-lg disabled:opacity-40 disabled:cursor-not-allowed text-sm font-semibold"
        >
          {streaming ? "..." : "জিজ্ঞাসা"}
        </motion.button>
      </div>

      {/* Agent trace */}
      <AnimatePresence>
        {(trace.length > 0 || streaming) && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            transition={{ duration: motionTokens.duration.fast }}
            className="bg-white/60 border border-gray-100 rounded-xl p-3"
          >
            <AgentTrace events={trace} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Result */}
      <AnimatePresence mode="wait">
        {result && (
          <motion.div
            key={result.query}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            transition={{ duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth }}
            className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm space-y-3"
          >
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${CATEGORY_BADGE[result.category]?.bg || "bg-gray-100"}`}>
                {CATEGORY_BADGE[result.category]?.label || result.category}
              </span>
            </div>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1, duration: motionTokens.duration.normal }}
              className="text-sm text-gray-800 whitespace-pre-wrap leading-relaxed"
            >
              {result.answer}
            </motion.div>
            {result.sources.length > 0 && (
              <details className="text-xs text-gray-500 pt-2 border-t border-gray-100">
                <summary className="cursor-pointer font-semibold hover:text-green-700 transition-colors">
                  {result.sources.length}টি উৎস দেখুন
                </summary>
                <div className="mt-2 space-y-1">
                  {result.sources.map((s) => (
                    <div key={s.id} className="bg-gray-50 p-2 rounded-lg font-mono text-[10px]">{s.id}</div>
                  ))}
                </div>
              </details>
            )}
          </motion.div>
        )}
      </AnimatePresence>
      <div ref={bottomRef} />
    </div>
  );
}
