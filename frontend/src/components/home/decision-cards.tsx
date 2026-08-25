"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Calendar,
  Camera,
  MessageSquare,
  CloudRain,
  ArrowRight,
  Sparkles,
  Volume2,
  CheckCircle2,
  AlertTriangle,
  Smartphone,
  ShieldCheck,
} from "lucide-react";
import { ProvenanceBadge } from "@/components/provenance/provenance-badge";
import { Button } from "@/components/ui/button";

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
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const handleSpeak = (text: string) => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "bn-BD";
    utterance.onstart = () => setIsPlayingAudio(true);
    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 my-6">
      {/* 1. Stage Tasks Card */}
      <div className="flex flex-col justify-between p-5 lg:p-6 rounded-2xl border border-leaf/20 bg-gradient-to-br from-paper-1 to-leaf/5 shadow-sm hover:border-leaf/40 transition-all">
        <div>
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-leaf/10 text-leaf">
                <Calendar className="w-5 h-5" />
              </div>
              <span className="font-semibold text-ink text-sm">ফসলের বৃদ্ধি পর্যায় ও করণীয়</span>
            </div>
            <ProvenanceBadge kind="templated_advisory" />
          </div>

          <div className="my-2">
            <div className="flex items-baseline justify-between">
              <h3 className="text-lg font-bold text-ink">{stageName}</h3>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-leaf/10 text-leaf font-medium">
                {farmDas} দিন (DAS)
              </span>
            </div>
            <p className="text-sm text-ink-soft mt-2 leading-relaxed">
              {stageAction}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between gap-2 pt-4 mt-2 border-t border-paper-3/50">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => handleSpeak(`${stageName}। ${stageAction}`)}
            className="text-xs font-medium text-ink-soft hover:text-leaf gap-1.5 h-8 px-2.5"
          >
            <Volume2 className={`w-3.5 h-3.5 ${isPlayingAudio ? "text-leaf animate-pulse" : ""}`} />
            <span>{isPlayingAudio ? "পড়া হচ্ছে..." : "শুনে নিন"}</span>
          </Button>

          <Link href="/chat" className="inline-flex items-center text-xs font-semibold text-leaf hover:underline gap-1">
            <span>বিস্তারিত জানুন</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* 2. Photo Diagnosis Card */}
      <div className="flex flex-col justify-between p-5 lg:p-6 rounded-2xl border border-paper-3 bg-gradient-to-br from-paper-1 to-paper-2/40 shadow-sm hover:border-leaf/40 transition-all">
        <div>
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                <Camera className="w-5 h-5" />
              </div>
              <span className="font-semibold text-ink text-sm">রোগ ও পোকা নির্ণয়</span>
            </div>
            <ProvenanceBadge kind="on_device" />
          </div>

          <div className="my-2">
            <h3 className="text-lg font-bold text-ink">ফসলের ছবি আপলোড করুন</h3>
            <p className="text-sm text-ink-soft mt-2 leading-relaxed">
              মোবাইলে ইন্টারনেট ছাড়াই চোখের পলকে (৫০ মিলি-সেকেন্ডে) রোগ শনাক্ত করুন। ছবি অস্পষ্ট হলে স্বয়ংক্রিয়ভাবে সার্ভারে যাচাই হবে।
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between gap-2 pt-4 mt-2 border-t border-paper-3/50">
          <div className="flex items-center gap-1.5 text-xs text-ink-soft">
            <Smartphone className="w-3.5 h-3.5 text-emerald-600" />
            <span>অন-ডিভাইস এআই মডেল</span>
          </div>

          <Link href="/detect">
            <Button size="sm" className="bg-leaf hover:bg-leaf-dark text-white text-xs font-medium h-8 px-3 gap-1">
              <span>ক্যামেরা খুলুন</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Button>
          </Link>
        </div>
      </div>

      {/* 3. Advisory Chat Card */}
      <div className="flex flex-col justify-between p-5 lg:p-6 rounded-2xl border border-paper-3 bg-gradient-to-br from-paper-1 to-paper-2/40 shadow-sm hover:border-leaf/40 transition-all">
        <div>
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
                <MessageSquare className="w-5 h-5" />
              </div>
              <span className="font-semibold text-ink text-sm">কৃষি প্রশ্নোত্তর ও সার সুপারিশ</span>
            </div>
            <ProvenanceBadge kind="structured_fact" />
          </div>

          <div className="my-2">
            <h3 className="text-lg font-bold text-ink">যেকোনো কৃষি প্রশ্ন করুন</h3>
            <p className="text-sm text-ink-soft mt-2 leading-relaxed">
              সরাসরি মুখে বলে বা লিখে প্রশ্ন করুন। সরকারি গবেষণাগার অনুমোদিত সঠিক প্রয়োগমাত্রা ও আইপিএম সমাধান জানুন।
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between gap-2 pt-4 mt-2 border-t border-paper-3/50">
          <div className="flex items-center gap-1.5 text-xs text-ink-soft">
            <ShieldCheck className="w-3.5 h-3.5 text-leaf" />
            <span>১৬১২৩ কল সেন্টার লিঙ্কড</span>
          </div>

          <Link href="/chat">
            <Button variant="outline" size="sm" className="text-xs font-medium h-8 px-3 gap-1">
              <span>পরামর্শ নিন</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Button>
          </Link>
        </div>
      </div>

      {/* 4. Weather & Blight Risk Card */}
      <div className="flex flex-col justify-between p-5 lg:p-6 rounded-2xl border border-sky-500/20 bg-gradient-to-br from-paper-1 to-sky-500/5 shadow-sm hover:border-sky-500/40 transition-all">
        <div>
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
                <CloudRain className="w-5 h-5" />
              </div>
              <span className="font-semibold text-ink text-sm">আবহাওয়া ও বালাই সতর্কতা</span>
            </div>
            <ProvenanceBadge kind="forecast_derived" />
          </div>

          <div className="my-2">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-ink">{weatherRiskDistrict} জেলা বালাই পূর্বাভাস</h3>
              <span className="text-xs font-medium px-2 py-0.5 rounded bg-amber-500/15 text-amber-700 dark:text-amber-400">
                সতর্কবার্তা
              </span>
            </div>
            <p className="text-sm text-ink-soft mt-2 leading-relaxed">
              আবহাওয়া পূর্বাভাস অনুযায়ী আগামী ৩ দিন ঠাণ্ডা ও আর্দ্র আবহাওয়ার কারণে আলুর নাবি ধসা রোগের ঝুঁকি রয়েছে। অনুমোদিত ছত্রাকনাশক স্প্রে করুন।
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between gap-2 pt-4 mt-2 border-t border-paper-3/50">
          <div className="flex items-center gap-1.5 text-xs text-ink-soft">
            <CheckCircle2 className="w-3.5 h-3.5 text-sky-600" />
            <span>RIMES আবহাওয়া উপাত্ত</span>
          </div>

          <Link href="/analytics" className="inline-flex items-center text-xs font-semibold text-sky-600 dark:text-sky-400 hover:underline gap-1">
            <span>পূর্বাভাস দেখুন</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
