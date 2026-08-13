"use client";

import { motion } from "motion/react";
import { PhoneCall, Siren, ShieldCheck } from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";

/* =========================================================================
   যোগাযোগ (Contact) — real government helplines only, no fabricated
   contact details. Hours are from the DAE extension manual in the corpus
   (call centre open 9am–5pm, except Fridays & government holidays).
   ========================================================================= */

export default function ContactPage() {
  return (
    <div className="mx-auto max-w-2xl space-y-8 py-12">
      {/* Header */}
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">
          যোগাযোগ
        </motion.p>
        <motion.h1 variants={enter} className="mt-3 font-display text-3xl text-ink">
          সাহায্য ও পরামর্শ
        </motion.h1>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          কৃষি সংক্রান্ত যেকোনো প্রশ্নের জন্য নিচের সরকারি নম্বরে সরাসরি কল করুন।
        </motion.p>
      </motion.div>

      {/* Helpline cards */}
      <motion.div initial="hidden" animate="visible" variants={stagger} className="space-y-3">
        <motion.a
          variants={enter}
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="group flex items-center justify-between gap-4 rounded-xl border rule bg-paper px-5 py-4 transition-all hover:-translate-y-0.5 hover:border-leaf hover:shadow-[0_10px_28px_rgba(52,39,23,0.08)]"
        >
          <div className="flex min-w-0 items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
              <PhoneCall className="h-5 w-5" />
            </div>
            <div>
              <div className="text-xs font-semibold text-ink-faint">কৃষক কল সেন্টার</div>
              <div className="mt-0.5 text-sm text-ink">বাংলাদেশ সরকার · সকাল ৯টা–বিকাল ৫টা</div>
            </div>
          </div>
          <span className="shrink-0 tabular text-lg font-semibold text-leaf">
            {HELPLINE.krishiCallCenter}
          </span>
        </motion.a>

        <motion.a
          variants={enter}
          href={`tel:${HELPLINE.emergency}`}
          className="group flex items-center justify-between gap-4 rounded-xl border rule bg-paper px-5 py-4 transition-all hover:-translate-y-0.5 hover:border-clay hover:shadow-[0_10px_28px_rgba(52,39,23,0.08)]"
        >
          <div className="flex min-w-0 items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-clay/10 text-clay">
              <Siren className="h-5 w-5" />
            </div>
            <div>
              <div className="text-xs font-semibold text-ink-faint">জরুরি</div>
              <div className="mt-0.5 text-sm text-ink">জাতীয় জরুরি সেবা</div>
            </div>
          </div>
          <span className="shrink-0 tabular text-lg font-semibold text-clay">
            {HELPLINE.emergency}
          </span>
        </motion.a>
      </motion.div>

      {/* Prototype note */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="flex items-start gap-3 rounded-xl border rule bg-paper-2/40 px-5 py-4"
      >
        <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-leaf" />
        <p className="text-xs leading-relaxed text-ink-faint">
          এই ব্যবস্থা একটি গবেষণা প্রোটোটাইপ — এটি জরুরি সেবার বিকল্প নয়। জরুরি
          পরিস্থিতিতে সরাসরি ৯৯৯ নম্বরে কল করুন।
        </p>
      </motion.div>
    </div>
  );
}