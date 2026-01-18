import os
import time
from playwright.sync_api import sync_playwright

def verify_audio_ui():
    with sync_playwright() as p:
        # Launch browser with fake media stream to simulate microphone
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream"
            ]
        )
        context = browser.new_context(
            permissions=["microphone"]
        )
        page = context.new_page()

        # Navigate to the app (assuming it's running locally on port 5173 or we can serve it)
        # Since I can't easily start the dev server and keep it running in the background reliably in this environment without blocking,
        # I will rely on the fact that I can't fully render React without a server.
        # However, I can try to start it in background.

        # NOTE: For this environment, I'll try to start the frontend server in the background first.
        page.goto("http://localhost:5173/")

        # Wait for app to load
        page.wait_for_selector("text=Smart City Scanner", timeout=10000)

        # Click on "Report Issue" or navigate to ReportForm if reachable
        # The home page has a button to report issue usually, or we can go to /report
        # Let's try to find a way to the report form.
        # Assuming there is a "Report Issue" button or similar.
        # Based on file structure, Home.jsx likely links to ReportForm.

        # Let's try to find a button that looks like it goes to report.
        # Or navigate directly if router allows.
        page.goto("http://localhost:5173/report")

        # Wait for the description field
        page.wait_for_selector("textarea[placeholder='Describe the issue...']")

        # Check for the microphone button
        mic_button = page.locator("button[title='Record voice note']")
        if mic_button.is_visible():
            print("Microphone button is visible.")

            # Take a screenshot of the initial state
            page.screenshot(path="frontend_verification/audio_ui_initial.png")

            # Click the microphone button to start recording
            mic_button.click()

            # Wait a bit to simulate recording state
            time.sleep(1)

            # Check if button changed to stop (square icon or title change)
            stop_button = page.locator("button[title='Stop recording']")
            if stop_button.is_visible():
                print("Stop button is visible (Recording active).")
                page.screenshot(path="frontend_verification/audio_ui_recording.png")

                # Stop recording
                stop_button.click()
                print("Stopped recording.")

                # Wait for transcription attempt (it might fail if backend isn't reachable, but UI should handle it)
                # We mainly verify UI existence here.
            else:
                print("Failed to enter recording state.")
        else:
            print("Microphone button not found.")

        browser.close()

if __name__ == "__main__":
    verify_audio_ui()
