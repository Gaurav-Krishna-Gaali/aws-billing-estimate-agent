"""
Robust AWS OpenSearch Configuration Class
Uses exact field information from discovery to handle all dynamic options
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class RobustAWSOpenSearchConfigurator(BaseAWSConfigurator):
    """Robust AWS OpenSearch configuration class using exact field mappings"""
    
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
    
    def apply_robust_aws_opensearch_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS OpenSearch configuration using robust field discovery"""
        try:
            print(f"\n[INFO] Applying robust AWS OpenSearch configuration...")
            
            # Wait for page to fully load
            self.page.wait_for_timeout(3000)
            
            settings_applied = 0
            
            # First, let's discover all current input fields
            print(f"\n[INFO] Discovering all current input fields...")
            all_inputs = self.page.query_selector_all("input[type='text'], input[type='number']")
            
            for i, input_field in enumerate(all_inputs):
                try:
                    aria_label = input_field.get_attribute("aria-label")
                    placeholder = input_field.get_attribute("placeholder")
                    name = input_field.get_attribute("name")
                    is_visible = input_field.is_visible()
                    
                    if is_visible and (aria_label or placeholder):
                        field_identifier = aria_label or placeholder
                        print(f"[INFO] Found field {i}: {field_identifier}")
                        
                        # Try to fill with appropriate value based on field type
                        value_to_fill = None
                        
                        if "description" in field_identifier.lower():
                            value_to_fill = config.get("description", "AWS OpenSearch cluster")
                        elif "node" in field_identifier.lower():
                            value_to_fill = config.get("nodes", 3)
                        elif "instance" in field_identifier.lower() and "number" in field_identifier.lower():
                            value_to_fill = config.get("instances", 3)
                        elif "storage" in field_identifier.lower() and "amount" in field_identifier.lower():
                            value_to_fill = config.get("storage_gb", 500)
                        elif "utilization" in field_identifier.lower():
                            value_to_fill = config.get("utilization_percent", 80)
                        elif "managed" in field_identifier.lower() and "storage" in field_identifier.lower():
                            value_to_fill = config.get("managed_storage_gb", 1000)
                        elif "iops" in field_identifier.lower():
                            value_to_fill = config.get("iops", 3000)
                        elif "throughput" in field_identifier.lower():
                            value_to_fill = config.get("throughput_mbps", 125)
                        else:
                            # Default value for unidentified fields
                            value_to_fill = 1
                        
                        if value_to_fill is not None:
                            input_field.fill(str(value_to_fill))
                            print(f"[OK] Filled {field_identifier}: {value_to_fill}")
                            settings_applied += 1
                            
                except Exception as e:
                    print(f"[WARNING] Could not process input field {i}: {e}")
            
            # Handle radio buttons for OpenSearch type selection
            print(f"\n[INFO] Handling radio button selections...")
            radio_buttons = self.page.query_selector_all("input[type='radio']")
            
            for i, radio in enumerate(radio_buttons):
                try:
                    value = radio.get_attribute("value")
                    name = radio.get_attribute("name")
                    is_visible = radio.is_visible()
                    
                    if is_visible and value:
                        print(f"[INFO] Found radio button {i}: {name} = {value}")
                        
                        # Select appropriate radio button based on configuration
                        opensearch_type = config.get("opensearch_type", "traditional")
                        
                        should_select = False
                        if opensearch_type == "traditional" and "elasticSearchService" in value and "serverless" not in value:
                            should_select = True
                        elif opensearch_type == "serverless" and "serverlesss" in value and "Ingestion" not in value:
                            should_select = True
                        elif opensearch_type == "serverless_ingestion" and "Ingestion" in value:
                            should_select = True
                        
                        if should_select:
                            radio.click()
                            self.page.wait_for_timeout(1000)  # Wait for UI to update
                            print(f"[OK] Selected radio button: {value}")
                            settings_applied += 1
                            
                except Exception as e:
                    print(f"[WARNING] Could not process radio button {i}: {e}")
            
            # Handle button selections (like instance types, storage types, etc.)
            print(f"\n[INFO] Handling button selections...")
            buttons = self.page.query_selector_all("button")
            
            for i, button in enumerate(buttons):
                try:
                    text = button.text_content()
                    aria_label = button.get_attribute("aria-label")
                    is_visible = button.is_visible()
                    
                    if is_visible and text and len(text.strip()) > 0:
                        button_identifier = text.strip()
                        
                        # Select appropriate buttons based on configuration
                        should_click = False
                        
                        # Instance type selection
                        if "Memory optimized" in button_identifier:
                            should_click = True
                        elif "OnDemand" in button_identifier:
                            should_click = True
                        elif "EBS Only" in button_identifier:
                            should_click = True
                        elif "General Purpose SSD" in button_identifier:
                            should_click = True
                        elif "GB" in button_identifier and len(button_identifier) <= 5:  # Storage unit
                            should_click = True
                        elif "MBps" in button_identifier:  # Throughput unit
                            should_click = True
                        elif "TB" in button_identifier and len(button_identifier) <= 5:  # Data transfer unit
                            should_click = True
                        
                        if should_click:
                            try:
                                button.click()
                                print(f"[OK] Clicked button: {button_identifier}")
                                settings_applied += 1
                            except Exception as e:
                                print(f"[WARNING] Could not click button '{button_identifier}': {e}")
                                
                except Exception as e:
                    print(f"[WARNING] Could not process button {i}: {e}")
            
            print(f"[OK] Applied {settings_applied} AWS OpenSearch settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply robust AWS OpenSearch configuration: {e}")
            return False


def main():
    """Test the robust AWS OpenSearch configurator"""
    from playwright.sync_api import sync_playwright
    
    # Test configuration with all options
    test_config = {
        'description': 'Robust AWS OpenSearch cluster with all dynamic options',
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
        
        configurator = RobustAWSOpenSearchConfigurator(page)
        
        if configurator.navigate_to_aws_opensearch_config():
            # Apply robust configuration
            if configurator.apply_robust_aws_opensearch_configuration(test_config):
                print(f"\n[SUCCESS] Robust configuration applied successfully!")
                
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS OpenSearch configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("robust_aws_opensearch_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to robust_aws_opensearch_estimate_url.txt")
            else:
                print(f"[ERROR] Failed to apply robust configuration")
        else:
            print(f"[ERROR] Failed to navigate to AWS OpenSearch configuration")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
