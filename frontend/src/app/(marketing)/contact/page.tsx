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
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre font-semibold">
          জরুরি সহায়তা ও যোগাযোগ
        </motion.p>
        <motion.h1 variants={enter} className="mt-3 font-display text-3xl text-ink sm:text-4xl">
          কৃষি পরামর্শ ও হেল্পলাইন
        </motion.h1>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          কৃষি, বালাই ব্যবস্থাপনা বা কীটনাশক ব্যবহারের যেকোনো জরুরি সন্দেহে সরাসরি নিচের সরকারি হটলাইনে কল করুন।
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
              <div className="text-xs font-semibold text-leaf">কৃষক কল সেন্টার (AIS / DAE)</div>
              <div className="mt-0.5 text-sm text-ink">সকাল ৯টা–বিকাল ৫টা (শুক্রবার ও সরকারি ছুটি ব্যতীত)</div>
            </div>
          </div>
          <span className="shrink-0 tabular text-xl font-bold text-leaf">
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
              <div className="text-xs font-semibold text-clay">জাতীয় জরুরি সেবা (৯৯৯)</div>
              <div className="mt-0.5 text-sm text-ink">কীটনাশক বিষক্রিয়া, দুর্ঘটনা ও তাৎক্ষণিক জরুরি সহায়তা</div>
            </div>
          </div>
          <span className="shrink-0 tabular text-xl font-bold text-clay">
            {HELPLINE.emergency}
          </span>
        </motion.a>
      </motion.div>

      {/* Extension Officer / Field Guidance */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="rounded-xl border rule bg-paper p-5"
      >
        <div className="flex items-center gap-2 text-sm font-semibold text-ink">
          <ShieldCheck className="h-4 w-4 text-leaf" />
          মাঠ পর্যায়ের উপসহকারী কৃষি কর্মকর্তা (SAAO)
        </div>
        <p className="mt-2 text-xs leading-relaxed text-ink-soft">
          কীটনাশকের সঠিক ডোজ বা কোনো বিশেষ রোগের ক্ষেত্রে স্থানীয় উপসহকারী কৃষি কর্মকর্তার সাথে পরামর্শ করুন অথবা আপনার নিকটস্থ উপজেলা কৃষি অফিসে নমুনা প্রদর্শন করুন।
        </p>
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
          কৃষক চ্যাট একটি গবেষণা প্রোটোটাইপ। এটি বিশেষজ্ঞ কৃষি সম্প্রসারণ পরামর্শের সহায়ক হিসেবে কাজ করে, কোনো চরম বিষক্রিয়া বা জরুরি অবস্থায় অবিলম্বে সরকারি ৯৯৯ বা নিকটস্থ স্বাস্থ্যকেন্দ্রে যোগাযোগ করুন।
        </p>
      </motion.div>
    </div>
  );
}