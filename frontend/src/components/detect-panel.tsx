"use client";
import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { detectDisease, DetectResponse } from "@/lib/api";
import { motionTokens } from "@/lib/motionTokens";

export function DetectPanel({ onDetected }: { onDetected?: (crop: string, disease: string) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<DetectResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function onSelect(f: File) {
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError(null);
  }

  async function runDetect() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const r = await detectDisease(file);
      setResult(r);
      if (onDetected && r.disease && !r.disease.toLowerCase().includes("healthy")) {
        onDetected(r.crop, r.disease);
      }
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  }

  return (
    <div className="space-y-5">
      <motion.div
        whileHover={{ scale: 1.005 }}
        transition={{ duration: motionTokens.duration.fast }}
        className="border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center cursor-pointer bg-gray-50/50 hover:bg-green-50/30 transition-colors"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); if (e.dataTransfer.files[0]) onSelect(e.dataTransfer.files[0]); }}
      >
        <input ref={inputRef} type="file" accept="image/*" className="hidden"
               onChange={(e) => e.target.files?.[0] && onSelect(e.target.files[0])} />
        <AnimatePresence mode="wait">
          {preview ? (
            <motion.div key="preview" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}>
              <img src={preview} alt="preview" className="max-h-52 mx-auto rounded-xl shadow-md" />
              <p className="text-xs text-gray-400 mt-2">ছবি পরিবর্তন করতে ক্লিক করুন</p>
            </motion.div>
          ) : (
            <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="text-4xl mb-3">📷</div>
              <div className="text-sm font-semibold text-gray-700">পাতার ছবি আপলোড করুন</div>
              <div className="text-xs text-gray-400 mt-1">ড্র্যাগ অ্যান্ড ড্রপ অথবে ক্লিক করুন</div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      <AnimatePresence>
        {file && (
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 8 }}>
            <motion.button
              onClick={runDetect}
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.97 }}
              transition={{ duration: motionTokens.duration.fast }}
              className="w-full bg-gradient-to-r from-[#1a5632] to-[#2d7d46] text-white py-3 rounded-xl font-semibold hover:shadow-lg disabled:opacity-50 transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <motion.span animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}>⟳</motion.span>
                  বিশ্লেষণ হচ্ছে...
                </span>
              ) : (
                "🔬 রোগ নির্ণয় করুন"
              )}
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {error && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl p-3">
            {error}
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence mode="wait">
        {result && (
          <motion.div
            key={result.disease}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            transition={{ duration: motionTokens.duration.normal }}
            className="bg-white border border-gray-100 rounded-2xl p-5 shadow-md space-y-4"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center text-2xl">🌱</div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 bg-green-100 text-green-800 text-xs font-bold rounded-full">{result.crop}</span>
                  <span className="text-xs text-gray-400">{(result.crop_confidence * 100).toFixed(0)}% নিশ্চিত</span>
                </div>
                <div className="text-lg font-bold text-gray-900 mt-1">{result.disease.replace(/__/g, " — ").replace(/_/g, " ")}</div>
                <div className="text-xs text-gray-500">রোগ নিশ্চিতা: {(result.disease_confidence * 100).toFixed(1)}%</div>
              </div>
            </div>

            <AnimatePresence>
              {result.disease_info && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: motionTokens.duration.normal }}
                  className="space-y-3 pt-3 border-t border-gray-100"
                >
                  {result.disease_info.description_bn && (
                    <div>
                      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">বিবরণ</div>
                      <p className="text-sm text-gray-700 leading-relaxed">{result.disease_info.description_bn}</p>
                    </div>
                  )}
                  {result.disease_info.solution_bn && (
                    <div className="bg-amber-50 border border-amber-100 rounded-xl p-3">
                      <div className="text-xs font-semibold text-amber-700 uppercase tracking-wide mb-1">💊 প্রতিকার</div>
                      <p className="text-sm text-gray-800 leading-relaxed">{result.disease_info.solution_bn}</p>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
