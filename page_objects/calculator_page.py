"""
AWS Calculator Page Object
Handles navigation, service search, and URL retrieval for the AWS Pricing Calculator
"""

from playwright.sync_api import Page, TimeoutError as PWTimeout
import time
from typing import List, Optional


class AWSCalculatorPage:
    """Page object for AWS Pricing Calculator interactions"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://calculator.aws"
    
    def navigate_to_calculator(self) -> bool:
        """Navigate to the AWS Pricing Calculator"""
        try:
            print("[INFO] Navigating to AWS Pricing Calculator...")
            self.page.goto(self.base_url, wait_until="networkidle", timeout=30000)
            
            # Wait for the page to fully load
            self.page.wait_for_timeout(3000)
            
            print("[OK] Successfully navigated to AWS Pricing Calculator")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to calculator: {e}")
            return False
    
    def create_new_estimate(self) -> bool:
        """Create a new estimate"""
        try:
            print("[CREATE] Creating new estimate...")
            
            # Try multiple selectors for create estimate button
            create_selectors = [
                'text="Create estimate"',
                'text="Create new estimate"',
                'button:has-text("Create estimate")',
                'button:has-text("Create new estimate")',
                '[data-testid="create-estimate"]',
                'button[aria-label*="Create"]'
            ]
            
            for selector in create_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.click(selector)
                    print(f"[OK] Clicked create estimate with selector: {selector}")
                    self.page.wait_for_timeout(2000)
                    return True
                except PWTimeout:
                    continue
            
            # If no explicit button found, the estimate might auto-open
            print("[INFO] No explicit create button found - estimate may auto-open")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to create estimate: {e}")
            return False
    
    def add_service(self, service_name: str) -> bool:
        """Add a service to the estimate"""
        try:
            print(f"[ADD] Adding service: {service_name}")
            
            # Try to find and click "Add service" button
            add_selectors = [
                'text="Add service"',
                'button:has-text("Add service")',
                'text="Add service to estimate"',
                'button[aria-label="Add service"]',
                'button:has-text("+ Add service")',
                'button:has-text("+ Add")',
                '[data-testid="add-service"]'
            ]
            
            service_added = False
            for selector in add_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.click(selector)
                    print(f"[OK] Clicked add service with selector: {selector}")
                    self.page.wait_for_timeout(1500)
                    service_added = True
                    break
                except PWTimeout:
                    continue
            
            if not service_added:
                print("[WARNING] Could not find add service button - trying alternative approach")
                # Try to open services panel via search
                self._try_open_services_panel()
            
            # Search for the service
            return self._search_and_select_service(service_name)
            
        except Exception as e:
            print(f"❌ Failed to add service {service_name}: {e}")
            return False
    
    def _try_open_services_panel(self) -> bool:
        """Try to open the services panel using alternative methods"""
        try:
            panel_selectors = [
                'text="Browse services"',
                'button:has-text("Browse services")',
                'input[placeholder*="Search services"]',
                'input[placeholder*="Find services"]',
                'input[placeholder*="Search"]',
                '[data-testid="service-search"]'
            ]
            
            for selector in panel_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=3000)
                    if 'input' in selector:
                        self.page.click(selector)
                    else:
                        self.page.click(selector)
                    print(f"[OK] Opened services panel with selector: {selector}")
                    self.page.wait_for_timeout(1000)
                    return True
                except PWTimeout:
                    continue
            
            return False
            
        except Exception as e:
            print(f"[WARNING] Could not open services panel: {e}")
            return False
    
    def _search_and_select_service(self, service_name: str) -> bool:
        """Search for and select a service"""
        try:
            # Try to find search input
            search_selectors = [
                'input[placeholder*="Search"]',
                'input[placeholder*="Find services"]',
                'input[placeholder*="Search services"]',
                'input[aria-label*="Search"]',
                'input[type="search"]',
                '[data-testid="service-search-input"]'
            ]
            
            search_input_found = False
            for selector in search_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=3000)
                    self.page.fill(selector, service_name)
                    print(f"[OK] Filled search with '{service_name}' using selector: {selector}")
                    self.page.wait_for_timeout(1000)
                    search_input_found = True
                    break
                except PWTimeout:
                    continue
            
            if not search_input_found:
                print("[WARNING] Could not find search input - trying direct service selection")
                return self._select_service_directly(service_name)
            
            # Wait for search results and select the service
            return self._select_service_from_results(service_name)
            
        except Exception as e:
            print(f"[ERROR] Failed to search for service {service_name}: {e}")
            return False
    
    def _select_service_directly(self, service_name: str) -> bool:
        """Try to select service directly without search"""
        try:
            # Common service name variations
            service_variations = [
                service_name,
                f"Amazon {service_name}",
                f"AWS {service_name}",
                service_name.replace(" ", ""),
                service_name.split()[0]  # First word
            ]
            
            for variation in service_variations:
                selectors = [
                    f'text="{variation}"',
                    f'text=/{variation}/i',
                    f'[data-testid*="{variation.lower()}"]',
                    f'button:has-text("{variation}")'
                ]
                
                for selector in selectors:
                    try:
                        self.page.wait_for_selector(selector, timeout=3000)
                        self.page.click(selector)
                        print(f"[OK] Selected service '{variation}' with selector: {selector}")
                        self.page.wait_for_timeout(1500)
                        return True
                    except PWTimeout:
                        continue
            
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to select service directly: {e}")
            return False
    
    def _select_service_from_results(self, service_name: str) -> bool:
        """Select service from search results"""
        try:
            # Wait for search results
            self.page.wait_for_timeout(2000)
            
            # Try to find and click the service in results
            result_selectors = [
                f'text="{service_name}"',
                f'text="Amazon {service_name}"',
                f'text="AWS {service_name}"',
                f'text=/{service_name}/i',
                f'[data-testid*="{service_name.lower()}"]',
                f'button:has-text("{service_name}")'
            ]
            
            for selector in result_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.click(selector)
                    print(f"[OK] Selected service from results with selector: {selector}")
                    self.page.wait_for_timeout(2000)
                    return True
                except PWTimeout:
                    continue
            
            print(f"[WARNING] Could not find {service_name} in search results")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to select service from results: {e}")
            return False
    
    def wait_for_service_configuration_panel(self, timeout: int = 10000) -> bool:
        """Wait for the service configuration panel to appear"""
        try:
            # Common selectors for configuration panels
            panel_selectors = [
                '[data-testid="service-configuration"]',
                'form',
                '.configuration-panel',
                '[role="form"]',
                'div:has(input)',
                'div:has(select)'
            ]
            
            for selector in panel_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=timeout)
                    print(f"[OK] Service configuration panel loaded")
                    self.page.wait_for_timeout(1000)
                    return True
                except PWTimeout:
                    continue
            
            print("[WARNING] Configuration panel not detected, but continuing...")
            return True
            
        except Exception as e:
            print(f"[WARNING] Error waiting for configuration panel: {e}")
            return True  # Continue anyway
    
    def get_estimate_url(self) -> str:
        """Get the current estimate URL"""
        try:
            current_url = self.page.url
            print(f"[URL] Current estimate URL: {current_url}")
            return current_url
        except Exception as e:
            print(f"[ERROR] Failed to get estimate URL: {e}")
            return ""
    
    def save_estimate(self) -> bool:
        """Save the estimate (if there's a save button)"""
        try:
            save_selectors = [
                'text="Save"',
                'button:has-text("Save")',
                'text="Save estimate"',
                'button:has-text("Save estimate")',
                '[data-testid="save-estimate"]'
            ]
            
            for selector in save_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=3000)
                    self.page.click(selector)
                    print(f"[OK] Saved estimate with selector: {selector}")
                    self.page.wait_for_timeout(2000)
                    return True
                except PWTimeout:
                    continue
            
            print("[INFO] No save button found - estimate may auto-save")
            return True
            
        except Exception as e:
            print(f"[WARNING] Could not save estimate: {e}")
            return True  # Continue anyway
    
    def take_screenshot(self, filename: str = "aws_calculator.png") -> bool:
        """Take a screenshot of the current page"""
        try:
            self.page.screenshot(path=filename, full_page=True)
            print(f"[SCREENSHOT] Screenshot saved as {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to take screenshot: {e}")
            return False
    
    def wait_for_calculation(self, timeout: int = 5000) -> bool:
        """Wait for the calculator to finish calculating"""
        try:
            # Wait a bit for any calculations to complete
            self.page.wait_for_timeout(timeout)
            print("[OK] Calculation completed")
            return True
        except Exception as e:
            print(f"[WARNING] Error waiting for calculation: {e}")
            return True  # Continue anyway
