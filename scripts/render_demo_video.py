"""
Assemble captured demo screenshots into a smooth, high-definition MP4 demo video and GIF.
"""
import os
import glob
import subprocess
from PIL import Image

BRAIN_DIR = r"C:\Users\raiya\.gemini\antigravity-ide\brain\8fbdc941-f31d-4b2f-b81e-2e8c55d709c3"
OUT_DIR = r"d:\KrishokChat Advisory System"
PUBLIC_DIR = r"d:\KrishokChat Advisory System\frontend\public"

# Curate the chronological sequence of screenshots
SHOTS = [
    ("home_page_top", 3),
    ("home_page_mid1", 2),
    ("home_page_mid2", 2),
    ("home_page_mid3", 2),
    ("home_page_bot", 2),
    ("home_page_bot2", 2),
    ("home_page_back_top", 2),
    ("detect_page_init", 2),
    ("detect_page_image_loaded", 3),
    ("detect_page_results", 4),
    ("detect_prescription_modal", 4),
    ("chat_input_english", 4),
]

img_files = []
for name, duration in SHOTS:
    matches = glob.glob(os.path.join(BRAIN_DIR, f"{name}_*.png"))
    if matches:
        img_files.append((matches[0], duration))

print(f"Found {len(img_files)} curated screenshots for demo video.")

# Resize/pad images to standard 1920x1080 for high definition video
TARGET_SIZE = (1920, 1080)
temp_frames_dir = os.path.join(OUT_DIR, "scratch_frames")
os.makedirs(temp_frames_dir, exist_ok=True)

frame_idx = 0
fps = 2  # 2 frames per second (each image shown for 2-4 seconds)

all_frame_paths = []
for img_path, duration in img_files:
    img = Image.open(img_path).convert("RGB")
    # Fit into 1920x1080 keeping aspect ratio with subtle letterboxing
    img.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)
    
    # Create canvas
    canvas = Image.new("RGB", TARGET_SIZE, (246, 247, 244)) # KrishokChat background color
    offset_x = (TARGET_SIZE[0] - img.size[0]) // 2
    offset_y = (TARGET_SIZE[1] - img.size[1]) // 2
    canvas.paste(img, (offset_x, offset_y))
    
    # Write frames for the duration
    num_frames = int(duration * fps)
    for _ in range(num_frames):
        frame_name = os.path.join(temp_frames_dir, f"frame_{frame_idx:04d}.png")
        canvas.save(frame_name)
        all_frame_paths.append(frame_name)
        frame_idx += 1

print(f"Generated {frame_idx} video frames.")

# 1. Compile to MP4 using ffmpeg
mp4_path = os.path.join(OUT_DIR, "krishokchat_demo_video.mp4")
mp4_public = os.path.join(PUBLIC_DIR, "krishokchat_demo_video.mp4")

cmd_mp4 = [
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "24",
    mp4_path
]

print("Running ffmpeg for MP4...")
subprocess.run(cmd_mp4, check=True)
subprocess.run(["copy", mp4_path, mp4_public], shell=True)

# 2. Compile to animated GIF for quick web preview
gif_path = os.path.join(OUT_DIR, "krishokchat_demo.gif")
gif_public = os.path.join(PUBLIC_DIR, "krishokchat_demo.gif")

cmd_gif = [
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
    "-vf", "scale=1280:-1:flags=lanczos,fps=2",
    gif_path
]

print("Running ffmpeg for GIF...")
subprocess.run(cmd_gif, check=True)
subprocess.run(["copy", gif_path, gif_public], shell=True)

print("\n=== Demo Video Creation Complete ===")
print("MP4 Video:", mp4_path)
print("GIF Animation:", gif_path)
