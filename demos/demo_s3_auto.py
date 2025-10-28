#!/usr/bin/env python3
"""
Auto Demo S3 Service - Runs automatically without pauses
Shows complete flow: Search → Configure → Fill Fields → Click Button
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from aws_services.estimate_builder import AWSEstimateBuilder

def demo_s3_auto():
    """Demonstrate S3 service automatically"""
    print("\n" + "="*80)
    print("🚀 S3 SERVICE AUTO DEMO")
    print("="*80)
    
    s3_config = {
        "description": "Demo S3 Storage Bucket",
        "region": "us-east-1",
        "storage_gb": 100,
        "storage_class": "Standard",
        "put_requests": 1000,
        "get_requests": 5000,
        "data_transfer_out_gb": 10
    }
    
    print("\n📋 Configuration:")
    for key, value in s3_config.items():
        print(f"   • {key}: {value}")
    
    print("\n" + "="*80)
    print("Running automation...")
    print("="*80)
    
    builder = AWSEstimateBuilder(headless=False)
    
    try:
        print("\n[Step 1/4] Creating estimate...")
        if not builder.start_session():
            print("❌ Failed to create estimate")
            return
        print("✅ Estimate created ✓")
        
        print("\n[Step 2/4] Searching for S3 service...")
        print("   → Searching: 'Amazon Simple Storage Service (S3)'")
        
        print("\n[Step 3/4] Adding S3 service...")
        print("   → Clicking Configure button")
        print("   → Filling configuration fields")
        print("   → Clicking 'Save and add service' button ⬅️ YOUR BUTTON!")
        
        success = builder.add_service("Amazon Simple Storage Service (S3)", s3_config)
        
        if success:
            print("✅ S3 service added successfully!")
            print(f"   Button clicked: .appFooter button[data-cy='Save and add service-button']")
        else:
            print("❌ Failed to add S3 service")
            return
        
        print("\n[Step 4/4] Finalizing estimate...")
        url = builder.finalize_estimate()
        
        if url:
            print("\n" + "="*80)
            print("✅ DEMO COMPLETE!")
            print("="*80)
            print(f"\nEstimate URL: {url}")
            print("\nSummary:")
            print("  ✓ S3 service searched")
            print("  ✓ Configure button clicked")
            print("  ✓ Fields filled")
            print("  ✓ 'Save and add service' button clicked")
            print("\nAll services follow this same pattern!")
        else:
            print("❌ Failed to get estimate URL")
        
        print("\nKeeping browser open for inspection...")
        input("Press Enter to close...")
        
    finally:
        builder.close_session()

if __name__ == "__main__":
    demo_s3_auto()

