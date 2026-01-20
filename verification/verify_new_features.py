from playwright.sync_api import sync_playwright
import time
import os

def verify_ui():
    if not os.path.exists("verification"):
        os.makedirs("verification")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile view is better for this app
        context = browser.new_context(viewport={'width': 390, 'height': 844})
        page = context.new_page()

        # Navigate to Home
        print("Waiting for server...")
        time.sleep(2)
        try:
            page.goto("http://localhost:5173", timeout=30000)
        except Exception as e:
            print(f"Failed to load page: {e}")
            browser.close()
            return

        # Wait for Home component to load (look for specific Home content)
        try:
            page.wait_for_selector("text=Smart City Scanner", timeout=15000)
        except:
            print("Timed out waiting for Smart City Scanner. Taking debug screenshot.")
            page.screenshot(path="verification/debug_timeout.png")
            browser.close()
            return

        # Take screenshot of Home with new buttons
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        page.screenshot(path="verification/home_new_features.png")
        print("Captured home_new_features.png")

        # Navigate to Noise Detector
        print("Clicking Noise...")
        page.click("text=Noise")
        page.wait_for_selector("text=Noise Pollution Detector")
        page.screenshot(path="verification/noise_detector.png")
        print("Captured noise_detector.png")

        # Go back
        print("Clicking Back...")
        page.click("text=Back to Home")
        page.wait_for_selector("text=Smart City Scanner")

        # Navigate to Stats
        print("Clicking City Stats...")
        page.click("text=City Stats")
        page.wait_for_selector("text=City Statistics")
        page.screenshot(path="verification/stats_view.png")
        print("Captured stats_view.png")

        browser.close()

if __name__ == "__main__":
    verify_ui()
