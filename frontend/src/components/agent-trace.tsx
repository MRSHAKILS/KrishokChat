"use client";

import { motion } from "motion/react";
import { Activity, CheckCircle2 } from "lucide-react";
import { PipelineRail, type RailEvent, type RailStage } from "@/components/detect/pipeline-rail";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

export function AgentTrace({
  stages,
  events,
  active = false,
  title,
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
  const { locale } = useLanguage();
  const en = locale === "en";
  const current = [...events].reverse().find((event) => event.status === "start" || event.status === "active");
  const completed = !active && events.length > 0 && events.every((event) => ["complete", "skip"].includes(event.status));
  const resolvedTitle = title ?? (en ? "Agent trace" : "এজেন্ট ট্রেস");

  return (
    <motion.section
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: dur.fast, ease: ease.smooth }}
      aria-label={resolvedTitle}
      className={cn("rounded-2xl border rule bg-paper-2/35 p-4 sm:p-5", className)}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex min-w-0 items-center gap-2.5">
          <span className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-lg", active ? "bg-ochre/15 text-ochre" : "bg-leaf/10 text-leaf")}>
            {active ? <Activity className="h-4 w-4" /> : <CheckCircle2 className="h-4 w-4" />}
          </span>
          <div className="min-w-0">
            <div className="text-xs font-semibold text-ink">{resolvedTitle}</div>
            <div className="mt-0.5 truncate text-xs text-ink-faint">
              {active
                ? (detail ?? (en ? "Steps are completing safely" : "নিরাপদভাবে ধাপগুলো সম্পন্ন হচ্ছে"))
                : completed
                  ? (en ? "All steps complete" : "সব ধাপ সম্পন্ন")
                  : (en ? "Ready" : "প্রস্তুত")}
            </div>
          </div>
        </div>
        <span className={cn("shrink-0 rounded-full px-2 py-1 text-xs font-semibold", active ? "bg-ochre-soft/30 text-ochre" : completed ? "bg-leaf/10 text-leaf" : "bg-bone text-ink-faint")}>
          {active ? (en ? "Running" : "চলছে") : completed ? (en ? "Done" : "সম্পন্ন") : (en ? "Waiting" : "অপেক্ষায়")}
        </span>
      </div>
      {current?.detail && active && <div className="mt-3 rounded-lg border border-ochre-soft/40 bg-ochre-soft/10 px-3 py-2 text-xs text-ink-soft">{current.detail}</div>}
      <div className="mt-5 overflow-x-auto pb-1">
        <PipelineRail stages={stages} events={events} active={active} />
      </div>
    </motion.section>
  );
}
