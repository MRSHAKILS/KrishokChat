"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import {
  ArrowRight, ShieldCheck, Landmark, Database, Users,
  Building2, Check, ArrowUpRight, Sparkles, Phone,
  Cpu, TrendingDown, CreditCard, Star, TrendingUp,
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
    id: "b2g",
    icon: Landmark,
    name: "সরকারি অংশীদারিত্ব",
    nameEn: "B2G — Government Partnership (Primary)",
    badge: "প্রাথমিক · Primary",
    who: "DAE · a2i · সরকারি কৃষি কল সেন্টার ১৬১২৩",
    whoEn: "DAE · a2i · 16123 Krishi Call Center",
    color: "ochre",
    value: "১৬১২৩ কৃষি কল সেন্টারের জন্য AI ফ্রন্ট-এন্ড — ট্রায়েজ ও এসক্যালেশন, প্রতিযোগিতা নয়। অনিরাপদ প্রশ্ন মডেলে যাওয়ার আগেই থামানো হয় এবং সরাসরি কল সেন্টারে পাঠানো হয়। প্রতিটি সিদ্ধান্তের অডিট লগ সরকারি ক্রেতার বিশ্বাস অর্জনের মূল সম্পদ।",
    valueEn: "AI front-end to 16123 — triage + escalation, not competition. Audit log is the trust asset that makes a government buyer comfortable.",
    evidence: [
      { label: "১৬১২৩ কল ভলিউম", value: "৯২,০৯৪ / বছর" },
      { label: "দৈনিক কল", value: "~১৮০–২০০" },
    ],
    moat: "নিরাপত্তা/অডিট স্তরটি বিশ্বব্যাপী অনন্য — Plantix, Farmer.Chat, KissanAI-এর কোনো সমতুল্য নেই।",
  },
  {
    id: "b2b",
    icon: Building2,
    name: "B2B ড্যাশবোর্ড ও অ্যানালিটিক্স",
    nameEn: "B2B — Agro-Dealers, Seed & Input Companies",
    badge: "দ্বিতীয় · Secondary",
    who: "কৃষি ডিলার · বীজ কোম্পানি · SAAO · NGO",
    whoEn: "Agro-dealers · seed companies · SAAOs · NGOs",
    color: "leaf",
    value: "জেলাভিত্তিক অ্যানালিটিক্স ড্যাশবোর্ড: কোন জেলায় কোন রোগ বাড়ছে, কোন সার বেশি জিজ্ঞেস করা হচ্ছে, কোন রাসায়নিক ফ্ল্যাগ হচ্ছে — এই মার্কেট ইন্টেলিজেন্স ডিলার ও বীজ কোম্পানির জন্য সাবস্ক্রিপশন পণ্য। ACI Fosholi ঠিক এই পথেই €৩.৫M লক্ষ্য রেখেছে।",
    valueEn: "Sell the analytics/audit dashboard (district-level disease spikes, chemical demand) to input retailers and seed companies as market intelligence.",
    evidence: [
      { label: "ACI IDSS / Fosholi লক্ষ্য", value: "€৩.৫M (২০২৫)" },
      { label: "PxD ব্যবহারকারী", value: "৭.৮M" },
    ],
    moat: "অডিট ইঞ্জিনই সবচেয়ে কম পণ্যায়নযোগ্য সম্পদ — অন্য কোনো কৃষি চ্যাটবট এটি রাখে না।",
  },
  {
    id: "api",
    icon: Database,
    name: "ডেটাসেট ও API লাইসেন্সিং",
    nameEn: "Dataset + API Licensing",
    badge: "তৃতীয় · Tertiary",
    who: "গবেষক · কৃষি-ফিনটেক · বীমা · NGO",
    whoEn: "Researchers · agri-fintech · insurance · NGOs",
    color: "clay",
    value: "৮৫,৯৭৯-ইনস্ট্যান্স প্রোভিন্যান্স-ট্রেসড বেঞ্চমার্ক ও ৭২২-ইমেজ মাটির ডেটাসেট (CC-BY-4.0 গবেষণার জন্য; বাণিজ্যিক লাইসেন্স প্রতিষ্ঠানের জন্য)। কৃষি-ফিনটেক ও ফসল বীমার জন্য গ্রাউন্ডেড পরামর্শ API। বাংলাদেশে এই পরিসরের কোনো প্রোভিন্যান্স-ট্রেসড ডেটাসেট আগে ছিল না।",
    valueEn: "85,979 benchmark + 722-image soil dataset (CC-BY-4.0 for research, commercial for companies); advisory API for agri-fintech and insurance.",
    evidence: [
      { label: "বেঞ্চমার্ক", value: "৮৫,৯৭৯ ইনস্ট্যান্স" },
      { label: "মাটির ডেটাসেট", value: "৭২২ ছবি" },
    ],
    moat: "একমাত্র প্রোভিন্যান্স-ট্রেসড বাংলা কৃষি বেঞ্চমার্ক — পুনরুৎপাদনযোগ্য, উদ্ভূতিযোগ্য।",
  },
  {
    id: "pro",
    icon: Star,
    name: "কৃষক Pro সাবস্ক্রিপশন",
    nameEn: "Farmer Pro Subscription (Secondary, Small)",
    badge: "সম্পূরক · Supplementary",
    who: "বাণিজ্যিক / নগদ-ফসল কৃষক",
    whoEn: "Commercial / cash-crop farmers who will pay for one-on-one LLM answers",
    color: "leaf",
    value: "মাসে ১০০ টাকায় (~$০.৮২) অসীমিত LLM উত্তর, ভয়েস আউটপুট, এবং প্রায়রিটি সাপোর্ট। প্রতি কৃষকে LLM খরচ মাত্র $০.০৩/মাস (Gemini API) — গ্রস মার্জিন ~৯৬%। এটি মূল রাজস্ব লেন নয়; এটি প্রমাণ করে যে ফ্রি টিয়ারের একটি আপগ্রেড পথ আছে।",
    valueEn: "100 BDT/month — unlimited LLM, voice, priority. ~96% gross margin. Not the core; proves the free tier has an upgrade path.",
    evidence: [
      { label: "মূল্য", value: "১০০ টাকা / মাস" },
      { label: "গ্রস মার্জিন", value: "~৯৬%" },
    ],
    moat: "উচ্চ মার্জিনের অর্থ হলো B2B/B2G ভলিউম সরাসরি অবদানে পরিণত হয় — লাভজনকতার ঝুঁকি নেই।",
  },
] as const;

