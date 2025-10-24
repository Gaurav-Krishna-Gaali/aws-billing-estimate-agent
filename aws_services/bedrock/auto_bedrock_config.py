"""
Automatic Bedrock Configuration
Runs a specific configuration without user input
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


def apply_config(configurator: BedrockConfigurator, config: dict) -> bool:
    """Apply configuration to Bedrock"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        print(f"[INFO] Description: {config['description']}")
        print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
        
        # Set description
        if 'description' in config:
            elements = configurator.map_all_elements()
            for input_id, input_details in elements['inputs'].items():
                if 'description' in input_details.get('aria_label', '').lower():
                    configurator.page.fill(input_details['selector'], config['description'])
                    print(f"[OK] Set description: {config['description']}")
                    break
        
        # Apply settings
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            elements = configurator.map_all_elements()
            
            if setting_id in elements['inputs']:
                selector = elements['inputs'][setting_id]['selector']
                configurator.page.fill(selector, str(value))
                print(f"[OK] Set {setting_id} = {value}")
                settings_applied += 1
            elif setting_id in elements['checkboxes']:
                selector = elements['checkboxes'][setting_id]['selector']
                if value:
                    configurator.page.check(selector)
                else:
                    configurator.page.uncheck(selector)
                print(f"[OK] Set {setting_id} = {value}")
                settings_applied += 1
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False


def run_configuration(config_name: str = "light_usage", headless: bool = False):
    """Run a specific Bedrock configuration"""
    print(f"[INFO] Running Bedrock configuration: {config_name}")
    
    # Load configurations
    configs = load_configs()
    if not configs:
        return None
    
    if config_name not in configs:
        print(f"[ERROR] Configuration '{config_name}' not found.")
        print(f"[INFO] Available configurations: {list(configs.keys())}")
        return None
    
    selected_config = configs[config_name]
    
    # Run configuration
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
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
                    filename = f"bedrock_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"💾 URL saved to {filename}")
                    
                    browser.close()
                    return url
                else:
                    print("[ERROR] Failed to save configuration")
            else:
                print("[ERROR] Failed to apply configuration")
        else:
            print("[ERROR] Failed to navigate to Bedrock configuration")
        
        browser.close()
        return None


def main():
    """Main function - runs light_usage configuration by default"""
    print("[INFO] Automatic Bedrock Configuration")
    print("[INFO] Running 'light_usage' configuration...")
    
    url = run_configuration("light_usage", headless=False)
    
    if url:
        print(f"\n✅ Configuration completed successfully!")
        print(f"🔗 Your Bedrock estimate URL: {url}")
    else:
        print("\n❌ Configuration failed")


if __name__ == "__main__":
    main()
