"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, AlertCircle, Eye, EyeOff } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { QA_STAGES, PipelineRail, type RailEvent } from "@/components/detect/pipeline-rail";
import { ConfidenceBadge } from "./confidence-badge";
import { SourceList } from "./source-list";
import { SafetyNotice } from "./safety-notice";
import { HELPLINE } from "@/lib/constants";
import type { QAResponse, AgentStageEvent } from "@/lib/api";

/* =========================================================================
   ChatMessage — renders one message in the conversation.

   User messages: right-aligned leaf-green bubble.

   Assistant messages (during streaming):
     - PipelineRail (QA_STAGES) lighting up as SSE events arrive
     - "লেখছে…" indicator

   Assistant messages (after completion):
     - If blocked (non-safe_agri category): SafetyNotice
     - If answered: answer text + ConfidenceBadge + verifier flags + SourceList
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

/* --- Completed state: answer + confidence + sources + flags + trace toggle --- */

function CompletedContent({ response }: { response: QAResponse }) {
  const blocked = response.category !== "safe_agri";
  const [traceOpen, setTraceOpen] = useState(false);

  // Safety-blocked query → show SafetyNotice
  if (blocked) {
    return <SafetyNotice category={response.category} answer={response.answer} />;
  }

  // Normal answered query
  return (
    <div className="space-y-3">
      {/* Answer text */}
      <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink">
        {response.answer}
      </p>

      {/* Confidence + trace toggle row */}
      <div className="flex items-center gap-3">
        <ConfidenceBadge confidence={response.confidence} />
        {response.agent_trace.length > 0 && (
          <button
            onClick={() => setTraceOpen((v) => !v)}
            className="flex items-center gap-1 text-[11px] uppercase tracking-[0.14em] text-ink-faint transition-colors hover:text-leaf"
          >
            {traceOpen ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
            ধাপ
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
