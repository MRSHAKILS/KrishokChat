"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { streamQuestion, AgentStageEvent } from "@/lib/api";
import { AgentTrace, TraceEvent } from "@/components/agent-trace";
import { motionTokens } from "@/lib/motionTokens";

type ChatMessage = { role: "user" | "assistant"; content: string };

export function QAPanel({ detectedCrop, detectedDisease }: { detectedCrop?: string | null; detectedDisease?: string | null }) {
  const [sessionId] = useState(() => crypto.randomUUID());
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [trace, setTrace] = useState<TraceEvent[]>([]);
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, trace]);

  const applyEvent = useCallback((ev: TraceEvent) => {
    setTrace((prev) => {
      const idx = prev.findIndex((p) => p.stage === ev.stage);
      if (idx >= 0) { const next = [...prev]; next[idx] = ev; return next; }
      return [...prev, ev];
    });
  }, []);

  async function submit() {
    if (!query.trim() || streaming) return;
    const userMsg: ChatMessage = { role: "user", content: query };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setStreaming(true);
    setTrace([{ stage: "safety", status: "start" }]);
    setQuery("");

    const history = newMessages.slice(0, -1).map((m) => ({
      role: m.role === "user" ? "user" : "assistant",
      content: m.content,
    }));

    try {
      const final = await streamQuestion(query, applyEvent, detectedCrop, detectedDisease, sessionId, history);
      if (final) {
        setMessages((prev) => [...prev, { role: "assistant", content: final.answer }]);
      }
    } catch (e: any) {
      setMessages((prev) => [...prev, { role: "assistant", content: "ত্রুটি: " + e.message }]);
    }
    setStreaming(false);
    setTrace([]);
  }

  return (
    <div className="space-y-4 flex flex-col h-full">
      <div className="flex-1 space-y-3 max-h-96 overflow-y-auto pr-1">
        <AnimatePresence initial={false}>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: motionTokens.duration.fast }}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-[#1a5632] text-white rounded-br-md"
                    : "bg-gray-100 text-gray-800 rounded-bl-md"
                }`}
              >
                {msg.content}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        {streaming && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
              <AgentTrace events={trace} />
            </div>
          </motion.div>
        )}
      </div>

      <div className="flex gap-2 pt-2 border-t border-gray-100">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="আপনার কৃষি সংক্রান্ত প্রশ্ন লিখুন (বাংলায়)..."
          className="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent"
        />
        <motion.button
          onClick={submit}
          disabled={streaming || !query.trim()}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          transition={{ duration: motionTokens.duration.fast }}
          className="bg-gradient-to-r from-[#1a5632] to-[#2d7d46] text-white px-5 py-2.5 rounded-xl disabled:opacity-40 disabled:cursor-not-allowed text-sm font-semibold"
        >
          {streaming ? "..." : "জিজ্ঞাসা"}
        </motion.button>
      </div>
      <div ref={bottomRef} />
    </div>
  );
}
