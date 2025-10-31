#!/usr/bin/env python3
"""
AWS CloudWatch Service Auto Demo
Demonstrates AWS CloudWatch configuration flow
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS CLOUDWATCH SERVICE AUTO DEMO")
    print("=" * 80)
    
    cloudwatch_config = {
        "description": "CloudWatch monitoring for production",
        "region": "us-east-1",
        # Use plausible fields; actual mapping will depend on real UI
        "custom_metrics": 100,
        "logs_ingested_gb": 50,
        "alarms": 10,
        "api_requests": 10000
    }
    print("\n📋 Configuration:")
    for key, value in cloudwatch_config.items():
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
        print("\n[Step 2/4] Searching for AWS CloudWatch service...")
        print("\n[Step 3/4] Adding AWS CloudWatch service...")
        cloudwatch_services = {"cloudwatch": [cloudwatch_config]}
        results = builder.add_multiple_services(cloudwatch_services)
        r = results.get('cloudwatch', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ AWS CloudWatch service added successfully!")
        else:
            print("❌ Failed to add AWS CloudWatch service")
            return
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("cloudwatch_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: cloudwatch_estimate_url.txt")
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
