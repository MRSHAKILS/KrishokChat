"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Search, Filter, X, ChevronDown, BookOpen,
  ExternalLink, FileText, Languages as LangIcon,
} from "lucide-react";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Library Page — professional catalog list, not card grid.
   No cover images needed — each book is a horizontal row.

   Features:
   - Live search (title/publisher/keyword)
   - Category + publisher filter chips
   - Grouped by publisher (collapsible)
   - Books with PDFs get "পড়ুন" button, rest get "শীঘ্রই"
   - Smooth layout animations on filter
   ========================================================================= */

type Book = {
  id: string;
  title_bn: string;
  title_en: string;
  publisher: string;
  category: string;
  pages: number;
  year: string;
  language: string;
  excerpt: string;
  pdf: string | null;
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
  { id: "economics", label: "অর্থনীতি" },
];

// Publisher colors
const PUBLISHER_COLORS: Record<string, string> = {
  BRRI: "var(--color-leaf)",
  IRRI: "var(--color-leaf-2)",
  BARC: "var(--color-ochre)",
  SRDI: "var(--color-ochre)",
  MoA: "var(--color-clay)",
  BARI: "var(--color-leaf)",
  CDB: "var(--color-ochre)",
  BSRTI: "var(--color-ochre)",
  CABI: "var(--color-leaf-2)",
  NARS: "var(--color-ink-soft)",
  DAE: "var(--color-clay)",
  DLS: "var(--color-leaf-2)",
  DoF: "var(--color-leaf)",
  FAO: "var(--color-ochre)",
};

