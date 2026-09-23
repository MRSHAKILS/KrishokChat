"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { FileText, Layers, Lock, Snowflake, GitBranch, ShieldCheck, Search, PenLine, CheckCircle2, ChevronDown } from "lucide-react";
import { RESEARCH_STATS } from "@/lib/constants";
import { statLocale, numLocale } from "@/lib/bn";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   Methodology Page — shows how 284 PDFs became 85,979 benchmark instances.
   The construction pipeline, the 4 tracks, design principles, and
   knowledge node construction from the AgriTrust paper.

   No images needed — built entirely with animated HTML/SVG/Motion.
   ========================================================================= */

const PIPELINE_STAGES = [
  { value: RESEARCH_STATS.publications, label: { bn: "সরকারি PDF প্রকাশনা", en: "Government PDF Publications" }, detail: { bn: "১৩টি জাতীয় প্রতিষ্ঠান থেকে", en: "From 13 national institutions" } },
  { value: "২,৬৮০", label: { bn: "সেকশন প্যাসেজ", en: "Section Passages" }, detail: { bn: "উন্নত OCR ও লেআউট রূপান্তর", en: "Advanced OCR and layout conversion" } },
  { value: "২,৯৪৬", label: { bn: "সিম্যান্টিক ইউনিট", en: "Semantic Units" }, detail: { bn: "হেডার-ভিত্তিক অর্থপূর্ণ খণ্ডায়ন", en: "Header-based meaningful chunking" } },
  { value: RESEARCH_STATS.benchmarkInstances, label: { bn: "বেঞ্চমার্ক প্রশ্নোত্তর", en: "Benchmark Q&A Pairs" }, detail: { bn: "মাল্টি-টাস্ক কোয়ালিটি গেট পাস", en: "Passed the multi-task quality gate" } },
  { value: "৪", label: { bn: "মূল্যায়ন ট্র্যাক", en: "Evaluation Tracks" }, detail: { bn: "স্বতন্ত্র কৃষি ডোমেইন", en: "Distinct agricultural domains" } },
] as const;

const TRACKS = [
  {
    name: { bn: "সাধারণ কৃষি জ্ঞান QA", en: "General Agricultural Knowledge QA" },
    en: "General Knowledge QA",
    count: "২৮,৯৯৩",
    desc: { bn: "রাসায়নিক-মুক্ত সাধারণ কৃষি পদ্ধতি", en: "Chemical-free general agricultural practices" },
    detail: { bn: "চাষাবাদ, জাত নির্বাচন, সেচ ও ফসল সংগ্রহোত্তর ব্যবস্থাপনা", en: "Cultivation, variety selection, irrigation, and post-harvest management" },
  },
  {
    name: { bn: "বালাই ও রোগ নিরাময় QA", en: "Pest and Disease Treatment QA" },
    en: "Treatment & Disease QA",
    count: "১১,২২৪",
    desc: { bn: "নিরাপত্তা-সংবেদনশীল রাসায়নিক ও জৈব পরামর্শ", en: "Safety-sensitive chemical and organic advice" },
    detail: { bn: "৭,৪৩৭টি (৬৬.৩%) সুনির্দিষ্ট রাসায়নিক ট্রেস বহনকারী", en: "7,437 (66.3%) carry a specific chemical trace" },
  },
  {
    name: { bn: "নিরাপত্তা ও প্রত্যাখ্যান QA", en: "Safety and Refusal QA" },
    en: "Safety Refusal & Re-query",
    count: "২০,১১২",
    desc: { bn: "১২-শ্রেণির ঝুঁকি প্রত্যাখ্যান ও স্পষ্টীকরণ প্রশ্ন", en: "12-category risk refusal and clarification questions" },
    detail: { bn: "৩,২১৬টি টার্মিনাল রিফিউজাল ও ১৬,৮৯৬টি রি-কোয়েরি পেয়ার", en: "3,216 terminal refusals and 16,896 re-query pairs" },
  },
  {
    name: { bn: "সারণিভিত্তিক যুক্তি QA", en: "Table Reasoning QA" },
    en: "Table Reasoning QA",
    count: "২৫,৬৫০",
    desc: { bn: "৩-স্তরের কাঠামোগত ডেটা রিজনিং", en: "3-tier structured data reasoning" },
    detail: { bn: "L1 লুকআপ + L2 সারি যুক্তি + L3 সমষ্টিগত হিসাব", en: "L1 lookup + L2 row reasoning + L3 aggregate computation" },
  },
] as const;

