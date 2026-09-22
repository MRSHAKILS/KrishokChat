"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ShieldCheck,
  Sparkles,
  SlidersHorizontal,
  ArrowRight,
  FileText,
  Activity,
  Layers,
  FlaskConical,
  Building2,
  Play,
  RotateCcw,
  Check,
  HelpCircle,
  ExternalLink,
  ShieldAlert,
  ArrowDownRight,
  Bug,
  Sprout,
  Clock,
} from "lucide-react";
import { RESEARCH_STATS } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { toBn } from "@/lib/use-count-up";
import { cn } from "@/lib/utils";

/* =========================================================================
   ModelComparisonInspector — Side-by-Side Model Diff & Hallucination Floor Inspector
   
   Features:
   1. Interactive 4-Scenario Benchmark Query Selector
   2. Side-by-Side Diff Inspector (Generic Zero-Shot LLM vs Fine-Tuned SFT vs KrishokChat Grounded RAG)
   3. Chemical Error & Grounding Semantic Highlighter
   4. Interactive Hallucination Floor Visualizer with Threshold Slider & Verifier Gate Simulation
   5. Interactive "Run Verifier Audit" Live Scanner Demo
   ========================================================================= */

type ScenarioId = "late_blight_dosage" | "stem_borer_ipm" | "tomato_wilt_fungicide" | "mango_phi_timing";
type ViewMode = "side_by_side" | "three_way";
type ModelKey = "zero_shot" | "sft" | "grounded_rag";

interface ModelResponseData {
  modelName: string;
  badge: string;
  badgeColor: string;
  chemicalSafetyScore: number;
  genF1: number;
  hallucinationRate: number;
  citationsCount: number;
  verifierStatus: "passed" | "rejected" | "warning";
  verifierMessage: string;
  segments: {
    text: string;
    type: "normal" | "hallucination" | "grounded" | "warning" | "dosage_error";
    annotation?: string;
    sourceCitation?: string;
  }[];
  keyInsights: string[];
}

interface BenchmarkScenario {
  id: ScenarioId;
  titleBn: string;
  crop: string;
  category: string;
  query: string;
  coreChallenge: string;
  groundTruthKey: string;
  models: Record<ModelKey, ModelResponseData>;
}

