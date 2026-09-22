"use client";

import Link from "next/link";
import {
  Play,
  ExternalLink,
  ArrowRight,
} from "lucide-react";

export default function ScreencastPage() {
  return (
    <div className="py-12 md:py-16 space-y-12">
      {/* Header section */}
      <div className="space-y-4 max-w-3xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <Play className="w-3.5 h-3.5 fill-emerald-400" />
          <span>EACL 2027 System Demonstration — Screencast Walkthrough (&lt; 2.5 min)</span>
        </div>
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-foreground">
          KrishokTech: সিস্টেম ডেমোনস্ট্রেশন ও ভিডিও স্ক্রিনকাস্ট
        </h1>
        <p className="text-base sm:text-lg text-muted-foreground leading-relaxed">
          প্রমাণভিত্তিক ও নির্ভরযোগ্য বাংলা কৃষি এআই পরামর্শ ব্যবস্থা। ভাষা মডেলকে একমাত্র সিদ্ধান্তকারী না বানিয়ে
          স্বচ্ছ সিদ্ধান্ত সীমানা, অন-ডিভাইস এজ ভিশন (WASM INT8) এবং মাত্রাগত ভেরিফায়ার দ্বারা নিয়ন্ত্রিত কার্যপ্রবাহ।
        </p>
      </div>

      {/* Primary Video Player Card */}
      <div className="relative rounded-2xl overflow-hidden border border-border/80 bg-card shadow-2xl">
        <div className="aspect-video w-full bg-black/90 relative flex items-center justify-center">
          <iframe
            className="w-full h-full"
            src="https://www.youtube-nocookie.com/embed/a4cibXlvGdQ?rel=0"
            title="KrishokTech EACL 2027 screencast"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          />
        </div>
        
        {/* Under-video action bar */}
        <div className="p-4 sm:p-6 bg-muted/30 border-t border-border/60 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="flex h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs sm:text-sm font-medium text-foreground">
              Official Submission Video (YouTube, 2:24)
            </span>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="https://youtu.be/a4cibXlvGdQ"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 text-xs sm:text-sm font-semibold rounded-lg bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              <span>YouTube-এ দেখুন</span>
            </a>
            <Link
              href="/chat"
              className="inline-flex items-center gap-2 px-4 py-2 text-xs sm:text-sm font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-500 transition-colors shadow-sm"
            >
              <span>লাইভ ইন্টারঅ্যাক্টিভ ডেমো</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      {/* Artifacts & Submission Reference Section */}
      <div className="p-6 sm:p-8 rounded-2xl border border-border bg-card/40 space-y-6">
        <h2 className="text-xl sm:text-2xl font-bold text-foreground">
          গবেষণা ও প্রকাশনা পরিচিতি (Publication Assets)
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            href="/chat"
            className="p-4 rounded-xl border border-border/60 bg-muted/30 hover:border-emerald-500/50 hover:bg-muted/60 transition-all space-y-2 group"
          >
            <div className="font-semibold text-foreground group-hover:text-emerald-400 flex items-center justify-between">
              <span>লাইভ অ্যাডভাইজরি</span>
              <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-emerald-400 transition-transform group-hover:translate-x-1" />
            </div>
            <p className="text-xs text-muted-foreground">বাংলা ভাষার কথোপকথনমূলক এগ্রিকালচারাল আরএজি চ্যাটবট।</p>
          </Link>

          <Link
            href="/detect"
            className="p-4 rounded-xl border border-border/60 bg-muted/30 hover:border-emerald-500/50 hover:bg-muted/60 transition-all space-y-2 group"
          >
            <div className="font-semibold text-foreground group-hover:text-emerald-400 flex items-center justify-between">
              <span>অন-ডিভাইস রোগ নির্ণয়</span>
              <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-emerald-400 transition-transform group-hover:translate-x-1" />
            </div>
            <p className="text-xs text-muted-foreground">ব্রাউজার-ভিত্তিক WASM INT8 ভিশন শনাক্তকরণ।</p>
          </Link>

          <a
            href="https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System"
            target="_blank"
            rel="noopener noreferrer"
            className="p-4 rounded-xl border border-border/60 bg-muted/30 hover:border-emerald-500/50 hover:bg-muted/60 transition-all space-y-2 group"
          >
            <div className="font-semibold text-foreground group-hover:text-emerald-400 flex items-center justify-between">
              <span>সোর্স কোড (GitHub)</span>
              <ExternalLink className="w-4 h-4 text-muted-foreground group-hover:text-emerald-400" />
            </div>
            <p className="text-xs text-muted-foreground">সম্পূর্ণ কোডবেস, পাইপলাইন টেস্ট এবং ডকার কন্টেইনার।</p>
          </a>

          <a
            href="https://huggingface.co/spaces/RaiyanKhaan/KrishokTech"
            target="_blank"
            rel="noopener noreferrer"
            className="p-4 rounded-xl border border-border/60 bg-muted/30 hover:border-emerald-500/50 hover:bg-muted/60 transition-all space-y-2 group"
          >
            <div className="font-semibold text-foreground group-hover:text-emerald-400 flex items-center justify-between">
              <span>হাগিংফেইস স্পেস</span>
              <ExternalLink className="w-4 h-4 text-muted-foreground group-hover:text-emerald-400" />
            </div>
            <p className="text-xs text-muted-foreground">উন্মুক্ত মডেল মিরর, বেঞ্চমার্ক এবং নলেজ নোডসমূহ।</p>
          </a>
        </div>
      </div>
    </div>
  );
}
