"use client";

import { useEffect } from "react";

export function PwaRegister() {
  useEffect(() => {
    if (
      typeof window !== "undefined" &&
      "serviceWorker" in navigator &&
      process.env.NODE_ENV === "production"
    ) {
      let refreshing = false;
      navigator.serviceWorker.addEventListener("controllerchange", () => {
        if (!refreshing) {
          refreshing = true;
          window.location.reload();
        }
      });

      navigator.serviceWorker
        .register("/sw.js")
        .then((reg) => {
          // Check for updates on load
          reg.update();

          reg.onupdatefound = () => {
            const installing = reg.installing;
            if (installing) {
              installing.onstatechange = () => {
                if (
                  installing.state === "installed" &&
                  navigator.serviceWorker.controller
                ) {
                  // Activate new service worker immediately
                  installing.postMessage({ type: "SKIP_WAITING" });
                }
              };
            }
          };
        })
        .catch(() => {
          // Registration failed or ignored
        });

      // Global fallback for uncaught chunk errors (stale version skew)
      const handleGlobalChunkError = (event: ErrorEvent | PromiseRejectionEvent) => {
        const message =
          event instanceof ErrorEvent
            ? event.message || event.error?.message || ""
            : event.reason?.message || String(event.reason || "");

        if (
          typeof message === "string" &&
          (message.includes("Failed to load chunk") ||
            message.includes("Loading chunk") ||
            message.includes("failed to fetch dynamically imported module"))
        ) {
          const reloadKey = "krishok_chunk_auto_recover";
          const last = sessionStorage.getItem(reloadKey);
          const now = Date.now();
          if (!last || now - parseInt(last, 10) > 10000) {
            sessionStorage.setItem(reloadKey, now.toString());
            if ("caches" in window) {
              caches.keys().then((names) => {
                for (const name of names) caches.delete(name);
              });
            }
            window.location.reload();
          }
        }
      };

      window.addEventListener("error", handleGlobalChunkError);
      window.addEventListener("unhandledrejection", handleGlobalChunkError);

      return () => {
        window.removeEventListener("error", handleGlobalChunkError);
        window.removeEventListener("unhandledrejection", handleGlobalChunkError);
      };
    }
  }, []);

  return null;
}
