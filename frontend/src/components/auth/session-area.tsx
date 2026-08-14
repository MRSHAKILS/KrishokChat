"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import { ChevronDown, LogOut, Bookmark } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { cn } from "@/lib/utils";

/* =========================================================================
   SessionArea — navbar auth surface (additive, never blocking).

   Anonymous visitors see a small "লগইন" pill. Signed-in visitors see an
   account chip with a sign-out dropdown. This component NEVER redirects,
   never pops up, and never degrades the anonymous demo (AGENTS.md §2 rule 1).
   ========================================================================= */

export function SessionArea() {
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
    return <div className="hidden h-9 w-16 animate-pulse rounded-full bg-paper-2/60 sm:block" />;
  }

  if (!user) {
    return (
      <Link
        href="/auth"
        className="hidden items-center rounded-full border rule bg-paper-2/40 px-4 py-2 text-sm font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink sm:flex"
      >
        লগইন
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
    <div ref={ref} className="relative hidden sm:block">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={open}
        className={cn(
          "flex items-center gap-2 rounded-full border rule bg-paper-2/40 py-1.5 pl-1.5 pr-3 text-sm transition-colors hover:border-leaf",
          open && "border-leaf",
        )}
      >
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-leaf text-xs font-bold text-paper">
          {initial}
        </span>
        <span className="max-w-28 truncate text-ink-soft">{email}</span>
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