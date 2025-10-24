# LLM Mapping Instructions for SOW to AWS Service Schemas

## Overview
This document provides instructions for mapping unstructured SOW (Statement of Work) JSON data to standardized AWS service configuration schemas.

## Input Format
The input will be a JSON structure containing service estimates with the following format:
```json
{
  "result": {
    "estimate": [
      {
        "estimated_yearly_price": 900,
        "service_name": "CloudWatch",
        "configurations": {
          "Metrics": "Custom metrics 50/month",
          "Alarms": "20",
          "Region": "us-east-1",
          "LogsStoragePerMonth": "50 GB",
          "EstimatedMonthlyCost": "$75",
          "LogsIngestionPerMonth": "15 GB"
        },
        "description": "Monitoring and logging for ECS tasks, ALB, API Gateway and custom application logs."
      }
    ]
  }
}
```

## Output Format
Transform the input into standardized service configurations:
```json
{
  "services": {
    "cloudwatch": [
      {
        "description": "Monitoring and logging for ECS tasks, ALB, API Gateway and custom application logs.",
        "region": "us-east-1",
        "custom_metrics": 50,
        "alarms": 20,
        "logs_storage_gb": 50,
        "logs_ingestion_gb": 15
      }
    ]
  }
}
```

## Service Name Mapping Rules

### Direct Mappings
- "CloudWatch" → "cloudwatch"
- "S3" → "s3"
- "Lambda" → "lambda"
- "API Gateway" → "api_gateway"
- "Application Load Balancer" → "alb"
- "ECS Fargate" → "ecs_fargate"
- "IAM" → "iam"
- "KMS" → "kms"
- "Shield" → "shield"
- "WAF" → "waf"
- "VPC" → "vpc"
- "SQS" → "sqs"
- "EC2" → "ec2"
- "OpenSearch" → "opensearch"
- "Bedrock" → "bedrock"

### Complex Mappings
- "Input S3 Bucket" → "s3" (with description: "Input S3 Bucket")
- "Output S3 Bucket" → "s3" (with description: "Output S3 Bucket")
- "Ingestion Service (Fargate task)" → "ecs_fargate" (with description: "Ingestion Service")
- "Policy Evaluation Service (Fargate task)" → "ecs_fargate" (with description: "Policy Evaluation Service")
- "Verdict Generation Service (Fargate task)" → "ecs_fargate" (with description: "Verdict Generation Service")

## Field Mapping Rules

### Unit Conversions
- "50 GB" → 50 (for storage fields)
- "1 TB" → 1024 (for data transfer fields)
- "20M" → 20000000 (for request fields)
- "100k" → 100000 (for request fields)

### Default Values
- If region is missing: "us-east-1"
- If description is missing: Use service_name
- If numeric fields are missing: 0
- If boolean fields are missing: false

### Field Name Mappings

#### S3 Fields
- "AverageStorage" → "storage_gb"
- "PUT/GETRequestsPerMonth" → "put_requests"/"get_requests"
- "DataTransferOut" → "data_transfer_out_gb"
- "StorageClass" → "storage_class"

#### ECS Fargate Fields
- "AvgConcurrentTasks" → "number_of_tasks"
- "vCPU" → "vcpu_per_task"
- "Memory" → "memory_gb"
- "TaskHoursPerMonth" → "task_hours_per_month"

#### ALB Fields
- "DataProcessedPerMonth" → "alb_ec2_processed_bytes"
- "HoursPerMonth" → "alb_connection_duration"
- "LCU" → "alb_requests_per_second"

#### API Gateway Fields
- "RequestsPerMonth" → "requests_per_month"
- "DataTransferOutPerMonth" → "data_transfer_out_gb"
- "APIType" → "api_type"

#### CloudWatch Fields
- "Metrics" → "custom_metrics"
- "Alarms" → "alarms"
- "LogsStoragePerMonth" → "logs_storage_gb"
- "LogsIngestionPerMonth" → "logs_ingestion_gb"

#### IAM Fields
- "Users/Roles" → "users_roles"
- "ManagedPolicies" → "managed_policies"

#### KMS Fields
- "CustomerManagedKeys" → "customer_managed_keys"
- "KeyUsage" → "key_usage"
- "KeyMonthlyPrice" → "key_monthly_price"

#### Shield Fields
- "ProtectionScope" → "protection_scope"
- "Type" → "shield_type"
- "EstimatedCost" → "estimated_cost"

#### WAF Fields
- "RequestsPerMonth" → "requests_per_month"
- "WebACLs" → "web_acls"
- "Rules" → "rules"
- "EstimatedMonthlyRate" → "estimated_monthly_rate"

#### VPC Fields
- "NATGateways" → "nat_gateways"
- "Subnets" → "subnets"
- "AZs" → "availability_zones"
- "EstimatedCost" → "estimated_cost"

#### SQS Fields
- "StandardQueue" → "standard_queue"
- "LongPoll" → "long_poll"
- "MessagesPerMonth" → "messages_per_month"
- "EstimatedMonthlyCost" → "estimated_monthly_cost"

#### EC2 Fields
- "InstanceType" → "instance_type"
- "OperatingSystem" → "operating_system"
- "StorageGB" → "storage_amount_gb"
- "vCPUs" → "vcpu_per_task"
- "MemoryGB" → "memory_gb"

#### OpenSearch Fields
- "InstanceType" → "instance_type"
- "InstanceCount" → "instance_count"
- "StorageGB" → "storage_gb"
- "SearchRequestsPerMonth" → "search_requests_per_month"
- "IndexingRequestsPerMonth" → "indexing_requests_per_month"

#### Bedrock Fields
- "ModelCallsPerMonth" → "model_calls_per_month"
- "AvgCallDuration" → "avg_call_duration"
- "UsageTier" → "usage_tier"
- "EstimatedMonthlySpend" → "estimated_monthly_spend"

## Multiple Instances Handling

When multiple instances of the same service exist (e.g., multiple S3 buckets), create an array:
```json
{
  "services": {
    "s3": [
      {
        "description": "Input S3 Bucket",
        "storage_gb": 500,
        "put_requests": 100000,
        "get_requests": 200000
      },
      {
        "description": "Output S3 Bucket", 
        "storage_gb": 500,
        "put_requests": 50000,
        "get_requests": 150000
      }
    ]
  }
}
```

## Error Handling

- If a service cannot be mapped, skip it and log a warning
- If required fields are missing, use reasonable defaults
- If data types don't match, attempt conversion (e.g., "50" → 50)
- If a service appears multiple times with different configurations, create separate entries

## Output Validation

Ensure the output:
1. Contains only valid service types from the schema
2. Has all required fields for each service
3. Uses correct data types (numbers, not strings for numeric fields)
4. Includes proper descriptions for each service instance
5. Groups multiple instances of the same service into arrays
