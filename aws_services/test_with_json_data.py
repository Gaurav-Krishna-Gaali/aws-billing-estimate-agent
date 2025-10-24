"""
Test AWS Services with JSON Data from sow-analysis-Ody.json
Maps the JSON data to our existing service configurators
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import service configurators
from bedrock.aws_bedrock_configurator import BedrockConfigurator
from s3.s3_configurator import S3Configurator
from iam.comprehensive_iam_configurator import ComprehensiveIAMConfigurator
from cloudwatch.comprehensive_cloudwatch_configurator import ComprehensiveCloudWatchConfigurator


def load_json_data(file_path: str = "../sow-analysis-Ody.json") -> dict:
    """Load the JSON data from sow-analysis-Ody.json"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] JSON file {file_path} not found.")
        return {}


def map_json_to_bedrock_config(json_data: dict) -> dict:
    """Map JSON data to Bedrock configuration"""
    bedrock_service = None
    for service in json_data.get('result', {}).get('estimate', []):
        if service.get('service_name') == 'AWS Bedrock':
            bedrock_service = service
            break
    
    if not bedrock_service:
        print("[WARNING] No Bedrock service found in JSON data")
        return {}
    
    config = bedrock_service.get('configurations', {})
    
    # Map to our Bedrock configuration format
    bedrock_config = {
        'name': 'JSON Data - Bedrock Configuration',
        'description': bedrock_service.get('description', 'Bedrock configuration from JSON data'),
        'estimated_monthly_cost': f"${bedrock_service.get('estimated_yearly_price', 0) / 12:.2f}",
        'settings': {
            'input_8_text': 100,  # Default values since JSON doesn't have detailed breakdown
            'input_9_text': 8,
            'input_10_text': 1000,
            'input_11_text': 500
        }
    }
    
    print(f"[INFO] Mapped Bedrock: {config.get('ModelCallsPerMonth', 'N/A')} calls/month")
    return bedrock_config


def map_json_to_s3_config(json_data: dict) -> dict:
    """Map JSON data to S3 configuration"""
    s3_services = []
    for service in json_data.get('result', {}).get('estimate', []):
        if 'S3' in service.get('service_name', ''):
            s3_services.append(service)
    
    if not s3_services:
        print("[WARNING] No S3 services found in JSON data")
        return {}
    
    # Combine all S3 services
    total_storage = 0
    total_put_requests = 0
    total_get_requests = 0
    
    for s3_service in s3_services:
        config = s3_service.get('configurations', {})
        storage_gb = int(config.get('AverageStorage', '0').replace(' GB', ''))
        
        # Parse requests with 'k' suffix
        requests_str = config.get('PUT/GETRequestsPerMonth', '0/0')
        put_str, get_str = requests_str.split('/')
        put_requests = int(put_str.replace('k', '000').replace('K', '000'))
        get_requests = int(get_str.replace('k', '000').replace('K', '000'))
        
        total_storage += storage_gb
        total_put_requests += put_requests
        total_get_requests += get_requests
    
    s3_config = {
        'name': 'JSON Data - S3 Configuration',
        'description': f'Combined S3 configuration from {len(s3_services)} buckets',
        'estimated_monthly_cost': f"${sum(s.get('estimated_yearly_price', 0) for s in s3_services) / 12:.2f}",
        'settings': {
            'storage_gb': total_storage,
            'put_requests': total_put_requests,
            'get_requests': total_get_requests,
            's3_select_returned_gb': total_storage // 10,  # Estimate
            's3_select_scanned_gb': total_storage // 5   # Estimate
        }
    }
    
    print(f"[INFO] Mapped S3: {total_storage} GB storage, {total_put_requests:,} PUT, {total_get_requests:,} GET requests")
    return s3_config


