"""
Comprehensive Security Groups Configuration Runner
Handles all Security Groups configuration scenarios with robust automation
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from security_groups.comprehensive_security_groups_configurator import ComprehensiveSecurityGroupsConfigurator

def load_security_groups_configs() -> Dict[str, Any]:
    """Load Security Groups configurations from JSON file"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), "security_groups_configs.json")
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load Security Groups configurations: {e}")
        return {}

def run_security_groups_config(config_name: str, headless: bool = True) -> Optional[str]:
    """Run Security Groups configuration with specified preset"""
    print(f"[INFO] Starting Security Groups configuration: {config_name}")
    
    # Load configurations
    configs = load_security_groups_configs()
    if config_name not in configs:
        print(f"[ERROR] Configuration '{config_name}' not found")
        print(f"[INFO] Available configurations: {list(configs.keys())}")
        return None
    
    config = configs[config_name]
    print(f"[INFO] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config['estimated_monthly_cost']}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveSecurityGroupsConfigurator(page)
        
        # Navigate to Security Groups configuration
        if configurator.navigate_to_security_groups_config():
            print(f"[OK] Successfully navigated to Security Groups configuration page")
            
            # Apply configuration
            if configurator.apply_security_groups_configuration(config['settings']):
                print(f"[OK] Applied Security Groups configuration successfully")
                
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] Security Groups configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    url_filename = f"security_groups_{config_name}_estimate_url.txt"
                    with open(url_filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {url_filename}")
                    
                    return url
                else:
                    print(f"[ERROR] Failed to save Security Groups configuration")
            else:
                print(f"[ERROR] Failed to apply Security Groups configuration")
        else:
            print(f"[ERROR] Failed to navigate to Security Groups configuration page")
        
        browser.close()
        return None

def run_all_security_groups_configs(headless: bool = True) -> Dict[str, str]:
    """Run all Security Groups configurations and return URLs"""
    print(f"[INFO] Running all Security Groups configurations...")
    
    configs = load_security_groups_configs()
    results = {}
    
    for config_name in configs.keys():
        if config_name == 'custom':  # Skip custom configuration
            continue
            
        print(f"\n{'='*60}")
        print(f"Running Security Groups Configuration: {config_name}")
        print(f"{'='*60}")
        
        url = run_security_groups_config(config_name, headless)
        if url:
            results[config_name] = url
            print(f"[SUCCESS] {config_name} completed")
        else:
            print(f"[FAILED] {config_name} failed")
    
    return results

def list_security_groups_configs():
    """List all available Security Groups configurations"""
    configs = load_security_groups_configs()
    
    print(f"\n{'='*80}")
    print("AVAILABLE SECURITY GROUPS CONFIGURATIONS")
    print(f"{'='*80}")
    
    for config_name, config in configs.items():
        print(f"\n{config_name.upper()}:")
        print(f"  Name: {config['name']}")
        print(f"  Description: {config['description']}")
        print(f"  Estimated Cost: {config['estimated_monthly_cost']}")
        
        # Show key settings
        settings = config['settings']
        key_settings = [
            'number_of_security_groups', 'number_of_inbound_rules', 'number_of_outbound_rules',
            'number_of_custom_rules', 'enable_http_access', 'enable_https_access'
        ]
        
        print(f"  Key Settings:")
        for setting in key_settings:
            if setting in settings:
                print(f"    {setting}: {settings[setting]}")

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Security Groups Configuration Runner')
    parser.add_argument('--config', '-c', help='Configuration name to run')
    parser.add_argument('--list', '-l', action='store_true', help='List all configurations')
    parser.add_argument('--all', '-a', action='store_true', help='Run all configurations')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    if args.list:
        list_security_groups_configs()
    elif args.all:
        results = run_all_security_groups_configs(headless=args.headless)
        print(f"\n{'='*60}")
        print("SECURITY GROUPS CONFIGURATION RESULTS")
        print(f"{'='*60}")
        for config_name, url in results.items():
            print(f"{config_name}: {url}")
    elif args.config:
        url = run_security_groups_config(args.config, headless=args.headless)
        if url:
            print(f"\n[SUCCESS] Security Groups configuration '{args.config}' completed!")
            print(f"[URL] {url}")
        else:
            print(f"\n[FAILED] Security Groups configuration '{args.config}' failed!")
    else:
        # Interactive mode
        print("[INFO] Security Groups Configuration Runner")
        print("[INFO] Available commands:")
        print("  --list: List all configurations")
        print("  --all: Run all configurations")
        print("  --config <name>: Run specific configuration")
        print("  --headless: Run in headless mode")
        
        # Show available configurations
        list_security_groups_configs()

if __name__ == "__main__":
    main()
