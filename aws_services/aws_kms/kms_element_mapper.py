"""
AWS KMS Element Mapper
Discovers and maps ALL interactive elements on the AWS Key Management Service configuration page
"""

import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class AWSKMSConfigurator(BaseAWSConfigurator):
    """AWS KMS configuration class"""
    
    def __init__(self, page):
        super().__init__(page, "AWS KMS")
    
    def navigate_to_aws_kms_config(self) -> bool:
        """Navigate to AWS KMS configuration page"""
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
            
            # Look for "Configure AWS Key Management Service" button directly
            try:
                kms_button = self.page.locator("button[aria-label='Configure AWS Key Management Service']")
                if kms_button.count() > 0:
                    kms_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure AWS Key Management Service' button")
                    print(f"[OK] Successfully navigated to AWS Key Management Service configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure AWS Key Management Service' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click KMS button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS KMS config: {e}")
            return False


def map_aws_kms_elements():
    """Map all AWS KMS configuration elements"""
    print("[INFO] Starting AWS KMS Element Mapping...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = AWSKMSConfigurator(page)
        
        # Navigate to AWS KMS config
        if configurator.navigate_to_aws_kms_config():
            print("[INFO] Successfully navigated to AWS Key Management Service configuration page")
            
            # Map all elements
            elements = configurator.map_all_elements()
            
            # Print detailed summary
            print_detailed_summary(elements)
            
            # Save element map
            configurator.save_element_map("kms_elements_map.json")
            
            # Take screenshot for reference
            configurator.take_screenshot("aws_kms_config_page.png")
            
            print("\n[SUCCESS] AWS KMS element mapping completed!")
            print("[INFO] Files created:")
            print("  - kms_elements_map.json (complete element mapping)")
            print("  - aws_kms_config_page.png (screenshot for reference)")
            
        else:
            print("[ERROR] Failed to navigate to AWS Key Management Service configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def print_detailed_summary(elements):
    """Print detailed summary of all mapped elements"""
    print(f"\n{'='*80}")
    print("COMPLETE AWS KMS CONFIGURATION PAGE ELEMENT MAP")
    print(f"{'='*80}")
    
    total_elements = sum(len(v) for v in elements.values())
    print(f"Total interactive elements found: {total_elements}")
    
    for element_type, element_dict in elements.items():
        print(f"\n{element_type.upper()} ({len(element_dict)} found):")
        print("-" * 60)
        
        for identifier, details in element_dict.items():
            print(f"\n  {identifier}:")
            
            # Show key attributes
            if 'text' in details and details['text']:
                print(f"    Text: '{details['text']}'")
            if 'aria_label' in details and details['aria_label']:
                print(f"    Aria Label: '{details['aria_label']}'")
            if 'placeholder' in details and details['placeholder']:
                print(f"    Placeholder: '{details['placeholder']}'")
            if 'type' in details and details['type']:
                print(f"    Type: {details['type']}")
            if 'name' in details and details['name']:
                print(f"    Name: {details['name']}")
            if 'id' in details and details['id']:
                print(f"    ID: {details['id']}")
            if 'options' in details and details['options']:
                print(f"    Options: {len(details['options'])} available")
                for option in details['options'][:3]:  # Show first 3 options
                    print(f"      - {option['text']} ({option['value']})")
                if len(details['options']) > 3:
                    print(f"      ... and {len(details['options']) - 3} more")
            if 'checked' in details:
                print(f"    Checked: {details['checked']}")
            if 'value' in details and details['value']:
                print(f"    Value: {details['value']}")


def analyze_aws_kms_capabilities(elements):
    """Analyze what AWS KMS configuration capabilities we have"""
    print(f"\n{'='*80}")
    print("AWS KMS CONFIGURATION CAPABILITY ANALYSIS")
    print(f"{'='*80}")
    
    # Analyze inputs
    inputs = elements.get('inputs', {})
    print(f"\nINPUT FIELDS ({len(inputs)} found):")
    for input_id, details in inputs.items():
        aria_label = details.get('aria_label', '')
        placeholder = details.get('placeholder', '')
        input_type = details.get('type', '')
        
        if aria_label:
            print(f"  - {aria_label} ({input_type})")
        elif placeholder:
            print(f"  - {placeholder} ({input_type})")
        else:
            print(f"  - {input_id} ({input_type})")
    
    # Analyze selects
    selects = elements.get('selects', {})
    print(f"\nSELECT DROPDOWNS ({len(selects)} found):")
    for select_id, details in selects.items():
        aria_label = details.get('aria_label', '')
        options = details.get('options', [])
        
        if aria_label:
            print(f"  - {aria_label} ({len(options)} options)")
        else:
            print(f"  - {select_id} ({len(options)} options)")
    
    # Analyze checkboxes
    checkboxes = elements.get('checkboxes', {})
    print(f"\nCHECKBOXES ({len(checkboxes)} found):")
    for checkbox_id, details in checkboxes.items():
        aria_label = details.get('aria_label', '')
        checked = details.get('checked', False)
        
        if aria_label:
            print(f"  - {aria_label} (checked: {checked})")
        else:
            print(f"  - {checkbox_id} (checked: {checked})")
    
    # Analyze radio buttons
    radios = elements.get('radio_buttons', {})
    print(f"\nRADIO BUTTONS ({len(radios)} found):")
    for radio_id, details in radios.items():
        aria_label = details.get('aria_label', '')
        value = details.get('value', '')
        checked = details.get('checked', False)
        
        if aria_label:
            print(f"  - {aria_label} = {value} (checked: {checked})")
        else:
            print(f"  - {radio_id} = {value} (checked: {checked})")
    
    # Analyze buttons
    buttons = elements.get('buttons', {})
    print(f"\nBUTTONS ({len(buttons)} found):")
    action_buttons = []
    for button_id, details in buttons.items():
        text = details.get('text', '')
        aria_label = details.get('aria_label', '')
        
        if any(keyword in text.lower() for keyword in ['save', 'add', 'configure', 'select', 'choose', 'create', 'delete', 'kms', 'key', 'encryption', 'decrypt', 'encrypt']):
            action_buttons.append(f"  - {text} ({aria_label})")
    
    print("  Action buttons:")
    for button in action_buttons[:10]:  # Show first 10
        print(button)
    if len(action_buttons) > 10:
        print(f"  ... and {len(action_buttons) - 10} more action buttons")


def main():
    """Main function"""
    print("[INFO] AWS KMS Element Mapper - Discovering ALL AWS Key Management Service Configuration Options")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = AWSKMSConfigurator(page)
        
        if configurator.navigate_to_aws_kms_config():
            # Map all elements
            elements = configurator.map_all_elements()
            
            # Print detailed analysis
            print_detailed_summary(elements)
            analyze_aws_kms_capabilities(elements)
            
            # Save files
            configurator.save_element_map("kms_elements_map.json")
            configurator.take_screenshot("aws_kms_config_page.png")
            
            print(f"\n[SUCCESS] AWS KMS element mapping completed!")
            print(f"[INFO] Total elements mapped: {sum(len(v) for v in elements.values())}")
            
        else:
            print("[ERROR] Failed to navigate to AWS Key Management Service configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()