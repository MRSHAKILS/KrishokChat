"use client";

import { useRef, useState, useCallback } from "react";
import { motion, AnimatePresence } from "motion/react";
import { RefreshCw, AlertCircle, Upload, Sprout } from "lucide-react";
import { cn } from "@/lib/utils";
import { dur, ease } from "@/lib/motion";
import { VISION } from "@/lib/constants";
import { TestSamplesSelector } from "./test-samples-selector";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   IntakeZone — the upload / preview / quality-warning area.
   Designed as a field-notebook specimen card with full i18n support.
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
  onSample?: (path: string, name: string, cropHint?: string) => void;
  sampleLoading?: boolean;
  qualityWarnings: string[];
  loading: boolean;
  cropHint: string;
  onCropHintChange: (value: string) => void;
}) {
  const { t, locale } = useLanguage();
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleSelect = useCallback(
    (f: File) => {
      if (!VISION.acceptedTypes.includes(f.type)) {
        onValidationError?.(t.detect.invalidType);
        return;
      }
      if (f.size > VISION.maxFileSizeMB * 1024 * 1024) {
        onValidationError?.(t.detect.sizeExceeded);
        return;
      }
      onFile(f);
    },
    [onFile, onValidationError, t]
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
          {t.detect.cropLabel}
        </label>
        <select
          id="crop-hint"
          value={cropHint}
          onChange={(e) => onCropHintChange(e.target.value)}
          className="min-h-9 flex-1 rounded-lg border rule bg-paper px-2.5 py-1.5 text-xs text-ink focus:border-leaf focus:outline-hidden sm:flex-none cursor-pointer"
          aria-label={t.detect.cropLabel}
        >
          <option value="">{t.detect.cropAuto}</option>
          <option value="rice">{t.detect.cropRice}</option>
          <option value="wheat">{t.detect.cropWheat}</option>
          <option value="corn">{t.detect.cropCorn}</option>
          <option value="potato">{t.detect.cropPotato}</option>
          <option value="brassica">{t.detect.cropBrassica}</option>
          <option value="chilli">{t.detect.cropChilli}</option>
        </select>
        {cropHint && (
          <span className="w-full text-xs text-leaf sm:w-auto">
            {t.detect.cropHintHelp}
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
        aria-label={preview ? t.detect.changePhoto : t.detect.dropTitle}
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
                alt={preview ? t.detect.dropTitle : "Leaf Preview"}
                className="mx-auto max-h-52 rounded-lg border border-bone object-contain shadow-sm"
              />
              <div className="mt-3 flex items-center justify-center gap-3 text-xs text-ink-faint">
                <span className="max-w-[160px] truncate">{file?.name ?? "Photo"}</span>
                {!loading && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onClear();
                    }}
                    className="flex min-h-11 items-center gap-1 rounded-lg px-2 text-ink-soft transition-colors hover:text-leaf cursor-pointer"
                  >
                    <RefreshCw className="h-3 w-3" />
                    {t.detect.changePhoto}
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
              <div className="mt-4 font-display text-lg text-ink">{t.detect.dropTitle}</div>
              <div className="mt-1 flex items-center justify-center gap-1.5 text-xs text-ink-faint">
                <Upload className="h-3 w-3" />
                {t.detect.dropPrompt}
              </div>
              <div className="mt-1 text-xs text-ink-faint/70">
                {t.detect.dropSpecs}
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
              {t.detect.dropReady}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Verified test sets for reviewers and farmers: compact dropdown and loader */}
      {onSample && (
        <TestSamplesSelector
          onSelectSample={onSample}
          loading={loading}
          sampleLoading={sampleLoading}
          compact={Boolean(preview)}
        />
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
        <span>{t.detect.cropsCoverage}</span>
      </p>
    </div>
  );
}

function LeafFramingGuide() {
  const { t } = useLanguage();
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
          {t.detect.viewfinderTitle}
        </span>
        <span className="text-xs text-leaf">{open ? t.detect.viewfinderOpen : t.detect.viewfinderClose}</span>
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
                  <span className="block text-xs font-semibold text-leaf mt-0.5">{t.detect.viewfinderCenter}</span>
                </div>
              </div>
            </div>

            <ul className="space-y-1.5 text-xs text-ink-soft">
              <li className="flex items-start gap-1.5">
                <span className="text-leaf font-bold">✓</span>
                <span>{t.detect.viewfinderDaylight}</span>
              </li>
              <li className="flex items-start gap-1.5">
                <span className="text-leaf font-bold">✓</span>
                <span>{t.detect.viewfinderDistance}</span>
              </li>
              <li className="flex items-start gap-1.5">
                <span className="text-leaf font-bold">✓</span>
                <span>{t.detect.viewfinderSingleLeaf}</span>
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
