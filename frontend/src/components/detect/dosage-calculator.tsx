"use client";

import { useState, useMemo } from "react";
import { Calculator, Droplets, ShieldCheck, Phone } from "lucide-react";
import { HELPLINE } from "@/lib/constants";
import { toBn } from "@/lib/use-count-up";
import { cn } from "@/lib/utils";

/* =========================================================================
   DosageCalculator — Interactive Spray Tank & Land Dosage Calculator.
   
   Solves the #1 safety hazard in Bangladeshi agriculture:
   Farmers miscalculating powder/liquid chemical ratios per knapsack tank
   or per bigha/katha/decimal, causing crop burn or dangerous toxicity.
   ========================================================================= */

interface DosageCalculatorProps {
  defaultDosageText?: string | null;
  cropName?: string;
  diseaseName?: string;
}

// Preset standard sprayer knapsack tank capacities in Bangladesh
const TANK_PRESETS = [
  { liters: 10, label: "১০ লিটার", desc: "ছোট স্প্রেয়ার" },
  { liters: 16, label: "১৬ লিটার", desc: "স্ট্যান্ডার্ড ন্যাপস্যাক", standard: true },
  { liters: 20, label: "২০ লিটার", desc: "বড় ব্যাটারি স্প্রেয়ার" },
];

const LAND_UNITS = [
  { id: "shotok", name: "শতক / ডেসিমাল", multiplier: 1, waterLitersPerUnit: 4 },
  { id: "katha", name: "কাঠা", multiplier: 1.65, waterLitersPerUnit: 6.6 },
  { id: "bigha", name: "বিঘা (৩৩ শতক)", multiplier: 33, waterLitersPerUnit: 132 },
];

// Helper to extract a reasonable default dose per liter from raw text (defaults to 2g/L if unspecified)
function parseDosePerLiter(text?: string | null): { dose: number; unit: "g" | "ml" } {
  if (!text) return { dose: 2, unit: "g" };
  
  // Look for patterns like "২ গ্রাম", "0.5 মিলি", "1.5 g/L", "২.৫ মিলি/লিটার"
  const match = text.match(/([০-৯0-9.]+)\s*(গ্রাম|মি\.?লি|মিলি|g|ml)/i);
  if (match) {
    let numStr = match[1];
    // Convert Bengali digits to ASCII
    numStr = numStr.replace(/[০-৯]/g, (d) => "০১২৩৪৫৬৭৮৯".indexOf(d).toString());
    const val = parseFloat(numStr);
    const isLiquid = /মি\.?লি|মিলি|ml/i.test(match[2]);
    if (!isNaN(val) && val > 0 && val <= 50) {
      return { dose: val, unit: isLiquid ? "ml" : "g" };
    }
  }
  return { dose: 2, unit: "g" };
}

