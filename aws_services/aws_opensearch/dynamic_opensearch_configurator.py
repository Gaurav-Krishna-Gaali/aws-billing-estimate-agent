"""
Dynamic AWS OpenSearch Configuration Class
Handles dynamic UI options that change based on radio button selections
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class DynamicAWSOpenSearchConfigurator(BaseAWSConfigurator):
    """Dynamic AWS OpenSearch configuration class that handles changing UI options"""
    
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
    
    def discover_all_radio_buttons(self) -> List[Dict]:
        """Discover all radio buttons and their options"""
        print(f"\n[INFO] Discovering all radio button options...")
        
        radio_buttons = []
        
        # Find all radio button groups
        radio_groups = self.page.query_selector_all("input[type='radio']")
        
        for i, radio in enumerate(radio_groups):
            try:
                name = radio.get_attribute("name")
                value = radio.get_attribute("value")
                checked = radio.is_checked()
                aria_label = radio.get_attribute("aria-label")
                
                # Find the label text
                label_text = ""
                try:
                    # Try to find associated label
                    label = self.page.locator(f"label[for='{radio.get_attribute('id')}']")
                    if label.count() > 0:
                        label_text = label.first.text_content().strip()
                except:
                    pass
                
                radio_info = {
                    "index": i,
                    "name": name,
                    "value": value,
                    "checked": checked,
                    "aria_label": aria_label,
                    "label_text": label_text
                }
                
                radio_buttons.append(radio_info)
                print(f"[INFO] Radio {i}: {name} = {value} (checked: {checked}) - {label_text}")
                
            except Exception as e:
                print(f"[WARNING] Could not process radio button {i}: {e}")
        
        return radio_buttons
    
    def click_radio_button_by_value(self, value: str) -> bool:
        """Click a radio button by its value"""
        try:
            radio = self.page.locator(f"input[type='radio'][value='{value}']")
            if radio.count() > 0:
                radio.first.click()
                self.page.wait_for_timeout(1000)  # Wait for UI to update
                print(f"[OK] Clicked radio button with value: {value}")
                return True
            else:
                print(f"[WARNING] Radio button with value '{value}' not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not click radio button '{value}': {e}")
            return False
    
    def click_radio_button_by_text(self, text: str) -> bool:
        """Click a radio button by its label text"""
        try:
            # Try to find radio button by label text
            radio = self.page.locator(f"input[type='radio']").filter(has_text=text)
            if radio.count() > 0:
                radio.first.click()
                self.page.wait_for_timeout(1000)  # Wait for UI to update
                print(f"[OK] Clicked radio button with text: {text}")
                return True
            else:
                print(f"[WARNING] Radio button with text '{text}' not found")
                return False
        except Exception as e:
            print(f"[WARNING] Could not click radio button with text '{text}': {e}")
            return False
    
    def discover_all_input_fields(self) -> List[Dict]:
        """Discover all input fields after radio button selections"""
        print(f"\n[INFO] Discovering all input fields...")
        
        input_fields = []
        
        # Find all input fields
        inputs = self.page.query_selector_all("input[type='text'], input[type='number'], input[type='email']")
        
        for i, input_field in enumerate(inputs):
            try:
                field_type = input_field.get_attribute("type")
                aria_label = input_field.get_attribute("aria-label")
                placeholder = input_field.get_attribute("placeholder")
                name = input_field.get_attribute("name")
                id_attr = input_field.get_attribute("id")
                value = input_field.get_attribute("value")
                
                # Check if field is visible
                is_visible = input_field.is_visible()
                
                field_info = {
                    "index": i,
                    "type": field_type,
                    "aria_label": aria_label,
                    "placeholder": placeholder,
                    "name": name,
                    "id": id_attr,
                    "value": value,
                    "visible": is_visible
                }
                
                input_fields.append(field_info)
                
                if is_visible:
                    print(f"[INFO] Input {i}: {aria_label or placeholder or name} ({field_type}) - Visible")
                else:
                    print(f"[INFO] Input {i}: {aria_label or placeholder or name} ({field_type}) - Hidden")
                
            except Exception as e:
                print(f"[WARNING] Could not process input field {i}: {e}")
        
        return input_fields
    
    def fill_all_visible_inputs(self, config: Dict[str, Any]) -> int:
        """Fill all visible input fields with configuration values"""
        print(f"\n[INFO] Filling all visible input fields...")
        
        fields_filled = 0
        input_fields = self.discover_all_input_fields()
        
        for field in input_fields:
            if not field["visible"]:
                continue
                
            try:
                aria_label = field.get("aria_label", "")
                placeholder = field.get("placeholder", "")
                name = field.get("name", "")
                
                # Determine what value to use based on field identification
                value_to_fill = None
                
                # Map common OpenSearch fields
                if "node" in aria_label.lower() or "node" in placeholder.lower():
                    value_to_fill = config.get("number_of_nodes", 1)
                elif "instance" in aria_label.lower() or "instance" in placeholder.lower():
                    value_to_fill = config.get("number_of_instances", 1)
                elif "storage" in aria_label.lower() or "storage" in placeholder.lower():
                    value_to_fill = config.get("storage_size_gb", 100)
                elif "data" in aria_label.lower() and "transfer" in aria_label.lower():
                    value_to_fill = config.get("data_transfer_tb", 10)
                elif "search" in aria_label.lower() and "request" in aria_label.lower():
                    value_to_fill = config.get("search_requests", 1000)
                elif "index" in aria_label.lower() and "request" in aria_label.lower():
                    value_to_fill = config.get("indexing_requests", 500)
                elif "ocu" in aria_label.lower() and "index" in aria_label.lower():
                    value_to_fill = config.get("indexing_ocus", 1)
                elif "ocu" in aria_label.lower() and "search" in aria_label.lower():
                    value_to_fill = config.get("search_ocus", 1)
                elif "index" in aria_label.lower() and "data" in aria_label.lower():
                    value_to_fill = config.get("index_data_size_gb", 10)
                elif "description" in aria_label.lower():
                    value_to_fill = config.get("description", "AWS OpenSearch cluster")
                else:
                    # Default values for unidentified fields
                    value_to_fill = 1
                
                if value_to_fill is not None:
                    # Find the input field and fill it
                    input_selector = f"input[aria-label*='{aria_label}']" if aria_label else f"input:nth-of-type({field['index'] + 1})"
                    input_field_element = self.page.locator(input_selector)
                    
                    if input_field_element.count() > 0:
                        input_field_element.first.fill(str(value_to_fill))
                        print(f"[OK] Filled {aria_label or placeholder or name}: {value_to_fill}")
                        fields_filled += 1
                    else:
                        print(f"[WARNING] Could not find input field: {aria_label or placeholder or name}")
                        
            except Exception as e:
                print(f"[WARNING] Could not fill field {field.get('aria_label', 'unknown')}: {e}")
        
        return fields_filled
    
    def explore_all_radio_options(self) -> Dict[str, List[Dict]]:
        """Explore all radio button options and their resulting input fields"""
        print(f"\n[INFO] Exploring all radio button options and their effects...")
        
        all_options = {}
        radio_buttons = self.discover_all_radio_buttons()
        
        # Group radio buttons by name
        radio_groups = {}
        for radio in radio_buttons:
            name = radio.get("name", "unknown")
            if name not in radio_groups:
                radio_groups[name] = []
            radio_groups[name].append(radio)
        
        # Explore each radio group
        for group_name, radios in radio_groups.items():
            print(f"\n[INFO] Exploring radio group: {group_name}")
            group_options = []
            
            for radio in radios:
                try:
                    value = radio.get("value", "")
                    label = radio.get("label_text", "")
                    
                    print(f"[INFO] Testing option: {label} ({value})")
                    
                    # Click this radio button
                    if self.click_radio_button_by_value(value):
                        # Wait for UI to update
                        self.page.wait_for_timeout(2000)
                        
                        # Discover input fields that appear
                        input_fields = self.discover_all_input_fields()
                        visible_fields = [f for f in input_fields if f.get("visible", False)]
                        
                        option_info = {
                            "value": value,
                            "label": label,
                            "input_fields": visible_fields,
                            "field_count": len(visible_fields)
                        }
                        
                        group_options.append(option_info)
                        print(f"[OK] Option '{label}' revealed {len(visible_fields)} input fields")
                        
                except Exception as e:
                    print(f"[WARNING] Could not explore option {radio.get('value', 'unknown')}: {e}")
            
            all_options[group_name] = group_options
        
        return all_options
    
    def apply_dynamic_aws_opensearch_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS OpenSearch configuration with dynamic option handling"""
        try:
            print(f"\n[INFO] Applying dynamic AWS OpenSearch configuration...")
            
            # First, explore all radio button options
            all_options = self.explore_all_radio_options()
            
            # Apply configuration based on available options
            settings_applied = 0
            
            # Set description if available
            if 'description' in config:
                try:
                    desc_field = self.page.locator("input[aria-label*='Description']")
                    if desc_field.count() > 0:
                        desc_field.first.fill(config['description'])
                        print(f"[OK] Set description: {config['description']}")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set description: {e}")
            
            # Try to select appropriate radio button options
            if 'deployment_type' in config:
                # Try to select deployment type
                if self.click_radio_button_by_text(config['deployment_type']):
                    settings_applied += 1
            
            if 'instance_type' in config:
                # Try to select instance type
                if self.click_radio_button_by_text(config['instance_type']):
                    settings_applied += 1
            
            # Fill all visible input fields
            fields_filled = self.fill_all_visible_inputs(config)
            settings_applied += fields_filled
            
            print(f"[OK] Applied {settings_applied} AWS OpenSearch settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply dynamic AWS OpenSearch configuration: {e}")
            return False

