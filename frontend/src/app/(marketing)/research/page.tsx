"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import { motion, useInView } from "motion/react";
import { ArrowRight, BookOpen, Database, Shield, Copy, Check } from "lucide-react";
import { RESEARCH_STATS, RESEARCH_STATS_N, LINKS } from "@/lib/constants";
import { toLocaleCount, useCountUp } from "@/lib/use-count-up";
import { statLocale } from "@/lib/bn";
import { enter, stagger } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   Research Overview — the "why we're better" page.
   This is where judges spend 2 minutes reading.
   Built entirely from paper data — no images needed.
   ========================================================================= */

const PAPERS = [
  {
    venue: "EACL 2026 — Data Resource & Benchmark Track",
    title: "KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory",
    summary: {
      bn: "৮৫,৯৭৯-ইনস্ট্যান্স বাংলা কৃষি বেঞ্চমার্ক, ৪ ট্র্যাক, রাসায়নিক প্রমাণ-অডিট, ১,০০০-কোয়েরি ফার্মার বেঞ্চমার্ক।",
      en: "An 85,979-instance Bengali agricultural benchmark, 4 tracks, chemical provenance auditing, a 1,000-query farmer benchmark.",
    },
    stats: [
      { label: { bn: "ইনস্ট্যান্স", en: "Instances" }, value: RESEARCH_STATS.benchmarkInstances },
      { label: { bn: "ট্র্যাক", en: "Tracks" }, value: "৪" },
      { label: { bn: "ফার্মার কোয়েরি", en: "Farmer Queries" }, value: RESEARCH_STATS.farmerQueries },
      { label: { bn: "নিরাপত্তা শ্রেণী", en: "Safety Categories" }, value: RESEARCH_STATS.safetyCategories },
    ],
    links: [
      { label: "Hugging Face", href: LINKS.huggingface },
    ],
    bibtex: `@misc{krishokchat2026,
  title = {KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory},
  year = {2026},
  note = {Preprint in review; manuscript artifact: paper/done papers/KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf}
}`,
  },
  {
    venue: "SIGIR-AP 2026",
    title: "AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval",
    summary: {
      bn: "২,৮৮২-নোড প্রমাণ-ভিত্তিক তথ্য-সংগ্রহ বেঞ্চমার্ক, ৫ আর্কিটেকচার, ৬ এম্বেডিং মডেল, রেজিস্টার-গ্যাপ আবিষ্কার।",
      en: "A 2,882-node provenance-grounded retrieval benchmark, 5 architectures, 6 embedding models, a register-gap discovery.",
    },
    stats: [
      { label: { bn: "নোড", en: "Nodes" }, value: RESEARCH_STATS.knowledgeNodes },
      { label: { bn: "এনটিটি", en: "Entities" }, value: RESEARCH_STATS.entities },
      { label: { bn: "ট্রিপল", en: "Triples" }, value: RESEARCH_STATS.triples },
      { label: { bn: "কোয়েরি", en: "Queries" }, value: "৯০০" },
    ],
    links: [],
    bibtex: `@misc{agritrust2026,
  title = {AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval},
  year = {2026}
}`,
  },
] as const;

