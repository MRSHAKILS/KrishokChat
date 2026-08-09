"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import {
  LogIn,
  UserPlus,
  Mail,
  Lock,
  User,
  Phone,
  MapPin,
  Eye,
  EyeOff,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Sprout,
} from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { enter, stagger, dur, ease } from "@/lib/motion";

/* =========================================================================
   Auth Page — industry-grade login/register skeleton.
   Toggle between login and register modes.
   Currently a UI skeleton — no backend auth wired (demo prototype).
   Form validates client-side, shows success/error states.
   ========================================================================= */

type Mode = "login" | "register";

export default function AuthPage() {
  const searchParams = useSearchParams();
  const initialMode: Mode = searchParams.get("mode") === "register" ? "register" : "login";
  const [mode, setMode] = useState<Mode>(initialMode);

  return (
    <div className="flex min-h-[calc(100vh-8rem)] items-center justify-center py-10">
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="w-full max-w-md"
      >
        {/* Logo + title */}
        <motion.div variants={enter} className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-leaf text-paper">
            <Sprout className="h-6 w-6" />
          </div>
          <h1 className="font-display text-2xl text-ink">
            {mode === "login" ? "প্রবেশ করুন" : "নিবন্ধন করুন"}
          </h1>
          <p className="mt-1 text-sm text-ink-soft">
            {mode === "login"
              ? "আপনার অ্যাকাউন্টে প্রবেশ করুন"
              : "নতুন অ্যাকাউন্ট তৈরি করুন"}
          </p>
        </motion.div>

        {/* Form card */}
        <motion.div variants={enter} className="rounded-2xl border rule bg-paper p-6 shadow-sm sm:p-8">
          <AnimatePresence mode="wait">
            {mode === "login" ? (
              <LoginForm key="login" onSwitch={() => setMode("register")} />
            ) : (
              <RegisterForm key="register" onSwitch={() => setMode("login")} />
            )}
          </AnimatePresence>
        </motion.div>

        {/* Helpline */}
        <motion.p variants={enter} className="mt-6 text-center text-xs text-ink-faint">
          সাহায্য দরকার? কৃষক কল সেন্টার:{" "}
          <a href={`tel:${HELPLINE.krishiCallCenter}`} className="font-medium text-leaf">
            {HELPLINE.krishiCallCenter}
          </a>
        </motion.p>
      </motion.div>
    </div>
  );
}

/* === Login Form === */
function LoginForm({ onSwitch }: { onSwitch: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ type: "success" | "error"; msg: string } | null>(null);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setResult({ type: "error", msg: "সব ফিল্ড পূরণ করুন।" });
      return;
    }
    setLoading(true);
    setResult(null);
    // Demo: simulate API call
    setTimeout(() => {
      setLoading(false);
      setResult({
        type: "success",
        msg: "প্রবেশ সফল (ডেমো) — প্রোটোটাইপে প্রকৃত প্রমাণীকরণ নেই।",
      });
    }, 1500);
  };

  return (
    <motion.form
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 10 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      onSubmit={submit}
      className="space-y-4"
    >
      {/* Email */}
      <Field label="ইমেইল বা ফোন" icon={Mail}>
        <input
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          className="w-full bg-transparent py-2.5 pl-10 pr-3 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
        />
      </Field>

      {/* Password */}
      <Field label="পাসওয়ার্ড" icon={Lock}>
        <input
          type={showPass ? "text" : "password"}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          className="w-full bg-transparent py-2.5 pl-10 pr-10 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
        />
        <button
          type="button"
          onClick={() => setShowPass((v) => !v)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink"
        >
          {showPass ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
        </button>
      </Field>

      {/* Forgot password */}
      <div className="flex items-center justify-between">
        <label className="flex items-center gap-2 text-xs text-ink-soft">
          <input type="checkbox" className="rounded border-bone" />
          মনে রাখুন
        </label>
        <button type="button" className="text-xs text-leaf hover:text-leaf-2">
          পাসওয়ার্ড ভুলেছেন?
        </button>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-leaf py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-50"
      >
        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <LogIn className="h-4 w-4" />}
        {loading ? "প্রবেশ হচ্ছে…" : "প্রবেশ"}
      </button>

      {/* Result */}
      {result && <ResultBanner type={result.type} msg={result.msg} />}

      {/* Switch to register */}
      <p className="pt-2 text-center text-sm text-ink-soft">
        অ্যাকাউন্ট নেই?{" "}
        <button type="button" onClick={onSwitch} className="font-medium text-leaf hover:text-leaf-2">
          নিবন্ধন করুন
        </button>
      </p>
    </motion.form>
  );
}

