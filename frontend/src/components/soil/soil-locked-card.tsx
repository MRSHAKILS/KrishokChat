"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Lock, ChevronDown, FlaskConical, MessageCircle, Droplets, CheckCircle2, AlertTriangle, Info, Sparkles } from "lucide-react";
import type { SoilDatasetInfo, SoilAnalyzeResponse } from "@/lib/api";
import { bn, numLocale } from "@/lib/bn";
import { dur, ease } from "@/lib/motion";
import { useLanguage } from "@/context/language-context";

interface AgronomicSoilState {
  badgeTitle: string;
  badgeDesc: string;
  tone: "leaf" | "ochre" | "clay" | "sky";
  irrigationAction: string;
  squeezeTest: string;
}

function getSoilAgronomicState(kpa: number, english = false): AgronomicSoilState {
  if (english) {
    if (kpa < 2.0) {
      return {
        badgeTitle: "Waterlogged",
        badgeDesc: "The soil is saturated. Extra water can rot roots.",
        tone: "sky",
        irrigationAction: "Stop irrigation and open the drains",
        squeezeTest: "A squeezed handful drips muddy water.",
      };
    }
    if (kpa <= 10.0) {
      return {
        badgeTitle: "Good working moisture",
        badgeDesc: "Moisture is in a range plants can use.",
        tone: "leaf",
        irrigationAction: "No irrigation needed now",
        squeezeTest: "A handful forms a ball without coating the hand in mud.",
      };
    }
    if (kpa <= 15.0) {
      return {
        badgeTitle: "Drying — watch",
        badgeDesc: "The surface is drying and moisture is falling.",
        tone: "ochre",
        irrigationAction: "Plan a light irrigation in the next one or two days",
        squeezeTest: "A ball forms, then crumbles under light pressure.",
      };
    }
    return {
      badgeTitle: "Severe dry stress",
      badgeDesc: "Available moisture is exhausted. Plants may wilt quickly.",
      tone: "clay",
      irrigationAction: "Irrigate with a moderate amount now",
      squeezeTest: "A handful will not form a ball. It falls apart as dust.",
    };
  }
  if (kpa < 2.0) {
    return {
      badgeTitle: "অতিরিক্ত আর্দ্র / জলমগ্ন অবস্থা",
      badgeDesc: "মাটি পানিতে সম্পৃক্ত — অতিরিক্ত রস শিকড় পচা ঘটাতে পারে",
      tone: "sky",
      irrigationAction: "সেচ সম্পূর্ণ বন্ধ রাখুন ও নিকাশ নালা সচল করুন",
      squeezeTest: "মাটি মুঠো করলে আঙুলের ফাঁক দিয়ে অতিরিক্ত পানি বা কাদা চুইয়ে পড়ে।",
    };
  }
  if (kpa <= 10.0) {
    return {
      badgeTitle: "মাটির আদর্শ 'জো' অবস্থা (Optimum Moisture)",
      badgeDesc: "মাটিতে উদ্ভিদের খাদ্য গ্রহণ ও বৃদ্ধির জন্য চমৎকার রস বিদ্যমান",
      tone: "leaf",
      irrigationAction: "এখনই কোনো সেচ প্রয়োজন নেই",
      squeezeTest: "মাটি হাতে চেপে গোল লাড্ডু করলে সহজে বল বাঁধে, হাত কাদা হয় না এবং মাটিতে ধুলো ওড়ে না।",
    };
  }
  if (kpa <= 15.0) {
    return {
      badgeTitle: "হালকা রস সংকট / শুকনা টান (Watch State)",
      badgeDesc: "মাটির উপরিভাগে শুকনা ভাব দেখা দিয়েছে, রস দ্রুত কমছে",
      tone: "ochre",
      irrigationAction: "আগামী ১-২ দিনের মধ্যে হালকা সেচের প্রস্তুতি নিন",
      squeezeTest: "মুঠো করলে লাড্ডু হয় কিন্তু সামান্য মৃদু আঘাতেই ভেঙে গুঁড়ো হয়ে যায়।",
    };
  }
  return {
    badgeTitle: "তীব্র খরা / শুষ্ক মাটি (Severe Stress)",
    badgeDesc: "মাটির রস পুরোপুরি নিঃশেষিত — গাছ দ্রুত নুয়ে পড়ার ঝুঁকি",
    tone: "clay",
    irrigationAction: "অবিলম্বে পরিমিত সেচ প্রয়োগ করুন",
    squeezeTest: "মাটি মুঠো করলে কোনো বল বা লাড্ডু বাঁধে না, ধুলোর মতো ঝরে পড়ে।",
  };
}

