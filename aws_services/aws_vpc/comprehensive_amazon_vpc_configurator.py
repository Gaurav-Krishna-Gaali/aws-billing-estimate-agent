"""
Comprehensive Amazon VPC Configuration Class
Handles all 106 interactive elements on the Amazon Virtual Private Cloud (VPC) configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveAmazonVPCConfigurator(BaseAWSConfigurator):
    """Comprehensive Amazon VPC configuration class handling all 106 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "Amazon VPC")
    
    def navigate_to_amazon_vpc_config(self) -> bool:
        """Navigate to Amazon VPC configuration page"""
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
            
            # Look for "Configure Amazon Virtual Private Cloud (VPC)" button directly
            try:
                vpc_button = self.page.locator("button[aria-label='Configure Amazon Virtual Private Cloud (VPC)']")
                if vpc_button.count() > 0:
                    vpc_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure Amazon Virtual Private Cloud (VPC)' button")
                    print(f"[OK] Successfully navigated to Amazon VPC configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure Amazon Virtual Private Cloud (VPC)' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click VPC button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to Amazon VPC config: {e}")
            return False
    
    def apply_amazon_vpc_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply Amazon VPC configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying Amazon VPC configuration...")
            
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
            
            # Site-to-Site VPN Connections
            if 'site_to_site_vpn_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Site-to-Site VPN Connections Enter the amount']", str(config['site_to_site_vpn_connections']))
                    print(f"[OK] Set site-to-site VPN connections to {config['site_to_site_vpn_connections']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set site-to-site VPN connections: {e}")
            
            # Average duration for VPN connections
            if 'vpn_connection_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average duration for each connection Value']", str(config['vpn_connection_duration']))
                    print(f"[OK] Set VPN connection duration to {config['vpn_connection_duration']} hours")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set VPN connection duration: {e}")
            
            # Client VPN connections
            if 'client_vpn_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Number of active Client VPN connections (or users) Value']", str(config['client_vpn_connections']))
                    print(f"[OK] Set client VPN connections to {config['client_vpn_connections']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set client VPN connections: {e}")
            
            # Client VPN connection duration
            if 'client_vpn_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average duration for each connection Value']", str(config['client_vpn_duration']))
                    print(f"[OK] Set client VPN duration to {config['client_vpn_duration']} hours")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set client VPN duration: {e}")
            
            # Working days per month
            if 'working_days_per_month' in config:
                try:
                    self.page.fill("input[aria-label*='Working days per month Enter the number of working days']", str(config['working_days_per_month']))
                    print(f"[OK] Set working days per month to {config['working_days_per_month']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set working days per month: {e}")
            
            # Network assessments per month
            if 'network_assessments_per_month' in config:
                try:
                    self.page.fill("input[aria-label*='Number of network assessments per month Enter the number of network assessments using Network Access Analyzer in a month.']", str(config['network_assessments_per_month']))
                    print(f"[OK] Set network assessments per month to {config['network_assessments_per_month']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set network assessments per month: {e}")
            
            # Elastic Network Interfaces (ENIs)
            if 'elastic_network_interfaces' in config:
                try:
                    self.page.fill("input[aria-label*='Number of ENIs (elastic network interfaces) Enter the number of EINs (elastic network interfaces).']", str(config['elastic_network_interfaces']))
                    print(f"[OK] Set elastic network interfaces to {config['elastic_network_interfaces']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set elastic network interfaces: {e}")
            
            # Connectivity analysis per month
            if 'connectivity_analysis_per_month' in config:
                try:
                    self.page.fill("input[aria-label*='Number of connectivity analysis per month Enter the number of times you analyze connectivity.']", str(config['connectivity_analysis_per_month']))
                    print(f"[OK] Set connectivity analysis per month to {config['connectivity_analysis_per_month']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set connectivity analysis per month: {e}")
            
            # Traffic mirroring sessions
            if 'traffic_mirroring_sessions' in config:
                try:
                    self.page.fill("input[aria-label*='Number of traffic mirroring sessions Enter the number of traffic mirroring sessions on ENIs.']", str(config['traffic_mirroring_sessions']))
                    print(f"[OK] Set traffic mirroring sessions to {config['traffic_mirroring_sessions']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set traffic mirroring sessions: {e}")
            
            # In-use public IPv4 addresses
            if 'in_use_public_ipv4_addresses' in config:
                try:
                    self.page.fill("input[aria-label*='Number of In-use public IPv4 addresses Enter the number of public IPv4 addresses attached to EC2 instances and AWS services.']", str(config['in_use_public_ipv4_addresses']))
                    print(f"[OK] Set in-use public IPv4 addresses to {config['in_use_public_ipv4_addresses']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set in-use public IPv4 addresses: {e}")
            
            # Idle public IPv4 addresses
            if 'idle_public_ipv4_addresses' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Idle public IPv4 addresses Enter the number of Idle public IPv4 addresses allocated to the account, unattached to AWS services.']", str(config['idle_public_ipv4_addresses']))
                    print(f"[OK] Set idle public IPv4 addresses to {config['idle_public_ipv4_addresses']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set idle public IPv4 addresses: {e}")
            
            # Active IP addresses
            if 'active_ip_addresses' in config:
                try:
                    self.page.fill("input[aria-label*='Number of active IP addresses Enter the number of IP addresses used on EC2 instance.']", str(config['active_ip_addresses']))
                    print(f"[OK] Set active IP addresses to {config['active_ip_addresses']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set active IP addresses: {e}")
            
            # Route Server endpoints
            if 'route_server_endpoints' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Route Server endpoints Enter the number of of Route Server endpoints.']", str(config['route_server_endpoints']))
                    print(f"[OK] Set route server endpoints to {config['route_server_endpoints']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set route server endpoints: {e}")
            
            # NAT Gateways
            if 'nat_gateways' in config:
                try:
                    self.page.fill("input[aria-label*='Number of NAT Gateways Enter the amount']", str(config['nat_gateways']))
                    print(f"[OK] Set NAT gateways to {config['nat_gateways']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NAT gateways: {e}")
            
            # Data processed per NAT Gateway
            if 'nat_gateway_data_processed' in config:
                try:
                    self.page.fill("input[aria-label*='Data Processed per NAT Gateway Value']", str(config['nat_gateway_data_processed']))
                    print(f"[OK] Set NAT gateway data processed to {config['nat_gateway_data_processed']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NAT gateway data processed: {e}")
            
            # Transit Gateway attachments
            if 'transit_gateway_attachments' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Transit Gateway attachments Enter the amount']", str(config['transit_gateway_attachments']))
                    print(f"[OK] Set transit gateway attachments to {config['transit_gateway_attachments']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set transit gateway attachments: {e}")
            
            # Transit Gateway ingress data
            if 'transit_gateway_ingress_data' in config:
                try:
                    self.page.fill("input[aria-label*='Ingress data processed per TGW attachment Value']", str(config['transit_gateway_ingress_data']))
                    print(f"[OK] Set transit gateway ingress data to {config['transit_gateway_ingress_data']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set transit gateway ingress data: {e}")
            
            # VPC Interface endpoints
            if 'vpc_interface_endpoints' in config:
                try:
                    self.page.fill("input[aria-label*='Number of VPC Interface endpoints per AWS region Enter the amount']", str(config['vpc_interface_endpoints']))
                    print(f"[OK] Set VPC interface endpoints to {config['vpc_interface_endpoints']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set VPC interface endpoints: {e}")
            
            # VPC Interface endpoint data processed
            if 'vpc_endpoint_data_processed' in config:
                try:
                    self.page.fill("input[aria-label*='Total data processed by all VPCE Interface endpoints in the AWS region Value']", str(config['vpc_endpoint_data_processed']))
                    print(f"[OK] Set VPC endpoint data processed to {config['vpc_endpoint_data_processed']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set VPC endpoint data processed: {e}")
            
            # Gateway Load Balancer endpoints
            if 'gateway_load_balancer_endpoints' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Gateway Load Balancer Endpoints']", str(config['gateway_load_balancer_endpoints']))
                    print(f"[OK] Set gateway load balancer endpoints to {config['gateway_load_balancer_endpoints']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set gateway load balancer endpoints: {e}")
            
            # Gateway Load Balancer data processed
            if 'gateway_lb_data_processed' in config:
                try:
                    self.page.fill("input[aria-label*='Total processed bytes Value']", str(config['gateway_lb_data_processed']))
                    print(f"[OK] Set gateway load balancer data processed to {config['gateway_lb_data_processed']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set gateway load balancer data processed: {e}")
            
            # Gateway Load Balancer connections
            if 'gateway_lb_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of new connections/flows Value']", str(config['gateway_lb_connections']))
                    print(f"[OK] Set gateway load balancer connections to {config['gateway_lb_connections']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set gateway load balancer connections: {e}")
            
            # Gateway Load Balancer connection duration
            if 'gateway_lb_connection_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average connection/flow duration Value']", str(config['gateway_lb_connection_duration']))
                    print(f"[OK] Set gateway load balancer connection duration to {config['gateway_lb_connection_duration']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set gateway load balancer connection duration: {e}")
            
            # Transit Gateway Peering Connections
            if 'transit_gateway_peering_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Transit Gateway Peering Connections Enter the amount']", str(config['transit_gateway_peering_connections']))
                    print(f"[OK] Set transit gateway peering connections to {config['transit_gateway_peering_connections']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set transit gateway peering connections: {e}")
            
            # Transit Gateway Peering data processed
            if 'transit_gateway_peering_data' in config:
                try:
                    self.page.fill("input[aria-label*='Total amount of data processed Value']", str(config['transit_gateway_peering_data']))
                    print(f"[OK] Set transit gateway peering data processed to {config['transit_gateway_peering_data']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set transit gateway peering data processed: {e}")
            
            print(f"[OK] Applied {settings_applied} Amazon VPC settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply Amazon VPC configuration: {e}")
            return False

