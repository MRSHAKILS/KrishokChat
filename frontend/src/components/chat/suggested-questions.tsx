"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { Sparkles, Languages } from "lucide-react";
import { enter } from "@/lib/motion";
import { DialectSelector, type DialectId } from "./dialect-selector";
import { cn } from "@/lib/utils";

/* =========================================================================
   SuggestedQuestions — starter prompts + Regional Dialect Selector.
   Supports compact mode for sidebars (e.g. /detect) and full mode for /chat.
   ========================================================================= */

const DEFAULT_SUGGESTIONS = [
  "আলুর লেট ব্লাইট কীভাবে প্রতিরোধ করব?",
  "ধানের ব্লাস্ট রোগের লক্ষণ ও চিকিৎসা কী?",
  "গমের লিফ রাস্ট রোগ দমনে কী অনুমোদিত?",
  "ফসলে পাতা হলুদ ও বাদামী দাগ হলে কী করব?",
];

const CROP_LABELS: Record<string, string> = {
  আলু: "আলু",
  potato: "আলু",
  ধান: "ধান",
  rice: "ধান",
  গম: "গম",
  wheat: "গম",
  ভুট্টা: "ভুট্টা",
  corn: "ভুট্টা",
  maize: "ভুট্টা",
  টমেটো: "টমেটো",
  tomato: "টমেটো",
  মরিচ: "মরিচ",
  chilli: "মরিচ",
  pepper: "মরিচ",
  brassica: "বাঁধাকপি/ফুলকপি",
  বাঁধাকপি: "বাঁধাকপি",
  cabbage: "বাঁধাকপি",
  ফুলকপি: "ফুলকপি",
  cauliflower: "ফুলকপি",
};

const DISEASE_LABELS: Record<string, string> = {
  "late blight": "লেট ব্লাইট (নাবি ধসা)",
  late_blight: "লেট ব্লাইট (নাবি ধসা)",
  "early blight": "আর্লি ব্লাইট (আগাম ধসা)",
  early_blight: "আর্লি ব্লাইট (আগাম ধসা)",
  "northern leaf blight": "উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
  northern_leaf_blight: "উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
  "gray leaf spot": "ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  gray_leaf_spot: "ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "common rust": "সাধারণ রাস্ট (Common Rust)",
  common_rust: "সাধারণ রাস্ট (Common Rust)",
  "brown spot": "বাদামী দাগ রোগ (Brown Spot)",
  brown_spot: "বাদামী দাগ রোগ (Brown Spot)",
  "leaf scald": "পাতা পোড়া রোগ (Leaf Scald)",
  leaf_scald: "পাতা পোড়া রোগ (Leaf Scald)",
  "narrow brown spot": "সরু বাদামী দাগ (Narrow Brown Spot)",
  narrow_brown_spot: "সরু বাদামী দাগ (Narrow Brown Spot)",
  "rice hispa": "পামরি পোকা (Rice Hispa)",
  hispa: "পামরি পোকা (Rice Hispa)",
  "sheath blight": "খোলপোড়া রোগ (Sheath Blight)",
  sheath_blight: "খোলপোড়া রোগ (Sheath Blight)",
  blast: "ব্লাস্ট",
  "leaf rust": "লিফ রাস্ট",
  leaf_rust: "লিফ রাস্ট",
  rust: "রাস্ট",
  "downy mildew": "ডাউনি মিলডিউ",
  downy_mildew: "ডাউনি মিলডিউ",
  "bacterial blight": "ব্যাকটেরিয়াল ব্লাইট",
  bacterial_blight: "ব্যাকটেরিয়াল ব্লাইট",
  "black rot": "কালো পচা রোগ (Black Rot)",
  black_rot: "কালো পচা রোগ (Black Rot)",
  "alternaria leaf spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  alternaria_leaf_spot: "অল্টারনারিয়া পাতা দাগ রোগ",
};

function labelFor(value: string | null | undefined, labels: Record<string, string>) {
  if (!value) return null;
  const normalized = value.trim().replaceAll("__", " ").replaceAll("-", " ").toLowerCase();
  if (labels[normalized] || labels[value.trim().toLowerCase()]) {
    return labels[normalized] ?? labels[value.trim().toLowerCase()];
  }
  const matchingKey = Object.keys(labels)
    .filter((key) => normalized.includes(key.replaceAll("_", " ")))
    .sort((a, b) => b.length - a.length)[0];
  return matchingKey ? labels[matchingKey] : normalized;
}