/* Hallucination floor is a published range — kept as text; the rest count up */
const KEY_FINDINGS = [
  {
    value: RESEARCH_STATS.hallucinationFloor,
    label: { bn: "রাসায়নিক হ্যালুসিনেশন ফ্লোর", en: "Chemical Hallucination Floor" },
    detail: {
      bn: "পরিপূর্ণ সঠিক নথিপত্র থাকা সত্ত্বেও জেনারেটিভ মডেলগুলোতে ৪-৭% রাসায়নিক ভুলের ঝুঁকি থাকে — যা ভেরিফায়ার দ্বারা প্রতিরোধ করা আবশ্যক।",
      en: "Even with perfectly correct source documents, generative models carry a 4–7% risk of chemical errors — which a verifier must prevent.",
    },
  },
  {
    n: RESEARCH_STATS_N.sftGenF1,
    label: { bn: "ফাইন-টিউনড Gen-F1", en: "Fine-Tuned Gen-F1" },
    detail: {
      bn: "প্রমিত কৃষি নির্দেশিকায় ফাইন-টিউনিংয়ের মাধ্যমে জিরো-শট মডেল (০.১৬৫) থেকে ১.৯ গুণ বেশি নির্ভরযোগ্য উত্তর প্রস্তুত।",
      en: "Fine-tuning on standard agricultural guidelines produces 1.9x more reliable answers than the zero-shot model (0.165).",
    },
  },
  {
    n: RESEARCH_STATS_N.hybridR10,
    label: { bn: "হাইব্রিড রিট্রিভাল (R@10)", en: "Hybrid Retrieval (R@10)" },
    detail: {
      bn: "BM25 শব্দ মিল ও ডেন্স ভেক্টর এম্বেডিংয়ের হাইব্রিড RRF ফিউশনে ৫৩.৯% সর্বোচ্চ তথ্য সংগ্রহের নির্ভুলতা।",
      en: "A hybrid RRF fusion of BM25 keyword matching and dense vector embeddings reaches 53.9% top retrieval accuracy.",
    },
  },
  {
    n: RESEARCH_STATS_N.interAnnotatorKappa,
    label: { bn: "বিশেষজ্ঞ সম্মতি সূচক (κ)", en: "Expert Agreement Index (κ)" },
    detail: {
      bn: "মাঠ পর্যায়ের কৃষক প্রশ্ন ও বিশেষজ্ঞ কৃষি কর্মকর্তাদের মধ্যে ০.৭২ উচ্চমাত্রার নির্ভরযোগ্য সম্মতি।",
      en: "A high, reliable agreement of 0.72 between field-level farmer questions and expert agriculture officers.",
    },
  },
];

const CONTRIBUTIONS = [
  {
    bn: "৮৫,৯৭৯ বেঞ্চমার্ক প্রশ্নোত্তর — ২৮৪টি সরকারি প্রকাশনা, ১৩টি গবেষণা প্রতিষ্ঠান ও ৬টি আঞ্চলিক উপভাষার সমন্বয়।",
    en: "85,979 benchmark Q&A pairs — combining 284 government publications, 13 research institutions, and 6 regional dialects.",
  },
  {
    bn: "প্রমাণ-ভিত্তিক এক্সট্রাকশন পাইপলাইন — কোনো অনুমাননির্ভর তথ্য নয়, প্রতিটি উত্তর সরাসরি উৎস নথিপত্র থেকে নিষ্কাশিত।",
    en: "A provenance-grounded extraction pipeline — no guesswork; every answer is extracted directly from a source document.",
  },
  {
    bn: "নিরাপত্তা ও গার্ডরেইল স্তর — ১২-শ্রেণির ঝুঁকি শনাক্তকরণ এবং ক্ষতিকর বা নিষিদ্ধ কীটনাশক প্রত্যাখ্যান ফ্রেমওয়ার্ক।",
    en: "A safety and guardrail layer — 12-category risk detection and a framework for rejecting harmful or banned pesticides.",
  },
  {
    bn: "১,০০০টি বাস্তব কৃষক প্রশ্নের বেঞ্চমার্ক — রাজশাহী ও নাটোরের ৩০০ জন কৃষকের মাঠ সাক্ষাৎকার থেকে কিউরেটেড।",
    en: "A benchmark of 1,000 real farmer questions — curated from field interviews with 300 farmers in Rajshahi and Natore.",
  },
] as const;

const SUBPAGE_LINKS = [
  { href: "/research/safety", icon: Shield, title: { bn: "নিরাপত্তা কাঠামো", en: "Safety Framework" }, desc: { bn: "মাল্টি-এজেন্ট গার্ডরেইল ও ভেরিফায়ার", en: "Multi-agent guardrails and verifier" } },
  { href: "/data", icon: Database, title: { bn: "উপাত্ত ও নলেজ গ্রাফ", en: "Data and Knowledge Graph" }, desc: { bn: "জ্ঞানভাণ্ডার নোড ও ওপেন ডেটাসেট", en: "Knowledge base nodes and open datasets" } },
  { href: "/team", icon: BookOpen, title: { bn: "গবেষক দল", en: "Research Team" }, desc: { bn: "মাঠ পর্যায়ের কাজ ও পরিচিতি", en: "Field work and introduction" } },
] as const;