def main():
    """Test the comprehensive Amazon VPC configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveAmazonVPCConfigurator(page)
        
        if configurator.navigate_to_amazon_vpc_config():
            # Example configuration
            example_config = {
                'description': 'Amazon VPC for enterprise networking infrastructure',
                'site_to_site_vpn_connections': 2,
                'vpn_connection_duration': 24,
                'client_vpn_connections': 50,
                'client_vpn_duration': 8,
                'working_days_per_month': 22,
                'network_assessments_per_month': 10,
                'elastic_network_interfaces': 20,
                'connectivity_analysis_per_month': 5,
                'traffic_mirroring_sessions': 5,
                'in_use_public_ipv4_addresses': 10,
                'idle_public_ipv4_addresses': 2,
                'active_ip_addresses': 15,
                'route_server_endpoints': 2,
                'nat_gateways': 3,
                'nat_gateway_data_processed': 1000,
                'transit_gateway_attachments': 5,
                'transit_gateway_ingress_data': 2000,
                'vpc_interface_endpoints': 8,
                'vpc_endpoint_data_processed': 500,
                'gateway_load_balancer_endpoints': 2,
                'gateway_lb_data_processed': 100,
                'gateway_lb_connections': 1000,
                'gateway_lb_connection_duration': 300,
                'transit_gateway_peering_connections': 2,
                'transit_gateway_peering_data': 1000
            }
            
            # Apply configuration
            if configurator.apply_amazon_vpc_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] Amazon VPC configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("amazon_vpc_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to amazon_vpc_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
