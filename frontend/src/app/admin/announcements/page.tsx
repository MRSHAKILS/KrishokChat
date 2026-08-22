"use client";

/* =========================================================================
   /admin/announcements — Bengali composer with a LIVE preview of exactly
   what the farmer sees (bell row + banner). Draft → publish → expire flow;
   every mutation is audited server-side (amendment 02).
   ========================================================================= */

import { useCallback, useEffect, useMemo, useState } from "react";
import { Loader2, Send, Ban, Trash2, BadgeCheck, Siren, Megaphone, Wrench, Eye } from "lucide-react";
import {
  adminCreateAnnouncement,
  adminDeleteAnnouncement,
  adminListAnnouncements,
  adminSetAnnouncementPublished,
  type AdminAnnouncement,
} from "@/lib/admin-api";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { cn } from "@/lib/utils";

const KINDS = [
  { value: "announcement", label: "ঘোষণা", icon: Megaphone },
  { value: "disease_alert", label: "রোগ সতর্কতা", icon: Siren },
  { value: "maintenance", label: "রক্ষণাবেক্ষণ", icon: Wrench },
] as const;

const SEVERITIES = [
  { value: "info", label: "তথ্য" },
  { value: "warning", label: "সতর্ক" },
  { value: "urgent", label: "জরুরি" },
] as const;

const AUDIENCES = [
  { value: "all", label: "সবাই (লগইন ছাড়াও)" },
  { value: "free", label: "ফ্রি ব্যবহারকারী" },
  { value: "premium", label: "প্রিমিয়াম" },
] as const;

interface Draft {
  kind: "announcement" | "disease_alert" | "maintenance";
  severity: "info" | "warning" | "urgent";
  title_bn: string;
  body_bn: string;
  crop: string;
  audience: "all" | "free" | "premium";
  cta_url: string;
}

const EMPTY_DRAFT: Draft = {
  kind: "disease_alert",
  severity: "urgent",
  title_bn: "",
  body_bn: "",
  crop: "",
  audience: "all",
  cta_url: "",
};

