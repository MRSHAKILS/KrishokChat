"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import {
  ArrowRight, Shield, FileText, Languages, CloudSun, Phone,
  CheckCircle2, Loader2, MapPin, Play, Search, PenLine, RotateCcw,
} from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
  PieChart, Pie,
} from "recharts";
import { APP, RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { getWeather, registerHelpline } from "@/lib/api";

/* =========================================================================
   Landing Page — modern, visual, multi-section.
   Team + fieldwork visible directly. Charts instead of plain numbers.
   RAG pipeline animated demo. Weather + helpline.
   ========================================================================= */

const TRACK_DATA = [
  { name: "সাধারণ QA", value: 28993, color: "var(--color-leaf)" },
  { name: "টেবিল QA", value: 25650, color: "var(--color-leaf-2)" },
  { name: "নিরাপত্তা QA", value: 20112, color: "var(--color-ochre)" },
  { name: "চিকিৎসা QA", value: 11224, color: "var(--color-clay)" },
];

const RETRIEVAL_DATA = [
  { name: "Hybrid RRF", value: 0.539 },
  { name: "BM25", value: 0.506 },
  { name: "Dense", value: 0.464 },
  { name: "ColBERT", value: 0.487 },
];

const RAG_QUERY = "আলুর দেরি ব্লাইট কীভাবে প্রতিরোধ করব?";
const RAG_SOURCES = [
  { id: "DAE_PEST_1206A0_001", score: 33.23, snippet: "প্রতি লিটার পানিতে ২ গ্রাম মাত্রায় Mancozeb 80WP..." },
  { id: "CABI_POTATO_834B4F_001", score: 32.59, snippet: "Phytophthora infestans ছত্রাক দ্বারা সৃষ্ট..." },
  { id: "DAE_PEST_B3531E_001", score: 31.08, snippet: "অধিকাংশ প্যান্ডি 80WP ফরমুলেশন..." },
];

export default function LandingPage() {
  return (
    <div className="space-y-20 py-10">
      <HeroSection />
      <VisualStatsSection />
      <RagPipelineDemo />
      <ComparisonSection />
      <TimelineSection />
      <WeatherSection />
      <HelplineFormSection />
      <DemoCTA />
    </div>
  );
}

/* === A. Hero === */
function HeroSection() {
  return (
    <motion.section initial="hidden" animate="visible" variants={stagger} className="mx-auto max-w-5xl overflow-hidden rounded-2xl border rule">
      <div className="grid grid-cols-1 lg:grid-cols-2">
        <div className="bg-paper px-8 py-12 sm:px-12 sm:py-16">
          <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">{APP.taglineEn}</motion.p>
          <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink sm:text-5xl">
            বাংলাদেশের কৃষকের জন্য<br /><span className="text-leaf">নিরাপদ কৃষি পরামর্শ</span>
          </motion.h1>
          <motion.p variants={enter} className="mt-5 max-w-md text-base leading-relaxed text-ink-soft">
            ফসলের ছবি থেকে রোগ শনাক্ত করুন, বাংলায় পরামর্শ নিন — প্রতিটি উত্তর নিরাপত্তা যাচাই, তথ্য সংগ্রহ, উত্তর তৈরি ও যাচাইকরণের ধাপ দিয়ে আসে।
          </motion.p>
          <motion.div variants={enter} className="mt-8 flex flex-wrap items-center gap-3">
            <Link href="/detect" className="group flex items-center gap-2 rounded-lg bg-leaf px-7 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2">
              শুরু করুন<ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Link>
            <Link href="/chat" className="rounded-lg border rule px-7 py-3 text-sm font-medium text-ink transition-colors hover:border-leaf hover:text-leaf">প্রশ্ন করুন</Link>
          </motion.div>
        </div>
        <div className="relative min-h-[280px] bg-paper-2 lg:min-h-full">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/assets/hero_image.jpg" alt="বাংলাদেশের কৃষি ক্ষেত" className="absolute inset-0 h-full w-full object-cover" />
        </div>
      </div>
    </motion.section>
  );
}

/* === B. Visual Stats — charts instead of plain numbers === */
function VisualStatsSection() {
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-60px" }} variants={stagger} className="mx-auto max-w-5xl">
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
          <h3 className="mb-4 font-display text-sm text-ink">তথ্য সংগ্রহ নির্ভুলতা (R@10)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={RETRIEVAL_DATA} layout="vertical" margin={{ left: 10, right: 20 }}>
              <XAxis type="number" domain={[0, 0.6]} hide />
              <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: "var(--color-ink-soft)" }} width={70} />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                {RETRIEVAL_DATA.map((_, i) => <Cell key={i} fill="var(--color-leaf)" />)}
              </Bar>
              <Tooltip formatter={(v) => Number(v).toFixed(3)} />
            </BarChart>
          </ResponsiveContainer>
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
            <div className="mt-1 text-[11px] uppercase tracking-[0.12em] text-ink-soft">{s.label}</div>
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

  const stages = [
    { label: "নিরাপত্তা", icon: Shield },
    { label: "তথ্য সংগ্রহ", icon: Search },
    { label: "উত্তর তৈরি", icon: PenLine },
    { label: "যাচাই", icon: CheckCircle2 },
  ];

  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="mx-auto max-w-4xl">
      <motion.h2 variants={enter} className="text-center font-display text-2xl text-ink">কীভাবে কাজ করে</motion.h2>
      <motion.p variants={enter} className="mx-auto mt-2 max-w-md text-center text-sm text-ink-soft">
        একটি প্রকৃত প্রশ্ন কীভাবে উত্তর হয় — দেখুন।
      </motion.p>

      {/* Query + run button */}
      <motion.div variants={enter} className="mt-6 rounded-xl border rule bg-paper-2/40 p-4">
        <div className="flex items-center justify-between gap-4">
          <div className="flex-1">
            <div className="text-[10px] uppercase tracking-[0.14em] text-ink-faint">কৃষকের প্রশ্ন</div>
            <div className="mt-1 text-sm font-medium text-ink">{RAG_QUERY}</div>
          </div>
          <button onClick={run} disabled={running} className="flex items-center gap-2 rounded-lg bg-leaf px-5 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-50">
            {running ? <Loader2 className="h-4 w-4 animate-spin" /> : stage === 0 ? <Play className="h-4 w-4" /> : <RotateCcw className="h-4 w-4" />}
            {stage === 0 ? "চালান" : "পুনরায়"}
          </button>
        </div>
      </motion.div>

      {/* Pipeline stages */}
      <motion.div variants={enter} className="mt-6 flex items-center justify-between gap-1">
        {stages.map((s, i) => {
          const active = stage > i;
          const current = stage === i + 1;
          return (
            <div key={s.label} className="flex flex-1 flex-col items-center">
              <motion.div
                animate={{ scale: current ? 1.1 : 1, backgroundColor: active || current ? "var(--color-leaf)" : "var(--color-paper)" }}
                className="flex h-11 w-11 items-center justify-center rounded-full border-2"
                style={{ borderColor: active || current ? "var(--color-leaf)" : "var(--color-bone)", color: active || current ? "var(--color-paper)" : "var(--color-ink-faint)" }}
              >
                <s.icon className="h-5 w-5" />
              </motion.div>
              <div className={`mt-2 text-xs ${active || current ? "text-ink" : "text-ink-faint"}`}>{s.label}</div>
              {i < stages.length - 1 && <div className="mt-1 h-6 w-px" style={{ backgroundColor: stage > i + 1 ? "var(--color-leaf)" : "var(--color-bone)" }} />}
            </div>
          );
        })}
      </motion.div>

      {/* Results panel */}
      <AnimatePresence>
        {stage >= 1 && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="mt-4 overflow-hidden rounded-xl border rule bg-paper-2/20 p-4">
            {stage >= 1 && (
              <div className="flex items-center gap-2 text-sm">
                <Shield className="h-4 w-4 text-leaf" />
                <span className="rounded-md bg-leaf/10 px-2 py-0.5 text-xs text-leaf">safe_agri</span>
                <span className="text-ink-faint">→ নিরাপদ, তথ্য সংগ্রহে যান</span>
              </div>
            )}
            {stage >= 2 && visibleSources > 0 && (
              <div className="mt-3 space-y-1.5">
                <div className="text-xs font-medium text-ink">জ্ঞান নোড ({visibleSources}):</div>
                {RAG_SOURCES.slice(0, visibleSources).map((src, i) => (
                  <motion.div key={src.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }} className="rounded-md border rule bg-paper px-3 py-2">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[10px] text-ink">{src.id}</span>
                      <span className="font-mono text-[10px] text-leaf">score: {src.score}</span>
                    </div>
                    <p className="mt-0.5 text-[11px] text-ink-soft">{src.snippet}</p>
                  </motion.div>
                ))}
              </div>
            )}
            {stage >= 3 && (
              <div className="mt-3 rounded-md bg-paper p-3">
                <div className="text-xs font-medium text-leaf">উত্তর (Gemma-4):</div>
                <p className="mt-1 text-xs leading-relaxed text-ink">আলুর দেরি ব্লাইট একটি ছত্রাকজনিত রোগ। প্রতি লিটার পানিতে ২ গ্রাম Mancozeb 80WP মিশ্রণ করে স্প্রে করুন [DAE_PEST_1206A0_001]।</p>
              </div>
            )}
            {stage >= 4 && (
              <div className="mt-2 flex items-center gap-2 rounded-md bg-leaf/8 px-3 py-1.5 text-xs">
                <CheckCircle2 className="h-3.5 w-3.5 text-leaf" />
                <span className="text-leaf">verified</span>
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
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="mx-auto max-w-4xl">
      <motion.h2 variants={enter} className="text-center font-display text-2xl text-ink">আমাদের যাত্রা</motion.h2>
      <motion.div variants={enter} className="mt-8 space-y-0">
        {milestones.map((m, i) => (
          <motion.div key={i} initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.15, duration: dur.normal, ease: ease.smooth }} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className={`flex h-10 w-10 items-center justify-center rounded-full font-display text-xs tabular ${i === milestones.length - 1 ? "bg-leaf text-paper" : "border-2 border-leaf bg-paper text-leaf"}`}>{i + 1}</div>
              {i < milestones.length - 1 && <div className="my-1 h-10 w-px bg-bone" />}
            </div>
            <div className={`flex-1 ${i < milestones.length - 1 ? "pb-6" : "pb-0"}`}>
              <div className="flex items-baseline gap-3">
                <span className="font-display text-sm text-ochre tabular">{m.year}</span>
                <span className="font-display text-base text-ink">{m.title}</span>
              </div>
              <p className="mt-1 text-sm text-ink-soft">{m.desc}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </motion.section>
  );
}

/* === F. Weather === */
function WeatherSection() {
  const [district, setDistrict] = useState("");
  const [weather, setWeather] = useState<{ summary_bn: string; advice_bn: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const fetchWeather = async () => {
    if (!district.trim()) return;
    setLoading(true);
    try {
      const r = await getWeather(district.trim());
      setWeather({ summary_bn: r.summary_bn, advice_bn: r.advice_bn });
    } catch { setWeather({ summary_bn: "তথ্য পাওয়া যায়নি।", advice_bn: "কৃষক কল সেন্টার: ১৬১২৩।" }); }
    setLoading(false);
  };
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="mx-auto max-w-2xl">
      <motion.div variants={enter} className="rounded-xl border rule bg-paper-2/30 p-6">
        <div className="flex items-center gap-2 text-leaf"><CloudSun className="h-5 w-5" /><h2 className="font-display text-lg text-ink">আবহাওয়া ও পরামর্শ</h2></div>
        <p className="mt-2 text-sm text-ink-soft">আপনার জেলার নাম লিখুন।</p>
        <div className="mt-4 flex gap-2">
          <div className="relative flex-1"><MapPin className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" />
            <input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} onKeyDown={(e) => e.key === "Enter" && fetchWeather()} placeholder="জেলার নাম" className="w-full rounded-lg border rule bg-paper py-2.5 pl-10 pr-4 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none" />
          </div>
          <button onClick={fetchWeather} disabled={loading || !district.trim()} className="flex items-center gap-2 rounded-lg bg-leaf px-5 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-40">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <CloudSun className="h-4 w-4" />}
          </button>
        </div>
        <AnimatePresence>{weather && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="mt-4 overflow-hidden rounded-lg border rule bg-paper p-4">
            <p className="text-sm text-ink">{weather.summary_bn}</p>
            <div className="mt-2 flex items-start gap-2 rounded-md bg-leaf/8 px-3 py-2 text-sm text-ink"><span className="text-leaf">↳</span><span>{weather.advice_bn}</span></div>
          </motion.div>
        )}</AnimatePresence>
      </motion.div>
    </motion.section>
  );
}

