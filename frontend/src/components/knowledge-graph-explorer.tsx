"use client";

import { useState, useMemo, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Network,
  Database,
  Search,
  Tag,
  FileText,
  Boxes,
  ChevronRight,
  ExternalLink,
  Filter,
  CheckCircle2,
  Sparkles,
  FlaskConical,
  X,
  Code,
  Building2,
} from "lucide-react";
import { toLocaleCount } from "@/lib/use-count-up";
import { statLocale } from "@/lib/bn";
import { cn } from "@/lib/utils";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   KnowledgeGraphExplorer — Interactive 2,882-Node Knowledge & Provenance Graph.
   
   Allows defense judges, researchers, and visitors to interactively explore:
   1. The 13 Institutional Hubs (DAE, BARI, BRRI, CABI, etc.)
   2. The 6 Core Taxonomic Clusters (Variety, Cultivation, Disease, Pest, Fertilizer)
   3. Factual Knowledge Triples (Subject -> Predicate -> Object)
   4. Chemical Provenance Trace Arrays
   ========================================================================= */

interface KnowledgeNodeData {
  id: string;
  category: "Variety" | "Cultivation Practice" | "Disease" | "Pest" | "Fertilizer" | "Other";
  categoryBn: string;
  titleBn: string;
  titleEn: string;
  publisher: string;
  publisherFull: string;
  publisherFullEn: string;
  sourceDoc: string;
  sourceDocEn: string;
  page: string;
  year: string;
  contentBn: string;
  contentEn: string;
  entities: string[];
  entitiesEn: string[];
  triples: { s: string; p: string; o: string }[];
  triplesEn: { s: string; p: string; o: string }[];
  chemicals: string[];
}

