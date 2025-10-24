"""
Comprehensive Application Load Balancer Configuration Runner
Handles all 79 ALB elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_alb_configurator import ComprehensiveALBConfigurator


def load_configs(filename: str = "alb_configs.json") -> dict:
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
    print("COMPREHENSIVE APPLICATION LOAD BALANCER CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific ALB configuration"""
    print(f"[INFO] Running comprehensive ALB configuration: {config_name}")
    
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
        
        configurator = ComprehensiveALBConfigurator(page)
        
        if configurator.navigate_to_alb_config():
            if configurator.apply_alb_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_alb_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to ALB configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    total_alb = settings.get('alb_count', 0)
    total_nlb = settings.get('nlb_count', 0)
    total_glb = settings.get('glb_endpoints', 0)
    total_clb = settings.get('clb_count', 0)
    total_load_balancers = total_alb + total_nlb + total_glb + total_clb
    
    print(f"[INFO] Load Balancer Configuration:")
    print(f"  - Application Load Balancers: {total_alb}")
    print(f"  - Network Load Balancers: {total_nlb}")
    print(f"  - Gateway Load Balancer Endpoints: {total_glb}")
    print(f"  - Classic Load Balancers: {total_clb}")
    print(f"  - Total Load Balancers: {total_load_balancers}")
    
    if total_alb > 0:
        print(f"  - ALB Lambda Processed: {settings.get('alb_lambda_processed_bytes', 0):,} bytes")
        print(f"  - ALB EC2 Processed: {settings.get('alb_ec2_processed_bytes', 0):,} bytes")
        print(f"  - ALB New Connections: {settings.get('alb_new_connections', 0):,}")
        print(f"  - ALB Requests/Second: {settings.get('alb_requests_per_second', 0)}")
    
    if total_nlb > 0:
        print(f"  - NLB TCP Processed: {settings.get('nlb_tcp_processed_bytes', 0):,} bytes")
        print(f"  - NLB UDP Processed: {settings.get('nlb_udp_processed_bytes', 0):,} bytes")
        print(f"  - NLB TLS Processed: {settings.get('nlb_tls_processed_bytes', 0):,} bytes")
    
    if total_glb > 0:
        print(f"  - GLB Processed: {settings.get('glb_processed_bytes', 0):,} bytes")
        print(f"  - GLB Availability Zones: {settings.get('glb_availability_zones', 0)}")
    
    if total_clb > 0:
        print(f"  - CLB Processed: {settings.get('clb_processed_bytes', 0):,} bytes")


def main():
    """Test the comprehensive ALB configurator"""
    print("[INFO] Comprehensive Application Load Balancer Configuration Runner")
    print("[INFO] Handles all 79 ALB configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['basic_web_app', 'medium_enterprise', 'large_enterprise', 'high_traffic_web']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive ALB estimate URL: {url}")
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
