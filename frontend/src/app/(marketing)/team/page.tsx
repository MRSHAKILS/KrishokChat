"use client";

import { motion } from "motion/react";
import { MapPin, Users, FileText, ExternalLink } from "lucide-react";
import { RESEARCH_STATS, LINKS } from "@/lib/constants";
import { statLocale, numLocale } from "@/lib/bn";
import { enter, stagger } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   Team & Fieldwork Page — shows the real people and real fieldwork.
   Uses the photos in /assets/researchers/ and fieldwork photos.

   Sections:
   A. Team members (3 cards with photos)
   B. Fieldwork story (photos + 5-stage pipeline)
   C. Institutional partners
   D. Publications
   ========================================================================= */

const TEAM = [
  {
    name: "Khan Raiyan Ibne Reza",
    role: { bn: "প্রধান গবেষক · Lead Researcher", en: "Lead Researcher" },
    affiliation: "North South University",
    image: "/assets/researchers/raiyan_khan.jpg",
  },
  {
    name: "Sanjana Maria",
    role: { bn: "গবেষক · Researcher", en: "Researcher" },
    affiliation: "North South University",
    image: "/assets/researchers/sanjana_maria.jpg",
  },
  {
    name: "Shakil Ahmed",
    role: { bn: "গবেষক · Researcher", en: "Researcher" },
    affiliation: "North South University",
    image: "/assets/researchers/shakil_ahmed.jpg",
  },
] as const;

