"""
Check Security Services
See what security-related services are available in AWS Calculator
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

def check_security_services():
    """Check what security services are available"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to calculator
        page.goto("https://calculator.aws/#/")
        page.wait_for_selector("text='Create estimate'")
        page.click("text='Create estimate'")
        page.wait_for_selector("input[placeholder='Search for a service']")
        
        # Try to find security services
        security_terms = ["security", "firewall", "waf", "shield", "ddos", "protection"]
        
        for term in security_terms:
            try:
                print(f"\n[INFO] Searching for: {term}")
                search_input = page.locator("input[placeholder='Search for a service']")
                search_input.fill(term)
                page.wait_for_timeout(2000)
                
                # Check if any results appear
                results = page.locator("text=" + term).count()
                if results > 0:
                    print(f"[SUCCESS] Found {results} results for '{term}'")
                else:
                    print(f"[INFO] No results for '{term}'")
                    
            except Exception as e:
                print(f"[ERROR] Error searching for '{term}': {e}")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    check_security_services()
