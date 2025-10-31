#!/usr/bin/env python3
"""
API Gateway Service Auto Demo
Demonstrates API Gateway configuration flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    """Run API Gateway demo"""
    
    print("=" * 80)
    print("🚀 API GATEWAY SERVICE AUTO DEMO")
    print("=" * 80)
    
    # API Gateway configuration (using correct field names)
    api_gateway_config = {
        "description": "Production API Gateway",
        "region": "us-east-1",
        "http_api_requests": 1000000,  # 1M HTTP API requests
        "http_api_request_size_kb": 5,  # 5KB average request size
        "rest_api_requests": 500000,  # 500K REST API requests
        "websocket_messages": 2000000,  # 2M WebSocket messages
        "websocket_message_size_kb": 2,  # 2KB average message size
        "websocket_connection_duration_seconds": 300,  # 5 minutes
        "websocket_connection_rate": 100  # 100 connections per second
    }
    
    print("\n📋 Configuration:")
    for key, value in api_gateway_config.items():
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
        
        # Step 2: Search for API Gateway service
        print("\n[Step 2/4] Searching for API Gateway service...")
        print("   → Searching: 'Amazon API Gateway'")
        
        # Step 3: Add API Gateway service
        print("\n[Step 3/4] Adding API Gateway service...")
        print("   → Clicking Configure button")
        print("   → Filling configuration fields")
        print("   → Clicking 'Save and add service' button ⬅️ YOUR BUTTON!")
        
        # Add API Gateway service
        api_gateway_services = {"api_gateway": [api_gateway_config]}
        results = builder.add_multiple_services(api_gateway_services)
        
        api_gateway_result = results.get('api_gateway', {'successful': 0, 'total': 0})
        if api_gateway_result['successful'] > 0:
            print("✅ API Gateway service added successfully!")
            print("   Button clicked: .appFooter button[data-cy='Save and add service-button']")
        else:
            print("❌ Failed to add API Gateway service")
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
            print("  ✓ API Gateway service searched")
            print("  ✓ Configure button clicked")
            print("  ✓ Fields filled")
            print("  ✓ 'Save and add service' button clicked")
            
            print("\nAll services follow this same pattern!")
            
            # Save URL
            with open("api_gateway_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print(f"\n💾 URL saved to: api_gateway_estimate_url.txt")
            
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
