import { ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";
import { cn } from "@/lib/utils";

/* =========================================================================
   ConfidenceBadge — shows the verification status of a generated answer.
   verified = grounded in retrieved sources
   flagged-unverified = some claims (e.g. dosages) couldn't be verified
   low_confidence = sources were weak or absent
   blocked = safety classification stopped the pipeline
   ========================================================================= */

const CONFIG = {
  verified: {
    icon: ShieldCheck,
    label: "যাচাইকৃত",
    color: "text-leaf",
    bg: "bg-leaf/10",
  },
  "flagged-unverified": {
    icon: ShieldAlert,
    label: "আংশিক যাচাইকৃত",
    color: "text-ochre",
    bg: "bg-ochre-soft/20",
  },
  "low_confidence": {
    icon: ShieldX,
    label: "নিম্ন নিশ্চিততা",
    color: "text-clay",
    bg: "bg-clay-soft/20",
  },
  "blocked": {
    icon: ShieldX,
    label: "অবরুদ্ধ",
    color: "text-clay",
    bg: "bg-clay-soft/20",
  },
} as const;

export function ConfidenceBadge({ confidence }: { confidence: string }) {
  const c = CONFIG[confidence as keyof typeof CONFIG] ?? CONFIG["low_confidence"];
  const Icon = c.icon;
  return (
    <div className={cn("inline-flex items-center gap-1.5 rounded-md border border-current/20 px-2.5 py-1 text-xs font-medium", c.bg, c.color)}>
      <Icon className="h-3.5 w-3.5" strokeWidth={1.5} />
      {c.label}
    </div>
  );
}
