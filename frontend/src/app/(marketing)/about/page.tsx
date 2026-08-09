"use client";

import Link from "next/link";
import { motion } from "motion/react";
import {
  Shield,
  Database,
  MapPin,
  BarChart3,
  BookOpen,
} from "lucide-react";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";

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
    image: "/assets/researchers image/raiyan_khan.jpg",
  },
  {
    name: "Sanjana Maria",
    role: "Researcher",
    affiliation: "North South University",
    image: "/assets/researchers image/sanjana_maria.jpg",
  },
  {
    name: "Shakil Ahmed",
    role: "Researcher",
    affiliation: "North South University",
    image: "/assets/researchers image/shakil_ahmed.jpg",
  },
];

const HUB_LINKS = [
  { href: "/data", icon: Database, title: "উপাত্ত", desc: "জ্ঞান গ্রাফ ও ডেটাসেট" },
  { href: "/analytics", icon: BarChart3, title: "পরিসংখ্যান", desc: "নিরাপত্তা মূল্যায়ন ড্যাশবোর্ড" },
  { href: "/research/safety", icon: Shield, title: "নিরাপত্তা নকশা", desc: "এজেন্টিক পাইপলাইন অ্যানিমেশন" },
  { href: "/research/benchmark", icon: BookOpen, title: "ফলাফল", desc: "মূল্যায়ন সংখ্যা ও চার্ট" },
];

const INSTITUTIONS = [
  "BARC", "BARI", "DAE", "DLS", "DoF", "CDB", "NARS", "SRDI", "BSRTI", "MoA", "CABI", "IRRI", "WorldFish",
];

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* === Mission === */}
      <motion.section initial="hidden" animate="visible" variants={stagger}>
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          পরিচিতি
        </motion.p>
        <motion.h1 variants={enter} className="mt-3 font-display text-4xl text-ink">
          কৃষক চ্যাট <span className="text-leaf">প্রকল্প</span>
        </motion.h1>
        <motion.p variants={enter} className="mt-4 text-sm leading-relaxed text-ink-soft">
          বাংলাদেশে ২৩ কোটি+ বাংলাভাষী মানুষ, কিন্তু কৃষি সম্প্রসারণ কর্মকর্তা অপর্যাপ্ত। কৃষক যখন সাহায্য
          চান, তখন তাৎক্ষণিক পরামর্শ পাওয়া যায় না। কৃষক চ্যাট এই শূন্যতা পূরণের লক্ষ্যে — একটি নিরাপদ,
          নির্ভরযোগ্য, বাংলাভাষিক কৃষি পরামর্শ ব্যবস্থা।
        </motion.p>
      </motion.section>

      {/* === Hub links — Data, Analytics, Safety, Benchmark === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.div variants={enter} className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {HUB_LINKS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="group flex flex-col items-center gap-2 rounded-xl border rule bg-paper p-4 text-center transition-colors hover:border-leaf"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                <item.icon className="h-5 w-5" />
              </div>
              <div className="font-display text-sm text-ink">{item.title}</div>
              <div className="text-[10px] text-ink-faint">{item.desc}</div>
            </Link>
          ))}
        </motion.div>
      </motion.section>

      {/* === Team === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          দল
        </motion.h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          {TEAM.map((member) => (
            <motion.div key={member.name} variants={enter} className="overflow-hidden rounded-xl border rule bg-paper">
              <div className="aspect-square overflow-hidden bg-paper-2">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={member.image} alt={member.name} className="h-full w-full object-cover" />
              </div>
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

      {/* === Fieldwork === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="font-display text-2xl text-ink">
          মাঠ পর্যায়ের কাজ
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          রাজশাহী ও নাটোর জেলায় {RESEARCH_STATS.fieldInterviews} জন কৃষকের সাথে সাক্ষাৎকার।
        </motion.p>
        <motion.div variants={enter} className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/researcher_interviewing_farmer.png" alt="গবেষক কৃষকের সাক্ষাৎকার" className="aspect-video w-full object-cover" />
          </div>
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/small_group_researcher_farmer_discussion.png" alt="গোষ্ঠী আলোচনা" className="aspect-video w-full object-cover" />
          </div>
        </motion.div>
        <motion.div variants={enter} className="mt-6 grid grid-cols-3 gap-3">
          {[
            { value: RESEARCH_STATS.fieldInterviews, label: "মাঠ সাক্ষাৎকার" },
            { value: "৬৯", label: "অফিসার যাচাই" },
            { value: "১০০%", label: "অফিসার সম্মতি" },
          ].map((stat) => (
            <div key={stat.label} className="rounded-lg border rule bg-paper px-4 py-3 text-center">
              <div className="font-display text-xl tabular text-leaf">{stat.value}</div>
              <div className="mt-1 text-[11px] text-ink-faint">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* === Institutions === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          প্রতিষ্ঠান সহযোগী
        </motion.h2>
        <motion.p variants={enter} className="mb-4 text-sm text-ink-soft">
          {RESEARCH_STATS.institutions}টি সরকারি ও গবেষণা প্রতিষ্ঠান থেকে {RESEARCH_STATS.publications}টি প্রকাশনা।
        </motion.p>
        <motion.div variants={enter} className="flex flex-wrap gap-2">
          {INSTITUTIONS.map((inst) => (
            <div key={inst} className="rounded-lg border rule bg-paper px-3 py-1.5 text-center">
              <span className="font-display text-sm text-ink">{inst}</span>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* === Status + Stats === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="space-y-6">
        <motion.div variants={enter} className="rounded-lg border border-clay-soft/40 bg-clay-soft/8 px-5 py-4">
          <p className="text-sm leading-relaxed text-ink-soft">
            <span className="font-medium text-clay">গবেষণা প্রোটোটাইপ — উৎপাদন ব্যবহারের জন্য নয়।</span>{" "}
            ফাইন-টিউনড মডেলের রাসায়নিক হ্যালুসিনেশন রেট ({RESEARCH_STATS.hallucinationFloor}) এখনও অমীমাংসিত।
          </p>
        </motion.div>
        <motion.div variants={enter} className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
          {[
            { value: RESEARCH_STATS.publications, label: "প্রকাশনা" },
            { value: RESEARCH_STATS.knowledgeNodes, label: "নোড" },
            { value: RESEARCH_STATS.benchmarkInstances, label: "ইনস্ট্যান্স" },
            { value: RESEARCH_STATS.dialects, label: "উপভাষা" },
          ].map((stat) => (
            <div key={stat.label} className="bg-paper p-4 text-center">
              <div className="font-display text-2xl tabular text-leaf">{stat.value}</div>
              <div className="mt-1 text-[11px] text-ink-faint">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </motion.section>

      <motion.p variants={enter} className="border-t rule pt-6 text-center text-xs text-ink-faint">
        গবেষণা প্রোটোটাইপ — CC-BY-4.0 লাইসেন্স। © 2026 North South University.
      </motion.p>
    </div>
  );
}
