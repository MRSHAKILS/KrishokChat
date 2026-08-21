import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("d:/KrishokChat Advisory System/capstone/poster-design/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 960},
            device_scale_factor=2,
            locale="bn-BD"
        )
        page = context.new_page()

        print("=== 1. /detect ===")
        page.goto("http://localhost:3000/detect", wait_until="networkidle")
        time.sleep(1)
        
        try:
            page.select_option("#crop-hint", "rice")
        except Exception as e:
            print("Crop hint note:", e)

        img_path = Path("d:/KrishokChat Advisory System/demo-assets/images/rice/brown_spot.jpg").resolve()
        if img_path.exists():
            input_file = page.locator('input[type="file"]')
            input_file.set_input_files(str(img_path))
            print("File selected. Waiting...")
            time.sleep(1.5)
            
            btn = page.locator('button:has-text("রোগ শনাক্ত করুন"), button:has-text("বিশ্লেষণ করুন"), button:has-text("শনাক্ত করুন")')
            if btn.count() > 0:
                print("Clicking diagnose button...")
                btn.first.click()
                time.sleep(6)
            else:
                p_btn = page.locator('button:has-text("শনাক্ত")')
                if p_btn.count() > 0:
                    p_btn.first.click()
                    time.sleep(6)
        
        page.screenshot(path=str(OUT_DIR / "01_detect_rice_disease_diagnosis.png"))
        print("Captured 01_detect_rice_disease_diagnosis.png")

        print("=== 2. /chat (Safety Refusal) ===")
        page.goto("http://localhost:3000/chat", wait_until="networkidle")
        time.sleep(1)
        
        textarea = page.locator("textarea")
        if textarea.count() > 0:
            textarea.fill("প্যারাকোয়াট দিয়ে কীভাবে স্প্রে করব?")
            time.sleep(0.5)
            send_btn = page.locator('button[type="submit"], button:has(svg.lucide-send)')
            if send_btn.count() > 0:
                send_btn.first.click()
            else:
                textarea.press("Enter")
            print("Banned query sent. Waiting 4s...")
            time.sleep(4.0)
        
        page.screenshot(path=str(OUT_DIR / "02_chat_safety_refusal_16123.png"))
        print("Captured 02_chat_safety_refusal_16123.png")

        print("=== 3. /chat (Verified Advisory) ===")
        page.goto("http://localhost:3000/chat", wait_until="networkidle")
        time.sleep(1)
        
        textarea = page.locator("textarea")
        if textarea.count() > 0:
            textarea.fill("ধানের ব্লাইট বা পাতা পোড়া রোগের লক্ষণ ও অনুমোদিত প্রতিকার কী?")
            time.sleep(0.5)
            send_btn = page.locator('button[type="submit"], button:has(svg.lucide-send)')
            if send_btn.count() > 0:
                send_btn.first.click()
            else:
                textarea.press("Enter")
            print("Agronomic query sent. Waiting 8s...")
            time.sleep(8.0)
        
        page.screenshot(path=str(OUT_DIR / "03_chat_verified_advisory.png"))
        print("Captured 03_chat_verified_advisory.png")

        print("=== 4. /analytics ===")
        page.goto("http://localhost:3000/analytics", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=str(OUT_DIR / "04_analytics_audit_dashboard.png"))
        print("Captured 04_analytics_audit_dashboard.png")

        print("=== 5. /soil ===")
        page.goto("http://localhost:3000/soil", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=str(OUT_DIR / "05_soil_moisture_dataset.png"))
        print("Captured 05_soil_moisture_dataset.png")

        print("=== 6. Landing Hero ===")
        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1.5)
        page.screenshot(path=str(OUT_DIR / "06_landing_hero.png"))
        print("Captured 06_landing_hero.png")

        browser.close()
        print("ALL CAPTURES COMPLETED!")

if __name__ == "__main__":
    main()
