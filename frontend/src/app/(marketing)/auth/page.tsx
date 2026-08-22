"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "motion/react";
import { Sprout, Phone, ArrowRight, Camera, MessageSquare, ShieldCheck, Loader2, Mail, Lock } from "lucide-react";
import { APP, HELPLINE } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";
import { createClient } from "@/lib/supabase/client";
import { cn } from "@/lib/utils";

/* Dev-only test personas (amendment 02 §6): rendered ONLY when
   NEXT_PUBLIC_DEV_USER_SWITCHER=true — never set in production. The
   credentials come from NEXT_PUBLIC_TEST_* env vars and belong to throwaway
   Supabase test accounts provisioned by tools/ops/supabase_test_user.ps1. */
const DEV_SWITCHER = process.env.NEXT_PUBLIC_DEV_USER_SWITCHER === "true";
const TEST_PERSONAS = [
  {
    key: "free",
    label: "ফ্রি ব্যবহারকারী",
    email: process.env.NEXT_PUBLIC_TEST_FREE_USER_EMAIL,
    password: process.env.NEXT_PUBLIC_TEST_FREE_USER_PASSWORD,
  },
  {
    key: "premium",
    label: "প্রিমিয়াম ব্যবহারকারী",
    email: process.env.NEXT_PUBLIC_TEST_PREMIUM_USER_EMAIL,
    password: process.env.NEXT_PUBLIC_TEST_PREMIUM_USER_PASSWORD,
  },
  {
    key: "admin",
    label: "অ্যাডমিন",
    email: process.env.NEXT_PUBLIC_TEST_ADMIN_USER_EMAIL,
    password: process.env.NEXT_PUBLIC_TEST_ADMIN_USER_PASSWORD,
  },
] as const;

/* =========================================================================
   /auth → Login / register (optional, additive).

   Auth is OPTIONAL: the anonymous single-session demo keeps working without
   any account (AGENTS.md §2 rule 1). This page offers email+password and
   (when enabled) Google OAuth for future premium features, and always keeps
   the direct demo entry points and the 16123 helpline visible.

   Google requires: provider enabled in the Supabase dashboard + a Google
   Cloud Console OAuth app (see amendment 15). The button renders only when
   NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED=true.
   ========================================================================= */

export default function AuthPage() {
  return (
    <Suspense fallback={null}>
      <AuthForm />
    </Suspense>
  );
}

function AuthForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialMode = searchParams.get("mode") === "register" ? "register" : "login";
  const urlError = searchParams.get("error");

  const [mode, setMode] = useState<"login" | "register">(initialMode);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(
    urlError === "auth_callback_failed" ? "লগইন সম্পূর্ণ হয়নি। আবার চেষ্টা করুন।" : null,
  );
  const [info, setInfo] = useState<string | null>(null);

  const googleEnabled = process.env.NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED === "true";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    setBusy(true);

    const supabase = createClient();

    if (mode === "login") {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      setBusy(false);
      if (error) {
        setError(
          error.message.includes("Invalid login credentials")
            ? "ইমেইল বা পাসওয়ার্ড সঠিক নয়।"
            : "লগইন ব্যর্থ হয়েছে। আবার চেষ্টা করুন।",
        );
        return;
      }
      router.push("/");
      router.refresh();
      return;
    }

    // register
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { emailRedirectTo: `${window.location.origin}/auth/callback` },
    });
    setBusy(false);
    if (error) {
      if (error.message.toLowerCase().includes("already registered")) {
        setError("এই ইমেইলে ইতিমধ্যে অ্যাকাউন্ট আছে — লগইন করুন।");
        setMode("login");
      } else {
        setError("নিবন্ধন ব্যর্থ হয়েছে। আবার চেষ্টা করুন।");
      }
      return;
    }
    setInfo("নিবন্ধন সফল! কনফার্মেশন ইমেইল পাঠানো হয়েছে — ইনবক্স দেখে নিশ্চিত করুন।");
  }

  async function handleGoogle() {
    setError(null);
    const supabase = createClient();
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });
    if (error) setError("Google লগইন শুরু হয়নি। আবার চেষ্টা করুন।");
  }

  async function handlePersona(email?: string, password?: string) {
    if (!email || !password) {
      setError("এই টেস্ট অ্যাকাউন্টের env ভেরিয়েবল সেট করা নেই (.env.local দেখুন)।");
      return;
    }
    setError(null);
    setInfo(null);
    setBusy(true);
    const supabase = createClient();
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    setBusy(false);
    if (error) {
      setError("টেস্ট লগইন ব্যর্থ — tools/ops/supabase_test_user.ps1 চালিয়ে অ্যাকাউন্ট তৈরি করুন।");
      return;
    }
    router.push("/");
    router.refresh();
  }

  return (
    <div className="flex min-h-[calc(100vh-8rem)] items-center justify-center py-10">
      <motion.div initial="hidden" animate="visible" variants={stagger} className="w-full max-w-lg">
        {/* Mark + heading */}
        <motion.div variants={enter} className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-leaf text-paper">
            <Sprout className="h-6 w-6" />
          </div>
          <h1 className="font-display text-2xl text-ink">
            {mode === "login" ? "লগইন" : "নিবন্ধন"}
          </h1>
          <p className="mt-1 text-sm text-ink-soft">
            অ্যাকাউন্ট ঐচ্ছিক — ডেমো চলবে লগইন ছাড়াই
          </p>
        </motion.div>

        <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 shadow-sm">
          {/* Mode toggle */}
          <div className="grid grid-cols-2 gap-1 rounded-lg bg-paper-2/60 p-1">
            {(["login", "register"] as const).map((m) => (
              <button
                key={m}
                onClick={() => {
                  setMode(m);
                  setError(null);
                  setInfo(null);
                }}
                className={cn(
                  "rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  mode === m ? "bg-leaf text-paper shadow-sm" : "text-ink-soft hover:text-ink",
                )}
              >
                {m === "login" ? "লগইন" : "নিবন্ধন"}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="mt-5 space-y-4">
            <div>
              <label htmlFor="auth-email" className="mb-1.5 block text-sm text-ink-soft">
                ইমেইল
              </label>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" />
                <input
                  id="auth-email"
                  type="email"
                  required
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full rounded-lg border rule bg-paper-2/40 py-2.5 pl-9 pr-3 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
                />
              </div>
            </div>
            <div>
              <label htmlFor="auth-password" className="mb-1.5 block text-sm text-ink-soft">
                পাসওয়ার্ড
              </label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" />
                <input
                  id="auth-password"
                  type="password"
                  required
                  minLength={8}
                  autoComplete={mode === "login" ? "current-password" : "new-password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="কমপক্ষে ৮ অক্ষর"
                  className="w-full rounded-lg border rule bg-paper-2/40 py-2.5 pl-9 pr-3 text-sm text-ink placeholder:text-ink-faint focus:border-leaf focus:outline-none"
                />
              </div>
            </div>

            {error && (
              <p role="alert" className="rounded-lg bg-clay/10 px-3 py-2 text-sm text-clay">
                {error}
              </p>
            )}
            {info && (
              <p role="status" className="rounded-lg bg-leaf/10 px-3 py-2 text-sm text-leaf">
                {info}
              </p>
            )}

            <button
              type="submit"
              disabled={busy}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-leaf px-4 py-2.5 text-sm font-semibold text-paper transition-colors hover:bg-leaf-2 disabled:opacity-60"
            >
              {busy && <Loader2 className="h-4 w-4 animate-spin" />}
              {mode === "login" ? "লগইন করুন" : "নিবন্ধন করুন"}
            </button>
          </form>

          {googleEnabled && (
            <>
              <div className="my-4 flex items-center gap-3 text-xs text-ink-faint">
                <span className="h-px flex-1 bg-rule" />
                অথবা
                <span className="h-px flex-1 bg-rule" />
              </div>
              <button
                onClick={handleGoogle}
                disabled={busy}
                className="flex w-full items-center justify-center gap-2 rounded-lg border rule bg-paper-2/40 px-4 py-2.5 text-sm font-medium text-ink transition-colors hover:border-leaf disabled:opacity-60"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden>
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1Z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23Z" />
                  <path fill="#FBBC05" d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84Z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15A11 11 0 0 0 2.18 7.06l3.66 2.84C6.71 7.3 9.14 5.38 12 5.38Z" />
                </svg>
                Google দিয়ে লগইন করুন
              </button>
            </>
          )}

          {/* Dev-only test persona switcher — never rendered in production */}
          {DEV_SWITCHER && (
            <div className="mt-5 rounded-lg border border-ochre/40 bg-ochre/5 p-4">
              <div className="text-xs font-semibold text-ochre">
                ডেভ টেস্ট অ্যাকাউন্ট (শুধু ডেভেলপমেন্ট)
              </div>
              <div className="mt-2 grid grid-cols-3 gap-2">
                {TEST_PERSONAS.map((p) => (
                  <button
                    key={p.key}
                    type="button"
                    onClick={() => handlePersona(p.email, p.password)}
                    disabled={busy}
                    className="rounded-lg border border-ochre/30 bg-paper px-2 py-2 text-xs font-medium text-ink-soft transition-colors hover:border-ochre hover:text-ink disabled:opacity-60"
                  >
                    {p.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Demo entry — anonymous first */}
          <div className="mt-5 rounded-lg border border-leaf/20 bg-paper-2/40 p-4">
            <div className="flex items-start gap-2 text-sm text-leaf">
              <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0" />
              <span>
                অ্যাকাউন্ট ছাড়াই সরাসরি ডেমো ব্যবহার করুন
              </span>
            </div>
            <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
              <Link
                href="/detect"
                className="group flex items-center gap-2.5 rounded-xl border rule bg-paper px-3 py-3 transition-colors hover:border-leaf hover:bg-leaf/5"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
                  <Camera className="h-4.5 w-4.5" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-ink">রোগ নির্ণয়</div>
                  <div className="text-xs text-ink-faint">পাতার ছবি দিন</div>
                </div>
                <ArrowRight className="h-4 w-4 text-ink-faint transition-transform group-hover:translate-x-0.5 group-hover:text-leaf" />
              </Link>
              <Link
                href="/chat"
                className="group flex items-center gap-2.5 rounded-xl border rule bg-paper px-3 py-3 transition-colors hover:border-leaf hover:bg-leaf/5"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
                  <MessageSquare className="h-4.5 w-4.5" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-ink">কৃষি পরামর্শ</div>
                  <div className="text-xs text-ink-faint">বাংলায় প্রশ্ন করুন</div>
                </div>
                <ArrowRight className="h-4 w-4 text-ink-faint transition-transform group-hover:translate-x-0.5 group-hover:text-leaf" />
              </Link>
            </div>
          </div>

          {/* Helpline */}
          <div className="mt-5 flex items-center justify-between rounded-lg border border-leaf/20 bg-paper-2/40 px-4 py-3">
            <div className="flex items-center gap-2 text-sm text-ink-soft">
              <Phone className="h-4 w-4 text-leaf" />
              সাহায্য দরকার? কৃষি কল সেন্টার
            </div>
            <a
              href={`tel:${HELPLINE.krishiCallCenter}`}
              className="rounded-full bg-leaf px-4 py-1.5 text-sm font-semibold text-paper transition-colors hover:bg-leaf-2"
            >
              <span className="tabular">{HELPLINE.krishiCallCenter}</span>
            </a>
          </div>
        </motion.div>

        <motion.p variants={enter} className="mt-6 text-center text-xs text-ink-faint">
          © ২০২৬ {APP.nameEn} · গবেষণা প্রোটোটাইপ · North South University
        </motion.p>
      </motion.div>
    </div>
  );
}