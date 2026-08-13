"use client";

import { useState, useMemo, useEffect, useRef } from "react";
import { motion, AnimatePresence, MotionConfig } from "motion/react";
import {
  Search, Filter, X, ChevronDown, BookOpen, Database, Download,
  ExternalLink, FileText, Layers, Tag, Box, Sparkles, Image as ImageIcon,
  Copy, Check, ArrowDownUp, ArrowRight,
} from "lucide-react";
import { enter, stagger, dur, ease } from "@/lib/motion";
import { paletteState } from "@/components/command-menu";
import { LINKS } from "@/lib/constants";
import { cn } from "@/lib/utils";

/* =========================================================================
   Library Page — masterclass.
   Two tabs: Books (government publications) + Datasets (training resources).

   2026 redesign (P0, safe-scope):
   - Uniform equal-height card grid — identical card sizes, no blank cells,
     no spans. (Bento variant was tried and reverted: it misaligned cards.)
   - Sort control (curated / records / size / name), removable active-filter
     chips, "/" focuses search, Escape clears.
   - Researcher affordances: per-card HF download, Copy-CLI button with
     "কপি হয়েছে" confirmation, schema preview (first 4 fields + reveal).
   - MotionConfig reducedMotion="user" — WCAG 2.3.3 pattern.
   All data from /library/*.json; no hardcoded stats.
   ========================================================================= */

type Tab = "books" | "datasets";

type Book = {
  id: string; title_bn: string; title_en: string; publisher: string;
  category: string; pages: number; year: string; language: string;
  excerpt: string; pdf: string | null;
};

type Dataset = {
  id: string; name: string; name_bn: string; count: number; size_mb: number;
  format: string; category: string; description: string; description_en: string;
  use_case: string; fields: string[]; splits: Record<string, number>; color: string;
  image?: string; image_caption?: string; badge?: string; link?: string;
  stats?: { label: string; value: string }[];
};

const CATEGORIES = [
  { id: "all", label: "সব" },
  { id: "disease", label: "রোগ" },
  { id: "pest", label: "পোকা" },
  { id: "fertilizer", label: "সার" },
  { id: "cultivation", label: "চাষ" },
  { id: "fisheries", label: "মৎস্য" },
  { id: "livestock", label: "পশুপালন" },
  { id: "pesticide", label: "কীটনাশক" },
  { id: "soil", label: "মাটি" },
  { id: "regulation", label: "আইন" },
];

const DATASET_CATEGORIES = [
  { id: "all", label: "সব" },
  { id: "vision", label: "ভিশন" },
  { id: "qa", label: "QA" },
  { id: "safety", label: "নিরাপত্তা" },
  { id: "benchmark", label: "বেঞ্চমার্ক" },
  { id: "multimodal", label: "মাল্টিমোডাল" },
  { id: "retrieval", label: "রিট্রিভাল" },
  { id: "corpus", label: "কর্পাস" },
];

/* Repo-level HF download command (the catalog lives in one dataset repo). */
const HF_DOWNLOAD_CMD = "hf download RaiyanKhaan/krishokChat --repo-type dataset";

const SORTS = [
  { id: "curated", label: "বৈশিষ্ট্যযুক্ত" },
  { id: "records", label: "রেকর্ড" },
  { id: "size", label: "আকার" },
  { id: "name", label: "নাম" },
] as const;
type SortKey = (typeof SORTS)[number]["id"];

const PUBLISHER_COLORS: Record<string, string> = {
  BRRI: "var(--color-leaf)", IRRI: "var(--color-leaf-2)", BARC: "var(--color-ochre)",
  SRDI: "var(--color-ochre)", MoA: "var(--color-clay)", BARI: "var(--color-leaf)",
  CDB: "var(--color-ochre)", BSRTI: "var(--color-ochre)", CABI: "var(--color-leaf-2)",
  NARS: "var(--color-ink-soft)", DAE: "var(--color-clay)", DLS: "var(--color-leaf-2)",
  DoF: "var(--color-leaf)", FAO: "var(--color-ochre)",
};

const COLOR_MAP: Record<string, string> = {
  leaf: "var(--color-leaf)", clay: "var(--color-clay)", ochre: "var(--color-ochre)",
};

