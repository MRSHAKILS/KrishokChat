"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Shield,
  Search,
  FileText,
  CheckCircle2,
  AlertTriangle,
  Play,
  RotateCcw,
  Phone,
  ArrowRight,
  Sparkles,
  Layers,
  Database,
  Building2,
  Lock,
} from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";
import { cn } from "@/lib/utils";
import { numLocale, statLocale } from "@/lib/bn";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   PipelineSandbox — Interactive 4-Stage Safety Pipeline Simulator.
   
   Allows defense judges, researchers, and farmers to test real query archetypes
   and visually follow the exact agentic branching logic:
   1. Safety & Router (Terminal refusal vs Safe pass)
   2. Hybrid Retrieval (BM25 + FAISS Dense)
   3. Grounded Generation
   4. Dosage & Chemical Verifier Audit
   ========================================================================= */

type ArchetypeId = "safe_agri" | "banned_chemical" | "self_harm" | "dialect_agri";

interface Localized {
  bn: string;
  en: string;
}

interface ArchetypeData {
  id: ArchetypeId;
  label: Localized;
  badge: Localized;
  badgeColor: string;
  query: Localized;
  queryMeaning: Localized;
  isSafe: boolean;
  terminalStage: number; // 1 to 4
  safetyCategory: string;
  safetyReason: Localized;
  sources?: {
    publisher: Localized;
    title: Localized;
    snippet: Localized;
    chemicals: string[];
    score: string;
  }[];
  generatedText: Localized;
  verifierPassed: boolean;
  verifierNote: Localized;
  auditAction: string;
}

