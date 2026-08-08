"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DetectPanel } from "@/components/detect-panel";
import { QAPanel } from "@/components/qa-panel";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-green-700 text-white py-4 px-6 shadow">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="text-2xl">🌾</div>
          <div>
            <h1 className="text-xl font-bold">কৃষক চ্যাট</h1>
            <p className="text-xs text-green-200">KrishokChat — বাংলাদেশ কৃষি-এআই পরামর্ষদাতা</p>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-6">
        <Tabs defaultValue="detect" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="detect">রোগ নির্ণয়</TabsTrigger>
            <TabsTrigger value="qa">প্রশ্ন করুন</TabsTrigger>
          </TabsList>
          <TabsContent value="detect">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-bold text-gray-800 mb-4">ফসলের রোগ নির্ণয়</h2>
              <p className="text-sm text-gray-500 mb-4">পাতার ছবি আপলোড করুন — ফসল শনাক্ত করে নির্দিষ্ট রোগ মডেল দিয়ে বিশ্লেষণ করা হবে।</p>
              <DetectPanel />
            </div>
          </TabsContent>
          <TabsContent value="qa">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-bold text-gray-800 mb-4">কৃষি পরামর্শ</h2>
              <p className="text-sm text-gray-500 mb-4">বাংলায় যেকোনো কৃষি প্রশ্ন করুন — নিরাপত্তা যাচাই, তথ্য সংগ্রহ, উত্তর তৈরি, এবং যাচাইকরণের ধাপগুলো দেখুন।</p>
              <QAPanel />
            </div>
          </TabsContent>
        </Tabs>
      </main>

      <footer className="text-center text-xs text-gray-400 py-6">
        KrishokChat Advisory System v0.1 — Safety-aware Bengali Agri-AI
      </footer>
    </div>
  );
}
