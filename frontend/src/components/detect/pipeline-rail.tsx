"use client";

import { motion } from "motion/react";
import { cn } from "@/lib/utils";
import { stagger, enter, dur, ease } from "@/lib/motion";
import { STAGE_LABELS } from "@/lib/constants";

/* =========================================================================
   PipelineRail — the agentic workflow visualization.
   A horizontal rail of N nodes connected by flow lines that light up
   sequentially as the backend reports stage events.

   Reusable: pass any stage list. The vision pipeline uses
   ["intake","crop_classification","disease_classification","advisory"]
   and the QA pipeline uses ["safety","retrieval","generation","verifier"].
   ========================================================================= */

export interface RailStage {
  key: string;
  label: string;
}

export interface RailEvent {
  stage: string;
  status: string; // pending | start/active | complete | skip | error
  detail?: string | null;
}

type NodeStatus = "pending" | "active" | "complete" | "skip" | "error";

function resolveStatus(ev: RailEvent | undefined): NodeStatus {
  if (!ev) return "pending";
  const s = ev.status;
  if (s === "complete") return "complete";
  if (s === "skip") return "skip";
  if (s === "error") return "error";
  if (s === "start" || s === "active") return "active";
  return "pending";
}

export function PipelineRail({
  stages,
  events,
  active = false,
}: {
  stages: RailStage[];
  events: RailEvent[];
  active?: boolean; // true while the pipeline is running
}) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={stagger}
      className="flex items-start gap-0"
    >
      {stages.map((stage, i) => {
        const ev = events.find((e) => e.stage === stage.key);
        const hasRunningStage = events.some((event) => {
          const eventStatus = resolveStatus(event);
          return eventStatus === "active" || eventStatus === "complete";
        });
        const status = active && !hasRunningStage && i === 0 ? "active" : resolveStatus(ev);
        const isLast = i === stages.length - 1;

        return (
          <div key={stage.key} className="flex items-stretch" style={{ flex: 1 }}>
            {/* Node + label column */}
            <motion.div variants={enter} className="flex min-w-0 flex-col items-center" style={{ minWidth: 52 }}>
               <RailNode status={status} active={active} />
              <div
                className={cn(
                  "mt-2 max-w-[72px] text-center text-[10px] font-medium leading-tight transition-colors sm:max-w-[100px] sm:text-[11px]",
                  status === "pending" && "text-ink-faint",
                  status === "active" && "text-ochre",
                  status === "complete" && "text-ink",
                  status === "skip" && "text-ink-faint line-through",
                  status === "error" && "text-clay",
                )}
              >
                {stage.label}
              </div>
              {ev?.detail && status === "complete" && (
                <div className="mt-0.5 max-w-[100px] truncate text-[10px] text-ink-faint">
                  {ev.detail}
                </div>
              )}
            </motion.div>

            {/* Flow connector — not on the last node */}
            {!isLast && (
              <div className="relative flex-1 self-start" style={{ marginTop: 13, height: 2 }}>
                <FlowLine status={resolveStatus(events.find((e) => e.stage === stages[i + 1].key))} />
              </div>
            )}
          </div>
        );
      })}
    </motion.div>
  );
}

/* --- Node circle -------------------------------------------------------- */

function RailNode({ status, active }: { status: NodeStatus; active: boolean }) {
  const base = "flex h-7 w-7 items-center justify-center rounded-full text-xs shrink-0 transition-colors";

  if (status === "complete") {
    return (
      <motion.div
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 320, damping: 18 }}
        className={cn(base, "bg-leaf text-paper")}
      >
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden>
          <path d="M3 7L5.5 9.5L10 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </motion.div>
    );
  }

  if (status === "active") {
    return (
      <div className={cn(base, "bg-ochre text-paper")}>
        <motion.span
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="block h-2.5 w-2.5 rounded-full border-2 border-paper border-t-transparent"
        />
      </div>
    );
  }

  if (status === "error") {
    return (
      <motion.div
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 320, damping: 18 }}
        className={cn(base, "bg-clay text-paper")}
      >
        <span className="text-[11px] font-bold">!</span>
      </motion.div>
    );
  }

  if (status === "skip") {
    return <div className={cn(base, "bg-bone text-ink-faint")}>—</div>;
  }

  // pending
  return (
    <div
      className={cn(
        base,
        active ? "border-2 border-dashed border-bone bg-paper-2/50" : "border-2 border-bone bg-paper",
      )}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-bone" />
    </div>
  );
}

/* --- Flow connector line ------------------------------------------------ */

function FlowLine({ status }: { status: NodeStatus }) {
  if (status === "complete") {
    return (
      <motion.div
        className="absolute inset-y-0 left-0 rounded-full bg-leaf"
        initial={{ scaleX: 0, originX: 0 }}
        animate={{ scaleX: 1, originX: 0 }}
        transition={{ duration: dur.normal, ease: ease.smooth }}
        style={{ width: "100%" }}
      />
    );
  }
  if (status === "active") {
    return (
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 bg-ochre"
          initial={{ width: "0%" }}
          animate={{ width: "50%" }}
          transition={{ duration: dur.slow, ease: ease.smooth }}
          style={{ borderRadius: 1 }}
        />
      </div>
    );
  }
  // pending / skip / error — just a faint track
  return <div className="absolute inset-y-0 left-0 w-full rounded-full bg-bone" style={{ height: 2, marginTop: 0 }} />;
}

/* --- Default stage presets --------------------------------------------- */

export const VISION_STAGES: RailStage[] = [
  { key: "intake", label: STAGE_LABELS.intake },
  { key: "crop_classification", label: STAGE_LABELS.crop_classification },
  { key: "disease_classification", label: STAGE_LABELS.disease_classification },
  { key: "advisory", label: STAGE_LABELS.advisory },
];

export const QA_STAGES: RailStage[] = [
  { key: "safety", label: STAGE_LABELS.safety },
  { key: "retrieval", label: STAGE_LABELS.retrieval },
  { key: "generation", label: STAGE_LABELS.generation },
  { key: "verifier", label: STAGE_LABELS.verifier },
];
