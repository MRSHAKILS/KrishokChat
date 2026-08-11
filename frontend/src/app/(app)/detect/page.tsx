"use client";

import { useState, useCallback, useMemo, useEffect, useRef } from "react";

const SCAN_STORAGE_KEY = "krishokchat:latest-scan:v1";
import { motion, AnimatePresence } from "motion/react";
import { Search, Loader2, Camera, MessageCircle, RotateCcw, X } from "lucide-react";
import { detectDisease, type DetectResponse } from "@/lib/api";
import { VISION_STAGES, type RailEvent } from "@/components/detect/pipeline-rail";
import { AgentTrace } from "@/components/agent-trace";
import { IntakeZone } from "@/components/detect/intake-zone";
import { DiagnosisCard } from "@/components/detect/diagnosis-card";
import { TreatmentCard } from "@/components/detect/treatment-card";
import { ContextBanner } from "@/components/detect/context-banner";
import { QAPanel } from "@/components/qa-panel";
import { stagger, enter, dur, ease } from "@/lib/motion";
import { prepareUploadImage } from "@/lib/image";

/* =========================================================================
   DetectPage — the hero page.
   Left: image intake → pipeline rail → diagnosis → treatment.
   Right: chat panel (always visible), with detected-crop context banner.
   ========================================================================= */

