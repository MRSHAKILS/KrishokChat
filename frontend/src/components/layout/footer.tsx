import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-white mt-auto">
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-sm">
          <div>
            <h3 className="font-bold text-gray-900 mb-2">কৃষক চ্যাট</h3>
            <p className="text-gray-500 text-xs">
              বাংলাদেশ কৃষি-এআই পরামর্শদাতা — নিরাপদ, ভিত্তিক, বাংলায়।
            </p>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 mb-2">দ্রুত লিংক</h3>
            <div className="flex flex-col gap-1">
              <Link href="/detect" className="text-gray-500 hover:text-green-700 transition-colors text-xs">রোগ নির্ণয়</Link>
              <Link href="/chat" className="text-gray-500 hover:text-green-700 transition-colors text-xs">প্রশ্ন করুন</Link>
              <Link href="/analytics" className="text-gray-500 hover:text-green-700 transition-colors text-xs">পরিসংখ্যান</Link>
              <Link href="/about" className="text-gray-500 hover:text-green-700 transition-colors text-xs">পরিচিতি</Link>
            </div>
          </div>
          <div>
            <h3 className="font-bold text-gray-900 mb-2">সাহায্য</h3>
            <p className="text-gray-500 text-xs">
              কৃষক কল সেন্টার: <a href="tel:16123" className="text-green-700 font-semibold">১৬১২৩</a>
            </p>
            <p className="text-gray-500 text-xs mt-1">
              জরুরি: <a href="tel:999" className="text-red-600 font-semibold">৯৯৯</a>
            </p>
          </div>
        </div>
        <div className="border-t border-gray-100 mt-4 pt-4 text-center text-xs text-gray-400">
          © ২০২৬ KrishokChat — বাংলাদেশ কৃষি-এআই পরামর্ষদাতা v0.1
        </div>
      </div>
    </footer>
  );
}
