"use client";

/* =========================================================================
   InlineAdvisory — collapsible advisory card for /detect and /soil.

   Replaces the old always-visible right chat column. The two-column layout
   is preserved (detection left, advisory right) — but the right column is
   now collapsible:
     • Collapsed (default): a slim header bar with icon, title, optional
       context pill, pulsing "open" hint, and a chevron.
     • Expanded (on click): the header + full QAPanel + context banner +
       /chat deep link, with a smooth height-auto slide animation.

   The chat conversation is unchanged — QAPanel persists to the same
   localStorage key, so this and /chat are two doors into one conversation.
   MotionConfig reducedMotion="user" collapses the animation under OS
   reduced-motion.
   ========================================================================= */

import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import { MessageCircle, ChevronDown, ArrowRight, Leaf } from "lucide-react";
import { QAPanel } from "@/components/qa-panel";
import { ContextBanner } from "@/components/detect/context-banner";
import { humanizeLabel } from "@/lib/bn";
import { dur, ease } from "@/lib/motion";
import { cn } from "@/lib/utils";

export function InlineAdvisory({
  open,
  onToggle,
  detectedCrop,
  detectedDisease,
  prefillQuestion,
  eyebrow = "CONTEXTUAL ADVISORY",
  heading = "কৃষি পরামর্শ",
  subheading,
  showContext = true,
  sticky = true,
  ctaHint = "প্রশ্ন করুন",
}: {
  open: boolean;
  onToggle: (v: boolean) => void;
  detectedCrop?: string | null;
  detectedDisease?: string | null;
  prefillQuestion?: string | null;
  eyebrow?: string;
  heading?: string;
  subheading?: string;
  showContext?: boolean;
  sticky?: boolean;
  ctaHint?: string;
}) {
  const hasContext = Boolean(detectedCrop && detectedDisease);

  return (
    <div
      className={cn(
        "overflow-hidden rounded-2xl border rule bg-paper shadow-[0_10px_28px_rgba(52,39,23,0.05)] flex flex-col",
        sticky && "lg:sticky lg:top-20 lg:max-h-[calc(100vh-6rem)]",
      )}
    >
      {/* Header — always visible, clickable toggle */}
      <button
        type="button"
        onClick={() => onToggle(!open)}
        aria-expanded={open}
        aria-controls="inline-advisory-body"
        className={cn(
          "control-press shrink-0 flex w-full items-center justify-between gap-3 px-5 py-4 text-left transition-colors",
          open ? "bg-leaf/[0.03]" : "hover:bg-paper-2/40",
        )}
      >
        <span className="flex min-w-0 items-center gap-3">
          <span className="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
            <MessageCircle className="h-4 w-4" />
            {!open && (
              <span className="absolute -right-0.5 -top-0.5 flex h-2.5 w-2.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-ochre opacity-60" />
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-ochre" />
              </span>
            )}
          </span>
          <span className="min-w-0">
            <span className="block text-[10px] font-semibold uppercase tracking-[0.16em] text-ochre">
              {eyebrow}
            </span>
            <span className="mt-0.5 block font-display text-base text-ink">{heading}</span>
          </span>
        </span>

        <span className="flex shrink-0 items-center gap-2">
          {/* Context pill — shown when collapsed + context exists */}
          {!open && hasContext && detectedCrop && detectedDisease && (
            <span className="hidden items-center gap-1.5 rounded-full border border-leaf/20 bg-leaf/5 px-2.5 py-1 text-[10px] font-medium text-leaf sm:inline-flex">
              <Leaf className="h-3 w-3" strokeWidth={1.5} />
              <span className="max-w-[120px] truncate">
                {detectedCrop} — {humanizeLabel(detectedDisease)}
              </span>
            </span>
          )}
          {/* CTA hint — shown when collapsed, no context */}
          {!open && !hasContext && (
            <span className="hidden text-[11px] font-medium text-ink-faint sm:inline">{ctaHint}</span>
          )}
          <motion.span
            animate={{ rotate: open ? 180 : 0 }}
            transition={{ duration: dur.fast, ease: ease.smooth }}
            className="text-ink-faint"
            aria-hidden
          >
            <ChevronDown className="h-5 w-5" />
          </motion.span>
        </span>
      </button>

      {/* Body — collapsible */}
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            id="inline-advisory-body"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="flex-1 min-h-0 overflow-hidden flex flex-col"
          >
            <div
              className="flex flex-col flex-1 min-h-0 border-t rule overflow-hidden"
              style={{ height: "clamp(24rem, calc(100vh - 13rem), 42rem)" }}
            >
              {/* Context banner + subheading */}
              {(showContext || subheading) && (
                <div className="shrink-0 space-y-2 px-5 pt-3">
                  {showContext && (
                    <ContextBanner crop={detectedCrop ?? null} disease={detectedDisease ?? null} />
                  )}
                  {subheading && <p className="text-sm text-ink-soft">{subheading}</p>}
                </div>
              )}

              {/* Chat */}
              <div className="flex-1 min-h-0 overflow-hidden px-5 pb-3 pt-1">
                <QAPanel
                  compact={true}
                  detectedCrop={detectedCrop}
                  detectedDisease={detectedDisease}
                  prefillQuestion={prefillQuestion}
                />
              </div>

              {/* Deep link to the dedicated chat home */}
              <div className="shrink-0 border-t rule px-5 py-2.5 bg-paper">
                <Link
                  href="/chat"
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-leaf transition-colors hover:text-leaf-2"
                >
                  পূর্ণ চ্যাট পৃষ্ঠায় যান <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
