"use client";

import { motion } from "motion/react";
import { cn } from "@/lib/utils";
import { bnPercent } from "@/lib/bn";
import { dur, ease } from "@/lib/motion";

/* =========================================================================
   ConfidenceMeter — a visual bar that fills from 0 to the actual percentage.
   Farmers understand a bar more than a decimal. Bengali numerals throughout.
   ========================================================================= */

type Tone = "leaf" | "ochre" | "clay";

const TONE_FILL: Record<Tone, string> = {
  leaf: "bg-leaf",
  ochre: "bg-ochre",
  clay: "bg-clay",
};
const TONE_TEXT: Record<Tone, string> = {
  leaf: "text-leaf",
  ochre: "text-ochre",
  clay: "text-clay",
};

export function ConfidenceMeter({
  value,
  label,
  tone = "leaf",
  compact = false,
}: {
  value: number; // 0-1
  label?: string;
  tone?: Tone;
  compact?: boolean;
}) {
  const pct = Math.round(value * 100);

  return (
    <div className={cn("flex items-center gap-3", compact ? "text-xs" : "text-sm")}>
      {label && (
        <span className="shrink-0 text-ink-soft">
          {label}
        </span>
      )}
      <div
        className="relative h-2 flex-1 overflow-hidden rounded-full bg-bone"
        role="progressbar"
        aria-label={label ?? "নিশ্চিততা"}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={pct}
      >
        <motion.div
          className={cn("absolute inset-y-0 left-0 rounded-full", TONE_FILL[tone])}
          initial={{ scaleX: 0, originX: 0 }}
          animate={{ scaleX: pct / 100, originX: 0 }}
          transition={{ duration: dur.slow, ease: ease.smooth, delay: 0.15 }}
          style={{ width: "100%" }}
        />
      </div>
      <span className={cn("shrink-0 font-semibold tabular", TONE_TEXT[tone])}>
        {bnPercent(value)}
      </span>
    </div>
  );
}
