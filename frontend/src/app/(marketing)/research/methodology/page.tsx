"use client";

import { motion } from "motion/react";
import { FileText, Layers, Lock, Snowflake, GitBranch } from "lucide-react";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Methodology Page — shows how 284 PDFs became 85,979 benchmark instances.
   The construction pipeline, the 4 tracks, design principles, and
   knowledge node construction from the AgriTrust paper.

   No images needed — built entirely with animated HTML/SVG/Motion.
   ========================================================================= */

const PIPELINE_STAGES = [
  { value: RESEARCH_STATS.publications, label: "সরকারি PDF", detail: "১৩ প্রতিষ্ঠান থেকে" },
  { value: "২,৬৮০", label: "সেকশন প্যাসেজ", detail: "OCR + Markdown রূপান্তর" },
  { value: "২,৯৪৬", label: "সিম্যান্টিক ইউনিট", detail: "হেডার-গাইডেড খণ্ডায়ন" },
  { value: RESEARCH_STATS.benchmarkInstances, label: "ইনস্ট্যান্স", detail: "উত্পাদন সেল + ইনটেন্ট" },
  { value: "৪", label: "ট্র্যাক", detail: "কোয়ালিটি গেট পাস" },
];

const TRACKS = [
  {
    name: "সাধারণ জ্ঞান QA",
    en: "General Knowledge QA",
    count: "২৮,৯৯৩",
    desc: "রাসায়নিক-মুক্ত জ্ঞান পরীক্ষণ",
    detail: "চাষ, জাত নির্বাচন, সেচ, পোষ্ট-হার্ভেস্ট",
  },
  {
    name: "চিকিৎসা QA",
    en: "Treatment QA",
    count: "১১,২২৪",
    desc: "নিরাপত্তা-সংবেদনশীল রাসায়নিক পরামর্শ",
    detail: "৭,৪৩৭ (৬৬.৩%) রাসায়নিক_ট্রেস বহনকারী",
  },
  {
    name: "নিরাপত্তা QA",
    en: "Safety Refusal & Re-query",
    count: "২০,১১২",
    desc: "১২-শ্রেণী প্রত্যাখ্যান + EVPI রি-কোয়েরি",
    detail: "৩,২১৬ T3 প্রত্যাখ্যান + ১৬,৮৯৬ T4 রি-কোয়েরি",
  },
  {
    name: "টেবিল QA",
    en: "Table Reasoning QA",
    count: "২৫,৬৫০",
    desc: "৩-স্তরের কাঠামোগত রিজনিং",
    detail: "L1 লুকআপ + L2 রো রিজনিং + L3 সমষ্টি",
  },
];

const PRINCIPLES = [
  {
    icon: FileText,
    title: "উত্তর নির্যাসিত, তৈরি নয়",
    en: "Answers extracted, never generated",
    desc: "রেফারেন্স উত্তর সরাসরি সিম্যান্টিক ইউনিট থেকে নির্যাসিত — মডেল শুধু প্রশ্নের পৃষ্ঠ পরিবর্তন করে।",
  },
  {
    icon: Layers,
    title: "বৈচিত্র্য নমুনায়িত, টেমপ্লেট নয়",
    en: "Diversity sampled, not templated",
    desc: "প্রশ্ন পৃষ্ঠ ডায়ালেক্ট, পার্সোনা, ফর্মুলেশন, সিনারিও, ব্লুম স্তরে বিভক্ত মাতৃকা থেকে।",
  },
  {
    icon: Snowflake,
    title: "কনটেন্ট টোকেন ফ্রোজেন",
    en: "Content tokens frozen across dialects",
    desc: "৬ উপভাষায় রাসায়নিক নাম, ডোজ, ইউনিট, সংখ্যা অপরিবর্তিত — সিলেটি কৃষক প্রমিত কৃষকের সমান পরামর্শ পান।",
  },
  {
    icon: Lock,
    title: "প্রতিটি ইনস্ট্যান্স প্রমাণ-লকড",
    en: "Each instance provenance-locked",
    desc: "উৎস পাথ, প্রকাশক, পৃষ্ঠা সাইটেশন প্রতিটি রেকর্ডে — পুনরায় অডিটযোগ্য।",
  },
];

const NODE_CONSTRUCTION = [
  { step: 1, label: "PDF → Markdown", detail: "Mistral OCR, লেআউট সংরক্ষণ" },
  { step: 2, label: "টপিক খণ্ডায়ন", detail: "২,৮৮২ টপিক-কোহেরেন্ট নোড" },
  { step: 3, label: "এনটিটি নিষ্কাশন", detail: "১৯,৭৬৮ এনটিটি (৬.৯/নোড)" },
  { step: 4, label: "ট্রিপল নিষ্কাশন", detail: "১৭,৫০১ ফ্যাক্টুয়াল ট্রিপল" },
  { step: 5, label: "প্রমাণ ইনজেকশন", detail: "ডিটারমিনিস্টিক, LLM-বিহীন" },
  { step: 6, label: "ক্রস-ভেরিফিকেশন", detail: "GPT-5-Nano দ্বারা যাচাই" },
  { step: 7, label: "ক্লোজড-লুপ পরিমার্জন", detail: "২৮৩ নোড (৯.৮%) পুনরায় তৈরি" },
];

