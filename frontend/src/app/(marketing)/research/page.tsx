"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import { motion, useInView } from "motion/react";
import { ArrowRight, BookOpen, Database, Shield, Copy, Check } from "lucide-react";
import { RESEARCH_STATS, RESEARCH_STATS_N, LINKS } from "@/lib/constants";
import { toBn, useCountUp } from "@/lib/use-count-up";
import { enter, stagger } from "@/lib/motion";

/* =========================================================================
   Research Overview — the "why we're better" page.
   This is where judges spend 2 minutes reading.
   Built entirely from paper data — no images needed.
   ========================================================================= */

const PAPERS = [
  {
    venue: "EACL 2026 — Data Resource & Benchmark Track",
    title: "KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory",
    summary: "৮৫,৯৭৯-ইনস্ট্যান্স বাংলা কৃষি বেঞ্চমার্ক, ৪ ট্র্যাক, রাসায়নিক প্রমাণ-অডিট, ১,০০০-কোয়েরি ফার্মার বেঞ্চমার্ক।",
    stats: [
      { label: "ইনস্ট্যান্স", value: RESEARCH_STATS.benchmarkInstances },
      { label: "ট্র্যাক", value: "৪" },
      { label: "ফার্মার কোয়েরি", value: RESEARCH_STATS.farmerQueries },
      { label: "নিরাপত্তা শ্রেণী", value: RESEARCH_STATS.safetyCategories },
    ],
    links: [
      { label: "Hugging Face", href: LINKS.huggingface },
    ],
    bibtex: `@misc{krishokchat2026,
  title = {KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory},
  year = {2026},
  note = {Authoritative copy: paper/done papers/KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf (TODO: add arXiv URL when available)}
}`,
  },
  {
    venue: "SIGIR-AP 2026",
    title: "AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval",
    summary: "২,৮৮২-নোড প্রমাণ-ভিত্তিক তথ্য-সংগ্রহ বেঞ্চমার্ক, ৫ আর্কিটেকচার, ৬ এম্বেডিং মডেল, রেজিস্টার-গ্যাপ আবিষ্কার।",
    stats: [
      { label: "নোড", value: RESEARCH_STATS.knowledgeNodes },
      { label: "এনটিটি", value: RESEARCH_STATS.entities },
      { label: "ট্রিপল", value: RESEARCH_STATS.triples },
      { label: "কোয়েরি", value: "৯০০" },
    ],
    links: [],
    bibtex: `@misc{agritrust2026,
  title = {AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval},
  year = {2026}
}`,
  },
];

/* Hallucination floor is a published range — kept as text; the rest count up */
const KEY_FINDINGS = [
  {
    value: RESEARCH_STATS.hallucinationFloor,
    label: "রাসায়নিক হ্যালুসিনেশন ফ্লোর",
    detail: "পরিপূর্ণ অরাকল তথ্য থাকা সত্ত্বেও এই হার থেকে যায় — সব মডেলে।",
  },
  {
    n: RESEARCH_STATS_N.sftGenF1,
    label: "ফাইন-টিউনড GenF1",
    detail: "বেস্ট জিরো-শট (০.১৬৫) থেকে ১.৯× উন্নত।",
  },
  {
    n: RESEARCH_STATS_N.hybridR10,
    label: "হাইব্রিড R@10",
    detail: "BM25+Dense ফিউশন সর্বোচ্চ নির্ভুলতা।",
  },
  {
    n: RESEARCH_STATS_N.interAnnotatorKappa,
    label: "ইন্টার-নির্দেশক κ",
    detail: "ফার্মার কোয়েরি গোল্ড ম্যাপিং নির্ভরযোগ্য।",
  },
];

const CONTRIBUTIONS = [
  "৮৫,৯৭৯-ইনস্ট্যান্স, ৪-ট্র্যাক বেঞ্চমার্ক — ২৮৪ সরকারি প্রকাশনা, ১৩ প্রতিষ্ঠান, ৬ উপভাষা",
  "প্রমাণ-সংরক্ষণকারী নির্মাণ পাইপলাইন — উত্তর নির্যাসিত, তৈরি নয়",
  "নিরাপত্তা-সচেতন ট্র্যাক পেয়ারিং — রাসায়নিক প্রমাণ-অডিট + ১২-শ্রেণী প্রত্যাখ্যান",
  "১,০০০-কোয়েরি রিয়েল-ওয়ার্ল্ড ফার্মার বেঞ্চমার্ক — ৩০০টি মাঠ সাক্ষাৎকার থেকে",
];

