import { VISION } from "@/lib/constants";

const MAX_EDGE = 1280;
const JPEG_QUALITY = 0.82;

/**
 * Prepares and compresses image on client side before upload.
 * Reduces 8-15 MB mobile photos down to ~250-350 KB, speeding up upload
 * on 2G/3G connections by >95% while keeping high fidelity for YOLO classification.
 */
export async function prepareUploadImage(file: File): Promise<File> {
  if (!VISION.acceptedTypes.includes(file.type)) {
    throw new Error("শুধু JPEG, PNG বা WebP ছবি দিন।");
  }
  if (file.size > VISION.maxFileSizeMB * 1024 * 1024) {
    throw new Error(`ছবিটি ${VISION.maxFileSizeMB}MB-এর ছোট হতে হবে।`);
  }

  // Already small enough
  if (file.size <= 300 * 1024 && file.type === "image/jpeg") {
    return file;
  }

  try {
    let bitmap: ImageBitmap;
    try {
      bitmap = await createImageBitmap(file, { imageOrientation: "from-image" });
    } catch {
      bitmap = await createImageBitmap(file);
    }

    try {
      const scale = Math.min(1, MAX_EDGE / Math.max(bitmap.width, bitmap.height));
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.round(bitmap.width * scale));
      canvas.height = Math.max(1, Math.round(bitmap.height * scale));
      const context = canvas.getContext("2d", { alpha: false });
      if (!context) return file;

      // High quality image smoothing
      context.imageSmoothingEnabled = true;
      context.imageSmoothingQuality = "high";
      context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);

      const blob = await new Promise<Blob | null>((resolve) =>
        canvas.toBlob(resolve, "image/jpeg", JPEG_QUALITY),
      );
      if (!blob || blob.size >= file.size) return file;
      const name = file.name.replace(/\.[^.]+$/, "") || "crop-photo";
      return new File([blob], `${name}.jpg`, { type: "image/jpeg", lastModified: Date.now() });
    } finally {
      bitmap.close();
    }
  } catch {
    // If bitmap creation fails, return original file without blocking the user
    return file;
  }
}

