"""
Comprehensive S3 Configuration Runner
Handles all 172 S3 elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_s3_configurator import ComprehensiveS3Configurator


def load_configs(filename: str = "advanced_s3_configs.json") -> dict:
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
    print("COMPREHENSIVE S3 CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
        
        # Show which storage classes are configured
        storage_classes = []
        for key in config.keys():
            if key in ['standard', 'int', 'standard_ia', 'one_zone_ia', 'glacier_flexible', 'glacier_deep', 'glacier_instant', 'express_one_zone']:
                storage_classes.append(key.replace('_', ' ').title())
        
        if storage_classes:
            print(f"   Storage Classes: {', '.join(storage_classes)}")


def run_configuration(config_name: str = "development_testing", headless: bool = False):
    """Run a specific S3 configuration"""
    print(f"[INFO] Running comprehensive S3 configuration: {config_name}")
    
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
        
        configurator = ComprehensiveS3Configurator(page)
        
        if configurator.navigate_to_s3_config():
            if configurator.apply_comprehensive_configuration(selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_s3_{config_name}_url.txt"
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


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    # Count storage classes
    storage_classes = []
    for key in config.keys():
        if key in ['standard', 'int', 'standard_ia', 'one_zone_ia', 'glacier_flexible', 'glacier_deep', 'glacier_instant', 'express_one_zone']:
            storage_classes.append(key)
    
    print(f"[INFO] Storage Classes: {len(storage_classes)} configured")
    for sc in storage_classes:
        sc_config = config[sc]
        storage_gb = sc_config.get('storage_gb', 0)
        print(f"  - {sc.replace('_', ' ').title()}: {storage_gb} GB")
    
    # Count advanced features
    if 'advanced_features' in config:
        af = config['advanced_features']
        features_count = len([k for k, v in af.items() if v > 0])
        print(f"[INFO] Advanced Features: {features_count} configured")
        
        if af.get('vector_indexes', 0) > 0:
            print(f"  - Vector Search: {af['vector_indexes']} indexes, {af.get('vectors_per_index', 0)} vectors each")
        if af.get('object_lambda_requests', 0) > 0:
            print(f"  - Object Lambda: {af['object_lambda_requests']} requests")
        if af.get('encrypted_data_gb', 0) > 0:
            print(f"  - Encryption: {af['encrypted_data_gb']} GB encrypted")
    
    total_storage = sum(config.get(sc, {}).get('storage_gb', 0) for sc in storage_classes)
    print(f"[INFO] Total Storage: {total_storage:,} GB")


def main():
    """Main function"""
    print("[INFO] Comprehensive S3 Configuration Runner")
    print("[INFO] Handles all 172 S3 configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['enterprise_multi_tier', 'ai_ml_workload', 'cost_optimized', 'development_testing']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_testing")
    url = run_configuration("development_testing", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive S3 estimate URL: {url}")
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