/* Unit economics — verified 2026-08 (RunPod + Gemini public pricing) */
const COST_ROWS = [
  {
    option: "Gemini 2.5 Flash-Lite API",
    costUSD: "$০.০০০২",
    costBDT: "~০.০২৪ টাকা",
    note: "পে-পার-ইউজ, কোনো ফিক্সড কস্ট নেই",
    highlight: true,
  },
  {
    option: "RunPod RTX 4090 (Serverless)",
    costUSD: "$০.০০১৮",
    costBDT: "~০.২২ টাকা",
    note: "প্রতি সেকেন্ড বিলিং, কোনো এগ্রেস চার্জ নেই",
    highlight: false,
  },
  {
    option: "RunPod RTX 4090 (সর্বদা-চালু, ব্যাচ)",
    costUSD: "$০.০০০০৪",
    costBDT: "~০.০০৫ টাকা",
    note: "১.৫M+ প্রশ্ন/মাসে সুইচ করুন",
    highlight: false,
  },
];

const READY_NOW = [
  "কাজ করছে এন্ড-টু-এন্ড প্রোটোটাইপ: চ্যাট, রোগ নির্ণয়, মাটি, অডিট, গবেষণা প্যানেল",
  "প্রকাশিত ডেটাসেট (HuggingFace CC-BY-4.0)",
  "দুটি পেপার পিয়ার রিভিউতে (EACL + SIGIR-AP ২০২৬)",
  "এজ-ডিপ্লয়েবল রোগ মডেল (ONNX + TFLite, Android-এ <৩০ ms)",
  "লোকাল-ফার্স্ট: ল্যাপটপে অফলাইনে চলে (Ollama)",
];

