#!/usr/bin/env python3
"""
Service Field Mapping Overview
Shows all configured fields and their names for each AWS service
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aws_services.service_registry import SERVICE_REGISTRY

def show_service_fields():
    """Show all service field mappings"""
    
    print("=" * 100)
    print("🔍 AWS SERVICE FIELD MAPPING OVERVIEW")
    print("=" * 100)
    
    # Service configurations with their field names
    service_configs = {
        "s3": {
            "description": "S3 Storage Configuration",
            "fields": {
                "description": "Service description",
                "region": "AWS region",
                "storage_gb": "Storage amount in GB",
                "storage_class": "Storage class (standard, int, glacier_flexible, glacier_deep)",
                "put_requests": "Number of PUT requests",
                "get_requests": "Number of GET requests",
                "data_transfer_out_gb": "Data transfer out in GB",
                "data_returned_gb": "Data returned in GB"
            }
        },
        
        "alb": {
            "description": "Application Load Balancer Configuration",
            "fields": {
                "description": "Service description",
                "region": "AWS region",
                "alb_count": "Number of ALBs",
                "alb_ec2_processed_gb": "Processed data for EC2 targets (GB)",
                "alb_lambda_processed_gb": "Processed data for Lambda targets (GB)",
                "alb_new_connections": "New connections per second",
                "alb_connection_duration": "Connection duration in seconds",
                "alb_requests_per_second": "Requests per second",
                "alb_rule_evaluations": "Rule evaluations per request"
            }
        },
        
        "ec2": {
            "description": "EC2 Instance Configuration",
            "fields": {
                "description": "Service description",
                "region": "AWS region",
                "instance_type": "EC2 instance type (e.g., t3.medium)",
                "instance_count": "Number of instances",
                "hours_per_month": "Hours per month (730 for always-on)",
                "storage_gb": "Storage size in GB",
                "data_transfer_in_gb": "Data transfer in GB",
                "data_transfer_out_gb": "Data transfer out GB"
            }
        },
        
        "ecs_fargate": {
            "description": "ECS Fargate Configuration",
            "fields": {
                "description": "Service description",
                "region": "AWS region",
                "cpu_units": "CPU units (256, 512, 1024, etc.)",
                "memory_gb": "Memory in GB",
                "task_count": "Number of tasks",
                "hours_per_month": "Hours per month",
                "storage_gb": "Storage size in GB"
            }
        },
        
        "sqs": {
            "description": "Simple Queue Service Configuration",
            "fields": {
                "description": "Service description",
                "region": "AWS region",
                "requests": "Number of requests",
                "messages": "Number of messages",
                "data_transfer_gb": "Data transfer in GB"
            }
        },
        
        "vpc": {
            "description": "Virtual Private Cloud Configuration",
            "fields": {
                "description": "Service description",
                "region": "AWS region",
                "vpc_count": "Number of VPCs",
                "subnets_per_vpc": "Subnets per VPC",
                "nat_gateways": "Number of NAT Gateways",
                "vpc_endpoints": "Number of VPC Endpoints",
                "data_processed_gb": "Data processed in GB"
            }
        }
    }
    
    for service_name, config in service_configs.items():
        print(f"\n📋 {service_name.upper()} - {config['description']}")
        print("-" * 80)
        
        for field_name, field_description in config['fields'].items():
            print(f"   • {field_name:<25} → {field_description}")
    
    print("\n" + "=" * 100)
    print("⚠️  IMPORTANT FIELD LIMITS")
    print("=" * 100)
    
    limits = {
        "ALB": {
            "alb_ec2_processed_gb": "Max: 1 GB/hour",
            "alb_new_connections": "Max: 1,000,000 per second"
        },
        "S3": {
            "storage_gb": "No specific limit",
            "put_requests": "No specific limit",
            "get_requests": "No specific limit"
        },
        "EC2": {
            "instance_count": "No specific limit",
            "hours_per_month": "Max: 744 (31 days × 24 hours)"
        }
    }
    
    for service, service_limits in limits.items():
        print(f"\n🔒 {service} Limits:")
        for field, limit in service_limits.items():
            print(f"   • {field}: {limit}")
    
    print("\n" + "=" * 100)
    print("✅ RECOMMENDED VALUES FOR TESTING")
    print("=" * 100)
    
    recommended = {
        "s3": {
            "storage_gb": 100,
            "put_requests": 1000,
            "get_requests": 5000,
            "data_transfer_out_gb": 10
        },
        "alb": {
            "alb_count": 1,
            "alb_ec2_processed_gb": 0.1,  # 0.1 GB
            "alb_new_connections": 100,  # per second
            "alb_connection_duration": 300
        },
        "ec2": {
            "instance_count": 2,
            "hours_per_month": 730,
            "storage_gb": 50
        },
        "ecs_fargate": {
            "cpu_units": 512,
            "memory_gb": 1,
            "task_count": 2,
            "hours_per_month": 730
        },
        "sqs": {
            "requests": 1000000,
            "messages": 10000000
        },
        "vpc": {
            "vpc_count": 1,
            "subnets_per_vpc": 3,
            "nat_gateways": 1
        }
    }
    
    for service, values in recommended.items():
        print(f"\n📊 {service.upper()} Recommended Values:")
        for field, value in values.items():
            print(f"   • {field}: {value}")

if __name__ == "__main__":
    show_service_fields()
