"""
AWS Estimate Builder - Centralized multi-service estimate creation
Manages a single browser session to add multiple AWS services to one estimate
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright, Page
from typing import Dict, Any, List, Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_configurator import BaseAWSConfigurator
from service_registry import get_configurator_class


class AWSEstimateBuilder:
    """
    Centralized builder that:
    1. Opens browser once
    2. Creates estimate once  
    3. Adds multiple services sequentially
    4. Returns single shareable URL
    """
    
    def __init__(self, headless: bool = False):
        self.playwright = None
        self.browser = None
        self.page = None
        self.estimate_url = None
        self.headless = headless
        self.services_added = []
        self.base_url = "https://calculator.aws/#/"
    
    def start_session(self) -> bool:
        """Initialize browser and create estimate"""
        try:
            print("[INFO] Starting AWS Estimate Builder session...")
            
            # Launch browser
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            
            # Navigate to AWS Calculator
            print("[INFO] Navigating to AWS Calculator...")
            self.page.goto(self.base_url)
            
            # Wait for page to load
            self.page.wait_for_timeout(3000)
            
            # Create new estimate
            print("[INFO] Creating new estimate...")
            self.page.wait_for_selector("text='Create estimate'", timeout=10000)
            self.page.click("text='Create estimate'")
            
            # Wait for estimate to be created
            self.page.wait_for_timeout(2000)
            
            print("[SUCCESS] Estimate session started successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to start session: {e}")
            return False
    
    def add_service(self, service_type: str, config: Dict[str, Any]) -> bool:
        """
        Add one service configuration to current estimate
        
        Args:
            service_type: e.g., 's3', 'ecs_fargate', 'alb'
            config: Standardized config dict for that service
            
        Returns:
            bool: True if service was added successfully
        """
        try:
            print(f"[INFO] Adding {service_type} service to estimate...")
            
            # Get the appropriate configurator class
            configurator_class = get_configurator_class(service_type)
            if not configurator_class:
                print(f"[ERROR] No configurator found for service: {service_type}")
                return False
            
            # Create configurator instance
            configurator = configurator_class(self.page)
            
            # Navigate to service configuration
            if not configurator.navigate_to_service_config():
                print(f"[ERROR] Failed to navigate to {service_type} configuration")
                return False
            
            # Apply configuration in "add to estimate" mode
            if not configurator.apply_configuration(config, add_to_estimate=True):
                print(f"[ERROR] Failed to apply {service_type} configuration")
                return False
            
            # Verify service was added
            self.page.wait_for_timeout(2000)
            
            # Navigate back to service search for next service
            self._navigate_to_service_search()
            
            self.services_added.append({
                'service_type': service_type,
                'config': config,
                'timestamp': self._get_timestamp()
            })
            
            print(f"[SUCCESS] {service_type} service added to estimate")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to add {service_type} service: {e}")
            return False
    
    def add_multiple_services(self, services_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
        """
        Add multiple services from standardized input
        
        Args:
            services_dict: {
                's3': [{config1}, {config2}],
                'ecs_fargate': [{config1}]
            }
            
        Returns:
            Dict with success/failure counts per service type
        """
        results = {}
        
        for service_type, configs_list in services_dict.items():
            print(f"\n[INFO] Processing {len(configs_list)} {service_type} service(s)...")
            success_count = 0
            
            for i, config in enumerate(configs_list):
                print(f"[INFO] Adding {service_type} instance {i+1}/{len(configs_list)}")
                
                if self.add_service(service_type, config):
                    success_count += 1
                else:
                    print(f"[WARNING] Failed to add {service_type} instance {i+1}")
            
            results[service_type] = {
                'total': len(configs_list),
                'successful': success_count,
                'failed': len(configs_list) - success_count
            }
            
            print(f"[INFO] {service_type}: {success_count}/{len(configs_list)} services added successfully")
        
        return results
    
    def finalize_estimate(self) -> Optional[str]:
        """Save estimate and return shareable URL"""
        try:
            print("[INFO] Finalizing estimate...")
            
            # Navigate to estimate summary if not already there
            self._navigate_to_estimate_summary()
            
            # Click save/share button
            print("[INFO] Saving estimate...")
            self.page.wait_for_selector("button:has-text('Save and share')", timeout=10000)
            self.page.click("button:has-text('Save and share')")
            
            # Wait for URL to be generated
            self.page.wait_for_timeout(3000)
            
            # Extract the estimate URL
            current_url = self.page.url
            if "calculator.aws" in current_url and "estimate" in current_url:
                self.estimate_url = current_url
                print(f"[SUCCESS] Estimate finalized: {self.estimate_url}")
                return self.estimate_url
            else:
                print("[ERROR] Failed to generate estimate URL")
                return None
                
        except Exception as e:
            print(f"[ERROR] Failed to finalize estimate: {e}")
            return None
    
    def close_session(self):
        """Close browser session"""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("[INFO] Browser session closed")
        except Exception as e:
            print(f"[WARNING] Error closing session: {e}")
    
    def get_services_added(self) -> List[Dict[str, Any]]:
        """Get list of services that were successfully added"""
        return self.services_added.copy()
    
    def _navigate_to_service_search(self):
        """Navigate back to service search page"""
        try:
            # Look for "Add service" or "Add another service" button
            if self.page.locator("button:has-text('Add service')").is_visible():
                self.page.click("button:has-text('Add service')")
            elif self.page.locator("button:has-text('Add another service')").is_visible():
                self.page.click("button:has-text('Add another service')")
            else:
                # Navigate to calculator home
                self.page.goto(self.base_url)
                self.page.wait_for_timeout(2000)
        except Exception as e:
            print(f"[WARNING] Could not navigate to service search: {e}")
    
    def _navigate_to_estimate_summary(self):
        """Navigate to estimate summary page"""
        try:
            # Look for estimate summary or review button
            if self.page.locator("button:has-text('Review estimate')").is_visible():
                self.page.click("button:has-text('Review estimate')")
            elif self.page.locator("button:has-text('View estimate')").is_visible():
                self.page.click("button:has-text('View estimate')")
            
            self.page.wait_for_timeout(2000)
        except Exception as e:
            print(f"[WARNING] Could not navigate to estimate summary: {e}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Test the estimate builder with a simple example"""
    print("Testing AWS Estimate Builder...")
    
    # Example services configuration
    test_services = {
        "s3": [
            {
                "description": "Test S3 bucket",
                "region": "us-east-1",
                "storage_gb": 100,
                "storage_class": "Standard",
                "put_requests": 1000,
                "get_requests": 5000,
                "data_transfer_out_gb": 10
            }
        ],
        "ecs_fargate": [
            {
                "description": "Test Fargate service",
                "region": "us-east-1",
                "number_of_tasks": 1,
                "average_duration_minutes": 60,
                "memory_gb": 1,
                "ephemeral_storage_gb": 10
            }
        ]
    }
    
    builder = AWSEstimateBuilder(headless=False)
    
    try:
        # Start session
        if not builder.start_session():
            print("Failed to start session")
            return
        
        # Add services
        results = builder.add_multiple_services(test_services)
        print(f"Results: {results}")
        
        # Finalize estimate
        url = builder.finalize_estimate()
        if url:
            print(f"Estimate URL: {url}")
        else:
            print("Failed to generate estimate URL")
            
    finally:
        builder.close_session()


if __name__ == "__main__":
    main()
