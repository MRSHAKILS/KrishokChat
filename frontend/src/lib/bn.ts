/* =========================================================================
   Bengali numeral helpers — the entire UI speaks in Bengali numerals.
   A farmer reads ৯৮%, not 98%. This is the single conversion point.
   ========================================================================= */

const BN_DIGITS = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"];

/** Convert a number to a Bengali numeral string. */
export function bn(value: number | string): string {
  return String(value).replace(/[0-9]/g, (d) => BN_DIGITS[Number(d)]);
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
  "late_blight": "লেট ব্লাইট (নাবি ধসা)",
  "late blight": "লেট ব্লাইট (নাবি ধসা)",
  "early_blight": "আর্লি ব্লাইট (আগাম ধসা)",
  "early blight": "আর্লি ব্লাইট (আগাম ধসা)",
  "northern_leaf_blight": "উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
  "northern leaf blight": "উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
  "gray_leaf_spot": "ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "gray leaf spot": "ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "common_rust": "সাধারণ রাস্ট (Common Rust)",
  "common rust": "সাধারণ রাস্ট (Common Rust)",
  "brown_spot": "বাদামী দাগ রোগ (Brown Spot)",
  "brown spot": "বাদামী দাগ রোগ (Brown Spot)",
  "leaf_scald": "পাতা পোড়া রোগ (Leaf Scald)",
  "leaf scald": "পাতা পোড়া রোগ (Leaf Scald)",
  "narrow_brown_spot": "সরু বাদামী দাগ (Narrow Brown Spot)",
  "narrow brown spot": "সরু বাদামী দাগ (Narrow Brown Spot)",
  "rice_hispa": "পামরি পোকা (Rice Hispa)",
  "hispa": "পামরি পোকা (Rice Hispa)",
  "sheath_blight": "খোলপোড়া রোগ (Sheath Blight)",
  "sheath blight": "খোলপোড়া রোগ (Sheath Blight)",
  "bacterial_leaf_blight": "ব্যাকটেরিয়াল লিফ ব্লাইট",
  "bacterial leaf blight": "ব্যাকটেরিয়াল লিফ ব্লাইট",
  "black_rot": "কালো পচা রোগ (Black Rot)",
  "black rot": "কালো পচা রোগ (Black Rot)",
  "alternaria_leaf_spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  "alternaria leaf spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  "downy_mildew": "ডাউনি মিলডিউ",
  "downy mildew": "ডাউনি মিলডিউ",
};

/** Crop display labels in Bengali (used when the farmer selects the crop). */
const CROP_BN_MAP: Record<string, string> = {
  rice: "ধান",
  wheat: "গম",
  corn: "ভুট্টা",
  potato: "আলু",
  brassica: "বাঁধাকপি/ফুলকপি",
  solanacea: "টমেটো/মরিচ",
  gourdguava: "কদু/পেয়ারা",
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