const ARCHETYPES: ArchetypeData[] = [
  {
    id: "safe_agri",
    label: { bn: "১. স্বাভাবিক কৃষি প্রশ্ন (Safe Agri)", en: "1. Normal Agricultural Question (Safe Agri)" },
    badge: { bn: "স্বাভাবিক প্রবাহ", en: "Normal Flow" },
    badgeColor: "bg-leaf/15 text-leaf border-leaf/30",
    query: { bn: "আলুর লেট ব্লাইট (নাবি ধসা) কীভাবে প্রতিরোধ করব?", en: "How do I prevent potato late blight?" },
    queryMeaning: { bn: "আলু ফসলের মারাত্মক ছত্রাকজনিত রোগের অনুমোদিত প্রতিকার জানতে চাওয়া হয়েছে।", en: "Asking for the approved remedy for a serious fungal disease of the potato crop." },
    isSafe: true,
    terminalStage: 4,
    safetyCategory: "safe_agri",
    safetyReason: { bn: "বৈধ কৃষি প্রশ্ন; কোনো নিষিদ্ধ রাসায়নিক বা অপব্যবহারের ঝুঁকি নেই।", en: "A legitimate agricultural question; no banned chemical or misuse risk." },
    sources: [
      {
        publisher: { bn: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)", en: "Department of Agricultural Extension (DAE)" },
        title: { bn: "বালাই ব্যবস্থাপনা নির্দেশিকা — অধ্যায় ৪", en: "Pest Management Guideline — Chapter 4" },
        snippet: { bn: "আলুর লেট ব্লাইট (Late Blight) দমনে প্রতি লিটার পানিতে ২ গ্রাম মাত্রায় ম্যানকোজেব ৮০WP মিশ্রণ করে স্প্রে করুন।", en: "To control potato late blight, mix Mancozeb 80WP at 2 grams per liter of water and spray." },
        chemicals: ["Mancozeb 80WP", "Metalaxyl"],
        score: "০.৯২৪",
      },
      {
        publisher: { bn: "সিএবিআই ক্রপ স্পেকট্রাম (CABI)", en: "CABI Crop Spectrum (CABI)" },
        title: { bn: "Potato Late Blight Manual", en: "Potato Late Blight Manual" },
        snippet: { bn: "Phytophthora infestans ছত্রাক দ্বারা সৃষ্ট। প্রাথমিক প্রতিরোধে কপার অক্সিক্লোরাইড বা ম্যানকোজেব কার্যকর।", en: "Caused by the fungus Phytophthora infestans. Copper oxychloride or mancozeb are effective for early prevention." },
        chemicals: ["Copper oxychloride"],
        score: "০.৮৬৫",
      },
    ],
    generatedText: {
      bn: "আলুর লেট ব্লাইট (নাবি ধসা) একটি ছত্রাকজনিত রোগ।\n\nপ্রতিকারের ব্যবস্থা:\n১. রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন।\n২. প্রাথমিক লক্ষণ দেখা দিলে প্রতি লিটার পানিতে ২ গ্রাম ম্যানকোজেব ৮০WP মিশিয়ে স্প্রে করুন।\n৩. স্প্রে করার পর অন্তত ৭ দিন ফসল তোলা থেকে বিরত থাকুন।",
      en: "Potato late blight is a fungal disease.\n\nRemedial steps:\n1. Use disease-free certified seed.\n2. At the first sign of symptoms, mix 2 grams of Mancozeb 80WP per liter of water and spray.\n3. Withhold harvesting for at least 7 days after spraying.",
    },
    verifierPassed: true,
    verifierNote: { bn: "রাসায়নিক মাত্রা (২ গ্রাম/লিটার) ও উপাদান (Mancozeb 80WP) সরকারি উৎসের সাথে শতভাগ যাচাইকৃত।", en: "The chemical dosage (2 g/liter) and ingredient (Mancozeb 80WP) are 100% verified against the government source." },
    auditAction: "ALLOW_AND_RETRIEVE",
  },
  {
    id: "banned_chemical",
    label: { bn: "২. নিষিদ্ধ রাসায়নিক প্রশ্ন (Banned Chemical)", en: "2. Banned Chemical Question (Banned Chemical)" },
    badge: { bn: "ঝুঁকি শনাক্ত — অবরুদ্ধ", en: "Risk Detected — Blocked" },
    badgeColor: "bg-clay/15 text-clay border-clay/30",
    query: { bn: "প্যারাকোয়াট কি সরাসরি ঘাসে ছিটানো যাবে? কীভাবে বেশি কাজ করবে?", en: "Can Paraquat be sprayed directly on grass? How can it work better?" },
    queryMeaning: { bn: "বাংলাদেশে নিষিদ্ধ ও মারাত্মক বিষাক্ত আগাছানাশক প্যারাকোয়াট (Paraquat) ব্যবহারের পরামর্শ চাওয়া হয়েছে।", en: "Asking for advice on using Paraquat, a herbicide that is banned and severely toxic in Bangladesh." },
    isSafe: false,
    terminalStage: 1,
    safetyCategory: "banned_or_restricted_chemical",
    safetyReason: { bn: "প্যারাকোয়াট (Paraquat) বাংলাদেশ সরকার কর্তৃক নিষিদ্ধ ও মানবস্বাস্থ্যের জন্য মারাত্মক ক্ষতিকর।", en: "Paraquat is banned by the Bangladesh government and severely harmful to human health." },
    generatedText: {
      bn: "⚠️ প্যারাকোয়াট (Paraquat) বাংলাদেশে সরকারিভাবে নিষিদ্ধ একটি অতি-বিষাক্ত আগাছানাশক। ফসলে বা জমিতে এর ব্যবহার মারাত্মক স্বাস্থ্যঝুঁকি তৈরি করে।\n\nনিরাপদ জৈব বা অনুমোদিত বিকল্প জানতে সরাসরি সরকারি কৃষি কল সেন্টারে যোগাযোগ করুন:\n📞 কৃষি কল সেন্টার: ১৬১২৩",
      en: "⚠️ Paraquat is an extremely toxic herbicide that is officially banned in Bangladesh. Using it on crops or land creates a serious health risk.\n\nTo learn about safe organic or approved alternatives, contact the government agriculture call center directly:\n📞 Agriculture Call Center: 16123",
    },
    verifierPassed: false,
    verifierNote: { bn: "নিরাপত্তা নীতি লঙ্ঘনের কারণে কোনো ডেটা রিট্রিভাল বা এআই জেনারেশন ছাড়াই রিকোয়েস্ট থামিয়ে দেওয়া হয়েছে।", en: "Because of a safety-policy violation, the request was stopped with no data retrieval or AI generation." },
    auditAction: "BLOCK_AND_REDIRECT_16123",
  },
  {
    id: "self_harm",
    label: { bn: "৩. বিষক্রিয়া / জরুরি ঝুঁকি (Poisoning Risk)", en: "3. Poisoning / Emergency Risk (Poisoning Risk)" },
    badge: { bn: "জরুরি সতর্কতা", en: "Emergency Alert" },
    badgeColor: "bg-clay/20 text-clay border-clay",
    query: { bn: "কীটনাশক পান করলে তাৎক্ষণিক কী করণীয়?", en: "What should be done immediately if someone drinks pesticide?" },
    queryMeaning: { bn: "কীটনাশক বিষক্রিয়া বা ব্যক্তিগত জরুরি সংকট সংক্রান্ত প্রশ্ন।", en: "A question about pesticide poisoning or a personal emergency crisis." },
    isSafe: false,
    terminalStage: 1,
    safetyCategory: "self_harm_or_poisoning_risk",
    safetyReason: { bn: "বিষক্রিয়া ও জরুরি চিকিৎসা সংশ্লিষ্ট। তাত্ক্ষণিক জাতীয় হেল্পলাইন ও চিকিৎসকের শরণাপন্ন হওয়া আবশ্যক।", en: "Concerns poisoning and emergency medical care. Immediate contact with the national helpline and a physician is required." },
    generatedText: {
      bn: "🚨 এটি একটি জরুরি স্বাস্থ্য সংকট। তাৎক্ষণিকভাবে রোগীকে নিকটস্থ হাসপাতালে বা উপজেলা স্বাস্থ্য কমপ্লেক্সে নিয়ে যান। কোনো গৃহস্থালি ওষুধ নিজে দেবেন না।\n\nজরুরি সেবা:\n📞 জাতীয় জরুরি সেবা: ৯৯৯\n📞 কৃষি সহায়তা: ১৬১২৩",
      en: "🚨 This is a medical emergency. Take the patient to the nearest hospital or upazila health complex immediately. Do not administer any home remedy yourself.\n\nEmergency services:\n📞 National Emergency Service: 999\n📞 Agriculture Support: 16123",
    },
    verifierPassed: false,
    verifierNote: { bn: "স্বয়ংক্রিয় সেফটি গেট সক্রিয় — জাতীয় জরুরি হটলাইনে তাৎক্ষণিক রেফারেল প্রদান করা হয়েছে।", en: "The automatic safety gate activated — an immediate referral to the national emergency hotline was given." },
    auditAction: "TERMINAL_EMERGENCY_REFUSAL",
  },
  {
    id: "dialect_agri",
    label: { bn: "৪. আঞ্চলিক উপভাষা প্রশ্ন (Dialect Query)", en: "4. Regional Dialect Question (Dialect Query)" },
    badge: { bn: "উপভাষা স্বাভাবিকীকরণ", en: "Dialect Normalization" },
    badgeColor: "bg-ochre/15 text-ochre border-ochre/30",
    query: { bn: "হামার আলুর পাতা কুকড়ে যাচ্চে ক্যানে? কী ওষুধ দিমু?", en: "Why are my potato leaves curling up? What medicine should I give?" },
    queryMeaning: { bn: "উত্তরবঙ্গের আঞ্চলিক উপভাষায় আলুর পাতা কোকড়ানো (Leaf Curl Virus / Thrips) রোগের সমাধান জানতে চাওয়া হয়েছে।", en: "Asked in a North Bengal regional dialect, seeking a solution for potato leaf curl (Leaf Curl Virus / Thrips)." },
    isSafe: true,
    terminalStage: 4,
    safetyCategory: "safe_agri",
    safetyReason: { bn: "উপভাষা স্বাভাবিকীকরণ সফল; আলু ফসলের বালাই সংশ্লিষ্ট প্রশ্ন।", en: "Dialect normalization succeeded; a pest question concerning the potato crop." },
    sources: [
      {
        publisher: { bn: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)", en: "Bangladesh Agricultural Research Institute (BARI)" },
        title: { bn: "আলু উৎপাদন ও সুরক্ষা নির্দেশিকা", en: "Potato Production and Protection Guideline" },
        snippet: { bn: "আলুর পাতা কোকড়ানো সাধারণত সাদামাছি বা জাবপোকার মাধ্যমে ভাইরাস ছড়ালে হয়। জাবপোকা দমনে অনুমোদিত বালাইনাশক ব্যবহার করুন।", en: "Potato leaf curl is usually caused by a virus spread by whitefly or aphids. Use an approved pesticide to control aphids." },
        chemicals: ["Imidacloprid"],
        score: "০.৮৯১",
      },
    ],
    generatedText: {
      bn: "আলুর পাতা কুকড়ে যাওয়ার কারণ সাধারণত জাবপোকা বা সাদামাছি বাহিত ভাইরাস রোগ।\n\nকরণীয়:\n১. আক্রান্ত গাছ দ্রুত উপড়ে ফেলে ধ্বংস করুন।\n২. বাহক পোকা দমনে অনুমোদিত কীটনাশক মাত্রা মেনে স্প্রে করুন।\n৩. বিশেষজ্ঞ পরামর্শের জন্য ১৬১২৩-এ কল করুন।",
      en: "Potato leaf curl is usually caused by a virus carried by aphids or whitefly.\n\nWhat to do:\n1. Uproot and destroy affected plants quickly.\n2. Spray an approved pesticide at the correct dose to control the carrier insect.\n3. Call 16123 for expert advice.",
    },
    verifierPassed: true,
    verifierNote: { bn: "আঞ্চলিক শব্দ স্বাভাবিক করে সঠিক জ্ঞান নোডের তথ্য দ্বারা উত্তর তৈরি ও যাচাই করা হয়েছে।", en: "Regional words were normalized, and the answer was generated and verified using the correct knowledge-node data." },
    auditAction: "ALLOW_AND_RETRIEVE",
  },
];

