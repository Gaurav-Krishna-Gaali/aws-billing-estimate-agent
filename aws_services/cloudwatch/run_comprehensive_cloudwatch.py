"""
Comprehensive CloudWatch Configuration Runner
Handles all 81 CloudWatch elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_cloudwatch_configurator import ComprehensiveCloudWatchConfigurator


def load_configs(filename: str = "cloudwatch_configs.json") -> dict:
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
    print("COMPREHENSIVE CLOUDWATCH CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific CloudWatch configuration"""
    print(f"[INFO] Running comprehensive CloudWatch configuration: {config_name}")
    
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
        
        configurator = ComprehensiveCloudWatchConfigurator(page)
        
        if configurator.navigate_to_cloudwatch_config():
            if configurator.apply_cloudwatch_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_cloudwatch_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to CloudWatch configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    total_metrics = settings.get('metrics_count', 0)
    total_api_requests = (settings.get('get_metric_data_requests', 0) + 
                         settings.get('get_metric_widget_image_requests', 0) + 
                         settings.get('other_api_requests', 0))
    total_logs_gb = (settings.get('standard_logs_data_ingested_gb', 0) + 
                    settings.get('infrequent_logs_data_ingested_gb', 0))
    total_alarms = (settings.get('standard_resolution_alarms', 0) + 
                   settings.get('high_resolution_alarms', 0) + 
                   settings.get('composite_alarms', 0))
    
    print(f"[INFO] Monitoring Scope:")
    print(f"  - Metrics: {total_metrics:,}")
    print(f"  - API Requests: {total_api_requests:,}")
    print(f"  - Logs Data: {total_logs_gb:,} GB")
    print(f"  - Dashboards: {settings.get('dashboards_count', 0)}")
    print(f"  - Alarms: {total_alarms}")
    print(f"  - Lambda Functions: {settings.get('lambda_functions', 0)}")
    print(f"  - RUM Visitors: {settings.get('rum_monthly_visitors', 0):,}")
    print(f"  - Synthetics Resources: {settings.get('synthetics_monitored_resources', 0)}")
    print(f"  - X-Ray Requests: {settings.get('xray_incoming_requests', 0):,}")
    print(f"  - SLOs: {settings.get('slo_count', 0)}")


def main():
    """Main function"""
    print("[INFO] Comprehensive CloudWatch Configuration Runner")
    print("[INFO] Handles all 81 CloudWatch configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['startup_monitoring', 'medium_enterprise', 'large_enterprise', 'high_performance_app']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive CloudWatch estimate URL: {url}")
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

