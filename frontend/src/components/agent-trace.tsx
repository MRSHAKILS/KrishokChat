"use client";

import { motion } from "motion/react";
import { Activity, CheckCircle2 } from "lucide-react";
import { PipelineRail, type RailEvent, type RailStage } from "@/components/detect/pipeline-rail";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";

export function AgentTrace({
  stages,
  events,
  active = false,
  title = "এজেন্ট ট্রেস",
  detail,
  className,
}: {
  stages: RailStage[];
  events: RailEvent[];
  active?: boolean;
  title?: string;
  detail?: string;
  className?: string;
}) {
  const current = [...events].reverse().find((event) => event.status === "start" || event.status === "active");
  const completed = !active && events.length > 0 && events.every((event) => ["complete", "skip"].includes(event.status));

  return (
    <motion.section
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: dur.fast, ease: ease.smooth }}
      aria-label={title}
      className={cn("rounded-2xl border rule bg-paper-2/35 p-4 sm:p-5", className)}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex min-w-0 items-center gap-2.5">
          <span className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-lg", active ? "bg-ochre/15 text-ochre" : "bg-leaf/10 text-leaf")}>
            {active ? <Activity className="h-4 w-4" /> : <CheckCircle2 className="h-4 w-4" />}
          </span>
          <div className="min-w-0">
            <div className="text-[11px] font-semibold text-ink">{title}</div>
            <div className="mt-0.5 truncate text-[10px] text-ink-faint">
              {active ? (detail ?? "নিরাপদভাবে ধাপগুলো সম্পন্ন হচ্ছে") : completed ? "সব ধাপ সম্পন্ন" : "প্রস্তুত"}
            </div>
          </div>
        </div>
        <span className={cn("shrink-0 rounded-full px-2 py-1 text-[10px] font-semibold", active ? "bg-ochre-soft/30 text-ochre" : completed ? "bg-leaf/10 text-leaf" : "bg-bone text-ink-faint")}>
          {active ? "চলছে" : completed ? "সম্পন্ন" : "অপেক্ষায়"}
        </span>
      </div>
      {current?.detail && active && <div className="mt-3 rounded-lg border border-ochre-soft/40 bg-ochre-soft/10 px-3 py-2 text-[11px] text-ink-soft">{current.detail}</div>}
      <div className="mt-5 overflow-x-auto pb-1">
        <PipelineRail stages={stages} events={events} active={active} />
      </div>
    </motion.section>
  );
}
