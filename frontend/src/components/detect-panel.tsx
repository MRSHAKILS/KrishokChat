"use client";

import { useState, useRef } from "react";
import { classifyCrop, detectDisease, ClassifyResponse, DetectResponse } from "@/lib/api";

export function DetectPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<DetectResponse | null>(null);
  const [cropOnly, setCropOnly] = useState<ClassifyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [trace, setTrace] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  function onSelect(f: File) {
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setCropOnly(null);
    setError(null);
    setTrace([]);
  }

  async function runClassify() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setTrace((t) => [...t, "ফসল শ্রেণীবদ্ধ হচ্ছে..."]);
    try {
      const r = await classifyCrop(file);
      setCropOnly(r);
      setTrace((t) => [...t, `ফসল: ${r.crop} (${(r.confidence * 100).toFixed(0)}%)`]);
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  }

  async function runDetect() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setTrace(["ফসল শ্রেণীবদ্ধ হচ্ছে..."]);
    await new Promise((r) => setTimeout(r, 400));
    setTrace((t) => [...t, "রোগ নির্ণয় হচ্ছে..."]);
    try {
      const r = await detectDisease(file);
      setResult(r);
      setTrace((t) => [...t, `রোগ: ${r.disease} (${(r.disease_confidence * 100).toFixed(0)}%)`, "তথ্য যাচাই সম্পন্ন"]);
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  }

  return (
    <div className="space-y-4">
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-green-400 transition-colors"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); if (e.dataTransfer.files[0]) onSelect(e.dataTransfer.files[0]); }}
      >
        <input ref={inputRef} type="file" accept="image/*" className="hidden"
               onChange={(e) => e.target.files?.[0] && onSelect(e.target.files[0])} />
        {preview ? (
          <img src={preview} alt="preview" className="max-h-48 mx-auto rounded" />
        ) : (
          <div className="text-gray-500">
            <div className="text-3xl mb-2">📷</div>
            <div>ছবি আপলোড করুন অথবে ড্র্যাগ অ্যান্ড ড্রপ করুন</div>
          </div>
        )}
      </div>

      {file && (
        <div className="flex gap-2">
          <button onClick={runClassify} disabled={loading}
                  className="flex-1 bg-green-600 text-white py-2 rounded hover:bg-green-700 disabled:opacity-50">
            ফসল শনাক্ত করুন
          </button>
          <button onClick={runDetect} disabled={loading}
                  className="flex-1 bg-emerald-700 text-white py-2 rounded hover:bg-emerald-800 disabled:opacity-50">
            রোগ নির্ণয় করুন
          </button>
        </div>
      )}

      {loading && (
        <div className="text-sm text-gray-500 animate-pulse">
          {trace.map((t, i) => <div key={i}>{t}</div>)}
        </div>
      )}

      {error && <div className="text-red-600 text-sm bg-red-50 p-2 rounded">{error}</div>}

      {cropOnly && !result && (
        <div className="bg-green-50 border border-green-200 rounded p-4">
          <div className="font-bold text-green-800">{cropOnly.crop}</div>
          <div className="text-sm text-green-600">নিশ্চিতা: {(cropOnly.confidence * 100).toFixed(1)}%</div>
          {cropOnly.top3.slice(1).map((t) => (
            <div key={t.class} className="text-xs text-gray-500">{t.class}: {(t.confidence * 100).toFixed(1)}%</div>
          ))}
        </div>
      )}

      {result && (
        <div className="bg-white border rounded-lg p-5 space-y-3 shadow-sm">
          <div className="flex items-center gap-2">
            <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-bold rounded">{result.crop}</span>
            <span className="text-xs text-gray-500">{(result.crop_confidence * 100).toFixed(0)}% নিশ্চিত</span>
          </div>
          <div className="text-2xl font-bold text-red-700">{result.disease.replace(/_/g, " ")}</div>
          <div className="text-sm text-gray-600">রোগ নিশ্চিতা: {(result.disease_confidence * 100).toFixed(1)}%</div>
          {result.disease_info && (
            <div className="space-y-2 pt-2 border-t">
              {result.disease_info.description_bn && (
                <div><div className="text-xs font-semibold text-gray-500 uppercase">বিবরণ</div>
                  <div className="text-sm text-gray-700">{result.disease_info.description_bn}</div></div>
              )}
              {result.disease_info.solution_bn && (
                <div><div className="text-xs font-semibold text-gray-500 uppercase">প্রতিকার</div>
                  <div className="text-sm text-gray-800 bg-yellow-50 p-2 rounded">{result.disease_info.solution_bn}</div></div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
