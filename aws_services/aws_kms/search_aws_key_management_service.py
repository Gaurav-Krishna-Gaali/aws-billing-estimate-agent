"""
Search for AWS Key Management Service specifically
"""

from playwright.sync_api import sync_playwright


def search_aws_key_management_service():
    """Search for AWS Key Management Service"""
    print("[INFO] Searching for 'AWS Key Management Service'...")
    
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
            
            # Search for "AWS Key Management Service" specifically
            print("\n[INFO] Searching for 'AWS Key Management Service'...")
            
            # Try to find the service by exact name
            service_buttons = page.query_selector_all("button")
            found_service = None
            
            for i in range(service_buttons.count()):
                try:
                    aria_label = service_buttons.nth(i).get_attribute("aria-label")
                    button_text = service_buttons.nth(i).text_content()
                    
                    if aria_label and "AWS Key Management Service" in aria_label:
                        found_service = aria_label
                        print(f"[FOUND] AWS Key Management Service: {aria_label}")
                        break
                    elif button_text and "AWS Key Management Service" in button_text:
                        found_service = button_text
                        print(f"[FOUND] AWS Key Management Service: {button_text}")
                        break
                    elif aria_label and "Key Management" in aria_label:
                        print(f"[POTENTIAL] {aria_label}")
                    elif button_text and "Key Management" in button_text:
                        print(f"[POTENTIAL] {button_text}")
                        
                except Exception as e:
                    continue
            
            if found_service:
                print(f"\n[SUCCESS] Found AWS Key Management Service!")
                print(f"[SERVICE] {found_service}")
                
                # Try to click the service
                try:
                    if "Configure" in found_service:
                        # It's already a configure button
                        service_button = page.locator(f"button[aria-label='{found_service}']")
                        if service_button.count() > 0:
                            service_button.first.click()
                            page.wait_for_timeout(3000)
                            print("[OK] Clicked AWS Key Management Service button")
                            print("[SUCCESS] Successfully navigated to AWS Key Management Service configuration page")
                            return True
                    else:
                        # Look for configure button
                        configure_button = page.locator(f"button[aria-label*='Configure AWS Key Management Service']")
                        if configure_button.count() > 0:
                            configure_button.first.click()
                            page.wait_for_timeout(3000)
                            print("[OK] Clicked Configure AWS Key Management Service button")
                            print("[SUCCESS] Successfully navigated to AWS Key Management Service configuration page")
                            return True
                except Exception as e:
                    print(f"[WARNING] Could not click AWS Key Management Service: {e}")
                
            else:
                print("\n[INFO] AWS Key Management Service not found")
                print("[INFO] Let me check all available services...")
                
                # List all services to see what's available
                print("\n[INFO] All available services:")
                for i in range(min(50, service_buttons.count())):
                    try:
                        aria_label = service_buttons.nth(i).get_attribute("aria-label")
                        if aria_label and "Configure" in aria_label:
                            print(f"  {i+1}. {aria_label}")
                    except:
                        pass
            
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to search for AWS Key Management Service: {e}")
            return False
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def main():
    """Main function"""
    print("[INFO] AWS Key Management Service Searcher")
    print("[INFO] Searching for 'AWS Key Management Service' in AWS Calculator")
    
    found = search_aws_key_management_service()
    
    if found:
        print("\n[SUCCESS] AWS Key Management Service is available!")
        print("[INFO] You can proceed with creating a KMS configurator")
    else:
        print("\n[INFO] AWS Key Management Service not found")
        print("[INFO] It might be named differently or not available")


if __name__ == "__main__":
    main()
