"use client";

import { useState, useRef } from "react";
import dynamic from "next/dynamic";
import { motion, useInView } from "motion/react";
import { TrendingUp, AlertTriangle, Globe, ShieldCheck, Hourglass } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, LabelList } from "recharts";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { useCountUp, toBn } from "@/lib/use-count-up";
import goldenStats from "@/lib/golden_stats.json";

/* The inspector is a 1,200+ line interactive component — lazy-loaded so it
   stays out of this page's first-load bundle. */
const ModelComparisonInspector = dynamic(
  () => import("@/components/model-comparison-inspector").then((m) => m.ModelComparisonInspector),
  {
    ssr: false,
    loading: () => (
      <div className="min-h-96 animate-pulse rounded-xl border rule bg-paper-2/30" aria-hidden />
    ),
  },
);

/* =========================================================================
   Benchmark Results Page — the credibility page with actual paper numbers.
   Tables + charts, all from the two papers. No fabrication.

   Sections:
   A. Main results table (KrishokChat RQ1/RQ2)
   B. Retrieval results (AgriTrust)
   C. Register gap discovery (bimodal dense retrieval)
   D. Cross-lingual collapse
   E. Farmer benchmark
   F. Hallucination floor
   G. Live-system golden eval (precomputed artifact, pending human scores)
   ========================================================================= */

type Condition = "cb" | "oracle";

const MAIN_RESULTS = [
  { model: "Gemini-2.5-FL", genF1_cb: 0.104, genHal_cb: 37.15, trtCor_cb: 43.64, trtHal_cb: 15.90, genF1_or: 0.281, genHal_or: 32.40, trtCor_or: 51.73, trtHal_or: 4.91 },
  { model: "Gemma-4-26B", genF1_cb: 0.087, genHal_cb: 32.12, trtCor_cb: 38.73, trtHal_cb: 9.83, genF1_or: 0.253, genHal_or: 29.05, trtCor_or: 54.05, trtHal_or: 4.05 },
  { model: "LLaMA-3.1-8B", genF1_cb: 0.165, genHal_cb: 10.06, trtCor_cb: 12.43, trtHal_cb: 1.73, genF1_or: 0.230, genHal_or: 16.48, trtCor_or: 30.64, trtHal_or: 5.49 },
  { model: "Qwen-2.5-7B", genF1_cb: 0.136, genHal_cb: 11.17, trtCor_cb: 13.29, trtHal_cb: 2.02, genF1_or: 0.198, genHal_or: 20.54, trtCor_or: 41.33, trtHal_or: 4.62 },
  { model: "GPT-OSS-120B", genF1_cb: 0.113, genHal_cb: 36.20, trtCor_cb: 32.92, trtHal_cb: 9.47, genF1_or: 0.191, genHal_or: 30.00, trtCor_or: 49.79, trtHal_or: 7.00 },
  { model: "KrishokChat-4B (SFT)", sft: true, genF1_cb: 0.314, genHal_cb: 19.83, trtCor_cb: 35.55, trtHal_cb: 8.96, genF1_or: 0.300, genHal_or: 19.83, trtCor_or: 34.97, trtHal_or: 6.07 },
];

const RETRIEVAL_RESULTS = [
  { arch: "Hybrid RRF (Gemini+BM25)", r1: 0.291, r5: 0.466, r10: 0.539, mrr: 0.551, best: true },
  { arch: "BM25 (Sparse)", r1: 0.205, r5: 0.405, r10: 0.506, mrr: 0.481, bestSingle: true },
  { arch: "Dense (Gemini-001)", r1: 0.320, r5: 0.431, r10: 0.464, mrr: 0.514 },
  { arch: "Dense (BGE-M3 Native)", r1: 0.281, r5: 0.369, r10: 0.408, mrr: 0.432 },
  { arch: "ColBERT (BGE-M3)", r1: 0.255, r5: 0.414, r10: 0.487, mrr: 0.324 },
];

const REGISTER_GAP = [
  { category: "ফার্মার (colloquial)", dense: 0.093, bm25: 0.523, color: "clay" },
  { category: "নিরাপত্তা (formal)", dense: 0.970, bm25: 0.539, color: "leaf" },
  { category: "KG-grounded", dense: 0.489, bm25: 0.478, color: "ochre" },
];

