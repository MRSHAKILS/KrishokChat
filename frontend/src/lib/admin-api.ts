"use client";

/* =========================================================================
   Admin API client (amendment 02) — thin typed fetchers for /api/admin/*.
   Every call carries the admin's access token; the backend re-verifies the
   caller's profiles.role='admin' on each request (these helpers assert
   nothing client-side). 401/403 responses surface as errors the UI shows
   honestly.
   ========================================================================= */

import { API_BASE } from "./api";

export interface AdminProfileRow {
  id: string;
  email: string;
  display_name?: string | null;
  role: "user" | "admin";
  plan: "free" | "premium";
  created_at?: string;
  updated_at?: string;
}

export interface AdminActionRow {
  id: string;
  actor_id: string;
  action: string;
  target_type: string;
  target_id: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface AdminAnnouncement {
  id: string;
  kind: "announcement" | "disease_alert" | "maintenance";
  severity: "info" | "warning" | "urgent";
  title_bn: string;
  body_bn: string;
  crop: string;
  audience: "all" | "free" | "premium";
  cta_url: string;
  published: boolean;
  published_at: string | null;
  expires_at: string | null;
  created_at: string;
}

async function adminFetch<T>(token: string, path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(init?.headers ?? {}),
    },
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail ?? `admin request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export function adminListUsers(
  token: string,
  page: number,
  pageSize: number,
  search = "",
): Promise<{ items: AdminProfileRow[]; total: number; page: number; page_size: number }> {
  const params = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
  if (search) params.set("q", search);
  return adminFetch(token, `/api/admin/users?${params.toString()}`);
}

export function adminPatchUser(
  token: string,
  userId: string,
  changes: { role?: "user" | "admin"; plan?: "free" | "premium" },
): Promise<AdminProfileRow> {
  return adminFetch(token, `/api/admin/users/${userId}`, {
    method: "PATCH",
    body: JSON.stringify(changes),
  });
}

export function adminListActions(token: string, limit = 20): Promise<{ items: AdminActionRow[] }> {
  return adminFetch(token, `/api/admin/actions?limit=${limit}`);
}

export function adminListAnnouncements(token: string, limit = 50): Promise<{ items: AdminAnnouncement[] }> {
  return adminFetch(token, `/api/admin/announcements?limit=${limit}`);
}

export function adminCreateAnnouncement(
  token: string,
  payload: Partial<AdminAnnouncement> & { title_bn: string; body_bn: string },
): Promise<AdminAnnouncement> {
  return adminFetch(token, "/api/admin/announcements", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function adminSetAnnouncementPublished(
  token: string,
  id: string,
  published: boolean,
): Promise<AdminAnnouncement> {
  return adminFetch(token, `/api/admin/announcements/${id}/${published ? "publish" : "unpublish"}`, {
    method: "POST",
  });
}

export function adminDeleteAnnouncement(token: string, id: string): Promise<void> {
  return adminFetch(token, `/api/admin/announcements/${id}`, { method: "DELETE" });
}
