export type Locale = "bn" | "en";

export interface Translations {
  // Navigation
  nav: {
    home: string;
    detect: string;
    soil: string;
    chat: string;
    library: string;
    project: string;
    otherPages: string;
    analytics: string;
    analyticsDesc: string;
    research: string;
    researchDesc: string;
    business: string;
    businessDesc: string;
    data: string;
    dataDesc: string;
    about: string;
    aboutDesc: string;
    team: string;
    teamDesc: string;
    contact: string;
    contactDesc: string;
    screencast: string;
    screencastDesc: string;
    menu: string;
    sunlightOn: string;
    sunlightOff: string;
    sunlightTitle: string;
    langToggleTitle: string;
    langBadge: string;
    login: string;
    signedIn: string;
    logout: string;
    callCenter: string;
    helplineTitle: string;
  };

  // Footer
  footer: {
    tagline: string;
    researchPrototype: string;
    services: string;
    research: string;
    organization: string;
    resources: string;
    agriHelpline: string;
    emergency: string;
    privacy: string;
    copyright: string;
  };

  // Detect Page
  detect: {
    subtitle: string;
    title: string;
    systemOnline: string;
    offline: string;
    offlineNotice: string;
    classificationMode: string;
    pageDescription: string;
    cropLabel: string;
    cropAuto: string;
    cropRice: string;
    cropWheat: string;
    cropCorn: string;
    cropPotato: string;
    cropBrassica: string;
    cropChilli: string;
    cropHintHelp: string;
    dropTitle: string;
    dropPrompt: string;
    dropSpecs: string;
    dropReady: string;
    changePhoto: string;
    runDiagnosis: string;
    preparingImage: string;
    analyzingImage: string;
    cancel: string;
    tryAgain: string;
    invalidType: string;
    sizeExceeded: string;
    prepFailed: string;
    sampleUnavailable: string;
    serverUnreachable: string;
    analysisFailed: string;
    pipelineTitle: string;
    pipelineSubtitle: string;
    viewfinderTitle: string;
    viewfinderOpen: string;
    viewfinderClose: string;
    viewfinderCenter: string;
    viewfinderDaylight: string;
    viewfinderDistance: string;
    viewfinderSingleLeaf: string;
    cropsCoverage: string;
  };

  // Reviewer Test Samples
  samples: {
    title: string;
    subtitle: string;
    badge: string;
    loadButton: string;
    loading: string;
    selectedLabel: string;
    confidenceLabel: string;
    allCrops: string;
    searchPlaceholder: string;
    prev: string;
    next: string;
    random: string;
    diagnoseNow: string;
    reviewerNote: string;
    modelsLink: string;
  };

  // Diagnosis Card
  diagnosis: {
    resultsTitle: string;
    clear: string;
    cropConfidence: string;
    diseaseConfidence: string;
    selectedCrop: string;
    routedBySelection: string;
    description: string;
    cause: string;
    primarySolution: string;
    healthyTitle: string;
    healthyDesc: string;
    healthyDetected: string;
    healthyCare: string;
    uncertainTitle: string;
    uncertainDesc: string;
    uncertainRoute: string;
    secondImageTitle: string;
    secondImageDesc: string;
    outOfDistTitle: string;
    outOfDistDesc: string;
    notRecognizedTitle: string;
    notRecognizedDesc: string;
    nextSteps: string;
    stepCloserPhoto: string;
    stepCallHelpline: string;
    noModelTitle: string;
    noModelDesc: string;
    modelErrorTitle: string;
    modelErrorDesc: string;
  };

  // Treatment Card
  treatment: {
    actionPlan: string;
    prescriptionButton: string;
    dosageCalculator: string;
    sourcesTitle: string;
    askFollowUp: string;
    preHarvestInterval: string;
    readAloud: string;
    stopReading: string;
    audioNotSupported: string;
  };

  // Chat Page
  chat: {
    farmerSupport: string;
    title: string;
    description: string;
    safetyVerified: string;
    liveResponse: string;
    bilingualSupport: string;
    asideGuide: string;
    asideTitle: string;
    safetyFirst: string;
    safetyDesc: string;
    groundedInfo: string;
    groundedDesc: string;
    verifiedSources: string;
    verifiedDesc: string;
    startWithPhoto: string;
  };

  // Soil Page
  soil: {
    subtitle: string;
    title: string;
    pageDescription: string;
    datasetShowcase: string;
    lockedTitle: string;
    lockedDesc: string;
  };
}

