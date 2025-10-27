#!/usr/bin/env python3
"""
Multi-Service AWS Estimate Runner
Main script: SOW JSON → AWS Calculator Shareable URL

Usage:
  python run_multi_service_estimate.py input.json
  python run_multi_service_estimate.py input.json --llm-process
  python run_multi_service_estimate.py input.json --output estimate_url.txt
  python run_multi_service_estimate.py input.json --headless
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from llm_processor.sow_to_schema_mapper import SOWToSchemaMapper
from llm_processor.schema_validator import SchemaValidator
from aws_services.estimate_builder import AWSEstimateBuilder


def load_input_file(input_path: str) -> Dict[str, Any]:
    """Load and parse input JSON file"""
    try:
        with open(input_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in input file: {e}")
        sys.exit(1)


def process_with_llm(input_data: Dict[str, Any], region: str = 'us-east-1', model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0') -> Dict[str, Any]:
    """Process input data with AWS Bedrock to standardize service configurations"""
    print("[INFO] Processing input with AWS Bedrock...")
    
    try:
        mapper = SOWToSchemaMapper(region=region, model_id=model_id)
        standardized = mapper.map_sow_to_schemas(input_data)
        
        if not standardized:
            print("[ERROR] Bedrock processing failed to produce any services")
            return {}
        
        print(f"[SUCCESS] Bedrock processing completed. {len(standardized)} service types found")
        return standardized
        
    except Exception as e:
        print(f"[ERROR] Bedrock processing failed: {e}")
        print("Make sure you have AWS credentials configured and Bedrock access enabled")
        return {}


def validate_services(services_dict: Dict[str, Any]) -> bool:
    """Validate service configurations against schemas"""
    print("[INFO] Validating service configurations...")
    
    try:
        validator = SchemaValidator()
        results = validator.validate_multiple_services(services_dict)
        
        total_services = sum(result['total'] for result in results.values())
        valid_services = sum(result['valid'] for result in results.values())
        invalid_services = sum(result['invalid'] for result in results.values())
        
        print(f"[INFO] Validation results: {valid_services}/{total_services} services valid")
        
        if invalid_services > 0:
            print("[WARNING] Some services failed validation:")
            for service_type, result in results.items():
                if result['invalid'] > 0:
                    print(f"  {service_type}: {result['invalid']} invalid configuration(s)")
                    for error in result['errors']:
                        print(f"    Instance {error['instance']}: {error['errors']}")
        
        return invalid_services == 0
        
    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        return False


def build_estimate(services_dict: Dict[str, Any], headless: bool = False) -> Optional[str]:
    """Build AWS estimate with multiple services"""
    print("[INFO] Building AWS estimate...")
    
    builder = AWSEstimateBuilder(headless=headless)
    
    try:
        # Start session
        if not builder.start_session():
            print("[ERROR] Failed to start estimate session")
            return None
        
        # Add services
        results = builder.add_multiple_services(services_dict)
        
        # Print results summary
        print("\n[INFO] Service addition results:")
        for service_type, result in results.items():
            print(f"  {service_type}: {result['successful']}/{result['total']} successful")
        
        # Finalize estimate
        url = builder.finalize_estimate()
        
        if url:
            print(f"[SUCCESS] Estimate created: {url}")
            return url
        else:
            print("[ERROR] Failed to create estimate URL")
            return None
            
    except Exception as e:
        print(f"[ERROR] Estimate building failed: {e}")
        return None
    finally:
        builder.close_session()


def save_estimate_url(url: str, output_path: str):
    """Save estimate URL to file"""
    try:
        with open(output_path, 'w') as f:
            f.write(url)
        print(f"[SUCCESS] Estimate URL saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save URL: {e}")


def save_standardized_json(services_dict: Dict[str, Any], output_path: str):
    """Save standardized services JSON to file"""
    try:
        # Create a structured output with metadata
        output_data = {
            "metadata": {
                "generated_at": __import__('datetime').datetime.now().isoformat(),
                "total_service_types": len(services_dict),
                "total_instances": sum(len(instances) for instances in services_dict.values()),
                "source": "aws_billing_automation"
            },
            "services": services_dict
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"[SUCCESS] Standardized JSON saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save JSON: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Multi-Service AWS Calculator Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process SOW with AWS Bedrock and create estimate
  python run_multi_service_estimate.py sow-analysis-Ody.json --llm-process
  
  # Use pre-standardized JSON
  python run_multi_service_estimate.py standardized_services.json
  
  # Run in headless mode
  python run_multi_service_estimate.py input.json --headless
  
  # Use different AWS region and model
  python run_multi_service_estimate.py input.json --llm-process --region us-west-2 --model-id anthropic.claude-3-haiku-20240307-v1:0
  
  # Save URL to specific file
  python run_multi_service_estimate.py input.json --output my_estimate.txt
  
  # Save standardized JSON output
  python run_multi_service_estimate.py sow-analysis-Ody.json --llm-process --save-json standardized_output.json
        """
    )
    
    parser.add_argument('input_file', help='Input JSON file (SOW or standardized)')
    parser.add_argument('--llm-process', action='store_true', 
                       help='Process input with AWS Bedrock first (for SOW JSON)')
    parser.add_argument('--output', default='estimate_url.txt',
                       help='Output file for estimate URL (default: estimate_url.txt)')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--region', default='us-east-1',
                       help='AWS region for Bedrock (default: us-east-1)')
    parser.add_argument('--model-id', default='anthropic.claude-3-sonnet-20240229-v1:0',
                       help='Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)')
    parser.add_argument('--save-json', 
                       help='Save standardized JSON output to file (e.g., --save-json output.json)')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate configurations, do not build estimate')
    
    args = parser.parse_args()
    
    # Check input file exists
    if not os.path.exists(args.input_file):
        print(f"[ERROR] Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Load input data
    print(f"[INFO] Loading input from: {args.input_file}")
    input_data = load_input_file(args.input_file)
    
    # Determine if we need Bedrock processing
    if args.llm_process:
        # Check for AWS credentials
        if not (os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_PROFILE')):
            print("[WARNING] No AWS credentials found. Make sure you have:")
            print("  - AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables, or")
            print("  - AWS_PROFILE configured, or")
            print("  - AWS credentials configured via 'aws configure'")
            print()
        
        # Process with Bedrock
        services_dict = process_with_llm(input_data, args.region, args.model_id)
        if not services_dict:
            print("[ERROR] Bedrock processing failed")
            sys.exit(1)
    else:
        # Assume already standardized
        if 'services' in input_data:
            services_dict = input_data['services']
        else:
            print("[ERROR] Input does not contain 'services' key. Use --llm-process for SOW JSON")
            sys.exit(1)
    
    # Validate services
    if not validate_services(services_dict):
        print("[WARNING] Some services failed validation, but continuing...")
    
    # Save standardized JSON if requested
    if args.save_json:
        save_standardized_json(services_dict, args.save_json)
    
    # If validate-only, stop here
    if args.validate_only:
        print("[INFO] Validation completed (--validate-only)")
        return
    
    # Build estimate
    estimate_url = build_estimate(services_dict, args.headless)
    
    if estimate_url:
        # Save URL
        save_estimate_url(estimate_url, args.output)
        
        print(f"\n[SUCCESS] Multi-service estimate completed!")
        print(f"[URL] {estimate_url}")
        print(f"[SAVE] URL saved to: {args.output}")
    else:
        print("[ERROR] Failed to create estimate")
        sys.exit(1)


if __name__ == "__main__":
    main()
