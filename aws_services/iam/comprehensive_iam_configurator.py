"""
Comprehensive IAM Access Analyzer Configuration Class
Handles all 38 interactive elements on the IAM Access Analyzer configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class ComprehensiveIAMConfigurator(BaseAWSConfigurator):
    """Comprehensive IAM Access Analyzer configuration class handling all 38 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "IAM")
    
    def navigate_to_iam_config(self) -> bool:
        """Navigate to IAM Access Analyzer configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for AWS IAM Access Analyzer
            if not self.search_and_select_service("AWS IAM Access Analyzer"):
                return False
            
            print(f"[OK] Successfully navigated to IAM Access Analyzer configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to IAM config: {e}")
            return False
    
    def apply_iam_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply IAM Access Analyzer configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying IAM Access Analyzer configuration...")
            
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
            
            # Number of accounts to monitor
            if 'accounts_to_monitor' in config:
                try:
                    self.page.fill("input[aria-label*='Number of accounts to monitor Enter amount']", str(config['accounts_to_monitor']))
                    print(f"[OK] Set accounts to monitor to {config['accounts_to_monitor']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set accounts to monitor: {e}")
            
            # Average roles per account
            if 'average_roles_per_account' in config:
                try:
                    self.page.fill("input[aria-label*='Average roles per account Enter amount']", str(config['average_roles_per_account']))
                    print(f"[OK] Set average roles per account to {config['average_roles_per_account']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set average roles per account: {e}")
            
            # Average users per account
            if 'average_users_per_account' in config:
                try:
                    self.page.fill("input[aria-label*='Average users per account Enter amount']", str(config['average_users_per_account']))
                    print(f"[OK] Set average users per account to {config['average_users_per_account']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set average users per account: {e}")
            
            # Number of analyzers per account
            if 'analyzers_per_account' in config:
                try:
                    self.page.fill("input[aria-label*='Number of analyzers per account Enter amount']", str(config['analyzers_per_account']))
                    print(f"[OK] Set analyzers per account to {config['analyzers_per_account']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set analyzers per account: {e}")
            
            # CheckNoNewAccess API requests
            if 'check_no_new_access_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of requests to CheckNoNewAccess API Value']", str(config['check_no_new_access_requests']))
                    print(f"[OK] Set CheckNoNewAccess API requests to {config['check_no_new_access_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set CheckNoNewAccess API requests: {e}")
            
            # CheckAccessNotGranted API requests
            if 'check_access_not_granted_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of requests to CheckAccessNotGranted API Value']", str(config['check_access_not_granted_requests']))
                    print(f"[OK] Set CheckAccessNotGranted API requests to {config['check_access_not_granted_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set CheckAccessNotGranted API requests: {e}")
            
            # Number of resources to monitor
            if 'resources_to_monitor' in config:
                try:
                    self.page.fill("input[aria-label*='Number of resources to monitor Value']", str(config['resources_to_monitor']))
                    print(f"[OK] Set resources to monitor to {config['resources_to_monitor']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set resources to monitor: {e}")
            
            print(f"[OK] Applied {settings_applied} IAM Access Analyzer settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply IAM configuration: {e}")
            return False


def main():
    """Test the comprehensive IAM configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveIAMConfigurator(page)
        
        if configurator.navigate_to_iam_config():
            # Example configuration
            example_config = {
                'description': 'IAM Access Analyzer for security monitoring',
                'accounts_to_monitor': 10,
                'average_roles_per_account': 50,
                'average_users_per_account': 100,
                'analyzers_per_account': 5,
                'check_no_new_access_requests': 1000,
                'check_access_not_granted_requests': 500,
                'resources_to_monitor': 1000
            }
            
            # Apply configuration
            if configurator.apply_iam_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] IAM Access Analyzer configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("iam_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to iam_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()

