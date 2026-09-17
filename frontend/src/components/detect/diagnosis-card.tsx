"use client";

import { motion } from "motion/react";
import { CheckCircle, HelpCircle, ImageIcon, XCircle, AlertTriangle, Leaf, X } from "lucide-react";
import { enter } from "@/lib/motion";
import { bnPercent, humanizeLabel, diseaseCore, cleanKnowledgeText, translateDiseaseToBn, cropBn } from "@/lib/bn";
import { HELPLINE } from "@/lib/constants";
import { ConfidenceMeter } from "./confidence-meter";
import type { DetectResponse } from "@/lib/api";

/* =========================================================================
   DiagnosisCard — renders one of 6 honest states based on backend status.
   Never fabricates a diagnosis from a weak signal. Each state has a
   dedicated, considered design.
   ========================================================================= */

export function DiagnosisCard({
  result,
  onClear,
  onSelectCrop,
}: {
  result: DetectResponse;
  onClear?: () => void;
  onSelectCrop?: (crop: string) => void;
}) {
  // Defensive: a legacy backend response may lack a `status` field
  // (pre-refactor versions returned disease labels without status).
  // Never surface a bogus "model_error" for a valid legacy response.
  const status = result.status ?? inferStatus(result);

  switch (status) {
    case "diagnosed":
      return <DiagnosedCard result={result} onClear={onClear} />;
    case "healthy":
      return <HealthyCard result={result} />;
    case "uncertain":
      return <UncertainClarificationCard result={result} onSelectCrop={onSelectCrop} onClear={onClear} />;
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
      return <ModelErrorCard result={result} />;
    default:
      return <ModelErrorCard result={result} />;
  }
}

/** Derive the honest status from the response shape when `status` is absent. */
function inferStatus(result: DetectResponse): string {
  if (result.disease_info || result.treatment_advice || result.disease) {
    // If a disease + knowledge exists, this was a completed diagnosis.
    if (result.disease && /healthy/i.test(result.disease)) return "healthy";
    return "diagnosed";
  }
  if (result.crop && result.crop_confidence < 0.6) return "not_recognized";
  if (result.error) return "model_error";
  return "not_recognized";
}

/* --- 1. DIAGNOSED — the full diagnosis ---------------------------------- */

