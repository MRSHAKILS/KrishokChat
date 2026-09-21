"use client";

import { useState } from "react";
import { Sparkles, CheckCircle2, Loader2, FlaskConical } from "lucide-react";
import { VERIFIED_TEST_SAMPLES, CROP_GROUPS, type TestSampleInstance } from "@/lib/test-samples";
import { useLanguage } from "@/context/language-context";

interface TestSamplesSelectorProps {
  onSelectSample: (path: string, name: string, cropHint?: string, diseaseHint?: string) => void;
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
  const [selectedId, setSelectedId] = useState<string>(VERIFIED_TEST_SAMPLES[0].id);

  const currentSample = VERIFIED_TEST_SAMPLES.find((s) => s.id === selectedId) ?? VERIFIED_TEST_SAMPLES[0];

  const handleApply = (instance: TestSampleInstance) => {
    setSelectedId(instance.id);
    onSelectSample(instance.imageSrc, `${instance.id}.jpg`, instance.cropHint, instance.disease);
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newId = e.target.value;
    setSelectedId(newId);
    const found = VERIFIED_TEST_SAMPLES.find((s) => s.id === newId);
    if (found) {
      onSelectSample(found.imageSrc, `${found.id}.jpg`, found.cropHint, found.disease);
    }
  };

  const currentCrop = locale === "bn" ? currentSample.cropBn : currentSample.cropEn;
  const currentDisease = locale === "bn" ? currentSample.diseaseBn : currentSample.diseaseEn;

  return (
    <div className="rounded-xl border border-leaf/25 bg-leaf/5 p-3 sm:p-3.5 transition-all space-y-2.5">
      {/* Header bar */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="flex h-6 w-6 items-center justify-center rounded-md bg-leaf/15 text-leaf">
            <FlaskConical className="h-3.5 w-3.5" />
          </span>
          <div>
            <span className="text-xs font-bold text-ink">{t.samples.title}</span>
            {!compact && (
              <span className="hidden sm:inline-block ml-2 text-[11px] text-ink-soft">
                {t.samples.subtitle}
              </span>
            )}
          </div>
        </div>

        <span className="inline-flex items-center gap-1 rounded-full bg-leaf/15 px-2 py-0.5 text-[10px] font-semibold text-leaf border border-leaf/20">
          <CheckCircle2 className="h-2.5 w-2.5" />
          <span>{t.samples.badge}</span>
        </span>
      </div>

      {/* Selector Dropdown & Quick Load Action */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
        <div className="relative flex-1">
          <select
            value={selectedId}
            onChange={handleSelectChange}
            disabled={loading || sampleLoading}
            className="w-full appearance-none rounded-lg border border-leaf/30 bg-paper px-3 py-2 text-xs font-medium text-ink shadow-2xs transition-colors hover:border-leaf/60 focus:border-leaf focus:outline-hidden focus:ring-1 focus:ring-leaf disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
            aria-label={t.samples.title}
          >
            {CROP_GROUPS.map((grp) => {
              const groupSamples = VERIFIED_TEST_SAMPLES.filter((s) => s.crop === grp.crop);
              if (!groupSamples.length) return null;
              const groupLabel = locale === "bn" ? grp.cropBn : grp.cropEn;
              return (
                <optgroup key={grp.crop} label={groupLabel}>
                  {groupSamples.map((s) => {
                    const sampleCrop = locale === "bn" ? s.cropBn : s.cropEn;
                    const sampleDisease = locale === "bn" ? s.diseaseBn : s.diseaseEn;
                    const sampleConfidence = locale === "bn" ? formatNumber(s.confidence) : s.confidence;
                    return (
                      <option key={s.id} value={s.id}>
                        {sampleCrop} — {sampleDisease} ({sampleConfidence}%)
                      </option>
                    );
                  })}
                </optgroup>
              );
            })}
          </select>
        </div>

        <button
          type="button"
          onClick={() => handleApply(currentSample)}
          disabled={loading || sampleLoading}
          className="inline-flex shrink-0 min-h-9 items-center justify-center gap-1.5 rounded-lg border border-leaf/30 bg-leaf text-paper px-3.5 py-2 text-xs font-semibold shadow-xs transition-colors hover:bg-leaf/90 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
        >
          {sampleLoading ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <Sparkles className="h-3.5 w-3.5" />
          )}
          <span>{sampleLoading ? t.samples.loading : t.samples.loadButton}</span>
        </button>
      </div>

      {/* Contextual Pill of Current Selection */}
      <div className="flex flex-wrap items-center justify-between gap-1.5 text-[11px] text-ink-faint border-t border-leaf/10 pt-2">
        <div className="flex items-center gap-1.5 truncate">
          <span className="font-semibold text-leaf">{t.samples.selectedLabel}</span>
          <span className="text-ink truncate">
            {currentCrop} • {currentDisease}
          </span>
        </div>
        <span className="text-[10px] text-ink-soft bg-paper/60 px-1.5 py-0.5 rounded border rule">
          {t.samples.confidenceLabel}{" "}
          {locale === "bn" ? formatNumber(currentSample.confidence) : currentSample.confidence}%
        </span>
      </div>
    </div>
  );
}
