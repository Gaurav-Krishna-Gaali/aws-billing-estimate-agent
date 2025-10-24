"""
Find KMS service in AWS Calculator
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


def find_kms_service():
    """Find KMS service in AWS Calculator"""
    print("[INFO] Finding KMS service in AWS Calculator...")
    
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
            page.wait_for_timeout(2000)
            print("[OK] Clicked 'Add service' button")
            
            # List all available services
            print("\n[INFO] Listing all available services...")
            configure_buttons = page.query_selector_all("button[aria-label*='Configure']")
            total_services = configure_buttons.count()
            print(f"[INFO] Found {total_services} total services")
            
            kms_services = []
            for i in range(total_services):
                try:
                    aria_label = configure_buttons.nth(i).get_attribute("aria-label")
                    if aria_label:
                        # Check if it's KMS-related
                        if any(keyword in aria_label.lower() for keyword in 
                              ['kms', 'key', 'encryption', 'cryptographic', 'cmk']):
                            kms_services.append(aria_label)
                            print(f"[KMS-RELATED] {i+1}. {aria_label}")
                        elif i < 30:  # Show first 30 services
                            print(f"[SERVICE] {i+1}. {aria_label}")
                except Exception as e:
                    print(f"[WARNING] Could not get service {i+1}: {e}")
            
            if kms_services:
                print(f"\n[SUCCESS] Found {len(kms_services)} KMS-related services:")
                for service in kms_services:
                    print(f"  - {service}")
            else:
                print("\n[INFO] No KMS-related services found")
                print("[INFO] KMS might be included in other services or not available as standalone")
                
                # Check if KMS is mentioned in other services
                print("\n[INFO] Checking for KMS mentions in service descriptions...")
                all_text = page.text_content()
                if 'kms' in all_text.lower() or 'key management' in all_text.lower():
                    print("[INFO] KMS is mentioned in the page - it might be part of another service")
                else:
                    print("[INFO] No KMS mentions found - KMS might not be available in the calculator")
            
            return kms_services
            
        except Exception as e:
            print(f"[ERROR] Failed to find KMS service: {e}")
            return []
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def main():
    """Main function"""
    print("[INFO] AWS KMS Service Finder")
    print("[INFO] Searching for KMS service in AWS Calculator")
    
    kms_services = find_kms_service()
    
    if kms_services:
        print(f"\n[SUCCESS] Found KMS services: {kms_services}")
    else:
        print("\n[INFO] No dedicated KMS service found")
        print("[INFO] KMS costs are typically included in other AWS services")
        print("[INFO] KMS pricing is usually based on API calls and key usage")


if __name__ == "__main__":
    main()
