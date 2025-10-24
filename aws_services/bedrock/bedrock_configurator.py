"""
AWS Bedrock Configuration Class
Maps all interactive elements on the Bedrock configuration page
"""

from playwright.sync_api import Page, TimeoutError as PWTimeout
from typing import Dict, Any, List, Optional
import time


class BedrockConfigurator:
    """Comprehensive Bedrock configuration class with all page elements mapped"""
    
    def __init__(self, page: Page):
        self.page = page
        self.configuration_data = {}
    
    def navigate_to_bedrock_config(self) -> bool:
        """Navigate to Bedrock configuration page"""
        try:
            print("[INFO] Navigating to AWS Calculator...")
            self.page.goto("https://calculator.aws/#/")
            
            # Create estimate
            self.page.wait_for_selector("text='Create estimate'")
            self.page.click("text='Create estimate'")
            
            # Search for Bedrock
            self.page.wait_for_selector("input[placeholder='Search for a service']")
            self.page.fill("input[placeholder='Search for a service']", "bedrock")
            
            # Select Bedrock
            self.page.wait_for_selector("text='Amazon Bedrock'")
            self.page.click("button[aria-label='Configure Amazon Bedrock']")
            
            # Wait for configuration page to load
            self.page.wait_for_timeout(3000)
            print("[OK] Successfully navigated to Bedrock configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to Bedrock config: {e}")
            return False
    
    def map_all_elements(self) -> Dict[str, Any]:
        """Map all interactive elements on the Bedrock configuration page"""
        print("[INFO] Mapping all interactive elements...")
        
        elements = {
            'buttons': self._map_buttons(),
            'inputs': self._map_inputs(),
            'selects': self._map_selects(),
            'checkboxes': self._map_checkboxes(),
            'radio_buttons': self._map_radio_buttons(),
            'text_areas': self._map_text_areas()
        }
        
        print(f"[OK] Mapped {sum(len(v) for v in elements.values())} interactive elements")
        return elements
    
    def _map_buttons(self) -> Dict[str, str]:
        """Map all buttons on the page"""
        buttons = {}
        try:
            button_elements = self.page.query_selector_all("button")
            for i, button in enumerate(button_elements):
                try:
                    # Get button text
                    text = button.inner_text().strip()
                    if text:
                        # Get button attributes
                        aria_label = button.get_attribute("aria-label") or ""
                        data_cy = button.get_attribute("data-cy") or ""
                        button_type = button.get_attribute("type") or ""
                        
                        # Create unique identifier
                        identifier = f"button_{i}_{text.replace(' ', '_').lower()}"
                        
                        buttons[identifier] = {
                            'text': text,
                            'aria_label': aria_label,
                            'data_cy': data_cy,
                            'type': button_type,
                            'selector': f"button:nth-of-type({i+1})"
                        }
                except:
                    continue
        except Exception as e:
            print(f"[WARNING] Error mapping buttons: {e}")
        
        return buttons
    
    def _map_inputs(self) -> Dict[str, str]:
        """Map all input fields on the page"""
        inputs = {}
        try:
            input_elements = self.page.query_selector_all("input")
            for i, input_elem in enumerate(input_elements):
                try:
                    # Get input attributes
                    input_type = input_elem.get_attribute("type") or "text"
                    placeholder = input_elem.get_attribute("placeholder") or ""
                    name = input_elem.get_attribute("name") or ""
                    id_attr = input_elem.get_attribute("id") or ""
                    aria_label = input_elem.get_attribute("aria-label") or ""
                    
                    # Create unique identifier
                    identifier = f"input_{i}_{input_type}"
                    if placeholder:
                        identifier += f"_{placeholder.replace(' ', '_').lower()}"
                    elif name:
                        identifier += f"_{name}"
                    
                    inputs[identifier] = {
                        'type': input_type,
                        'placeholder': placeholder,
                        'name': name,
                        'id': id_attr,
                        'aria_label': aria_label,
                        'selector': f"input:nth-of-type({i+1})"
                    }
                except:
                    continue
        except Exception as e:
            print(f"[WARNING] Error mapping inputs: {e}")
        
        return inputs
    
    def _map_selects(self) -> Dict[str, str]:
        """Map all select dropdowns on the page"""
        selects = {}
        try:
            select_elements = self.page.query_selector_all("select")
            for i, select in enumerate(select_elements):
                try:
                    name = select.get_attribute("name") or ""
                    id_attr = select.get_attribute("id") or ""
                    aria_label = select.get_attribute("aria-label") or ""
                    
                    # Get options
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
                    
                    identifier = f"select_{i}"
                    if name:
                        identifier += f"_{name}"
                    elif id_attr:
                        identifier += f"_{id_attr}"
                    
                    selects[identifier] = {
                        'name': name,
                        'id': id_attr,
                        'aria_label': aria_label,
                        'options': options,
                        'selector': f"select:nth-of-type({i+1})"
                    }
                except:
                    continue
        except Exception as e:
            print(f"[WARNING] Error mapping selects: {e}")
        
        return selects
    
    def _map_checkboxes(self) -> Dict[str, str]:
        """Map all checkboxes on the page"""
        checkboxes = {}
        try:
            checkbox_elements = self.page.query_selector_all("input[type='checkbox']")
            for i, checkbox in enumerate(checkbox_elements):
                try:
                    name = checkbox.get_attribute("name") or ""
                    id_attr = checkbox.get_attribute("id") or ""
                    aria_label = checkbox.get_attribute("aria-label") or ""
                    checked = checkbox.is_checked()
                    
                    identifier = f"checkbox_{i}"
                    if name:
                        identifier += f"_{name}"
                    elif id_attr:
                        identifier += f"_{id_attr}"
                    
                    checkboxes[identifier] = {
                        'name': name,
                        'id': id_attr,
                        'aria_label': aria_label,
                        'checked': checked,
                        'selector': f"input[type='checkbox']:nth-of-type({i+1})"
                    }
                except:
                    continue
        except Exception as e:
            print(f"[WARNING] Error mapping checkboxes: {e}")
        
        return checkboxes
    
    def _map_radio_buttons(self) -> Dict[str, str]:
        """Map all radio buttons on the page"""
        radios = {}
        try:
            radio_elements = self.page.query_selector_all("input[type='radio']")
            for i, radio in enumerate(radio_elements):
                try:
                    name = radio.get_attribute("name") or ""
                    id_attr = radio.get_attribute("id") or ""
                    value = radio.get_attribute("value") or ""
                    checked = radio.is_checked()
                    
                    identifier = f"radio_{i}"
                    if name:
                        identifier += f"_{name}"
                    elif id_attr:
                        identifier += f"_{id_attr}"
                    
                    radios[identifier] = {
                        'name': name,
                        'id': id_attr,
                        'value': value,
                        'checked': checked,
                        'selector': f"input[type='radio']:nth-of-type({i+1})"
                    }
                except:
                    continue
        except Exception as e:
            print(f"[WARNING] Error mapping radio buttons: {e}")
        
        return radios
    
    def _map_text_areas(self) -> Dict[str, str]:
        """Map all text areas on the page"""
        text_areas = {}
        try:
            textarea_elements = self.page.query_selector_all("textarea")
            for i, textarea in enumerate(textarea_elements):
                try:
                    name = textarea.get_attribute("name") or ""
                    id_attr = textarea.get_attribute("id") or ""
                    placeholder = textarea.get_attribute("placeholder") or ""
                    aria_label = textarea.get_attribute("aria-label") or ""
                    
                    identifier = f"textarea_{i}"
                    if name:
                        identifier += f"_{name}"
                    elif id_attr:
                        identifier += f"_{id_attr}"
                    
                    text_areas[identifier] = {
                        'name': name,
                        'id': id_attr,
                        'placeholder': placeholder,
                        'aria_label': aria_label,
                        'selector': f"textarea:nth-of-type({i+1})"
                    }
                except:
                    continue
        except Exception as e:
            print(f"[WARNING] Error mapping text areas: {e}")
        
        return text_areas
    
    def save_element_map(self, filename: str = "bedrock_elements_map.json"):
        """Save the element map to a JSON file"""
        import json
        
        elements = self.map_all_elements()
        
        with open(filename, 'w') as f:
            json.dump(elements, f, indent=2)
        
        print(f"[OK] Element map saved to {filename}")
        return elements
    
    def print_element_summary(self):
        """Print a summary of all mapped elements"""
        elements = self.map_all_elements()
        
        print("\n" + "="*60)
        print("BEDROCK CONFIGURATION PAGE ELEMENT MAP")
        print("="*60)
        
        for element_type, element_dict in elements.items():
            print(f"\n{element_type.upper()} ({len(element_dict)} found):")
            print("-" * 40)
            
            for identifier, details in element_dict.items():
                print(f"  {identifier}:")
                for key, value in details.items():
                    if key != 'selector':  # Don't show selectors in summary
                        print(f"    {key}: {value}")
                print()
    
    def configure_bedrock(self, config: Dict[str, Any]) -> bool:
        """Configure Bedrock with provided settings"""
        try:
            print("[INFO] Configuring Bedrock with provided settings...")
            
            # Map elements first
            elements = self.map_all_elements()
            
            # Configure inputs
            for input_id, input_details in elements['inputs'].items():
                if input_id in config:
                    value = config[input_id]
                    selector = input_details['selector']
                    self.page.fill(selector, str(value))
                    print(f"[OK] Set {input_id} to {value}")
            
            # Configure selects
            for select_id, select_details in elements['selects'].items():
                if select_id in config:
                    value = config[select_id]
                    selector = select_details['selector']
                    self.page.select_option(selector, label=str(value))
                    print(f"[OK] Selected {select_id} to {value}")
            
            # Configure checkboxes
            for checkbox_id, checkbox_details in elements['checkboxes'].items():
                if checkbox_id in config:
                    checked = config[checkbox_id]
                    selector = checkbox_details['selector']
                    if checked:
                        self.page.check(selector)
                    else:
                        self.page.uncheck(selector)
                    print(f"[OK] Set {checkbox_id} to {checked}")
            
            # Configure radio buttons
            for radio_id, radio_details in elements['radios'].items():
                if radio_id in config:
                    value = config[radio_id]
                    selector = radio_details['selector']
                    self.page.check(selector)
                    print(f"[OK] Selected radio {radio_id} with value {value}")
            
            print("[OK] Bedrock configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure Bedrock: {e}")
            return False
    
    def save_and_exit(self) -> str:
        """Save the configuration and return the estimate URL"""
        try:
            print("[INFO] Saving Bedrock configuration...")
            
            # Wait for save button and click it
            self.page.wait_for_selector("button[aria-label='Save and add service']", state="attached", timeout=5000)
            self.page.evaluate("document.querySelector('button[aria-label=\"Save and add service\"]').click()")
            
            # Wait for page to process
            self.page.wait_for_timeout(3000)
            
            # Get the estimate URL
            current_url = self.page.url
            print(f"[OK] Configuration saved. URL: {current_url}")
            
            return current_url
            
        except Exception as e:
            print(f"[ERROR] Failed to save configuration: {e}")
            return ""


def main():
    """Test the BedrockConfigurator class"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Create configurator
        configurator = BedrockConfigurator(page)
        
        # Navigate to Bedrock config
        if configurator.navigate_to_bedrock_config():
            # Map all elements
            configurator.print_element_summary()
            
            # Save element map
            configurator.save_element_map()
            
            # Example configuration
            example_config = {
                # Add your configuration here based on the mapped elements
                # 'input_0_text': '1000',
                # 'select_0_model': 'Claude 3',
                # 'checkbox_0_enable': True
            }
            
            # Configure Bedrock (uncomment when you have actual config)
            # configurator.configure_bedrock(example_config)
            
            # Save and get URL
            # url = configurator.save_and_exit()
            # print(f"Final URL: {url}")
        
        input("Press Enter to close browser...")
        browser.close()


if __name__ == "__main__":
    main()
