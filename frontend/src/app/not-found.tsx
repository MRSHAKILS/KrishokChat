"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { ArrowRight, Camera } from "lucide-react";

export default function NotFound() {
  return (
    <div className="flex min-h-[55vh] flex-col items-center justify-center gap-6 px-5 text-center">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
        className="font-display text-6xl text-leaf tabular"
      >
        ৪০৪
      </motion.div>

      <div className="space-y-2">
        <h2 className="font-display text-2xl text-ink">পাতাটি পাওয়া যায়নি</h2>
        <p className="text-sm text-ink-soft">আপনি যে পাতাটি খুঁজছেন সেটি এখানে নেই।</p>
      </div>

      <div className="flex flex-wrap justify-center gap-3">
        <Link
          href="/"
          className="group flex min-h-12 items-center gap-2 rounded-lg bg-leaf px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
        >
          মূল পাতায় ফিরুন <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
        </Link>
        <Link
          href="/detect"
          className="flex min-h-12 items-center gap-2 rounded-lg border rule px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-leaf hover:text-leaf"
        >
          <Camera className="h-4 w-4" /> রোগ নির্ণয়
        </Link>
      </div>
    </div>
  );
}