const INSTITUTIONS = [
  { abbr: "BARC", full: { bn: "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)", en: "Bangladesh Agricultural Research Council (BARC)" } },
  { abbr: "BARI", full: { bn: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)", en: "Bangladesh Agricultural Research Institute (BARI)" } },
  { abbr: "DAE", full: { bn: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)", en: "Department of Agricultural Extension (DAE)" } },
  { abbr: "DLS", full: { bn: "প্রাণিসম্পদ অধিদপ্তর (DLS)", en: "Department of Livestock Services (DLS)" } },
  { abbr: "DoF", full: { bn: "মৎস্য অধিদপ্তর (DoF)", en: "Department of Fisheries (DoF)" } },
  { abbr: "CDB", full: { bn: "তুলা উন্নয়ন বোর্ড (CDB)", en: "Cotton Development Board (CDB)" } },
  { abbr: "NARS", full: { bn: "জাতীয় কৃষি গবেষণা সিস্টেম (NARS)", en: "National Agricultural Research System (NARS)" } },
  { abbr: "SRDI", full: { bn: "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট (SRDI)", en: "Soil Resource Development Institute (SRDI)" } },
  { abbr: "BSRTI", full: { bn: "বাংলাদেশ রেশম গবেষণা ও প্রশিক্ষণ ইনস্টিটিউট", en: "Bangladesh Sericulture Research and Training Institute" } },
  { abbr: "MoA", full: { bn: "কৃষি মন্ত্রণালয়, গণপ্রজাতন্ত্রী বাংলাদেশ সরকার", en: "Ministry of Agriculture, Government of the People's Republic of Bangladesh" } },
  { abbr: "CABI", full: { bn: "সেন্টার ফর এগ্রিকালচার অ্যান্ড বায়োসায়েন্স ইন্টারন্যাশনাল", en: "Centre for Agriculture and Bioscience International" } },
  { abbr: "IRRI", full: { bn: "আন্তর্জাতিক ধান গবেষণা ইনস্টিটিউট (IRRI)", en: "International Rice Research Institute (IRRI)" } },
  { abbr: "WorldFish", full: { bn: "ওয়ার্ল্ডফিশ বাংলাদেশ সেন্টার", en: "WorldFish Bangladesh Center" } },
] as const;

const FIELDWORK_STAGES = [
  {
    label: { bn: "মাঠে কৃষকের সাথে প্রত্যক্ষ সাক্ষাৎকার", en: "Direct interviews with farmers in the field" },
    detail: { bn: "রাজশাহী ও নাটোর জেলার মাঠে কৃষকদের বাস্তব কৃষি সমস্যার মুখোমুখি সাক্ষাৎকার।", en: "Face-to-face interviews with farmers about real agricultural problems, in the fields of Rajshahi and Natore districts." },
  },
  {
    label: { bn: "জাতীয় কৃষি নথিপত্র ও নির্দেশিকা ম্যাপিং", en: "Mapping to national agricultural documents and guidelines" },
    detail: { bn: "DAE, BARC ও BRRI-এর ২৮৪টি সরকারি প্রকাশনা থেকে সঠিক সমাধান চিহ্নিতকরণ।", en: "Identifying the correct solution from 284 government publications by DAE, BARC, and BRRI." },
  },
  {
    label: { bn: "উপসহকারী কৃষি কর্মকর্তা (SAAO) দ্বারা যাচাই", en: "Validation by Sub-Assistant Agriculture Officers (SAAO)" },
    detail: { bn: "৬৯ জন মাঠ পর্যায়ের কৃষি সম্প্রসারণ কর্মকর্তা দ্বারা প্রতিটি উত্তরের নির্ভুলতা অডিট।", en: "Every answer's accuracy audited by 69 field-level agricultural extension officers." },
  },
  {
    label: { bn: "আঞ্চলিক উপভাষা ও বালাই পরিভাষা সমরূপীকরণ", en: "Regional dialect and pest-terminology normalization" },
    detail: { bn: "স্থানীয় ও আঞ্চলিক ভাষার প্রশ্নগুলোকে জাতীয় প্রমিত কৃষি পরিভাষায় ম্যাপিং।", en: "Mapping local and regional-dialect questions to standard national agricultural terminology." },
  },
  {
    label: { bn: "মাল্টি-এজেন্ট নিরাপত্তা ও ডোজ নিয়ন্ত্রণ", en: "Multi-agent safety and dose control" },
    detail: { bn: "কীটনাশক ও রাসায়নিকের মাত্রা Verifier Agent দ্বারা চূড়ান্তভাবে লক করা।", en: "Pesticide and chemical dosage finally locked by a Verifier Agent." },
  },
] as const;

const PUBLICATIONS = [
  {
    venue: "EACL 2026 — Data Resource & Benchmark Track",
    title: "KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory",
    link: null, // No public URL yet (arXiv v1 is deprecated — docs/PAPER_POLICY.md); TODO: add real link when published
    linkLabel: "",
    extraLink: LINKS.huggingface,
    extraLabel: "Hugging Face",
  },
  {
    venue: "SIGIR-AP 2026",
    title: "AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval",
    link: null,
    linkLabel: "",
    extraLink: null,
    extraLabel: "",
  },
];

const COPY = {
  bn: {
    titlePrefix: "দল",
    titleHighlight: "ও গবেষণা",
    intro: "নর্থ সাউথ বিশ্ববিদ্যালয়ের গবেষক দল — বাংলাদেশের কৃষকের জন্য নিরাপদ এআই পরামর্শ ব্যবস্থা তৈরি।",
    fieldworkHeading: "মাঠ পর্যায়ের কাজ",
    fieldworkDescPrefix: "রাজশাহী ও নাটোর জেলায়",
    fieldworkDescSuffix: "জন কৃষকের সাথে সাক্ষাৎকার — প্রতিটি কৃষককে জিজ্ঞাসা করা হয়েছিল: “আপনি আজ একজন কৃষি সম্প্রসারণ কর্মকর্তাকে কী প্রশ্ন করবেন?”",
    interviewPhotoAlt: "গবেষক কৃষকের সাক্ষাৎকার নিচ্ছেন",
    groupPhotoAlt: "গবেষক ও কৃষকদের গোষ্ঠী আলোচনা",
    stagesLabel: "গ্রাউন্ড-ট্রুথ তৈরির ৫ ধাপ",
    farmerInterviewsLabel: "কৃষক সাক্ষাৎকার",
    saaoLabel: "SAAO কর্মকর্তা যাচাই",
    expertAgreementLabel: "বিশেষজ্ঞ সম্মতি",
    institutionsHeading: "সহযোগী গবেষণা ও সরকারি প্রতিষ্ঠানসমূহ",
    institutionsDesc: (institutions: string, publications: string) =>
      `${institutions}টি সরকারি ও গবেষণা প্রতিষ্ঠান থেকে ${publications}টি অনুমোদিত প্রকাশনা।`,
    publicationsHeading: "প্রকাশিত গবেষণাপত্র ও রিসোর্স",
    summaryHeading: "গবেষণা অবদানের সারসংক্ষেপ",
    benchmarkLabel: "বেঞ্চমার্ক প্রশ্নোত্তর",
    farmerQueriesLabel: "বাস্তব কৃষক প্রশ্ন",
    fieldInterviewsLabel: "মাঠ সাক্ষাৎকার",
  },
  en: {
    titlePrefix: "Team",
    titleHighlight: "and Research",
    intro: "A research team from North South University — building a safe AI advisory system for Bangladesh's farmers.",
    fieldworkHeading: "Field-Level Work",
    fieldworkDescPrefix: "In Rajshahi and Natore districts, interviews with",
    fieldworkDescSuffix: "farmers — every farmer was asked: “What question would you ask an agricultural extension officer today?”",
    interviewPhotoAlt: "A researcher interviewing a farmer",
    groupPhotoAlt: "Researchers and farmers in a group discussion",
    stagesLabel: "The 5 Stages of Building Ground Truth",
    farmerInterviewsLabel: "Farmer Interviews",
    saaoLabel: "SAAO Officers Validated",
    expertAgreementLabel: "Expert Agreement",
    institutionsHeading: "Collaborating Research and Government Institutions",
    institutionsDesc: (institutions: string, publications: string) =>
      `${publications} approved publications from ${institutions} government and research institutions.`,
    publicationsHeading: "Published Papers and Resources",
    summaryHeading: "Research Contribution Summary",
    benchmarkLabel: "Benchmark Q&A Pairs",
    farmerQueriesLabel: "Real Farmer Queries",
    fieldInterviewsLabel: "Field Interviews",
  },
} as const;

export default function TeamPage() {
  const { locale } = useLanguage();
  const en = locale === "en";
  const c = COPY[en ? "en" : "bn"];
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* === A. Team === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
      >
        <motion.h1 variants={enter} className="text-center font-display text-4xl text-ink">
          {c.titlePrefix} <span className="text-leaf">{c.titleHighlight}</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-lg text-center text-base text-ink-soft">
          {c.intro}
        </motion.p>

        {/* Team cards */}
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-3">
          {TEAM.map((member) => (
            <motion.div
              key={member.name}
              variants={enter}
              className="group overflow-hidden rounded-xl border rule bg-paper transition-shadow hover:shadow-[0_12px_32px_rgba(52,39,23,0.10)]"
            >
              {/* Photo */}
              <div className="aspect-square overflow-hidden bg-paper-2">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={member.image}
                  alt={member.name}
                  className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
                />
              </div>
              {/* Info */}
              <div className="p-4 text-center">
                <div className="font-display text-base text-ink">{member.name}</div>
                <div className="mt-1 text-xs text-ochre">{en ? member.role.en : member.role.bn}</div>
                <div className="mt-2 flex items-center justify-center gap-1 text-[11px] text-ink-faint">
                  <MapPin className="h-3 w-3" />
                  {member.affiliation}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === B. Fieldwork Story === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="font-display text-2xl text-ink">
          {c.fieldworkHeading}
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          {c.fieldworkDescPrefix} {statLocale(RESEARCH_STATS.fieldInterviews, en)} {c.fieldworkDescSuffix}
        </motion.p>

        {/* Fieldwork photos */}
        <motion.div variants={enter} className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/assets/researcher-interviewing-farmer.png"
              alt={c.interviewPhotoAlt}
              className="aspect-video w-full object-cover"
            />
          </div>
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/assets/small_group_researcher_farmer_discussion.png"
              alt={c.groupPhotoAlt}
              className="aspect-video w-full object-cover"
            />
          </div>
        </motion.div>

        {/* 5-stage ground truth pipeline */}
        <motion.div variants={enter} className="mt-8">
          <div className="mb-3 text-xs font-semibold text-ochre">
            {c.stagesLabel}
          </div>
          <div className="space-y-2">
            {FIELDWORK_STAGES.map((step, i) => (
              <motion.div
                key={step.label.en}
                initial={{ opacity: 0, x: -10 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.3 }}
                className="flex items-center gap-3 rounded-lg border rule bg-paper px-4 py-3"
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-leaf/10 font-display text-sm text-leaf tabular">
                  {numLocale(i + 1, en)}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-ink">{en ? step.label.en : step.label.bn}</div>
                  <div className="text-xs text-ink-faint">{en ? step.detail.en : step.detail.bn}</div>
                </div>
                {/* Connector */}
                {i < FIELDWORK_STAGES.length - 1 && (
                  <div className="hidden text-ink-faint sm:block">↓</div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Validation stats */}
        <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          {[
            { value: statLocale(RESEARCH_STATS.fieldInterviews, en), label: c.farmerInterviewsLabel },
            { value: statLocale("৬৯", en), label: c.saaoLabel },
            { value: statLocale("১০০%", en), label: c.expertAgreementLabel },
          ].map((stat) => (
            <div key={stat.label} className="rounded-lg border rule bg-paper px-4 py-3 text-center">
              <div className="font-display text-xl tabular text-leaf">{stat.value}</div>
              <div className="mt-1 text-[11px] font-medium text-ink-faint">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* === C. Institutional Partners === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="font-display text-2xl text-ink">
          {c.institutionsHeading}
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          {c.institutionsDesc(statLocale(RESEARCH_STATS.institutions, en), statLocale(RESEARCH_STATS.publications, en))}
        </motion.p>
        <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
          {INSTITUTIONS.map((inst) => (
            <div
              key={inst.abbr}
              className="rounded-lg border rule bg-paper px-3 py-2.5 text-center shadow-2xs"
            >
              <div className="font-display text-sm font-bold text-ink">{inst.abbr}</div>
              <div className="mt-0.5 text-[10px] leading-tight text-ink-faint">{en ? inst.full.en : inst.full.bn}</div>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* === D. Publications === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.h2 variants={enter} className="font-display text-2xl text-ink">
          {c.publicationsHeading}
        </motion.h2>
        <div className="mt-6 space-y-4">
          {PUBLICATIONS.map((paper, i) => (
            <motion.div
              key={i}
              variants={enter}
              className="flex items-start gap-4 rounded-xl border rule bg-paper p-5"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <FileText className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="text-xs uppercase tracking-[0.14em] text-ochre font-semibold">
                  {paper.venue}
                </div>
                <div className="mt-2 font-display text-sm leading-snug text-ink">
                  {paper.title}
                </div>
                {(paper.link || paper.extraLink) && (
                  <div className="mt-3 flex flex-wrap gap-3">
                    {paper.link && (
                      <a
                        href={paper.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 rounded-md border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
                      >
                        {paper.linkLabel}
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                    {paper.extraLink && (
                      <a
                        href={paper.extraLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 rounded-md border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
                      >
                        {paper.extraLabel}
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* === E. Dataset Stats Summary === */}
      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
        className="rounded-xl border rule bg-paper-2/30 p-6 text-center"
      >
        <motion.div variants={enter}>
          <Users className="mx-auto h-8 w-8 text-leaf" />
          <h2 className="mt-3 font-display text-lg text-ink">{c.summaryHeading}</h2>
          <div className="mt-4 grid grid-cols-3 gap-3">
            {[
              { value: statLocale(RESEARCH_STATS.benchmarkInstances, en), label: c.benchmarkLabel },
              { value: statLocale(RESEARCH_STATS.farmerQueries, en), label: c.farmerQueriesLabel },
              { value: statLocale(RESEARCH_STATS.fieldInterviews, en), label: c.fieldInterviewsLabel },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="font-display text-2xl tabular text-leaf">{stat.value}</div>
                <div className="mt-1 text-[11px] font-medium text-ink-faint">{stat.label}</div>
              </div>
            ))}
          </div>
        </motion.div>
      </motion.section>
    </div>
  );
}
