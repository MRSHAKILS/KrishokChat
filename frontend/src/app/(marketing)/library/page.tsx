"use client";

/* =========================================================================
   Library Page — redesigned (2026-08-15)
   Two tabs: Books (government publications) + Datasets (training resources).

   Redesign pillars (all within the warm "Field Notebook" design system —
   no green-gradient AI look, information-carrying motion only):
   1. Sliding animated tab indicator (shared layoutId pill).
   2. Count-up stats (reuses useCountUp/toBn from /data page) so numbers
      "load in" rather than appear as static text.
   3. Books rendered as a proper responsive card grid (1/2/3 cols) grouped
      under publisher section headers — equal-height cards, no blank cells.
   4. Dataset cards gain a split-composition bar (train/val/test) — a real
      visual signal of dataset structure — plus hover lift + refined hierarchy.
   5. Smoother transitions: staggered entrances, popLayout on filter changes,
      consistent removable active-filter chips on both tabs, "/" focuses
      search, Escape clears.

   MotionConfig reducedMotion="user" — WCAG 2.3.3. All data from
   /library/*.json; no hardcoded stats.
   ========================================================================= */

import { useState, useMemo, useEffect, useRef } from "react";
import { motion, AnimatePresence, MotionConfig, useInView } from "motion/react";
import {
  Search, Filter, X, ChevronDown, BookOpen, Database, Download,
  ExternalLink, FileText, Layers, Tag, Box, Sparkles, Image as ImageIcon,
  Copy, Check, ArrowDownUp, ArrowRight, BookMarked,
} from "lucide-react";
import { enter, stagger, dur, ease, spring } from "@/lib/motion";
import { paletteState } from "@/components/command-menu";
import { LINKS } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { fetchWithOfflineFallback, CACHE_KEYS } from "@/lib/offline-cache";
import { useCountUp, toBn } from "@/lib/use-count-up";

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
  { id: "all", label: "সব বিষয়" },
  { id: "disease", label: "রোগ ও প্রতিকার" },
  { id: "pest", label: "পোকা দমন" },
  { id: "fertilizer", label: "সার ও পুষ্টি" },
  { id: "cultivation", label: "চাষাবাদ পদ্ধতি" },
  { id: "fisheries", label: "মৎস্য সম্পদ" },
  { id: "livestock", label: "প্রাণিসম্পদ" },
  { id: "pesticide", label: "বালাইনাশক বিধি" },
  { id: "soil", label: "মাটি ও সেচ" },
  { id: "regulation", label: "সরকারি নীতিমালা" },
];

