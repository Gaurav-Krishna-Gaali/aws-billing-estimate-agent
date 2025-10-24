"""
Comprehensive API Gateway Configuration Class
Handles all 46 interactive elements on the API Gateway configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveAPIGatewayConfigurator(BaseAWSConfigurator):
    """Comprehensive API Gateway configuration class handling all 46 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "API Gateway")
    
    def navigate_to_api_gateway_config(self) -> bool:
        """Navigate to API Gateway configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for Amazon API Gateway
            if not self.search_and_select_service("Amazon API Gateway"):
                return False
            
            print(f"[OK] Successfully navigated to API Gateway configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to API Gateway config: {e}")
            return False
    
    def apply_api_gateway_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply API Gateway configuration with provided settings"""
        try:
            print(f"\n[INFO] Applying API Gateway configuration...")
            
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
            
            # HTTP API requests
            if 'http_api_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Requests Value'][placeholder*='HTTP API requests']", str(config['http_api_requests']))
                    print(f"[OK] Set HTTP API requests to {config['http_api_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set HTTP API requests: {e}")
            
            # HTTP API request size
            if 'http_api_request_size_kb' in config:
                try:
                    self.page.fill("input[aria-label*='Average size of each request Value']", str(config['http_api_request_size_kb']))
                    print(f"[OK] Set HTTP API request size to {config['http_api_request_size_kb']} KB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set HTTP API request size: {e}")
            
            # REST API requests
            if 'rest_api_requests' in config:
                try:
                    self.page.fill("input[aria-label*='Requests Value'][placeholder*='REST API requests']", str(config['rest_api_requests']))
                    print(f"[OK] Set REST API requests to {config['rest_api_requests']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set REST API requests: {e}")
            
            # WebSocket messages
            if 'websocket_messages' in config:
                try:
                    self.page.fill("input[aria-label*='Messages Value'][placeholder*='WebSocket messages']", str(config['websocket_messages']))
                    print(f"[OK] Set WebSocket messages to {config['websocket_messages']:,}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set WebSocket messages: {e}")
            
            # WebSocket message size
            if 'websocket_message_size_kb' in config:
                try:
                    self.page.fill("input[aria-label*='Average message size Value']", str(config['websocket_message_size_kb']))
                    print(f"[OK] Set WebSocket message size to {config['websocket_message_size_kb']} KB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set WebSocket message size: {e}")
            
            # WebSocket connection duration
            if 'websocket_connection_duration_seconds' in config:
                try:
                    self.page.fill("input[aria-label*='Average connection duration Value']", str(config['websocket_connection_duration_seconds']))
                    print(f"[OK] Set WebSocket connection duration to {config['websocket_connection_duration_seconds']} seconds")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set WebSocket connection duration: {e}")
            
            # WebSocket connection rate
            if 'websocket_connection_rate' in config:
                try:
                    self.page.fill("input[aria-label*='Average connection rate Value']", str(config['websocket_connection_rate']))
                    print(f"[OK] Set WebSocket connection rate to {config['websocket_connection_rate']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set WebSocket connection rate: {e}")
            
            print(f"[OK] Applied {settings_applied} API Gateway settings successfully")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply API Gateway configuration: {e}")
            return False

def main():
    """Test the comprehensive API Gateway configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveAPIGatewayConfigurator(page)
        
        if configurator.navigate_to_api_gateway_config():
            # Example configuration
            example_config = {
                'description': 'API Gateway for production microservices',
                'http_api_requests': 1000000,
                'http_api_request_size_kb': 10,
                'rest_api_requests': 500000,
                'websocket_messages': 2000000,
                'websocket_message_size_kb': 5,
                'websocket_connection_duration_seconds': 300,
                'websocket_connection_rate': 1000
            }
            
            # Apply configuration
            if configurator.apply_api_gateway_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] API Gateway configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("api_gateway_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to api_gateway_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
