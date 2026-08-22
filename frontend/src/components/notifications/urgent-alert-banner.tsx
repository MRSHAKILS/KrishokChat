"use client";

/* =========================================================================
   UrgentAlertBanner — top banner for urgent/warning disease alerts on farmer
   surfaces (/detect, /chat). Dismissable; dismissal respects read state
   (server for signed-in users, localStorage for anonymous). Renders nothing
   when there is no live alert — the demo path is unchanged.
   ========================================================================= */

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";
import { Siren, X, ArrowRight } from "lucide-react";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { useNotifications, markNotificationRead } from "@/lib/notifications";
import { cn } from "@/lib/utils";

export function UrgentAlertBanner() {
  const { session } = useSupabaseSession();
  const token = session?.access_token;
  const { urgentAlert } = useNotifications(token);
  // Local dismissal survives the session-token refresh cycle.
  const [dismissedId, setDismissedId] = useState<string | null>(null);

  if (!urgentAlert || urgentAlert.id === dismissedId) return null;

  const urgent = urgentAlert.severity === "urgent";

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
        role="alert"
        className={cn(
          "flex items-start gap-3 rounded-xl border-2 px-4 py-3",
          urgent ? "border-clay/50 bg-clay/10" : "border-ochre/50 bg-ochre/10",
        )}
      >
        <span
          className={cn(
            "mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
            urgent ? "bg-clay/15 text-clay" : "bg-ochre/15 text-ochre",
          )}
        >
          <Siren className="h-4 w-4" aria-hidden />
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-1.5">
            <span className={cn("text-xs font-bold", urgent ? "text-clay" : "text-ochre")}>
              {urgent ? "জরুরি রোগ সতর্কতা" : "রোগ সতর্কতা"}
            </span>
            {urgentAlert.crop && (
              <span className="rounded-full bg-leaf/10 px-1.5 py-0.5 text-xs font-medium text-leaf">
                {urgentAlert.crop}
              </span>
            )}
          </div>
          <p className="mt-0.5 text-sm font-semibold leading-snug text-ink">{urgentAlert.title_bn}</p>
          <p className="mt-1 text-sm leading-relaxed text-ink-soft">{urgentAlert.body_bn}</p>
          {urgentAlert.cta_url && urgentAlert.cta_url.startsWith("/") && (
            <Link
              href={urgentAlert.cta_url}
              onClick={() => {
                markNotificationRead(urgentAlert, token);
                setDismissedId(urgentAlert.id);
              }}
              className="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-leaf hover:underline"
            >
              ব্যবস্থা দেখুন <ArrowRight className="h-3 w-3" />
            </Link>
          )}
        </div>
        <button
          type="button"
          aria-label="সতর্কতা বন্ধ করুন"
          onClick={() => {
            markNotificationRead(urgentAlert, token);
            setDismissedId(urgentAlert.id);
          }}
          className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-ink-faint transition-colors hover:bg-paper"
        >
          <X className="h-4 w-4" />
        </button>
      </motion.div>
    </AnimatePresence>
  );
}
