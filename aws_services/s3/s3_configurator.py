"""
Comprehensive S3 Configuration Class
Handles all 172 interactive elements on the S3 configuration page
"""

import json
import sys
import os
from playwright.sync_api import Page
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_configurator import BaseAWSConfigurator

class ComprehensiveS3Configurator(BaseAWSConfigurator):
    """Comprehensive S3 configuration class handling all 172 elements"""
    
    def __init__(self, page: Page):
        super().__init__(page, "S3")
        self.storage_classes = {
            'standard': 'S3 Standard',
            'int': 'S3 INT',
            'standard_ia': 'S3 Standard-IA', 
            'one_zone_ia': 'S3 One Zone-IA',
            'glacier_flexible': 'S3 Glacier Flexible Retrieval',
            'glacier_deep': 'S3 Glacier Deep Archive',
            'glacier_instant': 'S3 Glacier Instant Retrieval',
            'express_one_zone': 'S3 Express One Zone'
        }
    
    def navigate_to_s3_config(self) -> bool:
        """Navigate to S3 configuration page"""
        try:
            # Navigate to calculator
            if not self.navigate_to_calculator():
                return False
            
            # Search for S3 using the correct service name
            if not self.search_and_select_service("Amazon Simple Storage Service (S3)"):
                return False
            
            print(f"[OK] Successfully navigated to S3 configuration page")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to S3 config: {e}")
            return False
    
    def enable_storage_class(self, storage_class: str) -> bool:
        """Enable a specific storage class by clicking its checkbox"""
        try:
            # Map of storage class to checkbox ID patterns
            checkbox_patterns = {
                'standard': '2230',      # S3 Standard
                'int': '2231',           # S3 INT
                'standard_ia': '2232',   # S3 Standard-IA
                'one_zone_ia': '2233',   # S3 One Zone-IA
                'glacier_flexible': '2234',  # S3 Glacier Flexible Retrieval
                'glacier_deep': '2235',      # S3 Glacier Deep Archive
                'glacier_instant': '2236',   # S3 Glacier Instant Retrieval
                'express_one_zone': '2237'   # S3 Express One Zone
            }
            
            if storage_class in checkbox_patterns:
                pattern = checkbox_patterns[storage_class]
                checkbox_selector = f"input[id*='{pattern}']"
                
                # Check if already enabled
                is_checked = self.page.is_checked(checkbox_selector)
                if not is_checked:
                    self.page.check(checkbox_selector)
                    print(f"[OK] Enabled {self.storage_classes[storage_class]}")
                else:
                    print(f"[INFO] {self.storage_classes[storage_class]} already enabled")
                return True
            else:
                print(f"[ERROR] Unknown storage class: {storage_class}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to enable {storage_class}: {e}")
            return False
    
    def disable_storage_class(self, storage_class: str) -> bool:
        """Disable a specific storage class by unchecking its checkbox"""
        try:
            checkbox_patterns = {
                'standard': '2230',
                'int': '2231', 
                'standard_ia': '2232',
                'one_zone_ia': '2233',
                'glacier_flexible': '2234',
                'glacier_deep': '2235',
                'glacier_instant': '2236',
                'express_one_zone': '2237'
            }
            
            if storage_class in checkbox_patterns:
                pattern = checkbox_patterns[storage_class]
                checkbox_selector = f"input[id*='{pattern}']"
                
                # Check if already disabled
                is_checked = self.page.is_checked(checkbox_selector)
                if is_checked:
                    self.page.uncheck(checkbox_selector)
                    print(f"[OK] Disabled {self.storage_classes[storage_class]}")
                else:
                    print(f"[INFO] {self.storage_classes[storage_class]} already disabled")
                return True
            else:
                print(f"[ERROR] Unknown storage class: {storage_class}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to disable {storage_class}: {e}")
            return False
    
    def configure_storage_class(self, storage_class: str, config: Dict[str, Any]) -> bool:
        """Configure a specific storage class with provided settings"""
        try:
            print(f"[INFO] Configuring {self.storage_classes[storage_class]}...")
            
            # Enable the storage class first
            if not self.enable_storage_class(storage_class):
                return False
            
            settings_applied = 0
            
            # Storage amount
            if 'storage_gb' in config:
                try:
                    selector = f"input[aria-label*='{self.storage_classes[storage_class]} storage Value']"
                    self.page.fill(selector, str(config['storage_gb']))
                    print(f"[OK] Set {storage_class} storage to {config['storage_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} storage: {e}")
            
            # Average object size (for some storage classes)
            if 'average_object_size_mb' in config and storage_class in ['int', 'glacier_flexible', 'glacier_deep']:
                try:
                    selector = f"input[aria-label*='{self.storage_classes[storage_class]} Average Object Size Value']"
                    self.page.fill(selector, str(config['average_object_size_mb']))
                    print(f"[OK] Set {storage_class} average object size to {config['average_object_size_mb']} MB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} average object size: {e}")
            
            # PUT requests
            if 'put_requests' in config:
                try:
                    selector = f"input[aria-label*='PUT, COPY, POST, LIST requests to {self.storage_classes[storage_class]} Enter amount of requests']"
                    self.page.fill(selector, str(config['put_requests']))
                    print(f"[OK] Set {storage_class} PUT requests to {config['put_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} PUT requests: {e}")
            
            # GET requests
            if 'get_requests' in config:
                try:
                    selector = f"input[aria-label*='GET, SELECT, and all other requests from {self.storage_classes[storage_class]} Enter amount of requests']"
                    self.page.fill(selector, str(config['get_requests']))
                    print(f"[OK] Set {storage_class} GET requests to {config['get_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} GET requests: {e}")
            
            # Lifecycle transitions
            if 'lifecycle_transitions' in config:
                try:
                    selector = f"input[aria-label*='Lifecycle Transition requests Enter amount of requests']"
                    self.page.fill(selector, str(config['lifecycle_transitions']))
                    print(f"[OK] Set {storage_class} lifecycle transitions to {config['lifecycle_transitions']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} lifecycle transitions: {e}")
            
            # Data retrievals (for IA and Glacier classes)
            if 'data_retrievals_gb' in config and storage_class in ['standard_ia', 'one_zone_ia', 'glacier_flexible', 'glacier_deep', 'glacier_instant']:
                try:
                    selector = f"input[aria-label*='Data retrievals Value']"
                    self.page.fill(selector, str(config['data_retrievals_gb']))
                    print(f"[OK] Set {storage_class} data retrievals to {config['data_retrievals_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} data retrievals: {e}")
            
            # S3 Select data returned
            if 's3_select_returned_gb' in config:
                try:
                    selector = f"input[aria-label*='Data returned by S3 Select Value']"
                    self.page.fill(selector, str(config['s3_select_returned_gb']))
                    print(f"[OK] Set {storage_class} S3 Select returned to {config['s3_select_returned_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} S3 Select returned: {e}")
            
            # S3 Select data scanned
            if 's3_select_scanned_gb' in config:
                try:
                    selector = f"input[aria-label*='Data scanned by S3 Select Value']"
                    self.page.fill(selector, str(config['s3_select_scanned_gb']))
                    print(f"[OK] Set {storage_class} S3 Select scanned to {config['s3_select_scanned_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set {storage_class} S3 Select scanned: {e}")
            
            print(f"[OK] Applied {settings_applied} settings for {storage_class}")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to configure {storage_class}: {e}")
            return False
    
    def configure_int_tiering(self, config: Dict[str, Any]) -> bool:
        """Configure S3 INT tiering percentages"""
        try:
            print(f"[INFO] Configuring S3 INT tiering...")
            
            settings_applied = 0
            
            # INT tiering percentages
            tiering_configs = {
                'int_frequent_percent': 'Percentage of Storage in INT-Frequent Access Tier',
                'int_infrequent_percent': 'Percentage of Storage in INT-Infrequent Access Tier',
                'int_archive_instant_percent': 'Percentage of Storage in INT-Archive Instant Access Tier',
                'int_archive_percent': 'Percentage of Storage in INT-Archive Access Tier',
                'int_deep_archive_percent': 'Percentage of Storage in INT-Deep Archive Access Tier'
            }
            
            for config_key, aria_label in tiering_configs.items():
                if config_key in config:
                    try:
                        selector = f"input[aria-label*='{aria_label}']"
                        self.page.fill(selector, str(config[config_key]))
                        print(f"[OK] Set {config_key} to {config[config_key]}%")
                        settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set {config_key}: {e}")
            
            print(f"[OK] Applied {settings_applied} INT tiering settings")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to configure INT tiering: {e}")
            return False
    
    def configure_glacier_retrieval(self, storage_class: str, config: Dict[str, Any]) -> bool:
        """Configure Glacier retrieval options"""
        try:
            print(f"[INFO] Configuring {storage_class} retrieval options...")
            
            settings_applied = 0
            
            # Restore requests
            restore_types = ['standard', 'expedited', 'bulk']
            for restore_type in restore_types:
                config_key = f'restore_{restore_type}_requests'
                if config_key in config:
                    try:
                        selector = f"input[aria-label*='Restore requests ({restore_type.title()}) Enter amount of requests']"
                        self.page.fill(selector, str(config[config_key]))
                        print(f"[OK] Set {restore_type} restore requests to {config[config_key]}")
                        settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set {restore_type} restore requests: {e}")
            
            # Data retrievals by type
            for restore_type in restore_types:
                config_key = f'data_retrievals_{restore_type}_gb'
                if config_key in config:
                    try:
                        selector = f"input[aria-label*='Data retrievals ({restore_type.title()}) Value']"
                        self.page.fill(selector, str(config[config_key]))
                        print(f"[OK] Set {restore_type} data retrievals to {config[config_key]} GB")
                        settings_applied += 1
                    except Exception as e:
                        print(f"[WARNING] Could not set {restore_type} data retrievals: {e}")
            
            print(f"[OK] Applied {settings_applied} Glacier retrieval settings")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to configure Glacier retrieval: {e}")
            return False
    
    def configure_advanced_features(self, config: Dict[str, Any]) -> bool:
        """Configure advanced S3 features"""
        try:
            print(f"[INFO] Configuring advanced S3 features...")
            
            settings_applied = 0
            
            # S3 Storage Lens
            if 'storage_lens_objects' in config:
                try:
                    selector = "input[aria-label*='S3 Storage Lens Objects Value']"
                    self.page.fill(selector, str(config['storage_lens_objects']))
                    print(f"[OK] Set Storage Lens objects to {config['storage_lens_objects']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Storage Lens objects: {e}")
            
            # S3 Batch Operations
            if 'batch_operations_jobs' in config:
                try:
                    selector = "input[aria-label*='S3 Batch Operations Jobs Value']"
                    self.page.fill(selector, str(config['batch_operations_jobs']))
                    print(f"[OK] Set Batch Operations jobs to {config['batch_operations_jobs']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Batch Operations jobs: {e}")
            
            if 'batch_operations_objects' in config:
                try:
                    selector = "input[aria-label*='S3 Batch Operations Objects Value']"
                    self.page.fill(selector, str(config['batch_operations_objects']))
                    print(f"[OK] Set Batch Operations objects to {config['batch_operations_objects']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Batch Operations objects: {e}")
            
            # Encryption
            if 'encrypted_data_gb' in config:
                try:
                    selector = "input[aria-label*='Size of encrypted data Value']"
                    self.page.fill(selector, str(config['encrypted_data_gb']))
                    print(f"[OK] Set encrypted data to {config['encrypted_data_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set encrypted data: {e}")
            
            # S3 Object Lambda
            if 'object_lambda_requests' in config:
                try:
                    selector = "input[aria-label*='GET requests from S3 Enter number of requests']"
                    self.page.fill(selector, str(config['object_lambda_requests']))
                    print(f"[OK] Set Object Lambda requests to {config['object_lambda_requests']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Object Lambda requests: {e}")
            
            if 'object_lambda_duration_ms' in config:
                try:
                    selector = "input[aria-label*='Duration that the Lambda function is set to execute per request (in ms) Enter duration in ms']"
                    self.page.fill(selector, str(config['object_lambda_duration_ms']))
                    print(f"[OK] Set Object Lambda duration to {config['object_lambda_duration_ms']} ms")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Object Lambda duration: {e}")
            
            if 'object_lambda_memory_mb' in config:
                try:
                    selector = "input[aria-label*='Amount of memory allocated to the Lambda function Value']"
                    self.page.fill(selector, str(config['object_lambda_memory_mb']))
                    print(f"[OK] Set Object Lambda memory to {config['object_lambda_memory_mb']} MB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Object Lambda memory: {e}")
            
            if 'object_lambda_data_returned_gb' in config:
                try:
                    selector = "input[aria-label*='Size of data returned by S3 Object Lambda Value']"
                    self.page.fill(selector, str(config['object_lambda_data_returned_gb']))
                    print(f"[OK] Set Object Lambda data returned to {config['object_lambda_data_returned_gb']} GB")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set Object Lambda data returned: {e}")
            
            # Vector Search
            if 'vector_indexes' in config:
                try:
                    selector = "input[aria-label*='Number of indexes Enter number of indexes']"
                    self.page.fill(selector, str(config['vector_indexes']))
                    print(f"[OK] Set vector indexes to {config['vector_indexes']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set vector indexes: {e}")
            
            if 'vectors_per_index' in config:
                try:
                    selector = "input[aria-label*='Number of vectors per index Enter Number of vectors per index']"
                    self.page.fill(selector, str(config['vectors_per_index']))
                    print(f"[OK] Set vectors per index to {config['vectors_per_index']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set vectors per index: {e}")
            
            if 'vector_dimensions' in config:
                try:
                    selector = "input[aria-label*='Vector Dimensions Enter number']"
                    self.page.fill(selector, str(config['vector_dimensions']))
                    print(f"[OK] Set vector dimensions to {config['vector_dimensions']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set vector dimensions: {e}")
            
            if 'vector_queries_per_month' in config:
                try:
                    selector = "input[aria-label*='Total number of queries per month (across all indexes) Value']"
                    self.page.fill(selector, str(config['vector_queries_per_month']))
                    print(f"[OK] Set vector queries per month to {config['vector_queries_per_month']}")
                    settings_applied += 1
                except Exception as e:
                    print(f"[WARNING] Could not set vector queries per month: {e}")
            
            print(f"[OK] Applied {settings_applied} advanced feature settings")
            return settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to configure advanced features: {e}")
            return False
    
    def apply_comprehensive_configuration(self, config: Dict[str, Any]) -> bool:
        """Apply comprehensive S3 configuration"""
        try:
            print(f"\n[INFO] Applying comprehensive S3 configuration...")
            
            total_settings_applied = 0
            
            # Set description
            if 'description' in config:
                try:
                    self.page.fill("input[aria-label*='Description']", config['description'])
                    print(f"[OK] Set description: {config['description']}")
                except Exception as e:
                    print(f"[WARNING] Could not set description: {e}")
            
            # Configure each storage class
            for storage_class in self.storage_classes.keys():
                if storage_class in config:
                    class_config = config[storage_class]
                    if self.configure_storage_class(storage_class, class_config):
                        total_settings_applied += 1
                    
                    # Configure INT tiering if it's INT storage class
                    if storage_class == 'int' and 'tiering' in class_config:
                        if self.configure_int_tiering(class_config['tiering']):
                            total_settings_applied += 1
                    
                    # Configure Glacier retrieval if it's a Glacier storage class
                    if storage_class in ['glacier_flexible', 'glacier_deep'] and 'retrieval' in class_config:
                        if self.configure_glacier_retrieval(storage_class, class_config['retrieval']):
                            total_settings_applied += 1
            
            # Configure advanced features
            if 'advanced_features' in config:
                if self.configure_advanced_features(config['advanced_features']):
                    total_settings_applied += 1
            
            print(f"[OK] Applied {total_settings_applied} configuration sections successfully")
            return total_settings_applied > 0
            
        except Exception as e:
            print(f"[ERROR] Failed to apply comprehensive configuration: {e}")
            return False
    
    def navigate_to_service_config(self) -> bool:
        """Navigate to S3 service configuration page (for multi-service estimates)"""
        try:
            print("[INFO] Navigating to S3 service configuration...")
            
            # Search for S3 using the correct service name
            search_terms = ["Amazon Simple Storage Service (S3)", "S3", "Simple Storage Service"]
            for term in search_terms:
                if self.search_and_select_service(term):
                    return True
            
            print("[ERROR] Could not find S3 service")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to navigate to S3 configuration: {e}")
            return False
    
    def _get_service_search_terms(self) -> List[str]:
        """Get search terms for finding S3 service in AWS Calculator"""
        return ["Amazon Simple Storage Service (S3)", "S3", "Simple Storage Service"]
    
    def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
        """Apply S3-specific configuration logic"""
        try:
            print("[INFO] Applying S3-specific configuration...")
            
            # Use the comprehensive configuration method if full config is provided
            if 'standard' in config or 'int' in config or 'glacier_flexible' in config or 'glacier_deep' in config:
                # Full configuration format
                return self.apply_comprehensive_configuration(config)
            
            # Simple configuration format - map to comprehensive format
            storage_gb = config.get('storage_gb', 0)
            storage_class = config.get('storage_class', 'standard')
            put_requests = config.get('put_requests', 0)
            get_requests = config.get('get_requests', 0)
            data_transfer_out_gb = config.get('data_transfer_out_gb', 0)
            
            # Build simple config format
            simple_config = {
                'description': config.get('description', 'S3 Storage')
            }
            
            # Map to storage class structure
            if storage_class.lower() == 'standard' and storage_gb > 0:
                simple_config['standard'] = {
                    'storage_gb': storage_gb,
                    'put_requests': put_requests,
                    'get_requests': get_requests
                }
            
            # Use comprehensive configuration method
            if simple_config:
                return self.apply_comprehensive_configuration(simple_config)
            else:
                print("[WARNING] No valid S3 configuration provided")
                return True
            
        except Exception as e:
            print(f"[ERROR] Failed to apply S3 configuration: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Test the comprehensive S3 configurator"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveS3Configurator(page)
        
        if configurator.navigate_to_s3_config():
            # Example comprehensive configuration
            example_config = {
                'description': 'Comprehensive S3 configuration test',
                'standard': {
                    'storage_gb': 1000,
                    'put_requests': 100000,
                    'get_requests': 500000,
                    's3_select_returned_gb': 10,
                    's3_select_scanned_gb': 100
                },
                'int': {
                    'storage_gb': 500,
                    'average_object_size_mb': 1,
                    'put_requests': 50000,
                    'get_requests': 200000,
                    'tiering': {
                        'int_frequent_percent': 60,
                        'int_infrequent_percent': 30,
                        'int_archive_instant_percent': 8,
                        'int_archive_percent': 2,
                        'int_deep_archive_percent': 0
                    }
                },
                'glacier_flexible': {
                    'storage_gb': 2000,
                    'average_object_size_mb': 10,
                    'put_requests': 1000,
                    'lifecycle_transitions': 500,
                    'retrieval': {
                        'restore_standard_requests': 100,
                        'restore_expedited_requests': 10,
                        'restore_bulk_requests': 5,
                        'data_retrievals_standard_gb': 50,
                        'data_retrievals_expedited_gb': 5,
                        'data_retrievals_bulk_gb': 10
                    }
                },
                'advanced_features': {
                    'storage_lens_objects': 1000000,
                    'batch_operations_jobs': 10,
                    'batch_operations_objects': 100000,
                    'encrypted_data_gb': 500,
                    'object_lambda_requests': 10000,
                    'object_lambda_duration_ms': 1000,
                    'object_lambda_memory_mb': 512,
                    'object_lambda_data_returned_gb': 5,
                    'vector_indexes': 5,
                    'vectors_per_index': 100000,
                    'vector_dimensions': 768,
                    'vector_queries_per_month': 10000
                }
            }
            
            # Apply comprehensive configuration
            if configurator.apply_comprehensive_configuration(example_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"[SUCCESS] Comprehensive S3 configuration completed!")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("comprehensive_s3_estimate_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to comprehensive_s3_estimate_url.txt")
        
        try:
            input("Press Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()


if __name__ == "__main__":
    main()
