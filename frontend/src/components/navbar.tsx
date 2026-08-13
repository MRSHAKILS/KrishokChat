"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import { Phone, ChevronDown } from "lucide-react";
import { APP, HELPLINE } from "@/lib/constants";
import { cn } from "@/lib/utils";

/* =========================================================================
   Navbar — top-level navigation.

   Design decisions (from UI audit):
   - NO auth buttons. The project is a single-session live demo; login/register
     forms would mislead farmers and demo viewers. Replaced with a permanent,
     high-contrast 16123 Krishi Call Center pill (real verified helpline).
   - Primary nav surfaces the headline features — including the Library
     (লাইব্রেরি), the public data-resource hub for researchers. Secondary
     routes (data, contact, about) live under an "প্রকল্প" dropdown so the
     bar never crowds.
   - The 16123 pill is reachable on BOTH desktop and mobile — it is the
     single most important emergency action on the site.
   ========================================================================= */

const NAV = [
  { href: "/", label: "হোম" },
  { href: "/detect", label: "রোগ নির্ণয়" },
  { href: "/soil", label: "মাটি" },
  { href: "/chat", label: "পরামর্শ" },
  { href: "/library", label: "লাইব্রেরি" },
] as const;

const MORE = [
  { href: "/analytics", label: "লাইভ পরিসংখ্যান", desc: "এজেন্ট সিদ্ধান্ত ও স্থানীয় অডিট" },
  { href: "/research", label: "গবেষণা ও ফলাফল", desc: "পেপার, benchmark ও নিরাপত্তা নকশা" },
  { href: "/data", label: "উপাত্ত", desc: "ডেটাসেট ও গবেষণা উপাত্ত" },
  { href: "/about", label: "পরিচিতি", desc: "প্রকল্প ও প্রতিষ্ঠান" },
  { href: "/team", label: "দল", desc: "গবেষণা দল ও কৃতিত্ব" },
  { href: "/contact", label: "যোগাযোগ", desc: "জরুরি হেল্পলাইন ও সহায়তা" },
] as const;

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (moreRef.current && !moreRef.current.contains(e.target as Node)) {
        setMoreOpen(false);
      }
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  const moreActive = MORE.some((m) => pathname === m.href || pathname.startsWith(`${m.href}/`));

  return (
    <header className="sticky top-0 z-50 border-b rule bg-paper/85 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-2 px-5">
        {/* Wordmark */}
        <Link href="/" className="group flex shrink-0 items-center gap-2.5" aria-label={APP.nameEn}>
          <Mark />
          <div className="leading-none">
            <div className="font-display text-[17px] text-ink">{APP.name}</div>
            <div className="mt-0.5 text-[10px] text-ink-faint">{APP.nameEn}</div>
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden flex-1 items-center justify-center gap-0.5 lg:flex">
          {NAV.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative px-3 py-2 text-sm transition-colors",
                  active ? "text-leaf" : "text-ink-soft hover:text-ink",
                )}
              >
                {item.label}
                {active && (
                  <motion.span
                    layoutId="nav-underline"
                    className="absolute inset-x-3 -bottom-px h-px bg-leaf"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}

          {/* "আরও" dropdown — secondary routes */}
          <div ref={moreRef} className="relative">
            <button
              onClick={() => setMoreOpen((v) => !v)}
              aria-haspopup="menu"
              aria-expanded={moreOpen}
              className={cn(
                "flex items-center gap-1 px-3 py-2 text-sm transition-colors",
                moreActive || moreOpen ? "text-leaf" : "text-ink-soft hover:text-ink",
              )}
            >
              প্রকল্প
              <ChevronDown className={cn("h-3.5 w-3.5 transition-transform", moreOpen && "rotate-180")} />
            </button>
            <AnimatePresence>
              {moreOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 6, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 6, scale: 0.98 }}
                  transition={{ duration: 0.16, ease: [0.22, 1, 0.36, 1] }}
                  className="absolute right-0 top-full mt-1 w-64 overflow-hidden rounded-xl border rule bg-paper p-1.5 shadow-lg shadow-ink/5"
                >
                  <div className="px-3 py-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-ink-faint">
                    Project overview
                  </div>
                  {MORE.map((m) => {
                    const active = pathname === m.href || pathname.startsWith(`${m.href}/`);
                    return (
                      <Link
                        key={m.href}
                        href={m.href}
                        onClick={() => setMoreOpen(false)}
                        className={cn(
                          "block rounded-lg px-3 py-2.5 transition-colors",
                          active ? "bg-leaf/10" : "hover:bg-paper-2",
                        )}
                      >
                        <div className={cn("text-sm font-medium", active ? "text-leaf" : "text-ink")}>
                          {m.label}
                        </div>
                        <div className="mt-0.5 text-xs text-ink-faint">{m.desc}</div>
                      </Link>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </nav>

        {/* Right: 16123 call pill + mobile toggle */}
        <div className="flex shrink-0 items-center gap-2">
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="group relative hidden items-center gap-2 overflow-hidden rounded-full bg-leaf px-4 py-2 text-sm font-semibold text-paper shadow-sm transition-all hover:bg-leaf-2 hover:shadow-md hover:shadow-leaf/20 sm:flex"
            aria-label={`কৃষি কল সেন্টার ${HELPLINE.krishiCallCenter}`}
          >
            <span className="relative flex h-2.5 w-2.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-paper/70 opacity-75" />
              <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-paper" />
            </span>
            <Phone className="h-4 w-4" />
            <span className="tabular">{HELPLINE.krishiCallCenter}</span>
            <span className="hidden md:inline">কল করুন</span>
          </a>
          <button
            onClick={() => setOpen((v) => !v)}
            className="flex h-10 w-10 items-center justify-center rounded-md text-ink-soft transition-colors hover:bg-paper-2 lg:hidden"
            aria-label="মেনু"
            aria-expanded={open}
          >
            <span className="text-lg leading-none">{open ? "✕" : "☰"}</span>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-hidden border-t rule lg:hidden"
          >
            <div className="space-y-0.5 px-5 py-3">
              {NAV.map((item) => {
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setOpen(false)}
                    className={cn(
                      "block rounded-md px-3 py-2.5 text-sm transition-colors",
                      active ? "bg-paper-2 text-leaf" : "text-ink-soft hover:bg-paper-2/60",
                    )}
                  >
                    {item.label}
                  </Link>
                );
              })}
              {/* Secondary routes inline on mobile */}
              <div className="my-1 border-t rule pt-1">
                {MORE.map((item) => {
                  const active = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setOpen(false)}
                      className={cn(
                        "block rounded-md px-3 py-2.5 text-sm transition-colors",
                        active ? "bg-paper-2 text-leaf" : "text-ink-soft hover:bg-paper-2/60",
                      )}
                    >
                      {item.label}
                    </Link>
                  );
                })}
              </div>
              {/* Always-visible 16123 call card on mobile */}
              <a
                href={`tel:${HELPLINE.krishiCallCenter}`}
                className="mt-2 flex items-center justify-center gap-2 rounded-lg bg-leaf px-3 py-3 text-sm font-semibold text-paper"
              >
                <Phone className="h-4 w-4" />
                কৃষি কল সেন্টার
                <span className="tabular">{HELPLINE.krishiCallCenter}</span>
              </a>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}

/* A small custom mark — a stylized leaf-grain, not an emoji. */
function Mark() {
  return (
    <span className="relative flex h-9 w-9 items-center justify-center rounded-md bg-leaf text-paper">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden>
        <path
          d="M3 14C3 8 7 4 14 3.5C13.5 10 9.5 14 3 14Z"
          fill="currentColor"
          opacity="0.9"
        />
        <path
          d="M4 13.5C7 11 10 8 13 5"
          stroke="var(--color-ochre-soft)"
          strokeWidth="1"
          strokeLinecap="round"
        />
      </svg>
    </span>
  );
}
