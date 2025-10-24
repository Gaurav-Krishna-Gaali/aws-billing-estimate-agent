"""
SOW to Schema Mapper - LLM-powered transformation of SOW JSON to standardized service schemas
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    print("[WARNING] boto3 not available. Install with: pip install boto3")


class SOWToSchemaMapper:
    """
    Takes unstructured SOW JSON and maps to standardized service schemas using LLM
    """
    
    def __init__(self, region: str = 'us-east-1', model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0'):
        self.region = region
        self.model_id = model_id
        
        if not BOTO3_AVAILABLE:
            raise ValueError("boto3 not available. Install with: pip install boto3")
        
        # Initialize Bedrock client
        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=self.region)
        except Exception as e:
            raise ValueError(f"Failed to initialize Bedrock client: {e}")
        
        # Load service schemas
        self.schemas = self.load_schemas()
        
    def load_schemas(self) -> Dict[str, Any]:
        """Load service schemas from schemas/service_schemas.json"""
        try:
            schema_path = Path(__file__).parent.parent / "schemas" / "service_schemas.json"
            with open(schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load schemas: {e}")
            return {}
    
    def map_sow_to_schemas(self, sow_json: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Main method: Transform SOW to standardized format
        
        Args:
            sow_json: SOW JSON in the format from sow-analysis-Ody.json
            
        Returns:
            Dict with standardized service configurations:
            {
                's3': [{...}, {...}],
                'ecs_fargate': [{...}]
            }
        """
        try:
            print("[INFO] Starting SOW to schema mapping...")
            
            # Extract services from SOW
            services_data = self._extract_services_from_sow(sow_json)
            
            if not services_data:
                print("[WARNING] No services found in SOW data")
                return {}
            
            # Group services by type
            grouped_services = self._group_services_by_type(services_data)
            
            # Map each service group to standardized format
            standardized_services = {}
            
            for service_type, service_instances in grouped_services.items():
                print(f"[INFO] Processing {len(service_instances)} {service_type} service(s)...")
                
                mapped_instances = []
                for service_instance in service_instances:
                    mapped_instance = self._map_service(service_instance, service_type)
                    if mapped_instance:
                        mapped_instances.append(mapped_instance)
                
                if mapped_instances:
                    standardized_services[service_type] = mapped_instances
                    print(f"[SUCCESS] Mapped {len(mapped_instances)} {service_type} service(s)")
            
            print(f"[SUCCESS] Mapping completed. {len(standardized_services)} service types processed")
            return standardized_services
            
        except Exception as e:
            print(f"[ERROR] Failed to map SOW to schemas: {e}")
            return {}
    
    def _extract_services_from_sow(self, sow_json: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract service data from SOW JSON structure"""
        try:
            if 'result' in sow_json and 'estimate' in sow_json['result']:
                return sow_json['result']['estimate']
            elif 'estimate' in sow_json:
                return sow_json['estimate']
            else:
                print("[WARNING] Unexpected SOW JSON structure")
                return []
        except Exception as e:
            print(f"[ERROR] Failed to extract services from SOW: {e}")
            return []
    
    def _group_services_by_type(self, services_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group services by their normalized type"""
        grouped = {}
        
        for service in services_data:
            service_type = self._normalize_service_name(service.get('service_name', ''))
            if service_type not in grouped:
                grouped[service_type] = []
            grouped[service_type].append(service)
        
        return grouped
    
    def _normalize_service_name(self, service_name: str) -> str:
        """Normalize service name to match schema keys"""
        if not service_name:
            return 'unknown'
        
        # Convert to lowercase and clean up
        normalized = service_name.lower().strip()
        
        # Remove common prefixes
        prefixes_to_remove = ['aws ', 'amazon ', 'aws_', 'amazon_']
        for prefix in prefixes_to_remove:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
        
        # Remove common suffixes
        suffixes_to_remove = [' service', ' configuration', ' setup', ' deployment', ' (fargate task)', ' (multi-az)']
        for suffix in suffixes_to_remove:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
        
        # Direct mappings
        service_mappings = {
            'application load balancer': 'alb',
            'load balancer': 'alb',
            'aws lambda': 'lambda',
            'lambda function': 'lambda',
            'api gateway': 'api_gateway',
            'gateway': 'api_gateway',
            'aws s3': 's3',
            's3 bucket': 's3',
            'bucket': 's3',
            'aws ecs': 'ecs_fargate',
            'fargate': 'ecs_fargate',
            'container': 'ecs_fargate',
            'aws cloudwatch': 'cloudwatch',
            'monitoring': 'cloudwatch',
            'aws iam': 'iam',
            'identity': 'iam',
            'aws kms': 'kms',
            'encryption': 'kms',
            'aws shield': 'shield',
            'ddos': 'shield',
            'aws waf': 'waf',
            'firewall': 'waf',
            'aws vpc': 'vpc',
            'network': 'vpc',
            'aws sqs': 'sqs',
            'queue': 'sqs',
            'aws ec2': 'ec2',
            'instance': 'ec2',
            'aws opensearch': 'opensearch',
            'search': 'opensearch',
            'aws bedrock': 'bedrock',
            'ai': 'bedrock',
            'llm': 'bedrock'
        }
        
        # Check direct mappings
        if normalized in service_mappings:
            return service_mappings[normalized]
        
        # Check if it matches any schema key
        if normalized in self.schemas.get('services', {}):
            return normalized
        
        # Try partial matching
        for schema_key in self.schemas.get('services', {}).keys():
            if schema_key in normalized or normalized in schema_key:
                return schema_key
        
        # Default fallback
        return 'unknown'
    
    def _map_service(self, service_data: Dict[str, Any], service_type: str) -> Optional[Dict[str, Any]]:
        """Map one service using LLM with appropriate schema"""
        try:
            if service_type not in self.schemas.get('services', {}):
                print(f"[WARNING] No schema found for service type: {service_type}")
                return None
            
            schema = self.schemas['services'][service_type]
            
            # Create LLM prompt
            prompt = self._create_mapping_prompt(service_data, service_type, schema)
            
            # Call LLM
            response = self._call_llm(prompt)
            
            # Parse and validate response
            mapped_config = self._parse_llm_response(response, service_type, schema)
            
            if mapped_config:
                print(f"[SUCCESS] Mapped {service_data.get('service_name', 'unknown')} to {service_type}")
                return mapped_config
            else:
                print(f"[WARNING] Failed to map {service_data.get('service_name', 'unknown')}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Failed to map service {service_data.get('service_name', 'unknown')}: {e}")
            return None
    
    def _create_mapping_prompt(self, service_data: Dict[str, Any], service_type: str, schema: Dict[str, Any]) -> str:
        """Create LLM prompt for service mapping"""
        prompt = f"""
You are an expert at mapping AWS service configurations from SOW (Statement of Work) data to standardized schemas.

Given this AWS service description from a SOW:
{json.dumps(service_data, indent=2)}

Map it to this standardized schema for {service_type}:
{json.dumps(schema, indent=2)}

IMPORTANT RULES:
1. Return ONLY valid JSON matching the schema structure
2. Convert units appropriately (e.g., "50 GB" → 50, "1 TB" → 1024)
3. Use reasonable defaults for missing fields
4. Ensure all numeric fields are numbers, not strings
5. Include the description from the original service data
6. Set region to "us-east-1" if not specified

Return the mapped configuration as JSON:
"""
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call AWS Bedrock with the prompt"""
        try:
            # Prepare the request body for Claude model
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "temperature": 0.1,
                "system": "You are an expert at mapping AWS service configurations. Always return valid JSON.",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType="application/json"
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
                
        except Exception as e:
            print(f"[ERROR] Bedrock call failed: {e}")
            return ""
    
    def _parse_llm_response(self, response: str, service_type: str, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse and validate LLM response"""
        try:
            # Extract JSON from response (in case LLM adds extra text)
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
            else:
                json_str = response
            
            # Parse JSON
            mapped_config = json.loads(json_str)
            
            # Basic validation
            if not isinstance(mapped_config, dict):
                print(f"[ERROR] LLM response is not a dictionary for {service_type}")
                return None
            
            # Ensure required fields are present
            required_fields = ['description']
            for field in required_fields:
                if field not in mapped_config:
                    mapped_config[field] = f"{service_type} service"
            
            # Set default region if not present
            if 'region' not in mapped_config:
                mapped_config['region'] = 'us-east-1'
            
            print(f"[SUCCESS] Parsed LLM response for {service_type}")
            return mapped_config
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse LLM response as JSON for {service_type}: {e}")
            print(f"[DEBUG] Response: {response[:200]}...")
            return None
        except Exception as e:
            print(f"[ERROR] Failed to parse LLM response for {service_type}: {e}")
            return None


def main():
    """Test the SOW to schema mapper"""
    print("Testing SOW to Schema Mapper with AWS Bedrock...")
    
    # Load test SOW data
    try:
        with open('sow-analysis-Ody.json', 'r') as f:
            sow_data = json.load(f)
    except FileNotFoundError:
        print("[ERROR] Test SOW file not found: sow-analysis-Ody.json")
        return
    
    # Create mapper with Bedrock
    try:
        mapper = SOWToSchemaMapper(region='us-east-1', model_id='anthropic.claude-3-sonnet-20240229-v1:0')
    except Exception as e:
        print(f"[ERROR] Failed to initialize Bedrock client: {e}")
        print("Make sure you have AWS credentials configured and Bedrock access enabled")
        return
    
    # Map SOW to schemas
    result = mapper.map_sow_to_schemas(sow_data)
    
    # Print results
    print(f"\nMapping Results:")
    for service_type, instances in result.items():
        print(f"  {service_type}: {len(instances)} instance(s)")
        for i, instance in enumerate(instances):
            print(f"    {i+1}. {instance.get('description', 'No description')}")
    
    # Save results
    with open('mapped_services.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nResults saved to: mapped_services.json")


if __name__ == "__main__":
    main()
