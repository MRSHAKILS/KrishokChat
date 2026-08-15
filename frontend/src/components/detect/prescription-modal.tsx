"use client";

import { useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  X,
  Printer,
  Share2,
  Phone,
  ShieldCheck,
  Building2,
  Calendar,
  CheckCircle2,
  AlertCircle,
  Copy,
  Check,
} from "lucide-react";
import { APP, HELPLINE } from "@/lib/constants";
import { toBn } from "@/lib/use-count-up";
import { cropBn, translateDiseaseToBn, humanizeLabel } from "@/lib/bn";
import type { DetectResponse } from "@/lib/api";

interface PrescriptionModalProps {
  open: boolean;
  onClose: () => void;
  result: DetectResponse;
  cropHint?: string;
}

export function PrescriptionModal({
  open,
  onClose,
  result,
  cropHint,
}: PrescriptionModalProps) {
  const [copied, setCopied] = useState(false);
  const printRef = useRef<HTMLDivElement>(null);

  if (!open) return null;

  const cropDisplay = result.crop ? cropBn(result.crop) : (cropHint || "চিহ্নিত ফসল");
  const diseaseDisplay = result.disease ? translateDiseaseToBn(result.disease) : (result.disease_info?.class_name || "শনাক্তকৃত রোগ");

  const todayBn = new Intl.DateTimeFormat("bn-BD", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date());

  const handlePrint = () => {
    window.print();
  };

  const handleShare = async () => {
    const textToShare = `🌾 ${APP.name} — কৃষি পরামর্শ ও ব্যবস্থাপত্র\nফসল: ${cropDisplay}\nরোগ: ${diseaseDisplay}\n\nপরামর্শ: ${result.treatment_advice?.slice(0, 200)}...\n\nজরুরি কৃষি সহায়তা: ১৬১২৩`;

    if (typeof navigator !== "undefined" && navigator.share) {
      try {
        await navigator.share({
          title: `${APP.name} — কৃষি ব্যবস্থাপত্র`,
          text: textToShare,
          url: window.location.href,
        });
        return;
      } catch {
        // User cancelled or share failed, fallback to copy
      }
    }

    try {
      await navigator.clipboard.writeText(textToShare);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      // ignore
    }
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-ink/60 backdrop-blur-xs transition-opacity"
        />

        {/* Modal Window */}
        <motion.div
          initial={{ opacity: 0, scale: 0.96, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.96, y: 10 }}
          transition={{ type: "spring", stiffness: 300, damping: 26 }}
          className="relative z-10 w-full max-w-2xl overflow-hidden rounded-2xl border rule bg-paper shadow-2xl"
        >
          {/* Top action bar (hidden during print) */}
          <div className="flex items-center justify-between border-b rule bg-paper-2/60 px-5 py-3.5 print:hidden">
            <div className="flex items-center gap-2 text-xs font-semibold text-leaf">
              <ShieldCheck className="h-4 w-4" />
              <span>কৃষি পরামর্শ ও ব্যবস্থাপত্র পত্রক</span>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handlePrint}
                className="control-press inline-flex items-center gap-1.5 rounded-lg border border-leaf/30 bg-paper px-3 py-1.5 text-xs font-semibold text-leaf hover:bg-leaf/10 cursor-pointer"
              >
                <Printer className="h-3.5 w-3.5" /> প্রিন্ট / PDF
              </button>
              <button
                type="button"
                onClick={handleShare}
                className="control-press inline-flex items-center gap-1.5 rounded-lg border rule bg-paper px-3 py-1.5 text-xs font-medium text-ink-soft hover:bg-paper-2 cursor-pointer"
              >
                {copied ? (
                  <>
                    <Check className="h-3.5 w-3.5 text-leaf" /> কপি হয়েছে
                  </>
                ) : (
                  <>
                    <Share2 className="h-3.5 w-3.5" /> শেয়ার
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg p-1.5 text-ink-faint hover:bg-paper-2 hover:text-ink cursor-pointer"
                aria-label="বন্ধ করুন"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Printable Prescription Body */}
          <div
            ref={printRef}
            className="max-h-[75vh] overflow-y-auto p-6 sm:p-8 space-y-6 text-ink bg-paper print:max-h-none print:p-0"
          >
            {/* Prescription Header */}
            <div className="border-b-2 border-leaf pb-5 text-center">
              <div className="flex items-center justify-center gap-2 text-leaf font-semibold text-xs tracking-wider uppercase">
                <Building2 className="h-4 w-4" />
                <span>গণপ্রজাতন্ত্রী বাংলাদেশ কৃষি নির্দেশিকা ও এআই ভেরিফাইড</span>
              </div>
              <h2 className="mt-2 font-display text-2xl font-bold text-ink sm:text-3xl">
                {APP.name} — ডিজিটাল কৃষি ব্যবস্থাপত্র
              </h2>
              <p className="mt-1 text-xs text-ink-soft">
                প্রমাণ-সংরক্ষিত কৃষি বালাই ও রোগ ব্যবস্থাপনা পরামর্শ পত্র
              </p>
              <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-dashed border-bone pt-3 text-xs text-ink-faint">
                <div className="flex items-center gap-1.5">
                  <Calendar className="h-3.5 w-3.5 text-ochre" />
                  <span>তারিখ: {todayBn}</span>
                </div>
                <div>
                  রেফারেন্স আইডি: <span className="font-mono text-ink">KC-{Date.now().toString().slice(-6)}</span>
                </div>
              </div>
            </div>

            {/* Diagnosis Overview Grid */}
            <div className="grid grid-cols-2 gap-3 rounded-xl border border-leaf/20 bg-leaf/5 p-4 sm:grid-cols-3">
              <div>
                <div className="text-[11px] font-semibold text-ink-faint">আক্রান্ত ফসল</div>
                <div className="mt-0.5 font-display text-base font-bold text-leaf">
                  {cropDisplay}
                </div>
              </div>
              <div>
                <div className="text-[11px] font-semibold text-ink-faint">শনাক্তকৃত রোগ</div>
                <div className="mt-0.5 font-display text-base font-bold text-clay">
                  {diseaseDisplay}
                </div>
              </div>
              <div className="col-span-2 sm:col-span-1">
                <div className="text-[11px] font-semibold text-ink-faint">নিশ্চয়তা / নির্ভরযোগ্যতা</div>
                <div className="mt-0.5 text-xs font-semibold text-leaf flex items-center gap-1">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  {result.treatment_confidence === "verified" ? "সরকারি তথ্যে যাচাইকৃত" : "আংশিক যাচাইকৃত"}
                </div>
              </div>
            </div>

            {/* Prescribed Treatment Section */}
            <div className="space-y-3">
              <h3 className="font-display text-base font-semibold text-ink flex items-center gap-2 border-b rule pb-2">
                <span className="flex h-5 w-5 items-center justify-center rounded-full bg-leaf text-xs font-bold text-paper">
                  ১
                </span>
                চিকিৎসা ও বালাইনাশক প্রয়োগ নির্দেশিকা (Prescription Advice)
              </h3>
              <div className="rounded-xl border rule bg-paper p-4 text-sm leading-relaxed whitespace-pre-wrap text-ink">
                {result.treatment_advice || "উপযুক্ত বালাইনাশকের পরামর্শ নিচে দেওয়া হলো।"}
              </div>
            </div>

            {/* Application & Dosage Precaution */}
            <div className="space-y-3">
              <h3 className="font-display text-base font-semibold text-ink flex items-center gap-2 border-b rule pb-2">
                <span className="flex h-5 w-5 items-center justify-center rounded-full bg-ochre text-xs font-bold text-paper">
                  ২
                </span>
                প্রয়োগের সঠিক নিয়ম ও সতর্কতা (Safety Precautions)
              </h3>
              <ul className="space-y-2 text-xs text-ink-soft">
                <li className="flex items-start gap-2">
                  <span className="text-leaf font-bold">•</span>
                  <span><strong>স্প্রে করার উপযুক্ত সময়:</strong> কড়া রোদে স্প্রে করবেন না; সকালের দিকে বা বিকেলে স্প্রে করুন।</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-leaf font-bold">•</span>
                  <span><strong>সুরক্ষা পোশাক:</strong> মাস্ক, গ্লাভস ও ফুল হাতা জামা পরে স্প্রে করুন। স্প্রে করার সময় ধুমপান বা খাবার গ্রহণ করবেন না।</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-leaf font-bold">•</span>
                  <span><strong>ফসল তোলার বিরতি (PHI):</strong> বালাইনাশক স্প্রে করার পর অন্তত ৭ থেকে ১৪ দিন পর্যন্ত ফসল বাজারজাত বা খাওয়া থেকে বিরত থাকুন।</span>
                </li>
              </ul>
            </div>

            {/* Source Provenance Footer */}
            {result.treatment_sources.length > 0 && (
              <div className="rounded-lg border rule bg-paper-2/30 p-3 text-[11px] text-ink-faint">
                <span className="font-semibold text-ink">তথ্যের প্রাতিষ্ঠানিক উৎস:</span>{" "}
                {result.treatment_sources.join(", ")} — কৃষি সম্প্রসারণ অধিদপ্তর (DAE) ও সংশ্লিষ্ট গবেষণা সংস্থা।
              </div>
            )}

            {/* Emergency Krishi Call Center Footer */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 rounded-xl border border-leaf/30 bg-leaf/10 p-4">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-leaf text-paper font-bold shadow-xs">
                  <Phone className="h-5 w-5" />
                </div>
                <div>
                  <div className="text-xs font-bold text-leaf">কৃষি জরুরি পরামর্শ ও কল সেন্টার</div>
                  <div className="text-[11px] text-ink-soft">যে কোনো প্রশ্নে সরকারি কৃষি কর্মকর্তার সাথে সরাসরি কথা বলুন</div>
                </div>
              </div>
              <div className="font-display text-xl font-bold tabular text-leaf">
                {HELPLINE.krishiCallCenter}
              </div>
            </div>

            {/* Disclaimer */}
            <div className="text-center text-[10px] text-ink-faint border-t rule pt-3">
              * এটি একটি গবেষণা ও সরকারি তথ্য-সংরক্ষিত ডিজিটাল পরামর্শ। কোনো বিভ্রান্তি হলে স্থানীয় উপসহকারী কৃষি কর্মকর্তা (SAAO)-এর সাথে যোগাযোগ করুন।
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
