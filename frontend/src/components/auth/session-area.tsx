"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, LogOut, Bookmark, UserRound } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { cn } from "@/lib/utils";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   SessionArea — navbar auth surface (additive, never blocking).

   Anonymous visitors see a small "লগইন" pill. Signed-in visitors see an
   account chip with a sign-out dropdown. This component NEVER redirects,
   never pops up, and never degrades the anonymous demo (AGENTS.md §2 rule 1).
   ========================================================================= */

export function SessionArea() {
  const { locale } = useLanguage();
  const en = locale === "en";
  const router = useRouter();
  const { user, loading } = useSupabaseSession();
  const [open, setOpen] = useState(false);
  const [signingOut, setSigningOut] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  if (loading) {
    return <div className="h-9 w-9 animate-pulse rounded-full bg-paper-2/60 sm:w-16" />;
  }

  if (!user) {
    return (
      <Link
        href="/auth"
        aria-label={en ? "Log in or register" : "লগইন / নিবন্ধন"}
        className="flex items-center justify-center gap-1.5 rounded-full border rule bg-paper-2/40 px-2.5 py-2 text-sm font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink sm:px-4"
      >
        <UserRound className="h-4 w-4" aria-hidden />
        <span className="hidden sm:inline">{en ? "Log in" : "লগইন"}</span>
      </Link>
    );
  }

  const email = user.email ?? "অ্যাকাউন্ট";
  const initial = email.charAt(0).toUpperCase();

  async function handleSignOut() {
    setSigningOut(true);
    const supabase = createClient();
    await supabase.auth.signOut();
    setOpen(false);
    router.refresh();
  }

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label="অ্যাকাউন্ট মেনু"
        className={cn(
          "flex items-center gap-2 rounded-full border rule bg-paper-2/40 py-1.5 pl-1.5 pr-2 text-sm transition-colors hover:border-leaf sm:pr-3",
          open && "border-leaf",
        )}
      >
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-leaf text-xs font-bold text-paper">
          {initial}
        </span>
        <span className="hidden max-w-28 truncate text-ink-soft sm:inline">{email}</span>
        <ChevronDown className={cn("h-3.5 w-3.5 text-ink-faint transition-transform", open && "rotate-180")} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 6, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 6, scale: 0.98 }}
            transition={{ duration: 0.16, ease: [0.22, 1, 0.36, 1] }}
            className="absolute right-0 top-full mt-2 w-60 overflow-hidden rounded-xl border rule bg-paper p-1.5 shadow-lg shadow-ink/5"
          >
            <div className="px-3 py-2">
              <div className="truncate text-sm font-medium text-ink">{email}</div>
              <div className="mt-0.5 text-xs text-ink-faint">সাইন-ইন করা আছে</div>
            </div>
            <Link
              href="/account"
              onClick={() => setOpen(false)}
              className="flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-sm text-ink-soft transition-colors hover:bg-paper-2"
            >
              <Bookmark className="h-4 w-4" />
              আমার হিসাব
            </Link>
            <button
              onClick={handleSignOut}
              disabled={signingOut}
              className="flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-sm text-ink-soft transition-colors hover:bg-paper-2 disabled:opacity-50"
            >
              <LogOut className="h-4 w-4" />
              {signingOut ? "লগ আউট হচ্ছে..." : "লগ আউট"}
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}