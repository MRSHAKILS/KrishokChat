/* =========================================================================
   App-wide constants — single source of truth for names, helplines, limits.
   Helpline numbers are real and verified (Bangladesh government services).
   ========================================================================= */

export const APP = {
  name: "কৃষক চ্যাট",
  nameEn: "KrishokChat",
  tagline: "বাংলাদেশ কৃষি পরামর্শদাতা",
  taglineEn: "Safety-aware Bengali Agri-AI Advisory",
  version: "0.2.0",
} as const;

export const HELPLINE = {
  krishiCallCenter: "১৬১২৩", // Government of Bangladesh Krishi Call Center — verified
  emergency: "৯৯৯",
} as const;

/* Hugging Face dataset — verified public.
   No public paper link here by policy (docs/PAPER_POLICY.md): authoritative papers
   are local files at `paper/done papers/`; add a real public link (TODO) once the
   researcher provides one. */
export const LINKS = {
  huggingface: "https://huggingface.co/datasets/RaiyanKhaan/krishokChat",
  github: "https://github.com/RaiyanKhaan/KrishokChat",
} as const;

/* Key research numbers — from the two papers, NOT fabricated */
export const RESEARCH_STATS = {
  benchmarkInstances: "৮৫,৯৭৯",
  knowledgeNodes: "২,৮৮২",
  publications: "২৮৪",
  institutions: "১৩",
  dialects: "৬",
  entities: "১৯,৭৬৮",
  triples: "১৭,৫০১",
  farmerQueries: "১,০০০",
  fieldInterviews: "৩০০",
  safetyCategories: "১২",
  hallucinationFloor: "৪.০৫–৭.০০%",
  sftGenF1: "০.৩১৪",
  bestZeroShotGenF1: "০.১৬৫",
  hybridR10: "০.৫৩৯",
  bm25R10: "০.৫০৬",
  denseR10: "০.৪৬৪",
  denseFarmerR10: "০.০৯৩",
  denseSafetyR10: "০.৯৭০",
  interAnnotatorKappa: "০.৭২",
} as const;

/* API base is intentionally empty: next.config.ts rewrites /api/* to the backend,
   so the frontend and backend share an origin in dev. */
export const API_BASE = "";

export const CHAT = {
  maxHistoryTurns: 10,
  maxMessageLength: 4000,
} as const;

export const VISION = {
  maxFileSizeMB: 10,
  acceptedTypes: ["image/jpeg", "image/png", "image/webp"] as readonly string[],
} as const;

/* Pipeline stage labels — used by the trace rail across /detect and /chat */
export const STAGE_LABELS = {
  intake: "ছবি গ্রহণ",
  crop_classification: "ফসল শনাক্ত",
  disease_classification: "রোগ শনাক্ত",
  advisory: "পরামর্শ",
  safety: "নিরাপত্তা",
  retrieval: "তথ্য সংগ্রহ",
  generation: "উত্তর তৈরি",
  verifier: "যাচাই",
} as const;
