"""
Robust AWS Lambda Configuration Class
Enhanced with proper validation and field mapping
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class RobustAWSLambdaConfigurator(BaseAWSConfigurator):
    """Robust AWS Lambda configuration class with enhanced validation"""
    
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
    
    def validate_lambda_config(self, config: Dict[str, Any]) -> bool:
        """Validate AWS Lambda configuration parameters"""
        print(f"\n[VALIDATION] Validating AWS Lambda configuration...")
        
        required_fields = ['number_of_requests', 'duration_ms', 'memory_mb']
        missing_fields = []
        
        for field in required_fields:
            if field not in config or config[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"[ERROR] Missing required fields: {missing_fields}")
            return False
        
        # Validate numeric values
        numeric_fields = {
            'number_of_requests': (1, 10000000),
            'duration_ms': (1, 900000),
            'memory_mb': (128, 10240),
            'ephemeral_storage_mb': (512, 10240),
            'concurrency': (1, 1000)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in config and config[field] is not None:
                value = config[field]
                if not isinstance(value, (int, float)) or value < min_val or value > max_val:
                    print(f"[ERROR] Invalid {field}: {value} (must be between {min_val} and {max_val})")
                    return False
        
        print(f"[OK] Configuration validation passed")
        return True
    
    def apply_aws_lambda_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply AWS Lambda configuration with enhanced validation and field mapping"""
        try:
            print(f"\n[INFO] Applying AWS Lambda configuration...")
            
            # Validate configuration first
            if not self.validate_lambda_config(config):
                return False
            
            # Map elements first
            elements = self.map_all_elements()
            
            # Apply settings using robust selectors with validation
            settings_applied = 0
            
            # Set description
            if 'description' in config and config['description']:
                try:
                    desc_field = self.page.locator("input[aria-label*='Description']")
                    if desc_field.count() > 0:
                        desc_field.first.fill(config['description'])
                        print(f"[OK] Set description: {config['description']}")
                        settings_applied += 1
                    else:
                        print(f"[WARNING] Description field not found")
                except Exception as e:
                    print(f"[WARNING] Could not set description: {e}")
            
            # Number of requests - use the first occurrence
            if 'number_of_requests' in config and config['number_of_requests'] > 0:
                try:
                    request_fields = self.page.locator("input[aria-label*='Number of requests Value']")
                    if request_fields.count() > 0:
                        request_fields.first.fill(str(config['number_of_requests']))
                        print(f"[OK] Set number of requests to {config['number_of_requests']:,}")
                        settings_applied += 1
                    else:
                        print(f"[WARNING] Number of requests field not found")
                except Exception as e:
                    print(f"[WARNING] Could not set number of requests: {e}")
            
            # Duration of each request (in ms) - use the first occurrence
            if 'duration_ms' in config and config['duration_ms'] > 0:
                try:
                    duration_fields = self.page.locator("input[aria-label*='Duration of each request (in ms) Enter duration in ms']")
                    if duration_fields.count() > 0:
                        duration_fields.first.fill(str(config['duration_ms']))
                        print(f"[OK] Set duration to {config['duration_ms']} ms")
                        settings_applied += 1
                    else:
                        print(f"[WARNING] Duration field not found")
                except Exception as e:
                    print(f"[WARNING] Could not set duration: {e}")
            
            # Amount of memory allocated - use the first occurrence
            if 'memory_mb' in config and config['memory_mb'] > 0:
                try:
                    memory_fields = self.page.locator("input[aria-label*='Amount of memory allocated Value']")
                    if memory_fields.count() > 0:
                        memory_fields.first.fill(str(config['memory_mb']))
                        print(f"[OK] Set memory allocated to {config['memory_mb']} MB")
                        settings_applied += 1
                    else:
                        print(f"[WARNING] Memory allocated field not found")
                except Exception as e:
                    print(f"[WARNING] Could not set memory allocated: {e}")
            
            # Amount of ephemeral storage allocated
            if 'ephemeral_storage_mb' in config and config['ephemeral_storage_mb'] > 0:
                try:
                    storage_fields = self.page.locator("input[aria-label*='Amount of ephemeral storage allocated Value']")
                    if storage_fields.count() > 0:
                        storage_fields.first.fill(str(config['ephemeral_storage_mb']))
                        print(f"[OK] Set ephemeral storage to {config['ephemeral_storage_mb']} MB")
                        settings_applied += 1
                    else:
                        print(f"[WARNING] Ephemeral storage field not found")
                except Exception as e:
                    print(f"[WARNING] Could not set ephemeral storage: {e}")
            
            # Concurrency
            if 'concurrency' in config and config['concurrency'] > 0:
                try:
                    concurrency_fields = self.page.locator("input[aria-label*='Concurrency Enter amount']")
                    if concurrency_fields.count() > 0:
                        concurrency_fields.first.fill(str(config['concurrency']))
                        print(f"[OK] Set concurrency to {config['concurrency']}")
                        settings_applied += 1
                    else:
                        print(f"[WARNING] Concurrency field not found")
                except Exception as e:
                    print(f"[WARNING] Could not set concurrency: {e}")
            
            # Provisioned Concurrency settings (only if enabled)
            if config.get('provisioned_concurrency_enabled_hours', 0) > 0:
                # Time for which Provisioned Concurrency is enabled
                if 'provisioned_concurrency_enabled_hours' in config:
                    try:
                        pc_hours_fields = self.page.locator("input[aria-label*='Time for which Provisioned Concurrency is enabled Value']")
                        if pc_hours_fields.count() > 0:
                            pc_hours_fields.first.fill(str(config['provisioned_concurrency_enabled_hours']))
                            print(f"[OK] Set provisioned concurrency enabled time to {config['provisioned_concurrency_enabled_hours']} hours")
                            settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set provisioned concurrency enabled time: {e}")
                
                # Number of requests for Provisioned Concurrency
                if 'provisioned_concurrency_requests' in config and config['provisioned_concurrency_requests'] > 0:
                    try:
                        pc_requests_fields = self.page.locator("input[aria-label*='Number of requests for Provisioned Concurrency Value']")
                        if pc_requests_fields.count() > 0:
                            pc_requests_fields.first.fill(str(config['provisioned_concurrency_requests']))
                            print(f"[OK] Set provisioned concurrency requests to {config['provisioned_concurrency_requests']:,}")
                            settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set provisioned concurrency requests: {e}")
                
                # Duration of each provisioned request
                if 'provisioned_concurrency_duration_ms' in config and config['provisioned_concurrency_duration_ms'] > 0:
                    try:
                        pc_duration_fields = self.page.locator("input[aria-label*='Duration of each provisioned request (in ms) Enter duration in ms']")
                        if pc_duration_fields.count() > 0:
                            pc_duration_fields.first.fill(str(config['provisioned_concurrency_duration_ms']))
                            print(f"[OK] Set provisioned concurrency duration to {config['provisioned_concurrency_duration_ms']} ms")
                            settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set provisioned concurrency duration: {e}")
                
                # Memory for provisioned concurrency (use second memory field)
                if 'provisioned_concurrency_memory_mb' in config and config['provisioned_concurrency_memory_mb'] > 0:
                    try:
                        memory_fields = self.page.locator("input[aria-label*='Amount of memory allocated Value']")
                        if memory_fields.count() > 1:  # Second memory field is for provisioned concurrency
                            memory_fields.nth(1).fill(str(config['provisioned_concurrency_memory_mb']))
                            print(f"[OK] Set provisioned concurrency memory to {config['provisioned_concurrency_memory_mb']} MB")
                            settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set provisioned concurrency memory: {e}")
            
            print(f"[OK] Applied {settings_applied} AWS Lambda settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply AWS Lambda configuration: {e}")
            return False
    
    def verify_configuration(self, config: Dict[str, Any]) -> bool:
        """Verify that the configuration was applied correctly"""
        try:
            print(f"\n[VERIFICATION] Verifying AWS Lambda configuration...")
            
            verification_passed = 0
            total_checks = 0
            
            # Check description
            if 'description' in config and config['description']:
                total_checks += 1
                try:
                    desc_field = self.page.locator("input[aria-label*='Description']")
                    if desc_field.count() > 0:
                        actual_value = desc_field.first.input_value()
                        if actual_value == config['description']:
                            print(f"[OK] Description verified: {actual_value}")
                            verification_passed += 1
                        else:
                            print(f"[WARNING] Description mismatch: expected '{config['description']}', got '{actual_value}'")
                except Exception as e:
                    print(f"[WARNING] Could not verify description: {e}")
            
            # Check number of requests
            if 'number_of_requests' in config and config['number_of_requests'] > 0:
                total_checks += 1
                try:
                    request_fields = self.page.locator("input[aria-label*='Number of requests Value']")
                    if request_fields.count() > 0:
                        actual_value = request_fields.first.input_value()
                        if actual_value == str(config['number_of_requests']):
                            print(f"[OK] Number of requests verified: {actual_value}")
                            verification_passed += 1
                        else:
                            print(f"[WARNING] Number of requests mismatch: expected '{config['number_of_requests']}', got '{actual_value}'")
                except Exception as e:
                    print(f"[WARNING] Could not verify number of requests: {e}")
            
            # Check duration
            if 'duration_ms' in config and config['duration_ms'] > 0:
                total_checks += 1
                try:
                    duration_fields = self.page.locator("input[aria-label*='Duration of each request (in ms) Enter duration in ms']")
                    if duration_fields.count() > 0:
                        actual_value = duration_fields.first.input_value()
                        if actual_value == str(config['duration_ms']):
                            print(f"[OK] Duration verified: {actual_value} ms")
                            verification_passed += 1
                        else:
                            print(f"[WARNING] Duration mismatch: expected '{config['duration_ms']}', got '{actual_value}'")
                except Exception as e:
                    print(f"[WARNING] Could not verify duration: {e}")
            
            # Check memory
            if 'memory_mb' in config and config['memory_mb'] > 0:
                total_checks += 1
                try:
                    memory_fields = self.page.locator("input[aria-label*='Amount of memory allocated Value']")
                    if memory_fields.count() > 0:
                        actual_value = memory_fields.first.input_value()
                        if actual_value == str(config['memory_mb']):
                            print(f"[OK] Memory verified: {actual_value} MB")
                            verification_passed += 1
                        else:
                            print(f"[WARNING] Memory mismatch: expected '{config['memory_mb']}', got '{actual_value}'")
                except Exception as e:
                    print(f"[WARNING] Could not verify memory: {e}")
            
            print(f"[OK] Verification completed: {verification_passed}/{total_checks} checks passed")
            return verification_passed == total_checks
            
        except Exception as e:
            print(f"[ERROR] Failed to verify configuration: {e}")
            return False


