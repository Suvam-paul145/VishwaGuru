from playwright.sync_api import sync_playwright, expect
import time
import sys

def test_new_features(page):
    # Mock /api/issues/recent for Map View
    page.route("**/api/issues/recent", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='[{"id": 1, "category": "pothole", "description": "Big hole", "created_at": "2023-01-01T10:00:00", "latitude": 19.75, "longitude": 75.71, "status": "open", "location": "Nagpur"}]'
    ))

    # Go to Home
    page.goto("http://localhost:5173")

    # 1. Test Map View Toggle
    print("Testing Map View Toggle...")
    # Default is List - check if List button has active style (bg-white)
    # Note: Class checks in playwright can be string contains
    list_btn = page.get_by_text("List", exact=True)
    map_btn = page.get_by_text("Map", exact=True)

    expect(list_btn).to_be_visible()

    # Click Map
    map_btn.click()

    # Check Map Container exists (leaflet-container)
    expect(page.locator(".leaflet-container")).to_be_visible()

    # Check Marker exists (leaflet-marker-icon)
    # Wait for map to render markers
    expect(page.locator(".leaflet-marker-icon")).to_be_visible()

    print("Map View Verified.")

    # 2. Test Smart Scanner (Camera)
    # Go back to list or just click the header button?
    # Smart City Scanner button is in the header/CTA section, it should be visible

    print("Testing Smart Scanner...")
    # Click Smart City Scanner
    page.get_by_text("Smart City Scanner").click()

    # Expect video element
    expect(page.locator("video")).to_be_visible(timeout=5000)

    print("Smart Scanner Verified.")

if __name__ == "__main__":
    with sync_playwright() as p:
        # Launch with fake device for camera
        browser = p.chromium.launch(
            headless=True,
            args=["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream"]
        )
        page = browser.new_page()
        try:
            test_new_features(page)
            print("All verifications passed.")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/feature_error.png")
            sys.exit(1)
        finally:
            browser.close()