const DATASET_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  qa: FileText, safety: Layers, benchmark: Sparkles,
  multimodal: ImageIcon, retrieval: Search, corpus: Database, vision: ImageIcon,
};

export default function LibraryPage() {
  const [tab, setTab] = useState<Tab>("books");
  const [books, setBooks] = useState<Book[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");

  useEffect(() => {
    fetch("/library/catalog.json").then((r) => r.json()).then((d) => setBooks(d.books)).catch(() => {});
    fetch("/library/datasets.json").then((r) => r.json()).then((d) => setDatasets(d.datasets)).catch(() => {});
  }, []);

  return (
    <MotionConfig reducedMotion="user">
      <div className="mx-auto max-w-6xl space-y-8 py-14">
        {/* Hero */}
        <motion.section initial="hidden" animate="visible" variants={stagger} className="text-center">
          <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">Library & Data</motion.p>
          <motion.h1 variants={enter} className="mt-4 font-display text-3xl leading-tight text-ink md:text-4xl">
            কৃষি <span className="text-leaf">জ্ঞান ভান্ডার</span>
          </motion.h1>
          <motion.p variants={enter} className="mx-auto mt-3 max-w-xl text-sm text-ink-soft md:text-base">
            সরকারি প্রকাশনা ও প্রশিক্ষণ ডেটাসেট — অনুসন্ধান, পড়া ও ডাউনলোড। গবেষকদের জন্য উন্মুক্ত, সাইটেশন-গ্রাউন্ডেড বাংলা সম্পদ।
          </motion.p>
          <motion.p variants={enter} className="mt-5">
            <a href="/data" className="inline-flex items-center gap-1.5 rounded-full border rule bg-paper px-4 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf">
              জ্ঞান গ্রাফ ও উপাত্ত পরিসংখ্যান দেখুন<ArrowRight className="h-3 w-3" />
            </a>
          </motion.p>
        </motion.section>

        {/* Tab switcher */}
        <motion.div initial="hidden" animate="visible" variants={stagger} className="flex justify-center">
          <motion.div variants={enter} className="inline-flex rounded-xl border rule bg-paper p-1">
            <TabButton active={tab === "books"} onClick={() => { setTab("books"); setCategory("all"); setSearch(""); }} icon={BookOpen} label="বই ও প্রকাশনা" count={books.length} />
            <TabButton active={tab === "datasets"} onClick={() => { setTab("datasets"); setCategory("all"); setSearch(""); }} icon={Database} label="ডেটাসেট" count={datasets.length} />
          </motion.div>
        </motion.div>

        <AnimatePresence mode="wait">
          {tab === "books" ? (
            <BooksSection key="books" books={books} search={search} setSearch={setSearch} category={category} setCategory={setCategory} />
          ) : (
            <DatasetsSection key="datasets" datasets={datasets} search={search} setSearch={setSearch} category={category} setCategory={setCategory} />
          )}
        </AnimatePresence>
      </div>
    </MotionConfig>
  );
}

/* === Tab button === */
function TabButton({ active, onClick, icon: Icon, label, count }: { active: boolean; onClick: () => void; icon: React.ComponentType<{ className?: string }>; label: string; count: number; }) {
  return (
    <button onClick={onClick} className={`flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-medium transition-colors ${active ? "bg-leaf text-paper" : "text-ink-soft hover:text-ink"}`}>
      <Icon className="h-4 w-4" />
      {label}
      {count > 0 && <span className={`rounded-full px-1.5 py-0.5 text-[10px] tabular ${active ? "bg-paper/20" : "bg-bone"}`}>{count}</span>}
    </button>
  );
}

/* === Books Section === */
function BooksSection({ books, search, setSearch, category, setCategory }: { books: Book[]; search: string; setSearch: (v: string) => void; category: string; setCategory: (v: string) => void; }) {
  const [expandedPublishers, setExpandedPublishers] = useState<Set<string>>(new Set());

  const filtered = useMemo(() => books.filter((b) => {
    const mc = category === "all" || b.category === category;
    const q = search.toLowerCase().trim();
    const ms = !q || b.title_en.toLowerCase().includes(q) || b.title_bn.includes(q) || b.publisher.toLowerCase().includes(q) || b.excerpt.includes(q);
    return mc && ms;
  }), [books, search, category]);

  const grouped = useMemo(() => {
    const g: Record<string, Book[]> = {};
    for (const b of filtered) { if (!g[b.publisher]) g[b.publisher] = []; g[b.publisher].push(b); }
    return Object.entries(g).sort((a, b) => a[0].localeCompare(b[0]));
  }, [filtered]);

  const togglePub = (pub: string) => setExpandedPublishers((p) => {
    const next = new Set(p);
    if (next.has(pub)) next.delete(pub);
    else next.add(pub);
    return next;
  });
  const availableCount = books.filter((b) => b.pdf).length;
  const institutionCount = new Set(books.map((b) => b.publisher)).size;

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: dur.normal }} className="space-y-6">
      {/* Stats strip */}
      <div className="grid grid-cols-3 gap-px overflow-hidden rounded-xl border rule bg-bone">
        <div className="bg-paper px-4 py-3 text-center"><div className="font-display text-xl tabular text-leaf">{books.length}</div><div className="text-[10px] text-ink-faint">মোট বই</div></div>
        <div className="bg-paper px-4 py-3 text-center"><div className="font-display text-xl tabular text-ochre">{availableCount}</div><div className="text-[10px] text-ink-faint">পঠনযোগ্য</div></div>
        <div className="bg-paper px-4 py-3 text-center"><div className="font-display text-xl tabular text-ink">{institutionCount}</div><div className="text-[10px] text-ink-faint">প্রতিষ্ঠান</div></div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-ink-faint" />
        <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="বই, প্রকাশক, বা বিষয় খুঁজুন..." className="w-full rounded-xl border rule bg-paper py-3.5 pl-12 pr-4 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none" />
        {search && <button onClick={() => setSearch("")} className="absolute right-4 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink"><X className="h-4 w-4" /></button>}
      </div>

      {/* Category chips */}
      <div className="flex flex-wrap items-center gap-2">
        <Filter className="h-4 w-4 text-ink-faint" />
        {CATEGORIES.map((cat) => (
          <button key={cat.id} onClick={() => setCategory(cat.id)} className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${category === cat.id ? "bg-leaf text-paper" : "border rule bg-paper text-ink-soft hover:border-leaf hover:text-leaf"}`}>{cat.label}</button>
        ))}
      </div>

      <p className="text-sm text-ink-soft">{filtered.length}টি বই পাওয়া গেছে</p>

      {/* Publisher groups */}
      <div className="space-y-4">
        <AnimatePresence mode="popLayout">
          {grouped.map(([publisher, pubBooks]) => {
            const isExpanded = expandedPublishers.has(publisher) || expandedPublishers.size === 0;
            const color = PUBLISHER_COLORS[publisher] || "var(--color-ink-soft)";
            return (
              <motion.div key={publisher} layout initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="overflow-hidden rounded-xl border rule bg-paper">
                <button onClick={() => togglePub(publisher)} className="flex w-full items-center justify-between px-5 py-3.5 transition-colors hover:bg-paper-2/40">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-md font-display text-xs font-medium" style={{ backgroundColor: `color-mix(in srgb, ${color} 12%, transparent)`, color }}>{publisher.slice(0, 3)}</div>
                    <div className="text-left"><span className="font-display text-base text-ink">{publisher}</span><span className="ml-2 text-xs text-ink-faint">{pubBooks.length}টি বই</span></div>
                  </div>
                  <ChevronDown className={`h-4 w-4 text-ink-faint transition-transform ${isExpanded ? "rotate-180" : ""}`} />
                </button>
                <AnimatePresence initial={false}>
                  {isExpanded && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden border-t rule">
                      <div className="divide-y divide-bone">
                        {pubBooks.map((book) => <BookRow key={book.id} book={book} color={color} />)}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {filtered.length === 0 && books.length > 0 && <EmptyState onReset={() => { setSearch(""); setCategory("all"); }} />}
      {books.length === 0 && <LoadingState />}
    </motion.div>
  );
}

/* === Book row === */
function BookRow({ book, color }: { book: Book; color: string }) {
  return (
    <motion.div layout initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="group flex items-start gap-4 px-5 py-4 transition-colors hover:bg-paper-2/30">
      <div className="mt-1 h-12 w-1 shrink-0 rounded-full" style={{ backgroundColor: color, opacity: 0.3 }} />
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0"><h3 className="font-display text-sm text-ink">{book.title_bn}</h3><p className="mt-0.5 text-xs text-ink-faint">{book.title_en}</p></div>
          {book.pdf ? <a href={book.pdf} target="_blank" rel="noopener noreferrer" className="flex shrink-0 items-center gap-1.5 rounded-lg border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"><FileText className="h-3.5 w-3.5" />পড়ুন<ExternalLink className="h-3 w-3" /></a> : <span className="shrink-0 rounded-lg border border-dashed border-bone px-3 py-1.5 text-[11px] text-ink-faint">শীঘ্রই</span>}
        </div>
        <p className="mt-1.5 text-xs leading-relaxed text-ink-soft line-clamp-2">{book.excerpt}</p>
        <div className="mt-2 flex flex-wrap items-center gap-3 text-[10px] text-ink-faint"><span className="flex items-center gap-1"><FileText className="h-3 w-3" />{book.pages} পৃঃ</span><span className="tabular">{book.year}</span><span className="rounded bg-bone/50 px-1.5 py-0.5 font-mono">{book.id}</span></div>
      </div>
    </motion.div>
  );
}

/* === Datasets Section — uniform card catalog === */
function DatasetsSection({ datasets, search, setSearch, category, setCategory }: { datasets: Dataset[]; search: string; setSearch: (v: string) => void; category: string; setCategory: (v: string) => void; }) {
  const [sort, setSort] = useState<SortKey>("curated");
  const searchRef = useRef<HTMLInputElement>(null);

  /* "/" focuses search from anywhere (unless typing or the command palette is open). */
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (paletteState.open) return;
      const t = e.target as HTMLElement | null;
      const typing = !!t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable);
      if (e.key === "/" && !typing) {
        e.preventDefault();
        searchRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const filtered = useMemo(() => datasets.filter((d) => {
    const mc = category === "all" || d.category === category;
    const q = search.toLowerCase().trim();
    const ms = !q || d.name.toLowerCase().includes(q) || d.name_bn.includes(q) || d.description.includes(q) || d.use_case.includes(q);
    return mc && ms;
  }), [datasets, search, category]);

  const sorted = useMemo(() => {
    const arr = [...filtered];
    if (sort === "records") arr.sort((a, b) => b.count - a.count);
    else if (sort === "size") arr.sort((a, b) => b.size_mb - a.size_mb);
    else if (sort === "name") arr.sort((a, b) => a.name_bn.localeCompare(b.name_bn, "bn"));
    return arr;
  }, [filtered, sort]);

  const totalRecords = datasets.reduce((s, d) => s + d.count, 0);
  const totalSize = datasets.reduce((s, d) => s + d.size_mb, 0);
  const sizeLabel = totalSize >= 1024 ? `${(totalSize / 1024).toFixed(1)}GB` : `${Math.round(totalSize)}MB`;

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: dur.normal }} className="space-y-6">
      {/* Stats masthead — one line, editorial, not a box grid */}
      {datasets.length > 0 && (
        <motion.div initial="hidden" animate="visible" variants={stagger} className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 rounded-xl border rule bg-paper px-4 py-3">
          <motion.div variants={enter}><StatItem value={String(datasets.length)} label="ডেটাসেট" tone="leaf" /></motion.div>
          <span className="hidden h-4 w-px bg-bone sm:block" aria-hidden />
          <motion.div variants={enter}><StatItem value={`${(totalRecords / 1000).toFixed(0)}K+`} label="মোট রেকর্ড" tone="ochre" /></motion.div>
          <span className="hidden h-4 w-px bg-bone sm:block" aria-hidden />
          <motion.div variants={enter}><StatItem value={sizeLabel} label="মোট আকার" tone="ink" /></motion.div>
          <span className="hidden h-4 w-px bg-bone sm:block" aria-hidden />
          <motion.div variants={enter}><StatItem value="CC-BY-4.0" label="লাইসেন্স" tone="leaf" /></motion.div>
        </motion.div>
      )}

      {/* Search + sort */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-ink-faint" />
          <input
            ref={searchRef}
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Escape") setSearch(""); }}
            placeholder="ডেটাসেট, বিষয়, বা ব্যবহার খুঁজুন... (/)"
            aria-label="ডেটাসেট খুঁজুন"
            className="w-full rounded-xl border rule bg-paper py-3.5 pl-12 pr-4 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
          />
          {search && <button onClick={() => setSearch("")} aria-label="অনুসন্ধান মুছুন" className="absolute right-4 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink"><X className="h-4 w-4" /></button>}
        </div>
        <SortControl sort={sort} setSort={setSort} />
      </div>

      {/* Category chips — toggle off by clicking the active chip */}
      <div className="flex flex-wrap items-center gap-2">
        <Filter className="h-4 w-4 text-ink-faint" />
        {DATASET_CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setCategory(cat.id === category ? "all" : cat.id)}
            aria-pressed={category === cat.id}
            className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${category === cat.id ? "bg-leaf text-paper" : "border rule bg-paper text-ink-soft hover:border-leaf hover:text-leaf"}`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Active filters — removable chips */}
      {(search || category !== "all") && (
        <motion.div initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] text-ink-faint">সক্রিয় ফিল্টার:</span>
          {category !== "all" && (
            <FilterChip onClear={() => setCategory("all")}>
              {DATASET_CATEGORIES.find((c) => c.id === category)?.label ?? category}
            </FilterChip>
          )}
          {search && <FilterChip onClear={() => setSearch("")}>“{search}”</FilterChip>}
          <button onClick={() => { setSearch(""); setCategory("all"); }} className="text-[11px] text-leaf transition-colors hover:text-leaf-2">সব মুছুন</button>
        </motion.div>
      )}

      {/* Uniform equal-height card grid — identical sizes, no blank cells */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="grid grid-cols-1 gap-4 md:grid-cols-2"
      >
        <AnimatePresence mode="popLayout">
          {sorted.map((ds) => (
            <DatasetCard key={ds.id} ds={ds} />
          ))}
        </AnimatePresence>
      </motion.div>

      {filtered.length === 0 && datasets.length > 0 && <EmptyState onReset={() => { setSearch(""); setCategory("all"); }} />}
      {datasets.length === 0 && <LoadingState />}

      {/* Download-all CTA */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="rounded-xl border rule bg-paper-2/30 p-5 text-center">
        <p className="text-sm text-ink-soft">সম্পূর্ণ ডেটাসেট রিপোজিটরি Hugging Face-এ উপলব্ধ — গবেষণা ও ট্রেনিং-এ ব্যবহারের জন্য উন্মুক্ত।</p>
        <div className="mt-3 flex flex-wrap items-center justify-center gap-3">
          <a href={LINKS.huggingface} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 rounded-lg bg-leaf px-5 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2">
            <Download className="h-4 w-4" />Hugging Face থেকে ডাউনলোড<ExternalLink className="h-3 w-3" />
          </a>
          <CliCopy className="rounded-lg px-4 py-2.5 text-sm" />
        </div>
      </motion.div>
    </motion.div>
  );
}

/* === Dataset card === */
function DatasetCard({ ds }: { ds: Dataset }) {
  const [showAllFields, setShowAllFields] = useState(false);
  const color = COLOR_MAP[ds.color] || "var(--color-leaf)";
  const Icon = DATASET_ICONS[ds.category] || Database;
  const splitEntries = Object.entries(ds.splits);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      className="flex flex-col overflow-hidden rounded-xl border rule bg-paper"
    >
      {/* Color top bar */}
      <div className="h-1" style={{ backgroundColor: color }} />

      {/* Optional preview image — used by the vision dataset */}
      {ds.image && (
        <div className="relative">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={ds.image} alt={ds.image_caption ?? ds.name} className="h-40 w-full object-cover" loading="lazy" />
          {ds.badge && (
            <span className="absolute left-3 top-3 rounded-full bg-paper/95 px-2.5 py-1 text-[10px] font-semibold" style={{ color }}>
              {ds.badge}
            </span>
          )}
        </div>
      )}

      {/* Header */}
      <div className="flex-1 p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg" style={{ backgroundColor: `color-mix(in srgb, ${color} 12%, transparent)`, color }}>
              <Icon className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-display text-base text-ink">{ds.name_bn}</h3>
              <p className="text-xs text-ink-faint">{ds.name}</p>
            </div>
          </div>
          <span className="rounded-md bg-bone/50 px-2 py-0.5 font-mono text-[9px] text-ink-soft">{ds.format}</span>
        </div>

        {/* Stats row */}
        <div className="mt-4 grid grid-cols-3 gap-2">
          <div className="rounded-md bg-paper-2/40 px-2 py-2 text-center">
            <div className="font-display text-sm tabular" style={{ color }}>{ds.count >= 1000 ? `${(ds.count / 1000).toFixed(0)}K` : ds.count}</div>
            <div className="text-[9px] text-ink-faint">রেকর্ড</div>
          </div>
          <div className="rounded-md bg-paper-2/40 px-2 py-2 text-center">
            <div className="font-display text-sm tabular" style={{ color }}>{ds.size_mb >= 1024 ? `${(ds.size_mb / 1024).toFixed(1)}GB` : `${ds.size_mb.toFixed(0)}MB`}</div>
            <div className="text-[9px] text-ink-faint">আকার</div>
          </div>
          <div className="rounded-md bg-paper-2/40 px-2 py-2 text-center">
            <div className="font-display text-sm" style={{ color }}>{splitEntries.length}</div>
            <div className="text-[9px] text-ink-faint">স্প্লিট</div>
          </div>
        </div>

        {/* Description */}
        <p className="mt-3 text-xs leading-relaxed text-ink-soft">{ds.description}</p>

        {/* Splits */}
        <div className="mt-3 flex flex-wrap gap-1.5">
          {splitEntries.map(([split, count]) => (
            <span key={split} className="rounded-md border rule px-2 py-0.5 text-[10px] text-ink-soft">
              <span className="font-mono text-ochre">{split}</span>: <span className="tabular">{count.toLocaleString()}</span>
            </span>
          ))}
        </div>

        {/* Use case */}
        <div className="mt-3 flex items-start gap-2">
          <Tag className="mt-0.5 h-3 w-3 shrink-0 text-ink-faint" />
          <p className="text-[11px] text-ink-faint">{ds.use_case}</p>
        </div>

        {/* Vision dataset — honest locked-model disclosure */}
        {ds.id === "soil_moisture" && (
          <p className="mt-3 text-[11px] text-ink-faint">
            লকড-মডেল নীতি: ডেটাসেট প্রকাশিত; স্বয়ংক্রিয় আর্দ্রতা নির্ণয় যাচাইয়ের পরে চালু হবে।
          </p>
        )}

        {/* Schema preview — first 4 fields always visible, reveal the rest */}
        <div className="mt-3 flex flex-wrap gap-1">
          {(showAllFields ? ds.fields : ds.fields.slice(0, 4)).map((f) => (
            <span key={f} className="rounded bg-bone/40 px-1.5 py-0.5 font-mono text-[9px] text-ink-soft">{f}</span>
          ))}
          {ds.fields.length > 4 && (
            <button
              onClick={() => setShowAllFields((v) => !v)}
              className="rounded bg-bone/40 px-1.5 py-0.5 font-mono text-[9px] text-leaf transition-colors hover:bg-leaf/10"
            >
              {showAllFields ? "কম দেখান" : `সব ${ds.fields.length}টি`}
            </button>
          )}
        </div>
      </div>

      {/* Download footer */}
      <div className="mt-auto flex flex-wrap items-center justify-between gap-x-3 gap-y-2 border-t rule px-5 py-3">
        <div className="flex items-center gap-3">
          {ds.id === "soil_moisture" && (
            <a href="/soil" className="inline-flex items-center gap-1.5 text-xs font-medium text-ochre transition-colors hover:text-ochre-soft">
              <Box className="h-3.5 w-3.5" />মাটি কনসোলে দেখুন
            </a>
          )}
          <a href={LINKS.huggingface} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-leaf transition-colors hover:text-leaf-2">
            <Download className="h-3.5 w-3.5" />ডাউনলোড<ExternalLink className="h-3 w-3" />
          </a>
        </div>
        <CliCopy />
      </div>
    </motion.div>
  );
}