const CROSS_LINGUAL = [
  { setting: "BN→BN", dense: 0.464, bm25: 0.506, winner: "BM25" },
  { setting: "EN→BN (cross-lingual)", dense: 0.425, bm25: 0.004, winner: "Dense" },
  { setting: "EN→EN", dense: 0.442, bm25: 0.384, winner: "Dense" },
];

const FARMER_RESULTS = [
  { model: "Gemini-2.5-FL", f1: 0.2196, hal: 38.29, best: true },
  { model: "Gemma-4-26B", f1: 0.1375, hal: 23.14 },
  { model: "KrishokChat-4B (SFT)", f1: 0.1170, hal: 41.14 },
  { model: "Qwen-2.5-7B", f1: 0.0841, hal: 14.29 },
  { model: "LLaMA-3.1-8B", f1: 0.0078, hal: 1.71 },
  { model: "GPT-OSS-120B", f1: 0.0002, hal: 14.57 },
];

/* Chart labels — display-only shortening of real model names (full names in tables) */
const GENF1_LABELS: Record<string, string> = {
  "Gemini-2.5-FL": "Gemini-2.5-FL",
  "Gemma-4-26B": "Gemma-4",
  "LLaMA-3.1-8B": "LLaMA-3.1",
  "Qwen-2.5-7B": "Qwen-2.5",
  "GPT-OSS-120B": "GPT-OSS",
  "KrishokChat-4B (SFT)": "KrishokChat-4B",
};

/* Section kickers — indexed structure, same system as /data */
const KICKERS = ["০১ · মূল ফলাফল", "০২ · তথ্য সংগ্রহ", "০৩ · রেজিস্টার গ্যাপ", "০৪ · ক্রস-লিঙ্গুয়াল", "০৫ · ফার্মার বেঞ্চমার্ক", "০৬ · হ্যালুসিনেশন ফ্লোর ও মডেল তুলনা", "০৭ · গোল্ডেন ইভাল"] as const;

/* Section G — live-system golden eval. Numbers come from the PRECOMPUTED
   artifact generated offline (scripts/08..11 in backend/ml_assets/rag_index/
   scripts). Never computed live. Before the two evaluators fill the scoring
   sheet, the artifact honestly reports status: pending_scores. */
type CategoryStats = { n: number; refused: number; verified: number };
type GoldenStats = {
  status: "scored" | "pending_scores" | "not_built";
  items: number;
  evaluators: number;
  source: string;
  note?: string;
  mechanical: {
    per_category: Record<string, CategoryStats>;
    unanswerable_refusal_rate: number | null;
    note: string;
  };
  kappa?: number;
  raw_agreement?: number;
  category_results?: Record<string, { n: number; correct: number; partial: number; unsupported: number; refused: number; correct_rate: number; acceptable_rate: number }>;
  unanswerable_refusal_rate_mechanical?: number | null;
  unanswerable_refusal_rate_validated?: number | null;
  disagreements?: { row_id: string; e1: string; e2: string }[];
  disagreement_count?: number;
};
const STATS = goldenStats as GoldenStats;

const CATEGORY_BN: Record<string, string> = {
  dosage: "ডোজ",
  timing: "সময়",
  pest_disease: "রোগ / পোকা",
  general: "সাধারণ",
  off_topic: "অপ্রাসঙ্গিক",
  unanswerable: "উত্তরযোগ্য নয়",
};
const CATEGORY_ORDER = ["dosage", "timing", "pest_disease", "general", "off_topic", "unanswerable"];

const SCORE_BN: Record<string, string> = {
  correct: "সঠিক",
  partial: "আংশিক",
  unsupported: "অসমর্থিত",
  refused: "অস্বীকৃত",
};

