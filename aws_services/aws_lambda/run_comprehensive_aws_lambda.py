"""
Comprehensive AWS Lambda Configuration Runner
Handles all 78 AWS Lambda elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_aws_lambda_configurator import ComprehensiveAWSLambdaConfigurator


def load_configs(filename: str = "aws_lambda_configs.json") -> dict:
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
    print("COMPREHENSIVE AWS LAMBDA CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific AWS Lambda configuration"""
    print(f"[INFO] Running comprehensive AWS Lambda configuration: {config_name}")
    
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
        
        configurator = ComprehensiveAWSLambdaConfigurator(page)
        
        if configurator.navigate_to_aws_lambda_config():
            if configurator.apply_aws_lambda_configuration(selected_config['settings']):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_aws_lambda_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to AWS Lambda configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    requests = settings.get('number_of_requests', 0)
    duration_ms = settings.get('duration_ms', 0)
    memory_mb = settings.get('memory_mb', 0)
    storage_mb = settings.get('ephemeral_storage_mb', 0)
    concurrency = settings.get('concurrency', 0)
    provisioned_hours = settings.get('provisioned_concurrency_enabled_hours', 0)
    provisioned_requests = settings.get('provisioned_concurrency_requests', 0)
    
    print(f"[INFO] AWS Lambda Configuration:")
    print(f"  - Number of Requests: {requests:,}")
    print(f"  - Duration per Request: {duration_ms} ms")
    print(f"  - Memory Allocated: {memory_mb} MB")
    print(f"  - Ephemeral Storage: {storage_mb} MB")
    print(f"  - Concurrency: {concurrency}")
    print(f"  - Provisioned Concurrency Hours: {provisioned_hours}")
    print(f"  - Provisioned Concurrency Requests: {provisioned_requests:,}")
    
    # Calculate compute metrics
    if requests > 0 and duration_ms > 0:
        total_compute_seconds = (requests * duration_ms) / 1000
        total_compute_hours = total_compute_seconds / 3600
        print(f"  - Total Compute Time: {total_compute_seconds:,.0f} seconds")
        print(f"  - Total Compute Hours: {total_compute_hours:.2f} hours")
    
    # Calculate memory usage
    if memory_mb > 0:
        total_memory_gb = (requests * memory_mb) / 1024
        print(f"  - Total Memory Usage: {total_memory_gb:,.0f} GB")
    
    # Calculate storage usage
    if storage_mb > 0:
        total_storage_gb = (requests * storage_mb) / 1024
        print(f"  - Total Storage Usage: {total_storage_gb:,.0f} GB")
    
    # Calculate provisioned concurrency metrics
    if provisioned_hours > 0:
        provisioned_daily_hours = provisioned_hours / 30
        print(f"  - Daily Provisioned Hours: {provisioned_daily_hours:.1f} hours")
        print(f"  - Monthly Provisioned Hours: {provisioned_hours} hours")


def main():
    """Test the comprehensive AWS Lambda configurator"""
    print("[INFO] Comprehensive AWS Lambda Configuration Runner")
    print("[INFO] Handles all 78 AWS Lambda configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['basic_function', 'high_traffic_api', 'data_processing', 'real_time_processing']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive AWS Lambda estimate URL: {url}")
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
