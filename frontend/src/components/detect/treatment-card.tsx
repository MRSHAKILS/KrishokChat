"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ShieldCheck, ShieldAlert, ShieldX, FileText, AlertCircle, Phone, CloudRain, MessageCircle, ChevronDown, ClipboardCheck, FileSpreadsheet, Volume2, VolumeX } from "lucide-react";
import { cn } from "@/lib/utils";
import { enter, dur, ease } from "@/lib/motion";
import { HELPLINE } from "@/lib/constants";
import { cropBn, translateDiseaseToBn } from "@/lib/bn";
import type { DetectResponse } from "@/lib/api";
import { DosageCalculator } from "@/components/detect/dosage-calculator";
import { PrescriptionModal } from "@/components/detect/prescription-modal";
import { useLanguage } from "@/context/language-context";
import { getLocalizedDisease } from "@/lib/i18n/disease-knowledge";

/* =========================================================================
   TreatmentCard — the grounded advisory result.
   Bilingual, safety-verified treatment advisory with audio speech support.
   ========================================================================= */

const PUBLISHER_NAMES_BN: Record<string, string> = {
  DAE: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)",
  BARC: "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)",
  BARI: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)",
  BRRI: "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI)",
  SRDI: "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট (SRDI)",
  CABI: "সিএবিআই ক্রপ স্পেকট্রাম (CABI)",
  IRRI: "আন্তর্জাতিক ধান গবেষণা ইনস্টিটিউট (IRRI)",
};

