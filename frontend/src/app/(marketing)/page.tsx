"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import {
  ArrowRight, Shield, FileText, Languages, CloudSun, Phone,
  CheckCircle2, Loader2, MapPin, Play, Search, PenLine, RotateCcw,
  Camera, MessageSquare, Calculator, Volume2, Sparkles, Building2,
  HelpCircle, ChevronDown, ScanLine, Network, BarChart3,
} from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
  PieChart, Pie,
} from "recharts";
import { APP, RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { AgentTrace } from "@/components/agent-trace";
import { QA_STAGES, type RailEvent } from "@/components/detect/pipeline-rail";
import { getWeather, registerHelpline } from "@/lib/api";
import { safetyLabel, TONE_BADGE, AGRI_DISTRICTS } from "@/lib/safety-labels";

/* =========================================================================
   Landing Page — modern, visual, multi-section.
   Team + fieldwork visible directly. Charts instead of plain numbers.
   RAG pipeline animated demo. Weather + helpline.
   ========================================================================= */

const TRACK_DATA = [
  { name: "সাধারণ কৃষি QA", value: 28993, color: "var(--color-leaf)" },
  { name: "সার ও সয়েল গাইড QA", value: 25650, color: "var(--color-leaf-2)" },
  { name: "নিরাপত্তা পলিসি QA", value: 20112, color: "var(--color-ochre)" },
  { name: "বালাই ব্যবস্থাপনা QA", value: 11224, color: "var(--color-clay)" },
];

/* Farmer-facing retrieval chart labels — the backend enums (BM25, Dense,
   Hybrid RRF, ColBERT) are technical jargon; the home page is for farmers.
   The /research/benchmark page keeps the full technical terms for reviewers. */
const RETRIEVAL_DATA = [
  { name: "মিশ্র পদ্ধতি", value: 0.539, best: true },
  { name: "শব্দ মিল", value: 0.506, best: false },
  { name: "অর্থ মিল", value: 0.464, best: false },
  { name: "সূক্ষ্ম মিল", value: 0.487, best: false },
];

const RAG_QUERY = "আলুর লেট ব্লাইট কীভাবে প্রতিরোধ করব?";
/* Human document titles instead of raw DB IDs (DAE_PEST_1206A0_001).
   Farmers should never see backend identifiers. */
const RAG_SOURCES = [
  {
    title: "কৃষি সম্প্রসারণ অধিদপ্তর — বালাই ব্যবস্থাপনা গাইডলাইন (অধ্যায় ৪)",
    agency: "DAE",
    snippet: "প্রতি লিটার পানিতে ২ গ্রাম মাত্রায় ম্যানকোজেব ৮০WP মিশ্রণ করে স্প্রে করুন...",
  },
  {
    title: "আলুর লেট ব্লাইট (নাবি ধসা) রোগ ব্যবস্থাপনা — ফসল সুরক্ষা নির্দেশিকা",
    agency: "CABI",
    snippet: "Phytophthora infestans ছত্রাক দ্বারা সৃষ্ট — আর্দ্র আবহাওয়ায় দ্রুত ছড়ায়...",
  },
  {
    title: "কীটনাশক ব্যবহারের নিরাপদ মাত্রা — সরকারি নির্দেশিকা",
    agency: "DAE",
    snippet: "অনুমোদিত ফরমুলেশন ৮০WP মাত্রায় সতর্কতার সাথে ব্যবহার করুন...",
  },
];

export default function LandingPage() {
  return (
    <div className="space-y-20 py-6 sm:py-10">
      <HeroSection />
      <JudgeNav />
      <CapabilityHub />
      <RagPipelineDemo />
      <VisualStatsSection />
      <ComparisonSection />
      <TimelineSection />
      <AgriDosageCalculatorSection />
      <AudioVoiceAccessibilitySection />
      <WeatherAndHelplineSection />
      <InstitutionalTrustSection />
      <AgriFAQSection />
      <DemoCTA />
    </div>
  );
}

/* === A. Hero === */
function HeroSection() {
  return (
    <motion.section initial="hidden" animate="visible" variants={stagger} className="surface-lift relative mx-auto max-w-6xl overflow-hidden rounded-[24px] border border-ink/10 bg-ink shadow-[0_20px_60px_rgba(26,22,17,0.18)]">
      <div className="grid min-h-[540px] grid-cols-1 lg:grid-cols-[1.05fr_0.95fr]">
        <div className="relative z-10 flex flex-col justify-between px-7 py-9 text-paper sm:px-12 sm:py-12">
          <div>
            <motion.div variants={enter} className="flex flex-wrap items-center gap-2 text-[11px] font-medium text-ochre-soft">
              <span className="h-2 w-2 rounded-full bg-ochre" /> {APP.taglineEn}
              <span className="rounded-full border border-paper/15 px-2 py-0.5 text-paper/65">CAPSTONE DEMO</span>
            </motion.div>
            <motion.h1 variants={enter} className="mt-6 max-w-xl font-display text-4xl leading-[1.18] text-paper sm:text-6xl">
              কৃষকের প্রশ্ন থেকে<br /><span className="text-ochre-soft">বিশ্বাসযোগ্য সিদ্ধান্ত</span>
            </motion.h1>
            <motion.p variants={enter} className="mt-5 max-w-lg text-base leading-relaxed text-paper/70">
              ছবি থেকে রোগের শ্রেণিবিন্যাস, বাংলা প্রশ্নোত্তর এবং উৎস-ভিত্তিক নিরাপত্তা যাচাই — একটি দৃশ্যমান এজেন্টিক কৃষি সহায়তা সিস্টেমে।
            </motion.p>
          </div>
          <motion.div variants={enter} className="mt-10 flex flex-wrap items-center gap-3">
            <Link href="/detect" className="control-press group flex min-h-12 items-center gap-2 rounded-xl bg-leaf-2 px-5 py-3 text-sm font-semibold text-paper shadow-lg shadow-black/10 hover:bg-leaf-3">
              <Camera className="h-4 w-4" /> লাইভ ডেমো শুরু করুন <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Link>
            <Link href="#workflow" className="control-press flex min-h-12 items-center gap-2 rounded-xl border border-paper/20 px-5 py-3 text-sm font-medium text-paper/85 hover:border-paper/50 hover:bg-paper/5">
              <Play className="h-4 w-4" /> কীভাবে কাজ করে
            </Link>
          </motion.div>
          <motion.div variants={enter} className="mt-9 grid max-w-md grid-cols-3 gap-4 border-t border-paper/15 pt-5">
            <HeroMetric value={RESEARCH_STATS.benchmarkInstances} label="মূল্যায়ন ইনস্ট্যান্স" />
            <HeroMetric value={RESEARCH_STATS.knowledgeNodes} label="জ্ঞান নোড" />
            <HeroMetric value={RESEARCH_STATS.dialects} label="উপভাষা" />
          </motion.div>
        </div>
        <div className="relative min-h-[330px] overflow-hidden bg-leaf lg:min-h-full">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/assets/hero_image.jpg"
            alt="বাংলাদেশের কৃষি ক্ষেত"
            className="absolute inset-0 h-full w-full object-cover opacity-70 mix-blend-luminosity"
            onError={(e) => {
              // Graceful fallback on slow 3G / missing asset — never an empty grey box.
              const t = e.currentTarget;
              t.style.display = "none";
              const parent = t.parentElement;
              if (parent && !parent.querySelector("[data-fallback]")) {
                parent.setAttribute("data-fallback", "1");
                parent.style.background =
                  "linear-gradient(135deg, var(--color-leaf) 0%, var(--color-leaf-2) 45%, var(--color-leaf-3) 100%)";
                parent.innerHTML += '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--color-paper);font-family:var(--font-display);font-size:1.25rem;text-align:center;padding:2rem">কৃষি ক্ষেত<br/>বাংলাদেশ</div>';
              }
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-tr from-leaf via-leaf/25 to-transparent" />
          <motion.div variants={enter} className="absolute inset-x-6 bottom-6 rounded-2xl border border-paper/20 bg-ink/75 p-4 shadow-2xl backdrop-blur-sm sm:inset-x-10 sm:bottom-10">
            <div className="flex items-center justify-between text-[10px] font-semibold uppercase tracking-[0.16em] text-paper/55">
              <span>Agent trace</span><span className="text-leaf-3">LIVE SYSTEM</span>
            </div>
            <div className="mt-4 grid grid-cols-4 gap-2">
              {[{ icon: Shield, label: "নিরাপত্তা" }, { icon: Search, label: "তথ্য" }, { icon: PenLine, label: "উত্তর" }, { icon: CheckCircle2, label: "যাচাই" }].map(({ icon: Icon, label }, i) => (
                <div key={label} className="relative text-center">
                  <div className="mx-auto flex h-9 w-9 items-center justify-center rounded-full bg-leaf text-paper ring-4 ring-leaf/20"><Icon className="h-4 w-4" /></div>
                  {i < 3 && <div className="absolute left-[calc(50%+22px)] right-[calc(-50%+13px)] top-4 h-px bg-paper/25" />}
                  <div className="mt-2 text-[10px] text-paper/75">{label}</div>
                </div>
              ))}
            </div>
            <div className="mt-4 rounded-lg bg-paper/10 px-3 py-2 text-xs text-paper/80">প্রতিটি দাবি উৎসে মিলিয়ে তারপর উত্তর দেখানো হয়</div>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}

function HeroMetric({ value, label }: { value: string; label: string }) {
  return <div><div className="font-display text-xl tabular text-paper">{value}</div><div className="mt-1 text-[10px] leading-tight text-paper/50">{label}</div></div>;
}

function JudgeNav() {
  const items = [
    { href: "#experience", label: "পণ্য" },
    { href: "#workflow", label: "এজেন্ট প্রবাহ" },
    { href: "#evidence", label: "গবেষণা প্রমাণ" },
    { href: "#field", label: "মাঠ ও সহায়তা" },
  ];

  return (
    <nav aria-label="প্রকল্পের দ্রুত পর্যবেক্ষণ" className="sticky top-[64px] z-30 mx-auto flex max-w-5xl items-center justify-between gap-3 overflow-x-auto rounded-xl border rule bg-paper/90 px-2 py-2 shadow-sm backdrop-blur-md">
      <span className="hidden shrink-0 px-2 text-[11px] font-semibold text-ink-faint sm:block">প্রকল্পটি দেখুন</span>
      <div className="flex min-w-max items-center gap-1">
        {items.map((item) => (
          <a key={item.href} href={item.href} className="control-press rounded-lg px-3 py-2 text-xs font-medium text-ink-soft hover:bg-paper-2 hover:text-leaf">
            {item.label}
          </a>
        ))}
      </div>
      <Link href="/research" className="hidden shrink-0 items-center gap-1 rounded-lg bg-leaf px-3 py-2 text-xs font-semibold text-paper hover:bg-leaf-2 sm:flex">
        রিসার্চ ব্রিফ <ArrowRight className="h-3.5 w-3.5" />
      </Link>
    </nav>
  );
}

type CapabilityKey = "assistant" | "vision" | "evidence";

const CAPABILITIES = {
  assistant: {
    icon: MessageSquare,
    eyebrow: "USER-FACING AI",
    title: "বাংলায় প্রশ্ন করুন, প্রমাণসহ উত্তর পান",
    body: "কৃষক স্বাভাবিক ভাষায় জিজ্ঞাসা করেন। Safety Agent আগে সিদ্ধান্ত নেয়, তারপর Retrieval, Generation এবং Verifier উত্তরটি সম্পূর্ণ করে।",
    cta: "চ্যাট খুলুন",
    href: "/chat",
    chips: ["বাংলা প্রশ্ন", "ভয়েস ইনপুট", "উৎসসহ উত্তর"],
  },
  vision: {
    icon: ScanLine,
    eyebrow: "MULTIMODAL WORKFLOW",
    title: "পাতার ছবি থেকে রোগের পরামর্শ",
    body: "ফসলের ছবি দিন, মডেল রোগের শ্রেণিবিন্যাস করে, তারপর একই grounded advisory path থেকে চিকিৎসা-তথ্য আনে।",
    cta: "রোগ নির্ণয় করুন",
    href: "/detect",
    chips: ["ছবি আপলোড", "Confidence", "Follow-up"],
  },
  evidence: {
    icon: Network,
    eyebrow: "RESEARCH TO PRODUCT",
    title: "গবেষণা শুধু পেজে নয়, প্রতিটি উত্তরে",
    body: "২৮৪টি সরকারি প্রকাশনা, জ্ঞান নোড, নিরাপত্তা taxonomy এবং audit trail — গবেষণার ফল সরাসরি user workflow-এ কাজ করে।",
    cta: "প্রমাণ দেখুন",
    href: "/research",
    chips: ["Provenance", "১২ safety class", "Audit trail"],
  },
} as const;

function CapabilityHub() {
  const [active, setActive] = useState<CapabilityKey>("assistant");
  const panel = CAPABILITIES[active];
  const Icon = panel.icon;

  return (
    <motion.section id="experience" initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="scroll-mt-32 mx-auto max-w-5xl">
      <motion.div variants={enter} className="mb-5 flex items-end justify-between gap-4">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-ochre">One system, three entry points</p>
          <h2 className="mt-2 font-display text-2xl text-ink sm:text-3xl">এক নজরে পুরো প্রকল্প</h2>
        </div>
        <span className="hidden items-center gap-1.5 text-xs text-ink-faint sm:flex"><BarChart3 className="h-4 w-4 text-leaf" /> user + research + evidence</span>
      </motion.div>
      <motion.div variants={enter} className="overflow-hidden rounded-2xl border rule bg-paper shadow-[0_12px_36px_rgba(52,39,23,0.07)]">
        <div className="grid md:grid-cols-[240px_1fr]">
          <div className="flex gap-1 overflow-x-auto border-b rule bg-paper-2/35 p-2 md:flex-col md:border-b-0 md:border-r md:p-3">
            {(Object.keys(CAPABILITIES) as CapabilityKey[]).map((key) => {
              const item = CAPABILITIES[key];
              const ItemIcon = item.icon;
              return (
                <button key={key} type="button" onClick={() => setActive(key)} className={`control-press flex min-w-[150px] items-center gap-3 rounded-xl px-3 py-3 text-left text-sm md:min-w-0 ${active === key ? "bg-paper text-leaf shadow-sm" : "text-ink-soft hover:bg-paper/60"}`}>
                  <ItemIcon className="h-4 w-4 shrink-0" />
                  <span>{key === "assistant" ? "কৃষি সহকারী" : key === "vision" ? "রোগ বিশ্লেষণ" : "গবেষণা প্রমাণ"}</span>
                </button>
              );
            })}
          </div>
          <AnimatePresence mode="wait">
            <motion.div key={active} initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -8 }} transition={{ duration: dur.fast, ease: ease.smooth }} className="grid gap-6 p-6 sm:p-8 lg:grid-cols-[1fr_220px]">
              <div>
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-leaf/10 text-leaf"><Icon className="h-5 w-5" /></div>
                <p className="mt-5 text-[10px] font-semibold tracking-[0.16em] text-ochre">{panel.eyebrow}</p>
                <h3 className="mt-2 max-w-xl font-display text-2xl leading-snug text-ink">{panel.title}</h3>
                <p className="mt-3 max-w-2xl text-sm leading-relaxed text-ink-soft">{panel.body}</p>
                <div className="mt-5 flex flex-wrap gap-2">{panel.chips.map((chip) => <span key={chip} className="rounded-full border border-leaf/20 bg-leaf/5 px-2.5 py-1 text-[11px] font-medium text-leaf">{chip}</span>)}</div>
                <Link href={panel.href} className="control-press mt-6 inline-flex min-h-11 items-center gap-2 rounded-xl bg-leaf px-4 py-2.5 text-sm font-semibold text-paper hover:bg-leaf-2">{panel.cta}<ArrowRight className="h-4 w-4" /></Link>
              </div>
              <div className="grid content-center gap-2 rounded-xl border rule bg-paper-2/30 p-4">
                {["প্রশ্ন/ছবি গ্রহণ", "এজেন্ট সিদ্ধান্ত", "প্রমাণ ও ফলাফল"].map((label, i) => (
                  <div key={label} className="flex items-center gap-3 rounded-lg bg-paper px-3 py-2.5 text-xs text-ink-soft shadow-sm"><span className="flex h-6 w-6 items-center justify-center rounded-full bg-leaf text-[10px] font-semibold text-paper">{i + 1}</span>{label}</div>
                ))}
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === B. Visual Stats — charts instead of plain numbers === */
function VisualStatsSection() {
  return (
    <motion.section id="evidence" initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="scroll-mt-32 mx-auto max-w-5xl">
      <motion.h2 variants={enter} className="mb-6 text-center font-display text-2xl text-ink">প্রকল্পের পরিসংখ্যান</motion.h2>
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Track distribution pie chart */}
        <motion.div variants={enter} className="rounded-xl border rule bg-paper p-6">
          <h3 className="mb-4 font-display text-sm text-ink">৪ ট্র্যাকে {RESEARCH_STATS.benchmarkInstances} ইনস্ট্যান্স</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={TRACK_DATA} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} innerRadius={40}>
                {TRACK_DATA.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Pie>
              <Tooltip formatter={(v) => Number(v).toLocaleString()} />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-2 grid grid-cols-2 gap-1 text-xs">
            {TRACK_DATA.map((t) => (
              <div key={t.name} className="flex items-center gap-1.5">
                <div className="h-2 w-2 rounded-full" style={{ backgroundColor: t.color }} />
                <span className="text-ink-soft">{t.name}: {t.value.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Retrieval performance bar chart */}
        <motion.div variants={enter} className="rounded-xl border rule bg-paper p-6">
          <h3 className="mb-1 font-display text-sm text-ink">তথ্য সংগ্রহ নির্ভুলতা</h3>
          <p className="mb-4 text-[11px] text-ink-faint">প্রতিটি প্রশ্নের সঠিক উৎস খুঁজে পাওয়ার হার</p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={RETRIEVAL_DATA} layout="vertical" margin={{ left: 10, right: 20 }}>
              <XAxis type="number" domain={[0, 0.6]} hide />
              <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: "var(--color-ink-soft)" }} width={90} />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                {RETRIEVAL_DATA.map((entry, i) => (
                  <Cell key={i} fill={entry.best ? "var(--color-leaf)" : "var(--color-leaf-3)"} />
                ))}
              </Bar>
              <Tooltip formatter={(v) => `${(Number(v) * 100).toFixed(1)}%`} />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-2 flex items-center gap-2 rounded-md bg-leaf/10 px-2.5 py-1.5 text-[11px] text-leaf">
            <CheckCircle2 className="h-3 w-3" />
            <span className="font-medium">মিশ্র পদ্ধতি</span> সবচেয়ে নির্ভুল ফলাফল দিয়েছে
          </div>
        </motion.div>
      </div>

      {/* Key numbers strip */}
      <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
        {[
          { value: RESEARCH_STATS.knowledgeNodes, label: "জ্ঞান নোড" },
          { value: RESEARCH_STATS.publications, label: "সরকারি প্রকাশনা" },
          { value: RESEARCH_STATS.dialects, label: "উপভাষা" },
          { value: RESEARCH_STATS.entities, label: "এনটিটি" },
        ].map((s) => (
          <div key={s.label} className="bg-paper px-4 py-5 text-center">
            <div className="font-display text-2xl tabular text-leaf">{s.value}</div>
            <div className="mt-1 text-[11px] font-medium text-ink-soft">{s.label}</div>
          </div>
        ))}
      </motion.div>
    </motion.section>
  );
}

/* === C. RAG Pipeline Demo — animated, interactive === */
function RagPipelineDemo() {
  const [running, setRunning] = useState(false);
  const [stage, setStage] = useState(0); // 0=idle, 1=safety, 2=retrieval, 3=generation, 4=done
  const [visibleSources, setVisibleSources] = useState(0);

  const run = () => {
    setRunning(true);
    setStage(1);
    setVisibleSources(0);
    setTimeout(() => setStage(2), 800);
    setTimeout(() => setVisibleSources(1), 1000);
    setTimeout(() => setVisibleSources(2), 1300);
    setTimeout(() => setVisibleSources(3), 1600);
    setTimeout(() => setStage(3), 2000);
    setTimeout(() => setStage(4), 3500);
    setTimeout(() => setRunning(false), 4000);
  };

  const traceEvents: RailEvent[] = QA_STAGES.flatMap((item, i) => {
    if (stage > i + 1) return [{ stage: item.key, status: "complete" }];
    if (stage === i + 1 && running) return [{ stage: item.key, status: "active" }];
    if (stage === 4 && i === 3) return [{ stage: item.key, status: "complete" }];
    return [];
  });

  return (
    <motion.section id="workflow" initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="scroll-mt-32 mx-auto max-w-4xl">
      <motion.h2 variants={enter} className="text-center font-display text-2xl text-ink">কীভাবে কাজ করে</motion.h2>
      <motion.p variants={enter} className="mx-auto mt-2 max-w-md text-center text-sm text-ink-soft">
        একটি প্রকৃত প্রশ্ন কীভাবে উত্তর হয় — দেখুন।
      </motion.p>

      {/* Query + run button */}
      <motion.div variants={enter} className="mt-6 rounded-xl border rule bg-paper-2/40 p-4">
        <div className="flex items-center justify-between gap-4">
          <div className="flex-1">
            <div className="text-[10px] font-semibold text-ink-faint">কৃষকের প্রশ্ন</div>
            <div className="mt-1 text-sm font-medium text-ink">{RAG_QUERY}</div>
          </div>
          <button onClick={run} disabled={running} className="flex items-center gap-2 rounded-lg bg-leaf px-5 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-50">
            {running ? <Loader2 className="h-4 w-4 animate-spin" /> : stage === 0 ? <Play className="h-4 w-4" /> : <RotateCcw className="h-4 w-4" />}
            {stage === 0 ? "চালান" : "পুনরায়"}
          </button>
        </div>
      </motion.div>

      <motion.div variants={enter} className="mt-6">
        <AgentTrace stages={QA_STAGES} events={traceEvents} active={running} title="কৃষক চ্যাট এজেন্ট প্রবাহ" detail="একই trace chat ও diagnosis workspace-এ দেখা যায়" />
      </motion.div>

      {/* Results panel */}
      <AnimatePresence>
        {stage >= 1 && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="mt-4 overflow-hidden rounded-xl border rule bg-paper-2/20 p-4">
            {stage >= 1 && (
              <div className="flex items-center gap-2 text-sm">
                <Shield className="h-4 w-4 text-leaf" />
                {(() => {
                  const s = safetyLabel("safe_agri");
                  return (
                    <span className={`rounded-md px-2 py-0.5 text-xs font-medium ${TONE_BADGE[s.tone]}`}>
                      {s.badge}
                    </span>
                  );
                })()}
                <span className="text-ink-soft">{safetyLabel("safe_agri").detail}</span>
              </div>
            )}
            {stage >= 2 && visibleSources > 0 && (
              <div className="mt-3 space-y-1.5">
                <div className="text-xs font-medium text-ink">প্রাসঙ্গিক জ্ঞান নোড ({visibleSources}):</div>
                {RAG_SOURCES.slice(0, visibleSources).map((src, i) => (
                  <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }} className="rounded-md border rule bg-paper px-3 py-2">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-[11px] font-medium text-ink">{src.title}</span>
                      <span className="shrink-0 rounded bg-bone px-1.5 py-0.5 text-[9px] font-semibold text-ink-soft">{src.agency}</span>
                    </div>
                    <p className="mt-0.5 text-[11px] text-ink-soft">{src.snippet}</p>
                  </motion.div>
                ))}
              </div>
            )}
            {stage >= 3 && (
              <div className="mt-3 rounded-md bg-paper p-3">
                <div className="text-xs font-medium text-leaf">উত্তর:</div>
                <p className="mt-1 text-xs leading-relaxed text-ink">আলুর লেট ব্লাইট (নাবি ধসা) একটি ফাঙ্গাসজনিত মারাত্মক রোগ। প্রতি লিটার পানিতে ২ গ্রাম ম্যানকোজেব ৮০WP মিশ্রণ করে স্প্রে করুন। বিস্তারিত জানতে নিকটস্থ কৃষি কর্মকর্তার পরামর্শ নিন।</p>
              </div>
            )}
            {stage >= 4 && (
              <div className="mt-2 flex items-center gap-2 rounded-md bg-leaf/8 px-3 py-1.5 text-xs">
                <CheckCircle2 className="h-3.5 w-3.5 text-leaf" />
                <span className="font-medium text-leaf">যাচাইকৃত</span>
                <span className="text-ink-soft">— সব দাবি উৎসে যাচাইকৃত</span>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.section>
  );
}

/* === D. Comparison === */
function ComparisonSection() {
  const rows = [
    { aspect: "উৎস", chatbot: "ওয়েব থেকে অনুমান", krishok: "২৮৪ সরকারি প্রকাশনা" },
    { aspect: "নিরাপত্তা", chatbot: "নেই", krishok: "১২-শ্রেণী ট্যাক্সোনমি" },
    { aspect: "রাসায়নিক", chatbot: "অনিয়ন্ত্রিত", krishok: "প্রমাণ-অডিটযোগ্য" },
    { aspect: "উপভাষা", chatbot: "শুধু প্রমিত", krishok: "৬ উপভাষা" },
  ];
  const cards = [
    { icon: FileText, title: "প্রমাণ-ভিত্তিক", body: "প্রতিটি উত্তর সরকারি প্রকাশনা থেকে, উৎসসহ।" },
    { icon: Shield, title: "নিরাপত্তা-সচেতন", body: "১২-শ্রেণীর ট্যাক্সোনমি, রাসায়নিক প্রমাণ-অডিট।" },
    { icon: Languages, title: "বহু-উপভাষিক", body: "৬টি আঞ্চলিক উপভাষায়।" },
  ];
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="mx-auto max-w-4xl space-y-6">
      <motion.div variants={enter} className="grid grid-cols-1 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-3">
        {cards.map((c) => (
          <div key={c.title} className="bg-paper p-5">
            <div className="flex h-9 w-9 items-center justify-center rounded-md bg-leaf/10 text-leaf"><c.icon className="h-5 w-5" /></div>
            <h3 className="mt-3 font-display text-base text-ink">{c.title}</h3>
            <p className="mt-1 text-xs text-ink-soft">{c.body}</p>
          </div>
        ))}
      </motion.div>
      <motion.div variants={enter} className="overflow-hidden rounded-xl border rule">
        <table className="w-full text-sm">
          <thead><tr className="bg-paper-2">
            <th className="px-4 py-2.5 text-left font-display text-ink">দিক</th>
            <th className="px-4 py-2.5 text-left font-display text-ink-soft">সাধারণ চ্যাটবট</th>
            <th className="px-4 py-2.5 text-left font-display text-leaf">কৃষক চ্যাট</th>
          </tr></thead>
          <tbody className="divide-y divide-bone">
            {rows.map((r, i) => (
              <tr key={i} className="bg-paper">
                <td className="px-4 py-2.5 font-medium text-ink">{r.aspect}</td>
                <td className="px-4 py-2.5 text-ink-soft">{r.chatbot}</td>
                <td className="px-4 py-2.5 font-medium text-leaf">{r.krishok}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </motion.section>
  );
}

/* === E. Research Timeline === */
function TimelineSection() {
  const milestones = [
    { year: "২০২৪", title: "কর্পাস সংগ্রহ", desc: "২৮৪ সরকারি প্রকাশনা, ১৩ প্রতিষ্ঠান" },
    { year: "২০২৫", title: "জ্ঞান গ্রাফ নির্মাণ", desc: "২,৮৮২ নোড, ১৯,৭৬৮ এনটিটি" },
    { year: "২০২৫", title: "মাঠ সাক্ষাৎকার", desc: "রাজশাহী ও নাটোরে ৩০০ কৃষক" },
    { year: "২০২৬", title: "বেঞ্চমার্ক প্রকাশ", desc: "EACL + SIGIR-AP" },
  ];
  return (
    <motion.section id="field" initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="scroll-mt-32 mx-auto max-w-5xl">
      <motion.div variants={enter} className="mb-6 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-ochre">From fieldwork to product</p>
          <h2 className="mt-2 font-display text-2xl text-ink sm:text-3xl">গবেষণা যেভাবে ব্যবহারযোগ্য সিস্টেম হলো</h2>
        </div>
        <Link href="/team" className="control-press inline-flex min-h-10 items-center gap-1.5 self-start rounded-lg border rule px-3 text-xs font-medium text-ink-soft hover:border-leaf hover:text-leaf">
          মাঠ ও দল দেখুন <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </motion.div>
      <div className="grid overflow-hidden rounded-2xl border rule bg-paper shadow-[0_12px_36px_rgba(52,39,23,0.07)] lg:grid-cols-[1.05fr_0.95fr]">
        <motion.div variants={enter} className="relative min-h-[350px] overflow-hidden bg-leaf">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/assets/researcher_interviewing_farmer.png" alt="মাঠ পর্যায়ে কৃষকের সাক্ষাৎকার" className="absolute inset-0 h-full w-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-ink/80 via-transparent to-transparent" />
          <div className="absolute inset-x-5 bottom-5 text-paper sm:inset-x-7 sm:bottom-7">
            <div className="text-[10px] font-semibold uppercase tracking-[0.18em] text-ochre-soft">Rajshahi + Natore field study</div>
            <div className="mt-2 font-display text-2xl">৩০০ কৃষকের বাস্তব ভাষা ও সমস্যা</div>
            <p className="mt-1 max-w-lg text-xs leading-relaxed text-paper/70">মাঠ সাক্ষাৎকারের প্রশ্ন থেকে farmer-query benchmark, dialect coverage এবং ব্যবহারযোগ্য Bengali interaction তৈরি হয়েছে।</p>
          </div>
        </motion.div>
        <motion.div variants={enter} className="p-6 sm:p-8">
          <div className="space-y-0">
            {milestones.map((m, i) => (
              <motion.div key={i} initial={{ opacity: 0, x: 12 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.08, duration: dur.normal, ease: ease.smooth }} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className={`flex h-9 w-9 items-center justify-center rounded-full font-display text-xs tabular ${i === milestones.length - 1 ? "bg-leaf text-paper" : "border border-leaf/30 bg-leaf/5 text-leaf"}`}>{i + 1}</div>
                  {i < milestones.length - 1 && <div className="my-1 h-10 w-px bg-bone" />}
                </div>
                <div className={`flex-1 ${i < milestones.length - 1 ? "pb-5" : "pb-0"}`}>
                  <div className="flex flex-wrap items-baseline gap-2"><span className="text-[11px] font-semibold text-ochre tabular">{m.year}</span><span className="font-display text-base text-ink">{m.title}</span></div>
                  <p className="mt-1 text-xs leading-relaxed text-ink-soft">{m.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="mt-6 grid grid-cols-3 gap-px overflow-hidden rounded-xl border rule bg-bone">
            {[{ value: RESEARCH_STATS.fieldInterviews, label: "সাক্ষাৎকার" }, { value: RESEARCH_STATS.publications, label: "প্রকাশনা" }, { value: RESEARCH_STATS.institutions, label: "প্রতিষ্ঠান" }].map((stat) => (
              <div key={stat.label} className="bg-paper-2/50 px-2 py-3 text-center"><div className="font-display text-lg tabular text-leaf">{stat.value}</div><div className="text-[9px] text-ink-faint">{stat.label}</div></div>
            ))}
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}

/* === F. Weather === */
/* === G & H. Weather & Helpline Unified Modern Block === */
function WeatherAndHelplineSection() {
  const [district, setDistrict] = useState("");
  const [weather, setWeather] = useState<{ summary_bn: string; advice_bn: string } | null>(null);
  const [weatherLoading, setWeatherLoading] = useState(false);

  const [form, setForm] = useState({ name: "", phone: "", district: "" });
  const [helplineResult, setHelplineResult] = useState<{ status: string; message: string } | null>(null);
  const [helplineLoading, setHelplineLoading] = useState(false);

  const fetchWeather = async () => {
    if (!district.trim()) return;
    setWeatherLoading(true);
    try {
      const r = await getWeather(district.trim());
      setWeather({ summary_bn: r.summary_bn, advice_bn: r.advice_bn });
    } catch {
      setWeather({ summary_bn: "তথ্য পাওয়া যায়নি।", advice_bn: "কৃষক কল সেন্টার: ১৬১২৩।" });
    }
    setWeatherLoading(false);
  };

  const submitHelpline = async () => {
    if (!form.name || !form.phone || !form.district) return;
    setHelplineLoading(true);
    try {
      const r = await registerHelpline({ ...form, crop: null, notes: null });
      setHelplineResult({ status: r.status, message: r.message });
      if (r.status === "ok") setForm({ name: "", phone: "", district: "" });
    } catch {
      setHelplineResult({ status: "error", message: "সমস্যা। কৃষক কল সেন্টার: ১৬১২৩।" });
    }
    setHelplineLoading(false);
  };

  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="mx-auto max-w-5xl">
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {/* Weather Card */}
        <motion.div variants={enter} className="flex flex-col justify-between rounded-2xl border rule bg-paper p-6 sm:p-8 shadow-2xs">
          <div>
            <div className="flex items-center gap-2.5 text-leaf">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-leaf/12">
                <CloudSun className="h-5 w-5" />
              </div>
              <h2 className="font-display text-xl text-ink">আবহাওয়া ও কৃষি বার্তা</h2>
            </div>
            <p className="mt-2 text-xs text-ink-soft">
              আপনার এলাকার স্থানীয় আবহাওয়ার পূর্বাভাস ও জরুরি শস্য সুরক্ষা টিপস দেখুন।
            </p>

            {/* Quick District Chips */}
            <div className="mt-4 flex flex-wrap gap-1.5">
              {AGRI_DISTRICTS.map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => setDistrict(d)}
                  className={`rounded-md border px-2.5 py-1 text-xs font-medium transition-colors ${
                    district === d
                      ? "border-leaf bg-leaf text-paper font-semibold"
                      : "border-rule bg-paper-2/40 text-ink-soft hover:border-leaf/50"
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>

            <div className="mt-4 flex gap-2">
              <div className="relative flex-1">
                <MapPin className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" />
                <input
                  type="text"
                  value={district}
                  onChange={(e) => setDistrict(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && fetchWeather()}
                  placeholder="জেলার নাম লিখুন…"
                  className="w-full rounded-lg border rule bg-paper py-2.5 pl-10 pr-4 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
                />
              </div>
              <button
                type="button"
                onClick={fetchWeather}
                disabled={weatherLoading || !district.trim()}
                className="flex items-center justify-center gap-2 rounded-lg bg-leaf px-4 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-40"
              >
                {weatherLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <CloudSun className="h-4 w-4" />}
              </button>
            </div>

            <AnimatePresence>
              {weather && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="mt-4 overflow-hidden rounded-lg border border-leaf/20 bg-leaf/5 p-4 text-xs">
                  <p className="font-semibold text-leaf">{weather.summary_bn}</p>
                  <div className="mt-2 flex items-start gap-1.5 text-ink-soft">
                    <span className="text-leaf font-bold">↳</span>
                    <span>{weather.advice_bn}</span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* Helpline Registration Card */}
        <motion.div variants={enter} className="flex flex-col justify-between rounded-2xl border rule bg-paper p-6 sm:p-8 shadow-2xs">
          <div>
            <div className="flex items-center justify-between gap-2 border-b rule pb-4">
              <div className="flex items-center gap-2.5 text-leaf">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-leaf/12">
                  <Phone className="h-5 w-5" />
                </div>
                <h2 className="font-display text-xl text-ink">১৬১২৩ হেল্পলাইন সংযোগ</h2>
              </div>
              <a href="tel:16123" className="flex items-center gap-1 rounded-full bg-leaf px-3 py-1 text-xs font-semibold text-paper hover:bg-leaf-2">
                <Phone className="h-3 w-3" /> ডায়াল ১৬১২৩
              </a>
            </div>
            <p className="mt-3 text-xs text-ink-soft">
              কৃষি অফিসারদের কাছ থেকে সরাসরি ফোনে এসএমএস ও সাহায্য পেতে বিনামূল্যে আপনার নম্বর জমা দিন।
            </p>

            <div className="mt-4 space-y-3">
              <div>
                <label className="text-[11px] font-semibold text-ink-faint">আপনার নাম *</label>
                <input
                  type="text"
                  placeholder="যেমন: মোঃ রফিকুল ইসলাম"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="mt-1 w-full rounded-lg border rule bg-paper px-3 py-2 text-xs text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[11px] font-semibold text-ink-faint">মোবাইল নম্বর *</label>
                  <input
                    type="tel"
                    placeholder="01712345678"
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    className="mt-1 w-full rounded-lg border rule bg-paper px-3 py-2 text-xs text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-ink-faint">জেলা *</label>
                  <input
                    type="text"
                    placeholder="যেমন: বগুড়া"
                    value={form.district}
                    onChange={(e) => setForm({ ...form, district: e.target.value })}
                    className="mt-1 w-full rounded-lg border rule bg-paper px-3 py-2 text-xs text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={submitHelpline}
              disabled={helplineLoading || !form.name || !form.phone || !form.district}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg bg-leaf py-2.5 text-xs font-semibold text-paper transition-all hover:bg-leaf-2 disabled:opacity-40"
            >
              {helplineLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
              {helplineLoading ? "জমা হচ্ছে…" : "বিনামূল্যে হেল্পলাইন নিবন্ধন করুন"}
            </button>

            <AnimatePresence>
              {helplineResult && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className={`mt-3 overflow-hidden rounded-lg px-3 py-2 text-xs ${helplineResult.status === "ok" ? "bg-leaf/10 text-leaf" : "bg-clay-soft/20 text-clay"}`}>
                  {helplineResult.message}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}

/* === I. Demo CTA === */
function DemoCTA() {
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="mx-auto max-w-2xl">
      <motion.div variants={enter} className="flex flex-col items-center gap-4 rounded-xl border rule bg-paper px-8 py-10 text-center">
        <h2 className="font-display text-2xl text-ink">এখনই চেষ্টা করুন</h2>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Link href="/detect" className="group flex items-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2">ছবি দিন নির্ণয় করুন<ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" /></Link>
          <Link href="/chat" className="rounded-lg border rule px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-leaf hover:text-leaf">বাংলায় প্রশ্ন করুন</Link>
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === J. Agrochemical Tank & Dosage Calculator Widget === */
function AgriDosageCalculatorSection() {
  const [landUnit, setLandUnit] = useState<"decimal" | "bigha">("decimal");
  const [area, setArea] = useState<number>(33); // 33 decimals default (1 bigha)
  const [pesticide, setPesticide] = useState("mancozeb");

  const PESTICIDES = [
    { id: "mancozeb", name: "ম্যানকোজেব ৮০WP (আলুর নাবি ধসা / ব্লাইট)", dosePerLiter: 2, unit: "গ্রাম" },
    { id: "autostin", name: "অটোস্টিন ৫০WDG (ধানের খোলপোড়া রোগ)", dosePerLiter: 1.5, unit: "গ্রাম" },
    { id: "imidacloprid", name: "ইমিডাক্লোপ্রিড ২০SL (পঁচন ও চোষক পোকা)", dosePerLiter: 0.5, unit: "মি.লি." },
  ];

  const selectedPest = PESTICIDES.find((p) => p.id === pesticide) || PESTICIDES[0];
  const decimalArea = landUnit === "bigha" ? area * 33 : area;
  const totalWaterLiters = Math.max(1, Math.round(decimalArea * 10));
  const totalTanks = Math.ceil(totalWaterLiters / 16);
  const totalChemical = (totalWaterLiters * selectedPest.dosePerLiter).toFixed(1);

  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="mx-auto max-w-4xl">
      <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 sm:p-8 shadow-2xs">
        <div className="flex items-center gap-2.5 text-leaf">
          <Calculator className="h-6 w-6" />
          <h2 className="font-display text-xl text-ink">স্প্রে ট্যাংক পরিকল্পনা সহায়ক</h2>
        </div>
        <p className="mt-1 text-xs text-ink-soft">
          জমির আয়তন ও উদাহরণ নির্বাচন করে ১৬ লিটারের ট্যাংক ও মিশ্রণের আনুমানিক পরিকল্পনা দেখুন। ব্যবহারের আগে পণ্যের লেবেল ও কৃষি কর্মকর্তার পরামর্শ যাচাই করুন।
        </p>

        <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-ink">জমির পরিমাপের একক</label>
              <div className="mt-1.5 flex gap-2">
                <button
                  type="button"
                  onClick={() => setLandUnit("decimal")}
                  className={`flex-1 rounded-lg border py-2 text-xs font-medium transition-colors ${
                    landUnit === "decimal" ? "border-leaf bg-leaf/10 text-leaf" : "border-rule text-ink-soft"
                  }`}
                >
                  শতক (Decimal)
                </button>
                <button
                  type="button"
                  onClick={() => setLandUnit("bigha")}
                  className={`flex-1 rounded-lg border py-2 text-xs font-medium transition-colors ${
                    landUnit === "bigha" ? "border-leaf bg-leaf/10 text-leaf" : "border-rule text-ink-soft"
                  }`}
                >
                  বিঘা (Bigha = ৩৩ শতক)
                </button>
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-ink">
                জমির পরিমাণ ({landUnit === "decimal" ? "শতক" : "বিঘা"})
              </label>
              <input
                type="number"
                min={1}
                max={500}
                value={area}
                onChange={(e) => setArea(Math.max(1, Number(e.target.value)))}
                className="mt-1.5 w-full rounded-lg border rule bg-paper px-4 py-2 text-sm text-ink focus:border-leaf focus:outline-none"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-ink">অনুমোদিত বালাইনাশক নির্বাচন</label>
              <select
                value={pesticide}
                onChange={(e) => setPesticide(e.target.value)}
                className="mt-1.5 w-full rounded-lg border rule bg-paper px-3 py-2 text-xs text-ink focus:border-leaf focus:outline-none"
              >
                {PESTICIDES.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="rounded-xl border border-leaf/20 bg-leaf/5 p-5 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="text-xs font-semibold text-leaf flex items-center justify-between">
                <span>হিসাবকৃত স্প্রে ফর্মুলা:</span>
                <span className="rounded bg-ochre-soft/25 px-2 py-0.5 text-[10px] text-ochre">ডেমো হিসাব</span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-center">
                <div className="rounded-lg bg-paper p-3 border rule">
                  <div className="text-xl font-bold text-leaf">{totalTanks} টি</div>
                  <div className="text-[10px] text-ink-soft mt-0.5">১৬L স্প্রে ট্যাংক লাগবে</div>
                </div>
                <div className="rounded-lg bg-paper p-3 border rule">
                  <div className="text-xl font-bold text-ochre">{totalChemical} {selectedPest.unit}</div>
                  <div className="text-[10px] text-ink-soft mt-0.5">মোট বালাইনাশক প্রয়োজন</div>
                </div>
              </div>

              <div className="text-xs text-ink-soft space-y-1 bg-paper p-3 rounded-lg border rule">
                <p>• প্রতি ১৬L স্প্রে ট্যাংকে মেশাবেন: <strong>{(selectedPest.dosePerLiter * 16).toFixed(1)} {selectedPest.unit}</strong></p>
                <p>• মোট পানির প্রয়োজন: <strong>{totalWaterLiters} লিটার</strong> ({decimalArea} শতক জমির জন্য)</p>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t rule flex items-center justify-between text-[11px] text-ink-faint">
              <span className="flex items-center gap-1 text-clay font-medium">
                ⚠️ মাস্ক ও গ্লাভস পরা বাধ্যতামূলক
              </span>
              <a href="tel:16123" className="text-leaf font-semibold hover:underline">
                পরামর্শে ১৬১২৩ ➔
              </a>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === K. Regional Voice & Dialect Accessibility Section === */
function AudioVoiceAccessibilitySection() {
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="mx-auto max-w-4xl">
      <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2.5 text-leaf">
          <Volume2 className="h-6 w-6" />
          <h2 className="font-display text-xl text-ink">ভয়েস অ্যাসিস্ট্যান্ট ও আঞ্চলিক উপভাষা সহায়তা</h2>
        </div>
        <p className="mt-1 text-xs text-ink-soft">
          কম শিক্ষিত প্রান্তিক কৃষকদের সুবিধার্থে বাংলায় ভয়েস রিডার এবং ৫টি প্রধান আঞ্চলিক উপভাষায় উত্তর শোনার ব্যবস্থা।
        </p>

        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="rounded-xl border rule bg-paper-2/40 p-4">
            <div className="flex items-center gap-2 text-leaf font-semibold text-sm">
              <Volume2 className="h-4 w-4" />
              <span>বাংলা অডিও রিডার</span>
            </div>
            <p className="mt-2 text-xs leading-relaxed text-ink-soft">
              যেকোনো এআই উত্তর এক ক্লিকেই বাংলায় পরিষ্কার অডিওতে শুনে নিতে পারেন।
            </p>
          </div>

          <div className="rounded-xl border rule bg-paper-2/40 p-4">
            <div className="flex items-center gap-2 text-ochre font-semibold text-sm">
              <Sparkles className="h-4 w-4" />
              <span>আঞ্চলিক উপভাষা</span>
            </div>
            <p className="mt-2 text-xs leading-relaxed text-ink-soft">
              নোয়াখালী, চাটগাঁইয়া, সিলেটি, রাজশাহী ও রংপুরের স্থানীয় উপভাষায় অনুবাদ।
            </p>
          </div>

          <div className="rounded-xl border rule bg-paper-2/40 p-4">
            <div className="flex items-center gap-2 text-clay font-semibold text-sm">
              <Phone className="h-4 w-4" />
              <span>১৬১২৩ সরাসরি রিডাইরেক্ট</span>
            </div>
            <p className="mt-2 text-xs leading-relaxed text-ink-soft">
              জরুরি কীটনাশক বা রাসায়নিক ডোজ সংশয়ে বিনামূল্যে সরকারি কল সেন্টারে ডায়াল করার সুবিধা।
            </p>
          </div>
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === L. Institutional Trust & Compliance Section === */
function InstitutionalTrustSection() {
  const INSTITUTES = [
    { code: "DAE", name: "কৃষি সম্প্রসারণ অধিদপ্তর", role: "জাতীয় বালাই গাইডলাইন" },
    { code: "BARC", name: "বাংলাদেশ কৃষি গবেষণা কাউন্সিল", role: "সয়েল ও ফার্টিলাইজার গাইড" },
    { code: "BARI", name: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট", role: "সবজি ও মসলা প্রযুক্তি" },
    { code: "BRRI", name: "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট", role: "ধানের বালাই তথ্যভাণ্ডার" },
    { code: "SRDI", name: "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট", role: "মাটির পিএইচ ও উপাদান" },
  ];

  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="mx-auto max-w-4xl">
      <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 text-center">
        <h2 className="font-display text-lg text-ink flex items-center justify-center gap-2">
          <Building2 className="h-5 w-5 text-leaf" />
          সরকারি ও ইনস্টিটিউশনাল তথ্যসূত্র সংযোগ
        </h2>
        <p className="mt-1 text-xs text-ink-faint">
          আমাদের RAG তথ্যভাণ্ডার সরাসরি জাতীয় নিবন্ধিত কৃষি গবেষণা সংস্থাগুলোর সাথে যুক্ত
        </p>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-5">
          {INSTITUTES.map((inst) => (
            <div key={inst.code} className="rounded-xl border rule bg-paper-2/30 p-3 text-center transition-all hover:border-leaf/30">
              <div className="font-display text-sm font-bold text-leaf">{inst.code}</div>
              <div className="mt-1 text-[11px] font-medium text-ink truncate">{inst.name}</div>
              <div className="mt-0.5 text-[9px] text-ink-faint">{inst.role}</div>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.section>
  );
}

/* === M. Agri FAQ Section === */
function AgriFAQSection() {
  const [openIdx, setOpenIdx] = useState<number | null>(0);

  const FAQS = [
    {
      q: "কৃষক চ্যাট এআই এর পরামর্শ কতটা নির্ভুল ও নিরাপদ?",
      a: "আমাদের সিস্টেমটি ৪-ধাপের মাল্টি-এজেন্ট সিকিউরিটি পাইপলাইন অনুসরণ করে। প্রতিটি পরামর্শ দেওয়ার আগে সরকারি DAE, BARC ও BRRI নির্দেশিকা থেকে রিট্রিভাল করা হয় এবং রাসায়নিকের মাত্রা Verifier Agent দ্বারা যাচাই করা হয়।",
    },
    {
      q: "ছবি তুলে ফসলের রোগ কিভাবে নির্ণয় করব?",
      a: "'রোগ নির্ণয়' পেজে গিয়ে আক্রান্ত পাতার পরিষ্কার ছবি তুলুন বা আপলোড করুন। বর্তমান Ultralytics মডেল ফসল ও রোগের শ্রেণিবিন্যাস করে; এরপর grounded advisory pipeline উৎস-ভিত্তিক পরামর্শ দেখায়।",
    },
    {
      q: "আঞ্চলিক উপভাষায় কিভাবে উত্তর পাওয়া যায়?",
      a: "গবেষণা ডেটাসেটে নোয়াখালী, চাটগাঁইয়া, সিলেটি, রাজশাহী ও রংপুরসহ উপভাষার উদাহরণ আছে। বর্তমান ডেমোতে বাংলা লেখা, ভয়েস ইনপুট ও উত্তর শোনার সুবিধা রয়েছে; আলাদা উপভাষা নির্বাচন ভবিষ্যৎ UI কাজ।",
    },
    {
      q: "ইন্টারনেট বা প্রযুক্তি না জানা কৃষক কিভাবে সাহায্য পাবেন?",
      a: "যেকোনো জরুরি প্রয়োজনে সরাসরি বিনামূল্যে কৃষক কল সেন্টার ১৬১২৩ নম্বরে ডায়াল করে বিশেষজ্ঞ কৃষি কর্মকর্তার সাথে কথা বলা যাবে।",
    },
  ];

  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="mx-auto max-w-3xl">
      <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 sm:p-8">
        <div className="flex items-center gap-2 text-leaf mb-6">
          <HelpCircle className="h-6 w-6" />
          <h2 className="font-display text-xl text-ink">সাধারণ জিজ্ঞাসা (FAQ)</h2>
        </div>

        <div className="space-y-3">
          {FAQS.map((faq, idx) => {
            const isOpen = openIdx === idx;
            return (
              <div key={idx} className="rounded-xl border rule bg-paper overflow-hidden">
                <button
                  type="button"
                  onClick={() => setOpenIdx(isOpen ? null : idx)}
                  className="w-full flex items-center justify-between p-4 text-left font-medium text-sm text-ink hover:text-leaf transition-colors"
                >
                  <span>{faq.q}</span>
                  <ChevronDown className={`h-4 w-4 shrink-0 transition-transform ${isOpen ? "rotate-180 text-leaf" : "text-ink-faint"}`} />
                </button>
                <AnimatePresence>
                  {isOpen && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="px-4 pb-4 text-xs leading-relaxed text-ink-soft border-t rule pt-3 bg-paper-2/30"
                    >
                      {faq.a}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </motion.div>
    </motion.section>
  );
}
