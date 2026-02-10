from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            '--use-fake-ui-for-media-stream',
            '--use-fake-device-for-media-stream',
            '--no-sandbox'
        ]
    )
    context = browser.new_context(
        permissions=['camera']
    )
    page = context.new_page()

    try:
        # 1. Go to Landing
        print("Navigating to landing...")
        page.goto("http://localhost:5173", timeout=60000)
        page.wait_for_load_state("networkidle")

        # Click Call Action Issue
        action_btn = page.get_by_text("Call Action Issue")
        if action_btn.is_visible():
             print("Clicking Call Action Issue...")
             action_btn.click()
             page.wait_for_timeout(3000)
        else:
             print("Call Action Issue button not found, maybe already on home?")

        # Take screenshot of home
        page.screenshot(path="verification/home_buttons.png")
        print("Home screenshot taken")

        # Scroll down
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        # 2. Check for Public Facilities button
        # It has text "Public Facilities"
        pub_btn = page.get_by_text("Public Facilities", exact=True)
        if pub_btn.count() > 0:
            print("Public Facilities button found")
            pub_btn.first.click()
            page.wait_for_timeout(3000) # Wait for lazy load
            # Check header
            if page.get_by_text("Public Facilities Check").is_visible():
                print("Public Facilities page loaded")
                page.screenshot(path="verification/public_facilities.png")
            else:
                print("Public Facilities header not found")
        else:
            print("Public Facilities button not found")
            page.screenshot(path="verification/missing_pf_button.png", full_page=True)

        # Go back
        print("Going back...")
        page.go_back()
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        # 3. Check for Construction Safety button
        const_btn = page.get_by_text("Construction Safety", exact=True)
        if const_btn.count() > 0:
            print("Construction Safety button found")
            const_btn.first.click()
            page.wait_for_timeout(3000)
            # Check header
            if page.get_by_text("Construction Site Safety").is_visible():
                print("Construction Safety page loaded")
                page.screenshot(path="verification/construction_safety.png")
            else:
                print("Construction Safety header not found")
        else:
            print("Construction Safety button not found")
            page.screenshot(path="verification/missing_button.png", full_page=True)

    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="verification/error.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
