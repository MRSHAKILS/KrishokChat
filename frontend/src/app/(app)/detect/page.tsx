"use client";

import { useState, useCallback, useMemo, useEffect, useRef } from "react";

const SCAN_STORAGE_KEY = "krishokchat:latest-scan:v1";
import { motion, AnimatePresence } from "motion/react";
import { Search, Loader2, RotateCcw, X } from "lucide-react";
import { detectDisease, type DetectResponse } from "@/lib/api";
import { VISION_STAGES, type RailEvent } from "@/components/detect/pipeline-rail";
import { AgentTrace } from "@/components/agent-trace";
import { IntakeZone } from "@/components/detect/intake-zone";
import { DiagnosisCard } from "@/components/detect/diagnosis-card";
import { UrgentAlertBanner } from "@/components/notifications/urgent-alert-banner";
import { TreatmentCard } from "@/components/detect/treatment-card";
import { SlideOverAdvisory } from "@/components/chat/slide-over-advisory";
import { stagger, enter, dur, ease } from "@/lib/motion";
import { prepareUploadImage } from "@/lib/image";

const VISION_ONDEVICE_ENABLED = process.env.NEXT_PUBLIC_VISION_ONDEVICE_ENABLED === "true";

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
  const [advisoryOpen, setAdvisoryOpen] = useState(false);
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
      hint, and detected context are hydrated from localStorage in a
      single mount effect AFTER SSR hydration. Starting with the default
      values keeps the first server and client renders identical (a lazy
      initializer reading localStorage would produce a hydration
      mismatch: the server renders null, the client re-renders with the
      stored value on first paint). */
  const [result, setResult] = useState<DetectResponse | null>(null);

  const [cropHint, setCropHint] = useState("");

  const [detectedContext, setDetectedContext] = useState<{ crop: string; disease: string } | null>(null);

  /* Hydrate persistent scan state once after the client mounts. */
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(SCAN_STORAGE_KEY);
      if (!saved) return;
      const parsed = JSON.parse(saved) as {
        result: DetectResponse;
        cropHint: string;
        savedAt: number;
      };
      if (parsed?.result) setResult(parsed.result);
      if (parsed?.cropHint) setCropHint(parsed.cropHint);
      const r = parsed?.result;
      if (r?.crop && r?.disease) {
        setDetectedContext({ crop: r.crop, disease: r.disease });
      }
    } catch {
      // Storage may be unavailable or corrupt; detection context stays in memory.
    }
  }, []);

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

  useEffect(() => {
    if (!VISION_ONDEVICE_ENABLED) return;
    let cancelled = false;
    const idle = (window as unknown as { requestIdleCallback?: (cb: () => void) => number }).requestIdleCallback;
    const run = async () => {
      if (cancelled) return;
      try {
        const mod = await import("@/lib/vision-ondevice");
        if (!cancelled && mod.isOnDeviceEnabled()) await mod.warmUpOnDevice(["crop_classifier"]);
      } catch {
        // warm-up is best-effort
      }
    };
    if (idle) idle(run);
    else window.setTimeout(run, 1200);
    return () => { cancelled = true; };
  }, []);

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
    setAdvisoryOpen(true);
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
    if (!file || loading) return;
    // Offline on-device path does not require `online`; the server fallback does.
    const controller = new AbortController();
    requestRef.current?.abort();
    requestRef.current = controller;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      // 1) Try on-device WASM inference when the flag is on. This module is
      // dynamically imported so onnxruntime-web never enters the First Load chunk.
      if (VISION_ONDEVICE_ENABLED) {
        try {
          const mod = await import("@/lib/vision-ondevice");
          if (mod.isOnDeviceEnabled()) {
            const od = await mod.detectDiseaseOnDevice(file, {
              cropHint: cropHint || undefined,
            });
            if (controller.signal.aborted) return;
            const mapped: DetectResponse = {
              status: od.status as DetectResponse["status"],
              detection_mode: "classification",
              crop: od.crop,
              crop_confidence: od.cropConfidence,
              crop_source: od.cropSource as DetectResponse["crop_source"],
              disease: od.disease,
              disease_confidence: od.diseaseConfidence,
              boxes: [],
              disease_info: null,
              top3_crops: od.top3Crops,
              top3_diseases: od.top3Diseases,
              // Advisory still comes from the server when online; offline shows
              // classification only (honest per AGENTS.md rule 5).
              treatment_advice: null,
              treatment_confidence: null,
              treatment_sources: [],
              verifier_flags: [],
              agent_trace: [
                { stage: "intake", status: "complete", detail: `on-device ${od.latencyMs}ms` },
                { stage: "crop_classification", status: od.crop ? "complete" : "skip", detail: od.crop ?? undefined },
                { stage: "disease_classification", status: od.disease ? "complete" : "skip", detail: od.disease ?? undefined },
              ],
              quality_warnings: [],
            };
            // When online, enrich with server-side advisory (grounded generation).
            // Fire-and-forget: classification is already shown; advisory fills in.
            if (online && od.crop && od.disease && (od.status === "diagnosed" || od.status === "healthy")) {
              setResult(mapped);
              if (mapped.crop && mapped.disease) setDetectedContext({ crop: mapped.crop, disease: mapped.disease });
              try {
                const server = await detectDisease(file, {
                  cropHint: cropHint || undefined,
                  signal: controller.signal,
                });
                if (controller.signal.aborted) return;
                setResult({
                  ...mapped,
                  disease_info: server.disease_info ?? null,
                  treatment_advice: server.treatment_advice,
                  treatment_confidence: server.treatment_confidence,
                  treatment_sources: server.treatment_sources,
                  verifier_flags: server.verifier_flags,
                  agent_trace: [...mapped.agent_trace, ...server.agent_trace],
                });
                return;
              } catch {
                // Advisory enrichment failed — keep the on-device classification alone.
                return;
              }
            }
            setResult(mapped);
            if (mapped.crop && mapped.disease) setDetectedContext({ crop: mapped.crop, disease: mapped.disease });
            else setDetectedContext(null);
            return;
          }
        } catch (e) {
          if (controller.signal.aborted) return;
          // On-device path failed; fall through to server. Log for debugging, do not surface.
          console.warn("[on-device] fallback to server:", e);
        }
      }
      if (!online) {
        setError("ইন্টারনেট সংযোগ নেই। অন-ডিভাইস মোড বন্ধ থাকায় সার্ভারে পৌঁছানো যায়নি।");
        return;
      }
      const r = await detectDisease(file, {
        cropHint: cropHint || undefined,
        signal: controller.signal,
      });
      if (controller.signal.aborted) return;
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
    <div className="mx-auto max-w-4xl space-y-7 pb-16">
      <UrgentAlertBanner />
      {!online && (
        <div role="status" className="sticky top-2 z-20 rounded-lg border border-ochre-soft bg-paper px-4 py-3 text-sm font-medium text-ink shadow-sm">
          ইন্টারনেট সংযোগ নেই। ছবি ও লেখা এই পর্দায় থাকবে; সংযোগ এলে আবার চেষ্টা করুন।
        </div>
      )}
      {/* Page heading */}
      <div>
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="mb-2 text-xs font-semibold text-ochre">ছবির মাধ্যমে ফসল পরামর্শ</p>
            <h1 className="font-display text-3xl text-ink">ফসলের রোগ নির্ণয়</h1>
          </div>
          <div className="flex flex-wrap items-center gap-2 text-xs text-ink-faint">
            <span className="inline-flex items-center gap-1.5 rounded-full border rule bg-paper-2/40 px-2.5 py-1.5"><span className={`h-1.5 w-1.5 rounded-full ${online ? "bg-leaf" : "bg-clay"}`} />{online ? "সিস্টেম অনলাইন" : "অফলাইন"}</span>
            <span className="rounded-full border rule bg-paper-2/40 px-2.5 py-1.5">শ্রেণিবিন্যাস মোড</span>
            {VISION_ONDEVICE_ENABLED && (
              <span className="inline-flex items-center gap-1 rounded-full border border-emerald-200 bg-emerald-500/10 px-2.5 py-1.5 font-mono text-[10px] leading-none text-emerald-700">On-Device INT8</span>
            )}
          </div>
        </div>
        <p className="mt-1 text-sm text-ink-soft">
          পাতার ছবি দিন — ফসল ও রোগ ডিভাইসেই শনাক্ত হবে — এরপর অনুমোদিত উৎস থেকে চিকিৎসা-পরামর্শ দেখানো হবে।
        </p>
      </div>

      {/* Detection Flow (Full-width, centered single-column) */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="space-y-6"
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

        {/* ④ Treatment Card — with spray calculator & prescription slip */}
        <AnimatePresence>
          {result && result.treatment_advice && !loading && (
            <motion.div initial="hidden" animate="visible" exit={{ opacity: 0 }} variants={enter}>
              <TreatmentCard result={result} onFollowUp={handleFollowUp} />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Floating Action Trigger & Slide-Over Assistant Drawer */}
      <SlideOverAdvisory
        open={advisoryOpen}
        onToggle={setAdvisoryOpen}
        detectedCrop={detectedContext?.crop}
        detectedDisease={detectedContext?.disease}
        prefillQuestion={followUpQuestion}
      />
    </div>
  );
}
