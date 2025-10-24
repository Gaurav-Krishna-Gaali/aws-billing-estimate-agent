# aws_calculator_playwright_test.py
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set headless=False for debugging
        page = browser.new_page()
        
        # Go to AWS Pricing Calculator
        page.goto("https://calculator.aws")

        # Wait for the pricing calculator app to load
        page.wait_for_selector('text=Create estimate', timeout=15000)

        page.click("text='Create estimate'")

        # Screenshot for confirmation
        page.screenshot(path="aws_calculator_home.png")
        print("✅ AWS Pricing Calculator loaded. Screenshot saved as aws_calculator_home.png")

        # Print the final URL
        print("Current URL:", page.url)

        browser.close()

if __name__ == "__main__":
    run()
