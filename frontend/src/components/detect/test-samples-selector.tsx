"use client";

import { useState } from "react";
import { Sparkles, CheckCircle2, ChevronRight, Loader2, FlaskConical } from "lucide-react";
import { VERIFIED_TEST_SAMPLES, CROP_GROUPS, type TestSampleInstance } from "@/lib/test-samples";

interface TestSamplesSelectorProps {
  onSelectSample: (path: string, name: string, cropHint?: string) => void;
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
  const [selectedId, setSelectedId] = useState<string>(VERIFIED_TEST_SAMPLES[0].id);

  const currentSample = VERIFIED_TEST_SAMPLES.find((s) => s.id === selectedId) ?? VERIFIED_TEST_SAMPLES[0];

  const handleApply = (instance: TestSampleInstance) => {
    setSelectedId(instance.id);
    onSelectSample(instance.imageSrc, `${instance.id}.jpg`, instance.cropHint);
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newId = e.target.value;
    setSelectedId(newId);
    const found = VERIFIED_TEST_SAMPLES.find((s) => s.id === newId);
    if (found) {
      onSelectSample(found.imageSrc, `${found.id}.jpg`, found.cropHint);
    }
  };

  return (
    <div className="rounded-xl border border-leaf/25 bg-leaf/5 p-3 sm:p-3.5 transition-all space-y-2.5">
      {/* Header bar */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="flex h-6 w-6 items-center justify-center rounded-md bg-leaf/15 text-leaf">
            <FlaskConical className="h-3.5 w-3.5" />
          </span>
          <div>
            <span className="text-xs font-bold text-ink">রিভিউয়ার টেস্ট সেট (Reviewer Samples)</span>
            {!compact && (
              <span className="hidden sm:inline-block ml-2 text-[11px] text-ink-soft">
                যাচাইকৃত ২১টি উচ্চ-নির্ভুলতার নমুনা
              </span>
            )}
          </div>
        </div>

        <span className="inline-flex items-center gap-1 rounded-full bg-leaf/15 px-2 py-0.5 text-[10px] font-semibold text-leaf border border-leaf/20">
          <CheckCircle2 className="h-2.5 w-2.5" />
          <span>২১ টি ভেরিফাইড কেস</span>
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
            aria-label="ফসল ও রোগের টেস্ট সেট নমুনা বেছে নিন"
          >
            {CROP_GROUPS.map((grp) => {
              const groupSamples = VERIFIED_TEST_SAMPLES.filter((s) => s.crop === grp.crop);
              if (!groupSamples.length) return null;
              return (
                <optgroup key={grp.crop} label={grp.cropBn}>
                  {groupSamples.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.cropBn} — {s.diseaseBn} ({s.confidence}%)
                    </option>
                  ))}
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
          <span>{sampleLoading ? "লোড হচ্ছে…" : "নমুনা লোড করুন"}</span>
        </button>
      </div>

      {/* Contextual Pill of Current Selection */}
      <div className="flex flex-wrap items-center justify-between gap-1.5 text-[11px] text-ink-faint border-t border-leaf/10 pt-2">
        <div className="flex items-center gap-1.5 truncate">
          <span className="font-semibold text-leaf">নির্বাচিত:</span>
          <span className="text-ink truncate">{currentSample.cropBn} • {currentSample.diseaseBn}</span>
        </div>
        <span className="text-[10px] text-ink-soft bg-paper/60 px-1.5 py-0.5 rounded border rule">
          মডেল প্রিডিকশন: {currentSample.confidence}%
        </span>
      </div>
    </div>
  );
}