/* === Copy-CLI button — researcher affordance with in-place confirmation === */
function CliCopy({ className }: { className?: string }) {
  const [copied, setCopied] = useState(false);
  const timer = useRef<number | null>(null);

  useEffect(() => () => { if (timer.current) window.clearTimeout(timer.current); }, []);

  const copy = () => {
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(HF_DOWNLOAD_CMD).catch(() => legacyCopy(HF_DOWNLOAD_CMD));
    } else {
      legacyCopy(HF_DOWNLOAD_CMD);
    }
    setCopied(true);
    if (timer.current) window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <button
      onClick={copy}
      aria-label="CLI কমান্ড কপি করুন"
      title="CLI কমান্ড কপি করুন"
      className={cn(
        "inline-flex items-center justify-center gap-1.5 rounded-lg border font-medium transition-colors",
        copied ? "border-leaf/50 bg-leaf/10 text-leaf" : "rule text-ink-soft hover:border-leaf hover:text-leaf",
        className ?? "px-3 py-1.5 text-xs",
      )}
    >
      {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
      {copied ? "কপি হয়েছে" : "CLI"}
    </button>
  );
}

function legacyCopy(text: string) {
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.position = "fixed";
  ta.style.opacity = "0";
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand("copy"); } catch { /* clipboard unavailable */ }
  ta.remove();
}

