"""
Schema Validator - Validate LLM outputs against service schemas
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path


class SchemaValidator:
    """Validates service configurations against their schemas"""
    
    def __init__(self, schemas_path: str = None):
        self.schemas_path = schemas_path or str(Path(__file__).parent.parent / "schemas" / "service_schemas.json")
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict[str, Any]:
        """Load service schemas"""
        try:
            with open(self.schemas_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load schemas: {e}")
            return {}
    
    def validate_service_config(self, service_type: str, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a service configuration against its schema
        
        Args:
            service_type: Type of service (e.g., 's3', 'ecs_fargate')
            config: Configuration dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check if service type exists in schema
        if service_type not in self.schemas.get('services', {}):
            errors.append(f"Unknown service type: {service_type}")
            return False, errors
        
        schema = self.schemas['services'][service_type]
        schema_fields = schema.get('fields', {})
        
        # Check required fields
        required_fields = self._get_required_fields(schema_fields)
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate field types and values
        for field_name, field_value in config.items():
            if field_name in schema_fields:
                field_errors = self._validate_field(field_name, field_value, schema_fields[field_name])
                errors.extend(field_errors)
            else:
                errors.append(f"Unknown field: {field_name}")
        
        return len(errors) == 0, errors
    
    def _get_required_fields(self, schema_fields: Dict[str, str]) -> List[str]:
        """Extract required fields from schema"""
        required = []
        for field_name, field_type in schema_fields.items():
            # Fields without "optional" in description are required
            if "optional" not in field_type.lower():
                required.append(field_name)
        return required
    
    def _validate_field(self, field_name: str, field_value: Any, field_type: str) -> List[str]:
        """Validate a single field against its type definition"""
        errors = []
        
        # Extract base type from field type string
        base_type = field_type.split()[0].lower()
        
        # Type validation
        if base_type == "string":
            if not isinstance(field_value, str):
                errors.append(f"Field '{field_name}' should be string, got {type(field_value).__name__}")
        elif base_type == "integer":
            if not isinstance(field_value, int):
                errors.append(f"Field '{field_name}' should be integer, got {type(field_value).__name__}")
        elif base_type == "number":
            if not isinstance(field_value, (int, float)):
                errors.append(f"Field '{field_name}' should be number, got {type(field_value).__name__}")
        elif base_type == "boolean":
            if not isinstance(field_value, bool):
                errors.append(f"Field '{field_name}' should be boolean, got {type(field_value).__name__}")
        
        # Value validation for specific fields
        if field_name == "region":
            if not isinstance(field_value, str) or len(field_value) < 3:
                errors.append(f"Field '{field_name}' should be a valid AWS region")
        
        elif field_name == "storage_gb":
            if not isinstance(field_value, (int, float)) or field_value < 0:
                errors.append(f"Field '{field_name}' should be a positive number")
        
        elif field_name == "memory_gb":
            if not isinstance(field_value, (int, float)) or field_value <= 0:
                errors.append(f"Field '{field_name}' should be a positive number")
        
        elif field_name == "number_of_tasks":
            if not isinstance(field_value, int) or field_value <= 0:
                errors.append(f"Field '{field_name}' should be a positive integer")
        
        return errors
    
    def validate_multiple_services(self, services_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
        """
        Validate multiple service configurations
        
        Args:
            services_dict: Dictionary of service types to configurations
            
        Returns:
            Dictionary with validation results for each service
        """
        results = {}
        
        for service_type, configs_list in services_dict.items():
            service_results = {
                'total': len(configs_list),
                'valid': 0,
                'invalid': 0,
                'errors': []
            }
            
            for i, config in enumerate(configs_list):
                is_valid, errors = self.validate_service_config(service_type, config)
                
                if is_valid:
                    service_results['valid'] += 1
                else:
                    service_results['invalid'] += 1
                    service_results['errors'].append({
                        'instance': i,
                        'config': config,
                        'errors': errors
                    })
            
            results[service_type] = service_results
        
        return results
    
    def get_schema_for_service(self, service_type: str) -> Optional[Dict[str, Any]]:
        """Get schema for a specific service type"""
        return self.schemas.get('services', {}).get(service_type)
    
    def list_available_services(self) -> List[str]:
        """Get list of available service types"""
        return list(self.schemas.get('services', {}).keys())
    
    def get_field_info(self, service_type: str, field_name: str) -> Optional[str]:
        """Get information about a specific field"""
        schema = self.get_schema_for_service(service_type)
        if schema and 'fields' in schema:
            return schema['fields'].get(field_name)
        return None


def main():
    """Test the schema validator"""
    print("Testing Schema Validator...")
    
    validator = SchemaValidator()
    
    # Test valid S3 configuration
    valid_s3_config = {
        "description": "Test S3 bucket",
        "region": "us-east-1",
        "storage_gb": 100,
        "storage_class": "Standard",
        "put_requests": 1000,
        "get_requests": 5000,
        "data_transfer_out_gb": 10
    }
    
    is_valid, errors = validator.validate_service_config("s3", valid_s3_config)
    print(f"Valid S3 config: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Test invalid configuration
    invalid_config = {
        "description": "Invalid config",
        "storage_gb": "not_a_number",  # Should be number
        "region": "us-east-1"
    }
    
    is_valid, errors = validator.validate_service_config("s3", invalid_config)
    print(f"Invalid config: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Test multiple services
    test_services = {
        "s3": [valid_s3_config],
        "ecs_fargate": [{
            "description": "Test Fargate",
            "region": "us-east-1",
            "number_of_tasks": 1,
            "memory_gb": 1
        }]
    }
    
    results = validator.validate_multiple_services(test_services)
    print(f"Multiple service validation: {results}")


if __name__ == "__main__":
    main()
