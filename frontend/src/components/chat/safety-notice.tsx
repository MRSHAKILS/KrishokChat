"use client";

import { motion } from "motion/react";
import { ShieldAlert, Phone, Info } from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { enter } from "@/lib/motion";
import { safetyLabel, refusalRuleLabel } from "@/lib/safety-labels";
import { cn } from "@/lib/utils";

/* =========================================================================
   SafetyNotice — shown when the QA pipeline blocked a query.
   Covers: banned_or_restricted_chemical, self_harm_or_poisoning_risk,
   off_topic, prompt_injection, low_confidence.

   This is NOT an error — it's a deliberate, calm, safe redirect.
   The tone is non-judgmental and always points to 16123. Labels come
   from the shared safety-labels map so backend enums never reach the user.

   P5: when the pipeline refused via a deterministic rule, `matchedRules`
   carries the rule ids (e.g. coverage_training) and renders as short Bengali
   reason chips so the user sees WHY — the D1a coverage gate made visible.
   ========================================================================= */

export function SafetyNotice({
  category,
  answer,
  matchedRules = [],
}: {
  category: string;
  answer: string;
  matchedRules?: string[];
}) {
  const s = safetyLabel(category);
  const isUrgent = category === "self_harm_or_poisoning_risk";
  const rules = matchedRules.filter(Boolean);

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

      {/* P5: deterministic refusal reason — why this query was redirected */}
      {rules.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-1.5">
          <Info className="h-3.5 w-3.5 shrink-0 text-ink-faint" />
          <span className="text-[11px] text-ink-faint">কারণ:</span>
          {rules.map((rule) => (
            <span
              key={rule}
              className="rounded-full bg-ink/5 px-2.5 py-1 text-[10px] font-medium text-ink-soft ring-1 ring-ink/10"
            >
              {refusalRuleLabel(rule)}
            </span>
          ))}
        </div>
      )}

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
