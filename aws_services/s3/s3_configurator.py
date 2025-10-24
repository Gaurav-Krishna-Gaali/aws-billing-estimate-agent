"""
S3 Configuration Class
Maps all interactive elements on the S3 configuration page
"""

from playwright.sync_api import Page
from typing import Dict, Any
import json
import sys
import os

# Add parent directory to path to import base configurator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class S3Configurator(BaseAWSConfigurator):
    """S3 configuration class with all page elements mapped"""
    
    def __init__(self, page: Page):
        super().__init__(page, "S3")
    
    def navigate_to_s3_config(self) -> bool:
        """Navigate to S3 configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for S3 using the correct service name
            if not self.search_and_select_service("Amazon Simple Storage Service (S3)"):
                return False
            
            print(f"[OK] Successfully navigated to S3 configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to S3 config: {e}")
            return False
    
    def apply_s3_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply S3 configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying S3 configuration...")
            
            # Map elements first
            elements = self.map_all_elements()
            
            # Apply settings using robust selectors
            settings_applied = 0
            
            # Storage amount
            if 'storage_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Storage amount']", str(config['storage_gb']))
                    print(f"[OK] Set storage amount to {config['storage_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set storage amount: {e}")
            
            # Storage class
            if 'storage_class' in config:
                try:
                    self.page.select_option("select[aria-label*='Storage class']", label=config['storage_class'])
                    print(f"[OK] Set storage class to {config['storage_class']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set storage class: {e}")
            
            # PUT requests
            if 'put_requests' in config:
                try:
                    self.page.fill("input[aria-label*='PUT']", str(config['put_requests']))
                    print(f"[OK] Set PUT requests to {config['put_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set PUT requests: {e}")
            
            # GET requests
            if 'get_requests' in config:
                try:
                    self.page.fill("input[aria-label*='GET']", str(config['get_requests']))
                    print(f"[OK] Set GET requests to {config['get_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GET requests: {e}")
            
            # Data transfer
            if 'data_transfer_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Data transfer']", str(config['data_transfer_gb']))
                    print(f"[OK] Set data transfer to {config['data_transfer_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set data transfer: {e}")
            
            print(f"[OK] Applied {settings_applied} S3 settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply S3 configuration: {e}")
            return False


def main():
    """Test the S3Configurator class"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Create configurator
        configurator = S3Configurator(page)
        
        # Navigate to S3 config
        if configurator.navigate_to_s3_config():
            # Map all elements
            configurator.print_element_summary()
            
            # Save element map
            configurator.save_element_map()
            
            # Example configuration
            example_config = {
                'storage_gb': 500,
                'storage_class': 'S3 Standard',
                'put_requests': 100000,
                'get_requests': 200000,
                'data_transfer_gb': 100
            }
            
            # Apply configuration
            if configurator.apply_s3_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] S3 configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("s3_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to s3_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
