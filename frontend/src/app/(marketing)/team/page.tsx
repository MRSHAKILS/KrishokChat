"use client";

import { motion } from "motion/react";
import { MapPin, Users, FileText, ExternalLink } from "lucide-react";
import { RESEARCH_STATS, LINKS } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";

/* =========================================================================
   Team & Fieldwork Page — shows the real people and real fieldwork.
   Uses the photos in /assets/researchers image/ and fieldwork photos.

   Sections:
   A. Team members (3 cards with photos)
   B. Fieldwork story (photos + 5-stage pipeline)
   C. Institutional partners
   D. Publications
   ========================================================================= */

const TEAM = [
  {
    name: "Khan Raiyan Ibne Reza",
    role: "প্রধান গবেষক · Lead Researcher",
    affiliation: "North South University",
    image: "/assets/researchers image/raiyan_khan.jpg",
  },
  {
    name: "Sanjana Maria",
    role: "গবেষক · Researcher",
    affiliation: "North South University",
    image: "/assets/researchers image/sanjana_maria.jpg",
  },
  {
    name: "Shakil Ahmed",
    role: "গবেষক · Researcher",
    affiliation: "North South University",
    image: "/assets/researchers image/shakil_ahmed.jpg",
  },
];

const INSTITUTIONS = [
  { abbr: "BARC", full: "বাংলাদেশ কৃষি গবেষণা কাউন্সিল (BARC)" },
  { abbr: "BARI", full: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)" },
  { abbr: "DAE", full: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)" },
  { abbr: "DLS", full: "প্রাণিসম্পদ অধিদপ্তর (DLS)" },
  { abbr: "DoF", full: "মৎস্য অধিদপ্তর (DoF)" },
  { abbr: "CDB", full: "তুলা উন্নয়ন বোর্ড (CDB)" },
  { abbr: "NARS", full: "জাতীয় কৃষি গবেষণা সিস্টেম (NARS)" },
  { abbr: "SRDI", full: "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট (SRDI)" },
  { abbr: "BSRTI", full: "বাংলাদেশ রেশম গবেষণা ও প্রশিক্ষণ ইনস্টিটিউট" },
  { abbr: "MoA", full: "কৃষি মন্ত্রণালয়, গণপ্রজাতন্ত্রী বাংলাদেশ সরকার" },
  { abbr: "CABI", full: "সেন্টার ফর এগ্রিকালচার অ্যান্ড বায়োসায়েন্স ইন্টারন্যাশনাল" },
  { abbr: "IRRI", full: "আন্তর্জাতিক ধান গবেষণা ইনস্টিটিউট (IRRI)" },
  { abbr: "WorldFish", full: "ওয়ার্ল্ডফিশ বাংলাদেশ সেন্টার" },
];

const FIELDWORK_STAGES = [
  { stage: "১", label: "মাঠে কৃষকের সাথে প্রত্যক্ষ সাক্ষাৎকার", detail: "রাজশাহী ও নাটোর জেলার মাঠে কৃষকদের বাস্তব কৃষি সমস্যার মুখোমুখি সাক্ষাৎকার।" },
  { stage: "২", label: "জাতীয় কৃষি নথিপত্র ও নির্দেশিকা ম্যাপিং", detail: "DAE, BARC ও BRRI-এর ২৮৪টি সরকারি প্রকাশনা থেকে সঠিক সমাধান চিহ্নিতকরণ।" },
  { stage: "৩", label: "উপসহকারী কৃষি কর্মকর্তা (SAAO) দ্বারা যাচাই", detail: "৬৯ জন মাঠ পর্যায়ের কৃষি সম্প্রসারণ কর্মকর্তা দ্বারা প্রতিটি উত্তরের নির্ভুলতা অডিট।" },
  { stage: "৪", label: "আঞ্চলিক উপভাষা ও বালাই পরিভাষা সমরূপীকরণ", detail: "স্থানীয় ও আঞ্চলিক ভাষার প্রশ্নগুলোকে জাতীয় প্রমিত কৃষি পরিভাষায় ম্যাপিং।" },
  { stage: "৫", label: "মাল্টি-এজেন্ট নিরাপত্তা ও ডোজ নিয়ন্ত্রণ", detail: "কীটনাশক ও রাসায়নিকের মাত্রা Verifier Agent দ্বারা চূড়ান্তভাবে লক করা।" },
];

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

