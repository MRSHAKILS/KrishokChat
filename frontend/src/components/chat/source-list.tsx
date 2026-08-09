"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, FileText } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import type { SourceNode } from "@/lib/api";

/* =========================================================================
   SourceList — expandable citations showing which knowledge nodes backed
   the answer. Transparency for the farmer and the demo/paper.
   ========================================================================= */

export function SourceList({ sources }: { sources: SourceNode[] }) {
  const [open, setOpen] = useState(false);

  if (!sources.length) return null;

  return (
    <div className="mt-3">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-1.5 text-[11px] uppercase tracking-[0.16em] text-ink-faint transition-colors hover:text-leaf"
      >
        <FileText className="h-3 w-3" />
        উৎস ({sources.length})
        <ChevronDown className={cn("h-3 w-3 transition-transform", open && "rotate-180")} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.ul
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="mt-2 space-y-1.5 overflow-hidden"
          >
            {sources.map((src, i) => (
              <li
                key={i}
                className="rounded-md border rule bg-paper-2/40 px-3 py-2"
              >
                <div className="flex items-center gap-2">
                  <span className="shrink-0 font-mono text-[10px] text-ink-faint">[{i + 1}]</span>
                  <span className="truncate font-mono text-[11px] text-ink-soft">{src.id}</span>
                  {src.expert_verified && (
                    <span className="shrink-0 text-[10px] text-leaf">যাচাইকৃত</span>
                  )}
                </div>
                {src.question && (
                  <p className="mt-1 ml-5 text-xs font-medium text-ink line-clamp-2">
                    {src.question}
                  </p>
                )}
                {src.answer && (
                  <p className="mt-1 ml-5 text-xs leading-relaxed text-ink-soft line-clamp-2">
                    {src.answer}
                  </p>
                )}
                {src.treatment && (
                  <p className="mt-1 ml-5 text-[11px] leading-relaxed text-ink-soft line-clamp-2">
                    প্রতিকার: {src.treatment}
                  </p>
                )}
                {src.source && (
                  <p className="mt-0.5 ml-5 text-[10px] text-ink-faint truncate">
                    {src.source}
                  </p>
                )}
              </li>
            ))}
          </motion.ul>
        )}
      </AnimatePresence>
    </div>
  );
}
