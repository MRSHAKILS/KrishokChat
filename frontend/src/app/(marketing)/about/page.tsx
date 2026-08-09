export default function AboutPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-6 py-8">
      <h1 className="text-3xl font-bold text-gray-900">পরিচিতি</h1>
      <div className="prose prose-sm text-gray-600 space-y-4">
        <p>
          কৃষক চ্যাট হলো একটি বাংলাদেশী কৃষি-এআই পরামর্শদাতা সিস্টেম যা কৃষকদের ফসলের রোগ শনাক্ত করতে এবং চিকিৎসা পরামর্শ দিতে সাহায্য করে।
        </p>
        <p>
          এই সিস্টেমটি তিনটি প্রধান প্রযুক্তি ব্যবহার করে: কম্পিউটার ভিশন (রোগ শনাক্ত),ি রিট্রিভাল-অগমেন্টেড জেনারেশন (তথ্যভিত্তিক উত্তর), এবং এজেন্টিক ওয়ার্কফ্লো (বিশ্লেষণ প্রক্রিয়া প্রদর্শন)।
        </p>
        <h2 className="text-xl font-bold text-gray-900">বৈশিষ্ট্য</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>পাতার ছবি থেকে রোগ শনাক্ত</li>
          <li>বাংলায় প্রশ্ন-উত্তর (বহু প্রশ্ন সমর্থন)</li>
          <li>নিরাপত্তা যাচাই ও নৈতিক সীমারেখা</li>
          <li>সক্রিয় পরিসংখ্যান ও অডিট লগ</li>
        </ul>
      </div>
    </div>
  );
}