export function DosageCalculator({
  defaultDosageText,
}: DosageCalculatorProps) {
  const parsed = useMemo(() => parseDosePerLiter(defaultDosageText), [defaultDosageText]);
  
  const [calcMode, setCalcMode] = useState<"tank" | "land">("tank");
  const [selectedTank, setSelectedTank] = useState<number>(16);
  const [dosePerLiter, setDosePerLiter] = useState<number>(parsed.dose);
  const [unitType, setUnitType] = useState<"g" | "ml">(parsed.unit);
  
  // Land mode states
  const [landArea, setLandArea] = useState<number>(10);
  const [landUnit, setLandUnit] = useState<string>("shotok");

  // Calculations
  const calculatedTotalDose = useMemo(() => {
    if (calcMode === "tank") {
      return selectedTank * dosePerLiter;
    } else {
      const unitObj = LAND_UNITS.find((u) => u.id === landUnit) || LAND_UNITS[0];
      const totalWater = landArea * unitObj.waterLitersPerUnit;
      return totalWater * dosePerLiter;
    }
  }, [calcMode, selectedTank, dosePerLiter, landArea, landUnit]);

  const totalWaterRequired = useMemo(() => {
    if (calcMode === "tank") {
      return selectedTank;
    } else {
      const unitObj = LAND_UNITS.find((u) => u.id === landUnit) || LAND_UNITS[0];
      return Math.round(landArea * unitObj.waterLitersPerUnit);
    }
  }, [calcMode, selectedTank, landArea, landUnit]);

  // Convert to practical household measurements
  // Standard tea spoon = ~2 grams powder; 1 bottle cap (ছিপি) = ~10 ml liquid
  const practicalHouseholdMeasure = useMemo(() => {
    if (unitType === "g") {
      const spoons = Math.round((calculatedTotalDose / 2) * 10) / 10;
      return `${toBn(spoons)} চা চামচ (প্রতি চামচ প্রায় ২ গ্রাম)`;
    } else {
      const caps = Math.round((calculatedTotalDose / 10) * 10) / 10;
      return `${toBn(caps)} বোতলের ছিপি (প্রতি ছিপি প্রায় ১০ মিলি)`;
    }
  }, [calculatedTotalDose, unitType]);

  // Safety concentration level
  const safetyStatus = useMemo(() => {
    if (dosePerLiter > 4) {
      return {
        level: "danger",
        label: "অতিরিক্ত ঘন মাত্রা (Overdose Warning)",
        color: "text-clay",
        bg: "bg-clay-soft/20",
        border: "border-clay-soft",
        desc: "গাছ পুড়ে যাওয়ার বা বিষক্রিয়ার উচ্চ ঝুঁকি রয়েছে। মাত্রা কমিয়ে আনুন।",
      };
    }
    if (dosePerLiter >= 1.5 && dosePerLiter <= 3) {
      return {
        level: "safe",
        label: "অনুমোদিত আদর্শ মাত্রা (Safe Recommended Ratio)",
        color: "text-leaf",
        bg: "bg-leaf/10",
        border: "border-leaf/30",
        desc: "সরকারি বালাই ব্যবস্থাপনা নির্দেশিকা অনুসারে সঠিক মাত্রা।",
      };
    }
    return {
      level: "caution",
      label: "হালকা মাত্রা (Light Dose)",
      color: "text-ochre",
      bg: "bg-ochre-soft/20",
      border: "border-ochre-soft",
      desc: "প্রাথমিক রোগ প্রতিরোধে কার্যকর, তবে তীব্র আক্রমণে কৃষি বিশেষজ্ঞের পরামর্শ নিন।",
    };
  }, [dosePerLiter]);

  return (
    <div className="overflow-hidden rounded-xl border border-leaf/20 bg-paper shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-leaf/15 bg-leaf/5 px-4 py-3 sm:px-5">
        <div className="flex items-center gap-2 text-xs font-semibold text-leaf">
          <Calculator className="h-4 w-4" />
          <span>সঠিক মাত্রা ও স্প্রে গণক (Dosage Calculator)</span>
        </div>
        <div className="flex rounded-lg border rule bg-paper p-0.5 text-[11px] font-medium text-ink-soft">
          <button
            type="button"
            onClick={() => setCalcMode("tank")}
            className={cn(
              "rounded-md px-2.5 py-1 transition-colors cursor-pointer",
              calcMode === "tank" ? "bg-leaf text-paper font-semibold shadow-xs" : "hover:text-ink"
            )}
          >
            স্প্রেয়ার ট্যাংক
          </button>
          <button
            type="button"
            onClick={() => setCalcMode("land")}
            className={cn(
              "rounded-md px-2.5 py-1 transition-colors cursor-pointer",
              calcMode === "land" ? "bg-leaf text-paper font-semibold shadow-xs" : "hover:text-ink"
            )}
          >
            জমির পরিমাণ
          </button>
        </div>
      </div>

      <div className="space-y-4 p-4 sm:p-5">
        {/* Mode 1: Spray Tank Presets */}
        {calcMode === "tank" ? (
          <div>
            <label className="text-[11px] font-semibold text-ink-faint">
              আপনার স্প্রেয়ার ট্যাংকের ধারণক্ষমতা নির্বাচন করুন:
            </label>
            <div className="mt-2 grid grid-cols-3 gap-2">
              {TANK_PRESETS.map((preset) => {
                const active = selectedTank === preset.liters;
                return (
                  <button
                    key={preset.liters}
                    type="button"
                    onClick={() => setSelectedTank(preset.liters)}
                    className={cn(
                      "flex flex-col items-center justify-center rounded-xl border p-2.5 text-center transition-all cursor-pointer",
                      active
                        ? "border-leaf bg-leaf/10 text-leaf shadow-xs ring-1 ring-leaf"
                        : "border-bone bg-paper-2/40 text-ink-soft hover:border-leaf/40 hover:bg-paper"
                    )}
                  >
                    <span className="font-display text-sm font-semibold sm:text-base">
                      {preset.label}
                    </span>
                    <span className="mt-0.5 text-[10px] text-ink-faint">
                      {preset.desc}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          /* Mode 2: Land Area Input */
          <div className="grid gap-3 sm:grid-cols-2">
            <div>
              <label className="text-[11px] font-semibold text-ink-faint">
                জমির পরিমাণ:
              </label>
              <div className="mt-1 flex items-center gap-2">
                <input
                  type="number"
                  min={1}
                  max={500}
                  value={landArea}
                  onChange={(e) => setLandArea(Math.max(1, parseFloat(e.target.value) || 1))}
                  className="w-full rounded-lg border rule bg-paper px-3 py-2 text-sm font-semibold tabular text-ink focus:border-leaf focus:outline-none"
                />
              </div>
            </div>
            <div>
              <label className="text-[11px] font-semibold text-ink-faint">
                পরিমাপের একক:
              </label>
              <select
                value={landUnit}
                onChange={(e) => setLandUnit(e.target.value)}
                className="mt-1 w-full rounded-lg border rule bg-paper px-3 py-2 text-sm font-medium text-ink focus:border-leaf focus:outline-none"
              >
                {LAND_UNITS.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}

        {/* Dose adjustment slider */}
        <div className="rounded-xl border rule bg-paper-2/25 p-3.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-ink">
              প্রস্তাবিত প্রয়োগ মাত্রা (প্রতি লিটার পানিতে):
            </span>
            <div className="flex items-center gap-1.5">
              <span className="font-display text-base font-bold tabular text-leaf">
                {toBn(dosePerLiter)}
              </span>
              <span className="text-xs font-semibold text-ink-soft">
                {unitType === "g" ? "গ্রাম / লিটার" : "মিলি / লিটার"}
              </span>
            </div>
          </div>

          <div className="mt-3 flex items-center gap-3">
            <input
              type="range"
              min={0.5}
              max={6.0}
              step={0.5}
              value={dosePerLiter}
              onChange={(e) => setDosePerLiter(parseFloat(e.target.value))}
              className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-bone accent-leaf"
            />
            <div className="flex shrink-0 rounded-md border rule bg-paper text-[10px] font-semibold">
              <button
                type="button"
                onClick={() => setUnitType("g")}
                className={cn("px-2 py-1 rounded-l-md cursor-pointer", unitType === "g" ? "bg-leaf text-paper" : "text-ink-faint")}
              >
                পাউডার (গ্রাম)
              </button>
              <button
                type="button"
                onClick={() => setUnitType("ml")}
                className={cn("px-2 py-1 rounded-r-md cursor-pointer", unitType === "ml" ? "bg-leaf text-paper" : "text-ink-faint")}
              >
                তরল (মিলি)
              </button>
            </div>
          </div>
        </div>

        {/* Result Card */}
        <div className="rounded-xl border-2 border-leaf/30 bg-leaf/5 p-4">
          <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-leaf">
                মোট মিশ্রণ হিসাব
              </span>
              <div className="mt-1 flex items-baseline gap-2">
                <span className="font-display text-2xl font-bold tabular text-ink sm:text-3xl">
                  {toBn(calculatedTotalDose)}
                </span>
                <span className="font-semibold text-leaf text-base">
                  {unitType === "g" ? "গ্রাম কীটনাশক / ছত্রাকনাশক" : "মিলি তরল ওষুধ"}
                </span>
              </div>
            </div>
            <div className="rounded-lg border border-leaf/20 bg-paper px-3 py-2 text-right">
              <div className="text-[10px] text-ink-faint">প্রয়োজনীয় পানি</div>
              <div className="font-display text-lg font-bold tabular text-ink">
                {toBn(totalWaterRequired)} <span className="text-xs font-normal">লিটার</span>
              </div>
            </div>
          </div>

          {/* Household Measure Helper */}
          <div className="mt-3 flex items-center gap-2 border-t border-leaf/15 pt-3 text-xs text-ink-soft">
            <Droplets className="h-4 w-4 shrink-0 text-ochre" />
            <span>
              সহজ পরিমাপ: <strong>{practicalHouseholdMeasure}</strong>
            </span>
          </div>
        </div>

        {/* Safety Indicator Banner */}
        <div className={cn("flex items-start gap-2.5 rounded-lg border p-3 text-xs leading-relaxed", safetyStatus.bg, safetyStatus.border)}>
          <ShieldCheck className={cn("mt-0.5 h-4 w-4 shrink-0", safetyStatus.color)} />
          <div className="flex-1">
            <div className={cn("font-semibold", safetyStatus.color)}>
              {safetyStatus.label}
            </div>
            <p className="mt-0.5 text-ink-soft">{safetyStatus.desc}</p>
          </div>
          <a
            href={`tel:${HELPLINE.krishiCallCenter}`}
            className="inline-flex shrink-0 items-center gap-1 rounded-md border border-leaf/30 bg-paper px-2 py-1 text-[11px] font-semibold text-leaf hover:bg-leaf/5"
            title="কৃষি কল সেন্টারে যোগাযোগ করুন"
          >
            <Phone className="h-3 w-3" /> ১৬১২৩
          </a>
        </div>
      </div>
    </div>
  );
}
