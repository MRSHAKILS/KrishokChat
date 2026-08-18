"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import {
  ArrowRight, ShieldCheck, Landmark, Database, Users,
  Building2, Check, ArrowUpRight, Sparkles, Phone,
} from "lucide-react";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { APP, HELPLINE } from "@/lib/constants";

/* =========================================================================
   Color helpers — static class strings so Tailwind JIT keeps them.
   Only leaf / ochre / clay are used. Do NOT use dynamic `bg-${color}`.
   ========================================================================= */
type LaneColor = "leaf" | "ochre" | "clay";

const COLOR: Record<LaneColor, { bg: string; bgSoft: string; text: string; border: string; ring: string }> = {
  leaf: {
    bg: "bg-leaf/10",
    bgSoft: "bg-leaf/5",
    text: "text-leaf",
    border: "border-leaf/30",
    ring: "ring-leaf/20",
  },
  ochre: {
    bg: "bg-ochre/10",
    bgSoft: "bg-ochre/5",
    text: "text-ochre",
    border: "border-ochre/30",
    ring: "ring-ochre/20",
  },
  clay: {
    bg: "bg-clay/10",
    bgSoft: "bg-clay/5",
    text: "text-clay",
    border: "border-clay/30",
    ring: "ring-clay/20",
  },
};

/* =========================================================================
   /business — ব্যবসায়িক মডেল (Business Model & Sustainability)
   Three revenue lanes + moat + value flow + market readiness + roadmap.
   Uses the "কৃষি পত্রক" Field-Notebook design system.
   ========================================================================= */

const LANES = [
  {
    id: "b2b",
    icon: Building2,
    name: "ফ্রিমিয়াম + B2B",
    nameEn: "Freemium + B2B",
    who: "কৃষক বিনামূল্যে · ডিলার, SAAO, কৃষি কর্মকর্তা সাবস্ক্রিপশন",
    whoEn: "Farmers free · dealers, SAAOs, extension officers subscribe",
    color: "leaf",
    value: "কৃষকের জন্য বিনামূল্যে পরামর্শ ও রোগ নির্ণয়। কৃষি ডিলার, সম্প্রসারণ কর্মকর্তা ও SAAO-দের জন্য প্রদত্ত অডিট ও অ্যানালিটিক্স ড্যাশবোর্ড — প্রতিটি পরামর্শের নিরাপত্তা যাচাই, রাসায়নিক ফ্ল্যাগ, এবং কমপ্লায়েন্স রিপোর্ট।",
    valueEn: "Free advisory + diagnosis for farmers; paid audit/analytics dashboard for agro-dealers, SAAOs, extension officers.",
    evidence: [
      { label: "PxD", value: "৭.৮M ব্যবহারকারী" },
      { label: "ACI IDSS / Fosholi", value: "€৩.৫M ২০২৫ লক্ষ্য" },
    ],
    moat: "অডিট ইঞ্জিনই সবচেয়ে কম পণ্যায়নযোগ্য সম্পদ — অন্য কোনো কৃষি চ্যাটবট এটি রাখে না।",
  },
  {
    id: "b2g",
    icon: Landmark,
    name: "সরকারি অংশীদারিত্ব",
    nameEn: "B2G Government Partnership",
    who: "DAE · a2i · সরকারি কৃষি কল সেন্টার ১৬১২৩",
    whoEn: "DAE · a2i · 16123 Krishi Call Center",
    color: "ochre",
    value: "১৬১২৩ কৃষি কল সেন্টারের জন্য AI ফ্রন্ট-এন্ড — ট্রায়েজ ও এসক্যালেশন, প্রতিযোগিতা নয়। অনিরাপদ প্রশ্ন মডেলে যাওয়ার আগেই থামানো হয় এবং সরাসরি কল সেন্টারে পাঠানো হয়।",
    valueEn: "AI front-end to 16123 — triage + escalation, not competition.",
    evidence: [
      { label: "১৬১২৩ কল ভলিউম", value: "৯২,০৯৪ / বছর" },
      { label: "দৈনিক কল", value: "~১৮০–২০০" },
    ],
    moat: "নিরাপত্তা/অডিট স্তরটি বিশ্বব্যাপী অনন্য — Plantix, Farmer.Chat, KissanAI-এর কোনো সমতুল্য নেই।",
  },
  {
    id: "api",
    icon: Database,
    name: "ডেটাসেট ও API লাইসেন্সিং",
    nameEn: "Dataset + API Licensing",
    who: "গবেষক · কৃষি-ফিনটেক · NGO",
    whoEn: "Researchers · agri-fintech · NGOs",
    color: "clay",
    value: "৮৫,৯৭৯-ইনস্ট্যান্স প্রোভিন্যান্স-ট্রেসড বেঞ্চমার্ক ও ৭২২-ইমেজ মাটির আর্দ্রতা ডেটাসেট (CC-BY-4.0)। তৃতীয় পক্ষের যাচাই, গবেষণা লাইসেন্সিং, এবং কৃষি-ফিনটেকের জন্য পরামর্শ API।",
    valueEn: "85,979 benchmark + 722-image soil dataset (CC-BY-4.0); advisory API for agri-fintech.",
    evidence: [
      { label: "বেঞ্চমার্ক", value: "৮৫,৯৭৯ ইনস্ট্যান্স" },
      { label: "লাইসেন্স", value: "CC-BY-4.0" },
    ],
    moat: "একমাত্র প্রোভিন্যান্স-ট্রেসড বাংলা কৃষি বেঞ্চমার্ক — পুনরুৎপাদনযোগ্য, উদ্ভূতিযোগ্য।",
  },
] as const;

