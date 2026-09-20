export interface LocalizedDiseaseKnowledge {
  nameBn: string;
  nameEn: string;
  cropBn: string;
  cropEn: string;
  descBn: string;
  descEn: string;
  causeBn: string;
  causeEn: string;
  solutionBn: string;
  solutionEn: string;
}

export const DISEASE_KNOWLEDGE_MAP: Record<string, LocalizedDiseaseKnowledge> = {
  // --- RICE (ধান) ---
  rice__brown_spot: {
    nameBn: "ধানের বাদামী দাগ রোগ (Brown Spot)",
    nameEn: "Rice Brown Spot Disease",
    cropBn: "ধান",
    cropEn: "Rice",
    descBn: "পাতায় ডিম্বাকৃতি বা গোলাকার তিল তিল বাদামী দাগ দেখা যায়, যার কেন্দ্র ধূসর বা হালকা বাদামী হয়।",
    descEn: "Small oval to circular brown lesions appear on leaves, typically with gray or light brown necrotic centers and yellow halos.",
    causeBn: "হেলমিন্থোস্পোরিয়াম ওরাইজি (Bipolaris oryzae) ছত্রাকের আক্রমণে ও মাটিতে পটাশ বা পুষ্টির ঘাটতি থাকলে এ রোগ বাড়ে।",
    causeEn: "Caused by the fungal pathogen Bipolaris oryzae, aggravated by soil nutrient deficiency (especially potassium and zinc) and water stress.",
    solutionBn: "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।",
    solutionEn: "Apply balanced fertilization with adequate potassium and zinc. Spray systemic fungicide (Propiconazole 25 EC or Carbendazim 50 WP) at early onset.",
  },
  rice__leaf_blast: {
    nameBn: "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
    nameEn: "Rice Leaf Blast Disease",
    cropBn: "ধান",
    cropEn: "Rice",
    descBn: "পাতায় দুই প্রান্ত সুচালো চোখের মতো বা মাকু আকৃতির দাগ দেখা যায়, যা দ্রুত ছড়িয়ে পাতা ঝলসে দেয়।",
    descEn: "Classic diamond or spindle-shaped lesions with gray-white centers and reddish-brown borders appear on leaf blades.",
    causeBn: "ম্যাগনাপোর্টে ওরাইজি (Magnaporthe oryzae) ছত্রাক। অতিরিক্ত ইউরিয়া সার এবং দীর্ঘস্থায়ী কুয়াশা বা মেঘলা আবহাওয়া এর প্রধান কারণ।",
    causeEn: "Caused by Magnaporthe oryzae (Pyricularia oryzae), promoted by excess nitrogen fertilizer, high relative humidity, and cool overcast weather.",
    solutionBn: "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।",
    solutionEn: "Withhold excess nitrogen fertilizer. Spray Tricyclazole 75 WP (0.75 g/L) or Kasugamycin at the appearance of initial spindle lesions.",
  },
  rice__bacterial_leaf_blight: {
    nameBn: "ধানের ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
    nameEn: "Rice Bacterial Leaf Blight (BLB)",
    cropBn: "ধান",
    cropEn: "Rice",
    descBn: "পাতার ডগা বা কিনারা বরাবর ঢেউ খেলানো পানির দাগ তৈরি হয়, যা শুকিয়ে বাদামী বা খড়ের মতো পুড়ে যায়।",
    descEn: "Water-soaked lesions begin at leaf margins and tips, expanding with undulating margins, turning yellowish-brown and straw-colored.",
    causeBn: "জ্যান্থোমোনাস ওরাইজি (Xanthomonas oryzae pv. oryzae) ব্যাকটেরিয়া। ঝড়ো বাতাস, অতিরিক্ত বৃষ্টি এবং জলাবদ্ধতায় দ্রুত ছড়ায়।",
    causeEn: "Caused by Xanthomonas oryzae pv. oryzae bacteria, rapidly transmitted through wind-driven rains, irrigation water, and leaf contact.",
    solutionBn: "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।",
    solutionEn: "Halt top-dressing of nitrogen and apply additional potash. Apply approved bactericides (Copper Oxychloride or Bronopol) early in the morning.",
  },
  rice__healthy_leaf: {
    nameBn: "সুস্থ ও নীরোগ ধান পাতা (Healthy)",
    nameEn: "Healthy Rice Leaf",
    cropBn: "ধান",
    cropEn: "Rice",
    descBn: "পাতার রঙ উজ্জ্বল সবুজ ও সম্পূর্ণ ক্ষতহীন। কোনো ছত্রাক বা ব্যাকটেরিয়ার লক্ষণ নেই।",
    descEn: "Uniform, vibrant green foliage free from lesions, chlorosis, necrosis, or pest feeding injury.",
    causeBn: "যথাযথ সেচ, সঠিক সুষম সার ও অনুকূল আবহাওয়া।",
    causeEn: "Optimal soil nutrition, proper water management, and absence of pathogenic inoculum.",
    solutionBn: "বর্তমান সেচ ও পরিচর্যা বজায় রাখুন। কোনো রাসায়নিক বালাইনাশকের প্রয়োজন নেই।",
    solutionEn: "Maintain current irrigation, drainage, and nutrient regime. No chemical intervention required.",
  },

  // --- POTATO (আলু) ---
  potato__early_blight: {
    nameBn: "আলুর আগাম ধসা রোগ (Early Blight)",
    nameEn: "Potato Early Blight",
    cropBn: "আলু",
    cropEn: "Potato",
    descBn: "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
    descEn: "Distinct target-board concentric dark brown rings surrounded by chlorotic yellow halos, starting on older lower leaves.",
    causeBn: "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
    causeEn: "Fungal pathogen Alternaria solani, favored by alternating wet and dry periods, warm temperatures (24–29°C), and crop stress.",
    solutionBn: "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
    solutionEn: "Spray protective Mancozeb 75 WP (2 g/L) or Azoxystrobin 23 SC. Remove lower infected leaves and avoid overhead irrigation.",
  },
  potato__late_blight: {
    nameBn: "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
    nameEn: "Potato Late Blight Disease",
    cropBn: "আলু",
    cropEn: "Potato",
    descBn: "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়ায় সাদা তুলার মতো ছত্রাক দেখা যায়।",
    descEn: "Irregular, water-soaked dark brown to purplish lesions that rapidly enlarge, with white cottony fungal sporulation on leaf undersides in high humidity.",
    causeBn: "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
    causeEn: "Caused by oomycete Phytophthora infestans, developing epidemically under persistent fog, high humidity (>90%), and cool temperatures (12–18°C).",
    solutionBn: "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
    solutionEn: "Preventive spray with Mancozeb (2 g/L). For active outbreaks, apply systemic Cymoxanil + Mancozeb (Curzate/Sectin) or Metalaxyl-M.",
  },
  potato__healthy_leaf: {
    nameBn: "সুস্থ আলু পাতা (Healthy)",
    nameEn: "Healthy Potato Leaf",
    cropBn: "আলু",
    cropEn: "Potato",
    descBn: "পাতায় কোনো দাগ বা ধসার চিহ্ন নেই। স্বাভাবিক আকৃতি ও স্বাস্থ্যবান সবুজ রঙ বিদ্যমান।",
    descEn: "Vigorous, dark-green leaves showing healthy turgor with zero signs of blighting, curling, or chlorosis.",
    causeBn: "সুস্থ বীজ ও সঠিক রোগমুক্ত পরিবেশ।",
    causeEn: "Certified disease-free seed tubers, balanced fertilization, and good soil drainage.",
    solutionBn: "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।",
    solutionEn: "Maintain regular hilling and soil moisture. Continue routine scouting, especially during foggy mornings.",
  },

  // --- WHEAT (গম) ---
  wheat__leaf_rust: {
    nameBn: "গমের পাতার মরিচা রোগ (Leaf Rust)",
    nameEn: "Wheat Leaf Rust (Brown Rust)",
    cropBn: "গম",
    cropEn: "Wheat",
    descBn: "পাতার উপর ছোট ছোট কমলা-বাদামী বা মরিচার মতো পাউডারের গুটি দেখা যায়। হাত দিলে আঙুলে মরিচার গুঁড়া লাগে।",
    descEn: "Small, circular to oval orange-brown powdery pustules (uredinia) scattered across the upper surface of wheat leaves.",
    causeBn: "পাকসিনিয়া ট্রাইটিচিনা (Puccinia triticina) ছত্রাক। উষ্ণ দিন (১৫–২২°C) ও আর্দ্র রাত এ রোগের অনুকূল।",
    causeEn: "Caused by the obligate biotrophic fungus Puccinia triticina, thriving in moderate temperatures with prolonged leaf wetness.",
    solutionBn: "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।",
    solutionEn: "Spray Propiconazole 25 EC (Tilt) at 1 ml/L upon first detection of pustules. In subsequent seasons, plant rust-resistant wheat cultivars.",
  },
  wheat__wheat_blast: {
    nameBn: "গমের ব্লাস্ট রোগ (Wheat Blast)",
    nameEn: "Wheat Blast Disease",
    cropBn: "গম",
    cropEn: "Wheat",
    descBn: "পাতায় ধূসর রঙের চোখা দাগ তৈরি হয় এবং শীষের উপরিভাগ সাদা হয়ে শুকিয়ে চিটা হয়ে যায়।",
    descEn: "Elliptical, eye-shaped lesions on leaves; premature bleaching and drying of spikelets above the infection point, causing sterile grain.",
    causeBn: "ম্যাগনাপোর্টে ওরাইজি ট্রাইটিকাম (Magnaporthe oryzae pathotype Triticum)। উষ্ণ ও বৃষ্টিময় আবহাওয়া এ রোগ বাড়ায়।",
    causeEn: "Caused by Magnaporthe oryzae pathotype Triticum (MoT), triggered by high temperatures (25–30°C) coinciding with heading rains.",
    solutionBn: "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।",
    solutionEn: "Apply preventive spray of Nativo 75 WG (Tebuconazole + Trifloxystrobin, 0.6 g/L) at heading stage. Do not save infected grain for seed.",
  },
  wheat__healthy: {
    nameBn: "সুস্থ গমের পাতা (Healthy)",
    nameEn: "Healthy Wheat Leaf",
    cropBn: "গম",
    cropEn: "Wheat",
    descBn: "সবুজ ও তেজস্বী পাতা, কোনো ধরনের মরিচা, দাগ বা ঝলসে যাওয়ার লক্ষণ নেই।",
    descEn: "Clean, erect green foliage displaying normal vegetative vigor without fungal pustules or tip necrosis.",
    causeBn: "সঠিক বপন সময়, পুষ্টি ও উপযোগী ঠাণ্ডা আবহাওয়া।",
    causeEn: "Timely sowing, balanced basal fertilization, and optimum seasonal conditions.",
    solutionBn: "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।",
    solutionEn: "Ensure adequate crown root and heading irrigation stages. No fungicide required.",
  },

  // --- CORN / MAIZE (ভুট্টা) ---
  corn__common_rust: {
    nameBn: "ভুট্টার কমন রাস্ট (Common Rust)",
    nameEn: "Corn Common Rust",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    descBn: "পাতার উভয় পিঠে ছোট ছোট বাদামী বা লালচে মরিচার ফোসকা তৈরি হয় যা ফেটে গুঁড়া ছড়ায়।",
    descEn: "Prominent golden to reddish-brown powdery pustules erupting on both upper and lower leaf surfaces, releasing brick-red urediniospores.",
    causeBn: "পাকসিনিয়া সরঘি (Puccinia sorghi) ছত্রাক। মাঝারি তাপমাত্রা (১৬–২৫°C) ও উচ্চ আর্দ্রতায় এ রোগ বৃদ্ধি পায়।",
    causeEn: "Fungal pathogen Puccinia sorghi, favored by cool to moderate temperatures and extended periods of dew.",
    solutionBn: "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।",
    solutionEn: "Apply protective Mancozeb (2 g/L) or Azoxystrobin 23 SC. For heavy infection, apply a systemic triazole fungicide.",
  },
  corn__gray_leaf_spot: {
    nameBn: "ভুট্টার ধূসর পাতা দাগ (Gray Leaf Spot)",
    nameEn: "Corn Gray Leaf Spot (GLS)",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    descBn: "পাতার শিরার সাথে সমান্তরাল আয়তাকার ধূসর বা বাদামী রঙের লম্বা দাগ দেখা যায়।",
    descEn: "Distinct rectangular, vein-delimited lesions with sharp margins, turning grayish-brown as spores mature on leaf surfaces.",
    causeBn: "সারকোস্পোরা জিয়া-মেডিস (Cercospora zeae-maydis) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়ায় নিচের পাতা থেকে উপরে ছড়ায়।",
    causeEn: "Caused by Cercospora zeae-maydis, favored by warm, humid overcast days (25–30°C) with persistent moisture in canopy.",
    solutionBn: "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।",
    solutionEn: "Practice crop rotation and bury crop residue. Apply Pyraclostrobin or Propiconazole at first sign of disease on lower leaves.",
  },
  corn__northern_leaf_blight: {
    nameBn: "ভুট্টার উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
    nameEn: "Corn Northern Leaf Blight (NLB)",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    descBn: "পাতায় লম্বাটে চুরুট আকৃতির বড় ধূসর-সবুজ বা বাদামী রঙের দাগ সৃষ্টি হয়।",
    descEn: "Large, elongated, cigar-shaped grayish-green to tan lesions (2.5–15 cm long) with smooth margins that coalesce and scorch foliage.",
    causeBn: "এক্সসিরোহিলাম টার্সিকাম (Exserohilum turcicum) ছত্রাক। ঠাণ্ডা-নাতিশীতোষ্ণ ভেজা আবহাওয়া এর অনুকূল।",
    causeEn: "Caused by the fungus Exserohilum turcicum, flourishing under moderate temperatures (18–27°C) and heavy dew periods.",
    solutionBn: "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।",
    solutionEn: "Apply systemic fungicides (Carbendazim + Mancozeb, 2 g/L or Azoxystrobin). Avoid dense plant populations to improve air circulation.",
  },
  corn__healthy: {
    nameBn: "সুস্থ ভুট্টা পাতা (Healthy)",
    nameEn: "Healthy Corn Foliage",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    descBn: "প্রশস্ত গাঢ় সবুজ পাতা, চমৎকার সালোকসংশ্লেষণ ক্ষমতা ও দাগমুক্ত উজ্জ্বলতা।",
    descEn: "Broad, robust, dark-green leaves showing vigorous architecture with intact leaf cuticle and zero lesion spots.",
    causeBn: "যথাযথ নাইট্রোজেন ও জিংক পুষ্টি এবং পর্যাপ্ত রোদ।",
    causeEn: "Balanced nitrogen and zinc uptake, proper spacing, and optimal solar radiation.",
    solutionBn: "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।",
    solutionEn: "Maintain soil moisture through tasseling and silking stages. No chemical application needed.",
  },

  // --- CHILLI (মরিচ) ---
  chilli__bacterial_spot: {
    nameBn: "মরিচের ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
    nameEn: "Chilli Bacterial Spot Disease",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    descBn: "পাতায় ছোট ছোট কালচে-বাদামী জলছাপের মতো দাগ দেখা যায়, যা পরবর্তীতে খসখসে হয়ে ছিদ্র তৈরি করে।",
    descEn: "Small, circular to irregular dark brown water-soaked specks on leaves that turn greasy and scabby with chlorotic yellow borders.",
    causeBn: "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. vesicatoria)। অতিরিক্ত বৃষ্টি ও পাতার ভেজা অবস্থায় দ্রুত ছড়ায়।",
    causeEn: "Caused by Xanthomonas campestris pv. vesicatoria, spread via splashing rain, overhead irrigation, and handling wet plants.",
    solutionBn: "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।",
    solutionEn: "Spray Copper Oxychloride 50 WP (2 g/L) combined with an agricultural bactericide. Avoid overhead sprinkler irrigation.",
  },
  chilli__curl_virus: {
    nameBn: "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl Virus)",
    nameEn: "Chilli Leaf Curl Virus (ChiLCV)",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    descBn: "পাতা উপরের দিকে চামচের মতো কুঁকড়ে যায়, গাছের বৃদ্ধি থমকে যায় এবং ফুল ও ফল ঝরে পড়ে।",
    descEn: "Severe upward and downward leaf curling, vein thickening, stunted bush-like growth, and drastic reduction in fruit setting.",
    causeBn: "বেগমোভাইরাস (Begomovirus)। সাদা মাছি (Bemisia tabaci) পোকা এ রোগের প্রধান বাহক।",
    causeEn: "Transmitted by the whitefly vector Bemisia tabaci. The virus does not spread by mechanical tools or seeds directly.",
    solutionBn: "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।",
    solutionEn: "Control the whitefly vector using Imidacloprid 20 SL (0.5 ml/L) or Acetamiprid 20 SP. Install yellow sticky traps (15–20 per acre).",
  },
  chilli__cercospora_leaf_spot: {
    nameBn: "মরিচের সারকোস্পোরা দাগ / ব্যাঙের চোখ দাগ (Cercospora)",
    nameEn: "Chilli Cercospora Leaf Spot (Frogeye)",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    descBn: "পাতায় গোলাকার দাগ যার কেন্দ্র ধূসর বা সাদাটে এবং চারপাশ গাঢ় বাদামী বৃত্তে ঘেরা (ব্যাঙের চোখের মতো)।",
    descEn: "Circular 'frogeye' lesions with light gray or whitish centers bordered by distinct dark reddish-brown margins.",
    causeBn: "সারকোস্পোরা ক্যাপসিকি (Cercospora capsici) ছত্রাক। আর্দ্র পরিবেশ ও ঘন গাছপালায় এটি দ্রুত ছড়ায়।",
    causeEn: "Fungal pathogen Cercospora capsici, prevalent during warm humid seasons with persistent leaf wetness.",
    solutionBn: "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।",
    solutionEn: "Spray Carbendazim 50 WP (1 g/L) or Chlorothalonil 75 WP (2 g/L). Provide adequate plant spacing to facilitate ventilation.",
  },
  chilli__healthy_leaf: {
    nameBn: "সুস্থ মরিচ পাতা (Healthy)",
    nameEn: "Healthy Chilli Leaf",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    descBn: "মসৃণ ও চকচকে গাঢ় সবুজ পাতা, কোনো কোঁকড়ানো বা দাগের উপসর্গ নেই।",
    descEn: "Glossy, uniform emerald-green leaves exhibiting balanced venation and firm lamina without curling or spotting.",
    causeBn: "সুষম সার, নিয়ন্ত্রিত আর্দ্রতা ও পোকা-মাকড়মুক্ত পরিবেশ।",
    causeEn: "Consistent moisture, adequate micronutrient availability, and absence of insect vector pressure.",
    solutionBn: "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।",
    solutionEn: "Maintain well-drained raised bed soil conditions. Continue visual scouting for sucking pests.",
  },

  // --- BRASSICA (বাঁধাকপি ও ফুলকপি) ---
  brassica__alternaria_spot: {
    nameBn: "বাঁধাকপির অল্টারনারিয়া গোল দাগ রোগ (Alternaria)",
    nameEn: "Cabbage Alternaria Leaf Spot",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    descBn: "পাতায় গাঢ় বাদামী থেকে কালো রঙের গোলাকার বলয়াকৃতি দাগ দেখা যায়, যা শুকিয়ে পাতার ভেতর ফুটো করে দেয়।",
    descEn: "Circular zonate dark brown to black spots with concentric rings, often developing a characteristic 'shot-hole' effect as dry centers fall out.",
    causeBn: "অল্টারনারিয়া ব্রাসিকি (Alternaria brassicae) ছত্রাক। কুয়াশাচ্ছন্ন দিন এবং ঘন শিশিরে এ রোগ ব্যাপক আকার ধারণ করে।",
    causeEn: "Caused by Alternaria brassicae / Alternaria brassicicola, favored by prolonged leaf wetness (cool temperatures 15–22°C).",
    solutionBn: "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।",
    solutionEn: "Spray Mancozeb 75 WP (2 g/L) or Iprodione 50 WP (Rovral). Always mix an agricultural sticker/spreader for waxy brassica foliage.",
  },
  brassica__cauliflower_alternaria: {
    nameBn: "ফুলকপির অল্টারনারিয়া রোগ (Cauliflower Alternaria)",
    nameEn: "Cauliflower Alternaria Disease",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    descBn: "পাতায় বাদামী রিং দাগ এবং ফুলকপির মাথায় বাদামী বা কালো দাগ পড়ে পণ্যের মান নষ্ট করে।",
    descEn: "Target-ring brown lesions on leaves; also causes dark sunken browning on the cauliflower curd, drastically reducing market value.",
    causeBn: "অল্টারনারিয়া ছত্রাকের আক্রমণ। অপরিচ্ছন্ন জমি ও আর্দ্র আবহাওয়ায় বিস্তার লাভ করে।",
    causeEn: "Caused by Alternaria species infecting both foliage and curd during wet, humid weather stages.",
    solutionBn: "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।",
    solutionEn: "Prune and dispose of infected leaves. Apply Difenoconazole 250 EC (Score, 0.5 ml/L) or Azoxystrobin + Difenoconazole.",
  },
  brassica__healthy: {
    nameBn: "সুস্থ ফুলকপি পাতা (Healthy)",
    nameEn: "Healthy Cauliflower Leaf",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    descBn: "মোমের মতো চকচকে অক্ষত পাতা, স্বাস্থ্যবান বর্ধনশীল কুঁড়ি ও চমৎকার গঠন।",
    descEn: "Robust waxy bloom on glaucous green leaves, structurally intact with zero necrotic spots or marginal rotting.",
    causeBn: "সঠিক জমি তৈরি, বোরণ ও মলিবডেনাম পুষ্টি এবং নিয়ন্ত্রিত সেচ।",
    causeEn: "Optimal soil boron and molybdenum levels, healthy seedling transplanting, and sound pest exclusion.",
    solutionBn: "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।",
    solutionEn: "Keep soil evenly moist without waterlogging the root zone. Continue regular weed and fertility management.",
  },
};

export function getLocalizedDisease(
  key: string | null | undefined,
  locale: "bn" | "en"
): LocalizedDiseaseKnowledge | null {
  if (!key) return null;
  const normalized = key.toLowerCase().trim().replace(/[\s-]+/g, "_");
  
  if (DISEASE_KNOWLEDGE_MAP[normalized]) {
    return DISEASE_KNOWLEDGE_MAP[normalized];
  }
  
  for (const [k, v] of Object.entries(DISEASE_KNOWLEDGE_MAP)) {
    if (normalized.includes(k) || k.includes(normalized)) {
      return v;
    }
  }
  return null;
}
