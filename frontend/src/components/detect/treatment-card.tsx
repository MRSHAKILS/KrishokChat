"use client";

import { motion, AnimatePresence } from "motion/react";
import { ShieldCheck, ShieldAlert, ShieldX, FileText, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { enter, dur, ease } from "@/lib/motion";
import { HELPLINE } from "@/lib/constants";
import type { DetectResponse } from "@/lib/api";

/* =========================================================================
   TreatmentCard — the grounded advisory result.
   Shows the generated treatment text, a confidence badge, source list,
   and any verifier flags. Only appears when status === "diagnosed"
   and treatment_advice is present.

   Confidence states:
     verified         → leaf checkmark
     flagged-unverified → ochre warning + specific flag text + 16123
     low_confidence   → clay + 16123 redirect
   ========================================================================= */

export function TreatmentCard({ result }: { result: DetectResponse }) {
  if (!result.treatment_advice) return null;

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="overflow-hidden rounded-xl border rule bg-paper"
    >
      {/* Ochre header strip — the "প্রতিকার" section */}
      <div className="border-b border-ochre-soft/50 bg-ochre-soft/15 px-5 py-3">
        <div className="text-[11px] uppercase tracking-[0.18em] text-ochre">প্রতিকার</div>
      </div>

      {/* Treatment text */}
      <div className="p-5">
        <p className="text-sm leading-relaxed text-ink whitespace-pre-wrap">
          {result.treatment_advice}
        </p>
      </div>

      {/* Confidence badge */}
      {result.treatment_confidence && (
        <div className="border-t rule px-5 py-3">
          <ConfidenceBadge confidence={result.treatment_confidence} />
        </div>
      )}

      {/* Verifier flags */}
      <AnimatePresence>
        {result.verifier_flags.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="border-t rule px-5 py-3"
          >
            <div className="flex items-start gap-2 rounded-lg border border-ochre-soft/50 bg-ochre-soft/15 p-3">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-ochre" />
              <div className="space-y-1 text-xs text-ink-soft">
                <div className="font-medium text-ochre">অযাচাইকৃত দাবি</div>
                {result.verifier_flags.map((flag, i) => (
                  <div key={i} className="text-ink-soft">{flag}</div>
                ))}
                <a
                  href={`tel:${HELPLINE.krishiCallCenter}`}
                  className="mt-1 inline-block font-medium text-leaf transition-colors hover:text-leaf-2"
                >
                  নিশ্চিত হতে কৃষক কল সেন্টারে যোগাযোগ করুন: {HELPLINE.krishiCallCenter}
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Source list — transparency */}
      {result.treatment_sources.length > 0 && (
        <div className="border-t rule px-5 py-3">
          <div className="mb-2 flex items-center gap-1.5 text-[11px] uppercase tracking-[0.16em] text-ink-faint">
            <FileText className="h-3 w-3" />
            উৎস
          </div>
          <ul className="space-y-1">
            {result.treatment_sources.map((src, i) => (
              <li key={i} className="truncate font-mono text-[11px] text-ink-faint">
                {src}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

/* --- Confidence badge ------------------------------------------------- */

function ConfidenceBadge({ confidence }: { confidence: string }) {
  const config = {
    verified: {
      icon: ShieldCheck,
      label: "যাচাইকৃত",
      color: "text-leaf",
      bg: "bg-leaf/10",
      border: "border-leaf/20",
    },
    "flagged-unverified": {
      icon: ShieldAlert,
      label: "আংশিক যাচাইকৃত",
      color: "text-ochre",
      bg: "bg-ochre-soft/20",
      border: "border-ochre-soft/40",
    },
    "low_confidence": {
      icon: ShieldX,
      label: "নিম্ন নিশ্চিততা",
      color: "text-clay",
      bg: "bg-clay-soft/20",
      border: "border-clay-soft/40",
    },
    "blocked": {
      icon: ShieldX,
      label: "অবরুদ্ধ",
      color: "text-clay",
      bg: "bg-clay-soft/20",
      border: "border-clay-soft/40",
    },
  };

  const c = config[confidence as keyof typeof config] ?? config["low_confidence"];
  const Icon = c.icon;

  return (
    <div className={cn("flex items-center gap-2 rounded-lg border px-3 py-2 text-sm", c.bg, c.border)}>
      <Icon className={cn("h-4 w-4 shrink-0", c.color)} strokeWidth={1.5} />
      <span className={cn("font-medium", c.color)}>{c.label}</span>
    </div>
  );
}
