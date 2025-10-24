"""
Direct search for AWS Key Management Service
"""

from playwright.sync_api import sync_playwright

def direct_kms_search():
    """Direct search for AWS Key Management Service"""
    print("[INFO] Direct search for AWS Key Management Service...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to calculator
            print("[INFO] Navigating to AWS Calculator...")
            page.goto("https://calculator.aws/#/")
            
            # Create estimate
            page.wait_for_selector("text='Create estimate'")
            page.click("text='Create estimate'")
            print("[OK] Successfully navigated to AWS Calculator")
            
            # Click "Add service" button
            page.click("text='Add service'")
            page.wait_for_timeout(3000)
            print("[OK] Clicked 'Add service' button")
            
            # Look for AWS Key Management Service button directly
            print("\n[INFO] Looking for AWS Key Management Service button...")
            
            # Try different possible button selectors
            possible_selectors = [
                "button[aria-label*='AWS Key Management Service']",
                "button[aria-label*='Key Management Service']", 
                "button[aria-label*='Configure AWS Key Management Service']",
                "button[aria-label*='Configure Key Management Service']",
                "button:has-text('AWS Key Management Service')",
                "button:has-text('Key Management Service')"
            ]
            
            found_button = None
            for selector in possible_selectors:
                try:
                    button = page.locator(selector)
                    if button.count() > 0:
                        aria_label = button.first.get_attribute("aria-label")
                        print(f"[FOUND] Button with selector '{selector}': {aria_label}")
                        found_button = button.first
                        break
                except:
                    continue
            
            if found_button:
                try:
                    found_button.click()
                    page.wait_for_timeout(3000)
                    print("[OK] Clicked AWS Key Management Service button")
                    print("[SUCCESS] Successfully navigated to AWS Key Management Service configuration page")
                    return True
                except Exception as e:
                    print(f"[WARNING] Could not click button: {e}")
            
            # If not found, list all available services
            print("\n[INFO] AWS Key Management Service not found. Listing all available services...")
            
            # Get all buttons on the page
            all_buttons = page.query_selector_all("button")
            print(f"[INFO] Found {all_buttons.count()} total buttons")
            
            # Look for any button containing "Key" or "Management"
            key_related_buttons = []
            for i in range(min(100, all_buttons.count())):  # Check first 100 buttons
                try:
                    button = all_buttons.nth(i)
                    text = button.text_content()
                    aria_label = button.get_attribute("aria-label")
                    
                    if text and any(keyword in text.lower() for keyword in ['key', 'management', 'kms']):
                        key_related_buttons.append(f"Text: {text}")
                        print(f"[KEY-RELATED] {text}")
                    elif aria_label and any(keyword in aria_label.lower() for keyword in ['key', 'management', 'kms']):
                        key_related_buttons.append(f"Aria: {aria_label}")
                        print(f"[KEY-RELATED] {aria_label}")
                except:
                    continue
            
            if key_related_buttons:
                print(f"\n[SUCCESS] Found {len(key_related_buttons)} key-related services:")
                for button in key_related_buttons:
                    print(f"  - {button}")
            else:
                print("\n[INFO] No key-related services found")
                print("[INFO] AWS Key Management Service might not be available in the calculator")
            
            return len(key_related_buttons) > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to search for AWS Key Management Service: {e}")
            return False
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

def main():
    """Main function"""
    print("[INFO] Direct AWS Key Management Service Search")
    
    found = direct_kms_search()
    
    if found:
        print("\n[SUCCESS] AWS Key Management Service found!")
        print("[INFO] You can proceed with creating a KMS configurator")
    else:
        print("\n[INFO] AWS Key Management Service not found")
        print("[INFO] KMS might not be available as a standalone service in AWS Calculator")

if __name__ == "__main__":
    main()
