"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Calendar,
  Camera,
  MessageSquare,
  CloudRain,
  ArrowRight,
  Volume2,
  CheckCircle2,
  Smartphone,
  ShieldCheck,
} from "lucide-react";
import { ProvenanceBadge } from "@/components/provenance/provenance-badge";
import { Button } from "@/components/ui/button";
import { useLanguage } from "@/context/language-context";
import { numLocale } from "@/lib/bn";

export interface DecisionCardsProps {
  farmCrop?: string;
  farmDistrict?: string;
  farmDas?: number;
  stageName?: string;
  stageAction?: string;
  weatherRiskDistrict?: string;
  weatherRiskLevel?: "low" | "watch" | "high";
  isOffline?: boolean;
}

export function DecisionCards({
  farmCrop = "আলু (Potato)",
  farmDistrict = "বগুড়া",
  farmDas = 45,
  stageName = "কন্দ বৃদ্ধি পর্যায় (Tuber Bulking)",
  stageAction = "কন্দ গঠনের এই সময়ে মাটিতে পর্যাপ্ত রস নিশ্চিত করতে হালকা সেচ দিন এবং নাবি ধসা রোগ নিয়মিত পর্যবেক্ষণ করুন।",
  weatherRiskDistrict = "বগুড়া",
  weatherRiskLevel = "watch",
  isOffline = false,
}: DecisionCardsProps) {
  const { locale } = useLanguage();
  const en = locale === "en";
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const handleSpeak = (text: string) => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = en ? "en-US" : "bn-BD";
    utterance.onstart = () => setIsPlayingAudio(true);
    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 my-6">
      {/* 1. Stage Tasks Card */}
      <div className="surface-lift group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-bone/80 bg-gradient-to-br from-white/95 via-paper to-leaf/[0.04] p-5 lg:p-6 shadow-[0_4px_20px_-4px_rgba(52,39,23,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(52,39,23,0.11)] hover:border-leaf/40 transition-all duration-300">
        <div className="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-leaf/10 blur-2xl" />

        <div className="relative z-10">
          <div className="flex items-center justify-between gap-2 mb-3.5">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-leaf/10 text-leaf ring-1 ring-leaf/15">
                <Calendar className="w-4.5 h-4.5" />
              </div>
              <span className="font-semibold text-ink text-sm">{en ? "Crop growth stage and what to do" : "ফসলের বৃদ্ধি পর্যায় ও করণীয়"}</span>
            </div>
            <ProvenanceBadge kind="templated_advisory" />
          </div>

          <div className="my-2.5">
            <div className="flex items-baseline justify-between gap-2 flex-wrap">
              <h3 className="text-lg font-bold font-display text-ink">{stageName}</h3>
              <span className="text-xs font-mono font-semibold px-2.5 py-0.5 rounded-lg bg-leaf/10 text-leaf border border-leaf/20">
                {en ? `Day ${numLocale(farmDas, en)} (DAS)` : `${farmDas} দিন (DAS)`}
              </span>
            </div>
            <p className="text-sm text-ink-soft/90 mt-2 leading-relaxed">
              {stageAction}
            </p>
          </div>
        </div>

        <div className="relative z-10 flex items-center justify-between gap-2 pt-4 mt-3 border-t border-bone/80">
          <button
            type="button"
            onClick={() => handleSpeak(en ? `${stageName}. ${stageAction}` : `${stageName}। ${stageAction}`)}
            className="control-press inline-flex items-center gap-1.5 rounded-xl border border-bone bg-white/90 px-3 py-1.5 text-xs font-medium text-ink-soft hover:border-leaf/40 hover:bg-leaf/5 hover:text-leaf transition-all shadow-2xs"
          >
            <Volume2 className={`w-3.5 h-3.5 text-leaf ${isPlayingAudio ? "animate-pulse" : ""}`} />
            <span>{isPlayingAudio ? (en ? "Reading..." : "পড়া হচ্ছে...") : (en ? "Listen" : "শুনে নিন")}</span>
          </button>

          <Link
            href="/chat"
            className="control-press group/link inline-flex items-center gap-1 text-xs font-semibold text-leaf hover:text-leaf-2 transition-colors"
          >
            <span>{en ? "Learn more" : "বিস্তারিত জানুন"}</span>
            <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover/link:translate-x-0.5" />
          </Link>
        </div>
      </div>

      {/* 2. Photo Diagnosis Card */}
      <div className="surface-lift group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-bone/80 bg-gradient-to-br from-white/95 via-paper to-emerald-600/[0.04] p-5 lg:p-6 shadow-[0_4px_20px_-4px_rgba(52,39,23,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(52,39,23,0.11)] hover:border-leaf/40 transition-all duration-300">
        <div className="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-emerald-500/10 blur-2xl" />

        <div className="relative z-10">
          <div className="flex items-center justify-between gap-2 mb-3.5">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-700 ring-1 ring-emerald-500/15">
                <Camera className="w-4.5 h-4.5" />
              </div>
              <span className="font-semibold text-ink text-sm">{en ? "Disease and pest diagnosis" : "রোগ ও পোকা নির্ণয়"}</span>
            </div>
            <ProvenanceBadge kind="on_device" />
          </div>

          <div className="my-2.5">
            <h3 className="text-lg font-bold font-display text-ink">{en ? "Upload a crop photo" : "ফসলের ছবি আপলোড করুন"}</h3>
            <p className="text-sm text-ink-soft/90 mt-2 leading-relaxed">
              {en ? "Diagnose in the blink of an eye (~50 ms) on your phone, no internet needed. Unclear photos are automatically re-checked on the server." : "মোবাইলে ইন্টারনেট ছাড়াই চোখের পলকে (৫০ মিলি-সেকেন্ডে) রোগ শনাক্ত করুন। ছবি অস্পষ্ট হলে স্বয়ংক্রিয়ভাবে সার্ভারে যাচাই হবে।"}
            </p>
          </div>
        </div>

        <div className="relative z-10 flex items-center justify-between gap-2 pt-4 mt-3 border-t border-bone/80">
          <div className="flex items-center gap-1.5 text-xs text-ink-soft/90">
            <Smartphone className="w-3.5 h-3.5 text-emerald-700" />
            <span className="font-medium">{en ? "On-device AI model" : "অন-ডিভাইস এআই মডেল"}</span>
          </div>

          <Link href="/detect">
            <Button
              size="sm"
              className="control-press group/btn inline-flex items-center gap-1.5 rounded-xl bg-leaf hover:bg-leaf-2 text-paper text-xs font-semibold h-8.5 px-3.5 shadow-sm transition-all"
            >
              <span>{en ? "Open camera" : "ক্যামেরা খুলুন"}</span>
              <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover/btn:translate-x-0.5" />
            </Button>
          </Link>
        </div>
      </div>

      {/* 3. Advisory Chat Card */}
      <div className="surface-lift group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-bone/80 bg-gradient-to-br from-white/95 via-paper to-ochre/[0.04] p-5 lg:p-6 shadow-[0_4px_20px_-4px_rgba(52,39,23,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(52,39,23,0.11)] hover:border-ochre/50 transition-all duration-300">
        <div className="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-ochre/10 blur-2xl" />

        <div className="relative z-10">
          <div className="flex items-center justify-between gap-2 mb-3.5">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-ochre/10 text-ochre ring-1 ring-ochre/20">
                <MessageSquare className="w-4.5 h-4.5" />
              </div>
              <span className="font-semibold text-ink text-sm">{en ? "Agri Q&A and fertilizer recommendations" : "কৃষি প্রশ্নোত্তর ও সার সুপারিশ"}</span>
            </div>
            <ProvenanceBadge kind="structured_fact" />
          </div>

          <div className="my-2.5">
            <h3 className="text-lg font-bold font-display text-ink">{en ? "Ask any farming question" : "যেকোনো কৃষি প্রশ্ন করুন"}</h3>
            <p className="text-sm text-ink-soft/90 mt-2 leading-relaxed">
              {en ? "Ask by voice or by typing. Get correct dosages and IPM solutions approved by government research bodies." : "সরাসরি মুখে বলে বা লিখে প্রশ্ন করুন। সরকারি গবেষণাগার অনুমোদিত সঠিক প্রয়োগমাত্রা ও আইপিএম সমাধান জানুন।"}
            </p>
          </div>
        </div>

        <div className="relative z-10 flex items-center justify-between gap-2 pt-4 mt-3 border-t border-bone/80">
          <div className="flex items-center gap-1.5 text-xs text-ink-soft/90">
            <ShieldCheck className="w-3.5 h-3.5 text-leaf" />
            <span className="font-medium">{en ? "Linked to the 16123 call center" : "১৬১২৩ কল সেন্টার লিঙ্কড"}</span>
          </div>

          <Link href="/chat">
            <Button
              variant="outline"
              size="sm"
              className="control-press group/btn inline-flex items-center gap-1.5 rounded-xl border-bone bg-white/90 px-3.5 h-8.5 text-xs font-semibold text-ink-soft hover:border-leaf/40 hover:bg-leaf/5 hover:text-leaf transition-all shadow-2xs"
            >
              <span>{en ? "Get advice" : "পরামর্শ নিন"}</span>
              <ArrowRight className="w-3.5 h-3.5 text-leaf transition-transform group-hover/btn:translate-x-0.5" />
            </Button>
          </Link>
        </div>
      </div>

      {/* 4. Weather & Blight Risk Card */}
      <div className="surface-lift group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-bone/80 bg-gradient-to-br from-white/95 via-paper to-sky-600/[0.04] p-5 lg:p-6 shadow-[0_4px_20px_-4px_rgba(52,39,23,0.06)] hover:shadow-[0_12px_32px_-6px_rgba(52,39,23,0.11)] hover:border-sky-500/40 transition-all duration-300">
        <div className="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-sky-500/10 blur-2xl" />

        <div className="relative z-10">
          <div className="flex items-center justify-between gap-2 mb-3.5">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-sky-500/10 text-sky-700 ring-1 ring-sky-500/20">
                <CloudRain className="w-4.5 h-4.5" />
              </div>
              <span className="font-semibold text-ink text-sm">{en ? "Weather and blight alert" : "আবহাওয়া ও বালাই সতর্কতা"}</span>
            </div>
            <ProvenanceBadge kind="forecast_derived" />
          </div>

          <div className="my-2.5">
            <div className="flex items-center justify-between gap-2 flex-wrap">
              <h3 className="text-lg font-bold font-display text-ink">{weatherRiskDistrict} {en ? "District Blight Forecast" : "জেলা বালাই পূর্বাভাস"}</h3>
              <span className="text-xs font-medium px-2.5 py-0.5 rounded-lg border border-ochre/30 bg-ochre/10 text-ochre">
                {en ? "Alert" : "সতর্কবার্তা"}
              </span>
            </div>
            <p className="text-sm text-ink-soft/90 mt-2 leading-relaxed">
              {en ? "The forecast calls for cold, humid weather over the next 3 days, raising late blight risk for potatoes. Spray an approved fungicide." : "আবহাওয়া পূর্বাভাস অনুযায়ী আগামী ৩ দিন ঠাণ্ডা ও আর্দ্র আবহাওয়ার কারণে আলুর নাবি ধসা রোগের ঝুঁকি রয়েছে। অনুমোদিত ছত্রাকনাশক স্প্রে করুন।"}
            </p>
          </div>
        </div>

        <div className="relative z-10 flex items-center justify-between gap-2 pt-4 mt-3 border-t border-bone/80">
          <div className="flex items-center gap-1.5 text-xs text-ink-soft/90">
            <CheckCircle2 className="w-3.5 h-3.5 text-sky-600" />
            <span className="font-medium">{en ? "RIMES weather data" : "RIMES আবহাওয়া উপাত্ত"}</span>
          </div>

          <Link
            href="/analytics"
            className="control-press group/link inline-flex items-center gap-1 text-xs font-semibold text-sky-700 hover:text-sky-800 dark:text-sky-400 hover:underline"
          >
            <span>{en ? "View forecast" : "পূর্বাভাস দেখুন"}</span>
            <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover/link:translate-x-0.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
