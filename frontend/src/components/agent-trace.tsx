"use client";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { motionTokens, fadeUp } from "@/lib/motionTokens";

const STAGE_LABELS: Record<string, string> = {
  safety: "নিরাপত্তা যাচাই",
  retrieval: "তথ্য সংগ্রহ",
  generation: "উত্তর তৈরি",
  verifier: "যাচাইকরণ",
};
const STAGE_ICONS: Record<string, string> = {
  safety: "🛡️",
  retrieval: "🔍",
  generation: "✨",
  verifier: "✅",
};
const STAGES = ["safety", "retrieval", "generation", "verifier"];

export interface TraceEvent {
  stage: string;
  status: "start" | "complete" | "skip";
  detail?: string | null;
}

export function AgentTrace({ events }: { events: TraceEvent[] }) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{ visible: { transition: { staggerChildren: 0.08 } } }}
      className="space-y-1.5 py-1"
    >
      {STAGES.map((stage) => {
        const ev = events.find((e) => e.stage === stage);
        const status = ev?.status || "pending";
        return (
          <motion.div
            key={stage}
            variants={fadeUp}
            className="flex items-center gap-2.5 rounded-lg px-2 py-1.5"
          >
            <div
              className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center text-base shrink-0 shadow-sm",
                status === "complete" && "bg-green-100",
                status === "start" && "bg-blue-100",
                status === "skip" && "bg-gray-100",
                status === "pending" && "bg-gray-50"
              )}
            >
              {status === "start" ? (
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="block"
                >
                  {STAGE_ICONS[stage]}
                </motion.span>
              ) : status === "complete" ? (
                <span>{STAGE_ICONS[stage]}</span>
              ) : (
                <span className="opacity-40">{STAGE_ICONS[stage]}</span>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <div
                className={cn(
                  "text-sm font-semibold leading-tight",
                  status === "pending" && "text-gray-400"
                )}
              >
                {STAGE_LABELS[stage]}
              </div>
              {ev?.detail && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  transition={{ duration: motionTokens.duration.fast }}
                  className="text-xs text-gray-500 truncate"
                >
                  {ev.detail}
                </motion.div>
              )}
            </div>
            <div className="text-xs font-medium shrink-0">
              {status === "complete" && <span className="text-green-600">সম্পন্ন</span>}
              {status === "start" && <span className="text-blue-600">চলছে...</span>}
              {status === "skip" && <span className="text-gray-400">বাদ</span>}
            </div>
          </motion.div>
        );
      })}
    </motion.div>
  );
}