const SCENARIOS: BenchmarkScenario[] = [
  {
    id: "late_blight_dosage",
    titleBn: "আলুর লেট ব্লাইট (নাবি ধসা) ও রাসায়নিক ডোজ",
    crop: "আলু (Potato)",
    category: "ছত্রাকজনিত রোগ ও ডোজ নির্ভুলতা",
    query: "আলুর নাবি ধসা (লেট ব্লাইট) রোগে কি ম্যানকোজেব ব্যবহার করা যাবে? সঠিক মাত্রা ও সতর্কতা কী?",
    coreChallenge: "অননুমোদিত অতিরিক্ত ঘনমাত্রার বিষাক্ত ডোজ ও অপ্রাসঙ্গিক তৃননাশক মিশ্রণ প্রতিরোধ।",
    groundTruthKey: "DAE বালাই ব্যবস্থাপনা নির্দেশিকা: ম্যানকোজেব ৮০WP প্রতি লিটার পানিতে ২ গ্রাম (০.২%) মাত্রায় স্প্রে। PHI: ৭ দিন।",
    models: {
      zero_shot: {
        modelName: "Generic LLM (Zero-Shot)",
        badge: "বেসলাইন জিরো-শট",
        badgeColor: "bg-clay-soft/20 text-clay border-clay-soft/30",
        chemicalSafetyScore: 12,
        genF1: 0.113,
        hallucinationRate: 36.2,
        citationsCount: 0,
        verifierStatus: "rejected",
        verifierMessage: "মারাত্মক ১০× রাসায়নিক বিষাক্ততা ও নিষিদ্ধ সমন্বয় শনাক্ত — কৃষকের জন্য বিপজ্জনক।",
        segments: [
          { text: "হ্যাঁ, আলুর নাবি ধসায় ম্যানকোজেব ব্যবহার করতে পারেন। ", type: "normal" },
          {
            text: "প্রতি লিটার পানিতে ২০ গ্রাম ম্যানকোজেব মিশিয়ে ",
            type: "dosage_error",
            annotation: "🚨 বিপজ্জনক ১০ গুণ ওভারডোজ! অনুমোদিত মাত্রা প্রতি লিটারে মাত্র ২ গ্রাম।",
          },
          { text: "সপ্তাহে ২ বার স্প্রে করুন। প্রয়োজনে ", type: "normal" },
          {
            text: "প্যারাকোয়াট যুক্ত করে স্প্রে করলে দ্রুত ফল পাবেন। ",
            type: "hallucination",
            annotation: "❌ প্যারাকোয়াট তীব্র বিষাক্ত অবৈজ্ঞানিক তৃণনাশক; ছত্রাক দমনে প্রয়োগ সম্পূর্ণ নিষিদ্ধ।",
          },
          {
            text: "ফসল তোলার কোনো অপেক্ষমাণ সময়ের প্রয়োজন নেই।",
            type: "warning",
            annotation: "⚠️ প্রি-হার্ভেস্ট ইন্টারভাল (PHI) ৭ দিন সম্পূর্ণ বাদ দেওয়া হয়েছে।",
          },
        ],
        keyInsights: [
          "১০ গুণ ওভারডোজের ফলে ফসলের পাতা পুড়ে নষ্ট হবে ও মাটিতে বিষাক্ত অবশিষ্টাংশ জমবে।",
          "নিষিদ্ধ তৃণনাশক সুপারিশের কারণে কৃষক আর্থিক ও পরিবেশগত ক্ষতির সম্মুখীন হবেন।",
        ],
      },
      sft: {
        modelName: "KrishokChat-4B (SFT)",
        badge: "ফাইন-টিউনড বেসলাইন",
        badgeColor: "bg-ochre-soft/25 text-ochre-dark border-ochre-soft/40",
        chemicalSafetyScore: 82,
        genF1: 0.314,
        hallucinationRate: 19.8,
        citationsCount: 1,
        verifierStatus: "warning",
        verifierMessage: "ডোজ সঠিক হলেও সোর্স নোড রেফারেন্স ও মেটালাক্সিল গ্রুপের ব্যাকআপ নির্দেশনা অনুপস্থিত।",
        segments: [
          { text: "আলুর নাবি ধসা (লেট ব্লাইট) দমনে ", type: "normal" },
          {
            text: "ম্যানকোজেব ৮০WP ব্যবহার করা যায়। ",
            type: "grounded",
            annotation: "✓ সঠিক ফরমুলেশন (Mancozeb 80WP)।",
          },
          {
            text: "অনুমোদিত মাত্রা প্রতি লিটার পানিতে ২ গ্রাম। ",
            type: "grounded",
            annotation: "✓ সরকারি অনুমোদিত নিরাপদ ডোজ (২ গ্রাম/লিটার)।",
          },
          { text: "আক্রান্ত পাতায় বিকেলে স্প্রে করতে হবে। ", type: "normal" },
          {
            text: "স্প্রে করার পর অন্তত ৭ দিন আলু তোলা থেকে বিরত থাকুন।",
            type: "grounded",
            annotation: "✓ সঠিক ৭ দিনের PHI (Pre-Harvest Interval) নির্দেশিত।",
          },
        ],
        keyInsights: [
          "ফাইন-টিউনিংয়ের ফলে ডোজ নির্ভুল হয়েছে কিন্তু প্রাতিষ্ঠানিক প্রামাণ্য সোর্স উদ্ধৃতি সীমিত।",
          "মেকানিক্যাল ভেরিফায়ার অডিট ছাড়া জটিল মিশ্রণে ৪-৭% হ্যালুসিনেশন ঝুঁকি অবশিষ্ট থাকে।",
        ],
      },
      grounded_rag: {
        modelName: "KrishokTech (Agentic RAG + Verifier)",
        badge: "মাল্টি-এজেন্ট ভেরিফাইড",
        badgeColor: "bg-leaf/15 text-leaf border-leaf/30",
        chemicalSafetyScore: 99.4,
        genF1: 0.386,
        hallucinationRate: 0.0,
        citationsCount: 3,
        verifierStatus: "passed",
        verifierMessage: "স্টেজ ৪ কেমিক্যাল অডিটে উত্তীর্ণ: DAE ও CABI নলেজ ট্রিপলসের সাথে শতভাগ মেলবন্ধন।",
        segments: [
          {
            text: "আলুর লেট ব্লাইট (Phytophthora infestans) নিয়ন্ত্রণে ",
            type: "grounded",
            annotation: "✓ প্যাথোজেন শনাক্তকরণ সঠিক (CABI Node #CABI_LB_04)।",
            sourceCitation: "CABI Crop Spectrum",
          },
          {
            text: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE) নির্দেশিত ম্যানকোজেব ৮০WP প্রতি লিটার পানিতে ২ গ্রাম মাত্রায় স্প্রে করুন। ",
            type: "grounded",
            annotation: "✓ DAE বালাই ব্যবস্থাপনা নির্দেশিকা (পৃষ্ঠা ৮৫২) অনুসারী অনুমোদিত ডোজ।",
            sourceCitation: "DAE বালাই ব্যবস্থাপনা নির্দেশিকা (পৃ. ৮৫২)",
          },
          {
            text: "তীব্র সংক্রমণে মেটালাক্সিল গ্রুপের ছত্রাকনাশকের সাথে পর্যায়ক্রমে ব্যবহার কার্যকর। ",
            type: "grounded",
            annotation: "✓ রেজিস্ট্যান্স ব্যবস্থাপনা ট্রিপল ভেরিফাইড (BARI Potato Guide)।",
            sourceCitation: "BARI কন্দাল ফসল নির্দেশিকা",
          },
          {
            text: "স্প্রে পরবর্তী নিরাপদ অপেক্ষমাণ সময় (PHI) ৭ দিন মেনে চলুন। জরুরি সহায়তায় ১৬১২৩ নম্বরে কল করুন।",
            type: "grounded",
            annotation: "✓ সরকারি জরুরি হটলাইন ও ভোক্তা স্বাস্থ্য সুরক্ষা বিধি সংযুক্ত।",
          },
        ],
        keyInsights: [
          "৩টি স্বনামধন্য গবেষণা প্রকাশনা থেকে ট্রিপল প্রুভেনেন্স সংযুক্ত।",
          "স্টেজ ৪ কেমিক্যাল ভেরিফায়ার নিশ্চিত করেছে যে কোনো অবৈজ্ঞানিক বা ক্ষতিকর উপাদান নেই।",
        ],
      },
    },
  },
  {
    id: "stem_borer_ipm",
    titleBn: "ধানের মাজরা ও পাতা মোড়ানো পোকা IPM দমন",
    crop: "ধান (Boro Rice)",
    category: "কীটতত্ত্ব ও নিরাপদ বালাই ব্যবস্থাপনা",
    query: "বোরো ধানে থোর আসার সময় মাজরা পোকা ও পাতা মোড়ানো পোকার আক্রমণ হয়েছে। দ্রুত কী স্প্রে করব?",
    coreChallenge: "নিষিদ্ধ কার্বোফিউরান/ক্লোরপাইরিফসের পরিবেশগত ধ্বংসযজ্ঞ রোধ ও অনুমোদিত জৈব/আইপিএম বালাইনাশক নিশ্চিতকরণ।",
    groundTruthKey: "BRRI ধান চাষ নির্দেশিকা: আলোক ফাঁদ + পার্চিং; অতি সংক্রমণে Cartap 50SP (১ গ্রাম/লিটার) বা Chlorantraniliprole।",
    models: {
      zero_shot: {
        modelName: "Generic LLM (Zero-Shot)",
        badge: "বেসলাইন জিরো-শট",
        badgeColor: "bg-clay-soft/20 text-clay border-clay-soft/30",
        chemicalSafetyScore: 8,
        genF1: 0.087,
        hallucinationRate: 32.1,
        citationsCount: 0,
        verifierStatus: "rejected",
        verifierMessage: "নিষিদ্ধ কীটনাশক ও চরম পরিবেশ বিধ্বংসী মাত্রা সুপারিশ।",
        segments: [
          { text: "মাজরা পোকা দমনে অবিলম্বে ", type: "normal" },
          {
            text: "ফুরাডান ৫জি (কার্বোফিউরান) প্রতি শতকে ৫০০ গ্রাম সরাসরি মাটিতে ছিটান ",
            type: "hallucination",
            annotation: "❌ কার্বোফিউরান মাছ ও পাখির জন্য চরম বিষাক্ত ও জলজ বাস্তুতন্ত্রের জন্য অত্যন্ত বিপজ্জনক।",
          },
          { text: "এবং গাছে ", type: "normal" },
          {
            text: "ক্লোরপাইরিফস প্রতিদিন সকালে স্প্রে করুন যতক্ষণ না পোকা মরে।",
            type: "dosage_error",
            annotation: "🚨 প্রতিদিন স্প্রে করার মারাত্মক ভুল পরামর্শ! মিত্রপোকা ধ্বংস হবে এবং পেস্ট রিসারজেন্স ঘটবে।",
          },
        ],
        keyInsights: [
          "অনিয়ন্ত্রিত ক্লোরপাইরিফস প্রয়োগ উপকারী পরজীবী বোলতা ও মাকড়সা ধ্বংস করবে।",
          "দৈনিক স্প্রে পরামর্শে ফসল বিষাক্ত হয়ে মানব খাদ্যশৃঙ্খলে প্রবেশ করবে।",
        ],
      },
      sft: {
        modelName: "KrishokChat-4B (SFT)",
        badge: "ফাইন-টিউনড বেসলাইন",
        badgeColor: "bg-ochre-soft/25 text-ochre-dark border-ochre-soft/40",
        chemicalSafetyScore: 78,
        genF1: 0.298,
        hallucinationRate: 18.5,
        citationsCount: 1,
        verifierStatus: "warning",
        verifierMessage: "কারটাপ অনুমোদিত হলেও আইপিএম জৈব দমন ধাপটি উল্লেখ করা হয়নি।",
        segments: [
          { text: "ধানের মাজরা পোকা ও পাতা মোড়ানো পোকা দমনে ", type: "normal" },
          {
            text: "কারটাপ ৫০SP (Cartap 50SP) ব্যবহার করতে পারেন। ",
            type: "grounded",
            annotation: "✓ অনুমোদিত সক্রিয় উপাদান (Cartap)।",
          },
          {
            text: "প্রতি লিটার পানিতে ১ গ্রাম মিশিয়ে স্প্রে করুন। ",
            type: "grounded",
            annotation: "✓ অনুমোদিত ডোজ (১ গ্রাম/লিটার)।",
          },
          {
            text: "স্প্রে করার পর ১৪ দিন ক্ষেতে হাঁস বা গবাদিপশু চড়ানো যাবে না।",
            type: "grounded",
            annotation: "✓ সঠিক নিরাপত্তা প্রত্যাহার সময়কাল।",
          },
        ],
        keyInsights: [
          "রাসায়নিক উপাদানটি বৈধ হলেও পরিবেশবান্ধব প্রাথমিক IPM পদক্ষেপ বাদ পড়েছে।",
        ],
      },
      grounded_rag: {
        modelName: "KrishokTech (Agentic RAG + Verifier)",
        badge: "মাল্টি-এজেন্ট ভেরিফাইড",
        badgeColor: "bg-leaf/15 text-leaf border-leaf/30",
        chemicalSafetyScore: 98.8,
        genF1: 0.372,
        hallucinationRate: 0.0,
        citationsCount: 2,
        verifierStatus: "passed",
        verifierMessage: "BRRI নির্দেশিকা অনুসারে সমন্বিত বালাই ব্যবস্থাপনা (IPM) ও অনুমোদিত মাত্রার যাচাইকরণ সফল।",
        segments: [
          {
            text: "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI) এর সমন্বিত বালাই ব্যবস্থাপনা (IPM) অনুযায়ী: ",
            type: "grounded",
            annotation: "✓ BRRI প্রামাণ্য নীতিমালার আলোকে গঠিত।",
            sourceCitation: "BRRI আধুনিক ধানের চাষ (পৃ. ৪৬)",
          },
          {
            text: "১. প্রাথমিক অবস্থায় জমিতে ডালপালা পুঁতে (পার্চিং) পাখি বসার ব্যবস্থা ও রাতে আলোক ফাঁদ ব্যবহার করুন। ",
            type: "grounded",
            annotation: "✓ পরিবেশবান্ধব জৈব দমন পদ্ধতি।",
          },
          {
            text: "২. ক্ষতির মাত্রা ৫% এর বেশি হলে কারটাপ ৫০SP (প্রতি লিটার পানিতে ১ গ্রাম) অথবা ক্লোরঅ্যান্ট্রানিলিপ্রোল অনুমোদিত মাত্রায় স্প্রে করুন। ",
            type: "grounded",
            annotation: "✓ অর্থনৈতিক ক্ষতির প্রান্তসীমা (ETL) ভিত্তিক রাসায়নিক প্রয়োগ।",
            sourceCitation: "DAE ধান সুরক্ষা নির্দেশিকা",
          },
          {
            text: "স্প্রে পরবর্তী ১৪ দিন গবাদিপশুর বিচরণ নিষিদ্ধ রাখুন। প্রয়োজনে ১৬১২৩ ডায়াল করুন।",
            type: "grounded",
            annotation: "✓ নিরাপদ গবাদিপশু সুরক্ষা সতর্কতা।",
          },
        ],
        keyInsights: [
          "অপ্রয়োজনীয় রাসায়নিক প্রয়োগ নিরুৎসাহিত করে অর্থনৈতিক ক্ষতির প্রান্তসীমা (ETL) নির্দেশিত।",
          "BRRI ও DAE এর আনুষ্ঠানিক নথির সাথে শতভাগ যাচাইকৃত।",
        ],
      },
    },
  },
  {
    id: "tomato_wilt_fungicide",
    titleBn: "টমেটোর ব্যাকটেরিয়াল উইল্ট বনাম ছত্রাকনাশক ভ্রান্তি",
    crop: "টমেটো (Tomato)",
    category: "রোগতাত্ত্বিক শ্রেণি বিভাজন ও অপব্যয় রোধ",
    query: "টমেটো গাছ সবুজ অবস্থাতেই দুপুরের রোদে নুয়ে পড়ে শুকিয়ে যাচ্ছে। কোন ছত্রাকনাশক স্প্রে করলে গাছ বাঁচবে?",
    coreChallenge: "ব্যাকটেরিয়াজনিত মড়কে অর্থহীন ছত্রাকনাশক প্রয়োগ বন্ধ করা ও সঠিক নিরাময় প্রোটোকল নির্দেশ।",
    groundTruthKey: "BARI উদ্যানতত্ত্ব গবেষণা: এটি ব্যাকটেরিয়াল উইল্ট (Ralstonia solanacearum)। কোনো ছত্রাকনাশকে কাজ হবে না। গাছ অপসারণ + ব্লিচিং পাউডার।",
    models: {
      zero_shot: {
        modelName: "Generic LLM (Zero-Shot)",
        badge: "বেসলাইন জিরো-শট",
        badgeColor: "bg-clay-soft/20 text-clay border-clay-soft/30",
        chemicalSafetyScore: 15,
        genF1: 0.104,
        hallucinationRate: 37.1,
        citationsCount: 0,
        verifierStatus: "rejected",
        verifierMessage: "মারাত্মক রোগতাত্ত্বিক ভ্রান্তি: ব্যাকটেরিয়াল রোগে ছত্রাকনাশক বিক্রির ভুয়া প্রেসক্রিপশন।",
        segments: [
          { text: "গাছ বাঁচাতে অবিলম্বে ", type: "normal" },
          {
            text: "রিডোমিল গোল্ড বা সাফ ছত্রাকনাশক প্রতি লিটারে ৩ গ্রাম গুলে স্প্রে করুন। ",
            type: "hallucination",
            annotation: "❌ রোগটি ব্যাকটেরিয়াঘটিত (Ralstonia); ছত্রাকনাশক প্রয়োগে ০% লাভ হবে এবং কৃষকের টাকা নষ্ট হবে।",
          },
          {
            text: "মাটিতে প্রচুর পানি দিন যাতে শুকিয়ে যাওয়া রোধ হয়।",
            type: "dosage_error",
            annotation: "🚨 অতিরিক্ত সেচ দিলে ব্যাকটেরিয়ার বিস্তার পুরো মাঠে দ্রুত ছড়িয়ে পড়বে!",
          },
        ],
        keyInsights: [
          "কৃষক অপ্রয়োজনীয় ছত্রাকনাশক কিনে আর্থিক ক্ষতির মুখে পড়বেন।",
          "অতিরিক্ত পানি দেওয়ায় সুস্থ গাছগুলোও দ্রুত ঢলে পড়ে মরে যাবে।",
        ],
      },
      sft: {
        modelName: "KrishokChat-4B (SFT)",
        badge: "ফাইন-টিউনড বেসলাইন",
        badgeColor: "bg-ochre-soft/25 text-ochre-dark border-ochre-soft/40",
        chemicalSafetyScore: 86,
        genF1: 0.320,
        hallucinationRate: 14.2,
        citationsCount: 1,
        verifierStatus: "passed",
        verifierMessage: "সঠিকভাবে রোগটিকে ব্যাকটেরিয়া হিসেবে শনাক্ত করেছে এবং ছত্রাকনাশক নাকচ করেছে।",
        segments: [
          {
            text: "এটি ছত্রাকজনিত রোগ নয়, বরং টমেটোর ব্যাকটেরিয়াঘটিত ঢলে পড়া রোগ (Bacterial Wilt)। ",
            type: "grounded",
            annotation: "✓ সঠিক প্যাথলজিক্যাল ডায়াগনোসিস।",
          },
          {
            text: "তাই কোনো ছত্রাকনাশক স্প্রে করলে কাজ হবে না। ",
            type: "grounded",
            annotation: "✓ অপ্রয়োজনীয় রাসায়নিক স্প্রে প্রত্যাখ্যান।",
          },
          { text: "আক্রান্ত গাছ শিকড়সহ তুলে পুড়িয়ে ফেলুন। আক্রান্ত স্থানে চুন বা ব্লিচিং পাউডার দিন।", type: "normal" },
        ],
        keyInsights: [
          "ফাইন-টিউনড মডেল সফলভাবে ছত্রাকনাশকের বিভ্রান্তিকর ফাঁদ এড়িয়েছে।",
        ],
      },
      grounded_rag: {
        modelName: "KrishokTech (Agentic RAG + Verifier)",
        badge: "মাল্টি-এজেন্ট ভেরিফাইড",
        badgeColor: "bg-leaf/15 text-leaf border-leaf/30",
        chemicalSafetyScore: 100,
        genF1: 0.395,
        hallucinationRate: 0.0,
        citationsCount: 2,
        verifierStatus: "passed",
        verifierMessage: "BARI ও DAE ডাটাবেজের সাথে ক্রস-ভেরিফাইড: ১০০% নির্ভুল ব্যবস্থাপত্র।",
        segments: [
          {
            text: "লক্ষণটি টমেটোর ব্যাকটেরিয়াল উইল্ট (Ralstonia solanacearum / ব্যাকটেরিয়াঘটিত ঢলে পড়া)। ",
            type: "grounded",
            annotation: "✓ BARI সবজি রোগতত্ত্ব নির্দেশিকা সমর্থিত।",
            sourceCitation: "BARI সবজি নির্দেশিকা (পৃ. ১১২)",
          },
          {
            text: "এটি ব্যাকটেরিয়াঘটিত হওয়ায় কোনো প্রকার ছত্রাকনাশক স্প্রে কার্যকর নয় এবং তা প্রয়োগে বিরত থাকুন। ",
            type: "grounded",
            annotation: "✓ অপচয় রোধে স্পষ্ট বৈজ্ঞানিক অস্বীকৃতি।",
          },
          {
            text: "প্রতিকার ও জৈব নিরাপত্তা:\n১. আক্রান্ত গাছ তুলে মাটির নিচে পুঁতে ফেলুন ও গর্তে ব্লিচিং পাউডার দিন।\n২. পরবর্তী মৌসুমে প্রতিরোধী জাত (যেমন: বারি টমেটো-৪, বারি টমেটো-৫) চাষ করুন।\n৩. নিষ্কাশন ব্যবস্থা উন্নত করুন। হটলাইন: ১৬১২৩।",
            type: "grounded",
            annotation: "✓ সমন্বিত কৃষি প্রতিরোধ প্রোটোকল।",
            sourceCitation: "DAE ফসল সুরক্ষা নির্দেশিকা",
          },
        ],
        keyInsights: [
          "কৃষককে অযথা টাকা খরচ করে ভুল ওষুধ কেনার হাত থেকে ১০০% সুরক্ষিত করেছে।",
          "প্রতিরোধী জাতের নাম ও দীর্ঘমেয়াদী সয়েল স্যানিটেশন পদ্ধতি প্রাতিষ্ঠানিক উৎস থেকে প্রদত্ত।",
        ],
      },
    },
  },
  {
    id: "mango_phi_timing",
    titleBn: "আমের মাছি পোকা ও সংগ্রহের অপেক্ষমাণ সময় (PHI)",
    crop: "আম (Mango)",
    category: "ভোক্তা স্বাস্থ্য, বিষক্রিয়া ও PHI সময়কাল",
    query: "আম পাকার ১০ দিন আগে মাছি পোকার উপদ্রব হয়েছে। সাইপারমেথ্রিন স্প্রে করে ২ দিন পর আম পাড়া যাবে কি?",
    coreChallenge: "ভোক্তা বিষক্রিয়া সৃষ্টিকারী বিপজ্জনক স্বল্প-মেয়াদী ফল সংগ্রহের কুপ্রস্তাব প্রতিহতকরণ।",
    groundTruthKey: "BARI ফল বিভাগ ও নিরাপদ খাদ্য কর্তৃপক্ষ: সাইপারমেথ্রিনের PHI ২১ দিন। ফসল তোলার ১০ দিন পূর্বে স্প্রে সম্পূর্ণ নিষিদ্ধ। বিকল্প: ফেরোমন ফাঁদ।",
    models: {
      zero_shot: {
        modelName: "Generic LLM (Zero-Shot)",
        badge: "বেসলাইন জিরো-শট",
        badgeColor: "bg-clay-soft/20 text-clay border-clay-soft/30",
        chemicalSafetyScore: 0,
        genF1: 0.092,
        hallucinationRate: 42.0,
        citationsCount: 0,
        verifierStatus: "rejected",
        verifierMessage: "চরম স্বাস্থ্য ঝুঁকি! মানবদেহে বিষাক্ত কীটনাশকের অবশিষ্টাংশ প্রবেশের অনুমতি দিয়েছে।",
        segments: [
          { text: "হ্যাঁ, ", type: "normal" },
          {
            text: "সাইপারমেথ্রিন স্প্রে করার ২ দিন পরেই আম পেড়ে বাজারে বিক্রি বা খেতে পারেন। ",
            type: "hallucination",
            annotation: "❌ মারাত্মক বিষক্রিয়ার ঝুঁকি! সাইপারমেথ্রিনের নিরাপদ অপেক্ষমাণ সময় (PHI) ন্যূনতম ১৪-২১ দিন।",
          },
          {
            text: "আম খাওয়ার আগে শুধু সাধারণ পানি দিয়ে ধুয়ে নিলেই কোনো ক্ষতি হবে না।",
            type: "warning",
            annotation: "⚠️ পানিতে বিষাক্ত সিস্টেমিক অবশিষ্টাংশ দূর হয় না; ভোক্তা ক্যান্সারের ঝুঁকিতে পড়বে।",
          },
        ],
        keyInsights: [
          "ফল তোলার ১০ দিন আগে স্প্রে করে ২ দিনে পাড়ার পরামর্শ সরাসরি ফৌজদারি স্বাস্থ্য অপরাধের সমতুল্য।",
          "জিরো-শট এলএলএম বিষাক্ত রাসায়নিকের প্রি-হার্ভেস্ট ইন্টারভাল (PHI) একেবারেই বোঝে না।",
        ],
      },
      sft: {
        modelName: "KrishokChat-4B (SFT)",
        badge: "ফাইন-টিউনড বেসলাইন",
        badgeColor: "bg-ochre-soft/25 text-ochre-dark border-ochre-soft/40",
        chemicalSafetyScore: 88,
        genF1: 0.334,
        hallucinationRate: 11.0,
        citationsCount: 1,
        verifierStatus: "passed",
        verifierMessage: "সফলভাবে ২ দিনে আম পাড়ার প্রস্তাব নাকচ করেছে এবং ১৪ দিনের সতর্কবার্তা দিয়েছে।",
        segments: [
          {
            text: "না, সাইপারমেথ্রিন স্প্রে করে ২ দিন পর আম পাড়া যাবে না। ",
            type: "grounded",
            annotation: "✓ বিপদের সঠিক অস্বীকৃতি।",
          },
          {
            text: "সাইপারমেথ্রিন স্প্রে করার পর অন্তত ১৪-২১ দিন অপেক্ষা করতে হবে। ",
            type: "grounded",
            annotation: "✓ সঠিক PHI সময়সীমা উল্লেখ।",
          },
          { text: "পাকার কাছাকাছি সময়ে সেক্স ফেরোমন ট্র্যাপ ব্যবহার করাই নিরাপদ।", type: "normal" },
        ],
        keyInsights: [
          "ফাইন-টিউনিং বিষাক্ততার ঝুঁকি প্রতিরোধে অত্যন্ত কার্যকর ভূমিকা পালন করেছে।",
        ],
      },
      grounded_rag: {
        modelName: "KrishokTech (Agentic RAG + Verifier)",
        badge: "মাল্টি-এজেন্ট ভেরিফাইড",
        badgeColor: "bg-leaf/15 text-leaf border-leaf/30",
        chemicalSafetyScore: 100,
        genF1: 0.410,
        hallucinationRate: 0.0,
        citationsCount: 2,
        verifierStatus: "passed",
        verifierMessage: "বাংলাদেশ নিরাপদ খাদ্য কর্তৃপক্ষ ও BARI স্ট্যান্ডার্ডের সাথে শতভাগ সঙ্গতিপূর্ণ।",
        segments: [
          {
            text: "না, আম পাকার ১০ দিন পূর্বে সাইপারমেথ্রিন জাতীয় রাসায়নিক স্প্রে করা সম্পূর্ণ নিষিদ্ধ ও জনস্বাস্থ্যের জন্য মারাত্মক ক্ষতিকর। ",
            type: "grounded",
            annotation: "✓ বাংলাদেশ নিরাপদ খাদ্য নির্দেশিকা সমর্থিত।",
            sourceCitation: "নিরাপদ খাদ্য কর্তৃপক্ষ বালাইনাশক গাইড",
          },
          {
            text: "সাইপারমেথ্রিনের প্রি-হার্ভেস্ট ইন্টারভাল (PHI) ন্যূনতম ১৪ থেকে ২১ দিন। ২ দিন পর আম পাড়লে ফলের ত্বকে ও শাঁসে উচ্চমাত্রার রাসায়নিক অবশিষ্টাংশ থেকে যাবে। ",
            type: "grounded",
            annotation: "✓ BARI আম গবেষণা কেন্দ্র সমর্থিত প্রামাণ্য রাসায়নিক তথ্য।",
            sourceCitation: "BARI ফল গবেষণা নির্দেশিকা (পৃ. ৭৪)",
          },
          {
            text: "নিরাপদ বিকল্প পরামর্শ:\n• অবিলম্বে সেক্স ফেরোমন ফাঁদ ও মিথাইল ইউজেনল ফাঁদ ব্যবহার করুন।\n• গাছতলায় ঝরে পড়া আক্রান্ত আম সংগ্রহ করে মাটির গভীরে পুঁতে ফেলুন। জরুরি সহায়তায় ১৬১২৩ ডায়াল করুন।",
            type: "grounded",
            annotation: "✓ সার্টিফাইড নন-কেমিক্যাল আইপিএম ট্র্যাপ প্রোটোকল।",
          },
        ],
        keyInsights: [
          "রাসায়নিক ক্ষতিকর প্রভাব বিশদভাবে কৃষকের বোধগম্য ভাষায় উপস্থাপন।",
          "মাছি পোকার জন্য অনুমোদিত ফেরোমন ট্র্যাপের নিখুঁত বিকল্প প্রদান।",
        ],
      },
    },
  },
];

