from playwright.sync_api import sync_playwright

def add_bedrock_and_view_summary():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run without UI
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://calculator.aws/#/")
        page.wait_for_selector("text='Create estimate'")
        page.click("text='Create estimate'")
        page.wait_for_selector("input[placeholder='Search for a service']")
        # 4. Search for AWS Bedrock
        page.fill("input[placeholder='Search for a service']", "bedrock")
        page.wait_for_selector("text='Amazon Bedrock'")
        page.click("button[aria-label='Configure Amazon Bedrock']")
        # Wait for the button to be ready and click it
        print("[INFO] Looking for 'Save and add service' button...")
        page.wait_for_timeout(3000)
        
        # Wait for button to be attached to DOM
        page.wait_for_selector("button[aria-label='Save and add service']", state="attached", timeout=5000)
        print("[INFO] Button found, clicking with JavaScript...")
        
        # Use JavaScript click (the only method that works)
        page.evaluate("document.querySelector('button[aria-label=\"Save and add service\"]').click()")
        print("[OK] Successfully clicked 'Save and add service' button using JavaScript")
        
        # Wait for the page to process the click
        page.wait_for_timeout(3000)
        
        # Get the current URL to see if we're on the summary page
        current_url = page.url
        print(f"[INFO] Current URL: {current_url}")
        
        # Take a screenshot to see the result
        page.screenshot(path="after_save_click.png", full_page=True)
        print("[INFO] Screenshot saved as after_save_click.png")
        
        print("[OK] Estimate should be saved. Leave browser open to inspect.")
        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    add_bedrock_and_view_summary()
