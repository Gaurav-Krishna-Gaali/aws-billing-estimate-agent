"""
AWS Estimate Builder V2 - Fixed version that only clicks "View Summary" at the end
Centralized multi-service estimate creation with proper navigation flow
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


class AWSEstimateBuilderV2:
    """
    Centralized builder that:
    1. Opens browser once
    2. Creates estimate once  
    3. Adds multiple services sequentially (clicks "Add service" between each)
    4. Only clicks "View summary" at the very end
    5. Returns single shareable URL
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
            
            # Check if page is still alive before starting
            try:
                _ = self.page.url  # This will raise if page is closed
            except Exception as e:
                print(f"[ERROR] Browser/page is closed, cannot add {service_type}")
                return False
            
            # Get the appropriate configurator class
            configurator_class = get_configurator_class(service_type)
            if not configurator_class:
                print(f"[ERROR] No configurator found for service: {service_type}")
                # Try to navigate back to service search if possible
                try:
                    self._navigate_to_service_search()
                except:
                    pass
                return False
            
            # Create configurator instance
            configurator = configurator_class(self.page)
            
            # Navigate to service configuration
            if not configurator.navigate_to_service_config():
                print(f"[ERROR] Failed to navigate to {service_type} configuration")
                # Try to navigate back to service search to continue with next service
                try:
                    self._navigate_to_service_search()
                except Exception as nav_e:
                    print(f"[WARNING] Could not navigate back after {service_type} failure: {nav_e}")
                return False
            
            # Apply configuration in "add to estimate" mode
            if not configurator.apply_configuration(config, add_to_estimate=True):
                print(f"[ERROR] Failed to apply {service_type} configuration")
                # Try to navigate back to service search to continue with next service
                try:
                    self._navigate_to_service_search()
                except Exception as nav_e:
                    print(f"[WARNING] Could not navigate back after {service_type} failure: {nav_e}")
                return False
            
            # Verify service was added
            self.page.wait_for_timeout(2000)
            
            # Navigate back to service search for next service
            # IMPORTANT: Only click "Add service" - NOT "View summary"!
            try:
                self._navigate_to_service_search()
            except Exception as nav_e:
                print(f"[WARNING] Failed to navigate back after adding {service_type}: {nav_e}")
                # Don't return False here - the service was added, just navigation failed
                # We'll try to continue
            
            self.services_added.append({
                'service_type': service_type,
                'config': config,
                'timestamp': self._get_timestamp()
            })
            
            print(f"[SUCCESS] {service_type} service added to estimate")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to add {service_type} service: {e}")
            import traceback
            traceback.print_exc()
            # Try to navigate back to service search to continue with next service
            try:
                # Check if page is still alive
                _ = self.page.url
                self._navigate_to_service_search()
            except Exception as nav_e:
                print(f"[WARNING] Could not navigate back after {service_type} error: {nav_e}")
            return False
    
    def add_multiple_services(self, services_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Add multiple services from standardized input
        
        Args:
            services_dict: {
                's3': [{config1}, {config2}],
                'ecs_fargate': [{config1}]
            }
            
        Returns:
            Dict with success/failure counts per service type and skipped services list
        """
        results = {}
        skipped_services = []  # Track all skipped/failed services
        
        for service_type, configs_list in services_dict.items():
            print(f"\n[INFO] Processing {len(configs_list)} {service_type} service(s)...")
            success_count = 0
            failed_instances = []
            
            for i, config in enumerate(configs_list):
                print(f"[INFO] Adding {service_type} instance {i+1}/{len(configs_list)}")
                
                try:
                    if self.add_service(service_type, config):
                        success_count += 1
                    else:
                        failed_instances.append(i + 1)
                        skipped_services.append({
                            'service_type': service_type,
                            'instance_number': i + 1,
                            'description': config.get('description', f'{service_type} instance {i+1}'),
                            'reason': 'Failed to add service'
                        })
                        print(f"[WARNING] Failed to add {service_type} instance {i+1} - continuing to next service...")
                        # Continue to next service instead of stopping
                except Exception as e:
                    failed_instances.append(i + 1)
                    skipped_services.append({
                        'service_type': service_type,
                        'instance_number': i + 1,
                        'description': config.get('description', f'{service_type} instance {i+1}'),
                        'reason': f'Exception: {str(e)}'
                    })
                    print(f"[ERROR] Exception while adding {service_type} instance {i+1}: {e}")
                    print(f"[INFO] Continuing to next service...")
                    # Continue to next service
                    continue
            
            results[service_type] = {
                'total': len(configs_list),
                'successful': success_count,
                'failed': len(configs_list) - success_count,
                'failed_instances': failed_instances
            }
            
            print(f"[INFO] {service_type}: {success_count}/{len(configs_list)} services added successfully")
        
        # Add skipped services summary to results
        results['_summary'] = {
            'total_services': sum(r['total'] for k, r in results.items() if k != '_summary'),
            'successful_services': sum(r['successful'] for k, r in results.items() if k != '_summary'),
            'failed_services': sum(r['failed'] for k, r in results.items() if k != '_summary'),
            'skipped_services': skipped_services,
            'skipped_count': len(skipped_services)
        }
        
        return results
    
    def finalize_estimate(self) -> Optional[str]:
        """Finalize estimate and return URL - NOW clicks 'View summary'"""
        try:
            print("[INFO] Finalizing estimate...")
            
            # Wait for page to settle
            self.page.wait_for_timeout(2000)
            
            # NOW we click "View summary" - this is the ONLY place we do it
            print("[INFO] Clicking 'View summary' button (final step)...")
            try:
                # Try different selectors for the View summary button
                view_summary_selectors = [
                    ".appFooter button[id='estimate-button']",
                    "button[id='estimate-button']",
                    "button[aria-label='View summary']",
                    "button:has-text('View summary')",
                    "button:has-text('View Summary')"
                ]
                
                clicked = False
                for selector in view_summary_selectors:
                    try:
                        if self.page.locator(selector).is_visible(timeout=2000):
                            self.page.click(selector)
                            self.page.wait_for_timeout(3000)
                            print(f"[SUCCESS] Clicked '{selector}' button")
                            clicked = True
                            break
                    except:
                        continue
                
                if not clicked:
                    print("[WARNING] Could not find 'View summary' button")
                
                # Wait for page to load after clicking View summary
                self.page.wait_for_timeout(3000)
                
                # Now click the "Share" button to get the shareable URL
                print("[INFO] Clicking 'Share' button...")
                share_selectors = [
                    "button[data-cy='save-and-share']",
                    "button[aria-label='Share']",
                    "button:has-text('Share')"
                ]
                
                share_clicked = False
                for selector in share_selectors:
                    try:
                        if self.page.locator(selector).is_visible(timeout=2000):
                            self.page.click(selector)
                            self.page.wait_for_timeout(3000)
                            print(f"[SUCCESS] Clicked '{selector}' button")
                            share_clicked = True
                            break
                    except:
                        continue
                
                if not share_clicked:
                    print("[WARNING] Could not find 'Share' button")
                else:
                    # After clicking Share, a notification popup might appear - close it first
                    print("[INFO] Checking for notification popup...")
                    try:
                        # Look for the notification close button
                        notification_close_selectors = [
                            "button[data-testid='notification-bubble-close-icon']",
                            "button[aria-label='Close notification']",
                            ".interact-module__notificationBubbleCloseIcon__PAHLX"
                        ]
                        
                        for selector in notification_close_selectors:
                            try:
                                if self.page.locator(selector).is_visible(timeout=2000):
                                    self.page.click(selector)
                                    self.page.wait_for_timeout(1000)
                                    print(f"[SUCCESS] Closed notification popup: {selector}")
                                    break
                            except:
                                continue
                    except:
                        pass
                    
                    # Now click "Agree and continue"
                    print("[INFO] Clicking 'Agree and continue' in modal...")
                    agree_selectors = [
                        "button[data-id='agree-continue']",
                        "button[aria-label='Agree and continue']",
                        "button:has-text('Agree and continue')"
                    ]
                    
                    agree_clicked = False
                    for selector in agree_selectors:
                        try:
                            if self.page.locator(selector).is_visible(timeout=3000):
                                self.page.click(selector)
                                self.page.wait_for_timeout(2000)
                                print(f"[SUCCESS] Clicked '{selector}' button")
                                agree_clicked = True
                                break
                        except:
                            continue
                    
                    if not agree_clicked:
                        print("[WARNING] Could not find 'Agree and continue' button")
                
                # Wait for the shareable link modal to appear and button to activate
                print("[INFO] Waiting for shareable link modal...")
                self.page.wait_for_timeout(3000)
                
                # Extract the URL from the input field in the modal
                try:
                    # Wait for the URL to appear in the input field
                    print("[INFO] Waiting for URL to populate...")
                    
                    # Try to wait for the input field to have a value
                    url_input_with_value = "input[aria-label='Copy public link'][value*='calculator.aws']"
                    self.page.wait_for_selector(url_input_with_value, timeout=5000)
                    
                    # Get the URL from the first input field (which has the value)
                    estimate_url = self.page.locator(url_input_with_value).first.get_attribute('value')
                    
                    if estimate_url and estimate_url.startswith('https://calculator.aws'):
                        self.estimate_url = estimate_url
                        print(f"[SUCCESS] Estimate URL: {self.estimate_url}")
                        return self.estimate_url
                    else:
                        print(f"[ERROR] Invalid URL extracted: {estimate_url}")
                        
                except Exception as e:
                    print(f"[WARNING] Could not extract URL from modal: {e}")
                    # Try alternative: get the first input field with value
                    try:
                        all_inputs = self.page.locator("input[aria-label='Copy public link']").all()
                        for inp in all_inputs:
                            value = inp.get_attribute('value')
                            if value and value.startswith('https://calculator.aws'):
                                self.estimate_url = value
                                print(f"[SUCCESS] Estimate URL (alternative): {self.estimate_url}")
                                return self.estimate_url
                    except:
                        pass
                
                # Fallback: try to get URL from current page
                current_url = self.page.url
                if "calculator.aws" in current_url:
                    self.estimate_url = current_url
                    print(f"[SUCCESS] Estimate URL (fallback): {self.estimate_url}")
                    return self.estimate_url
                else:
                    print("[ERROR] Failed to extract estimate URL")
                    return None
                    
            except Exception as e:
                print(f"[ERROR] Could not click View Summary: {e}")
                # Fallback: return current URL
                current_url = self.page.url
                if "calculator.aws" in current_url:
                    return current_url
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
        """
        Navigate back to service search page after adding a service
        IMPORTANT: Only clicks "Add service" - NEVER clicks "View summary"!
        "View summary" is only clicked in finalize_estimate() at the very end
        """
        try:
            # Wait for page to fully load after service was added
            print("[INFO] Waiting for page to load after service addition...")
            self.page.wait_for_load_state('networkidle', timeout=5000)
            self.page.wait_for_timeout(2000)
            
            # Check if we're already on the service search/add page
            try:
                search_input = self.page.locator("input[placeholder*='Search'], input[type='search'], input[aria-label*='Search']")
                if search_input.count() > 0 and search_input.first.is_visible(timeout=2000):
                    print("[INFO] Already on service search page")
                    return
            except:
                pass
            
            # Look ONLY for "Add service" buttons - DO NOT click "View summary" here!
            possible_buttons = [
                "button:has-text('Add service')",
                "button:has-text('Add another service')",
                "button:has-text('Add Service')",
                "button:has-text('Add a service')",
                "a:has-text('Add service')",
                "a:has-text('Add another service')",
                "button[aria-label*='Add service' i]",
                "button[data-cy*='add-service' i]",
                "[data-testid='add-service-button']",
                "[data-cy='add-service-button']",
            ]
            
            clicked = False
            for button_selector in possible_buttons:
                try:
                    button = self.page.locator(button_selector).first
                    if button.is_visible(timeout=2000):
                        button.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(500)
                        button.click()
                        print(f"[SUCCESS] Clicked 'Add service' button: {button_selector}")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                # Try to find any button/link containing "Add" and "service" text
                print("[INFO] Searching for 'Add service' button/link...")
                try:
                    all_buttons = self.page.locator("button, a").all()
                    for btn in all_buttons:
                        try:
                            text = btn.inner_text(timeout=1000).lower()
                            # Explicitly exclude "summary" to avoid clicking "View summary"
                            if 'add' in text and 'service' in text and 'summary' not in text:
                                btn.scroll_into_view_if_needed()
                                self.page.wait_for_timeout(500)
                                btn.click()
                                print(f"[SUCCESS] Clicked 'Add service' button with text: {text}")
                                clicked = True
                                break
                        except:
                            continue
                except:
                    pass
            
            if clicked:
                # Wait for service search page to load
                self.page.wait_for_load_state('networkidle', timeout=5000)
                self.page.wait_for_timeout(2000)
                print("[SUCCESS] Navigated back to service search page")
            else:
                # Check if we're already on a page with search capability
                try:
                    search_input = self.page.locator("input[placeholder*='Search'], input[type='search']")
                    if search_input.count() > 0:
                        print("[INFO] Already on a page with search capability")
                        return
                except:
                    pass
                
                raise Exception("Could not find 'Add service' button - DO NOT click 'View summary' yet!")
            
        except Exception as e:
            print(f"[WARNING] Could not navigate to service search automatically: {e}")
            # Try manual navigation as fallback (but this might lose estimate context)
            try:
                print("[WARNING] Attempting fallback navigation (may lose estimate context)...")
                self.page.goto(self.base_url)
                self.page.wait_for_timeout(2000)
                print("[WARNING] Navigated to calculator home - estimate context may be lost")
            except:
                print(f"[ERROR] Failed to navigate after adding service")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Test the estimate builder with a simple example"""
    print("Testing AWS Estimate Builder V2...")
    
    # Example services configuration
    test_services = {
        "s3": [
            {
                "description": "Test S3 bucket",
                "region": "us-east-1",
                "storage_gb": 100,
                "storage_class": "standard",
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
    
    builder = AWSEstimateBuilderV2(headless=False)
    
    try:
        # Start session
        if not builder.start_session():
            print("Failed to start session")
            return
        
        # Add services
        results = builder.add_multiple_services(test_services)
        print(f"Results: {results}")
        
        # Finalize estimate (only NOW clicks "View summary")
        url = builder.finalize_estimate()
        if url:
            print(f"Estimate URL: {url}")
        else:
            print("Failed to generate estimate URL")
            
    finally:
        builder.close_session()


if __name__ == "__main__":
    main()