export default function LibraryPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [expandedPublishers, setExpandedPublishers] = useState<Set<string>>(new Set());
  const [books, setBooks] = useState<Book[]>([]);

  // Load catalog
  if (books.length === 0 && typeof window !== "undefined") {
    fetch("/library/catalog.json")
      .then((r) => r.json())
      .then((data) => setBooks(data.books))
      .catch(() => setBooks([]));
  }

  const filtered = useMemo(() => {
    return books.filter((book) => {
      const matchesCategory = category === "all" || book.category === category;
      const q = search.toLowerCase().trim();
      const matchesSearch =
        !q ||
        book.title_en.toLowerCase().includes(q) ||
        book.title_bn.includes(q) ||
        book.publisher.toLowerCase().includes(q) ||
        book.excerpt.includes(q) ||
        book.id.toLowerCase().includes(q);
      return matchesCategory && matchesSearch;
    });
  }, [books, search, category]);

  // Group by publisher
  const grouped = useMemo(() => {
    const groups: Record<string, Book[]> = {};
    for (const book of filtered) {
      if (!groups[book.publisher]) groups[book.publisher] = [];
      groups[book.publisher].push(book);
    }
    return Object.entries(groups).sort((a, b) => a[0].localeCompare(b[0]));
  }, [filtered]);

  const togglePublisher = (pub: string) => {
    setExpandedPublishers((prev) => {
      const next = new Set(prev);
      if (next.has(pub)) next.delete(pub);
      else next.add(pub);
      return next;
    });
  };

  const availableCount = books.filter((b) => b.pdf).length;

  return (
    <div className="mx-auto max-w-5xl space-y-8 py-14">
      {/* Hero */}
      <motion.section initial="hidden" animate="visible" variants={stagger} className="text-center">
        <motion.p variants={enter} className="text-xs uppercase tracking-[0.22em] text-ochre">Library</motion.p>
        <motion.h1 variants={enter} className="mt-4 font-display text-4xl leading-tight text-ink">
          কৃষি <span className="text-leaf">জ্ঞান ভান্ডার</span>
        </motion.h1>
        <motion.p variants={enter} className="mx-auto mt-4 max-w-lg text-base text-ink-soft">
          {books.length}টি সরকারি কৃষি প্রকাশনা — ১৩টি প্রতিষ্ঠান থেকে। অনুসন্ধান করুন, পড়ুন, জানুন।
        </motion.p>
        {availableCount > 0 && (
          <motion.p variants={enter} className="mt-2 text-xs text-leaf">
            {availableCount}টি বই এখন পঠনযোগ্য
          </motion.p>
        )}
      </motion.section>

      {/* Search bar */}
      <motion.section initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={enter} className="relative">
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-ink-faint" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="বই, প্রকাশক, বা বিষয় খুঁজুন..."
            className="w-full rounded-xl border rule bg-paper py-3.5 pl-12 pr-4 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
          />
          {search && (
            <button onClick={() => setSearch("")} className="absolute right-4 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink">
              <X className="h-4 w-4" />
            </button>
          )}
        </motion.div>
      </motion.section>

      {/* Category filters */}
      <motion.section initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={enter} className="flex flex-wrap items-center gap-2">
          <Filter className="h-4 w-4 text-ink-faint" />
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setCategory(cat.id)}
              className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${
                category === cat.id
                  ? "bg-leaf text-paper"
                  : "border rule bg-paper text-ink-soft hover:border-leaf hover:text-leaf"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </motion.div>
      </motion.section>

      {/* Result count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-ink-soft">{filtered.length}টি বই পাওয়া গেছে</p>
        {grouped.length > 0 && (
          <button
            onClick={() => {
              const allPubs = grouped.map(([pub]) => pub);
              const allExpanded = allPubs.every((p) => expandedPublishers.has(p));
              setExpandedPublishers(allExpanded ? new Set() : new Set(allPubs));
            }}
            className="text-xs text-leaf hover:text-leaf-2"
          >
            {expandedPublishers.size === grouped.length ? "সব বন্ধ করুন" : "সব খুলুন"}
          </button>
        )}
      </div>

      {/* Book list — grouped by publisher */}
      <motion.div initial="hidden" animate="visible" variants={stagger} className="space-y-4">
        <AnimatePresence mode="popLayout">
          {grouped.map(([publisher, pubBooks]) => {
            const isExpanded = expandedPublishers.has(publisher) || expandedPublishers.size === 0;
            const color = PUBLISHER_COLORS[publisher] || "var(--color-ink-soft)";
            return (
              <motion.div
                key={publisher}
                layout
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: dur.normal, ease: ease.smooth }}
                className="overflow-hidden rounded-xl border rule bg-paper"
              >
                {/* Publisher header */}
                <button
                  onClick={() => togglePublisher(publisher)}
                  className="flex w-full items-center justify-between px-5 py-3.5 transition-colors hover:bg-paper-2/40"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-md font-display text-xs font-medium" style={{ backgroundColor: `color-mix(in srgb, ${color} 12%, transparent)`, color }}>
                      {publisher.slice(0, 3)}
                    </div>
                    <div className="text-left">
                      <span className="font-display text-base text-ink">{publisher}</span>
                      <span className="ml-2 text-xs text-ink-faint">{pubBooks.length}টি বই</span>
                    </div>
                  </div>
                  <ChevronDown className={`h-4 w-4 text-ink-faint transition-transform ${isExpanded ? "rotate-180" : ""}`} />
                </button>

                {/* Books in this publisher */}
                <AnimatePresence initial={false}>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: dur.normal, ease: ease.smooth }}
                      className="overflow-hidden"
                    >
                      <div className="divide-y divide-bone border-t rule">
                        {pubBooks.map((book) => (
                          <BookRow key={book.id} book={book} color={color} />
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </motion.div>

      {/* Empty state */}
      {filtered.length === 0 && books.length > 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-20 text-center">
          <Search className="mx-auto h-10 w-10 text-ink-faint" />
          <p className="mt-4 text-sm text-ink-soft">কোনো বই পাওয়া যায়নি।</p>
          <button onClick={() => { setSearch(""); setCategory("all"); }} className="mt-3 text-sm text-leaf hover:text-leaf-2">
            ফিল্টার মুছুন
          </button>
        </motion.div>
      )}

      {/* Loading state */}
      {books.length === 0 && (
        <div className="py-20 text-center">
          <BookOpen className="mx-auto h-10 w-10 animate-pulse text-ink-faint" />
          <p className="mt-4 text-sm text-ink-faint">লোড হচ্ছে…</p>
        </div>
      )}
    </div>
  );
}

/* === Single book row === */
function BookRow({ book, color }: { book: Book; color: string }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: dur.fast }}
      className="group flex items-start gap-4 px-5 py-4 transition-colors hover:bg-paper-2/30"
    >
      {/* Left border accent */}
      <div className="mt-1 h-12 w-1 shrink-0 rounded-full" style={{ backgroundColor: color, opacity: 0.3 }} />

      {/* Book info */}
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h3 className="font-display text-sm text-ink">{book.title_bn}</h3>
            <p className="mt-0.5 text-xs text-ink-faint">{book.title_en}</p>
          </div>
          {/* Read button */}
          {book.pdf ? (
            <a
              href={book.pdf}
              target="_blank"
              rel="noopener noreferrer"
              className="flex shrink-0 items-center gap-1.5 rounded-lg border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf"
            >
              <FileText className="h-3.5 w-3.5" />
              পড়ুন
              <ExternalLink className="h-3 w-3" />
            </a>
          ) : (
            <span className="shrink-0 rounded-lg border border-dashed border-bone px-3 py-1.5 text-[11px] text-ink-faint">
              শীঘ্রই
            </span>
          )}
        </div>
        {/* Excerpt */}
        <p className="mt-1.5 text-xs leading-relaxed text-ink-soft line-clamp-2">{book.excerpt}</p>
        {/* Meta */}
        <div className="mt-2 flex flex-wrap items-center gap-3 text-[10px] text-ink-faint">
          <span className="flex items-center gap-1"><FileText className="h-3 w-3" />{book.pages} পৃঃ</span>
          <span className="tabular">{book.year}</span>
          <span className="flex items-center gap-1"><LangIcon className="h-3 w-3" />{book.language}</span>
          <span className="rounded bg-bone/50 px-1.5 py-0.5 font-mono">{book.id}</span>
        </div>
      </div>
    </motion.div>
  );
}
