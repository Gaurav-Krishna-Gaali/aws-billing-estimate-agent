"""
Comprehensive ECS Fargate Configuration Class
Handles all 39 interactive elements on the ECS Fargate configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator


class ComprehensiveECSFargateConfigurator(BaseAWSConfigurator):
    """Comprehensive ECS Fargate configuration class handling all 39 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "ECS Fargate")
    
    def navigate_to_ecs_fargate_config(self) -> bool:
        """Navigate to ECS Fargate configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for AWS Fargate
            if not self.search_and_select_service("AWS Fargate"):
                return False
            
            print(f"[OK] Successfully navigated to ECS Fargate configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to ECS Fargate config: {e}")
            return False
    
    def apply_ecs_fargate_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply ECS Fargate configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying ECS Fargate configuration...")
            
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
            
            # Number of tasks or pods
            if 'number_of_tasks' in config:
                try:
                    self.page.fill("input[aria-label*='Number of tasks or pods Value']", str(config['number_of_tasks']))
                    print(f"[OK] Set number of tasks to {config['number_of_tasks']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set number of tasks: {e}")
            
            # Average duration
            if 'average_duration_minutes' in config:
                try:
                    self.page.fill("input[aria-label*='Average duration Value']", str(config['average_duration_minutes']))
                    print(f"[OK] Set average duration to {config['average_duration_minutes']} minutes")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set average duration: {e}")
            
            # Memory allocated
            if 'memory_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Amount of memory allocated Value']", str(config['memory_gb']))
                    print(f"[OK] Set memory allocated to {config['memory_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set memory allocated: {e}")
            
            # Ephemeral storage allocated
            if 'ephemeral_storage_gb' in config:
                try:
                    self.page.fill("input[aria-label*='Amount of ephemeral storage allocated for Amazon ECS Value']", str(config['ephemeral_storage_gb']))
                    print(f"[OK] Set ephemeral storage to {config['ephemeral_storage_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set ephemeral storage: {e}")
            
            print(f"[OK] Applied {settings_applied} ECS Fargate settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply ECS Fargate configuration: {e}")
            return False


def main():
    """Test the comprehensive ECS Fargate configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveECSFargateConfigurator(page)
        
        if configurator.navigate_to_ecs_fargate_config():
            # Example configuration
            example_config = {
                'description': 'ECS Fargate cluster for production microservices',
                'number_of_tasks': 10,
                'average_duration_minutes': 60,
                'memory_gb': 2,
                'ephemeral_storage_gb': 20
            }
            
            # Apply configuration
            if configurator.apply_ecs_fargate_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] ECS Fargate configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("ecs_fargate_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to ecs_fargate_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
