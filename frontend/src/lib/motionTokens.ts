// lib/motionTokens.ts
export const motionTokens = {
  duration: { fast: 0.18, normal: 0.35, slow: 0.6 },
  easing: {
    smooth: [0.22, 1, 0.36, 1] as [number, number, number, number],
    sharp: [0.4, 0, 0.2, 1] as [number, number, number, number],
  },
  distance: { sm: 8, md: 16, lg: 24 },
};

export const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.06 } },
};

export const fadeUp = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth },
  },
};

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: motionTokens.duration.fast, ease: motionTokens.easing.smooth },
  },
};
