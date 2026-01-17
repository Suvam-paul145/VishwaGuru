from playwright.sync_api import sync_playwright, expect
import time
import os

def run():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Since we can't easily run the full frontend-backend stack in this environment
        # without complex setup (background processes, proxying), and the verification
        # is about the "Loading..." state and polling logic which depends on API responses,
        # we will use Playwright's network interception to simulate the backend.

        # 1. Intercept the initial recent issues call
        page.route("**/api/issues/recent", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[]'
        ))

        # 2. Intercept the create issue call (POST)
        # Return success with ID, but NULL action_plan
        page.route("**/api/issues", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 123, "message": "Issue reported", "action_plan": null}'
        ))

        # 3. Intercept the get issue call (GET /api/issues/123)
        # First call: return null action plan (simulating processing)
        # Second call: return populated action plan

        call_count = {"count": 0}

        def handle_get_issue(route):
            call_count["count"] += 1
            print(f"Intercepted GET issue. Count: {call_count['count']}")

            if call_count["count"] <= 2: # Fail/Wait first 2 times
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"id": 123, "action_plan": null}'
                )
            else: # Return success
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"id": 123, "action_plan": {"whatsapp": "Ready!", "email_subject": "Sub", "email_body": "Body", "x_post": "Tweet"}}'
                )

        page.route("**/api/issues/123", handle_get_issue)

        # Also need to serve the frontend.
        # Since we are in a container without a running dev server for the frontend code we just modified,
        # we have a dilemma. We can't verify the *modified* frontend code unless we build/serve it.
        # But we can try to rely on the fact that we modified the source.

        # HOWEVER, the instructions say "Start the local development server".
        # I should try to start it.

        print("Done setup.")

if __name__ == "__main__":
    run()
