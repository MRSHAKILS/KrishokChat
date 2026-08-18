import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = Path("d:/KrishokChat Advisory System/capstone/poster deisgn/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 960},
        device_scale_factor=2,
        locale="bn-BD"
    )
    page = context.new_page()

    # 1. DETECT
    print("Capturing /detect with full diagnosis...")
    page.goto("http://localhost:3000/detect", wait_until="networkidle")
    time.sleep(1)
    
    try:
        page.select_option("#crop-hint", "rice")
    except Exception as e:
        print("Crop hint error:", e)

    img_path = Path("d:/KrishokChat Advisory System/demo-assets/images/rice/brown_spot.jpg").resolve()
    input_file = page.locator('input[type="file"]')
    input_file.set_input_files(str(img_path))
    time.sleep(1.5)

    diagnose_btn = page.locator('button:has-text("নির্ণয় করুন")')
    if diagnose_btn.count() > 0:
        print("Clicking diagnose button...")
        diagnose_btn.first.click()
        print("Waiting 6 seconds for diagnosis and animations...")
        time.sleep(6)
    
    page.screenshot(path=str(OUT_DIR / "01_detect_rice_disease_diagnosis.png"))
    print("01_detect_rice_disease_diagnosis.png updated.")

    # 3. CHAT VERIFIED ADVISORY
    print("Capturing /chat verified advisory...")
    page.goto("http://localhost:3000/chat", wait_until="networkidle")
    time.sleep(1)

    textarea = page.locator("textarea")
    textarea.fill("ধানের ব্লাইট বা পাতা পোড়া রোগের লক্ষণ ও অনুমোদিত প্রতিকার কী?")
    time.sleep(0.5)

    send_btn = page.locator('button:has-text("জিজ্ঞাসা করুন"), button[type="submit"]')
    if send_btn.count() > 0:
        send_btn.first.click()
    else:
        textarea.press("Enter")

    print("Waiting 12 seconds for streaming to finish...")
    time.sleep(12)

    page.screenshot(path=str(OUT_DIR / "03_chat_verified_advisory.png"))
    print("03_chat_verified_advisory.png updated.")

    browser.close()
    print("Done perfecting 01 and 03.")
