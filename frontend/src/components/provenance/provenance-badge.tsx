"use client";

import React from "react";
import { Cpu, BookOpen, FileText, Sparkles, XCircle, CloudRain, Database, Smartphone, WifiOff, Sprout } from "lucide-react";
import { cn } from "@/lib/utils";

/* =========================================================================
   ProvenanceBadge (R11 / R3) — System-wide honesty component.
   
   Explicitly informs farmers, researchers, and reviewers *how* information
   was derived:
     - Tiers: deterministic_guard, structured_fact, templated_advisory, grounded_generation, progressive_guidance, honest_refusal
     - Provenance kinds: official_table, official_document, measured, ai_drafted, forecast_derived, sample_data, offline_pack, on_device
   ========================================================================= */

export type ProvenanceKind =
  | "deterministic_guard"
  | "structured_fact"
  | "templated_advisory"
  | "grounded_generation"
  | "progressive_guidance"
  | "honest_refusal"
  | "interactive_clarification"
  | "official_table"
  | "official_document"
  | "measured"
  | "ai_drafted"
  | "forecast_derived"
  | "sample_data"
  | "offline_pack"
  | "on_device";

interface BadgeConfig {
  icon: React.ElementType;
  label: string;
  desc: string;
  color: string;
  bg: string;
  pill?: string;
  isStrong?: boolean;
}

