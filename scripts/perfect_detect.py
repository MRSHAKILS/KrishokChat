import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = Path("d:/KrishokChat Advisory System/capstone/poster deisgn/screenshots")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 960},
        device_scale_factor=2,
        locale="bn-BD"
    )
    page = context.new_page()

    print("Capturing /detect...")
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
        diagnose_btn.first.click()
        print("Clicked diagnose, waiting up to 25s for diagnosis card...")
        # Wait for either diagnosis card, treatment card, or error
        for i in range(25):
            time.sleep(1)
            # check if diagnosis completed
            if page.locator('text=Brown_Spot, text=ব্রাউন স্পট, text=রোগ নির্ণয় ফলাফল, text=চিকিৎসা ও প্রতিকার, text=শনাক্ত').count() > 0:
                print(f"Diagnosis completed in {i+1}s!")
                break
        time.sleep(2)
    
    # Scroll slightly down if needed to frame the diagnosis card beautifully
    page.screenshot(path=str(OUT_DIR / "01_detect_rice_disease_diagnosis.png"))
    print("01_detect_rice_disease_diagnosis.png updated.")

    browser.close()
