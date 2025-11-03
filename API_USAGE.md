# AWS Billing Automation API

FastAPI REST API server for creating AWS Calculator estimates.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python api_server.py
```

Or with uvicorn directly:
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
```bash
GET /health
```

### List Available Services
```bash
GET /services
```

### Get Service Information
```bash
GET /services/{service_type}
# Example: GET /services/s3
```

### Create Estimate (Main Endpoint)

**POST** `/estimate`

**Request Body Options:**

#### Option 1: Pre-standardized Services JSON
```json
{
  "services": {
    "s3": [
      {
        "description": "Production S3 Storage",
        "region": "us-east-1",
        "storage_gb": 500,
        "storage_class": "standard",
        "put_requests": 10000,
        "get_requests": 50000
      }
    ],
    "ec2": [
      {
        "description": "Web Server",
        "region": "us-east-1",
        "instance_type": "t3.medium",
        "instance_count": 3,
        "hours_per_month": 730
      }
    ]
  },
  "headless": false,
  "validate_only": false
}
```

#### Option 2: SOW Data with LLM Processing
```json
{
  "sow_data": {
    "project_name": "Production Web Application",
    "requirements": {
      "storage": "500GB S3 storage",
      "compute": "3 EC2 t3.medium instances",
      "load_balancer": "ALB with 1000GB data processing"
    }
  },
  "use_llm": true,
  "headless": false
}
```

**Response:**
```json
{
  "success": true,
  "estimate_url": "https://calculator.aws/#/estimate?id=...",
  "message": "Estimate created successfully. 2/2 services added.",
  "services_added": {
    "s3": {"successful": 1, "total": 1},
    "ec2": {"successful": 1, "total": 1}
  },
  "validation_results": {
    "valid": true,
    "total_services": 2,
    "valid_services": 2,
    "invalid_services": 0
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## Example Requests

### Using curl

```bash
# Simple estimate with pre-configured services
curl -X POST "http://localhost:8000/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "services": {
      "s3": [{"description": "My S3", "storage_gb": 100, "storage_class": "standard"}],
      "sqs": [{"description": "My Queue", "standard_queue_requests": 1000000}]
    }
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/estimate"
payload = {
    "services": {
        "s3": [
            {
                "description": "Production Storage",
                "storage_gb": 500,
                "storage_class": "standard",
                "put_requests": 10000,
                "get_requests": 50000
            }
        ],
        "waf": [
            {
                "description": "Web Firewall",
                "web_acls": 2,
                "web_requests_received": 1000000
            }
        ]
    },
    "headless": True
}

response = requests.post(url, json=payload)
result = response.json()

if result["success"]:
    print(f"Estimate URL: {result['estimate_url']}")
else:
    print(f"Error: {result['message']}")
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

Set environment variables:
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `DEBUG`: Enable debug mode (default: False)
- `AWS_REGION`: AWS region for Bedrock (default: us-east-1)
- `BEDROCK_MODEL_ID`: Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)
- `HEADLESS`: Run browser headless (default: False)

## Available Services

The API supports all services registered in the service registry:
- s3, ec2, ecs_fargate, alb, api_gateway
- lambda, cloudwatch, iam, kms
- shield, waf, vpc, sqs
- opensearch, bedrock

View all available services:
```bash
GET /services
```

