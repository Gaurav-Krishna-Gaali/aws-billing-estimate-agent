"""
AWS Service Configuration Runner
Main script to run configurations for different AWS services
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
from waf.comprehensive_waf_configurator import ComprehensiveWAFConfigurator
from api_gateway.comprehensive_api_gateway_configurator import ComprehensiveAPIGatewayConfigurator
from alb.comprehensive_alb_configurator import ComprehensiveALBConfigurator
from ecs_fargate.comprehensive_ecs_fargate_configurator import ComprehensiveECSFargateConfigurator
from sqs.comprehensive_sqs_configurator import ComprehensiveSQSConfigurator
from aws_shield.comprehensive_aws_shield_configurator import ComprehensiveAWSShieldConfigurator
from ec2.comprehensive_ec2_configurator import ComprehensiveEC2Configurator
from aws_lambda.comprehensive_aws_lambda_configurator import ComprehensiveAWSLambdaConfigurator
from vpc.comprehensive_vpc_configurator import ComprehensiveVPCConfigurator
from security_groups.comprehensive_security_groups_configurator import ComprehensiveSecurityGroupsConfigurator

def load_service_configs(service: str) -> dict:
    """Load configurations for a specific service"""
    config_file = f"{service}/{service}_configs.json"
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Configuration file {config_file} not found.")
        return {}

def print_service_menu(service: str, configs: dict):
    """Print configuration menu for a service"""
    print(f"\n{'='*60}")
    print(f"{service.upper()} CONFIGURATION MENU")
    print(f"{'='*60}")
    
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        config = configs[config_id]
        print(f"\n{i}. {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Estimated Cost: {config.get('estimated_monthly_cost', 'TBD')}")

def run_bedrock_config(config_name: str = "light_usage", headless: bool = False):
    """Run Bedrock configuration"""
    print(f"[INFO] Running Bedrock configuration: {config_name}")
    
    configs = load_service_configs("bedrock")
    if not configs or config_name not in configs:
        print(f"[ERROR] Bedrock configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = BedrockConfigurator(page)
        
        if configurator.navigate_to_bedrock_config():
            # Apply configuration using the robust method
            if apply_bedrock_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Bedrock configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"bedrock_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def run_s3_config(config_name: str = "small_bucket", headless: bool = False):
    """Run S3 configuration"""
    print(f"[INFO] Running S3 configuration: {config_name}")
    
    configs = load_service_configs("s3")
    if not configs or config_name not in configs:
        print(f"[ERROR] S3 configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = S3Configurator(page)
        
        if configurator.navigate_to_s3_config():
            # Apply configuration using the robust method
            if apply_s3_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] S3 configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"s3_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def run_iam_config(config_name: str = "development_testing", headless: bool = False):
    """Run IAM configuration"""
    print(f"[INFO] Running IAM configuration: {config_name}")
    
    configs = load_service_configs("iam")
    if not configs or config_name not in configs:
        print(f"[ERROR] IAM configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveIAMConfigurator(page)
        
        if configurator.navigate_to_iam_config():
            # Apply configuration using the robust method
            if apply_iam_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] IAM configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"iam_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_bedrock_config_robust(configurator, config: dict) -> bool:
    """Apply Bedrock configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "input_8_text": "input[aria-label*='Average requests per minute']:first-of-type",
            "input_9_text": "input[aria-label*='Hours per day at this rate']:first-of-type", 
            "input_10_text": "input[aria-label*='Average input tokens per request']:first-of-type",
            "input_11_text": "input[aria-label*='Average output tokens per request']:first-of-type",
            "input_12_text": "input[aria-label*='Average requests per minute']:nth-of-type(2)",
            "input_13_text": "input[aria-label*='Hours per day at this rate']:nth-of-type(2)",
            "input_14_text": "input[aria-label*='Average input tokens per request']:nth-of-type(2)",
            "input_15_text": "input[aria-label*='Average output tokens per request']:nth-of-type(2)",
            "input_16_text": "input[aria-label*='Average requests per minute']:nth-of-type(3)",
            "input_17_text": "input[aria-label*='Hours per day at this rate']:nth-of-type(3)",
            "input_18_text": "input[aria-label*='Average input tokens per request']:nth-of-type(3)",
            "input_19_text": "input[aria-label*='Average output tokens per request']:nth-of-type(3)"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
            elif setting_id.startswith("checkbox_"):
                # Handle checkboxes
                try:
                    if "2231" in setting_id:  # Model 2 checkbox
                        checkbox_selector = "input[id*='2231']"
                    elif "2232" in setting_id:  # Model 3 checkbox
                        checkbox_selector = "input[id*='2232']"
                    else:
                        continue
                    
                    if value:
                        configurator.page.check(checkbox_selector)
                    else:
                        configurator.page.uncheck(checkbox_selector)
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set checkbox {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def apply_s3_config_robust(configurator, config: dict) -> bool:
    """Apply S3 configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "storage_gb": "input[aria-label*='S3 Standard storage Value']",
            "put_requests": "input[aria-label*='PUT, COPY, POST, LIST requests to S3 Standard Enter amount of requests']",
            "get_requests": "input[aria-label*='GET, SELECT, and all other requests from S3 Standard Enter amount of requests']",
            "s3_select_returned_gb": "input[aria-label*='Data returned by S3 Select Value']",
            "s3_select_scanned_gb": "input[aria-label*='Data scanned by S3 Select Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def apply_iam_config_robust(configurator, config: dict) -> bool:
    """Apply IAM configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "accounts_to_monitor": "input[aria-label*='Number of accounts to monitor Enter amount']",
            "average_roles_per_account": "input[aria-label*='Average roles per account Enter amount']",
            "average_users_per_account": "input[aria-label*='Average users per account Enter amount']",
            "analyzers_per_account": "input[aria-label*='Number of analyzers per account Enter amount']",
            "check_no_new_access_requests": "input[aria-label*='Number of requests to CheckNoNewAccess API Value']",
            "check_access_not_granted_requests": "input[aria-label*='Number of requests to CheckAccessNotGranted API Value']",
            "resources_to_monitor": "input[aria-label*='Number of resources to monitor Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_cloudwatch_config(config_name: str = "development_testing", headless: bool = False):
    """Run CloudWatch configuration"""
    print(f"[INFO] Running CloudWatch configuration: {config_name}")
    
    configs = load_service_configs("cloudwatch")
    if not configs or config_name not in configs:
        print(f"[ERROR] CloudWatch configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveCloudWatchConfigurator(page)
        
        if configurator.navigate_to_cloudwatch_config():
            # Apply configuration using the robust method
            if apply_cloudwatch_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] CloudWatch configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"cloudwatch_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_cloudwatch_config_robust(configurator, config: dict) -> bool:
    """Apply CloudWatch configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "metrics_count": "input[aria-label*='Number of Metrics (includes detailed and custom metrics) Enter the amount']",
            "get_metric_data_requests": "input[aria-label*='GetMetricData: Number of metrics requested Enter the amount']",
            "get_metric_widget_image_requests": "input[aria-label*='GetMetricWidgetImage: Number of metrics requested Enter the amount']",
            "other_api_requests": "input[aria-label*='Number of other API requests Enter the amount']",
            "database_insights_vcpus": "input[aria-label*='Number of vCPUs monitored by Database Insights Value']",
            "database_insights_aurora_acus": "input[aria-label*='Number of Aurora Capacity Units (ACUs) monitored by Database Insights Value']",
            "standard_logs_data_ingested_gb": "input[aria-label*='Standard Logs: Data Ingested Value']",
            "infrequent_logs_data_ingested_gb": "input[aria-label*='Infrequent Access Logs: Data Ingested Value']",
            "standard_logs_delivered_gb": "input[aria-label*='Standard Logs Delivered to CloudWatch Logs Value']",
            "infrequent_logs_delivered_gb": "input[aria-label*='Infrequent Access Logs Delivered to CloudWatch Logs Value']",
            "logs_delivered_to_s3_gb": "input[aria-label*='Logs Delivered to S3: Data Ingested Value']",
            "logs_data_scanned_gb": "input[aria-label*='Expected Logs Data scanned Value']",
            "dashboards_count": "input[aria-label*='Number of Dashboards Enter the amount']",
            "standard_resolution_alarms": "input[aria-label*='Number of Standard Resolution Alarm Metrics Enter the amount']",
            "high_resolution_alarms": "input[aria-label*='Number of High Resolution Alarm Metrics Enter the amount']",
            "composite_alarms": "input[aria-label*='Number of composite alarms Enter the amount']",
            "metrics_insights_alarms": "input[aria-label*='Number of alarms defined with a Metrics Insights query Enter the amount']",
            "metrics_scanned_per_query": "input[aria-label*='Average number of metrics scanned by each Metrics Insights query Enter the amount']",
            "canary_runs": "input[aria-label*='Number of Canary runs Enter the amount']",
            "contributor_insights_cloudwatch_rules": "input[aria-label*='Number of Contributor Insights rules for CloudWatch Enter the amount']",
            "contributor_insights_cloudwatch_events": "input[aria-label*='Total number of matched log events for CloudWatch Value']",
            "contributor_insights_dynamodb_rules": "input[aria-label*='Number of Contributor Insights rules for DynamoDB Enter the amount']",
            "contributor_insights_dynamodb_events": "input[aria-label*='Total number of events for DynamoDB Value']",
            "lambda_functions": "input[aria-label*='Number of Lambda functions Enter the amount']",
            "lambda_requests_per_function": "input[aria-label*='Number of requests per function Value']",
            "rum_monthly_visitors": "input[aria-label*='Monthly visitors to your web application Enter the amount']",
            "rum_events_per_visit": "input[aria-label*='Number of RUM events per visit Enter the amount']",
            "rum_event_percentage": "input[aria-label*='Percentage of RUM event Enter the amount']",
            "synthetics_monitored_resources": "input[aria-label*='Number of monitored resources Value']",
            "synthetics_city_networks": "input[aria-label*='Number of city-networks to be monitored Value']",
            "xray_incoming_requests": "input[aria-label*='Volume of incoming requests Value']",
            "xray_outgoing_requests": "input[aria-label*='Volume of outgoing requests to dependencies Value']",
            "slo_count": "input[aria-label*='Number of Service level objectives (SLO) Enter the amount']",
            "slo_metric_period_minutes": "input[aria-label*='Service level indicator metric period (minutes) Enter the Service level indicator metric period in minutes']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_waf_config(config_name: str = "development_testing", headless: bool = False):
    """Run WAF configuration"""
    print(f"[INFO] Running WAF configuration: {config_name}")
    
    configs = load_service_configs("waf")
    if not configs or config_name not in configs:
        print(f"[ERROR] WAF configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveWAFConfigurator(page)
        
        if configurator.navigate_to_waf_config():
            # Apply configuration using the robust method
            if apply_waf_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] WAF configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"waf_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_waf_config_robust(configurator, config: dict) -> bool:
    """Apply WAF configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "web_acls": "input[aria-label*='Number of Web Access Control Lists (Web ACLs) utilized Value']",
            "rules_per_web_acl": "input[aria-label*='Number of Rules added per Web ACL Value']",
            "rule_groups_per_web_acl": "input[aria-label*='Number of Rule Groups per Web ACL Value']",
            "rules_inside_rule_group": "input[aria-label*='Number of Rules inside each Rule Group Value']",
            "managed_rule_groups_per_web_acl": "input[aria-label*='Number of Managed Rule Groups per Web ACL Value']",
            "web_requests_received": "input[aria-label*='Number of web requests received across all web ACLs Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_api_gateway_config(config_name: str = "development_testing", headless: bool = False):
    """Run API Gateway configuration"""
    print(f"[INFO] Running API Gateway configuration: {config_name}")
    
    configs = load_service_configs("api_gateway")
    if not configs or config_name not in configs:
        print(f"[ERROR] API Gateway configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveAPIGatewayConfigurator(page)
        
        if configurator.navigate_to_api_gateway_config():
            # Apply configuration using the robust method
            if apply_api_gateway_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] API Gateway configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"api_gateway_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_api_gateway_config_robust(configurator, config: dict) -> bool:
    """Apply API Gateway configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "http_api_requests": "input[aria-label*='Requests Value'][placeholder*='HTTP API requests']",
            "http_api_request_size_kb": "input[aria-label*='Average size of each request Value']",
            "rest_api_requests": "input[aria-label*='Requests Value'][placeholder*='REST API requests']",
            "websocket_messages": "input[aria-label*='Messages Value'][placeholder*='WebSocket messages']",
            "websocket_message_size_kb": "input[aria-label*='Average message size Value']",
            "websocket_connection_duration_seconds": "input[aria-label*='Average connection duration Value']",
            "websocket_connection_rate": "input[aria-label*='Average connection rate Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_alb_config(config_name: str = "development_testing", headless: bool = False):
    """Run ALB configuration"""
    print(f"[INFO] Running ALB configuration: {config_name}")
    
    configs = load_service_configs("alb")
    if not configs or config_name not in configs:
        print(f"[ERROR] ALB configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveALBConfigurator(page)
        
        if configurator.navigate_to_alb_config():
            # Apply configuration using the robust method
            if apply_alb_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] ALB configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"alb_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_alb_config_robust(configurator, config: dict) -> bool:
    """Apply ALB configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "alb_count": "input[aria-label*='Number of Application Load Balancers']",
            "alb_lambda_processed_bytes": "input[aria-label*='Processed bytes (Lambda functions as targets) Value']",
            "alb_ec2_processed_bytes": "input[aria-label*='Processed bytes (EC2 Instances and IP addresses as targets) Value']",
            "alb_new_connections": "input[aria-label*='Average number of new connections per ALB Value']",
            "alb_connection_duration": "input[aria-label*='Average connection duration Value']",
            "alb_requests_per_second": "input[aria-label*='Average number of requests per second per ALB Enter amount']",
            "alb_rule_evaluations": "input[aria-label*='Average number of rule evaluations per request Enter amount']",
            "nlb_count": "input[aria-label*='Number of Network Load Balancers']",
            "nlb_tcp_processed_bytes": "input[aria-label*='Processed bytes per NLB for TCP Value']",
            "nlb_tcp_connections": "input[aria-label*='Average number of new TCP connections Value']",
            "nlb_tcp_connection_duration": "input[aria-label*='Average TCP connection duration Value']",
            "nlb_udp_processed_bytes": "input[aria-label*='Processed bytes per NLB for UDP Value']",
            "nlb_udp_flows": "input[aria-label*='Average number of new UDP Flows Value']",
            "nlb_udp_flow_duration": "input[aria-label*='Average UDP Flow duration Value']",
            "nlb_tls_processed_bytes": "input[aria-label*='Processed bytes per NLB for TLS Value']",
            "nlb_tls_connections": "input[aria-label*='Average number of new TLS connections Value']",
            "nlb_tls_connection_duration": "input[aria-label*='Average TLS connection duration Value']",
            "glb_availability_zones": "input[aria-label*='Number of Availability Zones that Gateway Load Balancer is deployed to']",
            "glb_processed_bytes": "input[aria-label*='Total processed bytes Value']",
            "glb_connections_flows": "input[aria-label*='Average number of new connections/flows Value']",
            "glb_connection_flow_duration": "input[aria-label*='Average connection/flow duration Value']",
            "glb_endpoints": "input[aria-label*='Number of Gateway Load Balancer Endpoints']",
            "clb_count": "input[aria-label*='Number of Classic Load Balancers']",
            "clb_processed_bytes": "input[aria-label*='Processed bytes per CLB Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_ecs_fargate_config(config_name: str = "development_testing", headless: bool = False):
    """Run ECS Fargate configuration"""
    print(f"[INFO] Running ECS Fargate configuration: {config_name}")
    
    configs = load_service_configs("ecs_fargate")
    if not configs or config_name not in configs:
        print(f"[ERROR] ECS Fargate configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveECSFargateConfigurator(page)
        
        if configurator.navigate_to_ecs_fargate_config():
            # Apply configuration using the robust method
            if apply_ecs_fargate_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] ECS Fargate configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"ecs_fargate_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_ecs_fargate_config_robust(configurator, config: dict) -> bool:
    """Apply ECS Fargate configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "number_of_tasks": "input[aria-label*='Number of tasks or pods Value']",
            "average_duration_minutes": "input[aria-label*='Average duration Value']",
            "memory_gb": "input[aria-label*='Amount of memory allocated Value']",
            "ephemeral_storage_gb": "input[aria-label*='Amount of ephemeral storage allocated for Amazon ECS Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_sqs_config(config_name: str = "development_testing", headless: bool = False):
    """Run SQS configuration"""
    print(f"[INFO] Running SQS configuration: {config_name}")
    
    configs = load_service_configs("sqs")
    if not configs or config_name not in configs:
        print(f"[ERROR] SQS configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveSQSConfigurator(page)
        
        if configurator.navigate_to_sqs_config():
            # Apply configuration using the robust method
            if apply_sqs_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] SQS configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"sqs_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_sqs_config_robust(configurator, config: dict) -> bool:
    """Apply SQS configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "standard_queue_requests": "input[aria-label*='Standard queue requests Value']",
            "fifo_queue_requests": "input[aria-label*='FIFO queue requests Value']",
            "fair_queue_requests": "input[aria-label*='Fair queue requests Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        # Handle data transfer fields (they have the same aria-label)
        if 'inbound_data_transfer_tb' in config:
            try:
                inbound_fields = configurator.page.query_selector_all("input[aria-label*='Enter Amount Enter amount']")
                if len(inbound_fields) > 0:
                    inbound_fields[0].fill(str(config['inbound_data_transfer_tb']))
                    print(f"[OK] Set inbound_data_transfer_tb = {config['inbound_data_transfer_tb']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not set inbound_data_transfer_tb: {e}")
        
        if 'outbound_data_transfer_tb' in config:
            try:
                outbound_fields = configurator.page.query_selector_all("input[aria-label*='Enter Amount Enter amount']")
                if len(outbound_fields) > 1:
                    outbound_fields[1].fill(str(config['outbound_data_transfer_tb']))
                    print(f"[OK] Set outbound_data_transfer_tb = {config['outbound_data_transfer_tb']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not set outbound_data_transfer_tb: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_aws_shield_config(config_name: str = "development_testing", headless: bool = False):
    """Run AWS Shield configuration"""
    print(f"[INFO] Running AWS Shield configuration: {config_name}")
    
    configs = load_service_configs("aws_shield")
    if not configs or config_name not in configs:
        print(f"[ERROR] AWS Shield configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveAWSShieldConfigurator(page)
        
        if configurator.navigate_to_aws_shield_config():
            # Apply configuration using the robust method
            if apply_aws_shield_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] AWS Shield configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"aws_shield_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_aws_shield_config_robust(configurator, config: dict) -> bool:
    """Apply AWS Shield configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "cloudfront_usage": "input[aria-label*='Cloud Front Usage Value']",
            "elb_usage": "input[aria-label*='Elastic Load Balancing (ELB) Usage Value']",
            "elastic_ip_usage": "input[aria-label*='Elastic IP Usage Value']",
            "global_accelerator_usage": "input[aria-label*='Global Accelerator Usage Value']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_ec2_config(config_name: str = "development_environment", headless: bool = False):
    """Run EC2 configuration"""
    print(f"[INFO] Running EC2 configuration: {config_name}")
    
    configs = load_service_configs("ec2")
    if not configs or config_name not in configs:
        print(f"[ERROR] EC2 configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveEC2Configurator(page)
        
        if configurator.navigate_to_ec2_config():
            # Apply configuration using the robust method
            if apply_ec2_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] EC2 configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"ec2_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_ec2_config_robust(configurator, config: dict) -> bool:
    """Apply EC2 configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "number_of_instances": "input[aria-label*='Number of instances Enter amount']",
            "storage_amount_gb": "input[aria-label*='Storage amount Value']",
            "iops_per_volume": "input[aria-label*='General Purpose SSD (gp3) - IOPS Enter amount of IOPS per volume']",
            "throughput_mbps": "input[aria-label*='General Purpose SSD (gp3) - Throughput Value']",
            "licensing_cost": "input[aria-label*='Enter any placeholder cost such as Licensing to add to your estimate']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        # Handle monitoring checkbox
        if 'enable_monitoring' in config and config['enable_monitoring']:
            try:
                monitoring_checkbox = configurator.page.locator("input[aria-label*='Enable monitoring']")
                if monitoring_checkbox.count() > 0 and not monitoring_checkbox.first.is_checked():
                    monitoring_checkbox.first.check()
                    print(f"[OK] Enabled monitoring")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not enable monitoring: {e}")
        
        # Handle data transfer fields (they have the same aria-label)
        if 'inbound_data_transfer_tb' in config:
            try:
                inbound_fields = configurator.page.query_selector_all("input[aria-label*='Enter Amount Enter amount']")
                if len(inbound_fields) > 0:
                    inbound_fields[0].fill(str(config['inbound_data_transfer_tb']))
                    print(f"[OK] Set inbound_data_transfer_tb = {config['inbound_data_transfer_tb']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not set inbound_data_transfer_tb: {e}")
        
        if 'outbound_data_transfer_tb' in config:
            try:
                outbound_fields = configurator.page.query_selector_all("input[aria-label*='Enter Amount Enter amount']")
                if len(outbound_fields) > 1:
                    outbound_fields[1].fill(str(config['outbound_data_transfer_tb']))
                    print(f"[OK] Set outbound_data_transfer_tb = {config['outbound_data_transfer_tb']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not set outbound_data_transfer_tb: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_vpc_config(config_name: str = "basic_vpc", headless: bool = False):
    """Run VPC configuration"""
    print(f"[INFO] Running VPC configuration: {config_name}")
    
    configs = load_service_configs("vpc")
    if not configs or config_name not in configs:
        print(f"[ERROR] VPC configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveVPCConfigurator(page)
        
        if configurator.navigate_to_vpc_config():
            # Apply configuration using the robust method
            if apply_vpc_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] VPC configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"vpc_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_vpc_config_robust(configurator, config: dict) -> bool:
    """Apply VPC configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "number_of_vpcs": "input[aria-label*='Number of VPCs']",
            "number_of_subnets": "input[aria-label*='Number of subnets']",
            "number_of_internet_gateways": "input[aria-label*='Number of Internet Gateways']",
            "number_of_nat_gateways": "input[aria-label*='Number of NAT Gateways']",
            "number_of_vpc_endpoints": "input[aria-label*='Number of VPC Endpoints']",
            "number_of_route_tables": "input[aria-label*='Number of Route Tables']",
            "number_of_security_groups": "input[aria-label*='Number of Security Groups']",
            "number_of_network_acls": "input[aria-label*='Number of Network ACLs']",
            "data_processed_gb": "input[aria-label*='Data processed']",
            "endpoint_hours": "input[aria-label*='Endpoint hours']",
            "nat_gateway_hours": "input[aria-label*='NAT Gateway hours']",
            "vpc_peering_hours": "input[aria-label*='VPC Peering hours']",
            "transit_gateway_hours": "input[aria-label*='Transit Gateway hours']",
            "vpn_connection_hours": "input[aria-label*='VPN Connection hours']",
            "vpn_tunnel_hours": "input[aria-label*='VPN Tunnel hours']",
            "data_transfer_gb": "input[aria-label*='Data transfer']",
            "availability_zones": "input[aria-label*='Availability Zones']",
            "cidr_block": "input[aria-label*='CIDR block']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        # Handle boolean settings (checkboxes)
        boolean_settings = [
            'enable_dns_hostnames', 'enable_dns_resolution', 'enable_classic_link',
            'enable_vpc_flow_logs', 'enable_vpc_endpoints', 'enable_nat_gateway',
            'enable_internet_gateway', 'enable_vpn_connection'
        ]
        
        for setting in boolean_settings:
            if setting in config:
                try:
                    checkbox = configurator.page.locator(f"input[aria-label*='{setting.replace('_', ' ').title()}']")
                    if checkbox.count() > 0:
                        if config[setting] and not checkbox.first.is_checked():
                            checkbox.first.check()
                            print(f"[OK] Enabled {setting}")
                            settings_applied += 1
                        elif not config[setting] and checkbox.first.is_checked():
                            checkbox.first.uncheck()
                            print(f"[OK] Disabled {setting}")
                            settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not configure {setting}: {e}")
        
        # Handle region selection
        if 'region' in config:
            try:
                region_select = configurator.page.locator("select[aria-label*='Region']")
                if region_select.count() > 0:
                    region_select.first.select_option(value=config['region'])
                    print(f"[OK] Selected region: {config['region']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not select region: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def run_security_groups_config(config_name: str = "basic_security_groups", headless: bool = False):
    """Run Security Groups configuration"""
    print(f"[INFO] Running Security Groups configuration: {config_name}")
    
    configs = load_service_configs("security_groups")
    if not configs or config_name not in configs:
        print(f"[ERROR] Security Groups configuration '{config_name}' not found.")
        return None
    
    selected_config = configs[config_name]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        configurator = ComprehensiveSecurityGroupsConfigurator(page)
        
        if configurator.navigate_to_security_groups_config():
            # Apply configuration using the robust method
            if apply_security_groups_config_robust(configurator, selected_config):
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] Security Groups configuration completed!")
                    print(f"[INFO] Configuration: {selected_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL
                    filename = f"security_groups_{config_name}_url.txt"
                    with open(filename, "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to {filename}")
                    
                    browser.close()
                    return url
        
        browser.close()
        return None

def apply_security_groups_config_robust(configurator, config: dict) -> bool:
    """Apply Security Groups configuration using robust selectors"""
    try:
        print(f"\n[INFO] Applying: {config['name']}")
        
        # Set description
        if 'description' in config:
            try:
                configurator.page.fill("input[aria-label*='Description']", config['description'])
                print(f"[OK] Set description")
            except:
                print("[WARNING] Could not set description")
        
        # Apply settings using robust selectors
        settings_map = {
            "number_of_security_groups": "input[aria-label*='Number of Security Groups']",
            "number_of_inbound_rules": "input[aria-label*='Number of Inbound Rules']",
            "number_of_outbound_rules": "input[aria-label*='Number of Outbound Rules']",
            "number_of_custom_rules": "input[aria-label*='Number of Custom Rules']",
            "number_of_http_rules": "input[aria-label*='Number of HTTP Rules']",
            "number_of_https_rules": "input[aria-label*='Number of HTTPS Rules']",
            "number_of_ssh_rules": "input[aria-label*='Number of SSH Rules']",
            "number_of_rdp_rules": "input[aria-label*='Number of RDP Rules']",
            "number_of_custom_tcp_rules": "input[aria-label*='Number of Custom TCP Rules']",
            "number_of_custom_udp_rules": "input[aria-label*='Number of Custom UDP Rules']",
            "number_of_icmp_rules": "input[aria-label*='Number of ICMP Rules']",
            "data_processed_gb": "input[aria-label*='Data Processed']",
            "rules_per_security_group": "input[aria-label*='Rules per Security Group']",
            "custom_ports_count": "input[aria-label*='Custom Ports Count']",
            "port_ranges_count": "input[aria-label*='Port Ranges Count']",
            "default_port": "input[aria-label*='Default Port']",
            "source_ip_range": "input[aria-label*='Source IP Range']"
        }
        
        settings_applied = 0
        for setting_id, value in config['settings'].items():
            if setting_id in settings_map:
                selector = settings_map[setting_id]
                try:
                    configurator.page.fill(selector, str(value))
                    print(f"[OK] Set {setting_id} = {value}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {setting_id}: {e}")
        
        # Handle boolean settings (checkboxes)
        boolean_settings = [
            'enable_http_access', 'enable_https_access', 'enable_ssh_access',
            'enable_rdp_access', 'enable_custom_tcp', 'enable_custom_udp',
            'enable_icmp', 'enable_all_traffic', 'enable_restricted_access',
            'enable_web_server_access', 'enable_database_access', 'enable_load_balancer_access'
        ]
        
        for setting in boolean_settings:
            if setting in config['settings']:
                try:
                    checkbox = configurator.page.locator(f"input[aria-label*='{setting.replace('_', ' ').title()}']")
                    if checkbox.count() > 0:
                        if config['settings'][setting] and not checkbox.first.is_checked():
                            checkbox.first.check()
                            print(f"[OK] Enabled {setting}")
                            settings_applied += 1
                        elif not config['settings'][setting] and checkbox.first.is_checked():
                            checkbox.first.uncheck()
                            print(f"[OK] Disabled {setting}")
                            settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not configure {setting}: {e}")
        
        # Handle protocol selection
        if 'default_protocol' in config['settings']:
            try:
                protocol_select = configurator.page.locator("select[aria-label*='Protocol']")
                if protocol_select.count() > 0:
                    protocol_select.first.select_option(value=config['settings']['default_protocol'])
                    print(f"[OK] Selected protocol: {config['settings']['default_protocol']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not select protocol: {e}")
        
        # Handle region selection
        if 'region' in config['settings']:
            try:
                region_select = configurator.page.locator("select[aria-label*='Region']")
                if region_select.count() > 0:
                    region_select.first.select_option(value=config['settings']['region'])
                    print(f"[OK] Selected region: {config['settings']['region']}")
                    settings_applied += 1
            except Exception as e:
                print(f"[WARNING] Could not select region: {e}")
        
        print(f"[OK] Applied {settings_applied} settings successfully")
        return settings_applied > 0
        
    except Exception as e:
        print(f"[ERROR] Failed to apply config: {e}")
        return False

def main():
    """Main function"""
    print("[INFO] AWS Service Configuration Runner")
    print("[INFO] Available services: bedrock, s3, iam, cloudwatch, waf, api_gateway, alb, ecs_fargate, sqs, aws_shield, ec2, aws_lambda, vpc, security_groups")
    
    # Show available services and configurations
    services = ["bedrock", "s3", "iam", "cloudwatch", "waf", "api_gateway", "alb", "ecs_fargate", "sqs", "aws_shield", "ec2", "aws_lambda", "vpc", "security_groups"]
    
    for service in services:
        configs = load_service_configs(service)
        if configs:
            print_service_menu(service, configs)
    
    # Run default configurations
    print(f"\n[INFO] Running default configurations...")
    
    # Run Bedrock
    bedrock_url = run_bedrock_config("light_usage", headless=False)
    
    # Run S3
    s3_url = run_s3_config("small_bucket", headless=False)
    
    # Run IAM
    iam_url = run_iam_config("development_testing", headless=False)
    
    # Run CloudWatch
    cloudwatch_url = run_cloudwatch_config("development_testing", headless=False)
    
    # Run WAF
    waf_url = run_waf_config("development_testing", headless=False)
    
    # Run API Gateway
    api_gateway_url = run_api_gateway_config("development_testing", headless=False)
    
    # Run ALB
    alb_url = run_alb_config("development_testing", headless=False)
    
    # Run ECS Fargate
    ecs_fargate_url = run_ecs_fargate_config("development_testing", headless=False)
    
    # Run SQS
    sqs_url = run_sqs_config("development_testing", headless=False)
    
    # Run AWS Shield
    aws_shield_url = run_aws_shield_config("development_testing", headless=False)
    
    # Run EC2
    ec2_url = run_ec2_config("development_environment", headless=False)
    
    # Run AWS Lambda
    aws_lambda_url = run_aws_lambda_config("development_testing", headless=False)
    
    # Run VPC
    vpc_url = run_vpc_config("basic_vpc", headless=False)
    
    # Run Security Groups
    security_groups_url = run_security_groups_config("basic_security_groups", headless=False)
    
    # Summary
    print(f"\n{'='*60}")
    print("CONFIGURATION SUMMARY")
    print(f"{'='*60}")
    
    if bedrock_url:
        print(f"[SUCCESS] Bedrock: {bedrock_url}")
    else:
        print(f"[FAILED] Bedrock configuration failed")
    
    if s3_url:
        print(f"[SUCCESS] S3: {s3_url}")
    else:
        print(f"[FAILED] S3 configuration failed")
    
    if iam_url:
        print(f"[SUCCESS] IAM: {iam_url}")
    else:
        print(f"[FAILED] IAM configuration failed")
    
    if cloudwatch_url:
        print(f"[SUCCESS] CloudWatch: {cloudwatch_url}")
    else:
        print(f"[FAILED] CloudWatch configuration failed")
    
    if waf_url:
        print(f"[SUCCESS] WAF: {waf_url}")
    else:
        print(f"[FAILED] WAF configuration failed")
    
    if api_gateway_url:
        print(f"[SUCCESS] API Gateway: {api_gateway_url}")
    else:
        print(f"[FAILED] API Gateway configuration failed")
    
    if alb_url:
        print(f"[SUCCESS] ALB: {alb_url}")
    else:
        print(f"[FAILED] ALB configuration failed")
    
    if ecs_fargate_url:
        print(f"[SUCCESS] ECS Fargate: {ecs_fargate_url}")
    else:
        print(f"[FAILED] ECS Fargate configuration failed")
    
    if sqs_url:
        print(f"[SUCCESS] SQS: {sqs_url}")
    else:
        print(f"[FAILED] SQS configuration failed")
    
    if aws_shield_url:
        print(f"[SUCCESS] AWS Shield: {aws_shield_url}")
    else:
        print(f"[FAILED] AWS Shield configuration failed")
    
    if ec2_url:
        print(f"[SUCCESS] EC2: {ec2_url}")
    else:
        print(f"[FAILED] EC2 configuration failed")
    
    if aws_lambda_url:
        print(f"[SUCCESS] AWS Lambda: {aws_lambda_url}")
    else:
        print(f"[FAILED] AWS Lambda configuration failed")
    
    if vpc_url:
        print(f"[SUCCESS] VPC: {vpc_url}")
    else:
        print(f"[FAILED] VPC configuration failed")
    
    if security_groups_url:
        print(f"[SUCCESS] Security Groups: {security_groups_url}")
    else:
        print(f"[FAILED] Security Groups configuration failed")

if __name__ == "__main__":
    main()
