"""
WAF Search Test
Test different search terms to find WAF in AWS Calculator
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class WAFSearchTest(BaseAWSConfigurator):
    """WAF search test class"""
    
    def __init__(self, page):
        super().__init__(page, "WAF")
    
    def test_waf_search_terms(self):
        """Test different search terms for WAF"""
        search_terms = [
            "WAF",
            "Web Application Firewall", 
            "AWS WAF",
            "AWS Web Application Firewall",
            "WAFv2",
            "AWS WAFv2",
            "Web ACL",
            "Firewall",
            "Application Firewall",
            "Web Security",
            "DDoS",
            "Shield",
            "Security",
            "Protection"
        ]
        
        print("[INFO] Testing WAF search terms...")
        
        for term in search_terms:
            try:
                print(f"\n[INFO] Testing search term: '{term}'")
                
                # Navigate to calculator
                if not self.navigate_to_calculator():
                    print(f"[ERROR] Failed to navigate to calculator for '{term}'")
                    continue
                
                # Search for the term
                if self.search_and_select_service(term):
                    print(f"[SUCCESS] Found service with term: '{term}'")
                    
                    # Take screenshot
                    self.take_screenshot(f"waf_search_{term.replace(' ', '_').lower()}.png")
                    
                    # Get current URL
                    current_url = self.page.url
                    print(f"[INFO] Current URL: {current_url}")
                    
                    # Map elements quickly
                    elements = self.map_all_elements()
                    total_elements = sum(len(v) for v in elements.values())
                    print(f"[INFO] Found {total_elements} interactive elements")
                    
                    return True
                else:
                    print(f"[FAILED] No service found for term: '{term}'")
                    
            except Exception as e:
                print(f"[ERROR] Error testing '{term}': {e}")
                continue
        
        return False


def main():
    """Main function"""
    print("[INFO] WAF Search Test - Finding WAF in AWS Calculator")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        search_test = WAFSearchTest(page)
        
        if search_test.test_waf_search_terms():
            print("\n[SUCCESS] Found WAF service!")
        else:
            print("\n[ERROR] Could not find WAF service with any search term")
            print("[INFO] WAF might not be available in AWS Calculator or has a different name")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
