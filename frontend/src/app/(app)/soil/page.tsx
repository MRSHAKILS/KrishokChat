"use client";

import { useState, useCallback, useMemo, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Search, Loader2, RotateCcw, X } from "lucide-react";
import { getSoilDataset, analyzeSoil, type SoilDatasetInfo, type SoilAnalyzeResponse } from "@/lib/api";
import { SOIL_STAGES, type RailEvent } from "@/components/detect/pipeline-rail";
import { AgentTrace } from "@/components/agent-trace";
import { SlideOverAdvisory } from "@/components/chat/slide-over-advisory";
import { SoilDatasetCard } from "@/components/soil/soil-dataset-card";
import { SoilLockedCard } from "@/components/soil/soil-locked-card";
import { stagger, enter, dur, ease } from "@/lib/motion";
import { prepareUploadImage } from "@/lib/image";

/* =========================================================================
   SoilPage — the soil moisture field console.
   Left: photo intake → pipeline rail → locked-model card → dataset showcase.
   Right: chat panel (always visible) for soil & irrigation questions.
   The analyzer is intentionally locked (models in development, negative R²);
   the page explains this honestly with real numbers.
   ========================================================================= */

const SOIL_SAMPLES = [
  { path: "/assets/soil_samples/P0001_Doash_8.0kpa.jpg", name: "দোআঁশ · ৮ kPa" },
  { path: "/assets/soil_samples/P0064_Bele_0.0kpa.jpg", name: "বেলে · ০ kPa" },
  { path: "/assets/soil_samples/P0406_Atel_16.5kpa.jpg", name: "এঁটেল · ১৬.৫ kPa" },
];

