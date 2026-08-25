/**
 * R9 — Client-side deterministic fact resolver for offline zero-connectivity advisory.
 *
 * Runs the identical matching and formatting contract as backend StructuredResolver (R4/R12).
 * Operates purely over precached JSON packs under /packs/.
 */

export interface FactRow {
  crop: string;
  problem: string;
  stage: string;
  active_ingredient: string;
  trade_names_sample: string[];
  dose_min: number;
  dose_max: number;
  dose_unit: string;
  application_method_bn: string;
  phi_days: number;
  max_applications_per_season: number;
  reentry_interval_hours: number;
  ipm_alternative_bn: string;
  source_node_id: string;
  citation_short: string;
  grounding: string;
  is_banned: boolean;
}

export interface OfflinePack {
  crop: string;
  pack_version: number;
  built_at: string;
  source: string;
  calendar?: {
    key: string;
    name_bn: string;
    stages: Array<{
      key: string;
      name_bn: string;
      start_das: number;
      end_das: number;
      advisory_bn: string;
      source: string;
      grounding: string;
    }>;
  };
  facts: FactRow[];
}

export interface OfflineResolution {
  answer: string;
  resolution_tier: "structured_fact" | "templated_advisory";
  crop: string;
  problem: string;
  pack_version: number;
  citation: string;
  source_node_id: string;
}

const CROP_ALIASES: Record<string, string> = {
  "আলু": "potato",
  "potato": "potato",
  "ভুট্টা": "maize",
  "corn": "maize",
  "maize": "maize",
  "ধান": "rice",
  "rice": "rice",
  "paddy": "rice",
};

const PROBLEM_ALIASES: Record<string, string> = {
  "নাবি ধসা": "late_blight",
  "নাবি ধ্বসা": "late_blight",
  "লেট ব্লাইট": "late_blight",
  "late blight": "late_blight",
  "ফল আর্মিওয়ার্ম": "fall_armyworm",
  "আর্মিওয়ার্ম": "fall_armyworm",
  "মাজরা পোকা": "stem_borer",
  "মাজরা": "stem_borer",
  "কারেন্ট পোকা": "brown_planthopper",
  "বাদামি গাছফড়িং": "brown_planthopper",
  "ব্লাস্ট": "blast",
  "ধানের ব্লাস্ট": "blast",
};

const packCache = new Map<string, OfflinePack>();

export async function fetchPack(crop: string): Promise<OfflinePack | null> {
  const normCrop = crop.toLowerCase().trim();
  if (packCache.has(normCrop)) {
    return packCache.get(normCrop)!;
  }
  try {
    const res = await fetch(`/packs/facts_${normCrop}_v1.json`);
    if (!res.ok) return null;
    const data: OfflinePack = await res.json();
    packCache.set(normCrop, data);
    return data;
  } catch {
    return null;
  }
}

function detectCropAndProblem(query: string, cropHint?: string): { crop: string; problem: string } | null {
  const q = query.toLowerCase();
  let crop = cropHint ? cropHint.toLowerCase().trim() : "";

  if (!crop) {
    for (const [alias, canonical] of Object.entries(CROP_ALIASES)) {
      if (q.includes(alias)) {
        crop = canonical;
        break;
      }
    }
  }

  let problem = "";
  for (const [alias, canonical] of Object.entries(PROBLEM_ALIASES)) {
    if (q.includes(alias)) {
      problem = canonical;
      break;
    }
  }

  if (crop && problem) {
    return { crop, problem };
  }
  return null;
}

export function formatT1Answer(fact: FactRow): string {
  const tradeStr = fact.trade_names_sample?.length > 0 ? ` (বাণিজ্যিক নাম যেমন: ${fact.trade_names_sample.join(", ")})` : "";
  const doseStr = fact.dose_min === fact.dose_max ? `${fact.dose_min} ${fact.dose_unit}` : `${fact.dose_min}–${fact.dose_max} ${fact.dose_unit}`;

  return `অনুমোদিত কীটনাশক/ছত্রাকনাশক: **${fact.active_ingredient}**${tradeStr}।
প্রয়োগমাত্রা: **${doseStr}** (${fact.application_method_bn})।
অপেক্ষমান সময় (PHI): **${fact.phi_days} দিন**।
আইপিএম বিকল্প: ${fact.ipm_alternative_bn}।
[তথ্যসূত্র: ${fact.citation_short}]`;
}

export async function resolveOfflineQuery(query: string, cropHint?: string): Promise<OfflineResolution | null> {
  const detected = detectCropAndProblem(query, cropHint);
  if (!detected) return null;

  const pack = await fetchPack(detected.crop);
  if (!pack || !pack.facts || pack.facts.length === 0) return null;

  // Find matching fact
  const fact = pack.facts.find(
    (f) => f.problem.toLowerCase() === detected.problem.toLowerCase() && !f.is_banned
  );
  if (!fact) return null;

  const answer = formatT1Answer(fact);

  return {
    answer,
    resolution_tier: "structured_fact",
    crop: detected.crop,
    problem: detected.problem,
    pack_version: pack.pack_version,
    citation: fact.citation_short,
    source_node_id: fact.source_node_id,
  };
}