const DATASET_CATEGORIES = [
  { id: "all", label: "সব ডেটাসেট" },
  { id: "vision", label: "কম্পিউটার ভিশন" },
  { id: "qa", label: "কৃষি প্রশ্নোত্তর (QA)" },
  { id: "safety", label: "নিরাপত্তা ও গার্ডরেইল" },
  { id: "benchmark", label: "বেঞ্চমার্ক মূল্যায়ন" },
  { id: "multimodal", label: "মাল্টিমোডাল" },
  { id: "retrieval", label: "তথ্য সংগ্রহ (RAG)" },
  { id: "corpus", label: "মূল কর্পাস" },
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

/* Split-segment colors — a genuine composition signal, not decoration. */
const SPLIT_COLORS: Record<string, string> = {
  train: "var(--color-leaf)",
  dev: "var(--color-ochre)",
  val: "var(--color-ochre)",
  test: "var(--color-clay)",
  full: "var(--color-ink-soft)",
};

const CAT_LABELS: Record<string, string> = Object.fromEntries(CATEGORIES.map((c) => [c.id, c.label]));

export default function LibraryPage() {
  const [tab, setTab] = useState<Tab>("books");
  const [books, setBooks] = useState<Book[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");

  useEffect(() => {
    fetchWithOfflineFallback<{ books: Book[] }>("/library/catalog.json", CACHE_KEYS.CATALOG).then((d) => {
      if (d?.books) setBooks(d.books);
    });
    fetchWithOfflineFallback<{ datasets: Dataset[] }>("/library/datasets.json", CACHE_KEYS.DATASETS).then((d) => {
      if (d?.datasets) setDatasets(d.datasets);
    });
  }, []);

  return (
    <MotionConfig reducedMotion="user">
      <div className="mx-auto max-w-6xl space-y-8 py-14">
        {/* Hero */}
        <motion.section initial="hidden" animate="visible" variants={stagger} className="text-center">
          <motion.div variants={enter} className="flex items-center justify-center gap-2 text-xs text-ochre">
            <BookMarked className="h-3.5 w-3.5" />
            লাইব্রেরি ও ডেটা
          </motion.div>
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

        {/* Tab switcher — sliding shared-layout indicator */}
        <motion.div initial="hidden" animate="visible" variants={stagger} className="flex justify-center">
          <motion.div variants={enter} className="inline-flex rounded-xl border rule bg-paper p-1 shadow-sm">
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

/* === Tab button — shared-layout sliding pill === */
function TabButton({ active, onClick, icon: Icon, label, count }: { active: boolean; onClick: () => void; icon: React.ComponentType<{ className?: string }>; label: string; count: number; }) {
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        "control-press relative flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-medium transition-colors",
        active ? "text-paper" : "text-ink-soft hover:text-ink",
      )}
    >
      {active && (
        <motion.span
          layoutId="library-tab-pill"
          className="absolute inset-0 rounded-lg bg-leaf shadow-sm"
          transition={spring}
          style={{ zIndex: 0 }}
        />
      )}
      <span className="relative z-10 flex items-center gap-2">
        <Icon className="h-4 w-4" />
        {label}
        {count > 0 && (
          <span className={cn("rounded-full px-1.5 py-0.5 text-xs tabular", active ? "bg-paper/20" : "bg-bone")}>
            {toBn(count)}
          </span>
        )}
      </span>
    </button>
  );
}

/* === Books Section — publisher-grouped card grid === */
function BooksSection({ books, search, setSearch, category, setCategory }: { books: Book[]; search: string; setSearch: (v: string) => void; category: string; setCategory: (v: string) => void; }) {
  const [collapsedPublishers, setCollapsedPublishers] = useState<Set<string>>(new Set());
  const searchRef = useRef<HTMLInputElement>(null);

  /* "/" focuses search from anywhere (unless typing or palette open). */
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (paletteState.open) return;
      const t = e.target as HTMLElement | null;
      const typing = !!t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable);
      if (e.key === "/" && !typing) { e.preventDefault(); searchRef.current?.focus(); }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

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

  const togglePub = (pub: string) => setCollapsedPublishers((p) => {
    const next = new Set(p);
    if (next.has(pub)) next.delete(pub); else next.add(pub);
    return next;
  });

  const availableCount = books.filter((b) => b.pdf).length;
  const institutionCount = new Set(books.map((b) => b.publisher)).size;
  const hasFilters = search || category !== "all";

  const statsRef = useRef<HTMLDivElement>(null);
  const statsInView = useInView(statsRef, { once: true, margin: "-40px" });

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }} transition={{ duration: dur.normal, ease: ease.smooth }} className="space-y-6">
      {/* Stats strip — count-up */}
      <div ref={statsRef} className="grid grid-cols-3 gap-px overflow-hidden rounded-xl border rule bg-bone">
        <CountStat value={books.length} label="মোট বই" tone="leaf" active={statsInView} />
        <CountStat value={availableCount} label="পঠনযোগ্য" tone="ochre" active={statsInView} />
        <CountStat value={institutionCount} label="প্রতিষ্ঠান" tone="ink" active={statsInView} />
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-ink-faint" />
        <input
          ref={searchRef}
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Escape") setSearch(""); }}
          placeholder="বই, প্রকাশক, বা বিষয় খুঁজুন... (/)"
          aria-label="বই খুঁজুন"
          className="w-full rounded-xl border rule bg-paper py-3.5 pl-12 pr-11 text-sm text-ink placeholder:text-ink-faint transition-colors focus:border-leaf focus:outline-none"
        />
        {search && (
          <button onClick={() => setSearch("")} aria-label="অনুসন্ধান মুছুন" className="absolute right-4 top-1/2 -translate-y-1/2 text-ink-faint transition-colors hover:text-ink">
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Category chips */}
      <ChipRow>
        {CATEGORIES.map((cat) => (
          <Chip key={cat.id} active={category === cat.id} onClick={() => setCategory(cat.id === category ? "all" : cat.id)}>
            {cat.label}
          </Chip>
        ))}
      </ChipRow>

      {/* Active filters */}
      <AnimatePresence>
        {hasFilters && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-ink-faint">সক্রিয় ফিল্টার:</span>
            {category !== "all" && <FilterChip onClear={() => setCategory("all")}>{CAT_LABELS[category] ?? category}</FilterChip>}
            {search && <FilterChip onClear={() => setSearch("")}>“{search}”</FilterChip>}
            <button onClick={() => { setSearch(""); setCategory("all"); }} className="text-xs text-leaf transition-colors hover:text-leaf-2">সব মুছুন</button>
          </motion.div>
        )}
      </AnimatePresence>

      <p className="text-sm text-ink-soft">{toBn(filtered.length)}টি বই পাওয়া গেছে</p>

      {/* Publisher-grouped card grids */}
      <div className="space-y-6">
        <AnimatePresence mode="popLayout">
          {grouped.map(([publisher, pubBooks]) => {
            const isCollapsed = collapsedPublishers.has(publisher);
            const color = PUBLISHER_COLORS[publisher] || "var(--color-ink-soft)";
            return (
              <motion.section
                key={publisher}
                layout
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                transition={{ duration: dur.normal, ease: ease.smooth }}
                className="overflow-hidden rounded-xl border rule bg-paper/60"
              >
                {/* Publisher section header */}
                <button
                  onClick={() => togglePub(publisher)}
                  aria-expanded={!isCollapsed}
                  className="flex w-full items-center justify-between gap-3 px-5 py-3.5 transition-colors hover:bg-paper-2/40"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-md font-display text-xs font-medium" style={{ backgroundColor: `color-mix(in srgb, ${color} 14%, transparent)`, color }}>
                      {publisher.slice(0, 3)}
                    </div>
                    <div className="text-left">
                      <span className="font-display text-base text-ink">{publisher}</span>
                      <span className="ml-2 text-xs text-ink-faint">{toBn(pubBooks.length)}টি বই</span>
                    </div>
                  </div>
                  <motion.span animate={{ rotate: isCollapsed ? 0 : 180 }} transition={{ duration: dur.fast, ease: ease.smooth }}>
                    <ChevronDown className="h-4 w-4 text-ink-faint" />
                  </motion.span>
                </button>

                {/* Grid of book cards */}
                <AnimatePresence initial={false}>
                  {!isCollapsed && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: dur.normal, ease: ease.smooth }}
                      className="overflow-hidden border-t rule"
                    >
                      <motion.div
                        initial="hidden"
                        animate="visible"
                        variants={stagger}
                        className="grid grid-cols-1 gap-3 p-4 sm:grid-cols-2 lg:grid-cols-3"
                      >
                        {pubBooks.map((book) => (
                          <BookCard key={book.id} book={book} color={color} />
                        ))}
                      </motion.div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.section>
            );
          })}
        </AnimatePresence>
      </div>

      {filtered.length === 0 && books.length > 0 && <EmptyState onReset={() => { setSearch(""); setCategory("all"); }} />}
      {books.length === 0 && <LoadingState />}
    </motion.div>
  );
}

