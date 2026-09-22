/* =========================================================================
   Bengali numeral helpers — the entire UI speaks in Bengali numerals.
   A farmer reads ৯৮%, not 98%. This is the single conversion point.
   ========================================================================= */

const BN_DIGITS = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"];

/** Convert a number to a Bengali numeral string. */
export function bn(value: number | string): string {
  return String(value).replace(/[0-9]/g, (d) => BN_DIGITS[Number(d)]);
}

/** Bengali numeral in Bengali mode, plain Latin-digit string in English mode. */
export function numLocale(value: number | string, en: boolean): string {
  return en ? String(value) : bn(value);
}

/** Format a 0-1 confidence as a Bengali percentage, e.g. 0.976 → "৯৮%". */
export function bnPercent(confidence: number): string {
  return bn(Math.round(confidence * 100)) + "%";
}

/** Format a 0-1 confidence with one decimal, e.g. 0.953 → "৯৫.৩%". */
export function bnPercent1(confidence: number): string {
  return bn((confidence * 100).toFixed(1)) + "%";
}

/** Humanize a machine disease label: "Potato__Early_Blight" → "Potato — Early Blight". */
export function humanizeLabel(label: string): string {
  return label.replace(/__/g, " — ").replace(/_/g, " ").replace(/\s+/g, " ").trim();
}

/** Extract the disease core from a "Crop__Disease" label: "Potato__Early_Blight" → "Early Blight". */
export function diseaseCore(label: string): string {
  const parts = label.split("__");
  return humanizeLabel(parts.length > 1 ? parts.slice(1).join(" ") : label);
}

const DISEASE_BN_MAP: Record<string, string> = {
  // Rice diseases
  "rice bacterial leaf blight": "ধানের পাতা পোড়া / বিএলবি রোগ (Bacterial Blight)",
  "bacterial_leaf_blight": "ধানের পাতা পোড়া / বিএলবি রোগ (Bacterial Blight)",
  "bacterial leaf blight": "ধানের পাতা পোড়া / বিএলবি রোগ (Bacterial Blight)",
  "rice brown spot": "ধানের বাদামী দাগ রোগ (Brown Spot)",
  "brown_spot": "ধানের বাদামী দাগ রোগ (Brown Spot)",
  "brown spot": "ধানের বাদামী দাগ রোগ (Brown Spot)",
  "rice leaf blast": "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
  "leaf blast": "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
  "rice leaf scald": "ধানের পাতা ঝলসানো রোগ (Leaf Scald)",
  "leaf_scald": "ধানের পাতা ঝলসানো রোগ (Leaf Scald)",
  "leaf scald": "ধানের পাতা ঝলসানো রোগ (Leaf Scald)",
  "rice narrow brown leaf spot": "ধানের সরু বাদামী দাগ (Narrow Brown Spot)",
  "narrow_brown_spot": "ধানের সরু বাদামী দাগ (Narrow Brown Spot)",
  "narrow brown spot": "ধানের সরু বাদামী দাগ (Narrow Brown Spot)",
  "rice hispa": "ধানের পামরি পোকা (Rice Hispa)",
  "rice_hispa": "ধানের পামরি পোকা (Rice Hispa)",
  "hispa": "ধানের পামরি পোকা (Rice Hispa)",
  "rice sheath blight": "ধানের খোলপোড়া রোগ (Sheath Blight)",
  "sheath_blight": "ধানের খোলপোড়া রোগ (Sheath Blight)",
  "sheath blight": "ধানের খোলপোড়া রোগ (Sheath Blight)",

  // Potato diseases
  "potato late blight": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
  "late_blight": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
  "late blight": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
  "potato early blight": "আলুর আগাম ধসা / পাতা ঝলসানো (Early Blight)",
  "early_blight": "আলুর আগাম ধসা / পাতা ঝলসানো (Early Blight)",
  "early blight": "আলুর আগাম ধসা / পাতা ঝলসানো (Early Blight)",

  // Corn / Maize diseases
  "northern leaf blight": "ভুট্টার পাতা পোড়া রোগ (Northern Leaf Blight)",
  "northern_leaf_blight": "ভুট্টার পাতা পোড়া রোগ (Northern Leaf Blight)",
  "gray leaf spot": "ভুট্টার ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "gray_leaf_spot": "ভুট্টার ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "common rust": "ভুট্টার পাতার মরিচা রোগ (Common Rust)",
  "common_rust": "ভুট্টার পাতার মরিচা রোগ (Common Rust)",

  // Wheat diseases
  "wheat blast": "গমের ব্লাস্ট রোগ (Wheat Blast)",
  "wheatblast": "গমের ব্লাস্ট রোগ (Wheat Blast)",
  "black point": "গমের দানা কালো দাগ রোগ (Black Point)",
  "blackpoint": "গমের দানা কালো দাগ রোগ (Black Point)",
  "fusarium foot rot": "গমের গোড়া পচা রোগ (Foot Rot)",
  "fusariumfootrot": "গমের গোড়া পচা রোগ (Foot Rot)",
  "leaf rust": "গমের পাতার মরিচা রোগ (Leaf Rust)",
  "stem rust": "গমের কাণ্ডের মরিচা রোগ (Stem Rust)",
  "stripe rust": "গমের হলুদ মরিচা রোগ (Stripe Rust)",
  "powdery mildew": "পাউডারি মিলডিউ (পাতায় সাদা গুঁড়া রোগ)",
  "blast": "ব্লাস্ট রোগ (Blast)",

  // Cabbage & Cauliflower (Brassica) diseases
  "cabbage black rot": "বাঁধাকপির কালো পচা রোগ (Black Rot)",
  "black_rot": "বাঁধাকপির কালো পচা রোগ (Black Rot)",
  "black rot": "বাঁধাকপির কালো পচা রোগ (Black Rot)",
  "cabbage downy mildew": "বাঁধাকপির ডাউনি মিলডিউ (পাতার ছাতা রোগ)",
  "downy_mildew": "ডাউনি মিলডিউ (পাতার ছাতা রোগ)",
  "downy mildew": "ডাউনি মিলডিউ (পাতার ছাতা রোগ)",
  "cabbage alternaria spot": "বাঁধাকপির অল্টারনারিয়া গোল দাগ রোগ",
  "cauliflower alternaria disease": "ফুলকপির অল্টারনারিয়া পাতা দাগ রোগ",
  "alternaria_leaf_spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  "alternaria leaf spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  "cauliflower bacterial soft rot": "ফুলকপির নরম পচা রোগ (Soft Rot)",
  "cauliflower bacterial spot": "ফুলকপির ব্যাকটেরিয়াল দাগ রোগ",
  "cauliflower black spot": "ফুলকপির কালো দাগ রোগ (Black Spot)",
  "cauliflower downy mildew": "ফুলকপির ডাউনি মিলডিউ (ছাতা রোগ)",
  "cauliflower nutrient deficiency": "ফুলকপির পুষ্টি উপাদানের ঘাটতি (Nutrient Deficiency)",

  // Chilli diseases
  "chili bacterial spot": "মরিচের ব্যাকটেরিয়াল দাগ রোগ (Bacterial Spot)",
  "chili cercospora leaf spot": "মরিচের তিল দাগ বা চোখ দাগ রোগ (Cercospora Leaf Spot)",
  "chili curl virus": "মরিচের পাতা কোঁকড়ানো রোগ (মরিচ মোজাইক ভাইরাস)",
  "chili powdery mildew": "মরিচের পাউডারি মিলডিউ (পাতায় সাদা গুঁড়া রোগ)",
  "chili white spot": "মরিচের সাদা দাগ ও ফল পচা রোগ (অ্যানথ্রাকনোজ)",
  "chili nutrition deficiency": "মরিচের পুষ্টি উপাদানের ঘাটতি (Nutrient Deficiency)",

  // Healthy plant indicators
  "healthy leaf": "সুস্থ ও নিরোগ পাতা",
  "healthy": "সুস্থ ও নিরোগ ফসল",
};

