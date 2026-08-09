"use client";
import { motion } from "motion/react";

export default function Loading() {
  return (
    <div className="flex min-h-[55vh] flex-col items-center justify-center gap-5">
      <motion.div
        className="h-10 w-10 rounded-full border-2 border-bone border-t-leaf"
        animate={{ rotate: 360 }}
        transition={{ duration: 1.1, repeat: Infinity, ease: "linear" }}
      />
      <motion.p
        className="text-sm text-ink-soft"
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
      >
        লোড হচ্ছে…
      </motion.p>
    </div>
  );
}
