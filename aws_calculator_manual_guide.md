
# Manual AWS Pricing Calculator Setup Guide
## Project: Ody
## Total Estimated Cost: $10,500/year
## Budget: $10,000

## Step 1: Open AWS Pricing Calculator
1. Go to https://calculator.aws/#/estimate
2. Click "Create estimate"
3. Set region to "US East (N. Virginia)"

## Step 2: Add Services (in this order)


### 1. CloudWatch - $900/year
**Description:** Monitoring and logging for ECS tasks, ALB, API Gateway and custom application logs.

**Steps:**
1. Click "Add service"
2. Search for "CloudWatch"
3. Select the service
4. Configure with these values:
   - Metrics: Custom metrics 50/month
   - Alarms: 20
   - Region: us-east-1
   - LogsStoragePerMonth: 50 GB
   - EstimatedMonthlyCost: $75
   - LogsIngestionPerMonth: 15 GB


### 2. KMS - $24/year
**Description:** Customer Master Key(s) for encrypting S3 objects and other resources.

**Steps:**
1. Click "Add service"
2. Search for "Key Management Service"
3. Select the service
4. Configure with these values:
   - CustomerManagedKeys: 2
   - Region: us-east-1
   - KeyUsage: Encrypt/Decrypt for S3 and application
   - KeyMonthlyPrice: $1 each


### 3. WAF - $300/year
**Description:** Web Application Firewall protecting API Gateway / ALB with a set of rules.

**Steps:**
1. Click "Add service"
2. Search for "Web Application Firewall"
3. Select the service
4. Configure with these values:
   - RequestsPerMonth: 20M
   - WebACLs: 1
   - Region: us-east-1
   - EstimatedMonthlyRate: ~$25
   - Rules: 10 managed + 5 custom


### 4. API Gateway - $800/year
**Description:** Front-door API Gateway accepting API ingest traffic from clients.

**Steps:**
1. Click "Add service"
2. Search for "API Gateway"
3. Select the service
4. Configure with these values:
   - APIType: REST/HTTP
   - RequestsPerMonth: 10M
   - Region: us-east-1
   - EstimatedRequestRate: ~$66.67/month
   - DataTransferOutPerMonth: 50 GB


### 5. Application Load Balancer - $600/year
**Description:** ALB in public subnets for inbound traffic distribution to services.

**Steps:**
1. Click "Add service"
2. Search for "Application Load Balancer"
3. Select the service
4. Configure with these values:
   - HoursPerMonth: 730
   - Region: us-east-1
   - DataProcessedPerMonth: 1 TB
   - EstimatedMonthlyCost: ~$50
   - LCU: 1.5 average


### 6. Input S3 Bucket - $300/year
**Description:** S3 bucket for batch ingest and input artifacts.

**Steps:**
1. Click "Add service"
2. Search for "S3"
3. Select the service
4. Configure with these values:
   - AverageStorage: 500 GB
   - DataTransferOut: 100 GB/month
   - StorageClass: Standard
   - Region: us-east-1
   - PUT/GETRequestsPerMonth: 100k/200k
   - EstimatedMonthlyStorageCost: ~$25


### 7. Output S3 Bucket - $300/year
**Description:** S3 bucket for NDJSON outputs and artifacts produced by verdict generation.

**Steps:**
1. Click "Add service"
2. Search for "S3"
3. Select the service
4. Configure with these values:
   - AverageStorage: 500 GB
   - DataTransferOut: 200 GB/month
   - EventTriggers: S3->SQS
   - StorageClass: Standard
   - Region: us-east-1
   - PUT/GETRequestsPerMonth: 50k/150k
   - EstimatedMonthlyStorageCost: ~$25


### 8. ECS Fargate Cluster - $200/year
**Description:** ECS cluster using Fargate to run containerized services (cluster management overhead).

**Steps:**
1. Click "Add service"
2. Search for "ECS"
3. Select the service
4. Configure with these values:
   - FargateOverhead: management and orchestration
   - ClusterSize: 1 logical cluster
   - Region: us-east-1
   - MonthlyBaseline: ~$16.67
   - Scaling: auto (tasks billed separately)


### 9. Ingestion Service (Fargate task) - $2,000/year
**Description:** Ingest pipeline component (container on Fargate) handling API and S3 batch ingest.

**Steps:**
1. Click "Add service"
2. Search for "Fargate"
3. Select the service
4. Configure with these values:
   - AvgConcurrentTasks: 3
   - vCPU: 1 vCPU per task
   - Memory: 2 GB per task
   - TaskHoursPerMonth: 3 tasks * 730 hours
   - Region: us-east-1
   - EstimatedvCPUHours: 2190 vCPU-hours/month
   - EstimatedMonthlyCost: ~$166.67


### 10. Policy Evaluation Service (Fargate task) - $2,500/year
**Description:** Policy evaluation compute doing rule processing and AI integration (heavier workload).

**Steps:**
1. Click "Add service"
2. Search for "Fargate"
3. Select the service
4. Configure with these values:
   - AvgConcurrentTasks: 3
   - vCPU: 2 vCPU per task
   - Memory: 4 GB per task
   - TaskHoursPerMonth: 3 tasks * 730 hours
   - Region: us-east-1
   - EstimatedMonthlyCost: ~$208.33


### 11. Verdict Generation Service (Fargate task) - $1,200/year
**Description:** Generates final NDJSON outputs and integrates with S3/SQS and Bedrock for dual LLM eval.

**Steps:**
1. Click "Add service"
2. Search for "Fargate"
3. Select the service
4. Configure with these values:
   - AvgConcurrentTasks: 2
   - vCPU: 1 vCPU per task
   - Memory: 2 GB per task
   - TaskHoursPerMonth: 2 tasks * 730 hours
   - Region: us-east-1
   - EstimatedMonthlyCost: ~$100


### 12. SQS Queue - $150/year
**Description:** Simple Queue Service for optional async event processing and integration triggers.

**Steps:**
1. Click "Add service"
2. Search for "SQS"
3. Select the service
4. Configure with these values:
   - StandardQueue: yes
   - LongPoll: enabled
   - Region: us-east-1
   - MessagesPerMonth: 5M
   - EstimatedMonthlyCost: ~$12.50


### 13. AWS Bedrock - $1,226/year
**Description:** Managed foundation models for dual LLM evaluation called by the verdict generation/policy evaluation flows.

**Steps:**
1. Click "Add service"
2. Search for "Bedrock"
3. Select the service
4. Configure with these values:
   - AvgCallDuration: short/text-inference
   - UsageTier: on-demand
   - Region: us-east-1
   - EstimatedMonthlySpend: ~$102.17
   - ModelCallsPerMonth: 100k small-inference calls


## Step 3: Review and Save
1. Review all services in your estimate
2. Check total cost matches expected: ~$10,500/year
3. Click "Save estimate" or copy the URL
4. Share the estimate URL

## Services to Skip (No Cost)
- IAM: $0/year
- Shield: $0/year
- VPC (multi-AZ): $0/year
- Public Subnet (multi-AZ): $0/year
- Private Subnet (multi-AZ): $0/year

## Expected Results
- Total Annual Cost: $10,500
- Monthly Cost: ~$875.00
- Budget Remaining: $-500

## Troubleshooting
- If a service isn't found, try alternative names
- Some services may have different field names
- Free services (IAM, VPC, etc.) don't need to be added
- Save your estimate frequently to avoid losing work
