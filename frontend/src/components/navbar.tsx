"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import { Phone, ChevronDown, LogOut, Sun, Languages } from "lucide-react";
import { APP, HELPLINE, HELPLINE_EN } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { SessionArea } from "@/components/auth/session-area";
import { NotificationBell } from "@/components/notifications/notification-bell";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { createClient } from "@/lib/supabase/client";
import { useLanguage } from "@/context/language-context";

/* =========================================================================
   Navbar — Clean, Spacious & Uncluttered Top Navigation with i18n Toggle.
   ========================================================================= */

export function Navbar() {
  const pathname = usePathname();
  const { t, locale, toggleLocale } = useLanguage();
  const helplineShown = locale === "en" ? HELPLINE_EN : HELPLINE;
  const [open, setOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const [sunlight, setSunlight] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);

  const NAV = [
    { href: "/", label: t.nav.home },
    { href: "/detect", label: t.nav.detect },
    { href: "/soil", label: t.nav.soil },
    { href: "/chat", label: t.nav.chat },
    { href: "/library", label: t.nav.library },
  ] as const;

  const MORE = [
    { href: "/analytics", label: t.nav.analytics, desc: t.nav.analyticsDesc },
    { href: "/research", label: t.nav.research, desc: t.nav.researchDesc },
    { href: "/business", label: t.nav.business, desc: t.nav.businessDesc },
    { href: "/data", label: t.nav.data, desc: t.nav.dataDesc },
    { href: "/about", label: t.nav.about, desc: t.nav.aboutDesc },
    { href: "/team", label: t.nav.team, desc: t.nav.teamDesc },
    { href: "/contact", label: t.nav.contact, desc: t.nav.contactDesc },
  ] as const;

  useEffect(() => {
    try {
      const isSun = localStorage.getItem("krishokchat:contrast") === "sunlight";
      if (isSun) {
        setSunlight(true);
        document.documentElement.setAttribute("data-contrast", "sunlight");
      }
    } catch {
      // Storage unavailable
    }
  }, []);

  const toggleSunlight = () => {
    const next = !sunlight;
    setSunlight(next);
    try {
      if (next) {
        document.documentElement.setAttribute("data-contrast", "sunlight");
        localStorage.setItem("krishokchat:contrast", "sunlight");
      } else {
        document.documentElement.removeAttribute("data-contrast");
        localStorage.removeItem("krishokchat:contrast");
      }
    } catch {
      // Storage unavailable
    }
  };

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
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-5">
        {/* Wordmark */}
        <Link href="/" className="group flex shrink-0 items-center gap-2.5" aria-label={APP.nameEn}>
          <Mark />
          <div className="leading-none">
            {locale === "en" ? (
              <div className="font-display text-[14px] text-ink">{APP.nameEn}</div>
            ) : (
              <div className="font-display text-[17px] text-ink">{APP.name}</div>
            )}
            {locale !== "en" && <div className="mt-0.5 text-xs text-ink-faint">{APP.nameEn}</div>}
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden flex-1 items-center justify-center gap-1 md:flex">
          {NAV.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative px-3.5 py-2 text-sm whitespace-nowrap transition-colors",
                  active ? "text-leaf font-medium" : "text-ink-soft hover:text-ink",
                )}
              >
                {item.label}
                {active && (
                  <motion.span
                    layoutId="nav-underline"
                    className="absolute inset-x-3.5 -bottom-px h-px bg-leaf"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}

          {/* "প্রকল্প" dropdown — secondary routes */}
          <div ref={moreRef} className="relative">
            <button
              onClick={() => setMoreOpen((v) => !v)}
              aria-haspopup="menu"
              aria-expanded={moreOpen}
              className={cn(
                "flex items-center gap-1 px-3 py-2 text-sm whitespace-nowrap transition-colors cursor-pointer",
                moreActive || moreOpen ? "text-leaf font-medium" : "text-ink-soft hover:text-ink",
              )}
            >
              {t.nav.project}
              <ChevronDown className={cn("h-3.5 w-3.5 transition-transform duration-200", moreOpen && "rotate-180")} />
            </button>
            <AnimatePresence>
              {moreOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 6, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 6, scale: 0.98 }}
                  transition={{ duration: 0.16, ease: [0.22, 1, 0.36, 1] }}
                  className="absolute right-0 top-full mt-1.5 w-64 overflow-hidden rounded-xl border rule bg-paper p-1.5 shadow-lg shadow-ink/5 z-50"
                >
                  <div className="px-3 py-2 text-xs font-semibold text-ink-faint">
                    {t.nav.otherPages}
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

        {/* Right: Language switch + Sunlight mode + session area + mobile toggle */}
        <div className="flex shrink-0 items-center gap-2 sm:gap-2.5">
          {/* Krishi Call Center — always reachable, desktop too */}
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            title={t.nav.helplineTitle}
            className="control-press hidden items-center gap-1.5 rounded-full bg-leaf px-3.5 py-1.5 text-xs font-bold tabular text-paper whitespace-nowrap transition-opacity hover:opacity-90 md:inline-flex"
          >
            <Phone className="h-3.5 w-3.5" aria-hidden />
            <span>{helplineShown.krishiCallCenter}</span>
          </a>

          {/* Language Change Icon & Switcher Button */}
          <button
            type="button"
            onClick={toggleLocale}
            className="control-press inline-flex items-center gap-1.5 rounded-full border border-bone bg-paper-2/50 px-2.5 py-1.5 text-xs font-semibold text-ink-soft hover:border-leaf/40 hover:bg-paper hover:text-ink transition-all cursor-pointer"
            title={t.nav.langToggleTitle}
            aria-label={t.nav.langToggleTitle}
          >
            <Languages className="h-3.5 w-3.5 text-leaf" aria-hidden />
            <span
              className={cn(
                "rounded-md px-1.5 py-0.5 text-[10px] font-bold uppercase transition-colors",
                locale === "bn" ? "bg-leaf text-paper" : "text-ink-soft",
              )}
            >
              বাং
            </span>
            <span className="text-ink-faint/60">/</span>
            <span
              className={cn(
                "rounded-md px-1.5 py-0.5 text-[10px] font-bold uppercase transition-colors",
                locale === "en" ? "bg-leaf text-paper" : "text-ink-soft",
              )}
            >
              EN
            </span>
          </button>

          {/* Sunlight Mode Toggle */}
          <button
            type="button"
            onClick={toggleSunlight}
            className={cn(
              "control-press inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-semibold whitespace-nowrap transition-all cursor-pointer",
              sunlight
                ? "border-ochre bg-ochre/20 text-ochre shadow-2xs ring-1 ring-ochre/50"
                : "border-bone bg-paper-2/50 text-ink-soft hover:border-leaf/40 hover:bg-paper hover:text-ink"
            )}
            title={t.nav.sunlightTitle}
            aria-pressed={sunlight}
          >
            <Sun className={cn("h-3.5 w-3.5", sunlight && "text-ochre animate-spin-slow")} />
            <span className="hidden sm:inline">{sunlight ? t.nav.sunlightOn : t.nav.sunlightOff}</span>
          </button>

          {/* Notifications (admin broadcasts) — renders nothing when disabled */}
          <NotificationBell />

          {/* User Session / Login Button */}
          <SessionArea />

          {/* Mobile Menu Button */}
          <button
            onClick={() => setOpen((v) => !v)}
            className="flex h-10 w-10 items-center justify-center rounded-md text-ink-soft transition-colors hover:bg-paper-2 md:hidden"
            aria-label={t.nav.menu}
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
              {/* Language Switch Row on Mobile */}
              <div className="mb-2 flex items-center justify-between rounded-lg border rule bg-paper-2/40 px-3 py-2">
                <span className="flex items-center gap-2 text-xs font-medium text-ink">
                  <Languages className="h-4 w-4 text-leaf" />
                  <span>{locale === "bn" ? "ভাষা (Language)" : "Language (ভাষা)"}</span>
                </span>
                <button
                  type="button"
                  onClick={toggleLocale}
                  className="inline-flex items-center gap-1 rounded-full border border-leaf/30 bg-leaf/10 px-3 py-1 text-xs font-bold text-leaf hover:bg-leaf/20 cursor-pointer"
                >
                  <span>{locale === "bn" ? "English এ পরিবর্তন" : "বাংলায় পরিবর্তন"}</span>
                </button>
              </div>

              {/* Account row — additive, never blocking */}
              <MobileAccountRow />
              {NAV.map((item) => {
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setOpen(false)}
                    className={cn(
                      "block rounded-md px-3 py-2.5 text-sm transition-colors",
                      active ? "bg-paper-2 text-leaf font-medium" : "text-ink-soft hover:bg-paper-2/60",
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
                        active ? "bg-paper-2 text-leaf font-medium" : "text-ink-soft hover:bg-paper-2/60",
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
                {t.nav.callCenter}
                <span className="tabular">{helplineShown.krishiCallCenter}</span>
              </a>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}

/* Mobile account row — shows login link or signed-in state with sign-out. */
function MobileAccountRow() {
  const { user, loading } = useSupabaseSession();
  const { t } = useLanguage();
  const [signingOut, setSigningOut] = useState(false);
  const router = useRouter();

  if (loading) return null;

  if (!user) {
    return (
      <Link
        href="/auth"
        className="block rounded-md px-3 py-2.5 text-sm font-medium text-leaf transition-colors hover:bg-paper-2/60"
      >
        {t.nav.login}
      </Link>
    );
  }

  async function handleSignOut() {
    setSigningOut(true);
    const supabase = createClient();
    await supabase.auth.signOut();
    router.refresh();
  }

  return (
    <div className="mb-1 flex items-center justify-between gap-2 rounded-md bg-paper-2/40 px-3 py-2.5">
      <div className="min-w-0">
        <div className="truncate text-sm font-medium text-ink">{user.email}</div>
        <div className="text-xs text-ink-faint">{t.nav.signedIn}</div>
      </div>
      <button
        onClick={handleSignOut}
        disabled={signingOut}
        className="flex shrink-0 items-center gap-1.5 rounded-md border rule px-2.5 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink disabled:opacity-50"
      >
        <LogOut className="h-3.5 w-3.5" />
        {signingOut ? "..." : t.nav.logout}
      </button>
    </div>
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
