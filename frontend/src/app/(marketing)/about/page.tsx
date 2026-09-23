"use client";

import Link from "next/link";
import { useRef } from "react";
import { motion, useInView } from "motion/react";
import {
  Shield,
  Database,
  MapPin,
  BarChart3,
  BookOpen,
} from "lucide-react";
import { RESEARCH_STATS, RESEARCH_STATS_N } from "@/lib/constants";
import { toLocaleCount, useCountUp } from "@/lib/use-count-up";
import { statLocale } from "@/lib/bn";
import { enter, stagger } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   পরিচিতি (About) — hub page.
   Mission, team, fieldwork, data/analytics links, publications.
   Everything that doesn't need its own navbar item lives here.
   ========================================================================= */

const TEAM = [
  {
    name: "Khan Raiyan Ibne Reza",
    role: "Lead Researcher",
    affiliation: "North South University",
    image: "/assets/researchers/raiyan_khan.jpg",
  },
  {
    name: "Sanjana Maria",
    role: "Researcher",
    affiliation: "North South University",
    image: "/assets/researchers/sanjana_maria.jpg",
  },
  {
    name: "Shakil Ahmed",
    role: "Researcher",
    affiliation: "North South University",
    image: "/assets/researchers/shakil_ahmed.jpg",
  },
];

const HUB_LINKS = [
  {
    href: "/data",
    icon: Database,
    title: { bn: "উপাত্ত ও নলেজ গ্রাফ", en: "Data and Knowledge Graph" },
    desc: { bn: "জ্ঞানভাণ্ডার ও উন্মুক্ত ডেটাসেট", en: "Knowledge base and open datasets" },
  },
  {
    href: "/analytics",
    icon: BarChart3,
    title: { bn: "লাইভ পরিসংখ্যান", en: "Live Analytics" },
    desc: { bn: "এজেন্ট সিদ্ধান্ত ও নিরাপত্তা ড্যাশবোর্ড", en: "Agent decision and safety dashboard" },
  },
  {
    href: "/research/safety",
    icon: Shield,
    title: { bn: "নিরাপত্তা কাঠামো", en: "Safety Framework" },
    desc: { bn: "মাল্টি-এজেন্ট গার্ডরেইল ও ভেরিফায়ার", en: "Multi-agent guardrails and verifier" },
  },
  {
    href: "/research/benchmark",
    icon: BookOpen,
    title: { bn: "বেঞ্চমার্ক ফলাফল", en: "Benchmark Results" },
    desc: { bn: "মডেল মূল্যায়ন ও তুলনামূলক চার্ট", en: "Model evaluation and comparison charts" },
  },
] as const;

const INSTITUTIONS = [
  "BARC", "BARI", "DAE", "DLS", "DoF", "CDB", "NARS", "SRDI", "BSRTI", "MoA", "CABI", "IRRI", "WorldFish",
];

