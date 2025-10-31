#!/usr/bin/env python3
"""
ALB Service Auto Demo
Demonstrates Application Load Balancer configuration flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run ALB demo"""
    
    print("=" * 80)
    print("🚀 ALB SERVICE AUTO DEMO")
    print("=" * 80)
    
    # ALB configuration (using GB units)
    alb_config = {
        "description": "Production Application Load Balancer",
        "region": "us-east-1",
        "alb_count": 2,
        "alb_ec2_processed_gb": 0.5,  # 0.5 GB (within 1GB/hour limit)
        "alb_new_connections": 100,  # per second (within 1M/second limit)
        "alb_connection_duration": 300,  # seconds
        "alb_requests_per_second": 1000
    }
    
    print("\n📋 Configuration:")
    for key, value in alb_config.items():
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
        
        # Step 2: Search for ALB service
        print("\n[Step 2/4] Searching for ALB service...")
        print("   → Searching: 'Application Load Balancer'")
        
        # Step 3: Add ALB service
        print("\n[Step 3/4] Adding ALB service...")
        print("   → Clicking Configure button")
        print("   → Filling configuration fields")
        print("   → Clicking 'Save and add service' button ⬅️ YOUR BUTTON!")
        
        # Add ALB service
        alb_services = {"alb": [alb_config]}
        results = builder.add_multiple_services(alb_services)
        
        alb_result = results.get('alb', {'successful': 0, 'total': 0})
        if alb_result['successful'] > 0:
            print("✅ ALB service added successfully!")
            print("   Button clicked: .appFooter button[data-cy='Save and add service-button']")
        else:
            print("❌ Failed to add ALB service")
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
            print("  ✓ ALB service searched")
            print("  ✓ Configure button clicked")
            print("  ✓ Fields filled")
            print("  ✓ 'Save and add service' button clicked")
            
            print("\nAll services follow this same pattern!")
            
            # Save URL
            with open("alb_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print(f"\n💾 URL saved to: alb_estimate_url.txt")
            
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
