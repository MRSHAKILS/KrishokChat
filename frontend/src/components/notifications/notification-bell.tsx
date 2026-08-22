"use client";

/* =========================================================================
   NotificationBell — navbar entry for admin broadcasts (amendment 02).

   Renders NOTHING when the notification lane is disabled/unreachable, so the
   anonymous offline demo is visually unchanged. Panel lists announcements
   with severity styling in the Field Notebook palette; clicking an item marks
   it read (server for signed-in users, localStorage for anonymous).
   ========================================================================= */

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import { Bell, Siren, Wrench, Megaphone, X, ArrowRight } from "lucide-react";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import {
  useNotifications,
  markNotificationRead,
  type NotificationItem,
} from "@/lib/notifications";
import { cn } from "@/lib/utils";

const KIND_META = {
  announcement: { icon: Megaphone, label: "ঘোষণা" },
  disease_alert: { icon: Siren, label: "রোগ সতর্কতা" },
  maintenance: { icon: Wrench, label: "রক্ষণাবেক্ষণ" },
} as const;

function severityClass(severity: string): string {
  if (severity === "urgent") return "border-clay/40 bg-clay/10";
  if (severity === "warning") return "border-ochre/40 bg-ochre/10";
  return "border-leaf/25 bg-leaf/5";
}

function severityTextClass(severity: string): string {
  if (severity === "urgent") return "text-clay";
  if (severity === "warning") return "text-ochre";
  return "text-leaf";
}

export function NotificationBell() {
  const { session } = useSupabaseSession();
  const token = session?.access_token ?? null;
  const { items, unreadCount, enabled } = useNotifications(token);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  // Entirely absent when the lane is off — demo path unchanged.
  if (!enabled && items.length === 0) return null;

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label={unreadCount > 0 ? `${unreadCount}টি নতুন বিজ্ঞপ্তি` : "বিজ্ঞপ্তি"}
        aria-haspopup="menu"
        aria-expanded={open}
        className={cn(
          "control-press relative flex h-9 w-9 items-center justify-center rounded-full border rule bg-paper-2/40 text-ink-soft transition-colors hover:border-leaf hover:text-ink",
          open && "border-leaf text-ink",
        )}
      >
        <Bell className="h-4 w-4" />
        {unreadCount > 0 && (
          <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-clay px-1 text-[10px] font-bold leading-none text-paper">
            {unreadCount > 9 ? "৯+" : String(unreadCount).replace(/\d/g, (d) => "০১২৩৪৫৬৭৮৯"[Number(d)])}
          </span>
        )}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 6, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 6, scale: 0.98 }}
            transition={{ duration: 0.16, ease: [0.22, 1, 0.36, 1] }}
            role="menu"
            aria-label="বিজ্ঞপ্তি তালিকা"
            className="absolute right-0 top-full z-50 mt-2 w-80 overflow-hidden rounded-xl border rule bg-paper shadow-lg shadow-ink/10 sm:w-96"
          >
            <div className="flex items-center justify-between border-b rule px-4 py-3">
              <span className="text-sm font-semibold text-ink">বিজ্ঞপ্তি</span>
              <button
                type="button"
                onClick={() => setOpen(false)}
                aria-label="বন্ধ করুন"
                className="flex h-7 w-7 items-center justify-center rounded-md text-ink-faint hover:bg-paper-2"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="max-h-[60vh] overflow-y-auto scrollbar-thin">
              {items.length === 0 ? (
                <p className="px-4 py-6 text-center text-sm text-ink-faint">এখন কোনো বিজ্ঞপ্তি নেই।</p>
              ) : (
                items.map((item) => (
                  <NotificationRow key={item.id} item={item} token={token} onDone={() => setOpen(false)} />
                ))
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function NotificationRow({
  item,
  token,
  onDone,
}: {
  item: NotificationItem;
  token: string | null;
  onDone: () => void;
}) {
  const meta = KIND_META[item.kind] ?? KIND_META.announcement;
  const Icon = meta.icon;
  const inner = (
    <>
      <div className="flex shrink-0 items-start gap-2.5">
        <span
          className={cn(
            "mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border",
            severityClass(item.severity),
          )}
        >
          <Icon className={cn("h-4 w-4", severityTextClass(item.severity))} aria-hidden />
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-1.5">
            <span className={cn("text-xs font-semibold", severityTextClass(item.severity))}>{meta.label}</span>
            {item.crop && (
              <span className="rounded-full bg-leaf/10 px-1.5 py-0.5 text-xs font-medium text-leaf">{item.crop}</span>
            )}
            {!item.read && <span className="h-1.5 w-1.5 rounded-full bg-clay" aria-label="নতুন" />}
          </div>
          <p className="mt-0.5 text-sm font-semibold leading-snug text-ink">{item.title_bn}</p>
          <p className="mt-1 line-clamp-3 text-sm leading-relaxed text-ink-soft">{item.body_bn}</p>
          {item.cta_url && (
            <span className="mt-1.5 inline-flex items-center gap-1 text-xs font-medium text-leaf">
              আরও দেখুন <ArrowRight className="h-3 w-3" />
            </span>
          )}
        </div>
      </div>
    </>
  );

  const className = cn(
    "block w-full border-b rule px-4 py-3 text-left transition-colors last:border-b-0 hover:bg-paper-2/50",
    !item.read && "bg-leaf/[0.04]",
  );

  const handleClick = () => {
    markNotificationRead(item, token);
    onDone();
  };

  if (item.cta_url && item.cta_url.startsWith("/")) {
    return (
      <Link href={item.cta_url} onClick={handleClick} className={className}>
        {inner}
      </Link>
    );
  }
  return (
    <button type="button" onClick={handleClick} className={className}>
      {inner}
    </button>
  );
}