const BADGE_CONFIGS: Record<ProvenanceKind, BadgeConfig> = {
  deterministic_guard: {
    icon: Cpu,
    label: "নিরাপত্তা নিয়ম",
    desc: "নিরাপত্তা ফিল্টার ও সরাসরি নির্দেশনা (এআই ব্যবহার হয়নি)",
    color: "text-leaf",
    bg: "bg-leaf/10",
    pill: "0 AI",
    isStrong: true,
  },
  structured_fact: {
    icon: BookOpen,
    label: "সরাসরি তথ্যসারণি উত্তর",
    desc: "যাচাইকৃত BARI/BRRI তথ্যসারণি থেকে সরাসরি প্রদত্ত উত্তর — এআই ব্যবহার হয়নি",
    color: "text-leaf",
    bg: "bg-leaf/10",
    pill: "0 AI",
    isStrong: true,
  },
  templated_advisory: {
    icon: FileText,
    label: "অনুমোদিত টেমপ্লেট পরামর্শ",
    desc: "অনুমোদিত আইপিএম গাইডলাইন ও ক্রপ ক্যালেন্ডার অনুসারে নির্মিত উত্তর — এআই ব্যবহার হয়নি",
    color: "text-leaf",
    bg: "bg-leaf/10",
    pill: "0 AI",
    isStrong: true,
  },
  grounded_generation: {
    icon: Sparkles,
    label: "সূত্রভিত্তিক এআই উত্তর",
    desc: "যাচাইকৃত নথি থেকে তথ্য নিয়ে এআই উত্তর তৈরি করেছে",
    color: "text-ink-soft",
    bg: "bg-bone/60",
    pill: "Grounded LLM",
    isStrong: false,
  },
  progressive_guidance: {
    icon: Sprout,
    label: "পরিবেশবান্ধব পরিচর্যা ও পর্যবেক্ষণ",
    desc: "রাসায়নিক মাত্রা অনুপস্থিত থাকায় নন-কেমিক্যাল সাংস্কৃতিক ব্যবস্থাপনা ও মাঠ পর্যবেক্ষণ নির্দেশিকা",
    color: "text-leaf",
    bg: "bg-leaf/10",
    pill: "নন-কেমিক্যাল",
    isStrong: true,
  },
  honest_refusal: {
    icon: XCircle,
    label: "সরাসরি প্রত্যাখ্যান",
    desc: "তথ্যভাণ্ডারে পর্যাপ্ত নির্ভরযোগ্য প্রমাণ না থাকায় উত্তর প্রদান করা হয়নি",
    color: "text-clay",
    bg: "bg-clay-soft/20",
    pill: "Refusal",
    isStrong: false,
  },
  interactive_clarification: {
    icon: Sparkles,
    label: "স্লট স্পষ্টকরণ (Clarification)",
    desc: "সঠিক উত্তরের জন্য কৃষকের কাছে ফসলের নাম নিশ্চিত করা হচ্ছে",
    color: "text-ochre-dark dark:text-ochre",
    bg: "bg-ochre-soft/30",
    pill: "Disambiguation",
    isStrong: true,
  },
  official_table: {
    icon: BookOpen,
    label: "সরকারি সার সুপারিশ",
    desc: "BARC মৃত্তিকা সার নির্দেশিকা সারণি",
    color: "text-leaf",
    bg: "bg-leaf/10",
    pill: "BARC 2024",
    isStrong: true,
  },
  official_document: {
    icon: FileText,
    label: "অফিসিয়াল ম্যানুয়াল",
    desc: "DAE / BARI / BRRI প্রকাশিত নথি",
    color: "text-ink-soft",
    bg: "bg-bone/60",
    isStrong: false,
  },
  measured: {
    icon: Database,
    label: "পরিমাপিত ল্যাব উপাত্ত",
    desc: "SRDI ও গবেষণা ল্যাবরেটরির বাস্তব পরিমাপ",
    color: "text-leaf",
    bg: "bg-leaf/10",
    isStrong: true,
  },
  ai_drafted: {
    icon: Sparkles,
    label: "এআই খসড়া",
    desc: "মডেলের খসড়া — বিশেষজ্ঞ দ্বারা যাচাই সাপেক্ষ",
    color: "text-amber-700 dark:text-amber-400",
    bg: "bg-amber-500/10",
    isStrong: false,
  },
  forecast_derived: {
    icon: CloudRain,
    label: "পূর্বাভাস ভিত্তিক",
    desc: "RIMES / BMD আবহাওয়া পূর্বাভাস থেকে গণনাকৃত ঝুঁকি",
    color: "text-sky-700 dark:text-sky-400",
    bg: "bg-sky-500/10",
    pill: "Forecast",
    isStrong: true,
  },
  sample_data: {
    icon: Database,
    label: "নমুনা উপাত্ত (Placeholder)",
    desc: "ডেমো প্রদর্শনের জন্য নমুনা উপাত্ত — বাস্তব উপাত্ত নয়",
    color: "text-amber-700 dark:text-amber-400",
    bg: "bg-amber-500/10",
    pill: "Sample",
    isStrong: false,
  },
  offline_pack: {
    icon: WifiOff,
    label: "অফলাইন তথ্যপ্যাক",
    desc: "ডিভাইসে সংরক্ষিত তথ্যপ্যাক থেকে অফলাইনে প্রদত্ত উত্তর",
    color: "text-teal-700 dark:text-teal-400",
    bg: "bg-teal-500/10",
    pill: "Offline",
    isStrong: true,
  },
  on_device: {
    icon: Smartphone,
    label: "অন-ডিভাইস এআই",
    desc: "ইন্টারনেট ছাড়া সম্পূর্ণ ডিভাইসের ভেতরে নির্ণয় সম্পন্ন",
    color: "text-emerald-700 dark:text-emerald-400",
    bg: "bg-emerald-500/10",
    pill: "On-Device",
    isStrong: true,
  },
};

export interface ProvenanceBadgeProps {
  kind?: ProvenanceKind | string | null;
  tier?: string | null;
  className?: string;
  sourceNote?: string;
}

export function ProvenanceBadge({ kind, tier, className, sourceNote }: ProvenanceBadgeProps) {
  const targetKey = (kind || tier || "grounded_generation") as ProvenanceKind;
  const cfg = BADGE_CONFIGS[targetKey] ?? BADGE_CONFIGS["grounded_generation"];
  const Icon = cfg.icon;
  const tooltip = sourceNote || cfg.desc;

  return (
    <div
      title={tooltip}
      aria-label={tooltip}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border border-current/15 px-2.5 py-1 text-xs font-medium transition-colors",
        cfg.bg,
        cfg.color,
        cfg.isStrong && "border-current/25 font-semibold",
        className
      )}
    >
      <Icon className="h-3.5 w-3.5 shrink-0" strokeWidth={1.5} />
      <span>{cfg.label}</span>
      {cfg.pill && (
        <span className="ml-0.5 rounded bg-current/10 px-1 py-0.5 text-[10px] font-mono leading-none">
          {cfg.pill}
        </span>
      )}
    </div>
  );
}