const PRINCIPLES = [
  {
    icon: FileText,
    title: { bn: "উত্তর সরাসরি নথি থেকে নির্যাসিত", en: "Answers Extracted Directly From Documents" },
    en: "Answers extracted, never synthesized",
    desc: { bn: "রেফারেন্স উত্তর সরাসরি সরকারি নথিপত্র থেকে নিষ্কাশিত — কোনো মনগড়া তথ্য বা কৃত্রিম টেক্সট যোগ করা হয় না।", en: "Reference answers are extracted directly from government documents — no fabricated information or synthetic text is added." },
  },
  {
    icon: Layers,
    title: { bn: "ভাষাগত বৈচিত্র্য নমুনায়িত", en: "Linguistic Diversity Sampled" },
    en: "Diversity sampled, not templated",
    desc: { bn: "প্রশ্নগুলো আঞ্চলিক উপভাষা, কৃষকের পার্সোনা ও বিভিন্ন ব্যবহারিক বাস্তবতার ম্যাট্রিক্স থেকে স্যাম্পল করা।", en: "Questions are sampled from a matrix of regional dialects, farmer personas, and varied practical realities." },
  },
  {
    icon: Snowflake,
    title: { bn: "ডোজ ও রাসায়নিক নাম সম্পূর্ণ সুরক্ষিত", en: "Dosage and Chemical Names Fully Protected" },
    en: "Content tokens frozen across dialects",
    desc: { bn: "সব উপভাষার ক্ষেত্রেই কীটনাশকের নাম, ডোজ, একক ও সংখ্যা অপরিবর্তিত রাখা হয় — যাতে কোনো কৃষক ভুল পরামর্শ না পান।", en: "Pesticide names, dosages, units, and numbers are kept unchanged across every dialect — so no farmer receives incorrect advice." },
  },
  {
    icon: Lock,
    title: { bn: "প্রতিটি প্রশ্নোত্তর সোর্স-লকড", en: "Every Instance Is Provenance-Locked" },
    en: "Each instance provenance-locked",
    desc: { bn: "প্রতিটি রেকর্ডের সাথে মূল নথির নাম, প্রকাশক ও পৃষ্ঠা নম্বর স্থায়ীভাবে যুক্ত — ফলে যেকোনো উত্তর পুনরায় অডিট করা সম্ভব।", en: "The source document's name, publisher, and page number are permanently attached to every record — so any answer can be re-audited." },
  },
] as const;

const NODE_CONSTRUCTION = [
  { step: 1, label: { bn: "PDF → Markdown", en: "PDF → Markdown" }, detail: { bn: "Mistral OCR, লেআউট সংরক্ষণ", en: "Mistral OCR, layout preserved" } },
  { step: 2, label: { bn: "টপিক খণ্ডায়ন", en: "Topic Chunking" }, detail: { bn: "২,৮৮২ টপিক-কোহেরেন্ট নোড", en: "2,882 topic-coherent nodes" } },
  { step: 3, label: { bn: "এনটিটি নিষ্কাশন", en: "Entity Extraction" }, detail: { bn: "১৯,৭৬৮ এনটিটি (৬.৯/নোড)", en: "19,768 entities (6.9/node)" } },
  { step: 4, label: { bn: "ট্রিপল নিষ্কাশন", en: "Triple Extraction" }, detail: { bn: "১৭,৫০১ ফ্যাক্টুয়াল ট্রিপল", en: "17,501 factual triples" } },
  { step: 5, label: { bn: "প্রমাণ ইনজেকশন", en: "Provenance Injection" }, detail: { bn: "ডিটারমিনিস্টিক, LLM-বিহীন", en: "Deterministic, no LLM" } },
  { step: 6, label: { bn: "ক্রস-ভেরিফিকেশন", en: "Cross-Verification" }, detail: { bn: "GPT-5-Nano দ্বারা যাচাই", en: "Verified by GPT-5-Nano" } },
  { step: 7, label: { bn: "ক্লোজড-লুপ পরিমার্জন", en: "Closed-Loop Refinement" }, detail: { bn: "২৮৩ নোড (৯.৮%) পুনরায় তৈরি", en: "283 nodes (9.8%) regenerated" } },
] as const;

