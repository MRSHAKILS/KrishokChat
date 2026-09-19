"use client";

import { useRef, useState, useCallback } from "react";
import { motion, AnimatePresence } from "motion/react";
import { RefreshCw, AlertCircle, Upload, ImageIcon, Loader2, Sprout } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { VISION } from "@/lib/constants";

/* =========================================================================
   IntakeZone — the upload / preview / quality-warning area.
   Designed as a field-notebook specimen card, not a generic dropzone.
   ========================================================================= */

export function IntakeZone({
  file,
  preview,
  onFile,
  onValidationError,
  onClear,
  onSample,
  sampleLoading,
  qualityWarnings,
  loading,
  cropHint,
  onCropHintChange,
}: {
  file: File | null;
  preview: string | null;
  onFile: (f: File) => void;
  onValidationError?: (message: string) => void;
  onClear: () => void;
  onSample?: (path: string, name: string) => void;
  sampleLoading?: boolean;
  qualityWarnings: string[];
  loading: boolean;
  cropHint: string;
  onCropHintChange: (value: string) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleSelect = useCallback(
    (f: File) => {
      if (!VISION.acceptedTypes.includes(f.type)) {
        onValidationError?.("শুধু JPEG, PNG বা WebP ছবি দিন।");
        return;
      }
      if (f.size > VISION.maxFileSizeMB * 1024 * 1024) {
        onValidationError?.(`ছবিটি ${VISION.maxFileSizeMB}MB-এর ছোট হতে হবে।`);
        return;
      }
      onFile(f);
    },
    [onFile, onValidationError],
  );

  return (
    <div className="space-y-3">
      {/* Crop selector — the 6-class crop model cannot recognize every crop
          (it has no Rice class), so farmers can declare what they grow. The
          backend then routes directly to the matching disease model. */}
      <div className="flex flex-wrap items-center gap-2 rounded-lg border rule bg-paper-2/40 px-3 py-2.5">
        <label
          htmlFor="crop-hint"
          className="flex items-center gap-1.5 text-xs font-semibold text-ink-soft"
        >
          <Sprout className="h-3.5 w-3.5 text-leaf" />
          ফসল
        </label>
        <select
          id="crop-hint"
          value={cropHint}
          onChange={(e) => onCropHintChange(e.target.value)}
          className="min-h-9 flex-1 rounded-lg border rule bg-paper px-2.5 py-1.5 text-xs text-ink focus:border-leaf focus:outline-none sm:flex-none"
          aria-label="ফসল নির্বাচন করুন"
        >
          <option value="">অটো — মডেল শনাক্ত করবে</option>
          <option value="rice">ধান</option>
          <option value="wheat">গম</option>
          <option value="corn">ভুট্টা</option>
          <option value="potato">আলু</option>
          <option value="brassica">বাঁধাকপি / ফুলকপি</option>
          <option value="chilli">মরিচ</option>
        </select>
        {cropHint && (
          <span className="w-full text-xs text-leaf sm:w-auto">
            এই ফসলের রোগ মডেল দিয়ে বিশ্লেষণ হবে
          </span>
        )}
      </div>

      {/* Drop / preview area */}
      <motion.div
        onClick={() => !loading && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          const f = e.dataTransfer.files[0];
          if (f) handleSelect(f);
        }}
        whileHover={file ? undefined : { scale: 1.005 }}
        transition={{ duration: dur.fast, ease: ease.smooth }}
        role="button"
        tabIndex={loading ? -1 : 0}
        onKeyDown={(e) => {
          if (!loading && (e.key === "Enter" || e.key === " ")) inputRef.current?.click();
        }}
        aria-label={preview ? "আপলোড করা ছবি পরিবর্তন করুন" : "পাতার ছবি আপলোড করুন"}
        className={cn(
          "surface-lift relative cursor-pointer overflow-hidden rounded-xl border-2 p-8 text-center transition-colors focus-visible:ring-2 focus-visible:ring-leaf",
          dragging
            ? "border-leaf bg-leaf/5"
            : file
              ? "border-bone bg-paper-2/30"
              : "border-dashed border-bone bg-paper-2/30 hover:border-leaf hover:bg-paper-2/50",
        )}
      >
        <input
          ref={inputRef}
          type="file"
          accept={VISION.acceptedTypes.join(",")}
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleSelect(f);
            e.target.value = ""; // allow re-selecting the same file
          }}
        />

        <AnimatePresence mode="wait">
          {preview ? (
            /* --- Preview state: framed specimen --- */
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.96 }}
              transition={{ duration: dur.normal, ease: ease.smooth }}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={preview}
                alt="আপলোড করা পাতার ছবি"
                className="mx-auto max-h-52 rounded-lg border border-bone object-contain shadow-sm"
              />
              <div className="mt-3 flex items-center justify-center gap-3 text-xs text-ink-faint">
                <span className="max-w-[160px] truncate">{file?.name ?? "ছবি"}</span>
                {!loading && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onClear();
                    }}
                    className="flex min-h-11 items-center gap-1 rounded-lg px-2 text-ink-soft transition-colors hover:text-leaf"
                  >
                    <RefreshCw className="h-3 w-3" />
                    পরিবর্তন
                  </button>
                )}
              </div>
            </motion.div>
          ) : (
            /* --- Empty state: botanical invitation --- */
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: dur.fast }}
            >
              <LeafLine />
              <div className="mt-4 font-display text-lg text-ink">পাতার ছবি দিন</div>
              <div className="mt-1 flex items-center justify-center gap-1.5 text-xs text-ink-faint">
                <Upload className="h-3 w-3" />
                টানে দিন বা ক্লিক করুন
              </div>
              <div className="mt-1 text-xs text-ink-faint/70">
                JPEG · PNG · WebP · সর্বোচ্চ {VISION.maxFileSizeMB}MB
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence mode="wait">
          {dragging && !loading && (
            <motion.div
              key="drop-ready"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="pointer-events-none absolute inset-2 flex items-center justify-center rounded-lg border border-leaf/30 bg-paper/90 text-sm font-semibold text-leaf"
            >
              ছবি ছেড়ে দিন
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Only verified assets are offered here. More crop-specific samples
          can be added when real checked-in images become available. */}
      {!preview && onSample && (
        <div className="rounded-lg border border-leaf/20 bg-leaf/5 p-3">
          <div className="flex items-center justify-between gap-3">
            <div>
              <div className="text-sm font-medium text-ink">নমুনা ছবি দিয়ে চেষ্টা করুন</div>
              <p className="mt-0.5 text-xs text-ink-soft">চেক-ইন করা ধানের পাতার ছবি</p>
            </div>
            <ImageIcon className="h-5 w-5 shrink-0 text-leaf" />
          </div>
          <button
            type="button"
            onClick={() => onSample("/assets/close_rice.jpg", "rice-leaf-sample.jpg")}
            disabled={sampleLoading || loading}
            className="mt-3 flex min-h-11 w-full items-center justify-center gap-2 rounded-lg border border-leaf/30 bg-paper px-3 py-2 text-sm font-medium text-leaf transition-colors hover:bg-leaf/10 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {sampleLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
            {sampleLoading ? "নমুনা প্রস্তুত হচ্ছে…" : "ধানের পাতার নমুনা নিন"}
          </button>
        </div>
      )}

      {/* Quality warnings — gentle, actionable, not aggressive */}
      <AnimatePresence>
        {qualityWarnings.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
            className="space-y-1.5"
          >
            {qualityWarnings.map((w, i) => (
              <div
                key={i}
                className="flex items-start gap-2 rounded-lg border border-ochre-soft/50 bg-ochre-soft/15 px-3 py-2 text-xs text-ink-soft"
              >
                <AlertCircle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-ochre" />
                <span>{w}</span>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Field Photography & Viewfinder Framing Guide */}
      <LeafFramingGuide />

      {/* Scope note — polite, non-blocking */}
      <p className="flex items-center justify-center gap-1.5 pt-1 text-center text-[11px] leading-relaxed text-ink-faint/60">
        <Sprout className="h-3 w-3 shrink-0 opacity-50" />
        <span>Optimized for 6 crops — ধান · আলু · বাঁধাকপি · ভুট্টা · গম · মরিচ — other crops coming soon</span>
      </p>
    </div>
  );
}

function LeafFramingGuide() {
  const [open, setOpen] = useState(false);

  return (
    <div className="rounded-lg border rule bg-paper-2/25 p-2.5 text-xs text-ink-soft">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between font-medium text-ink transition-colors hover:text-leaf cursor-pointer"
      >
        <span className="flex items-center gap-1.5">
          <span className="flex h-4 w-4 items-center justify-center rounded-full bg-leaf/12 text-xs font-bold text-leaf">
            ℹ
          </span>
          সঠিক ছবি তোলার সহায়িকা (ভিউফাইন্ডার গাইড)
        </span>
        <span className="text-xs text-leaf">{open ? "সংক্ষিপ্ত করুন ▲" : "দেখুন ▼"}</span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-2.5 space-y-2 border-t rule pt-2.5"
          >
            <div className="flex items-center justify-center rounded-lg border border-dashed border-leaf/30 bg-leaf/5 py-4">
              <div className="relative flex h-24 w-36 items-center justify-center rounded-lg border-2 border-leaf/40 bg-paper/80 shadow-2xs">
                {/* Reticle corner marks */}
                <div className="absolute top-1 left-1 h-2.5 w-2.5 border-t-2 border-l-2 border-leaf" />
                <div className="absolute top-1 right-1 h-2.5 w-2.5 border-t-2 border-r-2 border-leaf" />
                <div className="absolute bottom-1 left-1 h-2.5 w-2.5 border-b-2 border-l-2 border-leaf" />
                <div className="absolute bottom-1 right-1 h-2.5 w-2.5 border-b-2 border-r-2 border-leaf" />
                <div className="text-center">
                  <LeafLineSmall />
                  <span className="block text-xs font-semibold text-leaf mt-0.5">আক্রান্ত অংশ কেন্দ্রে রাখুন</span>
                </div>
              </div>
            </div>

            <ul className="space-y-1.5 text-xs text-ink-soft">
              <li className="flex items-start gap-1.5">
                <span className="text-leaf font-bold">✓</span>
                <span><strong>দিনের আলো:</strong> ছায়া বা অতিরিক্ত ফ্ল্যাশ এড়িয়ে সরাসরি স্বাভাবিক আলোতে ছবি তুলুন।</span>
              </li>
              <li className="flex items-start gap-1.5">
                <span className="text-leaf font-bold">✓</span>
                <span><strong>দূরত্ব:</strong> পাতা থেকে ১৫–২০ সেন্টিমিটার দূরত্বে ক্যামেরা স্থির রেখে তুলুন।</span>
              </li>
              <li className="flex items-start gap-1.5">
                <span className="text-leaf font-bold">✓</span>
                <span><strong>একক পাতা:</strong> পুরো গাছের বদলে আক্রান্ত একটি পাতার ক্ষত পরিষ্কারভাবে ফ্রেমে রাখুন।</span>
              </li>
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function LeafLineSmall() {
  return (
    <svg width="24" height="24" viewBox="0 0 48 48" fill="none" aria-hidden className="mx-auto">
      <path
        d="M8 38C8 22 18 10 40 8C38 28 26 38 8 38Z"
        stroke="var(--color-leaf)"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M12 34C20 28 28 20 36 12"
        stroke="var(--color-leaf)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

/* A simple botanical line-drawing — not an emoji, not a stock icon. */
function LeafLine() {
  return (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden className="mx-auto">
      <path
        d="M8 38C8 22 18 10 40 8C38 28 26 38 8 38Z"
        stroke="var(--color-leaf)"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        opacity="0.7"
      />
      <path
        d="M12 34C20 28 28 20 36 12"
        stroke="var(--color-leaf)"
        strokeWidth="1"
        strokeLinecap="round"
        opacity="0.4"
      />
      <path
        d="M18 30C22 28 26 24 30 20"
        stroke="var(--color-leaf)"
        strokeWidth="0.8"
        strokeLinecap="round"
        opacity="0.3"
      />
    </svg>
  );
}