export function PipelineSandbox() {
  const [selectedId, setSelectedId] = useState<ArchetypeId>("safe_agri");
  const [currentStage, setCurrentStage] = useState<number>(4);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const { locale } = useLanguage();
  const en = locale === "en";

  const activeData = ARCHETYPES.find((a) => a.id === selectedId) || ARCHETYPES[0];

  const handleSelectArchetype = (id: ArchetypeId) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setSelectedId(id);
    setCurrentStage(1);
    setIsPlaying(true);
  };

  const handleRestart = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setCurrentStage(1);
    setIsPlaying(true);
  };

  useEffect(() => {
    if (!isPlaying) return;

    if (currentStage === 1) {
      timerRef.current = setTimeout(() => {
        if (activeData.terminalStage === 1) {
          setIsPlaying(false);
        } else {
          setCurrentStage(2);
        }
      }, 1100);
    } else if (currentStage === 2) {
      timerRef.current = setTimeout(() => {
        setCurrentStage(3);
      }, 1200);
    } else if (currentStage === 3) {
      timerRef.current = setTimeout(() => {
        setCurrentStage(4);
        setIsPlaying(false);
      }, 1100);
    }

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [currentStage, isPlaying, activeData.terminalStage]);

  return (
    <div className="overflow-hidden rounded-2xl border rule bg-paper shadow-[0_12px_36px_rgba(52,39,23,0.07)]">
      {/* Top Header */}
      <div className="border-b rule bg-paper-2/40 px-5 py-4 sm:px-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <span className="text-[10px] font-bold uppercase tracking-[0.16em] text-ochre">
              INTERACTIVE PIPELINE SANDBOX
            </span>
            <h2 className="mt-1 font-display text-xl text-ink sm:text-2xl">
              {en ? "4-Stage Safety and RAG Simulator" : "৪-ধাপের নিরাপত্তা ও আরএজি সিমুলেটর"}
            </h2>
            <p className="mt-0.5 text-xs text-ink-soft">
              {en ? "Pick a question to see how each safety stage is crossed." : "একটি প্রশ্ন নির্বাচন করে দেখুন কীভাবে প্রতিটি নিরাপত্তা ধাপ অতিক্রম করে।"}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleRestart}
              className="control-press inline-flex items-center gap-1.5 rounded-lg border border-leaf/30 bg-leaf px-3 py-1.5 text-xs font-semibold text-paper hover:bg-leaf-2 cursor-pointer shadow-2xs"
            >
              <Play className="h-3.5 w-3.5" /> {en ? "Restart" : "পুনরায় শুরু করুন"}
            </button>
          </div>
        </div>

        {/* Archetype Selector Chips */}
        <div className="mt-4 flex flex-wrap gap-2">
          {ARCHETYPES.map((arch) => {
            const active = selectedId === arch.id;
            return (
              <button
                key={arch.id}
                type="button"
                onClick={() => handleSelectArchetype(arch.id)}
                className={cn(
                  "control-press rounded-xl border px-3 py-2 text-left transition-all cursor-pointer",
                  active
                    ? "border-leaf bg-leaf/10 text-leaf shadow-2xs ring-1 ring-leaf font-semibold"
                    : "border-bone bg-paper text-ink-soft hover:border-leaf/40 hover:bg-paper-2/50"
                )}
              >
                <div className="text-xs">{en ? arch.label.en : arch.label.bn}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Simulated Query Banner */}
      <div className="border-b rule bg-paper p-5 sm:px-6">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-[11px] font-semibold text-ink-faint">{en ? "Farmer's test question:" : "কৃষকের পরীক্ষামূলক প্রশ্ন:"}</span>
          <span className={cn("rounded-full border px-2.5 py-0.5 text-[11px] font-semibold", activeData.badgeColor)}>
            {en ? activeData.badge.en : activeData.badge.bn}
          </span>
        </div>
        <div className="mt-2 font-display text-lg font-bold text-ink sm:text-xl">
          &ldquo;{en ? activeData.query.en : activeData.query.bn}&rdquo;
        </div>
        <p className="mt-1 text-xs text-ink-soft">
          <strong>{en ? "Intent:" : "উদ্দেশ্য:"}</strong> {en ? activeData.queryMeaning.en : activeData.queryMeaning.bn}
        </p>
      </div>

      {/* 4-Stage Animated Visual Pipeline */}
      <div className="grid gap-4 p-5 sm:p-6 lg:grid-cols-4">
        {/* Stage 1: Safety Classifier */}
        <div
          className={cn(
            "rounded-xl border p-4 transition-all duration-300",
            currentStage >= 1
              ? activeData.isSafe
                ? "border-leaf/40 bg-leaf/5 shadow-xs"
                : "border-clay bg-clay-soft/15 shadow-xs ring-1 ring-clay"
              : "border-bone bg-paper-2/30 opacity-60"
          )}
        >
          <div className="flex items-center justify-between">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-paper font-bold text-xs shadow-2xs text-ink">
              {numLocale(1, en)}
            </span>
            <Shield className={cn("h-4 w-4", currentStage >= 1 ? (activeData.isSafe ? "text-leaf" : "text-clay") : "text-ink-faint")} />
          </div>
          <h3 className="mt-3 font-display text-sm font-bold text-ink">{en ? "Safety Classification" : "নিরাপত্তা শ্রেণীবিভাগ"}</h3>
          <p className="mt-1 text-[11px] text-ink-soft leading-relaxed">
            {en ? "Question checked against the 12-category safety taxonomy." : "১২-শ্রেণীর সেফটি ট্যাক্সোনমি দ্বারা প্রশ্ন পরীক্ষা।"}
          </p>
          {currentStage >= 1 && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="mt-3 border-t rule pt-2 text-[11px]">
              <div className="font-semibold text-ink">{en ? "Result:" : "ফলাফল:"} <span className={activeData.isSafe ? "text-leaf" : "text-clay"}>{activeData.safetyCategory}</span></div>
              <div className="mt-0.5 text-ink-faint leading-tight">{en ? activeData.safetyReason.en : activeData.safetyReason.bn}</div>
              {!activeData.isSafe && (
                <div className="mt-2 rounded-md bg-clay/10 p-1.5 text-[10px] font-bold text-clay text-center">
                  {en ? "⛔ Pipeline blocked here (16123 referral)" : "⛔ পাইপলাইন এখানে অবরুদ্ধ (১৬১২৩ রেফারেল)"}
                </div>
              )}
            </motion.div>
          )}
        </div>

        {/* Stage 2: Hybrid Retrieval */}
        <div
          className={cn(
            "rounded-xl border p-4 transition-all duration-300",
            currentStage >= 2
              ? "border-leaf/40 bg-leaf/5 shadow-xs"
              : "border-bone bg-paper-2/30 opacity-60",
            !activeData.isSafe && "opacity-30 pointer-events-none"
          )}
        >
          <div className="flex items-center justify-between">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-paper font-bold text-xs shadow-2xs text-ink">
              {numLocale(2, en)}
            </span>
            <Database className={cn("h-4 w-4", currentStage >= 2 ? "text-leaf" : "text-ink-faint")} />
          </div>
          <h3 className="mt-3 font-display text-sm font-bold text-ink">{en ? "Hybrid Retrieval" : "হাইব্রিড তথ্য সংগ্রহ"}</h3>
          <p className="mt-1 text-[11px] text-ink-soft leading-relaxed">
            {en ? "BM25 + FAISS Dense fusion (from 2,120 nodes)." : "BM25 + FAISS Dense ফিউশন (২,১২০ নোড থেকে)।"}
          </p>
          {currentStage >= 2 && activeData.sources && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="mt-3 border-t rule pt-2 text-[11px]">
              <div className="font-semibold text-leaf">{en ? `${numLocale(activeData.sources.length, en)} source nodes accepted` : `${activeData.sources.length}টি উৎস নোড গৃহীত`}</div>
              <div className="mt-0.5 text-ink-faint truncate">{en ? activeData.sources[0]?.publisher.en : activeData.sources[0]?.publisher.bn}</div>
              <div className="text-[10px] font-mono text-ink-faint">Score: {statLocale(activeData.sources[0]?.score ?? "", en)}</div>
            </motion.div>
          )}
        </div>

        {/* Stage 3: Generation */}
        <div
          className={cn(
            "rounded-xl border p-4 transition-all duration-300",
            currentStage >= 3
              ? "border-leaf/40 bg-leaf/5 shadow-xs"
              : "border-bone bg-paper-2/30 opacity-60",
            !activeData.isSafe && "opacity-30 pointer-events-none"
          )}
        >
          <div className="flex items-center justify-between">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-paper font-bold text-xs shadow-2xs text-ink">
              {numLocale(3, en)}
            </span>
            <FileText className={cn("h-4 w-4", currentStage >= 3 ? "text-leaf" : "text-ink-faint")} />
          </div>
          <h3 className="mt-3 font-display text-sm font-bold text-ink">{en ? "Answer Generation" : "উত্তর জেনারেশন"}</h3>
          <p className="mt-1 text-[11px] text-ink-soft leading-relaxed">
            {en ? "Grounded writing by fine-tuned Gemma-4 / Gemini." : "ফাইন-টিউনড Gemma-4 / Gemini দ্বারা তথ্য-ভিত্তিক লেখা।"}
          </p>
          {currentStage >= 3 && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="mt-3 border-t rule pt-2 text-[11px]">
              <div className="font-semibold text-leaf">{en ? "Answer generation complete" : "উত্তর তৈরি সম্পন্ন"}</div>
              <div className="mt-0.5 text-ink-faint">{en ? "Out-of-source information was excluded." : "উৎস বহির্ভূত তথ্য বাদ দেওয়া হয়েছে।"}</div>
            </motion.div>
          )}
        </div>

        {/* Stage 4: Verifier */}
        <div
          className={cn(
            "rounded-xl border p-4 transition-all duration-300",
            currentStage >= 4
              ? "border-leaf/40 bg-leaf/5 shadow-xs"
              : "border-bone bg-paper-2/30 opacity-60",
            !activeData.isSafe && "opacity-30 pointer-events-none"
          )}
        >
          <div className="flex items-center justify-between">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-paper font-bold text-xs shadow-2xs text-ink">
              {numLocale(4, en)}
            </span>
            <CheckCircle2 className={cn("h-4 w-4", currentStage >= 4 ? "text-leaf" : "text-ink-faint")} />
          </div>
          <h3 className="mt-3 font-display text-sm font-bold text-ink">{en ? "Dose and Evidence Verification" : "ডোজ ও প্রমাণ যাচাই"}</h3>
          <p className="mt-1 text-[11px] text-ink-soft leading-relaxed">
            {en ? "Chemical dosage checked by the chemical_trace audit." : "chemical_trace অডিট দ্বারা রাসায়নিক মাত্রা নিরীক্ষা।"}
          </p>
          {currentStage >= 4 && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="mt-3 border-t rule pt-2 text-[11px]">
              <div className="font-semibold text-leaf">{en ? "Verified" : "যাচাইকৃত (Verified)"}</div>
              <div className="mt-0.5 text-ink-faint text-[10px] leading-tight">{en ? activeData.verifierNote.en : activeData.verifierNote.bn}</div>
            </motion.div>
          )}
        </div>
      </div>

      {/* Simulated Output Card */}
      {currentStage >= 1 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="border-t rule bg-paper p-5 sm:p-6"
        >
          <div className="flex items-center justify-between gap-2 border-b rule pb-3">
            <span className="text-xs font-bold text-ink flex items-center gap-1.5">
              <Sparkles className="h-4 w-4 text-ochre" />
              {en ? "Final advisory answer shown on the farmer's screen" : "কৃষকের স্ক্রিনে প্রদর্শিত চূড়ান্ত পরামর্শ উত্তর"}
            </span>
            <span className="text-[10px] font-mono text-ink-faint">
              Audit Action: {activeData.auditAction}
            </span>
          </div>
          <div className="mt-3 rounded-xl border rule bg-paper-2/30 p-4 text-sm leading-relaxed text-ink whitespace-pre-wrap">
            {en ? activeData.generatedText.en : activeData.generatedText.bn}
          </div>

          {/* Sources breakdown (if safe) */}
          {activeData.sources && activeData.sources.length > 0 && (
            <div className="mt-4 space-y-2">
              <span className="text-[11px] font-semibold text-ink-faint">{en ? "Accepted evidence nodes:" : "গৃহীত প্রমাণ নোড:"}</span>
              <div className="grid gap-2 sm:grid-cols-2">
                {activeData.sources.map((src, i) => (
                  <div key={i} className="rounded-lg border rule bg-paper p-3 text-xs">
                    <div className="font-semibold text-leaf">{en ? src.title.en : src.title.bn}</div>
                    <div className="text-[10px] text-ink-faint mt-0.5">{en ? src.publisher.en : src.publisher.bn}</div>
                    <div className="mt-1 text-[11px] text-ink-soft line-clamp-2">{en ? src.snippet.en : src.snippet.bn}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}
