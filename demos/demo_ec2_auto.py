#!/usr/bin/env python3
"""
AWS EC2 Service Auto Demo
Demonstrates AWS EC2 configuration flow
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS EC2 SERVICE AUTO DEMO")
    print("=" * 80)
    
    ec2_config = {
        "description": "Production EC2 workload",
        "region": "us-east-1",
        "instance_type": "t3.medium",
        "instance_count": 3,
        "hours_per_month": 730,
        "storage_gb": 50,
        "data_transfer_in_gb": 100,
        "data_transfer_out_gb": 200
    }
    print("\n📋 Configuration:")
    for key, value in ec2_config.items():
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
        print("\n[Step 2/4] Searching for AWS EC2 service...")
        print("\n[Step 3/4] Adding AWS EC2 service...")
        ec2_services = {"ec2": [ec2_config]}
        results = builder.add_multiple_services(ec2_services)
        r = results.get('ec2', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ AWS EC2 service added successfully!")
        else:
            print("❌ Failed to add AWS EC2 service")
            return
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("ec2_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: ec2_estimate_url.txt")
        else:
            print("❌ Failed to get estimate URL")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback; traceback.print_exc()
    finally:
        print("\n🔒 Keeping browser open for inspection...")
        try:
            input("Press Enter to close...")
        except Exception:
            pass
        builder.close_session()

if __name__ == "__main__":
    main()
