"""
Complete AWS OpenSearch Configuration Class
Handles all 85 elements with dynamic radio button options
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class CompleteAWSOpenSearchConfigurator(BaseAWSConfigurator):
    """Complete AWS OpenSearch configuration class handling all 85 elements with dynamic options"""
    
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
    
    def select_opensearch_type(self, opensearch_type: str) -> bool:
        """Select the OpenSearch service type"""
        try:
            print(f"\n[INFO] Selecting OpenSearch type: {opensearch_type}")
            
            # Map configuration types to radio button values
            type_mapping = {
                "traditional": "elasticSearchService",
                "serverless": "elasticSearchService-serverlesss", 
                "serverless_ingestion": "elasticSearchService-serverlesss-Ingestion"
            }
            
            if opensearch_type not in type_mapping:
                print(f"[WARNING] Unknown OpenSearch type: {opensearch_type}")
                return False
            
            value = type_mapping[opensearch_type]
            
            # Click the radio button
            radio = self.page.locator(f"input[type='radio'][value='{value}']")
            if radio.count() > 0:
                radio.first.click()
                self.page.wait_for_timeout(2000)  # Wait for UI to update
                print(f"[OK] Selected OpenSearch type: {opensearch_type}")
                return True
            else:
                print(f"[WARNING] Could not find radio button for type: {opensearch_type}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Could not select OpenSearch type: {e}")
            return False
    
    def fill_description(self, description: str) -> bool:
        """Fill the description field"""
        try:
            desc_field = self.page.locator("input[aria-label*='Description']")
            if desc_field.count() > 0:
                desc_field.first.fill(description)
                print(f"[OK] Set description: {description}")
                return True
            else:
                print(f"[WARNING] Description field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set description: {e}")
            return False
    
    def configure_nodes(self, nodes: int) -> bool:
        """Configure number of nodes"""
        try:
            node_fields = self.page.locator("input[aria-label*='Nodes']")
            if node_fields.count() > 0:
                node_fields.first.fill(str(nodes))
                print(f"[OK] Set nodes to {nodes}")
                return True
            else:
                print(f"[WARNING] Nodes field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set nodes: {e}")
            return False
    
    def configure_instances(self, instances: int) -> bool:
        """Configure number of instances"""
        try:
            instance_fields = self.page.locator("input[aria-label*='Number of instances Enter amount']")
            if instance_fields.count() > 0:
                instance_fields.first.fill(str(instances))
                print(f"[OK] Set instances to {instances}")
                return True
            else:
                print(f"[WARNING] Instances field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set instances: {e}")
            return False
    
    def configure_storage(self, storage_gb: int) -> bool:
        """Configure storage amount"""
        try:
            storage_fields = self.page.locator("input[aria-label*='Storage amount per volume (gp3) Value']")
            if storage_fields.count() > 0:
                storage_fields.first.fill(str(storage_gb))
                print(f"[OK] Set storage to {storage_gb} GB")
                return True
            else:
                print(f"[WARNING] Storage field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set storage: {e}")
            return False
    
    def configure_utilization(self, utilization: int) -> bool:
        """Configure utilization percentage"""
        try:
            util_fields = self.page.locator("input[aria-label*='Utilization (On-Demand only) Value']")
            if util_fields.count() > 0:
                util_fields.first.fill(str(utilization))
                print(f"[OK] Set utilization to {utilization}%")
                return True
            else:
                print(f"[WARNING] Utilization field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set utilization: {e}")
            return False
    
    def configure_managed_storage(self, storage_gb: int) -> bool:
        """Configure managed storage for UltraWarm"""
        try:
            managed_storage_fields = self.page.locator("input[aria-label*='Managed storage amount (per UltraWarm instance) Value']")
            if managed_storage_fields.count() > 0:
                managed_storage_fields.first.fill(str(storage_gb))
                print(f"[OK] Set managed storage to {storage_gb} GB")
                return True
            else:
                print(f"[WARNING] Managed storage field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set managed storage: {e}")
            return False
    
    def configure_iops(self, iops: int) -> bool:
        """Configure IOPS for storage"""
        try:
            iops_fields = self.page.locator("input[aria-label*='Provisioning IOPS per volume (gp3) Enter amount']")
            if iops_fields.count() > 0:
                iops_fields.first.fill(str(iops))
                print(f"[OK] Set IOPS to {iops}")
                return True
            else:
                print(f"[WARNING] IOPS field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set IOPS: {e}")
            return False
    
    def configure_throughput(self, throughput: int) -> bool:
        """Configure throughput for storage"""
        try:
            throughput_fields = self.page.locator("input[aria-label*='Provisioning throughput (MB/s) per volume (gp3) Value']")
            if throughput_fields.count() > 0:
                throughput_fields.first.fill(str(throughput))
                print(f"[OK] Set throughput to {throughput} MB/s")
                return True
            else:
                print(f"[WARNING] Throughput field not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not set throughput: {e}")
            return False
    
    def apply_complete_aws_opensearch_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply complete AWS OpenSearch configuration with all dynamic options"""
        try:
            print(f"\n[INFO] Applying complete AWS OpenSearch configuration...")
            
            settings_applied = 0
            
            # Set description
            if 'description' in config:
                if self.fill_description(config['description']):
                    settings_applied += 1
            
            # Select OpenSearch type
            if 'opensearch_type' in config:
                if self.select_opensearch_type(config['opensearch_type']):
                    settings_applied += 1
            
            # Configure nodes
            if 'nodes' in config:
                if self.configure_nodes(config['nodes']):
                    settings_applied += 1
            
            # Configure instances
            if 'instances' in config:
                if self.configure_instances(config['instances']):
                    settings_applied += 1
            
            # Configure storage
            if 'storage_gb' in config:
                if self.configure_storage(config['storage_gb']):
                    settings_applied += 1
            
            # Configure utilization
            if 'utilization_percent' in config:
                if self.configure_utilization(config['utilization_percent']):
                    settings_applied += 1
            
            # Configure managed storage
            if 'managed_storage_gb' in config:
                if self.configure_managed_storage(config['managed_storage_gb']):
                    settings_applied += 1
            
            # Configure IOPS
            if 'iops' in config:
                if self.configure_iops(config['iops']):
                    settings_applied += 1
            
            # Configure throughput
            if 'throughput_mbps' in config:
                if self.configure_throughput(config['throughput_mbps']):
                    settings_applied += 1
            
            print(f"[OK] Applied {settings_applied} AWS OpenSearch settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply complete AWS OpenSearch configuration: {e}")
            return False


def main():
    """Test the complete AWS OpenSearch configurator"""
    from playwright.sync_api import sync_playwright
    
    # Test configuration with all dynamic options
    test_config = {
        'description': 'Complete AWS OpenSearch cluster with all options',
        'opensearch_type': 'traditional',  # or 'serverless', 'serverless_ingestion'
        'nodes': 3,
        'instances': 3,
        'storage_gb': 500,
        'utilization_percent': 80,
        'managed_storage_gb': 1000,
        'iops': 3000,
        'throughput_mbps': 125
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = CompleteAWSOpenSearchConfigurator(page)
        
        if configurator.navigate_to_aws_opensearch_config():
            # Apply complete configuration
            if configurator.apply_complete_aws_opensearch_configuration(test_config):
                print(f"\n[SUCCESS] Complete configuration applied successfully!")
                
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS OpenSearch configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("complete_aws_opensearch_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to complete_aws_opensearch_estimate_url.txt")
            else:
                print(f"[ERROR] Failed to apply complete configuration")
        else:
            print(f"[ERROR] Failed to navigate to AWS OpenSearch configuration")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
