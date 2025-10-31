#!/usr/bin/env python3
"""
AWS Shield Service Auto Demo
Demonstrates AWS Shield configuration flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run AWS Shield demo"""
    
    print("=" * 80)
    print("🚀 AWS SHIELD SERVICE AUTO DEMO")
    print("=" * 80)
    
    # AWS Shield configuration
    shield_config = {
        "description": "Production DDoS protection",
        "region": "us-east-1",
        "cloudfront_usage": 1000,
        "elb_usage": 500,
        "elastic_ip_usage": 10,
        "global_accelerator_usage": 200
    }
    
    print("\n📋 Configuration:")
    for key, value in shield_config.items():
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
        
        print("\n[Step 2/4] Searching for AWS Shield service...")
        
        print("\n[Step 3/4] Adding AWS Shield service...")
        shield_services = {"shield": [shield_config]}
        results = builder.add_multiple_services(shield_services)
        r = results.get('shield', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ AWS Shield service added successfully!")
        else:
            print("❌ Failed to add AWS Shield service")
            return
        
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("shield_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: shield_estimate_url.txt")
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
