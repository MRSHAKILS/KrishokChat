/* =========================================================================
   Bengali numeral helpers — the entire UI speaks in Bengali numerals.
   A farmer reads ৯৮%, not 98%. This is the single conversion point.
   ========================================================================= */

const BN_DIGITS = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"];

/** Convert a number to a Bengali numeral string. */
export function bn(value: number | string): string {
  return String(value).replace(/[0-9]/g, (d) => BN_DIGITS[Number(d)]);
}

/** Format a 0-1 confidence as a Bengali percentage, e.g. 0.976 → "৯৮%". */
export function bnPercent(confidence: number): string {
  return bn(Math.round(confidence * 100)) + "%";
}

/** Format a 0-1 confidence with one decimal, e.g. 0.953 → "৯৫.৩%". */
export function bnPercent1(confidence: number): string {
  return bn((confidence * 100).toFixed(1)) + "%";
}

/** Humanize a machine disease label: "Potato__Early_Blight" → "Potato — Early Blight". */
export function humanizeLabel(label: string): string {
  return label.replace(/__/g, " — ").replace(/_/g, " ").replace(/\s+/g, " ").trim();
}

/** Extract the disease core from a "Crop__Disease" label: "Potato__Early_Blight" → "Early Blight". */
export function diseaseCore(label: string): string {
  const parts = label.split("__");
  return humanizeLabel(parts.length > 1 ? parts.slice(1).join(" ") : label);
}