export default function TeamPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* === A. Team === */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={stagger}
      >
        <motion.h1 variants={enter} className="text-center font-display text-4xl text-ink">
          দল <span className="text-leaf">ও গবেষণা</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-lg text-center text-base text-ink-soft">
          নর্থ সাউথ বিশ্ববিদ্যালয়ের গবেষক দল — বাংলাদেশের কৃষকের জন্য নিরাপদ এআই পরামর্শ ব্যবস্থা তৈরি।
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
                <div className="mt-1 text-xs text-ochre">{member.role}</div>
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
          মাঠ পর্যায়ের কাজ
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          রাজশাহী ও নাটোর জেলায় {RESEARCH_STATS.fieldInterviews} জন কৃষকের সাথে সাক্ষাৎকার —
          প্রতিটি কৃষককে জিজ্ঞাসা করা হয়েছিল: &ldquo;আপনি আজ একজন কৃষি সম্প্রসারণ কর্মকর্তাকে কী প্রশ্ন করবেন?&rdquo;
        </motion.p>

        {/* Fieldwork photos */}
        <motion.div variants={enter} className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/assets/researcher_interviewing_farmer.png"
              alt="গবেষক কৃষকের সাক্ষাৎকার নিচ্ছেন"
              className="aspect-video w-full object-cover"
            />
          </div>
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/assets/small_group_researcher_farmer_discussion.png"
              alt="গবেষক ও কৃষকদের গোষ্ঠী আলোচনা"
              className="aspect-video w-full object-cover"
            />
          </div>
        </motion.div>

        {/* 5-stage ground truth pipeline */}
        <motion.div variants={enter} className="mt-8">
          <div className="mb-3 text-xs font-semibold text-ochre">
            গ্রাউন্ড-ট্রুথ তৈরির ৫ ধাপ
          </div>
          <div className="space-y-2">
            {FIELDWORK_STAGES.map((step, i) => (
              <motion.div
                key={step.stage}
                initial={{ opacity: 0, x: -10 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.3 }}
                className="flex items-center gap-3 rounded-lg border rule bg-paper px-4 py-3"
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-leaf/10 font-display text-sm text-leaf tabular">
                  {step.stage}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-ink">{step.label}</div>
                  <div className="text-xs text-ink-faint">{step.detail}</div>
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
            { value: RESEARCH_STATS.fieldInterviews, label: "কৃষক সাক্ষাৎকার" },
            { value: "৬৯", label: "SAAO কর্মকর্তা যাচাই" },
            { value: "১০০%", label: "বিশেষজ্ঞ সম্মতি" },
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
          সহযোগী গবেষণা ও সরকারি প্রতিষ্ঠানসমূহ
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          {RESEARCH_STATS.institutions}টি সরকারি ও গবেষণা প্রতিষ্ঠান থেকে {RESEARCH_STATS.publications}টি অনুমোদিত প্রকাশনা।
        </motion.p>
        <motion.div variants={enter} className="mt-6 grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
          {INSTITUTIONS.map((inst) => (
            <div
              key={inst.abbr}
              className="rounded-lg border rule bg-paper px-3 py-2.5 text-center shadow-2xs"
            >
              <div className="font-display text-sm font-bold text-ink">{inst.abbr}</div>
              <div className="mt-0.5 text-[10px] leading-tight text-ink-faint">{inst.full}</div>
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
          প্রকাশিত গবেষণাপত্র ও রিসোর্স
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
          <h2 className="mt-3 font-display text-lg text-ink">গবেষণা অবদানের সারসংক্ষেপ</h2>
          <div className="mt-4 grid grid-cols-3 gap-3">
            {[
              { value: RESEARCH_STATS.benchmarkInstances, label: "বেঞ্চমার্ক প্রশ্নোত্তর" },
              { value: RESEARCH_STATS.farmerQueries, label: "বাস্তব কৃষক প্রশ্ন" },
              { value: RESEARCH_STATS.fieldInterviews, label: "মাঠ সাক্ষাৎকার" },
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
