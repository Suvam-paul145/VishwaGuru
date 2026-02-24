from playwright.sync_api import sync_playwright
import time
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Mock API responses
    page.route("**/auth/me", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"id": 1, "email": "test@example.com", "full_name": "Test User", "role": "user"}'
    ))

    page.route("**/api/stats", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"total_issues": 100, "resolved_issues": 60, "pending_issues": 40}'
    ))

    # Set token in localStorage before navigation
    page.add_init_script("""
        localStorage.setItem('token', 'fake-token');
    """)

    # Navigate to Civic Insight page
    try:
        page.goto("http://localhost:5173/insight")
        # Wait for content to load
        page.wait_for_selector("text=Civic Intelligence Dashboard", timeout=30000)

        # Take screenshot
        screenshot_path = "verification_civic_insight.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"Error: {e}")
        # Try to capture whatever is on screen
        page.screenshot(path="error_screenshot.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
