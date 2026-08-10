"use client";

import { motion } from "motion/react";
import { ShieldAlert, Phone } from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { enter } from "@/lib/motion";
import { safetyLabel } from "@/lib/safety-labels";
import { cn } from "@/lib/utils";

/* =========================================================================
   SafetyNotice — shown when the QA pipeline blocked a query.
   Covers: banned_or_restricted_chemical, self_harm_or_poisoning_risk,
   off_topic, prompt_injection, low_confidence.

   This is NOT an error — it's a deliberate, calm, safe redirect.
   The tone is non-judgmental and always points to 16123. Labels come
   from the shared safety-labels map so backend enums never reach the user.
   ========================================================================= */

export function SafetyNotice({
  category,
  answer,
}: {
  category: string;
  answer: string;
}) {
  const s = safetyLabel(category);
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
            "text-[11px] font-semibold",
            isUrgent ? "text-clay" : "text-ochre",
          )}
        >
          {s.label}
        </span>
      </div>

      <p className="mt-2 text-sm leading-relaxed text-ink">{answer}</p>

      <div className="mt-3 flex flex-wrap gap-2">
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="inline-flex items-center gap-2 rounded-md border border-leaf/30 bg-leaf/10 px-3 py-1.5 text-xs font-medium text-leaf transition-colors hover:bg-leaf/20"
        >
          <Phone className="h-3.5 w-3.5" />
          কৃষক কল সেন্টার
          <span className="tabular">{HELPLINE.krishiCallCenter}</span>
        </a>

        {isUrgent && (
          <a
            href={`tel:${HELPLINE.emergency}`}
            className="inline-flex items-center gap-2 rounded-md border border-clay-soft/40 bg-clay-soft/10 px-3 py-1.5 text-xs font-medium text-clay transition-colors hover:border-clay"
          >
            <Phone className="h-3.5 w-3.5" />
            জরুরি সেবা
            <span className="tabular">{HELPLINE.emergency}</span>
          </a>
        )}
      </div>
    </motion.div>
  );
}
