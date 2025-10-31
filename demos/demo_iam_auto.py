#!/usr/bin/env python3
"""
AWS IAM Service Auto Demo (Full Config)
Demonstrates AWS IAM configuration flow, covering all mappable fields
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS IAM SERVICE AUTO DEMO (FULL CONFIG)")
    print("=" * 80)
    
    iam_config = {
        "description": "IAM Access Analyzer for production",
        "region": "us-east-1",
        "accounts_to_monitor": 10,
        "average_roles_per_account": 25,
        "average_users_per_account": 100,
        "analyzers_per_account": 3,
        "check_no_new_access_requests": 2000,
        "check_access_not_granted_requests": 1200,
        "resources_to_monitor": 500
    }
    print("\n📋 Configuration:")
    for key, value in iam_config.items():
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
        print("\n[Step 2/4] Searching for AWS IAM service...")
        print("\n[Step 3/4] Adding AWS IAM service...")
        iam_services = {"iam": [iam_config]}
        results = builder.add_multiple_services(iam_services)
        r = results.get('iam', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ AWS IAM service added successfully!")
        else:
            print("❌ Failed to add AWS IAM service")
            return
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("iam_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: iam_estimate_url.txt")
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