function DiagnosedCard({ result, onClear }: { result: DetectResponse; onClear?: () => void }) {
  const info = result.disease_info;
  const diseaseName = result.disease ? humanizeLabel(result.disease) : "";
  const diseaseBn = result.disease ? translateDiseaseToBn(result.disease) : (info?.class_name ?? "");
  const coreDisease = result.disease ? diseaseCore(result.disease) : "";

  const descClean = cleanKnowledgeText(info?.description_bn ?? "");
  const causeClean = cleanKnowledgeText(info?.cause_bn ?? "");
  const solClean = cleanKnowledgeText(info?.solution_bn ?? "");

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
              aria-label="নির্ণয় মুছুন"
              className="flex min-h-9 items-center gap-1.5 rounded-lg px-2.5 text-xs text-ink-faint transition-colors hover:bg-paper-2 hover:text-ink"
            >
              <X className="h-3.5 w-3.5" />
              মুছুন
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
                {result.crop_source === "user" ? cropBn(result.crop) : (result.crop ?? "—")}
              </span>
              {result.crop_source === "user" && (
                <span className="rounded-md bg-paper-2 px-1.5 py-0.5 text-xs font-medium text-ink-faint">
                  নির্বাচিত
                </span>
              )}
            </div>
            {result.crop_source === "user" ? (
              <div className="text-xs text-ink-faint">
                আপনার নির্বাচন অনুযায়ী {cropBn(result.crop) || ""} রোগ মডেল দিয়ে বিশ্লেষণ হয়েছে
              </div>
            ) : (
              <ConfidenceMeter value={result.crop_confidence} label="ফসল নিশ্চিতা" tone="leaf" compact />
            )}
          </div>
        </div>

        <div className="border-t rule pt-3">
          <h3 className="font-display text-xl text-ink">{diseaseBn || diseaseName || coreDisease}</h3>
          {diseaseName && diseaseBn !== diseaseName && (
            <p className="mt-0.5 text-xs text-ink-faint font-mono">{diseaseName}</p>
          )}
          <div className="mt-2.5">
            <ConfidenceMeter
              value={result.disease_confidence}
              label="রোগ নিশ্চিতা"
              tone={result.disease_confidence > 0.85 ? "leaf" : "ochre"}
              compact
            />
          </div>
        </div>
      </div>

      {/* Body: description + cause + solution (from knowledge base) */}
      {info && (descClean || causeClean || solClean) && (
        <div className="space-y-4 border-t rule p-5">
          {descClean && (
            <div>
              <div className="mb-1.5 text-xs font-semibold text-ink-faint">
                বিবরণ
              </div>
              <p className="text-sm leading-relaxed text-ink-soft">{descClean}</p>
            </div>
          )}
          {causeClean && (
            <div>
              <div className="mb-1.5 text-xs font-semibold text-ink-faint">
                কারণ
              </div>
              <p className="text-sm leading-relaxed text-ink-soft">{causeClean}</p>
            </div>
          )}
          {solClean && (
            <div className="rounded-lg border border-leaf/20 bg-leaf/5 p-4">
              <div className="mb-1.5 text-xs font-semibold text-leaf">
                প্রাথমিক সতর্কতা ও ব্যবস্থা
              </div>
              <p className="text-sm leading-relaxed text-ink">{solClean}</p>
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
}

/* --- 2. HEALTHY — the positive reassurance ------------------------------ */

function HealthyCard({ result }: { result: DetectResponse }) {
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
      <h3 className="mt-4 font-display text-xl text-ink">আপনার ফসল সুস্থ!</h3>
      <p className="mx-auto mt-2 max-w-xs text-sm leading-relaxed text-ink-soft">
        পাতায় কোনো রোগের লক্ষণ পাওয়া যায়নি।
        {result.crop && (
          <>
            {" "}
            শনাক্ত ফসল:{" "}
            <strong className="text-ink">{result.crop}</strong> ({bnPercent(result.crop_confidence)})
          </>
        )}
      </p>
      <p className="mt-3 text-xs text-ink-faint">
        নিয়মিত পরিচর্যা চালিয়ে যান। সাময়িক পরিদর্শন ফসল সুস্থ রাখে।
      </p>
    </motion.div>
  );
}

/* --- 3. NOT_RECOGNIZED — honest uncertainty ----------------------------- */

function NotRecognizedCard({ result }: { result: DetectResponse }) {
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
      <h3 className="mt-4 font-display text-xl text-ink">আমি নিশ্চিত নই</h3>
      <p className="mx-auto mt-2 max-w-xs text-sm leading-relaxed text-ink-soft">
        ফসল/রোগ নির্ণয়ে নিশ্চিততা কম ({bnPercent(result.crop_confidence || result.disease_confidence)})।
      </p>
      <div className="mt-4 space-y-2 text-left">
        <p className="text-sm text-ink-soft">দুটি পথ আছে:</p>
        <div className="rounded-lg border rule bg-paper-2/40 p-3 text-xs text-ink-soft">
          <strong className="text-ink">১.</strong> আরও পরিষ্কার, কাছের ছবি দিন — দিনের
          আলোতে, পাতা ভরে ফ্রেমে।
        </div>
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="flex items-center gap-2 rounded-lg border rule bg-paper p-3 text-xs text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
        >
          <strong className="text-ink">২.</strong> কৃষক কল সেন্টারে যোগাযোগ করুন
          <span className="ml-auto tabular font-semibold text-leaf">{HELPLINE.krishiCallCenter}</span>
        </a>
      </div>
    </motion.div>
  );
}

/* --- 4. NO_DISEASE_MODEL — honest gap ----------------------------------- */

function NoModelCard({ result }: { result: DetectResponse }) {
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
          <div className="font-display text-lg text-ink">{result.crop ?? "ফসল"}</div>
          <div className="text-xs text-ink-faint tabular">{bnPercent(result.crop_confidence)} নিশ্চিত</div>
        </div>
      </div>
      <div className="mt-4 border-t rule pt-4">
        <div className="flex items-start gap-2 text-sm text-ink-soft">
          <ImageIcon className="mt-0.5 h-4 w-4 shrink-0 text-ink-faint" />
          <p className="leading-relaxed">
            এই ফসলের জন্য বিশেষায়িত রোগ মডেল এখন আমাদের প্রোটোটাইপে নেই।
            {result.crop_source === "model" && (
              <> উপরের <strong className="text-ink">ফসল</strong> বাছাই থেকে সঠিক
              ফসল (যেমন: ধান) নির্বাচন করে আবার চেষ্টা করুন।</>
            )}{" "}
            ডান পাশের চ্যাটে এই ফসল সম্পর্কে প্রশ্ন করতে পারেন, অথবা
            কৃষক কল সেন্টারে যোগাযোগ করুন।
          </p>
        </div>
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="mt-3 flex items-center justify-between rounded-lg border rule bg-paper px-4 py-2.5 text-sm text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
        >
          কৃষক কল সেন্টার
          <span className="tabular font-semibold text-leaf">{HELPLINE.krishiCallCenter}</span>
        </a>
      </div>
    </motion.div>
  );
}

/* --- 5. INVALID_IMAGE — quality guidance -------------------------------- */

function InvalidImageCard({ result }: { result: DetectResponse }) {
  const warnings = result.quality_warnings.length > 0
    ? result.quality_warnings
    : ["ছবির গুণমান যথেষ্ট নয়"];
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
        <h3 className="font-display text-lg text-ink">ছবির গুণমান</h3>
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
          ভালো ছবির জন্য
        </div>
        <ul className="space-y-1.5 text-xs text-ink-soft">
          <li>· দিনের আলোতে ছবি তুলুন</li>
          <li>· পাতা পুরো ফ্রেমে রাখুন</li>
          <li>· কাছ থেকে, পরিষ্কারভাবে তুলুন</li>
          <li>· একটি পাতা ফোকাসে রাখুন</li>
        </ul>
      </div>
    </motion.div>
  );
}

