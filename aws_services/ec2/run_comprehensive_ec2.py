"""
Comprehensive EC2 Configuration Runner
Handles all 144 EC2 elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_ec2_configurator import ComprehensiveEC2Configurator


def load_configs(filename: str = "ec2_configs.json") -> dict:
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
    print("COMPREHENSIVE EC2 CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_environment", headless: bool = False):
    """Run a specific EC2 configuration"""
    print(f"[INFO] Running comprehensive EC2 configuration: {config_name}")
    
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
        
        configurator = ComprehensiveEC2Configurator(page)
        
        if configurator.navigate_to_ec2_config():
            if configurator.apply_ec2_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_ec2_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to EC2 configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    instances = settings.get('number_of_instances', 0)
    storage_gb = settings.get('storage_amount_gb', 0)
    iops = settings.get('iops_per_volume', 0)
    throughput = settings.get('throughput_mbps', 0)
    inbound_tb = settings.get('inbound_data_transfer_tb', 0)
    outbound_tb = settings.get('outbound_data_transfer_tb', 0)
    total_tb = inbound_tb + outbound_tb
    licensing = settings.get('licensing_cost', 0)
    monitoring = settings.get('enable_monitoring', False)
    
    print(f"[INFO] EC2 Configuration:")
    print(f"  - Number of Instances: {instances}")
    print(f"  - Storage Amount: {storage_gb} GB")
    print(f"  - IOPS per Volume: {iops:,}")
    print(f"  - Throughput: {throughput} MBps")
    print(f"  - Inbound Data Transfer: {inbound_tb} TB")
    print(f"  - Outbound Data Transfer: {outbound_tb} TB")
    print(f"  - Total Data Transfer: {total_tb} TB")
    print(f"  - Licensing Cost: ${licensing:,}")
    print(f"  - Monitoring Enabled: {monitoring}")
    
    # Calculate resource ratios
    if instances > 0:
        storage_per_instance = storage_gb / instances
        iops_per_instance = iops / instances
        print(f"  - Storage per Instance: {storage_per_instance:.1f} GB")
        print(f"  - IOPS per Instance: {iops_per_instance:.0f}")
    
    # Calculate data transfer ratios
    if total_tb > 0:
        inbound_percentage = (inbound_tb / total_tb) * 100
        outbound_percentage = (outbound_tb / total_tb) * 100
        print(f"  - Inbound Data: {inbound_percentage:.1f}%")
        print(f"  - Outbound Data: {outbound_percentage:.1f}%")


def main():
    """Test the comprehensive EC2 configurator"""
    print("[INFO] Comprehensive EC2 Configuration Runner")
    print("[INFO] Handles all 144 EC2 configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['basic_web_server', 'medium_enterprise', 'large_enterprise', 'high_performance']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_environment")
    url = run_configuration("development_environment", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive EC2 estimate URL: {url}")
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
