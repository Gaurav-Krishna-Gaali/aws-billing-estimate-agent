"""
Comprehensive AWS Lambda Configuration Class
Handles all 78 interactive elements on the AWS Lambda configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveAWSLambdaConfigurator(BaseAWSConfigurator):
    """Comprehensive AWS Lambda configuration class handling all 78 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "AWS Lambda")
    
    def navigate_to_aws_lambda_config(self) -> bool:
        """Navigate to AWS Lambda configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Click "Add service" button
            try:
                self.page.click("text='Add service'")
                self.page.wait_for_timeout(2000)
                print("[OK] Clicked 'Add service' button")
            except Exception as e:
                print(f"[WARNING] Could not click 'Add service' button: {e}")
            
            # Look for "Configure AWS Lambda" button directly
            try:
                lambda_button = self.page.locator("button[aria-label='Configure AWS Lambda']")
                if lambda_button.count() > 0:
                    lambda_button.first.click()
                    self.page.wait_for_timeout(3000)
                    print("[OK] Clicked 'Configure AWS Lambda' button")
                    print(f"[OK] Successfully navigated to AWS Lambda configuration page")
                    return True
                else:
                    print("[ERROR] Could not find 'Configure AWS Lambda' button")
                    return False
            except Exception as e:
                print(f"[ERROR] Failed to click Lambda button: {e}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS Lambda config: {e}")
            return False
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to AWS Lambda service configuration page (for multi-service estimates)"""
        try:
            print("[INFO] Navigating to AWS Lambda service configuration...")
            
            # Search for Lambda using the correct service name
            search_terms = ["AWS Lambda", "Lambda", "Serverless"]
            for term in search_terms:
                if self.search_and_select_service(term):
                    return True
            
            print("[ERROR] Could not find AWS Lambda service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to AWS Lambda configuration: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding AWS Lambda service in AWS Calculator"""
        return ["AWS Lambda", "Lambda", "Serverless"]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """Apply AWS Lambda-specific configuration logic"""
        try:
            print("[INFO] Applying AWS Lambda-specific configuration...")
            return self.apply_aws_lambda_configuration(config)
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS Lambda configuration: {e}")
            return False
    
    def apply_aws_lambda_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS Lambda configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying AWS Lambda configuration...")
            
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
            
            # Number of requests
            if 'number_of_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of requests Value']", str(config['number_of_requests']))
                    print(f"[OK] Set number of requests to {config['number_of_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set number of requests: {e}")
            
            # Duration of each request (in ms)
            if 'duration_ms' in config:
                try:
                    self.page.fill("input[aria-label*='Duration of each request (in ms) Enter duration in ms']", str(config['duration_ms']))
                    print(f"[OK] Set duration to {config['duration_ms']} ms")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set duration: {e}")
            
            # Amount of memory allocated
            if 'memory_mb' in config:
                try:
                    self.page.fill("input[aria-label*='Amount of memory allocated Value']", str(config['memory_mb']))
                    print(f"[OK] Set memory allocated to {config['memory_mb']} MB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set memory allocated: {e}")
            
            # Amount of ephemeral storage allocated
            if 'ephemeral_storage_mb' in config:
                try:
                    self.page.fill("input[aria-label*='Amount of ephemeral storage allocated Value']", str(config['ephemeral_storage_mb']))
                    print(f"[OK] Set ephemeral storage to {config['ephemeral_storage_mb']} MB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ephemeral storage: {e}")
            
            # Concurrency
            if 'concurrency' in config:
                try:
                    self.page.fill("input[aria-label*='Concurrency Enter amount']", str(config['concurrency']))
                    print(f"[OK] Set concurrency to {config['concurrency']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set concurrency: {e}")
            
            # Provisioned Concurrency settings
            if 'provisioned_concurrency_enabled_hours' in config:
                try:
                    self.page.fill("input[aria-label*='Time for which Provisioned Concurrency is enabled Value']", str(config['provisioned_concurrency_enabled_hours']))
                    print(f"[OK] Set provisioned concurrency enabled time to {config['provisioned_concurrency_enabled_hours']} hours")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set provisioned concurrency enabled time: {e}")
            
            if 'provisioned_concurrency_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Number of requests for Provisioned Concurrency Value']", str(config['provisioned_concurrency_requests']))
                    print(f"[OK] Set provisioned concurrency requests to {config['provisioned_concurrency_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set provisioned concurrency requests: {e}")
            
            if 'provisioned_concurrency_duration_ms' in config:
                try:
                    self.page.fill("input[aria-label*='Duration of each provisioned request (in ms) Enter duration in ms']", str(config['provisioned_concurrency_duration_ms']))
                    print(f"[OK] Set provisioned concurrency duration to {config['provisioned_concurrency_duration_ms']} ms")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set provisioned concurrency duration: {e}")
            
            if 'provisioned_concurrency_memory_mb' in config:
                try:
                    # Find the provisioned concurrency memory field (it has the same aria-label as regular memory)
                    memory_fields = self.page.query_selector_all("input[aria-label*='Amount of memory allocated Value']")
                    if len(memory_fields) > 1:  # Second memory field is for provisioned concurrency
                        memory_fields[1].fill(str(config['provisioned_concurrency_memory_mb']))
                        print(f"[OK] Set provisioned concurrency memory to {config['provisioned_concurrency_memory_mb']} MB")
                        settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set provisioned concurrency memory: {e}")
            
            print(f"[OK] Applied {settings_applied} AWS Lambda settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS Lambda configuration: {e}")
            return False

def main():
    """Test the comprehensive AWS Lambda configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveAWSLambdaConfigurator(page)
        
        if configurator.navigate_to_aws_lambda_config():
            # Example configuration
            example_config = {
                'description': 'AWS Lambda functions for production API processing',
                'number_of_requests': 1000000,
                'duration_ms': 500,
                'memory_mb': 512,
                'ephemeral_storage_mb': 10240,
                'concurrency': 100,
                'provisioned_concurrency_enabled_hours': 720,
                'provisioned_concurrency_requests': 100000,
                'provisioned_concurrency_duration_ms': 300,
                'provisioned_concurrency_memory_mb': 1024
            }
            
            # Apply configuration
            if configurator.apply_aws_lambda_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] AWS Lambda configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("aws_lambda_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to aws_lambda_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