const AGENT_STEPS = [
  {
    id: "safety",
    label: { bn: "নিরাপত্তা / রাউটার", en: "Safety / Router" },
    short: { bn: "প্রথমে প্রশ্ন যাচাই", en: "The question is checked first" },
    icon: ShieldCheck,
    detail: { bn: "নিরাপত্তা শ্রেণী নির্ধারণ করে। safe_agri না হলে তথ্য সংগ্রহ শুরু হয় না।", en: "Determines the safety category. Retrieval does not begin unless the result is safe_agri." },
    contract: { bn: "SafetyClassifier.classify → terminal outcome বা safe_agri", en: "SafetyClassifier.classify → terminal outcome or safe_agri" },
  },
  {
    id: "retrieval",
    label: { bn: "তথ্য সংগ্রহ", en: "Retrieval" },
    short: { bn: "প্রমাণ খোঁজা", en: "Finding evidence" },
    icon: Search,
    detail: { bn: "প্রি-কম্পিউটেড কৃষি জ্ঞানভাণ্ডার থেকে প্রাসঙ্গিক উৎস খোঁজা হয়।", en: "Relevant sources are found from the pre-computed agricultural knowledge base." },
    contract: { bn: "Retriever.retrieve → উৎস-সহ প্রাসঙ্গিক জ্ঞান নোড", en: "Retriever.retrieve → relevant knowledge nodes with sources" },
  },
  {
    id: "generation",
    label: { bn: "উত্তর তৈরি", en: "Generation" },
    short: { bn: "উৎস-ভিত্তিক উত্তর", en: "A source-grounded answer" },
    icon: PenLine,
    detail: { bn: "পাওয়া উৎসের ভিত্তিতে বাংলায় উত্তর তৈরি হয়; অনুমানভিত্তিক উত্তর নয়।", en: "The answer is written in Bengali based on the retrieved sources; never a guessed answer." },
    contract: { bn: "GenerationModel.generate → grounded Bengali answer", en: "GenerationModel.generate → grounded Bengali answer" },
  },
  {
    id: "verifier",
    label: { bn: "যাচাই", en: "Verifier" },
    short: { bn: "দাবি মিলিয়ে দেখা", en: "Checking claims against sources" },
    icon: CheckCircle2,
    detail: { bn: "উত্তরের দাবি ও মাত্রা উৎসের সাথে মিলিয়ে দেখা হয়; অনিশ্চয়তা থাকলে সতর্কতা যোগ হয়।", en: "The answer's claims and dosages are checked against the sources; a caution is added if there is uncertainty." },
    contract: { bn: "Verifier.verify → verified, flagged-unverified বা controlled referral", en: "Verifier.verify → verified, flagged-unverified, or controlled referral" },
  },
] as const;

