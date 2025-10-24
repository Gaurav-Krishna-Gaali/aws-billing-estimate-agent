"""
Search for Amazon Virtual Private Cloud (VPC) in AWS Calculator
"""

from playwright.sync_api import sync_playwright

def search_amazon_vpc():
    """Search for Amazon VPC service"""
    print("[INFO] Searching for 'Amazon Virtual Private Cloud (VPC)'...")
    
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
            
            # Search for Amazon VPC
            print("\n[INFO] Searching for Amazon VPC...")
            
            # Try different possible VPC service names
            vpc_search_terms = [
                "Amazon Virtual Private Cloud (VPC)",
                "Amazon VPC", 
                "VPC",
                "Virtual Private Cloud",
                "AWS VPC",
                "Configure Amazon VPC",
                "Configure VPC"
            ]
            
            found_service = None
            for search_term in vpc_search_terms:
                try:
                    # Look for button with this text or aria-label
                    button = page.locator(f"button[aria-label*='{search_term}']")
                    if button.count() > 0:
                        aria_label = button.first.get_attribute("aria-label")
                        print(f"[FOUND] {search_term}: {aria_label}")
                        found_service = aria_label
                        break
                    
                    # Also try text content
                    button = page.locator(f"button:has-text('{search_term}')")
                    if button.count() > 0:
                        text = button.first.text_content()
                        print(f"[FOUND] {search_term}: {text}")
                        found_service = text
                        break
                        
                except Exception as e:
                    continue
            
            if found_service:
                print(f"\n[SUCCESS] Found Amazon VPC service!")
                print(f"[SERVICE] {found_service}")
                
                # Try to click the service
                try:
                    if "Configure" in found_service:
                        # It's already a configure button
                        service_button = page.locator(f"button[aria-label='{found_service}']")
                        if service_button.count() > 0:
                            service_button.first.click()
                            page.wait_for_timeout(3000)
                            print("[OK] Clicked Amazon VPC button")
                            print("[SUCCESS] Successfully navigated to Amazon VPC configuration page")
                            return True
                    else:
                        # Look for configure button
                        configure_button = page.locator(f"button[aria-label*='Configure Amazon VPC']")
                        if configure_button.count() > 0:
                            configure_button.first.click()
                            page.wait_for_timeout(3000)
                            print("[OK] Clicked Configure Amazon VPC button")
                            print("[SUCCESS] Successfully navigated to Amazon VPC configuration page")
                            return True
                except Exception as e:
                    print(f"[WARNING] Could not click Amazon VPC: {e}")
                
            else:
                print("\n[INFO] Amazon VPC not found with direct search")
                print("[INFO] Let me check all available services...")
                
                # List all services to see what's available
                print("\n[INFO] All available services:")
                service_buttons = page.query_selector_all("button")
                vpc_related = []
                
                for i in range(min(100, service_buttons.count())):
                    try:
                        button = service_buttons.nth(i)
                        aria_label = button.get_attribute("aria-label")
                        text = button.text_content()
                        
                        if aria_label and any(keyword in aria_label.lower() for keyword in ['vpc', 'virtual', 'private', 'cloud', 'network', 'networking']):
                            vpc_related.append(f"Aria: {aria_label}")
                            print(f"[VPC-RELATED] {aria_label}")
                        elif text and any(keyword in text.lower() for keyword in ['vpc', 'virtual', 'private', 'cloud', 'network', 'networking']):
                            vpc_related.append(f"Text: {text}")
                            print(f"[VPC-RELATED] {text}")
                    except:
                        continue
                
                if vpc_related:
                    print(f"\n[SUCCESS] Found {len(vpc_related)} VPC-related services:")
                    for service in vpc_related:
                        print(f"  - {service}")
                else:
                    print("\n[INFO] No VPC-related services found")
                    print("[INFO] Amazon VPC might not be available as a standalone service in AWS Calculator")
            
            return len(vpc_related) > 0 if 'vpc_related' in locals() else False
            
        except Exception as e:
            print(f"[ERROR] Failed to search for Amazon VPC: {e}")
            return False
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

def main():
    """Main function"""
    print("[INFO] Amazon VPC Service Searcher")
    print("[INFO] Searching for 'Amazon Virtual Private Cloud (VPC)' in AWS Calculator")
    
    found = search_amazon_vpc()
    
    if found:
        print("\n[SUCCESS] Amazon VPC is available!")
        print("[INFO] You can proceed with creating a VPC configurator")
    else:
        print("\n[INFO] Amazon VPC not found")
        print("[INFO] VPC might be included in other services or not available as standalone")

if __name__ == "__main__":
    main()