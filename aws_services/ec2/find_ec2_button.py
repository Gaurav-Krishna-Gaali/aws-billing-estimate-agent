"""
Find the exact EC2 button text and attributes
"""

from playwright.sync_api import sync_playwright

class EC2ButtonFinder:
    def __init__(self, page):
        self.page = page

    def navigate_to_calculator(self):
        try:
            self.page.goto("https://calculator.aws/#/estimate")
            self.page.wait_for_selector("text='Add service'")
            print("[OK] Successfully navigated to AWS Calculator")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS Calculator: {e}")
            return False

    def find_ec2_button(self):
        try:
            print("\n[INFO] Looking for EC2 button...")
            
            # Click "Add service" button
            try:
                self.page.click("text='Add service'")
                self.page.wait_for_timeout(2000)
                print("[OK] Clicked 'Add service' button")
            except Exception as e:
                print(f"[WARNING] Could not click 'Add service' button: {e}")
            
            # Look for all buttons containing "EC2"
            ec2_buttons = self.page.locator("button:has-text('EC2')")
            if ec2_buttons.count() > 0:
                print(f"Found {ec2_buttons.count()} buttons containing 'EC2'")
                for i in range(ec2_buttons.count()):
                    button = ec2_buttons.nth(i)
                    print(f"  Button {i+1}: {button.text_content()}")
                    print(f"    Aria-label: {button.get_attribute('aria-label')}")
                    print(f"    Class: {button.get_attribute('class')}")
            else:
                print("No buttons containing 'EC2' found")
            
            # Look for all buttons containing "Amazon"
            amazon_buttons = self.page.locator("button:has-text('Amazon')")
            if amazon_buttons.count() > 0:
                print(f"Found {amazon_buttons.count()} buttons containing 'Amazon'")
                for i in range(amazon_buttons.count()):
                    button = amazon_buttons.nth(i)
                    text = button.text_content()
                    if 'EC2' in text:
                        print(f"  Amazon EC2 Button {i+1}: {text}")
                        print(f"    Aria-label: {button.get_attribute('aria-label')}")
                        print(f"    Class: {button.get_attribute('class')}")
            
            # Look for all buttons with aria-label containing "Configure"
            configure_buttons = self.page.locator("button[aria-label*='Configure']")
            if configure_buttons.count() > 0:
                print(f"Found {configure_buttons.count()} buttons with 'Configure' in aria-label")
                for i in range(configure_buttons.count()):
                    button = configure_buttons.nth(i)
                    aria_label = button.get_attribute('aria-label')
                    if 'EC2' in aria_label:
                        print(f"  Configure EC2 Button {i+1}: {aria_label}")
                        print(f"    Text: {button.text_content()}")
                        print(f"    Class: {button.get_attribute('class')}")
            
            # Look for all buttons with aria-label containing "Amazon"
            amazon_configure_buttons = self.page.locator("button[aria-label*='Amazon']")
            if amazon_configure_buttons.count() > 0:
                print(f"Found {amazon_configure_buttons.count()} buttons with 'Amazon' in aria-label")
                for i in range(amazon_configure_buttons.count()):
                    button = amazon_configure_buttons.nth(i)
                    aria_label = button.get_attribute('aria-label')
                    if 'EC2' in aria_label:
                        print(f"  Amazon EC2 Button {i+1}: {aria_label}")
                        print(f"    Text: {button.text_content()}")
                        print(f"    Class: {button.get_attribute('class')}")
            
        except Exception as e:
            print(f"[ERROR] Failed to find EC2 button: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        finder = EC2ButtonFinder(page)

        if finder.navigate_to_calculator():
            finder.find_ec2_button()
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
