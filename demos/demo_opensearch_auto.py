#!/usr/bin/env python3
"""
AWS OpenSearch Service Auto Demo
Demonstrates AWS OpenSearch configuration flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run AWS OpenSearch demo"""
    
    print("=" * 80)
    print("🚀 AWS OPENSEARCH SERVICE AUTO DEMO")
    print("=" * 80)
    
    # AWS OpenSearch configuration (simplified for limited fields)
    opensearch_config = {
        "description": "Production OpenSearch Cluster",
        "region": "us-east-1"
        # OpenSearch has limited configurable fields in AWS Calculator
        # The configurator will try to find and fill available fields automatically
    }
    
    print("\n📋 Configuration:")
    for key, value in opensearch_config.items():
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
        
        # Step 2: Search for OpenSearch service
        print("\n[Step 2/4] Searching for OpenSearch service...")
        print("   → Searching: 'Amazon OpenSearch Service'")
        
        # Step 3: Add OpenSearch service
        print("\n[Step 3/4] Adding OpenSearch service...")
        print("   → Clicking Configure button")
        print("   → Filling configuration fields")
        print("   → Clicking 'Save and add service' button ⬅️ YOUR BUTTON!")
        
        # Add OpenSearch service
        opensearch_services = {"opensearch": [opensearch_config]}
        results = builder.add_multiple_services(opensearch_services)
        
        opensearch_result = results.get('opensearch', {'successful': 0, 'total': 0})
        if opensearch_result['successful'] > 0:
            print("✅ OpenSearch service added successfully!")
            print("   Button clicked: .appFooter button[data-cy='Save and add service-button']")
        else:
            print("❌ Failed to add OpenSearch service")
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
            print("  ✓ OpenSearch service searched")
            print("  ✓ Configure button clicked")
            print("  ✓ Fields filled")
            print("  ✓ 'Save and add service' button clicked")
            
            print("\nAll services follow this same pattern!")
            
            # Save URL
            with open("opensearch_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print(f"\n💾 URL saved to: opensearch_estimate_url.txt")
            
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
