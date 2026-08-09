"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { TrendingUp, AlertTriangle, Globe } from "lucide-react";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";

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

export default function BenchmarkPage() {
  const [condition, setCondition] = useState<Condition>("cb");

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
          Benchmark Results
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          মূল্যায়ন <span className="text-leaf">ফলাফল</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          ৬টি মডেল, ৫টি তথ্য-সংগ্রহ আর্কিটেকচার, ৯০০টি কোয়েরি — সব সংখ্যা গবেষণাপত্র থেকে, কোনো তথ্য তৈরি নয়।
        </motion.p>
      </motion.section>

      {/* === A. Main Results Table === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
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

        {/* Table */}
        <motion.div variants={enter} className="overflow-x-auto rounded-xl border rule">
          <table className="w-full text-xs sm:text-sm">
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
                      {row.model}
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
        </motion.div>
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
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
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
        <motion.div variants={enter} className="mt-6 overflow-x-auto rounded-xl border rule">
          <table className="w-full text-xs sm:text-sm">
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
                  <td className={`px-3 py-2.5 ${row.best ? "font-medium text-leaf" : "text-ink"}`}>
                    {row.arch}
                  </td>
                  <td className="px-3 py-2.5 text-right tabular text-ink">{row.r1.toFixed(3)}</td>
                  <td className="px-3 py-2.5 text-right tabular text-ink">{row.r5.toFixed(3)}</td>
                  <td className="px-3 py-2.5 text-right tabular font-medium text-leaf">{row.r10.toFixed(3)}</td>
                  <td className="px-3 py-2.5 text-right tabular text-ink-soft">{row.mrr.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </motion.section>

      {/* === C. Register Gap === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
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
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
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
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
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
                  <td className="px-4 py-3 text-right tabular font-medium text-ink">
                    {row.f1.toFixed(4)}
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

      {/* === F. Hallucination Floor === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="rounded-xl border border-clay-soft/40 bg-clay-soft/8 p-8 text-center"
      >
        <motion.div variants={enter}>
          <AlertTriangle className="mx-auto h-10 w-10 text-clay" />
          <h2 className="mt-4 font-display text-2xl text-ink">রাসায়নিক হ্যালুসিনেশন ফ্লোর</h2>
          <p className="mx-auto mt-3 max-w-lg text-sm leading-relaxed text-ink-soft">
            পরিপূর্ণ অরাকল তথ্য থাকা সত্ত্বেও{" "}
            <span className="font-display text-lg text-clay">{RESEARCH_STATS.hallucinationFloor}</span>{" "}
            রাসায়নিক হ্যালুসিনেশন থেকে যায় — ৬টি ভিন্ন আর্কিটেকচার মডেলে। ডোজ ত্রুটি, বাদ দেওয়া নয়,
            মাঠে সবচেয়ে বেশি ক্ষতির কারণ।
          </p>
          <p className="mt-3 text-xs text-ink-faint">
            এই সমস্যা এখনও অমীমাংসিত — তথ্য-সংগ্রহ মানের উন্নতি একা যথেষ্ট নয়।
          </p>
        </motion.div>
      </motion.section>
    </div>
  );
}
