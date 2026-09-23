"use client";

import { motion } from "motion/react";
import { CheckCircle, HelpCircle, ImageIcon, XCircle, AlertTriangle, Leaf, X } from "lucide-react";
import { enter } from "@/lib/motion";
import { bnPercent, humanizeLabel, diseaseCore, cleanKnowledgeText, translateDiseaseToBn, cropBn } from "@/lib/bn";
import { HELPLINE, HELPLINE_EN } from "@/lib/constants";
import { ConfidenceMeter } from "./confidence-meter";
import type { DetectResponse } from "@/lib/api";
import { useLanguage } from "@/context/language-context";
import { getLocalizedDisease } from "@/lib/i18n/disease-knowledge";

/* =========================================================================
   DiagnosisCard — renders one of 6 honest states based on backend status.
   Fully localized for both Bengali and fluent, natural English.
   ========================================================================= */

export function DiagnosisCard({
  result,
  onClear,
  onSelectCrop,
  onSelectDisease,
}: {
  result: DetectResponse;
  onClear?: () => void;
  onSelectCrop?: (crop: string) => void;
  onSelectDisease?: (disease: string) => void;
}) {
  const status = result.status ?? inferStatus(result);

  switch (status) {
    case "diagnosed":
      return <DiagnosedCard result={result} onClear={onClear} />;
    case "healthy":
      return <HealthyCard result={result} />;
    case "uncertain":
      return (
        <UncertainClarificationCard
          result={result}
          onSelectCrop={onSelectCrop}
          onSelectDisease={onSelectDisease}
          onClear={onClear}
        />
      );
    case "requires_second_image":
      return <SecondImageCard result={result} onClear={onClear} />;
    case "out_of_distribution":
      return <OutOfDistributionCard result={result} onClear={onClear} />;
    case "not_recognized":
      return <NotRecognizedCard result={result} />;
    case "no_disease_model":
      return <NoModelCard result={result} />;
    case "invalid_image":
      return <InvalidImageCard result={result} />;
    case "model_error":
      return (
        <ModelErrorCard
          result={result}
          onSelectCrop={onSelectCrop}
          onSelectDisease={onSelectDisease}
          onClear={onClear}
        />
      );
    default:
      return (
        <ModelErrorCard
          result={result}
          onSelectCrop={onSelectCrop}
          onSelectDisease={onSelectDisease}
          onClear={onClear}
        />
      );
  }
}

function inferStatus(result: DetectResponse): string {
  if (result.disease_info || result.treatment_advice || result.disease) {
    if (result.disease && /healthy/i.test(result.disease)) return "healthy";
    return "diagnosed";
  }
  if (result.crop && result.crop_confidence < 0.6) return "not_recognized";
  if (result.error) return "model_error";
  return "not_recognized";
}

/* --- 1. DIAGNOSED — the full diagnosis ---------------------------------- */

