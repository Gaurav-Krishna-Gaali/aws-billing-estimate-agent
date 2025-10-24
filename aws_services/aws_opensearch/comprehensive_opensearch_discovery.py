"""
Comprehensive AWS OpenSearch Discovery
Discover ALL interactive elements including dynamic ones
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveOpenSearchDiscovery(BaseAWSConfigurator):
    """Comprehensive discovery for AWS OpenSearch elements"""
    
    def __init__(self, page):
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
    
    def discover_all_elements_comprehensive(self) -> Dict:
        """Discover ALL interactive elements comprehensively"""
        print(f"\n[INFO] Comprehensive element discovery...")
        
        all_elements = {
            "buttons": {},
            "inputs": {},
            "selects": {},
            "checkboxes": {},
            "radio_buttons": {},
            "text_areas": {},
            "links": {},
            "divs": {},
            "spans": {}
        }
        
        # Discover buttons
        print(f"[INFO] Discovering buttons...")
        buttons = self.page.query_selector_all("button")
        for i, button in enumerate(buttons):
            try:
                text = button.text_content()
                aria_label = button.get_attribute("aria-label")
                button_type = button.get_attribute("type")
                class_name = button.get_attribute("class")
                
                all_elements["buttons"][f"button_{i}"] = {
                    "text": text,
                    "aria_label": aria_label,
                    "type": button_type,
                    "class": class_name,
                    "visible": button.is_visible()
                }
                
                if button.is_visible():
                    print(f"[INFO] Button {i}: {text} ({aria_label}) - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process button {i}: {e}")
        
        # Discover inputs
        print(f"[INFO] Discovering inputs...")
        inputs = self.page.query_selector_all("input")
        for i, input_field in enumerate(inputs):
            try:
                field_type = input_field.get_attribute("type")
                aria_label = input_field.get_attribute("aria-label")
                placeholder = input_field.get_attribute("placeholder")
                name = input_field.get_attribute("name")
                value = input_field.get_attribute("value")
                checked = input_field.get_attribute("checked")
                
                all_elements["inputs"][f"input_{i}"] = {
                    "type": field_type,
                    "aria_label": aria_label,
                    "placeholder": placeholder,
                    "name": name,
                    "value": value,
                    "checked": checked,
                    "visible": input_field.is_visible()
                }
                
                if input_field.is_visible():
                    print(f"[INFO] Input {i}: {aria_label or placeholder} ({field_type}) - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process input {i}: {e}")
        
        # Discover selects
        print(f"[INFO] Discovering selects...")
        selects = self.page.query_selector_all("select")
        for i, select in enumerate(selects):
            try:
                aria_label = select.get_attribute("aria-label")
                name = select.get_attribute("name")
                
                # Get options
                options = []
                option_elements = select.query_selector_all("option")
                for j, option in enumerate(option_elements):
                    try:
                        option_text = option.text_content()
                        option_value = option.get_attribute("value")
                        options.append({
                            "text": option_text,
                            "value": option_value
                        })
                    except:
                        pass
                
                all_elements["selects"][f"select_{i}"] = {
                    "aria_label": aria_label,
                    "name": name,
                    "options": options,
                    "visible": select.is_visible()
                }
                
                if select.is_visible():
                    print(f"[INFO] Select {i}: {aria_label} ({len(options)} options) - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process select {i}: {e}")
        
        # Discover checkboxes
        print(f"[INFO] Discovering checkboxes...")
        checkboxes = self.page.query_selector_all("input[type='checkbox']")
        for i, checkbox in enumerate(checkboxes):
            try:
                aria_label = checkbox.get_attribute("aria-label")
                name = checkbox.get_attribute("name")
                checked = checkbox.is_checked()
                
                all_elements["checkboxes"][f"checkbox_{i}"] = {
                    "aria_label": aria_label,
                    "name": name,
                    "checked": checked,
                    "visible": checkbox.is_visible()
                }
                
                if checkbox.is_visible():
                    print(f"[INFO] Checkbox {i}: {aria_label} (checked: {checked}) - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process checkbox {i}: {e}")
        
        # Discover radio buttons
        print(f"[INFO] Discovering radio buttons...")
        radios = self.page.query_selector_all("input[type='radio']")
        for i, radio in enumerate(radios):
            try:
                aria_label = radio.get_attribute("aria-label")
                name = radio.get_attribute("name")
                value = radio.get_attribute("value")
                checked = radio.is_checked()
                
                all_elements["radio_buttons"][f"radio_{i}"] = {
                    "aria_label": aria_label,
                    "name": name,
                    "value": value,
                    "checked": checked,
                    "visible": radio.is_visible()
                }
                
                if radio.is_visible():
                    print(f"[INFO] Radio {i}: {name} = {value} ({aria_label}) - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process radio {i}: {e}")
        
        # Discover text areas
        print(f"[INFO] Discovering text areas...")
        text_areas = self.page.query_selector_all("textarea")
        for i, textarea in enumerate(text_areas):
            try:
                aria_label = textarea.get_attribute("aria-label")
                placeholder = textarea.get_attribute("placeholder")
                name = textarea.get_attribute("name")
                
                all_elements["text_areas"][f"textarea_{i}"] = {
                    "aria_label": aria_label,
                    "placeholder": placeholder,
                    "name": name,
                    "visible": textarea.is_visible()
                }
                
                if textarea.is_visible():
                    print(f"[INFO] TextArea {i}: {aria_label or placeholder} - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process textarea {i}: {e}")
        
        # Discover clickable divs and spans
        print(f"[INFO] Discovering clickable divs and spans...")
        clickable_divs = self.page.query_selector_all("div[role='button'], div[onclick], span[role='button'], span[onclick]")
        for i, element in enumerate(clickable_divs):
            try:
                text = element.text_content()
                role = element.get_attribute("role")
                onclick = element.get_attribute("onclick")
                class_name = element.get_attribute("class")
                
                all_elements["divs"][f"div_{i}"] = {
                    "text": text,
                    "role": role,
                    "onclick": onclick,
                    "class": class_name,
                    "visible": element.is_visible()
                }
                
                if element.is_visible():
                    print(f"[INFO] Clickable Div {i}: {text} ({role}) - Visible")
                
            except Exception as e:
                print(f"[WARNING] Could not process clickable div {i}: {e}")
        
        return all_elements
    
    def wait_and_discover_dynamic_elements(self, wait_time: int = 5) -> Dict:
        """Wait for dynamic elements to load and discover them"""
        print(f"\n[INFO] Waiting {wait_time} seconds for dynamic elements to load...")
        self.page.wait_for_timeout(wait_time * 1000)
        
        return self.discover_all_elements_comprehensive()
    
    def save_discovery_results(self, results: Dict, filename: str = "opensearch_comprehensive_discovery.json"):
        """Save discovery results to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"[SAVE] Discovery results saved to {filename}")
        except Exception as e:
            print(f"[ERROR] Could not save results: {e}")

