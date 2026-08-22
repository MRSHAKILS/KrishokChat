"use client";

/* =========================================================================
   LandingStats — the landing page's visual stats section (charts).

   Extracted from app/(marketing)/page.tsx so recharts stays out of the
   landing page's first-load JS bundle (rural-bandwidth budget). Loaded via
   next/dynamic with a skeleton placeholder.
   ========================================================================= */

import { motion } from "motion/react";
import { CheckCircle2 } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  PieChart,
  Pie,
} from "recharts";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";

const TRACK_DATA = [
  { name: "সাধারণ কৃষি QA", value: 28993, color: "var(--color-leaf)" },
  { name: "সার ও মাটি নির্দেশিকা QA", value: 25650, color: "var(--color-leaf-2)" },
  { name: "নিরাপত্তা ও গার্ডরেইল QA", value: 20112, color: "var(--color-ochre)" },
  { name: "বালাই ও রোগ ব্যবস্থাপনা QA", value: 11224, color: "var(--color-clay)" },
];

/* Farmer-facing retrieval chart labels — the backend enums (BM25, Dense,
   Hybrid RRF, ColBERT) are technical jargon; the home page is for farmers.
   The /research/benchmark page keeps the full technical terms for reviewers. */
const RETRIEVAL_DATA = [
  { name: "হাইব্রিড মিশ্র পদ্ধতি", value: 0.539, best: true },
  { name: "শব্দ মিল (BM25)", value: 0.506, best: false },
  { name: "অর্থ মিল (Dense)", value: 0.464, best: false },
  { name: "টোকেন মিল (ColBERT)", value: 0.487, best: false },
];

export function LandingStats() {
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
          <p className="mb-4 text-xs text-ink-faint">প্রতিটি প্রশ্নের সঠিক উৎস খুঁজে পাওয়ার হার</p>
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
          <div className="mt-2 flex items-center gap-2 rounded-md bg-leaf/10 px-2.5 py-1.5 text-xs text-leaf">
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
            <div className="mt-1 text-xs font-medium text-ink-soft">{s.label}</div>
          </div>
        ))}
      </motion.div>
    </motion.section>
  );
}
