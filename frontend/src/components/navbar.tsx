"use client";
import { motion } from "motion/react";
import { motionTokens } from "@/lib/motionTokens";

export function Navbar() {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth }}
      className="sticky top-0 z-50 bg-gradient-to-r from-[#1a5632] to-[#2d7d46] text-white shadow-lg backdrop-blur-md"
    >
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <motion.div
          className="flex items-center gap-3"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: motionTokens.duration.fast }}
        >
          <span className="text-2xl">🌾</span>
          <div>
            <h1 className="text-lg font-bold leading-tight">কৃষক চ্যাট</h1>
            <p className="text-[10px] text-green-200 leading-tight">KrishokChat — বাংলাদেশ কৃষি-এআই</p>
          </div>
        </motion.div>
        <div className="flex items-center gap-2 text-xs text-green-100">
          <span className="hidden sm:inline px-2 py-0.5 bg-white/10 rounded-full">Safety-aware</span>
          <span className="hidden sm:inline px-2 py-0.5 bg-white/10 rounded-full">RAG-powered</span>
          <span className="px-2 py-0.5 bg-white/10 rounded-full">🇧🇩 বাংলা</span>
        </div>
      </div>
    </motion.header>
  );
}
