"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Lock, ChevronDown, FlaskConical, MessageCircle, Droplets, CheckCircle2, AlertTriangle, Info, Sparkles } from "lucide-react";
import type { SoilDatasetInfo, SoilAnalyzeResponse } from "@/lib/api";
import { bn } from "@/lib/bn";
import { dur, ease } from "@/lib/motion";

export function SoilLockedCard({
  info,
  result,
  message,
  onAskChat,
}: {
  info: SoilDatasetInfo | null;
  result?: SoilAnalyzeResponse | null;
  message?: string | null;
  onAskChat?: () => void;
}) {
  const [showTable, setShowTable] = useState(false);
  const models = info?.model_results ?? [];

  // If the result is an analyzed (measured-sample replay), render the diagnostic card.
  if (result && result.status === "analyzed") {
    const isReplay = Boolean(result.sample_id);
    const kpa = result.kpa;
    const soilType = result.soil_type_bn ?? result.soil_type ?? "";
    const statusBn = result.moisture_status_bn ?? "";
    const advisory = result.advisory_bn ?? "";
    if (kpa == null || !soilType || !advisory) {
      // Defensive: a malformed analyzed payload must not invent values.
      return null;
    }

    // Determine color styling based on kPa
    const isDry = kpa >= 12.0;
    const isWet = kpa <= 2.0;

    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: dur.normal, ease: ease.smooth }}
        className="overflow-hidden rounded-2xl border border-leaf/40 bg-paper shadow-[0_12px_32px_rgba(34,70,44,0.08)]"
      >
        <div className="p-5 sm:p-6">
          {/* Header */}
          <div className="flex items-start justify-between gap-3 border-b rule pb-4">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-leaf/15 text-leaf">
                <Droplets className="h-6 w-6" strokeWidth={1.75} />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="font-display text-lg font-bold text-ink">মাটির আর্দ্রতা ও সেচ বিশ্লেষণ</h3>
                  {isReplay ? (
                    <span
                      className="inline-flex items-center gap-1 rounded-full bg-sky-600/10 px-2 py-0.5 text-xs font-semibold text-sky-700"
                      title="ডেটাসেট নমুনার মাঠে পরিমাপিত রেকর্ড — লাইভ মডেল নির্ণয় নয়"
                    >
                      <FlaskConical className="h-3 w-3" /> ডেটাসেট নমুনা {result.sample_id}
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 rounded-full bg-leaf/15 px-2 py-0.5 text-xs font-semibold text-leaf">
                      <Sparkles className="h-3 w-3" /> নির্ণীত
                    </span>
                  )}
                </div>
                <p className="text-xs text-ink-soft">পাবনা টেনশিওমিটার ফিল্ড সেন্সর গ্রাউন্ডেড · মাঠে পরিমাপিত মান</p>
              </div>
            </div>
            <div className="text-right">
              <span className="text-xs font-medium text-ink-faint">উৎস</span>
              <div className="font-display text-sm font-bold text-sky-700">{isReplay ? "পরিমাপিত" : bn(Math.round((result.confidence ?? 0) * 100)) + "%"}</div>
            </div>
          </div>

          {/* Key Metrics Grid */}
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
            {/* Metric 1: Tension in kPa */}
            <div className="rounded-xl border rule bg-paper-2 p-3.5 text-center">
              <span className="text-xs font-medium text-ink-faint">আর্দ্রতা টান (Tension)</span>
              <div className="mt-1 font-display text-2xl font-black text-ink">
                {bn(kpa.toFixed(1))} <span className="text-xs font-normal text-ink-soft">kPa</span>
              </div>
              <div className="mt-1 flex items-center justify-center gap-1 text-xs text-ink-soft">
                {isDry ? (
                  <span className="font-medium text-clay">ঘাটতি এলাকা (&gt;১২ kPa)</span>
                ) : isWet ? (
                  <span className="font-medium text-sky-600">সম্পৃক্ত এলাকা (&lt;২ kPa)</span>
                ) : (
                  <span className="font-medium text-leaf">আদর্শ মাত্রা (২-১০ kPa)</span>
                )}
              </div>
            </div>

            {/* Metric 2: Soil Classification */}
            <div className="rounded-xl border rule bg-paper-2 p-3.5 text-center">
              <span className="text-xs font-medium text-ink-faint">{isReplay ? "নমুনা রেকর্ডের মাটির ধরন" : "শনাক্তকৃত মাটির ধরন"}</span>
              <div className="mt-1 font-display text-lg font-bold text-ink">{soilType}</div>
              <span className="mt-1 inline-block text-xs text-ink-soft">{result.soil_type || ""}</span>
            </div>

            {/* Metric 3: Moisture Condition */}
            <div className="rounded-xl border rule bg-paper-2 p-3.5 text-center">
              <span className="text-xs font-medium text-ink-faint">আর্দ্রতার অবস্থা</span>
              <div className={`mt-1 font-display text-base font-bold ${isDry ? "text-clay" : isWet ? "text-sky-700" : "text-leaf"}`}>
                {statusBn}
              </div>
              <div className="mt-1 flex items-center justify-center gap-1 text-xs text-ink-soft">
                {isDry ? <AlertTriangle className="h-3 w-3 text-clay" /> : <CheckCircle2 className="h-3 w-3 text-leaf" />}
                {isDry ? "সেচ প্রয়োজন" : isWet ? "সেচ স্থগিত রাখুন" : "সেচ প্রয়োজন নেই"}
              </div>
            </div>
          </div>

          {/* Actionable Irrigation Advisory */}
          <div className="mt-4 rounded-xl border border-leaf/30 bg-leaf/5 p-4">
            <h4 className="flex items-center gap-1.5 text-xs font-bold text-ink">
              <Info className="h-4 w-4 text-leaf" />
              মাঠ পর্যায়ের সেচ ও পরিচর্যা সুপারিশ:
            </h4>
            <p className="mt-2 text-sm leading-relaxed text-ink-soft">{advisory}</p>
          </div>

          {/* Ask in Chat Action */}
          {onAskChat && (
            <button
              onClick={onAskChat}
              className="mt-4 flex min-h-11 w-full items-center justify-center gap-2 rounded-xl bg-leaf px-4 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
            >
              <MessageCircle className="h-4 w-4" />
              এই মাটির সেচ ও সার ব্যবস্থাপনা নিয়ে চ্যাটে কথা বলুন
            </button>
          )}
        </div>
      </motion.div>
    );
  }

  // Fallback: Honest Locked Card
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="overflow-hidden rounded-2xl border border-ochre-soft/60 bg-ochre-soft/10 shadow-[0_10px_28px_rgba(52,39,23,0.05)]"
    >
      <div className="p-5 sm:p-6">
        <div className="flex items-start gap-3.5">
          <motion.div
            initial={{ scale: 0.85, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 18, delay: 0.1 }}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-ochre/15 text-ochre"
          >
            <Lock className="h-5 w-5" strokeWidth={1.5} />
          </motion.div>
          <div className="flex-1">
            <h3 className="font-display text-lg text-ink">স্বয়ংক্রিয় আর্দ্রতা নির্ণয় — ডেটাসেট ভিত্তিক</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-soft">
              {message ??
                "পাবনা রিসার্চ সাইটের বাস্তব ফিল্ড ডেটাসেটের ভিত্তিতে নমুনা মাটির আর্দ্রতা ও টেনশন বিশ্লেষণ করা হয়েছে।"}
            </p>
          </div>
        </div>

        {/* Honest benchmark table */}
        {models.length > 0 && (
          <div className="mt-4 rounded-xl border rule bg-paper p-4">
            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1.5 text-xs font-semibold text-ink">
                <FlaskConical className="h-3.5 w-3.5 text-ochre" />
                গবেষণার বর্তমান ফলাফল ও ডেটাসেট মেট্রিক্স
              </span>
              <button
                onClick={() => setShowTable((v) => !v)}
                className="flex items-center gap-1 text-xs font-medium text-leaf hover:text-leaf-2"
                aria-expanded={showTable}
              >
                {showTable ? "লুকান" : `${bn(models.length)}টি মডেল দেখুন`}
                <ChevronDown className={`h-3 w-3 transition-transform ${showTable ? "rotate-180" : ""}`} />
              </button>
            </div>
            <p className="mt-1.5 text-xs leading-relaxed text-ink-faint">
              ৭২২টি ডিজিটাল টেনশিওমিটার পরিমাপের সাথে ইমেজ ফিচারের তুলনামূলক আরএমএসই (RMSE) স্কোর।
            </p>
            <AnimatePresence initial={false}>
              {showTable && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: dur.normal, ease: ease.smooth }}
                  className="overflow-hidden"
                >
                  <div className="mt-3 overflow-x-auto">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="border-b rule text-xs text-ink-faint">
                          <th className="py-2 pr-3 font-medium">মডেল</th>
                          <th className="py-2 pr-3 text-right font-medium">RMSE (kPa)</th>
                          <th className="py-2 text-right font-medium">R²</th>
                        </tr>
                      </thead>
                      <tbody>
                        {models.map((m) => (
                          <tr key={m.model} className="border-b border-bone/50 last:border-0">
                            <td className="py-2 pr-3 text-ink-soft">{m.model}</td>
                            <td className="py-2 pr-3 text-right tabular text-ink">{bn(m.rmse_kpa.toFixed(2))}</td>
                            <td className="py-2 text-right tabular text-clay">{bn(m.r2.toFixed(2))}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}

        {/* What you CAN do now */}
        {onAskChat && (
          <button
            onClick={onAskChat}
            className="mt-4 flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
          >
            <MessageCircle className="h-4 w-4" />
            মাটি ও পানি নিয়ে চ্যাটে প্রশ্ন করুন
          </button>
        )}
      </div>
    </motion.div>
  );
}