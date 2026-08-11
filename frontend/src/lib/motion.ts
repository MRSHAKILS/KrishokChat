import type { Variants, Transition } from "motion/react";

/* =========================================================================
   Motion vocabulary — information-carrying, not decorative.
   No fade-up-everything. Each variant maps to a specific UX meaning.
   ========================================================================= */

export const ease = {
  smooth: [0.22, 1, 0.36, 1] as [number, number, number, number],
  sharp: [0.4, 0, 0.2, 1] as [number, number, number, number],
  out: [0, 0, 0.2, 1] as [number, number, number, number],
} as const;

export const dur = {
  instant: 0.12,
  fast: 0.2,
  normal: 0.35,
  slow: 0.55,
} as const;

/** Product motion contract: calm enough for repeated field use. */
export const motionSpec = {
  interaction: `${dur.fast}s ${ease.sharp.join(",")}`,
  reveal: `${dur.normal}s ${ease.smooth.join(",")}`,
  progress: `${dur.slow}s ${ease.smooth.join(",")}`,
  stagger: 0.07,
} as const;

/* Stagger for sequenced reveals (stat cards, pipeline nodes) */
export const stagger: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.07, delayChildren: 0.05 } },
};

/* A content block entering — used sparingly, one per section */
export const enter: Variants = {
  hidden: { opacity: 0, y: 14 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: dur.normal, ease: ease.smooth },
  },
};

/* A pipeline node lighting up */
export const nodeActivate: Variants = {
  pending: { scale: 1, opacity: 0.35 },
  active: { scale: 1.08, opacity: 1, transition: { type: "spring", stiffness: 320, damping: 18 } },
  complete: { scale: 1, opacity: 1, transition: { duration: dur.fast, ease: ease.out } },
  skip: { scale: 0.92, opacity: 0.3, transition: { duration: dur.fast } },
  error: { scale: 1, opacity: 1, transition: { duration: dur.fast } },
};

/* Flow line draw — the connector between pipeline stages */
export const flowDraw: Variants = {
  pending: { scaleX: 0, opacity: 0 },
  active: { scaleX: 0.5, opacity: 0.6, transition: { duration: dur.slow, ease: ease.smooth } },
  complete: { scaleX: 1, opacity: 1, transition: { duration: dur.normal, ease: ease.out } },
};

/* Token type-out caret */
export const caret: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: [0, 1, 1, 0], transition: { duration: 1, repeat: Infinity, ease: "easeInOut" } },
};

/* Shared transition helper */
export const spring: Transition = { type: "spring", stiffness: 280, damping: 22 };