const NEXT_STEPS = [
  "B2G পাইলট — DAE / a2i-এর সাথে ১৬১২৩ ইন্টিগ্রেশন আলোচনা",
  "B2B পাইলট — জেলা সম্প্রসারণ অফিসের সাথে অডিট ড্যাশবোর্ড",
  "ভয়েস-আউট TTS — নিম্ন-সাক্ষরতার কৃষকদের জন্য বাংলা অডিও পরামর্শ",
  "বর্ধিত উপভাষা কভারেজ — ৬টি আঞ্চলিক রূপ",
  "মাটির মডেল উন্নয়ন — উচ্চ-নির্ভুল সেচ পরামর্শের জন্য",
];

export default function BusinessPage() {
  const [activeLane, setActiveLane] = useState(0);
  const lane = LANES[activeLane];
  const LaneIcon = lane.icon;

  return (
    <div className="space-y-16 py-8 sm:py-12">
      {/* === Hero === */}
      <HeroSection />

      {/* === Four Revenue Lanes (interactive) === */}
      <RevenueLanesSection
        activeLane={activeLane}
        setActiveLane={setActiveLane}
        lane={lane}
        LaneIcon={LaneIcon}
      />

      {/* === Unit Economics (NEW) === */}
      <UnitEconomicsSection />

      {/* === Two-Tier Product Comparison (NEW) === */}
      <TierComparisonSection />

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
          কৃষকের জন্য সব পরামর্শ সর্বদা বিনামূল্যে। আয় আসবে প্রাতিষ্ঠানিক খাত থেকে —
          সরকারি অংশীদারিত্ব (B2G), ডিলার অ্যানালিটিক্স (B2B), এবং ডেটাসেট লাইসেন্সিং।
          প্রতিটি LLM উত্তরের খরচ মাত্র <strong className="text-leaf">দুই পয়সা</strong>।
        </motion.p>
        <motion.div variants={enter} className="mt-8 grid grid-cols-2 gap-4 sm:max-w-2xl sm:grid-cols-4">
          <HeroStat value="৪.৭ কোটি" label="কৃষক পরিবার" />
          <HeroStat value="৯২,০৯৪" label="১৬১২৩ কল/বছর" />
          <HeroStat value="~২ পয়সা" label="প্রতি LLM উত্তর" color="ochre" />
          <HeroStat value="৯৬%" label="গ্রস মার্জিন (Pro)" />
        </motion.div>
      </div>
    </motion.section>
  );
}

function HeroStat({ value, label, color = "leaf" }: { value: string; label: string; color?: "leaf" | "ochre" }) {
  return (
    <div className="rounded-xl border rule bg-paper-2/40 p-4">
      <div className={`font-display text-2xl tabular ${color === "ochre" ? "text-ochre" : "text-leaf"}`}>{value}</div>
      <div className="mt-1 text-[11px] text-ink-faint">{label}</div>
    </div>
  );
}

/* === Four Revenue Lanes (interactive tabs) === */
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
        <h2 className="font-display text-2xl text-ink sm:text-3xl">চারটি আয়ের লেন</h2>
        <p className="mt-2 text-sm text-ink-faint">Four Revenue Lanes — প্রতিটির আছে সুস্পষ্ট গ্রাহক, মূল্য, ও প্রমাণ · B2G সর্বোচ্চ অগ্রাধিকার</p>
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
                <div className="mt-0.5 text-[10px] text-ink-faint">{l.badge}</div>
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

