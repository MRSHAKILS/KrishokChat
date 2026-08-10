"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, AlertCircle, Eye, EyeOff, Volume2, VolumeX } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { QA_STAGES, PipelineRail, type RailEvent } from "@/components/detect/pipeline-rail";
import { ConfidenceBadge } from "./confidence-badge";
import { SourceList } from "./source-list";
import { SafetyNotice } from "./safety-notice";
import { HELPLINE } from "@/lib/constants";
import { type QAResponse, type SourceNode, type AgentStageEvent } from "@/lib/api";

/* =========================================================================
   ChatMessage — renders one message in the conversation.

   User messages: right-aligned leaf-green bubble.

   Assistant messages (during streaming):
     - PipelineRail (QA_STAGES) lighting up as SSE events arrive
     - "লেখছে…" indicator

   Assistant messages (after completion):
   - If blocked (non-safe_agri category): SafetyNotice
   - If answered: answer text + ConfidenceBadge + verifier flags + SourceList
   - One browser voice control and a collapsible process trace
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
      <div className="w-full max-w-4xl rounded-xl rounded-bl-sm border rule bg-paper-2/80 px-4 py-4 shadow-sm sm:px-5">
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
  const activeEvent = [...events]
    .reverse()
    .find((event) => event.status === "start" || event.status === "active");
  const activeLabel = QA_STAGES.find((stage) => stage.key === activeEvent?.stage)?.label;

  return (
    <div className="space-y-4">
      <div className="rounded-xl border rule bg-paper/60 p-3 sm:p-4">
        <PipelineRail stages={QA_STAGES} events={railEvents} active={true} />
      </div>
      <motion.div
        animate={{ opacity: [0.55, 1, 0.55] }}
        transition={{ duration: 1.4, repeat: Infinity, ease: "easeInOut" }}
        className="flex items-center gap-2 text-sm text-ink-soft"
      >
        <span>{genActive ? "উত্তর তৈরি হচ্ছে" : activeLabel ? `${activeLabel} চলছে` : "উত্তর প্রস্তুত হচ্ছে"}</span>
        <span className="flex gap-0.5">
          <Dot /> <Dot delay={0.15} /> <Dot delay={0.3} />
        </span>
      </motion.div>
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

/* --- Completed state: answer + confidence + sources + flags + voice --- */

function formatAnswerWithCleanCitations(text: string, sources: SourceNode[] = []) {
  if (!text) return text;
  // Match [ID] including uppercase, lowercase, numbers, underscores, hyphens
  const tagRegex = /\[([A-Za-z0-9_\-]+)\]/g;
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

function getVoicesWhenReady(synth: SpeechSynthesis): Promise<SpeechSynthesisVoice[]> {
  const voices = synth.getVoices();
  if (voices.length > 0) return Promise.resolve(voices);

  return new Promise((resolve) => {
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timeoutId);
      synth.removeEventListener("voiceschanged", finish);
      resolve(synth.getVoices());
    };

    synth.addEventListener("voiceschanged", finish);
    // Some browsers do not emit voiceschanged until a second synthesis call.
    // A short timeout still lets the system default voice work.
    const timeoutId = window.setTimeout(finish, 450);
  });
}

function CompletedContent({ response }: { response: QAResponse }) {
  const blocked = response.category !== "safe_agri";
  const [traceOpen, setTraceOpen] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [speechError, setSpeechError] = useState(false);
  const speechRequest = useRef(0);

  useEffect(() => {
    return () => {
      speechRequest.current += 1;
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  // Safety-blocked query → show SafetyNotice
  if (blocked) {
    return <SafetyNotice category={response.category} answer={response.answer} />;
  }

  const cleanAnswer = formatAnswerWithCleanCitations(response.answer, response.sources);

  const toggleSpeech = async (textToRead: string) => {
    if (typeof window === "undefined") return;
    const synth = "speechSynthesis" in window ? window.speechSynthesis : null;

    if (speaking) {
      speechRequest.current += 1;
      synth?.cancel();
      setSpeaking(false);
      return;
    }

    const cleanText = textToRead
      .replace(/\[[^\]]+\]/g, "")
      .replace(/\s+/g, " ")
      .trim();
    if (!cleanText) return;

    if (!synth) {
      setSpeechError(true);
      return;
    }

    const requestId = ++speechRequest.current;
    setSpeechError(false);
    setSpeaking(true);

    synth.cancel();
    const voices = await getVoicesWhenReady(synth);
    if (speechRequest.current !== requestId) return;

    const bnVoice = voices.find(
      (voice) =>
        voice.lang.toLowerCase().startsWith("bn") ||
        voice.name.toLowerCase().includes("bengali"),
    );
    const selectedVoice = bnVoice ?? voices.find((voice) => voice.default) ?? voices[0];
    const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 1000));
    // Prefer a Bengali system voice. If the device has none, use its default
    // voice rather than silently failing with language-unavailable.
    utterance.lang = selectedVoice?.lang ?? "bn-BD";
    utterance.rate = 0.88;
    if (selectedVoice) utterance.voice = selectedVoice;

    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = (event) => {
      if (event.error !== "canceled" && event.error !== "interrupted") {
        setSpeechError(true);
      }
      setSpeaking(false);
    };

    // A brief yield after cancel prevents Chrome from dropping the new
    // utterance when a previous answer was just stopped.
    window.setTimeout(() => {
      if (speechRequest.current !== requestId) return;
      synth.resume();
      synth.speak(utterance);
    }, 40);
  };

  return (
    <div className="space-y-3">
      {/* Answer text with styled citation pills */}
      <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink">
        <FormattedAnswerText text={cleanAnswer} />
      </p>

      {/* Keep the answer actions to one useful voice control and one optional
          detail link. The verification badge is informational, not a button. */}
      <div className="flex flex-wrap items-center gap-2 border-t rule pt-3">
        <ConfidenceBadge confidence={response.confidence} />

        <button
          onClick={() => toggleSpeech(response.answer)}
          type="button"
          aria-label={speaking ? "আবৃত্তি বন্ধ করুন" : "পরামর্শটি শুনুন"}
          className={cn(
            "flex min-h-9 items-center gap-1.5 rounded-lg border px-3 text-xs font-medium transition-colors active:scale-[0.98]",
            speaking
              ? "border-leaf bg-leaf text-paper"
              : "border-leaf/25 bg-leaf/8 text-leaf hover:bg-leaf/15",
          )}
        >
          {speaking ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
          <span>{speaking ? "থামুন" : "শুনুন"}</span>
        </button>

        {response.agent_trace.length > 0 && (
          <button
            onClick={() => setTraceOpen((v) => !v)}
            aria-expanded={traceOpen}
            className="flex min-h-9 items-center gap-1 rounded-lg px-2 text-xs font-medium text-ink-faint transition-colors hover:text-leaf"
          >
            {traceOpen ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
            প্রক্রিয়া দেখুন
            <ChevronDown className={cn("h-3 w-3 transition-transform", traceOpen && "rotate-180")} />
          </button>
        )}
      </div>
      {speechError && (
        <p className="text-[11px] text-clay" role="status">
          এই ব্রাউজারে শব্দ চালু করা যায়নি। ব্রাউজারের শব্দ ও স্পিকারের অনুমতি পরীক্ষা করুন।
        </p>
      )}

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
