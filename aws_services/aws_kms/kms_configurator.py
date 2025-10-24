"""
Comprehensive AWS KMS Configuration Class
Handles all 34 interactive elements on the AWS Key Management Service configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveAWSKMSConfigurator(BaseAWSConfigurator):
    """Comprehensive AWS KMS configuration class handling all 34 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "AWS KMS")
    
    def navigate_to_aws_kms_config(self) -> bool:
        """Navigate to AWS KMS configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Click "Add service" button
            try:
                self.page.click("text='Add service'")
                self.page.wait_for_timeout(2000)
                print("[OK] Clicked 'Add service' button")
            except Exception as e:
                print(f"[WARNING] Could not click 'Add service' button: {e}")
            
            # Look for "Configure AWS Key Management Service" button directly
            try:
                kms_button = self.page.locator("button[aria-label='Configure AWS Key Management Service']")
                if kms_button.count() > 0:
                    kms_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure AWS Key Management Service' button")
                    print(f"[OK] Successfully navigated to AWS Key Management Service configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure AWS Key Management Service' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click KMS button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS KMS config: {e}")
            return False
    
    def apply_aws_kms_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS KMS configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying AWS KMS configuration...")
            
            # Map elements first
            elements = self.map_all_elements()
            
            # Apply settings using robust selectors
            settings_applied = 0
            
            # Set description
            if 'description' in config:
                try:
                    self.page.fill("input[aria-label*='Description']", config['description'])
                    print(f"[OK] Set description: {config['description']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set description: {e}")
            
            # Number of customer managed Customer Master Keys (CMK)
            if 'customer_managed_cmks' in config:
                try:
                    self.page.fill("input[aria-label*='Number of customer managed Customer Master Keys (CMK)']", str(config['customer_managed_cmks']))
                    print(f"[OK] Set customer managed CMKs to {config['customer_managed_cmks']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set customer managed CMKs: {e}")
            
            # Number of symmetric requests
            if 'symmetric_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of symmetric requests']", str(config['symmetric_requests']))
                    print(f"[OK] Set symmetric requests to {config['symmetric_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set symmetric requests: {e}")
            
            # Number of asymmetric requests except RSA 2048
            if 'asymmetric_requests_non_rsa' in config:
                try:
                    self.page.fill("input[aria-label*='Number of asymmetric requests except RSA 2048 Enter amount']", str(config['asymmetric_requests_non_rsa']))
                    print(f"[OK] Set asymmetric requests (non-RSA) to {config['asymmetric_requests_non_rsa']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set asymmetric requests (non-RSA): {e}")
            
            # Number of asymmetric requests involving RSA 2048
            if 'asymmetric_requests_rsa_2048' in config:
                try:
                    self.page.fill("input[aria-label*='Number of asymmetric requests involving RSA 2048 Enter amount']", str(config['asymmetric_requests_rsa_2048']))
                    print(f"[OK] Set asymmetric requests (RSA 2048) to {config['asymmetric_requests_rsa_2048']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set asymmetric requests (RSA 2048): {e}")
            
            # Number of ECC GenerateDataKeyPair requests
            if 'ecc_generate_data_key_pair_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of ECC GenerateDataKeyPair requests Enter amount']", str(config['ecc_generate_data_key_pair_requests']))
                    print(f"[OK] Set ECC GenerateDataKeyPair requests to {config['ecc_generate_data_key_pair_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ECC GenerateDataKeyPair requests: {e}")
            
            # Number of RSA GenerateDataKeyPair requests
            if 'rsa_generate_data_key_pair_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of RSA GenerateDataKeyPair requests Enter amount']", str(config['rsa_generate_data_key_pair_requests']))
                    print(f"[OK] Set RSA GenerateDataKeyPair requests to {config['rsa_generate_data_key_pair_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set RSA GenerateDataKeyPair requests: {e}")
            
            print(f"[OK] Applied {settings_applied} AWS KMS settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS KMS configuration: {e}")
            return False

def main():
    """Test the comprehensive AWS KMS configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveAWSKMSConfigurator(page)
        
        if configurator.navigate_to_aws_kms_config():
            # Example configuration
            example_config = {
                'description': 'AWS KMS for enterprise encryption key management',
                'customer_managed_cmks': 5,
                'symmetric_requests': 100000,
                'asymmetric_requests_non_rsa': 10000,
                'asymmetric_requests_rsa_2048': 5000,
                'ecc_generate_data_key_pair_requests': 2000,
                'rsa_generate_data_key_pair_requests': 1000
            }
            
            # Apply configuration
            if configurator.apply_aws_kms_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS KMS configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("aws_kms_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to aws_kms_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
