# Multi-Service AWS Calculator Flow

## Overview

This system allows you to create AWS estimates with multiple services in a single browser session. Each service can navigate from the service search page, fill in its configuration fields, and click "Save and add service" to return control to the estimate builder.

## Architecture

### Entry Point: `run_multi_service_estimate.py`
- Opens browser once
- Creates estimate once  
- Calls each service to configure and add itself
- Gets final shareable URL

### Service Flow:
1. **Estimate Builder** creates estimate and navigates to "Add service" page
2. **Service** receives the page context
3. **Service** searches for itself and navigates to its config page
4. **Service** fills in configuration fields
5. **Service** clicks "Save and add service" button
6. **Service** returns control to Estimate Builder
7. **Estimate Builder** navigates back to "Add service" page for next service
8. Repeat until all services are added

## Recent Changes

### Fixed Services for Multi-Service Flow
Updated the following services to work correctly in multi-service estimates:

1. **EC2** (`aws_services/ec2/ec2_configurator.py`)
   - Added `navigate_to_service_config()` that searches from "Add service" page
   - Kept standalone mode as `navigate_to_ec2_config()`

2. **VPC** (`aws_services/vpc/comprehensive_vpc_configurator.py`)
   - Added `navigate_to_service_config()` and `_get_service_search_terms()`
   - Kept standalone mode as `navigate_to_vpc_config()`

3. **ALB** (`aws_services/alb/alb_configurator.py`)
   - Updated `navigate_to_service_config()` to use base class pattern

4. **SQS** (`aws_services/sqs/sqs_configurator.py`)
   - Added `navigate_to_service_config()`, `_get_service_search_terms()`, `_apply_service_specific_config()`
   - Kept standalone mode as `navigate_to_sqs_config()`

5. **ECS Fargate** (`aws_services/ecs_fargate/ecs_fargate_configurator.py`)
   - Added `navigate_to_service_config()`, `_get_service_search_terms()`, `_apply_service_specific_config()`
   - Kept standalone mode as `navigate_to_ecs_fargate_config()`

### Estimate Builder Improvements
Updated `aws_services/estimate_builder.py`:
- Enhanced `_navigate_to_service_search()` to better handle clicking "Add service" button
- Added fallback navigation if automatic navigation fails

## Testing Individual Services

Use `test_service_interactions.py` to test each service:

```bash
python test_service_interactions.py
```

This script will:
1. Create a test estimate
2. Navigate to "Add service" page
3. Test each service's ability to:
   - Navigate from search to config page
   - Fill in fields
   - Click "Save and add service" button
4. Map all interactive elements

## How Services Work Now

### In Multi-Service Mode
When called from `AWSEstimateBuilder`:
1. `navigate_to_service_config()` - Searches for service from "Add service" page
2. `apply_configuration(config, add_to_estimate=True)` - Fills fields and clicks "Save and add service"
3. Returns control to builder

### In Standalone Mode  
Can still be used independently:
1. `navigate_to_[service]_config()` - Creates new estimate and navigates to config
2. `apply_[service]_configuration(config)` - Fills fields
3. `save_and_exit()` - Saves and gets estimate URL

## Service Methods

Each service configurator should have:

```python
def navigate_to_service_config(self) -> bool:
    """Navigate from 'Add service' page to service config page"""
    # Search for service using _get_service_search_terms()
    # Navigate to config page
    return True

def _get_service_search_terms(self) -> List[str]:
    """Return list of search terms to find this service"""
    return ["Service Name", "Alternative Name"]

def _apply_service_specific_config(self, config: Dict[str, Any]) -> bool:
    """Apply service-specific configuration"""
    # Fill fields based on config dict
    return True
```

## Next Steps

1. Test each service with `test_service_interactions.py`
2. Verify services can navigate and fill fields correctly
3. Test full multi-service flow with `run_multi_service_estimate.py`
4. Add more services following the same pattern

## Service Status

Services updated for multi-service flow:
- ✅ EC2
- ✅ VPC  
- ✅ ALB
- ✅ SQS
- ✅ ECS Fargate

Services that may need testing:
- S3
- Lambda
- IAM
- CloudWatch
- KMS
- Shield
- WAF
- API Gateway
- OpenSearch
- Bedrock
- Security Groups


