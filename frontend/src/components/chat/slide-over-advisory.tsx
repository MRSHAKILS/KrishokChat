"use client";

import { useEffect, useCallback } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import { MessageCircle, X, ArrowUpRight, Leaf, Sparkles } from "lucide-react";
import { QAPanel } from "@/components/qa-panel";
import { ContextBanner } from "@/components/detect/context-banner";
import { humanizeLabel } from "@/lib/bn";
import { cn } from "@/lib/utils";

/* =========================================================================
   SlideOverAdvisory — Floating Trigger Pill & Slide-Over Assistant Drawer.

   Replaces the congested 2-column layout on /detect with an on-demand,
   full-height slide-over drawer panel, providing maximum visual focus
   for disease diagnosis while keeping AI consultation 1 click away.
   ========================================================================= */

export function SlideOverAdvisory({
  open,
  onToggle,
  detectedCrop,
  detectedDisease,
  prefillQuestion,
  title = "এআই কৃষি পরামর্শদাতা",
  subtitle = "তথ্যভিত্তিক বাংলা কৃষি প্রশ্নোত্তর ও চিকিৎসা",
  triggerEyebrow = "কৃষি বিশেষজ্ঞ",
  triggerLabel = "এআই সহকারী · প্রশ্ন করুন",
}: {
  open: boolean;
  onToggle: (v: boolean) => void;
  detectedCrop?: string | null;
  detectedDisease?: string | null;
  prefillQuestion?: string | null;
  title?: string;
  subtitle?: string;
  triggerEyebrow?: string;
  triggerLabel?: string;
}) {
  const hasContext = Boolean(detectedCrop && detectedDisease);

  // Close on Escape key
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape" && open) {
        onToggle(false);
      }
    },
    [open, onToggle],
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  // Lock body scroll on small mobile screens when drawer is open
  useEffect(() => {
    if (open && window.innerWidth < 640) {
      document.body.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = "";
      };
    }
  }, [open]);

  return (
    <>
      {/* 1. Floating Action Pill Trigger (Bottom-Right) */}
      <AnimatePresence>
        {!open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="fixed bottom-5 right-5 z-40 sm:bottom-6 sm:right-6"
          >
            <button
              onClick={() => onToggle(true)}
              type="button"
              aria-label="এআই কৃষি সহকারী ওপেন করুন"
              className={cn(
                "group relative flex items-center gap-2.5 rounded-full px-4 py-3 text-sm font-semibold shadow-xl transition-all cursor-pointer",
                "bg-leaf text-paper hover:bg-leaf-2 hover:shadow-2xl hover:scale-102",
                "border border-leaf-2/30",
              )}
            >
              {/* Pulsing indicator when context is detected */}
              <span className="relative flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-paper/20">
                <MessageCircle className="h-4 w-4 text-paper" />
                {hasContext && (
                  <span className="absolute -top-0.5 -right-0.5 flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-ochre opacity-75" />
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-ochre" />
                  </span>
                )}
              </span>

              <span className="flex flex-col text-left">
                <span className="text-[11px] font-medium text-paper/80 leading-none">
                  {hasContext ? "আক্রান্ত ফসল নিয়ে" : triggerEyebrow}
                </span>
                <span className="text-sm font-bold leading-tight mt-0.5">
                  {hasContext
                    ? `${humanizeLabel(detectedDisease!)} নিয়ে প্রশ্ন করুন`
                    : triggerLabel}
                </span>
              </span>

              <span className="ml-1 rounded-full bg-paper/15 px-2 py-0.5 text-[11px] font-mono text-paper/90 group-hover:bg-paper/25">
                বার্তা ↵
              </span>
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 2. Slide-Over Drawer & Backdrop Overlay */}
      <AnimatePresence>
        {open && (
          <div className="fixed inset-0 z-50 overflow-hidden">
            {/* Backdrop Blur Overlay */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25 }}
              onClick={() => onToggle(false)}
              className="fixed inset-0 bg-ink/35 backdrop-blur-xs transition-opacity"
              aria-hidden="true"
            />

            {/* Slide-Over Drawer Panel */}
            <div className="fixed inset-y-0 right-0 flex max-w-full pl-0 sm:pl-10">
              <motion.div
                initial={{ x: "100%" }}
                animate={{ x: 0 }}
                exit={{ x: "100%" }}
                transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                className="flex h-full w-screen max-w-full sm:max-w-xl flex-col bg-paper shadow-2xl border-l rule"
                role="dialog"
                aria-modal="true"
                aria-label="এআই কৃষি পরামর্শদাতা প্যানেল"
              >
                {/* Drawer Header */}
                <div className="flex shrink-0 items-center justify-between border-b rule px-5 py-4 bg-paper-2/40">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-leaf/10 text-leaf">
                      <MessageCircle className="h-5 w-5" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h2 className="font-display text-base text-ink">{title}</h2>
                        <span className="rounded-full bg-leaf/10 px-2 py-0.5 text-[10px] font-semibold text-leaf">
                          সক্রিয়
                        </span>
                      </div>
                      <p className="text-xs text-ink-soft">{subtitle}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Link
                      href="/chat"
                      title="পূর্ণ চ্যাট স্ক্রিনে যান"
                      className="hidden sm:inline-flex items-center gap-1 rounded-lg border border-bone bg-paper px-2.5 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
                    >
                      <span>পূর্ণ স্ক্রিন</span>
                      <ArrowUpRight className="h-3.5 w-3.5" />
                    </Link>

                    <button
                      onClick={() => onToggle(false)}
                      type="button"
                      aria-label="প্যানেল বন্ধ করুন"
                      className="flex h-9 w-9 items-center justify-center rounded-lg border border-bone bg-paper text-ink-soft transition-colors hover:border-clay hover:text-clay cursor-pointer"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {/* Context Pill Banner (if crop/disease detected) */}
                {hasContext && (
                  <div className="shrink-0 border-b rule bg-leaf/5 px-5 py-2.5">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1.5 text-xs font-medium text-leaf">
                        <Leaf className="h-3.5 w-3.5" />
                        <span>
                          <strong>প্রসঙ্গ:</strong> {detectedCrop} — {humanizeLabel(detectedDisease!)}
                        </span>
                      </div>
                      <span className="text-[11px] text-ink-faint">শনাক্তকৃত ফসল ভিত্তিক উত্তর</span>
                    </div>
                  </div>
                )}

                {/* Drawer Body — Full QAPanel */}
                <div className="flex-1 min-h-0 overflow-hidden px-5 py-3">
                  <QAPanel
                    detectedCrop={detectedCrop}
                    detectedDisease={detectedDisease}
                    prefillQuestion={prefillQuestion}
                    compact={false}
                  />
                </div>
              </motion.div>
            </div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