export default function ResearchPage() {
  const { locale } = useLanguage();
  const en = locale === "en";
  return (
    <div className="mx-auto max-w-4xl space-y-16 py-14">
      {/* === Hero === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="text-center"
      >
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre font-semibold">
          {en ? "RESEARCH BRIEF" : "গবেষণা সারসংক্ষেপ · RESEARCH BRIEF"}
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink sm:text-5xl">
          {en ? (
            <>Evidence-Grounded and Safe <span className="text-leaf">Bengali Agricultural AI</span></>
          ) : (
            <>প্রমাণভিত্তিক ও নিরাপদ <span className="text-leaf">বাংলা কৃষি এআই</span></>
          )}
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-ink-soft">
          {en
            ? `284 government publications, ${statLocale(RESEARCH_STATS.knowledgeNodes, en)} knowledge base nodes, ${statLocale(RESEARCH_STATS.benchmarkInstances, en)} evaluation Q&A pairs — two papers, one goal: a safe and reliable AI advisor for farmers.`
            : `২৮৪টি সরকারি প্রকাশনা, ${RESEARCH_STATS.knowledgeNodes}টি জ্ঞানভাণ্ডার নোড, ${RESEARCH_STATS.benchmarkInstances}টি মূল্যায়ন প্রশ্নোত্তর — দুটি গবেষণাপত্র, একটিই লক্ষ্য: কৃষকের জন্য নিরাপদ ও নির্ভরযোগ্য এআই পরামর্শদাতা।`}
        </motion.p>
        <motion.div variants={enter} className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/research/safety"
            className="group flex items-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
          >
            {en ? "View the safety framework" : "নিরাপত্তা ফ্রেমওয়ার্ক দেখুন"}
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
          </Link>
          <Link
            href="/chat"
            className="rounded-lg border rule px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-leaf hover:text-leaf"
          >
            {en ? "Live advisory demo" : "লাইভ পরামর্শ ডেমো"}
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
          {en ? "Key Research Findings and Results" : "গবেষণার মূল পর্যবেক্ষণ ও ফলাফল"}
        </motion.h2>
        <div className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone lg:grid-cols-4">
          {KEY_FINDINGS.map((finding) => (
            <FindingCell key={finding.label.en} finding={finding} />
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
          {en ? "Published Papers" : "প্রকাশিত গবেষণাপত্রসমূহ"}
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
                <div className="text-xs uppercase tracking-[0.14em] text-ochre font-semibold">
                  {paper.venue}
                </div>
                <h3 className="mt-2 font-display text-lg leading-snug text-ink">
                  {paper.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-soft">{en ? paper.summary.en : paper.summary.bn}</p>

                {/* Paper stats */}
                <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                  {paper.stats.map((stat) => (
                    <div key={stat.label.en} className="rounded-md bg-paper-2/50 px-3 py-2 text-center">
                      <div className="font-display text-lg tabular text-leaf">{statLocale(stat.value, en)}</div>
                      <div className="text-[10px] font-medium text-ink-faint">
                        {en ? stat.label.en : stat.label.bn}
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
          {en ? "Core Research Contributions" : "গবেষণার মৌলিক অবদান"}
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
              <p className="text-sm leading-relaxed text-ink-soft">{en ? contrib.en : contrib.bn}</p>
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
        {SUBPAGE_LINKS.map((card) => (
          <motion.div key={card.href} variants={enter}>
            <Link
              href={card.href}
              className="group flex items-center gap-4 rounded-xl border rule bg-paper p-5 transition-all hover:border-leaf hover:shadow-xs"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <card.icon className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="font-display text-base text-ink group-hover:text-leaf">{en ? card.title.en : card.title.bn}</div>
                <div className="text-xs text-ink-faint">{en ? card.desc.en : card.desc.bn}</div>
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
  const { locale } = useLanguage();
  const en = locale === "en";
  return (
    <motion.div variants={enter} ref={ref} className="bg-paper p-6 text-center">
      <div className="font-display text-3xl tabular text-leaf">
        {finding.n === undefined ? statLocale(finding.value ?? "", en) : toLocaleCount(n, en)}
      </div>
      <div className="mt-2 text-sm font-medium text-ink">{en ? finding.label.en : finding.label.bn}</div>
      <div className="mt-1 text-xs leading-relaxed text-ink-faint">{en ? finding.detail.en : finding.detail.bn}</div>
    </motion.div>
  );
}

function BibTeXButton({ citation }: { citation: string }) {
  const [copied, setCopied] = useState(false);
  const { locale } = useLanguage();
  const en = locale === "en";

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
      title={en ? "Copy BibTeX" : "BibTeX কপি করুন"}
    >
      {copied ? <Check className="h-3.5 w-3.5 text-leaf" /> : <Copy className="h-3.5 w-3.5" />}
      {copied ? (en ? "Copied" : "কপি হয়েছে") : (en ? "Copy BibTeX" : "BibTeX কপি")}
    </button>
  );
}
