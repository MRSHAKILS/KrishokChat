"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { ArrowRight, Building2, Landmark, Database, TrendingUp } from "lucide-react";
import { enter, stagger } from "@/lib/motion";

/* =========================================================================
   Landing page teaser — compact 3-card business model section.
   Inserted after InstitutionalTrustSection, before AgriFAQSection.
   ========================================================================= */

const LANES = [
  {
    icon: Landmark,
    name: "সরকারি অংশীদারিত্ব",
    who: "DAE · a2i · ১৬১২৩ কল সেন্টার",
    value: "১৬১২৩-এর AI ফ্রন্ট-এন্ড — ট্রায়েজ ও এসক্যালেশন, প্রতিযোগিতা নয়।",
    evidence: "৯২,০৯৪ কল/বছর · B2G প্রাথমিক",
    accent: "ochre",
  },
  {
    icon: Building2,
    name: "B2B অ্যানালিটিক্স",
    who: "ডিলার · বীজ কোম্পানি · SAAO",
    value: "জেলাভিত্তিক রোগ স্পাইক ও রাসায়নিক ডিমান্ড অ্যানালিটিক্স।",
    evidence: "ACI Fosholi: €৩.৫M · PxD: ৭.৮M",
    accent: "leaf",
  },
  {
    icon: Database,
    name: "ডেটাসেট ও API লাইসেন্সিং",
    who: "গবেষক · কৃষি-ফিনটেক · NGO",
    value: "৮৫,৯৭৯-ইনস্ট্যান্স বেঞ্চমার্ক + ৭২২-ইমেজ মাটির ডেটাসেট (CC-BY-4.0)।",
    evidence: "CC-BY-4.0 · ২ পেপার",
    accent: "clay",
  },
] as const;

/* Static color classes (Tailwind-safe) */
const ACCENT = {
  leaf: { iconBg: "bg-leaf/10", iconText: "text-leaf", border: "hover:border-leaf/40" },
  ochre: { iconBg: "bg-ochre/10", iconText: "text-ochre", border: "hover:border-ochre/40" },
  clay: { iconBg: "bg-clay/10", iconText: "text-clay", border: "hover:border-clay/40" },
} as const;

export function BusinessModelSection() {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
      variants={stagger}
      className="mx-auto max-w-5xl"
    >
      <motion.div variants={enter} className="mb-6 text-center">
        <div className="flex items-center justify-center gap-2 text-leaf">
          <TrendingUp className="h-5 w-5" />
          <h2 className="font-display text-xl text-ink sm:text-2xl">ব্যবসায়িক মডেল ও টেকসই আয়</h2>
        </div>
        <p className="mt-2 text-xs text-ink-faint">
          কৃষকের জন্য সর্বদা বিনামূল্যে · প্রতি LLM উত্তর ~২ পয়সা · B2G সর্বোচ্চ অগ্রাধিকার — Business Model & Sustainability
        </p>
      </motion.div>

      <motion.div variants={enter} className="grid gap-3 sm:grid-cols-3">
        {LANES.map((lane, i) => {
          const Icon = lane.icon;
          const a = ACCENT[lane.accent];
          return (
            <div
              key={i}
              className={`surface-lift rounded-2xl border rule bg-paper p-5 transition-colors ${a.border}`}
            >
              <div className="flex items-center gap-2.5">
                <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${a.iconBg}`}>
                  <Icon className={`h-4.5 w-4.5 ${a.iconText}`} />
                </div>
                <h3 className="font-display text-sm font-semibold text-ink">{lane.name}</h3>
              </div>
              <p className="mt-3 text-[11px] text-ink-faint">{lane.who}</p>
              <p className="mt-2 text-xs leading-relaxed text-ink-soft">{lane.value}</p>
              <div className="mt-3 inline-block rounded-full bg-paper-2 px-2.5 py-0.5 text-[10px] font-medium text-ink-faint">
                {lane.evidence}
              </div>
            </div>
          );
        })}
      </motion.div>

      <motion.div variants={enter} className="mt-5 text-center">
        <Link
          href="/business"
          className="control-press group inline-flex items-center gap-2 rounded-xl border rule px-5 py-2.5 text-sm font-medium text-ink-soft hover:border-leaf/50 hover:bg-paper-2"
        >
          বিস্তারিত দেখুন <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
        </Link>
      </motion.div>
    </motion.section>
  );
}