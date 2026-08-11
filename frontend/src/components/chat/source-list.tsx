"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, Building2, BookOpen, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import type { SourceNode } from "@/lib/api";

/* =========================================================================
   SourceList — formal institutional citations linking back to root
   research organizations (DAE, BARC, BARI, BRRI, SRDI, CABI, IRRI).
   ========================================================================= */

export function SourceList({ sources }: { sources: SourceNode[] }) {
  const [open, setOpen] = useState(false);

  if (!sources.length) return null;

  return (
    <div className="mt-3 border-t rule pt-2">
      <button
        onClick={() => setOpen((v) => !v)}
        className="control-press flex min-h-9 items-center gap-1.5 rounded-lg px-1.5 text-[11px] font-semibold text-ink-faint transition-colors hover:text-leaf"
      >
        <Building2 className="h-3.5 w-3.5 text-leaf" />
        তথ্যসূত্র দেখুন ({sources.length}টি)
        <ChevronDown className={cn("h-3 w-3 transition-transform", open && "rotate-180")} />
      </button>

      <AnimatePresence mode="wait">
        {open && (
          <motion.ul
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="mt-2 space-y-2 overflow-hidden"
          >
            {sources.map((src, i) => {
              const pubName = src.publisher_bn || src.publisher || "জাতীয় কৃষি গবেষণা সংস্থা";
              const docTitle = src.source || src.title_bn || src.title_en || src.question || "কৃষি তথ্য ও প্রযুক্তি গাইড";

              return (
                <li
                  key={i}
                  id={`source-${i + 1}`}
                  className="surface-lift rounded-lg border rule bg-paper p-3 text-xs shadow-2xs"
                >
                  {/* Organization Header */}
                  <div className="flex flex-wrap items-center justify-between gap-1.5 border-b rule pb-2">
                    <div className="flex items-center gap-1.5">
                      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-leaf text-[10px] font-bold text-paper tabular">
                        {i + 1}
                      </span>
                      <span className="font-semibold text-leaf flex items-center gap-1">
                        <Building2 className="h-3 w-3 text-leaf/80" />
                        {pubName}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-[10px]">
                      {src.expert_verified && (
                        <span className="flex items-center gap-0.5 text-leaf font-medium">
                          <CheckCircle2 className="h-3 w-3" /> যাচাইকৃত
                        </span>
                      )}
                      <span className="font-mono text-ink-faint tabular">
                        প্রাসঙ্গিকতা: {(src.score * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>

                  {/* Document & Section Title */}
                  <div className="mt-2 flex items-start gap-1.5 font-medium text-ink">
                    <BookOpen className="h-3.5 w-3.5 shrink-0 mt-0.5 text-ink-faint" />
                    <span>{docTitle}</span>
                  </div>

                  {/* Citation / Section Note */}
                  {src.citation && (
                    <p className="mt-1 ml-5 text-[11px] italic text-ink-soft bg-paper-2/60 p-2 rounded rule">
                      &ldquo;{src.citation.trim()}&rdquo;
                    </p>
                  )}

                  {/* Grounded Excerpt */}
                  {src.answer && (
                    <p className="mt-1.5 ml-5 text-[11px] leading-relaxed text-ink-soft line-clamp-2">
                      {src.answer}
                    </p>
                  )}
                </li>
              );
            })}
          </motion.ul>
        )}
      </AnimatePresence>
    </div>
  );
}
