"""
Simple KMS service check
"""

from playwright.sync_api import sync_playwright


def check_kms_availability():
    """Check if KMS is available in AWS Calculator"""
    print("[INFO] Checking KMS availability in AWS Calculator...")
    
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
            
            # Get page content to check for KMS
            page_content = page.text_content()
            
            # Check for KMS-related terms
            kms_terms = ['KMS', 'Key Management', 'AWS KMS', 'Key Management Service', 'Encryption']
            found_terms = []
            
            for term in kms_terms:
                if term in page_content:
                    found_terms.append(term)
                    print(f"[FOUND] {term} mentioned on page")
            
            if found_terms:
                print(f"\n[SUCCESS] Found KMS-related terms: {found_terms}")
            else:
                print("\n[INFO] No KMS-related terms found on the page")
            
            # Look for any buttons with KMS in the name
            print("\n[INFO] Looking for KMS-related buttons...")
            all_buttons = page.query_selector_all("button")
            kms_buttons = []
            
            for i in range(min(50, all_buttons.count())):  # Check first 50 buttons
                try:
                    button_text = all_buttons.nth(i).text_content()
                    aria_label = all_buttons.nth(i).get_attribute("aria-label")
                    
                    if button_text and any(term.lower() in button_text.lower() for term in ['kms', 'key', 'encryption']):
                        kms_buttons.append(f"Text: {button_text}")
                        print(f"[KMS BUTTON] {button_text}")
                    elif aria_label and any(term.lower() in aria_label.lower() for term in ['kms', 'key', 'encryption']):
                        kms_buttons.append(f"Aria: {aria_label}")
                        print(f"[KMS BUTTON] {aria_label}")
                except:
                    pass
            
            if kms_buttons:
                print(f"\n[SUCCESS] Found {len(kms_buttons)} KMS-related buttons")
            else:
                print("\n[INFO] No KMS-related buttons found")
                print("[INFO] KMS might not be available as a standalone service in AWS Calculator")
                print("[INFO] KMS costs are typically included in other AWS services")
            
            return len(kms_buttons) > 0 or len(found_terms) > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to check KMS availability: {e}")
            return False
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def main():
    """Main function"""
    print("[INFO] AWS KMS Availability Check")
    
    kms_available = check_kms_availability()
    
    if kms_available:
        print("\n[SUCCESS] KMS appears to be available in AWS Calculator")
        print("[INFO] You can proceed with creating a KMS configurator")
    else:
        print("\n[INFO] KMS does not appear to be available as a standalone service")
        print("[INFO] KMS pricing is typically included in other AWS services")
        print("[INFO] KMS costs are based on:")
        print("  - API calls (encrypt, decrypt, generate data key)")
        print("  - Key storage (customer managed keys)")
        print("  - Key usage (requests per month)")
        print("  - Data transfer (if applicable)")


if __name__ == "__main__":
    main()
