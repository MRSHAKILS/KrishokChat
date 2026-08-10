"use client";

import { motion } from "motion/react";
import { Sparkles } from "lucide-react";
import { enter } from "@/lib/motion";

/* =========================================================================
   SuggestedQuestions — starter prompts for farmers who don't know what to ask.
   These are real, practical questions in Bengali based on the supported crops.
   ========================================================================= */

const DEFAULT_SUGGESTIONS = [
  "আলুর লেট ব্লাইট কীভাবে প্রতিরোধ করব?",
  "ধানের ব্লাস্ট রোগের লক্ষণ কী?",
  "গমের লিফ রাস্ট রোগের চিকিৎসা কী?",
  "ফসলে বাদামী দাগ দেখা দিলে কী করব?",
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
}: {
  onPick: (q: string) => void;
  crop?: string | null;
  disease?: string | null;
}) {
  const suggestions = contextualSuggestions(crop, disease);

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{ visible: { transition: { staggerChildren: 0.06 } } }}
      className="space-y-3"
    >
      <div className="flex items-center gap-1.5 text-[11px] font-semibold text-ink-faint">
        <Sparkles className="h-3 w-3" />
        পরামর্শিত প্রশ্ন
      </div>
      <div className="grid grid-cols-1 gap-1.5 sm:grid-cols-2">
        {suggestions.map((q) => (
          <motion.button
            key={q}
            variants={enter}
            whileHover={{ scale: 1.01, x: 2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onPick(q)}
            className="group flex min-h-11 items-start gap-2 rounded-xl border rule bg-paper-2/30 px-3.5 py-2.5 text-left text-xs text-ink-soft transition-colors hover:border-leaf/50 hover:bg-leaf/5 hover:text-leaf sm:text-sm"
          >
            <span className="mt-0.5 text-leaf opacity-60 transition-opacity group-hover:opacity-100">↳</span>
            <span className="line-clamp-2 flex-1 leading-snug">{q}</span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}
