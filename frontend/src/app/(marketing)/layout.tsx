import Link from "next/link";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="border-b border-gray-100 bg-white">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-xl">🌾</span>
            <span className="font-bold text-gray-900">কৃষক চ্যাট</span>
          </Link>
          <nav className="flex gap-4 text-sm">
            <Link href="/about" className="text-gray-600 hover:text-green-700">পরিচিতি</Link>
            <Link href="/contact" className="text-gray-600 hover:text-green-700">যোগাযোগ</Link>
            <Link href="/detect" className="bg-[#1a5632] text-white px-3 py-1.5 rounded-lg text-xs font-semibold">শুরু করুন</Link>
          </nav>
        </div>
      </header>
      <main className="flex-1">{children}</main>
      <footer className="border-t border-gray-100 py-4 text-center text-xs text-gray-400">
        © ২০২৬ KrishokChat • কৃষক কল সেন্টার: ১৬১২৩
      </footer>
    </div>
  );
}
