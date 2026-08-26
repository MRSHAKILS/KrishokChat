import { ProvenanceBadge } from "@/components/provenance/provenance-badge";

/* =========================================================================
   ResolutionBadge (R3) — tells the farmer *who authored* the answer.

   Thin single-source wrapper around ProvenanceBadge. The five resolution
   tiers (deterministic_guard, structured_fact, templated_advisory,
   grounded_generation, honest_refusal) are defined once in
   provenance-badge.tsx so their labels can never drift apart again:
     structured_fact      → "সরাসরি তথ্যসারণি উত্তর"        (T1, no LLM)
     templated_advisory   → "অনুমোদিত টেমপ্লেট পরামর্শ"    (T2, no LLM)
   ========================================================================= */

export function ResolutionBadge({ tier, className }: { tier?: string | null; className?: string }) {
  if (!tier) return null;
  return <ProvenanceBadge tier={tier} className={className} />;
}
