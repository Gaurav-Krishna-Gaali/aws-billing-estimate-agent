"""
Search for ECS services in AWS Calculator
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

def search_ecs_services():
    """Search for ECS-related services"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = BaseAWSConfigurator(page, 'ECS')
        configurator.navigate_to_calculator()
        
        # Try different search terms
        search_terms = ['ECS', 'Fargate', 'Container', 'Amazon ECS', 'AWS ECS']
        
        for term in search_terms:
            print(f"\n[INFO] Searching for: {term}")
            try:
                # Clear and search
                page.fill('input[placeholder*="Search"]', '')
                page.fill('input[placeholder*="Search"]', term)
                page.wait_for_timeout(2000)
                
                # Look for service cards
                services = page.query_selector_all('[data-testid*="service"], .service-card, [class*="service"]')
                print(f"Found {len(services)} potential services")
                
                for i, service in enumerate(services[:5]):
                    text = service.text_content()
                    if text and len(text.strip()) > 0:
                        print(f"  {i+1}. {text.strip()[:100]}...")
                        
            except Exception as e:
                print(f"Error searching for {term}: {e}")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    search_ecs_services()
