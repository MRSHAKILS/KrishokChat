"use client";

import { motion } from "motion/react";
import { PhoneCall, Siren, ShieldCheck } from "lucide-react";
import { HELPLINE, HELPLINE_EN } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   যোগাযোগ (Contact) — real government helplines only, no fabricated
   contact details. Hours are from the DAE extension manual in the corpus
   (call centre open 9am–5pm, except Fridays & government holidays).
   ========================================================================= */

const COPY = {
  bn: {
    eyebrow: "জরুরি সহায়তা ও যোগাযোগ",
    title: "কৃষি পরামর্শ ও হেল্পলাইন",
    intro: "কৃষি, বালাই ব্যবস্থাপনা বা কীটনাশক ব্যবহারের যেকোনো জরুরি সন্দেহে সরাসরি নিচের সরকারি হটলাইনে কল করুন।",
    callCenterTitle: "কৃষক কল সেন্টার (AIS / DAE)",
    callCenterHours: "সকাল ৯টা–বিকাল ৫টা (শুক্রবার ও সরকারি ছুটি ব্যতীত)",
    emergencyTitle: "জাতীয় জরুরি সেবা (৯৯৯)",
    emergencyDesc: "কীটনাশক বিষক্রিয়া, দুর্ঘটনা ও তাৎক্ষণিক জরুরি সহায়তা",
    saaoTitle: "মাঠ পর্যায়ের উপসহকারী কৃষি কর্মকর্তা (SAAO)",
    saaoDesc: "কীটনাশকের সঠিক ডোজ বা কোনো বিশেষ রোগের ক্ষেত্রে স্থানীয় উপসহকারী কৃষি কর্মকর্তার সাথে পরামর্শ করুন অথবা আপনার নিকটস্থ উপজেলা কৃষি অফিসে নমুনা প্রদর্শন করুন।",
    prototypeNote: "কৃষক টেক একটি গবেষণা প্রোটোটাইপ। এটি বিশেষজ্ঞ কৃষি সম্প্রসারণ পরামর্শের সহায়ক হিসেবে কাজ করে, কোনো চরম বিষক্রিয়া বা জরুরি অবস্থায় অবিলম্বে সরকারি ৯৯৯ বা নিকটস্থ স্বাস্থ্যকেন্দ্রে যোগাযোগ করুন।",
  },
  en: {
    eyebrow: "Emergency Assistance and Contact",
    title: "Agricultural Advisory and Helplines",
    intro: "For any urgent concern about crops, pest management, or pesticide use, call the government hotlines below directly.",
    callCenterTitle: "Farmer Call Center (AIS / DAE)",
    callCenterHours: "9am–5pm (except Fridays and government holidays)",
    emergencyTitle: "National Emergency Service (999)",
    emergencyDesc: "Pesticide poisoning, accidents, and immediate emergency assistance",
    saaoTitle: "Field-level Sub-Assistant Agriculture Officer (SAAO)",
    saaoDesc: "For the correct pesticide dose or a specific disease case, consult your local sub-assistant agriculture officer or show a sample at your nearest upazila agriculture office.",
    prototypeNote: "KrishokTech is a research prototype. It works as an aid alongside expert agricultural extension advice — in any severe poisoning or emergency, contact the government 999 line or your nearest health center immediately.",
  },
} as const;

export default function ContactPage() {
  const { locale } = useLanguage();
  const c = COPY[locale === "en" ? "en" : "bn"];
  const en = locale === "en";
  return (
    <div className="mx-auto max-w-2xl space-y-8 py-12">
      {/* Header */}
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre font-semibold">
          {c.eyebrow}
        </motion.p>
        <motion.h1 variants={enter} className="mt-3 font-display text-3xl text-ink sm:text-4xl">
          {c.title}
        </motion.h1>
        <motion.p variants={enter} className="mt-2 text-sm text-ink-soft">
          {c.intro}
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
              <div className="text-xs font-semibold text-leaf">{c.callCenterTitle}</div>
              <div className="mt-0.5 text-sm text-ink">{c.callCenterHours}</div>
            </div>
          </div>
          <span className="shrink-0 tabular text-xl font-bold text-leaf">
            {en ? HELPLINE_EN.krishiCallCenter : HELPLINE.krishiCallCenter}
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
              <div className="text-xs font-semibold text-clay">{c.emergencyTitle}</div>
              <div className="mt-0.5 text-sm text-ink">{c.emergencyDesc}</div>
            </div>
          </div>
          <span className="shrink-0 tabular text-xl font-bold text-clay">
            {en ? HELPLINE_EN.emergency : HELPLINE.emergency}
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
          {c.saaoTitle}
        </div>
        <p className="mt-2 text-xs leading-relaxed text-ink-soft">
          {c.saaoDesc}
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
          {c.prototypeNote}
        </p>
      </motion.div>
    </div>
  );
}