const COPY = {
  bn: {
    eyebrow: "প্রকল্প পরিচিতি ও লক্ষ্য",
    titlePrefix: "কৃষক টেক",
    titleHighlight: "উদ্যোগ",
    mission: "বাংলাদেশে ১৭ কোটি+ জনসংখ্যার এক বিশাল অংশ প্রত্যক্ষ ও পরোক্ষভাবে কৃষির সাথে যুক্ত। কিন্তু বিশেষজ্ঞ কৃষি কর্মকর্তার সংখ্যা প্রয়োজনের তুলনায় অপ্রতুল হওয়ায় মাঠের কৃষক তাৎক্ষণিক সঠিক পরামর্শ পেতে সমস্যার সম্মুখীন হন। কৃষক টেক এই শূন্যতা পূরণের লক্ষ্যে তৈরি — সরকারি কৃষি গবেষণা সংস্থাগুলোর নির্দেশিকা ও মাল্টি-এজেন্ট নিরাপত্তা পাইপলাইন দ্বারা পরিচালিত একটি নিরাপদ, নির্ভরযোগ্য ও প্রমাণযোগ্য বাংলা এআই কৃষি পরামর্শ ব্যবস্থা।",
    teamHeading: "গবেষক দল",
    fieldworkHeading: "মাঠ পর্যায়ের গবেষণা ও যাচাই",
    fieldworkDescSuffix: "জন কৃষকের সরাসরি সাক্ষাৎকার এবং উপসহকারী কৃষি কর্মকর্তা (SAAO) দ্বারা পরামর্শের মাঠ উপযোগিতা যাচাই।",
    fieldworkDescPrefix: "রাজশাহী ও নাটোর জেলার মাঠে",
    interviewPhotoAlt: "গবেষক কর্তৃক কৃষকের সাক্ষাৎকার গ্রহণ",
    groupPhotoAlt: "কৃষক দলীয় আলোচনা",
    farmerInterviewsLabel: "কৃষক সাক্ষাৎকার",
    saaoLabel: "SAAO কর্মকর্তা যাচাই",
    expertAgreementLabel: "বিশেষজ্ঞ সম্মতি",
    institutionsHeading: "সহযোগী গবেষণা ও সরকারি প্রতিষ্ঠানসমূহ",
    institutionsDesc: (institutions: string, publications: string) =>
      `${institutions}টি জাতীয় ও আন্তর্জাতিক কৃষি প্রতিষ্ঠান থেকে সংগৃহীত ${publications}টি অনুমোদিত প্রকাশনা।`,
    statusLabel: "গবেষণা প্রোটোটাইপ ও নিরাপত্তা বার্তা:",
    statusText: (floor: string) => `অনিয়ন্ত্রিত এলএলএম-এর রাসায়নিক হ্যালুসিনেশন ঝুঁকি (${floor}) প্রতিরোধে আমাদের মাল্টি-এজেন্ট ভেরিফায়ার সিস্টেম সরকারি নির্দেশিকা থেকে যাচাইকৃত সঠিক ডোজ নিশ্চিত করে।`,
    publicationsLabel: "সরকারি প্রকাশনা",
    knowledgeNodesLabel: "জ্ঞানভাণ্ডার নোড",
    benchmarkLabel: "বেঞ্চমার্ক প্রশ্নোত্তর",
    dialectsLabel: "আঞ্চলিক উপভাষা",
    footer: "গবেষণা প্রোটোটাইপ — CC-BY-4.0 লাইসেন্স। © 2026 North South University.",
  },
  en: {
    eyebrow: "Project Introduction and Goals",
    titlePrefix: "KrishokTech",
    titleHighlight: "Initiative",
    mission: "A large share of Bangladesh's 170 million+ population is directly or indirectly connected to agriculture. But the number of expert agriculture officers is inadequate relative to need, so farmers in the field struggle to get accurate advice right away. KrishokTech is built to fill that gap — a safe, reliable, and evidence-grounded Bengali AI agricultural advisory system, governed by guidelines from government agricultural research institutions and a multi-agent safety pipeline.",
    teamHeading: "Research Team",
    fieldworkHeading: "Field Research and Validation",
    fieldworkDescPrefix: "In the field across Rajshahi and Natore districts,",
    fieldworkDescSuffix: "direct farmer interviews, plus field-utility validation of advisories by Sub-Assistant Agriculture Officers (SAAO).",
    interviewPhotoAlt: "A researcher interviewing a farmer",
    groupPhotoAlt: "Farmer group discussion",
    farmerInterviewsLabel: "Farmer Interviews",
    saaoLabel: "SAAO Officers Validated",
    expertAgreementLabel: "Expert Agreement",
    institutionsHeading: "Collaborating Research and Government Institutions",
    institutionsDesc: (institutions: string, publications: string) =>
      `${publications} approved publications gathered from ${institutions} national and international agricultural institutions.`,
    statusLabel: "Research Prototype and Safety Notice:",
    statusText: (floor: string) => `To prevent the chemical hallucination risk of unconstrained LLMs (${floor}), our multi-agent verifier system ensures the exact dose is verified against government guidelines.`,
    publicationsLabel: "Government Publications",
    knowledgeNodesLabel: "Knowledge Base Nodes",
    benchmarkLabel: "Benchmark Q&A Pairs",
    dialectsLabel: "Regional Dialects",
    footer: "Research Prototype — CC-BY-4.0 License. © 2026 North South University.",
  },
} as const;

/* Count-up cell — rAF tween when the cell scrolls into view */
function CountCell({
  value,
  suffix,
  label,
  bordered = false,
}: {
  value: number;
  suffix?: string;
  label: string;
  bordered?: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });
  const n = useCountUp(value, inView);
  const { locale } = useLanguage();
  const en = locale === "en";
  const box = bordered
    ? "rounded-lg border rule bg-paper px-4 py-3 text-center"
    : "bg-paper p-4 text-center";
  return (
    <div ref={ref} className={box}>
      <div className="font-display text-xl tabular text-leaf sm:text-2xl">
        {toLocaleCount(n, en)}
        {suffix ? <span className="text-base">{suffix}</span> : null}
      </div>
      <div className="mt-1 text-[11px] font-medium text-ink-faint">{label}</div>
    </div>
  );
}

