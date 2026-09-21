import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(BASE_DIR, 'frontend', 'src', 'lib', 'test-samples-catalog.json')
TS_PATH = os.path.join(BASE_DIR, 'frontend', 'src', 'lib', 'test-samples.ts')

with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Knowledge dictionary to embed in cachedResult
# Read disease-knowledge.ts or define the canonical knowledge map
KNOWLEDGE_MAP = {
    # Rice
    "rice__brown_spot": {
        "name_bn": "ধানের বাদামী দাগ রোগ (Brown Spot)",
        "description_bn": "পাতায় ডিম্বাকৃতি বা গোলাকার তিল তিল বাদামী দাগ দেখা যায়, যার কেন্দ্র ধূসর বা হালকা বাদামী হয়।",
        "cause_bn": "হেলমিন্থোস্পোরিয়াম ওরাইজি (Bipolaris oryzae) ছত্রাকের আক্রমণে ও মাটিতে পটাশ বা পুষ্টির ঘাটতি থাকলে এ রোগ বাড়ে।",
        "solution_bn": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।",
        "solution_en": "Apply balanced fertilization with adequate potassium and zinc. Spray systemic fungicide (Propiconazole 25 EC or Carbendazim 50 WP) at early onset."
    },
    "rice__leaf_blast": {
        "name_bn": "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
        "description_bn": "পাতায় দুই প্রান্ত সুচালো চোখের মতো বা মাকু আকৃতির দাগ দেখা যায়, যা দ্রুত ছড়িয়ে পাতা ঝলসে দেয়।",
        "cause_bn": "ম্যাগনাপোর্টে ওরাইজি (Magnaporthe oryzae) ছত্রাক। অতিরিক্ত ইউরিয়া সার এবং দীর্ঘস্থায়ী কুয়াশা বা মেঘলা আবহাওয়া এর প্রধান কারণ।",
        "solution_bn": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।",
        "solution_en": "Withhold excess nitrogen fertilizer. Spray Tricyclazole 75 WP (0.75 g/L) or Kasugamycin at the appearance of initial spindle lesions."
    },
    "rice__bacterial_leaf_blight": {
        "name_bn": "ধানের ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
        "description_bn": "পাতার ডগা বা কিনারা বরাবর ঢেউ খেলানো পানির দাগ তৈরি হয়, যা শুকিয়ে বাদামী বা খড়ের মতো পুড়ে যায়।",
        "cause_bn": "জ্যান্থোমোনাস ওরাইজি (Xanthomonas oryzae pv. oryzae) ব্যাকটেরিয়া। ঝড়ো বাতাস, অতিরিক্ত বৃষ্টি এবং জলাবদ্ধতায় দ্রুত ছড়ায়।",
        "solution_bn": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।",
        "solution_en": "Halt top-dressing of nitrogen and apply additional potash. Apply approved bactericides (Copper Oxychloride or Bronopol) early in the morning."
    },
    "rice__sheath_blight": {
        "name_bn": "ধানের খোল পোড়া রোগ (Sheath Blight)",
        "description_bn": "গাছের গোড়ার খোলে পানির মতো ভেজা সবুজাভ-ধূসর ডিম্বাকৃতি দাগ হয়, যা ক্রমশ বাদামী হয়ে ওপরের দিকে ছড়ায়।",
        "cause_bn": "রাইজোকটোনিয়া সোলানি (Rhizoctonia solani) ছত্রাক। ঘন চারা রোপণ ও অতিরিক্ত ইউরিয়া ব্যবহার।",
        "solution_bn": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।",
        "solution_en": "Apply balanced fertilization with extra potassium. Spray Validamycin 3L (2 ml/L) or Hexaconazole 5 EC (1 ml/L) at stem base."
    },
    "rice__leaf_scald": {
        "name_bn": "ধানের পাতা ঝলসানো রোগ (Leaf Scald)",
        "description_bn": "পাতার ডগা বা কিনারা থেকে শুরু করে হালকা ও গাঢ় বাদামী বলয়াকৃতির তরঙ্গের মতো ঝলসানো দাগ দেখা যায়।",
        "cause_bn": "মাইক্রোডোকিয়াম ওরাইজি (Microdochium oryzae) ছত্রাক। স্যাঁতসেঁতে ভেজা আবহাওয়া।",
        "solution_bn": "সুষম সার প্রয়োগ করুন। প্রতিরোধে কার্বেন্ডাজিম বা ট্রাইসাইক্লাজল স্প্রে করুন।",
        "solution_en": "Use balanced fertilizer. Spray Carbendazim 50 WP (1 g/L) or Propiconazole 25 EC at disease onset."
    },
    "rice__narrow_brown_leaf_spot": {
        "name_bn": "ধানের সরু বাদামী দাগ রোগ (Narrow Brown Leaf Spot)",
        "description_bn": "পাতার শিরার সমান্তরালে ছোট ও লম্বাটে সুঁচালো গাঢ় লালচে-বাদামী রেখা দাগ দেখা যায়।",
        "cause_bn": "সারকোস্পোরা ওরাইজি (Cercospora oryzae) ছত্রাক। ফসলের শেষ পর্যায়ে পুষ্টির অভাবে এটি বাড়ে।",
        "solution_bn": "মাটিতে পর্যাপ্ত পটাশ নিশ্চিত করুন। রোগ দেখা দিলে প্রোপিকোনাজল বা ডাইফেনোকোনাজল স্প্রে করুন।",
        "solution_en": "Maintain adequate soil potassium. Apply Propiconazole 25 EC (1 ml/L) or Azoxystrobin."
    },
    "rice__rice_hispa": {
        "name_bn": "ধানের পামরী পোকা / ক্ষত (Rice Hispa Damage)",
        "description_bn": "পাতার ওপর সমান্তরাল সাদাটে দাগ বা আঁচড়ের মতো রেখা পড়ে, শুকিয়ে পাতা ঝলসে খড়ের মতো দেখায়।",
        "cause_bn": "পামরী পোকা (Dicladispa armigera)। পূর্ণাঙ্গ পোকা পাতার সবুজ অংশ খায় ও কীড়া পাতার স্তরে সুড়ঙ্গ কাটে।",
        "solution_bn": "আক্রান্ত পাতার ডগা কেটে নষ্ট করুন এবং হাতজাল দিয়ে পোকা ধরুন। আক্রমণ তীব্র হলে ক্লোরপাইরিফস বা সাইপারমেথ্রিন স্প্রে করুন।",
        "solution_en": "Clip infected leaf tips during transplanting and sweep-net adults. Apply approved contact insecticide (Chlorpyrifos 20 EC at 2 ml/L) if ETL exceeds."
    },
    "rice__healthy_leaf": {
        "name_bn": "সুস্থ ও নীরোগ ধান পাতা (Healthy)",
        "description_bn": "পাতার রঙ উজ্জ্বল সবুজ ও সম্পূর্ণ ক্ষতহীন। কোনো ছত্রাক বা ব্যাকটেরিয়ার লক্ষণ নেই।",
        "cause_bn": "যথাযথ সেচ, সঠিক সুষম সার ও অনুকূল আবহাওয়া।",
        "solution_bn": "বর্তমান সেচ ও পরিচর্যা বজায় রাখুন। কোনো রাসায়নিক বালাইনাশকের প্রয়োজন নেই।",
        "solution_en": "Maintain current irrigation, drainage, and nutrient regime. No chemical intervention required."
    },

    # Potato
    "potato__early_blight": {
        "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
        "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
        "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
        "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
        "solution_en": "Spray protective Mancozeb 75 WP (2 g/L) or Azoxystrobin 23 SC. Remove lower infected leaves and avoid overhead irrigation."
    },
    "potato__late_blight": {
        "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
        "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
        "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
        "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
        "solution_en": "Preventive spray with Mancozeb (2 g/L). For active outbreaks, apply systemic Cymoxanil + Mancozeb (Curzate/Sectin) or Metalaxyl-M."
    },
    "potato__healthy_leaf": {
        "name_bn": "সুস্থ আলু পাতা (Healthy)",
        "description_bn": "পাতায় কোনো দাগ বা ধসার চিহ্ন নেই। স্বাভাবিক আকৃতি ও স্বাস্থ্যবান সবুজ রঙ বিদ্যমান।",
        "cause_bn": "সুস্থ বীজ ও সঠিক রোগমুক্ত পরিবেশ।",
        "solution_bn": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।",
        "solution_en": "Maintain regular hilling and soil moisture. Continue routine scouting, especially during foggy mornings."
    },

    # Wheat
    "wheat__leaf_rust": {
        "name_bn": "গমের পাতার মরিচা রোগ (Leaf Rust)",
        "description_bn": "পাতার উপর ছোট ছোট কমলা-বাদামী বা মরিচার মতো পাউডারের গুটি দেখা যায়। হাত দিলে আঙুলে মরিচার গুঁড়া লাগে।",
        "cause_bn": "পাকসিনিয়া ট্রাইটিচিনা (Puccinia triticina) ছত্রাক। উষ্ণ দিন (১৫–২২°C) ও আর্দ্র রাত এ রোগের অনুকূল।",
        "solution_bn": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।",
        "solution_en": "Spray Propiconazole 25 EC (Tilt) at 1 ml/L upon first detection of pustules. In subsequent seasons, plant rust-resistant wheat cultivars."
    },
    "wheat__wheat_blast": {
        "name_bn": "গমের ব্লাস্ট রোগ (Wheat Blast)",
        "description_bn": "পাতায় ধূসর রঙের চোখা দাগ তৈরি হয় এবং শীষের উপরিভাগ সাদা হয়ে শুকিয়ে চিটা হয়ে যায়।",
        "cause_bn": "ম্যাগনাপোর্টে ওরাইজি ট্রাইটিকাম (Magnaporthe oryzae pathotype Triticum)। উষ্ণ ও বৃষ্টিময় আবহাওয়া এ রোগ বাড়ায়।",
        "solution_bn": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।",
        "solution_en": "Apply preventive spray of Nativo 75 WG (Tebuconazole + Trifloxystrobin, 0.6 g/L) at heading stage. Do not save infected grain for seed."
    },
    "wheat__powdery_mildew": {
        "name_bn": "গমের পাউডারি মিলডিউ (Powdery Mildew)",
        "description_bn": "পাতার উপরিভাগে সাদা পাউডার বা আটার মতো তুলতুলে ছত্রাকের আবরণ দেখা যায়, যা পরবর্তীতে ধূসর হয়ে যায়।",
        "cause_bn": "ব্লুমেরিয়া গ্রামিনিস (Blumeria graminis f. sp. tritici) ছত্রাক। ছায়াযুক্ত ও আর্দ্র ঠান্ডা আবহাওয়া।",
        "solution_bn": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।",
        "solution_en": "Avoid high-density sowing. Spray Wettable Sulfur 80 WP (Thiovit, 2 g/L) or Propiconazole 25 EC at disease onset."
    },
    "wheat__stripe_rust": {
        "name_bn": "গমের হলুদ মরিচা রোগ (Stripe / Yellow Rust)",
        "description_bn": "পাতার শিরার সমান্তরালে সরু হলুদ রঙের ডোরাকাটা বা সারিবদ্ধ ফোসকার মতো গুটি দেখা যায়।",
        "cause_bn": "পাকসিনিয়া স্ট্রাইফর্মিস (Puccinia striiformis) ছত্রাক। শীতকালীন ঠান্ডা ও আর্দ্র আবহাওয়া (১০–১৫°C)।",
        "solution_bn": "হলুদ ডোরা দেখা মাত্রই টিল্ট (প্রোপিকোনাজল ২৫০ ইসি) ১ মিলি/লিটার হারে স্প্রে করুন।",
        "solution_en": "Apply Propiconazole 25 EC (1 ml/L) or Tebuconazole upon first detection of yellow stripes."
    },
    "wheat__healthy": {
        "name_bn": "সুস্থ গমের পাতা (Healthy)",
        "description_bn": "সবুজ ও তেজস্বী পাতা, কোনো ধরনের মরিচা, দাগ বা ঝলসে যাওয়ার লক্ষণ নেই।",
        "cause_bn": "সঠিক বপন সময়, পুষ্টি ও উপযোগী ঠাণ্ডা আবহাওয়া।",
        "solution_bn": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।",
        "solution_en": "Ensure adequate crown root and heading irrigation stages. No fungicide required."
    },

    # Corn
    "corn__common_rust": {
        "name_bn": "ভুট্টার কমন রাস্ট (Common Rust)",
        "description_bn": "পাতার উভয় পিঠে ছোট ছোট বাদামী বা লালচে মরিচার ফোসকা তৈরি হয় যা ফেটে গুঁড়া ছড়ায়।",
        "cause_bn": "পাকসিনিয়া সরঘি (Puccinia sorghi) ছত্রাক। মাঝারি তাপমাত্রা (১৬–২৫°C) ও উচ্চ আর্দ্রতায় এ রোগ বৃদ্ধি পায়।",
        "solution_bn": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।",
        "solution_en": "Apply protective Mancozeb (2 g/L) or Azoxystrobin 23 SC. For heavy infection, apply a systemic triazole fungicide."
    },
    "corn__gray_leaf_spot": {
        "name_bn": "ভুট্টার ধূসর পাতা দাগ (Gray Leaf Spot)",
        "description_bn": "পাতার শিরার সাথে সমান্তরাল আয়তাকার ধূসর বা বাদামী রঙের লম্বা দাগ দেখা যায়।",
        "cause_bn": "সারকোস্পোরা জিয়া-মেডিস (Cercospora zeae-maydis) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়ায় নিচের পাতা থেকে উপরে ছড়ায়।",
        "solution_bn": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।",
        "solution_en": "Practice crop rotation and bury crop residue. Apply Pyraclostrobin or Propiconazole at first sign of disease on lower leaves."
    },
    "corn__northern_leaf_blight": {
        "name_bn": "ভুট্টার উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
        "description_bn": "পাতায় লম্বাটে চুরুট আকৃতির বড় ধূসর-সবুজ বা বাদামী রঙের দাগ সৃষ্টি হয়।",
        "cause_bn": "এক্সসিরোহিলাম টার্সিকাম (Exserohilum turcicum) ছত্রাক। ঠাণ্ডা-নাতিশীতোষ্ণ ভেজা আবহাওয়া এর অনুকূল।",
        "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।",
        "solution_en": "Apply systemic fungicides (Carbendazim + Mancozeb, 2 g/L or Azoxystrobin). Avoid dense plant populations to improve air circulation."
    },
    "corn__healthy": {
        "name_bn": "সুস্থ ভুট্টা পাতা (Healthy)",
        "description_bn": "প্রশস্ত গাঢ় সবুজ পাতা, চমৎকার সালোকসংশ্লেষণ ক্ষমতা ও দাগমুক্ত উজ্জ্বলতা।",
        "cause_bn": "যথাযথ নাইট্রোজেন ও জিংক পুষ্টি এবং পর্যাপ্ত রোদ।",
        "solution_bn": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।",
        "solution_en": "Maintain soil moisture through tasseling and silking stages. No chemical application needed."
    },

    # Chilli
    "chilli__bacterial_spot": {
        "name_bn": "মরিচের ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
        "description_bn": "পাতায় ছোট ছোট কালচে-বাদামী জলছাপের মতো দাগ দেখা যায়, যা পরবর্তীতে খসখসে হয়ে ছিদ্র তৈরি করে।",
        "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. vesicatoria)। অতিরিক্ত বৃষ্টি ও পাতার ভেজা অবস্থায় দ্রুত ছড়ায়।",
        "solution_bn": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।",
        "solution_en": "Spray Copper Oxychloride 50 WP (2 g/L) combined with an agricultural bactericide. Avoid overhead sprinkler irrigation."
    },
    "chilli__curl_virus": {
        "name_bn": "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl Virus)",
        "description_bn": "পাতা উপরের দিকে চামচের মতো কুঁকড়ে যায়, গাছের বৃদ্ধি থমকে যায় এবং ফুল ও ফল ঝরে পড়ে।",
        "cause_bn": "বেগমোভাইরাস (Begomovirus)। সাদা মাছি (Bemisia tabaci) পোকা এ রোগের প্রধান বাহক।",
        "solution_bn": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।",
        "solution_en": "Control the whitefly vector using Imidacloprid 20 SL (0.5 ml/L) or Acetamiprid 20 SP. Install yellow sticky traps (15–20 per acre)."
    },
    "chilli__cercospora_leaf_spot": {
        "name_bn": "মরিচের সারকোস্পোরা দাগ / ব্যাঙের চোখ দাগ (Cercospora)",
        "description_bn": "পাতায় গোলাকার দাগ যার কেন্দ্র ধূসর বা সাদাটে এবং চারপাশ গাঢ় বাদামী বৃত্তে ঘেরা (ব্যাঙের চোখের মতো)।",
        "cause_bn": "সারকোস্পোরা ক্যাপসিকি (Cercospora capsici) ছত্রাক। আর্দ্র পরিবেশ ও ঘন গাছপালায় এটি দ্রুত ছড়ায়।",
        "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।",
        "solution_en": "Spray Carbendazim 50 WP (1 g/L) or Chlorothalonil 75 WP (2 g/L). Provide adequate plant spacing to facilitate ventilation."
    },
    "chilli__powdery_mildew": {
        "name_bn": "মরিচের পাউডারি মিলডিউ (Powdery Mildew)",
        "description_bn": "পাতার নিচের পিঠে সাদা পাউডারের মতো ছত্রাকের উপস্থিতি এবং ওপরের পিঠে হলুদ বা তামাটে ছোপ দেখা যায়।",
        "cause_bn": "লেভেইলুলা টরিকা (Leveillula taurica) ছত্রাক। শুষ্ক উষ্ণ দিন ও আর্দ্র রাত।",
        "solution_bn": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।",
        "solution_en": "Spray Wettable Sulfur 80 WP (2 g/L) or Hexaconazole 5 EC (1 ml/L). Remove severely blighted foliage."
    },
    "chilli__healthy_leaf": {
        "name_bn": "সুস্থ মরিচ পাতা (Healthy)",
        "description_bn": "মসৃণ ও চকচকে গাঢ় সবুজ পাতা, কোনো কোঁকড়ানো বা দাগের উপসর্গ নেই।",
        "cause_bn": "সুষম সার, নিয়ন্ত্রিত আর্দ্রতা ও পোকা-মাকড়মুক্ত পরিবেশ।",
        "solution_bn": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।",
        "solution_en": "Maintain well-drained raised bed soil conditions. Continue visual scouting for sucking pests."
    },

    # Brassica
    "brassica__alternaria_spot": {
        "name_bn": "বাঁধাকপির অল্টারনারিয়া গোল দাগ রোগ (Alternaria)",
        "description_bn": "পাতায় গাঢ় বাদামী থেকে কালো রঙের গোলাকার বলয়াকৃতি দাগ দেখা যায়, যা শুকিয়ে পাতার ভেতর ফুটো করে দেয়।",
        "cause_bn": "অল্টারনারিয়া ব্রাসিকি (Alternaria brassicae) ছত্রাক। কুয়াশাচ্ছন্ন দিন এবং ঘন শিশিরে এ রোগ ব্যাপক আকার ধারণ করে।",
        "solution_bn": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।",
        "solution_en": "Spray Mancozeb 75 WP (2 g/L) or Iprodione 50 WP (Rovral). Always mix an agricultural sticker/spreader for waxy brassica foliage."
    },
    "brassica__black_rot": {
        "name_bn": "কপির ব্লাক রট রোগ (Cabbage Black Rot)",
        "description_bn": "পাতার কিনারা থেকে ভেতরের দিকে ইংরেজি 'V' অক্ষরের মতো হলুদ দাগ তৈরি হয় এবং পাতার শিরাগুলো কালো হয়ে যায়।",
        "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. campestris) ব্যাকটেরিয়া।",
        "solution_bn": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।",
        "solution_en": "Use hot-water treated certified seeds. Spray Copper Oxychloride (2 g/L) with agricultural bactericide."
    },
    "brassica__downy_mildew": {
        "name_bn": "কপির ডাউনি মিলডিউ (Downy Mildew)",
        "description_bn": "পাতার উপরের পৃষ্ঠে কৌণিক হলুদ ছোপ এবং ঠিক নিচের পিঠে সাদাটে বা ধূসর রোমশ ছত্রাকের জাল দেখা যায়।",
        "cause_bn": "হায়ালোপারোনোস্পোরা ব্রাসিকি (Hyaloperonospora brassicae)। ঠান্ডা ও শিশিরভেজা কুয়াশা।",
        "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। মেটাল্যাক্সিল + ম্যানকোজেব (রিডোমিল গোল্ড ২ গ্রাম/লিটার) স্প্রে করুন।",
        "solution_en": "Prune infected seedlings. Spray Metalaxyl-M + Mancozeb (Ridomil Gold, 2 g/L) preventively."
    },
    "brassica__cauliflower_alternaria": {
        "name_bn": "ফুলকপির অল্টারনারিয়া রোগ (Cauliflower Alternaria)",
        "description_bn": "পাতায় বাদামী রিং দাগ এবং ফুলকপির মাথায় বাদামী বা কালো দাগ পড়ে পণ্যের মান নষ্ট করে।",
        "cause_bn": "অল্টারনারিয়া ছত্রাকের আক্রমণ। অপরিচ্ছন্ন জমি ও আর্দ্র আবহাওয়ায় বিস্তার লাভ করে।",
        "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।",
        "solution_en": "Prune and dispose of infected leaves. Apply Difenoconazole 250 EC (Score, 0.5 ml/L) or Azoxystrobin + Difenoconazole."
    },
    "brassica__cauliflower_bacterial_spot": {
        "name_bn": "ফুলকপির ব্যাকটেরিয়াল দাগ (Cauliflower Bacterial Spot)",
        "description_bn": "পাতায় ছোট ছোট কালচে কৌণিক পানির মতো দাগ তৈরি হয় যা দ্রুত বাদামী বা কালো ক্ষতে রূপ নেয়।",
        "cause_bn": "সিউডোমোনাস বা জ্যান্থোমোনাস ব্যাকটেরিয়া। ভারী বৃষ্টি ও অপরিচ্ছন্ন জমি।",
        "solution_bn": "সুষম সার দিন ও জলাবদ্ধতা দূর করুন। কপার হাইড্রোক্সাইড বা কপার অক্সিক্লোরাইড স্প্রে করুন।",
        "solution_en": "Improve drainage and avoid overhead sprinkler watering. Apply Copper Hydroxide (2 g/L)."
    },
    "brassica__healthy": {
        "name_bn": "সুস্থ ফুলকপি পাতা (Healthy)",
        "description_bn": "মোমের মতো চকচকে অক্ষত পাতা, স্বাস্থ্যবান বর্ধনশীল কুঁড়ি ও চমৎকার গঠন।",
        "cause_bn": "সঠিক জমি তৈরি, বোরণ ও মলিবডেনাম পুষ্টি এবং নিয়ন্ত্রিত সেচ।",
        "solution_bn": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।",
        "solution_en": "Keep soil evenly moist without waterlogging the root zone. Continue regular weed and fertility management."
    }
}