function DiagnosedCard({ result, onClear }: { result: DetectResponse; onClear?: () => void }) {
  const { t, locale, localizeCrop, localizeDisease } = useLanguage();
  const info = result.disease_info;

  const localizedKnowledge = getLocalizedDisease(result.disease, locale);

  const rawDiseaseName = result.disease ? humanizeLabel(result.disease) : "";
  const diseaseTitle =
    locale === "bn"
      ? result.disease
        ? translateDiseaseToBn(result.disease)
        : (info?.class_name ?? "")
      : localizedKnowledge?.nameEn ?? rawDiseaseName ?? diseaseCore(result.disease ?? "");

  const descText =
    locale === "en" && localizedKnowledge?.descEn
      ? localizedKnowledge.descEn
      : cleanKnowledgeText(info?.description_bn ?? "");

  const causeText =
    locale === "en" && localizedKnowledge?.causeEn
      ? localizedKnowledge.causeEn
      : cleanKnowledgeText(info?.cause_bn ?? "");

  const solText =
    locale === "en" && localizedKnowledge?.solutionEn
      ? localizedKnowledge.solutionEn
      : cleanKnowledgeText(info?.solution_bn ?? "");

  const cropDisplay = localizeCrop(result.crop);

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="overflow-hidden rounded-xl border rule bg-paper"
    >
      {/* Header: crop + disease */}
      <div className="space-y-3 p-5">
        {onClear && (
          <div className="flex justify-end">
            <button
              type="button"
              onClick={onClear}
              aria-label={t.diagnosis.clear}
              className="flex min-h-9 items-center gap-1.5 rounded-lg px-2.5 text-xs text-ink-faint transition-colors hover:bg-paper-2 hover:text-ink cursor-pointer"
            >
              <X className="h-3.5 w-3.5" />
              {t.diagnosis.clear}
            </button>
          </div>
        )}
        <div className="flex items-start gap-3">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
            <Leaf className="h-5 w-5" strokeWidth={1.5} />
          </div>
          <div className="flex-1 space-y-2.5">
            <div className="flex items-center gap-2">
              <span className="rounded-md bg-leaf/10 px-2 py-0.5 text-xs font-semibold text-leaf">
                {cropDisplay || (result.crop ?? "—")}
              </span>
              {result.crop_source === "user" && (
                <span className="rounded-md bg-paper-2 px-1.5 py-0.5 text-xs font-medium text-ink-faint">
                  {t.diagnosis.selectedCrop}
                </span>
              )}
            </div>
            {result.crop_source === "user" ? (
              <div className="text-xs text-ink-faint">
                {locale === "en"
                  ? `Analyzed using ${cropDisplay} disease models according to your selection`
                  : `আপনার নির্বাচন অনুযায়ী ${cropDisplay} রোগ মডেল দিয়ে বিশ্লেষণ হয়েছে`}
              </div>
            ) : (
              <ConfidenceMeter value={result.crop_confidence} label={t.diagnosis.cropConfidence} tone="leaf" compact />
            )}
          </div>
        </div>

        <div className="border-t rule pt-3">
          <h3 className="font-display text-xl text-ink">{diseaseTitle}</h3>
          {rawDiseaseName && diseaseTitle !== rawDiseaseName && (
            <p className="mt-0.5 text-xs text-ink-faint font-mono">{rawDiseaseName}</p>
          )}
          <div className="mt-2.5">
            <ConfidenceMeter
              value={result.disease_confidence}
              label={t.diagnosis.diseaseConfidence}
              tone={result.disease_confidence > 0.85 ? "leaf" : "ochre"}
              compact
            />
          </div>
        </div>
      </div>

      {/* Body: description + cause + solution */}
      {(descText || causeText || solText) && (
        <div className="space-y-4 border-t rule p-5">
          {descText && (
            <div>
              <div className="mb-1.5 text-xs font-semibold text-ink-faint">
                {t.diagnosis.description}
              </div>
              <p className="text-sm leading-relaxed text-ink-soft">{descText}</p>
            </div>
          )}
          {causeText && (
            <div>
              <div className="mb-1.5 text-xs font-semibold text-ink-faint">
                {t.diagnosis.cause}
              </div>
              <p className="text-sm leading-relaxed text-ink-soft">{causeText}</p>
            </div>
          )}
          {solText && (
            <div className="rounded-lg border border-leaf/20 bg-leaf/5 p-4">
              <div className="mb-1.5 text-xs font-semibold text-leaf">
                {t.diagnosis.primarySolution}
              </div>
              <p className="text-sm leading-relaxed text-ink">{solText}</p>
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
}

/* --- 2. HEALTHY — the positive reassurance ------------------------------ */

function HealthyCard({ result }: { result: DetectResponse }) {
  const { t, formatPercent, localizeCrop } = useLanguage();
  const cropDisplay = localizeCrop(result.crop);

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border rule bg-leaf/5 p-6 text-center"
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: "spring", stiffness: 280, damping: 20, delay: 0.1 }}
        className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-leaf/15 text-leaf"
      >
        <CheckCircle className="h-7 w-7" strokeWidth={1.5} />
      </motion.div>
      <h3 className="mt-4 font-display text-xl text-ink">{t.diagnosis.healthyTitle}</h3>
      <p className="mx-auto mt-2 max-w-xs text-sm leading-relaxed text-ink-soft">
        {t.diagnosis.healthyDesc}
        {result.crop && (
          <>
            {" "}
            {t.diagnosis.healthyDetected}{" "}
            <strong className="text-ink">{cropDisplay}</strong> ({formatPercent(result.crop_confidence)})
          </>
        )}
      </p>
      <p className="mt-3 text-xs text-ink-faint">
        {t.diagnosis.healthyCare}
      </p>
    </motion.div>
  );
}

/* --- 3. NOT_RECOGNIZED — honest uncertainty ----------------------------- */

function NotRecognizedCard({ result }: { result: DetectResponse }) {
  const { t, locale, formatPercent } = useLanguage();

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border rule bg-paper p-6 text-center"
    >
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-ochre-soft/40 text-ochre">
        <HelpCircle className="h-7 w-7" strokeWidth={1.5} />
      </div>
      <h3 className="mt-4 font-display text-xl text-ink">{t.diagnosis.notRecognizedTitle}</h3>
      <p className="mx-auto mt-2 max-w-xs text-sm leading-relaxed text-ink-soft">
        {t.diagnosis.notRecognizedDesc} ({formatPercent(result.crop_confidence || result.disease_confidence)}).
      </p>
      <div className="mt-4 space-y-2 text-left">
        <p className="text-sm text-ink-soft">{t.diagnosis.nextSteps}</p>
        <div className="rounded-lg border rule bg-paper-2/40 p-3 text-xs text-ink-soft">
          {t.diagnosis.stepCloserPhoto}
        </div>
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="flex items-center gap-2 rounded-lg border rule bg-paper p-3 text-xs text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
        >
          {t.diagnosis.stepCallHelpline}
          <span className="ml-auto tabular font-semibold text-leaf">{locale === "en" ? HELPLINE_EN.krishiCallCenter : HELPLINE.krishiCallCenter}</span>
        </a>
      </div>
    </motion.div>
  );
}

