"use client";

import { motion } from "framer-motion";

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-6 px-4 text-center">
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="text-6xl"
      >
        ⚠️
      </motion.div>
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">কিছু একটা ঠিক নেই</h2>
        <p className="text-sm text-gray-500 max-w-md">
          দুঃখিত, একটি সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।
        </p>
        {error?.message && (
          <p className="text-xs text-red-500 mt-2 font-mono bg-red-50 p-2 rounded">{error.message}</p>
        )}
      </div>
      <button
        onClick={reset}
        className="bg-[#1a5632] text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-[#143d22] transition-colors"
      >
        আবার চেষ্টা করুন
      </button>
    </div>
  );
}
