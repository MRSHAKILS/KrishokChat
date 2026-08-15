"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { WifiOff, Wifi, CheckCircle2 } from "lucide-react";
import { useOnlineStatus } from "@/lib/offline-cache";

export function OfflineIndicator() {
  const isOnline = useOnlineStatus();
  const [showReconnected, setShowReconnected] = useState(false);
  const [hasBeenOffline, setHasBeenOffline] = useState(false);

  useEffect(() => {
    if (!isOnline) {
      setHasBeenOffline(true);
    } else if (hasBeenOffline) {
      setShowReconnected(true);
      const timer = window.setTimeout(() => {
        setShowReconnected(false);
        setHasBeenOffline(false);
      }, 3500);
      return () => window.clearTimeout(timer);
    }
  }, [isOnline, hasBeenOffline]);

  return (
    <AnimatePresence>
      {!isOnline && (
        <motion.div
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -40 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="fixed top-18 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 rounded-full border border-ochre/40 bg-paper/95 px-4 py-2 text-xs font-semibold text-ochre-dark shadow-lg backdrop-blur-md"
          role="status"
          aria-live="polite"
        >
          <WifiOff className="h-4 w-4 text-ochre animate-pulse" />
          <span>অফলাইন মোড — সংরক্ষিত তথ্য প্রদর্শিত হচ্ছে</span>
        </motion.div>
      )}

      {isOnline && showReconnected && (
        <motion.div
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -40 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="fixed top-18 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 rounded-full border border-leaf/40 bg-paper/95 px-4 py-2 text-xs font-semibold text-leaf shadow-lg backdrop-blur-md"
          role="status"
          aria-live="polite"
        >
          <CheckCircle2 className="h-4 w-4 text-leaf" />
          <span>অনলাইন সংযোগ পুনঃস্থাপিত হয়েছে</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
