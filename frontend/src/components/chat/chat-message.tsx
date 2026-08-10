"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, AlertCircle, Eye, EyeOff, Volume2, VolumeX, Globe, Loader2, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { QA_STAGES, PipelineRail, type RailEvent } from "@/components/detect/pipeline-rail";
import { ConfidenceBadge } from "./confidence-badge";
import { SourceList } from "./source-list";
import { SafetyNotice } from "./safety-notice";
import { HELPLINE } from "@/lib/constants";
import { translateDialect, type QAResponse, type SourceNode, type AgentStageEvent } from "@/lib/api";

/* =========================================================================
   ChatMessage — renders one message in the conversation.

   User messages: right-aligned leaf-green bubble.

   Assistant messages (during streaming):
     - PipelineRail (QA_STAGES) lighting up as SSE events arrive
     - "লেখছে…" indicator

   Assistant messages (after completion):
     - If blocked (non-safe_agri category): SafetyNotice
     - If answered: answer text + ConfidenceBadge + verifier flags + SourceList
     - Regional Dialect Translator (Gemini 2.5 Flash Lite) + Voice TTS
     - Collapsible "ধাপ দেখুন" toggle for the trace
   ========================================================================= */

export type ChatMessageData =
  | { role: "user"; content: string }
  | { role: "assistant"; content: string; response?: QAResponse; error?: string };

export function ChatMessage({
  message,
  streaming,
  traceEvents,
}: {
  message: ChatMessageData;
  streaming?: boolean;
  traceEvents?: AgentStageEvent[];
}) {
  if (message.role === "user") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: dur.fast, ease: ease.smooth }}
        className="flex justify-end"
      >
        <div className="max-w-[85%] rounded-lg rounded-br-sm bg-leaf px-4 py-2.5 text-sm leading-relaxed text-paper">
          {message.content}
        </div>
      </motion.div>
    );
  }

  // Assistant message
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="flex justify-start"
    >
      <div className="w-full max-w-[88%] rounded-lg rounded-bl-sm bg-paper-2 px-4 py-3">
        {streaming ? (
          <StreamingContent events={traceEvents ?? []} />
        ) : message.error ? (
          <ErrorContent error={message.error} />
        ) : message.response ? (
          <CompletedContent response={message.response} />
        ) : (
          <p className="text-sm leading-relaxed text-ink">{message.content}</p>
        )}
      </div>
    </motion.div>
  );
}

/* --- Streaming state: pipeline rail + typing indicator --- */

function StreamingContent({ events }: { events: AgentStageEvent[] }) {
  const railEvents: RailEvent[] = events.map((e) => ({
    stage: e.stage,
    status: e.status,
    detail: e.detail,
  }));

  // Check if generation stage is active (show typing indicator)
  const genActive = events.some(
    (e) => e.stage === "generation" && (e.status === "start" || e.status === "active"),
  );

  return (
    <div className="space-y-3">
      <PipelineRail stages={QA_STAGES} events={railEvents} active={true} />
      {genActive && (
        <motion.div
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 1.2, repeat: Infinity, ease: "easeInOut" }}
          className="flex items-center gap-1 text-sm text-ink-soft"
        >
          <span>লেখছে</span>
          <span className="flex gap-0.5">
            <Dot /> <Dot delay={0.15} /> <Dot delay={0.3} />
          </span>
        </motion.div>
      )}
    </div>
  );
}

function Dot({ delay = 0 }: { delay?: number }) {
  return (
    <motion.span
      animate={{ opacity: [0.3, 1, 0.3] }}
      transition={{ duration: 1, repeat: Infinity, delay, ease: "easeInOut" }}
      className="block h-1 w-1 rounded-full bg-ink-soft"
    />
  );
}

/* --- Error state --- */

function ErrorContent({ error }: { error: string }) {
  return (
    <div className="rounded-md border border-clay-soft/40 bg-clay-soft/15 px-3 py-2 text-sm text-clay">
      ত্রুটি: {error}
    </div>
  );
}

/* --- Completed state: answer + confidence + sources + flags + dialect/voice --- */

function formatAnswerWithCleanCitations(text: string, sources: SourceNode[] = []) {
  if (!text) return text;
  const tagRegex = /\[([A-Z0-9_]+)\]/g;
  const bnDigits = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "১০"];

  return text.replace(tagRegex, (match, id) => {
    const idx = sources.findIndex((s) => s.id === id);
    if (idx >= 0) {
      const digit = bnDigits[idx] || String(idx + 1);
      return ` [${digit}] `;
    }
    return "";
  }).trim();
}

function FormattedAnswerText({ text }: { text: string }) {
  if (!text) return null;
  const parts = text.split(/(\[\s*[১-১০1-9]+\s*\])/g);
  return (
    <span>
      {parts.map((part, i) => {
        const match = part.match(/^\[\s*([১-১০1-9]+)\s*\]$/);
        if (match) {
          const num = match[1];
          return (
            <span
              key={i}
              title={`উৎস [${num}] দেখুন`}
              className="mx-0.5 inline-flex items-center justify-center rounded bg-leaf/12 px-1.5 py-0.5 font-mono text-xs font-bold text-leaf transition-colors hover:bg-leaf hover:text-paper cursor-pointer"
            >
              [{num}]
            </span>
          );
        }
        return part;
      })}
    </span>
  );
}

