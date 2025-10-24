"""
Service Registry - Dynamic loading of AWS service configurators
Maps service names to their configurator classes for dynamic import
"""

import importlib
import sys
import os
from typing import Optional, Type, Any

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Service registry mapping service names to (module_path, class_name)
SERVICE_REGISTRY = {
    's3': ('s3.s3_configurator', 'ComprehensiveS3Configurator'),
    'ecs_fargate': ('ecs_fargate.ecs_fargate_configurator', 'ComprehensiveECSFargateConfigurator'),
    'alb': ('alb.alb_configurator', 'ComprehensiveALBConfigurator'),
    'api_gateway': ('api_gateway.api_gateway_configurator', 'ComprehensiveAPIGatewayConfigurator'),
    'lambda': ('aws_lambda.lambda_configurator', 'ComprehensiveAWSLambdaConfigurator'),
    'cloudwatch': ('cloudwatch.cloudwatch_configurator', 'ComprehensiveCloudWatchConfigurator'),
    'iam': ('iam.iam_configurator', 'ComprehensiveIAMConfigurator'),
    'kms': ('aws_kms.kms_configurator', 'ComprehensiveAWSKMSConfigurator'),
    'shield': ('aws_shield.shield_configurator', 'ComprehensiveAWSShieldConfigurator'),
    'waf': ('waf.waf_configurator', 'ComprehensiveWAFConfigurator'),
    'vpc': ('vpc.comprehensive_vpc_configurator', 'ComprehensiveVPCConfigurator'),
    'sqs': ('sqs.sqs_configurator', 'ComprehensiveSQSConfigurator'),
    'ec2': ('ec2.ec2_configurator', 'ComprehensiveEC2Configurator'),
    'opensearch': ('aws_opensearch.opensearch_configurator', 'ComprehensiveAWSOpenSearchConfigurator'),
    'bedrock': ('bedrock.bedrock_configurator', 'BedrockConfigurator')
}

# Alternative service name mappings (for flexibility)
SERVICE_ALIASES = {
    'application_load_balancer': 'alb',
    'load_balancer': 'alb',
    'aws_lambda': 'lambda',
    'lambda_function': 'lambda',
    'api_gateway': 'api_gateway',
    'gateway': 'api_gateway',
    'aws_s3': 's3',
    'bucket': 's3',
    'aws_ecs': 'ecs_fargate',
    'fargate': 'ecs_fargate',
    'container': 'ecs_fargate',
    'aws_cloudwatch': 'cloudwatch',
    'monitoring': 'cloudwatch',
    'aws_iam': 'iam',
    'identity': 'iam',
    'aws_kms': 'kms',
    'encryption': 'kms',
    'aws_shield': 'shield',
    'ddos': 'shield',
    'aws_waf': 'waf',
    'firewall': 'waf',
    'aws_vpc': 'vpc',
    'network': 'vpc',
    'aws_sqs': 'sqs',
    'queue': 'sqs',
    'aws_ec2': 'ec2',
    'instance': 'ec2',
    'aws_opensearch': 'opensearch',
    'search': 'opensearch',
    'aws_bedrock': 'bedrock',
    'ai': 'bedrock',
    'llm': 'bedrock'
}


def normalize_service_name(service_name: str) -> str:
    """
    Normalize service name to registry key
    
    Args:
        service_name: Input service name (e.g., "Application Load Balancer", "S3")
        
    Returns:
        str: Normalized service name for registry lookup
    """
    # Convert to lowercase and remove common prefixes/suffixes
    normalized = service_name.lower().strip()
    
    # Remove common prefixes
    prefixes_to_remove = ['aws ', 'amazon ', 'aws_', 'amazon_']
    for prefix in prefixes_to_remove:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
    
    # Remove common suffixes
    suffixes_to_remove = [' service', ' configuration', ' setup', ' deployment']
    for suffix in suffixes_to_remove:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)]
    
    # Check aliases first
    if normalized in SERVICE_ALIASES:
        return SERVICE_ALIASES[normalized]
    
    # Direct lookup
    if normalized in SERVICE_REGISTRY:
        return normalized
    
    # Try partial matching
    for registry_key in SERVICE_REGISTRY.keys():
        if registry_key in normalized or normalized in registry_key:
            return registry_key
    
    # Return original if no match found
    return normalized


def get_configurator_class(service_type: str) -> Optional[Type[Any]]:
    """
    Dynamically import and return configurator class for a service
    
    Args:
        service_type: Service name (e.g., 's3', 'ecs_fargate', 'alb')
        
    Returns:
        Configurator class or None if not found
    """
    try:
        # Normalize service name
        normalized_service = normalize_service_name(service_type)
        
        if normalized_service not in SERVICE_REGISTRY:
            print(f"[ERROR] Service '{service_type}' not found in registry")
            print(f"[INFO] Available services: {list(SERVICE_REGISTRY.keys())}")
            return None
        
        module_path, class_name = SERVICE_REGISTRY[normalized_service]
        
        # Import the module
        module = importlib.import_module(module_path)
        
        # Get the class
        configurator_class = getattr(module, class_name)
        
        print(f"[INFO] Loaded configurator: {class_name} from {module_path}")
        return configurator_class
        
    except ImportError as e:
        print(f"[ERROR] Failed to import configurator for {service_type}: {e}")
        return None
    except AttributeError as e:
        print(f"[ERROR] Class not found in module for {service_type}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error loading configurator for {service_type}: {e}")
        return None


def list_available_services() -> list:
    """Get list of all available services"""
    return list(SERVICE_REGISTRY.keys())


def get_service_info(service_type: str) -> Optional[dict]:
    """
    Get information about a service
    
    Args:
        service_type: Service name
        
    Returns:
        Dict with service information or None
    """
    normalized_service = normalize_service_name(service_type)
    
    if normalized_service not in SERVICE_REGISTRY:
        return None
    
    module_path, class_name = SERVICE_REGISTRY[normalized_service]
    
    return {
        'service_name': normalized_service,
        'module_path': module_path,
        'class_name': class_name,
        'original_input': service_type
    }


def test_service_loading():
    """Test function to verify all services can be loaded"""
    print("Testing service registry...")
    
    results = {}
    
    for service_name in SERVICE_REGISTRY.keys():
        print(f"\nTesting {service_name}...")
        
        try:
            configurator_class = get_configurator_class(service_name)
            if configurator_class:
                results[service_name] = "SUCCESS"
                print(f"[OK] {service_name}: {configurator_class.__name__}")
            else:
                results[service_name] = "FAILED"
                print(f"[FAIL] {service_name}: Failed to load")
        except Exception as e:
            results[service_name] = f"ERROR: {e}"
            print(f"[ERROR] {service_name}: {e}")
    
    print(f"\nTest Results:")
    for service, result in results.items():
        print(f"  {service}: {result}")
    
    return results


if __name__ == "__main__":
    # Test the service registry
    test_service_loading()
