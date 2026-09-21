"use client";

import { useEffect } from "react";
import { motion } from "motion/react";
import { AlertTriangle, RefreshCw } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const isChunkError =
    error?.name === "ChunkLoadError" ||
    Boolean(
      error?.message &&
        (error.message.includes("Failed to load chunk") ||
          error.message.includes("Loading chunk") ||
          error.message.includes("failed to fetch dynamically imported module"))
    );

  // Self-heal on chunk loading failures caused by new deployments
  useEffect(() => {
    if (isChunkError && typeof window !== "undefined") {
      const storageKey = `chunk_reload_${window.location.pathname}`;
      const lastReload = sessionStorage.getItem(storageKey);
      const now = Date.now();

      // Only auto-reload if we haven't reloaded within the last 12 seconds
      if (!lastReload || now - parseInt(lastReload, 10) > 12000) {
        sessionStorage.setItem(storageKey, now.toString());
        if ("caches" in window) {
          caches.keys().then((names) => {
            for (const name of names) caches.delete(name);
          });
        }
        window.location.reload();
      }
    }
  }, [isChunkError]);

  const handleRetry = async () => {
    if (isChunkError && typeof window !== "undefined") {
      if ("caches" in window) {
        try {
          const names = await caches.keys();
          await Promise.all(names.map((name) => caches.delete(name)));
        } catch {
          // ignore cache clearing errors
        }
      }
      window.location.reload();
    } else {
      reset();
    }
  };

  return (
    <div className="flex min-h-[55vh] flex-col items-center justify-center gap-6 px-5 text-center">
      <motion.div
        initial={{ scale: 0.85, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-clay-soft/40 text-clay"
      >
        <AlertTriangle className="h-7 w-7" strokeWidth={1.5} />
      </motion.div>

      <div className="space-y-2">
        <h2 className="font-display text-2xl text-ink">
          {isChunkError ? "নতুন সংস্করণ উপলব্ধ" : "কিছু একটা ঠিক নেই"}
        </h2>
        <p className="mx-auto max-w-md text-sm leading-relaxed text-ink-soft">
          {isChunkError
            ? "অ্যাপ্লিকেশনের একটি নতুন সংস্করণ আপডেট হয়েছে। পৃষ্ঠাটি রিফ্রেশ করা হচ্ছে..."
            : "দুঃখিত, একটি সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"}
        </p>
        {error?.message && !isChunkError && (
          <p className="mx-auto mt-1 max-w-md break-words rounded-md bg-clay-soft/30 px-3 py-2 font-mono text-xs text-clay">
            {error.message}
          </p>
        )}
      </div>

      <button
        onClick={handleRetry}
        className="inline-flex items-center gap-2 rounded-lg bg-leaf px-6 py-2.5 text-sm font-medium text-paper transition-colors hover:bg-leaf-2"
      >
        <RefreshCw className="h-4 w-4" />
        {isChunkError ? "রিফ্রেশ করুন" : "আবার চেষ্টা করুন"}
      </button>
    </div>
  );
}
