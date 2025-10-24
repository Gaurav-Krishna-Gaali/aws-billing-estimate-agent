"""
Find WAF Service
Find the exact WAF service name in AWS Calculator
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

def find_waf_service():
    """Find the exact WAF service name"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to calculator
        page.goto("https://calculator.aws/#/")
        page.wait_for_selector("text='Create estimate'")
        page.click("text='Create estimate'")
        page.wait_for_selector("input[placeholder='Search for a service']")
        
        # Search for WAF
        search_input = page.locator("input[placeholder='Search for a service']")
        search_input.fill("waf")
        page.wait_for_timeout(3000)
        
        # Get all visible text that might be WAF services
        print("[INFO] Looking for WAF services...")
        
        # Try to find clickable WAF services
        waf_elements = page.locator("text=/.*[Ww][Aa][Ff].*/").all()
        print(f"[INFO] Found {len(waf_elements)} WAF-related elements")
        
        for i, element in enumerate(waf_elements):
            try:
                text = element.text_content()
                print(f"[INFO] WAF Element {i+1}: '{text}'")
            except:
                pass
        
        # Try to find any clickable services
        clickable_services = page.locator("button, a").all()
        print(f"\n[INFO] Found {len(clickable_services)} clickable elements")
        
        for i, element in enumerate(clickable_services[:10]):  # Check first 10
            try:
                text = element.text_content()
                if text and ('waf' in text.lower() or 'firewall' in text.lower()):
                    print(f"[INFO] Clickable WAF Service {i+1}: '{text}'")
            except:
                pass
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    find_waf_service()
