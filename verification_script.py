from playwright.sync_api import sync_playwright, expect
import os

def test_auto_describe(page):
    # Mock the backend response for description
    page.route("**/api/generate-description", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"description": "A generated description of a pothole"}'
    ))

    # Also mock severity detection if it triggers
    page.route("**/api/detect-severity", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"level": "Medium", "raw_label": "pothole", "confidence": 0.8}'
    ))

    # Go directly to Report page to avoid navigation menu interaction issues
    page.goto("http://localhost:5173/report")

    # Wait for page load
    page.wait_for_timeout(2000)

    # Verify we are on Report Form
    expect(page.get_by_role("heading", name="Report an Issue")).to_be_visible()

    # Upload an image
    with open("dummy.jpg", "wb") as f:
        f.write(b"dummy image content")

    # There are two file inputs (upload and camera). We want the upload one.
    # The first one is usually the upload one.
    # Or locate by name/id if available.
    # Looking at ReportForm.jsx would help, but let's assume first input[type=file] is correct
    # or look for the one associated with the Upload UI.

    # Try setting on the first file input found
    page.locator('input[type="file"]').first.set_input_files("dummy.jpg")

    # Wait for "Auto-fill description from image" button to appear
    # The text might be "Auto-fill description from image" or similar.
    # Let's verify visibility before clicking.
    auto_describe_btn = page.get_by_role("button", name="Auto-fill description from image")
    expect(auto_describe_btn).to_be_visible()

    # Click it
    auto_describe_btn.click()

    # Verify description is updated
    # It might take a moment
    page.wait_for_timeout(1000)
    expect(page.locator("textarea")).to_have_value("A generated description of a pothole")

    # Screenshot
    page.screenshot(path="/home/jules/verification/verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_auto_describe(page)
            print("Verification script finished successfully.")
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()
