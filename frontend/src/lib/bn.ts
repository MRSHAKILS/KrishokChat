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
  // Rice diseases
  "rice bacterial leaf blight": "ব্যাকটেরিয়াল পাতা পোড়া (BLB)",
  "bacterial_leaf_blight": "ব্যাকটেরিয়াল পাতা পোড়া (BLB)",
  "bacterial leaf blight": "ব্যাকটেরিয়াল পাতা পোড়া (BLB)",
  "rice brown spot": "ধানের বাদামী দাগ রোগ (Brown Spot)",
  "brown_spot": "বাদামী দাগ রোগ (Brown Spot)",
  "brown spot": "বাদামী দাগ রোগ (Brown Spot)",
  "rice leaf blast": "ধানের পাতা ব্লাস্ট (Leaf Blast)",
  "leaf blast": "পাতা ব্লাস্ট (Leaf Blast)",
  "rice leaf scald": "ধানের পাতা পোড়া রোগ (Leaf Scald)",
  "leaf_scald": "পাতা পোড়া রোগ (Leaf Scald)",
  "leaf scald": "পাতা পোড়া রোগ (Leaf Scald)",
  "rice narrow brown leaf spot": "ধানের সরু বাদামী দাগ (Narrow Brown Spot)",
  "narrow_brown_spot": "সরু বাদামী দাগ (Narrow Brown Spot)",
  "narrow brown spot": "সরু বাদামী দাগ (Narrow Brown Spot)",
  "rice hispa": "ধানের পামরি পোকা (Rice Hispa)",
  "rice_hispa": "ধানের পামরি পোকা (Rice Hispa)",
  "hispa": "পামরি পোকা (Rice Hispa)",
  "rice sheath blight": "ধানের খোলপোড়া রোগ (Sheath Blight)",
  "sheath_blight": "খোলপোড়া রোগ (Sheath Blight)",
  "sheath blight": "খোলপোড়া রোগ (Sheath Blight)",

  // Potato diseases
  "potato late blight": "আলুর লেট ব্লাইট (নাবি ধসা)",
  "late_blight": "লেট ব্লাইট (নাবি ধসা)",
  "late blight": "লেট ব্লাইট (নাবি ধসা)",
  "potato early blight": "আলুর আর্লি ব্লাইট (আগাম ধসা)",
  "early_blight": "আর্লি ব্লাইট (আগাম ধসা)",
  "early blight": "আর্লি ব্লাইট (আগাম ধসা)",

  // Corn / Maize diseases
  "northern leaf blight": "ভুট্টার নর্দার্ন লিফ ব্লাইট (Northern Leaf Blight)",
  "northern_leaf_blight": "ভুট্টার নর্দার্ন লিফ ব্লাইট (Northern Leaf Blight)",
  "gray leaf spot": "ভুট্টার ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "gray_leaf_spot": "ভুট্টার ধূসর পাতা দাগ রোগ (Gray Leaf Spot)",
  "common rust": "ভুট্টার সাধারণ মরিচা রোগ (Common Rust)",
  "common_rust": "ভুট্টার সাধারণ মরিচা রোগ (Common Rust)",

  // Wheat diseases
  "wheat blast": "গমের ব্লাস্ট রোগ (Wheat Blast)",
  "wheatblast": "গমের ব্লাস্ট রোগ (Wheat Blast)",
  "black point": "গমের কালো দাগ রোগ (Black Point)",
  "blackpoint": "গমের কালো দাগ রোগ (Black Point)",
  "fusarium foot rot": "গমের ফিউজেরিয়াম গোড়া পচা রোগ",
  "fusariumfootrot": "গমের ফিউজেরিয়াম গোড়া পচা রোগ",
  "leaf rust": "গমের পাতার মরিচা রোগ (Leaf Rust)",
  "stem rust": "গমের কাণ্ডের মরিচা রোগ (Stem Rust)",
  "stripe rust": "গমের হলুদ/ডোরা মরিচা রোগ (Stripe Rust)",
  "powdery mildew": "পাউডারি মিলডিউ (Powdery Mildew)",
  "blast": "ব্লাস্ট রোগ (Blast)",

  // Cabbage & Cauliflower (Brassica) diseases
  "cabbage black rot": "বাঁধাকপির কালো পচা রোগ (Black Rot)",
  "black_rot": "কালো পচা রোগ (Black Rot)",
  "black rot": "কালো পচা রোগ (Black Rot)",
  "cabbage downy mildew": "বাঁধাকপির ডাউনি মিলডিউ",
  "downy_mildew": "ডাউনি মিলডিউ (Downy Mildew)",
  "downy mildew": "ডাউনি মিলডিউ (Downy Mildew)",
  "cabbage alternaria spot": "বাঁধাকপির অল্টারনারিয়া দাগ",
  "cauliflower alternaria disease": "ফুলকপির অল্টারনারিয়া রোগ",
  "alternaria_leaf_spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  "alternaria leaf spot": "অল্টারনারিয়া পাতা দাগ রোগ",
  "cauliflower bacterial soft rot": "ফুলকপির ব্যাকটেরিয়াল নরম পচা রোগ",
  "cauliflower bacterial spot": "ফুলকপির ব্যাকটেরিয়াল দাগ রোগ",
  "cauliflower black spot": "ফুলকপির কালো দাগ রোগ",
  "cauliflower downy mildew": "ফুলকপির ডাউনি মিলডিউ",
  "cauliflower nutrient deficiency": "ফুলকপির পুষ্টি উপাদান ঘাটতি (Nutrient Deficiency)",

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
