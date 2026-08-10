"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Sprout, Phone, ArrowRight, ShieldCheck, MessageSquare, Camera } from "lucide-react";
import { APP, HELPLINE } from "@/lib/constants";
import { enter, stagger } from "@/lib/motion";

/* =========================================================================
   /auth → Demo Access page.

   The project directive is explicit: NO authentication, NO user accounts.
   This page used to host login/register forms that misled farmers and demo
   evaluators into thinking an account was required. It now explains, in
   plain Bengali, that KrishokChat is a single-session live demo — no
   login, no signup, just use it directly. Any ?mode=register query param
   is ignored on purpose.
   ========================================================================= */

export default function DemoAccessPage() {
  return (
    <div className="flex min-h-[calc(100vh-8rem)] items-center justify-center py-10">
      <motion.div
        initial="hidden"
        animate="visible"
        variants={stagger}
        className="w-full max-w-lg"
      >
        {/* Mark + heading */}
        <motion.div variants={enter} className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-leaf text-paper">
            <Sprout className="h-6 w-6" />
          </div>
          <h1 className="font-display text-2xl text-ink">সরাসরি ব্যবহার করুন</h1>
          <p className="mt-1 text-sm text-ink-soft">
            এটি একটি লাইভ ডেমো প্রোটোটাইপ — কোনো রেজিস্ট্রেশন বা লগইনের প্রয়োজন নেই।
          </p>
        </motion.div>

        {/* Single-session banner */}
        <motion.div
          variants={enter}
          className="rounded-2xl border rule bg-paper p-6 shadow-sm"
        >
          <div className="flex items-start gap-3 rounded-lg bg-leaf/10 px-4 py-3 text-leaf">
            <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0" />
            <div className="text-sm">
              <div className="font-medium">এক-সেশন ডেমো প্রোটোটাইপ</div>
              <p className="mt-0.5 text-leaf/80">
                {APP.name} একটি গবেষণা প্রোটোটাইপ। কোনো অ্যাকাউন্ট তৈরি ছাড়াই
                সরাসরি ফসলের রোগ নির্ণয় ও বাংলা পরামর্শ ব্যবহার করতে পারবেন।
              </p>
            </div>
          </div>

          {/* Direct entry actions */}
          <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <Link
              href="/detect"
              className="group flex items-center gap-3 rounded-xl border rule bg-paper-2/40 px-4 py-4 transition-colors hover:border-leaf hover:bg-leaf/5"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
                <Camera className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-ink">রোগ নির্ণয়</div>
                <div className="text-xs text-ink-faint">পাতার ছবি দিন</div>
              </div>
              <ArrowRight className="h-4 w-4 text-ink-faint transition-transform group-hover:translate-x-0.5 group-hover:text-leaf" />
            </Link>
            <Link
              href="/chat"
              className="group flex items-center gap-3 rounded-xl border rule bg-paper-2/40 px-4 py-4 transition-colors hover:border-leaf hover:bg-leaf/5"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-leaf/10 text-leaf">
                <MessageSquare className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-ink">কৃষি পরামর্শ</div>
                <div className="text-xs text-ink-faint">বাংলায় প্রশ্ন করুন</div>
              </div>
              <ArrowRight className="h-4 w-4 text-ink-faint transition-transform group-hover:translate-x-0.5 group-hover:text-leaf" />
            </Link>
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