/* --- 6. MODEL_ERROR — system failure ------------------------------------ */

function ModelErrorCard({ result }: { result: DetectResponse }) {
  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="rounded-xl border rule bg-clay-soft/15 p-6 text-center"
    >
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-clay-soft/40 text-clay">
        <XCircle className="h-6 w-6" strokeWidth={1.5} />
      </div>
      <h3 className="mt-3 font-display text-lg text-ink">বিশ্লেষণে সমস্যা হয়েছে</h3>
      <p className="mx-auto mt-2 max-w-xs text-sm leading-relaxed text-ink-soft">
        আবার চেষ্টা করুন, অথবা কৃষক কল সেন্টারে যোগাযোগ করুন।
      </p>
      {result.error && (
        <p className="mx-auto mt-2 max-w-md break-words rounded-md bg-clay-soft/25 px-3 py-2 font-mono text-xs text-clay">
          {result.error}
        </p>
      )}
      <a
        href={`tel:${HELPLINE.krishiCallCenter}`}
        className="mt-3 inline-flex items-center gap-2 rounded-lg border rule bg-paper px-4 py-2 text-sm text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
      >
        কৃষক কল সেন্টার
        <span className="tabular font-semibold text-leaf">{HELPLINE.krishiCallCenter}</span>
      </a>
    </motion.div>
  );
}

/* --- 7. UNCERTAIN — Disambiguation with Quick-Reply Chips --------------- */

