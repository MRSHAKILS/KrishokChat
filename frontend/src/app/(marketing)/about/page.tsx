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
import { toBn, useCountUp } from "@/lib/use-count-up";
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
  { href: "/data", icon: Database, title: "উপাত্ত ও নলেজ গ্রাফ", desc: "জ্ঞানভাণ্ডার ও উন্মুক্ত ডেটাসেট" },
  { href: "/analytics", icon: BarChart3, title: "লাইভ পরিসংখ্যান", desc: "এজেন্ট সিদ্ধান্ত ও নিরাপত্তা ড্যাশবোর্ড" },
  { href: "/research/safety", icon: Shield, title: "নিরাপত্তা কাঠামো", desc: "মাল্টি-এজেন্ট গার্ডরেইল ও ভেরিফায়ার" },
  { href: "/research/benchmark", icon: BookOpen, title: "বেঞ্চমার্ক ফলাফল", desc: "মডেল মূল্যায়ন ও তুলনামূলক চার্ট" },
];

const INSTITUTIONS = [
  "BARC", "BARI", "DAE", "DLS", "DoF", "CDB", "NARS", "SRDI", "BSRTI", "MoA", "CABI", "IRRI", "WorldFish",
];

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
  const box = bordered
    ? "rounded-lg border rule bg-paper px-4 py-3 text-center"
    : "bg-paper p-4 text-center";
  return (
    <div ref={ref} className={box}>
      <div className="font-display text-xl tabular text-leaf sm:text-2xl">
        {toBn(n)}
        {suffix ? <span className="text-base">{suffix}</span> : null}
      </div>
      <div className="mt-1 text-[11px] font-medium text-ink-faint">{label}</div>
    </div>
  );
}

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-20 py-14">
      {/* === Mission === */}
      <motion.section initial="hidden" animate="visible" variants={stagger}>
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre font-semibold">
          প্রকল্প পরিচিতি ও লক্ষ্য
        </motion.p>
        <motion.h1 variants={enter} className="mt-3 font-display text-4xl text-ink">
          কৃষক টেক <span className="text-leaf">উদ্যোগ</span>
        </motion.h1>
        <motion.p variants={enter} className="mt-4 text-sm leading-relaxed text-ink-soft sm:text-base">
          বাংলাদেশে ১৭ কোটি+ জনসংখ্যার এক বিশাল অংশ প্রত্যক্ষ ও পরোক্ষভাবে কৃষির সাথে যুক্ত। কিন্তু বিশেষজ্ঞ কৃষি কর্মকর্তার সংখ্যা প্রয়োজনের তুলনায় অপ্রতুল হওয়ায় মাঠের কৃষক তাৎক্ষণিক সঠিক পরামর্শ পেতে সমস্যার সম্মুখীন হন। কৃষক টেক এই শূন্যতা পূরণের লক্ষ্যে তৈরি — সরকারি কৃষি গবেষণা সংস্থাগুলোর নির্দেশিকা ও মাল্টি-এজেন্ট নিরাপত্তা পাইপলাইন দ্বারা পরিচালিত একটি নিরাপদ, নির্ভরযোগ্য ও প্রমাণযোগ্য বাংলা এআই কৃষি পরামর্শ ব্যবস্থা।
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
              <div className="font-display text-sm text-ink group-hover:text-leaf">{item.title}</div>
              <div className="text-[10px] text-ink-faint">{item.desc}</div>
            </Link>
          ))}
        </motion.div>
      </motion.section>

      {/* === Team === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="mb-6 font-display text-2xl text-ink">
          গবেষক দল
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
          মাঠ পর্যায়ের গবেষণা ও যাচাই
        </motion.h2>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          রাজশাহী ও নাটোর জেলার মাঠে {RESEARCH_STATS.fieldInterviews} জন কৃষকের সরাসরি সাক্ষাৎকার এবং উপসহকারী কৃষি কর্মকর্তা (SAAO) দ্বারা পরামর্শের মাঠ উপযোগিতা যাচাই।
        </motion.p>
        <motion.div variants={enter} className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/researcher-interviewing-farmer.png" alt="গবেষক কর্তৃক কৃষকের সাক্ষাৎকার গ্রহণ" className="aspect-video w-full object-cover" />
          </div>
          <div className="overflow-hidden rounded-xl border rule">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/assets/small_group_researcher_farmer_discussion.png" alt="কৃষক দলীয় আলোচনা" className="aspect-video w-full object-cover" />
          </div>
        </motion.div>
        <motion.div variants={enter} className="mt-6 grid grid-cols-3 gap-3">
          <CountCell bordered value={RESEARCH_STATS_N.fieldInterviews} label="কৃষক সাক্ষাৎকার" />
          <CountCell bordered value={69} label="SAAO কর্মকর্তা যাচাই" />
          <CountCell bordered value={100} suffix="%" label="বিশেষজ্ঞ সম্মতি" />
        </motion.div>
      </motion.section>

      {/* === Institutions === */}
      <motion.section initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger}>
        <motion.h2 variants={enter} className="mb-3 font-display text-2xl text-ink">
          সহযোগী গবেষণা ও সরকারি প্রতিষ্ঠানসমূহ
        </motion.h2>
        <motion.p variants={enter} className="mb-4 text-sm text-ink-soft">
          {RESEARCH_STATS.institutions}টি জাতীয় ও আন্তর্জাতিক কৃষি প্রতিষ্ঠান থেকে সংগৃহীত {RESEARCH_STATS.publications}টি অনুমোদিত প্রকাশনা।
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
            <span className="font-medium text-clay">গবেষণা প্রোটোটাইপ ও নিরাপত্তা বার্তা:</span>{" "}
            অনিয়ন্ত্রিত এলএলএম-এর রাসায়নিক হ্যালুসিনেশন ঝুঁকি ({RESEARCH_STATS.hallucinationFloor}) প্রতিরোধে আমাদের মাল্টি-এজেন্ট ভেরিফায়ার সিস্টেম সরকারি নির্দেশিকা থেকে যাচাইকৃত সঠিক ডোজ নিশ্চিত করে।
          </p>
        </motion.div>
        <motion.div variants={enter} className="grid grid-cols-2 gap-px overflow-hidden rounded-xl border rule bg-bone sm:grid-cols-4">
          <CountCell value={RESEARCH_STATS_N.publications} label="সরকারি প্রকাশনা" />
          <CountCell value={RESEARCH_STATS_N.knowledgeNodes} label="জ্ঞানভাণ্ডার নোড" />
          <CountCell value={RESEARCH_STATS_N.benchmarkInstances} label="বেঞ্চমার্ক প্রশ্নোত্তর" />
          <CountCell value={RESEARCH_STATS_N.dialects} label="আঞ্চলিক উপভাষা" />
        </motion.div>
      </motion.section>

      <motion.p variants={enter} className="border-t rule pt-6 text-center text-xs text-ink-faint">
        গবেষণা প্রোটোটাইপ — CC-BY-4.0 লাইসেন্স। © 2026 North South University.
      </motion.p>
    </div>
  );
}
