import { VISION } from "@/lib/constants";

const MAX_EDGE = 1600;
const JPEG_QUALITY = 0.82;

export async function prepareUploadImage(file: File): Promise<File> {
  if (!VISION.acceptedTypes.includes(file.type)) {
    throw new Error("শুধু JPEG, PNG বা WebP ছবি দিন।");
  }
  if (file.size > VISION.maxFileSizeMB * 1024 * 1024) {
    throw new Error(`ছবিটি ${VISION.maxFileSizeMB}MB-এর ছোট হতে হবে।`);
  }

  const bitmap = await createImageBitmap(file);
  try {
    const scale = Math.min(1, MAX_EDGE / Math.max(bitmap.width, bitmap.height));
    if (scale === 1 && file.size <= 2 * 1024 * 1024) return file;

    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.round(bitmap.width * scale));
    canvas.height = Math.max(1, Math.round(bitmap.height * scale));
    const context = canvas.getContext("2d", { alpha: false });
    if (!context) return file;
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
}
