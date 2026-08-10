/* =========================================================================
   Safety-label display map — single source of truth for translating the
   backend's machine-readable safety categories into farmer-facing Bengali
   badges. Used on the home RAG demo, /chat safety trace, and /analytics.

   Why a shared map: the backend emits enum strings like `safe_agri`,
   `banned_or_restricted_chemical`. These must NEVER reach a farmer's eyes
   verbatim. Every surface renders through this one helper.
   ========================================================================= */

export type BadgeTone = "leaf" | "ochre" | "clay" | "ink";

export interface SafetyLabel {
  /** Farmer-facing Bengali label. */
  label: string;
  /** Short badge text shown in compact chips. */
  badge: string;
  /** One-line human description for the trace rail. */
  detail: string;
  /** Color tone for badges / dots. */
  tone: BadgeTone;
}

const MAP: Record<string, SafetyLabel> = {
  safe_agri: {
    label: "অনুমোদিত কৃষি প্রশ্ন",
    badge: "নিরাপদ",
    detail: "নিরাপদ, তথ্য সংগ্রহে যান",
    tone: "leaf",
  },
  banned_or_restricted_chemical: {
    label: "নিষিদ্ধ রাসায়নিক সতর্কতা",
    badge: "নিষিদ্ধ",
    detail: "অনুমোদনহীন রাসায়নিক — আটককৃত",
    tone: "clay",
  },
  self_harm_or_poisoning_risk: {
    label: "জরুরি স্বাস্থ্য সহায়তা",
    badge: "জরুরি",
    detail: "জরুরি স্বাস্থ্য রিসক — ১৬১২৩",
    tone: "clay",
  },
  prompt_injection: {
    label: "নির্দেশ অনুপ্রবেশ প্রচেষ্টা",
    badge: "অনুপ্রবেশ",
    detail: "নির্দেশ অনুপ্রবেশ — আটককৃত",
    tone: "clay",
  },
  off_topic: {
    label: "কৃষি-বহির্ভূত প্রশ্ন",
    badge: "বিষয়বহির্ভূত",
    detail: "কৃষি বিষয়ক নয় — আটককৃত",
    tone: "ink",
  },
  low_confidence: {
    label: "তথ্য অপর্যাপ্ত",
    badge: "অনিশ্চিত",
    detail: "কৃষি সম্পর্কিত, কিন্তু তথ্য অপর্যাপ্ত",
    tone: "ochre",
  },
};

const FALLBACK: SafetyLabel = {
  label: "অজানা শ্রেণী",
  badge: "অজানা",
  detail: "শ্রেণীবদ্ধ করা যায়নি",
  tone: "ink",
};

/** Resolve a backend category enum into a farmer-facing label. */
export function safetyLabel(category: string): SafetyLabel {
  return MAP[category] ?? FALLBACK;
}

/** Tone → Tailwind class fragments for a filled badge. */
export const TONE_BADGE: Record<BadgeTone, string> = {
  leaf: "bg-leaf/10 text-leaf ring-1 ring-leaf/25",
  ochre: "bg-ochre-soft/25 text-clay ring-1 ring-ochre-soft/50",
  clay: "bg-clay-soft/30 text-clay ring-1 ring-clay-soft/50",
  ink: "bg-bone text-ink-soft ring-1 ring-bone",
};

/** Tone → solid dot color. */
export const TONE_DOT: Record<BadgeTone, string> = {
  leaf: "bg-leaf",
  ochre: "bg-ochre",
  clay: "bg-clay",
  ink: "bg-ink-faint",
};

/** Tone → bar fill color for analytics. */
export const TONE_BAR: Record<BadgeTone, string> = {
  leaf: "bg-leaf",
  ochre: "bg-ochre",
  clay: "bg-clay",
  ink: "bg-ink-faint",
};

/* ---- Verifier confidence display (matches backend enum) ---- */

export interface ConfidenceLabel {
  label: string;
  tone: BadgeTone;
}

const CONF_MAP: Record<string, ConfidenceLabel> = {
  verified: { label: "যাচাইকৃত", tone: "leaf" },
  "flagged-unverified": { label: "আংশিক যাচাইকৃত", tone: "ochre" },
  low_confidence: { label: "নিম্ন নিশ্চিততা", tone: "clay" },
  blocked: { label: "অবরুদ্ধ", tone: "clay" },
};

export function confidenceLabel(confidence: string): ConfidenceLabel {
  return CONF_MAP[confidence] ?? { label: "নিম্ন নিশ্চিততা", tone: "clay" };
}

/* ---- Major agricultural districts for quick-select chips ---- */

export const AGRI_DISTRICTS = [
  "রাজশাহী",
  "রংপুর",
  "যশোর",
  "দিনাজপুর",
  "ময়মনসিংহ",
  "কুমিল্লা",
  "বরিশাল",
] as const;
