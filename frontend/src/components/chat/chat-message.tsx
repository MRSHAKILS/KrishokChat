"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, AlertCircle, Eye, EyeOff, Copy, Check, Sprout } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { QA_STAGES, PipelineRail, type RailEvent } from "@/components/detect/pipeline-rail";
import { AgentTrace } from "@/components/agent-trace";
import { ConfidenceBadge } from "./confidence-badge";
import { ResolutionBadge } from "./resolution-badge";
import { SourceList } from "./source-list";
import { SafetyNotice } from "./safety-notice";
import { ReadAloudButton, splitBengaliSentences } from "./read-aloud";
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
  onSelectSuggestion,
}: {
  message: ChatMessageData;
  streaming?: boolean;
  traceEvents?: AgentStageEvent[];
  streamedText?: string;
  onRetry?: () => void;
  onSelectSuggestion?: (text: string) => void;
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
          <CompletedContent response={message.response} onSelectSuggestion={onSelectSuggestion} />
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
        <div className="rounded-xl border border-bone/60 bg-paper/60 p-4 transition-all">
          <p aria-live="polite" className="whitespace-pre-wrap text-sm leading-relaxed text-ink font-sans">
            {text}
            <span
              className="stream-caret ml-1.5 inline-block h-4 w-1 rounded-full bg-leaf align-middle shadow-[0_0_6px_rgba(47,93,58,0.4)]"
              aria-hidden="true"
            />
          </p>
        </div>
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

function FormattedAnswerText({
  text,
  activeSentenceIndex,
}: {
  text: string;
  activeSentenceIndex?: number | null;
}) {
  if (!text) return null;
  const sentences = splitBengaliSentences(text);

  return (
    <span>
      {sentences.map((sentence, sIdx) => {
        const isActive = activeSentenceIndex === sIdx;
        const parts = sentence.split(/(\[\s*[১-১০1-9]+\s*\])/g);

        return (
          <span
            key={sIdx}
            className={cn(
              "transition-all duration-200",
              isActive &&
                "bg-ochre-soft/35 text-ink font-medium rounded px-1 py-0.5 shadow-2xs border-b border-ochre/40 inline-block my-0.5"
            )}
          >
            {parts.map((part, pIdx) => {
              const match = part.match(/^\[\s*([১-১০1-9]+)\s*\]$/);
              if (match) {
                const num = match[1];
                return (
                  <span
                    key={pIdx}
                    title={`উৎস [${num}] দেখুন`}
                    className="mx-0.5 inline-flex items-center justify-center rounded bg-leaf/12 px-1.5 py-0.5 font-mono text-xs font-bold text-leaf transition-colors hover:bg-leaf hover:text-paper cursor-pointer"
                  >
                    [{num}]
                  </span>
                );
              }
              return part;
            })}
            {" "}
          </span>
        );
      })}
    </span>
  );
}

function CompletedContent({
  response,
  onSelectSuggestion,
}: {
  response: QAResponse;
  onSelectSuggestion?: (text: string) => void;
}) {
  const blocked = response.category !== "safe_agri";
  const [traceOpen, setTraceOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeSentenceIndex, setActiveSentenceIndex] = useState<number | null>(null);

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
  const isClarification = response.resolution_tier === "interactive_clarification";

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
      {/* KAERA A3 Progressive Non-Chemical Guidance Badge */}
      {response.progressive_guidance && (
        <div className="flex items-center gap-2 rounded-xl bg-leaf/10 border border-leaf/20 px-3.5 py-2 text-xs font-semibold text-leaf shadow-2xs">
          <Sprout className="h-4 w-4 shrink-0" />
          <span>পরিবেশবান্ধব ও সাধারণ পরিচর্যা নির্দেশিকা (নন-কেমিক্যাল)</span>
        </div>
      )}

      {/* Answer text with styled citation pills and synchronized TTS highlighting */}
      <motion.p
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: dur.fast, ease: ease.smooth }}
        className="whitespace-pre-wrap text-[0.95rem] leading-[1.85] text-ink"
      >
        <FormattedAnswerText text={cleanAnswer} activeSentenceIndex={activeSentenceIndex} />
      </motion.p>

      {/* Interactive Crop Chips on Clarification Turns */}
      {isClarification && onSelectSuggestion && (
        <div className="rounded-xl border border-ochre-soft/40 bg-ochre-soft/10 p-3">
          <div className="mb-2 text-xs font-semibold text-ink-soft">
            নির্দিষ্ট ফসল নির্বাচন করে দ্রুত উত্তর পান:
          </div>
          <div className="flex flex-wrap gap-2">
            {[
              { label: "🌾 ধান (Rice)", value: "ধান" },
              { label: "🥔 আলু (Potato)", value: "আলু" },
              { label: "🍅 টমেটো (Tomato)", value: "টমেটো" },
              { label: "🌽 ভুট্টা (Maize)", value: "ভুট্টা" },
              { label: "🍆 বেগুন (Brinjal)", value: "বেগুন" },
              { label: "🌶️ মরিচ (Chilli)", value: "মরিচ" },
            ].map((item) => (
              <button
                key={item.value}
                type="button"
                onClick={() => onSelectSuggestion(item.value)}
                className="control-press inline-flex items-center gap-1.5 rounded-full border border-leaf/30 bg-paper px-3 py-1.5 text-xs font-medium text-leaf shadow-2xs transition-colors hover:bg-leaf hover:text-paper"
              >
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Keep the answer actions to one useful voice control and one optional
          detail link. The verification badge is informational, not a button. */}
      <div className="flex flex-wrap items-center gap-2 border-t rule pt-3">
        <ConfidenceBadge confidence={response.confidence} />
        {/* R3: how the answer was produced — tier badge (absent on stale backend) */}
        <ResolutionBadge tier={response.resolution_tier} />

        {/* Institutional Evidence Grounding Badge */}
        {response.sources && response.sources.length > 0 && response.confidence === "verified" && (
          <span
            title="জাতীয় কৃষি গবেষণা প্রতিষ্ঠানের সত্যায়িত তথ্যভিত্তিক"
            className="inline-flex items-center gap-1.5 rounded-full border border-leaf/30 bg-leaf/10 px-2.5 py-0.5 text-xs font-semibold text-leaf shadow-2xs"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-leaf" />
            {response.sources[0]?.publisher || response.sources[0]?.publisher_bn || (
              response.sources.some((s) => s.citation?.includes("BARI") || s.id?.includes("BARI")) ? "BARI" :
              response.sources.some((s) => s.citation?.includes("BRRI") || s.id?.includes("BRRI")) ? "BRRI" :
              response.sources.some((s) => s.citation?.includes("DAE") || s.id?.includes("DAE")) ? "DAE" :
              response.sources.some((s) => s.citation?.includes("BARC") || s.id?.includes("BARC")) ? "BARC" :
              "জাতীয় কৃষি উৎস"
            )}
          </span>
        )}

        <ReadAloudButton text={response.answer} onSentenceChange={setActiveSentenceIndex} />

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
