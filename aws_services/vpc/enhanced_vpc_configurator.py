"""
Enhanced VPC Configuration Class
Handles ALL interactive elements including radios, inputs, dropdowns, and dynamic options
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class EnhancedVPCConfigurator(BaseAWSConfigurator):
    """Enhanced VPC configuration class with full element interaction capabilities"""
    
    def __init__(self, page: Page):
        super().__init__(page, "VPC")
    
    def navigate_to_vpc_config(self) -> bool:
        """Navigate to VPC configuration page"""
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
    
    def discover_all_radio_buttons(self) -> List[Dict]:
        """Discover all radio buttons and their options"""
        print(f"\n[INFO] Discovering all radio button options...")
        
        radio_buttons = []
        
        # Find all radio button groups
        radio_groups = self.page.query_selector_all("input[type='radio']")
        print(f"[INFO] Found {len(radio_groups)} radio buttons")
        
        for i, radio in enumerate(radio_groups):
            try:
                name = radio.get_attribute("name")
                value = radio.get_attribute("value")
                checked = radio.is_checked()
                aria_label = radio.get_attribute("aria-label")
                id_attr = radio.get_attribute("id")
                
                # Find the label text
                label_text = ""
                try:
                    # Try to find associated label
                    if id_attr:
                        label = self.page.locator(f"label[for='{id_attr}']")
                        if label.count() > 0:
                            label_text = label.first.text_content().strip()
                    
                    # Try to find text near the radio button
                    if not label_text:
                        parent = radio.evaluate("el => el.closest('div, span, label')")
                        if parent:
                            label_text = parent.text_content().strip()
                except:
                    pass
                
                radio_info = {
                    "index": i,
                    "name": name,
                    "value": value,
                    "checked": checked,
                    "aria_label": aria_label,
                    "id": id_attr,
                    "label_text": label_text
                }
                
                radio_buttons.append(radio_info)
                print(f"[INFO] Radio {i}: {name} = {value} (checked: {checked}) - {label_text}")
                
            except Exception as e:
                print(f"[WARNING] Could not process radio button {i}: {e}")
        
        return radio_buttons
    
    def click_radio_button_by_value(self, value: str) -> bool:
        """Click radio button by value"""
        try:
            radio = self.page.locator(f"input[type='radio'][value='{value}']")
            if radio.count() > 0:
                radio.first.click()
                self.page.wait_for_timeout(1000)  # Wait for UI to update
                print(f"[OK] Selected radio button: {value}")
                return True
            else:
                print(f"[WARNING] Could not find radio button with value: {value}")
                return False
        except Exception as e:
            print(f"[ERROR] Could not click radio button: {e}")
            return False
    
    def click_radio_button_by_text(self, text: str) -> bool:
        """Click radio button by label text"""
        try:
            # Try to find radio button by associated label text
            radio = self.page.locator(f"input[type='radio']").filter(has_text=text)
            if radio.count() > 0:
                radio.first.click()
                self.page.wait_for_timeout(1000)
                print(f"[OK] Selected radio button: {text}")
                return True
            else:
                print(f"[WARNING] Could not find radio button with text: {text}")
                return False
        except Exception as e:
            print(f"[ERROR] Could not click radio button by text: {e}")
            return False
    
    def discover_all_dropdowns(self) -> List[Dict]:
        """Discover all dropdown/select elements"""
        print(f"\n[INFO] Discovering all dropdown options...")
        
        dropdowns = []
        
        # Find all select elements
        select_elements = self.page.query_selector_all("select")
        print(f"[INFO] Found {len(select_elements)} select dropdowns")
        
        for i, select in enumerate(select_elements):
            try:
                name = select.get_attribute("name")
                id_attr = select.get_attribute("id")
                aria_label = select.get_attribute("aria-label")
                
                # Get all options
                options = []
                option_elements = select.query_selector_all("option")
                for option in option_elements:
                    option_text = option.inner_text().strip()
                    option_value = option.get_attribute("value") or ""
                    if option_text:
                        options.append({
                            'text': option_text,
                            'value': option_value
                        })
                
                dropdown_info = {
                    "index": i,
                    "name": name,
                    "id": id_attr,
                    "aria_label": aria_label,
                    "options": options
                }
                
                dropdowns.append(dropdown_info)
                print(f"[INFO] Dropdown {i}: {name} ({len(options)} options)")
                
            except Exception as e:
                print(f"[WARNING] Could not process dropdown {i}: {e}")
        
        return dropdowns
    
    def select_dropdown_option(self, dropdown_name: str, option_value: str) -> bool:
        """Select option from dropdown by name and value"""
        try:
            select = self.page.locator(f"select[name='{dropdown_name}']")
            if select.count() > 0:
                select.first.select_option(value=option_value)
                self.page.wait_for_timeout(1000)
                print(f"[OK] Selected dropdown {dropdown_name}: {option_value}")
                return True
            else:
                print(f"[WARNING] Could not find dropdown: {dropdown_name}")
                return False
        except Exception as e:
            print(f"[ERROR] Could not select dropdown option: {e}")
            return False
    
    def discover_all_input_fields(self) -> List[Dict]:
        """Discover all input fields"""
        print(f"\n[INFO] Discovering all input fields...")
        
        input_fields = []
        
        # Find all input fields
        inputs = self.page.query_selector_all("input[type='text'], input[type='number'], input[type='email']")
        print(f"[INFO] Found {len(inputs)} input fields")
        
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
    
    def fill_input_field(self, field_identifier: str, value: str) -> bool:
        """Fill input field by identifier (aria-label, name, or id)"""
        try:
            # Try different selector strategies
            selectors = [
                f"input[aria-label*='{field_identifier}']",
                f"input[name='{field_identifier}']",
                f"input[id='{field_identifier}']",
                f"input[placeholder*='{field_identifier}']"
            ]
            
            for selector in selectors:
                field = self.page.locator(selector)
                if field.count() > 0:
                    field.first.fill(str(value))
                    print(f"[OK] Filled {field_identifier}: {value}")
                    return True
            
            print(f"[WARNING] Could not find input field: {field_identifier}")
            return False
        except Exception as e:
            print(f"[ERROR] Could not fill input field: {e}")
            return False
    
    def discover_all_checkboxes(self) -> List[Dict]:
        """Discover all checkbox elements"""
        print(f"\n[INFO] Discovering all checkboxes...")
        
        checkboxes = []
        
        # Find all checkboxes
        checkbox_elements = self.page.query_selector_all("input[type='checkbox']")
        print(f"[INFO] Found {len(checkbox_elements)} checkboxes")
        
        for i, checkbox in enumerate(checkbox_elements):
            try:
                name = checkbox.get_attribute("name")
                id_attr = checkbox.get_attribute("id")
                aria_label = checkbox.get_attribute("aria-label")
                checked = checkbox.is_checked()
                
                # Find label text
                label_text = ""
                try:
                    if id_attr:
                        label = self.page.locator(f"label[for='{id_attr}']")
                        if label.count() > 0:
                            label_text = label.first.text_content().strip()
                except:
                    pass
                
                checkbox_info = {
                    "index": i,
                    "name": name,
                    "id": id_attr,
                    "aria_label": aria_label,
                    "checked": checked,
                    "label_text": label_text
                }
                
                checkboxes.append(checkbox_info)
                print(f"[INFO] Checkbox {i}: {name} (checked: {checked}) - {label_text}")
                
            except Exception as e:
                print(f"[WARNING] Could not process checkbox {i}: {e}")
        
        return checkboxes
    
    def toggle_checkbox(self, checkbox_identifier: str, checked: bool = True) -> bool:
        """Toggle checkbox by identifier"""
        try:
            # Try different selector strategies
            selectors = [
                f"input[type='checkbox'][aria-label*='{checkbox_identifier}']",
                f"input[type='checkbox'][name='{checkbox_identifier}']",
                f"input[type='checkbox'][id='{checkbox_identifier}']"
            ]
            
            for selector in selectors:
                checkbox = self.page.locator(selector)
                if checkbox.count() > 0:
                    if checked and not checkbox.first.is_checked():
                        checkbox.first.check()
                        print(f"[OK] Checked {checkbox_identifier}")
                        return True
                    elif not checked and checkbox.first.is_checked():
                        checkbox.first.uncheck()
                        print(f"[OK] Unchecked {checkbox_identifier}")
                        return True
                    else:
                        print(f"[OK] Checkbox {checkbox_identifier} already in desired state")
                        return True
            
            print(f"[WARNING] Could not find checkbox: {checkbox_identifier}")
            return False
        except Exception as e:
            print(f"[ERROR] Could not toggle checkbox: {e}")
            return False
    
    def apply_comprehensive_vpc_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply comprehensive VPC configuration with full element interaction"""
        try:
            print(f"\n[INFO] Applying comprehensive VPC configuration...")
            
            # First, discover all available elements
            print(f"\n[INFO] Discovering all interactive elements...")
            radio_buttons = self.discover_all_radio_buttons()
            dropdowns = self.discover_all_dropdowns()
            input_fields = self.discover_all_input_fields()
            checkboxes = self.discover_all_checkboxes()
            
            settings_applied = 0
            
            # Set description
            if 'description' in config:
                if self.fill_input_field("Description", config['description']):
                    settings_applied += 1
            
            # Handle radio button selections
            radio_settings = [
                'vpc_type', 'deployment_model', 'connectivity_type', 
                'dns_resolution', 'dns_hostnames', 'classic_link'
            ]
            
            for setting in radio_settings:
                if setting in config:
                    if self.click_radio_button_by_text(config[setting]):
                        settings_applied += 1
            
            # Handle dropdown selections
            dropdown_settings = [
                'region', 'availability_zone', 'instance_type', 
                'storage_type', 'monitoring_level'
            ]
            
            for setting in dropdown_settings:
                if setting in config:
                    if self.select_dropdown_option(setting, config[setting]):
                        settings_applied += 1
            
            # Handle input field values
            input_settings = [
                'number_of_vpcs', 'number_of_subnets', 'number_of_internet_gateways',
                'number_of_nat_gateways', 'number_of_vpc_endpoints', 'number_of_route_tables',
                'number_of_security_groups', 'number_of_network_acls', 'data_processed_gb',
                'endpoint_hours', 'nat_gateway_hours', 'vpc_peering_hours',
                'transit_gateway_hours', 'vpn_connection_hours', 'vpn_tunnel_hours',
                'data_transfer_gb', 'availability_zones', 'cidr_block'
            ]
            
            for setting in input_settings:
                if setting in config:
                    if self.fill_input_field(setting, config[setting]):
                        settings_applied += 1
            
            # Handle checkbox toggles
            checkbox_settings = [
                'enable_dns_hostnames', 'enable_dns_resolution', 'enable_classic_link',
                'enable_vpc_flow_logs', 'enable_vpc_endpoints', 'enable_nat_gateway',
                'enable_internet_gateway', 'enable_vpn_connection'
            ]
            
            for setting in checkbox_settings:
                if setting in config:
                    if self.toggle_checkbox(setting, config[setting]):
                        settings_applied += 1
            
            print(f"[OK] Applied {settings_applied} VPC settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply comprehensive VPC configuration: {e}")
            return False
    
    def explore_all_vpc_options(self) -> Dict[str, Any]:
        """Explore all available VPC configuration options"""
        print(f"\n[INFO] Exploring all VPC configuration options...")
        
        # Discover all elements
        radio_buttons = self.discover_all_radio_buttons()
        dropdowns = self.discover_all_dropdowns()
        input_fields = self.discover_all_input_fields()
        checkboxes = self.discover_all_checkboxes()
        
        # Create comprehensive options map
        options_map = {
            "radio_buttons": radio_buttons,
            "dropdowns": dropdowns,
            "input_fields": input_fields,
            "checkboxes": checkboxes,
            "total_elements": len(radio_buttons) + len(dropdowns) + len(input_fields) + len(checkboxes)
        }
        
        print(f"\n[INFO] VPC Configuration Options Summary:")
        print(f"  - Radio Buttons: {len(radio_buttons)}")
        print(f"  - Dropdowns: {len(dropdowns)}")
        print(f"  - Input Fields: {len(input_fields)}")
        print(f"  - Checkboxes: {len(checkboxes)}")
        print(f"  - Total Elements: {options_map['total_elements']}")
        
        return options_map

