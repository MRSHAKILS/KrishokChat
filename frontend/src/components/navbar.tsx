"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import { LogIn, UserPlus, Phone } from "lucide-react";
import { APP, HELPLINE } from "@/lib/constants";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/", label: "হোম" },
  { href: "/detect", label: "রোগ নির্ণয়" },
  { href: "/chat", label: "পরামর্শ" },
  { href: "/research", label: "গবেষণা" },
  { href: "/library", label: "লাইব্রেরি" },
  { href: "/about", label: "পরিচিতি" },
] as const;

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b rule bg-paper/85 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        {/* Wordmark */}
        <Link href="/" className="group flex items-center gap-2.5" aria-label={APP.nameEn}>
          <Mark />
          <div className="leading-none">
            <div className="font-display text-[17px] text-ink">{APP.name}</div>
            <div className="mt-0.5 text-[10px] uppercase tracking-[0.18em] text-ink-faint">
              {APP.nameEn}
            </div>
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-1 md:flex">
          {NAV.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative px-3.5 py-2 text-sm transition-colors",
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
        </nav>

        {/* Auth buttons + mobile toggle */}
        <div className="flex items-center gap-2">
          <Link
            href="/auth"
            className="hidden items-center gap-1.5 rounded-md border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-leaf sm:flex"
          >
            <LogIn className="h-3.5 w-3.5" />
            প্রবেশ
          </Link>
          <Link
            href="/auth?mode=register"
            className="hidden items-center gap-1.5 rounded-md bg-leaf px-3 py-1.5 text-xs font-medium text-paper transition-colors hover:bg-leaf-2 sm:flex"
          >
            <UserPlus className="h-3.5 w-3.5" />
            নিবন্ধন
          </Link>
          <button
            onClick={() => setOpen((v) => !v)}
            className="flex h-9 w-9 items-center justify-center rounded-md text-ink-soft transition-colors hover:bg-paper-2 md:hidden"
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
            className="overflow-hidden border-t rule md:hidden"
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
              <div className="mt-2 flex gap-2">
                <Link
                  href="/auth"
                  onClick={() => setOpen(false)}
                  className="flex flex-1 items-center justify-center gap-1.5 rounded-md border rule px-3 py-2.5 text-sm font-medium text-ink-soft"
                >
                  <LogIn className="h-3.5 w-3.5" />
                  প্রবেশ
                </Link>
                <Link
                  href="/auth?mode=register"
                  onClick={() => setOpen(false)}
                  className="flex flex-1 items-center justify-center gap-1.5 rounded-md bg-leaf px-3 py-2.5 text-sm font-medium text-paper"
                >
                  <UserPlus className="h-3.5 w-3.5" />
                  নিবন্ধন
                </Link>
              </div>
              <a
                href={`tel:${HELPLINE.krishiCallCenter}`}
                className="mt-2 flex items-center justify-center gap-2 rounded-md bg-paper-2 px-3 py-2.5 text-sm font-medium text-ink-soft"
              >
                <Phone className="h-3.5 w-3.5" />
                কৃষক কল সেন্টার <span className="tabular">{HELPLINE.krishiCallCenter}</span>
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
