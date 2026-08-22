"use client";

import { useState, useRef, useEffect, useCallback, useSyncExternalStore } from "react";
import { motion } from "motion/react";
import { Send, Mic, Square, RotateCcw, ShieldCheck, X, Bookmark, Check, Loader2 } from "lucide-react";
import { streamQuestion, getModels, saveAnswer, type AgentStageEvent } from "@/lib/api";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { ChatMessage, type ChatMessageData } from "@/components/chat/chat-message";
import { stopAllSpeech } from "@/components/chat/read-aloud";
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
  prefillQuestion,
  compact = false,
}: {
  detectedCrop?: string | null;
  detectedDisease?: string | null;
  prefillQuestion?: string | null;
  compact?: boolean;
}) {
  const [sessionId] = useState(() => crypto.randomUUID());
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [traceEvents, setTraceEvents] = useState<AgentStageEvent[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [model, setModel] = useState<"gemini" | "krishokchat-4b">("gemini");
  const [localAvailable, setLocalAvailable] = useState<boolean>(false);
  const [streamedText, setStreamedText] = useState("");
  const [restored, setRestored] = useState(false);
  const [savedMessages, setSavedMessages] = useState<Set<number>>(new Set());
  const requestRef = useRef<AbortController | null>(null);
  const streamingRef = useRef(false);
  const storageKey = "krishokchat:conversation:v1";
  const { session } = useSupabaseSession();

  /* ---- Smooth Token Stream Easing Buffer (requestAnimationFrame) ----
     Interpolates incoming SSE token chunks smoothly over ~16ms frames rather
     than instant raw DOM appends, eliminating layout jumps and jittery scrolling. */
  const targetTextRef = useRef("");
  const displayedTextRef = useRef("");
  const rafIdRef = useRef<number | null>(null);

  const startEasingLoop = useCallback(() => {
    if (rafIdRef.current !== null) return;

    const tick = () => {
      const target = targetTextRef.current;
      const current = displayedTextRef.current;

      if (current.length < target.length) {
        const remaining = target.length - current.length;
        // Adaptive rate: steady 1-2 chars for small buffer, up to remaining/4 for large burst
        const step = remaining > 30 ? Math.ceil(remaining / 4) : remaining > 10 ? 3 : remaining > 3 ? 2 : 1;
        const next = target.slice(0, current.length + step);
        displayedTextRef.current = next;
        setStreamedText(next);
        rafIdRef.current = requestAnimationFrame(tick);
      } else {
        rafIdRef.current = null;
      }
    };

    rafIdRef.current = requestAnimationFrame(tick);
  }, []);

  const pushStreamToken = useCallback((token: string) => {
    targetTextRef.current += token;
    startEasingLoop();
  }, [startEasingLoop]);

  const flushStreamBuffer = useCallback(() => {
    if (rafIdRef.current !== null) {
      cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
    }
    displayedTextRef.current = targetTextRef.current;
    setStreamedText(targetTextRef.current);
  }, []);

  const resetStreamBuffer = useCallback(() => {
    if (rafIdRef.current !== null) {
      cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
    }
    targetTextRef.current = "";
    displayedTextRef.current = "";
    setStreamedText("");
  }, []);

  useEffect(() => {
    window.queueMicrotask(() => {
      try {
        const saved = window.localStorage.getItem(storageKey);
        if (saved) setMessages(JSON.parse(saved) as ChatMessageData[]);
      } catch {
        window.localStorage.removeItem(storageKey);
      } finally {
        setRestored(true);
      }
    });
    return () => {
      requestRef.current?.abort();
      if (rafIdRef.current !== null) {
        cancelAnimationFrame(rafIdRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (!restored) return;
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(messages.slice(-20)));
    } catch {
      // Storage may be unavailable in private mode; chat remains usable in memory.
    }
  }, [messages, restored]);

  useEffect(() => {
    if (!prefillQuestion) return;
    window.queueMicrotask(() => setQuery(prefillQuestion));
  }, [prefillQuestion]);

  /* ---- Voice input (Web Speech API, Bengali bn-BD) ----
     Rural farmers struggle to type Bengali agricultural terms on small
     touchscreens. The mic transcribes speech directly into the text box.
     Falls back silently where SpeechRecognition is unavailable. */
  const [listening, setListening] = useState(false);
  const speechSupported = useSyncExternalStore(
    () => () => undefined,
    getSpeechSupported,
    () => false,
  );
  const [voiceInputError, setVoiceInputError] = useState<string | null>(null);
  const recognitionRef = useRef<unknown>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const SR =
      (window as unknown as { SpeechRecognition?: unknown }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: unknown }).webkitSpeechRecognition;
    if (!SR) return;
    const rec = new (SR as new () => {
      lang: string;
      continuous: boolean;
      interimResults: boolean;
      onresult: ((e: { results: ArrayLike<ArrayLike<{ transcript: string }>>; resultIndex: number }) => void) | null;
      onend: (() => void) | null;
      onstart: (() => void) | null;
      onerror: ((event: { error?: string }) => void) | null;
      start: () => void;
      stop: () => void;
    })();
    rec.lang = "bn-BD";
    rec.continuous = false;
    rec.interimResults = true;
    rec.onstart = () => {
      setListening(true);
      setVoiceInputError(null);
    };
    rec.onresult = (e) => {
      let text = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        text += e.results[i][0].transcript;
      }
      setQuery(text);
    };
    rec.onend = () => setListening(false);
    rec.onerror = (event) => {
      setListening(false);
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        setVoiceInputError("মাইক্রোফোনের অনুমতি দিন");
      } else if (event.error !== "aborted") {
        setVoiceInputError("আবার চেষ্টা করুন");
      }
    };
    recognitionRef.current = rec;
  }, []);

  const toggleMic = useCallback(() => {
    const rec = recognitionRef.current as { start: () => void; stop: () => void } | null;
    if (!rec) return;
    if (listening) {
      rec.stop();
      setListening(false);
    } else {
      // Barge-in: speaking a new question stops any answer being read aloud.
      stopAllSpeech();
      setQuery("");
      setVoiceInputError(null);
      try {
        rec.start();
        setListening(true);
      } catch {
        setListening(false);
      }
    }
  }, [listening]);

  // Check local model availability (llama-server up + model loaded). Re-check
  // on window focus so starting the local server mid-session reveals the
  // "গবেষণা" option without a page reload. Any failure stays offline.
  const checkLocalAvailability = useCallback(() => {
    getModels()
      .then((ms) => {
        const local = ms.find((m) => m.id === "krishokchat-4b");
        setLocalAvailable(local?.available ?? false);
      })
      .catch(() => setLocalAvailable(false));
  }, []);

  useEffect(() => {
    checkLocalAvailability();
    window.addEventListener("focus", checkLocalAvailability);
    return () => window.removeEventListener("focus", checkLocalAvailability);
  }, [checkLocalAvailability]);

  // Scroll management — scroll ONLY the chat container, never the page.
  const scrollRef = useRef<HTMLDivElement>(null);
  const prevMsgCount = useRef(0);
  const keepScrolled = useRef(true);

  useEffect(() => {
    if (messages.length > prevMsgCount.current && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
    prevMsgCount.current = messages.length;
  }, [messages]);

  useEffect(() => {
    if (streamedText && keepScrolled.current && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [streamedText]);

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
      if (!q || streamingRef.current) return;

      // Barge-in: a new query stops any answer still being read aloud.
      stopAllSpeech();

      const userMsg: ChatMessageData = { role: "user", content: q };
      const newMessages = [...messages, userMsg];
      setMessages(newMessages);
      setStreaming(true);
      streamingRef.current = true;
      resetStreamBuffer();
      keepScrolled.current = true;
      setTraceEvents([{ stage: "safety", status: "start" }]);
      setQuery("");

      const fullHistory = newMessages
        .filter((m) => !(m.role === "assistant" && m.error))
        .slice(0, -1)
        .map((m) => ({
          role: m.role,
          content: m.content,
        }));

      try {
        const controller = new AbortController();
        requestRef.current = controller;
        const final = await streamQuestion(
          q,
          applyEvent,
          (token) => pushStreamToken(token),
          {
            crop: detectedCrop,
            disease: detectedDisease,
            session_id: sessionId,
            history: fullHistory,
            model,
            // The local CPU model needs minutes, not seconds, for a grounded
            // answer; the remote lane keeps the default (backend timeouts rule).
            timeoutMs: model === "krishokchat-4b" ? 300_000 : undefined,
            signal: controller.signal,
          },
        );

        // Ensure all buffered tokens are rendered before swapping to the final response
        flushStreamBuffer();

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
        if (requestRef.current?.signal.aborted) {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: "", error: "অনুরোধটি বাতিল করা হয়েছে। প্রশ্নটি আবার পাঠাতে পারেন।", retryQuery: q },
          ]);
          return;
        }
        const msg = e instanceof Error ? e.message : String(e);
        if (msg.includes("Failed to fetch") || msg.includes("fetch")) {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: "",
              error: "ব্যাকএন্ড সার্ভারে সংযোগ ব্যর্থ। নিশ্চিত করুন যে ব্যাকএন্ড চলছে।",
              retryQuery: q,
            },
          ]);
        } else {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: "", error: msg, retryQuery: q },
          ]);
        }
      } finally {
        requestRef.current = null;
        setStreaming(false);
        streamingRef.current = false;
        resetStreamBuffer();
        setTraceEvents([]);
      }
    },
    [messages, detectedCrop, detectedDisease, sessionId, applyEvent, model, pushStreamToken, flushStreamBuffer, resetStreamBuffer],
  );

  const clear = useCallback(() => {
    requestRef.current?.abort();
    resetStreamBuffer();
    setMessages([]);
    setTraceEvents([]);
    setQuery("");
    window.localStorage.removeItem(storageKey);
  }, [resetStreamBuffer]);

  const isEmpty = messages.length === 0;

  return (
    <div className="flex h-full min-h-0 flex-col">
      {/* Messages — scroll container */}
      <div
        ref={scrollRef}
        onScroll={(event) => {
          const node = event.currentTarget;
          keepScrolled.current = node.scrollHeight - node.scrollTop - node.clientHeight < 80;
        }}
        className="min-h-[220px] flex-1 space-y-5 overflow-y-auto pr-1 scrollbar-thin"
      >
        {isEmpty ? (
          <EmptyState
            onPick={send}
            detectedCrop={detectedCrop}
            detectedDisease={detectedDisease}
            compact={compact}
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
                  <ChatMessage
                    message={msg}
                    onRetry={msg.role === "assistant" && msg.retryQuery ? () => send(msg.retryQuery!) : undefined}
                  />
                  {msg.role === "assistant" && msg.response && !savedMessages.has(i) && (
                    <SaveAnswerButton
                      accessToken={session?.access_token ?? null}
                      queryText={messages[i - 1]?.content ?? msg.response.query}
                      response={msg.response}
                      onSaved={() => setSavedMessages((prev) => new Set(prev).add(i))}
                    />
                  )}
                  {isStreamingBubble && (
                    <ChatMessage
                      message={{ role: "assistant", content: "" }}
                      streaming={true}
                      traceEvents={traceEvents}
                      streamedText={streamedText}
                    />
                  )}
                </div>
              );
            })}
          </>
        )}
      </div>

      {/* Secondary controls stay quiet. Farmers only need the question box and
          one clear action; model selection is intentionally not presented as
          two competing primary buttons. */}
      <div className="mt-4 flex min-h-8 items-center justify-between gap-3 border-t rule pt-3">
        <div className="flex min-w-0 items-center gap-1.5 text-xs text-ink-faint">
          <ShieldCheck className="h-3.5 w-3.5 shrink-0 text-leaf" />
          <span className="truncate">তথ্যসূত্র মিলিয়ে নিরাপদ উত্তর</span>
        </div>

        <div className="flex shrink-0 items-center gap-3">
          {/* The selector is always visible so the choice is discoverable, but
              the local option is disabled (and labeled offline) when the local
              llama-server is not reachable — the remote lane stays the default. */}
          <label
            className="flex items-center gap-1.5 text-xs text-ink-faint"
            title={
              localAvailable
                ? "গবেষণা: লোকাল ফাইন-টিউনড মডেল"
                : "গবেষণা (অফলাইন): লোকাল সার্ভার চালু হলে পাওয়া যাবে"
            }
          >
            <span className="hidden sm:inline">উত্তরের ধরন</span>
            <select
              value={model}
              onChange={(event) => setModel(event.target.value as "gemini" | "krishokchat-4b")}
              className="rounded-md border rule bg-paper px-2 py-1 text-xs text-ink-soft focus:border-leaf focus:outline-none"
              aria-label="উত্তরের ধরন নির্বাচন করুন"
            >
              <option value="gemini">সাধারণ</option>
              <option value="krishokchat-4b" disabled={!localAvailable}>
                গবেষণা{!localAvailable ? " (অফলাইন)" : ""}
              </option>
            </select>
          </label>

          {!isEmpty && !streaming && (
            <button
              onClick={clear}
              title="নতুন কথোপকথন শুরু করুন"
              className="flex min-h-8 items-center gap-1 rounded-md px-1.5 text-xs font-medium text-ink-faint transition-colors hover:text-clay"
            >
              <RotateCcw className="h-3 w-3" />
              <span className="hidden sm:inline">নতুন করে শুরু</span>
            </button>
          )}
        </div>
      </div>

      {/* Input bar — text + voice + send. The mic lets low-literacy farmers
          speak their question in Bengali instead of typing on a phone. */}
      <div className="mt-2 flex items-stretch gap-2">
        <div className="focus-surface relative flex min-h-14 min-w-0 flex-1 items-center rounded-2xl border rule bg-paper transition-colors">
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
            placeholder={listening ? "শুনছি… কথা বলুন…" : "আপনার কৃষি প্রশ্ন লিখুন (বাংলায়)…"}
            className="min-h-[52px] w-full resize-none rounded-2xl border-0 bg-transparent px-4 py-3 pr-12 text-sm leading-relaxed text-ink placeholder:text-ink-faint focus:outline-none"
            style={{ maxHeight: "6rem" }}
          />
          {speechSupported && (
            <button
              onClick={toggleMic}
              type="button"
              aria-label={listening ? "রেকর্ড বন্ধ করুন" : "ভয়েস ইনপুট"}
              className={cn(
                "control-press absolute right-2 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-xl transition-colors",
                listening
                  ? "bg-clay/15 text-clay"
                  : "text-ink-faint hover:bg-leaf/10 hover:text-leaf",
              )}
            >
              {listening ? (
                <Square className="h-4 w-4 fill-current" />
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
          onClick={() => streaming ? requestRef.current?.abort() : send(query)}
          disabled={!streaming && !query.trim()}
          title={streaming ? "উত্তর তৈরি বন্ধ করুন" : "জিজ্ঞাসা করুন"}
          className={cn(
            "control-press flex h-14 shrink-0 items-center justify-center gap-2 rounded-2xl px-4 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-40 sm:min-w-[116px]",
            "bg-leaf text-paper shadow-sm hover:bg-leaf-2",
          )}
        >
          {streaming ? (
            <X className="h-4 w-4" />
          ) : (
            <Send className="h-4 w-4" />
          )}
          <span className="hidden sm:inline">{streaming ? "থামান" : "জিজ্ঞাসা করুন"}</span>
        </button>
      </div>
      {voiceInputError && (
        <p className="mt-1 text-right text-xs text-clay" role="status">
          {voiceInputError}
        </p>
      )}
    </div>
  );
}

/* --- Empty state: welcome + suggested questions --- */

/* Save-to-account action under completed answers (premium lane, P4).
   Visible ONLY when signed in; anonymous visitors see nothing (no buttons,
   no popups — amendment 15 invariant). Failures degrade to a retry label. */
function SaveAnswerButton({
  accessToken,
  queryText,
  response,
  onSaved,
}: {
  accessToken: string | null;
  queryText: string;
  response: import("@/lib/api").QAResponse;
  onSaved: () => void;
}) {
  const [state, setState] = useState<"idle" | "saving" | "saved" | "error">("idle");

  if (!accessToken) return null;

  // const arrow (not a hoisted declaration) so TS preserves the narrowing above.
  const handleSave = async () => {
    setState("saving");
    try {
      await saveAnswer(accessToken, {
        query_text: queryText,
        answer_text: response.answer,
        sources: response.sources,
        category: response.category,
      });
      setState("saved");
      onSaved();
    } catch {
      setState("error");
    }
  }

  return (
    <div className="flex items-center gap-2 pl-2">
      <button
        onClick={() => void handleSave()}
        disabled={state === "saving" || state === "saved"}
        className={cn(
          "control-press flex min-h-7 items-center gap-1.5 rounded-full border px-2.5 text-xs font-medium transition-colors",
          state === "saved"
            ? "border-leaf/30 bg-leaf/10 text-leaf"
            : "rule bg-paper text-ink-faint hover:border-leaf hover:text-leaf",
          state === "error" && "border-clay/30 text-clay",
        )}
      >
        {state === "saving" ? (
          <Loader2 className="h-3 w-3 animate-spin" />
        ) : state === "saved" ? (
          <Check className="h-3 w-3" />
        ) : (
          <Bookmark className="h-3 w-3" />
        )}
        {state === "saving"
          ? "সংরক্ষণ হচ্ছে…"
          : state === "saved"
            ? "সংরক্ষিত"
            : state === "error"
              ? "আবার চেষ্টা করুন"
              : "সংরক্ষণ করুন"}
      </button>
      {state === "idle" && <span className="text-xs text-ink-faint">আমার হিসাবে রাখুন</span>}
    </div>
  );
}

function EmptyState({
  onPick,
  detectedCrop,
  detectedDisease,
  compact = false,
}: {
  onPick: (q: string) => void;
  detectedCrop?: string | null;
  detectedDisease?: string | null;
  compact?: boolean;
}) {
  if (compact) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: dur.normal, ease: ease.smooth }}
        className="flex min-h-full flex-col justify-center py-4 text-center"
      >
        <div className="mb-2 mx-auto flex h-8 w-8 items-center justify-center rounded-full bg-leaf/10 text-leaf">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden>
            <path
              d="M4 18C4 11 9 6 20 5C19 14 13 18 4 18Z"
              fill="currentColor"
              opacity="0.85"
            />
          </svg>
        </div>
        <h3 className="font-display text-base text-ink">কৃষি জিজ্ঞাসা</h3>
        <p className="mt-0.5 text-xs text-ink-soft max-w-xs mx-auto">
          ফসলের রোগ বা পরিচর্যা নিয়ে প্রশ্ন করুন
        </p>
        <div className="mt-4 w-full text-left">
          <SuggestedQuestions
            onPick={onPick}
            crop={detectedCrop}
            disease={detectedDisease}
            showDialects={false}
          />
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="flex min-h-full flex-col items-center justify-center py-8 text-center"
    >
      <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-full bg-leaf/10 text-leaf">
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
      <p className="mb-0.5 text-xs font-semibold text-leaf">তথ্যভিত্তিক কৃষি সহায়তা</p>
      <h3 className="font-display text-xl text-ink">কী জানতে চান?</h3>
      <p className="mt-1 max-w-sm text-xs sm:text-sm leading-relaxed text-ink-soft">
        ফসলের রোগ, পরিচর্যা বা নিরাপদ বালাই ব্যবস্থাপনা নিয়ে প্রশ্ন করুন।
      </p>
      <div className="mt-6 w-full text-left">
        <SuggestedQuestions
          onPick={onPick}
          crop={detectedCrop}
          disease={detectedDisease}
          showDialects={true}
        />
      </div>
    </motion.div>
  );
}
