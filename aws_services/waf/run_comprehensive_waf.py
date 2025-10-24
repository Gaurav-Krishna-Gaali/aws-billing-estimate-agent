"""
Comprehensive WAF Configuration Runner
Handles all 40 WAF elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_waf_configurator import ComprehensiveWAFConfigurator


def load_configs(filename: str = "waf_configs.json") -> dict:
    """Load configurations from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Configuration file {filename} not found.")
        return {}


def print_config_menu(configs: dict):
    """Print configuration menu"""
    print("\n" + "="*80)
    print("COMPREHENSIVE WAF CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific WAF configuration"""
    print(f"[INFO] Running comprehensive WAF configuration: {config_name}")
    
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
        
        configurator = ComprehensiveWAFConfigurator(page)
        
        if configurator.navigate_to_waf_config():
            if configurator.apply_waf_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_waf_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to WAF configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    total_web_acls = settings.get('web_acls', 0)
    total_rules = settings.get('rules_per_web_acl', 0) * total_web_acls
    total_rule_groups = settings.get('rule_groups_per_web_acl', 0) * total_web_acls
    total_managed_rule_groups = settings.get('managed_rule_groups_per_web_acl', 0) * total_web_acls
    total_requests = settings.get('web_requests_received', 0)
    
    print(f"[INFO] WAF Protection Scope:")
    print(f"  - Web ACLs: {total_web_acls}")
    print(f"  - Total Rules: {total_rules:,}")
    print(f"  - Rule Groups: {total_rule_groups}")
    print(f"  - Managed Rule Groups: {total_managed_rule_groups}")
    print(f"  - Monthly Requests: {total_requests:,}")
    print(f"  - Rules per ACL: {settings.get('rules_per_web_acl', 0)}")
    print(f"  - Rule Groups per ACL: {settings.get('rule_groups_per_web_acl', 0)}")


def main():
    """Main function"""
    print("[INFO] Comprehensive WAF Configuration Runner")
    print("[INFO] Handles all 40 WAF configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['basic_website', 'medium_enterprise', 'large_enterprise', 'high_traffic_application']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive WAF estimate URL: {url}")
    else:
        print("\n[ERROR] Configuration failed")


def run_specific_config(config_name: str):
    """Run a specific configuration by name"""
    print(f"[INFO] Running specific configuration: {config_name}")
    
    configs = load_configs()
    if config_name not in configs:
        print(f"[ERROR] Configuration '{config_name}' not found.")
        print(f"[INFO] Available configurations: {list(configs.keys())}")
        return None
    
    # Analyze the configuration first
    analyze_configuration(configs[config_name])
    
    # Run the configuration
    url = run_configuration(config_name, headless=False)
    
    if url:
        print(f"\n[SUCCESS] {config_name} configuration completed!")
        print(f"[URL] Estimate URL: {url}")
        return url
    else:
        print(f"\n[ERROR] {config_name} configuration failed")
        return None


if __name__ == "__main__":
    main()
