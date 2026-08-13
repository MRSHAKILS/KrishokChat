"use client";

/* =========================================================================
   CommandMenu — site-wide Ctrl+K / "/" palette (cmdk 1.1.1, pinned).
   Searchable index over: pages, datasets, books. Data comes from the same
   static JSON the library page uses — no backend, no new endpoints.
   Dep version verified: https://www.npmjs.com/package/cmdk (React 19 peer OK).
   ========================================================================= */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Command } from "cmdk";
import { motion, AnimatePresence } from "motion/react";
import {
  Home, BookOpen, Database, Network, Sprout, ScanSearch, FlaskConical,
  BarChart3, Info, Users, Search, FileText, CornerDownLeft,
} from "lucide-react";
import { dur, ease } from "@/lib/motion";

/* Module-level palette state — lets pages (e.g. /library's "/" shortcut)
   know the palette is open so their own shortcuts don't double-fire. */
export const paletteState = { open: false };

/* ---- data (cached once, same JSON as the library page) ---- */
type DatasetLite = { id: string; name: string; name_bn: string; count: number; format: string; category: string };
type BookLite = { id: string; title_bn: string; title_en: string; publisher: string };

let datasetsCache: DatasetLite[] | null = null;
let booksCache: BookLite[] | null = null;

async function loadIndex() {
  if (datasetsCache === null) {
    try {
      const r = await fetch("/library/datasets.json");
      datasetsCache = (await r.json()).datasets.map((d: DatasetLite) => d);
    } catch { datasetsCache = []; }
  }
  if (booksCache === null) {
    try {
      const r = await fetch("/library/catalog.json");
      booksCache = (await r.json()).books.map((b: BookLite) => b);
    } catch { booksCache = []; }
  }
}

/* ---- route index ---- */
const ROUTES = [
  { href: "/", label: "হোম", hint: "ল্যান্ডিং পেজ", icon: Home },
  { href: "/library", label: "জ্ঞান ভান্ডার", hint: "বই ও ডেটাসেট", icon: BookOpen },
  { href: "/data", label: "জ্ঞান গ্রাফ ও উপাত্ত", hint: "নোড · এনটিটি · পরিসংখ্যান", icon: Network },
  { href: "/soil", label: "মাটি কনসোল", hint: "আর্দ্রতা নির্ণয়", icon: Sprout },
  { href: "/chat", label: "কৃষি পরামর্শ", hint: "নিরাপত্তা-সচেতন QA", icon: ScanSearch },
  { href: "/detect", label: "রোগ শনাক্ত", hint: "ছবি-ভিত্তিক", icon: FlaskConical },
  { href: "/research", label: "গবেষণা", hint: "পদ্ধতি · নিরাপত্তা · বেঞ্চমার্ক", icon: BarChart3 },
  { href: "/about", label: "প্রকল্প পরিচিতি", hint: "লক্ষ্য ও সুযোগ", icon: Info },
  { href: "/team", label: "দল", hint: "গবেষক", icon: Users },
] as const;

function isTypingTarget(t: EventTarget | null): boolean {
  if (!(t instanceof HTMLElement)) return false;
  return t instanceof HTMLInputElement || t instanceof HTMLTextAreaElement || t.isContentEditable;
}

