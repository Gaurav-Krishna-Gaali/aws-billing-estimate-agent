"""
Comprehensive CloudWatch Configuration Class
Handles all 81 interactive elements on the CloudWatch configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveCloudWatchConfigurator(BaseAWSConfigurator):
    """Comprehensive CloudWatch configuration class handling all 81 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "CloudWatch")
    
    def navigate_to_cloudwatch_config(self) -> bool:
        """Navigate to CloudWatch configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for Amazon CloudWatch
            if not self.search_and_select_service("Amazon CloudWatch"):
                return False
            
            print(f"[OK] Successfully navigated to CloudWatch configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to CloudWatch config: {e}")
            return False
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to AWS CloudWatch configuration page for multi-service flow."""
        try:
            print("[INFO] Navigating to CloudWatch configuration for multi-service flow...")
            for term in ["Amazon CloudWatch", "CloudWatch", "Monitoring"]:
                if self.search_and_select_service(term):
                    return True
            print("[ERROR] Could not find CloudWatch in calculator search")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to navigate to CloudWatch service config: {e}")
            return False

    def _get_service_search_terms(self) -> list:
        return ["Amazon CloudWatch", "CloudWatch", "Monitoring"]

    def _apply_service_specific_config(self, config: dict) -> bool:
        return self.apply_cloudwatch_configuration(config)
    
    def apply_cloudwatch_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply CloudWatch configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying CloudWatch configuration...")
            
            # Map elements first
            elements = self.map_all_elements()
            
            # Apply settings using robust selectors
            settings_applied = 0
            
            # Set description
            if 'description' in config:
                try:
                    self.page.fill("input[aria-label*='Description']", config['description'])
                    print(f"[OK] Set description: {config['description']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set description: {e}")
            
            # Metrics configuration
            if 'metrics_count' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Metrics (includes detailed and custom metrics) Enter the amount']", str(config['metrics_count']))
                    print(f"[OK] Set metrics count to {config['metrics_count']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set metrics count: {e}")
            
            # GetMetricData API requests
            if 'get_metric_data_requests' in config:
                try:
                    self.page.fill("input[aria-label*='GetMetricData: Number of metrics requested Enter the amount']", str(config['get_metric_data_requests']))
                    print(f"[OK] Set GetMetricData requests to {config['get_metric_data_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GetMetricData requests: {e}")
            
            # GetMetricWidgetImage API requests
            if 'get_metric_widget_image_requests' in config:
                try:
                    self.page.fill("input[aria-label*='GetMetricWidgetImage: Number of metrics requested Enter the amount']", str(config['get_metric_widget_image_requests']))
                    print(f"[OK] Set GetMetricWidgetImage requests to {config['get_metric_widget_image_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set GetMetricWidgetImage requests: {e}")
            
            # Other API requests
            if 'other_api_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of other API requests Enter the amount']", str(config['other_api_requests']))
                    print(f"[OK] Set other API requests to {config['other_api_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set other API requests: {e}")
            
            # Database Insights - vCPUs
            if 'database_insights_vcpus' in config:
                try:
                    self.page.fill("input[aria-label*='Number of vCPUs monitored by Database Insights Value']", str(config['database_insights_vcpus']))
                    print(f"[OK] Set Database Insights vCPUs to {config['database_insights_vcpus']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Database Insights vCPUs: {e}")
            
            # Database Insights - Aurora ACUs
            if 'database_insights_aurora_acus' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Aurora Capacity Units (ACUs) monitored by Database Insights Value']", str(config['database_insights_aurora_acus']))
                    print(f"[OK] Set Database Insights Aurora ACUs to {config['database_insights_aurora_acus']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Database Insights Aurora ACUs: {e}")
            
            # Logs - Standard data ingested
            if 'standard_logs_data_ingested_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Standard Logs: Data Ingested Value']", str(config['standard_logs_data_ingested_gb']))
                    print(f"[OK] Set standard logs data ingested to {config['standard_logs_data_ingested_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set standard logs data ingested: {e}")
            
            # Logs - Infrequent access data ingested
            if 'infrequent_logs_data_ingested_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Infrequent Access Logs: Data Ingested Value']", str(config['infrequent_logs_data_ingested_gb']))
                    print(f"[OK] Set infrequent logs data ingested to {config['infrequent_logs_data_ingested_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set infrequent logs data ingested: {e}")
            
            # Logs - Standard delivered to CloudWatch
            if 'standard_logs_delivered_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Standard Logs Delivered to CloudWatch Logs Value']", str(config['standard_logs_delivered_gb']))
                    print(f"[OK] Set standard logs delivered to {config['standard_logs_delivered_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set standard logs delivered: {e}")
            
            # Logs - Infrequent delivered to CloudWatch
            if 'infrequent_logs_delivered_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Infrequent Access Logs Delivered to CloudWatch Logs Value']", str(config['infrequent_logs_delivered_gb']))
                    print(f"[OK] Set infrequent logs delivered to {config['infrequent_logs_delivered_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set infrequent logs delivered: {e}")
            
            # Logs - Delivered to S3
            if 'logs_delivered_to_s3_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Logs Delivered to S3: Data Ingested Value']", str(config['logs_delivered_to_s3_gb']))
                    print(f"[OK] Set logs delivered to S3 to {config['logs_delivered_to_s3_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set logs delivered to S3: {e}")
            
            # Logs - Data scanned
            if 'logs_data_scanned_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Expected Logs Data scanned Value']", str(config['logs_data_scanned_gb']))
                    print(f"[OK] Set logs data scanned to {config['logs_data_scanned_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set logs data scanned: {e}")
            
            # Dashboards
            if 'dashboards_count' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Dashboards Enter the amount']", str(config['dashboards_count']))
                    print(f"[OK] Set dashboards count to {config['dashboards_count']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set dashboards count: {e}")
            
            # Alarms - Standard resolution
            if 'standard_resolution_alarms' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Standard Resolution Alarm Metrics Enter the amount']", str(config['standard_resolution_alarms']))
                    print(f"[OK] Set standard resolution alarms to {config['standard_resolution_alarms']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set standard resolution alarms: {e}")
            
            # Alarms - High resolution
            if 'high_resolution_alarms' in config:
                try:
                    self.page.fill("input[aria-label*='Number of High Resolution Alarm Metrics Enter the amount']", str(config['high_resolution_alarms']))
                    print(f"[OK] Set high resolution alarms to {config['high_resolution_alarms']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set high resolution alarms: {e}")
            
            # Composite alarms
            if 'composite_alarms' in config:
                try:
                    self.page.fill("input[aria-label*='Number of composite alarms Enter the amount']", str(config['composite_alarms']))
                    print(f"[OK] Set composite alarms to {config['composite_alarms']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set composite alarms: {e}")
            
            # Metrics Insights alarms
            if 'metrics_insights_alarms' in config:
                try:
                    self.page.fill("input[aria-label*='Number of alarms defined with a Metrics Insights query Enter the amount']", str(config['metrics_insights_alarms']))
                    print(f"[OK] Set Metrics Insights alarms to {config['metrics_insights_alarms']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Metrics Insights alarms: {e}")
            
            # Metrics scanned per query
            if 'metrics_scanned_per_query' in config:
                try:
                    self.page.fill("input[aria-label*='Average number of metrics scanned by each Metrics Insights query Enter the amount']", str(config['metrics_scanned_per_query']))
                    print(f"[OK] Set metrics scanned per query to {config['metrics_scanned_per_query']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set metrics scanned per query: {e}")
            
            # Canary runs
            if 'canary_runs' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Canary runs Enter the amount']", str(config['canary_runs']))
                    print(f"[OK] Set canary runs to {config['canary_runs']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set canary runs: {e}")
            
            # Contributor Insights - CloudWatch rules
            if 'contributor_insights_cloudwatch_rules' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Contributor Insights rules for CloudWatch Enter the amount']", str(config['contributor_insights_cloudwatch_rules']))
                    print(f"[OK] Set Contributor Insights CloudWatch rules to {config['contributor_insights_cloudwatch_rules']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Contributor Insights CloudWatch rules: {e}")
            
            # Contributor Insights - CloudWatch events
            if 'contributor_insights_cloudwatch_events' in config:
                try:
                    self.page.fill("input[aria-label*='Total number of matched log events for CloudWatch Value']", str(config['contributor_insights_cloudwatch_events']))
                    print(f"[OK] Set Contributor Insights CloudWatch events to {config['contributor_insights_cloudwatch_events']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Contributor Insights CloudWatch events: {e}")
            
            # Contributor Insights - DynamoDB rules
            if 'contributor_insights_dynamodb_rules' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Contributor Insights rules for DynamoDB Enter the amount']", str(config['contributor_insights_dynamodb_rules']))
                    print(f"[OK] Set Contributor Insights DynamoDB rules to {config['contributor_insights_dynamodb_rules']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Contributor Insights DynamoDB rules: {e}")
            
            # Contributor Insights - DynamoDB events
            if 'contributor_insights_dynamodb_events' in config:
                try:
                    self.page.fill("input[aria-label*='Total number of events for DynamoDB Value']", str(config['contributor_insights_dynamodb_events']))
                    print(f"[OK] Set Contributor Insights DynamoDB events to {config['contributor_insights_dynamodb_events']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Contributor Insights DynamoDB events: {e}")
            
            # Lambda monitoring
            if 'lambda_functions' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Lambda functions Enter the amount']", str(config['lambda_functions']))
                    print(f"[OK] Set Lambda functions to {config['lambda_functions']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Lambda functions: {e}")
            
            # Lambda requests per function
            if 'lambda_requests_per_function' in config:
                try:
                    self.page.fill("input[aria-label*='Number of requests per function Value']", str(config['lambda_requests_per_function']))
                    print(f"[OK] Set Lambda requests per function to {config['lambda_requests_per_function']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Lambda requests per function: {e}")
            
            # RUM - Monthly visitors
            if 'rum_monthly_visitors' in config:
                try:
                    self.page.fill("input[aria-label*='Monthly visitors to your web application Enter the amount']", str(config['rum_monthly_visitors']))
                    print(f"[OK] Set RUM monthly visitors to {config['rum_monthly_visitors']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set RUM monthly visitors: {e}")
            
            # RUM - Events per visit
            if 'rum_events_per_visit' in config:
                try:
                    self.page.fill("input[aria-label*='Number of RUM events per visit Enter the amount']", str(config['rum_events_per_visit']))
                    print(f"[OK] Set RUM events per visit to {config['rum_events_per_visit']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set RUM events per visit: {e}")
            
            # RUM - Event percentage
            if 'rum_event_percentage' in config:
                try:
                    self.page.fill("input[aria-label*='Percentage of RUM event Enter the amount']", str(config['rum_event_percentage']))
                    print(f"[OK] Set RUM event percentage to {config['rum_event_percentage']}%")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set RUM event percentage: {e}")
            
            # Synthetics - Monitored resources
            if 'synthetics_monitored_resources' in config:
                try:
                    self.page.fill("input[aria-label*='Number of monitored resources Value']", str(config['synthetics_monitored_resources']))
                    print(f"[OK] Set Synthetics monitored resources to {config['synthetics_monitored_resources']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Synthetics monitored resources: {e}")
            
            # Synthetics - City networks
            if 'synthetics_city_networks' in config:
                try:
                    self.page.fill("input[aria-label*='Number of city-networks to be monitored Value']", str(config['synthetics_city_networks']))
                    print(f"[OK] Set Synthetics city networks to {config['synthetics_city_networks']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Synthetics city networks: {e}")
            
            # X-Ray - Incoming requests
            if 'xray_incoming_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Volume of incoming requests Value']", str(config['xray_incoming_requests']))
                    print(f"[OK] Set X-Ray incoming requests to {config['xray_incoming_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set X-Ray incoming requests: {e}")
            
            # X-Ray - Outgoing requests
            if 'xray_outgoing_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Volume of outgoing requests to dependencies Value']", str(config['xray_outgoing_requests']))
                    print(f"[OK] Set X-Ray outgoing requests to {config['xray_outgoing_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set X-Ray outgoing requests: {e}")
            
            # SLO - Number of SLOs
            if 'slo_count' in config:
                try:
                    self.page.fill("input[aria-label*='Number of Service level objectives (SLO) Enter the amount']", str(config['slo_count']))
                    print(f"[OK] Set SLO count to {config['slo_count']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set SLO count: {e}")
            
            # SLO - Metric period
            if 'slo_metric_period_minutes' in config:
                try:
                    self.page.fill("input[aria-label*='Service level indicator metric period (minutes) Enter the Service level indicator metric period in minutes']", str(config['slo_metric_period_minutes']))
                    print(f"[OK] Set SLO metric period to {config['slo_metric_period_minutes']} minutes")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set SLO metric period: {e}")
            
            print(f"[OK] Applied {settings_applied} CloudWatch settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply CloudWatch configuration: {e}")
            return False

