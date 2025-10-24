"""
Explore all available services on AWS Calculator
"""

from playwright.sync_api import sync_playwright

class CalculatorExplorer:
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

    def explore_services(self):
        try:
            print("\n[INFO] Exploring available services...")
            
            # Look for service categories or lists
            categories = self.page.locator("div[data-testid*='service-category']")
            if categories.count() > 0:
                print(f"Found {categories.count()} service categories")
                for i in range(categories.count()):
                    print(f"  Category {i+1}: {categories.nth(i).text_content()}")
            
            # Look for service buttons or links
            service_buttons = self.page.locator("button[aria-label*='Configure']")
            if service_buttons.count() > 0:
                print(f"Found {service_buttons.count()} service configuration buttons")
                for i in range(service_buttons.count()):
                    print(f"  Service {i+1}: {service_buttons.nth(i).get_attribute('aria-label')}")
            
            # Look for service search results
            search_results = self.page.locator("div[data-testid*='service-search-results']")
            if search_results.count() > 0:
                print(f"Found {search_results.count()} service search result containers")
            
            # Try to find EC2 specifically
            ec2_elements = self.page.locator("text*='EC2'")
            if ec2_elements.count() > 0:
                print(f"Found {ec2_elements.count()} EC2-related elements")
                for i in range(ec2_elements.count()):
                    print(f"  EC2 Element {i+1}: {ec2_elements.nth(i).text_content()}")
            
            # Look for compute-related services
            compute_elements = self.page.locator("text*='Compute'")
            if compute_elements.count() > 0:
                print(f"Found {compute_elements.count()} Compute-related elements")
                for i in range(compute_elements.count()):
                    print(f"  Compute Element {i+1}: {compute_elements.nth(i).text_content()}")
            
        except Exception as e:
            print(f"[ERROR] Failed to explore services: {e}")

    def search_for_ec2_alternatives(self):
        try:
            print("\n[INFO] Searching for EC2 alternatives...")
            
            # Try different search terms
            search_terms = ["EC2", "Compute", "Instance", "Virtual Machine", "Server", "Amazon EC2", "AWS EC2"]
            
            for term in search_terms:
                try:
                    print(f"\n[INFO] Searching for: {term}")
                    # Clear any existing search
                    self.page.fill('input[placeholder*="Find Service"]', '')
                    self.page.wait_for_timeout(1000)
                    
                    # Search for the term
                    self.page.fill('input[placeholder*="Find Service"]', term)
                    self.page.wait_for_timeout(2000)
                    
                    # Look for results
                    results = self.page.locator("div[data-testid*='service-search-results']")
                    if results.count() > 0:
                        print(f"  Found search results for '{term}'")
                        # Get all text in the results
                        result_text = results.text_content()
                        if result_text:
                            print(f"  Results: {result_text}")
                    else:
                        print(f"  No results found for '{term}'")
                        
                except Exception as e:
                    print(f"  Error searching for '{term}': {e}")
            
        except Exception as e:
            print(f"[ERROR] Failed to search for EC2 alternatives: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        explorer = CalculatorExplorer(page)

        if explorer.navigate_to_calculator():
            explorer.explore_services()
            explorer.search_for_ec2_alternatives()
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
