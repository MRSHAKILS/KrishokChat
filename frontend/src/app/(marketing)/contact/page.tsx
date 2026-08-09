export default function ContactPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-6 py-8">
      <h1 className="text-3xl font-bold text-gray-900">যোগাযোগ</h1>
      <div className="space-y-4 text-sm text-gray-600">
        <p>কৃষি সংক্রান্ত যেকোনো প্রশ্নের জন্য নিচের নম্বরে যোগাযোগ করুন:</p>
        <div className="bg-green-50 border border-green-200 rounded-xl p-5 space-y-2">
          <div className="flex justify-between">
            <span>কৃষক কল সেন্টার (বাংলাদেশ সরকার)</span>
            <a href="tel:16123" className="font-bold text-green-700">১৬১২৩</a>
          </div>
          <div className="flex justify-between">
            <span>জাতীয় জরুরি সেবা</span>
            <a href="tel:999" className="font-bold text-red-600">৯৯৯</a>
          </div>
        </div>
        <p className="text-xs text-gray-400">এই সিস্টেম একটি গবেষণা প্রোটোটাইপ। জরুরি পরিস্থিতিতে সরাসরি কল করুন।</p>
      </div>
    </div>
  );
}