const PUBLISHER_NAMES_EN: Record<string, string> = {
  DAE: "Department of Agricultural Extension (DAE)",
  BARC: "Bangladesh Agricultural Research Council (BARC)",
  BARI: "Bangladesh Agricultural Research Institute (BARI)",
  BRRI: "Bangladesh Rice Research Institute (BRRI)",
  SRDI: "Soil Resource Development Institute (SRDI)",
  CABI: "CABI Crop Protection Compendium (CABI)",
  IRRI: "International Rice Research Institute (IRRI)",
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

function getOrgNameForSource(src: string, locale: "bn" | "en"): string {
  const upper = src.toUpperCase();
  const map = locale === "bn" ? PUBLISHER_NAMES_BN : PUBLISHER_NAMES_EN;
  for (const [key, name] of Object.entries(map)) {
    if (upper.includes(key)) return name;
  }
  if (upper.startsWith("B4") || upper.startsWith("B5")) {
    return locale === "bn" ? "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)" : "Bangladesh Agricultural Research Council (BARC)";
  }
  return locale === "bn" ? "জাতীয় কৃষি গবেষণা সংস্থা" : "National Agricultural Research System";
}

function findDosage(text: string): string | null {
  const line = text
    .split(/[\n।.]/)
    .map((part) => part.trim())
    .find((part) => /ডোজ|মাত্রা|গ্রাম|মি\.?লি|লিটার|কেজি|\b(?:ml|g|kg|l|dose|grams?)\b/i.test(part));
  return line || null;
}

export function TreatmentCard({
  result,
  onFollowUp,
}: {
  result: DetectResponse;
  onFollowUp?: (question: string) => void;
}) {
  const { t, locale, localizeCrop, localizeDisease } = useLanguage();
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const [prescriptionOpen, setPrescriptionOpen] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  if (!result.treatment_advice) return null;

  const cleanAdvice = formatTreatmentAdvice(result.treatment_advice, result.treatment_sources);
  const dosage = findDosage(cleanAdvice);

  const localizedKnowledge = getLocalizedDisease(result.disease, locale);

  const handleToggleSpeak = () => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const cropName = localizeCrop(result.crop) || (locale === "bn" ? "ফসল" : "Crop");
    const diseaseName = localizedKnowledge?.nameEn || localizeDisease(result.disease) || (locale === "bn" ? "রোগ" : "Condition");

    const textToRead =
      locale === "bn"
        ? `${cropName} এর ${diseaseName} এর চিকিৎসা। ${cleanAdvice}. ${
            dosage ? `প্রস্তাবিত মাত্রা: ${dosage}.` : ""
          } নিরাপদ অপেক্ষমাণ সময়: বালাইনাশক স্প্রে করার পর কমপক্ষে ৭ থেকে ১৪ দিন ফসল তোলা বন্ধ রাখুন।`
        : `Treatment for ${cropName} ${diseaseName}. ${cleanAdvice}. ${
            dosage ? `Recommended dosage: ${dosage}.` : ""
          } Pre-harvest interval: withhold crop harvesting for at least 7 to 14 days after pesticide application.`;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.lang = locale === "bn" ? "bn-BD" : "en-US";
    utterance.rate = locale === "bn" ? 0.92 : 0.98;

    const voices = window.speechSynthesis.getVoices();
    if (locale === "bn") {
      const bnVoice = voices.find(
        (v) => v.lang.startsWith("bn") || v.lang.toLowerCase().includes("bengali") || v.lang.toLowerCase().includes("bangla")
      );
      if (bnVoice) utterance.voice = bnVoice;
    } else {
      const enVoice = voices.find((v) => v.lang.startsWith("en"));
      if (enVoice) utterance.voice = enVoice;
    }

    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    return () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

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
          <ClipboardCheck className="h-4 w-4" /> {t.treatment.actionPlan}
        </div>
        <div className="flex items-center gap-2">
          {/* Audio Read-Aloud Button */}
          <button
            type="button"
            onClick={handleToggleSpeak}
            className={cn(
              "control-press inline-flex items-center gap-1.5 rounded-lg border px-2.5 py-1 text-xs font-semibold cursor-pointer shadow-2xs transition-colors",
              isSpeaking
                ? "border-clay bg-clay text-paper animate-pulse"
                : "border-ochre/40 bg-ochre/10 text-ochre hover:bg-ochre hover:text-paper"
            )}
            title={isSpeaking ? t.treatment.stopReading : t.treatment.readAloud}
          >
            {isSpeaking ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
            {isSpeaking ? t.treatment.stopReading : t.treatment.readAloud}
          </button>
          <button
            type="button"
            onClick={() => setPrescriptionOpen(true)}
            className="control-press inline-flex items-center gap-1.5 rounded-lg border border-leaf/40 bg-leaf/10 px-2.5 py-1 text-xs font-semibold text-leaf hover:bg-leaf hover:text-paper cursor-pointer shadow-2xs"
          >
            <FileSpreadsheet className="h-3.5 w-3.5" /> {t.treatment.prescriptionButton}
          </button>
          {result.treatment_confidence && <ConfidenceBadge confidence={result.treatment_confidence} locale={locale} compact />}
        </div>
      </div>

      {/* Immediate action */}
      <div className="border-b rule p-5">
        <div className="mb-1 text-xs font-semibold text-ink-faint">
          {locale === "bn" ? "তাৎক্ষণিক ব্যবস্থা" : "Immediate Action Plan"}
        </div>
        <p className="text-sm leading-relaxed text-ink whitespace-pre-wrap">{cleanAdvice}</p>
      </div>

      {/* Dosage, Spray Timing & Pre-Harvest Interval (PHI) */}
      <div className="grid gap-3 border-b rule p-5 sm:grid-cols-2">
        <div className="rounded-lg border border-ochre-soft/60 bg-ochre-soft/10 p-3">
          <div className="text-xs font-semibold text-ochre">
            {locale === "bn" ? "রাসায়নিক মাত্রা ও প্রয়োগ সতর্কতা" : "Chemical Dosage & Precautions"}
          </div>
          <p className="mt-1 text-xs leading-relaxed text-ink-soft">
            {dosage ??
              (locale === "bn"
                ? "এই ফলাফলে আলাদা মাত্রা উল্লেখ নেই। প্যাকেটের লেবেল ও কৃষি কর্মকর্তার পরামর্শ ছাড়া ডোজ ঠিক করবেন না।"
                : "Exact dose is unstated in source snippet. Follow official product label instructions or local extension advice.")}
          </p>
          <div className="mt-2.5 rounded border border-ochre/25 bg-paper/60 p-2 text-[11px] leading-relaxed text-ink-soft">
            <span className="font-semibold text-ochre">
              {locale === "bn" ? "নিরাপদ অপেক্ষমাণ সময় (PHI):" : "Pre-Harvest Interval (PHI):"}
            </span>{" "}
            {locale === "bn"
              ? "বালাইনাশক স্প্রে করার পর কমপক্ষে ৭ থেকে ১৪ দিন ফসল তোলা ও বাজারে বিক্রি বন্ধ রাখুন।"
              : "Withhold harvesting and consumption for at least 7–14 days following pesticide application."}
          </div>
        </div>
        <div className="rounded-lg border border-leaf/20 bg-leaf/5 p-3">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-leaf">
            <CloudRain className="h-3.5 w-3.5" />
            {locale === "bn" ? "স্প্রে করার উপযুক্ত সময় ও নিয়ম" : "Proper Spray Timing & Technique"}
          </div>
          <p className="mt-1 text-xs leading-relaxed text-ink-soft">
            {locale === "bn"
              ? "কখনও দুপুরের প্রখর রোদে স্প্রে করবেন না। সকালের শিশির শুকানোর পর বা বিকালের মৃদু রোদে বাতাসের অনুকূলে পিঠ রেখে স্প্রে করুন।"
              : "Never spray in midday heat. Apply after morning dew dissipates or during calm late afternoon, spraying with wind behind you."}
          </p>
          <div className="mt-2.5 rounded border border-leaf/25 bg-paper/60 p-2 text-[11px] leading-relaxed text-ink-soft">
            <span className="font-semibold text-leaf">
              {locale === "bn" ? "ব্যক্তিগত সুরক্ষা:" : "Personal Protection:"}
            </span>{" "}
            {locale === "bn"
              ? "স্প্রে করার সময় মুখে গামছা বা মাস্ক বাঁধুন এবং স্প্রে শেষে সাবান দিয়ে ভালো করে গোসল/হাত-মুখ ধুয়ে নিন।"
              : "Wear respiratory protection and eye-wear. Wash thoroughly with soap immediately following application."}
          </div>
        </div>
      </div>

      {/* Interactive Dosage Calculator Widget */}
      <div className="border-b rule p-5 bg-paper-2/20">
        <DosageCalculator
          defaultDosageText={dosage || cleanAdvice}
          cropName={localizeCrop(result.crop)}
          diseaseName={localizedKnowledge?.nameEn || localizeDisease(result.disease)}
        />
      </div>

      {/* Dosage guidance is safety-critical */}
      <div className="mx-5 mb-4 flex items-start gap-2 rounded-lg border border-clay-soft/60 bg-clay-soft/15 px-3 py-3 text-xs leading-relaxed text-ink-soft">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-ochre" />
        <div>
          <div className="font-semibold text-clay">
            {locale === "bn" ? "রাসায়নিক ব্যবহারের আগে যাচাই করুন" : "Verify Before Chemical Application"}
          </div>
          <p className="mt-0.5">
            {locale === "bn"
              ? "উৎসে স্পষ্ট মাত্রা না থাকলে নিজে থেকে ডোজ ঠিক করবেন না। লেবেল ও স্থানীয় কৃষি কর্মকর্তার পরামর্শ মেনে চলুন।"
              : "If label rates are absent, do not guess volume. Follow certified labels and consult local agricultural extension officers."}
          </p>
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="mt-1 inline-flex min-h-9 items-center gap-1 font-semibold text-leaf hover:text-leaf-2"
          >
            <Phone className="h-3.5 w-3.5" /> {HELPLINE.krishiCallCenter}
          </a>
        </div>
      </div>

      {/* Confidence badge explanation */}
      {result.treatment_confidence && (
        <div className="border-t rule px-5 py-3">
          <p className="text-xs leading-relaxed text-ink-faint">
            {locale === "bn"
              ? "যাচাই অবস্থা পরামর্শের উৎসসমর্থন বোঝায়; এটি রোগ শনাক্তকরণের শতাংশ নয়।"
              : "Verification badge indicates institutional source grounding, not the vision confidence score."}
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
                <div className="font-medium text-ochre">
                  {locale === "bn" ? "অযাচাইকৃত দাবি" : "Unverified Advisory Claims"}
                </div>
                {result.verifier_flags.map((flag, i) => (
                  <div key={i} className="text-ink-soft">{flag}</div>
                ))}
                <a
                  href={`tel:${HELPLINE.krishiCallCenter}`}
                  className="mt-1 inline-block font-medium text-leaf transition-colors hover:text-leaf-2"
                >
                  {locale === "bn"
                    ? `নিশ্চিত হতে কৃষক কল সেন্টারে যোগাযোগ করুন: ${HELPLINE.krishiCallCenter}`
                    : `To verify with an agronomist, call: ${HELPLINE.krishiCallCenter}`}
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
            className="control-press flex min-h-10 w-full items-center justify-between gap-3 rounded-lg text-left text-xs font-semibold text-leaf cursor-pointer"
          >
            <span className="flex items-center gap-1.5">
              <FileText className="h-3.5 w-3.5" />
              {locale === "bn"
                ? `প্রমাণিত সরকারি ও গবেষণা তথ্যসূত্র (${result.treatment_sources.length}টি)`
                : `Verified Government & Research Sources (${result.treatment_sources.length})`}
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
                  const orgName = getOrgNameForSource(src, locale);
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
          <MessageCircle className="h-3.5 w-3.5 text-leaf" />
          {locale === "bn" ? "পরের কাজ ও পরামর্শ" : "Next Recommended Actions"}
        </div>
        <div className="flex flex-wrap gap-2">
          {(locale === "bn"
            ? [
                "রাসায়নিক ছাড়া কীভাবে সামলাব?",
                "বৃষ্টির আগে কী করব?",
                "আরও পরিষ্কার ছবি দিলে দেখবেন?",
              ]
            : [
                "How to manage organically?",
                "What steps before rainfall?",
                "Inspect clearer photo?",
              ]
          ).map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => onFollowUp?.(question)}
              disabled={!onFollowUp}
              className="control-press min-h-11 rounded-full border border-leaf/25 bg-leaf/5 px-3 text-xs font-medium text-leaf hover:bg-leaf/10 disabled:cursor-default disabled:opacity-70 cursor-pointer"
            >
              {question}
            </button>
          ))}
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="inline-flex min-h-11 items-center rounded-full border border-bone px-3 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
          >
            {locale === "bn" ? "কৃষি বিশেষজ্ঞ:" : "Agri Specialist:"} {HELPLINE.krishiCallCenter}
          </a>
        </div>
      </div>
    </motion.div>
  );
}

/* --- Confidence badge ------------------------------------------------- */

function ConfidenceBadge({
  confidence,
  locale,
  compact = false,
}: {
  confidence: string;
  locale: "bn" | "en";
  compact?: boolean;
}) {
  const config = {
    verified: {
      icon: ShieldCheck,
      label: locale === "bn" ? "যাচাইকৃত" : "Verified",
      color: "text-leaf",
      bg: "bg-leaf/10",
      border: "border-leaf/20",
    },
    "flagged-unverified": {
      icon: ShieldAlert,
      label: locale === "bn" ? "আংশিক যাচাইকৃত" : "Partially Verified",
      color: "text-ochre",
      bg: "bg-ochre-soft/20",
      border: "border-ochre-soft/40",
    },
    "low_confidence": {
      icon: ShieldX,
      label: locale === "bn" ? "নিম্ন নিশ্চিততা" : "Low Confidence",
      color: "text-clay",
      bg: "bg-clay-soft/20",
      border: "border-clay-soft/40",
    },
    "blocked": {
      icon: ShieldX,
      label: locale === "bn" ? "অবরুদ্ধ" : "Safety Blocked",
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
