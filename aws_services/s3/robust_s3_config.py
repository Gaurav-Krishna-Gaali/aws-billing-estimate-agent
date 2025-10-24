"""
Robust S3 Configuration Runner
Applies S3 configurations using reliable selectors
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from s3_configurator import S3Configurator


def load_configs(filename: str = "s3_configs.json") -> dict:
    """Load configurations from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Configuration file {filename} not found.")
        return {}


def apply_config_robust(configurator: S3Configurator, config: dict) -> bool:
    """Apply configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        print(f"[INFO] Description: {config['description']}")
        print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description: {config['description']}")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "storage_gb": "input[aria-label*='Storage amount']",
            "storage_class": "select[aria-label*='Storage class']",
            "put_requests": "input[aria-label*='PUT']",
            "get_requests": "input[aria-label*='GET']",
            "data_transfer_gb": "input[aria-label*='Data transfer']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    if setting_id == "storage_class":
                        configurator.page.select_option(selector, label=str(value))
                    else:
                        configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False


def run_configuration(config_name: str = "small_bucket", headless: bool = False):
    """Run a specific S3 configuration"""
    print(f"[INFO] Running S3 configuration: {config_name}")
    
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
        
        configurator = S3Configurator(page)
        
        if configurator.navigate_to_s3_config():
            if apply_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"s3_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to S3 configuration")
        
        browser.close()
        return None


def print_config_menu(configs: dict):
    """Print configuration menu"""
    print("\n" + "="*60)
    print("S3 CONFIGURATION MENU")
    print("="*60)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def main():
    """Main function - runs small_bucket configuration by default"""
    print("[INFO] Robust S3 Configuration")
    print("[INFO] Running 'small_bucket' configuration...")
    
    # Load and show available configurations
    configs = load_configs()
    if configs:
        print_config_menu(configs)
    
    url = run_configuration("small_bucket", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your S3 estimate URL: {url}")
    else:
        print("\n[ERROR] Configuration failed")


if __name__ == "__main__":
    main()

