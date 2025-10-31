#!/usr/bin/env python3
"""
Simple Browser Test
Test if browser works at all
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Simple browser test"""
    
    print("🔍 SIMPLE BROWSER TEST")
    print("=" * 40)
    
    builder = AWSEstimateBuilder(headless=False)
    
    try:
        print("\n[1/2] Creating estimate...")
        if not builder.start_session():
            print("❌ Failed to start session")
            return
        print("✅ Estimate created")
        
        print("\n[2/2] Testing basic navigation...")
        print("Current URL:", builder.page.url)
        
        # Just wait and see if browser stays open
        print("Browser should be open now...")
        print("Press Enter to close...")
        input()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        builder.close_session()

if __name__ == "__main__":
    main()
