"""
AWS Calculator Automation Script
Main script that orchestrates JSON reading, service addition, and URL generation
"""

import sys
import time
from playwright.sync_api import sync_playwright
from utils.json_parser import JSONParser
from utils.service_mapping import ServiceMapping
from page_objects.calculator_page import AWSCalculatorPage
from page_objects.service_configurator import ServiceConfiguratorFactory


class AWSCalculatorAutomation:
    """Main automation class for AWS Calculator"""
    
    def __init__(self, json_file_path: str = "sow-analysis-Ody.json", headless: bool = False):
        self.json_file_path = json_file_path
        self.headless = headless
        self.calculator_page = None
        self.playwright = None
        self.browser = None
        self.page = None
        
    def run(self) -> str:
        """Run the complete automation process"""
        try:
            print("[START] Starting AWS Calculator Automation")
            print("=" * 50)
            
            # Step 1: Parse JSON
            json_data = self._parse_json()
            if not json_data:
                return ""
            
            # Step 2: Initialize browser
            if not self._initialize_browser():
                return ""
            
            # Step 3: Navigate to calculator
            if not self._navigate_to_calculator():
                return ""
            
            # Step 4: Create estimate
            if not self._create_estimate():
                return ""
            
            # Step 5: Add and configure services
            if not self._configure_services(json_data['services']):
                print("[WARNING]  Some services failed to configure, but continuing...")
            
            # Step 6: Get final URL
            final_url = self._get_final_url()
            
            # Step 7: Save results
            self._save_results(final_url)
            
            return final_url
            
        except Exception as e:
            print(f"[ERROR] Automation failed: {e}")
            return ""
        finally:
            self._cleanup()
    
    def _parse_json(self) -> dict:
        """Parse the JSON file"""
        try:
            print("[FILE] Parsing JSON file...")
            parser = JSONParser(self.json_file_path)
            data = parser.parse()
            parser.print_summary()
            return data
        except Exception as e:
            print(f"[ERROR] Failed to parse JSON: {e}")
            return {}
    
    def _initialize_browser(self) -> bool:
        """Initialize Playwright browser"""
        try:
            print("[WEB] Initializing browser...")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            self.calculator_page = AWSCalculatorPage(self.page)
            print("[OK] Browser initialized")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to initialize browser: {e}")
            return False
    
    def _navigate_to_calculator(self) -> bool:
        """Navigate to AWS Calculator"""
        try:
            print("[NAVIGATE] Navigating to AWS Calculator...")
            return self.calculator_page.navigate_to_calculator()
        except Exception as e:
            print(f"[ERROR] Failed to navigate to calculator: {e}")
            return False
    
    def _create_estimate(self) -> bool:
        """Create a new estimate"""
        try:
            print("[CREATE] Creating new estimate...")
            return self.calculator_page.create_new_estimate()
        except Exception as e:
            print(f"[ERROR] Failed to create estimate: {e}")
            return False
    
    def _configure_services(self, services) -> bool:
        """Configure all services from JSON"""
        try:
            print("[CONFIG] Configuring services...")
            print("-" * 30)
            
            services_to_configure = [s for s in services if not ServiceMapping.should_skip_service(s.service_name)]
            
            success_count = 0
            total_count = len(services_to_configure)
            
            for i, service in enumerate(services_to_configure, 1):
                print(f"\n[{i}/{total_count}] Processing: {service.service_name}")
                
                try:
                    # Add service to calculator
                    if not self.calculator_page.add_service(service.service_name):
                        print(f"[WARNING]  Failed to add service: {service.service_name}")
                        continue
                    
                    # Wait for configuration panel
                    self.calculator_page.wait_for_service_configuration_panel()
                    
                    # Configure the service
                    if self._configure_single_service(service):
                        success_count += 1
                        print(f"[OK] Successfully configured: {service.service_name}")
                    else:
                        print(f"[WARNING]  Configuration failed for: {service.service_name}")
                    
                    # Wait for calculation
                    self.calculator_page.wait_for_calculation()
                    
                    # Small delay between services
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"[ERROR] Error processing {service.service_name}: {e}")
                    continue
            
            print(f"\n[STATS] Configuration Summary: {success_count}/{total_count} services configured successfully")
            return success_count > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to configure services: {e}")
            return False
    
    def _configure_single_service(self, service) -> bool:
        """Configure a single service"""
        try:
            # Get the appropriate configurator
            configurator = ServiceConfiguratorFactory.get_configurator(service.service_name, self.page)
            
            # Extract configuration based on service type
            if 'S3' in service.service_name:
                config = ServiceMapping.extract_s3_config(service)
                return configurator.configure_s3(config)
            elif 'Fargate' in service.service_name or 'ECS' in service.service_name:
                config = ServiceMapping.extract_fargate_config(service)
                if 'Cluster' in service.service_name:
                    return configurator.configure_ecs_cluster(config)
                else:
                    return configurator.configure_fargate_task(config)
            elif 'CloudWatch' in service.service_name:
                config = ServiceMapping.extract_cloudwatch_config(service)
                return configurator.configure_cloudwatch(config)
            elif 'API Gateway' in service.service_name:
                config = ServiceMapping.extract_api_gateway_config(service)
                return configurator.configure_api_gateway(config)
            elif 'Load Balancer' in service.service_name:
                config = ServiceMapping.extract_alb_config(service)
                return configurator.configure_alb(config)
            elif 'Bedrock' in service.service_name:
                config = ServiceMapping.extract_bedrock_config(service)
                return configurator.configure_bedrock(config)
            elif 'SQS' in service.service_name:
                # Extract SQS config from service configurations
                config = {
                    'messages_per_month': 0
                }
                if 'MessagesPerMonth' in service.configurations:
                    messages_str = service.configurations['MessagesPerMonth']
                    if 'M' in messages_str:
                        config['messages_per_month'] = int(messages_str.replace('M', '')) * 1000000
                    else:
                        config['messages_per_month'] = int(messages_str)
                return configurator.configure_sqs(config)
            elif 'KMS' in service.service_name:
                # Extract KMS config
                config = {
                    'customer_managed_keys': 0
                }
                if 'CustomerManagedKeys' in service.configurations:
                    config['customer_managed_keys'] = int(service.configurations['CustomerManagedKeys'])
                return configurator.configure_kms(config)
            elif 'WAF' in service.service_name:
                # Extract WAF config
                config = {
                    'requests_per_month': 0,
                    'webacls': 0,
                    'rules': 0
                }
                if 'RequestsPerMonth' in service.configurations:
                    requests_str = service.configurations['RequestsPerMonth']
                    if 'M' in requests_str:
                        config['requests_per_month'] = int(requests_str.replace('M', '')) * 1000000
                    else:
                        config['requests_per_month'] = int(requests_str)
                if 'WebACLs' in service.configurations:
                    config['webacls'] = int(service.configurations['WebACLs'])
                if 'Rules' in service.configurations:
                    rules_str = service.configurations['Rules']
                    # Extract number from string like "10 managed + 5 custom"
                    if '+' in rules_str:
                        parts = rules_str.split('+')
                        total_rules = 0
                        for part in parts:
                            if 'managed' in part:
                                total_rules += int(part.split()[0])
                            elif 'custom' in part:
                                total_rules += int(part.split()[0])
                        config['rules'] = total_rules
                    else:
                        config['rules'] = int(rules_str.split()[0])
                return configurator.configure_waf(config)
            else:
                print(f"[WARNING]  No specific configurator for: {service.service_name}")
                return True  # Skip unknown services
                
        except Exception as e:
            print(f"[ERROR] Failed to configure {service.service_name}: {e}")
            return False
    
    def _get_final_url(self) -> str:
        """Get the final estimate URL"""
        try:
            print("[URL] Getting final estimate URL...")
            
            # Save the estimate
            self.calculator_page.save_estimate()
            
            # Get the URL
            url = self.calculator_page.get_estimate_url()
            
            if url:
                print(f"[OK] Final URL: {url}")
            else:
                print("[WARNING]  Could not retrieve final URL")
            
            return url
            
        except Exception as e:
            print(f"[ERROR] Failed to get final URL: {e}")
            return ""
    
    def _save_results(self, url: str):
        """Save results to files"""
        try:
            print("[SAVE] Saving results...")
            
            # Save URL to file
            if url:
                with open("estimate_url.txt", "w") as f:
                    f.write(url)
                print("[OK] URL saved to estimate_url.txt")
            
            # Take final screenshot
            self.calculator_page.take_screenshot("final_estimate.png")
            
            print("[OK] Results saved successfully")
            
        except Exception as e:
            print(f"[WARNING]  Failed to save results: {e}")
    
    def _cleanup(self):
        """Clean up resources"""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("[CLEANUP] Cleanup completed")
        except Exception as e:
            print(f"[WARNING]  Cleanup error: {e}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS Calculator Automation")
    parser.add_argument("--json", default="sow-analysis-Ody.json", help="Path to JSON file")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    # Run automation
    automation = AWSCalculatorAutomation(args.json, args.headless)
    final_url = automation.run()
    
    if final_url:
        print("\n[SUCCESS] Automation completed successfully!")
        print(f"[URL] Your estimate URL: {final_url}")
    else:
        print("\n[ERROR] Automation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