/* === Unit Economics (NEW) === */
function UnitEconomicsSection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">ইউনিট ইকোনমিক্স</h2>
        <p className="mt-2 text-sm text-ink-faint">Unit Economics — যাচাইকৃত খরচ (RunPod + Gemini, ২০২৬-০৮)</p>
      </motion.div>

      {/* Credibility spike banner */}
      <motion.div
        variants={enter}
        className="mb-6 rounded-2xl border border-leaf/30 bg-leaf/5 p-5 sm:p-7"
      >
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:gap-8">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-leaf/10">
              <TrendingDown className="h-6 w-6 text-leaf" />
            </div>
            <div>
              <div className="font-display text-3xl text-leaf">২ পয়সা</div>
              <div className="text-[11px] text-ink-faint">প্রতি LLM উত্তরের খরচ (Gemini API)</div>
            </div>
          </div>
          <div className="h-px bg-leaf/20 sm:h-12 sm:w-px" />
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-ochre/10">
              <Cpu className="h-6 w-6 text-ochre" />
            </div>
            <div>
              <div className="font-display text-xl text-ink">$৫০০/মাস → ১ কোটি+ উত্তর</div>
              <div className="text-[11px] text-ink-faint">RunPod RTX 4090, সর্বদা-চালু, ব্যাচ vLLM</div>
            </div>
          </div>
          <div className="h-px bg-leaf/20 sm:h-12 sm:w-px" />
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-clay/10">
              <CreditCard className="h-6 w-6 text-clay" />
            </div>
            <div>
              <div className="font-display text-xl text-ink">~৯৬% গ্রস মার্জিন</div>
              <div className="text-[11px] text-ink-faint">Pro কৃষক (১০০ টাকা/মাস, ১৫০ প্রশ্ন)</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Cost table */}
      <motion.div variants={enter} className="overflow-hidden rounded-2xl border rule bg-paper">
        <div className="border-b rule bg-paper-2/40 px-5 py-3">
          <p className="text-[11px] font-semibold uppercase tracking-wide text-ink-faint">
            এক LLM প্রশ্নের খরচ · ~৮০০ ইনপুট + ৩০০ আউটপুট টোকেন (বাস্তব KrishokChat প্রশ্ন)
          </p>
        </div>
        <div className="divide-y rule">
          {COST_ROWS.map((row, i) => (
            <div
              key={i}
              className={`grid grid-cols-[1fr_auto] items-center gap-4 px-5 py-4 sm:grid-cols-[2fr_1fr_1fr_2fr] ${
                row.highlight ? "bg-leaf/3" : ""
              }`}
            >
              <div className="flex items-center gap-2">
                {row.highlight && <span className="h-1.5 w-1.5 rounded-full bg-leaf" />}
                <span className={`text-sm ${row.highlight ? "font-semibold text-ink" : "text-ink-soft"}`}>
                  {row.option}
                </span>
              </div>
              <div className="text-right">
                <div className="font-display text-sm font-semibold text-leaf tabular">{row.costBDT}</div>
                <div className="text-[10px] text-ink-faint">{row.costUSD}</div>
              </div>
              <div className="hidden text-[11px] text-ink-faint sm:block col-span-2">{row.note}</div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* GPU scale math */}
      <motion.div variants={enter} className="mt-4 rounded-2xl border rule bg-ochre/5 p-5">
        <div className="flex items-start gap-3">
          <Cpu className="mt-0.5 h-4 w-4 shrink-0 text-ochre" />
          <div>
            <p className="text-sm font-semibold text-ink">স্কেল হিসাব (GPU সেলফ-হোস্টিং)</p>
            <p className="mt-1 text-xs leading-relaxed text-ink-soft">
              একটি RTX 4090 ($০.৬৯/ঘণ্টা RunPod কমিউনিটি) = <strong>~$৪৯৭/মাস</strong> সর্বদা-চালু।
              ব্যাচড vLLM-এ এটি <strong>প্রায় ১ কোটি ৩০ লাখ প্রশ্ন/মাস</strong> হ্যান্ডেল করে।
              ১০,০০০ সক্রিয় Pro কৃষক = ১৫ লাখ প্রশ্ন/মাস — মাত্র একটি GPU-তে অনেক জায়গা বাকি থাকে।
            </p>
            <p className="mt-2 text-xs text-ink-faint">
              কৌশল: ভলিউম কম থাকলে Gemini API দিয়ে শুরু (শূন্য ফিক্সড কস্ট)। ১৫ লাখ+ প্রশ্ন/মাস হলে সেলফ-হোস্টে স্যুইচ করুন — তখন মার্জিনাল কস্ট $০.০০০০৪/প্রশ্নে নামে।
            </p>
          </div>
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === Two-Tier Product Comparison (NEW) === */
function TierComparisonSection() {
  const FREE_ROWS = [
    { feature: "চ্যাট উত্তর", freeValue: "গ্রাউন্ডেড KB থেকে সরাসরি ম্যাপ (LLM চলে না)", paidValue: "পূর্ণ LLM (KrishokChat-4B / Gemini), রিট্রিভাল-গ্রাউন্ডেড" },
    { feature: "চলার জায়গা", freeValue: "অন-ডিভাইস + লাইট সার্ভার লুকআপ", paidValue: "GPU সার্ভার (RunPod) বা Gemini API" },
    { feature: "আমাদের খরচ", freeValue: "~শূন্য (কোনো GPU, কোনো টোকেন বিল নেই)", paidValue: "~০.০২–০.২২ টাকা/প্রশ্ন" },
    { feature: "রোগ নির্ণয়", freeValue: "অন-ডিভাইস মডেল (<৩০ ms, বিনামূল্যে)", paidValue: "একই + অ্যানালিটিক্স লগড" },
    { feature: "নিরাপত্তা পাইপলাইন", freeValue: "✓ সর্বদা চালু", paidValue: "✓ সর্বদা চালু" },
    { feature: "কে ব্যবহার করে", freeValue: "প্রতিটি ক্ষুদ্র কৃষক — সামাজিক সুবিধা", paidValue: "ডিলার, বীজ কোম্পানি, NGO, সরকার, Pro কৃষক" },
  ];

  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <h2 className="font-display text-2xl text-ink sm:text-3xl">দুই-স্তর পণ্য কাঠামো</h2>
        <p className="mt-2 text-sm text-ink-faint">Two-Tier Product — নিরাপত্তা সর্বদা উভয় স্তরে বিনামূল্যে</p>
      </motion.div>

      <motion.div variants={enter} className="overflow-hidden rounded-2xl border rule bg-paper">
        {/* Header */}
        <div className="grid grid-cols-3 border-b rule bg-paper-2/50">
          <div className="px-5 py-4 text-[11px] font-semibold uppercase tracking-wide text-ink-faint">বৈশিষ্ট্য</div>
          <div className="border-l rule px-5 py-4">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-leaf" />
              <span className="text-sm font-semibold text-ink">ফ্রি টিয়ার</span>
            </div>
            <p className="mt-0.5 text-[10px] text-ink-faint">প্রতিটি কৃষকের জন্য · বিনামূল্যে সর্বদা</p>
          </div>
          <div className="border-l rule bg-ochre/5 px-5 py-4">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-ochre" />
              <span className="text-sm font-semibold text-ink">প্রাতিষ্ঠানিক / Pro টিয়ার</span>
            </div>
            <p className="mt-0.5 text-[10px] text-ink-faint">ডিলার · সরকার · Pro কৃষক</p>
          </div>
        </div>

        {/* Rows */}
        {FREE_ROWS.map((row, i) => (
          <div key={i} className={`grid grid-cols-3 border-b rule ${i % 2 === 0 ? "bg-paper" : "bg-paper-2/20"}`}>
            <div className="px-5 py-3.5">
              <span className="text-xs font-medium text-ink-soft">{row.feature}</span>
            </div>
            <div className="border-l rule px-5 py-3.5">
              <span className="text-xs text-ink-soft">{row.freeValue}</span>
            </div>
            <div className="border-l rule bg-ochre/3 px-5 py-3.5">
              <span className="text-xs text-ink-soft">{row.paidValue}</span>
            </div>
          </div>
        ))}

        {/* Footer note */}
        <div className="bg-leaf/5 px-5 py-4">
          <p className="text-center text-xs text-ink-faint">
            <strong className="text-leaf">নিরাপত্তা উভয় স্তরে সর্বদা চালু</strong> — কৃষককে নিরাপদ থাকার জন্য কখনও অর্থ দিতে হবে না।
            Safety is always on in both tiers — you never gate safety behind money.
          </p>
        </div>
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
            {/* Top-right: B2G */}
            <MoatNode className="absolute right-0 top-2" icon={Landmark} label="B2G" subLabel="১৬১২৩ · DAE" color="ochre" />
            {/* Bottom-right: B2B */}
            <MoatNode className="absolute bottom-2 right-8" icon={Building2} label="B2B" subLabel="ডিলার · SAAO" color="leaf" />
            {/* Left: API */}
            <MoatNode className="absolute left-0 top-1/2 -translate-y-1/2" icon={Database} label="API" subLabel="ডেটাসেট · ফিনটেক" color="clay" />
          </div>

          {/* Mobile: stacked nodes */}
          <div className="ml-4 flex flex-col gap-3 sm:hidden">
            <MoatNodeMobile icon={Landmark} label="B2G" subLabel="১৬১২৩ · DAE" color="ochre" />
            <MoatNodeMobile icon={Building2} label="B2B" subLabel="ডিলার · SAAO" color="leaf" />
            <MoatNodeMobile icon={Database} label="API" subLabel="ডেটাসেট · ফিনটেক" color="clay" />
          </div>
        </div>

        <p className="mt-4 max-w-2xl text-center text-sm leading-relaxed text-ink-soft mx-auto">
          নিরাপত্তা/অডিট স্তরটি বিশ্বব্যাপী অনন্য — Plantix, Farmer.Chat, KissanAI-এর কোনো সমতুল্য নেই।
          এটি একই সাথে ডেমোর কেন্দ্রবিন্দু, বিশ্বস্ততার গল্প, এবং ভবিষ্যৎ B2G/B2B আয়ের ভিত্তি।
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
        <p className="mt-2 text-sm text-ink-faint">Value Flow — কৃষক বিনামূল্যে, আয় আসে তিনটি প্রাতিষ্ঠানিক উৎস থেকে</p>
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
            <FlowArrow label="আয়" vertical />
            <FlowNode icon={Landmark} title="১৬১২৩ / DAE" subtitle="B2G (প্রথম)" color="ochre" subtitleColor="ochre" small />
            <FlowNode icon={Building2} title="ডিলার / বীজ কোম্পানি" subtitle="B2B (দ্বিতীয়)" color="leaf" subtitleColor="leaf" small />
            <FlowNode icon={Database} title="গবেষক / ফিনটেক" subtitle="লাইসেন্স" color="clay" subtitleColor="clay" small />
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-ink-faint">
          কৃষকের জন্য প্রতিটি পরামর্শ ও রোগ নির্ণয় বিনামূল্যে। আয় আসে অডিট ইঞ্জিনের উপর ভিত্তি করে —
          সরকারি ট্রায়েজ অংশীদারিত্ব (B2G), ডিলারদের অ্যানালিটিক্স ড্যাশবোর্ড (B2B), এবং ডেটাসেট/API লাইসেন্সিং।
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
    { phase: "নিকট", title: "B2G আলোচনা শুরু", desc: "DAE / a2i-এর সাথে ১৬১২৩ ইন্টিগ্রেশন ও পাইলট আলোচনা", color: "ochre" },
    { phase: "মধ্যমেয়াদি", title: "B2B পাইলট + ভয়েস", desc: "জেলা অফিসের অডিট ড্যাশবোর্ড পাইলট; TTS অডিও পরামর্শ", color: "ochre" },
    { phase: "দীর্ঘমেয়াদি", title: "সম্পূর্ণ অংশীদারিত্ব", desc: "১৬১২৩ B2G ইন্টিগ্রেশন আনুষ্ঠানিক; সেলফ-হোস্টেড GPU স্কেলিং", color: "clay" },
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
        <h2 className="font-display text-2xl text-ink sm:text-3xl">সহযোগিতা ও অংশীদারিত্ব</h2>
        <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-ink-soft">
          আমরা কৃষি সম্প্রসারণ অধিদপ্তর (DAE), কৃষি ডিলার নেটওয়ার্ক, গবেষণা প্রতিষ্ঠান ও এগ্রি-ফিনটেক উদ্যোগের সাথে পাইলট অংশীদারিত্বে আগ্রহী।
        </p>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/contact"
            className="control-press group flex items-center gap-2 rounded-xl bg-leaf px-5 py-3 text-sm font-semibold text-paper shadow-sm hover:bg-leaf-2"
          >
            যোগাযোগ ও বিস্তারিত <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
          </Link>
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="control-press flex items-center gap-2 rounded-xl border rule px-5 py-3 text-sm font-medium text-ink-soft hover:border-leaf/50 hover:bg-paper-2"
          >
            <Phone className="h-4 w-4 text-leaf" /> ১৬১২৩ কৃষি কল সেন্টার
          </a>
        </div>
        <p className="mt-6 text-[11px] text-ink-faint">
          {APP.name} একটি গবেষণা প্রোটোটাইপ (v{APP.version}) — ওপেন-অ্যাক্সেস এবং কৃষকদের জন্য সম্পূর্ণ বিনামূল্যে উন্মুক্ত।
        </p>
      </motion.div>
    </motion.section>
  );
}