const READY_NOW = [
  "কাজ করছে এন্ড-টু-এন্ড প্রোটোটাইপ: চ্যাট, রোগ নির্ণয়, মাটি, অডিট, গবেষণা প্যানেল",
  "প্রকাশিত ডেটাসেট (HuggingFace CC-BY-4.0)",
  "দুটি পেপার পিয়ার রিভিউতে (EACL + SIGIR-AP ২০২৬)",
  "এজ-ডিপ্লয়েবল রোগ মডেল (ONNX + TFLite, Android-এ <৩০ ms)",
  "লোকাল-ফার্স্ট: ল্যাপটপে অফলাইনে চলে (Ollama)",
];

const NEXT_STEPS = [
  "B2B পাইলট — জেলা সম্প্রসারণ অফিসের সাথে",
  "ভয়েস-আউট TTS — নিম্ন-সাক্ষরতার কৃষকদের জন্য বাংলা অডিও পরামর্শ",
  "বর্ধিত উপভাষা কভারেজ — ৬টি আঞ্চলিক রূপ",
  "মাটির মডেল উন্নয়ন — উচ্চ-নির্ভুল সেচ পরামর্শের জন্য",
  "সম্পূর্ণ ব্যবসায়িক মূল্যায়ন ও বাজার বিশ্লেষণ",
];

export default function BusinessPage() {
  const [activeLane, setActiveLane] = useState(0);
  const lane = LANES[activeLane];
  const LaneIcon = lane.icon;

  return (
    <div className="space-y-16 py-8 sm:py-12">
      {/* === Hero === */}
      <HeroSection />

      {/* === Three Revenue Lanes (interactive) === */}
      <RevenueLanesSection
        activeLane={activeLane}
        setActiveLane={setActiveLane}
        lane={lane}
        LaneIcon={LaneIcon}
      />

      {/* === The Moat === */}
      <MoatSection />

      {/* === Value Flow === */}
      <ValueFlowSection />

      {/* === Market Readiness === */}
      <MarketReadinessSection />

      {/* === Roadmap === */}
      <RoadmapSection />

      {/* === CTA === */}
      <CTASection />
    </div>
  );
}

