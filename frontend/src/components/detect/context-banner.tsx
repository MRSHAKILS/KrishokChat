"use client";

import { motion, AnimatePresence } from "motion/react";
import { Leaf } from "lucide-react";
import { humanizeLabel } from "@/lib/bn";

/* =========================================================================
   ContextBanner — slim banner above the chat panel that shows what was
   detected and tells the farmer "ask about this crop."
   Automatically passes detectedCrop + detectedDisease to the QAPanel.
   ========================================================================= */

export function ContextBanner({
  crop,
  disease,
}: {
  crop: string | null;
  disease: string | null;
}) {
  return (
    <AnimatePresence>
      {crop && disease && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          className="overflow-hidden"
        >
          <div className="flex items-center gap-2.5 rounded-lg border border-leaf/20 bg-leaf/5 px-4 py-3">
            <Leaf className="h-4 w-4 shrink-0 text-leaf" strokeWidth={1.5} />
            <div className="text-sm">
              <span className="font-medium text-leaf">
                {crop} — {humanizeLabel(disease)}
              </span>
              <span className="text-ink-soft"> সনাক্ত হয়েছে।</span>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