/* === Sort segmented control === */
function SortControl({ sort, setSort }: { sort: SortKey; setSort: (s: SortKey) => void }) {
  return (
    <div className="flex items-center gap-1.5 self-start sm:self-auto">
      <ArrowDownUp className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />
      <div className="inline-flex rounded-lg border rule bg-paper p-0.5" role="group" aria-label="সাজান">
        {SORTS.map((s) => (
          <button
            key={s.id}
            onClick={() => setSort(s.id)}
            aria-pressed={sort === s.id}
            className={cn(
              "rounded-md px-3 py-1.5 text-xs font-medium transition-colors",
              sort === s.id ? "bg-leaf text-paper" : "text-ink-soft hover:text-ink",
            )}
          >
            {s.label}
          </button>
        ))}
      </div>
    </div>
  );
}

/* === Removable filter chip === */
function FilterChip({ children, onClear }: { children: React.ReactNode; onClear: () => void }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-leaf/30 bg-leaf/10 px-3 py-1 text-[11px] font-medium text-leaf">
      {children}
      <button onClick={onClear} aria-label="ফিল্টার মুছুন" className="transition-colors hover:text-leaf-2"><X className="h-3 w-3" /></button>
    </span>
  );
}

/* === Masthead stat item === */
function StatItem({ value, label, tone }: { value: string; label: string; tone: "leaf" | "ochre" | "ink" }) {
  const color = tone === "leaf" ? "text-leaf" : tone === "ochre" ? "text-ochre" : "text-ink";
  return (
    <div className="text-center">
      <div className={cn("font-display text-lg tabular leading-none", color)}>{value}</div>
      <div className="mt-1 text-[9px] uppercase tracking-[0.14em] text-ink-faint">{label}</div>
    </div>
  );
}

/* === Empty state === */
function EmptyState({ onReset }: { onReset: () => void }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-20 text-center">
      <Search className="mx-auto h-10 w-10 text-ink-faint" />
      <p className="mt-4 text-sm text-ink-soft">কিছু পাওয়া যায়নি।</p>
      <button onClick={onReset} className="mt-3 text-sm text-leaf hover:text-leaf-2">ফিল্টার মুছুন</button>
    </motion.div>
  );
}

/* === Loading === */
function LoadingState() {
  return (
    <div className="py-20 text-center">
      <Database className="mx-auto h-10 w-10 animate-pulse text-ink-faint" />
      <p className="mt-4 text-sm text-ink-faint">লোড হচ্ছে…</p>
    </div>
  );
}