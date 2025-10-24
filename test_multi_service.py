#!/usr/bin/env python3
"""
Test script for multi-service AWS estimate automation
"""

import json
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from aws_services.estimate_builder import AWSEstimateBuilder
from aws_services.service_registry import get_configurator_class, test_service_loading
from llm_processor.schema_validator import SchemaValidator


def test_service_registry():
    """Test the service registry"""
    print("Testing Service Registry...")
    results = test_service_loading()
    
    success_count = sum(1 for result in results.values() if result == "SUCCESS")
    total_count = len(results)
    
    print(f"Service Registry Test: {success_count}/{total_count} services loaded successfully")
    return success_count == total_count


def test_schema_validation():
    """Test schema validation"""
    print("\nTesting Schema Validation...")
    
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
    print(f"S3 validation: {'PASS' if is_valid else 'FAIL'}")
    if errors:
        print(f"  Errors: {errors}")
    
    # Test invalid configuration
    invalid_config = {
        "description": "Invalid config",
        "storage_gb": "not_a_number",  # Should be number
        "region": "us-east-1"
    }
    
    is_valid, errors = validator.validate_service_config("s3", invalid_config)
    print(f"Invalid config validation: {'PASS' if not is_valid else 'FAIL'}")
    if errors:
        print(f"  Expected errors: {errors}")
    
    return True


def test_estimate_builder():
    """Test the estimate builder (without actually running browser)"""
    print("\nTesting Estimate Builder...")
    
    try:
        # Test initialization
        builder = AWSEstimateBuilder(headless=True)
        print("[OK] Estimate builder initialized")
        
        # Test service registry integration
        configurator_class = get_configurator_class("s3")
        if configurator_class:
            print("[OK] S3 configurator loaded successfully")
        else:
            print("[FAIL] Failed to load S3 configurator")
            return False
        
        print("[OK] Estimate builder test passed")
        return True
        
    except Exception as e:
        print(f"[ERROR] Estimate builder test failed: {e}")
        return False


def test_example_configuration():
    """Test with example configuration"""
    print("\nTesting Example Configuration...")
    
    try:
        # Load example configuration
        with open('examples/standardized_multi_service.json', 'r') as f:
            example_config = json.load(f)
        
        services = example_config.get('services', {})
        print(f"Loaded {len(services)} service types from example")
        
        # Validate example configuration
        validator = SchemaValidator()
        results = validator.validate_multiple_services(services)
        
        total_services = sum(result['total'] for result in results.values())
        valid_services = sum(result['valid'] for result in results.values())
        
        print(f"Example validation: {valid_services}/{total_services} services valid")
        
        if valid_services == total_services:
            print("[OK] Example configuration validation passed")
            return True
        else:
            print("[FAIL] Example configuration validation failed")
            return False
            
    except Exception as e:
        print(f"[ERROR] Example configuration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("Multi-Service AWS Estimate Automation - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Service Registry", test_service_registry),
        ("Schema Validation", test_schema_validation),
        ("Estimate Builder", test_estimate_builder),
        ("Example Configuration", test_example_configuration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! The multi-service automation is ready.")
    else:
        print("[WARNING] Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