function UncertainClarificationCard({
  result,
  onSelectCrop,
  onClear,
}: {
  result: DetectResponse;
  onSelectCrop?: (crop: string) => void;
  onClear?: () => void;
}) {
  const prompt =
    result.clarification_prompt_bn ||
    "ছবিটি দেখে ফসল শতভাগ নিশ্চিত হওয়া যায়নি। ভুল বালাইনাশক এড়াতে নিচে আপনার সঠিক ফসলটি নির্বাচন করুন:";
  const suggestions =
    result.suggested_crops && result.suggested_crops.length > 0
      ? result.suggested_crops
      : result.top3_crops?.map((c) => c.class).filter(Boolean) ?? [];

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
              ফসল নিশ্চিতকরণ প্রয়োজন (নিরাপত্তা গেট)
            </h3>
            {onClear && (
              <button
                type="button"
                onClick={onClear}
                aria-label="মুছুন"
                className="flex h-7 w-7 items-center justify-center rounded-md text-ink-faint hover:bg-paper-2 hover:text-ink"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <p className="text-sm leading-relaxed text-ink-soft">{prompt}</p>

          {suggestions.length > 0 && (
            <div className="pt-2">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-ochre">
                সঠিক ফসল নির্বাচন করুন (এক-ট্যাপে বিশ্লেষণ):
              </p>
              <div className="flex flex-wrap gap-2">
                {suggestions.map((cropName) => (
                  <button
                    key={cropName}
                    type="button"
                    onClick={() => onSelectCrop?.(cropName.toLowerCase())}
                    className="control-press flex min-h-11 items-center gap-2 rounded-lg border border-leaf/30 bg-paper px-4 py-2 text-sm font-semibold text-leaf shadow-sm transition-all hover:border-leaf hover:bg-leaf/10 active:scale-95"
                  >
                    <Leaf className="h-4 w-4 text-leaf" />
                    <span>{cropBn(cropName)}</span>
                    <span className="text-xs text-ink-faint">({cropName})</span>
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
              পাতার অপর পিঠের ছবি প্রয়োজন (One-Shot Recovery)
            </h3>
            {onClear && (
              <button
                type="button"
                onClick={onClear}
                aria-label="মুছুন"
                className="flex h-7 w-7 items-center justify-center rounded-md text-ink-faint hover:bg-paper-2 hover:text-ink"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <p className="text-sm leading-relaxed text-ink-soft">
            পাতার লক্ষণটি অন্যান্য রোগের সাথে সাদৃশ্যপূর্ণ হওয়ায় রোগ শতভাগ নিশ্চিত হতে পাতার নিচের পিঠ (Under-leaf) বা দাগের স্পষ্ট আরেকটি ছবি দিন।
          </p>
          <div className="pt-2">
            <button
              type="button"
              onClick={onClear}
              className="control-press inline-flex min-h-11 items-center gap-2 rounded-lg bg-leaf px-4 py-2.5 text-sm font-semibold text-paper transition-colors hover:bg-leaf-2"
            >
              <ImageIcon className="h-4 w-4" />
              আরেকটি স্পষ্ট ছবি তুলুন
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
      <h3 className="mt-3 font-display text-lg font-semibold text-ink">অসমর্থিত ফসল বা পাতা</h3>
      <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-ink-soft">
        প্রদত্ত ছবিটি সমর্থিত কোনো ফসলের সাথে মেলেনি। অনুগ্রহ করে ধান, গম, ভুট্টা, আলু, বাঁধাকপি বা মরিচ ফসলের স্পষ্ট পাতার ছবি দিন।
      </p>
      <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
        {onClear && (
          <button
            type="button"
            onClick={onClear}
            className="control-press min-h-11 rounded-lg border rule bg-paper px-4 py-2 text-sm font-medium text-ink-soft hover:bg-paper-2"
          >
            নতুন ছবি দিন
          </button>
        )}
        <a
          href={`tel:${HELPLINE.krishiCallCenter}`}
          className="control-press inline-flex min-h-11 items-center gap-2 rounded-lg bg-leaf/10 px-4 py-2 text-sm font-semibold text-leaf hover:bg-leaf/20"
        >
          কৃষক কল সেন্টার: {HELPLINE.krishiCallCenter}
        </a>
      </div>
    </motion.div>
  );
}