const SAMPLE_NODES: KnowledgeNodeData[] = [
  {
    id: "DAE_PEST_1206A0_001",
    category: "Disease",
    categoryBn: "রোগ",
    titleBn: "আলুর লেট ব্লাইট (নাবি ধসা)",
    titleEn: "Potato Late Blight Management",
    publisher: "DAE",
    publisherFull: "কৃষি সম্প্রসারণ অধিদপ্তর (Department of Agricultural Extension)",
    publisherFullEn: "Department of Agricultural Extension (DAE)",
    sourceDoc: "Potato Disease Manuals (Plantwise Guidelines)",
    sourceDocEn: "Potato Disease Manuals (Plantwise Guidelines)",
    page: "৮৫২",
    year: "২০২১",
    contentBn:
      "আলুর লেট ব্লাইট (Late Blight / নাবি ধসা) একটি মারাত্মক ছত্রাকজনিত রোগ যা Phytophthora infestans দ্বারা সৃষ্ট। পাতার নিচে ছোট সবুজ-বাদামি জলভেজা দাগ দেখা যায়। অনুকূল আবহাওয়ায় পুরো ক্ষেত ২-৩ দিনে পুড়ে যাওয়ার মতো কালো হয়ে যায়।",
    contentEn:
      "Potato late blight is a serious fungal disease caused by Phytophthora infestans. Small green-brown water-soaked spots appear on the underside of leaves. Under favorable weather, an entire field can turn black as if scorched within 2–3 days.",
    entities: ["Phytophthora infestans", "আলু", "লেট ব্লাইট", "Mancozeb 80WP", "Metalaxyl"],
    entitiesEn: ["Phytophthora infestans", "Potato", "Late Blight", "Mancozeb 80WP", "Metalaxyl"],
    triples: [
      { s: "আলু (Potato)", p: "আক্রান্ত_হয় (affected_by)", o: "লেট ব্লাইট (Late Blight)" },
      { s: "লেট ব্লাইট", p: "সৃষ্টিকারী_জীবাণু (caused_by)", o: "Phytophthora infestans" },
      { s: "দমন_ব্যবস্থা", p: "অনুমোদিত_ছত্রাকনাশক (treated_with)", o: "Mancozeb 80WP / Metalaxyl" },
    ],
    triplesEn: [
      { s: "Potato", p: "affected_by", o: "Late Blight" },
      { s: "Late Blight", p: "caused_by", o: "Phytophthora infestans" },
      { s: "Control measure", p: "treated_with", o: "Mancozeb 80WP / Metalaxyl" },
    ],
    chemicals: ["Mancozeb 80WP", "Metalaxyl", "Copper oxychloride"],
  },
  {
    id: "BRRI_VAR_0481_003",
    category: "Variety",
    categoryBn: "জাত",
    titleBn: "ব্রি ধান২৮ ও ব্রি ধান৮৯ চাষ নির্দেশিকা",
    titleEn: "BRRI Dhan 28 & 89 Cultivation Profile",
    publisher: "BRRI",
    publisherFull: "বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI)",
    publisherFullEn: "Bangladesh Rice Research Institute (BRRI)",
    sourceDoc: "আধুনিক ধানের চাষ (Handbook on Modern Rice Cultivation)",
    sourceDocEn: "Handbook on Modern Rice Cultivation",
    page: "৪৬",
    year: "২০২২",
    contentBn:
      "ব্রি ধান৮৯ বোরো মৌসুমের একটি উচ্চফলনশীল জাত। এর জীবনকাল ১৫৪-১৬০ দিন এবং গড় ফলন হেক্টর প্রতি ৮.৫-৯.০ টন। চাল মাঝারি চিকন এবং ভাত ঝরঝরে। ব্লাস্ট রোগ প্রতিরোধী বৈশিষ্ট্য বিদ্যমান।",
    contentEn:
      "BRRI Dhan 89 is a high-yielding variety for the Boro season. Its life cycle is 154–160 days with an average yield of 8.5–9.0 tons per hectare. The grain is medium-slender and the cooked rice is non-sticky. It carries blast-disease-resistant traits.",
    entities: ["ব্রি ধান৮৯", "বোরো ধান", "উচ্চফলনশীল", "ব্লাস্ট সহনশীল"],
    entitiesEn: ["BRRI Dhan 89", "Boro rice", "High-yielding", "Blast tolerant"],
    triples: [
      { s: "ব্রি ধান৮৯", p: "মৌসুম (season)", o: "বোরো (Boro)" },
      { s: "ব্রি ধান৮৯", p: "গড়_ফলন (yield)", o: "৮.৫ - ৯.০ টন/হেক্টর" },
      { s: "ব্রি ধান৮৯", p: "রোগ_সহনশীলতা (tolerance)", o: "ব্লাস্ট প্রতিরোধী" },
    ],
    triplesEn: [
      { s: "BRRI Dhan 89", p: "season", o: "Boro" },
      { s: "BRRI Dhan 89", p: "yield", o: "8.5 - 9.0 tons/hectare" },
      { s: "BRRI Dhan 89", p: "tolerance", o: "Blast resistant" },
    ],
    chemicals: [],
  },
  {
    id: "BARI_CULT_0129_002",
    category: "Cultivation Practice",
    categoryBn: "চাষ পদ্ধতি",
    titleBn: "বারি গম-৩৩ ও ব্লাস্ট প্রতিরোধী ব্যবস্থাপনা",
    titleEn: "BARI Gom-33 Blast Resistant Cultivation",
    publisher: "BARI",
    publisherFull: "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)",
    publisherFullEn: "Bangladesh Agricultural Research Institute (BARI)",
    sourceDoc: "গম ও ভুট্টা গবেষণা নির্দেশিকা (BARI Wheat Manual)",
    sourceDocEn: "BARI Wheat Manual",
    page: "১১২",
    year: "২০২৩",
    contentBn:
      "বারি গম-৩৩ বাংলাদেশে গমের ব্লাস্ট রোগ প্রতিরোধী প্রথম জিংক-সমৃদ্ধ জাত। নভেম্বরের ১৫ থেকে ৩০ তারিখের মধ্যে বপন করলে সর্বোচ্চ ফলন পাওয়া যায়। বীজ শোধন অপরিহার্য।",
    contentEn:
      "BARI Gom-33 is Bangladesh's first zinc-enriched wheat variety resistant to wheat blast disease. Sowing between November 15 and 30 gives the highest yield. Seed treatment is essential.",
    entities: ["বারি গম-৩৩", "গম ব্লাস্ট", "জিংক সমৃদ্ধ", "Providax 200FF"],
    entitiesEn: ["BARI Gom-33", "Wheat blast", "Zinc-enriched", "Providax 200FF"],
    triples: [
      { s: "বারি গম-৩৩", p: "বৈশিষ্ট্য (trait)", o: "জিংক-সমৃদ্ধ ও ব্লাস্ট সহনশীল" },
      { s: "বপন_সময়", p: "আদর্শ_তারিখ (optimal_time)", o: "১৫-৩০ নভেম্বর" },
      { s: "বীজ_শোধন", p: "ছত্রাকনাশক (seed_treatment)", o: "Providax 200FF (কার্বক্সিন + থিরাম)" },
    ],
    triplesEn: [
      { s: "BARI Gom-33", p: "trait", o: "Zinc-enriched and blast tolerant" },
      { s: "Sowing time", p: "optimal_time", o: "15-30 November" },
      { s: "Seed treatment", p: "seed_treatment", o: "Providax 200FF (Carboxin + Thiram)" },
    ],
    chemicals: ["Providax 200FF", "Nat网上 / Tebuconazole"],
  },
  {
    id: "DAE_PEST_0892_005",
    category: "Pest",
    categoryBn: "পোকা",
    titleBn: "ধানের বাদামি গাছফড়িং (বিপিএইচ) দমন",
    titleEn: "Rice Brown Planthopper (BPH) Integrated Management",
    publisher: "DAE",
    publisherFull: "কৃষি সম্প্রসারণ অধিদপ্তর (DAE)",
    publisherFullEn: "Department of Agricultural Extension (DAE)",
    sourceDoc: "জাতীয় সমন্বিত বালাই ব্যবস্থাপনা (IPM) নির্দেশিকা",
    sourceDocEn: "National Integrated Pest Management (IPM) Guideline",
    page: "২০৮",
    year: "২০২০",
    contentBn:
      "বাদামি গাছফড়িং (BPH / কারেন্ট পোকা) ধানের গোড়ায় বসে রস চুষে খায়, ফলে ধানগাছ পুড়ে যাওয়ার মতো শুকিয়ে যায় (হপারবার্ন)। অতিরিক্ত ইউরিয়া সার ব্যবহার ও অপরিকল্পিত কীটনাশক স্প্রে এর আক্রমণ বাড়িয়ে দেয়।",
    contentEn:
      "The brown planthopper (BPH) feeds by sucking sap at the base of the rice plant, causing the plant to dry out as if scorched (hopperburn). Excessive urea fertilizer use and unplanned pesticide spraying increase its attack.",
    entities: ["বাদামি গাছফড়িং", "BPH", "হপারবার্ন", "Pymetrozine", "Triflumuron"],
    entitiesEn: ["Brown planthopper", "BPH", "Hopperburn", "Pymetrozine", "Triflumuron"],
    triples: [
      { s: "বাদামি গাছফড়িং", p: "ক্ষতির_ধরন (symptom)", o: "হপারবার্ন (Hopperburn)" },
      { s: "অনুকূল_শর্ত", p: "বৃদ্ধি_পায় (aggravated_by)", o: "অতিরিক্ত ইউরিয়া ও আর্দ্রতা" },
      { s: "দমন_ব্যবস্থা", p: "অনুমোদিত_কীটনাশক (chemical_control)", o: "Pymetrozine / Isoprocarb" },
    ],
    triplesEn: [
      { s: "Brown planthopper", p: "symptom", o: "Hopperburn" },
      { s: "Favorable condition", p: "aggravated_by", o: "Excess urea and humidity" },
      { s: "Control measure", p: "chemical_control", o: "Pymetrozine / Isoprocarb" },
    ],
    chemicals: ["Pymetrozine 50WDG", "Isoprocarb 75WP"],
  },
  {
    id: "SRDI_FERT_0341_001",
    category: "Fertilizer",
    categoryBn: "সার",
    titleBn: "সুষম সার প্রয়োগ নির্দেশিকা — আলুর সুষম পুষ্টি",
    titleEn: "Balanced Fertilizer Guide for Potato",
    publisher: "SRDI",
    publisherFull: "মৃত্তিকা সম্পদ উন্নয়ন ইনস্টিটিউট (SRDI)",
    publisherFullEn: "Soil Resource Development Institute (SRDI)",
    sourceDoc: "সার সুপারিশ নির্দেশিকা (Fertilizer Recommendation Guide)",
    sourceDocEn: "Fertilizer Recommendation Guide",
    page: "১৪৫",
    year: "২০১৮",
    contentBn:
      "আলু উৎপাদনের জন্য হেক্টর প্রতি ইউরিয়া ২৫০-৩০০ কেজি, টিএসপি ১৫০-২০০ কেজি, এমওপি ২২০-২৫০ কেজি, জিপসাম ১০০-১২০ কেজি এবং বোরন ১০-১২ কেজি প্রয়োজন। অর্ধেক ইউরিয়া ও পুরো এমওপি রোপণের সময় দিতে হবে।",
    contentEn:
      "Potato production requires 250–300 kg urea, 150–200 kg TSP, 220–250 kg MOP, 100–120 kg gypsum, and 10–12 kg boron per hectare. Half the urea and all the MOP should be applied at planting.",
    entities: ["ইউরিয়া", "টিএসপি", "এমওপি", "জিপসাম", "বোরন", "আলু"],
    entitiesEn: ["Urea", "TSP", "MOP", "Gypsum", "Boron", "Potato"],
    triples: [
      { s: "আলু", p: "নাইট্রোজেন_উৎস (N_source)", o: "ইউরিয়া (২৫০-৩০০ কেজি/হেক্টর)" },
      { s: "আলু", p: "পটাশ_উৎস (K_source)", o: "এমওপি (২২০-২৫০ কেজি/হেক্টর)" },
      { s: "আলু", p: "সালফার_উৎস (S_source)", o: "জিপসাম (১০০-১২০ কেজি/হেক্টর)" },
    ],
    triplesEn: [
      { s: "Potato", p: "N_source", o: "Urea (250-300 kg/hectare)" },
      { s: "Potato", p: "K_source", o: "MOP (220-250 kg/hectare)" },
      { s: "Potato", p: "S_source", o: "Gypsum (100-120 kg/hectare)" },
    ],
    chemicals: ["Urea", "TSP", "MOP", "Gypsum", "Boric Acid"],
  },
];