/* === Book card === */
function BookCard({ book, color }: { book: Book; color: string }) {
  return (
    <motion.article
      layout
      variants={enter}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      whileHover={{ y: -2 }}
      className="surface-lift flex h-full flex-col overflow-hidden rounded-lg border rule bg-paper"
    >
      {/* Publisher color top bar */}
      <div className="h-1 w-full" style={{ backgroundColor: color }} />

      <div className="flex flex-1 flex-col p-4">
        {/* Meta row: category + language */}
        <div className="flex items-center justify-between gap-2">
          <span
            className="rounded-full px-2 py-0.5 text-xs font-medium"
            style={{ backgroundColor: `color-mix(in srgb, ${color} 12%, transparent)`, color }}
          >
            {CAT_LABELS[book.category] ?? book.category}
          </span>
          <span className="text-xs text-ink-faint">{book.language}</span>
        </div>

        {/* Titles */}
        <h3 className="mt-2.5 font-display text-sm leading-snug text-ink">{book.title_bn}</h3>
        <p className="mt-0.5 text-xs text-ink-faint">{book.title_en}</p>

        {/* Excerpt */}
        <p className="mt-2 text-xs leading-relaxed text-ink-soft line-clamp-2">{book.excerpt}</p>

        {/* Footer meta + action — pinned to bottom for equal heights */}
        <div className="mt-auto pt-3">
          <div className="flex flex-wrap items-center gap-2.5 text-xs text-ink-faint">
            <span className="flex items-center gap-1"><FileText className="h-3 w-3" />{toBn(book.pages)} পৃঃ</span>
            <span className="tabular">{toBn(Number(book.year))}</span>
            <span className="rounded bg-bone/50 px-1.5 py-0.5 font-mono text-xs">{book.id}</span>
          </div>
          <div className="mt-3">
            {book.pdf ? (
              <a
                href={book.pdf}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 rounded-lg border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
              >
                <FileText className="h-3.5 w-3.5" />পড়ুন<ExternalLink className="h-3 w-3" />
              </a>
            ) : (
              <span className="inline-flex items-center rounded-lg border border-dashed border-bone px-3 py-1.5 text-xs text-ink-faint">শীঘ্রই</span>
            )}
          </div>
        </div>
      </div>
    </motion.article>
  );
}