export function SoilLockedCard({
  info,
  result,
  message,
  onAskChat,
}: {
  info: SoilDatasetInfo | null;
  result?: SoilAnalyzeResponse | null;
  message?: string | null;
  onAskChat?: () => void;
}) {
  const { locale } = useLanguage();
  const en = locale === "en";
  const [showTable, setShowTable] = useState(false);
  const [showSqueezeGuide, setShowSqueezeGuide] = useState(false);
  const models = info?.model_results ?? [];

  // If the result is an analyzed (measured-sample replay), render the diagnostic card.
  if (result && result.status === "analyzed") {
    const isReplay = Boolean(result.sample_id);
    const kpa = result.kpa;
    const soilType = en ? (result.soil_type ?? result.soil_type_bn ?? "") : (result.soil_type_bn ?? result.soil_type ?? "");
    const advisory = result.advisory_bn ?? "";
    if (kpa == null || !soilType || !advisory) {
      // Defensive: a malformed analyzed payload must not invent values.
      return null;
    }

    const agro = getSoilAgronomicState(kpa, en);
    const toneBorder =
      agro.tone === "clay"
        ? "border-clay/40"
        : agro.tone === "ochre"
        ? "border-ochre/40"
        : agro.tone === "sky"
        ? "border-sky-600/40"
        : "border-leaf/40";

    const toneBg =
      agro.tone === "clay"
        ? "bg-clay/10 text-clay"
        : agro.tone === "ochre"
        ? "bg-ochre/10 text-ochre"
        : agro.tone === "sky"
        ? "bg-sky-600/10 text-sky-700"
        : "bg-leaf/10 text-leaf";

    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: dur.normal, ease: ease.smooth }}
        className={`overflow-hidden rounded-2xl border ${toneBorder} bg-paper shadow-[0_12px_32px_rgba(34,70,44,0.08)]`}
      >
        <div className="p-5 sm:p-6">
          {/* Header */}
          <div className="flex items-start justify-between gap-3 border-b rule pb-4">
            <div className="flex items-center gap-3">
              <div className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${toneBg}`}>
                <Droplets className="h-6 w-6" strokeWidth={1.75} />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="font-display text-lg font-bold text-ink">{en ? "Soil moisture and irrigation" : "মাটির আর্দ্রতা ও সেচ বিশ্লেষণ"}</h3>
                  {isReplay ? (
                    <span
                      className="inline-flex items-center gap-1 rounded-full bg-sky-600/10 px-2.5 py-0.5 text-xs font-semibold text-sky-700"
                      title={en ? "Record measured in the field at the Pabna research site" : "পাবনা রিসার্চ সাইটের মাঠে পরিমাপিত রেকর্ড"}
                    >
                      <FlaskConical className="h-3 w-3" /> {en ? "Dataset sample" : "ডেটাসেট নমুনা"} {result.sample_id}
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 rounded-full bg-leaf/15 px-2.5 py-0.5 text-xs font-semibold text-leaf">
                      <Sparkles className="h-3 w-3" /> {en ? "Estimated" : "নির্ণীত"}
                    </span>
                  )}
                </div>
                <p className="text-xs text-ink-soft">{en ? "Grounded in Pabna field sensors · scientific tension and the farmer's familiar ‘jo’ state" : "পাবনা ফিল্ড সেন্সর গ্রাউন্ডেড · বৈজ্ঞানিক টেনশন ও কৃষকের 'জো' অবস্থা"}</p>
              </div>
            </div>
            <div className="text-right">
              <span className="text-xs font-medium text-ink-faint">{en ? "Source" : "উৎস"}</span>
              <div className="font-display text-sm font-bold text-leaf">{isReplay ? (en ? "Field record" : "মাঠ রেকর্ড") : numLocale(Math.round((result.confidence ?? 0) * 100), en) + "%"}</div>
            </div>
          </div>

          {/* Practical Agronomic Condition Headline Banner */}
          <div className={`mt-4 rounded-xl border ${toneBorder} ${toneBg} p-4`}>
            <div className="flex items-center justify-between gap-2">
              <span className="text-xs font-bold uppercase tracking-wider">{en ? "Current field condition:" : "মাঠের বর্তমান অবস্থা:"}</span>
              <span className="rounded-full bg-paper px-2.5 py-0.5 text-xs font-bold shadow-2xs">
                {agro.irrigationAction}
              </span>
            </div>
            <h4 className="mt-1 font-display text-lg font-bold">{agro.badgeTitle}</h4>
            <p className="mt-0.5 text-xs leading-relaxed opacity-90">{agro.badgeDesc}</p>
          </div>

          {/* Key Metrics Grid */}
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
            {/* Metric 1: Agronomic 'Jo' Status */}
            <div className="rounded-xl border rule bg-paper-2 p-3.5 text-center">
              <span className="text-xs font-medium text-ink-faint">{en ? "Farmer indicator" : "কৃষক নির্দেশক"}</span>
              <div className="mt-1 font-display text-base font-bold text-ink">
                {agro.badgeTitle.split("(")[0].trim()}
              </div>
              <div className="mt-1 text-xs font-semibold text-leaf">
                {agro.irrigationAction}
              </div>
            </div>

            {/* Metric 2: Soil Classification */}
            <div className="rounded-xl border rule bg-paper-2 p-3.5 text-center">
              <span className="text-xs font-medium text-ink-faint">{isReplay ? (en ? "Sample soil type" : "নমুনা মাটির ধরন") : (en ? "Identified soil type" : "শনাক্তকৃত মাটির ধরন")}</span>
              <div className="mt-1 font-display text-lg font-bold text-ink">{soilType}</div>
              <span className="mt-1 inline-block text-xs text-ink-soft">{result.soil_type || ""}</span>
            </div>

            {/* Metric 3: Scientific Tension in kPa */}
            <div className="rounded-xl border rule bg-paper-2 p-3.5 text-center">
              <span className="text-xs font-medium text-ink-faint">{en ? "Scientific moisture tension" : "বৈজ্ঞানিক আর্দ্রতা টান"}</span>
              <div className="mt-1 font-display text-2xl font-black text-ink">
                {numLocale(kpa.toFixed(1), en)} <span className="text-xs font-normal text-ink-soft">kPa</span>
              </div>
              <span className="mt-1 inline-block text-[11px] text-ink-faint">{en ? "Ideal range: 2.0–10.0 kPa" : "আদর্শ মাত্রা: ২.০–১০.০ kPa"}</span>
            </div>
          </div>

          {/* Actionable Irrigation Advisory */}
          <div className="mt-4 rounded-xl border border-leaf/30 bg-leaf/5 p-4">
            <h4 className="flex items-center gap-1.5 text-xs font-bold text-ink">
              <Info className="h-4 w-4 text-leaf" />
              {en ? "Field-level irrigation and care recommendation:" : "মাঠ পর্যায়ের সেচ ও পরিচর্যা সুপারিশ:"}
            </h4>
            <p className="mt-2 text-sm leading-relaxed text-ink-soft">{advisory}</p>
          </div>

          {/* Traditional Field Squeeze Test Helper */}
          <div className="mt-4 rounded-xl border rule bg-paper-2/40 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-bold text-ink">
                <CheckCircle2 className="h-4 w-4 text-leaf" />
                {en ? "Standing-in-the-field soil squeeze test (Squeeze Test Guide):" : "মাঠে দাঁড়িয়ে মাটি মুঠো পরীক্ষা (Squeeze Test Guide):"}
              </div>
              <button
                type="button"
                onClick={() => setShowSqueezeGuide((v) => !v)}
                className="text-xs font-semibold text-leaf hover:underline cursor-pointer"
              >
                {showSqueezeGuide ? (en ? "Collapse" : "সংক্ষেপ করুন") : (en ? "How to test?" : "কীভাবে পরীক্ষা করবেন?")}
              </button>
            </div>
            <p className="mt-1.5 text-xs leading-relaxed text-ink-soft">
              <strong>{en ? "This soil's feel:" : "এই মাটির স্পর্শ লক্ষণ:"}</strong> {agro.squeezeTest}
            </p>
            {showSqueezeGuide && (
              <div className="mt-3 border-t border-dashed border-bone pt-2 text-xs leading-relaxed text-ink-faint space-y-1">
                {en ? (
                  <>
                    <p>1. Take a handful of soil from the root zone (2–3 inches deep).</p>
                    <p>2. Squeeze it firmly in your palm and try to form a ball.</p>
                    <p>3. If the ball holds together, the field has enough moisture (‘jo’); if it crumbles apart as soon as you open your hand, irrigate right away.</p>
                  </>
                ) : (
                  <>
                    <p>১. ফসলের মূল এলাকা (মাটির ২-৩ ইঞ্চি গভীর) থেকে একমুঠো মাটি নিন।</p>
                    <p>২. হাতের তালুতে শক্ত করে চেপে গোল লাড্ডু বানানোর চেষ্টা করুন।</p>
                    <p>৩. লাড্ডু স্বাভাবিকভাবে জমে থাকলে জমিতে পর্যাপ্ত রস ('জো') আছে; মুঠো খুলতেই ভেঙে গুঁড়ো হয়ে গেলে জরুরি সেচ দিন।</p>
                  </>
                )}
              </div>
            )}
          </div>

          {/* Ask in Chat Action */}
          {onAskChat && (
            <button
              onClick={onAskChat}
              className="mt-4 flex min-h-11 w-full items-center justify-center gap-2 rounded-xl bg-leaf px-4 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
            >
              <MessageCircle className="h-4 w-4" />
              {en ? "Talk in chat about irrigation and fertilizer management for this soil" : "এই মাটির সেচ ও সার ব্যবস্থাপনা নিয়ে চ্যাটে কথা বলুন"}
            </button>
          )}
        </div>
      </motion.div>
    );
  }

  // Fallback: Honest Locked Card
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="overflow-hidden rounded-2xl border border-ochre-soft/60 bg-ochre-soft/10 shadow-[0_10px_28px_rgba(52,39,23,0.05)]"
    >
      <div className="p-5 sm:p-6">
        <div className="flex items-start gap-3.5">
          <motion.div
            initial={{ scale: 0.85, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 18, delay: 0.1 }}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-ochre/15 text-ochre"
          >
            <Lock className="h-5 w-5" strokeWidth={1.5} />
          </motion.div>
          <div className="flex-1">
            <h3 className="font-display text-lg font-bold text-ink">{en ? "Live camera diagnosis in testing · field dataset analysis is live" : "সরাসরি ক্যামেরা নির্ণয় পরীক্ষাধীন · ফিল্ড ডেটাসেট বিশ্লেষণ চালু"}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-soft">
              {message ??
                (en
                  ? "The computer-vision model that reads a photo to determine exact soil moisture is still under field research. To avoid false or risky irrigation advice, only analysis of the measured Pabna field tensiometer samples and chat-based advice are live for now."
                  : "ছবি দেখে মাটির সঠিক আর্দ্রতা নির্ণয়ের কম্পিউটার ভিশন মডেল বর্তমানে মাঠ গবেষণাধীন। অসত্য বা ঝুঁকিপূর্ণ সেচ পরামর্শ রোধে শুধুমাত্র পাবনা ফিল্ড টেনশিওমিটারের পরিমাপিত নমুনাসমূহের বিশ্লেষণ ও চ্যাটে পরামর্শ সরাসরি চালু রয়েছে।")}
            </p>
          </div>
        </div>

        {/* Traditional Farmer Tip Card */}
        <div className="mt-4 rounded-xl border border-leaf/30 bg-paper p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-leaf">
            <CheckCircle2 className="h-4 w-4" />
            {en ? "A simple way to gauge soil moisture in the field (soil squeeze test):" : "মাঠে দাঁড়িয়ে মাটির আর্দ্রতা বোঝার সহজ কৌশল (মাটি মুঠো পরীক্ষা):"}
          </div>
          <p className="mt-1.5 text-xs leading-relaxed text-ink-soft">
            {en
              ? "Take a handful of soil from 2–3 inches below the base of the crop and squeeze it firmly. If it forms a normal ball and your hand doesn't get muddy, the field has adequate ‘jo’ moisture and no irrigation is needed right now. If it won't hold together and crumbles apart, irrigate."
              : "ফসলের গোড়ার ২-৩ ইঞ্চি গভীর থেকে একমুঠো মাটি হাতে নিয়ে শক্ত করে চেপে দেখুন। যদি মাটি স্বাভাবিক গোল বল বাঁধে এবং হাত কাদা না হয়, তবে জমিতে উপযুক্ত 'জো' অবস্থা রয়েছে এবং এখনই সেচের প্রয়োজন নেই। মাটি মুঠো না বেঁধে ভেঙে গুঁড়ো হয়ে ঝরে গেলে সেচ দিন।"}
          </p>
        </div>

        {/* Honest benchmark table */}
        {models.length > 0 && (
          <div className="mt-4 rounded-xl border rule bg-paper p-4">
            <div className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1.5 text-xs font-semibold text-ink">
                <FlaskConical className="h-3.5 w-3.5 text-ochre" />
                {en ? "Current research results and dataset metrics" : "গবেষণার বর্তমান ফলাফল ও ডেটাসেট মেট্রিক্স"}
              </span>
              <button
                onClick={() => setShowTable((v) => !v)}
                className="flex items-center gap-1 text-xs font-medium text-leaf hover:text-leaf-2"
                aria-expanded={showTable}
              >
                {showTable ? (en ? "Hide" : "লুকান") : (en ? `View ${models.length} models` : `${bn(models.length)}টি মডেল দেখুন`)}
                <ChevronDown className={`h-3 w-3 transition-transform ${showTable ? "rotate-180" : ""}`} />
              </button>
            </div>
            <p className="mt-1.5 text-xs leading-relaxed text-ink-faint">
              {en ? "Comparative RMSE scores of image features against 722 digital tensiometer measurements." : "৭২২টি ডিজিটাল টেনশিওমিটার পরিমাপের সাথে ইমেজ ফিচারের তুলনামূলক আরএমএসই (RMSE) স্কোর।"}
            </p>
            <AnimatePresence initial={false}>
              {showTable && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: dur.normal, ease: ease.smooth }}
                  className="overflow-hidden"
                >
                  <div className="mt-3 overflow-x-auto">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="border-b rule text-xs text-ink-faint">
                          <th className="py-2 pr-3 font-medium">{en ? "Model" : "মডেল"}</th>
                          <th className="py-2 pr-3 text-right font-medium">RMSE (kPa)</th>
                          <th className="py-2 text-right font-medium">R²</th>
                        </tr>
                      </thead>
                      <tbody>
                        {models.map((m) => (
                          <tr key={m.model} className="border-b border-bone/50 last:border-0">
                            <td className="py-2 pr-3 text-ink-soft">{m.model}</td>
                            <td className="py-2 pr-3 text-right tabular text-ink">{numLocale(m.rmse_kpa.toFixed(2), en)}</td>
                            <td className="py-2 text-right tabular text-clay">{numLocale(m.r2.toFixed(2), en)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}

        {/* What you CAN do now */}
        {onAskChat && (
          <button
            onClick={onAskChat}
            className="mt-4 flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
          >
            <MessageCircle className="h-4 w-4" />
            {en ? "Ask about soil and water in chat" : "মাটি ও পানি নিয়ে চ্যাটে প্রশ্ন করুন"}
          </button>
        )}
      </div>
    </motion.div>
  );
}