/* --- 4. NO_DISEASE_MODEL — honest gap ----------------------------------- */

function NoModelCard({ result }: { result: DetectResponse }) {
  const { t, locale, formatPercent, localizeCrop } = useLanguage();
  const cropDisplay = localizeCrop(result.crop);

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border rule bg-paper p-6"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
          <Leaf className="h-5 w-5" strokeWidth={1.5} />
        </div>
        <div>
          <div className="font-display text-lg text-ink">{cropDisplay || (result.crop ?? "Crop")}</div>
          <div className="text-xs text-ink-faint tabular">{formatPercent(result.crop_confidence)}</div>
        </div>
      </div>
      <div className="mt-4 border-t rule pt-4">
        <div className="flex items-start gap-2 text-sm text-ink-soft">
          <ImageIcon className="mt-0.5 h-4 w-4 shrink-0 text-ink-faint" />
          <p className="leading-relaxed">
            {t.diagnosis.noModelDesc}
          </p>
        </div>
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="mt-3 flex items-center justify-between rounded-lg border rule bg-paper px-4 py-2.5 text-sm text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
        >
          {t.nav.callCenter}
          <span className="tabular font-semibold text-leaf">{locale === "en" ? HELPLINE_EN.krishiCallCenter : HELPLINE.krishiCallCenter}</span>
        </a>
      </div>
    </motion.div>
  );
}

/* --- 5. INVALID_IMAGE — quality guidance -------------------------------- */

function InvalidImageCard({ result }: { result: DetectResponse }) {
  const { locale } = useLanguage();
  const warnings =
    result.quality_warnings.length > 0
      ? result.quality_warnings
      : [locale === "bn" ? "ছবির গুণমান যথেষ্ট নয়" : "Image quality insufficient for diagnosis"];

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border rule bg-ochre-soft/15 p-6"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-ochre/15 text-ochre">
          <AlertTriangle className="h-5 w-5" strokeWidth={1.5} />
        </div>
        <h3 className="font-display text-lg text-ink">
          {locale === "bn" ? "ছবির গুণমান সতর্কতা" : "Image Quality Notice"}
        </h3>
      </div>

      <ul className="mt-4 space-y-1.5">
        {warnings.map((w, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-ink-soft">
            <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-ochre" />
            {w}
          </li>
        ))}
      </ul>

      <div className="mt-4 border-t border-ochre-soft/40 pt-4">
        <div className="mb-2 text-xs font-semibold text-ink-faint">
          {locale === "bn" ? "উন্নত ছবির জন্য পরামর্শ:" : "Photography Recommendations:"}
        </div>
        <ul className="space-y-1.5 text-xs text-ink-soft">
          <li>• {locale === "bn" ? "দিনের স্বাভাবিক আলোতে ছবি তুলুন" : "Capture in bright natural daylight"}</li>
          <li>• {locale === "bn" ? "আক্রান্ত পাতাটি পুরো ফ্রেমে রাখুন" : "Ensure leaf lesion fills the frame"}</li>
          <li>• {locale === "bn" ? "১৫-২০ সেমি দূরত্ব থেকে পরিষ্কারভাবে তুলুন" : "Hold camera steady 15–20 cm away"}</li>
          <li>• {locale === "bn" ? "একটি আক্রান্ত পাতায় স্পষ্ট ফোকাস রাখুন" : "Keep single symptomatic leaf sharply in focus"}</li>
        </ul>
      </div>
    </motion.div>
  );
}

