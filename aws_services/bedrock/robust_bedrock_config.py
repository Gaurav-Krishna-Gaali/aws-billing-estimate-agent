"""
Robust Bedrock Configuration
Uses more reliable selectors and handles element mapping better
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


def apply_config_robust(configurator: BedrockConfigurator, config: dict) -> bool:
    """Apply configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        print(f"[INFO] Description: {config['description']}")
        print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
        
        # Set description using aria-label
        try:
            configurator.page.fill("input[aria-label*='Description']", config['description'])
            print(f"[OK] Set description: {config['description']}")
        except:
            print("[WARNING] Could not set description")
        
        # Apply settings using aria-label selectors (more reliable)
        settings_map = {
            "input_8_text": "input[aria-label*='Average requests per minute']:first-of-type",
            "input_9_text": "input[aria-label*='Hours per day at this rate']:first-of-type", 
            "input_10_text": "input[aria-label*='Average input tokens per request']:first-of-type",
            "input_11_text": "input[aria-label*='Average output tokens per request']:first-of-type",
            "input_12_text": "input[aria-label*='Average requests per minute']:nth-of-type(2)",
            "input_13_text": "input[aria-label*='Hours per day at this rate']:nth-of-type(2)",
            "input_14_text": "input[aria-label*='Average input tokens per request']:nth-of-type(2)",
            "input_15_text": "input[aria-label*='Average output tokens per request']:nth-of-type(2)",
            "input_16_text": "input[aria-label*='Average requests per minute']:nth-of-type(3)",
            "input_17_text": "input[aria-label*='Hours per day at this rate']:nth-of-type(3)",
            "input_18_text": "input[aria-label*='Average input tokens per request']:nth-of-type(3)",
            "input_19_text": "input[aria-label*='Average output tokens per request']:nth-of-type(3)"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
            elif setting_id.startswith("checkbox_"):
                # Handle checkboxes
                try:
                    if "2231" in setting_id:  # Model 2 checkbox
                        checkbox_selector = "input[id*='2231']"
                    elif "2232" in setting_id:  # Model 3 checkbox
                        checkbox_selector = "input[id*='2232']"
                    else:
                        continue
                    
                    if value:
                        configurator.page.check(checkbox_selector)
                    else:
                        configurator.page.uncheck(checkbox_selector)
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set checkbox {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
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
            if apply_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"bedrock_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
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
    print("[INFO] Robust Bedrock Configuration")
    print("[INFO] Running 'light_usage' configuration...")
    
    url = run_configuration("light_usage", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your Bedrock estimate URL: {url}")
    else:
        print("\n[ERROR] Configuration failed")


if __name__ == "__main__":
    main()