export default function MethodologyPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* === Hero === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="text-center"
      >
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          Construction Methodology
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          প্রমাণ-সংরক্ষণকারী <span className="text-leaf">নির্মাণ পাইপলাইন</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          {RESEARCH_STATS.publications}টি সরকারি প্রকাশনা থেকে {RESEARCH_STATS.benchmarkInstances}টি মূল্যায়ন ইনস্ট্যান্স —
          প্রতিটি ধাপ প্রমাণ-সংরক্ষণকারী, প্রতিটি উত্তর উৎসে ফিরে যাচাইযোগ্য।
        </motion.p>
      </motion.section>

      {/* === A. Construction Pipeline (animated) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 text-center font-display text-2xl text-ink">
          নির্মাণ পাইপলাইন
        </motion.h2>
        <motion.p variants={enter} className="mb-8 text-center text-sm text-ink-soft">
          ৫ ধাপে ২৮৪টি PDF থেকে ৮৫,৯৭৯টি ইনস্ট্যান্স।
        </motion.p>

        {/* Horizontal pipeline on desktop, vertical on mobile */}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-stretch sm:justify-between">
          {PIPELINE_STAGES.map((stage, i) => (
            <div key={i} className="flex flex-1 flex-col items-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15, duration: dur.normal, ease: ease.smooth }}
                className="flex w-full flex-col items-center rounded-lg border rule bg-paper px-3 py-4 text-center"
              >
                <div className="font-display text-2xl tabular text-leaf">{stage.value}</div>
                <div className="mt-1 text-xs font-medium text-ink">{stage.label}</div>
                <div className="mt-0.5 text-[10px] leading-tight text-ink-faint">{stage.detail}</div>
              </motion.div>
              {/* Arrow connector */}
              {i < PIPELINE_STAGES.length - 1 && (
                <motion.div
                  initial={{ opacity: 0, scaleX: 0 }}
                  whileInView={{ opacity: 1, scaleX: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.15 + 0.1, duration: dur.normal }}
                  className="my-2 text-leaf sm:my-0 sm:mx-1"
                >
                  <div className="hidden sm:block">→</div>
                  <div className="sm:hidden">↓</div>
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </motion.section>

      {/* === B. The 4 Tracks === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          ৪ ট্র্যাক
        </motion.h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {TRACKS.map((track, i) => (
            <motion.div
              key={i}
              variants={enter}
              className="rounded-xl border rule bg-paper p-5"
            >
              <div className="flex items-baseline justify-between">
                <div>
                  <div className="font-display text-base text-ink">{track.name}</div>
                  <div className="font-mono text-[10px] text-ink-faint">{track.en}</div>
                </div>
                <div className="font-display text-xl tabular text-leaf">{track.count}</div>
              </div>
              <p className="mt-3 text-sm text-ink-soft">{track.desc}</p>
              <p className="mt-1 text-xs text-ink-faint">{track.detail}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === C. Design Principles === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          নকশা নীতি
        </motion.h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {PRINCIPLES.map((p, i) => (
            <motion.div key={i} variants={enter} className="rounded-lg border rule bg-paper p-5">
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                  <p.icon className="h-5 w-5" />
                </div>
                <div>
                  <div className="font-display text-base text-ink">{p.title}</div>
                  <div className="font-mono text-[10px] text-ink-faint">{p.en}</div>
                  <p className="mt-2 text-sm leading-relaxed text-ink-soft">{p.desc}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === D. Knowledge Node Construction (AgriTrust) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          জ্ঞান নোড নির্মাণ
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          AgriTrust পত্র থেকে — ৩-স্তরের নোড কাঠামো: কনটেন্ট, স্ট্রাকচার্ড ফ্যাক্ট, প্রমাণ।
        </motion.p>

        {/* 3-layer node structure */}
        <motion.div variants={enter} className="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
          {[
            { layer: "১", title: "ন্যাচারাল ল্যাঙ্গুয়েজ কনটেন্ট", detail: "সারাংশ, লক্ষণ, ব্যবস্থাপনা" },
            { layer: "২", title: "স্ট্রাকচার্ড ফ্যাক্ট", detail: "এনটিটি, ট্রিপল, রাসায়নিক" },
            { layer: "৩", title: "প্রমাণ", detail: "উৎস, পৃষ্ঠা, প্রতিষ্ঠান" },
          ].map((layer) => (
            <div key={layer.layer} className="rounded-lg border rule bg-paper-2/40 px-4 py-3 text-center">
              <div className="flex h-8 w-8 mx-auto items-center justify-center rounded-full bg-leaf/10 font-display text-sm text-leaf tabular">
                {layer.layer}
              </div>
              <div className="mt-2 font-display text-sm text-ink">{layer.title}</div>
              <div className="mt-1 text-xs text-ink-faint">{layer.detail}</div>
            </div>
          ))}
        </motion.div>

        {/* 7-step construction flow */}
        <motion.div variants={enter} className="space-y-2">
          <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-[0.14em] text-ochre">
            <GitBranch className="h-3.5 w-3.5" />
            নোড নির্মাণ প্রক্রিয়া
          </div>
          {NODE_CONSTRUCTION.map((step, i) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, x: -10 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08, duration: dur.fast }}
              className="flex items-center gap-3 rounded-lg border rule bg-paper px-4 py-2.5"
            >
              <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-leaf/10 font-display text-xs text-leaf tabular">
                {step.step}
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-ink">{step.label}</div>
              </div>
              <div className="text-xs text-ink-faint">{step.detail}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Verification stats */}
        <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
          {[
            { value: "৯৬.১%", label: "এনটিটি কভারেজ" },
            { value: "১০০%", label: "ট্রিপল কভারেজ" },
            { value: "২৮৩", label: "রিফাইন করা নোড" },
            { value: "০.৮১", label: "মানব অডিট κ" },
          ].map((stat) => (
            <div key={stat.label} className="rounded-lg border rule bg-paper px-3 py-3 text-center">
              <div className="font-display text-lg tabular text-leaf">{stat.value}</div>
              <div className="mt-1 text-[10px] text-ink-faint">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </motion.section>
    </div>
  );
}
