"use client";

/* =========================================================================
   Notifications client store (amendment 02) — shared by the navbar bell and
   the urgent disease-alert banners.

   Design constraints:
   - Anonymous-first: works with no session (audience "all" content only);
     anonymous read-state persists in localStorage.
   - Offline-tolerant: a failed fetch keeps the previous state and never
     throws; when Supabase/the backend is unconfigured the API answers an
     honest `{items: [], enabled: false}` and every surface renders nothing.
   - One poller: the first mounted consumer starts the interval refresh
     (NOTIFICATIONS_POLL_SECONDS, default 180s).
   ========================================================================= */

import { useEffect, useSyncExternalStore } from "react";
import { API_BASE } from "./api";

export type NotificationKind = "announcement" | "disease_alert" | "maintenance";
export type NotificationSeverity = "info" | "warning" | "urgent";

export interface NotificationItem {
  id: string;
  kind: NotificationKind;
  severity: NotificationSeverity;
  title_bn: string;
  body_bn: string;
  crop: string;
  audience: string;
  cta_url: string;
  published_at: string | null;
  read?: boolean;
}

export interface NotificationSnapshot {
  items: NotificationItem[];
  unreadCount: number;
  enabled: boolean;
  urgentAlert: NotificationItem | null;
}

const READ_KEY = "krishokchat:notification-read:v1";
const POLL_MS = Number(process.env.NEXT_PUBLIC_NOTIFICATIONS_POLL_SECONDS ?? 180) * 1000;

/* ---- anonymous read state (device-local) -------------------------------- */

export function getLocalReadIds(): string[] {
  try {
    const raw = localStorage.getItem(READ_KEY);
    return raw ? (JSON.parse(raw) as string[]) : [];
  } catch {
    return [];
  }
}

export function markLocalRead(id: string): void {
  try {
    const ids = new Set(getLocalReadIds());
    ids.add(id);
    // Keep the set bounded (last 200).
    const list = [...ids].slice(-200);
    localStorage.setItem(READ_KEY, JSON.stringify(list));
  } catch {
    /* storage unavailable — banner may reappear, harmless */
  }
}

/* ---- module store + pub/sub ---------------------------------------------- */

let items: NotificationItem[] = [];
let enabled = false;
let snapshot: NotificationSnapshot = { items: [], unreadCount: 0, enabled: false, urgentAlert: null };
const listeners = new Set<() => void>();
let pollTimer: ReturnType<typeof setInterval> | null = null;
let accessToken: string | null = null;

function rebuild(): void {
  const localRead = new Set(getLocalReadIds());
  const merged = items.map((item) => ({
    ...item,
    read: item.read || localRead.has(item.id),
  }));
  const unread = merged.filter((item) => !item.read);
  snapshot = {
    items: merged,
    unreadCount: unread.length,
    enabled,
    urgentAlert: unread.find(
      (item) => item.kind === "disease_alert" && (item.severity === "urgent" || item.severity === "warning"),
    ) ?? null,
  };
  for (const listener of listeners) listener();
}

function subscribe(onChange: () => void): () => void {
  listeners.add(onChange);
  return () => {
    listeners.delete(onChange);
  };
}

function getSnapshot(): NotificationSnapshot {
  return snapshot;
}

export async function refreshNotifications(token?: string | null): Promise<void> {
  try {
    const headers: HeadersInit = token ? { Authorization: `Bearer ${token}` } : {};
    const res = await fetch(`${API_BASE}/api/notifications?limit=20`, { headers });
    if (!res.ok) return;
    const body = (await res.json()) as { items: NotificationItem[]; enabled: boolean };
    items = body.items ?? [];
    enabled = Boolean(body.enabled);
    rebuild();
  } catch {
    /* offline / backend down — keep previous state */
  }
}

export function setNotificationSessionToken(token: string | null): void {
  accessToken = token;
  void refreshNotifications(token);
}

export function markNotificationRead(item: NotificationItem, token?: string | null): void {
  item.read = true;
  markLocalRead(item.id);
  rebuild();
  const bearer = token ?? accessToken;
  if (bearer) {
    void fetch(`${API_BASE}/api/notifications/${item.id}/read`, {
      method: "POST",
      headers: bearer ? { Authorization: `Bearer ${bearer}` } : {},
    }).catch(() => {
      /* server read-state sync is best-effort */
    });
  }
}

/* ---- consumer hook --------------------------------------------------------- */

export function useNotifications(token?: string | null): NotificationSnapshot {
  useEffect(() => {
    setNotificationSessionToken(token ?? null);
    if (!pollTimer) {
      pollTimer = setInterval(() => {
        void refreshNotifications(accessToken);
      }, POLL_MS);
    }
    return () => {
      /* the single poller intentionally outlives individual consumers */
    };
  }, [token]);
  return useSyncExternalStore(subscribe, getSnapshot, getSnapshot);
}
