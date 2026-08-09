"use client";

import { motion } from "motion/react";
import { AlertTriangle } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex min-h-[55vh] flex-col items-center justify-center gap-6 px-5 text-center">
      <motion.div
        initial={{ scale: 0.85, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-clay-soft/40 text-clay"
      >
        <AlertTriangle className="h-7 w-7" strokeWidth={1.5} />
      </motion.div>

      <div className="space-y-2">
        <h2 className="font-display text-2xl text-ink">কিছু একটা ঠিক নেই</h2>
        <p className="mx-auto max-w-md text-sm leading-relaxed text-ink-soft">
          দুঃখিত, একটি সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।
        </p>
        {error?.message && (
          <p className="mx-auto mt-1 max-w-md break-words rounded-md bg-clay-soft/30 px-3 py-2 font-mono text-xs text-clay">
            {error.message}
          </p>
        )}
      </div>

      <button
        onClick={reset}
        className="rounded-lg bg-leaf px-6 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
      >
        আবার চেষ্টা করুন
      </button>
    </div>
  );
}
