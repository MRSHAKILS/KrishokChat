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

export function useCountUp(to: number, active: boolean, duration = 0.9) {
  const [val, setVal] = useState(0);
  const reduced = useReducedMotion();
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (!active) return;
    if (reduced) {
      setVal(to);
      return;
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