"""
Base AWS Service Configurator
Common functionality for all AWS service configurators
"""

from playwright.sync_api import Page, TimeoutError as PWTimeout
from typing import Dict, Any, List, Optional
import time
import json


class BaseAWSConfigurator:
    """Base class for AWS service configuration with common helper methods"""
    
    def __init__(self, page: Page, service_name: str):
        self.page = page
        self.service_name = service_name
        self.configuration_data = {}
    
    def navigate_to_calculator(self) -> bool:
        """Navigate to AWS Calculator and create estimate"""
        try:
            print(f"[INFO] Navigating to AWS Calculator...")
            self.page.goto("https://calculator.aws/#/")
            
            # Create estimate
            self.page.wait_for_selector("text='Create estimate'")
            self.page.click("text='Create estimate'")
            
            print(f"[OK] Successfully navigated to AWS Calculator")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to calculator: {e}")
            return False
    
    def search_and_select_service(self, search_term: str) -> bool:
        """Search for and select a service"""
        try:
            print(f"[INFO] Searching for {search_term}...")
            
            # Wait for search input
            self.page.wait_for_selector("input[placeholder='Search for a service']")
            self.page.fill("input[placeholder='Search for a service']", search_term)
            
            # Wait for service to appear and click configure
            self.page.wait_for_selector(f"text='{search_term}'")
            self.page.click(f"button[aria-label='Configure {search_term}']")
            
            # Wait for configuration page to load
            self.page.wait_for_timeout(3000)
            print(f"[OK] Successfully navigated to {search_term} configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to search and select {search_term}: {e}")
            return False
    
    def map_all_elements(self) -> Dict[str, Any]:
        """Map all interactive elements on the configuration page"""
        print(f"[INFO] Mapping all interactive elements for {self.service_name}...")
        
        elements = {
            'buttons': self._map_buttons(),
            'inputs': self._map_inputs(),
            'selects': self._map_selects(),
            'checkboxes': self._map_checkboxes(),
            'radio_buttons': self._map_radio_buttons(),
            'text_areas': self._map_text_areas()
        }
        
        total_elements = sum(len(v) for v in elements.values())
        print(f"[OK] Mapped {total_elements} interactive elements")
        return elements
    
    def _map_buttons(self) -> Dict[str, str]:
        """Map all buttons on the page"""
        buttons = {}
        try:
            button_elements = self.page.query_selector_all("button")
            for i, button in enumerate(button_elements):
                try:
                    text = button.inner_text().strip()
                    if text:
                        aria_label = button.get_attribute("aria-label") or ""
                        data_cy = button.get_attribute("data-cy") or ""
                        button_type = button.get_attribute("type") or ""
                        
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
                    input_type = input_elem.get_attribute("type") or "text"
                    placeholder = input_elem.get_attribute("placeholder") or ""
                    name = input_elem.get_attribute("name") or ""
                    id_attr = input_elem.get_attribute("id") or ""
                    aria_label = input_elem.get_attribute("aria-label") or ""
                    
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
    
    def save_element_map(self, filename: str = None) -> Dict[str, Any]:
        """Save the element map to a JSON file"""
        if filename is None:
            filename = f"{self.service_name.lower()}_elements_map.json"
        
        elements = self.map_all_elements()
        
        with open(filename, 'w') as f:
            json.dump(elements, f, indent=2)
        
        print(f"[OK] Element map saved to {filename}")
        return elements
    
    def print_element_summary(self):
        """Print a summary of all mapped elements"""
        elements = self.map_all_elements()
        
        print(f"\n{'='*60}")
        print(f"{self.service_name.upper()} CONFIGURATION PAGE ELEMENT MAP")
        print(f"{'='*60}")
        
        for element_type, element_dict in elements.items():
            print(f"\n{element_type.upper()} ({len(element_dict)} found):")
            print("-" * 40)
            
            for identifier, details in element_dict.items():
                print(f"  {identifier}:")
                for key, value in details.items():
                    if key != 'selector':  # Don't show selectors in summary
                        print(f"    {key}: {value}")
                print()
    
    def save_and_exit(self) -> str:
        """Save the configuration and return the estimate URL"""
        try:
            print(f"[INFO] Saving {self.service_name} configuration...")
            
            # Wait for save button and click it using JavaScript (proven method)
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
    
    def take_screenshot(self, filename: str = None) -> bool:
        """Take a screenshot of the current page"""
        if filename is None:
            filename = f"{self.service_name.lower()}_config_screenshot.png"
        
        try:
            self.page.screenshot(path=filename, full_page=True)
            print(f"[SCREENSHOT] Screenshot saved as {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to take screenshot: {e}")
            return False