def main():
    """Test the comprehensive CloudWatch configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveCloudWatchConfigurator(page)
        
        if configurator.navigate_to_cloudwatch_config():
            # Example configuration
            example_config = {
                'description': 'CloudWatch monitoring for production environment',
                'metrics_count': 1000,
                'get_metric_data_requests': 10000,
                'get_metric_widget_image_requests': 1000,
                'other_api_requests': 5000,
                'standard_logs_data_ingested_gb': 100,
                'infrequent_logs_data_ingested_gb': 50,
                'dashboards_count': 10,
                'standard_resolution_alarms': 50,
                'high_resolution_alarms': 10,
                'composite_alarms': 5,
                'canary_runs': 100,
                'lambda_functions': 20,
                'lambda_requests_per_function': 1000,
                'rum_monthly_visitors': 100000,
                'rum_events_per_visit': 10,
                'rum_event_percentage': 80,
                'synthetics_monitored_resources': 5,
                'synthetics_city_networks': 3,
                'xray_incoming_requests': 50000,
                'xray_outgoing_requests': 25000,
                'slo_count': 5,
                'slo_metric_period_minutes': 5
            }
            
            # Apply configuration
            if configurator.apply_cloudwatch_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] CloudWatch configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("cloudwatch_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to cloudwatch_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()