def main():
    """Main discovery function"""
    print("[INFO] Comprehensive AWS OpenSearch Discovery")
    print("[INFO] Discovering ALL interactive elements including dynamic ones")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        discovery = ComprehensiveOpenSearchDiscovery(page)
        
        if discovery.navigate_to_aws_opensearch_config():
            print(f"\n[INFO] Successfully navigated to AWS OpenSearch configuration page")
            
            # Initial discovery
            print(f"\n[INFO] Initial element discovery...")
            initial_elements = discovery.discover_all_elements_comprehensive()
            
            # Wait for dynamic elements
            print(f"\n[INFO] Waiting for dynamic elements...")
            dynamic_elements = discovery.wait_and_discover_dynamic_elements(5)
            
            # Save results
            discovery.save_discovery_results(dynamic_elements)
            
            # Print summary
            total_elements = sum(len(v) for v in dynamic_elements.values())
            visible_elements = sum(len([e for e in elements.values() if e.get("visible", False)]) 
                                 for elements in dynamic_elements.values())
            
            print(f"\n[SUCCESS] Discovery completed!")
            print(f"[INFO] Total elements found: {total_elements}")
            print(f"[INFO] Visible elements: {visible_elements}")
            
            for element_type, elements in dynamic_elements.items():
                visible_count = len([e for e in elements.values() if e.get("visible", False)])
                print(f"[INFO] {element_type}: {len(elements)} total, {visible_count} visible")
            
        else:
            print("[ERROR] Failed to navigate to AWS OpenSearch configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