/** Crop display labels in Bengali (used when the farmer selects the crop). */
const CROP_BN_MAP: Record<string, string> = {
  rice: "ধান",
  wheat: "গম",
  corn: "ভুট্টা",
  potato: "আলু",
  brassica: "বাঁধাকপি / ফুলকপি",
  chilli: "মরিচ",
  chili: "মরিচ",
  tomato: "টমেটো",
  eggplant: "বেগুন",
  solanacea: "টমেটো / মরিচ / বেগুন",
  gourdguava: "লাউ / পেয়ারা",
  cabbage: "বাঁধাকপি",
  cauliflower: "ফুলকপি",
};

/** Translate a machine crop label to natural Bengali. Falls back to the raw label. */
export function cropBn(label: string | null | undefined): string {
  if (!label) return "";
  const key = label.trim().toLowerCase();
  return CROP_BN_MAP[key] ?? label;
}

/** Clean text by stripping verbatim [cite: N] markers and unrendered markdown symbols (*, **). */
export function cleanKnowledgeText(text: string): string {
  if (!text) return "";
  return text
    .replaceAll(/\[cite:\s*\d+\]/gi, "")
    .replaceAll(/\*\*/g, "")
    .replaceAll(/\*/g, "")
    .trim();
}

/** Translate machine disease string to natural Bengali title. */
export function translateDiseaseToBn(rawDisease: string): string {
  if (!rawDisease) return "";
  const normalized = rawDisease.trim().replaceAll("__", " ").replaceAll("-", " ").replaceAll("_", " ").toLowerCase();
  for (const [key, bnName] of Object.entries(DISEASE_BN_MAP)) {
    if (normalized.includes(key)) return bnName;
  }
  return humanizeLabel(rawDisease);
}
