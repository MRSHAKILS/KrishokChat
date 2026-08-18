import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("d:/KrishokChat Advisory System/capstone/poster deisgn/screenshots")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Taller viewport (1440x1200) so everything fits seamlessly in one shot
    context = browser.new_context(
        viewport={"width": 1440, "height": 1280},
        device_scale_factor=2,
        locale="bn-BD"
    )
    page = context.new_page()

    page.goto("http://localhost:3000/detect", wait_until="networkidle")
    time.sleep(1)
    
    page.select_option("#crop-hint", "rice")
    img_path = Path("d:/KrishokChat Advisory System/demo-assets/images/rice/brown_spot.jpg").resolve()
    input_file = page.locator('input[type="file"]')
    input_file.set_input_files(str(img_path))
    time.sleep(1)

    diagnose_btn = page.locator('button:has-text("নির্ণয় করুন")')
    if diagnose_btn.count() > 0:
        diagnose_btn.first.click()
        time.sleep(8)
    
    # Capture standard viewport showing the diagnosis & treatment
    page.screenshot(path=str(OUT_DIR / "01_detect_rice_disease_diagnosis.png"))
    
    # Also capture focused element of diagnosis + treatment card
    page.evaluate("window.scrollBy(0, 350)")
    time.sleep(1)
    page.screenshot(path=str(OUT_DIR / "01b_detect_diagnosis_and_treatment_card.png"))
    
    browser.close()
    print("Done capturing 01 and 01b")
