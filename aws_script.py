import json
import boto3
import hashlib
import urllib.parse
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function to generate AWS Pricing Calculator link from cost estimate JSON
    
    Input: JSON with service estimates
    Output: AWS Calculator shareable link
    """
    
    try:
        # Parse input - handle both direct invocation and API Gateway
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event
        
        result = body.get('result', body)
        estimates = result.get('estimate', [])
        project_name = result.get('projectName', 'AWS Architecture')
        max_budget = result.get('maxAnnualBudgetUSD', 0)
        
        # Generate calculator configuration
        calculator_config = generate_calculator_config(estimates, project_name, max_budget)
        
        # Create shareable link (simplified version)
        # In production, you'd use AWS Price List API or Calculator API
        calculator_url = create_calculator_link(calculator_config)
        
        # Calculate totals
        total_yearly = sum(svc.get('estimated_yearly_price', 0) for svc in estimates)
        total_monthly = total_yearly / 12
        
        response_body = {
            'success': True,
            'projectName': project_name,
            'totalYearlyCost': total_yearly,
            'totalMonthlyCost': round(total_monthly, 2),
            'maxBudget': max_budget,
            'budgetUtilization': f"{(total_yearly/max_budget*100):.1f}%" if max_budget > 0 else "N/A",
            'calculatorUrl': calculator_url,
            'servicesCount': len(estimates),
            'breakdown': [
                {
                    'service': svc['service_name'],
                    'yearlyPrice': svc['estimated_yearly_price'],
                    'monthlyPrice': round(svc['estimated_yearly_price'] / 12, 2),
                    'configurations': svc.get('configurations', {})
                }
                for svc in sorted(estimates, key=lambda x: x['estimated_yearly_price'], reverse=True)
            ]
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_body, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }


def generate_calculator_config(estimates, project_name, max_budget):
    """Generate AWS Calculator configuration from estimates"""
    
    services = []
    
    for estimate in estimates:
        service = {
            'name': estimate['service_name'],
            'region': estimate.get('configurations', {}).get('Region', 'us-east-1'),
            'yearlyPrice': estimate['estimated_yearly_price'],
            'monthlyPrice': estimate['estimated_yearly_price'] / 12,
            'description': estimate.get('description', ''),
            'configurations': estimate.get('configurations', {})
        }
        services.append(service)
    
    return {
        'projectName': project_name,
        'maxBudget': max_budget,
        'services': services,
        'timestamp': datetime.utcnow().isoformat()
    }


def create_calculator_link(config):
    """
    Create AWS Pricing Calculator link
    
    Note: AWS Calculator uses a complex internal format. This is a simplified version.
    For production, you would need to:
    1. Use the AWS Price List API to get exact service codes
    2. Generate the calculator's internal JSON format
    3. Use the Calculator's save/share API endpoint
    
    For now, returning a base calculator URL with query parameters
    """
    
    # Generate a simple hash for the estimate ID
    config_str = json.dumps(config, sort_keys=True)
    estimate_id = hashlib.md5(config_str.encode()).hexdigest()
    
    # Build URL with services as query parameters
    base_url = "https://calculator.aws"
    
    # The actual AWS calculator uses a different format
    # This is a placeholder that shows the concept
    params = {
        'estimate_id': estimate_id,
        'project': config['projectName'],
        'services': len(config['services'])
    }
    
    query_string = urllib.parse.urlencode(params)
    
    # Return the calculator URL format
    # In production, this would be: https://calculator.aws/#/estimate?id={actual_estimate_id}
    return f"{base_url}/#/estimate?id={estimate_id}"


def create_detailed_calculator_payload(estimates):
    """
    Create detailed payload for AWS Calculator API (if available)
    This would require AWS Calculator API integration
    """
    
    payload = {
        "version": "1.0",
        "estimate": {
            "services": []
        }
    }
    
    # Map services to AWS Calculator format
    service_mapping = {
        'ECS Fargate Cluster': 'AmazonECS',
        'API Gateway': 'AmazonAPIGateway',
        'CloudWatch': 'AmazonCloudWatch',
        'Application Load Balancer': 'AWSELB',
        'Input S3 Bucket': 'AmazonS3',
        'Output S3 Bucket': 'AmazonS3',
        'SQS Queue': 'AmazonSQS',
        'AWS Bedrock': 'AmazonBedrock',
        'KMS': 'awskms',
        'WAF': 'AWSWAFv2'
    }
    
    for estimate in estimates:
        service_name = estimate['service_name']
        aws_service = service_mapping.get(service_name, service_name)
        
        service_config = {
            "service": aws_service,
            "region": estimate.get('configurations', {}).get('Region', 'us-east-1'),
            "description": estimate.get('description', ''),
            "estimatedCost": estimate['estimated_yearly_price'] / 12,
            "configurations": estimate.get('configurations', {})
        }
        
        payload["estimate"]["services"].append(service_config)
    
    return payload


# For local testing
if __name__ == "__main__":
    # Test with sample data
    test_event = {
        "result": {
            "projectName": "Ody",
            "maxAnnualBudgetUSD": 10000,
            "estimate": [
                {
                    "service_name": "CloudWatch",
                    "estimated_yearly_price": 900,
                    "configurations": {
                        "Region": "us-east-1",
                        "Metrics": "Custom metrics 50/month"
                    },
                    "description": "Monitoring and logging"
                },
                {
                    "service_name": "API Gateway",
                    "estimated_yearly_price": 800,
                    "configurations": {
                        "Region": "us-east-1",
                        "RequestsPerMonth": "10M"
                    },
                    "description": "API Gateway"
                }
            ]
        }
    }
    
    response = lambda_handler(test_event, None)
    print(json.dumps(json.loads(response['body']), indent=2))