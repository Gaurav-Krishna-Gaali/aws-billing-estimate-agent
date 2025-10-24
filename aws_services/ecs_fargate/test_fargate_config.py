"""
Test ECS Fargate Configuration with Real Data
Uses the provided Fargate configuration to test the ECS Fargate configurator
"""

import json
import sys
import os
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from comprehensive_ecs_fargate_configurator import ComprehensiveECSFargateConfigurator

def test_fargate_configuration():
    """Test ECS Fargate configuration with the provided data"""
    
    # The provided Fargate configuration
    fargate_config = {
        "description": "Fargate tasks running backend API service returning structured responses",
        "number_of_instances": 4,
        "instance_type": "fargate-equivalent (2 vCPU, 4 GB)",
        "region": "us-east-1",
        "operating_system": "Linux",
        "purchase_option": "On-Demand",
        "tenancy": "Default",
        "enable_monitoring": True,
        "storage_type": "ephemeral",
        "storage_amount_gb": 50,
        "iops_per_volume": 0,
        "throughput_mbps": 0,
        "ebs_optimized": False,
        "instance_hours_per_month": 730,
        "spot_instance": False,
        "inbound_data_transfer_tb": 0,
        "outbound_data_transfer_tb": 40,
        "elastic_ip_count": 0,
        "load_balancer_enabled": False,
        "autoscaling_enabled": False,
        "licensing_cost": 0,
        "support_plan": "Basic",
        "os_software_cost": 0,
        "tagging_metadata": {
            "Environment": "Production",
            "Owner": "DevOps",
            "Project": "API Service"
        },
        "notes": "Estimated yearly price: $60,000 for ECS Fargate API Service configuration",
        "_metadata": {
            "version": 1.0,
            "last_updated": "2025-10-24",
            "created_by": "automated-mapping-script"
        }
    }
    
    print("[INFO] Testing ECS Fargate Configuration with Real Data")
    print("="*80)
    print(f"[INFO] Configuration: {fargate_config['description']}")
    print(f"[INFO] Number of Tasks: {fargate_config['number_of_instances']}")
    print(f"[INFO] Instance Type: {fargate_config['instance_type']}")
    print(f"[INFO] Region: {fargate_config['region']}")
    print(f"[INFO] Operating System: {fargate_config['operating_system']}")
    print(f"[INFO] Purchase Option: {fargate_config['purchase_option']}")
    print(f"[INFO] Monitoring Enabled: {fargate_config['enable_monitoring']}")
    print(f"[INFO] Storage: {fargate_config['storage_amount_gb']} GB {fargate_config['storage_type']}")
    print(f"[INFO] Outbound Data Transfer: {fargate_config['outbound_data_transfer_tb']} TB")
    print(f"[INFO] Estimated Yearly Price: $60,000")
    print("="*80)
    
    # Convert to ECS Fargate config format
    ecs_fargate_config = {
        "name": "Production API Service",
        "description": fargate_config["description"],
        "number_of_tasks": fargate_config["number_of_instances"],
        "average_duration_minutes": 60,  # Assuming 1 hour average duration
        "memory_gb": 4,  # From "4 GB" in instance_type
        "ephemeral_storage_gb": fargate_config["storage_amount_gb"]
    }
    
    print(f"\n[INFO] Converted ECS Fargate Configuration:")
    print(f"  - Number of Tasks: {ecs_fargate_config['number_of_tasks']}")
    print(f"  - Average Duration: {ecs_fargate_config['average_duration_minutes']} minutes")
    print(f"  - Memory: {ecs_fargate_config['memory_gb']} GB")
    print(f"  - Ephemeral Storage: {ecs_fargate_config['ephemeral_storage_gb']} GB")
    
    # Run the configuration
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        configurator = ComprehensiveECSFargateConfigurator(page)
        
        if configurator.navigate_to_ecs_fargate_config():
            print(f"\n[INFO] Successfully navigated to ECS Fargate configuration page")
            
            if configurator.apply_ecs_fargate_configuration(ecs_fargate_config):
                print(f"[OK] Applied ECS Fargate configuration successfully")
                
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"\n[SUCCESS] ECS Fargate configuration completed!")
                    print(f"[INFO] Configuration: {ecs_fargate_config['name']}")
                    print(f"[URL] Estimate URL: {url}")
                    
                    # Save URL to file
                    with open("fargate_api_service_url.txt", "w") as f:
                        f.write(url)
                    print(f"[SAVE] URL saved to fargate_api_service_url.txt")
                    
                    # Save the original configuration for reference
                    with open("fargate_api_service_config.json", "w") as f:
                        json.dump(fargate_config, f, indent=2)
                    print(f"[SAVE] Original configuration saved to fargate_api_service_config.json")
                    
                    browser.close()
                    return url
                else:
                    print("[ERROR] Failed to save configuration")
            else:
                print("[ERROR] Failed to apply ECS Fargate configuration")
        else:
            print("[ERROR] Failed to navigate to ECS Fargate configuration page")
        
        browser.close()
        return None

