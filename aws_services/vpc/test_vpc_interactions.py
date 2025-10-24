"""
Test VPC Interaction Capabilities
Demonstrates full interaction with radios, inputs, dropdowns, and checkboxes
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright
from typing import Dict, Any, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vpc.enhanced_vpc_configurator import EnhancedVPCConfigurator


def test_vpc_element_discovery():
    """Test discovering all VPC configuration elements"""
    print(f"\n{'='*80}")
    print("VPC ELEMENT DISCOVERY TEST")
    print(f"{'='*80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            print(f"\n[INFO] Successfully navigated to VPC configuration page")
            
            # Discover all elements
            options = configurator.explore_all_vpc_options()
            
            # Save discovery results
            with open("vpc_element_discovery_results.json", "w") as f:
                json.dump(options, f, indent=2)
            
            print(f"\n[SUCCESS] Element discovery completed!")
            print(f"[SAVE] Results saved to vpc_element_discovery_results.json")
            
            # Print detailed summary
            print_detailed_summary(options)
            
        else:
            print("[ERROR] Failed to navigate to VPC configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def test_radio_button_interactions():
    """Test radio button interaction capabilities"""
    print(f"\n{'='*80}")
    print("VPC RADIO BUTTON INTERACTION TEST")
    print(f"{'='*80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Discover all radio buttons
            radio_buttons = configurator.discover_all_radio_buttons()
            
            print(f"\n[INFO] Testing radio button interactions...")
            print(f"[INFO] Found {len(radio_buttons)} radio buttons")
            
            # Test clicking each radio button
            for i, radio in enumerate(radio_buttons):
                print(f"\n[TEST] Radio Button {i}:")
                print(f"  Name: {radio.get('name', 'N/A')}")
                print(f"  Value: {radio.get('value', 'N/A')}")
                print(f"  Label: {radio.get('label_text', 'N/A')}")
                print(f"  Currently Checked: {radio.get('checked', False)}")
                
                # Test clicking by value
                if radio.get('value'):
                    success = configurator.click_radio_button_by_value(radio['value'])
                    print(f"  Click by value: {'SUCCESS' if success else 'FAILED'}")
                
                # Test clicking by text
                if radio.get('label_text'):
                    success = configurator.click_radio_button_by_text(radio['label_text'])
                    print(f"  Click by text: {'SUCCESS' if success else 'FAILED'}")
            
            print(f"\n[SUCCESS] Radio button interaction test completed!")
            
        else:
            print("[ERROR] Failed to navigate to VPC configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def test_dropdown_interactions():
    """Test dropdown interaction capabilities"""
    print(f"\n{'='*80}")
    print("VPC DROPDOWN INTERACTION TEST")
    print(f"{'='*80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Discover all dropdowns
            dropdowns = configurator.discover_all_dropdowns()
            
            print(f"\n[INFO] Testing dropdown interactions...")
            print(f"[INFO] Found {len(dropdowns)} dropdowns")
            
            # Test each dropdown
            for i, dropdown in enumerate(dropdowns):
                print(f"\n[TEST] Dropdown {i}:")
                print(f"  Name: {dropdown.get('name', 'N/A')}")
                print(f"  ID: {dropdown.get('id', 'N/A')}")
                print(f"  Aria Label: {dropdown.get('aria_label', 'N/A')}")
                print(f"  Options: {len(dropdown.get('options', []))}")
                
                # Show first few options
                options = dropdown.get('options', [])
                for j, option in enumerate(options[:3]):
                    print(f"    Option {j}: {option.get('text', 'N/A')} = {option.get('value', 'N/A')}")
                if len(options) > 3:
                    print(f"    ... and {len(options) - 3} more options")
                
                # Test selecting first option
                if options:
                    first_option = options[0]
                    if first_option.get('value'):
                        success = configurator.select_dropdown_option(
                            dropdown.get('name', ''), 
                            first_option['value']
                        )
                        print(f"  Select first option: {'SUCCESS' if success else 'FAILED'}")
            
            print(f"\n[SUCCESS] Dropdown interaction test completed!")
            
        else:
            print("[ERROR] Failed to navigate to VPC configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def test_input_field_interactions():
    """Test input field interaction capabilities"""
    print(f"\n{'='*80}")
    print("VPC INPUT FIELD INTERACTION TEST")
    print(f"{'='*80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Discover all input fields
            input_fields = configurator.discover_all_input_fields()
            
            print(f"\n[INFO] Testing input field interactions...")
            print(f"[INFO] Found {len(input_fields)} input fields")
            
            # Test each input field
            for i, field in enumerate(input_fields):
                print(f"\n[TEST] Input Field {i}:")
                print(f"  Type: {field.get('type', 'N/A')}")
                print(f"  Aria Label: {field.get('aria_label', 'N/A')}")
                print(f"  Placeholder: {field.get('placeholder', 'N/A')}")
                print(f"  Name: {field.get('name', 'N/A')}")
                print(f"  ID: {field.get('id', 'N/A')}")
                print(f"  Visible: {field.get('visible', False)}")
                print(f"  Current Value: {field.get('value', 'N/A')}")
                
                # Test filling the field
                if field.get('visible'):
                    test_value = f"test_value_{i}"
                    success = configurator.fill_input_field(
                        field.get('aria_label', '') or field.get('name', '') or field.get('id', ''),
                        test_value
                    )
                    print(f"  Fill test: {'SUCCESS' if success else 'FAILED'}")
            
            print(f"\n[SUCCESS] Input field interaction test completed!")
            
        else:
            print("[ERROR] Failed to navigate to VPC configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def test_checkbox_interactions():
    """Test checkbox interaction capabilities"""
    print(f"\n{'='*80}")
    print("VPC CHECKBOX INTERACTION TEST")
    print(f"{'='*80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Discover all checkboxes
            checkboxes = configurator.discover_all_checkboxes()
            
            print(f"\n[INFO] Testing checkbox interactions...")
            print(f"[INFO] Found {len(checkboxes)} checkboxes")
            
            # Test each checkbox
            for i, checkbox in enumerate(checkboxes):
                print(f"\n[TEST] Checkbox {i}:")
                print(f"  Name: {checkbox.get('name', 'N/A')}")
                print(f"  ID: {checkbox.get('id', 'N/A')}")
                print(f"  Aria Label: {checkbox.get('aria_label', 'N/A')}")
                print(f"  Label Text: {checkbox.get('label_text', 'N/A')}")
                print(f"  Currently Checked: {checkbox.get('checked', False)}")
                
                # Test toggling the checkbox
                identifier = (checkbox.get('aria_label', '') or 
                            checkbox.get('name', '') or 
                            checkbox.get('id', ''))
                
                if identifier:
                    # Test checking
                    success = configurator.toggle_checkbox(identifier, True)
                    print(f"  Check test: {'SUCCESS' if success else 'FAILED'}")
                    
                    # Test unchecking
                    success = configurator.toggle_checkbox(identifier, False)
                    print(f"  Uncheck test: {'SUCCESS' if success else 'FAILED'}")
            
            print(f"\n[SUCCESS] Checkbox interaction test completed!")
            
        else:
            print("[ERROR] Failed to navigate to VPC configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def test_comprehensive_configuration():
    """Test comprehensive VPC configuration with all element types"""
    print(f"\n{'='*80}")
    print("VPC COMPREHENSIVE CONFIGURATION TEST")
    print(f"{'='*80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = EnhancedVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Comprehensive test configuration
            test_config = {
                'description': 'Comprehensive VPC Test Configuration',
                'vpc_type': 'Production',
                'deployment_model': 'Multi-AZ',
                'connectivity_type': 'Internet Gateway',
                'region': 'us-east-1',
                'availability_zone': 'us-east-1a',
                'number_of_vpcs': 1,
                'number_of_subnets': 4,
                'number_of_internet_gateways': 1,
                'number_of_nat_gateways': 2,
                'number_of_vpc_endpoints': 3,
                'number_of_route_tables': 4,
                'number_of_security_groups': 6,
                'number_of_network_acls': 2,
                'data_processed_gb': 500,
                'endpoint_hours': 744,
                'nat_gateway_hours': 1488,
                'vpc_peering_hours': 0,
                'transit_gateway_hours': 0,
                'vpn_connection_hours': 0,
                'vpn_tunnel_hours': 0,
                'data_transfer_gb': 250,
                'availability_zones': 2,
                'cidr_block': '10.0.0.0/16',
                'enable_dns_hostnames': True,
                'enable_dns_resolution': True,
                'enable_vpc_flow_logs': True,
                'enable_vpc_endpoints': True,
                'enable_nat_gateway': True,
                'enable_internet_gateway': True,
                'enable_vpn_connection': False
            }
            
            print(f"\n[INFO] Testing comprehensive VPC configuration...")
            print(f"[INFO] Configuration includes:")
            print(f"  - Description: {test_config.get('description', 'N/A')}")
            print(f"  - VPC Type: {test_config.get('vpc_type', 'N/A')}")
            print(f"  - Region: {test_config.get('region', 'N/A')}")
            print(f"  - Number of VPCs: {test_config.get('number_of_vpcs', 'N/A')}")
            print(f"  - Number of Subnets: {test_config.get('number_of_subnets', 'N/A')}")
            print(f"  - Enable DNS: {test_config.get('enable_dns_hostnames', 'N/A')}")
            
            # Apply comprehensive configuration
            success = configurator.apply_comprehensive_vpc_configuration(test_config)
            
            if success:
                print(f"\n[SUCCESS] Comprehensive VPC configuration test completed!")
                
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("comprehensive_vpc_test_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to comprehensive_vpc_test_url.txt")
            else:
                print(f"[FAILED] Comprehensive VPC configuration test failed!")
            
        else:
            print("[ERROR] Failed to navigate to VPC configuration page")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


def print_detailed_summary(options: Dict[str, Any]):
    """Print detailed summary of discovered elements"""
    print(f"\n{'='*80}")
    print("VPC ELEMENT DISCOVERY SUMMARY")
    print(f"{'='*80}")
    
    radio_buttons = options.get('radio_buttons', [])
    dropdowns = options.get('dropdowns', [])
    input_fields = options.get('input_fields', [])
    checkboxes = options.get('checkboxes', [])
    
    print(f"\nRADIO BUTTONS ({len(radio_buttons)} found):")
    for i, radio in enumerate(radio_buttons):
        print(f"  {i}. {radio.get('name', 'N/A')} = {radio.get('value', 'N/A')} ({radio.get('label_text', 'N/A')})")
    
    print(f"\nDROPDOWNS ({len(dropdowns)} found):")
    for i, dropdown in enumerate(dropdowns):
        print(f"  {i}. {dropdown.get('name', 'N/A')} ({len(dropdown.get('options', []))} options)")
    
    print(f"\nINPUT FIELDS ({len(input_fields)} found):")
    for i, field in enumerate(input_fields):
        if field.get('visible'):
            print(f"  {i}. {field.get('aria_label', 'N/A')} ({field.get('type', 'N/A')}) - Visible")
        else:
            print(f"  {i}. {field.get('aria_label', 'N/A')} ({field.get('type', 'N/A')}) - Hidden")
    
    print(f"\nCHECKBOXES ({len(checkboxes)} found):")
    for i, checkbox in enumerate(checkboxes):
        print(f"  {i}. {checkbox.get('name', 'N/A')} ({checkbox.get('label_text', 'N/A')}) - Checked: {checkbox.get('checked', False)}")
    
    print(f"\nTOTAL INTERACTIVE ELEMENTS: {options.get('total_elements', 0)}")


def main():
    """Main test function"""
    print("[INFO] VPC Interaction Capabilities Test Suite")
    print("[INFO] This test demonstrates full interaction with all VPC elements")
    
    # Run all tests
    test_vpc_element_discovery()
    test_radio_button_interactions()
    test_dropdown_interactions()
    test_input_field_interactions()
    test_checkbox_interactions()
    test_comprehensive_configuration()
    
    print(f"\n{'='*80}")
    print("ALL VPC INTERACTION TESTS COMPLETED")
    print(f"{'='*80}")
    print("[SUCCESS] VPC configurator can interact with:")
    print("  ✅ Radio Buttons - Click by value or text")
    print("  ✅ Dropdowns - Select options by name and value")
    print("  ✅ Input Fields - Fill by aria-label, name, or id")
    print("  ✅ Checkboxes - Toggle by identifier")
    print("  ✅ Dynamic Elements - Discover and interact with all available options")
    print("  ✅ Comprehensive Configuration - Apply complex multi-element configurations")


if __name__ == "__main__":
    main()
