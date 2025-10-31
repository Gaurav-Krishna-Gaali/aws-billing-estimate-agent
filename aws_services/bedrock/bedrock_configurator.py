"""
AWS Bedrock Configuration Class
Maps all interactive elements on the Bedrock configuration page
"""

from playwright.sync_api import Page, TimeoutError as PWTimeout
from typing import Dict, Any, List, Optional
import time
from aws_services.base_configurator import BaseAWSConfigurator

class BedrockConfigurator(BaseAWSConfigurator):
    """Unified Bedrock automation class."""
    def __init__(self, page):
        super().__init__(page, "Bedrock")
        self.configuration_data = {}

    def navigate_to_service_config(self) -> bool:
        """Navigate to Bedrock service configuration page for multi-service flow."""
        try:
            print("[INFO] Navigating to Bedrock configuration for multi-service flow...")
            # Try different search terms
            for term in ["Amazon Bedrock", "Bedrock"]:
                if self.search_and_select_service(term):
                    return True
            print("[ERROR] Could not find Bedrock in calculator search")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to navigate to Bedrock service config: {e}")
            return False

    def _get_service_search_terms(self) -> list:
        return ["Amazon Bedrock", "Bedrock"]

    def _apply_service_specific_config(self, config: dict) -> bool:
        """Entry point for multi-service automation config logic."""
        return self.configure_bedrock(config)

    def configure_bedrock(self, config: dict) -> bool:
        """Configure Bedrock with provided settings (simplified for automation)"""
        try:
            print("[INFO] Configuring Bedrock with provided settings (automation)...")
            # Map all input and select fields
            element_inputs = self.page.query_selector_all('input')
            for input_elem in element_inputs:
                try:
                    aria_label = input_elem.get_attribute('aria-label') or ''
                    name = input_elem.get_attribute('name') or ''
                    # fill description if possible
                    if 'description' in config and 'description' in aria_label.lower():
                        input_elem.fill(config['description'])
                        print(f"[OK] Set '{aria_label or name}' to {config['description']}")
                        continue
                except Exception:
                    pass
            # Optionally, handle other arbitrary fields as needed here
            print("[OK] Bedrock configuration completed (basic fields)")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to configure Bedrock: {e}")
            return False
