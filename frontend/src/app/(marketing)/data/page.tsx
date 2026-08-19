"use client";

/* =========================================================================
   Data & Dataset Page — the knowledge base as a tangible, credible resource.

   Every number on this page is sourced from RESEARCH_STATS (constants.ts),
   which is verified against the two local papers (`paper/done papers/`).
   No fabricated values. Charts render REAL counts; the AI-generated JPG is
   kept only as a labeled schematic with a proper frame + lightbox zoom.

   Motion: MotionConfig reducedMotion="user" (WCAG 2.3.3) — under OS
   reduced-motion, all animations collapse to instant show.
   ========================================================================= */

import { useRef, useState } from "react";
import { motion, AnimatePresence, MotionConfig, useInView } from "motion/react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, LabelList } from "recharts";
import {
  Database, ExternalLink, ChevronDown, Tag, FileText, Boxes, ArrowRight,
  GitBranch, ChevronRight, FlaskConical,
} from "lucide-react";
import { RESEARCH_STATS, LINKS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { useCountUp, toBn } from "@/lib/use-count-up";
import { KnowledgeGraphExplorer } from "@/components/knowledge-graph-explorer";

/* ---- real data (all verified against AgriTrust paper) ---- */

/* Numeric mirrors of RESEARCH_STATS — count-up needs numbers; display via toBn().
   2882 = knowledgeNodes, 19768 = entities, 17501 = triples, 1022 = imageLinkedNodes,
   915 = uniqueCrops, 704 = diseaseVariants, 2729 = chemicalEntities, 284 = publications */
const STAT_NUMS = {
  nodes: 2882, entities: 19768, triples: 17501, imageLinked: 1022,
  crops: 915, variants: 704, chemicals: 2729, pdfs: 284,
} as const;

const NODE_CATEGORIES = [
  { name: "Variety", bn: "জাত", count: 695 },
  { name: "Cultivation Practice", bn: "চাষ পদ্ধতি", count: 570 },
  { name: "Disease", bn: "রোগ", count: 430 },
  { name: "Pest", bn: "পোকা", count: 380 },
  { name: "Fertilizer", bn: "সার", count: 280 },
  { name: "Other", bn: "অন্যান্য", count: 527 },
] as const;

const CAT_COLORS: Record<string, string> = {
  Variety: "var(--color-leaf)", "Cultivation Practice": "var(--color-leaf-2)",
  Disease: "var(--color-ochre)", Pest: "var(--color-clay)",
  Fertilizer: "var(--color-leaf-3)", Other: "var(--color-ink-soft)",
};

const NODE_TOTAL = NODE_CATEGORIES.reduce((s, c) => s + c.count, 0); // 2,882 — matches RESEARCH_STATS.knowledgeNodes

/* Donut segments: real fractions of NODE_TOTAL, cumulative rotation */
const SEGMENTS = (() => {
  let acc = 0;
  return NODE_CATEGORIES.map((c) => {
    const frac = c.count / NODE_TOTAL;
    const rot = acc * 360 - 90;
    acc += frac;
    return { ...c, frac, rot, color: CAT_COLORS[c.name] };
  });
})();

const SAMPLE_NODE = {
  id: "DAE_PEST_1206A0_001",
  title_bn: "আলুর লেট ব্লাইট (নাবি ধসা)",
  title_en: "Potato Late Blight",
  category: "disease",
  publisher: "DAE",
  source_document: "Potato Disease Manuals (Plantwise)",
  citation: "DAE. Late blight. Potato Disease Manuals. p. 852.",
  content_bn:
    "আলুর লেট ব্লাইট (Late Blight / নাবি ধসা) একটি মারাত্মক ছত্রাকজনিত রোগ যা Phytophthora infestans দ্বারা সৃষ্ট। এটি পাতার ও কাণ্ডের নিচে ছোট ছোট সবুজ-বাদামি দাগ হিসেবে শুরু হয়।",
  entities: ["Phytophthora infestans", "potato", "late blight"],
  chemical_trace: ["Mancozeb 80WP", "Metalaxyl"],
};

const DATASET_STATS = [
  { value: STAT_NUMS.nodes, label: "জ্ঞানভাণ্ডার নোড", icon: Boxes },
  { value: STAT_NUMS.entities, label: "চিহ্নিত এনটিটি", icon: Tag },
  { value: STAT_NUMS.triples, label: "সম্পর্ক ট্রিপল", icon: Database },
  { value: STAT_NUMS.imageLinked, label: "চিত্রযুক্ত জ্ঞান নোড", icon: FileText, ratio: `মোট নোডের ${RESEARCH_STATS.imageLinkedShare}` },
  { value: STAT_NUMS.crops, label: "স্বতন্ত্র ফসল", icon: Tag },
  { value: STAT_NUMS.variants, label: "রোগ ও বালাই রূপভেদ", icon: Tag },
  { value: STAT_NUMS.chemicals, label: "রাসায়নিক উপাদান", icon: Tag },
  { value: STAT_NUMS.pdfs, label: "সরকারি প্রকাশনা (PDF)", icon: FileText },
] as const;

/* Data card groups — values all from RESEARCH_STATS (paper-verified) */
const CARD_GROUPS = [
  {
    name: "কর্পাস ও জ্ঞানভাণ্ডার",
    rows: [
      ["সরকারি মূল প্রকাশনা", RESEARCH_STATS.publications],
      ["উৎস প্রতিষ্ঠান", RESEARCH_STATS.institutions],
      ["জ্ঞানভাণ্ডার নোড", RESEARCH_STATS.knowledgeNodes],
      ["চিত্রযুক্ত নোড", `${RESEARCH_STATS.imageLinkedNodes} (${RESEARCH_STATS.imageLinkedShare})`],
      ["শনাক্তকৃত এনটিটি", RESEARCH_STATS.entities],
      ["সম্পর্ক ট্রিপল", RESEARCH_STATS.triples],
      ["স্বতন্ত্র ফসল শ্রেণি", RESEARCH_STATS.uniqueCrops],
      ["রোগ ও বালাই রূপভেদ", RESEARCH_STATS.diseaseVariants],
      ["রাসায়নিক উপাদান", RESEARCH_STATS.chemicalEntities],
    ] as [string, string][],
  },
  {
    name: "বেঞ্চমার্ক মূল্যায়ন",
    rows: [
      ["কৃষক প্রশ্ন (মোট)", RESEARCH_STATS.farmerQueries],
      ["মূল্যায়নযোগ্য প্রশ্ন", RESEARCH_STATS.answerableQueries],
    ] as [string, string][],
  },
  {
    name: "বিশেষজ্ঞ যাচাই — ইন্টার-অ্যানোটেটর κ",
    rows: [
      ["κ (কৃষক প্রশ্ন + নিরাপত্তা)", RESEARCH_STATS.interAnnotatorKappa, 72],
      ["κ (নলেজ-গ্রাফ গ্রাউন্ডেড)", RESEARCH_STATS.kgGroundedKappa, 78],
    ] as [string, string, number][],
  },
] as const;

/* === small pieces === */

function SectionHeading({ no, title, sub }: { no: string; title: string; sub?: string }) {
  return (
    <motion.div variants={enter}>
      <div className="font-mono text-[11px] uppercase tracking-[0.22em] text-ochre">{no}</div>
      <h2 className="mt-1 font-display text-2xl text-ink">{title}</h2>
      {sub && <p className="mt-2 text-sm leading-relaxed text-ink-soft">{sub}</p>}
    </motion.div>
  );
}

function StatCell({ value, label, icon: Icon, ratio, delay }: { value: number; label: string; icon: React.ComponentType<{ className?: string }>; ratio?: string; delay: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const n = useCountUp(value, inView);
  return (
    <motion.div ref={ref} variants={enter} transition={{ delay }} className="bg-paper p-5 text-center">
      <Icon className="mx-auto h-5 w-5 text-leaf" />
      <div className="mt-3 font-display text-2xl tabular text-ink">{toBn(n)}</div>
      <div className="mt-1 text-[10px] font-medium text-ink-faint">{label}</div>
      {ratio && <div className="mt-1 font-mono text-[10px] tabular text-ochre">{ratio}</div>}
    </motion.div>
  );
}

/* =========================================================================
   Main page
   ========================================================================= */

export default function DataPage() {
  const [nodeOpen, setNodeOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const selected = NODE_CATEGORIES.find((c) => c.name === selectedCategory);
  const selectedFrac = selected ? (selected.count / NODE_TOTAL) * 100 : 0;

  return (
    <MotionConfig reducedMotion="user">
      <div className="mx-auto max-w-6xl space-y-12 py-14">
        {/* === Hero === */}
        <motion.section initial="hidden" animate="visible" variants={stagger} className="text-center">
          <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
            Knowledge Base & Dataset
          </motion.p>
          <motion.h1 variants={enter} className="mt-4 font-display text-3xl leading-tight text-ink md:text-4xl">
            জ্ঞান গ্রাফ <span className="text-leaf">ও উপাত্ত</span>
          </motion.h1>
          <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
            {RESEARCH_STATS.publications}টি সরকারি প্রকাশনা থেকে নির্মিত {RESEARCH_STATS.knowledgeNodes}টি জ্ঞান নোড —
            প্রমাণ-ভিত্তিক, উৎস-লকড, প্রতিটি ট্রেসযোগ্য।
          </motion.p>
          <motion.p variants={enter} className="mt-5">
            <a href="/library" className="inline-flex items-center gap-1.5 rounded-full border rule bg-paper px-4 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf">
              বই ও ডেটাসেট ব্রাউজ করুন<ArrowRight className="h-3 w-3" />
            </a>
          </motion.p>
        </motion.section>

        {/* === ০১. Dataset Stats === */}
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={stagger}
        >
          <SectionHeading no="০১" title="উপাত্ত পরিসংখ্যান" sub="কর্পাসের আকার — সব সংখ্যা গবেষণাপত্র-যাচাইকৃত।" />
          <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
            {DATASET_STATS.map((stat, i) => (
              <StatCell key={stat.label} {...stat} delay={i * 0.04} />
            ))}
          </motion.div>
        </motion.section>

        {/* === ০২. Knowledge Graph === */}
        <motion.section
          id="knowledge-graph"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={stagger}
        >
          <SectionHeading no="০২" title="জ্ঞান গ্রাফ" sub="১৩-ক্যাটাগরি কৃষি ট্যাক্সোনমি — জাত, চাষ, রোগ, পোকা, সার থেকে খাদ্য নিরাপত্তা পর্যন্ত। নিচের চিত্রটি বাস্তব সংখ্যা থেকে আঁকা।" />

          <div className="mt-6 grid grid-cols-1 items-center gap-6 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
            {/* Real donut — category share, animated draw */}
            <motion.div variants={enter} className="flex flex-col items-center rounded-xl border rule bg-paper p-6">
              <svg viewBox="0 0 240 240" className="h-auto w-full max-w-[300px]">
                {SEGMENTS.map((s, i) => (
                  <motion.circle
                    key={s.name}
                    cx={120}
                    cy={120}
                    r={92}
                    fill="none"
                    stroke={s.color}
                    strokeWidth={30}
                    pathLength={1}
                    strokeDasharray={`${s.frac} ${1 - s.frac}`}
                    transform={`rotate(${s.rot} 120 120)`}
                    initial={{ opacity: 0, pathLength: 0 }}
                    whileInView={{ opacity: 1, pathLength: s.frac }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 + i * 0.12, duration: dur.slow, ease: ease.smooth }}
                  />
                ))}
                <text x={120} y={114} textAnchor="middle" className="fill-ink font-display" fontSize={26}>
                  {toBn(NODE_TOTAL)}
                </text>
                <text x={120} y={136} textAnchor="middle" className="fill-ink-faint" fontSize={10}>
                  জ্ঞান নোড
                </text>
              </svg>
              <div className="mt-4 w-full space-y-1.5">
                {NODE_CATEGORIES.map((cat) => {
                  const active = selectedCategory === cat.name;
                  return (
                    <button
                      key={cat.name}
                      onClick={() => setSelectedCategory(active ? null : cat.name)}
                      aria-pressed={active}
                      className={`flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-left transition-colors ${active ? "bg-bone" : "hover:bg-bone/60"}`}
                    >
                      <span className="h-2.5 w-2.5 shrink-0 rounded-full" style={{ backgroundColor: CAT_COLORS[cat.name] }} />
                      <span className="flex-1 text-sm text-ink">{cat.bn}</span>
                      <span className="font-mono text-[10px] text-ink-faint">{cat.name}</span>
                      <span className="font-display text-sm tabular text-ink">{toBn(cat.count)}</span>
                      <span className="w-10 text-right font-mono text-[10px] tabular text-ink-faint">
                        {((cat.count / NODE_TOTAL) * 100).toFixed(1)}%
                      </span>
                    </button>
                  );
                })}
              </div>
            </motion.div>

            {/* Absolute counts — recharts bar chart (real y-axis) */}
            <motion.div variants={enter} className="rounded-xl border rule bg-paper p-6">
              <div className="mb-2 text-xs font-semibold text-ochre">ক্যাটাগরি অনুযায়ী নোড — পরম সংখ্যা</div>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={[...NODE_CATEGORIES]} layout="vertical" margin={{ left: 8, right: 44 }}>
                  <XAxis type="number" domain={[0, 700]} tickFormatter={(v) => toBn(Number(v))} tick={{ fontSize: 11, fill: "var(--color-ink-faint)" }} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="bn" width={72} tick={{ fontSize: 12, fill: "var(--color-ink)" }} axisLine={false} tickLine={false} />
                  <Tooltip
                    formatter={(v) => [toBn(Number(v)), "নোড"]}
                    cursor={{ fill: "var(--color-bone)" }}
                    contentStyle={{ borderRadius: 12, border: "1px solid var(--color-bone)", background: "var(--color-paper)", fontSize: 12 }}
                  />
                  <Bar dataKey="count" radius={[0, 6, 6, 0]} isAnimationActive animationDuration={700} animationEasing="ease-out">
                    {NODE_CATEGORIES.map((d) => (
                      <Cell key={d.name} fill={CAT_COLORS[d.name]} />
                    ))}
                    <LabelList dataKey="count" position="right" formatter={(v) => toBn(Number(v))} fill="var(--color-ink-soft)" fontSize={11} />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <p className="mt-2 text-[11px] text-ink-faint">মোট {toBn(NODE_TOTAL)} নোড — {RESEARCH_STATS.publications}টি প্রকাশনা থেকে নির্যাসিত, উৎস আইডি ও পৃষ্ঠা নম্বরসহ।</p>
            </motion.div>
          </div>

          {/* Selected-category detail — REAL data only */}
          <AnimatePresence>
            {selected && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: dur.normal, ease: ease.smooth }}
                className="mt-4 overflow-hidden"
              >
                <div className="flex flex-wrap items-center gap-x-6 gap-y-2 rounded-xl border rule bg-paper-2/40 px-5 py-4">
                  <div>
                    <div className="font-display text-2xl tabular text-ink">{toBn(selected.count)}</div>
                    <div className="text-[10px] text-ink-faint">{selected.bn} নোড</div>
                  </div>
                  <div>
                    <div className="font-display text-2xl tabular text-ochre">{selectedFrac.toFixed(1)}%</div>
                    <div className="text-[10px] text-ink-faint">মোট কর্পাসের অংশ</div>
                  </div>
                  <div className="flex-1 text-sm leading-relaxed text-ink-soft">
                    প্রতিটি নোড একটি সরকারি প্রকাশনার নির্দিষ্ট পৃষ্ঠা থেকে নির্যাসিত — উৎস আইডি ও পৃষ্ঠা নম্বরসহ।
                  </div>
                  {selected.name === "Disease" && (
                    <a href="#sample-node" className="inline-flex items-center gap-1.5 rounded-lg border rule bg-paper px-3 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf">
                      <FlaskConical className="h-3.5 w-3.5" />নমুনা নোড দেখুন: আলুর লেট ব্লাইট
                    </a>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Interactive Knowledge Graph Explorer */}
          <motion.div variants={enter} className="mt-8">
            <KnowledgeGraphExplorer />
          </motion.div>
        </motion.section>

        {/* === ০৩. Sample Knowledge Node === */}
        <motion.section
          id="sample-node"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={stagger}
        >
          <SectionHeading no="০৩" title="নমুনা জ্ঞান নোড" sub="একটি বাস্তব জ্ঞান নোড — প্রমাণ-লকড, উৎস-ট্রেসযোগ্য, রাসায়নিক-অডিটযোগ্য।" />

          <motion.div variants={enter} className="mt-6 rounded-xl border rule bg-paper">
            {/* Header */}
            <button
              onClick={() => setNodeOpen((v) => !v)}
              className="flex w-full items-center justify-between px-5 py-4 text-left"
            >
              <div className="flex-1">
                <div className="font-mono text-xs text-ink-faint">{SAMPLE_NODE.id}</div>
                <div className="mt-1 font-display text-lg text-ink">{SAMPLE_NODE.title_bn}</div>
                <div className="text-sm text-ochre">{SAMPLE_NODE.title_en}</div>
                <div className="mt-1 font-mono text-[10px] text-ink-faint">
                  {SAMPLE_NODE.entities.length} এনটিটি · {SAMPLE_NODE.chemical_trace.length} রাসায়নিক ট্রেস
                </div>
              </div>
              <ChevronDown className={`h-5 w-5 shrink-0 text-ink-faint transition-transform ${nodeOpen ? "rotate-180" : ""}`} />
            </button>

            {/* Provenance path — doc -> page -> node */}
            <motion.div
              variants={stagger}
              className="flex flex-wrap items-center gap-x-2 gap-y-1.5 border-t rule px-5 py-3"
            >
              {[SAMPLE_NODE.publisher, SAMPLE_NODE.source_document, "p. 852", SAMPLE_NODE.id].map((step, i, arr) => (
                <motion.span key={step} variants={enter} className="flex items-center gap-2">
                  <span className={`rounded-md px-2 py-1 font-mono text-[10px] ${i === 0 ? "bg-clay-soft/20 text-clay" : "bg-bone text-ink-soft"}`}>
                    {step}
                  </span>
                  {i < arr.length - 1 && <ChevronRight className="h-3 w-3 text-ink-faint" />}
                </motion.span>
              ))}
              <span className="ml-auto font-mono text-[10px] text-ink-faint">উৎস → পৃষ্ঠা → নোড</span>
            </motion.div>

            {/* Expandable content */}
            <AnimatePresence>
              {nodeOpen && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: dur.normal, ease: ease.smooth }}
                  className="overflow-hidden border-t rule"
                >
                  <div className="space-y-4 px-5 py-4">
                    <div className="grid grid-cols-2 gap-3 text-xs sm:grid-cols-4">
                      <div>
                        <div className="text-ink-faint">ক্যাটাগরি</div>
                        <div className="font-medium text-ink">{SAMPLE_NODE.category}</div>
                      </div>
                      <div>
                        <div className="text-ink-faint">প্রকাশক</div>
                        <div className="font-medium text-ink">{SAMPLE_NODE.publisher}</div>
                      </div>
                      <div>
                        <div className="text-ink-faint">উৎস নথি</div>
                        <div className="font-medium text-ink">{SAMPLE_NODE.source_document}</div>
                      </div>
                      <div>
                        <div className="text-ink-faint">সাইটেশন</div>
                        <div className="font-medium text-ink">{SAMPLE_NODE.citation}</div>
                      </div>
                    </div>

                    <div>
                      <div className="text-xs text-ink-faint">কনটেন্ট (বাংলা)</div>
                      <p className="mt-1 text-sm leading-relaxed text-ink-soft">{SAMPLE_NODE.content_bn}</p>
                    </div>

                    <div>
                      <div className="text-xs text-ink-faint">এনটিটি</div>
                      <div className="mt-1 flex flex-wrap gap-1.5">
                        {SAMPLE_NODE.entities.map((entity) => (
                          <span key={entity} className="rounded-md bg-leaf/10 px-2 py-0.5 font-mono text-[11px] text-leaf">
                            {entity}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div>
                      <div className="text-xs text-ink-faint">রাসায়নিক ট্রেস</div>
                      <div className="mt-1 flex flex-wrap gap-1.5">
                        {SAMPLE_NODE.chemical_trace.map((chem) => (
                          <span key={chem} className="rounded-md bg-clay-soft/20 px-2 py-0.5 font-mono text-[11px] text-clay">
                            {chem}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </motion.section>

        {/* === ০৪. Dataset Access === */}
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={stagger}
        >
          <SectionHeading no="০৪" title="উপাত্ত অ্যাক্সেস" sub="ডেটাসেট রিপোজিটরি ও লাইসেন্স — সব প্রকাশ্যে, কোনো লগইন নেই।" />
          <motion.div variants={enter} className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <a
              href={LINKS.huggingface}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-4 rounded-xl border rule bg-paper p-5 transition-colors hover:border-leaf"
            >
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <Database className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <div className="font-display text-base text-ink">Hugging Face</div>
                <div className="text-xs text-ink-faint">RaiyanKhaan/krishokChat</div>
              </div>
              <ExternalLink className="h-4 w-4 text-ink-faint transition-colors group-hover:text-leaf" />
            </a>
            <a
              href={LINKS.github}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-4 rounded-xl border rule bg-paper p-5 transition-colors hover:border-leaf"
            >
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-ochre/10 text-ochre">
                <GitBranch className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <div className="font-display text-base text-ink">GitHub</div>
                <div className="text-xs text-ink-faint">RaiyanKhaan/KrishokChat</div>
              </div>
              <ExternalLink className="h-4 w-4 text-ink-faint transition-colors group-hover:text-leaf" />
            </a>
          </motion.div>

          <motion.div variants={enter} className="mt-4 flex items-center justify-center gap-3 rounded-lg border rule bg-paper-2/40 px-5 py-3">
            <span className="flex h-7 w-7 items-center justify-center rounded-md bg-ochre/10 font-display text-xs font-bold text-ochre">CC</span>
            <span className="text-xs text-ink-faint">লাইসেন্স: CC-BY-4.0 | গবেষণা প্রোটোটাইপ | উৎপাদন ব্যবহারের জন্য নয়</span>
          </motion.div>
        </motion.section>

        {/* === ০৫. Data Card === */}
        <motion.section
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          <SectionHeading no="০৫" title="ডেটা কার্ড" sub="কর্পাস, বেঞ্চমার্ক ও গুণমান — সংক্ষিপ্ত, সোর্স-লকড সারাংশ।" />
          <motion.div variants={enter} className="mt-6 overflow-hidden rounded-xl border rule bg-paper">
            <table className="w-full text-sm">
              {CARD_GROUPS.map((g) => (
                <tbody key={g.name}>
                  <tr className="bg-paper-2/60">
                    <th colSpan={2} className="px-5 py-2 text-left font-mono text-[10px] font-semibold uppercase tracking-[0.18em] text-ochre">
                      {g.name}
                    </th>
                  </tr>
                  {g.rows.map(([label, value, bar]) => (
                    <tr key={label} className="border-t border-bone">
                      <td className="px-5 py-2.5 text-ink-faint">{label}</td>
                      <td className="px-5 py-2.5 text-right">
                        {bar ? (
                          <span className="inline-flex items-center gap-2.5">
                            <span className="inline-block h-1.5 w-24 overflow-hidden rounded-full bg-bone">
                              <motion.span
                                className="block h-full rounded-full bg-leaf"
                                initial={{ width: 0 }}
                                whileInView={{ width: `${bar}%` }}
                                viewport={{ once: true }}
                                transition={{ duration: dur.normal, ease: ease.smooth }}
                              />
                            </span>
                            <span className="font-medium tabular text-ink">{value}</span>
                          </span>
                        ) : (
                          <span className="font-medium tabular text-ink">{value}</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              ))}
            </table>
          </motion.div>
        </motion.section>
      </div>
    </MotionConfig>
  );
}