export default function AboutPage() {
  const { locale } = useLanguage();
  const en = locale === "en";
  const c = COPY[en ? "en" : "bn"];
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* === Mission === */}
      <motion.section initial="hidden" animate="visible" variants={stagger}>
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre font-semibold">
          {c.eyebrow}
        </motion.p>
        <motion.h1 variants={enter} className="mt-3 font-display text-4xl text-ink">
          {c.titlePrefix} <span className="text-leaf">{c.titleHighlight}</span>
        </motion.h1>
        <motion.p variants={enter} className="mt-4 text-sm leading-relaxed text-ink-soft sm:text-base">
          {c.mission}
        </motion.p>
      </motion.section>

      {/* === Hub links — Data, Analytics, Safety, Benchmark === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.div variants={enter} className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {HUB_LINKS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="group flex flex-col items-center gap-2 rounded-xl border rule bg-paper p-4 text-center transition-all hover:border-leaf hover:shadow-xs"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <item.icon className="h-5 w-5" />
              </div>
              <div className="font-display text-sm text-ink group-hover:text-leaf">{en ? item.title.en : item.title.bn}</div>
              <div className="text-[10px] text-ink-faint">{en ? item.desc.en : item.desc.bn}</div>
            </Link>
          ))}
        </motion.div>
      </motion.section>

      {/* === Team === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          {c.teamHeading}
        </motion.h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          {TEAM.map((member) => (
            <motion.div key={member.name} variants={enter} className="group overflow-hidden rounded-xl border rule bg-paper transition-shadow hover:shadow-[0_12px_32px_rgba(52,39,23,0.10)]">
              <div className="aspect-square overflow-hidden bg-paper-2">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={member.image} alt={member.name} className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105" />
              </div>
              <div className="p-4 text-center">
                <div className="font-display text-base text-ink">{member.name}</div>
                <div className="mt-1 text-xs text-ochre font-medium">{member.role}</div>
                <div className="mt-2 flex items-center justify-center gap-1 text-[11px] text-ink-faint">
                  <MapPin className="h-3 w-3" />
                  {member.affiliation}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === Fieldwork === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="font-display text-2xl text-ink">
          {c.fieldworkHeading}
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          {c.fieldworkDescPrefix} {statLocale(RESEARCH_STATS.fieldInterviews, en)} {c.fieldworkDescSuffix}
        </motion.p>
        <motion.div variants={enter} className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/researcher-interviewing-farmer.png" alt={c.interviewPhotoAlt} className="aspect-video w-full object-cover" />
          </div>
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/small_group_researcher_farmer_discussion.png" alt={c.groupPhotoAlt} className="aspect-video w-full object-cover" />
          </div>
        </motion.div>
        <motion.div variants={enter} className="mt-6 grid grid-cols-3 gap-3">
          <CountCell bordered value={RESEARCH_STATS_N.fieldInterviews} label={c.farmerInterviewsLabel} />
          <CountCell bordered value={69} label={c.saaoLabel} />
          <CountCell bordered value={100} suffix="%" label={c.expertAgreementLabel} />
        </motion.div>
      </motion.section>

      {/* === Institutions === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          {c.institutionsHeading}
        </motion.h2>
        <motion.p variants={enter} className="mb-4 text-sm text-ink-soft">
          {c.institutionsDesc(statLocale(RESEARCH_STATS.institutions, en), statLocale(RESEARCH_STATS.publications, en))}
        </motion.p>
        <motion.div variants={enter} className="flex flex-wrap gap-2">
          {INSTITUTIONS.map((inst) => (
            <div key={inst} className="rounded-lg border rule bg-paper px-3 py-1.5 text-center shadow-2xs">
              <span className="font-display text-sm text-ink">{inst}</span>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* === Status + Stats === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="space-y-6">
        <motion.div variants={enter} className="rounded-lg border border-clay-soft/40 bg-clay-soft/8 px-5 py-4">
          <p className="text-sm leading-relaxed text-ink-soft">
            <span className="font-medium text-clay">{c.statusLabel}</span>{" "}
            {c.statusText(statLocale(RESEARCH_STATS.hallucinationFloor, en))}
          </p>
        </motion.div>
        <motion.div variants={enter} className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
          <CountCell value={RESEARCH_STATS_N.publications} label={c.publicationsLabel} />
          <CountCell value={RESEARCH_STATS_N.knowledgeNodes} label={c.knowledgeNodesLabel} />
          <CountCell value={RESEARCH_STATS_N.benchmarkInstances} label={c.benchmarkLabel} />
          <CountCell value={RESEARCH_STATS_N.dialects} label={c.dialectsLabel} />
        </motion.div>
      </motion.section>

      <motion.p variants={enter} className="border-t rule pt-6 text-center text-xs text-ink-faint">
        {c.footer}
      </motion.p>
    </div>
  );
}
