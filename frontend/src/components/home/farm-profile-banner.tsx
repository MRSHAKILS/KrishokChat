"use client";

import React from "react";
import Link from "next/link";
import { MapPin, Sprout, ShieldAlert, WifiOff, CheckCircle2, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLanguage } from "@/context/language-context";
import { numLocale } from "@/lib/bn";

export interface FarmProfileBannerProps {
  crop?: string;
  district?: string;
  das?: number;
  isGuest?: boolean;
  offlinePackVersion?: number;
}

export function FarmProfileBanner({
  crop = "আলু (Potato)",
  district = "বগুড়া",
  das = 45,
  isGuest = true,
  offlinePackVersion = 1,
}: FarmProfileBannerProps) {
  const { locale } = useLanguage();
  const en = locale === "en";
  return (
    <div className="relative overflow-hidden rounded-2xl border border-bone/80 bg-gradient-to-r from-white/95 via-paper to-leaf/5 p-4 sm:p-5 my-4 shadow-[0_4px_20px_-4px_rgba(52,39,23,0.05)] hover:shadow-[0_8px_30px_-6px_rgba(52,39,23,0.09)] transition-all duration-300">
      {/* Soft ambient blur effect */}
      <div className="pointer-events-none absolute -right-12 -top-12 h-36 w-36 rounded-full bg-leaf/10 blur-2xl" />

      <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start sm:items-center gap-3.5">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-leaf text-paper shadow-xs ring-4 ring-leaf/10 mt-0.5 sm:mt-0">
            <Sprout className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-bold text-ink text-base font-display">{crop}</span>
              <span className="inline-flex items-center gap-1 text-xs font-medium text-ink-soft bg-paper-2/90 px-2.5 py-0.5 rounded-lg border border-bone shadow-2xs">
                <MapPin className="w-3 h-3 text-leaf" />
                {district}
              </span>
              <span className="inline-flex items-center text-xs font-mono font-semibold text-leaf bg-leaf/10 px-2.5 py-0.5 rounded-lg border border-leaf/20">
                {en ? `Age: ${numLocale(das, en)} days` : `বয়স: ${das} দিন`}
              </span>
            </div>
            <p className="text-xs text-ink-soft/80 mt-1.5 flex items-center gap-1.5">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-leaf" />
              {en
                ? `Advice customized to your farm profile • Offline data pack v${offlinePackVersion} active`
                : `আপনার খামারের প্রোফাইল অনুযায়ী পরামর্শ কাস্টমাইজ করা হয়েছে • অফলাইন তথ্যপ্যাক v${offlinePackVersion} সক্রিয়`}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-end sm:self-center shrink-0">
          <Link href="/account">
            <Button
              variant="outline"
              size="sm"
              className="h-8.5 rounded-xl border-bone bg-white/90 px-3.5 text-xs font-medium text-ink-soft hover:border-leaf/40 hover:bg-leaf/5 hover:text-leaf transition-all shadow-2xs"
            >
              <span>{en ? "Edit profile" : "প্রোফাইল পরিবর্তন"}</span>
              <ChevronRight className="w-3.5 h-3.5 ml-1 text-leaf" />
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
