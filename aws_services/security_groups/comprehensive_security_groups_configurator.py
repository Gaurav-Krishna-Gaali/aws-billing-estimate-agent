"""
Comprehensive Security Groups Configuration Class
Handles all interactive elements on the Security Groups configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveSecurityGroupsConfigurator(BaseAWSConfigurator):
    """Comprehensive Security Groups configuration class handling all elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "Security Groups")
    
    def navigate_to_security_groups_config(self) -> bool:
        """Navigate to Security Groups configuration page"""
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
            
            # Look for "Configure Amazon EC2" button (Security Groups are part of EC2)
            try:
                ec2_button = self.page.locator("button[aria-label*='EC2']")
                if ec2_button.count() > 0:
                    ec2_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure Amazon EC2' button")
                    print(f"[OK] Successfully navigated to EC2 configuration page (Security Groups are part of EC2)")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure Amazon EC2' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click EC2 button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to Security Groups config: {e}")
            return False
    
    def apply_security_groups_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply Security Groups configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying Security Groups configuration...")
            
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
            
            # EC2 configuration settings (Security Groups are part of EC2)
            ec2_settings = [
                'number_of_instances',
                'usage_hours',
                'storage_amount',
                'data_transfer_in',
                'data_transfer_out'
            ]
            
            for setting in ec2_settings:
                if setting in config:
                    try:
                        # Try different selector patterns for EC2 settings
                        selectors = [
                            f"input[aria-label*='{setting.replace('_', ' ').title()}']",
                            f"input[aria-label*='{setting}']",
                            f"input[placeholder*='{setting.replace('_', ' ')}']",
                            f"input[name*='{setting}']"
                        ]
                        
                        for selector in selectors:
                            try:
                                field = self.page.locator(selector)
                                if field.count() > 0:
                                    field.first.fill(str(config[setting]))
                                    print(f"[OK] Set {setting} to {config[setting]}")
                                    settings_applied += 1
                                    break
                            except:
                                continue
                    except Exception as e:
                        print(f"[WARNING] Could not set {setting}: {e}")
            
            # Enable/disable features
            boolean_settings = [
                'enable_monitoring'
            ]
            
            for setting in boolean_settings:
                if setting in config:
                    try:
                        checkbox = self.page.locator(f"input[aria-label*='{setting.replace('_', ' ').title()}']")
                        if checkbox.count() > 0:
                            if config[setting] and not checkbox.first.is_checked():
                                checkbox.first.check()
                                print(f"[OK] Enabled {setting}")
                                settings_applied += 1
                            elif not config[setting] and checkbox.first.is_checked():
                                checkbox.first.uncheck()
                                print(f"[OK] Disabled {setting}")
                                settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not configure {setting}: {e}")
            
            # Pricing strategy selection
            if 'pricing_strategy' in config:
                try:
                    # Try to select pricing strategy radio button
                    strategy_radio = self.page.locator(f"input[aria-label*='{config['pricing_strategy'].title()}']")
                    if strategy_radio.count() > 0:
                        strategy_radio.first.click()
                        print(f"[OK] Selected pricing strategy: {config['pricing_strategy']}")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not select pricing strategy: {e}")
            
            print(f"[OK] Applied {settings_applied} Security Groups settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply Security Groups configuration: {e}")
            return False

def main():
    """Test the comprehensive Security Groups configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveSecurityGroupsConfigurator(page)
        
        if configurator.navigate_to_security_groups_config():
            # Example configuration
            example_config = {
                'description': 'Security Groups for production web application',
                'number_of_security_groups': 4,
                'number_of_inbound_rules': 8,
                'number_of_outbound_rules': 4,
                'number_of_custom_rules': 2,
                'number_of_http_rules': 2,
                'number_of_https_rules': 2,
                'number_of_ssh_rules': 1,
                'number_of_rdp_rules': 1,
                'number_of_custom_tcp_rules': 1,
                'number_of_custom_udp_rules': 1,
                'number_of_icmp_rules': 1,
                'data_processed_gb': 500,
                'rules_per_security_group': 3,
                'custom_ports_count': 5,
                'port_ranges_count': 2,
                'enable_http_access': True,
                'enable_https_access': True,
                'enable_ssh_access': True,
                'enable_rdp_access': False,
                'enable_custom_tcp': True,
                'enable_custom_udp': False,
                'enable_icmp': True,
                'enable_all_traffic': False,
                'enable_restricted_access': True,
                'enable_web_server_access': True,
                'enable_database_access': True,
                'enable_load_balancer_access': True,
                'default_protocol': 'TCP',
                'default_port': 80,
                'source_ip_range': '0.0.0.0/0',
                'region': 'us-east-1'
            }
            
            # Apply configuration
            if configurator.apply_security_groups_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] Security Groups configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("security_groups_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to security_groups_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
