"use client";

import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from "react";
import { TRANSLATIONS, type Locale, type Translations } from "@/lib/i18n/translations";
import { bn, bnPercent, humanizeLabel, translateDiseaseToBn, cropBn } from "@/lib/bn";
import { getLocalizedDisease } from "@/lib/i18n/disease-knowledge";

const STORAGE_KEY = "krishokchat:locale:v1";

interface LanguageContextValue {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  toggleLocale: () => void;
  t: Translations;
  formatNumber: (value: number | string) => string;
  formatPercent: (confidence: number) => string;
  formatPercent1: (confidence: number) => string;
  localizeCrop: (crop: string | null | undefined) => string;
  localizeDisease: (disease: string | null | undefined) => string;
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("bn");

  // Hydrate locale from storage on mount
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY) as Locale | null;
      if (saved === "en" || saved === "bn") {
        setLocaleState(saved);
        document.documentElement.lang = saved;
        document.documentElement.setAttribute("data-lang", saved);
      }
    } catch {
      // localStorage may be unavailable
    }
  }, []);

  const setLocale = useCallback((newLocale: Locale) => {
    setLocaleState(newLocale);
    try {
      window.localStorage.setItem(STORAGE_KEY, newLocale);
      document.documentElement.lang = newLocale;
      document.documentElement.setAttribute("data-lang", newLocale);
    } catch {
      // Storage unavailable
    }
  }, []);

  const toggleLocale = useCallback(() => {
    const next = locale === "bn" ? "en" : "bn";
    setLocale(next);
  }, [locale, setLocale]);

  const formatNumber = useCallback(
    (value: number | string): string => {
      if (locale === "bn") return bn(value);
      return String(value);
    },
    [locale]
  );

  const formatPercent = useCallback(
    (confidence: number): string => {
      if (locale === "bn") return bnPercent(confidence);
      return `${Math.round(confidence * 100)}%`;
    },
    [locale]
  );

  const formatPercent1 = useCallback(
    (confidence: number): string => {
      if (locale === "bn") return bn((confidence * 100).toFixed(1)) + "%";
      return `${(confidence * 100).toFixed(1)}%`;
    },
    [locale]
  );

  const localizeCrop = useCallback(
    (crop: string | null | undefined): string => {
      if (!crop) return "";
      const lower = crop.toLowerCase().trim();
      if (locale === "bn") return cropBn(crop);

      const EN_MAP: Record<string, string> = {
        rice: "Rice",
        wheat: "Wheat",
        corn: "Corn",
        potato: "Potato",
        brassica: "Cabbage / Cauliflower",
        chilli: "Chilli",
        chili: "Chilli",
        tomato: "Tomato",
        eggplant: "Eggplant",
        cabbage: "Cabbage",
        cauliflower: "Cauliflower",
      };
      return EN_MAP[lower] ?? crop.charAt(0).toUpperCase() + crop.slice(1);
    },
    [locale]
  );

  const localizeDisease = useCallback(
    (disease: string | null | undefined): string => {
      if (!disease) return "";
      if (locale === "bn") return translateDiseaseToBn(disease);

      const info = getLocalizedDisease(disease, "en");
      if (info?.nameEn) return info.nameEn;

      return humanizeLabel(disease);
    },
    [locale]
  );

  const value = useMemo(
    () => ({
      locale,
      setLocale,
      toggleLocale,
      t: TRANSLATIONS[locale],
      formatNumber,
      formatPercent,
      formatPercent1,
      localizeCrop,
      localizeDisease,
    }),
    [locale, setLocale, toggleLocale, formatNumber, formatPercent, formatPercent1, localizeCrop, localizeDisease]
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage(): LanguageContextValue {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    // Fallback if rendered outside provider
    return {
      locale: "bn",
      setLocale: () => {},
      toggleLocale: () => {},
      t: TRANSLATIONS.bn,
      formatNumber: (v) => bn(v),
      formatPercent: (c) => bnPercent(c),
      formatPercent1: (c) => bn((c * 100).toFixed(1)) + "%",
      localizeCrop: (c) => cropBn(c),
      localizeDisease: (d) => translateDiseaseToBn(d ?? ""),
    };
  }
  return ctx;
}