ts_lines = [
    'import type { DetectResponse } from "@/lib/api";',
    '',
    'export interface TestSampleInstance {',
    '  id: string;',
    '  crop: "Rice" | "Potato" | "Wheat" | "Corn" | "Chilli" | "Brassica";',
    '  cropBn: string;',
    '  cropEn: string;',
    '  disease: string;',
    '  diseaseBn: string;',
    '  diseaseEn: string;',
    '  targetClass: string;',
    '  confidence: number;',
    '  imageSrc: string;',
    '  cropHint: string;',
    '  cachedResult: DetectResponse;',
    '}',
    '',
    'export const CROP_GROUPS: {',
    '  crop: TestSampleInstance["crop"];',
    '  cropBn: string;',
    '  cropEn: string;',
    '  icon: string;',
    '  count: number;',
    '}[] = [',
    '  { crop: "Rice", cropBn: "ধান", cropEn: "Rice", icon: "🌾", count: 20 },',
    '  { crop: "Potato", cropBn: "আলু", cropEn: "Potato", icon: "🥔", count: 16 },',
    '  { crop: "Wheat", cropBn: "গম", cropEn: "Wheat", icon: "🌿", count: 16 },',
    '  { crop: "Corn", cropBn: "ভুট্টা", cropEn: "Corn", icon: "🌽", count: 16 },',
    '  { crop: "Chilli", cropBn: "মরিচ", cropEn: "Chilli", icon: "🌶️", count: 16 },',
    '  { crop: "Brassica", cropBn: "কপি ও ব্রাসিকা", cropEn: "Cabbage & Cauliflower (Brassica)", icon: "🥦", count: 16 },',
    '];',
    '',
    'export const VERIFIED_TEST_SAMPLES: TestSampleInstance[] = ['
]

