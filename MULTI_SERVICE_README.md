# Multi-Service AWS Calculator Automation

A comprehensive system for automating AWS cost estimates with multiple services in a single browser session, powered by LLM processing for intelligent service configuration mapping.

## 🚀 Features

- **Multi-Service Support**: Configure multiple AWS services in one estimate session
- **LLM-Powered Mapping**: Automatically transform SOW JSON to standardized service configurations
- **Centralized Browser Management**: Single browser session for all services
- **Service Validation**: Schema-based validation of service configurations
- **Shareable URLs**: Generate single AWS Calculator estimate URLs
- **Extensible Architecture**: Easy to add new AWS services

## 📋 Architecture

```
Input (SOW JSON) → LLM Processing → Standardized JSON → AWS Calculator → Shareable URL
```

### Components

1. **Service Schemas** (`schemas/`): Standardized JSON schemas for each AWS service
2. **LLM Processor** (`llm_processor/`): Transforms SOW data to standardized formats
3. **Estimate Builder** (`aws_services/estimate_builder.py`): Manages multi-service browser sessions
4. **Service Registry** (`aws_services/service_registry.py`): Dynamic configurator loading
5. **Main Runner** (`run_multi_service_estimate.py`): User-facing orchestration script

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Set up LLM API Key** (optional, for SOW processing):
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   # OR
   export ANTHROPIC_API_KEY="your-anthropic-key"
   ```

## 🎯 Usage

### Basic Usage

```bash
# Process SOW JSON with LLM and create estimate
python run_multi_service_estimate.py sow-analysis-Ody.json --llm-process

# Use pre-standardized JSON
python run_multi_service_estimate.py examples/standardized_multi_service.json

# Run in headless mode
python run_multi_service_estimate.py input.json --headless

# Save URL to specific file
python run_multi_service_estimate.py input.json --output my_estimate.txt
```

### Advanced Usage

```bash
# Validate configurations only (no browser)
python run_multi_service_estimate.py input.json --validate-only

# Use Anthropic Claude instead of OpenAI
python run_multi_service_estimate.py input.json --llm-process --provider anthropic