export default function ResearchPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-16 py-14">
      {/* === Hero === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="text-center"
      >
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          Research
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          প্রমাণ-ভিত্তিক <span className="text-leaf">বাংলা কৃষি এআই</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          ২৮৪ সরকারি প্রকাশনা, {RESEARCH_STATS.knowledgeNodes} জ্ঞান নোড, {RESEARCH_STATS.benchmarkInstances} মূল্যায়ন ইনস্ট্যান্স —
          দুটি গবেষণাপত্র, একটি লক্ষ্য: নিরাপদ ও নির্ভরযোগ্য কৃষি পরামর্শ।
        </motion.p>
        <motion.div variants={enter} className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/research/safety"
            className="group flex items-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
          >
            নিরাপত্তা নকশা দেখুন
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
          </Link>
          <Link
            href="/chat"
            className="rounded-lg border rule px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-leaf hover:text-leaf"
          >
            লাইভ ডেমো
          </Link>
        </motion.div>
      </motion.section>

      {/* === Key Findings — animated counters === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 text-center font-display text-2xl text-ink">
          মূল আবিষ্কার
        </motion.h2>
        <div className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone lg:grid-cols-4">
          {KEY_FINDINGS.map((finding) => (
            <FindingCell key={finding.label} finding={finding} />
          ))}
        </div>
      </motion.section>

      {/* === Two Papers === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
        className="space-y-6"
      >
        <motion.h2 variants={enter} className="text-center font-display text-2xl text-ink">
          গবেষণাপত্র
        </motion.h2>
        {PAPERS.map((paper, i) => (
          <motion.div
            key={i}
            variants={enter}
            className="rounded-xl border rule bg-paper p-6"
          >
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <BookOpen className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <div className="text-xs uppercase tracking-[0.14em] text-ochre">
                  {paper.venue}
                </div>
                <h3 className="mt-2 font-display text-lg leading-snug text-ink">
                  {paper.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-soft">{paper.summary}</p>

                {/* Paper stats */}
                <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                  {paper.stats.map((stat) => (
                    <div key={stat.label} className="rounded-md bg-paper-2/50 px-3 py-2 text-center">
                      <div className="font-display text-lg tabular text-leaf">{stat.value}</div>
                      <div className="text-[10px] font-medium text-ink-faint">
                        {stat.label}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Links */}
                {paper.links.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-3">
                    {paper.links.map((link) => (
                      <a
                        key={link.label}
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 rounded-md border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
                      >
                        {link.label}
                        <ArrowRight className="h-3 w-3" />
                      </a>
                    ))}
                    <BibTeXButton citation={paper.bibtex} />
                  </div>
                )}
                {paper.links.length === 0 && <div className="mt-4"><BibTeXButton citation={paper.bibtex} /></div>}
              </div>
            </div>
          </motion.div>
        ))}
      </motion.section>

      {/* === Contributions === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 text-center font-display text-2xl text-ink">
          অবদান
        </motion.h2>
        <motion.div variants={enter} className="space-y-3">
          {CONTRIBUTIONS.map((contrib, i) => (
            <div
              key={i}
              className="flex items-start gap-3 rounded-lg border rule bg-paper px-5 py-4"
            >
              <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-leaf/10 font-display text-sm text-leaf tabular">
                {i + 1}
              </span>
              <p className="text-sm leading-relaxed text-ink-soft">{contrib}</p>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* === Sub-page links === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="grid grid-cols-1 gap-4 sm:grid-cols-3"
      >
        {[
          { href: "/research/safety", icon: Shield, title: "নিরাপত্তা নকশা", desc: "এজেন্টিক পাইপলাইন অ্যানিমেশন" },
          { href: "/data", icon: Database, title: "উপাত্ত", desc: "জ্ঞান গ্রাফ ও নোড" },
          { href: "/team", icon: BookOpen, title: "দল", desc: "মাঠ পর্যায়ের কাজ" },
        ].map((card) => (
          <motion.div key={card.href} variants={enter}>
            <Link
              href={card.href}
              className="group flex items-center gap-4 rounded-xl border rule bg-paper p-5 transition-colors hover:border-leaf"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <card.icon className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="font-display text-base text-ink">{card.title}</div>
                <div className="text-xs text-ink-faint">{card.desc}</div>
              </div>
              <ArrowRight className="h-4 w-4 text-ink-faint transition-transform group-hover:translate-x-0.5 group-hover:text-leaf" />
            </Link>
          </motion.div>
        ))}
      </motion.section>
    </div>
  );
}

/* Count-up finding cell — numeric values tween when scrolled into view,
   range values (hallucination floor) render as verified text. */
function FindingCell({ finding }: { finding: (typeof KEY_FINDINGS)[number] }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });
  const n = useCountUp(finding.n ?? 0, inView);
  return (
    <motion.div variants={enter} ref={ref} className="bg-paper p-6 text-center">
      <div className="font-display text-3xl tabular text-leaf">
        {finding.n === undefined ? finding.value : toBn(n)}
      </div>
      <div className="mt-2 text-sm font-medium text-ink">{finding.label}</div>
      <div className="mt-1 text-xs leading-relaxed text-ink-faint">{finding.detail}</div>
    </motion.div>
  );
}

function BibTeXButton({ citation }: { citation: string }) {  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(citation);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  return (
    <button
      type="button"
      onClick={copy}
      className="flex min-h-10 items-center gap-1.5 rounded-md border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
      title="BibTeX কপি করুন"
    >
      {copied ? <Check className="h-3.5 w-3.5 text-leaf" /> : <Copy className="h-3.5 w-3.5" />}
      {copied ? "কপি হয়েছে" : "BibTeX কপি"}
    </button>
  );
}