def main():
    """Test the robust AWS Lambda configurator"""
    from playwright.sync_api import sync_playwright
    
    # Test configuration
    test_config = {
        'description': 'Robust AWS Lambda test configuration',
        'number_of_requests': 100000,
        'duration_ms': 500,
        'memory_mb': 512,
        'ephemeral_storage_mb': 1024,
        'concurrency': 50,
        'provisioned_concurrency_enabled_hours': 0,  # Disabled for basic test
        'provisioned_concurrency_requests': 0,
        'provisioned_concurrency_duration_ms': 0,
        'provisioned_concurrency_memory_mb': 0
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = RobustAWSLambdaConfigurator(page)
        
        if configurator.navigate_to_aws_lambda_config():
            # Apply configuration
            if configurator.apply_aws_lambda_configuration(test_config):
                # Verify configuration
                if configurator.verify_configuration(test_config):
                    print(f"\n[SUCCESS] Configuration applied and verified successfully!")
                    
                    # Save and get URL
                    url = configurator.save_and_exit()
                    if url:
                        print(f"[SUCCESS] AWS Lambda configuration completed!")
                        print(f"[URL] Estimate URL: {url}")
                        
                        # Save URL to file
                        with open("robust_aws_lambda_estimate_url.txt", "w") as f:
                            f.write(url)
                        print(f"[SAVE] URL saved to robust_aws_lambda_estimate_url.txt")
                else:
                    print(f"[WARNING] Configuration applied but verification failed")
            else:
                print(f"[ERROR] Failed to apply configuration")
        else:
            print(f"[ERROR] Failed to navigate to AWS Lambda configuration")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
