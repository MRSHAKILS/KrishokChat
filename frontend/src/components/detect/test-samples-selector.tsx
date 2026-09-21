"use client";

import { useState, useMemo, useCallback } from "react";
import {
  Sparkles,
  CheckCircle2,
  Loader2,
  FlaskConical,
  Search,
  ChevronLeft,
  ChevronRight,
  Shuffle,
  Zap,
} from "lucide-react";
import { VERIFIED_TEST_SAMPLES, CROP_GROUPS, type TestSampleInstance } from "@/lib/test-samples";
import { useLanguage } from "@/context/language-context";
import { cn } from "@/lib/utils";

interface TestSamplesSelectorProps {
  onSelectSample: (path: string, name: string, cropHint?: string, diseaseHint?: string, autoRun?: boolean) => void;
  loading?: boolean;
  sampleLoading?: boolean;
  compact?: boolean;
}

export function TestSamplesSelector({
  onSelectSample,
  loading = false,
  sampleLoading = false,
  compact = false,
}: TestSamplesSelectorProps) {
  const { t, locale, formatNumber } = useLanguage();

  // Crop filter: "all" or specific crop name
  const [activeCrop, setActiveCrop] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedId, setSelectedId] = useState<string>(VERIFIED_TEST_SAMPLES[0].id);

  // Filtered samples based on active crop tab and search query
  const filteredSamples = useMemo(() => {
    return VERIFIED_TEST_SAMPLES.filter((s) => {
      const matchCrop = activeCrop === "all" || s.crop.toLowerCase() === activeCrop.toLowerCase();
      if (!matchCrop) return false;
      if (!searchQuery.trim()) return true;
      const q = searchQuery.toLowerCase().trim();
      return (
        s.disease.toLowerCase().includes(q) ||
        s.diseaseBn.toLowerCase().includes(q) ||
        s.diseaseEn.toLowerCase().includes(q) ||
        s.cropBn.toLowerCase().includes(q) ||
        s.cropEn.toLowerCase().includes(q) ||
        s.id.toLowerCase().includes(q)
      );
    });
  }, [activeCrop, searchQuery]);

  // Current selected instance (fallback to first filtered item or first sample)
  const currentSample = useMemo(() => {
    const found = VERIFIED_TEST_SAMPLES.find((s) => s.id === selectedId);
    if (found && (activeCrop === "all" || found.crop.toLowerCase() === activeCrop.toLowerCase())) {
      return found;
    }
    return filteredSamples[0] ?? VERIFIED_TEST_SAMPLES[0];
  }, [selectedId, activeCrop, filteredSamples]);

  const currentIndex = useMemo(() => {
    return filteredSamples.findIndex((s) => s.id === currentSample.id);
  }, [filteredSamples, currentSample]);

  // Actions
  const handleApply = useCallback(
    (instance: TestSampleInstance, autoRun = false) => {
      setSelectedId(instance.id);
      onSelectSample(instance.imageSrc, `${instance.id}.jpg`, instance.cropHint, instance.disease, autoRun);
    },
    [onSelectSample]
  );

  const handlePrev = useCallback(() => {
    if (filteredSamples.length === 0) return;
    const prevIdx = (currentIndex - 1 + filteredSamples.length) % filteredSamples.length;
    const target = filteredSamples[prevIdx];
    handleApply(target);
  }, [currentIndex, filteredSamples, handleApply]);

  const handleNext = useCallback(() => {
    if (filteredSamples.length === 0) return;
    const nextIdx = (currentIndex + 1) % filteredSamples.length;
    const target = filteredSamples[nextIdx];
    handleApply(target);
  }, [currentIndex, filteredSamples, handleApply]);

  const handleRandom = useCallback(() => {
    const pool = filteredSamples.length > 0 ? filteredSamples : VERIFIED_TEST_SAMPLES;
    const randomIdx = Math.floor(Math.random() * pool.length);
    const target = pool[randomIdx];
    handleApply(target);
  }, [filteredSamples, handleApply]);

  const handleSelectChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      const newId = e.target.value;
      setSelectedId(newId);
      const found = VERIFIED_TEST_SAMPLES.find((s) => s.id === newId);
      if (found) {
        onSelectSample(found.imageSrc, `${found.id}.jpg`, found.cropHint, found.disease, false);
      }
    },
    [onSelectSample]
  );

  const currentCrop = locale === "bn" ? currentSample.cropBn : currentSample.cropEn;
  const currentDisease = locale === "bn" ? currentSample.diseaseBn : currentSample.diseaseEn;

  return (
    <div className="rounded-xl border border-leaf/25 bg-leaf/5 p-3 sm:p-4 transition-all space-y-3 shadow-2xs">
      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-leaf/10 pb-2.5">
        <div className="flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-leaf/15 text-leaf shadow-2xs">
            <FlaskConical className="h-4 w-4" />
          </span>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-ink">{t.samples.title}</span>
              <span className="inline-flex items-center gap-1 rounded-full bg-leaf/15 px-2 py-0.5 text-[10px] font-semibold text-leaf border border-leaf/20">
                <CheckCircle2 className="h-2.5 w-2.5" />
                <span>{t.samples.badge}</span>
              </span>
            </div>
            {!compact && (
              <p className="text-[11px] text-ink-soft">
                {t.samples.subtitle}
              </p>
            )}
          </div>
        </div>

        {/* Quick Stepper Controls for Reviewers */}
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={handlePrev}
            disabled={loading || sampleLoading || filteredSamples.length <= 1}
            title={t.samples.prev}
            className="flex h-7 w-7 items-center justify-center rounded-md border border-leaf/20 bg-paper text-ink transition-colors hover:bg-leaf/10 disabled:opacity-40 cursor-pointer"
          >
            <ChevronLeft className="h-3.5 w-3.5" />
          </button>

          <span className="px-1 text-[11px] font-mono text-ink-faint">
            {currentIndex >= 0 ? currentIndex + 1 : 1}/{filteredSamples.length}
          </span>

          <button
            type="button"
            onClick={handleNext}
            disabled={loading || sampleLoading || filteredSamples.length <= 1}
            title={t.samples.next}
            className="flex h-7 w-7 items-center justify-center rounded-md border border-leaf/20 bg-paper text-ink transition-colors hover:bg-leaf/10 disabled:opacity-40 cursor-pointer"
          >
            <ChevronRight className="h-3.5 w-3.5" />
          </button>

          <button
            type="button"
            onClick={handleRandom}
            disabled={loading || sampleLoading}
            title={t.samples.random}
            className="ml-1 inline-flex h-7 items-center gap-1 rounded-md border border-leaf/25 bg-paper px-2 text-[11px] font-medium text-leaf hover:bg-leaf/10 disabled:opacity-40 cursor-pointer"
          >
            <Shuffle className="h-3 w-3" />
            <span className="hidden sm:inline">{t.samples.random}</span>
          </button>
        </div>
      </div>

      {/* Crop Filter Tabs */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs scrollbar-none">
        <button
          type="button"
          onClick={() => setActiveCrop("all")}
          className={cn(
            "shrink-0 rounded-lg px-2.5 py-1 text-xs font-medium transition-colors cursor-pointer",
            activeCrop === "all"
              ? "bg-leaf text-paper shadow-2xs font-semibold"
              : "bg-paper/70 text-ink-soft hover:bg-paper hover:text-ink border border-leaf/15"
          )}
        >
          {t.samples.allCrops} (100)
        </button>

        {CROP_GROUPS.map((grp) => {
          const isActive = activeCrop.toLowerCase() === grp.crop.toLowerCase();
          const label = locale === "bn" ? grp.cropBn : grp.cropEn;
          return (
            <button
              key={grp.crop}
              type="button"
              onClick={() => setActiveCrop(grp.crop.toLowerCase())}
              className={cn(
                "shrink-0 rounded-lg px-2.5 py-1 text-xs font-medium transition-colors cursor-pointer flex items-center gap-1",
                isActive
                  ? "bg-leaf text-paper shadow-2xs font-semibold"
                  : "bg-paper/70 text-ink-soft hover:bg-paper hover:text-ink border border-leaf/15"
              )}
            >
              <span>{grp.icon}</span>
              <span>{label}</span>
              <span className="text-[10px] opacity-75">({grp.count})</span>
            </button>
          );
        })}
      </div>

      {/* Search Input & Dropdown Selector */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
        {/* Search input */}
        <div className="relative flex-1 sm:max-w-xs">
          <Search className="pointer-events-none absolute left-2.5 top-2.5 h-3.5 w-3.5 text-ink-faint" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t.samples.searchPlaceholder}
            className="w-full rounded-lg border border-leaf/30 bg-paper pl-8 pr-2.5 py-1.5 text-xs text-ink placeholder:text-ink-faint/70 focus:border-leaf focus:outline-hidden focus:ring-1 focus:ring-leaf shadow-2xs"
          />
        </div>

        {/* Dropdown Selector */}
        <div className="relative flex-1">
          <select
            value={currentSample.id}
            onChange={handleSelectChange}
            disabled={loading || sampleLoading || filteredSamples.length === 0}
            className="w-full appearance-none rounded-lg border border-leaf/30 bg-paper px-3 py-1.5 text-xs font-medium text-ink shadow-2xs transition-colors hover:border-leaf/60 focus:border-leaf focus:outline-hidden focus:ring-1 focus:ring-leaf disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
            aria-label={t.samples.title}
          >
            {filteredSamples.length === 0 ? (
              <option value="">কোনো নমুনা পাওয়া যায়নি (No matches)</option>
            ) : (
              filteredSamples.map((s, idx) => {
                const sampleCrop = locale === "bn" ? s.cropBn : s.cropEn;
                const sampleDisease = locale === "bn" ? s.diseaseBn : s.diseaseEn;
                const sampleConfidence = locale === "bn" ? formatNumber(s.confidence) : s.confidence;
                return (
                  <option key={s.id} value={s.id}>
                    #{idx + 1 < 10 ? `0${idx + 1}` : idx + 1} · {sampleCrop} — {sampleDisease} ({sampleConfidence}%)
                  </option>
                );
              })
            )}
          </select>
        </div>

        {/* Load Sample Button */}
        <button
          type="button"
          onClick={() => handleApply(currentSample, false)}
          disabled={loading || sampleLoading}
          className="inline-flex shrink-0 min-h-8.5 items-center justify-center gap-1.5 rounded-lg border border-leaf/30 bg-leaf text-paper px-3 py-1.5 text-xs font-semibold shadow-2xs transition-colors hover:bg-leaf/90 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
        >
          {sampleLoading ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <Sparkles className="h-3.5 w-3.5" />
          )}
          <span>{sampleLoading ? t.samples.loading : t.samples.loadButton}</span>
        </button>

        {/* Instant Test (1-Click Diagnose) */}
        <button
          type="button"
          onClick={() => handleApply(currentSample, true)}
          disabled={loading || sampleLoading}
          className="inline-flex shrink-0 min-h-8.5 items-center justify-center gap-1 rounded-lg border border-ochre/30 bg-ochre/15 text-ochre-deep font-semibold px-2.5 py-1.5 text-xs transition-colors hover:bg-ochre/25 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
          title="তাৎক্ষণিক বেঞ্চমার্ক পরীক্ষা (Zero Latency)"
        >
          <Zap className="h-3 w-3 fill-ochre" />
          <span>{t.samples.diagnoseNow}</span>
        </button>
      </div>

      {/* Selected Specimen Preview Card */}
      <div className="flex flex-wrap items-center justify-between gap-2 text-[11px] text-ink-faint border-t border-leaf/10 pt-2 bg-paper/40 rounded-lg p-2">
        <div className="flex items-center gap-2.5 min-w-0">
          {/* Thumbnail preview */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={currentSample.imageSrc}
            alt={currentSample.id}
            className="h-8 w-8 rounded-md border border-leaf/25 object-cover shrink-0 shadow-2xs"
            loading="lazy"
          />
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 truncate">
              <span className="font-semibold text-leaf">{currentCrop}:</span>
              <span className="font-medium text-ink truncate">{currentDisease}</span>
            </div>
            <div className="text-[10px] text-ink-faint font-mono truncate">
              ID: {currentSample.id}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <span className="text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-semibold">
            BARI/BRRI Verified
          </span>
          <span className="text-[10px] text-ink-soft bg-paper px-2 py-0.5 rounded border border-leaf/20 font-medium">
            {t.samples.confidenceLabel}{" "}
            {locale === "bn" ? formatNumber(currentSample.confidence) : currentSample.confidence}%
          </span>
        </div>
      </div>
    </div>
  );
}
