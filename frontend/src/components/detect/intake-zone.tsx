"use client";

import { useRef, useState, useCallback } from "react";
import { motion, AnimatePresence } from "motion/react";
import { RefreshCw, AlertCircle, Upload } from "lucide-react";
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
  onClear,
  qualityWarnings,
  loading,
}: {
  file: File | null;
  preview: string | null;
  onFile: (f: File) => void;
  onClear: () => void;
  qualityWarnings: string[];
  loading: boolean;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleSelect = useCallback(
    (f: File) => {
      if (!f.type.startsWith("image/")) return;
      onFile(f);
    },
    [onFile],
  );

  return (
    <div className="space-y-3">
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
        className={cn(
          "relative cursor-pointer rounded-xl border-2 p-8 text-center transition-colors",
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
                className="mx-auto max-h-52 rounded-lg border border-bone object-contain"
              />
              <div className="mt-3 flex items-center justify-center gap-3 text-xs text-ink-faint">
                <span className="max-w-[160px] truncate">{file?.name ?? "ছবি"}</span>
                {!loading && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onClear();
                    }}
                    className="flex items-center gap-1 text-ink-soft transition-colors hover:text-leaf"
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
              <div className="mt-1 text-[11px] text-ink-faint/70">
                JPEG · PNG · WebP · সর্বোচ্চ {VISION.maxFileSizeMB}MB
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

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
    </div>
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
