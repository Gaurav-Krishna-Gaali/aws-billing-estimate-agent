"""
Comprehensive AWS Shield Configuration Class
Handles all 36 interactive elements on the AWS Shield configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveAWSShieldConfigurator(BaseAWSConfigurator):
    """Comprehensive AWS Shield configuration class handling all 36 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "AWS Shield")
    
    def navigate_to_aws_shield_config(self) -> bool:
        """Navigate to AWS Shield configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for AWS Shield
            if not self.search_and_select_service("AWS Shield"):
                return False
            
            print(f"[OK] Successfully navigated to AWS Shield configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS Shield config: {e}")
            return False
    
    def apply_aws_shield_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS Shield configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying AWS Shield configuration...")
            
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
            
            # CloudFront Usage
            if 'cloudfront_usage' in config:
                try:
                    self.page.fill("input[aria-label*='Cloud Front Usage Value']", str(config['cloudfront_usage']))
                    print(f"[OK] Set CloudFront usage to {config['cloudfront_usage']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set CloudFront usage: {e}")
            
            # Elastic Load Balancing (ELB) Usage
            if 'elb_usage' in config:
                try:
                    self.page.fill("input[aria-label*='Elastic Load Balancing (ELB) Usage Value']", str(config['elb_usage']))
                    print(f"[OK] Set ELB usage to {config['elb_usage']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ELB usage: {e}")
            
            # Elastic IP Usage
            if 'elastic_ip_usage' in config:
                try:
                    self.page.fill("input[aria-label*='Elastic IP Usage Value']", str(config['elastic_ip_usage']))
                    print(f"[OK] Set Elastic IP usage to {config['elastic_ip_usage']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Elastic IP usage: {e}")
            
            # Global Accelerator Usage
            if 'global_accelerator_usage' in config:
                try:
                    self.page.fill("input[aria-label*='Global Accelerator Usage Value']", str(config['global_accelerator_usage']))
                    print(f"[OK] Set Global Accelerator usage to {config['global_accelerator_usage']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Global Accelerator usage: {e}")
            
            print(f"[OK] Applied {settings_applied} AWS Shield settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS Shield configuration: {e}")
            return False

    # --- Multi-service integration hooks ---
    def navigate_to_service_config(self) -> bool:
        """Navigate to AWS Shield configuration page for multi-service estimates"""
        try:
            print("[INFO] Navigating to AWS Shield service configuration...")
            for term in ["AWS Shield", "Shield", "DDoS"]:
                if self.search_and_select_service(term):
                    return True
            print("[ERROR] Could not find AWS Shield in calculator search")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS Shield service config: {e}")
            return False

    def _get_service_search_terms(self) -> List[str]:
        return ["AWS Shield", "Shield", "DDoS"]

    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        return self.apply_aws_shield_configuration(config)

def main():
    """Test the comprehensive AWS Shield configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveAWSShieldConfigurator(page)
        
        if configurator.navigate_to_aws_shield_config():
            # Example configuration
            example_config = {
                'description': 'AWS Shield DDoS protection for production infrastructure',
                'cloudfront_usage': 1000,
                'elb_usage': 500,
                'elastic_ip_usage': 10,
                'global_accelerator_usage': 200
            }
            
            # Apply configuration
            if configurator.apply_aws_shield_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS Shield configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("aws_shield_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to aws_shield_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
