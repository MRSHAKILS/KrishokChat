"use client";

import { useState, useRef, useEffect, useCallback, useSyncExternalStore } from "react";
import { motion } from "motion/react";
import { Send, Loader2, Mic, Square, RotateCcw } from "lucide-react";
import { streamQuestion, getModels, type AgentStageEvent } from "@/lib/api";
import { ChatMessage, type ChatMessageData } from "@/components/chat/chat-message";
import { SuggestedQuestions } from "@/components/chat/suggested-questions";
import { dur, ease } from "@/lib/motion";
import { cn } from "@/lib/utils";
import { CHAT } from "@/lib/constants";

const getSpeechSupported = () => {
  if (typeof window === "undefined") return false;
  const browser = window as unknown as { SpeechRecognition?: unknown; webkitSpeechRecognition?: unknown };
  return Boolean(browser.SpeechRecognition || browser.webkitSpeechRecognition);
};

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
  const [model, setModel] = useState<"gemini" | "krishokchat-4b">("gemini");
  const [localAvailable, setLocalAvailable] = useState<boolean>(false);

  /* ---- Voice input (Web Speech API, Bengali bn-BD) ----
     Rural farmers struggle to type Bengali agricultural terms on small
     touchscreens. The mic transcribes speech directly into the text box.
     Falls back silently where SpeechRecognition is unavailable. */
  const [listening, setListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef<unknown>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const SR =
      (window as unknown as { SpeechRecognition?: unknown }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: unknown }).webkitSpeechRecognition;
    if (!SR) return;
    setSpeechSupported(true);
    const rec = new (SR as new () => {
      lang: string;
      continuous: boolean;
      interimResults: boolean;
      onresult: ((e: { results: ArrayLike<ArrayLike<{ transcript: string }>>; resultIndex: number }) => void) | null;
      onend: (() => void) | null;
      onerror: (() => void) | null;
      start: () => void;
      stop: () => void;
    })();
    rec.lang = "bn-BD";
    rec.continuous = false;
    rec.interimResults = true;
    rec.onresult = (e) => {
      let text = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        text += e.results[i][0].transcript;
      }
      setQuery(text);
    };
    rec.onend = () => setListening(false);
    rec.onerror = () => setListening(false);
    recognitionRef.current = rec;
  }, []);

  const toggleMic = useCallback(() => {
    const rec = recognitionRef.current as { start: () => void; stop: () => void } | null;
    if (!rec) return;
    if (listening) {
      rec.stop();
      setListening(false);
    } else {
      setQuery("");
      try {
        rec.start();
        setListening(true);
      } catch {
        setListening(false);
      }
    }
  }, [listening]);

  // Check local model availability once (Ollama running + model loaded)
  useEffect(() => {
    getModels()
      .then((ms) => {
        const local = ms.find((m) => m.id === "krishokchat-4b");
        setLocalAvailable(local?.available ?? false);
      })
      .catch(() => setLocalAvailable(false));
  }, []);

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
            model,
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
    [messages, streaming, detectedCrop, detectedDisease, sessionId, applyEvent, model],
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

      {/* Model selector — farmer-facing labels, not technical model IDs.
         The underlying ids ("gemini", "krishokchat-4b") stay as the value;
         farmers see "সাধারণ এআই" / "গবেষণা এআই". */}
      {/* Model selector & Clear actions */}
      <div className="mt-3 flex items-center justify-between gap-2 border-t rule pt-2">
        <div className="flex items-center gap-1">
          {([
            { id: "gemini", label: "সাধারণ এআই", hint: "অনলাইন" },
            { id: "krishokchat-4b", label: "গবেষণা এআই", hint: localAvailable ? "লোকাল" : "লোকাল নেই" },
          ] as const).map((m) => {
            const disabled = m.id === "krishokchat-4b" && !localAvailable;
            return (
              <button
                key={m.id}
                onClick={() => setModel(m.id)}
                disabled={disabled}
                title={m.id === "krishokchat-4b" ? (localAvailable ? "স্থানীয়ভাবে চালিত গবেষণা মডেল" : "Ollama चालू নয় — মডেল অনুপলব্ধ") : "ডিফল্ট অনলাইন এআই মডেল"}
                className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-[11px] font-medium transition-colors ${
                  model === m.id
                    ? "bg-leaf/15 text-leaf ring-1 ring-leaf/30"
                    : disabled
                      ? "cursor-not-allowed text-ink-faint"
                      : "text-ink-faint hover:text-ink-soft"
                }`}
              >
                {m.label}
                <span className={`rounded-full px-1.5 text-[9px] ${model === m.id ? "bg-leaf/20" : "bg-bone"}`}>
                  {m.hint}
                </span>
              </button>
            );
          })}
        </div>

        {!isEmpty && !streaming && (
          <button
            onClick={clear}
            title="নতুন কথোপকথন শুরু করুন"
            className="flex items-center gap-1 rounded-md px-2 py-1 text-[11px] font-medium text-ink-faint transition-colors hover:bg-clay/10 hover:text-clay"
          >
            <RotateCcw className="h-3 w-3" />
            <span className="hidden sm:inline">কথোপকথন সাফ করুন</span>
          </button>
        )}
      </div>

      {/* Input bar — text + voice + send. The mic lets low-literacy farmers
          speak their question in Bengali instead of typing on a phone. */}
      <div className="mt-2 flex items-end gap-2">
        <div className="relative flex-1">
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
            placeholder={listening ? "শুনছি… কথা বলুন…" : "আপনার কৃষি সংক্রান্ত প্রশ্ন লিখুন (বাংলায়)…"}
            className="w-full min-h-[42px] resize-none rounded-lg border rule bg-paper px-4 py-2 pr-12 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
            style={{ maxHeight: "6rem" }}
          />
          {speechSupported && (
            <button
              onClick={toggleMic}
              type="button"
              aria-label={listening ? "রেকর্ড বন্ধ করুন" : "ভয়েস ইনপুট"}
              className={cn(
                "absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-md transition-colors",
                listening
                  ? "bg-clay/15 text-clay"
                  : "text-ink-faint hover:bg-leaf/10 hover:text-leaf",
              )}
            >
              {listening ? (
                <Square className="h-3.5 w-3.5 fill-current" />
              ) : (
                <Mic className="h-4 w-4" />
              )}
              {listening && (
                <span className="absolute inset-0 animate-ping rounded-md bg-clay/20" />
              )}
            </button>
          )}
        </div>
        <button
          onClick={() => send(query)}
          disabled={streaming || !query.trim()}
          className={cn(
            "flex h-[42px] shrink-0 items-center justify-center gap-2 rounded-lg px-4 text-sm font-medium transition-all disabled:cursor-not-allowed disabled:opacity-40",
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
