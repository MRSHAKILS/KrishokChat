"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { MapPin, Sparkles, ArrowRight, Languages, Check } from "lucide-react";
import { cn } from "@/lib/utils";

/* =========================================================================
   DialectSelector — Regional Dialect Normalizer & Suggestion Chips.
   
   Empirically grounds the "Register Gap" discovery (AgriTrust paper §4.2):
   Farmers speak colloquial regional Bengali (e.g. Rajshahi, Rangpur, Chittagong, Sylhet),
   while agricultural extension guidelines are written in formal Standard Bengali.
   ========================================================================= */

export type DialectId = "standard" | "rajshahi" | "rangpur" | "chittagong" | "sylhet" | "barishal";

export interface DialectQuery {
  colloquial: string;
  normalized: string;
  crop: string;
  region: string;
}

export interface DialectData {
  id: DialectId;
  label: string;
  regionName: string;
  description: string;
  queries: DialectQuery[];
}

export const DIALECTS: DialectData[] = [
  {
    id: "standard",
    label: "প্রমিত বাংলা",
    regionName: "সারাদেশ",
    description: "প্রাতিষ্ঠানিক ও জাতীয় কৃষি নির্দেশিকা",
    queries: [
      {
        colloquial: "আলুর লেট ব্লাইট (নাবি ধসা) কীভাবে প্রতিরোধ করব?",
        normalized: "আলুর লেট ব্লাইট দমন ও ম্যানকোজেব স্প্রে মাত্রা",
        crop: "আলু",
        region: "সারাদেশ",
      },
      {
        colloquial: "ধানের মাজরা পোকা দমনে কী বালাইনাশক অনুমোদিত?",
        normalized: "ধানের মাজরা পোকা দমনে কারটাপ ও আইপিএম পদ্ধতি",
        crop: "ধান",
        region: "সারাদেশ",
      },
      {
        colloquial: "টমেটো গাছে ব্যাকটেরিয়াল উইল্ট হলে কী করণীয়?",
        normalized: "টমেটোর ব্যাকটেরিয়াঘটিত ঢলে পড়া রোগ প্রতিরোধ",
        crop: "টমেটো",
        region: "সারাদেশ",
      },
    ],
  },
  {
    id: "rajshahi",
    label: "রাজশাহী / নাটোর",
    regionName: "বরেন্দ্র অঞ্চল",
    description: "উত্তর-পশ্চিমাঞ্চলের আঞ্চলিক কৃষি বাগধারা",
    queries: [
      {
        colloquial: "হামার আলুর পাতা কুকড়ে যাচ্চে ক্যানে? কী ওষুধ ছিটামো?",
        normalized: "আলুর পাতা কুঁকড়ে যাওয়ার কারণ ও অনুমোদিত ছত্রাকনাশক",
        crop: "আলু",
        region: "রাজশাহী",
      },
      {
        colloquial: "ধানোত মাজরা পোকা লাইগ্যা শীষ শুকা যাচ্চে বাহে",
        normalized: "ধানের মাজরা পোকার আক্রমণ ও থোর অবস্থায় শীষ শুকানো প্রতিকার",
        crop: "ধান",
        region: "নাটোর",
      },
      {
        colloquial: "আমের গুটি ঝরে যাচ্চে, গাছে কি স্প্রে করমু?",
        normalized: "আমের গুটি ঝরা রোধে হপার পোকা দমন ও ছত্রাকনাশক স্প্রে",
        crop: "আম",
        region: "চাঁপাইনবাবগঞ্জ",
      },
    ],
  },
  {
    id: "rangpur",
    label: "রংপুর ও উত্তর",
    regionName: "রংপুর / দিনাজপুর",
    description: "তিস্তা ও তিস্তা অববাহিকার আঞ্চলিক ভাষা",
    queries: [
      {
        colloquial: "ধানের পাতাত লালচে দাগ হইছে, কি বিষ দিমু বাহে?",
        normalized: "ধানের পাতা পোড়া বা ব্রাউন স্পট রোগ দমন",
        crop: "ধান",
        region: "রংপুর",
      },
      {
        colloquial: "মরিচ গাছ শুকি মরবার নাগছে, কি করিলে ভালো হইবে?",
        normalized: "মরিচের ঢলে পড়া রোগ ও শিকড় পচা ব্যবস্থাপনা",
        crop: "মরিচ",
        region: "দিনাজপুর",
      },
      {
        colloquial: "আলুর ক্ষেতোত কুয়াশাত পাতা পচি গেইছে",
        normalized: "শীতকালে কুয়াশায় আলুর নাবি ধসা (লেট ব্লাইট) প্রতিরোধ",
        crop: "আলু",
        region: "কুড়িগ্রাম",
      },
    ],
  },
  {
    id: "chittagong",
    label: "চট্টগ্রাম",
    regionName: "চট্টগ্রাম ও পাহাড়ি অঞ্চল",
    description: "উপকূলীয় ও দক্ষিণাঞ্চলীয় চাঁটগাঁইয়া ভাষা",
    queries: [
      {
        colloquial: "আঁর খেতোত মরিচ গাছ মুরি যায়্যির, অন কি গইত্তাম?",
        normalized: "মরিচ গাছের ডাই-ব্যাক বা মড়ক রোগের চিকিৎসা",
        crop: "মরিচ",
        region: "চট্টগ্রাম",
      },
      {
        colloquial: "ধানোত পোকা লাগি হকল নষ্ট অই যার, কি ওষধ ছিটামু?",
        normalized: "ধানের ক্ষতিকারক পোকা দমন ও নিরাপদ বালাইনাশক প্রয়োগ",
        crop: "ধান",
        region: "কক্সবাজার",
      },
      {
        colloquial: "টমেটোর গাছ রোইদে হুইল্যা পইরগ্যে",
        normalized: "টমেটো গাছের ব্যাকটেরিয়াল উইল্ট ও সেচ ব্যবস্থাপনা",
        crop: "টমেটো",
        region: "ফেনী",
      },
    ],
  },
  {
    id: "sylhet",
    label: "সিলেট",
    regionName: "হাওর ও সুরমা অববাহিকা",
    description: "সিলেটি আঞ্চলিক কৃষক কথোপকথন",
    queries: [
      {
        colloquial: "খেতোর ধান পচিয়া যাইতাছে, কিতা করমু?",
        normalized: "হাওর অঞ্চলে বোরো ধানের ব্লাস্ট ও খোলপচা রোগ নিয়ন্ত্রণ",
        crop: "ধান",
        region: "সিলেট",
      },
      {
        colloquial: "আলুর পাতা কালা হইয়া ঝরিয়া পড়ের কিতা দিতাম?",
        normalized: "আলুর আগাম বা নাবি ধসা রোগে অনুমোদিত স্প্রে",
        crop: "আলু",
        region: "মৌলভীবাজার",
      },
      {
        colloquial: "লেবুর পাতাত ফোস্কা দাগ উঠছে",
        normalized: "লেবুর ক্যাংকার ও ডাই-ব্যাক রোগের চিকিৎসা",
        crop: "লেবু",
        region: "হবিগঞ্জ",
      },
    ],
  },
  {
    id: "barishal",
    label: "বরিশাল",
    regionName: "উপকূল ও দক্ষিণাঞ্চল",
    description: "দক্ষিণাঞ্চলীয় আঞ্চলিক কৃষক উপভাষা",
    queries: [
      {
        colloquial: "মোদের ধানের চারা পচ্যা যায়, কোনো ওষুধ দিলে সারবে?",
        normalized: "ধানের চারা পোড়া ও শিকড় পচা রোগ দমন",
        crop: "ধান",
        region: "বরিশাল",
      },
      {
        colloquial: "পানের পাতায় কালা দাগ পড়ছে, কি করণীয়?",
        normalized: "পানের পাতায় দাগ ও গোড়া পচা রোগের ছত্রাকনাশক",
        crop: "পান",
        region: "পটুয়াখালী",
      },
    ],
  },
];