def main():
    """Test the dynamic AWS OpenSearch configurator"""
    from playwright.sync_api import sync_playwright
    
    # Test configuration with dynamic options
    test_config = {
        'description': 'Dynamic AWS OpenSearch test configuration',
        'deployment_type': 'Production',  # Try to select production deployment
        'instance_type': 'r5.large',      # Try to select instance type
        'number_of_nodes': 3,
        'number_of_instances': 3,
        'storage_size_gb': 500,
        'data_transfer_tb': 50,
        'search_requests': 100000,
        'indexing_requests': 50000,
        'indexing_ocus': 2,
        'search_ocus': 2,
        'index_data_size_gb': 100
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = DynamicAWSOpenSearchConfigurator(page)
        
        if configurator.navigate_to_aws_opensearch_config():
            # Explore all options first
            print(f"\n[INFO] Exploring all radio button options...")
            all_options = configurator.explore_all_radio_options()
            
            # Apply configuration
            if configurator.apply_dynamic_aws_opensearch_configuration(test_config):
                print(f"\n[SUCCESS] Dynamic configuration applied successfully!")
                
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS OpenSearch configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("dynamic_aws_opensearch_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to dynamic_aws_opensearch_estimate_url.txt")
            else:
                print(f"[ERROR] Failed to apply dynamic configuration")
        else:
            print(f"[ERROR] Failed to navigate to AWS OpenSearch configuration")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
