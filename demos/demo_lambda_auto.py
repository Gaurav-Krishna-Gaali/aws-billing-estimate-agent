#!/usr/bin/env python3
"""
AWS Lambda Service Auto Demo
Demonstrates AWS Lambda configuration flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run AWS Lambda demo"""
    
    print("=" * 80)
    print("🚀 AWS LAMBDA SERVICE AUTO DEMO")
    print("=" * 80)
    
    # AWS Lambda configuration (using correct field names and valid values)
    lambda_config = {
        "description": "Production Lambda Functions",
        "region": "us-east-1",
        "number_of_requests": 1000000,  # 1M requests per month
        "duration_ms": 1000,  # 1 second execution time
        "memory_mb": 512,  # 512MB memory per function
        "ephemeral_storage_mb": 1024,  # 1GB ephemeral storage
        "concurrency": 100,  # 100 concurrent executions
        # Remove provisioned concurrency fields to avoid validation errors
        # "provisioned_concurrency_enabled_hours": 0,  # No provisioned concurrency
        # "provisioned_concurrency_requests": 0,
        # "provisioned_concurrency_duration_ms": 0,
        # "provisioned_concurrency_memory_mb": 0
    }
    
    print("\n📋 Configuration:")
    for key, value in lambda_config.items():
        print(f"   • {key}: {value}")
    
    print("\n" + "=" * 80)
    print("Running automation...")
    print("=" * 80)
    
    # Create estimate builder
    builder = AWSEstimateBuilder(headless=False)
    
    try:
        # Step 1: Create estimate
        print("\n[Step 1/4] Creating estimate...")
        if not builder.start_session():
            print("❌ Failed to start estimate session")
            return
        print("✅ Estimate created ✓")
        
        # Step 2: Search for Lambda service
        print("\n[Step 2/4] Searching for Lambda service...")
        print("   → Searching: 'AWS Lambda'")
        
        # Step 3: Add Lambda service
        print("\n[Step 3/4] Adding Lambda service...")
        print("   → Clicking Configure button")
        print("   → Filling configuration fields")
        print("   → Clicking 'Save and add service' button ⬅️ YOUR BUTTON!")
        
        # Add Lambda service
        lambda_services = {"lambda": [lambda_config]}
        results = builder.add_multiple_services(lambda_services)
        
        lambda_result = results.get('lambda', {'successful': 0, 'total': 0})
        if lambda_result['successful'] > 0:
            print("✅ Lambda service added successfully!")
            print("   Button clicked: .appFooter button[data-cy='Save and add service-button']")
        else:
            print("❌ Failed to add Lambda service")
            return
        
        # Step 4: Finalize estimate
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            
            print("\n📋 Summary:")
            print("  ✓ Lambda service searched")
            print("  ✓ Configure button clicked")
            print("  ✓ Fields filled")
            print("  ✓ 'Save and add service' button clicked")
            
            print("\nAll services follow this same pattern!")
            
            # Save URL
            with open("lambda_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print(f"\n💾 URL saved to: lambda_estimate_url.txt")
            
        else:
            print("❌ Failed to get estimate URL")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🔒 Keeping browser open for inspection...")
        print("Press Enter to close...")
        input()
        builder.close_session()

if __name__ == "__main__":
    main()
