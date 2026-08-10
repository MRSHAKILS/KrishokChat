"use client";

import { useState, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Search, Loader2, Camera, MessageCircle } from "lucide-react";
import { detectDisease, type DetectResponse } from "@/lib/api";
import { VISION_STAGES, PipelineRail, type RailEvent } from "@/components/detect/pipeline-rail";
import { IntakeZone } from "@/components/detect/intake-zone";
import { DiagnosisCard } from "@/components/detect/diagnosis-card";
import { TreatmentCard } from "@/components/detect/treatment-card";
import { ContextBanner } from "@/components/detect/context-banner";
import { QAPanel } from "@/components/qa-panel";
import { stagger, enter, dur, ease } from "@/lib/motion";

/* =========================================================================
   DetectPage — the hero page.
   Left: image intake → pipeline rail → diagnosis → treatment.
   Right: chat panel (always visible), with detected-crop context banner.
   ========================================================================= */

export default function DetectPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<DetectResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activePane, setActivePane] = useState<"detect" | "chat">("detect");
  const [sampleLoading, setSampleLoading] = useState(false);
  const [detectedContext, setDetectedContext] = useState<{
    crop: string;
    disease: string;
  } | null>(null);

  /* Pipeline events — derived from the result's agent_trace.
     While loading (no result yet), we show the rail in an "active" state
     with the intake node complete and the rest pending. */
  const railEvents: RailEvent[] = useMemo(() => {
    if (!result) return [];
    return (result.agent_trace ?? []).map((e) => ({
      stage: e.stage,
      status: e.status,
      detail: e.detail,
    }));
  }, [result]);

  const handleFile = useCallback((f: File) => {
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError(null);
  }, []);

  const handleClear = useCallback(() => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  }, []);

  const handleSample = useCallback(async (samplePath: string, sampleName: string) => {
    setSampleLoading(true);
    setError(null);
    try {
      const response = await fetch(samplePath);
      if (!response.ok) throw new Error("sample image unavailable");
      const blob = await response.blob();
      handleFile(new File([blob], sampleName, { type: blob.type || "image/jpeg" }));
    } catch {
      setError("নমুনা ছবিটি এখন পাওয়া যাচ্ছে না। নিজের ছবি আপলোড করুন।");
    } finally {
      setSampleLoading(false);
    }
  }, [handleFile]);

  const runDetect = useCallback(async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const r = await detectDisease(file);
      setResult(r);
      if (r.crop && r.disease) {
        setDetectedContext({ crop: r.crop, disease: r.disease });
      } else {
        setDetectedContext(null);
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "বিশ্লেষণে সমস্যা হয়েছে";
      // Distinguish network errors (backend not running) from API errors
      if (msg.includes("Failed to fetch") || msg.includes("fetch")) {
        setError("ব্যাকএন্ড সার্ভারে সংযোগ ব্যর্থ। নিশ্চিত করুন যে ব্যাকএন্ড চলছে (uv run uvicorn app.main:app --reload)");
      } else if (msg.includes("detect failed:")) {
        setError(`ব্যাকএন্ড ত্রুটি: ${msg}`);
      } else {
        setError(msg);
      }
    }
    setLoading(false);
  }, [file]);

  return (
    <div className="space-y-7">
      {/* Page heading */}
      <div>
        <h1 className="font-display text-3xl text-ink">ফসলের রোগ নির্ণয়</h1>
        <p className="mt-1 text-sm text-ink-soft">
          পাতার ছবি দিন — ফসল শনাক্ত করে নির্দিষ্ট রোগ মডেল দিয়ে বিশ্লেষণ করা হবে।
          ডান পাশের চ্যাটে সনাক্ত করা ফসলের ভিত্তিতে প্রশ্ন করুন।
        </p>
      </div>

      {/* Mobile keeps the two workflows focused instead of stacking a long
          diagnosis, treatment, and chat page. Desktop always shows both. */}
      <div className="flex rounded-xl border rule bg-paper-2/40 p-1 lg:hidden" role="tablist" aria-label="রোগ নির্ণয় ও পরামর্শ">
        <button
          type="button"
          role="tab"
          aria-selected={activePane === "detect"}
          onClick={() => setActivePane("detect")}
          className={`flex min-h-11 flex-1 items-center justify-center gap-2 rounded-lg px-3 text-sm font-medium transition-colors ${
            activePane === "detect" ? "bg-leaf text-paper shadow-sm" : "text-ink-soft"
          }`}
        >
          <Camera className="h-4 w-4" /> রোগ নির্ণয়
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={activePane === "chat"}
          onClick={() => setActivePane("chat")}
          className={`relative flex min-h-11 flex-1 items-center justify-center gap-2 rounded-lg px-3 text-sm font-medium transition-colors ${
            activePane === "chat" ? "bg-leaf text-paper shadow-sm" : "text-ink-soft"
          }`}
        >
          <MessageCircle className="h-4 w-4" /> পরামর্শ চ্যাট
          {detectedContext && activePane !== "chat" && (
            <span className="absolute right-3 top-2 h-2 w-2 rounded-full bg-ochre" aria-label="নতুন রোগ নির্ণয়ের তথ্য" />
          )}
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* === LEFT: Detection Flow === */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={stagger}
          className={`space-y-5 ${activePane === "chat" ? "hidden lg:block" : "block"}`}
        >
          {/* ① Intake Zone */}
          <motion.div variants={enter} className="rounded-xl border rule bg-paper p-5">
            <IntakeZone
              file={file}
              preview={preview}
              onFile={handleFile}
              onClear={handleClear}
              onSample={handleSample}
              sampleLoading={sampleLoading}
              qualityWarnings={result?.quality_warnings ?? []}
              loading={loading}
            />

            {/* Action button */}
            <AnimatePresence>
              {file && !result && !loading && (
                <motion.button
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  onClick={runDetect}
                  className="mt-3 flex w-full items-center justify-center gap-2 rounded-lg bg-leaf py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
                >
                  <Search className="h-4 w-4" />
                  নির্ণয় করুন
                </motion.button>
              )}
            </AnimatePresence>

            {/* Loading indicator */}
            <AnimatePresence>
              {loading && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="mt-3 flex w-full items-center justify-center gap-2 rounded-lg bg-leaf/10 py-3 text-sm text-leaf"
                >
                  <Loader2 className="h-4 w-4 animate-spin" />
                  বিশ্লেষণ হচ্ছে…
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
                  {error}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* ② Pipeline Rail — appears when result has trace or while loading */}
          <AnimatePresence>
            {(loading || (result && railEvents.length > 0)) && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: dur.normal, ease: ease.smooth }}
                className="overflow-hidden rounded-xl border rule bg-paper-2/30 p-5"
              >
                <div className="mb-3 text-[11px] font-semibold text-ink-faint">
                  বিশ্লেষণ প্রক্রিয়া
                </div>
                <PipelineRail stages={VISION_STAGES} events={railEvents} active={loading} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* ③ Diagnosis Card */}
          <AnimatePresence mode="wait">
            {result && !loading && (
              <motion.div
                key="diagnosis"
                initial="hidden"
                animate="visible"
                exit={{ opacity: 0, y: -8 }}
                variants={enter}
              >
                <DiagnosisCard result={result} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* ④ Treatment Card — only when diagnosed with treatment advice.
              status may be absent on legacy backends; show it whenever
              treatment advice exists (it only exists for real diagnoses). */}
          <AnimatePresence>
            {result && result.treatment_advice && !loading && (
              <motion.div initial="hidden" animate="visible" exit={{ opacity: 0 }} variants={enter}>
                <TreatmentCard result={result} />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* === RIGHT: Chat Panel (always visible) === */}
        <section className={`min-h-[60vh] flex-col rounded-xl border rule bg-paper p-5 lg:sticky lg:top-20 lg:flex lg:max-h-[calc(100vh-6rem)] ${activePane === "chat" ? "flex" : "hidden lg:flex"}`}>
          <div className="mb-3">
            <h2 className="font-display text-lg text-ink">কৃষি পরামর্শ</h2>
            <ContextBanner
              crop={detectedContext?.crop ?? null}
              disease={detectedContext?.disease ?? null}
            />
            {!detectedContext && (
              <p className="mt-1 text-sm text-ink-soft">
                প্রথমে বাম দিকে ফসলের ছবি দিয়ে নির্ণয় করুন। আপনার প্রশ্ন বাংলায় লিখুন।
              </p>
            )}
          </div>
          <div className="flex-1 overflow-hidden">
            <QAPanel
              detectedCrop={detectedContext?.crop}
              detectedDisease={detectedContext?.disease}
            />
          </div>
        </section>
      </div>
    </div>
  );
}
