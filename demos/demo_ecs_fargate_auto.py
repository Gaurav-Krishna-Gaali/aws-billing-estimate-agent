#!/usr/bin/env python3
"""
AWS ECS Fargate Service Auto Demo
Demonstrates AWS ECS Fargate configuration flow
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws_services.estimate_builder import AWSEstimateBuilder

def main():
    print("=" * 80)
    print("🚀 AWS ECS FARGATE SERVICE AUTO DEMO")
    print("=" * 80)
    
    ecs_config = {
        "description": "Production Fargate workload",
        "region": "us-east-1",
        "cpu_units": 1024,  # 1 vCPU
        "memory_gb": 2,     # 2GB RAM
        "task_count": 5,
        "hours_per_month": 730,
        "storage_gb": 20    # ephemeral storage
    }
    print("\n📋 Configuration:")
    for key, value in ecs_config.items():
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
        print("\n[Step 2/4] Searching for AWS ECS Fargate service...")
        print("\n[Step 3/4] Adding AWS ECS Fargate service...")
        ecs_services = {"ecs_fargate": [ecs_config]}
        results = builder.add_multiple_services(ecs_services)
        r = results.get('ecs_fargate', {'successful': 0, 'total': 0})
        if r['successful'] > 0:
            print("✅ AWS ECS Fargate service added successfully!")
        else:
            print("❌ Failed to add AWS ECS Fargate service")
            return
        print("\n[Step 4/4] Finalizing estimate...")
        estimate_url = builder.finalize_estimate()
        if estimate_url:
            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETE!")
            print("=" * 80)
            print(f"\n🔗 Estimate URL: {estimate_url}")
            with open("ecs_fargate_estimate_url.txt", "w") as f:
                f.write(estimate_url)
            print("\n💾 URL saved to: ecs_fargate_estimate_url.txt")
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
