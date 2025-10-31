"""
Comprehensive WAF Configuration Class
Handles all 40 interactive elements on the WAF configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveWAFConfigurator(BaseAWSConfigurator):
    """Comprehensive WAF configuration class handling all 40 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "WAF")
    
    def navigate_to_waf_config(self) -> bool:
        """Navigate to WAF configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for AWS Web Application Firewall (WAF)
            if not self.search_and_select_service("AWS Web Application Firewall (WAF)"):
                return False
            
            print(f"[OK] Successfully navigated to WAF configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to WAF config: {e}")
            return False
    
    def apply_waf_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply WAF configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying WAF configuration...")
            
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
            
            # Web ACLs
            if 'web_acls' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Web Access Control Lists (Web ACLs) utilized Value']", str(config['web_acls']))
                    print(f"[OK] Set Web ACLs to {config['web_acls']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Web ACLs: {e}")
            
            # Rules per Web ACL
            if 'rules_per_web_acl' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Rules added per Web ACL Value']", str(config['rules_per_web_acl']))
                    print(f"[OK] Set rules per Web ACL to {config['rules_per_web_acl']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set rules per Web ACL: {e}")
            
            # Rule Groups per Web ACL
            if 'rule_groups_per_web_acl' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Rule Groups per Web ACL Value']", str(config['rule_groups_per_web_acl']))
                    print(f"[OK] Set rule groups per Web ACL to {config['rule_groups_per_web_acl']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set rule groups per Web ACL: {e}")
            
            # Rules inside each Rule Group
            if 'rules_inside_rule_group' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Rules inside each Rule Group Value']", str(config['rules_inside_rule_group']))
                    print(f"[OK] Set rules inside rule group to {config['rules_inside_rule_group']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set rules inside rule group: {e}")
            
            # Managed Rule Groups per Web ACL
            if 'managed_rule_groups_per_web_acl' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Managed Rule Groups per Web ACL Value']", str(config['managed_rule_groups_per_web_acl']))
                    print(f"[OK] Set managed rule groups per Web ACL to {config['managed_rule_groups_per_web_acl']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set managed rule groups per Web ACL: {e}")
            
            # Web requests received
            if 'web_requests_received' in config:
                try:
                    self.page.fill("input[aria-label*='Number of web requests received across all web ACLs Value']", str(config['web_requests_received']))
                    print(f"[OK] Set web requests received to {config['web_requests_received']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set web requests received: {e}")
            
            print(f"[OK] Applied {settings_applied} WAF settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply WAF configuration: {e}")
            return False
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to WAF service configuration page (for multi-service estimates)"""
        try:
            print("[INFO] Navigating to WAF service configuration...")
            search_terms = ["AWS Web Application Firewall (WAF)", "WAF", "Web Application Firewall"]
            for term in search_terms:
                if self.search_and_select_service(term):
                    return True
            
            print("[ERROR] Could not find WAF service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to WAF configuration: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding WAF service in AWS Calculator"""
        return ["AWS Web Application Firewall (WAF)", "WAF", "Web Application Firewall"]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """Apply WAF-specific configuration logic"""
        try:
            print("[INFO] Applying WAF-specific configuration...")
            return self.apply_waf_configuration(config)
        except Exception as e:
            print(f"[ERROR] Failed to apply WAF configuration: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Test the comprehensive WAF configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveWAFConfigurator(page)
        
        if configurator.navigate_to_waf_config():
            # Example configuration
            example_config = {
                'description': 'WAF protection for production web application',
                'web_acls': 2,
                'rules_per_web_acl': 10,
                'rule_groups_per_web_acl': 3,
                'rules_inside_rule_group': 5,
                'managed_rule_groups_per_web_acl': 2,
                'web_requests_received': 1000000
            }
            
            # Apply configuration
            if configurator.apply_waf_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] WAF configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("waf_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to waf_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
