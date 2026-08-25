import { Cpu, BookOpen, FileText, Sparkles, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

/* =========================================================================
   ResolutionBadge (R3) — tells the farmer *who authored* the answer.

   Five tiers from the resolution ladder:
     deterministic_guard   → safety rule matched; no LLM
     structured_fact       → answered from a verified fact table; no LLM  (R4)
     templated_advisory    → template filled from fact rows; no LLM       (R4)
     grounded_generation   → retrieval → LLM → verifier
     honest_refusal        → classifier / coverage-gate refused

   Zero-LLM tiers (T0, T1, T2) render visually stronger than T3 to
   communicate the trust and cost properties to reviewers/judges.
   The badge follows the same shape as ConfidenceBadge.
   ========================================================================= */

interface TierConfig {
  icon: React.ElementType;
  label: string;
  /** Bengali description shown as a tooltip / aria-label */
  desc: string;
  color: string;
  bg: string;
  /** True for T0/T1/T2 — zero LLM calls, highest determinism */
  isZeroLLM?: boolean;
}

const TIER_CONFIG: Record<string, TierConfig> = {
  deterministic_guard: {
    icon: Cpu,
    label: "নিরাপত্তা নিয়ম",
    desc: "নিরাপত্তা নিয়ম (এআই ব্যবহার হয়নি)",
    color: "text-leaf",
    bg: "bg-leaf/10",
    isZeroLLM: true,
  },
  structured_fact: {
    icon: BookOpen,
    label: "অনুমোদিত তথ্যসারণি",
    desc: "অনুমোদিত তথ্যসারণি থেকে উত্তর (এআই ব্যবহার হয়নি)",
    color: "text-leaf",
    bg: "bg-leaf/10",
    isZeroLLM: true,
  },
  templated_advisory: {
    icon: FileText,
    label: "অনুমোদিত তথ্যসারণি",
    desc: "অনুমোদিত তথ্যসারণি থেকে উত্তর (এআই ব্যবহার হয়নি)",
    color: "text-leaf",
    bg: "bg-leaf/10",
    isZeroLLM: true,
  },
  grounded_generation: {
    icon: Sparkles,
    label: "সূত্রভিত্তিক এআই উত্তর",
    desc: "পুনরুদ্ধারকৃত তথ্যসূত্রের ভিত্তিতে এআই উত্তর তৈরি হয়েছে",
    color: "text-ink-soft",
    bg: "bg-bone/60",
    isZeroLLM: false,
  },
  honest_refusal: {
    icon: XCircle,
    label: "উত্তর দেওয়া হয়নি",
    desc: "জ্ঞানভাণ্ডার এই প্রশ্নটি সমর্থন করে না",
    color: "text-clay",
    bg: "bg-clay-soft/20",
    isZeroLLM: false,
  },
} as const;

const FALLBACK: TierConfig = TIER_CONFIG["grounded_generation"];

export function ResolutionBadge({ tier }: { tier?: string | null }) {
  if (!tier) return null;
  const c = TIER_CONFIG[tier] ?? FALLBACK;
  const Icon = c.icon;
  return (
    <div
      title={c.desc}
      aria-label={c.desc}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border border-current/15 px-2.5 py-1 text-xs font-medium",
        c.bg,
        c.color,
        // Zero-LLM tiers get a slightly heavier border to read as "stronger"
        c.isZeroLLM && "border-current/25 font-semibold",
      )}
    >
      <Icon className="h-3.5 w-3.5 shrink-0" strokeWidth={1.5} />
      {c.label}
      {c.isZeroLLM && (
        <span className="ml-0.5 rounded bg-current/10 px-1 py-0.5 text-[10px] font-mono leading-none">
          0 AI
        </span>
      )}
    </div>
  );
}
