"""
Comprehensive SQS Configuration Runner
Handles all 42 SQS elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_sqs_configurator import ComprehensiveSQSConfigurator


def load_configs(filename: str = "sqs_configs.json") -> dict:
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
    print("COMPREHENSIVE SQS CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific SQS configuration"""
    print(f"[INFO] Running comprehensive SQS configuration: {config_name}")
    
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
        
        configurator = ComprehensiveSQSConfigurator(page)
        
        if configurator.navigate_to_sqs_config():
            if configurator.apply_sqs_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_sqs_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to SQS configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    standard_requests = settings.get('standard_queue_requests', 0)
    fifo_requests = settings.get('fifo_queue_requests', 0)
    fair_requests = settings.get('fair_queue_requests', 0)
    total_requests = standard_requests + fifo_requests + fair_requests
    
    inbound_tb = settings.get('inbound_data_transfer_tb', 0)
    outbound_tb = settings.get('outbound_data_transfer_tb', 0)
    total_tb = inbound_tb + outbound_tb
    
    print(f"[INFO] SQS Configuration:")
    print(f"  - Standard Queue Requests: {standard_requests:,}")
    print(f"  - FIFO Queue Requests: {fifo_requests:,}")
    print(f"  - Fair Queue Requests: {fair_requests:,}")
    print(f"  - Total Queue Requests: {total_requests:,}")
    print(f"  - Inbound Data Transfer: {inbound_tb} TB")
    print(f"  - Outbound Data Transfer: {outbound_tb} TB")
    print(f"  - Total Data Transfer: {total_tb} TB")
    
    # Calculate message throughput
    if total_requests > 0:
        daily_requests = total_requests / 30  # Assuming monthly
        hourly_requests = daily_requests / 24
        print(f"  - Daily Message Volume: {daily_requests:,.0f} messages")
        print(f"  - Hourly Message Volume: {hourly_requests:,.0f} messages")


def main():
    """Test the comprehensive SQS configurator"""
    print("[INFO] Comprehensive SQS Configuration Runner")
    print("[INFO] Handles all 42 SQS configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['basic_messaging', 'medium_enterprise', 'large_enterprise', 'high_throughput']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive SQS estimate URL: {url}")
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