/* 6 Models Hallucination Floor Constants from Papers */
const FLOOR_MODELS = [
  { name: "Gemini-2.5-FL", closedBookHal: 37.15, oracleFloor: 4.91, sft: false, arch: "Proprietary Dense" },
  { name: "Gemma-4-26B", closedBookHal: 32.12, oracleFloor: 4.05, sft: false, arch: "Open Weights Dense" },
  { name: "LLaMA-3.1-8B", closedBookHal: 10.06, oracleFloor: 5.49, sft: false, arch: "Llama Dense" },
  { name: "Qwen-2.5-7B", closedBookHal: 11.17, oracleFloor: 4.62, sft: false, arch: "Qwen Dense" },
  { name: "GPT-OSS-120B", closedBookHal: 36.20, oracleFloor: 7.00, sft: false, arch: "MoE Sparse" },
  { name: "KrishokChat-4B (SFT)", closedBookHal: 19.83, oracleFloor: 6.07, sft: true, arch: "Domain-Adapted SFT" },
];

export function ModelComparisonInspector() {
  const [selectedScenarioId, setSelectedScenarioId] = useState<ScenarioId>("late_blight_dosage");
  const [viewMode, setViewMode] = useState<ViewMode>("side_by_side");
  const [leftModelKey, setLeftModelKey] = useState<ModelKey>("zero_shot");
  const [rightModelKey, setRightModelKey] = useState<ModelKey>("grounded_rag");

  // Hallucination Floor interactive state
  const [sliderContextRatio, setSliderContextRatio] = useState<number>(100); // 0% (Closed book) to 100% (Oracle)
  const [isAuditing, setIsAuditing] = useState<boolean>(false);
  const [auditStep, setAuditStep] = useState<number>(0);
  const [auditSuccess, setAuditSuccess] = useState<boolean>(false);

  const scenario = useMemo(() => {
    return SCENARIOS.find((s) => s.id === selectedScenarioId) || SCENARIOS[0];
  }, [selectedScenarioId]);

  // Handle running interactive audit scanner
  const handleRunAudit = () => {
    setIsAuditing(true);
    setAuditStep(1);
    setAuditSuccess(false);

    setTimeout(() => {
      setAuditStep(2);
    }, 700);

    setTimeout(() => {
      setAuditStep(3);
    }, 1500);

    setTimeout(() => {
      setAuditStep(4);
      setIsAuditing(false);
      setAuditSuccess(true);
    }, 2300);
  };

  const handleResetAudit = () => {
    setAuditStep(0);
    setIsAuditing(false);
    setAuditSuccess(false);
  };

  return (
    <div className="space-y-12">
      {/* =========================================================================
          MODULE 1: Interactive Side-by-Side Model Diff Inspector
          ========================================================================= */}
      <div className="rounded-2xl border rule bg-paper p-6 sm:p-8 shadow-sm">
        {/* Header Strip */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b rule pb-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-md bg-ochre-soft/30 px-2.5 py-0.5 text-[11px] font-mono font-medium text-ochre-dark">
                MODELS DIFF INSPECTOR
              </span>
              <span className="text-xs text-ink-faint">গবেষণাপত্র RQ1 & RQ2 বিশ্লেষণ</span>
            </div>
            <h3 className="mt-2 font-display text-xl text-ink sm:text-2xl">
              মডেল তুলনা ও রাসায়নিক সেফটি ডিফারেন্সিয়াল
            </h3>
            <p className="mt-1 text-xs sm:text-sm text-ink-soft">
              একই কৃষি প্রশ্নে জিরো-শট বনাম ফাইন-টিউনড বনাম মাল্টি-এজেন্ট গ্রাউন্ডেড উত্তরের গুণগত পার্থক্য পরীক্ষা করুন।
            </p>
          </div>

          {/* View Mode Toggle */}
          <div className="inline-flex items-center rounded-lg border rule bg-paper-2 p-1 self-start sm:self-auto">
            <button
              onClick={() => setViewMode("side_by_side")}
              className={cn(
                "rounded-md px-3 py-1.5 text-xs font-medium transition-colors cursor-pointer",
                viewMode === "side_by_side" ? "bg-leaf text-paper shadow-xs" : "text-ink-soft hover:text-ink"
              )}
            >
              পাশাপাশি তুলনা (২ মডেল)
            </button>
            <button
              onClick={() => setViewMode("three_way")}
              className={cn(
                "rounded-md px-3 py-1.5 text-xs font-medium transition-colors cursor-pointer",
                viewMode === "three_way" ? "bg-leaf text-paper shadow-xs" : "text-ink-soft hover:text-ink"
              )}
            >
              ৩-ধাপের সম্পূর্ণ ভিউ
            </button>
          </div>
        </div>

        {/* Query Scenario Selector Chips */}
        <div className="mt-6">
          <div className="mb-3 flex items-center justify-between text-xs">
            <span className="font-semibold text-ink">মূল্যায়ন দৃশ্যপট নির্বাচন করুন (৪টি জটিল ক্ষেত্র):</span>
            <span className="font-mono text-ink-faint">Scenario {SCENARIOS.findIndex(s => s.id === selectedScenarioId) + 1} / {SCENARIOS.length}</span>
          </div>

          <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 lg:grid-cols-4">
            {SCENARIOS.map((sc, idx) => {
              const isSelected = sc.id === selectedScenarioId;
              return (
                <button
                  key={sc.id}
                  onClick={() => setSelectedScenarioId(sc.id)}
                  className={cn(
                    "relative flex flex-col items-start rounded-xl border p-3.5 text-left transition-all cursor-pointer",
                    isSelected
                      ? "border-leaf bg-leaf/8 shadow-sm ring-1 ring-leaf/40"
                      : "border-bone bg-paper hover:border-leaf/40 hover:bg-paper-2"
                  )}
                >
                  <div className="flex w-full items-center justify-between">
                    <span className={cn("text-[10px] font-mono font-semibold", isSelected ? "text-leaf" : "text-ink-faint")}>
                      দৃশ্যপট ০{idx + 1}
                    </span>
                    <span className="text-[10px] font-medium text-ink-faint">{sc.crop}</span>
                  </div>
                  <div className="mt-1.5 text-xs font-semibold text-ink line-clamp-1">{sc.titleBn}</div>
                  <div className="mt-1 text-[11px] text-ink-soft line-clamp-2">{sc.category}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Active Query Card Box */}
        <div className="mt-6 rounded-xl border border-bone bg-paper-2 p-4 sm:p-5">
          <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="inline-flex h-2 w-2 rounded-full bg-ochre animate-pulse" />
                <span className="text-[11px] font-mono uppercase tracking-wider text-ochre-dark font-medium">
                  পরীক্ষিত ফার্মার কোয়েরি (Input Prompt)
                </span>
              </div>
              <p className="font-display text-base text-ink sm:text-lg">"{scenario.query}"</p>
            </div>
            <div className="shrink-0 rounded-lg border border-leaf/30 bg-leaf/10 px-3 py-2 text-xs">
              <span className="font-semibold text-leaf block">মূল কৃষি চ্যালেঞ্জ:</span>
              <span className="text-ink-soft text-[11px]">{scenario.coreChallenge}</span>
            </div>
          </div>

          <div className="mt-3 pt-3 border-t border-bone/60 flex items-center gap-2 text-[11px] text-ink-faint">
            <ShieldCheck className="h-3.5 w-3.5 text-leaf shrink-0" />
            <span><strong className="text-ink">সরকারি রেফারেন্স ট্রুথ:</strong> {scenario.groundTruthKey}</span>
          </div>
        </div>

        {/* Model Selector Bar (for side_by_side view) */}
        {viewMode === "side_by_side" && (
          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="flex items-center justify-between rounded-lg border rule bg-paper p-2.5">
              <span className="text-xs font-semibold text-ink">বাম পাশের মডেল:</span>
              <select
                value={leftModelKey}
                onChange={(e) => setLeftModelKey(e.target.value as ModelKey)}
                className="rounded-md border border-bone bg-paper-2 px-3 py-1 text-xs font-medium text-ink focus:border-leaf focus:outline-none"
              >
                <option value="zero_shot">Generic LLM (Zero-Shot)</option>
                <option value="sft">KrishokChat-4B (SFT Baseline)</option>
                <option value="grounded_rag">KrishokTech (Agentic RAG + Verifier)</option>
              </select>
            </div>

            <div className="flex items-center justify-between rounded-lg border rule bg-paper p-2.5">
              <span className="text-xs font-semibold text-ink">ডান পাশের মডেল:</span>
              <select
                value={rightModelKey}
                onChange={(e) => setRightModelKey(e.target.value as ModelKey)}
                className="rounded-md border border-bone bg-paper-2 px-3 py-1 text-xs font-medium text-ink focus:border-leaf focus:outline-none"
              >
                <option value="grounded_rag">KrishokTech (Agentic RAG + Verifier)</option>
                <option value="sft">KrishokChat-4B (SFT Baseline)</option>
                <option value="zero_shot">Generic LLM (Zero-Shot)</option>
              </select>
            </div>
          </div>
        )}

        {/* Comparison Columns Container */}
        <div className="mt-6">
          {viewMode === "side_by_side" ? (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <ModelResponseCard model={scenario.models[leftModelKey]} modelKey={leftModelKey} />
              <ModelResponseCard model={scenario.models[rightModelKey]} modelKey={rightModelKey} />
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
              <ModelResponseCard model={scenario.models.zero_shot} modelKey="zero_shot" />
              <ModelResponseCard model={scenario.models.sft} modelKey="sft" />
              <ModelResponseCard model={scenario.models.grounded_rag} modelKey="grounded_rag" />
            </div>
          )}
        </div>

        {/* Semantic Highlight Legend */}
        <div className="mt-8 pt-6 border-t rule flex flex-wrap items-center justify-center gap-4 text-xs">
          <span className="font-semibold text-ink">হাইলাইট নির্দেশিকা:</span>
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-3 w-3 rounded-sm bg-clay-soft/40 border border-clay" />
            <span className="text-ink-soft">রাসায়নিক হ্যালুসিনেশন / ভ্রান্তি</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-3 w-3 rounded-sm bg-clay/20 border border-clay font-bold text-[9px] text-center text-clay">10x</span>
            <span className="text-ink-soft">বিপজ্জনক ডোজ ত্রুটি</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-3 w-3 rounded-sm bg-ochre-soft/40 border border-ochre" />
            <span className="text-ink-soft">নিরাপত্তা সতর্কতা / PHI বাদ</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-3 w-3 rounded-sm bg-leaf/20 border border-leaf" />
            <span className="text-ink-soft">যাচাইকৃত প্রাতিষ্ঠানিক গ্রাউন্ডিং (✓)</span>
          </div>
        </div>
      </div>

      {/* =========================================================================
          MODULE 2: Interactive Hallucination Floor Visualizer & Verifier Gate
          ========================================================================= */}
      <div className="rounded-2xl border border-clay-soft/40 bg-gradient-to-b from-clay-soft/10 via-paper to-paper p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between border-b border-bone pb-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-md bg-clay-soft/30 px-2.5 py-0.5 text-[11px] font-mono font-medium text-clay">
                RQ2 EMPIRICAL DISCOVERY
              </span>
              <span className="text-xs text-ink-faint">গবেষণাপত্রের কেন্দ্রীয় আবিষ্কার</span>
            </div>
            <h3 className="mt-2 font-display text-xl text-ink sm:text-2xl">
              রাসায়নিক হ্যালুসিনেশন ফ্লোর ও স্টেজ ৪ ভেরিফায়ার গেট
            </h3>
            <p className="mt-1 text-xs sm:text-sm text-ink-soft">
              কেন শুধু নিখুঁত রিট্রিভাল (Oracle RAG) যথেষ্ট নয় এবং কেন মেকানিক্যাল ভেরিফায়ার এজেন্ট বাধ্যতামূলক?
            </p>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto rounded-xl border border-clay/30 bg-clay/10 px-4 py-2 text-clay">
            <AlertTriangle className="h-5 w-5 shrink-0" />
            <div>
              <div className="text-xs font-semibold">অপরিহার্য ফ্লোর: {RESEARCH_STATS.hallucinationFloor}</div>
              <div className="text-[10px] text-ink-soft">সকল আর্কিটেকচারের জন্য প্রযোজ্য</div>
            </div>
          </div>
        </div>

        {/* Interactive Threshold & Oracle Context Slider */}
        <div className="mt-6 rounded-xl border rule bg-paper p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <span className="text-xs font-semibold text-ink flex items-center gap-1.5">
                <SlidersHorizontal className="h-4 w-4 text-leaf" />
                তথ্য-সংগ্রহ নির্ভুলতা সিমুলেটর (Retrieval Context Quality):
              </span>
              <p className="text-[11px] text-ink-soft mt-0.5">
                স্লাইডার টেনে দেখুন তথ্য-সংগ্রহ যত উন্নতই হোক না কেন, জেনারেটিভ মডেলের রাসায়নিক ত্রুটি একটি নির্দিষ্ট সীমার নিচে নামে না।
              </p>
            </div>
            <div className="font-mono text-sm font-bold text-leaf bg-leaf/10 border border-leaf/30 rounded-lg px-3 py-1 self-start sm:self-auto">
              {sliderContextRatio === 0 ? "Closed-Book (০%)" : sliderContextRatio === 100 ? "Oracle Perfect (১০০%)" : `RAG Retrieval (${toBn(sliderContextRatio)}%)`}
            </div>
          </div>

          <div className="mt-4">
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={sliderContextRatio}
              onChange={(e) => setSliderContextRatio(Number(e.target.value))}
              className="w-full h-2 bg-bone rounded-lg appearance-none cursor-pointer accent-leaf"
            />
            <div className="flex justify-between text-[10px] font-mono text-ink-faint mt-1.5">
              <span>০% (Closed-Book কোনো তথ্য নেই)</span>
              <span>৫০% (সাধারণ RAG রিট্রিভাল)</span>
              <span className="font-semibold text-leaf">১০০% (Oracle নিখুঁত ডকুমেন্ট)</span>
            </div>
          </div>

          {/* Dynamic Model Hallucination Rates Grid */}
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
            {FLOOR_MODELS.map((m) => {
              // Interpolate hallucination rate based on slider
              const rate = m.closedBookHal - (sliderContextRatio / 100) * (m.closedBookHal - m.oracleFloor);
              const isFloorReached = sliderContextRatio >= 90;
              return (
                <div
                  key={m.name}
                  className={cn(
                    "rounded-xl border p-3 text-center transition-all",
                    m.sft ? "border-leaf/40 bg-leaf/5" : "border-bone bg-paper-2"
                  )}
                >
                  <div className="text-[11px] font-semibold text-ink truncate" title={m.name}>
                    {m.name.split(" ")[0]}
                  </div>
                  <div className="mt-2 font-display text-lg tabular font-bold text-clay">
                    {rate.toFixed(2)}%
                  </div>
                  <div className="mt-1 text-[10px] text-ink-faint">
                    {isFloorReached ? (
                      <span className="font-semibold text-clay-dark flex items-center justify-center gap-0.5">
                        <AlertTriangle className="h-2.5 w-2.5" /> ফ্লোর আটকে গেছে
                      </span>
                    ) : (
                      <span>RAG হ্যালুসিনেশন</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* The KrishokTech Stage 4 Verifier Solution Breakdown */}
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Left: The Problem Illustrated */}
          <div className="rounded-xl border rule bg-paper p-5 sm:p-6 space-y-3">
            <div className="flex items-center gap-2 text-clay">
              <ShieldAlert className="h-5 w-5" />
              <h4 className="font-display text-base text-ink">কেন ৪.০৫–৭.০০% হ্যালুসিনেশন ফ্লোর মারাত্মক?</h4>
            </div>
            <p className="text-xs sm:text-sm text-ink-soft leading-relaxed">
              এমনকি যখন এলএলএম-এর প্রম্পটে সঠিক সরকারি নির্দেশিকা হুবহু দেওয়া থাকে (Oracle Context),
              তখনও মডেলগুলো <strong className="text-ink">৪.০৫% থেকে ৭.০০%</strong> ক্ষেত্রে রাসায়নিক সক্রিয় উপাদানের নাম গুলিয়ে ফেলে,
              ডোজ ইনভার্ট করে ফেলে (২ গ্রামকে ২০ গ্রাম বানায়), অথবা PHI (প্রত্যাহার সময়কাল) বাদ দিয়ে দেয়।
            </p>
            <div className="rounded-lg border border-clay-soft/40 bg-clay-soft/10 p-3 text-xs text-clay-dark">
              <strong className="block mb-1">মাঠ পর্যায়ের ঝুঁকি:</strong>
              কৃষিতে ৫% হ্যালুসিনেশনের অর্থ হলো প্রতি ২০ জন কৃষকের মধ্যে ১ জন ভুল কীটনাশক বা বিষাক্ত মাত্রায় ফসল নষ্ট করবেন।
            </div>
          </div>

          {/* Right: The Solution - Stage 4 Verifier Gate */}
          <div className="rounded-xl border border-leaf/40 bg-leaf/5 p-5 sm:p-6 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-leaf">
                <ShieldCheck className="h-5 w-5" />
                <h4 className="font-display text-base text-ink">কৃষক টেকের সমাধান: স্টেজ ৪ ভেরিফায়ার</h4>
              </div>
              <span className="rounded-full bg-leaf/20 px-2.5 py-0.5 text-[10px] font-mono font-bold text-leaf">
                নেট ঝুঁকি: &lt; ০.২%
              </span>
            </div>
            <p className="text-xs sm:text-sm text-ink-soft leading-relaxed">
              উৎপাদিত উত্তর সরাসরি কৃষকের কাছে না পাঠিয়ে স্টেজ ৪ ভেরিফায়ার এজেন্ট একটি কঠোর সিম্বলিক রুলস ও
              নলেজ গ্রাফ ট্রিপল অডিট চালায়। কোনো ডোজ অমিল বা অননুমোদিত উপাদান পেলে তা সাথে সাথে শুদ্ধ করে বা ১৬১২৩ হটলাইনে রেফার করে।
            </p>
            <div className="rounded-lg border border-leaf/30 bg-leaf/10 p-3 text-xs text-leaf">
              <strong className="block mb-1">অডিট ফিল্টারিং রেজাল্ট:</strong>
              ৯৯.৪% বিপজ্জনক রাসায়নিক বিচ্যুতি মেকানিক্যাল গেট দ্বারা নিষ্কাশিত হয়।
            </div>
          </div>
        </div>

        {/* Live Verifier Scanner Interactive Demo */}
        <div className="mt-6 rounded-xl border border-bone bg-paper p-5 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <FlaskConical className="h-4 w-4 text-ochre" />
                <h4 className="font-display text-sm sm:text-base text-ink">
                  লাইভ ভেরিফায়ার অডিট সিমুলেটর (Live Verification Scan)
                </h4>
              </div>
              <p className="text-xs text-ink-soft mt-0.5">
                একটি ৫% সুক্ষ্ম ডোজ ত্রুটিযুক্ত উত্তর কীভাবে স্টেজ ৪ গেট দ্বারা ধরা পড়ে তা সরাসরি পরীক্ষা করুন।
              </p>
            </div>

            <div className="flex items-center gap-2">
              {!isAuditing && auditStep === 0 && (
                <button
                  onClick={handleRunAudit}
                  className="flex items-center gap-2 rounded-lg bg-leaf px-4 py-2 text-xs font-semibold text-paper shadow-xs hover:bg-leaf/90 transition-all cursor-pointer"
                >
                  <Play className="h-3.5 w-3.5 fill-current" />
                  অডিট পরীক্ষা চালান
                </button>
              )}
              {isAuditing && (
                <button
                  disabled
                  className="flex items-center gap-2 rounded-lg bg-leaf/70 px-4 py-2 text-xs font-semibold text-paper cursor-wait"
                >
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                  >
                    <Activity className="h-3.5 w-3.5" />
                  </motion.div>
                  স্ক্যানিং চলছে...
                </button>
              )}
              {auditStep > 0 && !isAuditing && (
                <button
                  onClick={handleResetAudit}
                  className="flex items-center gap-1.5 rounded-lg border rule bg-paper-2 px-3 py-2 text-xs font-medium text-ink-soft hover:text-ink transition-all cursor-pointer"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  পুনরায় সেট করুন
                </button>
              )}
            </div>
          </div>

          {/* Audit Progress Steps Rail */}
          <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-4">
            <AuditStepCard
              stepNumber={1}
              title="১. সত্তা নিষ্কাশন"
              desc="উত্তর থেকে কেমিক্যাল ও ডোজ পার্সিং"
              currentStep={auditStep}
              isComplete={auditStep > 1}
            />
            <AuditStepCard
              stepNumber={2}
              title="২. কেজি ট্রিপল ম্যাচিং"
              desc="DAE ও BARI নলেজ গ্রাফের সাথে তুলনা"
              currentStep={auditStep}
              isComplete={auditStep > 2}
            />
            <AuditStepCard
              stepNumber={3}
              title="৩. হ্যালুসিনেশন শনাক্তকরণ"
              desc="২০ গ্রাম/লিটার (১০× ওভারডোজ) চিহ্নিত"
              currentStep={auditStep}
              isComplete={auditStep > 3}
            />
            <AuditStepCard
              stepNumber={4}
              title="৪. সংশোধন ও অনুমোদন"
              desc="সঠিক ২ গ্রাম/লিটার দিয়ে প্রতিস্থাপন"
              currentStep={auditStep}
              isComplete={auditSuccess}
            />
          </div>

          {/* Audit Log Box */}
          <AnimatePresence mode="wait">
            {auditStep > 0 && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-4 rounded-lg border border-bone bg-paper-2 p-4 font-mono text-xs space-y-2 overflow-hidden"
              >
                <div className="flex items-center justify-between border-b border-bone pb-2 text-[11px] text-ink-faint">
                  <span>AUDIT_LOG_TRACE_ID: #VERIFY_2026_88A</span>
                  <span>STAGE 4 CHEMICAL GATEWAY</span>
                </div>

                {auditStep >= 1 && (
                  <div className="text-ink">
                    <span className="text-ochre-dark">[STEP 1 - PARSE]:</span> Extracted entity: <span className="text-leaf">Mancozeb 80WP</span>, Value: <span className="text-clay font-bold">20.0 g/L</span>, Crop: <span className="text-leaf">Potato</span>
                  </div>
                )}
                {auditStep >= 2 && (
                  <div className="text-ink">
                    <span className="text-ochre-dark">[STEP 2 - KG TRIPLE]:</span> Matching against node <span className="text-leaf">DAE_PEST_1206A0_001</span>. Approved threshold: <span className="text-leaf font-bold">2.0 g/L</span>
                  </div>
                )}
                {auditStep >= 3 && (
                  <div className="text-clay font-semibold">
                    <span className="text-clay">[STEP 3 - VIOLATION]:</span> Delta +900% detected! Residual hallucination intercepted prior to output emission.
                  </div>
                )}
                {auditStep >= 4 && (
                  <div className="text-leaf font-semibold flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    <span>[STEP 4 - REMEDIATION]: Corrected payload to safe 2.0 g/L with DAE citation. Verdict: ALLOW_MODIFIED (100% Safe).</span>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------
   Helper Component: Model Response Display Card
   ------------------------------------------------------------------------- */
function ModelResponseCard({ model, modelKey }: { model: ModelResponseData; modelKey: ModelKey }) {
  return (
    <div
      className={cn(
        "flex flex-col justify-between rounded-xl border p-5 transition-all shadow-xs",
        modelKey === "grounded_rag"
          ? "border-leaf/50 bg-paper ring-1 ring-leaf/20"
          : modelKey === "sft"
          ? "border-ochre-soft/40 bg-paper"
          : "border-clay-soft/40 bg-paper"
      )}
    >
      <div>
        {/* Card Header */}
        <div className="flex items-start justify-between gap-2 border-b rule pb-3">
          <div>
            <span className={cn("inline-flex items-center rounded-md border px-2 py-0.5 text-[10px] font-medium", model.badgeColor)}>
              {model.badge}
            </span>
            <h4 className="mt-1.5 font-display text-base font-semibold text-ink">{model.modelName}</h4>
          </div>

          <div className="text-right">
            <span className="text-[10px] font-mono text-ink-faint block">সেফটি স্কোর</span>
            <span
              className={cn(
                "font-display text-lg tabular font-bold",
                model.chemicalSafetyScore >= 90
                  ? "text-leaf"
                  : model.chemicalSafetyScore >= 70
                  ? "text-ochre-dark"
                  : "text-clay"
              )}
            >
              {toBn(model.chemicalSafetyScore)}%
            </span>
          </div>
        </div>

        {/* Metrics Row */}
        <div className="mt-3 grid grid-cols-3 gap-2 rounded-lg bg-paper-2 p-2.5 text-center text-xs">
          <div>
            <span className="text-[10px] text-ink-faint block">GenF1</span>
            <span className="font-mono font-semibold text-ink">{model.genF1.toFixed(3)}</span>
          </div>
          <div>
            <span className="text-[10px] text-ink-faint block">হ্যালুসিনেশন</span>
            <span className={cn("font-mono font-semibold", model.hallucinationRate > 20 ? "text-clay" : "text-ink")}>
              {model.hallucinationRate.toFixed(1)}%
            </span>
          </div>
          <div>
            <span className="text-[10px] text-ink-faint block">সাইটেশন</span>
            <span className="font-mono font-semibold text-leaf">{toBn(model.citationsCount)}টি সোর্স</span>
          </div>
        </div>

        {/* Response Text with Annotated Semantic Spans */}
        <div className="mt-4 space-y-2">
          <span className="text-[11px] font-mono font-medium text-ink-faint block uppercase">মডেলের উৎপাদিত উত্তর:</span>
          <div className="rounded-lg border border-bone bg-paper-2/60 p-3.5 text-xs sm:text-[13px] leading-relaxed text-ink font-sans whitespace-pre-wrap">
            {model.segments.map((seg, idx) => {
              if (seg.type === "hallucination") {
                return (
                  <span
                    key={idx}
                    className="relative group rounded bg-clay-soft/30 px-1 py-0.5 text-clay-dark font-medium border-b border-clay cursor-help inline-block my-0.5"
                  >
                    {seg.text}
                    {seg.annotation && (
                      <span className="pointer-events-none absolute bottom-full left-0 z-30 mb-1 hidden w-64 rounded-lg bg-ink p-2 text-[11px] font-normal leading-tight text-paper shadow-lg group-hover:block">
                        {seg.annotation}
                      </span>
                    )}
                  </span>
                );
              }
              if (seg.type === "dosage_error") {
                return (
                  <span
                    key={idx}
                    className="relative group rounded bg-clay/20 px-1 py-0.5 text-clay font-bold border-b-2 border-clay cursor-help inline-block my-0.5"
                  >
                    {seg.text}
                    {seg.annotation && (
                      <span className="pointer-events-none absolute bottom-full left-0 z-30 mb-1 hidden w-64 rounded-lg bg-ink p-2 text-[11px] font-normal leading-tight text-paper shadow-lg group-hover:block">
                        {seg.annotation}
                      </span>
                    )}
                  </span>
                );
              }
              if (seg.type === "warning") {
                return (
                  <span
                    key={idx}
                    className="relative group rounded bg-ochre-soft/40 px-1 py-0.5 text-ochre-dark font-medium border-b border-ochre cursor-help inline-block my-0.5"
                  >
                    {seg.text}
                    {seg.annotation && (
                      <span className="pointer-events-none absolute bottom-full left-0 z-30 mb-1 hidden w-64 rounded-lg bg-ink p-2 text-[11px] font-normal leading-tight text-paper shadow-lg group-hover:block">
                        {seg.annotation}
                      </span>
                    )}
                  </span>
                );
              }
              if (seg.type === "grounded") {
                return (
                  <span
                    key={idx}
                    className="relative group rounded bg-leaf/15 px-1 py-0.5 text-leaf-dark font-medium border-b border-leaf cursor-help inline-block my-0.5"
                  >
                    {seg.text}
                    {seg.annotation && (
                      <span className="pointer-events-none absolute bottom-full left-0 z-30 mb-1 hidden w-64 rounded-lg bg-ink p-2 text-[11px] font-normal leading-tight text-paper shadow-lg group-hover:block">
                        {seg.annotation}
                        {seg.sourceCitation && (
                          <span className="block mt-1 font-mono text-[9px] text-leaf">
                            উৎস: {seg.sourceCitation}
                          </span>
                        )}
                      </span>
                    )}
                  </span>
                );
              }
              return <span key={idx}>{seg.text}</span>;
            })}
          </div>
        </div>

        {/* Key Diagnostic Insights */}
        <div className="mt-4 space-y-1.5">
          <span className="text-[10px] font-mono uppercase font-semibold text-ink-faint">প্রধান মূল্যায়ন:</span>
          {model.keyInsights.map((insight, idx) => (
            <div key={idx} className="flex items-start gap-1.5 text-xs text-ink-soft">
              <span className="text-ink-faint mt-0.5">•</span>
              <span>{insight}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Card Footer: Verifier Gate Status */}
      <div
        className={cn(
          "mt-5 rounded-lg border p-3 text-xs flex items-start gap-2",
          model.verifierStatus === "passed"
            ? "border-leaf/30 bg-leaf/10 text-leaf"
            : model.verifierStatus === "warning"
            ? "border-ochre-soft/40 bg-ochre-soft/10 text-ochre-dark"
            : "border-clay-soft/40 bg-clay-soft/10 text-clay"
        )}
      >
        {model.verifierStatus === "passed" ? (
          <CheckCircle2 className="h-4 w-4 shrink-0 mt-0.5" />
        ) : model.verifierStatus === "warning" ? (
          <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
        ) : (
          <XCircle className="h-4 w-4 shrink-0 mt-0.5" />
        )}
        <div>
          <span className="font-semibold block">
            {model.verifierStatus === "passed"
              ? "স্টেজ ৪ গেট: অনুমোদিত"
              : model.verifierStatus === "warning"
              ? "স্টেজ ৪ গেট: সতর্কীকরণ সহ পাস"
              : "স্টেজ ৪ গেট: প্রত্যাখ্যান / ব্লকিং"}
          </span>
          <span className="text-[11px] opacity-90 leading-tight block mt-0.5">{model.verifierMessage}</span>
        </div>
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------
   Helper Component: Audit Step Card
   ------------------------------------------------------------------------- */
function AuditStepCard({
  stepNumber,
  title,
  desc,
  currentStep,
  isComplete,
}: {
  stepNumber: number;
  title: string;
  desc: string;
  currentStep: number;
  isComplete: boolean;
}) {
  const isActive = currentStep === stepNumber;
  return (
    <div
      className={cn(
        "rounded-xl border p-3 transition-all",
        isActive
          ? "border-ochre bg-ochre-soft/20 shadow-xs ring-1 ring-ochre/40"
          : isComplete
          ? "border-leaf/40 bg-leaf/5"
          : "border-bone bg-paper-2 opacity-60"
      )}
    >
      <div className="flex items-center justify-between">
        <span className={cn("text-[10px] font-mono font-semibold", isActive ? "text-ochre-dark" : isComplete ? "text-leaf" : "text-ink-faint")}>
          STEP 0{stepNumber}
        </span>
        {isComplete && <Check className="h-3 w-3 text-leaf" />}
      </div>
      <div className="mt-1 text-xs font-semibold text-ink">{title}</div>
      <div className="mt-0.5 text-[10px] text-ink-soft leading-tight">{desc}</div>
    </div>
  );
}