export default function CommandMenu() {
  const [open, setOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    paletteState.open = open;
  }, [open]);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((o) => !o);
        return;
      }
      if (e.key === "/" && !isTypingTarget(e.target)) {
        e.preventDefault();
        setOpen(true);
      }
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  useEffect(() => {
    if (open) loadIndex();
  }, [open]);

  const go = (href: string) => {
    setOpen(false);
    router.push(href);
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-start justify-center bg-ink/25 px-4 pt-[10vh] backdrop-blur-sm"
          onClick={() => setOpen(false)}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: dur.fast, ease: ease.out }}
        >
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label="কমান্ড প্যালেট"
            className="w-full max-w-xl overflow-hidden rounded-2xl border rule bg-paper shadow-[0_24px_64px_rgba(52,39,23,0.18)]"
            onClick={(e) => e.stopPropagation()}
            initial={{ opacity: 0, scale: 0.97, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.98, y: -4 }}
            transition={{ duration: dur.normal, ease: ease.smooth }}
          >
            <Command className="text-ink">
              <div className="flex items-center gap-3 border-b rule px-4 py-3.5">
                <Search className="h-4 w-4 shrink-0 text-ink-faint" />
                <Command.Input
                  autoFocus
                  placeholder="পৃষ্ঠা, ডেটাসেট বা বই খুঁজুন…"
                  className="w-full bg-transparent text-sm text-ink outline-none placeholder:text-ink-faint"
                />
                <kbd className="shrink-0 rounded-md border rule bg-bone px-1.5 py-0.5 font-mono text-[10px] text-ink-faint">esc</kbd>
              </div>

              <Command.List className="max-h-[min(60vh,420px)] overflow-y-auto p-2">
                <Command.Empty className="px-3 py-8 text-center text-sm text-ink-faint">
                  কিছু পাওয়া যায়নি — অন্য শব্দ চেষ্টা করুন
                </Command.Empty>

                <Command.Group
                  heading="পৃষ্ঠা"
                  className="text-ink-soft [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:pb-1.5 [&_[cmdk-group-heading]]:pt-2 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:font-semibold [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-[0.18em] [&_[cmdk-group-heading]]:text-ink-faint"
                >
                  {ROUTES.map((r) => (
                    <Command.Item
                      key={r.href}
                      value={`${r.label} ${r.hint} ${r.href}`}
                      onSelect={() => go(r.href)}
                      className="flex cursor-pointer items-center gap-3 rounded-lg px-2.5 py-2 text-sm data-[selected=true]:bg-bone"
                    >
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                        <r.icon className="h-4 w-4" />
                      </span>
                      <span className="flex-1 text-ink">{r.label}</span>
                      <span className="text-xs text-ink-faint">{r.hint}</span>
                    </Command.Item>
                  ))}
                </Command.Group>

                <Command.Group
                  heading="ডেটাসেট"
                  className="text-ink-soft [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:pb-1.5 [&_[cmdk-group-heading]]:pt-2 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:font-semibold [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-[0.18em] [&_[cmdk-group-heading]]:text-ink-faint"
                >
                  {datasetsCache?.map((d) => (
                    <Command.Item
                      key={d.id}
                      value={`${d.name_bn} ${d.name} ${d.category} ${d.format}`}
                      onSelect={() => go("/library")}
                      className="flex cursor-pointer items-center gap-3 rounded-lg px-2.5 py-2 text-sm data-[selected=true]:bg-bone"
                    >
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-ochre/10 text-ochre">
                        <Database className="h-4 w-4" />
                      </span>
                      <span className="flex-1 text-ink">{d.name_bn}</span>
                      <span className="font-mono text-[10px] text-ink-faint">{d.format}</span>
                    </Command.Item>
                  ))}
                </Command.Group>

                <Command.Group
                  heading="বই ও প্রকাশনা"
                  className="text-ink-soft [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:pb-1.5 [&_[cmdk-group-heading]]:pt-2 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:font-semibold [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-[0.18em] [&_[cmdk-group-heading]]:text-ink-faint"
                >
                  {booksCache?.slice(0, 40).map((b) => (
                    <Command.Item
                      key={b.id}
                      value={`${b.title_bn} ${b.title_en} ${b.publisher}`}
                      onSelect={() => go("/library")}
                      className="flex cursor-pointer items-center gap-3 rounded-lg px-2.5 py-2 text-sm data-[selected=true]:bg-bone"
                    >
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-leaf/10 text-leaf">
                        <FileText className="h-4 w-4" />
                      </span>
                      <span className="flex-1 truncate text-ink">{b.title_bn}</span>
                      <span className="text-xs text-ink-faint">{b.publisher}</span>
                    </Command.Item>
                  ))}
                </Command.Group>
              </Command.List>

              <div className="flex items-center justify-between border-t rule px-4 py-2.5 text-[10px] text-ink-faint">
                <span>↑↓ নেভিগেট · ↵ নির্বাচন · esc বন্ধ</span>
                <span className="flex items-center gap-1">
                  <CornerDownLeft className="h-3 w-3" />Ctrl K দিয়ে খুলুন
                </span>
              </div>
            </Command>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}