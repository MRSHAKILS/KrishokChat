"use client";

/* =========================================================================
   Offline Cache & Connectivity Utilities for KrishokTech PWA
   ========================================================================= */

import { useState, useEffect, useSyncExternalStore } from "react";

const CACHE_KEYS = {
  CATALOG: "krishokchat:cache:catalog:v1",
  DATASETS: "krishokchat:cache:datasets:v1",
  ADVISORY_HISTORY: "krishokchat:cache:advisories:v1",
} as const;

/**
 * Custom hook to subscribe to browser online/offline network status.
 */
export function useOnlineStatus(): boolean {
  return useSyncExternalStore(
    (callback) => {
      window.addEventListener("online", callback);
      window.addEventListener("offline", callback);
      return () => {
        window.removeEventListener("online", callback);
        window.removeEventListener("offline", callback);
      };
    },
    () => (typeof navigator !== "undefined" ? navigator.onLine : true),
    () => true
  );
}

/**
 * Save data into localStorage staged cache with safe error handling.
 */
export function saveToLocalCache<T>(key: string, data: T): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(key, JSON.stringify(data));
  } catch {
    // LocalStorage quota exceeded or private mode
  }
}

/**
 * Retrieve data from localStorage staged cache.
 */
export function getFromLocalCache<T>(key: string): T | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return null;
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

/**
 * Fetch JSON resource with offline cache fallback.
 */
export async function fetchWithOfflineFallback<T>(url: string, cacheKey: string): Promise<T | null> {
  try {
    const res = await fetch(url);
    if (res.ok) {
      const data = (await res.json()) as T;
      saveToLocalCache(cacheKey, data);
      return data;
    }
  } catch {
    // Network failed -> fallback to cached data
  }

  return getFromLocalCache<T>(cacheKey);
}

export { CACHE_KEYS };
