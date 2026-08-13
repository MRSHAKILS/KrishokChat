"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Lock, ChevronDown, FlaskConical, MessageCircle } from "lucide-react";
import type { SoilDatasetInfo } from "@/lib/api";
import { bn } from "@/lib/bn";
import { dur, ease } from "@/lib/motion";

/* =========================================================================
   SoilLockedCard — the honest "coming soon" state.
   The analyzer is deliberately locked: every model currently underperforms
   the mean predictor (negative R²). This card explains WHY with real
   numbers, so the lock reads as research integrity, not a missing feature.
   ========================================================================= */

export function SoilLockedCard({
  info,
  message,
  onAskChat,
}: {
  info: SoilDatasetInfo | null;
  message?: string | null;
  onAskChat?: () => void;
}) {
  const [showTable, setShowTable] = useState(false);
  const models = info?.model_results ?? [];

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
            <h3 className="font-display text-lg text-ink">স্বয়ংক্রিয় আর্দ্রতা নির্ণয় — উন্নয়নে</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-soft">
              {message ??
                "ছবি থেকে মাটির আর্দ্রতা মাপার মডেলটি এখনো যাচাই পর্যায়ে আছে, তাই এই মুহূর্তে চালু করা হয়নি। ডেটাসেটটি প্রকাশিত হয়েছে — মডেল প্রস্তুত হলে এখানে ফলাফল দেখানো হবে।"}
            </p>
          </div>
        </div>

        {/* Honest benchmark table */}
        {models.length > 0 && (
          <div className="mt-4 rounded-xl border rule bg-paper p-4">
            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1.5 text-xs font-semibold text-ink">
                <FlaskConical className="h-3.5 w-3.5 text-ochre" />
                গবেষণার বর্তমান ফলাফল (খোলামেলা)
              </span>
              <button
                onClick={() => setShowTable((v) => !v)}
                className="flex items-center gap-1 text-[11px] font-medium text-leaf hover:text-leaf-2"
                aria-expanded={showTable}
              >
                {showTable ? "লুকান" : `${bn(models.length)}টি মডেল দেখুন`}
                <ChevronDown className={`h-3 w-3 transition-transform ${showTable ? "rotate-180" : ""}`} />
              </button>
            </div>
            <p className="mt-1.5 text-[11px] leading-relaxed text-ink-faint">
              প্রতিটি মডেলের R² ঋণাত্মক — অর্থাৎ গড় অনুমানের চেয়েও কম নির্ভুল। তাই যাচাইয়ের আগে চালু করলে বিভ্রান্তি তৈরি হতো।
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
                        <tr className="border-b rule text-[10px] uppercase tracking-wide text-ink-faint">
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