function CompletedContent({ response }: { response: QAResponse }) {
  const blocked = response.category !== "safe_agri";
  const [traceOpen, setTraceOpen] = useState(false);
  const [speaking, setSpeaking] = useState(false);

  // Safety-blocked query → show SafetyNotice
  if (blocked) {
    return <SafetyNotice category={response.category} answer={response.answer} />;
  }

  const cleanAnswer = formatAnswerWithCleanCitations(response.answer, response.sources);

  const toggleSpeech = (textToRead: string) => {
    if (typeof window === "undefined") return;
    if (speaking) {
      if ("speechSynthesis" in window) window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    const cleanText = textToRead.replaceAll(/\[[A-Z0-9_]+\]/g, "").trim();
    if (!cleanText) return;

    setSpeaking(true);

    const playFallbackAudio = () => {
      try {
        const chunk = encodeURIComponent(cleanText.slice(0, 200));
        const audio = new Audio(`https://translate.google.com/translate_tts?ie=UTF-8&q=${chunk}&tl=bn&client=tw-ob`);
        audio.onended = () => setSpeaking(false);
        audio.onerror = () => setSpeaking(false);
        audio.play().catch(() => setSpeaking(false));
      } catch {
        setSpeaking(false);
      }
    };

    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      const voices = window.speechSynthesis.getVoices();
      const bnVoice = voices.find(
        (v) => v.lang.includes("bn") || v.lang.includes("BD") || v.name.toLowerCase().includes("bengali"),
      );

      const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 300));
      utterance.lang = "bn-BD";
      utterance.rate = 0.88;
      if (bnVoice) utterance.voice = bnVoice;

      utterance.onend = () => setSpeaking(false);
      utterance.onerror = () => playFallbackAudio();

      window.speechSynthesis.speak(utterance);
    } else {
      playFallbackAudio();
    }
  };

  return (
    <div className="space-y-3">
      {/* Answer text with styled citation pills */}
      <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink">
        <FormattedAnswerText text={cleanAnswer} />
      </p>

      {/* Action Row: Confidence + Voice Reader + Trace toggle */}
      <div className="flex flex-wrap items-center gap-2.5">
        <ConfidenceBadge confidence={response.confidence} />

        {/* Voice TTS Speaker button */}
        <button
          onClick={() => toggleSpeech(response.answer)}
          type="button"
          aria-label={speaking ? "আবৃত্তি বন্ধ করুন" : "পরামর্শটি শুনুন"}
          className={cn(
            "flex items-center gap-1 rounded-md px-2 py-0.5 text-xs font-medium transition-colors",
            speaking
              ? "bg-leaf text-paper"
              : "bg-leaf/10 text-leaf hover:bg-leaf/20",
          )}
        >
          {speaking ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
          <span>{speaking ? "থামুন" : "শুনুন"}</span>
        </button>

        {response.agent_trace.length > 0 && (
          <button
            onClick={() => setTraceOpen((v) => !v)}
            className="flex items-center gap-1 text-[11px] font-semibold text-ink-faint transition-colors hover:text-leaf"
          >
            {traceOpen ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
            ধাপ
            <ChevronDown className={cn("h-3 w-3 transition-transform", traceOpen && "rotate-180")} />
          </button>
        )}
      </div>

      {/* Regional Dialect Translator (Gemini 2.5 Flash Lite) */}
      <DialectTranslator originalText={response.answer} />

      {/* Verifier flags */}
      {response.verifier_flags.length > 0 && (
        <div className="space-y-1">
          {response.verifier_flags.map((flag, i) => (
            <div
              key={i}
              className="flex items-start gap-2 rounded-md border border-ochre-soft/40 bg-ochre-soft/10 px-3 py-2 text-xs text-ink-soft"
            >
              <AlertCircle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-ochre" />
              <span>{flag}</span>
            </div>
          ))}
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="inline-block text-xs font-medium text-leaf transition-colors hover:text-leaf-2"
          >
            নিশ্চিত হতে কৃষক কল সেন্টারে যোগাযোগ করুন: {HELPLINE.krishiCallCenter}
          </a>
        </div>
      )}

      {/* Sources */}
      <SourceList sources={response.sources} />

      {/* Collapsible trace rail */}
      <AnimatePresence>
        {traceOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="overflow-hidden border-t rule pt-3"
          >
            <PipelineRail
              stages={QA_STAGES}
              events={response.agent_trace.map((e) => ({
                stage: e.stage,
                status: e.status,
                detail: e.detail,
              }))}
              active={false}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* --- Regional Dialect Translator Sub-component --- */

const DIALECT_OPTIONS = [
  { id: "noakhali", label: "নোয়াখালী" },
  { id: "chattagram", label: "চাটগাঁইয়া" },
  { id: "sylhet", label: "সিলেটি" },
  { id: "rajshahi", label: "রাজশাহী" },
  { id: "rangpur", label: "রংপুর" },
] as const;

function DialectTranslator({ originalText }: { originalText: string }) {
  const [selected, setSelected] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [translations, setTranslations] = useState<Record<string, { name: string; text: string }>>({});
  const [speaking, setSpeaking] = useState(false);

  const handleSelect = async (dialectId: string) => {
    if (selected === dialectId) {
      setSelected(null);
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      setSpeaking(false);
      return;
    }
    setSelected(dialectId);

    if (translations[dialectId]) return;

    const opt = DIALECT_OPTIONS.find((o) => o.id === dialectId);
    const defaultLabel = opt ? opt.label : dialectId;

    setLoading(true);
    try {
      const res = await translateDialect(originalText, dialectId);
      setTranslations((prev) => ({
        ...prev,
        [dialectId]: { name: res.dialect_name, text: res.translated_bn },
      }));
    } catch {
      // Fallback clean Bengali advice text without raw DB tags
      const cleanOriginal = originalText.replaceAll(/\[[A-Z0-9_]+\]/g, "").trim();
      setTranslations((prev) => ({
        ...prev,
        [dialectId]: { name: defaultLabel, text: cleanOriginal },
      }));
    } finally {
      setLoading(false);
    }
  };

  const toggleDialectSpeech = (textToRead: string) => {
    if (typeof window === "undefined") return;
    if (speaking) {
      if ("speechSynthesis" in window) window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    const cleanText = textToRead.replaceAll(/\[[A-Z0-9_]+\]/g, "").trim();
    if (!cleanText) return;

    setSpeaking(true);

    const playFallbackAudio = () => {
      try {
        const chunk = encodeURIComponent(cleanText.slice(0, 200));
        const audio = new Audio(`https://translate.google.com/translate_tts?ie=UTF-8&q=${chunk}&tl=bn&client=tw-ob`);
        audio.onended = () => setSpeaking(false);
        audio.onerror = () => setSpeaking(false);
        audio.play().catch(() => setSpeaking(false));
      } catch {
        setSpeaking(false);
      }
    };

    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      const voices = window.speechSynthesis.getVoices();
      const bnVoice = voices.find(
        (v) => v.lang.includes("bn") || v.lang.includes("BD") || v.name.toLowerCase().includes("bengali"),
      );

      const u = new SpeechSynthesisUtterance(cleanText.slice(0, 300));
      u.lang = "bn-BD";
      u.rate = 0.88;
      if (bnVoice) u.voice = bnVoice;

      u.onend = () => setSpeaking(false);
      u.onerror = () => playFallbackAudio();

      window.speechSynthesis.speak(u);
    } else {
      playFallbackAudio();
    }
  };

  const currentTranslation = selected ? translations[selected] : null;

  return (
    <div className="mt-2 space-y-2 border-t rule pt-2">
      <div className="flex flex-wrap items-center gap-1.5 text-[11px] text-ink-faint">
        <span className="flex items-center gap-1 font-semibold text-leaf">
          <Globe className="h-3 w-3" />
          উপভাষা:
        </span>
        {DIALECT_OPTIONS.map((d) => {
          const active = selected === d.id;
          return (
            <button
              key={d.id}
              onClick={() => handleSelect(d.id)}
              className={cn(
                "rounded-md px-2 py-0.5 transition-colors",
                active
                  ? "bg-leaf text-paper font-medium"
                  : "bg-paper hover:bg-leaf/10 hover:text-leaf text-ink-soft",
              )}
            >
              {d.label} {active ? "✓" : ""}
            </button>
          );
        })}
      </div>

      <AnimatePresence mode="wait">
        {selected && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden rounded-lg border border-leaf/25 bg-leaf/5 p-3"
          >
            {loading ? (
              <div className="flex items-center gap-2 text-xs text-leaf">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span>Gemini এআই উপভাষায় রূপান্তর করছে…</span>
              </div>
            ) : currentTranslation ? (
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs font-semibold text-leaf">
                  <span className="flex items-center gap-1">
                    <Sparkles className="h-3 w-3" />
                    {currentTranslation.name} উপভাষায় পরামর্শ:
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => toggleDialectSpeech(currentTranslation.text)}
                      className="flex items-center gap-1 text-[11px] font-medium text-leaf hover:underline"
                    >
                      {speaking ? <VolumeX className="h-3 w-3" /> : <Volume2 className="h-3 w-3" />}
                      {speaking ? "থামুন" : "উপভাষায় শুনুন"}
                    </button>
                    <button
                      onClick={() => {
                        setSelected(null);
                        if (typeof window !== "undefined" && "speechSynthesis" in window) {
                          window.speechSynthesis.cancel();
                        }
                        setSpeaking(false);
                      }}
                      className="text-[11px] font-medium text-ink-faint hover:text-clay"
                      title="প্রমিত বাংলায় ফিরে যান"
                    >
                      ✕ বন্ধ করুন
                    </button>
                  </div>
                </div>
                <p className="text-xs leading-relaxed text-ink">{currentTranslation.text}</p>
              </div>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

