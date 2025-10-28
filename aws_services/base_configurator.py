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
    
    def __init__(self, page: Page, service_name: str = None):
        self.page = page
        self.service_name = service_name or "aws_service"
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
            self.page.wait_for_timeout(2000)  # Wait for search results
            
            # Wait for the configure button to appear and click it
            # This is better than waiting for text because the button is what we need to click
            configure_button_selector = f"button[aria-label*='{search_term}']"
            self.page.wait_for_selector(configure_button_selector, timeout=10000)
            self.page.click(configure_button_selector)
            
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
            
            # Scroll to bottom to ensure footer is visible
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(1000)
            
            # Wait for the footer to appear
            self.page.wait_for_selector(".appFooter", timeout=5000)
            
            # Use the working selector: .appFooter button[data-cy='Save and add service-button']
            self.page.click(".appFooter button[data-cy='Save and add service-button']")
            
            # Wait for page to process
            self.page.wait_for_timeout(3000)
            
            # Get the estimate URL
            current_url = self.page.url
            print(f"[OK] Configuration saved. URL: {current_url}")
            
            return current_url
            
        except Exception as e:
            print(f"[ERROR] Failed to save configuration: {e}")
            return ""
    
    def navigate_to_service_config(self) -> bool:
        """
        Navigate to service configuration page (for multi-service estimates)
        This method should be overridden by each service configurator
        """
        try:
            print(f"[INFO] Navigating to {self.service_name} configuration...")
            
            # Search for the service
            search_terms = self._get_service_search_terms()
            for term in search_terms:
                if self.search_and_select_service(term):
                    return True
            
            print(f"[ERROR] Could not find {self.service_name} service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to {self.service_name} configuration: {e}")
            return False
    
    def apply_configuration(self, config: Dict[str, Any], add_to_estimate: bool = False) -> bool:
        """
        Apply service configuration
        
        Args:
            config: Service configuration dictionary
            add_to_estimate: If True, add to existing estimate instead of creating new one
            
        Returns:
            bool: True if configuration was applied successfully
        """
        try:
            print(f"[INFO] Applying {self.service_name} configuration...")
            
            # Apply the specific service configuration
            if not self._apply_service_specific_config(config):
                print(f"[ERROR] Failed to apply {self.service_name} specific configuration")
                return False
            
            if add_to_estimate:
                # Add to existing estimate
                return self._add_to_estimate()
            else:
                # Original behavior: save and exit
                return self.save_and_exit() is not None
                
        except Exception as e:
            print(f"[ERROR] Failed to apply {self.service_name} configuration: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """
        Get search terms for finding this service in AWS Calculator
        Should be overridden by each service configurator
        """
        return [self.service_name]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """
        Apply service-specific configuration logic
        Should be overridden by each service configurator
        
        Args:
            config: Service configuration dictionary
            
        Returns:
            bool: True if configuration was applied successfully
        """
        # Default implementation - should be overridden
        print(f"[WARNING] {self.service_name} configurator does not implement _apply_service_specific_config")
        return True
    
    def _add_to_estimate(self) -> bool:
        """
        Add current service configuration to existing estimate
        
        Returns:
            bool: True if service was added successfully
        """
        try:
            print(f"[INFO] Adding {self.service_name} to estimate...")
            
            # Scroll to bottom to ensure footer is visible
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(1000)
            
            # Wait for the footer to appear
            self.page.wait_for_selector(".appFooter", timeout=5000)
            
            # Use the working selector from b.py: .appFooter button[data-cy='Save and add service-button']
            self.page.click(".appFooter button[data-cy='Save and add service-button']")
            
            print(f"[SUCCESS] Clicked 'Save and add service' for {self.service_name}")
            
            # Wait for service to be added
            self.page.wait_for_timeout(3000)
            
            # Success - the button click should navigate back to the estimate page
            print(f"[SUCCESS] {self.service_name} added to estimate")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to add {self.service_name} to estimate: {e}")
            import traceback
            traceback.print_exc()
            return False