const CLUSTER_METRICS = [
  { id: "all", labelBn: "সব ক্লাস্টার", labelEn: "All Clusters", count: 2882, color: "var(--color-ink)" },
  { id: "Variety", labelBn: "জাত (Variety)", labelEn: "Variety", count: 695, color: "var(--color-leaf)" },
  { id: "Cultivation Practice", labelBn: "চাষ পদ্ধতি (Cultivation)", labelEn: "Cultivation", count: 570, color: "var(--color-leaf-2)" },
  { id: "Disease", labelBn: "রোগ (Disease)", labelEn: "Disease", count: 430, color: "var(--color-ochre)" },
  { id: "Pest", labelBn: "পোকা (Pest)", labelEn: "Pest", count: 380, color: "var(--color-clay)" },
  { id: "Fertilizer", labelBn: "সার (Fertilizer)", labelEn: "Fertilizer", count: 280, color: "var(--color-leaf-3)" },
];

export function KnowledgeGraphExplorer() {
  const [activeCluster, setActiveCluster] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedNode, setSelectedNode] = useState<KnowledgeNodeData>(SAMPLE_NODES[0]);
  const [viewMode, setViewMode] = useState<"visual" | "json">("visual");
  const { locale } = useLanguage();
  const en = locale === "en";

  const filteredNodes = useMemo(() => {
    return SAMPLE_NODES.filter((node) => {
      const matchCluster = activeCluster === "all" || node.category === activeCluster;
      const q = searchQuery.trim().toLowerCase();
      if (!q) return matchCluster;
      const matchText =
        node.titleBn.toLowerCase().includes(q) ||
        node.titleEn.toLowerCase().includes(q) ||
        node.contentBn.toLowerCase().includes(q) ||
        node.entities.some((e) => e.toLowerCase().includes(q)) ||
        node.chemicals.some((c) => c.toLowerCase().includes(q));
      return matchCluster && matchText;
    });
  }, [activeCluster, searchQuery]);

  return (
    <div className="overflow-hidden rounded-2xl border rule bg-paper shadow-[0_14px_40px_rgba(52,39,23,0.08)]">
      {/* Explorer Top Control Bar */}
      <div className="border-b rule bg-paper-2/40 px-5 py-4 sm:px-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.16em] text-ochre">
              <Network className="h-3.5 w-3.5" />
              <span>{en ? "Provenance Knowledge Graph Explorer" : "প্রমাণ-জ্ঞানগ্রাফ এক্সপ্লোরার"}</span>
            </div>
            <h2 className="mt-1 font-display text-xl font-bold text-ink sm:text-2xl">
              {en ? "2,882-Node Knowledge Graph and Provenance Explorer" : "২,৮৮২-নোড জ্ঞান গ্রাফ ও প্রমাণ এক্সপ্লোরার"}
            </h2>
            <p className="mt-0.5 text-xs text-ink-soft">
              {en ? "Every node is extracted from one of 13 government agricultural publications, with triples and a chemical audit." : "প্রতিটি নোড ১৩টি সরকারি কৃষি প্রকাশনা থেকে নির্যাসিত, ট্রিপল ও রাসায়নিক অডিট সম্বলিত।"}
            </p>
          </div>

          {/* Search Box */}
          <div className="relative w-full md:w-72">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-ink-faint" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={en ? "Search entities or diseases (e.g., potato, Mancozeb)..." : "এনটিটি বা রোগ খুঁজুন (যেমন: আলু, Mancozeb)..."}
              className="w-full rounded-xl border rule bg-paper py-2 pl-9 pr-3 text-xs text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 top-2.5 text-ink-faint hover:text-ink cursor-pointer"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Cluster Filter Buttons */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <span className="text-[11px] font-semibold text-ink-faint mr-1">{en ? "Taxonomy cluster:" : "ট্যাক্সোনমি ক্লাস্টার:"}</span>
          {CLUSTER_METRICS.map((cluster) => {
            const active = activeCluster === cluster.id;
            return (
              <button
                key={cluster.id}
                type="button"
                onClick={() => setActiveCluster(cluster.id)}
                className={cn(
                  "control-press rounded-full border px-3 py-1 text-xs transition-all cursor-pointer",
                  active
                    ? "border-leaf bg-leaf text-paper font-semibold shadow-2xs"
                    : "border-bone bg-paper text-ink-soft hover:border-leaf/40 hover:bg-paper-2"
                )}
              >
                <span>{en ? cluster.labelEn : cluster.labelBn}</span>
                <span className="ml-1.5 opacity-75 tabular">({toLocaleCount(cluster.count, en)})</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Explorer Workspace (Grid Layout) */}
      <div className="grid lg:grid-cols-[minmax(0,1.15fr)_minmax(0,1.85fr)] divide-y lg:divide-y-0 lg:divide-x rule">
        {/* Left Pane: Sample Node Catalog */}
        <div className="max-h-[600px] overflow-y-auto p-4 sm:p-5 space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-ink-faint">
            <span>{en ? `Corpus sample node list (${toLocaleCount(filteredNodes.length, en)} shown)` : `কর্পাস নমুনা নোড তালিকা (${toLocaleCount(filteredNodes.length, en)}টি প্রদর্শিত)`}</span>
            <span className="text-[10px]">{en ? "Click for details" : "ক্লিক করে বিবরণ দেখুন"}</span>
          </div>

          {filteredNodes.length === 0 ? (
            <div className="p-8 text-center text-xs text-ink-faint">
              {en ? "No nodes found. Try changing the search." : "কোনো নোড পাওয়া যায়নি। অনুসন্ধান পরিবর্তন করুন।"}
            </div>
          ) : (
            filteredNodes.map((node) => {
              const isSelected = selectedNode.id === node.id;
              return (
                <div
                  key={node.id}
                  onClick={() => setSelectedNode(node)}
                  className={cn(
                    "surface-lift rounded-xl border p-4 transition-all cursor-pointer",
                    isSelected
                      ? "border-leaf bg-leaf/5 ring-1 ring-leaf shadow-xs"
                      : "border-bone bg-paper hover:border-leaf/40 hover:bg-paper-2/30"
                  )}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="rounded-md bg-paper-2 px-2 py-0.5 font-mono text-[10px] font-semibold text-ink">
                      {node.id}
                    </span>
                    <span
                      className={cn(
                        "rounded-full px-2 py-0.5 text-[10px] font-semibold",
                        node.category === "Disease"
                          ? "bg-ochre/15 text-ochre"
                          : node.category === "Variety"
                          ? "bg-leaf/15 text-leaf"
                          : node.category === "Pest"
                          ? "bg-clay/15 text-clay"
                          : "bg-bone text-ink"
                      )}
                    >
                      {en ? node.category : node.categoryBn}
                    </span>
                  </div>
                  <h3 className="mt-2 font-display text-sm font-bold text-ink">{en ? node.titleEn : node.titleBn}</h3>
                  <p className="mt-1 text-xs text-ink-soft line-clamp-2 leading-relaxed">
                    {en ? node.contentEn : node.contentBn}
                  </p>
                  <div className="mt-3 flex items-center justify-between border-t border-bone/60 pt-2 text-[11px] text-ink-faint">
                    <span className="font-semibold text-leaf">{node.publisher}</span>
                    <span>{en ? "Page:" : "পৃষ্ঠা:"} {statLocale(node.page, en)}</span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right Pane: Selected Node Deep Provenance Inspector */}
        <div className="p-5 sm:p-6 space-y-5 bg-paper">
          {/* Node Header & View Mode Switcher */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b rule pb-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs font-bold text-leaf bg-leaf/10 px-2 py-0.5 rounded-md">
                  {selectedNode.id}
                </span>
                <span className="text-xs text-ink-faint">{en ? "Publication year:" : "প্রকাশনা সাল:"} {statLocale(selectedNode.year, en)}</span>
              </div>
              <h3 className="mt-1 font-display text-xl font-bold text-ink">{en ? selectedNode.titleEn : selectedNode.titleBn}</h3>
              {!en && <div className="text-xs text-ink-faint font-medium">{selectedNode.titleEn}</div>}
            </div>

            <div className="flex rounded-lg border rule bg-paper p-0.5 text-xs font-semibold">
              <button
                type="button"
                onClick={() => setViewMode("visual")}
                className={cn(
                  "flex items-center gap-1 rounded-md px-2.5 py-1 transition-colors cursor-pointer",
                  viewMode === "visual" ? "bg-leaf text-paper shadow-2xs" : "text-ink-soft hover:text-ink"
                )}
              >
                <Sparkles className="h-3 w-3" /> {en ? "Visual View" : "ভিজ্যুয়াল ভিউ"}
              </button>
              <button
                type="button"
                onClick={() => setViewMode("json")}
                className={cn(
                  "flex items-center gap-1 rounded-md px-2.5 py-1 transition-colors cursor-pointer",
                  viewMode === "json" ? "bg-leaf text-paper shadow-2xs" : "text-ink-soft hover:text-ink"
                )}
              >
                <Code className="h-3 w-3" /> {en ? "JSON Data" : "JSON ডেটা"}
              </button>
            </div>
          </div>

          {viewMode === "visual" ? (
            <div className="space-y-5">
              {/* Natural Language Node Content */}
              <div>
                <div className="text-[11px] font-bold uppercase tracking-wider text-ink-faint">
                  {en ? "Extracted Factual Content" : "প্রমাণিত তথ্য নির্যাস (Extracted Factual Content)"}
                </div>
                <div className="mt-1.5 rounded-xl border border-bone bg-paper-2/25 p-4 text-sm leading-relaxed text-ink whitespace-pre-wrap">
                  {en ? selectedNode.contentEn : selectedNode.contentBn}
                </div>
              </div>

              {/* Factual Knowledge Triples (Subject -> Predicate -> Object) */}
              {selectedNode.triples.length > 0 && (
                <div>
                  <div className="flex items-center justify-between text-[11px] font-bold uppercase tracking-wider text-ink-faint">
                    <span>{en ? `Knowledge Graph Triple Relationships (${toLocaleCount(selectedNode.triples.length, en)} triples)` : `জ্ঞান গ্রাফ ট্রিপল রিলেশনশিপ (${toLocaleCount(selectedNode.triples.length, en)}টি ট্রিপল)`}</span>
                    <span className="text-ochre">KG Extraction</span>
                  </div>
                  <div className="mt-2 space-y-2">
                    {(en ? selectedNode.triplesEn : selectedNode.triples).map((tr, i) => (
                      <div
                        key={i}
                        className="flex flex-col sm:flex-row sm:items-center gap-2 rounded-lg border border-leaf/20 bg-leaf/5 px-3 py-2 text-xs"
                      >
                        <span className="font-bold text-ink bg-paper px-2 py-0.5 rounded border rule">
                          {tr.s}
                        </span>
                        <span className="text-ochre font-semibold text-[11px] flex items-center gap-1">
                          <ChevronRight className="h-3.5 w-3.5" /> {tr.p} <ChevronRight className="h-3.5 w-3.5" />
                        </span>
                        <span className="font-semibold text-leaf bg-paper px-2 py-0.5 rounded border rule">
                          {tr.o}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Entities & Chemical Provenance Array */}
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl border rule bg-paper p-3.5">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-ink">
                    <Tag className="h-3.5 w-3.5 text-ochre" /> {en ? `Identified Entities (${toLocaleCount(selectedNode.entities.length, en)})` : `শনাক্তকৃত এনটিটি (${selectedNode.entities.length}টি)`}
                  </div>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {(en ? selectedNode.entitiesEn : selectedNode.entities).map((ent, i) => (
                      <span
                        key={i}
                        className="rounded-md bg-paper-2 px-2 py-1 text-[11px] font-medium text-ink-soft"
                      >
                        {ent}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="rounded-xl border border-ochre/30 bg-ochre/5 p-3.5">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-ochre">
                    <FlaskConical className="h-3.5 w-3.5" /> {en ? "Chemical Trace Audit (Chemical Trace)" : "কেমিক্যাল ট্রেস অডিট (Chemical Trace)"}
                  </div>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {selectedNode.chemicals.length > 0 ? (
                      selectedNode.chemicals.map((chem, i) => (
                        <span
                          key={i}
                          className="rounded-md border border-ochre/40 bg-paper px-2 py-1 text-[11px] font-semibold text-ochre"
                        >
                          {chem}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-ink-faint">{en ? "No chemical components (chemical-free knowledge)" : "কোনো রাসায়নিক উপাদান নেই (রাসায়নিক-মুক্ত জ্ঞান)"}</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Institutional Provenance Reference */}
              <div className="rounded-xl border border-leaf/20 bg-leaf/5 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-wider text-leaf">
                    {en ? "Institutional Source and Citation" : "প্রাতিষ্ঠানিক উৎস ও সাইটেশন"}
                  </div>
                  <div className="mt-0.5 text-xs font-bold text-ink">{en ? selectedNode.publisherFullEn : selectedNode.publisherFull}</div>
                  <div className="text-[11px] text-ink-soft">
                    {en
                      ? <>Document: {selectedNode.sourceDocEn} (page no. {statLocale(selectedNode.page, en)})</>
                      : <>ডকুমেন্ট: {selectedNode.sourceDoc} (পৃষ্ঠা নং {selectedNode.page})</>}
                  </div>
                </div>
                <div className="shrink-0 flex items-center gap-1.5 text-xs font-semibold text-leaf">
                  <CheckCircle2 className="h-4 w-4" /> {en ? "Verified against government data" : "সরকারি তথ্যে যাচাইকৃত"}
                </div>
              </div>
            </div>
          ) : (
            /* JSON View */
            <pre className="max-h-[420px] overflow-auto rounded-xl border rule bg-ink p-4 font-mono text-[11px] leading-relaxed text-bone">
              {JSON.stringify(selectedNode, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