/* --- 6. MODEL_ERROR — Graceful Resolution with One-Tap Routing -------- */

const CROP_DISEASES: Record<string, { id: string; bn: string; en: string }[]> = {
  rice: [
    { id: "Leaf_Blast", bn: "ব্লাস্ট রোগ (Leaf Blast)", en: "Leaf Blast" },
    { id: "Brown_Spot", bn: "বাদামী দাগ (Brown Spot)", en: "Brown Spot" },
    { id: "Bacterial_Leaf_Blight", bn: "পাতা পোড়া (Blight)", en: "Bacterial Blight" },
  ],
  potato: [
    { id: "Late_Blight", bn: "নাবী ধসা (Late Blight)", en: "Late Blight" },
    { id: "Early_Blight", bn: "আগাম ধসা (Early Blight)", en: "Early Blight" },
  ],
  wheat: [
    { id: "Leaf_Rust", bn: "মরিচা রোগ (Rust)", en: "Leaf Rust" },
    { id: "Loose_Smut", bn: "আলগা চিটা (Smut)", en: "Loose Smut" },
  ],
  corn: [
    { id: "Common_Rust", bn: "মরিচা রোগ (Rust)", en: "Common Rust" },
    { id: "Northern_Leaf_Blight", bn: "পাতা পোড়া (Blight)", en: "Northern Leaf Blight" },
  ],
  chilli: [
    { id: "Leaf_Curl", bn: "পাতা কোঁকড়ানো (Leaf Curl)", en: "Leaf Curl" },
    { id: "Chilli_Leaf_Spot", bn: "পাতার দাগ (Leaf Spot)", en: "Leaf Spot" },
  ],
  brassica: [
    { id: "Alternaria_Spot", bn: "অল্টারনারিয়া দাগ (Spot)", en: "Alternaria Spot" },
    { id: "Downy_Mildew", bn: "ডাউনি মিলডিউ (Mildew)", en: "Downy Mildew" },
  ],
};