export default function DetectPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activePane, setActivePane] = useState<"detect" | "chat">("detect");
  const [sampleLoading, setSampleLoading] = useState(false);
  const [preparing, setPreparing] = useState(false);
  const [online, setOnline] = useState(true);
  const requestRef = useRef<AbortController | null>(null);
  /* Crop selection — the crop classifier has no Rice class, so the farmer
      declares the crop and the backend routes to the matching disease model
      directly. Empty = automatic classification. */
  const [followUpQuestion, setFollowUpQuestion] = useState<string | null>(null);

  /* Restore the latest scan result on mount so a refresh keeps context
      without keeping the raw image bytes in storage. The result, crop
      hint, and detected context are initialized from localStorage via
      lazy useState initializers to avoid cascading setState-in-effect.
      Guarded for SSR prerender where `window` is undefined. */
  const [result, setResult] = useState<DetectResponse | null>(() => {
    try {
      if (typeof window === "undefined") return null;
      const saved = window.localStorage.getItem(SCAN_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved) as {
          result: DetectResponse;
          cropHint: string;
          savedAt: number;
        };
        return parsed?.result ?? null;
      }
    } catch {
      // ignore
    }
    return null;
  });

  const [cropHint, setCropHint] = useState(() => {
    try {
      if (typeof window === "undefined") return "";
      const saved = window.localStorage.getItem(SCAN_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved) as { cropHint: string };
        return parsed?.cropHint ?? "";
      }
    } catch {
      // ignore
    }
    return "";
  });

  const [detectedContext, setDetectedContext] = useState<{ crop: string; disease: string } | null>(() => {
    try {
      if (typeof window === "undefined") return null;
      const saved = window.localStorage.getItem(SCAN_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved) as { result: DetectResponse };
        const r = parsed?.result;
        return r?.crop && r?.disease ? { crop: r.crop, disease: r.disease } : null;
      }
    } catch {
      // ignore
    }
    return null;
  });

  /* Persist the latest scan result separately from chat history. */
  useEffect(() => {
    if (!result) return;
    try {
      window.localStorage.setItem(
        SCAN_STORAGE_KEY,
        JSON.stringify({ result, cropHint, savedAt: Date.now() }),
      );
    } catch {
      // Storage may be unavailable; detection result stays in memory.
    }
  }, [result, cropHint]);

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
    setFollowUpQuestion(null);
  }, []);

  const handleClearScan = useCallback(() => {
    setResult(null);
    setDetectedContext(null);
    try {
      window.localStorage.removeItem(SCAN_STORAGE_KEY);
    } catch {
      // ignore
    }
  }, []);

  const handleFollowUp = useCallback((question: string) => {
    setFollowUpQuestion(question);
    setActivePane("chat");
  }, []);

  const handleSample = useCallback(async (samplePath: string, sampleName: string) => {
    setSampleLoading(true);
    setError(null);
    try {
      const response = await fetch(samplePath);
      if (!response.ok) throw new Error("sample image unavailable");
      const blob = await response.blob();
      // The verified sample is a rice leaf; the crop model cannot classify
      // rice itself, so preselect it for a guaranteed rice diagnosis.
      setCropHint("rice");
      handleFile(new File([blob], sampleName, { type: blob.type || "image/jpeg" }));
    } catch {
      setError("নমুনা ছবিটি এখন পাওয়া যাচ্ছে না। নিজের ছবি আপলোড করুন।");
    } finally {
      setSampleLoading(false);
    }
  }, [handleFile]);

  const runDetect = useCallback(async () => {
    if (!file || loading || !online) return;
    const controller = new AbortController();
    requestRef.current?.abort();
    requestRef.current = controller;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const r = await detectDisease(file, {
        cropHint: cropHint || undefined,
        signal: controller.signal,
      });
        setResult(r);
      if (r.crop && r.disease) {
        setDetectedContext({ crop: r.crop, disease: r.disease });
      } else {
        setDetectedContext(null);
      }
    } catch (e: unknown) {
      if (!controller.signal.aborted) {
        const msg = e instanceof Error ? e.message : "বিশ্লেষণে সমস্যা হয়েছে";
        if (msg.includes("Failed to fetch") || msg.includes("fetch")) {
          setError("সার্ভারে পৌঁছানো যায়নি। নেটওয়ার্ক দেখে আবার চেষ্টা করুন।");
        } else if (msg.includes("detect failed:")) {
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
  }, [file, cropHint, loading, online]);

  return (
    <div className="space-y-7">
      {!online && (
        <div role="status" className="sticky top-2 z-20 rounded-lg border border-ochre-soft bg-paper px-4 py-3 text-sm font-medium text-ink shadow-sm">
          ইন্টারনেট সংযোগ নেই। ছবি ও লেখা এই পর্দায় থাকবে; সংযোগ এলে আবার চেষ্টা করুন।
        </div>
      )}
      {/* Page heading */}
      <div>
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-ochre">MULTIMODAL FIELD CONSOLE</p>
            <h1 className="font-display text-3xl text-ink">ফসলের রোগ নির্ণয়</h1>
          </div>
          <div className="flex flex-wrap items-center gap-2 text-[11px] text-ink-faint">
            <span className="inline-flex items-center gap-1.5 rounded-full border rule bg-paper-2/40 px-2.5 py-1.5"><span className={`h-1.5 w-1.5 rounded-full ${online ? "bg-leaf" : "bg-clay"}`} />{online ? "সিস্টেম অনলাইন" : "অফলাইন"}</span>
            <span className="rounded-full border rule bg-paper-2/40 px-2.5 py-1.5">শ্রেণিবিন্যাস মোড</span>
          </div>
        </div>
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

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1.08fr)_minmax(320px,0.92fr)]">
        {/* === LEFT: Detection Flow === */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={stagger}
          className={`space-y-5 ${activePane === "chat" ? "hidden lg:block" : "block"}`}
        >
          {/* ① Intake Zone */}
          <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-5 shadow-[0_10px_28px_rgba(52,39,23,0.05)] sm:p-6">
            <IntakeZone
              file={file}
              preview={preview}
              onFile={handleFile}
              onValidationError={setError}
              onClear={handleClear}
              onSample={handleSample}
              sampleLoading={sampleLoading}
              qualityWarnings={result?.quality_warnings ?? []}
              loading={loading || preparing}
              cropHint={cropHint}
              onCropHintChange={setCropHint}
            />

            {/* Action button */}
            <AnimatePresence>
              {file && !result && !loading && !preparing && (
                <motion.button
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  onClick={runDetect}
                  disabled={!online}
                  className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <Search className="h-4 w-4" />
                  নির্ণয় করুন
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
                  {preparing ? "ছবি ছোট করে প্রস্তুত হচ্ছে…" : "বিশ্লেষণ হচ্ছে…"}
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
                      onClick={runDetect}
                      className="mt-2 flex min-h-11 items-center gap-2 rounded-lg font-semibold text-leaf"
                    >
                      <RotateCcw className="h-4 w-4" /> আবার চেষ্টা করুন
                    </button>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* ② Pipeline Rail — appears when result has trace or while loading */}
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
                  stages={VISION_STAGES}
                  events={railEvents}
                  active={loading}
                  title="রোগ বিশ্লেষণ প্রবাহ"
                  detail="ছবি থেকে শ্রেণিবিন্যাস ও grounded advisory তৈরি হচ্ছে"
                />
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
                <DiagnosisCard result={result} onClear={handleClearScan} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* ④ Treatment Card — only when diagnosed with treatment advice.
              status may be absent on legacy backends; show it whenever
              treatment advice exists (it only exists for real diagnoses). */}
          <AnimatePresence>
            {result && result.treatment_advice && !loading && (
              <motion.div initial="hidden" animate="visible" exit={{ opacity: 0 }} variants={enter}>
                <TreatmentCard result={result} onFollowUp={handleFollowUp} />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* === RIGHT: Chat Panel (always visible) === */}
        <section className={`min-h-[60vh] flex-col rounded-2xl border rule bg-paper p-5 shadow-[0_10px_28px_rgba(52,39,23,0.05)] lg:sticky lg:top-20 lg:flex lg:max-h-[calc(100vh-6rem)] ${activePane === "chat" ? "flex" : "hidden lg:flex"}`}>
          <div className="mb-3 border-b rule pb-4">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-ochre">CONTEXTUAL ADVISORY</p>
                <h2 className="mt-1 font-display text-xl text-ink">কৃষি পরামর্শ</h2>
              </div>
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-leaf/10 text-leaf" aria-hidden><MessageCircle className="h-4 w-4" /></span>
            </div>
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
              prefillQuestion={followUpQuestion}
            />
          </div>
        </section>
      </div>
    </div>
  );
}
