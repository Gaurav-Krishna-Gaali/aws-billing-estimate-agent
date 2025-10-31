#!/usr/bin/env python3
"""
Multi-Service AWS Calculator Demo
Demonstrates the complete flow with multiple AWS services
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run multi-service demo"""
    
    print("=" * 80)
    print("🚀 MULTI-SERVICE AWS CALCULATOR DEMO")
    print("=" * 80)
    
    # Define multiple services configuration
    services_config = {
        "s3": [
            {
                "description": "Production S3 Storage",
                "region": "us-east-1",
                "storage_gb": 500,
                "storage_class": "standard",
                "put_requests": 10000,
                "get_requests": 50000,
                "data_transfer_out_gb": 100
            }
        ],
        "alb": [
            {
                "description": "Application Load Balancer",
                "region": "us-east-1",
                "alb_count": 2,
                "data_processed_gb": 1000,
                "new_connections": 1000000,
                "active_connections": 10000
            }
        ],
        "ec2": [
            {
                "description": "Web Server Instances",
                "region": "us-east-1",
                "instance_type": "t3.medium",
                "instance_count": 3,
                "hours_per_month": 730,
                "storage_gb": 100
            }
        ],
        "sqs": [
            {
                "description": "Message Queue",
                "region": "us-east-1",
                "requests": 1000000,
                "messages": 10000000
            }
        ]
    }
    
    print("\n📋 Services to be configured:")
    for service_type, instances in services_config.items():
        print(f"   • {service_type.upper()}: {len(instances)} instance(s)")
        for i, instance in enumerate(instances, 1):
            print(f"     {i}. {instance['description']}")
    
    print("\n" + "=" * 80)
    print("Running automation...")
    print("=" * 80)
    
    # Create estimate builder
    builder = AWSEstimateBuilder(headless=True)
    
    try:
        # Step 1: Start session
        print("\n[Step 1/3] Creating estimate...")
        if not builder.start_session():
            print("❌ Failed to start estimate session")
            return
        
        print("✅ Estimate created ✓")
        
        # Step 2: Add all services
        print("\n[Step 2/3] Adding services...")
        results = builder.add_multiple_services(services_config)
        
        # Print results
        print("\n📊 Service Addition Results:")
        total_successful = 0
        total_services = 0
        
        for service_type, result in results.items():
            successful = result['successful']
            total = result['total']
            total_successful += successful
            total_services += total
            
            status = "✅" if successful == total else "⚠️" if successful > 0 else "❌"
            print(f"   {status} {service_type.upper()}: {successful}/{total} successful")
        
        print(f"\n📈 Overall: {total_successful}/{total_services} services added successfully")
        
        # Step 3: Finalize estimate
        print("\n[Step 3/3] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        
        if estimate_url:
            print("✅ Estimate finalized ✓")
            print("\n" + "=" * 80)
            print("🎉 DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            print(f"\n📋 Summary:")
            print(f"   ✓ {total_successful} services configured")
            print(f"   ✓ Multi-service estimate created")
            print(f"   ✓ Shareable URL generated")
            
            # Save URL to file
            with open("multi_service_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print(f"\n💾 URL saved to: multi_service_estimate_url.txt")
            
        else:
            print("❌ Failed to finalize estimate")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        builder.close_session()
        print("\n🔒 Browser session closed")
        print("\nPress Enter to exit...")
        input()

if __name__ == "__main__":
    main()
