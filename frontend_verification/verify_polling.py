from playwright.sync_api import sync_playwright, expect
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Intercept API calls to simulate backend behavior

        # 1. Recent issues (empty for clean state)
        page.route("**/api/issues/recent", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[]'
        ))

        # 2. Responsibility map (mock)
        page.route("**/api/responsibility-map", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{}'
        ))

        # 3. Create Issue
        page.route("**/api/issues", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 123, "message": "Issue reported", "action_plan": null}'
        ))

        # 4. Get Issue (Polling logic)
        call_count = {"count": 0}
        def handle_get_issue(route):
            call_count["count"] += 1
            print(f"Polling Attempt: {call_count['count']}")
            if call_count["count"] < 3:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"id": 123, "action_plan": null}'
                )
            else:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"id": 123, "action_plan": {"whatsapp": "This is a generated plan.", "email_subject": "Subject", "email_body": "Body", "x_post": "Tweet"}}'
                )

        page.route("**/api/issues/123", handle_get_issue)

        # Start Test
        print("Navigating to Home...")
        page.goto("http://localhost:5174/")

        # Debug: Wait and Screenshot
        page.wait_for_selector("#root")
        time.sleep(2) # Allow React to hydrate
        page.screenshot(path="frontend_verification/debug_home.png")

        # Go to Report Page
        print("Clicking 'Report an Issue'...")
        # Try a more generic selector or URL navigation if button not found
        try:
             page.get_by_role("link", name="Report an Issue").click()
        except:
             try:
                 page.get_by_text("Report an Issue").click()
             except:
                 print("Could not find link/button, navigating directly...")
                 page.goto("http://localhost:5174/report")

        # Fill Form
        print("Filling Form...")
        page.get_by_role("combobox").select_option("road")
        # Use more specific selector since there are multiple textboxes
        page.get_by_placeholder("Describe the issue...").fill("Test Pothole Description")

        # Submit
        print("Submitting...")
        page.get_by_role("button", name="Generate Action Plan").click()

        # Verify "Generating..." state
        print("Verifying Loading State...")
        expect(page.get_by_text("Generating Action Plan...")).to_be_visible()
        expect(page.get_by_text("Our AI is drafting")).to_be_visible()

        # Wait for polling to succeed (should take ~4-6 seconds based on interval and mock count)
        print("Waiting for Plan to appear...")
        # We expect the "Action Plan Generated!" text or specific button
        expect(page.get_by_text("Action Plan Generated!")).to_be_visible(timeout=10000)

        print("Plan Verified. Taking screenshot.")
        page.screenshot(path="frontend_verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run()