/* === H. Helpline Form === */
function HelplineFormSection() {
  const [form, setForm] = useState({ name: "", phone: "", district: "" });
  const [result, setResult] = useState<{ status: string; message: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const submit = async () => {
    if (!form.name || !form.phone || !form.district) return;
    setLoading(true);
    try {
      const r = await registerHelpline({ ...form, crop: null, notes: null });
      setResult({ status: r.status, message: r.message });
      if (r.status === "ok") setForm({ name: "", phone: "", district: "" });
    } catch { setResult({ status: "error", message: "সমস্যা। কৃষক কল সেন্টার: ১৬১২৩।" }); }
    setLoading(false);
  };
  return (
    <motion.section initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-80px" }} variants={stagger} className="mx-auto max-w-2xl">
      <motion.div variants={enter} className="rounded-xl border rule bg-paper-2/30 p-6">
        <div className="flex items-center gap-2 text-leaf"><Phone className="h-5 w-5" /><h2 className="font-display text-lg text-ink">হেল্পলাইন নিবন্ধন</h2></div>
        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
          <input type="text" placeholder="নাম *" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="rounded-lg border rule bg-paper px-4 py-2.5 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none" />
          <input type="tel" placeholder="ফোন *" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} className="rounded-lg border rule bg-paper px-4 py-2.5 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none" />
          <input type="text" placeholder="জেলা *" value={form.district} onChange={(e) => setForm({ ...form, district: e.target.value })} className="rounded-lg border rule bg-paper px-4 py-2.5 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none" />
        </div>
        <button onClick={submit} disabled={loading || !form.name || !form.phone || !form.district} className="mt-4 flex items-center gap-2 rounded-lg bg-leaf px-6 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-40">
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
          {loading ? "…" : "নিবন্ধন"}
        </button>
        <AnimatePresence>{result && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className={`mt-4 overflow-hidden rounded-lg px-4 py-3 text-sm ${result.status === "ok" ? "bg-leaf/10 text-leaf" : "bg-clay-soft/20 text-clay"}`}>{result.message}</motion.div>
        )}</AnimatePresence>
      </motion.div>
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
