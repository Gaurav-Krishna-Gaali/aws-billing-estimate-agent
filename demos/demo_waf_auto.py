#!/usr/bin/env python3
"""
AWS WAF Service Auto Demo
Demonstrates AWS Web Application Firewall (WAF) configuration flow using all mapped fields
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS WAF SERVICE AUTO DEMO")
    print("=" * 80)
    
    waf_config = {
        "description": "Demo WAF Protection for production web application",
        "region": "us-east-1",
        "web_acls": 2,
        "rules_per_web_acl": 10,
        "rule_groups_per_web_acl": 3,
        "rules_inside_rule_group": 5,
        "managed_rule_groups_per_web_acl": 2,
        "web_requests_received": 1000000
    }
    
    print("\n📋 Configuration:")
    for key, value in waf_config.items():
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
        
        print("\n[Step 2/4] Searching for AWS WAF service...")
        print("\n[Step 3/4] Adding AWS WAF service...")
        
        waf_services = {"waf": [waf_config]}
        results = builder.add_multiple_services(waf_services)
        r = results.get('waf', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ AWS WAF service added successfully!")
        else:
            print("❌ Failed to add AWS WAF service")
            return
        
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("waf_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: waf_estimate_url.txt")
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

