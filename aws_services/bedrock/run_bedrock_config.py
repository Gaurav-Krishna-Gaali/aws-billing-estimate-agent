"""
Simple Bedrock Configuration Runner
Loads configurations from JSON file and applies them
"""

import json
from playwright.sync_api import sync_playwright
from aws_bedrock_configurator import BedrockConfigurator


def load_configs(filename: str = "bedrock_configs.json") -> dict:
    """Load configurations from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Configuration file {filename} not found.")
        return {}


def print_config_menu(configs: dict):
    """Print configuration menu"""
    print("\n" + "="*60)
    print("BEDROCK CONFIGURATION MENU")
    print("="*60)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def apply_config(configurator: BedrockConfigurator, config: dict) -> bool:
    """Apply configuration to Bedrock"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            elements = configurator.map_all_elements()
            for input_id, input_details in elements['inputs'].items():
                if 'description' in input_details.get('aria_label', '').lower():
                    configurator.page.fill(input_details['selector'], config['description'])
                    print(f"[OK] Set description")
                    break
        
        # Apply settings
        for setting_id, value in config['settings'].items():
            elements = configurator.map_all_elements()
            
            if setting_id in elements['inputs']:
                selector = elements['inputs'][setting_id]['selector']
                configurator.page.fill(selector, str(value))
                print(f"[OK] Set {setting_id} = {value}")
            elif setting_id in elements['checkboxes']:
                selector = elements['checkboxes'][setting_id]['selector']
                if value:
                    configurator.page.check(selector)
                else:
                    configurator.page.uncheck(selector)
                print(f"[OK] Set {setting_id} = {value}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False


def main():
    """Main function"""
    print("[INFO] Bedrock Configuration Runner")
    
    # Load configurations
    configs = load_configs()
    if not configs:
        return
    
    # Show menu
    print_config_menu(configs)
    
    # Get user choice
    config_list = list(configs.keys())
    try:
        choice = input(f"\nSelect configuration (1-{len(config_list)}) or press Enter for 'light_usage': ").strip()
        if not choice:
            choice = "1"
        
        config_index = int(choice) - 1
        if 0 <= config_index < len(config_list):
            selected_config_id = config_list[config_index]
            selected_config = configs[selected_config_id]
        else:
            print("[ERROR] Invalid selection, using light_usage")
            selected_config = configs['light_usage']
    except (ValueError, KeyboardInterrupt):
        print("[INFO] Using default light_usage configuration")
        selected_config = configs['light_usage']
    
    # Run configuration
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = BedrockConfigurator(page)
        
        if configurator.navigate_to_bedrock_config():
            if apply_config(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n🎉 SUCCESS!")
                    print(f"📋 Configuration: {selected_config['name']}")
                    print(f"🔗 Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"bedrock_{selected_config['name'].lower().replace(' ', '_').replace('-', '_')}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"💾 URL saved to {filename}")
                else:
                    print("[ERROR] Failed to save configuration")
            else:
                print("[ERROR] Failed to apply configuration")
        
        try:
            input("\nPress Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
