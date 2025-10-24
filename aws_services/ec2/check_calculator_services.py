"""
Check what services are actually available on AWS Calculator
"""

from playwright.sync_api import sync_playwright

class CalculatorServiceChecker:
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

    def check_available_services(self):
        try:
            print("\n[INFO] Checking available services...")
            
            # Look for the "Add service" button and click it
            add_service_button = self.page.locator("text='Add service'")
            if add_service_button.count() > 0:
                print("[INFO] Clicking 'Add service' button...")
                add_service_button.first.click()
                self.page.wait_for_timeout(2000)
            
            # Look for service categories
            categories = self.page.locator("div[data-testid*='service-category']")
            if categories.count() > 0:
                print(f"Found {categories.count()} service categories")
                for i in range(categories.count()):
                    print(f"  Category {i+1}: {categories.nth(i).text_content()}")
            
            # Look for service buttons
            service_buttons = self.page.locator("button[aria-label*='Configure']")
            if service_buttons.count() > 0:
                print(f"Found {service_buttons.count()} service configuration buttons")
                for i in range(service_buttons.count()):
                    print(f"  Service {i+1}: {service_buttons.nth(i).get_attribute('aria-label')}")
            
            # Look for any text containing "EC2" or "Compute"
            ec2_elements = self.page.locator("text=EC2")
            if ec2_elements.count() > 0:
                print(f"Found {ec2_elements.count()} EC2 elements")
                for i in range(ec2_elements.count()):
                    print(f"  EC2 Element {i+1}: {ec2_elements.nth(i).text_content()}")
            
            compute_elements = self.page.locator("text=Compute")
            if compute_elements.count() > 0:
                print(f"Found {compute_elements.count()} Compute elements")
                for i in range(compute_elements.count()):
                    print(f"  Compute Element {i+1}: {compute_elements.nth(i).text_content()}")
            
            # Look for any text containing "Instance"
            instance_elements = self.page.locator("text=Instance")
            if instance_elements.count() > 0:
                print(f"Found {instance_elements.count()} Instance elements")
                for i in range(instance_elements.count()):
                    print(f"  Instance Element {i+1}: {instance_elements.nth(i).text_content()}")
            
            # Look for any text containing "Virtual"
            virtual_elements = self.page.locator("text=Virtual")
            if virtual_elements.count() > 0:
                print(f"Found {virtual_elements.count()} Virtual elements")
                for i in range(virtual_elements.count()):
                    print(f"  Virtual Element {i+1}: {virtual_elements.nth(i).text_content()}")
            
            # Look for any text containing "Server"
            server_elements = self.page.locator("text=Server")
            if server_elements.count() > 0:
                print(f"Found {server_elements.count()} Server elements")
                for i in range(server_elements.count()):
                    print(f"  Server Element {i+1}: {server_elements.nth(i).text_content()}")
            
        except Exception as e:
            print(f"[ERROR] Failed to check available services: {e}")

    def search_for_services(self):
        try:
            print("\n[INFO] Searching for services...")
            
            # Look for search input
            search_input = self.page.locator("input[placeholder*='Find Service']")
            if search_input.count() > 0:
                print("[INFO] Found search input, trying to search...")
                
                # Try searching for "EC2"
                try:
                    search_input.fill("EC2")
                    self.page.wait_for_timeout(2000)
                    print("  Searched for 'EC2'")
                except:
                    print("  Could not search for 'EC2'")
                
                # Try searching for "Compute"
                try:
                    search_input.fill("Compute")
                    self.page.wait_for_timeout(2000)
                    print("  Searched for 'Compute'")
                except:
                    print("  Could not search for 'Compute'")
                
                # Try searching for "Instance"
                try:
                    search_input.fill("Instance")
                    self.page.wait_for_timeout(2000)
                    print("  Searched for 'Instance'")
                except:
                    print("  Could not search for 'Instance'")
            else:
                print("[WARNING] No search input found")
            
        except Exception as e:
            print(f"[ERROR] Failed to search for services: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        checker = CalculatorServiceChecker(page)

        if checker.navigate_to_calculator():
            checker.check_available_services()
            checker.search_for_services()
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