/* === Hero === */
function HeroSection() {
  return (
    <motion.section
      initial="hidden"
      animate="visible"
      variants={stagger}
      className="surface-lift relative mx-auto max-w-5xl overflow-hidden rounded-[24px] border rule bg-paper shadow-[0_14px_40px_rgba(52,39,23,0.08)]"
    >
      <div className="px-7 py-10 sm:px-12 sm:py-14">
        <motion.div variants={enter} className="flex items-center gap-2 text-[11px] font-semibold text-leaf">
          <span className="h-2 w-2 rounded-full bg-ochre" />
          ব্যবসায়িক মডেল · BUSINESS MODEL
        </motion.div>
        <motion.h1 variants={enter} className="mt-5 max-w-2xl font-display text-3xl leading-tight text-ink sm:text-5xl">
          কীভাবে টেকসই হবে <span className="text-leaf">কৃষক চ্যাট?</span>
        </motion.h1>
        <motion.p variants={enter} className="mt-5 max-w-xl text-base leading-relaxed text-ink-soft">
          কৃষক চ্যাট একটি গবেষণা প্রোটোটাইপ — কিন্তু এর পেছনে একটি সুস্পষ্ট টেকসই আয়ের পথ রয়েছে।
          কৃষকের জন্য সব পরামর্শ বিনামূল্যে; আয় আসবে তিনটি লেন থেকে — B2B সাবস্ক্রিপশন, সরকারি অংশীদারিত্ব, এবং ডেটাসেট/API লাইসেন্সিং।
        </motion.p>
        <motion.div variants={enter} className="mt-8 grid grid-cols-2 gap-4 sm:max-w-xl sm:grid-cols-3">
          <HeroStat value="৪.৭ কোটি" label="কৃষক পরিবার" />
          <HeroStat value="৯২,০৯৪" label="১৬১২৩ কল/বছর" />
          <HeroStat value="৩টি" label="আয়ের লেন" />
        </motion.div>
      </div>
    </motion.section>
  );
}

function HeroStat({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-xl border rule bg-paper-2/40 p-4">
      <div className="font-display text-2xl text-leaf tabular">{value}</div>
      <div className="mt-1 text-[11px] text-ink-faint">{label}</div>
    </div>
  );
}

