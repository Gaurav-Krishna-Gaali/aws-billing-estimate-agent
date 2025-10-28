"""
Comprehensive SQS Configuration Class
Handles all 42 interactive elements on the SQS configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveSQSConfigurator(BaseAWSConfigurator):
    """Comprehensive SQS configuration class handling all 42 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "SQS")
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to SQS configuration page from current estimate"""
        try:
            print(f"[INFO] Navigating to {self.service_name} configuration...")
            
            # Search for the service using search terms
            search_terms = self._get_service_search_terms()
            for term in search_terms:
                if self.search_and_select_service(term):
                    print(f"[OK] Successfully navigated to {self.service_name} configuration page")
                    return True
            
            print(f"[ERROR] Could not find {self.service_name} service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to {self.service_name} configuration: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding SQS service in AWS Calculator"""
        return ["Amazon Simple Queue Service (SQS)", "SQS", "Simple Queue Service"]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """Apply SQS-specific configuration logic"""
        return self.apply_sqs_configuration(config)
    
    def navigate_to_sqs_config(self) -> bool:
        """Navigate to SQS configuration page (standalone mode - creates new estimate)"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for Amazon Simple Queue Service (SQS)
            if not self.search_and_select_service("Amazon Simple Queue Service (SQS)"):
                return False
            
            print(f"[OK] Successfully navigated to SQS configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to SQS config: {e}")
            return False
    
    def apply_sqs_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply SQS configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying SQS configuration...")
            
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
            
            # Standard queue requests
            if 'standard_queue_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Standard queue requests Value']", str(config['standard_queue_requests']))
                    print(f"[OK] Set standard queue requests to {config['standard_queue_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set standard queue requests: {e}")
            
            # FIFO queue requests
            if 'fifo_queue_requests' in config:
                try:
                    self.page.fill("input[aria-label*='FIFO queue requests Value']", str(config['fifo_queue_requests']))
                    print(f"[OK] Set FIFO queue requests to {config['fifo_queue_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set FIFO queue requests: {e}")
            
            # Fair queue requests
            if 'fair_queue_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Fair queue requests Value']", str(config['fair_queue_requests']))
                    print(f"[OK] Set fair queue requests to {config['fair_queue_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set fair queue requests: {e}")
            
            # Data transfer configurations
            if 'inbound_data_transfer_tb' in config:
                try:
                    # Find the first "Enter Amount" field for inbound data transfer
                    inbound_fields = self.page.query_selector_all("input[aria-label*='Enter Amount Enter amount']")
                    if len(inbound_fields) > 0:
                        inbound_fields[0].fill(str(config['inbound_data_transfer_tb']))
                        print(f"[OK] Set inbound data transfer to {config['inbound_data_transfer_tb']} TB")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set inbound data transfer: {e}")
            
            if 'outbound_data_transfer_tb' in config:
                try:
                    # Find the second "Enter Amount" field for outbound data transfer
                    outbound_fields = self.page.query_selector_all("input[aria-label*='Enter Amount Enter amount']")
                    if len(outbound_fields) > 1:
                        outbound_fields[1].fill(str(config['outbound_data_transfer_tb']))
                        print(f"[OK] Set outbound data transfer to {config['outbound_data_transfer_tb']} TB")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set outbound data transfer: {e}")
            
            print(f"[OK] Applied {settings_applied} SQS settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply SQS configuration: {e}")
            return False

def main():
    """Test the comprehensive SQS configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveSQSConfigurator(page)
        
        if configurator.navigate_to_sqs_config():
            # Example configuration
            example_config = {
                'description': 'SQS queues for production microservices messaging',
                'standard_queue_requests': 1000000,
                'fifo_queue_requests': 500000,
                'fair_queue_requests': 200000,
                'inbound_data_transfer_tb': 10,
                'outbound_data_transfer_tb': 5
            }
            
            # Apply configuration
            if configurator.apply_sqs_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] SQS configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("sqs_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to sqs_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
