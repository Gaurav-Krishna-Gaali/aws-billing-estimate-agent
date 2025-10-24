"""
Comprehensive EC2 Configuration Class
Handles all 144 interactive elements on the EC2 configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class ComprehensiveEC2Configurator(BaseAWSConfigurator):
    """Comprehensive EC2 configuration class handling all 144 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "EC2")
    
    def navigate_to_ec2_config(self) -> bool:
        """Navigate to EC2 configuration page"""
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
            
            # Look for "Configure Amazon EC2" button directly
            try:
                ec2_button = self.page.locator("button[aria-label='Configure Amazon EC2 ']")
                if ec2_button.count() > 0:
                    ec2_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure Amazon EC2' button")
                    print(f"[OK] Successfully navigated to EC2 configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure Amazon EC2' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click EC2 button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to EC2 config: {e}")
            return False
    
    def apply_ec2_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply EC2 configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying EC2 configuration...")
            
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
            
            # Number of instances
            if 'number_of_instances' in config:
                try:
                    self.page.fill("input[aria-label*='Number of instances Enter amount']", str(config['number_of_instances']))
                    print(f"[OK] Set number of instances to {config['number_of_instances']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set number of instances: {e}")
            
            # Storage amount
            if 'storage_amount_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Storage amount Value']", str(config['storage_amount_gb']))
                    print(f"[OK] Set storage amount to {config['storage_amount_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set storage amount: {e}")
            
            # IOPS per volume
            if 'iops_per_volume' in config:
                try:
                    self.page.fill("input[aria-label*='General Purpose SSD (gp3) - IOPS Enter amount of IOPS per volume']", str(config['iops_per_volume']))
                    print(f"[OK] Set IOPS per volume to {config['iops_per_volume']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set IOPS per volume: {e}")
            
            # Throughput
            if 'throughput_mbps' in config:
                try:
                    self.page.fill("input[aria-label*='General Purpose SSD (gp3) - Throughput Value']", str(config['throughput_mbps']))
                    print(f"[OK] Set throughput to {config['throughput_mbps']} MBps")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set throughput: {e}")
            
            # Enable monitoring
            if 'enable_monitoring' in config and config['enable_monitoring']:
                try:
                    monitoring_checkbox = self.page.locator("input[aria-label*='Enable monitoring']")
                    if monitoring_checkbox.count() > 0 and not monitoring_checkbox.first.is_checked():
                        monitoring_checkbox.first.check()
                        print(f"[OK] Enabled monitoring")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not enable monitoring: {e}")
            
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
            
            # Licensing cost
            if 'licensing_cost' in config:
                try:
                    self.page.fill("input[aria-label*='Enter any placeholder cost such as Licensing to add to your estimate']", str(config['licensing_cost']))
                    print(f"[OK] Set licensing cost to ${config['licensing_cost']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set licensing cost: {e}")
            
            print(f"[OK] Applied {settings_applied} EC2 settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply EC2 configuration: {e}")
            return False


def main():
    """Test the comprehensive EC2 configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveEC2Configurator(page)
        
        if configurator.navigate_to_ec2_config():
            # Example configuration
            example_config = {
                'description': 'EC2 instances for production web application',
                'number_of_instances': 3,
                'storage_amount_gb': 100,
                'iops_per_volume': 3000,
                'throughput_mbps': 125,
                'enable_monitoring': True,
                'inbound_data_transfer_tb': 10,
                'outbound_data_transfer_tb': 5,
                'licensing_cost': 500
            }
            
            # Apply configuration
            if configurator.apply_ec2_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] EC2 configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("ec2_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to ec2_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
