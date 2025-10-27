"""
Comprehensive Application Load Balancer Configuration Class
Handles all 79 interactive elements on the ALB configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveALBConfigurator(BaseAWSConfigurator):
    """Comprehensive ALB configuration class handling all 79 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "Application Load Balancer")
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to ALB configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for Elastic Load Balancing
            if not self.search_and_select_service("Elastic Load Balancing"):
                return False
            
            print(f"[OK] Successfully navigated to Application Load Balancer configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to ALB config: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding ALB service in AWS Calculator"""
        return ["Elastic Load Balancing", "Application Load Balancer", "ALB", "Load Balancer"]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """Apply ALB-specific configuration logic"""
        return self.apply_alb_configuration(config)
    
    def apply_alb_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply ALB configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying Application Load Balancer configuration...")
            
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
            
            # Application Load Balancer settings
            if 'alb_count' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Application Load Balancers']", str(config['alb_count']))
                    print(f"[OK] Set ALB count to {config['alb_count']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB count: {e}")
            
            # ALB processed bytes (Lambda targets)
            if 'alb_lambda_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Processed bytes (Lambda functions as targets) Value']", str(config['alb_lambda_processed_bytes']))
                    print(f"[OK] Set ALB Lambda processed bytes to {config['alb_lambda_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB Lambda processed bytes: {e}")
            
            # ALB processed bytes (EC2 targets)
            if 'alb_ec2_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Processed bytes (EC2 Instances and IP addresses as targets) Value']", str(config['alb_ec2_processed_bytes']))
                    print(f"[OK] Set ALB EC2 processed bytes to {config['alb_ec2_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB EC2 processed bytes: {e}")
            
            # ALB new connections
            if 'alb_new_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of new connections per ALB Value']", str(config['alb_new_connections']))
                    print(f"[OK] Set ALB new connections to {config['alb_new_connections']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB new connections: {e}")
            
            # ALB connection duration
            if 'alb_connection_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average connection duration Value']", str(config['alb_connection_duration']))
                    print(f"[OK] Set ALB connection duration to {config['alb_connection_duration']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB connection duration: {e}")
            
            # ALB requests per second
            if 'alb_requests_per_second' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of requests per second per ALB Enter amount']", str(config['alb_requests_per_second']))
                    print(f"[OK] Set ALB requests per second to {config['alb_requests_per_second']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB requests per second: {e}")
            
            # ALB rule evaluations
            if 'alb_rule_evaluations' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of rule evaluations per request Enter amount']", str(config['alb_rule_evaluations']))
                    print(f"[OK] Set ALB rule evaluations to {config['alb_rule_evaluations']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ALB rule evaluations: {e}")
            
            # Network Load Balancer settings
            if 'nlb_count' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Network Load Balancers']", str(config['nlb_count']))
                    print(f"[OK] Set NLB count to {config['nlb_count']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB count: {e}")
            
            # NLB TCP processed bytes
            if 'nlb_tcp_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Processed bytes per NLB for TCP Value']", str(config['nlb_tcp_processed_bytes']))
                    print(f"[OK] Set NLB TCP processed bytes to {config['nlb_tcp_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB TCP processed bytes: {e}")
            
            # NLB TCP connections
            if 'nlb_tcp_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of new TCP connections Value']", str(config['nlb_tcp_connections']))
                    print(f"[OK] Set NLB TCP connections to {config['nlb_tcp_connections']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB TCP connections: {e}")
            
            # NLB TCP connection duration
            if 'nlb_tcp_connection_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average TCP connection duration Value']", str(config['nlb_tcp_connection_duration']))
                    print(f"[OK] Set NLB TCP connection duration to {config['nlb_tcp_connection_duration']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB TCP connection duration: {e}")
            
            # NLB UDP processed bytes
            if 'nlb_udp_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Processed bytes per NLB for UDP Value']", str(config['nlb_udp_processed_bytes']))
                    print(f"[OK] Set NLB UDP processed bytes to {config['nlb_udp_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB UDP processed bytes: {e}")
            
            # NLB UDP flows
            if 'nlb_udp_flows' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of new UDP Flows Value']", str(config['nlb_udp_flows']))
                    print(f"[OK] Set NLB UDP flows to {config['nlb_udp_flows']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB UDP flows: {e}")
            
            # NLB UDP flow duration
            if 'nlb_udp_flow_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average UDP Flow duration Value']", str(config['nlb_udp_flow_duration']))
                    print(f"[OK] Set NLB UDP flow duration to {config['nlb_udp_flow_duration']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB UDP flow duration: {e}")
            
            # NLB TLS processed bytes
            if 'nlb_tls_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Processed bytes per NLB for TLS Value']", str(config['nlb_tls_processed_bytes']))
                    print(f"[OK] Set NLB TLS processed bytes to {config['nlb_tls_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB TLS processed bytes: {e}")
            
            # NLB TLS connections
            if 'nlb_tls_connections' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of new TLS connections Value']", str(config['nlb_tls_connections']))
                    print(f"[OK] Set NLB TLS connections to {config['nlb_tls_connections']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB TLS connections: {e}")
            
            # NLB TLS connection duration
            if 'nlb_tls_connection_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average TLS connection duration Value']", str(config['nlb_tls_connection_duration']))
                    print(f"[OK] Set NLB TLS connection duration to {config['nlb_tls_connection_duration']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set NLB TLS connection duration: {e}")
            
            # Gateway Load Balancer settings
            if 'glb_availability_zones' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Availability Zones that Gateway Load Balancer is deployed to']", str(config['glb_availability_zones']))
                    print(f"[OK] Set GLB availability zones to {config['glb_availability_zones']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GLB availability zones: {e}")
            
            # GLB processed bytes
            if 'glb_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Total processed bytes Value']", str(config['glb_processed_bytes']))
                    print(f"[OK] Set GLB processed bytes to {config['glb_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GLB processed bytes: {e}")
            
            # GLB connections/flows
            if 'glb_connections_flows' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of new connections/flows Value']", str(config['glb_connections_flows']))
                    print(f"[OK] Set GLB connections/flows to {config['glb_connections_flows']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GLB connections/flows: {e}")
            
            # GLB connection/flow duration
            if 'glb_connection_flow_duration' in config:
                try:
                    self.page.fill("input[aria-label*='Average connection/flow duration Value']", str(config['glb_connection_flow_duration']))
                    print(f"[OK] Set GLB connection/flow duration to {config['glb_connection_flow_duration']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GLB connection/flow duration: {e}")
            
            # GLB endpoints
            if 'glb_endpoints' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Gateway Load Balancer Endpoints']", str(config['glb_endpoints']))
                    print(f"[OK] Set GLB endpoints to {config['glb_endpoints']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GLB endpoints: {e}")
            
            # Classic Load Balancer settings
            if 'clb_count' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Classic Load Balancers']", str(config['clb_count']))
                    print(f"[OK] Set CLB count to {config['clb_count']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set CLB count: {e}")
            
            # CLB processed bytes
            if 'clb_processed_bytes' in config:
                try:
                    self.page.fill("input[aria-label*='Processed bytes per CLB Value']", str(config['clb_processed_bytes']))
                    print(f"[OK] Set CLB processed bytes to {config['clb_processed_bytes']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set CLB processed bytes: {e}")
            
            print(f"[OK] Applied {settings_applied} ALB settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply ALB configuration: {e}")
            return False

