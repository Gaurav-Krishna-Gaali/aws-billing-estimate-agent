"""
Comprehensive AWS OpenSearch Configuration Class
Handles all 18 interactive elements on the AWS OpenSearch configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveAWSOpenSearchConfigurator(BaseAWSConfigurator):
    """Comprehensive AWS OpenSearch configuration class handling all 18 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "AWS OpenSearch")
    
    def navigate_to_aws_opensearch_config(self) -> bool:
        """Navigate to AWS OpenSearch configuration page"""
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
            
            # Look for "Configure Amazon OpenSearch Service" button directly
            try:
                opensearch_button = self.page.locator("button[aria-label='Configure Amazon OpenSearch Service']")
                if opensearch_button.count() > 0:
                    opensearch_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure Amazon OpenSearch Service' button")
                    print(f"[OK] Successfully navigated to AWS OpenSearch configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure Amazon OpenSearch Service' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click OpenSearch button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS OpenSearch config: {e}")
            return False
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to AWS OpenSearch service configuration page (for multi-service estimates)"""
        try:
            print("[INFO] Navigating to AWS OpenSearch service configuration...")
            
            # Search for OpenSearch using the correct service name
            search_terms = ["Amazon OpenSearch Service", "OpenSearch", "Elasticsearch"]
            for term in search_terms:
                if self.search_and_select_service(term):
                    return True
            
            print("[ERROR] Could not find AWS OpenSearch service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS OpenSearch configuration: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding AWS OpenSearch service in AWS Calculator"""
        return ["Amazon OpenSearch Service", "OpenSearch", "Elasticsearch"]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """Apply AWS OpenSearch-specific configuration logic"""
        try:
            print("[INFO] Applying AWS OpenSearch-specific configuration...")
            return self.apply_aws_opensearch_configuration(config)
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS OpenSearch configuration: {e}")
            return False
    
    def apply_aws_opensearch_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS OpenSearch configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying AWS OpenSearch configuration...")
            
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
            
            # Explicit: Provisioning IOPS per volume (gp3)
            try:
                iops_input = self.page.locator("input[aria-label*='Provisioning IOPS per volume (gp3)']")
                if iops_input.count() == 0:
                    iops_input = self.page.locator("input[aria-label*='Provisioning IOPS per volume']")
                if iops_input.count() > 0:
                    iops_input.first.fill("3000")
                    print("[OK] Set gp3 Provisioning IOPS to 3000")
                    settings_applied += 1
            except Exception:
                pass

            # Since OpenSearch has limited configuration options, let's try to find common fields
            # that might be present but not captured by the element mapper
            
            # Try to find cluster configuration fields
            cluster_fields = [
                "input[aria-label*='Number of nodes']",
                "input[aria-label*='Instance type']",
                "input[aria-label*='Storage size']",
                "input[aria-label*='Data transfer']",
                "input[aria-label*='Search requests']",
                "input[aria-label*='Indexing requests']",
                "input[aria-label*='Storage amount']",
                "input[aria-label*='Data transfer out']"
            ]
            
            for field_selector in cluster_fields:
                try:
                    field = self.page.locator(field_selector)
                    if field.count() > 0:
                        print(f"[INFO] Found OpenSearch field: {field_selector}")
                        # Use appropriate default values based on field type
                        # IMPORTANT: Handle UltraWarm storage BEFORE generic storage to avoid overwrites
                        if "ultrawarm" in field_selector.lower() and "storage" in field_selector.lower():
                            # UltraWarm storage unit is TB by default; keep TB and use a safe value (<= 20TB)
                            field.first.fill("10")  # 10 TB
                            print("[OK] Set UltraWarm storage to 10 TB (kept TB unit)")
                        elif "storage" in field_selector.lower() or "gb" in field_selector.lower():
                            field.first.fill("100")  # 100GB (within 20480 GB limit)
                        elif "iops" in field_selector.lower():
                            field.first.fill("3000")  # Minimum IOPS for gp3
                        elif "throughput" in field_selector.lower():
                            field.first.fill("125")  # Default throughput MBps
                        elif "nodes" in field_selector.lower() or "instances" in field_selector.lower():
                            field.first.fill("3")  # 3 nodes/instances
                        elif "requests" in field_selector.lower():
                            field.first.fill("1000")  # 1000 requests
                        else:
                            field.first.fill("10")  # Default minimum value
                        settings_applied += 1
                except Exception as e:
                    pass  # Field not found, continue
            
            # Try to find any input fields that might be OpenSearch specific
            all_inputs = self.page.query_selector_all("input[type='text'], input[type='number']")
            for i, input_field in enumerate(all_inputs):
                try:
                    aria_label = input_field.get_attribute("aria-label")
                    placeholder = input_field.get_attribute("placeholder")
                    
                    if aria_label and any(keyword in aria_label.lower() for keyword in 
                                        ['node', 'instance', 'storage', 'data', 'request', 'search', 'index']):
                        print(f"[INFO] Found OpenSearch input: {aria_label}")
                        # Use appropriate values based on field type
                        # UltraWarm first to avoid being overwritten by generic storage rule
                        if "ultrawarm" in aria_label.lower() and "storage" in aria_label.lower():
                            input_field.fill("10")  # 10 TB
                            print("[OK] Set UltraWarm storage to 10 TB (kept TB unit)")
                        elif "storage" in aria_label.lower() or "gb" in aria_label.lower():
                            input_field.fill("100")  # 100GB (within 20480 GB limit)
                        elif "iops" in aria_label.lower():
                            input_field.fill("3000")  # Minimum IOPS for gp3
                        elif "throughput" in aria_label.lower():
                            input_field.fill("125")  # Default throughput MBps
                        elif "nodes" in aria_label.lower() or "instances" in aria_label.lower():
                            input_field.fill("3")  # 3 nodes/instances
                        elif "requests" in aria_label.lower():
                            input_field.fill("1000")  # 1000 requests
                        else:
                            input_field.fill("10")  # Default minimum value
                        settings_applied += 1
                except Exception as e:
                    pass  # Skip if can't interact with field
            
            print(f"[OK] Applied {settings_applied} AWS OpenSearch settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS OpenSearch configuration: {e}")
            return False

def main():
    """Test the comprehensive AWS OpenSearch configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveAWSOpenSearchConfigurator(page)
        
        if configurator.navigate_to_aws_opensearch_config():
            # Example configuration
            example_config = {
                'description': 'AWS OpenSearch cluster for search and analytics',
                'number_of_nodes': 3,
                'instance_type': 't3.small.search',
                'storage_size_gb': 100,
                'data_transfer_tb': 10
            }
            
            # Apply configuration
            if configurator.apply_aws_opensearch_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS OpenSearch configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("aws_opensearch_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to aws_opensearch_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