function StatCell({ value, label, delay }: { value: number; label: string; delay: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const n = useCountUp(value, inView);
  return (
    <motion.div ref={ref} variants={enter} transition={{ delay }} className="bg-paper p-5 text-center">
      <div className="font-display text-3xl tabular text-ink">{toBn(n)}</div>
      <div className="mt-1 text-[10px] font-medium text-ink-faint">{label}</div>
    </motion.div>
  );
}

export default function BenchmarkPage() {
  const [condition, setCondition] = useState<Condition>("cb");

  return (
    <div className="mx-auto max-w-6xl space-y-12 py-14">
      {/* === Hero === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="text-center"
      >
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          BENCHMARK RESULTS
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-3xl leading-tight text-ink md:text-4xl">
          মূল্যায়ন <span className="text-leaf">ফলাফল</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          ৬টি মডেল, ৫টি তথ্য-সংগ্রহ আর্কিটেকচার, ৯০০টি কোয়েরি — সব সংখ্যা গবেষণাপত্র থেকে, কোনো তথ্য তৈরি নয়।
        </motion.p>
      </motion.section>

      {/* Stat strip — real counts, count-up */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
          {[
            { value: 6, label: "মডেল" },
            { value: 5, label: "তথ্য-সংগ্রহ আর্কিটেকচার" },
            { value: 900, label: "মূল্যায়ন কোয়েরি" },
            { value: 284, label: "সোর্স PDF" },
          ].map((s, i) => (
            <StatCell key={s.label} value={s.value} label={s.label} delay={i * 0.04} />
          ))}
        </motion.div>
      </motion.section>

      {/* === A. Main Results Table === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[0]}</motion.div>
        <motion.h2 variants={enter} className="mt-1 mb-3 font-display text-2xl text-ink">
          মূল ফলাফল — General & Treatment QA
        </motion.h2>
        <motion.p variants={enter} className="mb-4 text-sm text-ink-soft">
          ৫টি জিরো-শট বেসলাইন + ১টি ফাইন-টিউনড মডেল।
        </motion.p>

        {/* Condition toggle */}
        <motion.div variants={enter} className="mb-4 inline-flex rounded-lg border rule bg-paper p-1">
          <button
            onClick={() => setCondition("cb")}
            className={`rounded-md px-4 py-1.5 text-xs font-medium transition-colors ${
              condition === "cb" ? "bg-leaf text-paper" : "text-ink-soft hover:text-ink"
            }`}
          >
            Closed-Book
          </button>
          <button
            onClick={() => setCondition("oracle")}
            className={`rounded-md px-4 py-1.5 text-xs font-medium transition-colors ${
              condition === "oracle" ? "bg-leaf text-paper" : "text-ink-soft hover:text-ink"
            }`}
          >
            Oracle
          </button>
        </motion.div>

        {/* Chart + table — side by side on lg */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <motion.div variants={enter} className="rounded-xl border rule bg-paper p-6">
          <div className="mb-2 text-xs font-semibold text-ochre">GenF1 তুলনা — {condition === "cb" ? "Closed-Book" : "Oracle"}</div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart
              data={MAIN_RESULTS.map((m) => ({
                name: GENF1_LABELS[m.model] ?? m.model,
                value: condition === "cb" ? m.genF1_cb : m.genF1_or,
                sft: !!m.sft,
              }))}
              margin={{ top: 24, right: 8, left: -18, bottom: 0 }}
            >
              <XAxis
                dataKey="name"
                interval={0}
                tick={{ angle: -12, textAnchor: "end", fontSize: 10, fill: "var(--color-ink-faint)" }}
                axisLine={false}
                tickLine={false}
                height={48}
              />
              <YAxis
                domain={[0, 0.35]}
                tickFormatter={(v) => Number(v).toFixed(2)}
                tick={{ fontSize: 10, fill: "var(--color-ink-faint)" }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                formatter={(v) => [Number(v).toFixed(3), "GenF1"]}
                cursor={{ fill: "var(--color-bone)" }}
                contentStyle={{ borderRadius: 12, border: "1px solid var(--color-bone)", background: "var(--color-paper)", fontSize: 12 }}
              />
              <Bar dataKey="value" radius={[6, 6, 0, 0]} isAnimationActive animationDuration={700} animationEasing="ease-out">
                {MAIN_RESULTS.map((m) => (
                  <Cell key={m.model} fill={m.sft ? "var(--color-leaf)" : "var(--color-leaf-3)"} />
                ))}
                <LabelList dataKey="value" position="top" formatter={(v) => Number(v).toFixed(3)} fill="var(--color-ink-soft)" fontSize={10} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <p className="mt-2 text-[11px] text-ink-faint">
            ফাইন-টিউনড KrishokChat-4B — সেরা জিরো-শটের চেয়ে {condition === "cb" ? "১.৯×" : "১.২×"} বেশি GenF1 (০.৩১৪ vs ০.১৬৫ / ০.৩০০ vs ০.২৫৩)।
          </p>
        </motion.div>
        <motion.div variants={enter} className="relative">
          <div className="overflow-x-auto rounded-xl border rule">
            <table className="w-full min-w-[620px] text-xs sm:text-sm">
            <thead>
              <tr className="bg-paper-2">
                <th className="px-3 py-3 text-left font-display text-ink">মডেল</th>
                <th className="px-3 py-3 text-right font-display text-ink">GenF1</th>
                <th className="px-3 py-3 text-right font-display text-ink">GenHal%</th>
                <th className="px-3 py-3 text-right font-display text-ink">TrtCor%</th>
                <th className="px-3 py-3 text-right font-display text-ink">TrtHal%</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone">
              {MAIN_RESULTS.map((row, i) => {
                const f1 = condition === "cb" ? row.genF1_cb : row.genF1_or;
                const hal = condition === "cb" ? row.genHal_cb : row.genHal_or;
                const cor = condition === "cb" ? row.trtCor_cb : row.trtCor_or;
                const thal = condition === "cb" ? row.trtHal_cb : row.trtHal_or;
                return (
                  <motion.tr
                    key={i}
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.05 }}
                    className={`bg-paper ${row.sft ? "border-t-2 border-leaf/30" : ""}`}
                  >
                     <td className={`px-3 py-2.5 ${row.sft ? "font-medium text-leaf" : "text-ink"}`}>
                       <div className="flex items-center gap-2">
                         <span>{row.model}</span>
                         {row.sft && <span className="shrink-0 rounded-full bg-leaf/10 px-2 py-0.5 text-[9px] font-semibold text-leaf">★ সেরা ফলাফল</span>}
                       </div>
                    </td>
                    <td className="px-3 py-2.5 text-right tabular text-ink">{f1.toFixed(3)}</td>
                    <td className="px-3 py-2.5 text-right tabular text-ink-soft">{hal.toFixed(2)}</td>
                    <td className="px-3 py-2.5 text-right tabular text-ink">{cor.toFixed(2)}</td>
                    <td className={`px-3 py-2.5 text-right tabular ${thal > 5 ? "text-clay" : "text-ink-faint"}`}>
                      {thal.toFixed(2)}
                    </td>
                  </motion.tr>
                );
              })}
            </tbody>
            </table>
          </div>
          <div className="pointer-events-none absolute right-0 top-0 h-full w-10 rounded-r-xl bg-gradient-to-l from-paper via-paper/70 to-transparent sm:hidden" aria-hidden />
          <p className="mt-2 text-right text-[10px] text-ink-faint sm:hidden">ডানে টানুন →</p>
        </motion.div>
        </div>
        <motion.p variants={enter} className="mt-2 text-[11px] text-ink-faint">
          KrishokChat-4B ফাইন-টিউনড — GenF1 তীব্রভাবে উন্নত (০.৩১৪ vs সেরা জিরো-শট ০.১৬৫)।
        </motion.p>
      </motion.section>

      {/* === B. Retrieval Results (AgriTrust) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[1]}</motion.div>
        <motion.h2 variants={enter} className="mt-1 mb-3 font-display text-2xl text-ink">
          তথ্য সংগ্রহ ফলাফল — ৯০০ কোয়েরি
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          ৫টি আর্কিটেকচার, BN→BN। হাইব্রিড RRF সর্বোচ্চ, BM25 সেরা একক।
        </motion.p>

        {/* R@10 bar chart */}
        <motion.div variants={enter} className="space-y-3">
          {RETRIEVAL_RESULTS.map((row, i) => (
            <div key={row.arch} className="flex items-center gap-3">
              <div className="w-40 shrink-0 text-right text-xs text-ink">{row.arch}</div>
              <div className="relative h-7 flex-1 overflow-hidden rounded-md bg-bone">
                <motion.div
                  className={`absolute inset-y-0 left-0 rounded-md ${
                    row.best ? "bg-leaf" : row.bestSingle ? "bg-leaf-2" : "bg-leaf-3"
                  }`}
                  initial={{ width: 0 }}
                  whileInView={{ width: `${(row.r10 / 0.539) * 100}%` }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1, duration: dur.slow, ease: ease.smooth }}
                />
                <span className="relative flex items-center justify-end px-2 text-xs font-medium tabular text-ink">
                  {row.r10.toFixed(3)}
                </span>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Full table */}
        <motion.div variants={enter} className="relative mt-6">
          <div className="overflow-x-auto rounded-xl border rule">
          <table className="w-full min-w-[560px] text-xs sm:text-sm">
            <thead>
              <tr className="bg-paper-2">
                <th className="px-3 py-2.5 text-left font-display text-ink">আর্কিটেকচার</th>
                <th className="px-3 py-2.5 text-right font-display text-ink">R@1</th>
                <th className="px-3 py-2.5 text-right font-display text-ink">R@5</th>
                <th className="px-3 py-2.5 text-right font-display text-ink">R@10</th>
                <th className="px-3 py-2.5 text-right font-display text-ink">MRR</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone">
              {RETRIEVAL_RESULTS.map((row, i) => (
                <tr key={i} className={`bg-paper ${row.best ? "bg-leaf/5" : ""}`}>
                     <td className={`px-3 py-2.5 ${row.best ? "bg-leaf/5 font-medium text-leaf" : "text-ink"}`}>
                     <div className="flex items-center gap-2">
                       <span>{row.arch}</span>
                       {row.best && <span className="shrink-0 rounded-full bg-leaf/10 px-2 py-0.5 text-[9px] font-semibold text-leaf">★ সেরা ফলাফল</span>}
                     </div>
                  </td>
                  <td className="px-3 py-2.5 text-right tabular text-ink">{row.r1.toFixed(3)}</td>
                  <td className="px-3 py-2.5 text-right tabular text-ink">{row.r5.toFixed(3)}</td>
                  <td className="px-3 py-2.5 text-right tabular font-medium text-leaf">{row.r10.toFixed(3)}</td>
                  <td className="px-3 py-2.5 text-right tabular text-ink-soft">{row.mrr.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
          <div className="pointer-events-none absolute right-0 top-0 h-full w-10 rounded-r-xl bg-gradient-to-l from-paper via-paper/70 to-transparent sm:hidden" aria-hidden />
          <p className="mt-2 text-right text-[10px] text-ink-faint sm:hidden">ডানে টানুন →</p>
        </motion.div>
      </motion.section>

      {/* === C. Register Gap === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[2]}</motion.div>
        <motion.h2 variants={enter} className="mt-1 mb-3 font-display text-2xl text-ink">
          রেজিস্টার গ্যাপ আবিষ্কার
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          Dense তথ্য-সংগ্রহ ফার্মার ভাষায় প্রায় ব্যর্থ (০.০৯৩), কিন্তু আনুষ্ঠানিক নিরাপত্তা কোয়েরিতে প্রায় নিখুঁত (০.৯৭০)।
        </motion.p>

        {/* Diverging bar chart */}
        <motion.div variants={enter} className="space-y-4 rounded-xl border rule bg-paper p-6">
          {REGISTER_GAP.map((item, i) => (
            <div key={item.category} className="flex items-center gap-3">
              <div className="w-32 shrink-0 text-right text-xs text-ink">{item.category}</div>
              <div className="relative h-8 flex-1 overflow-hidden rounded-md bg-bone">
                {/* Dense bar */}
                <motion.div
                  className={`absolute inset-y-0 left-0 rounded-md ${
                    item.color === "clay" ? "bg-clay" : item.color === "leaf" ? "bg-leaf" : "bg-ochre"
                  }`}
                  initial={{ width: 0 }}
                  whileInView={{ width: `${item.dense * 100}%` }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.15, duration: dur.slow, ease: ease.smooth }}
                />
                <span className="relative flex items-center px-2 text-xs font-medium tabular text-ink">
                  Dense: {item.dense.toFixed(3)}
                </span>
              </div>
              <div className="w-20 shrink-0 text-xs tabular text-ink-faint">
                BM25: {item.bm25.toFixed(3)}
              </div>
            </div>
          ))}
        </motion.div>
        <motion.p variants={enter} className="mt-2 text-[11px] text-ink-faint">
          ৯৬.৪% কোয়েরির জ্যাকার্ড {"<"} ০.১০ — ফার্মার ভাষা আনুষ্ঠানিক ভাষার চেয়ে আলাদা।
        </motion.p>
      </motion.section>

      {/* === D. Cross-Lingual Collapse === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[3]}</motion.div>
        <motion.h2 variants={enter} className="mt-1 mb-3 font-display text-2xl text-ink">
          <Globe className="mr-2 inline h-6 w-6 text-leaf" />
          ক্রস-লিঙ্গুয়াল কলাপস
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          BM25 স্ক্রিপ্ট সীমা পার হলে প্রায় ব্যর্থ (০.৫০৬ → ০.০০৪), Dense টিকে থাকে (০.৪৬৪ → ০.৪২৫)।
        </motion.p>

        <motion.div variants={enter} className="overflow-hidden rounded-xl border rule">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-paper-2">
                <th className="px-4 py-3 text-left font-display text-ink">সেটিং</th>
                <th className="px-4 py-3 text-right font-display text-ink">Dense</th>
                <th className="px-4 py-3 text-right font-display text-ink">BM25</th>
                <th className="px-4 py-3 text-right font-display text-ink">বিজয়ী</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone">
              {CROSS_LINGUAL.map((row, i) => (
                <tr key={i} className="bg-paper">
                  <td className="px-4 py-3 font-medium text-ink">{row.setting}</td>
                  <td className="px-4 py-3 text-right tabular text-ink">{row.dense.toFixed(3)}</td>
                  <td className={`px-4 py-3 text-right tabular ${row.bm25 < 0.01 ? "text-clay" : "text-ink"}`}>
                    {row.bm25.toFixed(3)}
                  </td>
                  <td className={`px-4 py-3 text-right text-xs font-medium ${
                    row.winner === "Dense" ? "text-leaf" : "text-ochre"
                  }`}>
                    {row.winner}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
        <motion.p variants={enter} className="mt-2 text-[11px] text-ink-faint">
          BM25: ৯৯% ড্রপ | Dense: মাত্র ৮% ড্রপ — আর্কিটেকচার পছন্দ ভাষা পরিস্থিতি থেকে আলাদা নয়।
        </motion.p>
      </motion.section>

      {/* === E. Farmer Benchmark === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[4]}</motion.div>
        <motion.h2 variants={enter} className="mt-1 mb-3 font-display text-2xl text-ink">
          <TrendingUp className="mr-2 inline h-6 w-6 text-leaf" />
          রিয়েল-ওয়ার্ল্ড ফার্মার বেঞ্চমার্ক
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          ৩৫০টি প্রকৃত ফার্মার কোয়েরি — ৩০০টি মাঠ সাক্ষাৎকার থেকে।
        </motion.p>

        <motion.div variants={enter} className="overflow-hidden rounded-xl border rule">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-paper-2">
                <th className="px-4 py-3 text-left font-display text-ink">মডেল</th>
                <th className="px-4 py-3 text-right font-display text-ink">Token F1</th>
                <th className="px-4 py-3 text-right font-display text-ink">Halluc %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-bone">
              {FARMER_RESULTS.map((row, i) => (
                <tr key={i} className={`bg-paper ${row.best ? "bg-leaf/5" : ""}`}>
                  <td className={`px-4 py-3 ${row.best ? "font-medium text-leaf" : "text-ink"}`}>
                    {row.model}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span className="inline-flex items-center justify-end gap-2">
                      <span className="inline-block h-1.5 w-16 overflow-hidden rounded-full bg-bone">
                        <motion.span
                          className="block h-full rounded-full bg-leaf"
                          initial={{ width: 0 }}
                          whileInView={{ width: `${Math.min((row.f1 / 0.25) * 100, 100)}%` }}
                          viewport={{ once: true }}
                          transition={{ duration: dur.normal, ease: ease.smooth }}
                        />
                      </span>
                      <span className="font-medium tabular text-ink">{row.f1.toFixed(4)}</span>
                    </span>
                  </td>
                  <td className={`px-4 py-3 text-right tabular ${row.hal > 30 ? "text-clay" : "text-ink-soft"}`}>
                    {row.hal.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </motion.section>

      {/* === F. Hallucination Floor & Model Diff Inspector === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="space-y-6"
      >
        <motion.div variants={enter}>
          <div className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[5]}</div>
          <h2 className="mt-1 mb-2 font-display text-2xl text-ink">
            রাসায়নিক হ্যালুসিনেশন ফ্লোর ও মডেল তুলনা (A/B Diff Inspector)
          </h2>
          <p className="text-sm text-ink-soft max-w-3xl">
            একই বেঞ্চমার্ক প্রশ্নে জিরো-শট বনাম ফাইন-টিউনড বনাম মাল্টি-এজেন্ট গ্রাউন্ডেড মডেলের পাশাপাশি ফলাফল, রাসায়নিক নিরাপত্তা স্কোর এবং কেন স্টেজ ৪ ভেরিফায়ার গেট আবশ্যক তার ইন্টারঅ্যাক্টিভ বিশ্লেষণ।
          </p>
        </motion.div>

        <motion.div variants={enter}>
          <ModelComparisonInspector />
        </motion.div>
      </motion.section>

      {/* === G. Live-System Golden Eval (precomputed artifact) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
      >
        <motion.div variants={enter} className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{KICKERS[6]}</motion.div>
        <motion.h2 variants={enter} className="mt-1 mb-3 font-display text-2xl text-ink">
          <ShieldCheck className="mr-2 inline h-6 w-6 text-leaf" />
          লাইভ সিস্টেম — গোল্ডেন ইভাল
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          ১,০০০টি প্রকৃত ফার্মার প্রশ্ন থেকে ৪৬টি নির্বাচিত, ৩ ধাপে মানব-পর্যালোচিত ক্যাটাগরি।
          প্রশ্নগুলো এই সিস্টেমের প্রকৃত পাইপলাইন দিয়ে চালানো হয়; সব সংখ্যা অফলাইনে প্রি-কম্পিউটেড।
        </motion.p>

        {/* Mini stat strip */}
        <motion.div variants={enter} className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
          {[
            { value: STATS.items, label: "গোল্ডেন প্রশ্ন" },
            { value: STATS.mechanical.per_category.unanswerable?.n ?? 0, label: "উত্তরযোগ্য নয়" },
            { value: STATS.evaluators, label: "স্বাধীন মূল্যায়নকারী" },
            { value: STATS.status === "pending_scores" ? 0 : (STATS.kappa ?? 0), label: STATS.status === "pending_scores" ? "কাপা (পেন্ডিং)" : "ইন্টার-রেটার কাপা (κ)" },
          ].map((s, i) => (
            <StatCell key={s.label} value={s.value} label={s.label} delay={i * 0.04} />
          ))}
        </motion.div>

        {/* Mechanical pipeline behavior */}
        <motion.div variants={enter} className="relative mt-6">
          <div className="overflow-x-auto rounded-xl border rule">
            <table className="w-full min-w-[480px] text-xs sm:text-sm">
              <thead>
                <tr className="bg-paper-2">
                  <th className="px-3 py-2.5 text-left font-display text-ink">ক্যাটাগরি</th>
                  <th className="px-3 py-2.5 text-right font-display text-ink">n</th>
                  <th className="px-3 py-2.5 text-right font-display text-ink">অস্বীকৃত (রেফারাল)</th>
                  <th className="px-3 py-2.5 text-right font-display text-ink">ভেরিফায়ার উত্তীর্ণ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-bone">
                {CATEGORY_ORDER.filter((c) => STATS.mechanical.per_category[c]).map((cat) => {
                  const s = STATS.mechanical.per_category[cat];
                  return (
                    <tr key={cat} className="bg-paper">
                      <td className="px-3 py-2.5 font-medium text-ink">{CATEGORY_BN[cat] ?? cat}</td>
                      <td className="px-3 py-2.5 text-right tabular text-ink">{s.n}</td>
                      <td className={`px-3 py-2.5 text-right tabular ${cat === "unanswerable" && s.refused === 0 ? "text-clay" : "text-ink"}`}>
                        {s.refused}
                      </td>
                      <td className="px-3 py-2.5 text-right tabular text-ink-soft">{s.verified}/{s.n}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-[11px] text-ink-faint">
            যান্ত্রিক পাইপলাইন আচরণ — মানব স্কোরই চূড়ান্ত বিচার। ক্যাটাগরি ট্রেনিং/রপ্তানি/যোগাযোগ-ধরনের প্রশ্ন মানে "উত্তরযোগ্য নয়"।
          </p>
        </motion.div>

        {/* Unanswerable refusal — gate outcome (D1a, 2026-08-14) */}
        {(() => {
          const rate = STATS.mechanical.unanswerable_refusal_rate ?? 0;
          const met = rate >= 0.9;
          return (
            <motion.div variants={enter} className={`mt-4 rounded-xl border p-5 ${met ? "border-leaf/40 bg-leaf/8" : "border-clay-soft/40 bg-clay-soft/8"}`}>
              <div className="flex items-start gap-3">
                {met ? (
                  <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-leaf" />
                ) : (
                  <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-clay" />
                )}
                <div>
                  <div className={`text-sm font-semibold ${met ? "text-leaf" : "text-ink"}`}>
                    উত্তরযোগ্য নয় এমন ১২টি প্রশ্নে রেফারাল-হার: {Math.round(rate * 100)}% (যান্ত্রিক)
                  </div>
                  {met ? (
                    <p className="mt-1 text-xs leading-relaxed text-ink-soft">
                      কর্পাস-কভারেজ গেট (D1a) সক্রিয়: প্রশিক্ষণ, রপ্তানি, ভেন্ডর/চারা প্রাপ্যতা, প্রতিষ্ঠানগত
                      ও সরকারি-সহায়তা সংক্রান্ত প্রশ্নে সরাসরি ১৬১২৩ রেফারাল — কোনো জল্পনা-কল্পনা নয়।
                      অফ-টপিক ২/২-ও প্রত্যাখ্যাত। লক্ষ্য পূরণ হয়েছে (≥৯০%)।
                    </p>
                  ) : (
                    <p className="mt-1 text-xs leading-relaxed text-ink-soft">
                      কর্পাসে নেই এমন প্রশ্নে সিস্টেম এখনও উত্তরের চেষ্টা করে — এটিই বর্তমান খোলা সমস্যা।
                      লক্ষ্য: এই হার ৯০%-এ উন্নীত করা।
                    </p>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })()}

        {/* Human scores — pending or complete */}
        {STATS.status === "pending_scores" ? (
          <motion.div variants={enter} className="mt-4 rounded-xl border rule bg-paper p-5">
            <div className="flex items-start gap-3">
              <Hourglass className="mt-0.5 h-5 w-5 shrink-0 text-ochre" />
              <div>
                <div className="text-sm font-semibold text-ink">স্কোরিং পেন্ডিং — ২ স্বাধীন মূল্যায়নকারী</div>
                <p className="mt-1 text-xs leading-relaxed text-ink-soft">
                  প্রতিটি উত্তর correct / partial / unsupported / refused স্কেলে মূল্যায়িত হয়।
                  স্কোর শেষ হলে এখানে κ (ইন্টার-রেটার এগ্রিমেন্ট), ক্যাটাগরি-ভিত্তিক ফলাফল এবং
                  অস্বীকৃতির নিশ্চিত হার স্বয়ংক্রিয়ভাবে প্রকাশ পাবে।
                </p>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div variants={enter} className="mt-6 space-y-4">
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              {[
                { label: "ইন্টার-রেটার κ", value: STATS.kappa ?? 0, color: "text-leaf" },
                { label: "র-এগ্রিমেন্ট", value: STATS.raw_agreement ?? 0, color: "text-leaf" },
                { label: "রেফারাল-হার (নিশ্চিত)", value: STATS.unanswerable_refusal_rate_validated ?? 0, color: "text-clay" },
                { label: "অসম্মতি", value: STATS.disagreement_count ?? 0, color: "text-ochre" },
              ].map((chip) => (
                <div key={chip.label} className="rounded-xl border rule bg-paper p-4 text-center">
                  <div className={`font-display text-2xl tabular ${chip.color}`}>{toBn(chip.value)}</div>
                  <div className="mt-1 text-[10px] font-medium text-ink-faint">{chip.label}</div>
                </div>
              ))}
            </div>
            <div className="overflow-x-auto rounded-xl border rule">
              <table className="w-full min-w-[560px] text-xs sm:text-sm">
                <thead>
                  <tr className="bg-paper-2">
                    <th className="px-3 py-2.5 text-left font-display text-ink">ক্যাটাগরি</th>
                    <th className="px-3 py-2.5 text-right font-display text-ink">n</th>
                    {Object.values(SCORE_BN).map((label) => (
                      <th key={label} className="px-3 py-2.5 text-right font-display text-ink">{label}</th>
                    ))}
                    <th className="px-3 py-2.5 text-right font-display text-ink">সঠিক-হার</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-bone">
                  {CATEGORY_ORDER.filter((c) => STATS.category_results?.[c]).map((cat) => {
                    const s = STATS.category_results![cat];
                    return (
                      <tr key={cat} className="bg-paper">
                        <td className="px-3 py-2.5 font-medium text-ink">{CATEGORY_BN[cat] ?? cat}</td>
                        <td className="px-3 py-2.5 text-right tabular text-ink">{s.n}</td>
                        <td className="px-3 py-2.5 text-right tabular text-ink">{s.correct}</td>
                        <td className="px-3 py-2.5 text-right tabular text-ink-soft">{s.partial}</td>
                        <td className="px-3 py-2.5 text-right tabular text-clay">{s.unsupported}</td>
                        <td className="px-3 py-2.5 text-right tabular text-ink">{s.refused}</td>
                        <td className="px-3 py-2.5 text-right tabular font-medium text-leaf">{s.correct_rate.toFixed(3)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </motion.div>
        )}
      </motion.section>
    </div>
  );
}
