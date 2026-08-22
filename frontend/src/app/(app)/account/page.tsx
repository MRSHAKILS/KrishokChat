"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "motion/react";
import { Bookmark, Trash2, Loader2, LogOut, Sprout, MessageSquare, ShieldCheck } from "lucide-react";
import { useSupabaseSession } from "@/lib/supabase/hooks";
import { createClient } from "@/lib/supabase/client";
import { getSavedHistory, deleteSavedQuery, type SavedQuery } from "@/lib/api";
import { enter, stagger } from "@/lib/motion";
import { APP } from "@/lib/constants";

/* =========================================================================
   /account — saved history (premium lane, P4 decision 1).

   Additive and optional: anonymous visitors see a login CTA, never a
   redirect. Signed-in visitors see their saved Q&A pairs with delete.
   Fetch failures (e.g., backend offline or migration not yet applied)
   degrade to a clear retry card — nothing blocks, nothing pops up.
   ========================================================================= */

export default function AccountPage() {
  const { user, session, loading } = useSupabaseSession();
  const [items, setItems] = useState<SavedQuery[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fetching, setFetching] = useState(true);
  const [deleting, setDeleting] = useState<string | null>(null);

  const token = session?.access_token;

  const load = useCallback(async () => {
    if (!token) return;
    setFetching(true);
    setError(null);
    try {
      const data = await getSavedHistory(token);
      setItems(data.items);
    } catch {
      setError("সংরক্ষিত ইতিহাস লোড হয়নি। ব্যাকএন্ড চালু আছে কিনা দেখুন।");
    } finally {
      setFetching(false);
    }
  }, [token]);

  useEffect(() => {
    if (token) void load();
    else setFetching(false);
  }, [token, load]);

  async function handleDelete(id: string) {
    if (!token) return;
    setDeleting(id);
    try {
      await deleteSavedQuery(token, id);
      setItems((prev) => (prev ? prev.filter((i) => i.id !== id) : prev));
    } catch {
      setError("মুছে ফেলা যায়নি। আবার চেষ্টা করুন।");
    } finally {
      setDeleting(null);
    }
  }

  async function handleSignOut() {
    const supabase = createClient();
    await supabase.auth.signOut();
    setItems(null);
  }

  return (
    <motion.div initial="hidden" animate="visible" variants={stagger} className="mx-auto max-w-3xl space-y-6">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="mb-2 text-xs font-semibold text-leaf">ব্যক্তিগত প্রোফাইল ও রেকর্ড</p>
          <h1 className="font-display text-2xl text-ink sm:text-3xl">সংরক্ষিত কৃষি পরামর্শ</h1>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-ink-soft">
            আপনার সংরক্ষিত প্রশ্নোত্তর ও ব্যবস্থাপত্র পরবর্তীতে পর্যালোচনার জন্য এখানে সুরক্ষিত থাকে।
          </p>
        </div>
      </header>

      {loading ? (
        <div className="flex h-40 items-center justify-center">
          <Loader2 className="h-5 w-5 animate-spin text-leaf" />
        </div>
      ) : !user ? (
        <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-8 text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-leaf/10 text-leaf">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <h2 className="font-display text-lg text-ink">লগইন করলে ইতিহাস সংরক্ষণ হবে</h2>
          <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-ink-soft">
            অ্যাকাউন্ট ঐচ্ছিক — লগইন ছাড়াই ডেমো ব্যবহার চালিয়ে যেতে পারেন।
          </p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/auth"
              className="rounded-full bg-leaf px-5 py-2.5 text-sm font-semibold text-paper transition-colors hover:bg-leaf-2"
            >
              লগইন / নিবন্ধন
            </Link>
            <Link
              href="/chat"
              className="rounded-full border rule bg-paper-2/40 px-5 py-2.5 text-sm font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink"
            >
              ডেমো চালিয়ে যান
            </Link>
          </div>
        </motion.div>
      ) : (
        <>
          {/* Profile card */}
          <motion.div
            variants={enter}
            className="flex items-center justify-between gap-3 rounded-2xl border rule bg-paper p-4"
          >
            <div className="flex min-w-0 items-center gap-3">
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-leaf text-sm font-bold text-paper">
                {(user.email ?? "অ").charAt(0).toUpperCase()}
              </span>
              <div className="min-w-0">
                <div className="truncate text-sm font-medium text-ink">{user.email}</div>
                <div className="text-xs text-ink-faint">সাইন-ইন করা আছে</div>
              </div>
            </div>
            <button
              onClick={handleSignOut}
              className="flex shrink-0 items-center gap-1.5 rounded-lg border rule px-3 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf hover:text-ink"
            >
              <LogOut className="h-3.5 w-3.5" />
              লগ আউট
            </button>
          </motion.div>

          {/* History list */}
          <motion.div variants={enter} className="space-y-3">
            {fetching ? (
              <div className="flex h-32 items-center justify-center">
                <Loader2 className="h-5 w-5 animate-spin text-leaf" />
              </div>
            ) : error ? (
              <div className="rounded-xl border rule bg-paper p-6 text-center">
                <p className="text-sm text-clay">{error}</p>
                <button
                  onClick={() => void load()}
                  className="mt-3 rounded-full border rule bg-paper-2/40 px-4 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-leaf"
                >
                  আবার চেষ্টা করুন
                </button>
              </div>
            ) : items && items.length === 0 ? (
              <div className="rounded-xl border rule bg-paper p-8 text-center">
                <Bookmark className="mx-auto mb-3 h-6 w-6 text-ink-faint" />
                <p className="text-sm text-ink-soft">কোনো সংরক্ষিত প্রশ্ন নেই।</p>
                <p className="mt-1 text-xs text-ink-faint">
                  চ্যাটে উত্তরের নিচে &quot;সংরক্ষণ করুন&quot; বাটনে চাপলে এখানে জমা হবে।
                </p>
              </div>
            ) : (
              items?.map((item) => (
                <div key={item.id} className="rounded-xl border rule bg-paper p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-ink">{item.query_text}</p>
                      <p className="mt-1 line-clamp-3 text-sm leading-relaxed text-ink-soft">
                        {item.answer_text}
                      </p>
                    </div>
                    <button
                      onClick={() => void handleDelete(item.id)}
                      disabled={deleting === item.id}
                      title="মুছে ফেলুন"
                      aria-label={`"${item.query_text}" মুছে ফেলুন`}
                      className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-ink-faint transition-colors hover:bg-clay/10 hover:text-clay disabled:opacity-50"
                    >
                      {deleting === item.id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Trash2 className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                  <div className="mt-3 flex flex-wrap items-center gap-2 text-xs text-ink-faint">
                    <span className="rounded-full bg-paper-2/60 px-2 py-0.5">
                      {new Date(item.created_at).toLocaleDateString("bn-BD")}
                    </span>
                    {item.category && (
                      <span className="rounded-full bg-leaf/10 px-2 py-0.5 text-leaf">{item.category}</span>
                    )}
                    <span>{item.sources.length} উৎস</span>
                  </div>
                </div>
              ))
            )}
          </motion.div>
        </>
      )}

      <p className="text-center text-xs text-ink-faint">
        © ২০২৬ {APP.nameEn} · গবেষণা প্রোটোটাইপ
      </p>
    </motion.div>
  );
}