def map_json_to_iam_config(json_data: dict) -> dict:
    """Map JSON data to IAM configuration"""
    iam_service = None
    for service in json_data.get('result', {}).get('estimate', []):
        if service.get('service_name') == 'IAM':
            iam_service = service
            break
    
    if not iam_service:
        print("[WARNING] No IAM service found in JSON data")
        return {}
    
    config = iam_service.get('configurations', {})
    users_roles = int(config.get('Users/Roles', '10'))
    managed_policies = int(config.get('ManagedPolicies', '5'))
    
    iam_config = {
        'name': 'JSON Data - IAM Configuration',
        'description': iam_service.get('description', 'IAM configuration from JSON data'),
        'estimated_monthly_cost': f"${iam_service.get('estimated_yearly_price', 0) / 12:.2f}",
        'settings': {
            'accounts_to_monitor': 1,
            'average_roles_per_account': users_roles,
            'average_users_per_account': users_roles * 2,  # Estimate
            'analyzers_per_account': 1,
            'check_no_new_access_requests': users_roles * 10,
            'check_access_not_granted_requests': users_roles * 5,
            'resources_to_monitor': users_roles * 20
        }
    }
    
    print(f"[INFO] Mapped IAM: {users_roles} users/roles, {managed_policies} policies")
    return iam_config


def map_json_to_cloudwatch_config(json_data: dict) -> dict:
    """Map JSON data to CloudWatch configuration"""
    cloudwatch_service = None
    for service in json_data.get('result', {}).get('estimate', []):
        if service.get('service_name') == 'CloudWatch':
            cloudwatch_service = service
            break
    
    if not cloudwatch_service:
        print("[WARNING] No CloudWatch service found in JSON data")
        return {}
    
    config = cloudwatch_service.get('configurations', {})
    metrics = config.get('Metrics', 'Custom metrics 50/month')
    alarms = int(config.get('Alarms', '20'))
    logs_storage = int(config.get('LogsStoragePerMonth', '50 GB').replace(' GB', ''))
    logs_ingestion = int(config.get('LogsIngestionPerMonth', '15 GB').replace(' GB', ''))
    
    cloudwatch_config = {
        'name': 'JSON Data - CloudWatch Configuration',
        'description': cloudwatch_service.get('description', 'CloudWatch configuration from JSON data'),
        'estimated_monthly_cost': f"${cloudwatch_service.get('estimated_yearly_price', 0) / 12:.2f}",
        'settings': {
            'metrics_count': 50,  # From metrics description
            'get_metric_data_requests': 1000,
            'get_metric_widget_image_requests': 100,
            'other_api_requests': 500,
            'standard_logs_data_ingested_gb': logs_ingestion,
            'infrequent_logs_data_ingested_gb': logs_storage - logs_ingestion,
            'dashboards_count': 5,
            'standard_resolution_alarms': alarms,
            'high_resolution_alarms': alarms // 4,
            'composite_alarms': alarms // 10,
            'canary_runs': 50,
            'lambda_functions': 10,
            'lambda_requests_per_function': 1000,
            'rum_monthly_visitors': 10000,
            'rum_events_per_visit': 5,
            'rum_event_percentage': 70,
            'synthetics_monitored_resources': 3,
            'synthetics_city_networks': 2,
            'xray_incoming_requests': 50000,
            'xray_outgoing_requests': 25000,
            'slo_count': 5,
            'slo_metric_period_minutes': 5
        }
    }
    
    print(f"[INFO] Mapped CloudWatch: {metrics}, {alarms} alarms, {logs_storage} GB logs")
    return cloudwatch_config


def test_bedrock_with_json():
    """Test Bedrock configuration with JSON data"""
    print("\n" + "="*60)
    print("TESTING BEDROCK WITH JSON DATA")
    print("="*60)
    
    json_data = load_json_data()
    if not json_data:
        return None
    
    bedrock_config = map_json_to_bedrock_config(json_data)
    if not bedrock_config:
        return None
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = BedrockConfigurator(page)
        
        if configurator.navigate_to_bedrock_config():
            if configurator.configure_bedrock(bedrock_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] Bedrock configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    with open("bedrock_json_test_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to bedrock_json_test_url.txt")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None


