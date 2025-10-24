"""
Comprehensive AWS Shield Configuration Runner
Handles all 36 AWS Shield elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_aws_shield_configurator import ComprehensiveAWSShieldConfigurator


def load_configs(filename: str = "aws_shield_configs.json") -> dict:
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
    print("COMPREHENSIVE AWS SHIELD CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific AWS Shield configuration"""
    print(f"[INFO] Running comprehensive AWS Shield configuration: {config_name}")
    
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
        
        configurator = ComprehensiveAWSShieldConfigurator(page)
        
        if configurator.navigate_to_aws_shield_config():
            if configurator.apply_aws_shield_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_aws_shield_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to AWS Shield configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    cloudfront_usage = settings.get('cloudfront_usage', 0)
    elb_usage = settings.get('elb_usage', 0)
    elastic_ip_usage = settings.get('elastic_ip_usage', 0)
    global_accelerator_usage = settings.get('global_accelerator_usage', 0)
    total_usage = cloudfront_usage + elb_usage + elastic_ip_usage + global_accelerator_usage
    
    print(f"[INFO] AWS Shield Configuration:")
    print(f"  - CloudFront Usage: {cloudfront_usage:,} requests")
    print(f"  - ELB Usage: {elb_usage:,} requests")
    print(f"  - Elastic IP Usage: {elastic_ip_usage:,} requests")
    print(f"  - Global Accelerator Usage: {global_accelerator_usage:,} requests")
    print(f"  - Total Protected Usage: {total_usage:,} requests")
    
    # Calculate protection coverage
    if total_usage > 0:
        cloudfront_percentage = (cloudfront_usage / total_usage) * 100
        elb_percentage = (elb_usage / total_usage) * 100
        elastic_ip_percentage = (elastic_ip_usage / total_usage) * 100
        global_accelerator_percentage = (global_accelerator_usage / total_usage) * 100
        
        print(f"  - CloudFront Protection: {cloudfront_percentage:.1f}%")
        print(f"  - ELB Protection: {elb_percentage:.1f}%")
        print(f"  - Elastic IP Protection: {elastic_ip_percentage:.1f}%")
        print(f"  - Global Accelerator Protection: {global_accelerator_percentage:.1f}%")


def main():
    """Test the comprehensive AWS Shield configurator"""
    print("[INFO] Comprehensive AWS Shield Configuration Runner")
    print("[INFO] Handles all 36 AWS Shield configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['basic_protection', 'medium_enterprise', 'large_enterprise', 'high_traffic']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive AWS Shield estimate URL: {url}")
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
