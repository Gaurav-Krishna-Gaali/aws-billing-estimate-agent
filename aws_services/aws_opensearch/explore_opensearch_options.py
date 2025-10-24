"""
Explore AWS OpenSearch Options
Systematically explore all radio button options and their effects
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class OpenSearchExplorer(BaseAWSConfigurator):
    """Explorer for AWS OpenSearch dynamic options"""
    
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
    
    def map_all_radio_buttons(self) -> Dict:
        """Map all radio buttons with their details"""
        print(f"\n[INFO] Mapping all radio buttons...")
        
        radio_buttons = {}
        
        # Find all radio buttons
        radios = self.page.query_selector_all("input[type='radio']")
        print(f"[INFO] Found {len(radios)} radio buttons")
        
        for i, radio in enumerate(radios):
            try:
                name = radio.get_attribute("name")
                value = radio.get_attribute("value")
                checked = radio.is_checked()
                aria_label = radio.get_attribute("aria-label")
                id_attr = radio.get_attribute("id")
                
                # Try to find the label text
                label_text = ""
                try:
                    # Look for label element
                    label = self.page.locator(f"label[for='{id_attr}']")
                    if label.count() > 0:
                        label_text = label.first.text_content().strip()
                    else:
                        # Try to find text near the radio button
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
                
                radio_buttons[f"radio_{i}"] = radio_info
                
                print(f"[INFO] Radio {i}: {name} = {value}")
                print(f"  - Label: {label_text}")
                print(f"  - Aria Label: {aria_label}")
                print(f"  - Checked: {checked}")
                print(f"  - ID: {id_attr}")
                
            except Exception as e:
                print(f"[WARNING] Could not process radio button {i}: {e}")
        
        return radio_buttons
    
    def map_all_input_fields(self) -> Dict:
        """Map all input fields with their details"""
        print(f"\n[INFO] Mapping all input fields...")
        
        input_fields = {}
        
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
                
                input_fields[f"input_{i}"] = field_info
                
                status = "Visible" if is_visible else "Hidden"
                print(f"[INFO] Input {i}: {aria_label or placeholder or name} ({field_type}) - {status}")
                
            except Exception as e:
                print(f"[WARNING] Could not process input field {i}: {e}")
        
        return input_fields
    
    def test_radio_button_click(self, radio_info: Dict) -> Dict:
        """Test clicking a radio button and see what changes"""
        try:
            name = radio_info.get("name")
            value = radio_info.get("value")
            label = radio_info.get("label_text", "")
            
            print(f"\n[INFO] Testing radio button: {name} = {value} ({label})")
            
            # Click the radio button
            radio = self.page.locator(f"input[type='radio'][name='{name}'][value='{value}']")
            if radio.count() > 0:
                radio.first.click()
                self.page.wait_for_timeout(2000)  # Wait for UI to update
                print(f"[OK] Clicked radio button: {label}")
                
                # Map input fields after clicking
                input_fields = self.map_all_input_fields()
                visible_fields = {k: v for k, v in input_fields.items() if v.get("visible", False)}
                
                return {
                    "radio_clicked": True,
                    "input_fields_before": len(input_fields),
                    "input_fields_after": len(visible_fields),
                    "visible_fields": visible_fields
                }
            else:
                print(f"[WARNING] Could not find radio button: {name} = {value}")
                return {"radio_clicked": False}
                
        except Exception as e:
            print(f"[ERROR] Could not test radio button: {e}")
            return {"radio_clicked": False, "error": str(e)}
    
    def explore_all_combinations(self) -> Dict:
        """Explore all possible radio button combinations"""
        print(f"\n[INFO] Exploring all radio button combinations...")
        
        # First, map all radio buttons
        radio_buttons = self.map_all_radio_buttons()
        
        # Group by name
        radio_groups = {}
        for radio_id, radio_info in radio_buttons.items():
            name = radio_info.get("name")
            if name not in radio_groups:
                radio_groups[name] = []
            radio_groups[name].append(radio_info)
        
        print(f"[INFO] Found {len(radio_groups)} radio button groups")
        
        exploration_results = {}
        
        # Explore each group
        for group_name, radios in radio_groups.items():
            print(f"\n[INFO] Exploring group: {group_name}")
            group_results = []
            
            for radio in radios:
                result = self.test_radio_button_click(radio)
                group_results.append({
                    "radio": radio,
                    "result": result
                })
            
            exploration_results[group_name] = group_results
        
        return exploration_results
    
    def save_exploration_results(self, results: Dict, filename: str = "opensearch_exploration_results.json"):
        """Save exploration results to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"[SAVE] Exploration results saved to {filename}")
        except Exception as e:
            print(f"[ERROR] Could not save results: {e}")

def main():
    """Main exploration function"""
    print("[INFO] AWS OpenSearch Options Explorer")
    print("[INFO] Systematically exploring all radio button options and their effects")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        explorer = OpenSearchExplorer(page)
        
        if explorer.navigate_to_aws_opensearch_config():
            print(f"\n[INFO] Successfully navigated to AWS OpenSearch configuration page")
            
            # Map initial state
            print(f"\n[INFO] Mapping initial state...")
            initial_radios = explorer.map_all_radio_buttons()
            initial_inputs = explorer.map_all_input_fields()
            
            # Explore all combinations
            exploration_results = explorer.explore_all_combinations()
            
            # Save results
            explorer.save_exploration_results(exploration_results)
            
            print(f"\n[SUCCESS] Exploration completed!")
            print(f"[INFO] Found {len(initial_radios)} radio buttons")
            print(f"[INFO] Found {len(initial_inputs)} input fields")
            
        else:
            print("[ERROR] Failed to navigate to AWS OpenSearch configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
