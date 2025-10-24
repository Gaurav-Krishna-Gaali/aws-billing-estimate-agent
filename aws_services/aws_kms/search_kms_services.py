"""
Search for KMS-related services in AWS Calculator
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class KMSServiceSearcher(BaseAWSConfigurator):
    """Search for KMS-related services"""
    
    def __init__(self, page):
        super().__init__(page, "KMS Search")
    
    def search_for_kms_services(self):
        """Search for KMS-related services"""
        try:
            print("[INFO] Searching for KMS-related services...")
            
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Click "Add service" button
            try:
                self.page.click("text='Add service'")
                self.page.wait_for_timeout(2000)
                print("[OK] Clicked 'Add service' button")
            except Exception as e:
                print(f"[WARNING] Could not click 'Add service' button: {e}")
            
            # Search for various KMS-related terms
            search_terms = [
                "KMS",
                "Key Management",
                "AWS KMS", 
                "Key Management Service",
                "Encryption",
                "Keys",
                "Cryptographic",
                "CMK",
                "Customer Master Key"
            ]
            
            for term in search_terms:
                try:
                    print(f"\n[INFO] Searching for: {term}")
                    
                    # Clear and fill search
                    search_input = self.page.locator("input[placeholder*='Search']")
                    if search_input.count() > 0:
                        search_input.first.fill(term)
                        self.page.wait_for_timeout(2000)
                        
                        # Look for any results
                        results = self.page.query_selector_all("button[aria-label*='Configure']")
                        print(f"[INFO] Found {results.count()} potential services for '{term}'")
                        
                        for i in range(min(5, results.count())):  # Show first 5 results
                            try:
                                aria_label = results.nth(i).get_attribute("aria-label")
                                print(f"  {i+1}. {aria_label}")
                            except:
                                pass
                    else:
                        print(f"[WARNING] Search input not found for '{term}'")
                        
                except Exception as e:
                    print(f"[WARNING] Could not search for '{term}': {e}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to search for KMS services: {e}")
            return False
    
    def list_all_available_services(self):
        """List all available services to find KMS"""
        try:
            print("\n[INFO] Listing all available services...")
            
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Click "Add service" button
            try:
                self.page.click("text='Add service'")
                self.page.wait_for_timeout(2000)
                print("[OK] Clicked 'Add service' button")
            except Exception as e:
                print(f"[WARNING] Could not click 'Add service' button: {e}")
            
            # Get all configure buttons
            configure_buttons = self.page.query_selector_all("button[aria-label*='Configure']")
            print(f"[INFO] Found {configure_buttons.count()} total services")
            
            kms_related = []
            for i in range(configure_buttons.count()):
                try:
                    aria_label = configure_buttons.nth(i).get_attribute("aria-label")
                    if aria_label and any(keyword in aria_label.lower() for keyword in 
                                        ['kms', 'key', 'encryption', 'cryptographic', 'cmk']):
                        kms_related.append(aria_label)
                        print(f"[KMS-RELATED] {i+1}. {aria_label}")
                    elif i < 20:  # Show first 20 services
                        print(f"[SERVICE] {i+1}. {aria_label}")
                except:
                    pass
            
            if kms_related:
                print(f"\n[SUCCESS] Found {len(kms_related)} KMS-related services:")
                for service in kms_related:
                    print(f"  - {service}")
            else:
                print("\n[INFO] No KMS-related services found in first 20 services")
                print("[INFO] KMS might be included in other services or not available as standalone")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to list services: {e}")
            return False


def main():
    """Main function"""
    print("[INFO] AWS KMS Service Searcher")
    print("[INFO] Searching for KMS-related services in AWS Calculator")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        searcher = KMSServiceSearcher(page)
        
        # Search for KMS services
        searcher.search_for_kms_services()
        
        # List all available services
        searcher.list_all_available_services()
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
