"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ShieldCheck, ShieldAlert, ShieldX, FileText, AlertCircle, Phone, CloudRain, MessageCircle, ChevronDown, ClipboardCheck, FileSpreadsheet } from "lucide-react";
import { cn } from "@/lib/utils";
import { enter, dur, ease } from "@/lib/motion";
import { HELPLINE } from "@/lib/constants";
import { cropBn, translateDiseaseToBn } from "@/lib/bn";
import type { DetectResponse } from "@/lib/api";
import { DosageCalculator } from "@/components/detect/dosage-calculator";
import { PrescriptionModal } from "@/components/detect/prescription-modal";

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
  const clean = text
    .replaceAll(/\[cite:\s*\d+\]/gi, "")
    .replaceAll(/\*\*/g, "")
    .replaceAll(/\*/g, "");

  const tagRegex = /\[([A-Z0-9_]+)\]/g;
  const bnDigits = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯", "১০"];

  return clean.replace(tagRegex, (match, id) => {
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

function findDosage(text: string): string | null {
  const line = text
    .split(/[\n।]/)
    .map((part) => part.trim())
    .find((part) => /ডোজ|মাত্রা|গ্রাম|মি\.?লি|লিটার|কেজি|\b(?:ml|g|kg|l)\b/i.test(part));
  return line || null;
}

export function TreatmentCard({
  result,
  onFollowUp,
}: {
  result: DetectResponse;
  onFollowUp?: (question: string) => void;
}) {
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const [prescriptionOpen, setPrescriptionOpen] = useState(false);
  if (!result.treatment_advice) return null;

  const cleanAdvice = formatTreatmentAdvice(result.treatment_advice, result.treatment_sources);
  const dosage = findDosage(cleanAdvice);

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="overflow-hidden rounded-xl border rule bg-paper shadow-[0_8px_28px_rgba(52,39,23,0.06)]"
    >
      {/* Prescription Modal Popup */}
      <PrescriptionModal
        open={prescriptionOpen}
        onClose={() => setPrescriptionOpen(false)}
        result={result}
      />

      {/* The first screenful is deliberately structured for a five-second scan. */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-ochre-soft/50 bg-ochre-soft/15 px-5 py-3">
        <div className="flex items-center gap-2 text-xs font-semibold text-ochre">
          <ClipboardCheck className="h-4 w-4" /> এখন কী করবেন
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setPrescriptionOpen(true)}
            className="control-press inline-flex items-center gap-1.5 rounded-lg border border-leaf/40 bg-leaf/10 px-2.5 py-1 text-xs font-semibold text-leaf hover:bg-leaf hover:text-paper cursor-pointer shadow-2xs"
          >
            <FileSpreadsheet className="h-3.5 w-3.5" /> ব্যবস্থাপত্র দেখুন
          </button>
          {result.treatment_confidence && <ConfidenceBadge confidence={result.treatment_confidence} compact />}
        </div>
      </div>

      {/* Immediate action */}
      <div className="border-b rule p-5">
        <div className="mb-1 text-xs font-semibold text-ink-faint">তাৎক্ষণিক ব্যবস্থা</div>
        <p className="text-sm leading-relaxed text-ink whitespace-pre-wrap">{cleanAdvice}</p>
      </div>

      {/* Dosage and Weather Consideration */}
      <div className="grid gap-3 border-b rule p-5 sm:grid-cols-2">
        <div className="rounded-lg border border-ochre-soft/60 bg-ochre-soft/10 p-3">
          <div className="text-xs font-semibold text-ochre">রাসায়নিক মাত্রা নির্দেশিকা</div>
          <p className="mt-1 text-xs leading-relaxed text-ink-soft">
            {dosage ?? "এই ফলাফলে আলাদা মাত্রা উল্লেখ নেই। লেবেল ছাড়া ডোজ ঠিক করবেন না।"}
          </p>
        </div>
        <div className="rounded-lg border border-leaf/20 bg-leaf/5 p-3">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-leaf">
            <CloudRain className="h-3.5 w-3.5" /> আবহাওয়া বিবেচনা
          </div>
          <p className="mt-1 text-xs leading-relaxed text-ink-soft">
            এই পরামর্শে আপনার এলাকার লাইভ আবহাওয়া নেই। স্প্রে করার আগে বৃষ্টি ও বাতাস দেখে নিন।
          </p>
        </div>
      </div>

      {/* Interactive Dosage Calculator Widget */}
      <div className="border-b rule p-5 bg-paper-2/20">
        <DosageCalculator
          defaultDosageText={dosage || cleanAdvice}
          cropName={result.crop ? cropBn(result.crop) : ""}
          diseaseName={result.disease ? translateDiseaseToBn(result.disease) : ""}
        />
      </div>

      {/* Dosage guidance is safety-critical */}
      <div className="mx-5 mb-4 flex items-start gap-2 rounded-lg border border-clay-soft/60 bg-clay-soft/15 px-3 py-3 text-xs leading-relaxed text-ink-soft">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-ochre" />
        <div>
          <div className="font-semibold text-clay">রাসায়নিক ব্যবহারের আগে যাচাই করুন</div>
          <p className="mt-0.5">উৎসে স্পষ্ট মাত্রা না থাকলে নিজে থেকে ডোজ ঠিক করবেন না। লেবেল ও স্থানীয় কৃষি কর্মকর্তার পরামর্শ মেনে চলুন।</p>
          <a href={`tel:${HELPLINE.krishiCallCenter}`} className="mt-1 inline-flex min-h-9 items-center gap-1 font-semibold text-leaf hover:text-leaf-2">
            <Phone className="h-3.5 w-3.5" /> {HELPLINE.krishiCallCenter}
          </a>
        </div>
      </div>

      {/* Confidence badge */}
      {result.treatment_confidence && (
        <div className="border-t rule px-5 py-3">
          <p className="text-xs leading-relaxed text-ink-faint">
            যাচাই অবস্থা পরামর্শের উৎসসমর্থন বোঝায়; এটি রোগ শনাক্তকরণের শতাংশ নয়।
          </p>
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
        <div className="border-t rule bg-paper-2/30 px-5 py-3">
          <button
            type="button"
            onClick={() => setSourcesOpen((open) => !open)}
            aria-expanded={sourcesOpen}
            className="control-press flex min-h-10 w-full items-center justify-between gap-3 rounded-lg text-left text-xs font-semibold text-leaf"
          >
            <span className="flex items-center gap-1.5">
              <FileText className="h-3.5 w-3.5" />
              প্রমাণিত সরকারি ও গবেষণা তথ্যসূত্র ({result.treatment_sources.length}টি)
            </span>
            <ChevronDown className={cn("h-4 w-4 transition-transform", sourcesOpen && "rotate-180")} />
          </button>
          <AnimatePresence mode="wait">
            {sourcesOpen && (
              <motion.ul
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: dur.normal, ease: ease.smooth }}
                className="space-y-1.5 overflow-hidden pt-2"
              >
                {result.treatment_sources.map((src, i) => {
                  const orgName = getOrgNameForSource(src);
                  return (
                    <li key={i} className="surface-lift flex items-center gap-2 rounded-lg border rule bg-paper px-3 py-2 text-xs text-ink">
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-leaf text-xs font-bold text-paper">
                        {i + 1}
                      </span>
                      <span className="font-semibold text-leaf">{orgName}</span>
                    </li>
                  );
                })}
              </motion.ul>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* Follow-up actions keep the assistant task-oriented instead of ending at a label. */}
      <div className="border-t rule px-5 py-4">
        <div className="mb-2 flex items-center gap-1.5 text-xs font-semibold text-ink-faint">
          <MessageCircle className="h-3.5 w-3.5 text-leaf" /> পরের কাজ
        </div>
        <div className="flex flex-wrap gap-2">
          {[
            "রাসায়নিক ছাড়া কীভাবে সামলাব?",
            "বৃষ্টির আগে কী করব?",
            "আরও পরিষ্কার ছবি দিলে দেখবেন?",
          ].map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => onFollowUp?.(question)}
              disabled={!onFollowUp}
               className="control-press min-h-11 rounded-full border border-leaf/25 bg-leaf/5 px-3 text-xs font-medium text-leaf hover:bg-leaf/10 disabled:cursor-default disabled:opacity-70"
            >
              {question}
            </button>
          ))}
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="inline-flex min-h-11 items-center rounded-full border border-bone px-3 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
          >
            কৃষি বিশেষজ্ঞ: {HELPLINE.krishiCallCenter}
          </a>
        </div>
      </div>
    </motion.div>
  );
}

/* --- Confidence badge ------------------------------------------------- */

function ConfidenceBadge({ confidence, compact = false }: { confidence: string; compact?: boolean }) {
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
    <div className={cn("flex items-center gap-2 rounded-lg border", compact ? "px-2 py-1 text-xs" : "px-3 py-2 text-sm", c.bg, c.border)}>
      <Icon className={cn("h-4 w-4 shrink-0", c.color)} strokeWidth={1.5} />
      <span className={cn("font-medium", c.color)}>{c.label}</span>
    </div>
  );
}
