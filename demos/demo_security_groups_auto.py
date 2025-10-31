#!/usr/bin/env python3
"""
AWS Security Groups Service Auto Demo
Demonstrates AWS Security Groups configuration flow using all mapped fields
Note: Security Groups are configured as part of EC2 in AWS Calculator
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS SECURITY GROUPS SERVICE AUTO DEMO")
    print("=" * 80)
    print("\n📝 Note: Security Groups are configured as part of EC2 in AWS Calculator")
    
    security_groups_config = {
        "description": "Demo Security Groups (web application)",
        "region": "us-east-1",
        "number_of_security_groups": 3,
        "number_of_inbound_rules": 6,
        "number_of_outbound_rules": 3,
        "number_of_http_rules": 1,
        "number_of_https_rules": 1,
        "number_of_ssh_rules": 1,
        "data_processed_gb": 200,
        "enable_http_access": True,
        "enable_https_access": True,
        "enable_ssh_access": True,
        "enable_restricted_access": True,
        "enable_web_server_access": True
    }
    
    print("\n📋 Configuration:")
    for key, value in security_groups_config.items():
        print(f"   • {key}: {value}")
    
    print("\n" + "=" * 80)
    print("Running automation...")
    print("=" * 80)
    
    # Note: Security Groups need to be registered in service_registry.py
    # For now, we'll use EC2 service and apply security groups config
    # Alternatively, we can use the security groups configurator directly
    builder = AWSEstimateBuilder(headless=False)
    try:
        print("\n[Step 1/4] Creating estimate...")
        if not builder.start_session():
            print("❌ Failed to start estimate session")
            return
        print("✅ Estimate created ✓")
        
        print("\n[Step 2/4] Adding EC2 service (Security Groups are part of EC2)...")
        print("\n[Step 3/4] Applying Security Groups configuration...")
        
        # Use EC2 service and pass security groups config
        # Note: This is a workaround since Security Groups are not a standalone service
        ec2_config = {
            "description": security_groups_config.get("description", "EC2 with Security Groups"),
            "region": security_groups_config.get("region", "us-east-1"),
            # Include security groups settings in EC2 config
            **security_groups_config
        }
        
        ec2_services = {"ec2": [ec2_config]}
        results = builder.add_multiple_services(ec2_services)
        r = results.get('ec2', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ EC2 service with Security Groups added successfully!")
        else:
            print("❌ Failed to add EC2 service with Security Groups")
            return
        
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("security_groups_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: security_groups_estimate_url.txt")
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