export const TRANSLATIONS: Record<Locale, Translations> = {
  bn: {
    nav: {
      home: "হোম",
      detect: "রোগ নির্ণয়",
      soil: "মাটি ও সেচ",
      chat: "কৃষি পরামর্শ",
      library: "লাইব্রেরি",
      project: "প্রকল্প",
      otherPages: "অন্যান্য পৃষ্ঠা ও গবেষণা",
      analytics: "লাইভ পরিসংখ্যান",
      analyticsDesc: "এজেন্ট সিদ্ধান্ত ও স্থানীয় অডিট",
      research: "গবেষণা ও ফলাফল",
      researchDesc: "পেপার, বেঞ্চমার্ক ও নিরাপত্তা ফ্রেমওয়ার্ক",
      business: "ব্যবসায়িক মডেল",
      businessDesc: "টেকসই অর্থনৈতিক রূপরেখা ও অংশীদারিত্ব",
      data: "উপাত্ত ও নলেজ গ্রাফ",
      dataDesc: "উন্মুক্ত ডেটাসেট ও জ্ঞানভাণ্ডার",
      about: "প্রকল্প পরিচিতি",
      aboutDesc: "উদ্দেশ্য ও সহযোগী প্রতিষ্ঠান",
      team: "গবেষক দল",
      teamDesc: "গবেষণা দল ও মাঠ পর্যায়ের কাজ",
      contact: "সাহায্য ও যোগাযোগ",
      contactDesc: "সরকারি হেল্পলাইন ও পরামর্শ",
      screencast: "ভিডিও স্ক্রিনকাস্ট",
      screencastDesc: "লাইভ সিস্টেম ডেমো ও ফিচার ওয়াকথ্রু",
      menu: "মেনু",
      sunlightOn: "মাঠের মোড অন",
      sunlightOff: "মাঠের মোড",
      sunlightTitle: "মাঠের মোড / তীব্র রোদের স্পষ্ট দৃশ্যমানতা (Sunlight Mode)",
      langToggleTitle: "Switch to English",
      langBadge: "বাং",
      login: "লগইন / নিবন্ধন",
      signedIn: "সাইন-ইন করা আছে",
      logout: "লগ আউট",
      callCenter: "কৃষি কল সেন্টার",
      helplineTitle: "কৃষি কল সেন্টার — জাতীয় কৃষি হেল্পলাইন",
    },
    footer: {
      tagline: "বাংলাদেশের কৃষকদের জন্য নির্ভরযোগ্য এআই কৃষি পরামর্শদাতা",
      researchPrototype: "গবেষণা প্রোটোটাইপ — CC-BY-4.0",
      services: "সেবাসমূহ",
      research: "গবেষণা",
      organization: "প্রতিষ্ঠান ও দল",
      resources: "সম্পদ",
      agriHelpline: "কৃষি হেল্পলাইন",
      emergency: "জরুরি",
      privacy: "গোপনীয়তা নীতি · Privacy",
      copyright: "North South University",
    },
    detect: {
      subtitle: "ছবির মাধ্যমে ফসল পরামর্শ",
      title: "ফসলের রোগ নির্ণয়",
      systemOnline: "সিস্টেম অনলাইন",
      offline: "অফলাইন",
      offlineNotice: "ইন্টারনেট সংযোগ নেই। ছবি ও লেখা এই পর্দায় থাকবে; সংযোগ এলে আবার চেষ্টা করুন।",
      classificationMode: "শ্রেণিবিন্যাস মোড",
      pageDescription: "পাতার ছবি দিন — ফসল ও রোগ ডিভাইসেই শনাক্ত হবে — এরপর অনুমোদিত উৎস থেকে চিকিৎসা-পরামর্শ দেখানো হবে।",
      cropLabel: "ফসল",
      cropAuto: "অটো — মডেল শনাক্ত করবে",
      cropRice: "ধান",
      cropWheat: "গম",
      cropCorn: "ভুট্টা",
      cropPotato: "আলু",
      cropBrassica: "বাঁধাকপি / ফুলকপি",
      cropChilli: "মরিচ",
      cropHintHelp: "এই ফসলের রোগ মডেল দিয়ে বিশ্লেষণ হবে",
      dropTitle: "পাতার ছবি দিন",
      dropPrompt: "টানে দিন বা ক্লিক করুন",
      dropSpecs: "JPEG · PNG · WebP · সর্বোচ্চ ৫MB",
      dropReady: "ছবি ছেড়ে দিন",
      changePhoto: "পরিবর্তন",
      runDiagnosis: "নির্ণয় করুন",
      preparingImage: "ছবি ছোট করে প্রস্তুত হচ্ছে…",
      analyzingImage: "বিশ্লেষণ হচ্ছে…",
      cancel: "বাতিল",
      tryAgain: "আবার চেষ্টা করুন",
      invalidType: "শুধু JPEG, PNG বা WebP ছবি দিন।",
      sizeExceeded: "ছবিটি ৫MB-এর ছোট হতে হবে।",
      prepFailed: "ছবিটি প্রস্তুত করা যায়নি।",
      sampleUnavailable: "নমুনা ছবিটি এখন পাওয়া যাচ্ছে না। নিজের ছবি আপলোড করুন।",
      serverUnreachable: "সার্ভারে পৌঁছানো যায়নি। নেটওয়ার্ক দেখে আবার চেষ্টা করুন।",
      analysisFailed: "ছবিটি বিশ্লেষণ করা যায়নি। একই ছবি আবার দিন বা নতুন ছবি তুলুন।",
      pipelineTitle: "রোগ বিশ্লেষণ প্রবাহ",
      pipelineSubtitle: "ছবি থেকে শ্রেণিবিন্যাস ও grounded advisory তৈরি হচ্ছে",
      viewfinderTitle: "সঠিক ছবি তোলার সহায়িকা (ভিউফাইন্ডার গাইড)",
      viewfinderOpen: "সংক্ষিপ্ত করুন ▲",
      viewfinderClose: "দেখুন ▼",
      viewfinderCenter: "আক্রান্ত অংশ কেন্দ্রে রাখুন",
      viewfinderDaylight: "দিনের আলো: ছায়া বা অতিরিক্ত ফ্ল্যাশ এড়িয়ে সরাসরি স্বাভাবিক আলোতে ছবি তুলুন।",
      viewfinderDistance: "দূরত্ব: পাতা থেকে ১৫–২০ সেন্টিমিটার দূরত্বে ক্যামেরা স্থির রেখে তুলুন।",
      viewfinderSingleLeaf: "একক পাতা: পুরো গাছের বদলে আক্রান্ত একটি পাতার ক্ষত পরিষ্কারভাবে ফ্রেমে রাখুন।",
      cropsCoverage: "৬টি প্রধান ফসলে অপ্টিমাইজড — ধান · আলু · বাঁধাকপি · ভুট্টা · গম · মরিচ",
    },
    samples: {
      title: "যাচাইকৃত কেস",
      subtitle: "প্রকাশিত পরীক্ষার ছবি",
      badge: "১০০টি কেস",
      loadButton: "শুধু ছবি দেখুন",
      loading: "লোড হচ্ছে…",
      selectedLabel: "নির্বাচিত:",
      confidenceLabel: "রেকর্ড করা নিশ্চিততা",
      allCrops: "সব",
      searchPlaceholder: "রোগ বা ফসল খুঁজুন",
      prev: "পূর্ববর্তী",
      next: "পরবর্তী",
      random: "যেকোনো",
      diagnoseNow: "রেকর্ড করা ফল দেখুন",
      reviewerNote: "এই ডেমোতে মডেল সার্ভার দেওয়া হয়নি। একটি কেস চালালে প্রকাশিত ছবির আগে থেকে রাখা ফল দেখায় — মডেল আবার চলে না। ওজন:",
      modelsLink: "Hugging Face",
    },
    diagnosis: {
      resultsTitle: "বিশ্লেষণের ফলাফল",
      clear: "মুছুন",
      cropConfidence: "ফসল নিশ্চিতা",
      diseaseConfidence: "রোগ নিশ্চিতা",
      selectedCrop: "নির্বাচিত",
      routedBySelection: "আপনার নির্বাচন অনুযায়ী রোগ মডেল দিয়ে বিশ্লেষণ হয়েছে",
      description: "বিবরণ ও লক্ষণ",
      cause: "আক্রমণের কারণ ও বিস্তার",
      primarySolution: "প্রাথমিক সতর্কতা ও ব্যবস্থা",
      healthyTitle: "আপনার ফসল সুস্থ!",
      healthyDesc: "পাতায় কোনো রোগের লক্ষণ পাওয়া যায়নি।",
      healthyDetected: "শনাক্ত ফসল:",
      healthyCare: "নিয়মিত পরিচর্যা চালিয়ে যান। সাময়িক পরিদর্শন ফসল সুস্থ রাখে।",
      uncertainTitle: "সঠিক ফসল চিহ্নিত করতে পারেননি?",
      uncertainDesc: "মডেল লক্ষণ দেখে একাধিক ফসলের সম্ভাবনা দেখতে পাচ্ছে:",
      uncertainRoute: "আপনার ফসলটি বেছে নিলে সঠিক রোগ মডেল দিয়ে সঙ্গে সঙ্গে বিশ্লেষণ করা হবে।",
      secondImageTitle: "আরও স্পষ্ট ছবি প্রয়োজন",
      secondImageDesc: "পাতার লক্ষণটি পরিষ্কার বোঝা যাচ্ছে না। আরেকটু কাছ থেকে পরিষ্কার আলোতে ছবি দিন।",
      outOfDistTitle: "অসমর্থিত অথবা অপরিচিত পাতা",
      outOfDistDesc: "এই পাতাটি আমাদের সমর্থিত ৬টি প্রধান ফসলের তালিকায় নেই।",
      notRecognizedTitle: "আমি নিশ্চিত নই",
      notRecognizedDesc: "ফসল/রোগ নির্ণয়ে নিশ্চিততা কম।",
      nextSteps: "পরবর্তী পদক্ষেপ:",
      stepCloserPhoto: "১. আরও পরিষ্কার, কাছের ছবি দিন — দিনের আলোতে, পাতা ভরে ফ্রেমে।",
      stepCallHelpline: "২. কৃষক কল সেন্টারে যোগাযোগ করুন",
      noModelTitle: "এই ফসলের রোগ মডেল এখনো প্রস্তুত হচ্ছে",
      noModelDesc: "খুব শীঘ্রই এই ফসলের রোগ শনাক্তকরণ মডেল উন্মুক্ত করা হবে।",
      modelErrorTitle: "বিশ্লেষণ সম্পন্ন করা যায়নি",
      modelErrorDesc: "মডেল বিশ্লেষণে সাময়িক সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
    },
    treatment: {
      actionPlan: "এখন কী করবেন",
      prescriptionButton: "প্রেসক্রিপশন প্রিন্ট",
      dosageCalculator: "স্প্রে পরিমাপক",
      sourcesTitle: "উৎসসমূহ",
      askFollowUp: "এই বিষয়ে চ্যাটে আরও জানুন",
      preHarvestInterval: "নিরাপদ অপেক্ষমাণ সময়: বালাইনাশক স্প্রে করার পর কমপক্ষে ৭ থেকে ১৪ দিন ফসল তোলা বন্ধ রাখুন।",
      readAloud: "পড়ে শুনুন",
      stopReading: "থামান",
      audioNotSupported: "অডিও সমর্থন নেই",
    },
    chat: {
      farmerSupport: "কৃষকের সহায়তা",
      title: "কৃষি পরামর্শ চ্যাট",
      description: "বাংলা বা ইংরেজিতে আপনার ফসলের কথা লিখুন। উত্তর দেওয়ার আগে জাতীয় কৃষি গবেষণা উৎস ও নিরাপত্তা যাচাই করা হবে।",
      safetyVerified: "নিরাপত্তা যাচাই",
      liveResponse: "লাইভ উত্তর",
      bilingualSupport: "দ্বিভাষিক সহায়তা",
      asideGuide: "নির্দেশিকা",
      asideTitle: "উত্তর কীভাবে তৈরি হয়",
      safetyFirst: "নিরাপত্তা আগে",
      safetyDesc: "প্রশ্নের ঝুঁকি ও ক্ষতিকর রাসায়নিক যাচাই",
      groundedInfo: "প্রাসঙ্গিক তথ্য",
      groundedDesc: "প্রি-কম্পিউটেড জাতীয় জ্ঞানভাণ্ডার",
      verifiedSources: "উৎস মিলিয়ে",
      verifiedDesc: "দাবি যাচাই ও গবেষণা সাইটেশন",
      startWithPhoto: "ছবি দিয়ে শুরু করুন",
    },
    soil: {
      subtitle: "মাটির আর্দ্রতা ও সেচ ব্যবস্থাপনা",
      title: "মাটি ও সেচ কনসোল",
      pageDescription: "মাটির ছবি বিশ্লেষণ করে টেনসিওমিটার রিডিং এবং সেচ সময়সূচী নির্ধারণ।",
      datasetShowcase: "মাটির উপাত্ত সংগ্রহ",
      lockedTitle: "মডেল ক্যালিব্রেশন চলছে",
      lockedDesc: "মাটির আর্দ্রতা মডেল বর্তমানে নতুন মাঠ উপাত্তে সমন্বয় করা হচ্ছে।",
    },
  },
  en: {
    nav: {
      home: "Home",
      detect: "Disease Detection",
      soil: "Soil & Irrigation",
      chat: "Agri Advisory",
      library: "Library",
      project: "Project",
      otherPages: "Other Pages & Research",
      analytics: "Live Analytics",
      analyticsDesc: "Agent Decisions & Local Audits",
      research: "Research & Results",
      researchDesc: "Papers, Benchmarks & Safety Framework",
      business: "Business Model",
      businessDesc: "Sustainable Economics & Partnerships",
      data: "Data & Knowledge Graph",
      dataDesc: "Open Datasets & Knowledge Base",
      about: "About Project",
      aboutDesc: "Mission & Partner Institutions",
      team: "Research Team",
      teamDesc: "Research Team & Field Deployments",
      contact: "Help & Contact",
      contactDesc: "Government Helpline & Inquiries",
      screencast: "Video Screencast",
      screencastDesc: "Live System Demo & Feature Walkthrough",
      menu: "Menu",
      sunlightOn: "Sunlight On",
      sunlightOff: "Sunlight Mode",
      sunlightTitle: "Sunlight Mode (High Contrast for Outdoor Field Visibility)",
      langToggleTitle: "বাংলায় পরিবর্তন করুন",
      langBadge: "EN",
      login: "Login / Register",
      signedIn: "Signed In",
      logout: "Log Out",
      callCenter: "Agri Call Center",
      helplineTitle: "Agri Call Center — National Agricultural Helpline",
    },
    footer: {
      tagline: "Evidence-Based & Safe Agricultural AI Advisory for Farmers",
      researchPrototype: "Research Prototype — CC-BY-4.0",
      services: "Services",
      research: "Research",
      organization: "Organization & Team",
      resources: "Resources",
      agriHelpline: "Agri Helpline",
      emergency: "Emergency",
      privacy: "Privacy Policy",
      copyright: "North South University",
    },
    detect: {
      subtitle: "Visual Crop Advisory",
      title: "Crop Disease Detection",
      systemOnline: "System Online",
      offline: "Offline",
      offlineNotice: "No internet connection. Uploaded image will stay on screen; retry once reconnected.",
      classificationMode: "Classification Mode",
      pageDescription: "Provide a leaf photograph — crop and disease are diagnosed directly on-device — followed by evidence-grounded treatment advisory.",
      cropLabel: "Crop",
      cropAuto: "Auto — Model Detects",
      cropRice: "Rice",
      cropWheat: "Wheat",
      cropCorn: "Corn",
      cropPotato: "Potato",
      cropBrassica: "Cabbage / Cauliflower",
      cropChilli: "Chilli",
      cropHintHelp: "Will be analyzed using disease models for this crop",
      dropTitle: "Upload Leaf Photograph",
      dropPrompt: "Drag & drop or click to browse",
      dropSpecs: "JPEG · PNG · WebP · Max 5MB",
      dropReady: "Drop leaf photo here",
      changePhoto: "Change Photo",
      runDiagnosis: "Run Diagnosis",
      preparingImage: "Optimizing image…",
      analyzingImage: "Analyzing leaf…",
      cancel: "Cancel",
      tryAgain: "Try Again",
      invalidType: "Please provide a JPEG, PNG, or WebP image file.",
      sizeExceeded: "Image size must be smaller than 5MB.",
      prepFailed: "Could not optimize image for processing.",
      sampleUnavailable: "Sample image temporarily unavailable. Please upload your own image.",
      serverUnreachable: "Could not reach the server. Please check your connection and retry.",
      analysisFailed: "Image analysis failed. Please try again or take a clearer photograph.",
      pipelineTitle: "Diagnostic Pipeline",
      pipelineSubtitle: "Running edge classification and synthesizing grounded advisory",
      viewfinderTitle: "Field Photography Guide (Viewfinder)",
      viewfinderOpen: "Collapse Guide ▲",
      viewfinderClose: "View Guide ▼",
      viewfinderCenter: "Center the affected lesion",
      viewfinderDaylight: "Daylight: Avoid harsh shadows or strong flash; photograph in clear natural daylight.",
      viewfinderDistance: "Distance: Hold camera steady at 15–20 cm distance from the leaf surface.",
      viewfinderSingleLeaf: "Single Leaf: Focus closely on one diseased leaf rather than the whole canopy.",
      cropsCoverage: "Optimized for 6 crops — Rice · Potato · Brassica · Corn · Wheat · Chilli",
    },
    samples: {
      title: "Verified cases",
      subtitle: "Published test images",
      badge: "100 cases",
      loadButton: "Preview image only",
      loading: "Loading…",
      selectedLabel: "Selected:",
      confidenceLabel: "Recorded confidence",
      allCrops: "All",
      searchPlaceholder: "Search disease or crop",
      prev: "Previous",
      next: "Next",
      random: "Any",
      diagnoseNow: "Show recorded result",
      reviewerNote: "This demo does not include a model server. Running a case replays the recorded result for that published test image and does not call the models. Weights:",
      modelsLink: "Hugging Face",
    },
    diagnosis: {
      resultsTitle: "Diagnostic Results",
      clear: "Clear",
      cropConfidence: "Crop Confidence",
      diseaseConfidence: "Disease Confidence",
      selectedCrop: "Selected",
      routedBySelection: "Analyzed using targeted disease models based on your crop selection",
      description: "Description & Symptoms",
      cause: "Cause & Disease Spread",
      primarySolution: "Primary Precautions & Immediate Action",
      healthyTitle: "Your Crop is Healthy!",
      healthyDesc: "No symptoms of pathogenic disease were detected on the leaf.",
      healthyDetected: "Identified Crop:",
      healthyCare: "Continue routine crop monitoring and balanced fertilization. Periodic inspection keeps plants resilient.",
      uncertainTitle: "Clarify Crop Identity",
      uncertainDesc: "Model observes visual features that could belong to multiple crops:",
      uncertainRoute: "Selecting your crop above will immediately route to the correct disease model.",
      secondImageTitle: "Clearer Photograph Required",
      secondImageDesc: "Lesion patterns are obscured or out of focus. Please capture a steady, well-lit close-up.",
      outOfDistTitle: "Unsupported Specimen",
      outOfDistDesc: "This leaf does not match the 6 crop families currently supported in the edge registry.",
      notRecognizedTitle: "Diagnosis Inconclusive",
      notRecognizedDesc: "Detection confidence is below clinical threshold.",
      nextSteps: "Recommended Next Steps:",
      stepCloserPhoto: "1. Capture a closer, clearer photo in daylight filling the frame.",
      stepCallHelpline: "2. Contact the National Agri Call Center directly",
      noModelTitle: "Disease Model In Preparation",
      noModelDesc: "Edge diagnostic models for this crop are currently being validated in field trials.",
      modelErrorTitle: "Analysis Incomplete",
      modelErrorDesc: "A processing exception occurred during inference. Please retry.",
    },
    treatment: {
      actionPlan: "Recommended Action Plan",
      prescriptionButton: "Prescription Slip",
      dosageCalculator: "Dosage Calculator",
      sourcesTitle: "Verified Evidence Sources",
      askFollowUp: "Ask KrishokTech for more details",
      preHarvestInterval: "Pre-Harvest Interval (PHI): Withhold harvesting for at least 7–14 days after pesticide application.",
      readAloud: "Read Aloud",
      stopReading: "Stop",
      audioNotSupported: "Audio not supported",
    },
    chat: {
      farmerSupport: "Farmer Support",
      title: "Agri Advisory Chat",
      description: "Ask your crop and soil questions in Bengali or English. Responses are rigorously verified against national agricultural research guidelines and safety boundaries.",
      safetyVerified: "Safety Verified",
      liveResponse: "Live Response",
      bilingualSupport: "Bilingual Support",
      asideGuide: "Guidelines",
      asideTitle: "How Answers Are Synthesized",
      safetyFirst: "Safety First",
      safetyDesc: "Pre-check against banned agrochemicals & toxic hazards",
      groundedInfo: "Grounded Knowledge",
      groundedDesc: "Pre-indexed national agronomy research repositories",
      verifiedSources: "Source Attributed",
      verifiedDesc: "Strict citation alignment and clinical verification",
      startWithPhoto: "Start with Leaf Photo",
    },
    soil: {
      subtitle: "Soil Moisture & Irrigation Console",
      title: "Soil & Irrigation Management",
      pageDescription: "Assess soil surface moisture, tensiometer tension readings, and irrigation schedules from field photographs.",
      datasetShowcase: "Soil Sample Registry",
      lockedTitle: "Model Calibration in Progress",
      lockedDesc: "Soil moisture estimation models are undergoing active recalibration with multi-district soil cores.",
    },
  },
};
