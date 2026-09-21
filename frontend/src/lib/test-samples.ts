import type { DetectResponse } from "@/lib/api";

export interface TestSampleInstance {
  id: string;
  crop: "Rice" | "Potato" | "Wheat" | "Corn" | "Chilli" | "Brassica";
  cropBn: string;
  cropEn: string;
  disease: string;
  diseaseBn: string;
  diseaseEn: string;
  targetClass: string;
  confidence: number;
  imageSrc: string;
  cropHint: string;
  cachedResult: DetectResponse;
}

export const CROP_GROUPS: {
  crop: TestSampleInstance["crop"];
  cropBn: string;
  cropEn: string;
  icon: string;
  count: number;
}[] = [
  { crop: "Rice", cropBn: "ধান", cropEn: "Rice", icon: "🌾", count: 20 },
  { crop: "Potato", cropBn: "আলু", cropEn: "Potato", icon: "🥔", count: 16 },
  { crop: "Wheat", cropBn: "গম", cropEn: "Wheat", icon: "🌿", count: 16 },
  { crop: "Corn", cropBn: "ভুট্টা", cropEn: "Corn", icon: "🌽", count: 16 },
  { crop: "Chilli", cropBn: "মরিচ", cropEn: "Chilli", icon: "🌶️", count: 16 },
  { crop: "Brassica", cropBn: "কপি ও ব্রাসিকা", cropEn: "Cabbage & Cauliflower (Brassica)", icon: "🥦", count: 16 },
];