export default function AdminAnnouncementsPage() {
  const { session } = useSupabaseSession();
  const token = session?.access_token;

  const [draft, setDraft] = useState<Draft>(EMPTY_DRAFT);
  const [items, setItems] = useState<AdminAnnouncement[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!token) return;
    try {
      const res = await adminListAnnouncements(token, 50);
      setItems(res.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "লোড করা যায়নি");
    }
  }, [token]);

  useEffect(() => {
    void load();
  }, [load]);

  const preview: AdminAnnouncement = useMemo(
    () => ({
      id: "preview",
      kind: draft.kind,
      severity: draft.severity,
      title_bn: draft.title_bn || "শিরোনাম এখানে দেখাবে…",
      body_bn: draft.body_bn || "বিস্তারিত লেখা এখানে দেখাবে…",
      crop: draft.crop,
      audience: draft.audience,
      cta_url: draft.cta_url,
      published: true,
      published_at: null,
      expires_at: null,
      created_at: "",
    }),
    [draft],
  );

  async function handleCreate(publish: boolean) {
    if (!token) return;
    if (!draft.title_bn.trim() || !draft.body_bn.trim()) {
      setError("শিরোনাম ও বিস্তারিত দুটোই দিতে হবে।");
      return;
    }
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      const created = await adminCreateAnnouncement(token, draft);
      if (publish) {
        await adminSetAnnouncementPublished(token, created.id, true);
      }
      setDraft(EMPTY_DRAFT);
      setNotice(publish ? "বিজ্ঞপ্তি প্রকাশিত হয়েছে — কৃষকরা এখন দেখবেন।" : "খসড়া সংরক্ষিত হয়েছে।");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "সংরক্ষণ করা যায়নি");
    } finally {
      setBusy(false);
    }
  }

  async function togglePublish(item: AdminAnnouncement) {
    if (!token) return;
    setBusy(true);
    try {
      await adminSetAnnouncementPublished(token, item.id, !item.published);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "পরিবর্তন করা যায়নি");
    } finally {
      setBusy(false);
    }
  }

  async function remove(item: AdminAnnouncement) {
    if (!token) return;
    setBusy(true);
    try {
      await adminDeleteAnnouncement(token, item.id);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "মুছে ফেলা যায়নি");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-2xl text-ink">ঘোষণা ও সতর্কতা</h1>
        <p className="mt-1 text-sm text-ink-soft">
          কৃষকদের কাছে পৌঁছানোর আগে ডান পাশে ঠিক যেমন দেখাবে তা যাচাই করুন।
        </p>
      </header>

      {error && (
        <div role="alert" className="rounded-lg bg-clay/10 px-4 py-3 text-sm text-clay">
          {error}
        </div>
      )}
      {notice && (
        <div role="status" className="rounded-lg bg-leaf/10 px-4 py-3 text-sm text-leaf">
          {notice}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_400px]">
        {/* Composer */}
        <section className="space-y-4 rounded-xl border rule bg-paper p-5">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <Field label="ধরন">
              <select
                value={draft.kind}
                onChange={(e) => setDraft({ ...draft, kind: e.target.value as Draft["kind"] })}
                className={inputClass}
              >
                {KINDS.map((k) => (
                  <option key={k.value} value={k.value}>
                    {k.label}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="গুরুত্ব">
              <select
                value={draft.severity}
                onChange={(e) => setDraft({ ...draft, severity: e.target.value as Draft["severity"] })}
                className={inputClass}
              >
                {SEVERITIES.map((s) => (
                  <option key={s.value} value={s.value}>
                    {s.label}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="দর্শক">
              <select
                value={draft.audience}
                onChange={(e) => setDraft({ ...draft, audience: e.target.value as Draft["audience"] })}
                className={inputClass}
              >
                {AUDIENCES.map((a) => (
                  <option key={a.value} value={a.value}>
                    {a.label}
                  </option>
                ))}
              </select>
            </Field>
          </div>

          <Field label="ফসল (ঐচ্ছিক — যেমন: ধান)">
            <input
              type="text"
              value={draft.crop}
              onChange={(e) => setDraft({ ...draft, crop: e.target.value })}
              placeholder="ধান"
              className={inputClass}
            />
          </Field>

          <Field label="শিরোনাম (বাংলা)">
            <input
              type="text"
              value={draft.title_bn}
              onChange={(e) => setDraft({ ...draft, title_bn: e.target.value })}
              placeholder="যেমন: ধানে ব্লাস্ট রোগের সতর্কতা"
              className={inputClass}
            />
          </Field>

          <Field label="বিস্তারিত (বাংলা)">
            <textarea
              value={draft.body_bn}
              onChange={(e) => setDraft({ ...draft, body_bn: e.target.value })}
              rows={4}
              placeholder="যেমন: আবহাওয়া অফিসের পরামর্শ অনুযায়ী সপ্তাহে দুইবার ছত্রাকনাশক স্প্রে করুন…"
              className={cn(inputClass, "resize-y")}
            />
          </Field>

          <Field label="লিংক (ঐচ্ছিক — যেমন: /detect)">
            <input
              type="text"
              value={draft.cta_url}
              onChange={(e) => setDraft({ ...draft, cta_url: e.target.value })}
              placeholder="/detect"
              className={inputClass}
            />
          </Field>

          <div className="flex flex-wrap gap-2 pt-1">
            <button
              type="button"
              disabled={busy}
              onClick={() => void handleCreate(false)}
              className="flex items-center gap-2 rounded-lg border rule bg-paper-2/40 px-4 py-2.5 text-sm font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink disabled:opacity-60"
            >
              খসড়া সংরক্ষণ
            </button>
            <button
              type="button"
              disabled={busy}
              onClick={() => void handleCreate(true)}
              className="flex items-center gap-2 rounded-lg bg-leaf px-4 py-2.5 text-sm font-semibold text-paper transition-colors hover:bg-leaf-2 disabled:opacity-60"
            >
              {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              প্রকাশ করুন
            </button>
          </div>
        </section>

        {/* Live preview — exactly what the farmer sees */}
        <section className="space-y-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink">
            <Eye className="h-4 w-4 text-leaf" aria-hidden />
            কৃষক যা দেখবেন
          </div>
          <PreviewBellRow item={preview} />
          {(preview.kind === "disease_alert" || preview.severity !== "info") && <PreviewBanner item={preview} />}
          <p className="text-xs leading-relaxed text-ink-faint">
            জরুরি/সতর্ক মানের রোগ-সতর্কতা রোগ নির্ণয় ও পরামর্শ পাতার উপরে ব্যানার হিসেবেও দেখাবে; বাকি সব
            ঘোষণা উপরের ঘণ্টা আইকনে থাকবে।
          </p>
        </section>
      </div>

      {/* Existing announcements */}
      <section className="rounded-xl border rule bg-paper p-5">
        <h2 className="font-display text-lg text-ink">সব বিজ্ঞপ্তি</h2>
        {items === null ? (
          <div className="flex h-20 items-center justify-center">
            <Loader2 className="h-5 w-5 animate-spin text-leaf" />
          </div>
        ) : items.length === 0 ? (
          <p className="mt-3 text-sm text-ink-faint">এখনো কোনো বিজ্ঞপ্তি তৈরি হয়নি।</p>
        ) : (
          <ul className="mt-3 space-y-2">
            {items.map((item) => (
              <li
                key={item.id}
                className={cn(
                  "flex flex-col justify-between gap-2 rounded-lg border rule px-4 py-3 sm:flex-row sm:items-center",
                  item.published ? "bg-leaf/[0.03]" : "bg-paper-2/30",
                )}
              >
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-sm font-semibold text-ink">{item.title_bn}</span>
                    {item.published ? (
                      <span className="inline-flex items-center gap-1 rounded-full bg-leaf/10 px-2 py-0.5 text-xs font-medium text-leaf">
                        <BadgeCheck className="h-3 w-3" /> প্রকাশিত
                      </span>
                    ) : (
                      <span className="rounded-full bg-paper-2 px-2 py-0.5 text-xs text-ink-faint">খসড়া</span>
                    )}
                  </div>
                  <div className="mt-0.5 text-xs text-ink-faint">
                    {KINDS.find((k) => k.value === item.kind)?.label} ·{" "}
                    {SEVERITIES.find((s) => s.value === item.severity)?.label} ·{" "}
                    {AUDIENCES.find((a) => a.value === item.audience)?.label}
                    {item.crop ? ` · ${item.crop}` : ""}
                    {item.published_at
                      ? ` · ${new Date(item.published_at).toLocaleDateString("bn-BD")}`
                      : ""}
                  </div>
                </div>
                <div className="flex shrink-0 gap-2">
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void togglePublish(item)}
                    className="flex items-center gap-1.5 rounded-lg border rule px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink disabled:opacity-50"
                  >
                    {item.published ? <Ban className="h-3.5 w-3.5" /> : <Send className="h-3.5 w-3.5" />}
                    {item.published ? "সরান" : "প্রকাশ"}
                  </button>
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void remove(item)}
                    className="flex items-center gap-1.5 rounded-lg border rule px-3 py-1.5 text-xs font-medium text-ink-faint transition-colors hover:border-clay hover:text-clay disabled:opacity-50"
                    aria-label={`"${item.title_bn}" মুছে ফেলুন`}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                    মুছুন
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

const inputClass =
  "w-full rounded-lg border rule bg-paper-2/40 px-3 py-2 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none";

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm text-ink-soft">{label}</span>
      {children}
    </label>
  );
}

function severityClasses(severity: string) {
  if (severity === "urgent") return { box: "border-clay/40 bg-clay/10", text: "text-clay", banner: "border-clay/50 bg-clay/10" };
  if (severity === "warning") return { box: "border-ochre/40 bg-ochre/10", text: "text-ochre", banner: "border-ochre/50 bg-ochre/10" };
  return { box: "border-leaf/25 bg-leaf/5", text: "text-leaf", banner: "border-leaf/25 bg-leaf/5" };
}

function PreviewBellRow({ item }: { item: AdminAnnouncement }) {
  const meta = KINDS.find((k) => k.value === item.kind) ?? KINDS[0];
  const Icon = meta.icon;
  const tone = severityClasses(item.severity);
  return (
    <div className="rounded-xl border rule bg-paper p-4 shadow-sm">
      <div className="mb-2 text-xs text-ink-faint">ঘণ্টা আইকনে (নোটিফিকেশন প্যানেল)</div>
      <div className="flex items-start gap-2.5">
        <span className={cn("mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border", tone.box)}>
          <Icon className={cn("h-4 w-4", tone.text)} aria-hidden />
        </span>
        <div className="min-w-0">
          <span className={cn("text-xs font-semibold", tone.text)}>{meta.label}</span>
          <p className="mt-0.5 text-sm font-semibold text-ink">{item.title_bn}</p>
          <p className="mt-0.5 line-clamp-2 text-sm text-ink-soft">{item.body_bn}</p>
        </div>
      </div>
    </div>
  );
}

function PreviewBanner({ item }: { item: AdminAnnouncement }) {
  const tone = severityClasses(item.severity);
  const urgent = item.severity === "urgent";
  return (
    <div className="rounded-xl border rule bg-paper p-4 shadow-sm">
      <div className="mb-2 text-xs text-ink-faint">রোগ নির্ণয় পাতার উপরে (ব্যানার)</div>
      <div className={cn("flex items-start gap-3 rounded-xl border-2 px-4 py-3", tone.banner)}>
        <span className={cn("mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg", tone.box)}>
          <Siren className={cn("h-4 w-4", tone.text)} aria-hidden />
        </span>
        <div className="min-w-0">
          <span className={cn("text-xs font-bold", tone.text)}>
            {urgent ? "জরুরি রোগ সতর্কতা" : "রোগ সতর্কতা"}
          </span>
          <p className="mt-0.5 text-sm font-semibold text-ink">{item.title_bn}</p>
          <p className="mt-0.5 text-sm text-ink-soft">{item.body_bn}</p>
        </div>
      </div>
    </div>
  );
}
