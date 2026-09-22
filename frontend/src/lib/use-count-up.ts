"use client";

/* =========================================================================
   useCountUp — rAF-based number tween for stat cells.
   No dependencies. Respects prefers-reduced-motion (via motion's hook).
   ========================================================================= */

import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "motion/react";

const BN_DIGITS = "০১২৩৪৫৬৭৮৯";

/** 2882 -> "২,৮৮২" (en-IN grouping, Bengali digits) */
export function toBn(n: number): string {
  return n.toLocaleString("en-IN").replace(/\d/g, (d) => BN_DIGITS[Number(d)]);
}

/** 2882 -> "২,৮৮২" in Bengali mode, "2,882" (en-IN grouping, Latin digits) in English mode. */
export function toLocaleCount(n: number, en: boolean): string {
  const grouped = n.toLocaleString("en-IN");
  return en ? grouped : grouped.replace(/\d/g, (d) => BN_DIGITS[Number(d)]);
}

export function useCountUp(to: number, active: boolean, duration = 0.9) {
  const reduced = useReducedMotion();
  const [val, setVal] = useState(() => (reduced ? to : 0));
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (!active) return;
    if (reduced) {
      rafRef.current = requestAnimationFrame(() => setVal(to));
      return () => {
        if (rafRef.current) cancelAnimationFrame(rafRef.current);
      };
    }
    const start = performance.now();
    const tick = (now: number) => {
      const p = Math.min((now - start) / (duration * 1000), 1);
      const eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
      setVal(Math.round(to * eased));
      if (p < 1) rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [to, active, reduced, duration]);

  return val;
}