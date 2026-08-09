"use client";

import { motion } from "motion/react";
import { CheckCircle, HelpCircle, ImageIcon, XCircle, AlertTriangle, Leaf } from "lucide-react";
import { enter } from "@/lib/motion";
import { bnPercent, humanizeLabel, diseaseCore } from "@/lib/bn";
import { HELPLINE } from "@/lib/constants";
import { ConfidenceMeter } from "./confidence-meter";
import type { DetectResponse } from "@/lib/api";

/* =========================================================================
   DiagnosisCard — renders one of 6 honest states based on backend status.
   Never fabricates a diagnosis from a weak signal. Each state has a
   dedicated, considered design.
   ========================================================================= */

export function DiagnosisCard({ result }: { result: DetectResponse }) {
  // Defensive: a legacy backend response may lack a `status` field
  // (pre-refactor versions returned disease labels without status).
  // Never surface a bogus "model_error" for a valid legacy response.
  const status = result.status ?? inferStatus(result);

  switch (status) {
    case "diagnosed":
      return <DiagnosedCard result={result} />;
    case "healthy":
      return <HealthyCard result={result} />;
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

function DiagnosedCard({ result }: { result: DetectResponse }) {
  const info = result.disease_info;
  const diseaseName = result.disease ? humanizeLabel(result.disease) : "";
  const diseaseBn = info?.class_name ?? "";
  const coreDisease = result.disease ? diseaseCore(result.disease) : "";

  return (
    <motion.div
      variants={enter}
      initial="hidden"
      animate="visible"
      className="overflow-hidden rounded-xl border rule bg-paper"
    >
      {/* Header: crop + disease */}
      <div className="space-y-3 p-5">
        <div className="flex items-start gap-3">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
            <Leaf className="h-5 w-5" strokeWidth={1.5} />
          </div>
          <div className="flex-1 space-y-2.5">
            <div className="flex items-center gap-2">
              <span className="rounded-md bg-leaf/10 px-2 py-0.5 text-xs font-semibold text-leaf">
                {result.crop ?? "—"}
              </span>
            </div>
            <ConfidenceMeter value={result.crop_confidence} label="ফসল নিশ্চিতা" tone="leaf" compact />
          </div>
        </div>

        <div className="border-t rule pt-3">
          <h3 className="font-display text-xl text-ink">{diseaseName || coreDisease}</h3>
          {diseaseBn && diseaseBn !== diseaseName && (
            <p className="mt-0.5 text-sm text-ink-soft">{diseaseBn}</p>
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
      {info && (info.description_bn || info.cause_bn || info.solution_bn) && (
        <div className="space-y-4 border-t rule p-5">
          {info.description_bn && (
            <div>
              <div className="mb-1.5 text-[11px] uppercase tracking-[0.16em] text-ink-faint">
                বিবরণ
              </div>
              <p className="text-sm leading-relaxed text-ink-soft">{info.description_bn}</p>
            </div>
          )}
          {info.cause_bn && (
            <div>
              <div className="mb-1.5 text-[11px] uppercase tracking-[0.16em] text-ink-faint">
                কারণ
              </div>
              <p className="text-sm leading-relaxed text-ink-soft">{info.cause_bn}</p>
            </div>
          )}
          {info.solution_bn && (
            <div className="rounded-lg border border-ochre-soft/50 bg-ochre-soft/15 p-4">
              <div className="mb-1.5 text-[11px] uppercase tracking-[0.16em] text-ochre">
                প্রতিকার
              </div>
              <p className="text-sm leading-relaxed text-ink">{info.solution_bn}</p>
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
        <div className="mb-2 text-[11px] uppercase tracking-[0.16em] text-ink-faint">
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