export default function MethodologyPage() {
  const { locale } = useLanguage();
  const en = locale === "en";
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
          Construction Methodology
        </motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          {en ? (
            <>Provenance-Preserving <span className="text-leaf">Construction Pipeline</span></>
          ) : (
            <>প্রমাণ-সংরক্ষণকারী <span className="text-leaf">নির্মাণ পাইপলাইন</span></>
          )}
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-ink-soft">
          {en ? (
            <>{statLocale(RESEARCH_STATS.publications, en)} government publications to {statLocale(RESEARCH_STATS.benchmarkInstances, en)} evaluation instances —
            every stage preserves provenance, every answer is traceable back to its source.</>
          ) : (
            <>{RESEARCH_STATS.publications}টি সরকারি প্রকাশনা থেকে {RESEARCH_STATS.benchmarkInstances}টি মূল্যায়ন ইনস্ট্যান্স —
            প্রতিটি ধাপ প্রমাণ-সংরক্ষণকারী, প্রতিটি উত্তর উৎসে ফিরে যাচাইযোগ্য।</>
          )}
        </motion.p>
      </motion.section>

      <AgentPipelineExplorer />

      {/* === A. Construction Pipeline (animated) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 text-center font-display text-2xl text-ink">
          {en ? "Construction Pipeline" : "নির্মাণ পাইপলাইন"}
        </motion.h2>
        <motion.p variants={enter} className="mb-8 text-center text-sm text-ink-soft">
          {en ? "284 PDFs to 85,979 instances, in 5 stages." : "৫ ধাপে ২৮৪টি PDF থেকে ৮৫,৯৭৯টি ইনস্ট্যান্স।"}
        </motion.p>

        {/* Horizontal pipeline on desktop, vertical on mobile */}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-stretch sm:justify-between">
          {PIPELINE_STAGES.map((stage, i) => (
            <div key={i} className="flex flex-1 flex-col items-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15, duration: dur.normal, ease: ease.smooth }}
                className="flex w-full flex-col items-center rounded-lg border rule bg-paper px-3 py-4 text-center"
              >
                <div className="font-display text-2xl tabular text-leaf">{statLocale(stage.value, en)}</div>
                <div className="mt-1 text-xs font-medium text-ink">{en ? stage.label.en : stage.label.bn}</div>
                <div className="mt-0.5 text-[10px] leading-tight text-ink-faint">{en ? stage.detail.en : stage.detail.bn}</div>
              </motion.div>
              {/* Arrow connector */}
              {i < PIPELINE_STAGES.length - 1 && (
                <motion.div
                  initial={{ opacity: 0, scaleX: 0 }}
                  whileInView={{ opacity: 1, scaleX: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.15 + 0.1, duration: dur.normal }}
                  className="my-2 text-leaf sm:my-0 sm:mx-1"
                >
                  <div className="hidden sm:block">→</div>
                  <div className="sm:hidden">↓</div>
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </motion.section>

      {/* === B. The 4 Tracks === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          {en ? "4 Tracks" : "৪ ট্র্যাক"}
        </motion.h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {TRACKS.map((track, i) => (
            <motion.div
              key={i}
              variants={enter}
              className="rounded-xl border rule bg-paper p-5"
            >
              <div className="flex items-baseline justify-between">
                <div>
                  <div className="font-display text-base text-ink">{en ? track.name.en : track.name.bn}</div>
                  <div className="font-mono text-[10px] text-ink-faint">{track.en}</div>
                </div>
                <div className="font-display text-xl tabular text-leaf">{statLocale(track.count, en)}</div>
              </div>
              <p className="mt-3 text-sm text-ink-soft">{en ? track.desc.en : track.desc.bn}</p>
              <p className="mt-1 text-xs text-ink-faint">{en ? track.detail.en : track.detail.bn}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === C. Design Principles === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          {en ? "Design Principles" : "নকশা নীতি"}
        </motion.h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {PRINCIPLES.map((p, i) => (
            <motion.div key={i} variants={enter} className="rounded-lg border rule bg-paper p-5">
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                  <p.icon className="h-5 w-5" />
                </div>
                <div>
                  <div className="font-display text-base text-ink">{en ? p.title.en : p.title.bn}</div>
                  <div className="font-mono text-[10px] text-ink-faint">{p.en}</div>
                  <p className="mt-2 text-sm leading-relaxed text-ink-soft">{en ? p.desc.en : p.desc.bn}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === D. Knowledge Node Construction (AgriTrust) === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          {en ? "Knowledge Node Construction" : "জ্ঞান নোড নির্মাণ"}
        </motion.h2>
        <motion.p variants={enter} className="mb-6 text-sm text-ink-soft">
          {en ? "From the AgriTrust paper — a 3-tier node structure: content, structured facts, provenance." : "AgriTrust পত্র থেকে — ৩-স্তরের নোড কাঠামো: কনটেন্ট, স্ট্রাকচার্ড ফ্যাক্ট, প্রমাণ।"}
        </motion.p>

        {/* 3-layer node structure */}
        <motion.div variants={enter} className="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
          {[
            { layer: 1, title: { bn: "ন্যাচারাল ল্যাঙ্গুয়েজ কনটেন্ট", en: "Natural Language Content" }, detail: { bn: "সারাংশ, লক্ষণ, ব্যবস্থাপনা", en: "Summary, symptoms, management" } },
            { layer: 2, title: { bn: "স্ট্রাকচার্ড ফ্যাক্ট", en: "Structured Facts" }, detail: { bn: "এনটিটি, ট্রিপল, রাসায়নিক", en: "Entities, triples, chemicals" } },
            { layer: 3, title: { bn: "প্রমাণ", en: "Provenance" }, detail: { bn: "উৎস, পৃষ্ঠা, প্রতিষ্ঠান", en: "Source, page, institution" } },
          ].map((layer) => (
            <div key={layer.layer} className="rounded-lg border rule bg-paper-2/40 px-4 py-3 text-center">
              <div className="flex h-8 w-8 mx-auto items-center justify-center rounded-full bg-leaf/10 font-display text-sm text-leaf tabular">
                {numLocale(layer.layer, en)}
              </div>
              <div className="mt-2 font-display text-sm text-ink">{en ? layer.title.en : layer.title.bn}</div>
              <div className="mt-1 text-xs text-ink-faint">{en ? layer.detail.en : layer.detail.bn}</div>
            </div>
          ))}
        </motion.div>

        {/* 7-step construction flow */}
        <motion.div variants={enter} className="space-y-2">
          <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-ochre">
            <GitBranch className="h-3.5 w-3.5" />
            {en ? "Node Construction Process" : "নোড নির্মাণ প্রক্রিয়া"}
          </div>
          {NODE_CONSTRUCTION.map((step, i) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, x: -10 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08, duration: dur.fast }}
              className="flex items-center gap-3 rounded-lg border rule bg-paper px-4 py-2.5"
            >
              <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-leaf/10 font-display text-xs text-leaf tabular">
                {step.step}
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-ink">{en ? step.label.en : step.label.bn}</div>
              </div>
              <div className="text-xs text-ink-faint">{en ? step.detail.en : step.detail.bn}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Verification stats */}
        <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
          {[
            { value: "৯৬.১%", label: { bn: "এনটিটি কভারেজ", en: "Entity Coverage" } },
            { value: "১০০%", label: { bn: "ট্রিপল কভারেজ", en: "Triple Coverage" } },
            { value: "২৮৩", label: { bn: "রিফাইন করা নোড", en: "Nodes Refined" } },
            { value: "০.৮১", label: { bn: "মানব অডিট κ", en: "Human Audit κ" } },
          ].map((stat) => (
            <div key={stat.label.en} className="rounded-lg border rule bg-paper px-3 py-3 text-center">
              <div className="font-display text-lg tabular text-leaf">{statLocale(stat.value, en)}</div>
              <div className="mt-1 text-[10px] text-ink-faint">{en ? stat.label.en : stat.label.bn}</div>
            </div>
          ))}
        </motion.div>
      </motion.section>
    </div>
  );
}

function AgentPipelineExplorer() {
  const [selected, setSelected] = useState("safety");
  const active = AGENT_STEPS.find((step) => step.id === selected) ?? AGENT_STEPS[0];
  const { locale } = useLanguage();
  const en = locale === "en";

  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-80px" }}
      variants={stagger}
    >
      <motion.div variants={enter} className="mb-5 text-center">
        <h2 className="font-display text-2xl text-ink">{en ? "Four-Agent Answer Flow" : "চার-এজেন্ট উত্তর প্রবাহ"}</h2>
        <p className="mt-2 text-sm text-ink-soft">{en ? "See what each stage does — safety first, verification last." : "প্রতিটি ধাপের কাজ দেখুন — নিরাপত্তা আগে, যাচাই শেষে।"}</p>
      </motion.div>

      <motion.div variants={enter} className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        {AGENT_STEPS.map((step, index) => {
          const Icon = step.icon;
          const isSelected = selected === step.id;
          return (
            <div key={step.id} className="relative">
              <button
                type="button"
                onClick={() => setSelected(step.id)}
                aria-expanded={isSelected}
                className={`flex min-h-28 w-full flex-col items-center justify-center rounded-xl border p-3 text-center transition-all ${
                  isSelected ? "border-leaf bg-leaf/10 shadow-sm" : "rule bg-paper hover:border-leaf/50"
                }`}
              >
                <Icon className={`h-5 w-5 ${isSelected ? "text-leaf" : "text-ink-faint"}`} />
                <span className={`mt-2 text-sm font-medium ${isSelected ? "text-leaf" : "text-ink"}`}>{en ? step.label.en : step.label.bn}</span>
                <span className="mt-0.5 text-[10px] text-ink-faint">{en ? step.short.en : step.short.bn}</span>
                <ChevronDown className={`mt-1 h-3.5 w-3.5 text-ink-faint transition-transform sm:hidden ${isSelected ? "rotate-180" : ""}`} />
              </button>
              {index < AGENT_STEPS.length - 1 && <span className="absolute -right-2 top-1/2 z-10 hidden text-leaf sm:block">→</span>}
            </div>
          );
        })}
      </motion.div>

      <motion.div
        key={active.id}
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-3 rounded-xl border border-leaf/20 bg-leaf/5 p-4"
      >
        <div className="text-sm font-medium text-ink">{en ? active.label.en : active.label.bn}</div>
        <p className="mt-1 text-sm leading-relaxed text-ink-soft">{en ? active.detail.en : active.detail.bn}</p>
        <div className="mt-3 rounded-lg bg-paper px-3 py-2 font-mono text-[10px] text-leaf">{en ? active.contract.en : active.contract.bn}</div>
      </motion.div>
    </motion.section>
  );
}
