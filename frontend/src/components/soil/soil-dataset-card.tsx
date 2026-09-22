"use client";

import { motion } from "motion/react";
import { Database, Lock, MapPin, Calendar, Gauge } from "lucide-react";
import type { SoilDatasetInfo } from "@/lib/api";
import { bn, numLocale } from "@/lib/bn";
import { SOIL_TYPES, LAND_TYPES } from "@/lib/constants";
import { stagger, enter, dur, ease } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   SoilDatasetCard — the released-asset showcase.
   Frozen, precomputed stats from /api/soil/dataset. The card tells the
   farmer-story: field tensiometer truth, Pabna, 6 soil classes. Model status
   is shown honestly (in development) so the lock reads as deliberate.
   ========================================================================= */

export function SoilDatasetCard({ info }: { info: SoilDatasetInfo }) {
  const { locale } = useLanguage();
  const en = locale === "en";
  if (!info.available) {
    return (
      <div className="rounded-2xl border rule bg-paper p-6 text-center">
        <Database className="mx-auto h-8 w-8 text-ink-faint" />
        <p className="mt-3 text-sm text-ink-soft">
          {en ? "The dataset details are not available right now." : "ডেটাসেট তথ্য বর্তমানে লোড করা যায়নি। পরে আবার চেষ্টা করুন।"}
        </p>
      </div>
    );
  }

  const [kpaLo, kpaHi] = info.kpa_range;
  const binMax = Math.max(...Object.values(info.kpa_bins), 1);
  const bins = Object.entries(info.kpa_bins);

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={stagger}
      className="overflow-hidden rounded-2xl border rule bg-paper shadow-[0_10px_28px_rgba(52,39,23,0.05)]"
    >
      {/* Header */}
      <div className="border-b rule p-5 sm:p-6">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold text-ochre">
              {en ? "Published dataset · Bangladesh soil-moisture images" : "প্রকাশিত ডেটাসেট · প্রথম বাংলাদেশি মাটি-আর্দ্রতা ডেটাসেট"}
            </p>
            <h2 className="mt-1 font-display text-xl text-ink">{en ? "Bangladesh soil-moisture dataset" : "বাংলাদেশ মাটি-আর্দ্রতা ডেটাসেট"}</h2>
            <p className="mt-1 text-xs text-ink-faint">
              {en ? "RGB to kPa · field tensiometer readings" : "RGB → kPa · টেনসিওমিটার ভিত্তিক মাঠপর্যায়ের তথ্য"}
            </p>
          </div>
          <span className="flex shrink-0 items-center gap-1.5 rounded-full border border-leaf/30 bg-leaf/10 px-3 py-1.5 text-xs font-semibold text-leaf">
            <Database className="h-3.5 w-3.5" /> {en ? "Published" : "প্রকাশিত"}
          </span>
        </div>

        {/* Stat grid */}
        <div className="mt-5 grid grid-cols-2 gap-2 sm:grid-cols-4">
          <Stat value={numLocale(info.total_images, en)} label={en ? "Field photos" : "মাঠের ছবি"} />
          <Stat value={numLocale(info.soil_types.length, en)} label={en ? "Soil types" : "মাটির ধরন"} />
          <Stat value={`${numLocale(kpaLo, en)}–${numLocale(kpaHi, en)} kPa`} label={en ? "Moisture range" : "আর্দ্রতা পরিসর"} />
          <Stat value={numLocale(info.series_count, en)} label={en ? "Measurement series" : "পরিমাপ সিরিজ"} />
        </div>

        {/* Collection line */}
        <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-ink-faint">
          <span className="flex items-center gap-1.5">
            <MapPin className="h-3.5 w-3.5 text-leaf" /> {info.collection.site}
          </span>
          <span className="flex items-center gap-1.5">
            <Calendar className="h-3.5 w-3.5 text-leaf" /> {info.collection.dates}
          </span>
          <span className="flex items-center gap-1.5">
            <Gauge className="h-3.5 w-3.5 text-leaf" /> {info.collection.instrument}
          </span>
        </div>
      </div>

      {/* Preview grid */}
      <div className="border-b rule p-5 sm:p-6">
        <SectionLabel>{en ? "Sample photos — 6 soil types, wet to dry" : "নমুনা ছবি — ৬ মাটির ধরন, ভেজা → শুকনা"}</SectionLabel>
        <motion.div variants={enter} className="overflow-hidden rounded-xl border rule">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/assets/soil_samples/preview_grid.jpg"
            alt={en ? "Grid of 12 soil-moisture sample photos" : "১২টি মাটি-আর্দ্রতার নমুনা ছবির গ্রিড"}
            className="w-full object-cover"
            loading="lazy"
          />
        </motion.div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {info.samples.slice(0, 12).map((s) => {
            const meta = SOIL_TYPES[s.soil_type as keyof typeof SOIL_TYPES];
            return (
              <span
                key={s.image_id}
                className="rounded-md border rule bg-paper-2/40 px-2 py-1 text-xs text-ink-soft tabular"
              >
                {(en ? meta?.usda : meta?.bn) ?? s.soil_type} · {numLocale(s.kpa, en)} kPa
              </span>
            );
          })}
        </div>
      </div>

      {/* Soil type chips */}
      <div className="border-b rule p-5 sm:p-6">
        <SectionLabel>{en ? "Soil types (6 USDA classes)" : "মাটির ধরন (৬টি USDA শ্রেণি)"}</SectionLabel>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
          {info.soil_types.map((t, i) => {
            const meta = SOIL_TYPES[t.key as keyof typeof SOIL_TYPES];
            return (
              <motion.div
                key={t.key}
                variants={enter}
                transition={{ duration: dur.normal, ease: ease.smooth, delay: i * 0.04 }}
                className="flex items-center justify-between rounded-lg border rule bg-paper-2/30 px-3 py-2.5"
              >
                <div>
                  <div className="text-sm font-medium text-ink">{en ? t.key.replace(/_/g, "-") : meta?.bn ?? t.key}</div>
                  <div className="text-xs text-ink-faint">{t.usda}</div>
                </div>
                <span className="font-display text-sm tabular text-leaf">{numLocale(t.count, en)}</span>
              </motion.div>
            );
          })}
        </div>

        {/* kPa bins bar */}
        <div className="mt-5">
          <SectionLabel>{en ? "Moisture distribution (kPa)" : "আর্দ্রতা বণ্টন (kPa)"}</SectionLabel>
          <div className="mt-2 space-y-2">
            {bins.map(([bin, count]) => (
              <div key={bin} className="flex items-center gap-3">
                <span className="w-14 shrink-0 text-xs text-ink-soft tabular">{bin} kPa</span>
                <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-bone">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(count / binMax) * 100}%` }}
                    transition={{ duration: dur.slow, ease: ease.smooth }}
                    className="h-full rounded-full bg-ochre"
                  />
                </div>
                <span className="w-8 shrink-0 text-right text-xs text-ink-faint tabular">{numLocale(count, en)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Land types + split */}
        <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="rounded-lg bg-paper-2/30 p-3.5">
            <SectionLabel>{en ? "Land type" : "জমির ধরন"}</SectionLabel>
            <div className="mt-2 space-y-1.5">
              {Object.entries(info.land_types).map(([k, v]) => (
                <div key={k} className="flex items-center justify-between text-xs">
                  <span className="text-ink-soft">{en ? k : LAND_TYPES[k as keyof typeof LAND_TYPES] ?? k}</span>
                  <span className="tabular text-ink">{numLocale(v, en)}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-lg bg-paper-2/30 p-3.5">
            <SectionLabel>{en ? "Split (series-based, no leakage)" : "বিভাজন (সিরিজ-ভিত্তিক, লিক ছাড়া)"}</SectionLabel>
            <div className="mt-2 space-y-1.5">
              {Object.entries(info.splits).map(([k, v]) => (
                <div key={k} className="flex items-center justify-between text-xs">
                  <span className="text-ink-soft">{k}</span>
                  <span className="tabular text-ink">{numLocale(v, en)}</span>
                </div>
              ))}
            </div>
            <div className="mt-2 text-xs text-ink-faint">
              {en
                ? `Audit: ${info.corrections} kPa corrections · ${info.metadata_matched}/722 matched`
                : `অডিট: ${bn(info.corrections)}টি kPa সংশোধন · ${bn(info.metadata_matched)}/৭২২ মিলেছে`}
            </div>
          </div>
        </div>
      </div>

      {/* Model status footer */}
      <div className="flex items-center justify-between gap-3 bg-paper-2/30 px-5 py-3.5 sm:px-6">
        <span className="flex items-center gap-2 text-xs text-ink-soft">
          <Lock className="h-3.5 w-3.5 text-ochre" />
          {en ? "Automatic detection model:" : "স্বয়ংক্রিয় নির্ণয় মডেল:"} <strong className="text-ink">{en ? "in development" : "উন্নয়নে"}</strong>
        </span>
        <span className="text-xs text-ink-faint">{en ? "Dataset open · model launches after validation" : "ডেটাসেট মুক্ত · মডেল যাচাইয়ের পর চালু হবে"}</span>
      </div>
    </motion.div>
  );
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-lg border rule bg-paper-2/30 px-3 py-2.5 text-center">
      <div className="font-display text-lg tabular text-leaf">{value}</div>
      <div className="mt-0.5 text-xs text-ink-faint">{label}</div>
    </div>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-xs font-semibold text-ink-faint">{children}</div>
  );
}