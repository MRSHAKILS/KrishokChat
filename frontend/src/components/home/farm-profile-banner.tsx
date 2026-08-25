"use client";

import React from "react";
import Link from "next/link";
import { MapPin, Sprout, ShieldAlert, WifiOff, CheckCircle2, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

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
  return (
    <div className="rounded-2xl border border-leaf/30 bg-gradient-to-r from-leaf/10 via-paper-1 to-leaf/5 p-4 sm:p-5 my-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start sm:items-center gap-3">
          <div className="p-2.5 rounded-xl bg-leaf text-white shrink-0 mt-0.5 sm:mt-0">
            <Sprout className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-bold text-ink text-base">{crop}</span>
              <span className="inline-flex items-center gap-1 text-xs text-ink-soft bg-paper-2 px-2 py-0.5 rounded-md border border-paper-3">
                <MapPin className="w-3 h-3 text-leaf" />
                {district}
              </span>
              <span className="text-xs font-mono font-semibold text-leaf bg-leaf/10 px-2 py-0.5 rounded-md">
                বয়স: {das} দিন
              </span>
            </div>
            <p className="text-xs text-ink-soft mt-1">
              আপনার খামারের প্রোফাইল অনুযায়ী পরামর্শ কাস্টমাইজ করা হয়েছে • অফলাইন তথ্যপ্যাক v{offlinePackVersion} সক্রিয়
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-end sm:self-center">
          <Link href="/account">
            <Button variant="outline" size="sm" className="text-xs h-8 px-3 border-leaf/30 hover:bg-leaf/10 text-leaf">
              <span>প্রোফাইল পরিবর্তন</span>
              <ChevronRight className="w-3.5 h-3.5 ml-1" />
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