def main():
    """Test the enhanced VPC configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Explore all available options
            options = configurator.explore_all_vpc_options()
            
            # Example comprehensive configuration
            example_config = {
                'description': 'Enhanced VPC for production web application',
                'vpc_type': 'Production',
                'deployment_model': 'Multi-AZ',
                'connectivity_type': 'Internet Gateway',
                'region': 'us-east-1',
                'availability_zone': 'us-east-1a',
                'number_of_vpcs': 2,
                'number_of_subnets': 6,
                'number_of_internet_gateways': 2,
                'number_of_nat_gateways': 3,
                'number_of_vpc_endpoints': 4,
                'number_of_route_tables': 6,
                'number_of_security_groups': 8,
                'number_of_network_acls': 2,
                'data_processed_gb': 1000,
                'endpoint_hours': 744,
                'nat_gateway_hours': 1488,
                'vpc_peering_hours': 744,
                'transit_gateway_hours': 744,
                'vpn_connection_hours': 0,
                'vpn_tunnel_hours': 0,
                'data_transfer_gb': 500,
                'availability_zones': 3,
                'cidr_block': '10.0.0.0/16',
                'enable_dns_hostnames': True,
                'enable_dns_resolution': True,
                'enable_vpc_flow_logs': True,
                'enable_vpc_endpoints': True,
                'enable_nat_gateway': True,
                'enable_internet_gateway': True,
                'enable_vpn_connection': False
            }
            
            # Apply comprehensive configuration
            if configurator.apply_comprehensive_vpc_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] Enhanced VPC configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("enhanced_vpc_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to enhanced_vpc_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