function contextualSuggestions(crop?: string | null, disease?: string | null): string[] {
  const cropLabel = labelFor(crop, CROP_LABELS);
  const diseaseLabel = labelFor(disease, DISEASE_LABELS);

  if (cropLabel && diseaseLabel) {
    return [
      `${cropLabel} গাছে ${diseaseLabel} রোগের লক্ষণ কী?`,
      `${cropLabel} এর ${diseaseLabel} রোগ কীভাবে কমাব?`,
      `${cropLabel} এর ${diseaseLabel} রোগ ছড়ানো কীভাবে রোধ করব?`,
      `${cropLabel} গাছে ${diseaseLabel} হলে কোন ভুলগুলো এড়াব?`,
    ];
  }
  if (cropLabel) {
    return [
      `${cropLabel} গাছের সাধারণ রোগের লক্ষণ কী?`,
      `${cropLabel} চাষে এখন কী পরিচর্যা দরকার?`,
      `${cropLabel} গাছে পাতা হলুদ হলে কী করব?`,
      `${cropLabel} এর রোগ প্রতিরোধের উপায় কী?`,
    ];
  }
  return DEFAULT_SUGGESTIONS;
}

export function SuggestedQuestions({
  onPick,
  crop,
  disease,
  showDialects = true,
}: {
  onPick: (q: string) => void;
  crop?: string | null;
  disease?: string | null;
  showDialects?: boolean;
}) {
  const [mode, setMode] = useState<"standard" | "dialect">("standard");
  const [selectedDialect, setSelectedDialect] = useState<DialectId>("rajshahi");
  const isContextual = Boolean(crop || disease);
  const suggestions = contextualSuggestions(crop, disease);

  // When contextual or inside compact sidebar (e.g. /detect): clean, spacious question pills
  if (isContextual || !showDialects) {
    return (
      <motion.div
        initial="hidden"
        animate="visible"
        variants={{ visible: { transition: { staggerChildren: 0.04 } } }}
        className="space-y-2 text-left"
      >
        <div className="flex items-center gap-1.5 text-[11px] font-medium text-ink-faint">
          <Sparkles className="h-3 w-3 text-leaf" />
          <span>{isContextual ? "সনাক্তকৃত ফসল সম্পর্কিত প্রশ্ন:" : "পরামর্শের জন্য প্রশ্ন নির্বাচন করুন:"}</span>
        </div>
        <div className="grid grid-cols-1 gap-2">
          {suggestions.slice(0, 3).map((q) => (
            <motion.button
              key={q}
              variants={enter}
              whileHover={{ scale: 1.008, x: 2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onPick(q)}
              className="group flex min-h-9 items-center gap-2.5 rounded-xl border rule bg-paper px-3 py-2 text-left text-xs text-ink-soft transition-colors hover:border-leaf/50 hover:bg-leaf/5 hover:text-leaf cursor-pointer shadow-2xs"
            >
              <span className="text-leaf/60 text-xs transition-transform group-hover:translate-x-0.5 group-hover:text-leaf">↳</span>
              <span className="line-clamp-1 flex-1 font-medium">{q}</span>
            </motion.button>
          ))}
        </div>
      </motion.div>
    );
  }

  // Full page view on /chat: rich dialect switcher + standard prompts
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{ visible: { transition: { staggerChildren: 0.05 } } }}
      className="space-y-4 text-left"
    >
      {/* Mode Switcher */}
      <div className="flex items-center justify-between border-b rule pb-2.5">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-ink">
          <Languages className="h-3.5 w-3.5 text-leaf" />
          <span>পরামর্শের নমুনা ও উপভাষা নির্বাচক</span>
        </div>

        <div className="flex items-center rounded-lg border rule bg-paper p-0.5 text-[11px]">
          <button
            onClick={() => setMode("standard")}
            className={cn(
              "rounded-md px-2.5 py-1 transition-colors cursor-pointer font-medium",
              mode === "standard" ? "bg-leaf text-paper font-semibold shadow-2xs" : "text-ink-soft hover:text-ink"
            )}
          >
            প্রমিত প্রশ্ন
          </button>
          <button
            onClick={() => setMode("dialect")}
            className={cn(
              "rounded-md px-2.5 py-1 transition-colors cursor-pointer font-medium",
              mode === "dialect" ? "bg-leaf text-paper font-semibold shadow-2xs" : "text-ink-soft hover:text-ink"
            )}
          >
            আঞ্চলিক উপভাষা
          </button>
        </div>
      </div>

      {mode === "dialect" ? (
        <DialectSelector
          selectedDialect={selectedDialect}
          onSelectDialect={setSelectedDialect}
          onPickQuery={onPick}
        />
      ) : (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {suggestions.map((q) => (
            <motion.button
              key={q}
              variants={enter}
              whileHover={{ scale: 1.008, x: 2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onPick(q)}
              className="group flex min-h-11 items-center gap-2 rounded-xl border rule bg-paper px-3.5 py-2.5 text-left text-xs text-ink-soft transition-colors hover:border-leaf/50 hover:bg-leaf/5 hover:text-leaf sm:text-sm cursor-pointer shadow-2xs"
            >
              <span className="text-leaf/60 text-xs transition-transform group-hover:translate-x-0.5 group-hover:text-leaf">↳</span>
              <span className="line-clamp-2 flex-1 font-medium leading-snug">{q}</span>
            </motion.button>
          ))}
        </div>
      )}
    </motion.div>
  );
}