/* === Datasets Section — uniform card catalog with split bars === */
function DatasetsSection({ datasets, search, setSearch, category, setCategory }: { datasets: Dataset[]; search: string; setSearch: (v: string) => void; category: string; setCategory: (v: string) => void; }) {
  const [sort, setSort] = useState<SortKey>("curated");
  const searchRef = useRef<HTMLInputElement>(null);

  /* "/" focuses search from anywhere (unless typing or the command palette is open). */
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (paletteState.open) return;
      const t = e.target as HTMLElement | null;
      const typing = !!t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable);
      if (e.key === "/" && !typing) { e.preventDefault(); searchRef.current?.focus(); }
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
  const hasFilters = search || category !== "all";

  const statsRef = useRef<HTMLDivElement>(null);
  const statsInView = useInView(statsRef, { once: true, margin: "-40px" });

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }} transition={{ duration: dur.normal, ease: ease.smooth }} className="space-y-6">
      {/* Stats masthead — count-up on the integer figures */}
      {datasets.length > 0 && (
        <motion.div
          ref={statsRef}
          initial="hidden"
          animate="visible"
          variants={stagger}
          className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 rounded-xl border rule bg-paper px-4 py-3 shadow-sm"
        >
          <MastheadStat value={datasets.length} label="ডেটাসেট" tone="leaf" active={statsInView} />
          <span className="hidden h-4 w-px bg-bone sm:block" aria-hidden />
          <MastheadStat value={totalRecords} label="মোট রেকর্ড" tone="ochre" active={statsInView} format={(n) => (n >= 1000 ? `${toBn(Math.round(n / 1000))}K+` : toBn(n))} />
          <span className="hidden h-4 w-px bg-bone sm:block" aria-hidden />
          <MastheadStat value={0} label="মোট আকার" tone="ink" active={statsInView} staticValue={sizeLabel} />
          <span className="hidden h-4 w-px bg-bone sm:block" aria-hidden />
          <MastheadStat value={0} label="লাইসেন্স" tone="leaf" active={statsInView} staticValue="CC-BY-4.0" />
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
            className="w-full rounded-xl border rule bg-paper py-3.5 pl-12 pr-11 text-sm text-ink placeholder:text-ink-faint transition-colors focus:border-leaf focus:outline-none"
          />
          {search && (
            <button onClick={() => setSearch("")} aria-label="অনুসন্ধান মুছুন" className="absolute right-4 top-1/2 -translate-y-1/2 text-ink-faint transition-colors hover:text-ink">
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
        <SortControl sort={sort} setSort={setSort} />
      </div>

      {/* Category chips */}
      <ChipRow>
        {DATASET_CATEGORIES.map((cat) => (
          <Chip key={cat.id} active={category === cat.id} onClick={() => setCategory(cat.id === category ? "all" : cat.id)}>
            {cat.label}
          </Chip>
        ))}
      </ChipRow>

      {/* Active filters — removable chips */}
      <AnimatePresence>
        {hasFilters && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-ink-faint">সক্রিয় ফিল্টার:</span>
            {category !== "all" && (
              <FilterChip onClear={() => setCategory("all")}>
                {DATASET_CATEGORIES.find((c) => c.id === category)?.label ?? category}
              </FilterChip>
            )}
            {search && <FilterChip onClear={() => setSearch("")}>“{search}”</FilterChip>}
            <button onClick={() => { setSearch(""); setCategory("all"); }} className="text-xs text-leaf transition-colors hover:text-leaf-2">সব মুছুন</button>
          </motion.div>
        )}
      </AnimatePresence>

      <p className="text-sm text-ink-soft">{toBn(filtered.length)}টি ডেটাসেট পাওয়া গেছে</p>

      {/* Uniform equal-height card grid */}
      <motion.div initial="hidden" animate="visible" variants={stagger} className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <AnimatePresence mode="popLayout">
          {sorted.map((ds) => (
            <DatasetCard key={ds.id} ds={ds} />
          ))}
        </AnimatePresence>
      </motion.div>

      {filtered.length === 0 && datasets.length > 0 && <EmptyState onReset={() => { setSearch(""); setCategory("all"); }} />}
      {datasets.length === 0 && <LoadingState />}

      {/* Download-all CTA */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: dur.normal, ease: ease.smooth }} className="rounded-xl border rule bg-paper-2/30 p-5 text-center">
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

/* === Dataset card — with split-composition bar === */
function DatasetCard({ ds }: { ds: Dataset }) {
  const [showAllFields, setShowAllFields] = useState(false);
  const color = COLOR_MAP[ds.color] || "var(--color-leaf)";
  const Icon = DATASET_ICONS[ds.category] || Database;
  const splitEntries = Object.entries(ds.splits);
  const splitTotal = splitEntries.reduce((s, [, n]) => s + n, 0) || 1;

  return (
    <motion.article
      layout
      initial={{ opacity: 0, scale: 0.96, y: 8 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.92, y: -8 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      whileHover={{ y: -3 }}
      className="surface-lift flex h-full flex-col overflow-hidden rounded-xl border rule bg-paper"
    >
      {/* Color top bar */}
      <div className="h-1" style={{ backgroundColor: color }} />

      {/* Optional preview image — used by the vision dataset */}
      {ds.image && (
        <div className="relative">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={ds.image} alt={ds.image_caption ?? ds.name} className="h-40 w-full object-cover" loading="lazy" />
          {ds.badge && (
            <span className="absolute left-3 top-3 rounded-full bg-paper/95 px-2.5 py-1 text-xs font-semibold shadow-sm" style={{ color }}>
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
          <span className="shrink-0 rounded-md bg-bone/50 px-2 py-0.5 font-mono text-xs text-ink-soft">{ds.format}</span>
        </div>

        {/* Stats row */}
        <div className="mt-4 grid grid-cols-3 gap-2">
          <MiniStat value={ds.count >= 1000 ? `${toBn(Math.round(ds.count / 1000))}K` : toBn(ds.count)} label="রেকর্ড" color={color} />
          <MiniStat value={ds.size_mb >= 1024 ? `${toBn(Number((ds.size_mb / 1024).toFixed(1)))}GB` : `${toBn(Math.round(ds.size_mb))}MB`} label="আকার" color={color} />
          <MiniStat value={toBn(splitEntries.length)} label="স্প্লিট" color={color} />
        </div>

        {/* Description */}
        <p className="mt-3 text-xs leading-relaxed text-ink-soft">{ds.description}</p>

        {/* Split-composition bar — visual train/val/test proportions */}
        {splitEntries.length > 1 && (
          <div className="mt-3">
            <div className="flex h-2 w-full overflow-hidden rounded-full bg-bone/50">
              {splitEntries.map(([split, count], i) => (
                <motion.div
                  key={split}
                  initial={{ width: 0 }}
                  animate={{ width: `${(count / splitTotal) * 100}%` }}
                  transition={{ duration: dur.slow, ease: ease.smooth, delay: 0.1 + i * 0.06 }}
                  style={{ backgroundColor: SPLIT_COLORS[split] || "var(--color-leaf-3)" }}
                  title={`${split}: ${count.toLocaleString()}`}
                />
              ))}
            </div>
          </div>
        )}

        {/* Split chips */}
        <div className="mt-2.5 flex flex-wrap gap-1.5">
          {splitEntries.map(([split, count]) => (
            <span key={split} className="inline-flex items-center gap-1.5 rounded-md border rule px-2 py-0.5 text-xs text-ink-soft">
              <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: SPLIT_COLORS[split] || "var(--color-leaf-3)" }} />
              <span className="font-mono text-ochre">{split}</span>: <span className="tabular">{toBn(count)}</span>
            </span>
          ))}
        </div>

        {/* Use case */}
        <div className="mt-3 flex items-start gap-2">
          <Tag className="mt-0.5 h-3 w-3 shrink-0 text-ink-faint" />
          <p className="text-xs text-ink-faint">{ds.use_case}</p>
        </div>

        {/* Vision dataset — honest locked-model disclosure */}
        {ds.id === "soil_moisture" && (
          <p className="mt-3 text-xs text-ink-faint">
            লকড-মডেল নীতি: ডেটাসেট প্রকাশিত; স্বয়ংক্রিয় আর্দ্রতা নির্ণয় যাচাইয়ের পরে চালু হবে।
          </p>
        )}

        {/* Schema preview — first 4 fields always visible, reveal the rest */}
        <div className="mt-3 flex flex-wrap gap-1">
          {(showAllFields ? ds.fields : ds.fields.slice(0, 4)).map((f) => (
            <span key={f} className="rounded bg-bone/40 px-1.5 py-0.5 font-mono text-xs text-ink-soft">{f}</span>
          ))}
          {ds.fields.length > 4 && (
            <button
              onClick={() => setShowAllFields((v) => !v)}
              className="rounded bg-bone/40 px-1.5 py-0.5 font-mono text-xs text-leaf transition-colors hover:bg-leaf/10"
            >
              {showAllFields ? "কম দেখান" : `সব ${toBn(ds.fields.length)}টি`}
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
    </motion.article>
  );
}

/* === Count-up stat (books strip) === */
function CountStat({ value, label, tone, active }: { value: number; label: string; tone: "leaf" | "ochre" | "ink"; active: boolean }) {
  const n = useCountUp(value, active);
  const color = tone === "leaf" ? "text-leaf" : tone === "ochre" ? "text-ochre" : "text-ink";
  return (
    <div className="bg-paper px-4 py-3 text-center">
      <div className={cn("font-display text-xl tabular leading-none", color)}>{toBn(n)}</div>
      <div className="mt-1.5 text-xs text-ink-faint">{label}</div>
    </div>
  );
}

/* === Masthead stat (datasets) — count-up or static === */
function MastheadStat({ value, label, tone, active, format, staticValue }: { value: number; label: string; tone: "leaf" | "ochre" | "ink"; active: boolean; format?: (n: number) => string; staticValue?: string }) {
  const n = useCountUp(value, active);
  const color = tone === "leaf" ? "text-leaf" : tone === "ochre" ? "text-ochre" : "text-ink";
  const display = staticValue ?? (format ? format(n) : toBn(n));
  return (
    <div className="text-center">
      <div className={cn("font-display text-lg tabular leading-none", color)}>{display}</div>
      <div className="mt-1 text-xs text-ink-faint">{label}</div>
    </div>
  );
}

/* === Mini stat cell (dataset card) === */
function MiniStat({ value, label, color }: { value: string; label: string; color: string }) {
  return (
    <div className="rounded-md bg-paper-2/40 px-2 py-2 text-center">
      <div className="font-display text-sm tabular" style={{ color }}>{value}</div>
      <div className="text-xs text-ink-faint">{label}</div>
    </div>
  );
}

/* === Chip row wrapper === */
function ChipRow({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <Filter className="h-4 w-4 shrink-0 text-ink-faint" />
      {children}
    </div>
  );
}

/* === Category chip === */
function Chip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        "control-press rounded-full px-4 py-1.5 text-xs font-medium transition-colors",
        active ? "bg-leaf text-paper" : "border rule bg-paper text-ink-soft hover:border-leaf hover:text-leaf",
      )}
    >
      {children}
    </button>
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
              "relative rounded-md px-3 py-1.5 text-xs font-medium transition-colors",
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
    <span className="inline-flex items-center gap-1.5 rounded-full border border-leaf/30 bg-leaf/10 px-3 py-1 text-xs font-medium text-leaf">
      {children}
      <button onClick={onClear} aria-label="ফিল্টার মুছুন" className="transition-colors hover:text-leaf-2"><X className="h-3 w-3" /></button>
    </span>
  );
}

/* === Empty state === */
function EmptyState({ onReset }: { onReset: () => void }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-20 text-center">
      <Search className="mx-auto h-10 w-10 text-ink-faint" />
      <p className="mt-4 text-sm text-ink-soft">কিছু পাওয়া যায়নি।</p>
      <button onClick={onReset} className="mt-3 text-sm text-leaf transition-colors hover:text-leaf-2">ফিল্টার মুছুন</button>
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
