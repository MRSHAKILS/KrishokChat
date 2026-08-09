"use client";

import { motion } from "motion/react";
import { ShieldAlert } from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { enter } from "@/lib/motion";
import { cn } from "@/lib/utils";

/* =========================================================================
   SafetyNotice — shown when the QA pipeline blocked a query.
   Covers: banned_or_restricted_chemical, self_harm_or_poisoning_risk,
   off_topic, prompt_injection, low_confidence.

   This is NOT an error — it's a deliberate, calm, safe redirect.
   The tone is non-judgmental and always points to 16123.
   ========================================================================= */

const CATEGORY_LABELS: Record<string, string> = {
  banned_or_restricted_chemical: "নিষিদ্ধ রাসায়নিক",
  self_harm_or_poisoning_risk: "নিরাপত্তা সতর্কতা",
  off_topic: "কৃষি-বহির্ভূত",
  prompt_injection: "নির্দেশনা আক্রমণ",
  low_confidence: "নিম্ন নিশ্চিততা",
};

export function SafetyNotice({
  category,
  answer,
}: {
  category: string;
  answer: string;
}) {
  const label = CATEGORY_LABELS[category] ?? "নিরাপত্তা";
  const isUrgent = category === "self_harm_or_poisoning_risk";

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className={cn(
        "rounded-lg border p-4",
        isUrgent
          ? "border-clay-soft/50 bg-clay-soft/15"
          : "border-ochre-soft/50 bg-ochre-soft/10",
      )}
    >
      <div className="flex items-center gap-2">
        <ShieldAlert
          className={cn("h-4 w-4 shrink-0", isUrgent ? "text-clay" : "text-ochre")}
          strokeWidth={1.5}
        />
        <span
          className={cn(
            "text-[11px] uppercase tracking-[0.16em]",
            isUrgent ? "text-clay" : "text-ochre",
          )}
        >
          {label}
        </span>
      </div>

      <p className="mt-2 text-sm leading-relaxed text-ink">{answer}</p>

      <a
        href={`tel:${HELPLINE.krishiCallCenter}`}
        className="mt-3 inline-flex items-center gap-2 rounded-md border rule bg-paper px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
      >
        কৃষক কল সেন্টার
        <span className="tabular text-leaf">{HELPLINE.krishiCallCenter}</span>
      </a>

      {isUrgent && (
        <a
          href={`tel:${HELPLINE.emergency}`}
          className="ml-2 inline-flex items-center gap-2 rounded-md border border-clay-soft/40 bg-clay-soft/10 px-3 py-1.5 text-xs font-medium text-clay transition-colors hover:border-clay"
        >
          জরুরি সেবা
          <span className="tabular">{HELPLINE.emergency}</span>
        </a>
      )}
    </motion.div>
  );
}
