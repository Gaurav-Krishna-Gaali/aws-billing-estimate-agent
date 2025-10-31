#!/usr/bin/env python3
"""
AWS KMS Service Auto Demo
Demonstrates AWS Key Management Service configuration flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run AWS KMS demo"""
    
    print("=" * 80)
    print("🚀 AWS KMS SERVICE AUTO DEMO")
    print("=" * 80)
    
    # AWS KMS configuration (using correct field names)
    kms_config = {
        "description": "Production KMS Keys",
        "region": "us-east-1",
        "customer_managed_cmks": 5,  # 5 customer-managed CMKs
        "symmetric_requests": 100000,  # 100K symmetric requests
        "asymmetric_requests_non_rsa": 10000,  # 10K asymmetric requests (non-RSA)
        "asymmetric_requests_rsa_2048": 5000,  # 5K RSA 2048 requests
        "ecc_generate_data_key_pair_requests": 2000,  # 2K ECC requests
        "rsa_generate_data_key_pair_requests": 1000  # 1K RSA requests
    }
    
    print("\n📋 Configuration:")
    for key, value in kms_config.items():
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
        
        # Step 2: Search for KMS service
        print("\n[Step 2/4] Searching for KMS service...")
        print("   → Searching: 'AWS Key Management Service'")
        
        # Step 3: Add KMS service
        print("\n[Step 3/4] Adding KMS service...")
        print("   → Clicking Configure button")
        print("   → Filling configuration fields")
        print("   → Clicking 'Save and add service' button ⬅️ YOUR BUTTON!")
        
        # Add KMS service
        kms_services = {"kms": [kms_config]}
        results = builder.add_multiple_services(kms_services)
        
        kms_result = results.get('kms', {'successful': 0, 'total': 0})
        if kms_result['successful'] > 0:
            print("✅ KMS service added successfully!")
            print("   Button clicked: .appFooter button[data-cy='Save and add service-button']")
        else:
            print("❌ Failed to add KMS service")
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
            print("  ✓ KMS service searched")
            print("  ✓ Configure button clicked")
            print("  ✓ Fields filled")
            print("  ✓ 'Save and add service' button clicked")
            
            print("\nAll services follow this same pattern!")
            
            # Save URL
            with open("kms_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print(f"\n💾 URL saved to: kms_estimate_url.txt")
            
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