export const VERIFIED_TEST_SAMPLES: TestSampleInstance[] = [
  {
    id: "rice_brown_spot_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Brown_Spot",
    diseaseBn: "বাদামী দাগ (Brown Spot)",
    diseaseEn: "Brown Spot",
    targetClass: "Rice__Brown_Spot",
    confidence: 99.8,
    imageSrc: "/samples/rice/rice_brown_spot_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Brown_Spot",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের বাদামী দাগ রোগ (Brown Spot)",
            "description_bn": "পাতায় ডিম্বাকৃতি বা গোলাকার তিল তিল বাদামী দাগ দেখা যায়, যার কেন্দ্র ধূসর বা হালকা বাদামী হয়।",
            "cause_bn": "হেলমিন্থোস্পোরিয়াম ওরাইজি (Bipolaris oryzae) ছত্রাকের আক্রমণে ও মাটিতে পটাশ বা পুষ্টির ঘাটতি থাকলে এ রোগ বাড়ে।",
            "solution_bn": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Brown_Spot",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_brown_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "বাদামী দাগ (Brown Spot) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_brown_spot_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Brown_Spot",
    diseaseBn: "বাদামী দাগ (Brown Spot)",
    diseaseEn: "Brown Spot",
    targetClass: "Rice__Brown_Spot",
    confidence: 99.8,
    imageSrc: "/samples/rice/rice_brown_spot_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Brown_Spot",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের বাদামী দাগ রোগ (Brown Spot)",
            "description_bn": "পাতায় ডিম্বাকৃতি বা গোলাকার তিল তিল বাদামী দাগ দেখা যায়, যার কেন্দ্র ধূসর বা হালকা বাদামী হয়।",
            "cause_bn": "হেলমিন্থোস্পোরিয়াম ওরাইজি (Bipolaris oryzae) ছত্রাকের আক্রমণে ও মাটিতে পটাশ বা পুষ্টির ঘাটতি থাকলে এ রোগ বাড়ে।",
            "solution_bn": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Brown_Spot",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_brown_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "বাদামী দাগ (Brown Spot) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_brown_spot_03",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Brown_Spot",
    diseaseBn: "বাদামী দাগ (Brown Spot)",
    diseaseEn: "Brown Spot",
    targetClass: "Rice__Brown_Spot",
    confidence: 99.8,
    imageSrc: "/samples/rice/rice_brown_spot_03.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Brown_Spot",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের বাদামী দাগ রোগ (Brown Spot)",
            "description_bn": "পাতায় ডিম্বাকৃতি বা গোলাকার তিল তিল বাদামী দাগ দেখা যায়, যার কেন্দ্র ধূসর বা হালকা বাদামী হয়।",
            "cause_bn": "হেলমিন্থোস্পোরিয়াম ওরাইজি (Bipolaris oryzae) ছত্রাকের আক্রমণে ও মাটিতে পটাশ বা পুষ্টির ঘাটতি থাকলে এ রোগ বাড়ে।",
            "solution_bn": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Brown_Spot",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "সুষম সার ব্যবহার করুন (ইউরিয়া কমিয়ে পটাশ ও দস্তা সার দিন)। আক্রান্ত জমিতে কার্বেন্ডাজিম বা প্রোপিকোনাজল গ্রুপের ছত্রাকনাশক স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_brown_spot_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "বাদামী দাগ (Brown Spot) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_leaf_blast_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Leaf_Blast",
    diseaseBn: "ব্লাস্ট রোগ (Leaf Blast)",
    diseaseEn: "Leaf Blast",
    targetClass: "Rice__Leaf_Blast",
    confidence: 100.0,
    imageSrc: "/samples/rice/rice_leaf_blast_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
            "description_bn": "পাতায় দুই প্রান্ত সুচালো চোখের মতো বা মাকু আকৃতির দাগ দেখা যায়, যা দ্রুত ছড়িয়ে পাতা ঝলসে দেয়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি (Magnaporthe oryzae) ছত্রাক। অতিরিক্ত ইউরিয়া সার এবং দীর্ঘস্থায়ী কুয়াশা বা মেঘলা আবহাওয়া এর প্রধান কারণ।",
            "solution_bn": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_leaf_blast_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্লাস্ট রোগ (Leaf Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_leaf_blast_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Leaf_Blast",
    diseaseBn: "ব্লাস্ট রোগ (Leaf Blast)",
    diseaseEn: "Leaf Blast",
    targetClass: "Rice__Leaf_Blast",
    confidence: 100.0,
    imageSrc: "/samples/rice/rice_leaf_blast_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
            "description_bn": "পাতায় দুই প্রান্ত সুচালো চোখের মতো বা মাকু আকৃতির দাগ দেখা যায়, যা দ্রুত ছড়িয়ে পাতা ঝলসে দেয়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি (Magnaporthe oryzae) ছত্রাক। অতিরিক্ত ইউরিয়া সার এবং দীর্ঘস্থায়ী কুয়াশা বা মেঘলা আবহাওয়া এর প্রধান কারণ।",
            "solution_bn": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_leaf_blast_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্লাস্ট রোগ (Leaf Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_leaf_blast_03",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Leaf_Blast",
    diseaseBn: "ব্লাস্ট রোগ (Leaf Blast)",
    diseaseEn: "Leaf Blast",
    targetClass: "Rice__Leaf_Blast",
    confidence: 100.0,
    imageSrc: "/samples/rice/rice_leaf_blast_03.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পাতা ব্লাস্ট রোগ (Leaf Blast)",
            "description_bn": "পাতায় দুই প্রান্ত সুচালো চোখের মতো বা মাকু আকৃতির দাগ দেখা যায়, যা দ্রুত ছড়িয়ে পাতা ঝলসে দেয়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি (Magnaporthe oryzae) ছত্রাক। অতিরিক্ত ইউরিয়া সার এবং দীর্ঘস্থায়ী কুয়াশা বা মেঘলা আবহাওয়া এর প্রধান কারণ।",
            "solution_bn": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "জমি থেকে অতিরিক্ত পানি নিষ্কাশন করুন এবং ইউরিয়ার উপরিপ্রয়োগ বন্ধ রাখুন। ট্রাইসাইক্লাজল ৭৫ ডব্লিউপি (প্রতি লিটারে ০.৭৫ গ্রাম) বা কাসুগামাইসিন স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_leaf_blast_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্লাস্ট রোগ (Leaf Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_bacterial_leaf_blight_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Bacterial_Leaf_Blight",
    diseaseBn: "ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
    diseaseEn: "Bacterial Leaf Blight",
    targetClass: "Rice__Bacterial_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/rice/rice_bacterial_leaf_blight_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Bacterial_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
            "description_bn": "পাতার ডগা বা কিনারা বরাবর ঢেউ খেলানো পানির দাগ তৈরি হয়, যা শুকিয়ে বাদামী বা খড়ের মতো পুড়ে যায়।",
            "cause_bn": "জ্যান্থোমোনাস ওরাইজি (Xanthomonas oryzae pv. oryzae) ব্যাকটেরিয়া। ঝড়ো বাতাস, অতিরিক্ত বৃষ্টি এবং জলাবদ্ধতায় দ্রুত ছড়ায়।",
            "solution_bn": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Bacterial_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_bacterial_leaf_blight_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্যাকটেরিয়াল পাতা পোড়া (Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_bacterial_leaf_blight_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Bacterial_Leaf_Blight",
    diseaseBn: "ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
    diseaseEn: "Bacterial Leaf Blight",
    targetClass: "Rice__Bacterial_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/rice/rice_bacterial_leaf_blight_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Bacterial_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
            "description_bn": "পাতার ডগা বা কিনারা বরাবর ঢেউ খেলানো পানির দাগ তৈরি হয়, যা শুকিয়ে বাদামী বা খড়ের মতো পুড়ে যায়।",
            "cause_bn": "জ্যান্থোমোনাস ওরাইজি (Xanthomonas oryzae pv. oryzae) ব্যাকটেরিয়া। ঝড়ো বাতাস, অতিরিক্ত বৃষ্টি এবং জলাবদ্ধতায় দ্রুত ছড়ায়।",
            "solution_bn": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Bacterial_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_bacterial_leaf_blight_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্যাকটেরিয়াল পাতা পোড়া (Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_bacterial_leaf_blight_03",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Bacterial_Leaf_Blight",
    diseaseBn: "ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
    diseaseEn: "Bacterial Leaf Blight",
    targetClass: "Rice__Bacterial_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/rice/rice_bacterial_leaf_blight_03.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Bacterial_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের ব্যাকটেরিয়াল পাতা পোড়া (Blight)",
            "description_bn": "পাতার ডগা বা কিনারা বরাবর ঢেউ খেলানো পানির দাগ তৈরি হয়, যা শুকিয়ে বাদামী বা খড়ের মতো পুড়ে যায়।",
            "cause_bn": "জ্যান্থোমোনাস ওরাইজি (Xanthomonas oryzae pv. oryzae) ব্যাকটেরিয়া। ঝড়ো বাতাস, অতিরিক্ত বৃষ্টি এবং জলাবদ্ধতায় দ্রুত ছড়ায়।",
            "solution_bn": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Bacterial_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ইউরিয়া প্রয়োগ স্থগিত রাখুন এবং পটাশ সার বাড়িয়ে দিন। কপার অক্সিক্লোরাইড বা ব্রোমোপোল (যেমন: ব্যক্ট্রোট্রন) সঠিক মাত্রায় স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_bacterial_leaf_blight_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্যাকটেরিয়াল পাতা পোড়া (Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_sheath_blight_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Sheath_Blight",
    diseaseBn: "খোল পোড়া রোগ (Sheath Blight)",
    diseaseEn: "Sheath Blight",
    targetClass: "Rice__Sheath_Blight",
    confidence: 99.7,
    imageSrc: "/samples/rice/rice_sheath_blight_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Sheath_Blight",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের খোল পোড়া রোগ (Sheath Blight)",
            "description_bn": "গাছের গোড়ার খোলে পানির মতো ভেজা সবুজাভ-ধূসর ডিম্বাকৃতি দাগ হয়, যা ক্রমশ বাদামী হয়ে ওপরের দিকে ছড়ায়।",
            "cause_bn": "রাইজোকটোনিয়া সোলানি (Rhizoctonia solani) ছত্রাক। ঘন চারা রোপণ ও অতিরিক্ত ইউরিয়া ব্যবহার।",
            "solution_bn": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Sheath_Blight",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_sheath_blight_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "খোল পোড়া রোগ (Sheath Blight) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_sheath_blight_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Sheath_Blight",
    diseaseBn: "খোল পোড়া রোগ (Sheath Blight)",
    diseaseEn: "Sheath Blight",
    targetClass: "Rice__Sheath_Blight",
    confidence: 99.7,
    imageSrc: "/samples/rice/rice_sheath_blight_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Sheath_Blight",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের খোল পোড়া রোগ (Sheath Blight)",
            "description_bn": "গাছের গোড়ার খোলে পানির মতো ভেজা সবুজাভ-ধূসর ডিম্বাকৃতি দাগ হয়, যা ক্রমশ বাদামী হয়ে ওপরের দিকে ছড়ায়।",
            "cause_bn": "রাইজোকটোনিয়া সোলানি (Rhizoctonia solani) ছত্রাক। ঘন চারা রোপণ ও অতিরিক্ত ইউরিয়া ব্যবহার।",
            "solution_bn": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Sheath_Blight",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_sheath_blight_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "খোল পোড়া রোগ (Sheath Blight) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_sheath_blight_03",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Sheath_Blight",
    diseaseBn: "খোল পোড়া রোগ (Sheath Blight)",
    diseaseEn: "Sheath Blight",
    targetClass: "Rice__Sheath_Blight",
    confidence: 99.7,
    imageSrc: "/samples/rice/rice_sheath_blight_03.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Sheath_Blight",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের খোল পোড়া রোগ (Sheath Blight)",
            "description_bn": "গাছের গোড়ার খোলে পানির মতো ভেজা সবুজাভ-ধূসর ডিম্বাকৃতি দাগ হয়, যা ক্রমশ বাদামী হয়ে ওপরের দিকে ছড়ায়।",
            "cause_bn": "রাইজোকটোনিয়া সোলানি (Rhizoctonia solani) ছত্রাক। ঘন চারা রোপণ ও অতিরিক্ত ইউরিয়া ব্যবহার।",
            "solution_bn": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Sheath_Blight",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "ইউরিয়ার মাত্রা কমান এবং পটাশ সার প্রয়োগ করুন। আক্রমণ দেখা দিলে হেক্সাকোনাজল ৫ ইসি বা ভ্যালিডামাইসিন ৩ এল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_sheath_blight_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "খোল পোড়া রোগ (Sheath Blight) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_leaf_scald_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Leaf_Scald",
    diseaseBn: "পাতা ঝলসানো (Leaf Scald)",
    diseaseEn: "Leaf Scald",
    targetClass: "Rice__Leaf_Scald",
    confidence: 99.5,
    imageSrc: "/samples/rice/rice_leaf_scald_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Scald",
      "disease_confidence": 0.995,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পাতা ঝলসানো রোগ (Leaf Scald)",
            "description_bn": "পাতার ডগা বা কিনারা থেকে শুরু করে হালকা ও গাঢ় বাদামী বলয়াকৃতির তরঙ্গের মতো ঝলসানো দাগ দেখা যায়।",
            "cause_bn": "মাইক্রোডোকিয়াম ওরাইজি (Microdochium oryzae) ছত্রাক। স্যাঁতসেঁতে ভেজা আবহাওয়া।",
            "solution_bn": "সুষম সার প্রয়োগ করুন। প্রতিরোধে কার্বেন্ডাজিম বা ট্রাইসাইক্লাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Scald",
                  "confidence": 0.995
            }
      ],
      "treatment_advice": "সুষম সার প্রয়োগ করুন। প্রতিরোধে কার্বেন্ডাজিম বা ট্রাইসাইক্লাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_leaf_scald_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতা ঝলসানো (Leaf Scald) [99.5%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_leaf_scald_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Leaf_Scald",
    diseaseBn: "পাতা ঝলসানো (Leaf Scald)",
    diseaseEn: "Leaf Scald",
    targetClass: "Rice__Leaf_Scald",
    confidence: 99.5,
    imageSrc: "/samples/rice/rice_leaf_scald_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Scald",
      "disease_confidence": 0.995,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পাতা ঝলসানো রোগ (Leaf Scald)",
            "description_bn": "পাতার ডগা বা কিনারা থেকে শুরু করে হালকা ও গাঢ় বাদামী বলয়াকৃতির তরঙ্গের মতো ঝলসানো দাগ দেখা যায়।",
            "cause_bn": "মাইক্রোডোকিয়াম ওরাইজি (Microdochium oryzae) ছত্রাক। স্যাঁতসেঁতে ভেজা আবহাওয়া।",
            "solution_bn": "সুষম সার প্রয়োগ করুন। প্রতিরোধে কার্বেন্ডাজিম বা ট্রাইসাইক্লাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Scald",
                  "confidence": 0.995
            }
      ],
      "treatment_advice": "সুষম সার প্রয়োগ করুন। প্রতিরোধে কার্বেন্ডাজিম বা ট্রাইসাইক্লাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_leaf_scald_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতা ঝলসানো (Leaf Scald) [99.5%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_narrow_brown_leaf_spot_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Narrow_Brown_Leaf_Spot",
    diseaseBn: "সরু বাদামী দাগ (Narrow Brown Spot)",
    diseaseEn: "Narrow Brown Leaf Spot",
    targetClass: "Rice__Narrow_Brown_Leaf_Spot",
    confidence: 99.4,
    imageSrc: "/samples/rice/rice_narrow_brown_leaf_spot_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Narrow_Brown_Leaf_Spot",
      "disease_confidence": 0.9940000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের সরু বাদামী দাগ রোগ (Narrow Brown Leaf Spot)",
            "description_bn": "পাতার শিরার সমান্তরালে ছোট ও লম্বাটে সুঁচালো গাঢ় লালচে-বাদামী রেখা দাগ দেখা যায়।",
            "cause_bn": "সারকোস্পোরা ওরাইজি (Cercospora oryzae) ছত্রাক। ফসলের শেষ পর্যায়ে পুষ্টির অভাবে এটি বাড়ে।",
            "solution_bn": "মাটিতে পর্যাপ্ত পটাশ নিশ্চিত করুন। রোগ দেখা দিলে প্রোপিকোনাজল বা ডাইফেনোকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Narrow_Brown_Leaf_Spot",
                  "confidence": 0.9940000000000001
            }
      ],
      "treatment_advice": "মাটিতে পর্যাপ্ত পটাশ নিশ্চিত করুন। রোগ দেখা দিলে প্রোপিকোনাজল বা ডাইফেনোকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_narrow_brown_leaf_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সরু বাদামী দাগ (Narrow Brown Spot) [99.4%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_narrow_brown_leaf_spot_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Narrow_Brown_Leaf_Spot",
    diseaseBn: "সরু বাদামী দাগ (Narrow Brown Spot)",
    diseaseEn: "Narrow Brown Leaf Spot",
    targetClass: "Rice__Narrow_Brown_Leaf_Spot",
    confidence: 99.4,
    imageSrc: "/samples/rice/rice_narrow_brown_leaf_spot_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Narrow_Brown_Leaf_Spot",
      "disease_confidence": 0.9940000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের সরু বাদামী দাগ রোগ (Narrow Brown Leaf Spot)",
            "description_bn": "পাতার শিরার সমান্তরালে ছোট ও লম্বাটে সুঁচালো গাঢ় লালচে-বাদামী রেখা দাগ দেখা যায়।",
            "cause_bn": "সারকোস্পোরা ওরাইজি (Cercospora oryzae) ছত্রাক। ফসলের শেষ পর্যায়ে পুষ্টির অভাবে এটি বাড়ে।",
            "solution_bn": "মাটিতে পর্যাপ্ত পটাশ নিশ্চিত করুন। রোগ দেখা দিলে প্রোপিকোনাজল বা ডাইফেনোকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Narrow_Brown_Leaf_Spot",
                  "confidence": 0.9940000000000001
            }
      ],
      "treatment_advice": "মাটিতে পর্যাপ্ত পটাশ নিশ্চিত করুন। রোগ দেখা দিলে প্রোপিকোনাজল বা ডাইফেনোকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_narrow_brown_leaf_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সরু বাদামী দাগ (Narrow Brown Spot) [99.4%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_rice_hispa_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Rice_Hispa",
    diseaseBn: "মাজরা / পামরী পোকার ক্ষত (Rice Hispa)",
    diseaseEn: "Rice Hispa Feeding Scars",
    targetClass: "Rice__Rice_Hispa",
    confidence: 99.6,
    imageSrc: "/samples/rice/rice_rice_hispa_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Rice_Hispa",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পামরী পোকা / ক্ষত (Rice Hispa Damage)",
            "description_bn": "পাতার ওপর সমান্তরাল সাদাটে দাগ বা আঁচড়ের মতো রেখা পড়ে, শুকিয়ে পাতা ঝলসে খড়ের মতো দেখায়।",
            "cause_bn": "পামরী পোকা (Dicladispa armigera)। পূর্ণাঙ্গ পোকা পাতার সবুজ অংশ খায় ও কীড়া পাতার স্তরে সুড়ঙ্গ কাটে।",
            "solution_bn": "আক্রান্ত পাতার ডগা কেটে নষ্ট করুন এবং হাতজাল দিয়ে পোকা ধরুন। আক্রমণ তীব্র হলে ক্লোরপাইরিফস বা সাইপারমেথ্রিন স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Rice_Hispa",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "আক্রান্ত পাতার ডগা কেটে নষ্ট করুন এবং হাতজাল দিয়ে পোকা ধরুন। আক্রমণ তীব্র হলে ক্লোরপাইরিফস বা সাইপারমেথ্রিন স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_rice_hispa_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "মাজরা / পামরী পোকার ক্ষত (Rice Hispa) [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_rice_hispa_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Rice_Hispa",
    diseaseBn: "মাজরা / পামরী পোকার ক্ষত (Rice Hispa)",
    diseaseEn: "Rice Hispa Feeding Scars",
    targetClass: "Rice__Rice_Hispa",
    confidence: 99.6,
    imageSrc: "/samples/rice/rice_rice_hispa_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Rice_Hispa",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "ধানের পামরী পোকা / ক্ষত (Rice Hispa Damage)",
            "description_bn": "পাতার ওপর সমান্তরাল সাদাটে দাগ বা আঁচড়ের মতো রেখা পড়ে, শুকিয়ে পাতা ঝলসে খড়ের মতো দেখায়।",
            "cause_bn": "পামরী পোকা (Dicladispa armigera)। পূর্ণাঙ্গ পোকা পাতার সবুজ অংশ খায় ও কীড়া পাতার স্তরে সুড়ঙ্গ কাটে।",
            "solution_bn": "আক্রান্ত পাতার ডগা কেটে নষ্ট করুন এবং হাতজাল দিয়ে পোকা ধরুন। আক্রমণ তীব্র হলে ক্লোরপাইরিফস বা সাইপারমেথ্রিন স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Rice_Hispa",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "আক্রান্ত পাতার ডগা কেটে নষ্ট করুন এবং হাতজাল দিয়ে পোকা ধরুন। আক্রমণ তীব্র হলে ক্লোরপাইরিফস বা সাইপারমেথ্রিন স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_rice_hispa_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "মাজরা / পামরী পোকার ক্ষত (Rice Hispa) [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_healthy_leaf_01",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ ও নীরোগ পাতা (Healthy)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Rice__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/rice/rice_healthy_leaf_01.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ও নীরোগ ধান পাতা (Healthy)",
            "description_bn": "পাতার রঙ উজ্জ্বল সবুজ ও সম্পূর্ণ ক্ষতহীন। কোনো ছত্রাক বা ব্যাকটেরিয়ার লক্ষণ নেই।",
            "cause_bn": "যথাযথ সেচ, সঠিক সুষম সার ও অনুকূল আবহাওয়া।",
            "solution_bn": "বর্তমান সেচ ও পরিচর্যা বজায় রাখুন। কোনো রাসায়নিক বালাইনাশকের প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "বর্তমান সেচ ও পরিচর্যা বজায় রাখুন। কোনো রাসায়নিক বালাইনাশকের প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_healthy_leaf_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ও নীরোগ পাতা (Healthy) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "rice_healthy_leaf_02",
    crop: "Rice",
    cropBn: "ধান",
    cropEn: "Rice",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ ও নীরোগ পাতা (Healthy)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Rice__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/rice/rice_healthy_leaf_02.jpg",
    cropHint: "Rice",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Rice",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ও নীরোগ ধান পাতা (Healthy)",
            "description_bn": "পাতার রঙ উজ্জ্বল সবুজ ও সম্পূর্ণ ক্ষতহীন। কোনো ছত্রাক বা ব্যাকটেরিয়ার লক্ষণ নেই।",
            "cause_bn": "যথাযথ সেচ, সঠিক সুষম সার ও অনুকূল আবহাওয়া।",
            "solution_bn": "বর্তমান সেচ ও পরিচর্যা বজায় রাখুন। কোনো রাসায়নিক বালাইনাশকের প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Rice",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "বর্তমান সেচ ও পরিচর্যা বজায় রাখুন। কোনো রাসায়নিক বালাইনাশকের প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: rice_healthy_leaf_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ধান (Rice)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ও নীরোগ পাতা (Healthy) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_early_blight_01",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Early_Blight",
    diseaseBn: "আগাম ধসা (Early Blight)",
    diseaseEn: "Early Blight",
    targetClass: "Potato__Early_Blight",
    confidence: 99.9,
    imageSrc: "/samples/potato/potato_early_blight_01.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Early_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
            "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
            "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
            "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Early_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_early_blight_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "আগাম ধসা (Early Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_early_blight_02",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Early_Blight",
    diseaseBn: "আগাম ধসা (Early Blight)",
    diseaseEn: "Early Blight",
    targetClass: "Potato__Early_Blight",
    confidence: 99.9,
    imageSrc: "/samples/potato/potato_early_blight_02.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Early_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
            "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
            "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
            "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Early_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_early_blight_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "আগাম ধসা (Early Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_early_blight_03",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Early_Blight",
    diseaseBn: "আগাম ধসা (Early Blight)",
    diseaseEn: "Early Blight",
    targetClass: "Potato__Early_Blight",
    confidence: 99.9,
    imageSrc: "/samples/potato/potato_early_blight_03.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Early_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
            "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
            "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
            "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Early_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_early_blight_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "আগাম ধসা (Early Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_early_blight_04",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Early_Blight",
    diseaseBn: "আগাম ধসা (Early Blight)",
    diseaseEn: "Early Blight",
    targetClass: "Potato__Early_Blight",
    confidence: 99.9,
    imageSrc: "/samples/potato/potato_early_blight_04.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Early_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
            "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
            "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
            "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Early_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_early_blight_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "আগাম ধসা (Early Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_early_blight_05",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Early_Blight",
    diseaseBn: "আগাম ধসা (Early Blight)",
    diseaseEn: "Early Blight",
    targetClass: "Potato__Early_Blight",
    confidence: 99.9,
    imageSrc: "/samples/potato/potato_early_blight_05.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Early_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
            "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
            "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
            "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Early_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_early_blight_05 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "আগাম ধসা (Early Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_early_blight_06",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Early_Blight",
    diseaseBn: "আগাম ধসা (Early Blight)",
    diseaseEn: "Early Blight",
    targetClass: "Potato__Early_Blight",
    confidence: 99.9,
    imageSrc: "/samples/potato/potato_early_blight_06.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Early_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর আগাম ধসা রোগ (Early Blight)",
            "description_bn": "পাতায় বলয়াকৃতি (কনসেন্ট্রিক রিং) বাদামী রঙের টার্গেট বোর্ডের মতো দাগ দেখা যায়।",
            "cause_bn": "অল্টারনারিয়া সোলানি (Alternaria solani) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়া এবং ফসলের পুষ্টিহীনতায় রোগ বাড়ে।",
            "solution_bn": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Early_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "ম্যানকোজেব (ডাইথেন এম-৪৫) প্রতি লিটার পানিতে ২ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। গাছের নিচের আক্রান্ত পাতা সরিয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_early_blight_06 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "আগাম ধসা (Early Blight) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_late_blight_01",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Late_Blight",
    diseaseBn: "নাবি ধসা (Late Blight)",
    diseaseEn: "Late Blight",
    targetClass: "Potato__Late_Blight",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_late_blight_01.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Late_Blight",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
            "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
            "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
            "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Late_Blight",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_late_blight_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "নাবি ধসা (Late Blight) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_late_blight_02",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Late_Blight",
    diseaseBn: "নাবি ধসা (Late Blight)",
    diseaseEn: "Late Blight",
    targetClass: "Potato__Late_Blight",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_late_blight_02.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Late_Blight",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
            "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
            "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
            "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Late_Blight",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_late_blight_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "নাবি ধসা (Late Blight) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_late_blight_03",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Late_Blight",
    diseaseBn: "নাবি ধসা (Late Blight)",
    diseaseEn: "Late Blight",
    targetClass: "Potato__Late_Blight",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_late_blight_03.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Late_Blight",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
            "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
            "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
            "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Late_Blight",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_late_blight_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "নাবি ধসা (Late Blight) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_late_blight_04",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Late_Blight",
    diseaseBn: "নাবি ধসা (Late Blight)",
    diseaseEn: "Late Blight",
    targetClass: "Potato__Late_Blight",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_late_blight_04.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Late_Blight",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
            "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
            "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
            "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Late_Blight",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_late_blight_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "নাবি ধসা (Late Blight) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_late_blight_05",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Late_Blight",
    diseaseBn: "নাবি ধসা (Late Blight)",
    diseaseEn: "Late Blight",
    targetClass: "Potato__Late_Blight",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_late_blight_05.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Late_Blight",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
            "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
            "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
            "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Late_Blight",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_late_blight_05 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "নাবি ধসা (Late Blight) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_late_blight_06",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Late_Blight",
    diseaseBn: "নাবি ধসা (Late Blight)",
    diseaseEn: "Late Blight",
    targetClass: "Potato__Late_Blight",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_late_blight_06.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Late_Blight",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "আলুর নাবি ধসা / মড়ক রোগ (Late Blight)",
            "description_bn": "পাতার কিনারে পানি ভেজা কালচে দাগ তৈরি হয় এবং পাতার উল্টো পিঠে ভেজা আবহাওয়াতে সাদা তুলার মতো ছত্রাক দেখা যায়।",
            "cause_bn": "ফাইটোফথোরা ইনফেস্ট্যান্স (Phytophthora infestans) ছত্রাক সদৃশ জীবাণু। কুয়াশাচ্ছন্ন ভেজা ঠাণ্ডা আবহাওয়ায় এটি দ্রুত মহামারি রূপ নেয়।",
            "solution_bn": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Late_Blight",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আবহাওয়া মেঘলা হলেই আগাম প্রতিরোধক হিসেবে ম্যানকোজেব স্প্রে করুন। আক্রমণ ঘটলে সিমোক্সানিল+ম্যানকোজেব (সেকটিন) বা মেটালেক্সিল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_late_blight_06 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "নাবি ধসা (Late Blight) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_healthy_leaf_01",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Potato__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_healthy_leaf_01.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ আলু পাতা (Healthy)",
            "description_bn": "পাতায় কোনো দাগ বা ধসার চিহ্ন নেই। স্বাভাবিক আকৃতি ও স্বাস্থ্যবান সবুজ রঙ বিদ্যমান।",
            "cause_bn": "সুস্থ বীজ ও সঠিক রোগমুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_healthy_leaf_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_healthy_leaf_02",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Potato__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_healthy_leaf_02.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ আলু পাতা (Healthy)",
            "description_bn": "পাতায় কোনো দাগ বা ধসার চিহ্ন নেই। স্বাভাবিক আকৃতি ও স্বাস্থ্যবান সবুজ রঙ বিদ্যমান।",
            "cause_bn": "সুস্থ বীজ ও সঠিক রোগমুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_healthy_leaf_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_healthy_leaf_03",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Potato__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_healthy_leaf_03.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ আলু পাতা (Healthy)",
            "description_bn": "পাতায় কোনো দাগ বা ধসার চিহ্ন নেই। স্বাভাবিক আকৃতি ও স্বাস্থ্যবান সবুজ রঙ বিদ্যমান।",
            "cause_bn": "সুস্থ বীজ ও সঠিক রোগমুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_healthy_leaf_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "potato_healthy_leaf_04",
    crop: "Potato",
    cropBn: "আলু",
    cropEn: "Potato",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Potato__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/potato/potato_healthy_leaf_04.jpg",
    cropHint: "Potato",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Potato",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ আলু পাতা (Healthy)",
            "description_bn": "পাতায় কোনো দাগ বা ধসার চিহ্ন নেই। স্বাভাবিক আকৃতি ও স্বাস্থ্যবান সবুজ রঙ বিদ্যমান।",
            "cause_bn": "সুস্থ বীজ ও সঠিক রোগমুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।"
      },
      "top3_crops": [
            {
                  "class": "Potato",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত পরিমিত সেচ দিন। কুয়াশাচ্ছন্ন আবহাওয়া দেখা দিলে সতর্কতামূলক ছাই বা জৈব ছত্রাকনাশক ব্যবহার করতে পারেন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: potato_healthy_leaf_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "আলু (Potato)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_leaf_rust_01",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Leaf_Rust",
    diseaseBn: "পাতার মরিচা রোগ (Leaf Rust)",
    diseaseEn: "Leaf Rust",
    targetClass: "Leaf Rust",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_leaf_rust_01.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাতার মরিচা রোগ (Leaf Rust)",
            "description_bn": "পাতার উপর ছোট ছোট কমলা-বাদামী বা মরিচার মতো পাউডারের গুটি দেখা যায়। হাত দিলে আঙুলে মরিচার গুঁড়া লাগে।",
            "cause_bn": "পাকসিনিয়া ট্রাইটিচিনা (Puccinia triticina) ছত্রাক। উষ্ণ দিন (১৫–২২°C) ও আর্দ্র রাত এ রোগের অনুকূল।",
            "solution_bn": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_leaf_rust_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতার মরিচা রোগ (Leaf Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_leaf_rust_02",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Leaf_Rust",
    diseaseBn: "পাতার মরিচা রোগ (Leaf Rust)",
    diseaseEn: "Leaf Rust",
    targetClass: "Leaf Rust",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_leaf_rust_02.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাতার মরিচা রোগ (Leaf Rust)",
            "description_bn": "পাতার উপর ছোট ছোট কমলা-বাদামী বা মরিচার মতো পাউডারের গুটি দেখা যায়। হাত দিলে আঙুলে মরিচার গুঁড়া লাগে।",
            "cause_bn": "পাকসিনিয়া ট্রাইটিচিনা (Puccinia triticina) ছত্রাক। উষ্ণ দিন (১৫–২২°C) ও আর্দ্র রাত এ রোগের অনুকূল।",
            "solution_bn": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_leaf_rust_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতার মরিচা রোগ (Leaf Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_leaf_rust_03",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Leaf_Rust",
    diseaseBn: "পাতার মরিচা রোগ (Leaf Rust)",
    diseaseEn: "Leaf Rust",
    targetClass: "Leaf Rust",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_leaf_rust_03.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাতার মরিচা রোগ (Leaf Rust)",
            "description_bn": "পাতার উপর ছোট ছোট কমলা-বাদামী বা মরিচার মতো পাউডারের গুটি দেখা যায়। হাত দিলে আঙুলে মরিচার গুঁড়া লাগে।",
            "cause_bn": "পাকসিনিয়া ট্রাইটিচিনা (Puccinia triticina) ছত্রাক। উষ্ণ দিন (১৫–২২°C) ও আর্দ্র রাত এ রোগের অনুকূল।",
            "solution_bn": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_leaf_rust_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতার মরিচা রোগ (Leaf Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_leaf_rust_04",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Leaf_Rust",
    diseaseBn: "পাতার মরিচা রোগ (Leaf Rust)",
    diseaseEn: "Leaf Rust",
    targetClass: "Leaf Rust",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_leaf_rust_04.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Leaf_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাতার মরিচা রোগ (Leaf Rust)",
            "description_bn": "পাতার উপর ছোট ছোট কমলা-বাদামী বা মরিচার মতো পাউডারের গুটি দেখা যায়। হাত দিলে আঙুলে মরিচার গুঁড়া লাগে।",
            "cause_bn": "পাকসিনিয়া ট্রাইটিচিনা (Puccinia triticina) ছত্রাক। উষ্ণ দিন (১৫–২২°C) ও আর্দ্র রাত এ রোগের অনুকূল।",
            "solution_bn": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Leaf_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রমণ দেখামাত্র প্রোপিকোনাজল (যেমন টিল্ট ২৫০ ইসি) প্রতি লিটার পানিতে ১ মিলি হারে স্প্রে করুন। পরবর্তী মৌসুমে মরিচা প্রতিরোধী জাত নির্বাচন করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_leaf_rust_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতার মরিচা রোগ (Leaf Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_wheat_blast_01",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Wheat_Blast",
    diseaseBn: "গমের ব্লাস্ট রোগ (Wheat Blast)",
    diseaseEn: "Wheat Blast",
    targetClass: "Blast",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_wheat_blast_01.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Wheat_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের ব্লাস্ট রোগ (Wheat Blast)",
            "description_bn": "পাতায় ধূসর রঙের চোখা দাগ তৈরি হয় এবং শীষের উপরিভাগ সাদা হয়ে শুকিয়ে চিটা হয়ে যায়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি ট্রাইটিকাম (Magnaporthe oryzae pathotype Triticum)। উষ্ণ ও বৃষ্টিময় আবহাওয়া এ রোগ বাড়ায়।",
            "solution_bn": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Wheat_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_wheat_blast_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "গমের ব্লাস্ট রোগ (Wheat Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_wheat_blast_02",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Wheat_Blast",
    diseaseBn: "গমের ব্লাস্ট রোগ (Wheat Blast)",
    diseaseEn: "Wheat Blast",
    targetClass: "Blast",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_wheat_blast_02.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Wheat_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের ব্লাস্ট রোগ (Wheat Blast)",
            "description_bn": "পাতায় ধূসর রঙের চোখা দাগ তৈরি হয় এবং শীষের উপরিভাগ সাদা হয়ে শুকিয়ে চিটা হয়ে যায়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি ট্রাইটিকাম (Magnaporthe oryzae pathotype Triticum)। উষ্ণ ও বৃষ্টিময় আবহাওয়া এ রোগ বাড়ায়।",
            "solution_bn": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Wheat_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_wheat_blast_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "গমের ব্লাস্ট রোগ (Wheat Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_wheat_blast_03",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Wheat_Blast",
    diseaseBn: "গমের ব্লাস্ট রোগ (Wheat Blast)",
    diseaseEn: "Wheat Blast",
    targetClass: "Blast",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_wheat_blast_03.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Wheat_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের ব্লাস্ট রোগ (Wheat Blast)",
            "description_bn": "পাতায় ধূসর রঙের চোখা দাগ তৈরি হয় এবং শীষের উপরিভাগ সাদা হয়ে শুকিয়ে চিটা হয়ে যায়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি ট্রাইটিকাম (Magnaporthe oryzae pathotype Triticum)। উষ্ণ ও বৃষ্টিময় আবহাওয়া এ রোগ বাড়ায়।",
            "solution_bn": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Wheat_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_wheat_blast_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "গমের ব্লাস্ট রোগ (Wheat Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_wheat_blast_04",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Wheat_Blast",
    diseaseBn: "গমের ব্লাস্ট রোগ (Wheat Blast)",
    diseaseEn: "Wheat Blast",
    targetClass: "Blast",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_wheat_blast_04.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Wheat_Blast",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের ব্লাস্ট রোগ (Wheat Blast)",
            "description_bn": "পাতায় ধূসর রঙের চোখা দাগ তৈরি হয় এবং শীষের উপরিভাগ সাদা হয়ে শুকিয়ে চিটা হয়ে যায়।",
            "cause_bn": "ম্যাগনাপোর্টে ওরাইজি ট্রাইটিকাম (Magnaporthe oryzae pathotype Triticum)। উষ্ণ ও বৃষ্টিময় আবহাওয়া এ রোগ বাড়ায়।",
            "solution_bn": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Wheat_Blast",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ বের হওয়ার সময় প্রতিরোধমূলকভাবে ন্যাটিভো (টেবুকোনাজল + ট্রাইফ্লক্সিস্ট্রবিন) বা ফলিকুর স্প্রে করুন। আক্রান্ত জমির গম বীজ হিসেবে ব্যবহার করবেন না।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_wheat_blast_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "গমের ব্লাস্ট রোগ (Wheat Blast) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_powdery_mildew_01",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Powdery_Mildew",
    diseaseBn: "পাউডারি মিলডিউ (Powdery Mildew)",
    diseaseEn: "Powdery Mildew",
    targetClass: "Powdery Mildew",
    confidence: 99.6,
    imageSrc: "/samples/wheat/wheat_powdery_mildew_01.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Powdery_Mildew",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাউডারি মিলডিউ (Powdery Mildew)",
            "description_bn": "পাতার উপরিভাগে সাদা পাউডার বা আটার মতো তুলতুলে ছত্রাকের আবরণ দেখা যায়, যা পরবর্তীতে ধূসর হয়ে যায়।",
            "cause_bn": "ব্লুমেরিয়া গ্রামিনিস (Blumeria graminis f. sp. tritici) ছত্রাক। ছায়াযুক্ত ও আর্দ্র ঠান্ডা আবহাওয়া।",
            "solution_bn": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Powdery_Mildew",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_powdery_mildew_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাউডারি মিলডিউ (Powdery Mildew) [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_powdery_mildew_02",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Powdery_Mildew",
    diseaseBn: "পাউডারি মিলডিউ (Powdery Mildew)",
    diseaseEn: "Powdery Mildew",
    targetClass: "Powdery Mildew",
    confidence: 99.6,
    imageSrc: "/samples/wheat/wheat_powdery_mildew_02.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Powdery_Mildew",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাউডারি মিলডিউ (Powdery Mildew)",
            "description_bn": "পাতার উপরিভাগে সাদা পাউডার বা আটার মতো তুলতুলে ছত্রাকের আবরণ দেখা যায়, যা পরবর্তীতে ধূসর হয়ে যায়।",
            "cause_bn": "ব্লুমেরিয়া গ্রামিনিস (Blumeria graminis f. sp. tritici) ছত্রাক। ছায়াযুক্ত ও আর্দ্র ঠান্ডা আবহাওয়া।",
            "solution_bn": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Powdery_Mildew",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_powdery_mildew_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাউডারি মিলডিউ (Powdery Mildew) [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_powdery_mildew_03",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Powdery_Mildew",
    diseaseBn: "পাউডারি মিলডিউ (Powdery Mildew)",
    diseaseEn: "Powdery Mildew",
    targetClass: "Powdery Mildew",
    confidence: 99.6,
    imageSrc: "/samples/wheat/wheat_powdery_mildew_03.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Powdery_Mildew",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের পাউডারি মিলডিউ (Powdery Mildew)",
            "description_bn": "পাতার উপরিভাগে সাদা পাউডার বা আটার মতো তুলতুলে ছত্রাকের আবরণ দেখা যায়, যা পরবর্তীতে ধূসর হয়ে যায়।",
            "cause_bn": "ব্লুমেরিয়া গ্রামিনিস (Blumeria graminis f. sp. tritici) ছত্রাক। ছায়াযুক্ত ও আর্দ্র ঠান্ডা আবহাওয়া।",
            "solution_bn": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Powdery_Mildew",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "ঘন করে বীজ বপন পরিহার করুন। সালফার গ্রুপের ছত্রাকনাশক (যেমন থিওভিট ২ গ্রাম/লিটার) বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_powdery_mildew_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাউডারি মিলডিউ (Powdery Mildew) [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_stripe_rust_01",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Stripe_Rust",
    diseaseBn: "হলুদ মরিচা রোগ (Stripe Rust)",
    diseaseEn: "Stripe Rust",
    targetClass: "Stripe Rust",
    confidence: 99.8,
    imageSrc: "/samples/wheat/wheat_stripe_rust_01.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Stripe_Rust",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের হলুদ মরিচা রোগ (Stripe / Yellow Rust)",
            "description_bn": "পাতার শিরার সমান্তরালে সরু হলুদ রঙের ডোরাকাটা বা সারিবদ্ধ ফোসকার মতো গুটি দেখা যায়।",
            "cause_bn": "পাকসিনিয়া স্ট্রাইফর্মিস (Puccinia striiformis) ছত্রাক। শীতকালীন ঠান্ডা ও আর্দ্র আবহাওয়া (১০–১৫°C)।",
            "solution_bn": "হলুদ ডোরা দেখা মাত্রই টিল্ট (প্রোপিকোনাজল ২৫০ ইসি) ১ মিলি/লিটার হারে স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Stripe_Rust",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "হলুদ ডোরা দেখা মাত্রই টিল্ট (প্রোপিকোনাজল ২৫০ ইসি) ১ মিলি/লিটার হারে স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_stripe_rust_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "হলুদ মরিচা রোগ (Stripe Rust) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_stripe_rust_02",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Stripe_Rust",
    diseaseBn: "হলুদ মরিচা রোগ (Stripe Rust)",
    diseaseEn: "Stripe Rust",
    targetClass: "Stripe Rust",
    confidence: 99.8,
    imageSrc: "/samples/wheat/wheat_stripe_rust_02.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Stripe_Rust",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "গমের হলুদ মরিচা রোগ (Stripe / Yellow Rust)",
            "description_bn": "পাতার শিরার সমান্তরালে সরু হলুদ রঙের ডোরাকাটা বা সারিবদ্ধ ফোসকার মতো গুটি দেখা যায়।",
            "cause_bn": "পাকসিনিয়া স্ট্রাইফর্মিস (Puccinia striiformis) ছত্রাক। শীতকালীন ঠান্ডা ও আর্দ্র আবহাওয়া (১০–১৫°C)।",
            "solution_bn": "হলুদ ডোরা দেখা মাত্রই টিল্ট (প্রোপিকোনাজল ২৫০ ইসি) ১ মিলি/লিটার হারে স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Stripe_Rust",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "হলুদ ডোরা দেখা মাত্রই টিল্ট (প্রোপিকোনাজল ২৫০ ইসি) ১ মিলি/লিটার হারে স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_stripe_rust_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "হলুদ মরিচা রোগ (Stripe Rust) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_healthy_01",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Healthy",
    diseaseBn: "সুস্থ গমের পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "HealthyLeaf",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_healthy_01.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ গমের পাতা (Healthy)",
            "description_bn": "সবুজ ও তেজস্বী পাতা, কোনো ধরনের মরিচা, দাগ বা ঝলসে যাওয়ার লক্ষণ নেই।",
            "cause_bn": "সঠিক বপন সময়, পুষ্টি ও উপযোগী ঠাণ্ডা আবহাওয়া।",
            "solution_bn": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_healthy_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ গমের পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_healthy_02",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Healthy",
    diseaseBn: "সুস্থ গমের পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "HealthyLeaf",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_healthy_02.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ গমের পাতা (Healthy)",
            "description_bn": "সবুজ ও তেজস্বী পাতা, কোনো ধরনের মরিচা, দাগ বা ঝলসে যাওয়ার লক্ষণ নেই।",
            "cause_bn": "সঠিক বপন সময়, পুষ্টি ও উপযোগী ঠাণ্ডা আবহাওয়া।",
            "solution_bn": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_healthy_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ গমের পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "wheat_healthy_03",
    crop: "Wheat",
    cropBn: "গম",
    cropEn: "Wheat",
    disease: "Healthy",
    diseaseBn: "সুস্থ গমের পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "HealthyLeaf",
    confidence: 100.0,
    imageSrc: "/samples/wheat/wheat_healthy_03.jpg",
    cropHint: "Wheat",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Wheat",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ গমের পাতা (Healthy)",
            "description_bn": "সবুজ ও তেজস্বী পাতা, কোনো ধরনের মরিচা, দাগ বা ঝলসে যাওয়ার লক্ষণ নেই।",
            "cause_bn": "সঠিক বপন সময়, পুষ্টি ও উপযোগী ঠাণ্ডা আবহাওয়া।",
            "solution_bn": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।"
      },
      "top3_crops": [
            {
                  "class": "Wheat",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "শীষ আসার সময় মাটি যেন বেশি শুকিয়ে না যায় সেদিকে খেয়াল রাখুন। পরিমিত সেচ বজায় রাখুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: wheat_healthy_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "গম (Wheat)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ গমের পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_common_rust_01",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Common_Rust",
    diseaseBn: "কমন রাস্ট (Common Rust)",
    diseaseEn: "Common Rust",
    targetClass: "Common_Rust",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_common_rust_01.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Common_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার কমন রাস্ট (Common Rust)",
            "description_bn": "পাতার উভয় পিঠে ছোট ছোট বাদামী বা লালচে মরিচার ফোসকা তৈরি হয় যা ফেটে গুঁড়া ছড়ায়।",
            "cause_bn": "পাকসিনিয়া সরঘি (Puccinia sorghi) ছত্রাক। মাঝারি তাপমাত্রা (১৬–২৫°C) ও উচ্চ আর্দ্রতায় এ রোগ বৃদ্ধি পায়।",
            "solution_bn": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Common_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_common_rust_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কমন রাস্ট (Common Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_common_rust_02",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Common_Rust",
    diseaseBn: "কমন রাস্ট (Common Rust)",
    diseaseEn: "Common Rust",
    targetClass: "Common_Rust",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_common_rust_02.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Common_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার কমন রাস্ট (Common Rust)",
            "description_bn": "পাতার উভয় পিঠে ছোট ছোট বাদামী বা লালচে মরিচার ফোসকা তৈরি হয় যা ফেটে গুঁড়া ছড়ায়।",
            "cause_bn": "পাকসিনিয়া সরঘি (Puccinia sorghi) ছত্রাক। মাঝারি তাপমাত্রা (১৬–২৫°C) ও উচ্চ আর্দ্রতায় এ রোগ বৃদ্ধি পায়।",
            "solution_bn": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Common_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_common_rust_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কমন রাস্ট (Common Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_common_rust_03",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Common_Rust",
    diseaseBn: "কমন রাস্ট (Common Rust)",
    diseaseEn: "Common Rust",
    targetClass: "Common_Rust",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_common_rust_03.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Common_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার কমন রাস্ট (Common Rust)",
            "description_bn": "পাতার উভয় পিঠে ছোট ছোট বাদামী বা লালচে মরিচার ফোসকা তৈরি হয় যা ফেটে গুঁড়া ছড়ায়।",
            "cause_bn": "পাকসিনিয়া সরঘি (Puccinia sorghi) ছত্রাক। মাঝারি তাপমাত্রা (১৬–২৫°C) ও উচ্চ আর্দ্রতায় এ রোগ বৃদ্ধি পায়।",
            "solution_bn": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Common_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_common_rust_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কমন রাস্ট (Common Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_common_rust_04",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Common_Rust",
    diseaseBn: "কমন রাস্ট (Common Rust)",
    diseaseEn: "Common Rust",
    targetClass: "Common_Rust",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_common_rust_04.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Common_Rust",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার কমন রাস্ট (Common Rust)",
            "description_bn": "পাতার উভয় পিঠে ছোট ছোট বাদামী বা লালচে মরিচার ফোসকা তৈরি হয় যা ফেটে গুঁড়া ছড়ায়।",
            "cause_bn": "পাকসিনিয়া সরঘি (Puccinia sorghi) ছত্রাক। মাঝারি তাপমাত্রা (১৬–২৫°C) ও উচ্চ আর্দ্রতায় এ রোগ বৃদ্ধি পায়।",
            "solution_bn": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Common_Rust",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব বা অ্যাজোক্সিস্ট্রবিন স্প্রে করুন। আক্রমণের মাত্রা বেশি হলে ট্রায়াজোল গ্রুপের ছত্রাকনাশক ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_common_rust_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কমন রাস্ট (Common Rust) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_gray_leaf_spot_01",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Gray_Leaf_Spot",
    diseaseBn: "ধূসর পাতা দাগ (Gray Leaf Spot)",
    diseaseEn: "Gray Leaf Spot",
    targetClass: "Gray_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_gray_leaf_spot_01.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Gray_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার ধূসর পাতা দাগ (Gray Leaf Spot)",
            "description_bn": "পাতার শিরার সাথে সমান্তরাল আয়তাকার ধূসর বা বাদামী রঙের লম্বা দাগ দেখা যায়।",
            "cause_bn": "সারকোস্পোরা জিয়া-মেডিস (Cercospora zeae-maydis) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়ায় নিচের পাতা থেকে উপরে ছড়ায়।",
            "solution_bn": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Gray_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_gray_leaf_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ধূসর পাতা দাগ (Gray Leaf Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_gray_leaf_spot_02",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Gray_Leaf_Spot",
    diseaseBn: "ধূসর পাতা দাগ (Gray Leaf Spot)",
    diseaseEn: "Gray Leaf Spot",
    targetClass: "Gray_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_gray_leaf_spot_02.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Gray_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার ধূসর পাতা দাগ (Gray Leaf Spot)",
            "description_bn": "পাতার শিরার সাথে সমান্তরাল আয়তাকার ধূসর বা বাদামী রঙের লম্বা দাগ দেখা যায়।",
            "cause_bn": "সারকোস্পোরা জিয়া-মেডিস (Cercospora zeae-maydis) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়ায় নিচের পাতা থেকে উপরে ছড়ায়।",
            "solution_bn": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Gray_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_gray_leaf_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ধূসর পাতা দাগ (Gray Leaf Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_gray_leaf_spot_03",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Gray_Leaf_Spot",
    diseaseBn: "ধূসর পাতা দাগ (Gray Leaf Spot)",
    diseaseEn: "Gray Leaf Spot",
    targetClass: "Gray_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_gray_leaf_spot_03.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Gray_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার ধূসর পাতা দাগ (Gray Leaf Spot)",
            "description_bn": "পাতার শিরার সাথে সমান্তরাল আয়তাকার ধূসর বা বাদামী রঙের লম্বা দাগ দেখা যায়।",
            "cause_bn": "সারকোস্পোরা জিয়া-মেডিস (Cercospora zeae-maydis) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়ায় নিচের পাতা থেকে উপরে ছড়ায়।",
            "solution_bn": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Gray_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_gray_leaf_spot_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ধূসর পাতা দাগ (Gray Leaf Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_gray_leaf_spot_04",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Gray_Leaf_Spot",
    diseaseBn: "ধূসর পাতা দাগ (Gray Leaf Spot)",
    diseaseEn: "Gray Leaf Spot",
    targetClass: "Gray_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_gray_leaf_spot_04.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Gray_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার ধূসর পাতা দাগ (Gray Leaf Spot)",
            "description_bn": "পাতার শিরার সাথে সমান্তরাল আয়তাকার ধূসর বা বাদামী রঙের লম্বা দাগ দেখা যায়।",
            "cause_bn": "সারকোস্পোরা জিয়া-মেডিস (Cercospora zeae-maydis) ছত্রাক। উষ্ণ ও আর্দ্র আবহাওয়ায় নিচের পাতা থেকে উপরে ছড়ায়।",
            "solution_bn": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Gray_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ফসল কাটার পর অবশিষ্টাংশ পরিষ্কার করুন। লক্ষণ দেখা দিলে পাইরাক্লোস্ট্রবিন বা প্রোপিকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_gray_leaf_spot_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ধূসর পাতা দাগ (Gray Leaf Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_northern_leaf_blight_01",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Northern_Leaf_Blight",
    diseaseBn: "উত্তরীয় পাতা পোড়া (NLB)",
    diseaseEn: "Northern Leaf Blight",
    targetClass: "Northern_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/corn/corn_northern_leaf_blight_01.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Northern_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
            "description_bn": "পাতায় লম্বাটে চুরুট আকৃতির বড় ধূসর-সবুজ বা বাদামী রঙের দাগ সৃষ্টি হয়।",
            "cause_bn": "এক্সসিরোহিলাম টার্সিকাম (Exserohilum turcicum) ছত্রাক। ঠাণ্ডা-নাতিশীতোষ্ণ ভেজা আবহাওয়া এর অনুকূল।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Northern_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_northern_leaf_blight_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "উত্তরীয় পাতা পোড়া (NLB) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_northern_leaf_blight_02",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Northern_Leaf_Blight",
    diseaseBn: "উত্তরীয় পাতা পোড়া (NLB)",
    diseaseEn: "Northern Leaf Blight",
    targetClass: "Northern_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/corn/corn_northern_leaf_blight_02.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Northern_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
            "description_bn": "পাতায় লম্বাটে চুরুট আকৃতির বড় ধূসর-সবুজ বা বাদামী রঙের দাগ সৃষ্টি হয়।",
            "cause_bn": "এক্সসিরোহিলাম টার্সিকাম (Exserohilum turcicum) ছত্রাক। ঠাণ্ডা-নাতিশীতোষ্ণ ভেজা আবহাওয়া এর অনুকূল।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Northern_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_northern_leaf_blight_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "উত্তরীয় পাতা পোড়া (NLB) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_northern_leaf_blight_03",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Northern_Leaf_Blight",
    diseaseBn: "উত্তরীয় পাতা পোড়া (NLB)",
    diseaseEn: "Northern Leaf Blight",
    targetClass: "Northern_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/corn/corn_northern_leaf_blight_03.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Northern_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
            "description_bn": "পাতায় লম্বাটে চুরুট আকৃতির বড় ধূসর-সবুজ বা বাদামী রঙের দাগ সৃষ্টি হয়।",
            "cause_bn": "এক্সসিরোহিলাম টার্সিকাম (Exserohilum turcicum) ছত্রাক। ঠাণ্ডা-নাতিশীতোষ্ণ ভেজা আবহাওয়া এর অনুকূল।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Northern_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_northern_leaf_blight_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "উত্তরীয় পাতা পোড়া (NLB) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_northern_leaf_blight_04",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Northern_Leaf_Blight",
    diseaseBn: "উত্তরীয় পাতা পোড়া (NLB)",
    diseaseEn: "Northern Leaf Blight",
    targetClass: "Northern_Leaf_Blight",
    confidence: 99.9,
    imageSrc: "/samples/corn/corn_northern_leaf_blight_04.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Northern_Leaf_Blight",
      "disease_confidence": 0.9990000000000001,
      "boxes": [],
      "disease_info": {
            "name_bn": "ভুট্টার উত্তরীয় পাতা পোড়া (Northern Leaf Blight)",
            "description_bn": "পাতায় লম্বাটে চুরুট আকৃতির বড় ধূসর-সবুজ বা বাদামী রঙের দাগ সৃষ্টি হয়।",
            "cause_bn": "এক্সসিরোহিলাম টার্সিকাম (Exserohilum turcicum) ছত্রাক। ঠাণ্ডা-নাতিশীতোষ্ণ ভেজা আবহাওয়া এর অনুকূল।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Northern_Leaf_Blight",
                  "confidence": 0.9990000000000001
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম + ম্যানকোজেব (কম্প্যানিয়ন) ২ গ্রাম/লিটার হারে স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_northern_leaf_blight_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "উত্তরীয় পাতা পোড়া (NLB) [99.9%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_healthy_01",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Healthy",
    diseaseBn: "সুস্থ ভুট্টা পাতা (Healthy)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Healthy",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_healthy_01.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ভুট্টা পাতা (Healthy)",
            "description_bn": "প্রশস্ত গাঢ় সবুজ পাতা, চমৎকার সালোকসংশ্লেষণ ক্ষমতা ও দাগমুক্ত উজ্জ্বলতা।",
            "cause_bn": "যথাযথ নাইট্রোজেন ও জিংক পুষ্টি এবং পর্যাপ্ত রোদ।",
            "solution_bn": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_healthy_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ভুট্টা পাতা (Healthy) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_healthy_02",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Healthy",
    diseaseBn: "সুস্থ ভুট্টা পাতা (Healthy)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Healthy",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_healthy_02.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ভুট্টা পাতা (Healthy)",
            "description_bn": "প্রশস্ত গাঢ় সবুজ পাতা, চমৎকার সালোকসংশ্লেষণ ক্ষমতা ও দাগমুক্ত উজ্জ্বলতা।",
            "cause_bn": "যথাযথ নাইট্রোজেন ও জিংক পুষ্টি এবং পর্যাপ্ত রোদ।",
            "solution_bn": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_healthy_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ভুট্টা পাতা (Healthy) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_healthy_03",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Healthy",
    diseaseBn: "সুস্থ ভুট্টা পাতা (Healthy)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Healthy",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_healthy_03.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ভুট্টা পাতা (Healthy)",
            "description_bn": "প্রশস্ত গাঢ় সবুজ পাতা, চমৎকার সালোকসংশ্লেষণ ক্ষমতা ও দাগমুক্ত উজ্জ্বলতা।",
            "cause_bn": "যথাযথ নাইট্রোজেন ও জিংক পুষ্টি এবং পর্যাপ্ত রোদ।",
            "solution_bn": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_healthy_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ভুট্টা পাতা (Healthy) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "corn_healthy_04",
    crop: "Corn",
    cropBn: "ভুট্টা",
    cropEn: "Corn",
    disease: "Healthy",
    diseaseBn: "সুস্থ ভুট্টা পাতা (Healthy)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Healthy",
    confidence: 100.0,
    imageSrc: "/samples/corn/corn_healthy_04.jpg",
    cropHint: "Corn",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Corn",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ভুট্টা পাতা (Healthy)",
            "description_bn": "প্রশস্ত গাঢ় সবুজ পাতা, চমৎকার সালোকসংশ্লেষণ ক্ষমতা ও দাগমুক্ত উজ্জ্বলতা।",
            "cause_bn": "যথাযথ নাইট্রোজেন ও জিংক পুষ্টি এবং পর্যাপ্ত রোদ।",
            "solution_bn": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Corn",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মোচা গঠনের সময় পর্যাপ্ত সেচ নিশ্চিত করুন। কোনো স্প্রে প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: corn_healthy_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "ভুট্টা (Corn)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ভুট্টা পাতা (Healthy) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_bacterial_spot_01",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Bacterial_Spot",
    diseaseBn: "ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
    diseaseEn: "Bacterial Spot",
    targetClass: "Chili__Bacterial_Spot",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_bacterial_spot_01.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Bacterial_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
            "description_bn": "পাতায় ছোট ছোট কালচে-বাদামী জলছাপের মতো দাগ দেখা যায়, যা পরবর্তীতে খসখসে হয়ে ছিদ্র তৈরি করে।",
            "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. vesicatoria)। অতিরিক্ত বৃষ্টি ও পাতার ভেজা অবস্থায় দ্রুত ছড়ায়।",
            "solution_bn": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Bacterial_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_bacterial_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্যাকটেরিয়াল দাগ (Bacterial Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_bacterial_spot_02",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Bacterial_Spot",
    diseaseBn: "ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
    diseaseEn: "Bacterial Spot",
    targetClass: "Chili__Bacterial_Spot",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_bacterial_spot_02.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Bacterial_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
            "description_bn": "পাতায় ছোট ছোট কালচে-বাদামী জলছাপের মতো দাগ দেখা যায়, যা পরবর্তীতে খসখসে হয়ে ছিদ্র তৈরি করে।",
            "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. vesicatoria)। অতিরিক্ত বৃষ্টি ও পাতার ভেজা অবস্থায় দ্রুত ছড়ায়।",
            "solution_bn": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Bacterial_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_bacterial_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্যাকটেরিয়াল দাগ (Bacterial Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_bacterial_spot_03",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Bacterial_Spot",
    diseaseBn: "ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
    diseaseEn: "Bacterial Spot",
    targetClass: "Chili__Bacterial_Spot",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_bacterial_spot_03.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Bacterial_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের ব্যাকটেরিয়াল দাগ (Bacterial Spot)",
            "description_bn": "পাতায় ছোট ছোট কালচে-বাদামী জলছাপের মতো দাগ দেখা যায়, যা পরবর্তীতে খসখসে হয়ে ছিদ্র তৈরি করে।",
            "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. vesicatoria)। অতিরিক্ত বৃষ্টি ও পাতার ভেজা অবস্থায় দ্রুত ছড়ায়।",
            "solution_bn": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Bacterial_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "কপার অক্সিক্লোরাইড (ব্লাইটক্স) প্রতি লিটারে ২ গ্রাম এবং সাথে ব্যাকটেরিসাইড স্প্রে করুন। আক্রান্ত গাছের পাতা পুড়িয়ে ফেলুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_bacterial_spot_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ব্যাকটেরিয়াল দাগ (Bacterial Spot) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_curl_virus_01",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Curl_Virus",
    diseaseBn: "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus)",
    diseaseEn: "Leaf Curl Virus",
    targetClass: "Chili__Curl_Virus",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_curl_virus_01.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Curl_Virus",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl Virus)",
            "description_bn": "পাতা উপরের দিকে চামচের মতো কুঁকড়ে যায়, গাছের বৃদ্ধি থমকে যায় এবং ফুল ও ফল ঝরে পড়ে।",
            "cause_bn": "বেগমোভাইরাস (Begomovirus)। সাদা মাছি (Bemisia tabaci) পোকা এ রোগের প্রধান বাহক।",
            "solution_bn": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Curl_Virus",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_curl_virus_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_curl_virus_02",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Curl_Virus",
    diseaseBn: "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus)",
    diseaseEn: "Leaf Curl Virus",
    targetClass: "Chili__Curl_Virus",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_curl_virus_02.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Curl_Virus",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl Virus)",
            "description_bn": "পাতা উপরের দিকে চামচের মতো কুঁকড়ে যায়, গাছের বৃদ্ধি থমকে যায় এবং ফুল ও ফল ঝরে পড়ে।",
            "cause_bn": "বেগমোভাইরাস (Begomovirus)। সাদা মাছি (Bemisia tabaci) পোকা এ রোগের প্রধান বাহক।",
            "solution_bn": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Curl_Virus",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_curl_virus_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_curl_virus_03",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Curl_Virus",
    diseaseBn: "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus)",
    diseaseEn: "Leaf Curl Virus",
    targetClass: "Chili__Curl_Virus",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_curl_virus_03.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Curl_Virus",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl Virus)",
            "description_bn": "পাতা উপরের দিকে চামচের মতো কুঁকড়ে যায়, গাছের বৃদ্ধি থমকে যায় এবং ফুল ও ফল ঝরে পড়ে।",
            "cause_bn": "বেগমোভাইরাস (Begomovirus)। সাদা মাছি (Bemisia tabaci) পোকা এ রোগের প্রধান বাহক।",
            "solution_bn": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Curl_Virus",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_curl_virus_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_curl_virus_04",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Curl_Virus",
    diseaseBn: "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus)",
    diseaseEn: "Leaf Curl Virus",
    targetClass: "Chili__Curl_Virus",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_curl_virus_04.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Curl_Virus",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাতা কোঁকড়ানো ভাইরাস (Chilli Leaf Curl Virus)",
            "description_bn": "পাতা উপরের দিকে চামচের মতো কুঁকড়ে যায়, গাছের বৃদ্ধি থমকে যায় এবং ফুল ও ফল ঝরে পড়ে।",
            "cause_bn": "বেগমোভাইরাস (Begomovirus)। সাদা মাছি (Bemisia tabaci) পোকা এ রোগের প্রধান বাহক।",
            "solution_bn": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Curl_Virus",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "সাদা মাছি দমনে ইমিডাক্লোপ্রিড (যেমন টিডো) বা অ্যাসিটামিপ্রিড স্প্রে করুন। জমিতে হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) ব্যবহার করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_curl_virus_04 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাতা কোঁকড়ানো ভাইরাস (Leaf Curl Virus) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_cercospora_leaf_spot_01",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Cercospora_Leaf_Spot",
    diseaseBn: "সারকোস্পোরা দাগ (Cercospora)",
    diseaseEn: "Cercospora Leaf Spot",
    targetClass: "Chili__Cercospora_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_cercospora_leaf_spot_01.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cercospora_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের সারকোস্পোরা দাগ / ব্যাঙের চোখ দাগ (Cercospora)",
            "description_bn": "পাতায় গোলাকার দাগ যার কেন্দ্র ধূসর বা সাদাটে এবং চারপাশ গাঢ় বাদামী বৃত্তে ঘেরা (ব্যাঙের চোখের মতো)।",
            "cause_bn": "সারকোস্পোরা ক্যাপসিকি (Cercospora capsici) ছত্রাক। আর্দ্র পরিবেশ ও ঘন গাছপালায় এটি দ্রুত ছড়ায়।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cercospora_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_cercospora_leaf_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সারকোস্পোরা দাগ (Cercospora) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_cercospora_leaf_spot_02",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Cercospora_Leaf_Spot",
    diseaseBn: "সারকোস্পোরা দাগ (Cercospora)",
    diseaseEn: "Cercospora Leaf Spot",
    targetClass: "Chili__Cercospora_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_cercospora_leaf_spot_02.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cercospora_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের সারকোস্পোরা দাগ / ব্যাঙের চোখ দাগ (Cercospora)",
            "description_bn": "পাতায় গোলাকার দাগ যার কেন্দ্র ধূসর বা সাদাটে এবং চারপাশ গাঢ় বাদামী বৃত্তে ঘেরা (ব্যাঙের চোখের মতো)।",
            "cause_bn": "সারকোস্পোরা ক্যাপসিকি (Cercospora capsici) ছত্রাক। আর্দ্র পরিবেশ ও ঘন গাছপালায় এটি দ্রুত ছড়ায়।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cercospora_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_cercospora_leaf_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সারকোস্পোরা দাগ (Cercospora) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_cercospora_leaf_spot_03",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Cercospora_Leaf_Spot",
    diseaseBn: "সারকোস্পোরা দাগ (Cercospora)",
    diseaseEn: "Cercospora Leaf Spot",
    targetClass: "Chili__Cercospora_Leaf_Spot",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_cercospora_leaf_spot_03.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cercospora_Leaf_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের সারকোস্পোরা দাগ / ব্যাঙের চোখ দাগ (Cercospora)",
            "description_bn": "পাতায় গোলাকার দাগ যার কেন্দ্র ধূসর বা সাদাটে এবং চারপাশ গাঢ় বাদামী বৃত্তে ঘেরা (ব্যাঙের চোখের মতো)।",
            "cause_bn": "সারকোস্পোরা ক্যাপসিকি (Cercospora capsici) ছত্রাক। আর্দ্র পরিবেশ ও ঘন গাছপালায় এটি দ্রুত ছড়ায়।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cercospora_Leaf_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। কার্বেন্ডাজিম বা ক্লোরোথ্যালোনিল সঠিক মাত্রায় স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_cercospora_leaf_spot_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সারকোস্পোরা দাগ (Cercospora) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_powdery_mildew_01",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Powdery_Mildew",
    diseaseBn: "পাউডারি মিলডিউ (Powdery Mildew)",
    diseaseEn: "Powdery Mildew",
    targetClass: "Chili__Powdery_Mildew",
    confidence: 99.7,
    imageSrc: "/samples/chilli/chilli_powdery_mildew_01.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Powdery_Mildew",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাউডারি মিলডিউ (Powdery Mildew)",
            "description_bn": "পাতার নিচের পিঠে সাদা পাউডারের মতো ছত্রাকের উপস্থিতি এবং ওপরের পিঠে হলুদ বা তামাটে ছোপ দেখা যায়।",
            "cause_bn": "লেভেইলুলা টরিকা (Leveillula taurica) ছত্রাক। শুষ্ক উষ্ণ দিন ও আর্দ্র রাত।",
            "solution_bn": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Powdery_Mildew",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_powdery_mildew_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাউডারি মিলডিউ (Powdery Mildew) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_powdery_mildew_02",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Powdery_Mildew",
    diseaseBn: "পাউডারি মিলডিউ (Powdery Mildew)",
    diseaseEn: "Powdery Mildew",
    targetClass: "Chili__Powdery_Mildew",
    confidence: 99.7,
    imageSrc: "/samples/chilli/chilli_powdery_mildew_02.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Powdery_Mildew",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাউডারি মিলডিউ (Powdery Mildew)",
            "description_bn": "পাতার নিচের পিঠে সাদা পাউডারের মতো ছত্রাকের উপস্থিতি এবং ওপরের পিঠে হলুদ বা তামাটে ছোপ দেখা যায়।",
            "cause_bn": "লেভেইলুলা টরিকা (Leveillula taurica) ছত্রাক। শুষ্ক উষ্ণ দিন ও আর্দ্র রাত।",
            "solution_bn": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Powdery_Mildew",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_powdery_mildew_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাউডারি মিলডিউ (Powdery Mildew) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_powdery_mildew_03",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Powdery_Mildew",
    diseaseBn: "পাউডারি মিলডিউ (Powdery Mildew)",
    diseaseEn: "Powdery Mildew",
    targetClass: "Chili__Powdery_Mildew",
    confidence: 99.7,
    imageSrc: "/samples/chilli/chilli_powdery_mildew_03.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Powdery_Mildew",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "মরিচের পাউডারি মিলডিউ (Powdery Mildew)",
            "description_bn": "পাতার নিচের পিঠে সাদা পাউডারের মতো ছত্রাকের উপস্থিতি এবং ওপরের পিঠে হলুদ বা তামাটে ছোপ দেখা যায়।",
            "cause_bn": "লেভেইলুলা টরিকা (Leveillula taurica) ছত্রাক। শুষ্ক উষ্ণ দিন ও আর্দ্র রাত।",
            "solution_bn": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Powdery_Mildew",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "সালফার ৮০ ডব্লিউপি (যেমন কুমুলাস বা থিওভিট ২ গ্রাম/লিটার) বা হেক্সাকোনাজল স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_powdery_mildew_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "পাউডারি মিলডিউ (Powdery Mildew) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_healthy_leaf_01",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ মরিচ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Chili__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_healthy_leaf_01.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ মরিচ পাতা (Healthy)",
            "description_bn": "মসৃণ ও চকচকে গাঢ় সবুজ পাতা, কোনো কোঁকড়ানো বা দাগের উপসর্গ নেই।",
            "cause_bn": "সুষম সার, নিয়ন্ত্রিত আর্দ্রতা ও পোকা-মাকড়মুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_healthy_leaf_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ মরিচ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_healthy_leaf_02",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ মরিচ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Chili__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_healthy_leaf_02.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ মরিচ পাতা (Healthy)",
            "description_bn": "মসৃণ ও চকচকে গাঢ় সবুজ পাতা, কোনো কোঁকড়ানো বা দাগের উপসর্গ নেই।",
            "cause_bn": "সুষম সার, নিয়ন্ত্রিত আর্দ্রতা ও পোকা-মাকড়মুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_healthy_leaf_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ মরিচ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "chilli_healthy_leaf_03",
    crop: "Chilli",
    cropBn: "মরিচ",
    cropEn: "Chilli",
    disease: "Healthy_Leaf",
    diseaseBn: "সুস্থ মরিচ পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Chili__Healthy_Leaf",
    confidence: 100.0,
    imageSrc: "/samples/chilli/chilli_healthy_leaf_03.jpg",
    cropHint: "Chilli",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Chilli",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy_Leaf",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ মরিচ পাতা (Healthy)",
            "description_bn": "মসৃণ ও চকচকে গাঢ় সবুজ পাতা, কোনো কোঁকড়ানো বা দাগের উপসর্গ নেই।",
            "cause_bn": "সুষম সার, নিয়ন্ত্রিত আর্দ্রতা ও পোকা-মাকড়মুক্ত পরিবেশ।",
            "solution_bn": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।"
      },
      "top3_crops": [
            {
                  "class": "Chilli",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy_Leaf",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "নিয়মিত নিড়ানি দিন এবং মাটিতে অতিরিক্ত পানি জমতে দেবেন না। কোনো কীটনাশক প্রয়োগের দরকার নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: chilli_healthy_leaf_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "মরিচ (Chilli)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ মরিচ পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_alternaria_spot_01",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Alternaria_Spot",
    diseaseBn: "বাঁধাকপির অল্টারনারিয়া দাগ",
    diseaseEn: "Cabbage Alternaria Spot",
    targetClass: "Cabbage__Alternaria_Spot",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_alternaria_spot_01.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Alternaria_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "বাঁধাকপির অল্টারনারিয়া গোল দাগ রোগ (Alternaria)",
            "description_bn": "পাতায় গাঢ় বাদামী থেকে কালো রঙের গোলাকার বলয়াকৃতি দাগ দেখা যায়, যা শুকিয়ে পাতার ভেতর ফুটো করে দেয়।",
            "cause_bn": "অল্টারনারিয়া ব্রাসিকি (Alternaria brassicae) ছত্রাক। কুয়াশাচ্ছন্ন দিন এবং ঘন শিশিরে এ রোগ ব্যাপক আকার ধারণ করে।",
            "solution_bn": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Alternaria_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_alternaria_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "বাঁধাকপির অল্টারনারিয়া দাগ [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_alternaria_spot_02",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Alternaria_Spot",
    diseaseBn: "বাঁধাকপির অল্টারনারিয়া দাগ",
    diseaseEn: "Cabbage Alternaria Spot",
    targetClass: "Cabbage__Alternaria_Spot",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_alternaria_spot_02.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Alternaria_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "বাঁধাকপির অল্টারনারিয়া গোল দাগ রোগ (Alternaria)",
            "description_bn": "পাতায় গাঢ় বাদামী থেকে কালো রঙের গোলাকার বলয়াকৃতি দাগ দেখা যায়, যা শুকিয়ে পাতার ভেতর ফুটো করে দেয়।",
            "cause_bn": "অল্টারনারিয়া ব্রাসিকি (Alternaria brassicae) ছত্রাক। কুয়াশাচ্ছন্ন দিন এবং ঘন শিশিরে এ রোগ ব্যাপক আকার ধারণ করে।",
            "solution_bn": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Alternaria_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_alternaria_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "বাঁধাকপির অল্টারনারিয়া দাগ [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_alternaria_spot_03",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Alternaria_Spot",
    diseaseBn: "বাঁধাকপির অল্টারনারিয়া দাগ",
    diseaseEn: "Cabbage Alternaria Spot",
    targetClass: "Cabbage__Alternaria_Spot",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_alternaria_spot_03.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Alternaria_Spot",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "বাঁধাকপির অল্টারনারিয়া গোল দাগ রোগ (Alternaria)",
            "description_bn": "পাতায় গাঢ় বাদামী থেকে কালো রঙের গোলাকার বলয়াকৃতি দাগ দেখা যায়, যা শুকিয়ে পাতার ভেতর ফুটো করে দেয়।",
            "cause_bn": "অল্টারনারিয়া ব্রাসিকি (Alternaria brassicae) ছত্রাক। কুয়াশাচ্ছন্ন দিন এবং ঘন শিশিরে এ রোগ ব্যাপক আকার ধারণ করে।",
            "solution_bn": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Alternaria_Spot",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "ম্যানকোজেব (২ গ্রাম/লিটার) অথবা রোভরাল (আইপ্রোডায়ন) স্প্রে করুন। স্প্রে করার সময় আঠালো স্প্রেডার স্টিকার মিশিয়ে নিন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_alternaria_spot_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "বাঁধাকপির অল্টারনারিয়া দাগ [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_black_rot_01",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Black_Rot",
    diseaseBn: "কপির ব্লাক রট রোগ (Black Rot)",
    diseaseEn: "Cabbage Black Rot",
    targetClass: "Cabbage__Black_Rot",
    confidence: 99.8,
    imageSrc: "/samples/brassica/brassica_black_rot_01.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Black_Rot",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "কপির ব্লাক রট রোগ (Cabbage Black Rot)",
            "description_bn": "পাতার কিনারা থেকে ভেতরের দিকে ইংরেজি 'V' অক্ষরের মতো হলুদ দাগ তৈরি হয় এবং পাতার শিরাগুলো কালো হয়ে যায়।",
            "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. campestris) ব্যাকটেরিয়া।",
            "solution_bn": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Black_Rot",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_black_rot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কপির ব্লাক রট রোগ (Black Rot) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_black_rot_02",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Black_Rot",
    diseaseBn: "কপির ব্লাক রট রোগ (Black Rot)",
    diseaseEn: "Cabbage Black Rot",
    targetClass: "Cabbage__Black_Rot",
    confidence: 99.8,
    imageSrc: "/samples/brassica/brassica_black_rot_02.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Black_Rot",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "কপির ব্লাক রট রোগ (Cabbage Black Rot)",
            "description_bn": "পাতার কিনারা থেকে ভেতরের দিকে ইংরেজি 'V' অক্ষরের মতো হলুদ দাগ তৈরি হয় এবং পাতার শিরাগুলো কালো হয়ে যায়।",
            "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. campestris) ব্যাকটেরিয়া।",
            "solution_bn": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Black_Rot",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_black_rot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কপির ব্লাক রট রোগ (Black Rot) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_black_rot_03",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Black_Rot",
    diseaseBn: "কপির ব্লাক রট রোগ (Black Rot)",
    diseaseEn: "Cabbage Black Rot",
    targetClass: "Cabbage__Black_Rot",
    confidence: 99.8,
    imageSrc: "/samples/brassica/brassica_black_rot_03.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Black_Rot",
      "disease_confidence": 0.998,
      "boxes": [],
      "disease_info": {
            "name_bn": "কপির ব্লাক রট রোগ (Cabbage Black Rot)",
            "description_bn": "পাতার কিনারা থেকে ভেতরের দিকে ইংরেজি 'V' অক্ষরের মতো হলুদ দাগ তৈরি হয় এবং পাতার শিরাগুলো কালো হয়ে যায়।",
            "cause_bn": "জ্যান্থোমোনাস ক্যাম্পোস্ট্রিস (Xanthomonas campestris pv. campestris) ব্যাকটেরিয়া।",
            "solution_bn": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Black_Rot",
                  "confidence": 0.998
            }
      ],
      "treatment_advice": "রোগমুক্ত প্রত্যয়িত বীজ ব্যবহার করুন। কপার অক্সিক্লোরাইড (২ গ্রাম/লিটার) এবং স্ট্রেপ্টোমাইসিন সালফেট স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_black_rot_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "কপির ব্লাক রট রোগ (Black Rot) [99.8%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_downy_mildew_01",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Downy_Mildew",
    diseaseBn: "ডাউনি মিলডিউ (Downy Mildew)",
    diseaseEn: "Cabbage Downy Mildew",
    targetClass: "Cabbage__Downy_Mildew",
    confidence: 99.7,
    imageSrc: "/samples/brassica/brassica_downy_mildew_01.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Downy_Mildew",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "কপির ডাউনি মিলডিউ (Downy Mildew)",
            "description_bn": "পাতার উপরের পৃষ্ঠে কৌণিক হলুদ ছোপ এবং ঠিক নিচের পিঠে সাদাটে বা ধূসর রোমশ ছত্রাকের জাল দেখা যায়।",
            "cause_bn": "হায়ালোপারোনোস্পোরা ব্রাসিকি (Hyaloperonospora brassicae)। ঠান্ডা ও শিশিরভেজা কুয়াশা।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। মেটাল্যাক্সিল + ম্যানকোজেব (রিডোমিল গোল্ড ২ গ্রাম/লিটার) স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Downy_Mildew",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। মেটাল্যাক্সিল + ম্যানকোজেব (রিডোমিল গোল্ড ২ গ্রাম/লিটার) স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_downy_mildew_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ডাউনি মিলডিউ (Downy Mildew) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_downy_mildew_02",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Downy_Mildew",
    diseaseBn: "ডাউনি মিলডিউ (Downy Mildew)",
    diseaseEn: "Cabbage Downy Mildew",
    targetClass: "Cabbage__Downy_Mildew",
    confidence: 99.7,
    imageSrc: "/samples/brassica/brassica_downy_mildew_02.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Downy_Mildew",
      "disease_confidence": 0.997,
      "boxes": [],
      "disease_info": {
            "name_bn": "কপির ডাউনি মিলডিউ (Downy Mildew)",
            "description_bn": "পাতার উপরের পৃষ্ঠে কৌণিক হলুদ ছোপ এবং ঠিক নিচের পিঠে সাদাটে বা ধূসর রোমশ ছত্রাকের জাল দেখা যায়।",
            "cause_bn": "হায়ালোপারোনোস্পোরা ব্রাসিকি (Hyaloperonospora brassicae)। ঠান্ডা ও শিশিরভেজা কুয়াশা।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। মেটাল্যাক্সিল + ম্যানকোজেব (রিডোমিল গোল্ড ২ গ্রাম/লিটার) স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Downy_Mildew",
                  "confidence": 0.997
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। মেটাল্যাক্সিল + ম্যানকোজেব (রিডোমিল গোল্ড ২ গ্রাম/লিটার) স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_downy_mildew_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ডাউনি মিলডিউ (Downy Mildew) [99.7%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_cauliflower_alternaria_01",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Cauliflower_Alternaria",
    diseaseBn: "ফুলকপির অল্টারনারিয়া রোগ",
    diseaseEn: "Cauliflower Alternaria Disease",
    targetClass: "Cauliflower__Alternaria_Disease",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_cauliflower_alternaria_01.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cauliflower_Alternaria",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ফুলকপির অল্টারনারিয়া রোগ (Cauliflower Alternaria)",
            "description_bn": "পাতায় বাদামী রিং দাগ এবং ফুলকপির মাথায় বাদামী বা কালো দাগ পড়ে পণ্যের মান নষ্ট করে।",
            "cause_bn": "অল্টারনারিয়া ছত্রাকের আক্রমণ। অপরিচ্ছন্ন জমি ও আর্দ্র আবহাওয়ায় বিস্তার লাভ করে।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cauliflower_Alternaria",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_cauliflower_alternaria_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ফুলকপির অল্টারনারিয়া রোগ [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_cauliflower_alternaria_02",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Cauliflower_Alternaria",
    diseaseBn: "ফুলকপির অল্টারনারিয়া রোগ",
    diseaseEn: "Cauliflower Alternaria Disease",
    targetClass: "Cauliflower__Alternaria_Disease",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_cauliflower_alternaria_02.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cauliflower_Alternaria",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ফুলকপির অল্টারনারিয়া রোগ (Cauliflower Alternaria)",
            "description_bn": "পাতায় বাদামী রিং দাগ এবং ফুলকপির মাথায় বাদামী বা কালো দাগ পড়ে পণ্যের মান নষ্ট করে।",
            "cause_bn": "অল্টারনারিয়া ছত্রাকের আক্রমণ। অপরিচ্ছন্ন জমি ও আর্দ্র আবহাওয়ায় বিস্তার লাভ করে।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cauliflower_Alternaria",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_cauliflower_alternaria_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ফুলকপির অল্টারনারিয়া রোগ [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_cauliflower_alternaria_03",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Cauliflower_Alternaria",
    diseaseBn: "ফুলকপির অল্টারনারিয়া রোগ",
    diseaseEn: "Cauliflower Alternaria Disease",
    targetClass: "Cauliflower__Alternaria_Disease",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_cauliflower_alternaria_03.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cauliflower_Alternaria",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "ফুলকপির অল্টারনারিয়া রোগ (Cauliflower Alternaria)",
            "description_bn": "পাতায় বাদামী রিং দাগ এবং ফুলকপির মাথায় বাদামী বা কালো দাগ পড়ে পণ্যের মান নষ্ট করে।",
            "cause_bn": "অল্টারনারিয়া ছত্রাকের আক্রমণ। অপরিচ্ছন্ন জমি ও আর্দ্র আবহাওয়ায় বিস্তার লাভ করে।",
            "solution_bn": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cauliflower_Alternaria",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "আক্রান্ত পাতা অপসারণ করুন। ডাইফেনোকোনাজল (যেমন স্কোর ২৫০ ইসি) প্রতি লিটারে ০.৫ মিলি স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_cauliflower_alternaria_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ফুলকপির অল্টারনারিয়া রোগ [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_cauliflower_bacterial_spot_01",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Cauliflower_Bacterial_Spot",
    diseaseBn: "ফুলকপির ব্যাকটেরিয়াল দাগ",
    diseaseEn: "Cauliflower Bacterial Spot",
    targetClass: "Cauliflower__Bacterial_Spot",
    confidence: 99.6,
    imageSrc: "/samples/brassica/brassica_cauliflower_bacterial_spot_01.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cauliflower_Bacterial_Spot",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "ফুলকপির ব্যাকটেরিয়াল দাগ (Cauliflower Bacterial Spot)",
            "description_bn": "পাতায় ছোট ছোট কালচে কৌণিক পানির মতো দাগ তৈরি হয় যা দ্রুত বাদামী বা কালো ক্ষতে রূপ নেয়।",
            "cause_bn": "সিউডোমোনাস বা জ্যান্থোমোনাস ব্যাকটেরিয়া। ভারী বৃষ্টি ও অপরিচ্ছন্ন জমি।",
            "solution_bn": "সুষম সার দিন ও জলাবদ্ধতা দূর করুন। কপার হাইড্রোক্সাইড বা কপার অক্সিক্লোরাইড স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cauliflower_Bacterial_Spot",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "সুষম সার দিন ও জলাবদ্ধতা দূর করুন। কপার হাইড্রোক্সাইড বা কপার অক্সিক্লোরাইড স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_cauliflower_bacterial_spot_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ফুলকপির ব্যাকটেরিয়াল দাগ [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_cauliflower_bacterial_spot_02",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Cauliflower_Bacterial_Spot",
    diseaseBn: "ফুলকপির ব্যাকটেরিয়াল দাগ",
    diseaseEn: "Cauliflower Bacterial Spot",
    targetClass: "Cauliflower__Bacterial_Spot",
    confidence: 99.6,
    imageSrc: "/samples/brassica/brassica_cauliflower_bacterial_spot_02.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "diagnosed",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Cauliflower_Bacterial_Spot",
      "disease_confidence": 0.996,
      "boxes": [],
      "disease_info": {
            "name_bn": "ফুলকপির ব্যাকটেরিয়াল দাগ (Cauliflower Bacterial Spot)",
            "description_bn": "পাতায় ছোট ছোট কালচে কৌণিক পানির মতো দাগ তৈরি হয় যা দ্রুত বাদামী বা কালো ক্ষতে রূপ নেয়।",
            "cause_bn": "সিউডোমোনাস বা জ্যান্থোমোনাস ব্যাকটেরিয়া। ভারী বৃষ্টি ও অপরিচ্ছন্ন জমি।",
            "solution_bn": "সুষম সার দিন ও জলাবদ্ধতা দূর করুন। কপার হাইড্রোক্সাইড বা কপার অক্সিক্লোরাইড স্প্রে করুন।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Cauliflower_Bacterial_Spot",
                  "confidence": 0.996
            }
      ],
      "treatment_advice": "সুষম সার দিন ও জলাবদ্ধতা দূর করুন। কপার হাইড্রোক্সাইড বা কপার অক্সিক্লোরাইড স্প্রে করুন।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_cauliflower_bacterial_spot_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "ফুলকপির ব্যাকটেরিয়াল দাগ [99.6%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_healthy_01",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Healthy",
    diseaseBn: "সুস্থ ফুলকপি পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Cauliflower__Healthy",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_healthy_01.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ফুলকপি পাতা (Healthy)",
            "description_bn": "মোমের মতো চকচকে অক্ষত পাতা, স্বাস্থ্যবান বর্ধনশীল কুঁড়ি ও চমৎকার গঠন।",
            "cause_bn": "সঠিক জমি তৈরি, বোরণ ও মলিবডেনাম পুষ্টি এবং নিয়ন্ত্রিত সেচ।",
            "solution_bn": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_healthy_01 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ফুলকপি পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_healthy_02",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Healthy",
    diseaseBn: "সুস্থ ফুলকপি পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Cauliflower__Healthy",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_healthy_02.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ফুলকপি পাতা (Healthy)",
            "description_bn": "মোমের মতো চকচকে অক্ষত পাতা, স্বাস্থ্যবান বর্ধনশীল কুঁড়ি ও চমৎকার গঠন।",
            "cause_bn": "সঠিক জমি তৈরি, বোরণ ও মলিবডেনাম পুষ্টি এবং নিয়ন্ত্রিত সেচ।",
            "solution_bn": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_healthy_02 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ফুলকপি পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
  {
    id: "brassica_healthy_03",
    crop: "Brassica",
    cropBn: "কপি ও সরিষা",
    cropEn: "Brassica",
    disease: "Healthy",
    diseaseBn: "সুস্থ ফুলকপি পাতা (Healthy Leaf)",
    diseaseEn: "Healthy Leaf",
    targetClass: "Cauliflower__Healthy",
    confidence: 100.0,
    imageSrc: "/samples/brassica/brassica_healthy_03.jpg",
    cropHint: "Brassica",
    cachedResult: {
      "status": "healthy",
      "detection_mode": "classification",
      "crop": "Brassica",
      "crop_confidence": 1.0,
      "crop_source": "user",
      "disease": "Healthy",
      "disease_confidence": 1.0,
      "boxes": [],
      "disease_info": {
            "name_bn": "সুস্থ ফুলকপি পাতা (Healthy)",
            "description_bn": "মোমের মতো চকচকে অক্ষত পাতা, স্বাস্থ্যবান বর্ধনশীল কুঁড়ি ও চমৎকার গঠন।",
            "cause_bn": "সঠিক জমি তৈরি, বোরণ ও মলিবডেনাম পুষ্টি এবং নিয়ন্ত্রিত সেচ।",
            "solution_bn": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।"
      },
      "top3_crops": [
            {
                  "class": "Brassica",
                  "confidence": 1.0
            }
      ],
      "top3_diseases": [
            {
                  "class": "Healthy",
                  "confidence": 1.0
            }
      ],
      "treatment_advice": "মাটি আর্দ্র রাখুন তবে গোড়ায় পানি জমতে দেবেন না। কোনো বালাইনাশকের প্রয়োজন নেই।",
      "treatment_confidence": "high",
      "treatment_sources": [
            "BARI/BRRI Verified Guide",
            "KrishokChat Evaluation Benchmark"
      ],
      "verifier_flags": [],
      "agent_trace": [
            {
                  "stage": "intake",
                  "status": "complete",
                  "detail": "Specimen: brassica_healthy_03 (Edge CDN)"
            },
            {
                  "stage": "crop_classification",
                  "status": "complete",
                  "detail": "কপি ও সরিষা (Brassica)"
            },
            {
                  "stage": "disease_classification",
                  "status": "complete",
                  "detail": "সুস্থ ফুলকপি পাতা (Healthy Leaf) [100.0%]"
            },
            {
                  "stage": "advisory",
                  "status": "complete",
                  "detail": "BARI/BRRI Verified Prescription"
            }
      ],
      "quality_warnings": []
},
  },
];
