"""
Search for EC2-related services on AWS Calculator
"""

from playwright.sync_api import sync_playwright

class EC2ServiceSearcher:
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

    def search_for_service(self, service_name):
        try:
            print(f"\n[INFO] Searching for: {service_name}")
            self.page.fill('input[placeholder*="Find Service"]', service_name)
            self.page.wait_for_timeout(2000)  # Wait for search results to appear
            
            # Extract and print potential service names
            service_locators = self.page.locator("div[data-testid*='service-search-results'] span.awsui_text_1f1d4_ocied_5")
            count = service_locators.count()
            print(f"Found {count} potential services")
            for i in range(count):
                print(f"  {i+1}. {service_locators.nth(i).text_content()}")
            
        except Exception as e:
            print(f"[ERROR] Failed to search for {service_name}: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        searcher = EC2ServiceSearcher(page)

        if searcher.navigate_to_calculator():
            search_terms = ["EC2", "Compute", "Instance", "Amazon EC2", "AWS EC2", "Elastic Compute", "Virtual Machine", "VM"]
            for term in search_terms:
                searcher.search_for_service(term)
        
        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    main()