def analyze_fargate_configuration(config):
    """Analyze the Fargate configuration and show what will be configured"""
    print(f"\n[ANALYSIS] Fargate Configuration Analysis")
    print("="*60)
    
    # Calculate resource usage
    tasks = config.get('number_of_instances', 0)
    memory_gb = 4  # From instance_type
    storage_gb = config.get('storage_amount_gb', 0)
    outbound_tb = config.get('outbound_data_transfer_tb', 0)
    
    print(f"[INFO] Resource Analysis:")
    print(f"  - Total Tasks: {tasks}")
    print(f"  - Memory per Task: {memory_gb} GB")
    print(f"  - Total Memory: {tasks * memory_gb} GB")
    print(f"  - Storage per Task: {storage_gb} GB")
    print(f"  - Total Storage: {tasks * storage_gb} GB")
    print(f"  - Outbound Data Transfer: {outbound_tb} TB")
    
    # Calculate monthly costs (rough estimates)
    monthly_cost_per_task = 50  # Rough estimate for 2 vCPU, 4 GB Fargate
    total_monthly_cost = tasks * monthly_cost_per_task
    yearly_cost = total_monthly_cost * 12
    
    print(f"\n[INFO] Cost Analysis:")
    print(f"  - Estimated Monthly Cost per Task: ${monthly_cost_per_task}")
    print(f"  - Total Monthly Cost: ${total_monthly_cost}")
    print(f"  - Estimated Yearly Cost: ${yearly_cost}")
    print(f"  - Provided Estimate: $60,000")
    print(f"  - Difference: ${abs(yearly_cost - 60000)}")
    
    # Calculate data transfer costs
    data_transfer_cost_per_tb = 90  # AWS data transfer out cost
    data_transfer_cost = outbound_tb * data_transfer_cost_per_tb
    
    print(f"\n[INFO] Data Transfer Analysis:")
    print(f"  - Outbound Data Transfer: {outbound_tb} TB")
    print(f"  - Data Transfer Cost per TB: ${data_transfer_cost_per_tb}")
    print(f"  - Monthly Data Transfer Cost: ${data_transfer_cost}")
    print(f"  - Yearly Data Transfer Cost: ${data_transfer_cost * 12}")

def main():
    """Main function"""
    print("[INFO] ECS Fargate Configuration Test with Real Data")
    print("[INFO] Testing with Production API Service configuration")
    
    # The provided configuration
    fargate_config = {
        "description": "Fargate tasks running backend API service returning structured responses",
        "number_of_instances": 4,
        "instance_type": "fargate-equivalent (2 vCPU, 4 GB)",
        "region": "us-east-1",
        "operating_system": "Linux",
        "purchase_option": "On-Demand",
        "tenancy": "Default",
        "enable_monitoring": True,
        "storage_type": "ephemeral",
        "storage_amount_gb": 50,
        "iops_per_volume": 0,
        "throughput_mbps": 0,
        "ebs_optimized": False,
        "instance_hours_per_month": 730,
        "spot_instance": False,
        "inbound_data_transfer_tb": 0,
        "outbound_data_transfer_tb": 40,
        "elastic_ip_count": 0,
        "load_balancer_enabled": False,
        "autoscaling_enabled": False,
        "licensing_cost": 0,
        "support_plan": "Basic",
        "os_software_cost": 0,
        "tagging_metadata": {
            "Environment": "Production",
            "Owner": "DevOps",
            "Project": "API Service"
        },
        "notes": "Estimated yearly price: $60,000 for ECS Fargate API Service configuration",
        "_metadata": {
            "version": 1.0,
            "last_updated": "2025-10-24",
            "created_by": "automated-mapping-script"
        }
    }
    
    # Analyze the configuration
    analyze_fargate_configuration(fargate_config)
    
    # Test the configuration
    print(f"\n[INFO] Running ECS Fargate configuration test...")
    url = test_fargate_configuration()
    
    if url:
        print(f"\n[SUCCESS] ECS Fargate configuration test completed!")
        print(f"[URL] Your Fargate API Service estimate URL: {url}")
        print(f"[INFO] This configuration represents a production API service")
        print(f"[INFO] with 4 Fargate tasks, 2 vCPU/4GB each, running 24/7")
        print(f"[INFO] Estimated yearly cost: $60,000")
    else:
        print(f"\n[ERROR] ECS Fargate configuration test failed")

if __name__ == "__main__":
    main()

