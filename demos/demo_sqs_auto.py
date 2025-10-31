#!/usr/bin/env python3
"""
AWS SQS Service Auto Demo
Demonstrates AWS Simple Queue Service (SQS) configuration flow using all mapped fields
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS SQS SERVICE AUTO DEMO")
    print("=" * 80)
    
    sqs_config = {
        "description": "Demo SQS Queues for microservices messaging",
        "region": "us-east-1",
        "standard_queue_requests": 1000000,
        "fifo_queue_requests": 500000,
        "fair_queue_requests": 200000,
        "inbound_data_transfer_tb": 10,
        "outbound_data_transfer_tb": 5
    }
    
    print("\n📋 Configuration:")
    for key, value in sqs_config.items():
        if isinstance(value, int) and value >= 1000:
            print(f"   • {key}: {value:,}")
        else:
            print(f"   • {key}: {value}")
    
    print("\n" + "=" * 80)
    print("Running automation...")
    print("=" * 80)
    
    builder = AWSEstimateBuilder(headless=False)
    try:
        print("\n[Step 1/4] Creating estimate...")
        if not builder.start_session():
            print("❌ Failed to start estimate session")
            return
        print("✅ Estimate created ✓")
        
        print("\n[Step 2/4] Searching for Amazon SQS service...")
        print("\n[Step 3/4] Adding Amazon SQS service...")
        
        sqs_services = {"sqs": [sqs_config]}
        results = builder.add_multiple_services(sqs_services)
        r = results.get('sqs', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ Amazon SQS service added successfully!")
        else:
            print("❌ Failed to add Amazon SQS service")
            return
        
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("sqs_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: sqs_estimate_url.txt")
        else:
            print("❌ Failed to get estimate URL")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔒 Keeping browser open for inspection...")
        try:
            input("Press Enter to close...")
        except Exception:
            pass
        builder.close_session()

if __name__ == "__main__":
    main()

