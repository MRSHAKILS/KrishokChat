"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Database, ExternalLink, ChevronDown, Tag, FileText, Boxes } from "lucide-react";
import { RESEARCH_STATS, LINKS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Data & Dataset Page — shows the knowledge base as a tangible resource.

   Sections:
   A. Dataset overview (stat cards)
   B. Knowledge graph visualization (image + category breakdown)
   C. Sample knowledge node (interactive expandable JSON)
   D. Source institutions
   E. Dataset access (links)
   F. Data card summary
   ========================================================================= */

const NODE_CATEGORIES = [
  { name: "Variety", bn: "জাত", count: 695 },
  { name: "Cultivation Practice", bn: "চাষ পদ্ধতি", count: 570 },
  { name: "Disease", bn: "রোগ", count: 430 },
  { name: "Pest", bn: "পোকা", count: 380 },
  { name: "Fertilizer", bn: "সার", count: 280 },
  { name: "Other", bn: "অন্যান্য", count: 527 },
];

const SAMPLE_NODE = {
  id: "DAE_PEST_1206A0_001",
  title_bn: "আলুর দেরি ব্লাইট",
  title_en: "Potato Late Blight",
  category: "disease",
  publisher: "DAE",
  source_document: "Potato Disease Manuals (Plantwise)",
  citation: "DAE. Late blight. Potato Disease Manuals. p. 852.",
  content_bn:
    "আলুর দেরি ব্লাইট (Late Blight) একটি মারাত্মক ছত্রাকজনিত রোগ যা Phytophthora infestans দ্বারা সৃষ্ট। এটি পাতার ও কান্ডের নিচে ছোট ছোট সবুজ-বাদামি দাগ হিসেবে শুরু হয়।",
  entities: ["Phytophthora infestans", "potato", "late blight"],
  chemical_trace: ["Mancozeb 80WP", "Metalaxyl"],
};

const DATASET_STATS = [
  { value: RESEARCH_STATS.knowledgeNodes, label: "জ্ঞান নোড", icon: Boxes },
  { value: RESEARCH_STATS.entities, label: "এনটিটি", icon: Tag },
  { value: RESEARCH_STATS.triples, label: "ফ্যাক্টুয়াল ট্রিপল", icon: Database },
  { value: "১,০২২", label: "ইমেজ-লিঙ্কড নোড", icon: FileText },
  { value: "৯১৫", label: "অনন্য ফসল", icon: Tag },
  { value: "৭০৪", label: "রোগ ভ্যারিয়েন্ট", icon: Tag },
  { value: "২,৭২৯", label: "রাসায়নিক এনটিটি", icon: Tag },
  { value: RESEARCH_STATS.publications, label: "সোর্স PDF", icon: FileText },
];

export default function DataPage() {
  const [nodeOpen, setNodeOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  return (
    <div className="mx-auto max-w-4xl space-y-16 py-14">
      {/* === A. Hero === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="text-center"
      >
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          Knowledge Base & Dataset
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          জ্ঞান গ্রাফ <span className="text-leaf">ও উপাত্ত</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          {RESEARCH_STATS.publications}টি সরকারি প্রকাশনা থেকে নির্মিত {RESEARCH_STATS.knowledgeNodes}টি জ্ঞান নোড —
          প্রমাণ-ভিত্তিক, উৎস-লকড, প্রতিটি ট্রেসযোগ্য।
        </motion.p>
      </motion.section>

      {/* === B. Dataset Stats === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          উপাত্ত পরিসংখ্যান
        </motion.h2>
        <div className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
          {DATASET_STATS.map((stat) => (
            <motion.div key={stat.label} variants={enter} className="bg-paper p-5 text-center">
              <stat.icon className="mx-auto h-5 w-5 text-leaf" />
              <div className="mt-3 font-display text-2xl tabular text-ink">{stat.value}</div>
              <div className="mt-1 text-[10px] font-medium text-ink-faint">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === C. Knowledge Graph Visualization === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          জ্ঞান গ্রাফ
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          ১৩-ক্যাটাগরি কৃষি ট্যাক্সোনমি — জাত, চাষ, রোগ, পোকা, সার থেকে খাদ্য নিরাপত্তা পর্যন্ত।
        </motion.p>

        {/* Graph image */}
        <motion.div variants={enter} className="overflow-hidden rounded-xl border rule">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/assets/knowledge_graph_gpt.jpg"
            alt="জ্ঞান গ্রাফ ভিজ্যুয়ালাইজেশন"
            className="w-full object-cover"
          />
        </motion.div>

        {/* Category breakdown — interactive */}
        <motion.div variants={enter} className="mt-6 space-y-2">
          <div className="mb-2 text-xs font-semibold text-ochre">
            ক্যাটাগরি অনুযায়ী নোড
          </div>
          {NODE_CATEGORIES.map((cat, i) => (
            <button
              key={cat.name}
              onClick={() => setSelectedCategory(selectedCategory === cat.name ? null : cat.name)}
              className="flex w-full items-center gap-3"
            >
              <div className="w-32 shrink-0 text-left">
                <div className="text-sm font-medium text-ink">{cat.bn}</div>
                <div className="font-mono text-[10px] text-ink-faint">{cat.name}</div>
              </div>
              <div className="relative h-6 flex-1 overflow-hidden rounded-md bg-bone">
                <motion.div
                  className="absolute inset-y-0 left-0 rounded-md bg-leaf"
                  initial={{ width: 0 }}
                  whileInView={{ width: `${(cat.count / 695) * 100}%` }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1, duration: dur.slow, ease: ease.smooth }}
                />
                <span className="relative flex items-center px-2 text-xs font-medium tabular text-ink">
                  {cat.count}
                </span>
              </div>
            </button>
          ))}
        </motion.div>

        <AnimatePresence>
          {selectedCategory && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 overflow-hidden rounded-lg border rule bg-paper-2/40 px-4 py-3 text-sm text-ink-soft"
            >
              <span className="font-medium text-ink">{selectedCategory}</span> ক্যাটাগরিতে সম্পর্কিত জ্ঞান নোড রয়েছে।
              প্রতিটি নোড একটি সরকারি প্রকাশনার নির্দিষ্ট পৃষ্ঠা থেকে নির্যাসিত — উৎস আইডি ও পৃষ্ঠা নম্বরসহ।
            </motion.div>
          )}
        </AnimatePresence>
      </motion.section>

      {/* === D. Sample Knowledge Node (interactive) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          নমুনা জ্ঞান নোড
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          একটি বাস্তব জ্ঞান নোড — প্রমাণ-লকড, উৎস-ট্রেসযোগ্য, রাসায়নিক-অডিটযোগ্য।
        </motion.p>

        <motion.div variants={enter} className="rounded-xl border rule bg-paper">
          {/* Header */}
          <button
            onClick={() => setNodeOpen((v) => !v)}
            className="flex w-full items-center justify-between px-5 py-4 text-left"
          >
            <div className="flex-1">
              <div className="font-mono text-xs text-ink-faint">{SAMPLE_NODE.id}</div>
              <div className="mt-1 font-display text-lg text-ink">{SAMPLE_NODE.title_bn}</div>
              <div className="text-sm text-ochre">{SAMPLE_NODE.title_en}</div>
            </div>
            <ChevronDown
              className={`h-5 w-5 shrink-0 text-ink-faint transition-transform ${nodeOpen ? "rotate-180" : ""}`}
            />
          </button>

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
                  {/* Metadata */}
                  <div className="grid grid-cols-2 gap-3 text-xs">
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

                  {/* Content */}
                  <div>
                    <div className="text-xs text-ink-faint">কনটেন্ট (বাংলা)</div>
                    <p className="mt-1 text-sm leading-relaxed text-ink-soft">{SAMPLE_NODE.content_bn}</p>
                  </div>

                  {/* Entities */}
                  <div>
                    <div className="text-xs text-ink-faint">এনটিটি</div>
                    <div className="mt-1 flex flex-wrap gap-1.5">
                      {SAMPLE_NODE.entities.map((entity) => (
                        <span
                          key={entity}
                          className="rounded-md bg-leaf/10 px-2 py-0.5 font-mono text-[11px] text-leaf"
                        >
                          {entity}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Chemical trace */}
                  <div>
                    <div className="text-xs text-ink-faint">রাসায়নিক ট্রেস</div>
                    <div className="mt-1 flex flex-wrap gap-1.5">
                      {SAMPLE_NODE.chemical_trace.map((chem) => (
                        <span
                          key={chem}
                          className="rounded-md bg-clay-soft/20 px-2 py-0.5 font-mono text-[11px] text-clay"
                        >
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

      {/* === E. Dataset Access === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          উপাত্ত অ্যাক্সেস
        </motion.h2>
        <motion.div variants={enter} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {/* Hugging Face */}
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

          {/* arXiv */}
          <a
            href={LINKS.arxiv}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-4 rounded-xl border rule bg-paper p-5 transition-colors hover:border-leaf"
          >
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
              <FileText className="h-6 w-6" />
            </div>
            <div className="flex-1">
              <div className="font-display text-base text-ink">arXiv</div>
              <div className="text-xs text-ink-faint">2606.29243</div>
            </div>
            <ExternalLink className="h-4 w-4 text-ink-faint transition-colors group-hover:text-leaf" />
          </a>
        </motion.div>

        {/* License */}
        <motion.div variants={enter} className="mt-4 rounded-lg border rule bg-paper-2/40 px-5 py-3 text-center text-xs text-ink-faint">
          লাইসেন্স: CC-BY-4.0 | গবেষণা প্রোটোটাইপ | উৎপাদন ব্যবহারের জন্য নয়
        </motion.div>
      </motion.section>

      {/* === F. Data Card Summary === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="rounded-xl border rule bg-paper p-6"
      >
        <motion.h2 variants={enter} className="mb-4 font-display text-xl text-ink">
          ডেটা কার্ড
        </motion.h2>
        <motion.div variants={enter} className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
          {[
            ["সোর্স PDF", RESEARCH_STATS.publications],
            ["প্রতিষ্ঠান", RESEARCH_STATS.institutions],
            ["জ্ঞান নোড", RESEARCH_STATS.knowledgeNodes],
            ["ইমেজ-লিঙ্কড নোড", "১,০২২ (৩৫.৫%)"],
            ["এনটিটি", RESEARCH_STATS.entities],
            ["ট্রিপল", RESEARCH_STATS.triples],
            ["অনন্য ফসল", "৯১৫"],
            ["রোগ ভ্যারিয়েন্ট", "৭০৪"],
            ["কোয়েরি (মোট)", "১,০০০"],
            ["কোয়েরি (মূল্যায়নযোগ্য)", "৯০০"],
            ["κ (ফার্মার+নিরাপত্তা)", RESEARCH_STATS.interAnnotatorKappa],
            ["κ (KG-grounded)", "০.৭৮"],
          ].map(([key, value]) => (
            <div key={key} className="flex justify-between border-b border-bone pb-2">
              <span className="text-ink-faint">{key}</span>
              <span className="font-medium tabular text-ink">{value}</span>
            </div>
          ))}
        </motion.div>
      </motion.section>
    </div>
  );
}