export default function SoilPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [preparing, setPreparing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [online, setOnline] = useState(true);
  const [advisoryOpen, setAdvisoryOpen] = useState(false);
  const [dataset, setDataset] = useState<SoilDatasetInfo | null>(null);
  const [datasetError, setDatasetError] = useState(false);
  const [result, setResult] = useState<SoilAnalyzeResponse | null>(null);
  const requestRef = useRef<AbortController | null>(null);

  /* Load the frozen dataset info once — never computed live. */
  useEffect(() => {
    getSoilDataset()
      .then(setDataset)
      .catch(() => setDatasetError(true));
  }, []);

  useEffect(() => {
    const update = () => setOnline(navigator.onLine);
    window.queueMicrotask(update);
    window.addEventListener("online", update);
    window.addEventListener("offline", update);
    return () => {
      requestRef.current?.abort();
      window.removeEventListener("online", update);
      window.removeEventListener("offline", update);
    };
  }, []);

  useEffect(() => () => {
    if (preview) URL.revokeObjectURL(preview);
  }, [preview]);

  const handleFile = useCallback(async (f: File) => {
    setPreparing(true);
    setError(null);
    try {
      const prepared = await prepareUploadImage(f);
      setFile(prepared);
      setPreview(URL.createObjectURL(prepared));
      setResult(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "ছবিটি প্রস্তুত করা যায়নি।");
    } finally {
      setPreparing(false);
    }
  }, []);

  const handleClear = useCallback(() => {
    requestRef.current?.abort();
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  }, []);

  const handleSample = useCallback(
    async (samplePath: string, sampleName: string) => {
      setPreparing(true);
      setError(null);
      try {
        const response = await fetch(samplePath);
        if (!response.ok) throw new Error("sample image unavailable");
        const blob = await response.blob();
        // Keep the released dataset filename (e.g. P0001_Doash_8.0kpa.jpg) —
        // the backend replays the measured record by image ID in the name.
        const datasetName = samplePath.split("/").pop() ?? sampleName;
        setFile(new File([blob], datasetName, { type: blob.type || "image/jpeg" }));
        setPreview(samplePath);
        setResult(null);
      } catch {
        setError("নমুনা ছবিটি এখন পাওয়া যাচ্ছে না। নিজের ছবি আপলোড করুন।");
      } finally {
        setPreparing(false);
      }
    },
    [],
  );

  const runAnalyze = useCallback(async () => {
    if (!file || loading || !online) return;
    const controller = new AbortController();
    requestRef.current?.abort();
    requestRef.current = controller;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const r = await analyzeSoil(file, { signal: controller.signal });
      setResult(r);
      if (!r.dataset) setDatasetError(true);
      else setDataset(r.dataset);
    } catch (e: unknown) {
      if (!controller.signal.aborted) {
        const msg = e instanceof Error ? e.message : "বিশ্লেষণে সমস্যা হয়েছে";
        if (msg.includes("Failed to fetch") || msg.includes("fetch")) {
          setError("সার্ভারে পৌঁছানো যায়নি। নেটওয়ার্ক দেখে আবার চেষ্টা করুন।");
        } else if (msg.includes("soil analyze failed:")) {
          setError("ছবিটি বিশ্লেষণ করা যায়নি। একই ছবি আবার দিন বা নতুন ছবি তুলুন।");
        } else {
          setError(msg);
        }
      }
    } finally {
      if (requestRef.current === controller) {
        requestRef.current = null;
        setLoading(false);
      }
    }
  }, [file, loading, online]);

  const railEvents: RailEvent[] = useMemo(() => {
    if (!result) return [];
    return (result.agent_trace ?? []).map((e) => ({
      stage: e.stage,
      status: e.status,
      detail: e.detail,
    }));
  }, [result]);

  const askInChat = useCallback(() => {
    setAdvisoryOpen(true);
  }, []);

  return (
    <div className="mx-auto max-w-4xl space-y-7 pb-16">
      {!online && (
        <div role="status" className="sticky top-2 z-20 rounded-lg border border-ochre-soft bg-paper px-4 py-3 text-sm font-medium text-ink shadow-sm">
          ইন্টারনেট সংযোগ নেই। ছবি ও লেখা এই পর্দায় থাকবে; সংযোগ এলে আবার চেষ্টা করুন।
        </div>
      )}
      {/* Page heading */}
      <div>
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="mb-2 text-xs font-semibold text-ochre">মাঠের মাটি পরীক্ষা</p>
            <h1 className="font-display text-3xl text-ink">মাটি ও সেচ</h1>
          </div>
          <div className="flex flex-wrap items-center gap-2 text-xs text-ink-faint">
            <span className="inline-flex items-center gap-1.5 rounded-full border rule bg-paper-2/40 px-2.5 py-1.5"><span className={`h-1.5 w-1.5 rounded-full ${online ? "bg-leaf" : "bg-clay"}`} />{online ? "সিস্টেম অনলাইন" : "অফলাইন"}</span>
            <span className="rounded-full border rule bg-paper-2/40 px-2.5 py-1.5">ডেটাসেট প্রকাশিত · মডেল উন্নয়নে</span>
          </div>
        </div>
        <p className="mt-1 text-sm text-ink-soft">
          পাবনার মাঠ থেকে সংগৃহীত ৭২২টি মাটির ছবি ও টেনশিওমিটার তথ্যভিত্তিক গবেষণা ডেটাসেট। এখানে মাটির বৈজ্ঞানিক আর্দ্রতা টান (kPa)-কে কৃষকের পরিচিত 'জো অবস্থা' ও সেচ নির্দেশনায় রূপান্তর করে দেখানো হয়েছে।
        </p>
      </div>

      {/* Soil Console Flow (Full-width, centered single-column) */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="space-y-6"
      >
        {/* ① Intake zone */}
        <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-5 shadow-[0_10px_28px_rgba(52,39,23,0.05)] sm:p-6">
          <SoilDropzone
            file={file}
            preview={preview}
            onFile={handleFile}
            onValidationError={setError}
            onClear={handleClear}
            onSample={handleSample}
            loading={loading || preparing}
          />

          {/* Action button */}
          <AnimatePresence>
            {file && !result && !loading && !preparing && (
              <motion.button
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                onClick={runAnalyze}
                disabled={!online}
                className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <Search className="h-4 w-4" />
                আর্দ্রতা নির্ণয় করুন
              </motion.button>
            )}
          </AnimatePresence>

          {/* Loading indicator */}
          <AnimatePresence>
            {(loading || preparing) && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="mt-3 flex w-full flex-col items-center justify-center gap-2 rounded-lg bg-leaf/10 py-3 text-sm text-leaf"
              >
                <Loader2 className="h-4 w-4 animate-spin" />
                {preparing ? "ছবি ছোট করে প্রস্তুত হচ্ছে…" : "আর্দ্রতা যাচাই হচ্ছে…"}
                {loading && (
                  <button
                    type="button"
                    onClick={() => requestRef.current?.abort()}
                    className="ml-2 flex min-h-11 items-center gap-1 rounded-lg px-2 font-medium text-clay"
                  >
                    <X className="h-4 w-4" /> বাতিল
                  </button>
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error */}
          <AnimatePresence>
            {error && !loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="mt-3 rounded-lg border border-clay-soft/50 bg-clay-soft/20 px-4 py-3 text-sm text-clay"
              >
                <p>{error}</p>
                {file && (
                  <button
                    type="button"
                    onClick={runAnalyze}
                    className="mt-2 flex min-h-11 items-center gap-2 rounded-lg font-semibold text-leaf"
                  >
                    <RotateCcw className="h-4 w-4" /> আবার চেষ্টা করুন
                  </button>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* ② Pipeline rail — when analysis runs or produced a trace */}
        <AnimatePresence mode="wait">
          {(loading || (result && railEvents.length > 0)) && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: dur.normal, ease: ease.smooth }}
              className="overflow-hidden"
            >
              <AgentTrace
                stages={SOIL_STAGES}
                events={railEvents}
                active={loading}
                title="আর্দ্রতা বিশ্লেষণ প্রবাহ"
                detail="ছবি গ্রহণ → আর্দ্রতা নির্ণয় → মাটি শনাক্ত → পরামর্শ"
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ③ Locked-model result */}
        <AnimatePresence mode="wait">
          {result && !loading && (
            <motion.div key="locked" initial="hidden" animate="visible" exit={{ opacity: 0, y: -8 }} variants={enter}>
              <SoilLockedCard info={dataset} result={result} message={result.error} onAskChat={askInChat} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ④ Dataset showcase (always visible) */}
        {dataset && <SoilDatasetCard info={dataset} />}
        {datasetError && !dataset && (
          <div className="rounded-2xl border rule bg-paper p-6 text-center text-sm text-ink-soft">
            ডেটাসেট তথ্য লোড করা যায়নি। পরে আবার চেষ্টা করুন।
          </div>
        )}
      </motion.div>

      {/* Floating Action Trigger & Slide-Over Assistant Drawer */}
      <SlideOverAdvisory
        open={advisoryOpen}
        onToggle={setAdvisoryOpen}
        triggerEyebrow="মাটি ও সেচ বিশেষজ্ঞ"
        triggerLabel="মাটি ও সেচ পরামর্শ · প্রশ্ন করুন"
        title="মাটি ও সেচ পরামর্শদাতা"
        subtitle="মাটির আর্দ্রতা, সেচ ও ফসল নির্বাচন সম্পর্কিত প্রশ্নোত্তর"
      />
    </div>
  );
}

/* --- Soil dropzone (field-notebook style, soil-flavored) ---------------- */

function SoilDropzone({
  file,
  preview,
  onFile,
  onValidationError,
  onClear,
  onSample,
  loading,
}: {
  file: File | null;
  preview: string | null;
  onFile: (f: File) => void;
  onValidationError?: (message: string) => void;
  onClear: () => void;
  onSample?: (path: string, name: string) => void;
  loading: boolean;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleSelect = useCallback(
    (f: File) => {
      if (!["image/jpeg", "image/png", "image/webp"].includes(f.type)) {
        onValidationError?.("শুধু JPEG, PNG বা WebP ছবি দিন।");
        return;
      }
      if (f.size > 10 * 1024 * 1024) {
        onValidationError?.("ছবিটি ১০MB-এর ছোট হতে হবে।");
        return;
      }
      onFile(f);
    },
    [onFile, onValidationError],
  );

  return (
    <div className="space-y-3">
      <motion.div
        onClick={() => !loading && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
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
        aria-label={preview ? "আপলোড করা মাটির ছবি পরিবর্তন করুন" : "মাটির ছবি আপলোড করুন"}
        className={`surface-lift relative cursor-pointer overflow-hidden rounded-xl border-2 p-8 text-center transition-colors focus-visible:ring-2 focus-visible:ring-leaf ${
          dragging
            ? "border-leaf bg-leaf/5"
            : file
              ? "border-bone bg-paper-2/30"
              : "border-dashed border-bone bg-paper-2/30 hover:border-leaf hover:bg-paper-2/50"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleSelect(f);
            e.target.value = "";
          }}
        />

        <AnimatePresence mode="wait">
          {preview ? (
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
                alt="আপলোড করা মাটির ছবি"
                className="mx-auto max-h-52 rounded-lg border border-bone object-contain shadow-sm"
              />
              <div className="mt-3 flex items-center justify-center gap-3 text-xs text-ink-faint">
                <span className="max-w-[160px] truncate">{file?.name ?? "ছবি"}</span>
                {!loading && (
                  <button
                    onClick={(e) => { e.stopPropagation(); onClear(); }}
                    className="flex min-h-11 items-center gap-1 rounded-lg px-2 text-ink-soft transition-colors hover:text-leaf"
                  >
                    <RotateCcw className="h-3 w-3" /> পরিবর্তন
                  </button>
                )}
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: dur.fast }}
            >
              <SoilLine />
              <div className="mt-4 font-display text-lg text-ink">মাটির ছবি দিন</div>
              <div className="mt-1 flex items-center justify-center gap-1.5 text-xs text-ink-faint">
                টানে দিন বা ক্লিক করুন
              </div>
              <div className="mt-1 text-xs text-ink-faint/70">
                JPEG · PNG · WebP · সর্বোচ্চ ১০MB
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

      {/* Released dataset sample photos — real field images from the release */}
      {!preview && onSample && (
        <div className="rounded-lg border border-leaf/20 bg-leaf/5 p-3">
          <div className="text-sm font-medium text-ink">ডেটাসেটের নমুনা দিয়ে চেষ্টা করুন</div>
          <p className="mt-0.5 text-xs text-ink-soft">পাবনা মাঠক্যাম্পেইনের প্রকৃত ছবি (মুক্ত ডেটাসেট থেকে)</p>
          <div className="mt-3 grid grid-cols-3 gap-2">
            {SOIL_SAMPLES.map((s) => (
              <button
                key={s.path}
                type="button"
                onClick={() => onSample(s.path, s.name)}
                disabled={loading}
                className="group overflow-hidden rounded-lg border rule bg-paper text-left transition-colors hover:border-leaf disabled:cursor-not-allowed disabled:opacity-60"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={s.path} alt={s.name} className="aspect-square w-full object-cover transition-transform duration-300 group-hover:scale-105" loading="lazy" />
                <div className="px-2 py-1.5 text-xs text-ink-soft">{s.name}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* A simple soil-layers line drawing — consistent with the field-notebook style. */
function SoilLine() {
  return (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden className="mx-auto">
      <path d="M8 30C14 26 22 24 40 24" stroke="var(--color-ochre)" strokeWidth="1.5" strokeLinecap="round" opacity="0.55" />
      <path d="M8 36C14 33 22 31 40 31" stroke="var(--color-leaf)" strokeWidth="1.5" strokeLinecap="round" opacity="0.4" />
      <path d="M8 42C14 40 22 38 40 38" stroke="var(--color-ink-soft)" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
      <path d="M10 16L20 8L30 14L40 6" stroke="var(--color-ochre)" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" opacity="0.35" />
      <circle cx="20" cy="8" r="1.5" fill="var(--color-ochre)" opacity="0.5" />
      <circle cx="40" cy="6" r="1.5" fill="var(--color-ochre)" opacity="0.5" />
    </svg>
  );
}