for item in catalog:
    crop = item['crop']
    crop_bn = item['cropBn']
    crop_en = item['cropEn']
    disease = item['disease']
    disease_bn = item['diseaseBn']
    disease_en = item['diseaseEn']
    target_class = item['targetClass']
    conf = item['confidence']
    img_src = item['imageSrc']
    crop_hint = item['cropHint']
    sample_id = item['id']

    k_key = f"{crop.lower()}__{disease.lower()}"
    info = KNOWLEDGE_MAP.get(k_key, {
        "name_bn": disease_bn,
        "description_bn": f"{crop_bn} ফসলের {disease_bn} সংক্রান্ত পরীক্ষিত নমুনা।",
        "cause_bn": "মাঠপর্যায়ের প্যাথোজেন সংক্রমণ।",
        "solution_bn": "কৃষি বিশেষজ্ঞ ও বিএআরআই নির্দেশিকা অনুযায়ী সুষম ব্যবস্থাপনা গ্রহণ করুন।",
        "solution_en": "Follow standard BARI/BRRI integrated pest management protocol."
    })

    is_healthy = "healthy" in disease.lower()
    status_str = "healthy" if is_healthy else "diagnosed"

    cached_result = {
        "status": status_str,
        "detection_mode": "classification",
        "crop": crop,
        "crop_confidence": 1.0,
        "crop_source": "user",
        "disease": disease,
        "disease_confidence": conf / 100.0,
        "boxes": [],
        "disease_info": {
            "name_bn": info.get("name_bn", disease_bn),
            "description_bn": info.get("description_bn", ""),
            "cause_bn": info.get("cause_bn", ""),
            "solution_bn": info.get("solution_bn", ""),
        },
        "top3_crops": [{"class": crop, "confidence": 1.0}],
        "top3_diseases": [{"class": disease, "confidence": conf / 100.0}],
        "treatment_advice": info.get("solution_bn", ""),
        "treatment_confidence": "high",
        "treatment_sources": ["BARI/BRRI Verified Guide", "KrishokChat Evaluation Benchmark"],
        "verifier_flags": [],
        "agent_trace": [
            {"stage": "intake", "status": "complete", "detail": f"Specimen: {sample_id} (Edge CDN)"},
            {"stage": "crop_classification", "status": "complete", "detail": f"{crop_bn} ({crop})"},
            {"stage": "disease_classification", "status": "complete", "detail": f"{disease_bn} [{conf}%]"},
            {"stage": "advisory", "status": "complete", "detail": "BARI/BRRI Verified Prescription"}
        ],
        "quality_warnings": []
    }

    # Format JSON nicely indented
    cached_json = json.dumps(cached_result, ensure_ascii=False, indent=6)

    ts_lines.append(f'  {{')
    ts_lines.append(f'    id: {json.dumps(sample_id)},')
    ts_lines.append(f'    crop: {json.dumps(crop)},')
    ts_lines.append(f'    cropBn: {json.dumps(crop_bn, ensure_ascii=False)},')
    ts_lines.append(f'    cropEn: {json.dumps(crop_en)},')
    ts_lines.append(f'    disease: {json.dumps(disease)},')
    ts_lines.append(f'    diseaseBn: {json.dumps(disease_bn, ensure_ascii=False)},')
    ts_lines.append(f'    diseaseEn: {json.dumps(disease_en)},')
    ts_lines.append(f'    targetClass: {json.dumps(target_class)},')
    ts_lines.append(f'    confidence: {conf},')
    ts_lines.append(f'    imageSrc: {json.dumps(img_src)},')
    ts_lines.append(f'    cropHint: {json.dumps(crop_hint)},')
    ts_lines.append(f'    cachedResult: {cached_json},')
    ts_lines.append(f'  }},')

ts_lines.append('];')
ts_lines.append('')

with open(TS_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(ts_lines))

print(f"Successfully generated {len(catalog)} test samples in: {TS_PATH}")