function ModelErrorCard({
  result,
  onSelectCrop,
  onSelectDisease,
  onClear,
}: {
  result: DetectResponse;
  onSelectCrop?: (crop: string) => void;
  onSelectDisease?: (disease: string) => void;
  onClear?: () => void;
}) {
  const { t, locale, localizeCrop } = useLanguage();
  const cropKey = (result.crop ?? "").trim().toLowerCase();
  const diseases = CROP_DISEASES[cropKey] ?? [];

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border border-ochre/35 bg-ochre/5 p-6 shadow-sm text-center"
    >
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-ochre/20 text-ochre">
        <HelpCircle className="h-6 w-6" strokeWidth={1.5} />
      </div>
      <h3 className="mt-3 font-display text-lg font-semibold text-ink">
        {locale === "bn" ? "অন-ডিভাইস স্ক্যান নির্দেশনা" : "Diagnosis Assistance"}
      </h3>
      <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-ink-soft">
        {locale === "bn"
          ? "সার্ভার ক্লাউড সীমাবদ্ধতায় সরাসরি শনাক্তকরণে বিলম্ব হচ্ছে। নিচে আপনার আক্রান্ত পাতার লক্ষণ অনুযায়ী রোগ নির্বাচন করে সম্পূর্ণ প্রতিকার ও ডোজ মাত্রা গ্রহণ করুন:"
          : "Direct cloud classifier is constrained. Please tap your leaf symptom below to immediately receive verified advisory & dosage:"}
      </p>

      {diseases.length > 0 && onSelectDisease && (
        <div className="mt-4 space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wider text-ochre">
            {locale === "bn" ? `${localizeCrop(result.crop)} ফসলের সম্ভাব্য রোগ:` : `Known ${result.crop} Conditions:`}
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {diseases.map((d) => (
              <button
                key={d.id}
                type="button"
                onClick={() => onSelectDisease(d.id)}
                className="control-press flex items-center gap-1.5 rounded-lg border border-leaf/40 bg-paper px-3.5 py-2 text-xs font-semibold text-leaf shadow-sm transition-all hover:bg-leaf hover:text-paper active:scale-95 cursor-pointer"
              >
                <Leaf className="h-3.5 w-3.5" />
                <span>{locale === "bn" ? d.bn : d.en}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {(!diseases.length || !onSelectDisease) && onSelectCrop && (
        <div className="mt-4 space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wider text-ochre">
            {locale === "bn" ? "আপনার সঠিক ফসলটি নির্বাচন করুন:" : "Select Your Crop:"}
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {[
              { id: "Rice", bn: "ধান", en: "Rice" },
              { id: "Potato", bn: "আলু", en: "Potato" },
              { id: "Wheat", bn: "গম", en: "Wheat" },
              { id: "Corn", bn: "ভুট্টা", en: "Corn" },
              { id: "Chilli", bn: "মরিচ", en: "Chilli" },
              { id: "Brassica", bn: "সরিষা/কপি", en: "Brassica" },
            ].map((c) => (
              <button
                key={c.id}
                type="button"
                onClick={() => onSelectCrop(c.id.toLowerCase())}
                className="control-press rounded-lg border border-leaf/30 bg-paper px-3 py-1.5 text-xs font-medium text-ink hover:bg-leaf hover:text-paper cursor-pointer"
              >
                {locale === "bn" ? c.bn : c.en}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
        {onClear && (
          <button
            type="button"
            onClick={onClear}
            className="control-press rounded-lg border rule bg-paper px-3.5 py-1.5 text-xs font-medium text-ink-soft hover:bg-paper-2 cursor-pointer"
          >
            {t.diagnosis.clear}
          </button>
        )}
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="control-press inline-flex items-center gap-1.5 rounded-lg bg-leaf/10 px-3.5 py-1.5 text-xs font-semibold text-leaf hover:bg-leaf/20"
        >
          {t.nav.callCenter}: {locale === "en" ? HELPLINE_EN.krishiCallCenter : HELPLINE.krishiCallCenter}
        </a>
      </div>
    </motion.div>
  );
}

/* --- 7. UNCERTAIN — Disambiguation with Quick-Reply Chips --------------- */

function UncertainClarificationCard({
  result,
  onSelectCrop,
  onSelectDisease,
  onClear,
}: {
  result: DetectResponse;
  onSelectCrop?: (crop: string) => void;
  onSelectDisease?: (disease: string) => void;
  onClear?: () => void;
}) {
  const { t, locale, localizeCrop } = useLanguage();
  const prompt =
    locale === "en"
      ? "Visual features suggest multiple possible crop families. To ensure strict chemical safety, please confirm your crop below:"
      : result.clarification_prompt_bn ||
        "ছবিটি দেখে ফসল শতভাগ নিশ্চিত হওয়া যায়নি। ভুল বালাইনাশক এড়াতে নিচে আপনার সঠিক ফসলটি নির্বাচন করুন:";

  const suggestions =
    result.suggested_crops && result.suggested_crops.length > 0
      ? result.suggested_crops
      : result.top3_crops?.map((c) => c.class).filter(Boolean) ?? [];

  const cropKey = (result.crop ?? "").trim().toLowerCase();
  const cropDiseases = CROP_DISEASES[cropKey] ?? [];

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border border-ochre/30 bg-ochre/10 p-5 shadow-sm"
    >
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-ochre/20 text-ochre">
          <HelpCircle className="h-5 w-5" strokeWidth={2} />
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-lg font-semibold text-ink">
              {t.diagnosis.uncertainTitle}
            </h3>
            {onClear && (
              <button
                type="button"
                onClick={onClear}
                aria-label={t.diagnosis.clear}
                className="flex h-7 w-7 items-center justify-center rounded-md text-ink-faint hover:bg-paper-2 hover:text-ink cursor-pointer"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <p className="text-sm leading-relaxed text-ink-soft">{prompt}</p>

          {suggestions.length > 0 && (
            <div className="pt-2">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-ochre">
                {locale === "bn" ? "সঠিক ফসল নির্বাচন করুন (এক-ট্যাপে বিশ্লেষণ):" : "Select Your Crop (One-Tap Routing):"}
              </p>
              <div className="flex flex-wrap gap-2">
                {suggestions.map((cropName) => (
                  <button
                    key={cropName}
                    type="button"
                    onClick={() => onSelectCrop?.(cropName.toLowerCase())}
                    className="control-press flex min-h-11 items-center gap-2 rounded-lg border border-leaf/30 bg-paper px-4 py-2 text-sm font-semibold text-leaf shadow-sm transition-all hover:border-leaf hover:bg-leaf/10 active:scale-95 cursor-pointer"
                  >
                    <Leaf className="h-4 w-4 text-leaf" />
                    <span>{localizeCrop(cropName)}</span>
                    <span className="text-xs text-ink-faint">({cropName})</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {cropDiseases.length > 0 && onSelectDisease && (
            <div className="pt-3 border-t border-ochre/20 mt-2">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-ochre">
                {locale === "bn" ? `${localizeCrop(result.crop)} ফসলের সম্ভাব্য রোগ:` : `Suspected ${result.crop} Disease:`}
              </p>
              <div className="flex flex-wrap gap-2">
                {cropDiseases.map((d) => (
                  <button
                    key={d.id}
                    type="button"
                    onClick={() => onSelectDisease(d.id)}
                    className="control-press flex items-center gap-1.5 rounded-lg border border-leaf/40 bg-paper px-3.5 py-2 text-xs font-semibold text-leaf shadow-sm transition-all hover:bg-leaf hover:text-paper cursor-pointer"
                  >
                    <Leaf className="h-3.5 w-3.5" />
                    <span>{locale === "bn" ? d.bn : d.en}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

/* --- 8. REQUIRES_SECOND_IMAGE — One-Shot Recovery ----------------------- */

function SecondImageCard({
  result,
  onClear,
}: {
  result: DetectResponse;
  onClear?: () => void;
}) {
  const { t, locale } = useLanguage();

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border border-leaf/30 bg-paper p-5 shadow-sm"
    >
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-leaf/15 text-leaf">
          <ImageIcon className="h-5 w-5" strokeWidth={2} />
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-lg font-semibold text-ink">
              {t.diagnosis.secondImageTitle}
            </h3>
            {onClear && (
              <button
                type="button"
                onClick={onClear}
                aria-label={t.diagnosis.clear}
                className="flex h-7 w-7 items-center justify-center rounded-md text-ink-faint hover:bg-paper-2 hover:text-ink cursor-pointer"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <p className="text-sm leading-relaxed text-ink-soft">
            {t.diagnosis.secondImageDesc}
          </p>
          <div className="pt-2">
            <button
              type="button"
              onClick={onClear}
              className="control-press inline-flex min-h-11 items-center gap-2 rounded-lg bg-leaf px-4 py-2.5 text-sm font-semibold text-paper transition-colors hover:bg-leaf-2 cursor-pointer"
            >
              <ImageIcon className="h-4 w-4" />
              {locale === "bn" ? "আরেকটি স্পষ্ট ছবি তুলুন" : "Capture Clearer Photo"}
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* --- 9. OUT_OF_DISTRIBUTION — Safe Non-Agri Leaf Rejection --------------- */

function OutOfDistributionCard({
  result,
  onClear,
}: {
  result: DetectResponse;
  onClear?: () => void;
}) {
  const { t, locale } = useLanguage();

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border border-bone bg-paper p-5 text-center shadow-sm"
    >
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-bone text-ink-soft">
        <AlertTriangle className="h-6 w-6" strokeWidth={1.5} />
      </div>
      <h3 className="mt-3 font-display text-lg font-semibold text-ink">{t.diagnosis.outOfDistTitle}</h3>
      <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-ink-soft">
        {t.diagnosis.outOfDistDesc}
      </p>
      <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
        {onClear && (
          <button
            type="button"
            onClick={onClear}
            className="control-press min-h-11 rounded-lg border rule bg-paper px-4 py-2 text-sm font-medium text-ink-soft hover:bg-paper-2 cursor-pointer"
          >
            {locale === "bn" ? "নতুন ছবি দিন" : "Upload New Photo"}
          </button>
        )}
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="control-press inline-flex min-h-11 items-center gap-2 rounded-lg bg-leaf/10 px-4 py-2 text-sm font-semibold text-leaf hover:bg-leaf/20"
        >
          {t.nav.callCenter}: {locale === "en" ? HELPLINE_EN.krishiCallCenter : HELPLINE.krishiCallCenter}
        </a>
      </div>
    </motion.div>
  );
}
