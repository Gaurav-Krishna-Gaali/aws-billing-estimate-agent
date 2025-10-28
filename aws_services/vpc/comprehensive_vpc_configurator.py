"""
Comprehensive VPC Configuration Class
Handles all interactive elements on the VPC configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveVPCConfigurator(BaseAWSConfigurator):
    """Comprehensive VPC configuration class handling all elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "VPC")
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding VPC service in AWS Calculator"""
        return ["Amazon VPC", "VPC", "Virtual Private Cloud"]
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to VPC configuration page from current estimate"""
        try:
            print(f"[INFO] Navigating to {self.service_name} configuration...")
            
            # Search for the service using search terms
            search_terms = self._get_service_search_terms()
            for term in search_terms:
                try:
                    # Look for search input
                    search_input = self.page.locator("input[placeholder='Search for a service']")
                    if search_input.count() > 0:
                        search_input.first.fill(term)
                        self.page.wait_for_timeout(2000)
                        
                        # Look for "Configure Amazon VPC" button
                        vpc_button = self.page.locator("button[aria-label*='VPC']").first
                        if vpc_button.count() > 0:
                            vpc_button.click()
                            self.page.wait_for_timeout(3000)
                            print(f"[OK] Successfully navigated to {self.service_name} configuration page")
                            return True
                        else:
                            print(f"[WARNING] VPC button not found, trying alternative search...")
                            continue
                    else:
                        print(f"[WARNING] Search input not found, trying next search term...")
                        continue
                except Exception as e:
                    print(f"[WARNING] Failed to search for {term}: {e}")
                    continue
            
            print(f"[ERROR] Could not find {self.service_name} service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to {self.service_name} configuration: {e}")
            return False
    
    def navigate_to_vpc_config(self) -> bool:
        """Navigate to VPC configuration page (standalone mode - creates new estimate)"""
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
            
            # Look for "Configure Amazon VPC" button directly
            try:
                vpc_button = self.page.locator("button[aria-label*='VPC']")
                if vpc_button.count() > 0:
                    vpc_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure Amazon VPC' button")
                    print(f"[OK] Successfully navigated to VPC configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure Amazon VPC' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click VPC button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to VPC config: {e}")
            return False
    
    def apply_vpc_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply VPC configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying VPC configuration...")
            
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
            
            # VPC configuration settings
            vpc_settings = [
                'number_of_vpcs',
                'number_of_subnets',
                'number_of_internet_gateways',
                'number_of_nat_gateways',
                'number_of_vpc_endpoints',
                'number_of_route_tables',
                'number_of_security_groups',
                'number_of_network_acls',
                'data_processed_gb',
                'endpoint_hours',
                'nat_gateway_hours',
                'vpc_peering_hours',
                'transit_gateway_hours',
                'vpn_connection_hours',
                'vpn_tunnel_hours',
                'data_transfer_gb'
            ]
            
            for setting in vpc_settings:
                if setting in config:
                    try:
                        # Try different selector patterns for VPC settings
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
                'enable_dns_hostnames',
                'enable_dns_resolution',
                'enable_classic_link',
                'enable_vpc_flow_logs',
                'enable_vpc_endpoints',
                'enable_nat_gateway',
                'enable_internet_gateway',
                'enable_vpn_connection'
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
            
            # Region selection
            if 'region' in config:
                try:
                    region_select = self.page.locator("select[aria-label*='Region']")
                    if region_select.count() > 0:
                        region_select.first.select_option(value=config['region'])
                        print(f"[OK] Selected region: {config['region']}")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not select region: {e}")
            
            # Availability zones
            if 'availability_zones' in config:
                try:
                    az_input = self.page.locator("input[aria-label*='Availability Zone']")
                    if az_input.count() > 0:
                        az_input.first.fill(str(config['availability_zones']))
                        print(f"[OK] Set availability zones to {config['availability_zones']}")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set availability zones: {e}")
            
            # CIDR block configuration
            if 'cidr_block' in config:
                try:
                    cidr_input = self.page.locator("input[aria-label*='CIDR']")
                    if cidr_input.count() > 0:
                        cidr_input.first.fill(config['cidr_block'])
                        print(f"[OK] Set CIDR block to {config['cidr_block']}")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set CIDR block: {e}")
            
            print(f"[OK] Applied {settings_applied} VPC settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply VPC configuration: {e}")
            return False

def main():
    """Test the comprehensive VPC configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Example configuration
            example_config = {
                'description': 'VPC for production web application',
                'number_of_vpcs': 1,
                'number_of_subnets': 4,
                'number_of_internet_gateways': 1,
                'number_of_nat_gateways': 2,
                'number_of_vpc_endpoints': 3,
                'number_of_route_tables': 4,
                'number_of_security_groups': 6,
                'number_of_network_acls': 2,
                'data_processed_gb': 1000,
                'endpoint_hours': 744,
                'nat_gateway_hours': 1488,
                'vpc_peering_hours': 744,
                'transit_gateway_hours': 744,
                'vpn_connection_hours': 744,
                'vpn_tunnel_hours': 1488,
                'data_transfer_gb': 500,
                'enable_dns_hostnames': True,
                'enable_dns_resolution': True,
                'enable_vpc_flow_logs': True,
                'enable_vpc_endpoints': True,
                'enable_nat_gateway': True,
                'enable_internet_gateway': True,
                'region': 'us-east-1',
                'availability_zones': 3,
                'cidr_block': '10.0.0.0/16'
            }
            
            # Apply configuration
            if configurator.apply_vpc_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] VPC configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("vpc_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to vpc_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
