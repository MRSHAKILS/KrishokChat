"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion } from "motion/react";
import { Send, Loader2 } from "lucide-react";
import { streamQuestion, type AgentStageEvent } from "@/lib/api";
import { ChatMessage, type ChatMessageData } from "@/components/chat/chat-message";
import { SuggestedQuestions } from "@/components/chat/suggested-questions";
import { dur, ease } from "@/lib/motion";
import { cn } from "@/lib/utils";
import { CHAT } from "@/lib/constants";

/* =========================================================================
   QAPanel — the safety-aware agentic chat component.
   Used on both /chat (standalone) and /detect (right panel with context).

   State flow:
   1. User types or picks a suggested question
   2. SSE stream starts: data: events light up the PipelineRail inside
      the streaming ChatMessage bubble
   3. token: events append to the answer (if the LLM supports streaming)
   4. final: event delivers the complete QAResponse → ChatMessage swaps
      from streaming to completed content

   Scroll management: only the container scrolls, never the page.
   Only on new message, never on mount, trace updates, or image inserts.
   ========================================================================= */

export function QAPanel({
  detectedCrop,
  detectedDisease,
}: {
  detectedCrop?: string | null;
  detectedDisease?: string | null;
}) {
  const [sessionId] = useState(() => crypto.randomUUID());
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [traceEvents, setTraceEvents] = useState<AgentStageEvent[]>([]);
  const [streaming, setStreaming] = useState(false);

  // Scroll management — scroll ONLY the chat container, never the page.
  const scrollRef = useRef<HTMLDivElement>(null);
  const prevMsgCount = useRef(0);

  useEffect(() => {
    if (messages.length > prevMsgCount.current && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
    prevMsgCount.current = messages.length;
  }, [messages]);

  const applyEvent = useCallback((ev: AgentStageEvent) => {
    setTraceEvents((prev) => {
      const idx = prev.findIndex((p) => p.stage === ev.stage);
      if (idx >= 0) {
        const next = [...prev];
        next[idx] = ev;
        return next;
      }
      return [...prev, ev];
    });
  }, []);

  const send = useCallback(
    async (text: string) => {
      const q = text.trim();
      if (!q || streaming) return;

      const userMsg: ChatMessageData = { role: "user", content: q };
      const newMessages = [...messages, userMsg];
      setMessages(newMessages);
      setStreaming(true);
      setTraceEvents([{ stage: "safety", status: "start" }]);
      setQuery("");

      const fullHistory = newMessages
        .slice(0, -1)
        .map((m) => ({
          role: m.role,
          content: m.content,
        }));

      try {
        const final = await streamQuestion(
          q,
          applyEvent,
          undefined,
          {
            crop: detectedCrop,
            disease: detectedDisease,
            session_id: sessionId,
            history: fullHistory,
          },
        );

        // Replace the streaming placeholder with the completed response
        setMessages((prev) => {
          const next = [...prev];
          // The last message is the user's; the streaming bubble is implicit.
          // Push the assistant's completed message.
          next.push({
            role: "assistant",
            content: final.answer,
            response: final,
          });
          return next;
        });
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        if (msg.includes("Failed to fetch") || msg.includes("fetch")) {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: "",
              error: "ব্যাকএন্ড সার্ভারে সংযোগ ব্যর্থ। নিশ্চিত করুন যে ব্যাকএন্ড চলছে।",
            },
          ]);
        } else {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: "", error: msg },
          ]);
        }
      }
      setStreaming(false);
      setTraceEvents([]);
    },
    [messages, streaming, detectedCrop, detectedDisease, sessionId, applyEvent],
  );

  const clear = useCallback(() => {
    setMessages([]);
    setTraceEvents([]);
    setQuery("");
  }, []);

  const isEmpty = messages.length === 0;

  return (
    <div className="flex h-full flex-col">
      {/* Messages — scroll container */}
      <div
        ref={scrollRef}
        className="flex-1 space-y-4 overflow-y-auto pr-1 scrollbar-thin"
        style={{ minHeight: "200px" }}
      >
        {isEmpty ? (
          <EmptyState
            onPick={send}
            detectedCrop={detectedCrop}
            detectedDisease={detectedDisease}
          />
        ) : (
          <>
            {messages.map((msg, i) => {
              // The streaming bubble appears after the last user message
              const isStreamingBubble =
                streaming &&
                i === messages.length - 1 &&
                msg.role === "user";
              return (
                <div key={i} className="space-y-4">
                  <ChatMessage message={msg} />
                  {isStreamingBubble && (
                    <ChatMessage
                      message={{ role: "assistant", content: "" }}
                      streaming={true}
                      traceEvents={traceEvents}
                    />
                  )}
                </div>
              );
            })}
          </>
        )}
      </div>

      {/* Input bar */}
      <div className="mt-3 flex gap-2 border-t rule pt-3">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send(query);
            }
          }}
          rows={1}
          maxLength={CHAT.maxMessageLength}
          placeholder="আপনার কৃষি সংক্রান্ত প্রশ্ন লিখুন (বাংলায়)..."
          className="flex-1 resize-none rounded-lg border rule bg-paper px-4 py-2.5 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
          style={{ maxHeight: "6rem" }}
        />
        <button
          onClick={() => send(query)}
          disabled={streaming || !query.trim()}
          className={cn(
            "flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-medium transition-all disabled:cursor-not-allowed disabled:opacity-40",
            "bg-leaf text-paper hover:bg-leaf-2",
          )}
        >
          {streaming ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
          <span className="hidden sm:inline">{streaming ? "…" : "জিজ্ঞাসা"}</span>
        </button>
      </div>

      {/* Clear button (only when there are messages) */}
      {!isEmpty && !streaming && (
        <button
          onClick={clear}
          className="mx-auto mt-2 text-xs text-ink-faint transition-colors hover:text-clay"
        >
          কথোপকথন মুছুন
        </button>
      )}
    </div>
  );
}

/* --- Empty state: welcome + suggested questions --- */

function EmptyState({
  onPick,
  detectedCrop,
  detectedDisease,
}: {
  onPick: (q: string) => void;
  detectedCrop?: string | null;
  detectedDisease?: string | null;
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="flex flex-col items-center justify-center py-8 text-center"
    >
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-leaf/10 text-leaf">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden>
          <path
            d="M4 18C4 11 9 6 20 5C19 14 13 18 4 18Z"
            fill="currentColor"
            opacity="0.85"
          />
          <path
            d="M6 17C10 14 13 11 17 7"
            stroke="var(--color-ochre-soft)"
            strokeWidth="1"
            strokeLinecap="round"
          />
        </svg>
      </div>
      <h3 className="font-display text-lg text-ink">আসসালামু আলাইকুম!</h3>
      <p className="mt-1 max-w-sm text-sm leading-relaxed text-ink-soft">
        বাংলায় আপনার কৃষি সংক্রান্ত যেকোনো প্রশ্ন করুন। আমি নিরাপত্তা যাচাই,
        তথ্য সংগ্রহ ও যাচাইকরণের মাধ্যমে উত্তর দেব।
      </p>
      <div className="mt-6 w-full">
        <SuggestedQuestions
          onPick={onPick}
          crop={detectedCrop}
          disease={detectedDisease}
        />
      </div>
    </motion.div>
  );
}
