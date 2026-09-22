/* =========================================================================
   App-wide constants — single source of truth for names, helplines, limits.
   Helpline numbers are real and verified (Bangladesh government services).
   ========================================================================= */

export const APP = {
  name: "কৃষক টেক",
  nameEn: "KrishokTech",
  tagline: "নিরাপদ ও প্রমাণভিত্তিক বাংলা কৃষি এআই",
  taglineEn: "Safety-aware Bengali Agri-AI Advisory",
  version: "0.2.0",
} as const;

export const HELPLINE = {
  krishiCallCenter: "১৬১২৩", // Government of Bangladesh Krishi Call Center — verified
  emergency: "৯৯৯",
} as const;

/* Same helpline numbers in Latin digits, for display in English mode only.
   tel: links keep using HELPLINE above (unchanged). */
export const HELPLINE_EN = {
  krishiCallCenter: "16123",
  emergency: "999",
} as const;

/* Hugging Face dataset — verified public.
   No public paper link here by policy (docs/PAPER_POLICY.md): authoritative papers
   are local files at `paper/done papers/`; add a real public link (TODO) once the
   researcher provides one. */
export const LINKS = {
  huggingface: "https://huggingface.co/datasets/RaiyanKhaan/krishokChat",
  github: "https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System",
} as const;

/* Key research numbers — from the two papers (local copies in `paper/done papers/`),
   verified 2026-08-13 by text extraction; NOT fabricated */
export const RESEARCH_STATS = {
  benchmarkInstances: "৮৫,৯৭৯",
  knowledgeNodes: "২,১৩৫",
  publications: "২৮৪",
  institutions: "১৩",
  dialects: "৬",
  entities: "১৯,৭৬৮",
  triples: "১৭,৫০১",
  farmerQueries: "১,০০০",
  fieldInterviews: "৩০০",
  soilImages: "৭২২",
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
  /* AgriTrust paper (§1, §3.3, §5.1): image-linked nodes, entity graph counts,
     answerable query set, KG-grounded inter-annotator κ */
  imageLinkedNodes: "১,০২২",
  imageLinkedShare: "৩৫.৫%",
  uniqueCrops: "৯১৫",
  diseaseVariants: "৭০৪",
  chemicalEntities: "২,৭২৯",
  answerableQueries: "৯০০",
  kgGroundedKappa: "০.৭৮",
  /* Empirical CEA & EACL Breakthrough Metrics (E27, E28, E34) */
  certifiedCorrectness: "৯৭.০%",
  unsafeAcceptanceRate: "০.০%",
  factBaseSpeedup: "৭০৮×",
  factBaseLatencyMs: "৩.৮",
  servingCostPer1k: "$০.০৮",
  misbindingDetection: "১০০.০%",
} as const;

/* Raw numeric values of the verified strings above — used only for count-up
   animations (toBn() re-produces the exact Bengali formatting from the number). */
export const RESEARCH_STATS_N = {
  benchmarkInstances: 85979,
  knowledgeNodes: 2135,
  publications: 284,
  institutions: 13,
  dialects: 6,
  farmerQueries: 1000,
  fieldInterviews: 300,
  sftGenF1: 0.314,
  bestZeroShotGenF1: 0.165,
  hybridR10: 0.539,
  interAnnotatorKappa: 0.72,
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

/* Pipeline stage labels — used by the trace rail across /detect, /soil and /chat */
export const STAGE_LABELS = {
  intake: "ছবি গ্রহণ",
  crop_classification: "ফসল শনাক্ত",
  disease_classification: "রোগ শনাক্ত",
  advisory: "পরামর্শ",
  safety: "নিরাপত্তা",
  retrieval: "তথ্য সংগ্রহ",
  generation: "উত্তর তৈরি",
  verifier: "যাচাই",
  moisture_regression: "আর্দ্রতা নির্ণয়",
  soil_classification: "মাটি শনাক্ত",
} as const;

/* Same stage labels in English, for display in English mode only. */
export const STAGE_LABELS_EN = {
  intake: "Photo received",
  crop_classification: "Crop identified",
  disease_classification: "Disease identified",
  advisory: "Advisory",
  safety: "Safety check",
  retrieval: "Retrieval",
  generation: "Answer generation",
  verifier: "Verification",
  moisture_regression: "Moisture estimate",
  soil_classification: "Soil identified",
} as const;

/* Soil type map — Bengali transliteration key → Bengali + USDA class.
   Keys match the frozen manifest in dataset_release/soil_moisture/. */
export const SOIL_TYPES = {
  Doash: { bn: "দোআঁশ", usda: "Loam" },
  Atel: { bn: "এঁটেল", usda: "Clay" },
  Bele: { bn: "বেলে", usda: "Sandy" },
  Poli: { bn: "পলি", usda: "Silt" },
  Bele_Doash: { bn: "বেলে-দোআঁশ", usda: "Sandy Loam" },
  Atel_Doash: { bn: "এঁটেল-দোআঁশ", usda: "Clay Loam" },
} as const;

/* Land type labels in Bengali */
export const LAND_TYPES = {
  High: "উঁচু",
  Medium: "মাঝারি",
  Low: "নিচু",
} as const;