/* === Register Form === */
function RegisterForm({ onSwitch }: { onSwitch: () => void }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    district: "",
    password: "",
    confirm: "",
  });
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ type: "success" | "error"; msg: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const e: Record<string, string> = {};
    if (!form.name || form.name.length < 2) e.name = "নাম কমপক্ষে ২ অক্ষর";
    if (!form.email || !form.email.includes("@")) e.email = "বৈধ ইমেইল দিন";
    if (!form.phone || form.phone.length < 6) e.phone = "বৈধ ফোন নম্বর দিন";
    if (!form.district) e.district = "জেলা দিন";
    if (form.password.length < 6) e.password = "পাসওয়ার্ড কমপক্ষে ৬ অক্ষর";
    if (form.password !== form.confirm) e.confirm = "পাসওয়ার্ড মেলেনি";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    setResult(null);
    setTimeout(() => {
      setLoading(false);
      setResult({
        type: "success",
        msg: "নিবন্ধন সফল (ডেমো) — প্রোটোটাইপে প্রকৃত প্রমাণীকরণ নেই।",
      });
    }, 1800);
  };

  return (
    <motion.form
      initial={{ opacity: 0, x: 10 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -10 }}
      transition={{ duration: dur.normal, ease: ease.smooth }}
      onSubmit={submit}
      className="space-y-4"
    >
      {/* Name */}
      <Field label="পুরো নাম *" icon={User} error={errors.name}>
        <input
          type="text"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          placeholder="আপনার নাম"
          className="w-full bg-transparent py-2.5 pl-10 pr-3 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
        />
      </Field>

      {/* Email */}
      <Field label="ইমেইল *" icon={Mail} error={errors.email}>
        <input
          type="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          placeholder="you@example.com"
          className="w-full bg-transparent py-2.5 pl-10 pr-3 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
        />
      </Field>

      {/* Phone + District */}
      <div className="grid grid-cols-2 gap-3">
        <Field label="ফোন *" icon={Phone} error={errors.phone}>
          <input
            type="tel"
            value={form.phone}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
            placeholder="01XXXXXXXXX"
            className="w-full bg-transparent py-2.5 pl-10 pr-3 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
          />
        </Field>
        <Field label="জেলা *" icon={MapPin} error={errors.district}>
          <input
            type="text"
            value={form.district}
            onChange={(e) => setForm({ ...form, district: e.target.value })}
            placeholder="রাজশাহী"
            className="w-full bg-transparent py-2.5 pl-10 pr-3 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
          />
        </Field>
      </div>

      {/* Password */}
      <Field label="পাসওয়ার্ড *" icon={Lock} error={errors.password}>
        <input
          type={showPass ? "text" : "password"}
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          placeholder="••••••••"
          className="w-full bg-transparent py-2.5 pl-10 pr-10 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
        />
        <button
          type="button"
          onClick={() => setShowPass((v) => !v)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink"
        >
          {showPass ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
        </button>
      </Field>

      {/* Confirm password */}
      <Field label="পাসওয়ার্ড নিশ্চিত *" icon={Lock} error={errors.confirm}>
        <input
          type={showPass ? "text" : "password"}
          value={form.confirm}
          onChange={(e) => setForm({ ...form, confirm: e.target.value })}
          placeholder="••••••••"
          className="w-full bg-transparent py-2.5 pl-10 pr-3 text-sm text-ink placeholder:text-ink-faint focus:outline-none"
        />
      </Field>

      {/* Terms */}
      <label className="flex items-start gap-2 text-xs text-ink-soft">
        <input type="checkbox" className="mt-0.5 rounded border-bone" />
        <span>
          আমি <span className="text-leaf">শর্তাবলী</span> এবং{" "}
          <span className="text-leaf">গোপনীয়তা নীতি</span> মেনে নিচ্ছি।
        </span>
      </label>

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-leaf py-3 text-sm font-medium text-paper transition-colors hover:bg-leaf-2 disabled:opacity-50"
      >
        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <UserPlus className="h-4 w-4" />}
        {loading ? "নিবন্ধন হচ্ছে…" : "অ্যাকাউন্ট তৈরি করুন"}
      </button>

      {/* Result */}
      {result && <ResultBanner type={result.type} msg={result.msg} />}

      {/* Switch to login */}
      <p className="pt-2 text-center text-sm text-ink-soft">
        অ্যাকাউন্ট আছে?{" "}
        <button type="button" onClick={onSwitch} className="font-medium text-leaf hover:text-leaf-2">
          প্রবেশ করুন
        </button>
      </p>
    </motion.form>
  );
}

/* === Reusable Field wrapper === */
function Field({
  label,
  icon: Icon,
  error,
  children,
}: {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium text-ink-soft">{label}</label>
      <div className="relative rounded-lg border rule bg-paper-2/30 transition-colors focus-within:border-leaf">
        <Icon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-faint" />
        {children}
      </div>
      {error && (
        <p className="mt-1 flex items-center gap-1 text-[11px] text-clay">
          <AlertCircle className="h-3 w-3" />
          {error}
        </p>
      )}
    </div>
  );
}

/* === Result banner === */
function ResultBanner({ type, msg }: { type: "success" | "error"; msg: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      className={`flex items-start gap-2 overflow-hidden rounded-lg px-4 py-3 text-sm ${
        type === "success" ? "bg-leaf/10 text-leaf" : "bg-clay-soft/20 text-clay"
      }`}
    >
      {type === "success" ? (
        <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" />
      ) : (
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
      )}
      <span>{msg}</span>
    </motion.div>
  );
}