/* === Three Revenue Lanes (interactive tabs) === */
function RevenueLanesSection({
  activeLane,
  setActiveLane,
  lane,
  LaneIcon,
}: {
  activeLane: number;
  setActiveLane: (n: number) => void;
  lane: (typeof LANES)[number];
  LaneIcon: typeof Building2;
}) {
  const c = COLOR[lane.color];
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">তিনটি আয়ের লেন</h2>
        <p className="mt-2 text-sm text-ink-faint">Three Revenue Lanes — প্রতিটির আছে সুস্পষ্ট গ্রাহক, মূল্য, ও প্রমাণ</p>
      </motion.div>

      {/* Tab list */}
      <motion.div variants={enter} className="flex flex-col gap-2 sm:flex-row sm:gap-3">
        {LANES.map((l, i) => {
          const Icon = l.icon;
          const active = i === activeLane;
          return (
            <button
              key={l.id}
              type="button"
              onClick={() => setActiveLane(i)}
              className={`control-press flex flex-1 items-center gap-3 rounded-xl border px-4 py-3.5 text-left transition-colors ${
                active
                  ? "border-leaf bg-leaf/8 text-ink"
                  : "border-rule bg-paper text-ink-soft hover:border-leaf/40 hover:bg-paper-2/50"
              }`}
            >
              <Icon className={`h-5 w-5 shrink-0 ${active ? "text-leaf" : "text-ink-faint"}`} />
              <div className="min-w-0">
                <div className="text-sm font-semibold leading-tight">{l.name}</div>
                <div className="mt-0.5 text-[10px] text-ink-faint">{l.nameEn}</div>
              </div>
              {active && <motion.div layoutId="lane-underline" className="ml-auto h-2 w-2 rounded-full bg-leaf" />}
            </button>
          );
        })}
      </motion.div>

      {/* Panel */}
      <motion.div
        variants={enter}
        className="mt-4 overflow-hidden rounded-2xl border rule bg-paper shadow-[0_8px_30px_rgba(52,39,23,0.06)]"
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={lane.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="grid gap-6 p-6 sm:grid-cols-[1.4fr_1fr] sm:p-8"
          >
            {/* Left: value */}
            <div>
              <div className="flex items-center gap-2.5">
                <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${c.bg}`}>
                  <LaneIcon className={`h-5 w-5 ${c.text}`} />
                </div>
                <div>
                  <h3 className="font-display text-lg text-ink">{lane.name}</h3>
                  <p className="text-[11px] text-ink-faint">{lane.nameEn}</p>
                </div>
              </div>
              <p className="mt-5 text-sm leading-relaxed text-ink-soft">{lane.value}</p>
              <div className="mt-5 rounded-xl border-l-2 border-ochre bg-ochre/5 p-3.5">
                <div className="flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-wide text-ochre">
                  <Sparkles className="h-3.5 w-3.5" /> মোট (Moat)
                </div>
                <p className="mt-1.5 text-xs leading-relaxed text-ink-soft">{lane.moat}</p>
              </div>
            </div>

            {/* Right: who pays + evidence */}
            <div className="space-y-4">
              <div className="rounded-xl border rule bg-paper-2/40 p-4">
                <div className="flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-wide text-ink-faint">
                  <Users className="h-3.5 w-3.5" /> কে পরিশোধ করে
                </div>
                <p className="mt-1.5 text-sm font-medium text-ink">{lane.who}</p>
                <p className="mt-0.5 text-[11px] text-ink-faint">{lane.whoEn}</p>
              </div>
              <div className="rounded-xl border rule bg-paper-2/40 p-4">
                <div className="text-[10px] font-semibold uppercase tracking-wide text-ink-faint">প্রমাণ (Evidence)</div>
                <div className="mt-2 space-y-2">
                  {lane.evidence.map((e) => (
                    <div key={e.label} className="flex items-center justify-between gap-2">
                      <span className="text-xs text-ink-soft">{e.label}</span>
                      <span className="font-display text-sm font-semibold text-leaf tabular">{e.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </motion.div>
    </motion.section>
  );
}

/* === The Moat === */
function MoatSection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">আমাদের মোট — অডিট ইঞ্জিন</h2>
        <p className="mt-2 text-sm text-ink-faint">The moat — the safety/audit engine is the least-commoditized asset</p>
      </motion.div>

      <motion.div
        variants={enter}
        className="relative overflow-hidden rounded-2xl border rule bg-paper-2/40 p-8 sm:p-12"
      >
        {/* Radial diagram */}
        <div className="relative mx-auto flex max-w-2xl items-center justify-center py-6">
          {/* Center: the audit engine */}
          <div className="relative z-10 flex flex-col items-center">
            <div className="flex h-24 w-24 items-center justify-center rounded-full border-2 border-leaf bg-leaf/10 shadow-[0_0_30px_rgba(47,93,58,0.15)]">
              <ShieldCheck className="h-10 w-10 text-leaf" />
            </div>
            <div className="mt-3 text-center">
              <div className="font-display text-sm font-semibold text-ink">অডিট ইঞ্জিন</div>
              <div className="text-[10px] text-ink-faint">Audit Engine</div>
            </div>
          </div>

          {/* Three revenue nodes positioned around — desktop only */}
          <div className="pointer-events-none absolute inset-0 hidden sm:block">
            {/* Top-right: B2B */}
            <MoatNode className="absolute right-0 top-2" icon={Building2} label="B2B" subLabel="ডিলার · SAAO" color="leaf" />
            {/* Bottom-right: B2G */}
            <MoatNode className="absolute bottom-2 right-8" icon={Landmark} label="B2G" subLabel="১৬১২৩ · DAE" color="ochre" />
            {/* Left: API */}
            <MoatNode className="absolute left-0 top-1/2 -translate-y-1/2" icon={Database} label="API" subLabel="ডেটাসেট · ফিনটেক" color="clay" />
          </div>

          {/* Mobile: stacked nodes */}
          <div className="ml-4 flex flex-col gap-3 sm:hidden">
            <MoatNodeMobile icon={Building2} label="B2B" subLabel="ডিলার · SAAO" color="leaf" />
            <MoatNodeMobile icon={Landmark} label="B2G" subLabel="১৬১২৩ · DAE" color="ochre" />
            <MoatNodeMobile icon={Database} label="API" subLabel="ডেটাসেট · ফিনটেক" color="clay" />
          </div>
        </div>

        <p className="mt-4 max-w-2xl text-center text-sm leading-relaxed text-ink-soft mx-auto">
          নিরাপত্তা/অডিট স্তরটি বিশ্বব্যাপী অনন্য — Plantix, Farmer.Chat, KissanAI-এর কোনো সমতুল্য নেই।
          এটি একই সাথে ডেমোর কেন্দ্রবিন্দু, বিশ্বস্ততার গল্প, এবং ভবিষ্যৎ B2B/B2G আয়ের ভিত্তি।
        </p>
      </motion.div>
    </motion.section>
  );
}

function MoatNode({
  className,
  icon: Icon,
  label,
  subLabel,
  color,
}: {
  className?: string;
  icon: typeof Building2;
  label: string;
  subLabel: string;
  color: "leaf" | "ochre" | "clay";
}) {
  const c = COLOR[color];
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className={`flex h-12 w-12 items-center justify-center rounded-xl border ${c.bg} ${c.border}`}>
        <Icon className={`h-5 w-5 ${c.text}`} />
      </div>
      <div>
        <div className="font-display text-sm font-semibold text-ink">{label}</div>
        <div className="text-[10px] text-ink-faint">{subLabel}</div>
      </div>
    </div>
  );
}

function MoatNodeMobile({
  icon: Icon,
  label,
  subLabel,
  color,
}: {
  icon: typeof Building2;
  label: string;
  subLabel: string;
  color: "leaf" | "ochre" | "clay";
}) {
  const c = COLOR[color];
  return (
    <div className="flex items-center gap-2.5">
      <div className={`flex h-10 w-10 items-center justify-center rounded-xl border ${c.bg} ${c.border}`}>
        <Icon className={`h-4 w-4 ${c.text}`} />
      </div>
      <div>
        <div className="text-sm font-semibold text-ink">{label}</div>
        <div className="text-[10px] text-ink-faint">{subLabel}</div>
      </div>
    </div>
  );
}

/* === Value Flow === */
function ValueFlowSection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">মূল্য প্রবাহ</h2>
        <p className="mt-2 text-sm text-ink-faint">Value Flow — কৃষক বিনামূল্যে, আয় আসে তিনটি উৎস থেকে</p>
      </motion.div>

      <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex flex-col items-stretch gap-3 sm:flex-row sm:items-center sm:justify-between">
          {/* Farmers (free) */}
          <FlowNode icon={Users} title="কৃষক" subtitle="বিনামূল্যে" color="leaf" subtitleColor="leaf" />

          <FlowArrow label="পরামর্শ" />

          {/* Audit engine core */}
          <FlowNode icon={ShieldCheck} title="অডিট ইঞ্জিন" subtitle="মূল সম্পদ" color="ochre" subtitleColor="ochre" wide />

          {/* Three outputs */}
          <div className="flex flex-col gap-2 sm:gap-2.5">
            <FlowArrow label="B2B" vertical />
            <FlowNode icon={Building2} title="ডিলার / SAAO" subtitle="সাবস্ক্রিপশন" color="leaf" subtitleColor="leaf" small />
            <FlowNode icon={Landmark} title="১৬১২৩ / DAE" subtitle="অংশীদারিত্ব" color="ochre" subtitleColor="ochre" small />
            <FlowNode icon={Database} title="গবেষক / ফিনটেক" subtitle="লাইসেন্স" color="clay" subtitleColor="clay" small />
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-ink-faint">
          কৃষকের জন্য প্রতিটি পরামর্শ ও রোগ নির্ণয় বিনামূল্যে। আয় আসে অডিট ইঞ্জিনের উপর ভিত্তি করে —
          ডিলারদের কমপ্লায়েন্স ড্যাশবোর্ড, সরকারি ট্রায়েজ অংশীদারিত্ব, এবং ডেটাসেট/API লাইসেন্সিং থেকে।
        </p>
      </motion.div>
    </motion.section>
  );
}

function FlowNode({
  icon: Icon,
  title,
  subtitle,
  color,
  subtitleColor,
  wide,
  small,
}: {
  icon: typeof Building2;
  title: string;
  subtitle: string;
  color: "leaf" | "ochre" | "clay";
  subtitleColor: "leaf" | "ochre" | "clay";
  wide?: boolean;
  small?: boolean;
}) {
  const c = COLOR[color];
  const sc = COLOR[subtitleColor];
  return (
    <div
      className={`surface-lift flex flex-col items-center justify-center rounded-xl border rule bg-paper-2/40 text-center ${
        small ? "p-2.5" : wide ? "min-w-[140px] p-4" : "min-w-[110px] p-3.5"
      }`}
    >
      <div className={`flex ${small ? "h-8 w-8" : "h-11 w-11"} items-center justify-center rounded-lg ${c.bg}`}>
        <Icon className={`${small ? "h-4 w-4" : "h-5 w-5"} ${c.text}`} />
      </div>
      <div className={`mt-2 font-semibold text-ink ${small ? "text-[11px]" : "text-sm"}`}>{title}</div>
      <div className={`${sc.text} ${small ? "text-[9px]" : "text-[11px]"} font-medium`}>{subtitle}</div>
    </div>
  );
}

function FlowArrow({ label, vertical }: { label: string; vertical?: boolean }) {
  return (
    <div className={`flex items-center justify-center ${vertical ? "my-1" : ""}`}>
      <div className="flex items-center gap-1.5">
        {!vertical && <div className="h-px w-4 bg-leaf/30 sm:w-6" />}
        <span className="rounded-full bg-leaf/10 px-2 py-0.5 text-[10px] font-medium text-leaf">{label}</span>
        {!vertical && <div className="h-px w-4 bg-leaf/30 sm:w-6" />}
        {!vertical && <ArrowRight className="h-3.5 w-3.5 text-leaf/50" />}
      </div>
    </div>
  );
}

/* === Market Readiness === */
function MarketReadinessSection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">বাজার প্রস্তুতি</h2>
        <p className="mt-2 text-sm text-ink-faint">Market Readiness — এখন যা প্রস্তুত, পরবর্তী যা আসবে</p>
      </motion.div>

      <motion.div variants={enter} className="grid gap-4 sm:grid-cols-2">
        {/* Ready now */}
        <div className="rounded-2xl border rule bg-leaf/5 p-6">
          <div className="flex items-center gap-2 text-leaf">
            <Check className="h-5 w-5" />
            <h3 className="font-display text-lg text-ink">এখনই প্রস্তুত</h3>
          </div>
          <ul className="mt-4 space-y-2.5">
            {READY_NOW.map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-ink-soft">
                <Check className="mt-0.5 h-4 w-4 shrink-0 text-leaf" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Next steps */}
        <div className="rounded-2xl border rule bg-ochre/5 p-6">
          <div className="flex items-center gap-2 text-ochre">
            <ArrowUpRight className="h-5 w-5" />
            <h3 className="font-display text-lg text-ink">পরবর্তী পদক্ষেপ</h3>
          </div>
          <ul className="mt-4 space-y-2.5">
            {NEXT_STEPS.map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-ink-soft">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-ochre" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === Roadmap === */
function RoadmapSection() {
  const items = [
    { phase: "এখন", title: "কার্যকর প্রোটোটাইপ", desc: "চ্যাট, রোগ নির্ণয়, মাটি, অডিট, গবেষণা — সব কাজ করছে", color: "leaf" },
    { phase: "নিকট", title: "B2B পাইলট", desc: "একটি জেলা সম্প্রসারণ অফিসের সাথে অডিট ড্যাশবোর্ড পাইলট", color: "ochre" },
    { phase: "মধ্যমেয়াদি", title: "ভয়েস ও উপভাষা", desc: "TTS অডিও পরামর্শ ও ৬ উপভাষার সম্পূর্ণ কভারেজ", color: "ochre" },
    { phase: "দীর্ঘমেয়াদি", title: "সরকারি অংশীদারিত্ব", desc: "১৬১২৩ কল সেন্টারের সাথে আনুষ্ঠানিক B2G ইন্টিগ্রেশন", color: "clay" },
  ] as const;

  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">রোডম্যাপ</h2>
        <p className="mt-2 text-sm text-ink-faint">Roadmap — এখন থেকে দীর্ঘমেয়াদি</p>
      </motion.div>

      <motion.div variants={enter} className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {items.map((item, i) => {
          const c = COLOR[item.color];
          return (
          <div
            key={i}
            className="surface-lift rounded-xl border rule bg-paper p-4"
          >
            <div className={`inline-block rounded-full ${c.bgSoft} px-2.5 py-0.5 text-[10px] font-semibold ${c.text}`}>
              {item.phase}
            </div>
            <h3 className="mt-3 font-display text-base text-ink">{item.title}</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-ink-soft">{item.desc}</p>
          </div>
          );
        })}
      </motion.div>
    </motion.section>
  );
}

/* === CTA === */
function CTASection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-3xl"
    >
      <motion.div
        variants={enter}
        className="surface-lift rounded-[24px] border rule bg-paper p-8 text-center shadow-[0_10px_30px_rgba(52,39,23,0.06)] sm:p-12"
      >
        <h2 className="font-display text-2xl text-ink sm:text-3xl">অংশীদারিত্বে আগ্রহী?</h2>
        <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-ink-soft">
          আমরা কৃষি সম্প্রসারণ অধিদপ্তমেন্ট, ডিলার নেটওয়ার্ক, গবেষণা প্রতিষ্ঠান ও ফিনটেকের সাথে
          অংশীদারিত্বে আগ্রহী। আলোচনার জন্য যোগাযোগ করুন।
        </p>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/contact"
            className="control-press group flex items-center gap-2 rounded-xl bg-leaf px-5 py-3 text-sm font-semibold text-paper shadow-sm hover:bg-leaf-2"
          >
            যোগাযোগ করুন <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
          </Link>
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="control-press flex items-center gap-2 rounded-xl border rule px-5 py-3 text-sm font-medium text-ink-soft hover:border-leaf/50 hover:bg-paper-2"
          >
            <Phone className="h-4 w-4 text-leaf" /> ১৬১২৩
          </a>
        </div>
        <p className="mt-6 text-[11px] text-ink-faint">
          {APP.name} একটি গবেষণা প্রোটোটাইপ (v{APP.version}) — বাণিজ্যিক পণ্য নয়। ব্যবসায়িক মডেল ক্যাপস্টোনের জন্য উন্নয়নাধীন।
        </p>
      </motion.div>
    </motion.section>
  );
}