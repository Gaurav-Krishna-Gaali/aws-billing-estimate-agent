# Demo Scripts

This folder contains demonstration scripts for AWS service configuration.

## Available Demos

### 1. S3 Service - Interactive Demo
**File:** `demo_s3.py`

Interactive demonstration with pauses at each step for inspection.

```bash
python demos/demo_s3.py
```

**Features:**
- Pauses at each step
- Shows configuration being applied
- Waits for user confirmation
- Best for understanding the flow

### 2. S3 Service - Auto Demo
**File:** `demo_s3_auto.py`

Automatic demonstration that runs without pauses.

```bash
python demos/demo_s3_auto.py
```

**Features:**
- Runs automatically
- Shows progress messages
- Fast demonstration
- Best for quick demo

## What Each Demo Shows

Both demos demonstrate the complete flow:

1. **Search for Service**
   - Searches for: "Amazon Simple Storage Service (S3)"
   - Code: `search_and_select_service()`

2. **Click Configure**
   - Clicks: `button[aria-label='Configure Amazon Simple Storage Service (S3)']`
   - Code: Base class search_and_select_service

3. **Fill Configuration Fields**
   - Description, Storage GB, Put/Get requests
   - Code: `_apply_service_specific_config()`

4. **Click "Save and add service" Button** ⬅️ Key action!
   - Button: `.appFooter button[data-cy='Save and add service-button']`
   - Code: `aws_services/base_configurator.py:427`

## Configuration Used

```python
s3_config = {
    "description": "Demo S3 Storage Bucket",
    "region": "us-east-1",
    "storage_gb": 100,
    "storage_class": "Standard",
    "put_requests": 1000,
    "get_requests": 5000,
    "data_transfer_out_gb": 10
}
```

## Expected Output

```
🚀 S3 SERVICE AUTO DEMO
================================================================================

📋 Configuration:
   • description: Demo S3 Storage Bucket
   • region: us-east-1
   • storage_gb: 100
   • storage_class: Standard
   • put_requests: 1000
   • get_requests: 5000
   • data_transfer_out_gb: 10

[Step 1/4] Creating estimate...
✅ Estimate created ✓

[Step 2/4] Searching for S3 service...

[Step 3/4] Adding S3 service...
✅ S3 service added successfully!
   Button clicked: .appFooter button[data-cy='Save and add service-button']

[Step 4/4] Finalizing estimate...

✅ DEMO COMPLETE!
Estimate URL: https://calculator.aws/...

Summary:
  ✓ S3 service searched
  ✓ Configure button clicked
  ✓ Fields filled
  ✓ 'Save and add service' button clicked

All services follow this same pattern!
```

## Key Takeaways

- All services (S3, ALB, EC2, ECS Fargate, SQS, VPC) follow the same pattern
- Same button is clicked: `.appFooter button[data-cy='Save and add service-button']`
- Flow is standardized across all services
- Code location: `aws_services/base_configurator.py:427`

