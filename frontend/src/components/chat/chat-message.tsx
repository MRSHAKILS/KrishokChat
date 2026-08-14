"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, AlertCircle, Eye, EyeOff, Copy, Check } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { QA_STAGES, PipelineRail, type RailEvent } from "@/components/detect/pipeline-rail";
import { AgentTrace } from "@/components/agent-trace";
import { ConfidenceBadge } from "./confidence-badge";
import { SourceList } from "./source-list";
import { SafetyNotice } from "./safety-notice";
import { ReadAloudButton } from "./read-aloud";
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
  | { role: "assistant"; content: string; response?: QAResponse; error?: string; retryQuery?: string };

export function ChatMessage({
  message,
  streaming,
  traceEvents,
  streamedText,
  onRetry,
}: {
  message: ChatMessageData;
  streaming?: boolean;
  traceEvents?: AgentStageEvent[];
  streamedText?: string;
  onRetry?: () => void;
}) {
  if (message.role === "user") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: dur.fast, ease: ease.smooth }}
        className="flex justify-end"
      >
        <div className="max-w-[85%] rounded-2xl rounded-br-md bg-leaf px-4 py-3 text-sm leading-relaxed text-paper shadow-sm">
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
      <div className="w-full max-w-4xl rounded-2xl rounded-bl-md border rule bg-paper-2/75 px-4 py-4 shadow-[0_4px_18px_rgba(52,39,23,0.045)] sm:px-5">
        {streaming ? (
          <StreamingContent events={traceEvents ?? []} text={streamedText ?? ""} />
        ) : message.error ? (
          <ErrorContent error={message.error} onRetry={onRetry} />
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

function StreamingContent({ events, text }: { events: AgentStageEvent[]; text: string }) {
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
      {text && (
        <p aria-live="polite" className="whitespace-pre-wrap text-sm leading-relaxed text-ink">
          {text}
           <span className="stream-caret ml-1 inline-block h-4 w-0.5 bg-leaf align-middle" />
        </p>
      )}
      <AgentTrace
        stages={QA_STAGES}
        events={railEvents}
        active={true}
        title="উত্তর তৈরির এজেন্ট প্রবাহ"
        detail={activeLabel ? `${activeLabel} ধাপ চলছে` : undefined}
      />
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

function ErrorContent({ error, onRetry }: { error: string; onRetry?: () => void }) {
  return (
    <div className="rounded-md border border-clay-soft/40 bg-clay-soft/15 px-3 py-3 text-sm text-clay">
      <p>ত্রুটি: {error}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 flex min-h-11 items-center rounded-lg font-semibold text-leaf"
        >
          আবার চেষ্টা করুন
        </button>
      )}
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

function CompletedContent({ response }: { response: QAResponse }) {
  const blocked = response.category !== "safe_agri";
  const [traceOpen, setTraceOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  // Safety-blocked query → show SafetyNotice
  if (blocked) {
    return (
      <SafetyNotice
        category={response.category}
        answer={response.answer}
        matchedRules={response.matched_rules}
      />
    );
  }

  const cleanAnswer = formatAnswerWithCleanCitations(response.answer, response.sources);

  const copyAnswer = async () => {
    try {
      await navigator.clipboard.writeText(response.answer);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div className="space-y-3">
      {/* Answer text with styled citation pills */}
      <motion.p
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: dur.fast, ease: ease.smooth }}
        className="whitespace-pre-wrap text-[0.95rem] leading-[1.85] text-ink"
      >
        <FormattedAnswerText text={cleanAnswer} />
      </motion.p>

      {/* Keep the answer actions to one useful voice control and one optional
          detail link. The verification badge is informational, not a button. */}
      <div className="flex flex-wrap items-center gap-2 border-t rule pt-3">
        <ConfidenceBadge confidence={response.confidence} />

        <ReadAloudButton text={response.answer} />

        <button
          onClick={copyAnswer}
          type="button"
          aria-label="উত্তর কপি করুন"
          className="control-press flex min-h-9 items-center gap-1.5 rounded-lg border border-bone px-3 text-xs font-medium text-ink-faint hover:border-leaf/30 hover:text-leaf"
        >
          {copied ? <Check className="h-3.5 w-3.5 text-leaf" /> : <Copy className="h-3.5 w-3.5" />}
          <span>{copied ? "কপি হয়েছে" : "কপি"}</span>
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
