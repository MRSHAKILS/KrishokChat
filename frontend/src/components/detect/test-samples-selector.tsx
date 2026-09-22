"use client";

import { useState, useMemo, useCallback } from "react";
import {
  Loader2,
  Search,
  ChevronLeft,
  ChevronRight,
  Shuffle,
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

  const currentCrop = locale === "bn" ? currentSample.cropBn : currentSample.cropEn;
  const currentDisease = locale === "bn" ? currentSample.diseaseBn : currentSample.diseaseEn;

  const confidence =
    locale === "bn" ? formatNumber(currentSample.confidence) : String(currentSample.confidence);

  return (
    <div className="space-y-3 rounded-xl border rule bg-paper px-3 py-3 sm:px-4">
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="text-sm font-medium text-ink">{t.samples.title}</p>
          {!compact && (
            <p className="text-xs text-ink-faint">{t.samples.subtitle}</p>
          )}
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

      <div className="flex gap-1 overflow-x-auto text-xs">
        <button
          type="button"
          onClick={() => setActiveCrop("all")}
          className={cn(
            "shrink-0 cursor-pointer rounded-full px-2.5 py-1 transition-colors",
            activeCrop === "all" ? "bg-leaf text-paper" : "text-ink-soft hover:text-ink"
          )}
        >
          {t.samples.allCrops}
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
                "shrink-0 cursor-pointer rounded-full px-2.5 py-1 transition-colors",
                isActive ? "bg-leaf text-paper" : "text-ink-soft hover:text-ink"
              )}
            >
              {label}
            </button>
          );
        })}
      </div>

      <div className="relative">
        <Search className="pointer-events-none absolute left-2.5 top-2.5 h-3.5 w-3.5 text-ink-faint" />
        <input
          type="search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder={t.samples.searchPlaceholder}
          className="w-full rounded-lg border rule bg-paper py-1.5 pl-8 pr-2.5 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-hidden"
        />
      </div>

      {filteredSamples.length === 0 ? (
        <p className="text-xs text-ink-faint">{t.samples.searchPlaceholder}</p>
      ) : (
        <div className="flex items-center gap-3">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            key={currentSample.id}
            src={currentSample.imageSrc}
            alt=""
            className="h-14 w-14 shrink-0 rounded-lg border rule object-cover"
            loading="lazy"
          />
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm text-ink">
              {currentCrop}
              <span className="text-ink-faint"> · </span>
              {currentDisease}
            </p>
            <p className="mt-0.5 text-xs text-ink-faint">
              {t.samples.confidenceLabel} {confidence}%
            </p>
          </div>
        </div>
      )}

      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <button
          type="button"
          onClick={() => handleApply(currentSample, true)}
          disabled={loading || sampleLoading || filteredSamples.length === 0}
          className="inline-flex min-h-9 cursor-pointer items-center gap-2 rounded-lg bg-leaf px-3 text-sm text-paper transition-colors hover:bg-leaf/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {sampleLoading && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
          {sampleLoading ? t.samples.loading : t.samples.diagnoseNow}
        </button>
        <button
          type="button"
          onClick={() => handleApply(currentSample, false)}
          disabled={loading || sampleLoading || filteredSamples.length === 0}
          className="cursor-pointer text-sm text-ink-soft underline-offset-2 hover:text-ink hover:underline disabled:cursor-not-allowed disabled:opacity-50"
        >
          {t.samples.loadButton}
        </button>
      </div>

      <p className="text-[11px] leading-relaxed text-ink-faint">
        {t.samples.reviewerNote}{" "}
        <a
          href="https://huggingface.co/RaiyanKhaan/KrishokTech-Models"
          target="_blank"
          rel="noopener noreferrer"
          className="text-ink-soft underline decoration-ink-faint/40 underline-offset-2 hover:text-ink"
        >
          {t.samples.modelsLink}
        </a>
      </p>
    </div>
  );
}
