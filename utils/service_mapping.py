"""
Service Mapping for AWS Calculator Automation
Maps JSON service names to AWS calculator search terms and configuration methods
"""

from typing import Dict, List, Optional, Tuple, Any
from .json_parser import ServiceConfig


class ServiceMapping:
    """Maps JSON service names to AWS calculator configurations"""
    
    # Mapping from JSON service names to AWS calculator search terms
    SERVICE_SEARCH_MAPPING = {
        'CloudWatch': 'CloudWatch',
        'KMS': 'Key Management Service',
        'WAF': 'Web Application Firewall',
        'API Gateway': 'API Gateway',
        'Application Load Balancer': 'Application Load Balancer',
        'Input S3 Bucket': 'S3',
        'Output S3 Bucket': 'S3',
        'ECS Fargate Cluster': 'ECS',
        'Ingestion Service (Fargate task)': 'Fargate',
        'Policy Evaluation Service (Fargate task)': 'Fargate',
        'Verdict Generation Service (Fargate task)': 'Fargate',
        'SQS Queue': 'SQS',
        'AWS Bedrock': 'Bedrock'
    }
    
    # Services that should be skipped (no calculator form or $0 cost)
    SKIP_SERVICES = {
        'IAM', 'Shield', 'VPC (multi-AZ)', 'Public Subnet (multi-AZ)', 'Private Subnet (multi-AZ)'
    }
    
    @classmethod
    def get_search_term(cls, service_name: str) -> Optional[str]:
        """Get the AWS calculator search term for a service"""
        return cls.SERVICE_SEARCH_MAPPING.get(service_name)
    
    @classmethod
    def should_skip_service(cls, service_name: str) -> bool:
        """Check if a service should be skipped"""
        return service_name in cls.SKIP_SERVICES
    
    @classmethod
    def get_configuration_method(cls, service_name: str) -> str:
        """Get the configuration method name for a service"""
        method_mapping = {
            'CloudWatch': 'configure_cloudwatch',
            'KMS': 'configure_kms',
            'WAF': 'configure_waf',
            'API Gateway': 'configure_api_gateway',
            'Application Load Balancer': 'configure_alb',
            'Input S3 Bucket': 'configure_s3',
            'Output S3 Bucket': 'configure_s3',
            'ECS Fargate Cluster': 'configure_ecs_cluster',
            'Ingestion Service (Fargate task)': 'configure_fargate_task',
            'Policy Evaluation Service (Fargate task)': 'configure_fargate_task',
            'Verdict Generation Service (Fargate task)': 'configure_fargate_task',
            'SQS Queue': 'configure_sqs',
            'AWS Bedrock': 'configure_bedrock'
        }
        return method_mapping.get(service_name, 'configure_generic')
    
    @classmethod
    def get_service_type(cls, service_name: str) -> str:
        """Get the service type for grouping similar services"""
        if 'S3' in service_name:
            return 'S3'
        elif 'Fargate' in service_name or 'ECS' in service_name:
            return 'Fargate'
        else:
            return service_name.split()[0]  # First word as type
    
    @classmethod
    def extract_s3_config(cls, service_config: ServiceConfig) -> Dict[str, Any]:
        """Extract S3-specific configuration from service config"""
        config = service_config.configurations
        
        # Parse storage amount
        storage_gb = 0
        if 'AverageStorage' in config:
            storage_str = config['AverageStorage']
            if 'GB' in storage_str:
                storage_gb = int(storage_str.replace('GB', '').strip())
        
        # Parse requests
        put_requests = 0
        get_requests = 0
        if 'PUT/GETRequestsPerMonth' in config:
            requests_str = config['PUT/GETRequestsPerMonth']
            if '/' in requests_str:
                put_str, get_str = requests_str.split('/')
                put_requests = int(put_str.replace('k', '000').replace(',', ''))
                get_requests = int(get_str.replace('k', '000').replace(',', ''))
        
        # Parse data transfer
        data_transfer_gb = 0
        if 'DataTransferOut' in config:
            transfer_str = config['DataTransferOut']
            if 'GB' in transfer_str:
                data_transfer_gb = int(transfer_str.replace('GB/month', '').strip())
        
        return {
            'storage_gb': storage_gb,
            'put_requests': put_requests,
            'get_requests': get_requests,
            'data_transfer_gb': data_transfer_gb,
            'storage_class': config.get('StorageClass', 'Standard'),
            'bucket_name': service_config.service_name
        }
    
    @classmethod
    def extract_fargate_config(cls, service_config: ServiceConfig) -> Dict[str, Any]:
        """Extract Fargate-specific configuration from service config"""
        config = service_config.configurations
        
        # Parse vCPU and memory
        vcpu = 0
        memory_gb = 0
        if 'vCPU' in config:
            vcpu_str = config['vCPU']
            vcpu = int(vcpu_str.replace('vCPU per task', '').strip())
        
        if 'Memory' in config:
            memory_str = config['Memory']
            memory_gb = int(memory_str.replace('GB per task', '').strip())
        
        # Parse concurrent tasks
        concurrent_tasks = 0
        if 'AvgConcurrentTasks' in config:
            concurrent_tasks = int(config['AvgConcurrentTasks'])
        
        # Parse task hours
        task_hours = 0
        if 'TaskHoursPerMonth' in config:
            hours_str = config['TaskHoursPerMonth']
            # Extract number from string like "3 tasks * 730 hours"
            if '*' in hours_str:
                parts = hours_str.split('*')
                if len(parts) >= 2:
                    task_hours = int(parts[1].replace('hours', '').strip())
        
        return {
            'vcpu': vcpu,
            'memory_gb': memory_gb,
            'concurrent_tasks': concurrent_tasks,
            'task_hours_per_month': task_hours,
            'service_name': service_config.service_name
        }
    
    @classmethod
    def extract_cloudwatch_config(cls, service_config: ServiceConfig) -> Dict[str, Any]:
        """Extract CloudWatch-specific configuration"""
        config = service_config.configurations
        
        # Parse metrics
        custom_metrics = 0
        if 'Metrics' in config:
            metrics_str = config['Metrics']
            if 'Custom metrics' in metrics_str and '/month' in metrics_str:
                custom_metrics = int(metrics_str.split('Custom metrics')[1].split('/month')[0].strip())
        
        # Parse alarms
        alarms = 0
        if 'Alarms' in config:
            alarms = int(config['Alarms'])
        
        # Parse logs
        logs_storage_gb = 0
        logs_ingestion_gb = 0
        if 'LogsStoragePerMonth' in config:
            storage_str = config['LogsStoragePerMonth']
            logs_storage_gb = int(storage_str.replace('GB', '').strip())
        
        if 'LogsIngestionPerMonth' in config:
            ingestion_str = config['LogsIngestionPerMonth']
            logs_ingestion_gb = int(ingestion_str.replace('GB', '').strip())
        
        return {
            'custom_metrics': custom_metrics,
            'alarms': alarms,
            'logs_storage_gb': logs_storage_gb,
            'logs_ingestion_gb': logs_ingestion_gb
        }
    
    @classmethod
    def extract_api_gateway_config(cls, service_config: ServiceConfig) -> Dict[str, Any]:
        """Extract API Gateway configuration"""
        config = service_config.configurations
        
        requests_per_month = 0
        if 'RequestsPerMonth' in config:
            requests_str = config['RequestsPerMonth']
            if 'M' in requests_str:
                requests_per_month = int(requests_str.replace('M', '')) * 1000000
            else:
                requests_per_month = int(requests_str)
        
        data_transfer_gb = 0
        if 'DataTransferOutPerMonth' in config:
            transfer_str = config['DataTransferOutPerMonth']
            data_transfer_gb = int(transfer_str.replace('GB', '').strip())
        
        return {
            'requests_per_month': requests_per_month,
            'data_transfer_gb': data_transfer_gb,
            'api_type': config.get('APIType', 'REST/HTTP')
        }
    
    @classmethod
    def extract_alb_config(cls, service_config: ServiceConfig) -> Dict[str, Any]:
        """Extract Application Load Balancer configuration"""
        config = service_config.configurations
        
        hours_per_month = 0
        if 'HoursPerMonth' in config:
            hours_per_month = int(config['HoursPerMonth'])
        
        data_processed_gb = 0
        if 'DataProcessedPerMonth' in config:
            data_str = config['DataProcessedPerMonth']
            if 'TB' in data_str:
                data_processed_gb = int(data_str.replace('TB', '').strip()) * 1000
            elif 'GB' in data_str:
                data_processed_gb = int(data_str.replace('GB', '').strip())
        
        return {
            'hours_per_month': hours_per_month,
            'data_processed_gb': data_processed_gb
        }
    
    @classmethod
    def extract_bedrock_config(cls, service_config: ServiceConfig) -> Dict[str, Any]:
        """Extract AWS Bedrock configuration"""
        config = service_config.configurations
        
        model_calls = 0
        if 'ModelCallsPerMonth' in config:
            calls_str = config['ModelCallsPerMonth']
            if 'k' in calls_str:
                model_calls = int(calls_str.replace('k', '000').replace('small-inference calls', '').strip())
            else:
                model_calls = int(calls_str)
        
        return {
            'model_calls_per_month': model_calls,
            'usage_tier': config.get('UsageTier', 'on-demand')
        }


if __name__ == "__main__":
    # Test the service mapping
    from .json_parser import JSONParser
    
    parser = JSONParser("sow-analysis-Ody.json")
    data = parser.parse()
    
    print("\n[TEST] Service Mapping:")
    for service in parser.get_services_to_configure():
        search_term = ServiceMapping.get_search_term(service.service_name)
        method = ServiceMapping.get_configuration_method(service.service_name)
        print(f"   {service.service_name} -> Search: '{search_term}', Method: {method}")