export function DialectSelector({
  selectedDialect,
  onSelectDialect,
  onPickQuery,
}: {
  selectedDialect: DialectId;
  onSelectDialect: (id: DialectId) => void;
  onPickQuery: (q: string) => void;
}) {
  const current = DIALECTS.find((d) => d.id === selectedDialect) || DIALECTS[0];

  return (
    <div className="space-y-2.5">
      {/* Dialect Selector Chips Bar */}
      <div className="flex flex-wrap items-center gap-1.5">
        <div className="flex items-center gap-1 text-xs font-semibold text-ink-faint mr-1">
          <Languages className="h-3 w-3 text-leaf" />
          <span>আঞ্চলিক ভাষা:</span>
        </div>

        {DIALECTS.map((d) => {
          const isActive = d.id === selectedDialect;
          return (
            <button
              key={d.id}
              onClick={() => onSelectDialect(d.id)}
              className={cn(
                "relative rounded-full px-2.5 py-1 text-xs transition-all cursor-pointer font-medium",
                isActive
                  ? "bg-leaf text-paper shadow-2xs font-semibold"
                  : "bg-paper border border-bone text-ink-soft hover:border-leaf/40 hover:text-ink"
              )}
            >
              {d.label}
            </button>
          );
        })}
      </div>

      {/* Suggested Questions Grid for Active Dialect */}
      <div className="grid grid-cols-1 gap-1.5 sm:grid-cols-2 pt-1">
        {current.queries.map((q) => (
          <button
            key={q.colloquial}
            onClick={() => onPickQuery(q.colloquial)}
            className="group flex flex-col items-start rounded-xl border border-bone bg-paper p-3 text-left transition-all hover:border-leaf/50 hover:bg-leaf/5 cursor-pointer shadow-2xs"
          >
            <div className="flex w-full items-center justify-between">
              <span className="text-xs font-mono text-leaf font-semibold">{q.crop} · {q.region}</span>
              <span className="text-xs text-ink-faint opacity-60 group-hover:opacity-100 transition-opacity">
                জিজ্ঞাসা করুন ↵
              </span>
            </div>
            <div className="mt-1 text-xs sm:text-[13px] font-medium text-ink leading-snug">
              "{q.colloquial}"
            </div>
            <div className="mt-1.5 text-xs text-ink-faint flex items-center gap-1">
              <ArrowRight className="h-2.5 w-2.5 text-ochre shrink-0" />
              <span className="line-clamp-1"><strong className="text-ink-soft font-normal">প্রমিত:</strong> {q.normalized}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
