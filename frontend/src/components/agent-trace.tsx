"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

const STAGE_LABELS: Record<string, string> = {
  safety: "নিরাপত্তা যাচাই",
  retrieval: "তথ্য সংগ্রহ",
  generation: "উত্তর তৈরি",
  verifier: "যাচাইকরণ",
};

const STAGES = ["safety", "retrieval", "generation", "verifier"];

export interface TraceEvent {
  stage: string;
  status: "start" | "complete" | "skip";
  detail?: string | null;
}

export function AgentTrace({ events }: { events: TraceEvent[] }) {
  return (
    <div className="space-y-2 py-2">
      {STAGES.map((stage) => {
        const ev = events.find((e) => e.stage === stage);
        const status = ev?.status || "pending";
        return (
          <div key={stage} className="flex items-center gap-3">
            <div className={cn(
              "w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold shrink-0",
              status === "complete" && "bg-green-100 text-green-700",
              status === "start" && "bg-blue-100 text-blue-700 animate-pulse",
              status === "skip" && "bg-gray-100 text-gray-400",
              status === "pending" && "bg-gray-50 text-gray-300",
            )}>
              {status === "complete" ? "✓" : status === "skip" ? "–" : status === "start" ? "⟳" : "○"}
            </div>
            <div className="flex-1 min-w-0">
              <div className={cn("text-sm font-medium", status === "pending" && "text-gray-400")}>
                {STAGE_LABELS[stage]}
              </div>
              {ev?.detail && (
                <div className="text-xs text-gray-500 truncate">{ev.detail}</div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
