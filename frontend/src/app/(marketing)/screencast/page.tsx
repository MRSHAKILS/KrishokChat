"use client";

import Link from "next/link";
import {
  Play,
  ShieldCheck,
  Cpu,
  Layers,
  Download,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  FileText,
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
          <video
            controls
            playsInline
            preload="metadata"
            className="w-full h-full object-contain"
            src="/krishokchat_demo_video.mp4"
          >
            আপনার ব্রাউজার ভিডিও প্লে করতে সমর্থন করে না। অনুগ্রহ করে নিচের লিংক থেকে ডাউনলোড করুন।
          </video>
        </div>
        
        {/* Under-video action bar */}
        <div className="p-4 sm:p-6 bg-muted/30 border-t border-border/60 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="flex h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs sm:text-sm font-medium text-foreground">
              Official Submission Video (HD MP4, 1080p, 150s cap compliant)
            </span>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="/krishokchat_demo_video.mp4"
              download="krishoktech_eacl_screencast.mp4"
              className="inline-flex items-center gap-2 px-4 py-2 text-xs sm:text-sm font-semibold rounded-lg bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>ডাউনলোড MP4</span>
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

      {/* Timestamped Architecture Breakdown */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
          <Layers className="w-6 h-6 text-emerald-500" />
          <span>স্ক্রিনকাস্ট ভিডিও পর্যায়ক্রম ও বৈশিষ্ট্য সূচী</span>
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* Stage 1 */}
          <div className="p-5 rounded-xl border border-border/70 bg-card/60 hover:bg-card transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-red-500/15 text-red-400 border border-red-500/25">
                0:00 - 0:32
              </span>
              <ShieldCheck className="w-4 h-4 text-red-400" />
            </div>
            <h3 className="font-semibold text-foreground text-base">T0 Deterministic Precheck & 16123 Referral</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              নিষিদ্ধ বিষাক্ত উপাদান (যেমন প্যারা কোয়াট) অথবা তীব্র কীটনাশক বিপদের ক্ষেত্রে 0.32 ms-এ LLM সার্চ আটকে সরাসরি সরকারি কৃষি কল সেন্টারে (16123) রেফারেল।
            </p>
          </div>

          {/* Stage 2 */}
          <div className="p-5 rounded-xl border border-border/70 bg-card/60 hover:bg-card transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-blue-500/15 text-blue-400 border border-blue-500/25">
                0:32 - 0:58
              </span>
              <AlertTriangle className="w-4 h-4 text-blue-400" />
            </div>
            <h3 className="font-semibold text-foreground text-base">C1: Pre-Retrieval Halt on Empty Crop</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              কৃষকের প্রশ্নে ফসলের নাম উল্লেখ না থাকলে অনুমানভিত্তিক ঝুঁকিপূর্ণ উত্তর না দিয়ে ইন্টারঅ্যাক্টিভ কুইক-রিপ্লাই চিপস উপস্থাপন (ধান, আলু, গম)।
            </p>
          </div>

          {/* Stage 3 */}
          <div className="p-5 rounded-xl border border-border/70 bg-card/60 hover:bg-card transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/25">
                0:58 - 1:28
              </span>
              <Cpu className="w-4 h-4 text-emerald-400" />
            </div>
            <h3 className="font-semibold text-foreground text-base">C2: Edge WASM INT8 Perception & Crop Fencing</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              ছবি ক্লাউডে না পাঠিয়ে ব্রাউজারে অন-ডিভাইস INT8 ওএনএনএক্স মডেলের মাধ্যমে নির্ভুল ফসল ও রোগ শনাক্তকরণ এবং সার্চ ফলাফলকে ওই নির্দিষ্ট ফসলে আবদ্ধ রাখা।
            </p>
          </div>

          {/* Stage 4 */}
          <div className="p-5 rounded-xl border border-border/70 bg-card/60 hover:bg-card transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-amber-500/15 text-amber-400 border border-amber-500/25">
                1:28 - 1:52
              </span>
              <AlertTriangle className="w-4 h-4 text-amber-400" />
            </div>
            <h3 className="font-semibold text-foreground text-base">Text-Image Contradiction Gating</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              লিখিত বর্ণনা ও ছবির মধ্যে অমিল দেখা দিলে (যেমন আলুর টেক্সট কিন্তু ধানের পাতা) সতর্কবার্তা ব্যাজ প্রদর্শন করে ভুল চিকিৎসা প্রতিরোধ।
            </p>
          </div>

          {/* Stage 5 */}
          <div className="p-5 rounded-xl border border-border/70 bg-card/60 hover:bg-card transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-purple-500/15 text-purple-400 border border-purple-500/25">
                1:52 - 2:15
              </span>
              <CheckCircle2 className="w-4 h-4 text-purple-400" />
            </div>
            <h3 className="font-semibold text-foreground text-base">C3: Grounded Advisory & Dosage Verification</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              BARI ও BRRI অনুমোদিত নির্দেশিকা অনুযায়ী মাত্রাগত মান যাচাই। অনিরাপদ বা অতিরিক্ত মাত্রার রাসায়নিক প্রেসক্রিপশন প্রদর্শন আটকে নিরাপদ ডোজ সুরক্ষা।
            </p>
          </div>

          {/* Stage 6 */}
          <div className="p-5 rounded-xl border border-border/70 bg-card/60 hover:bg-card transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-teal-500/15 text-teal-400 border border-teal-500/25">
                2:15 - 2:30
              </span>
              <FileText className="w-4 h-4 text-teal-400" />
            </div>
            <h3 className="font-semibold text-foreground text-base">Constrained Delivery: SMS & Offline Mode</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              ইন্টারনেট সংযোগবিহীন এলাকার জন্য অফলাইন ক্যাশ কার্ড এবং ফিচার ফোনের জন্য ১৬০ ক্যারেক্টার সীমিত এসএমএস প্রেসক্রিপশন কম্প্রেসর।
            </p>
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
