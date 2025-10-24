"""
Comprehensive AWS OpenSearch Configuration Runner
Handles all 56 AWS OpenSearch elements with advanced presets
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_aws_opensearch_configurator import ComprehensiveAWSOpenSearchConfigurator


def load_configs(filename: str = "aws_opensearch_configs.json") -> dict:
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
    print("COMPREHENSIVE AWS OPENSEARCH CONFIGURATION MENU")
    print("="*80)
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")


def run_configuration(config_name: str = "development_cluster", headless: bool = False):
    """Run a specific AWS OpenSearch configuration"""
    print(f"[INFO] Running comprehensive AWS OpenSearch configuration: {config_name}")
    
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
        
        configurator = ComprehensiveAWSOpenSearchConfigurator(page)
        
        if configurator.navigate_to_aws_opensearch_config():
            if configurator.apply_aws_opensearch_configuration(selected_config['settings']):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"comprehensive_aws_opensearch_{config_name}_url.txt"
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
            print("[ERROR] Failed to navigate to AWS OpenSearch configuration")
        
        browser.close()
        return None


def analyze_configuration(config: dict):
    """Analyze a configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Configuration: {config['name']}")
    print(f"[INFO] Description: {config['description']}")
    print(f"[INFO] Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")
    
    settings = config.get('settings', {})
    
    # Calculate totals
    nodes = settings.get('number_of_nodes', 0)
    storage_gb = settings.get('storage_size_gb', 0)
    data_transfer_tb = settings.get('data_transfer_tb', 0)
    search_requests = settings.get('search_requests', 0)
    indexing_requests = settings.get('indexing_requests', 0)
    
    print(f"[INFO] AWS OpenSearch Configuration:")
    print(f"  - Number of Nodes: {nodes}")
    print(f"  - Instance Type: {settings.get('instance_type', 'N/A')}")
    print(f"  - Storage Size: {storage_gb} GB")
    print(f"  - Data Transfer: {data_transfer_tb} TB")
    print(f"  - Search Requests: {search_requests:,}")
    print(f"  - Indexing Requests: {indexing_requests:,}")
    
    # Calculate resource metrics
    if nodes > 0 and storage_gb > 0:
        total_storage = nodes * storage_gb
        print(f"  - Total Cluster Storage: {total_storage} GB")
    
    if search_requests > 0 and indexing_requests > 0:
        total_requests = search_requests + indexing_requests
        print(f"  - Total Requests: {total_requests:,}")
        print(f"  - Search/Index Ratio: {search_requests/indexing_requests:.2f}")


def main():
    """Test the comprehensive AWS OpenSearch configurator"""
    print("[INFO] Comprehensive AWS OpenSearch Configuration Runner")
    print("[INFO] Handles all 56 AWS OpenSearch configuration elements")
    
    # Load and show available configurations
    configs = load_configs()
    if not configs:
        return
    
    print_config_menu(configs)
    
    # Analyze a few key configurations
    print(f"\n{'='*80}")
    print("CONFIGURATION ANALYSIS")
    print(f"{'='*80}")
    
    key_configs = ['development_cluster', 'small_production', 'medium_production', 'analytics_cluster']
    for config_name in key_configs:
        if config_name in configs:
            analyze_configuration(configs[config_name])
    
    # Run default configuration
    print(f"\n[INFO] Running default configuration: development_cluster")
    url = run_configuration("development_cluster", headless=False)
    
    if url:
        print(f"\n[SUCCESS] Configuration completed successfully!")
        print(f"[URL] Your comprehensive AWS OpenSearch estimate URL: {url}")
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