# Specify custom API key
python run_multi_service_estimate.py input.json --llm-process --api-key your-key
```

## 📁 File Structure

```
aws_billing_automation/
├── schemas/
│   ├── service_schemas.json          # Service schema definitions
│   ├── llm_mapping_prompt.md         # LLM instructions
│   └── example_sow_to_schema.json   # Example transformations
├── llm_processor/
│   ├── sow_to_schema_mapper.py       # LLM mapping logic
│   └── schema_validator.py           # Configuration validation
├── aws_services/
│   ├── estimate_builder.py           # Multi-service browser management
│   ├── service_registry.py           # Dynamic configurator loading
│   └── base_configurator.py          # Updated with multi-service support
├── examples/
│   └── standardized_multi_service.json  # Example configuration
├── run_multi_service_estimate.py     # Main orchestration script
├── test_multi_service.py             # Test suite
└── requirements.txt                  # Updated dependencies
```

## 🔧 Supported Services

- **S3**: Storage buckets with multiple instances
- **ECS Fargate**: Container services with task configurations
- **Application Load Balancer (ALB)**: Load balancing configurations
- **API Gateway**: REST/HTTP API configurations
- **AWS Lambda**: Serverless function configurations
- **CloudWatch**: Monitoring and logging
- **IAM**: Identity and access management
- **KMS**: Key management service
- **AWS Shield**: DDoS protection
- **WAF**: Web application firewall
- **VPC**: Virtual private cloud
- **SQS**: Simple queue service
- **EC2**: Elastic compute cloud
- **OpenSearch**: Search and analytics
- **Bedrock**: Foundation models

## 📝 Input Formats

### SOW JSON Format (for LLM processing)

```json
{
  "result": {
    "estimate": [
      {
        "estimated_yearly_price": 300,
        "service_name": "Input S3 Bucket",
        "configurations": {
          "AverageStorage": "500 GB",
          "DataTransferOut": "100 GB/month",
          "StorageClass": "Standard",
          "Region": "us-east-1"
        },
        "description": "S3 bucket for batch ingest and input artifacts."
      }
    ]
  }
}
```

### Standardized Format (direct use)

```json
{
  "project_name": "My Project",
  "services": {
    "s3": [
      {
        "description": "Input S3 Bucket",
        "region": "us-east-1",
        "storage_gb": 500,
        "storage_class": "Standard",
        "put_requests": 100000,
        "get_requests": 200000
      }
    ],
    "ecs_fargate": [
      {
        "description": "API Service",
        "region": "us-east-1",
        "number_of_tasks": 3,
        "memory_gb": 2,
        "vcpu_per_task": 1
      }
    ]
  }
}
```

## 🧪 Testing

Run the test suite to verify everything is working:

```bash
python test_multi_service.py
```

The test suite validates:
- Service registry loading
- Schema validation
- Estimate builder initialization
- Example configuration processing

## 🔄 Workflow

1. **Input Processing**: Load SOW JSON or standardized JSON
2. **LLM Mapping** (optional): Transform SOW data to standardized format
3. **Validation**: Validate configurations against service schemas
4. **Browser Session**: Open AWS Calculator and create estimate
5. **Service Addition**: Add each service configuration sequentially
6. **URL Generation**: Save and return shareable estimate URL

## 🎛️ Configuration

### Service Schemas

Each service has a standardized schema in `schemas/service_schemas.json`:

```json
{
  "s3": {
    "description": "Amazon S3 storage service configuration",
    "fields": {
      "description": "string - Description of the S3 bucket purpose",
      "region": "string - AWS region (default: us-east-1)",
      "storage_gb": "number - Storage size in GB",
      "storage_class": "string - Storage class (Standard/IA/Glacier/Deep Archive)"
    }
  }
}
```

### LLM Mapping

The LLM processor uses intelligent mapping to transform SOW data:

- **Service Name Mapping**: "Application Load Balancer" → "alb"
- **Unit Conversions**: "50 GB" → 50, "1 TB" → 1024
- **Field Mapping**: "AverageStorage" → "storage_gb"
- **Default Values**: Missing fields get reasonable defaults

## 🚨 Error Handling

The system includes comprehensive error handling:

- **Service Loading**: Graceful fallback if configurator fails to load
- **Validation**: Clear error messages for invalid configurations
- **Browser Errors**: Automatic retry and cleanup
- **LLM Errors**: Fallback to manual configuration

## 🔮 Future Enhancements

- **Additional Services**: Support for more AWS services
- **Custom Schemas**: User-defined service schemas
- **Batch Processing**: Process multiple SOW files
- **Cost Optimization**: Suggest cost-saving alternatives
- **Integration**: API endpoints for programmatic access

## 📊 Performance

- **Browser Efficiency**: Single session for all services
- **LLM Optimization**: Batch processing for multiple services
- **Memory Management**: Automatic cleanup of browser resources
- **Error Recovery**: Robust error handling and retry logic

## 🤝 Contributing

To add support for a new AWS service:

1. **Create Schema**: Add service schema to `schemas/service_schemas.json`
2. **Update Registry**: Add service to `aws_services/service_registry.py`
3. **Implement Configurator**: Create service configurator with required methods
4. **Add Tests**: Include service in test suite
5. **Update Documentation**: Add service to supported services list

## 📄 License

This project is part of the AWS Billing Automation suite. See the main project for license information.

## 🆘 Support

For issues and questions:

1. Check the test suite: `python test_multi_service.py`
2. Review service schemas in `schemas/service_schemas.json`
3. Validate your input JSON format
4. Check browser automation logs for detailed error messages

---

**Ready to automate your AWS cost estimates?** 🚀

Start with: `python run_multi_service_estimate.py examples/standardized_multi_service.json`
