/**
 * R10 — On-Device Mobile Vision Classifier & Confidence-Gated Upload (U1 + U3).
 *
 * Runs on-device diagnosis when confidence >= 0.80 (0 latency, offline capable).
 * Transparently compresses and falls back to server route when confidence < 0.80.
 */

export interface OnDeviceClassPrediction {
  label: string;
  label_bn: string;
  confidence: number;
}

export interface OnDeviceDiagnosisResult {
  isOnDevice: boolean;
  crop: OnDeviceClassPrediction;
  disease?: OnDeviceClassPrediction;
  needsServerVerification: boolean;
  transparencyReason?: string;
  latencyMs: number;
}

export const CONFIDENCE_THRESHOLD = 0.80;

export const SERVER_FALLBACK_REASONS = {
  LOW_CROP_CONFIDENCE: "ফসলের ধরন স্পষ্টভাবে শনাক্ত করা যায়নি, তাই সার্ভারে অধিকতর বিশ্লেষণের জন্য পাঠানো হচ্ছে।",
  LOW_DISEASE_CONFIDENCE: "রোগের লক্ষণটি স্পষ্ট নয়, তাই নিশ্চিত হতে সার্ভারে পাঠানো হচ্ছে।",
  UNSUPPORTED_CROP: "এই ফসলের অন-ডিভাইস মডেল এখনও প্রস্তুত নয়, সার্ভারে পাঠানো হচ্ছে।",
  ONDEVICE_ERROR: "ডিভাইসে বিশ্লেষণ সম্ভব হয়নি, সার্ভারে যাচাই করা হচ্ছে।",
};

/**
 * Evaluates whether an on-device prediction meets the confidence threshold.
 */
export function evaluateConfidenceGate(
  cropConfidence: number,
  diseaseConfidence?: number
): { passesGate: boolean; reason?: string } {
  if (cropConfidence < CONFIDENCE_THRESHOLD) {
    return {
      passesGate: false,
      reason: SERVER_FALLBACK_REASONS.LOW_CROP_CONFIDENCE,
    };
  }

  if (diseaseConfidence !== undefined && diseaseConfidence < CONFIDENCE_THRESHOLD) {
    return {
      passesGate: false,
      reason: SERVER_FALLBACK_REASONS.LOW_DISEASE_CONFIDENCE,
    };
  }

  return { passesGate: true };
}

/**
 * Compresses an image file (resize to max 1024px, strip EXIF, convert to WebP) before server upload.
 */
export async function compressImageForUpload(
  file: File | Blob,
  maxDimension = 1024,
  quality = 0.85
): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);

    img.onload = () => {
      URL.revokeObjectURL(url);
      let { width, height } = img;

      if (width > maxDimension || height > maxDimension) {
        if (width > height) {
          height = Math.round((height * maxDimension) / width);
          width = maxDimension;
        } else {
          width = Math.round((width * maxDimension) / height);
          height = maxDimension;
        }
      }

      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext("2d");
      if (!ctx) {
        resolve(file);
        return;
      }

      ctx.drawImage(img, 0, 0, width, height);
      canvas.toBlob(
        (blob) => {
          if (blob) {
            resolve(blob);
          } else {
            resolve(file);
          }
        },
        "image/webp",
        quality
      );
    };

    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("Failed to load image for compression"));
    };

    img.src = url;
  });
}