def test_s3_with_json():
    """Test S3 configuration with JSON data"""
    print("\n" + "="*60)
    print("TESTING S3 WITH JSON DATA")
    print("="*60)
    
    json_data = load_json_data()
    if not json_data:
        return None
    
    s3_config = map_json_to_s3_config(json_data)
    if not s3_config:
        return None
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = S3Configurator(page)
        
        if configurator.navigate_to_s3_config():
            if configurator.apply_s3_configuration(s3_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] S3 configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    with open("s3_json_test_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to s3_json_test_url.txt")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None


def test_iam_with_json():
    """Test IAM configuration with JSON data"""
    print("\n" + "="*60)
    print("TESTING IAM WITH JSON DATA")
    print("="*60)
    
    json_data = load_json_data()
    if not json_data:
        return None
    
    iam_config = map_json_to_iam_config(json_data)
    if not iam_config:
        return None
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveIAMConfigurator(page)
        
        if configurator.navigate_to_iam_config():
            if configurator.apply_iam_configuration(iam_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] IAM configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    with open("iam_json_test_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to iam_json_test_url.txt")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None


def test_cloudwatch_with_json():
    """Test CloudWatch configuration with JSON data"""
    print("\n" + "="*60)
    print("TESTING CLOUDWATCH WITH JSON DATA")
    print("="*60)
    
    json_data = load_json_data()
    if not json_data:
        return None
    
    cloudwatch_config = map_json_to_cloudwatch_config(json_data)
    if not cloudwatch_config:
        return None
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveCloudWatchConfigurator(page)
        
        if configurator.navigate_to_cloudwatch_config():
            if configurator.apply_cloudwatch_configuration(cloudwatch_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] CloudWatch configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    with open("cloudwatch_json_test_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to cloudwatch_json_test_url.txt")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None


def main():
    """Main function to test all services with JSON data"""
    print("[INFO] Testing AWS Services with JSON Data from sow-analysis-Ody.json")
    print("[INFO] Project: Ody | Budget: $10,000/year")
    
    # Load and analyze JSON data
    json_data = load_json_data()
    if not json_data:
        print("[ERROR] Could not load JSON data")
        return
    
    result = json_data.get('result', {})
    project_name = result.get('projectName', 'Unknown')
    budget = result.get('maxAnnualBudgetUSD', 0)
    services = result.get('estimate', [])
    
    print(f"\n[INFO] Project: {project_name}")
    print(f"[INFO] Budget: ${budget:,}/year")
    print(f"[INFO] Services in JSON: {len(services)}")
    
    # Show available services
    service_names = [s.get('service_name') for s in services]
    print(f"[INFO] Available services: {', '.join(service_names)}")
    
    # Test each service that we have configurators for
    results = {}
    
    # Test Bedrock
    if 'AWS Bedrock' in service_names:
        results['bedrock'] = test_bedrock_with_json()
    
    # Test S3
    s3_services = [s for s in service_names if 'S3' in s]
    if s3_services:
        results['s3'] = test_s3_with_json()
    
    # Test IAM
    if 'IAM' in service_names:
        results['iam'] = test_iam_with_json()
    
    # Test CloudWatch
    if 'CloudWatch' in service_names:
        results['cloudwatch'] = test_cloudwatch_with_json()
    
    # Summary
    print(f"\n{'='*60}")
    print("JSON DATA TESTING SUMMARY")
    print(f"{'='*60}")
    
    for service, url in results.items():
        if url:
            print(f"[SUCCESS] {service.upper()}: {url}")
        else:
            print(f"[FAILED] {service.upper()}: Configuration failed")
    
    print(f"\n[INFO] JSON data testing completed!")


if __name__ == "__main__":
    main()