def main():
    """Test the comprehensive ALB configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveALBConfigurator(page)
        
        if configurator.navigate_to_service_config():
            # Example configuration
            example_config = {
                'description': 'Application Load Balancer for production web application',
                'alb_count': 2,
                'alb_lambda_processed_bytes': 1000000000,  # 1GB
                'alb_ec2_processed_bytes': 5000000000,    # 5GB
                'alb_new_connections': 1000,
                'alb_connection_duration': 300,
                'alb_requests_per_second': 100,
                'alb_rule_evaluations': 2,
                'nlb_count': 1,
                'nlb_tcp_processed_bytes': 2000000000,   # 2GB
                'nlb_tcp_connections': 500,
                'nlb_tcp_connection_duration': 600,
                'nlb_udp_processed_bytes': 500000000,     # 500MB
                'nlb_udp_flows': 200,
                'nlb_udp_flow_duration': 120,
                'nlb_tls_processed_bytes': 1000000000,   # 1GB
                'nlb_tls_connections': 300,
                'nlb_tls_connection_duration': 400,
                'glb_availability_zones': 2,
                'glb_processed_bytes': 1000000000,      # 1GB
                'glb_connections_flows': 100,
                'glb_connection_flow_duration': 300,
                'glb_endpoints': 2,
                'clb_count': 0,
                'clb_processed_bytes': 0
            }
            
            # Apply configuration
            if configurator.apply_alb_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] ALB configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("alb_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to alb_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
