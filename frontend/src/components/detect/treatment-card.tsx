"use client";

import { motion, AnimatePresence } from "motion/react";
import { ShieldCheck, ShieldAlert, ShieldX, FileText, AlertCircle, Phone } from "lucide-react";
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

const PUBLISHER_NAMES: Record<string, string> = {
  DAE: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)",
  BARC: "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)",
  BARI: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)",
  BRRI: "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI)",
  SRDI: "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট (SRDI)",
  CABI: "সিএবিআই ক্রপ স্পেকট্রাম (CABI)",
  IRRI: "আন্তর্জাতিক ধান গবেষণা ইনস্টিটিউট (IRRI)",
};

function formatTreatmentAdvice(text: string, sources: string[]) {
  if (!text) return text;
  const tagRegex = /\[([A-Z0-9_]+)\]/g;
  const bnDigits = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "১০"];

  return text.replace(tagRegex, (match, id) => {
    const idx = sources.findIndex((s) => s === id);
    if (idx >= 0) {
      const digit = bnDigits[idx] || String(idx + 1);
      return ` [${digit}] `;
    }
    return "";
  }).trim();
}

function getOrgNameForSource(src: string): string {
  const upper = src.toUpperCase();
  for (const [key, name] of Object.entries(PUBLISHER_NAMES)) {
    if (upper.includes(key)) return name;
  }
  if (upper.startsWith("B4") || upper.startsWith("B5")) return "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)";
  return "জাতীয় কৃষি গবেষণা সংস্থা";
}

export function TreatmentCard({ result }: { result: DetectResponse }) {
  if (!result.treatment_advice) return null;

  const cleanAdvice = formatTreatmentAdvice(result.treatment_advice, result.treatment_sources);

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="overflow-hidden rounded-xl border rule bg-paper shadow-2xs"
    >
      {/* Ochre header strip — the "প্রতিকার" section */}
      <div className="border-b border-ochre-soft/50 bg-ochre-soft/15 px-5 py-3">
        <div className="text-[11px] font-semibold text-ochre">প্রতিকার ও ফসল সুরক্ষা নির্দেশিকা</div>
      </div>

      {/* Treatment text */}
      <div className="p-5">
        <p className="text-sm leading-relaxed text-ink whitespace-pre-wrap">
          {cleanAdvice}
        </p>
      </div>

      {/* Dosage guidance is safety-critical */}
      <div className="mx-5 mb-4 flex items-start gap-2 rounded-lg border border-ochre-soft/60 bg-ochre-soft/15 px-3 py-3 text-xs leading-relaxed text-ink-soft">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-ochre" />
        <div>
          <div className="font-semibold text-ochre">কীটনাশক ব্যবহারে সতর্কতা</div>
          <p className="mt-0.5">ব্যবহারের আগে স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন। নিশ্চিত হতে কৃষক কল সেন্টারে কল করুন।</p>
          <a href={`tel:${HELPLINE.krishiCallCenter}`} className="mt-1 inline-flex min-h-9 items-center gap-1 font-semibold text-leaf hover:text-leaf-2">
            <Phone className="h-3.5 w-3.5" /> {HELPLINE.krishiCallCenter}
          </a>
        </div>
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

      {/* Source list — formal institutional sources */}
      {result.treatment_sources.length > 0 && (
        <div className="border-t rule px-5 py-3 bg-paper-2/30">
          <div className="mb-2 flex items-center gap-1.5 text-[11px] font-semibold text-leaf">
            <FileText className="h-3.5 w-3.5 text-leaf" />
            প্রমাণিত সরকারি ও গবেষণা তথ্যসূত্র ({result.treatment_sources.length}টি উৎস)
          </div>
          <ul className="space-y-1.5">
            {result.treatment_sources.map((src, i) => {
              const orgName = getOrgNameForSource(src);
              return (
                <li key={i} className="flex items-center gap-2 text-xs text-ink">
                  <span className="flex h-4 w-4 items-center justify-center rounded-full bg-leaf text-[9px] font-bold text-paper">
                    {i + 1}
                  </span>
                  <span className="font-semibold text-leaf">{orgName}</span>
                </li>
              );
            })}
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
