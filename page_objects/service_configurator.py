"""
Service Configurator Classes for AWS Calculator Automation
Handles configuration of different AWS services in the pricing calculator
"""

from playwright.sync_api import Page, TimeoutError as PWTimeout
from typing import Dict, Any, List, Optional
import time


class BaseServiceConfigurator:
    """Base class for service configuration with common helper methods"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def try_fill_by_labels(self, labels: List[str], value: str, timeout: int = 3000) -> bool:
        """Try to fill a field using various label selectors"""
        for label in labels:
            try:
                self.page.get_by_label(label).fill(value, timeout=timeout)
                print(f"[OK] Filled '{label}' with '{value}'")
                return True
            except Exception:
                continue
        return False
    
    def try_fill_by_placeholder(self, placeholders: List[str], value: str, timeout: int = 3000) -> bool:
        """Try to fill a field using placeholder selectors"""
        for placeholder in placeholders:
            try:
                selector = f'input[placeholder*="{placeholder}"]'
                self.page.fill(selector, value, timeout=timeout)
                print(f"[OK] Filled placeholder '{placeholder}' with '{value}'")
                return True
            except Exception:
                continue
        return False
    
    def try_fill_by_aria_label(self, aria_labels: List[str], value: str, timeout: int = 3000) -> bool:
        """Try to fill a field using aria-label selectors"""
        for aria_label in aria_labels:
            try:
                selector = f'input[aria-label*="{aria_label}"]'
                self.page.fill(selector, value, timeout=timeout)
                print(f"[OK] Filled aria-label '{aria_label}' with '{value}'")
                return True
            except Exception:
                continue
        return False
    
    def try_select_option(self, labels: List[str], option_text: str, timeout: int = 3000) -> bool:
        """Try to select an option from a dropdown"""
        for label in labels:
            try:
                self.page.get_by_label(label).select_option(label=option_text)
                print(f"[OK] Selected '{option_text}' for '{label}'")
                return True
            except Exception:
                try:
                    # Try clicking the select and then the option
                    select_selector = f'select[aria-label*="{label}"]'
                    self.page.click(select_selector, timeout=timeout)
                    self.page.wait_for_timeout(500)
                    self.page.click(f'text="{option_text}"', timeout=timeout)
                    print(f"[OK] Selected '{option_text}' for '{label}' (click method)")
                    return True
                except Exception:
                    continue
        return False
    
    def wait_for_field(self, timeout: int = 5000) -> bool:
        """Wait for form fields to appear"""
        try:
            # Wait for any input or select element
            self.page.wait_for_selector('input, select', timeout=timeout)
            self.page.wait_for_timeout(1000)
            return True
        except PWTimeout:
            print("[WARNING]  No form fields detected")
            return False


class S3Configurator(BaseServiceConfigurator):
    """Configurator for S3 service"""
    
    def configure_s3(self, config: Dict[str, Any]) -> bool:
        """Configure S3 service with the provided configuration"""
        try:
            print(f"[CONFIG] Configuring S3: {config.get('bucket_name', 'S3 Bucket')}")
            
            # Wait for configuration panel
            self.wait_for_field()
            
            # Storage amount (GB)
            storage_gb = config.get('storage_gb', 0)
            if storage_gb > 0:
                storage_labels = [
                    "Storage amount", "Storage (GB)", "Storage (GiB)", 
                    "Storage amount (GB)", "Storage (GB) per month", "Amount (GB)"
                ]
                if not self.try_fill_by_labels(storage_labels, str(storage_gb)):
                    self.try_fill_by_placeholder(["GB", "Amount", "Storage"], str(storage_gb))
            
            # Storage class
            storage_class = config.get('storage_class', 'Standard')
            if storage_class:
                class_labels = ["Storage class", "Storage class (tier)", "Storage Class"]
                self.try_select_option(class_labels, "S3 Standard")
            
            # PUT requests
            put_requests = config.get('put_requests', 0)
            if put_requests > 0:
                put_labels = [
                    "PUT, COPY, POST, or LIST Requests", "PUT requests", 
                    "PUT, COPY, POST or LIST requests", "PUT/COPY/POST/LIST"
                ]
                if not self.try_fill_by_labels(put_labels, str(put_requests)):
                    self.try_fill_by_placeholder(["PUT", "Requests"], str(put_requests))
            
            # GET requests
            get_requests = config.get('get_requests', 0)
            if get_requests > 0:
                get_labels = [
                    "GET and all other Requests", "GET requests", 
                    "GET and all other requests", "GET"
                ]
                if not self.try_fill_by_labels(get_labels, str(get_requests)):
                    self.try_fill_by_placeholder(["GET"], str(get_requests))
            
            # Data transfer
            data_transfer_gb = config.get('data_transfer_gb', 0)
            if data_transfer_gb > 0:
                transfer_labels = [
                    "Data transfer out", "Data transfer", "Transfer out", "Data egress"
                ]
                if not self.try_fill_by_labels(transfer_labels, str(data_transfer_gb)):
                    self.try_fill_by_placeholder(["Transfer", "Data"], str(data_transfer_gb))
            
            print("[OK] S3 configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure S3: {e}")
            return False


class CloudWatchConfigurator(BaseServiceConfigurator):
    """Configurator for CloudWatch service"""
    
    def configure_cloudwatch(self, config: Dict[str, Any]) -> bool:
        """Configure CloudWatch service"""
        try:
            print("[CONFIG] Configuring CloudWatch")
            self.wait_for_field()
            
            # Custom metrics
            custom_metrics = config.get('custom_metrics', 0)
            if custom_metrics > 0:
                metrics_labels = ["Custom metrics", "Metrics", "Custom metrics per month"]
                self.try_fill_by_labels(metrics_labels, str(custom_metrics))
            
            # Alarms
            alarms = config.get('alarms', 0)
            if alarms > 0:
                alarm_labels = ["Alarms", "CloudWatch alarms", "Alarm count"]
                self.try_fill_by_labels(alarm_labels, str(alarms))
            
            # Logs storage
            logs_storage_gb = config.get('logs_storage_gb', 0)
            if logs_storage_gb > 0:
                storage_labels = ["Log storage", "Logs storage", "Storage (GB)"]
                self.try_fill_by_labels(storage_labels, str(logs_storage_gb))
            
            # Logs ingestion
            logs_ingestion_gb = config.get('logs_ingestion_gb', 0)
            if logs_ingestion_gb > 0:
                ingestion_labels = ["Log ingestion", "Logs ingestion", "Ingestion (GB)"]
                self.try_fill_by_labels(ingestion_labels, str(logs_ingestion_gb))
            
            print("[OK] CloudWatch configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure CloudWatch: {e}")
            return False


class FargateConfigurator(BaseServiceConfigurator):
    """Configurator for ECS Fargate services"""
    
    def configure_fargate_task(self, config: Dict[str, Any]) -> bool:
        """Configure Fargate task"""
        try:
            service_name = config.get('service_name', 'Fargate Task')
            print(f"[CONFIG] Configuring Fargate: {service_name}")
            self.wait_for_field()
            
            # vCPU
            vcpu = config.get('vcpu', 0)
            if vcpu > 0:
                vcpu_labels = ["vCPU", "CPU", "vCPUs", "Compute units"]
                self.try_fill_by_labels(vcpu_labels, str(vcpu))
            
            # Memory
            memory_gb = config.get('memory_gb', 0)
            if memory_gb > 0:
                memory_labels = ["Memory (GB)", "Memory", "RAM (GB)", "Memory size"]
                self.try_fill_by_labels(memory_labels, str(memory_gb))
            
            # Task hours per month
            task_hours = config.get('task_hours_per_month', 0)
            if task_hours > 0:
                hours_labels = ["Task hours", "Hours per month", "Running hours", "Usage hours"]
                self.try_fill_by_labels(hours_labels, str(task_hours))
            
            # Concurrent tasks
            concurrent_tasks = config.get('concurrent_tasks', 0)
            if concurrent_tasks > 0:
                task_labels = ["Concurrent tasks", "Tasks", "Task count", "Running tasks"]
                self.try_fill_by_labels(task_labels, str(concurrent_tasks))
            
            print("[OK] Fargate configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure Fargate: {e}")
            return False
    
    def configure_ecs_cluster(self, config: Dict[str, Any]) -> bool:
        """Configure ECS cluster (usually just cluster management overhead)"""
        try:
            print("[CONFIG] Configuring ECS Cluster")
            self.wait_for_field()
            
            # ECS cluster is usually just management overhead
            # Most fields might be optional or have defaults
            print("[OK] ECS Cluster configuration completed (using defaults)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure ECS Cluster: {e}")
            return False


class APIGatewayConfigurator(BaseServiceConfigurator):
    """Configurator for API Gateway service"""
    
    def configure_api_gateway(self, config: Dict[str, Any]) -> bool:
        """Configure API Gateway"""
        try:
            print("[CONFIG] Configuring API Gateway")
            self.wait_for_field()
            
            # Requests per month
            requests = config.get('requests_per_month', 0)
            if requests > 0:
                request_labels = [
                    "API calls", "Requests", "API requests", "Requests per month"
                ]
                self.try_fill_by_labels(request_labels, str(requests))
            
            # Data transfer
            data_transfer_gb = config.get('data_transfer_gb', 0)
            if data_transfer_gb > 0:
                transfer_labels = [
                    "Data transfer", "Data transfer out", "Transfer out", "Data egress"
                ]
                self.try_fill_by_labels(transfer_labels, str(data_transfer_gb))
            
            # API type
            api_type = config.get('api_type', 'REST/HTTP')
            if api_type:
                type_labels = ["API type", "Gateway type", "Type"]
                self.try_select_option(type_labels, "REST API")
            
            print("[OK] API Gateway configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure API Gateway: {e}")
            return False


class ALBConfigurator(BaseServiceConfigurator):
    """Configurator for Application Load Balancer"""
    
    def configure_alb(self, config: Dict[str, Any]) -> bool:
        """Configure Application Load Balancer"""
        try:
            print("[CONFIG] Configuring Application Load Balancer")
            self.wait_for_field()
            
            # Hours per month
            hours = config.get('hours_per_month', 0)
            if hours > 0:
                hours_labels = [
                    "Hours per month", "Running hours", "Usage hours", "Hours"
                ]
                self.try_fill_by_labels(hours_labels, str(hours))
            
            # Data processed
            data_processed_gb = config.get('data_processed_gb', 0)
            if data_processed_gb > 0:
                data_labels = [
                    "Data processed", "Data processed (GB)", "Processed data", "Data volume"
                ]
                self.try_fill_by_labels(data_labels, str(data_processed_gb))
            
            print("[OK] ALB configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure ALB: {e}")
            return False


class BedrockConfigurator(BaseServiceConfigurator):
    """Configurator for AWS Bedrock service"""
    
    def configure_bedrock(self, config: Dict[str, Any]) -> bool:
        """Configure AWS Bedrock"""
        try:
            print("[CONFIG] Configuring AWS Bedrock")
            self.wait_for_field()
            
            # Model calls per month
            model_calls = config.get('model_calls_per_month', 0)
            if model_calls > 0:
                call_labels = [
                    "Model calls", "API calls", "Inference calls", "Calls per month"
                ]
                self.try_fill_by_labels(call_labels, str(model_calls))
            
            # Usage tier
            usage_tier = config.get('usage_tier', 'on-demand')
            if usage_tier:
                tier_labels = ["Usage tier", "Pricing tier", "Tier"]
                self.try_select_option(tier_labels, "On-demand")
            
            print("[OK] Bedrock configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure Bedrock: {e}")
            return False


class SQSConfigurator(BaseServiceConfigurator):
    """Configurator for SQS service"""
    
    def configure_sqs(self, config: Dict[str, Any]) -> bool:
        """Configure SQS"""
        try:
            print("[CONFIG] Configuring SQS")
            self.wait_for_field()
            
            # Messages per month
            messages = config.get('messages_per_month', 0)
            if messages > 0:
                message_labels = [
                    "Messages", "Messages per month", "Message count", "Requests"
                ]
                self.try_fill_by_labels(message_labels, str(messages))
            
            print("[OK] SQS configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure SQS: {e}")
            return False


class KMSConfigurator(BaseServiceConfigurator):
    """Configurator for KMS service"""
    
    def configure_kms(self, config: Dict[str, Any]) -> bool:
        """Configure KMS"""
        try:
            print("[CONFIG] Configuring KMS")
            self.wait_for_field()
            
            # Customer managed keys
            keys = config.get('customer_managed_keys', 0)
            if keys > 0:
                key_labels = [
                    "Customer managed keys", "Keys", "CMK count", "Key count"
                ]
                self.try_fill_by_labels(key_labels, str(keys))
            
            print("[OK] KMS configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure KMS: {e}")
            return False


class WAFConfigurator(BaseServiceConfigurator):
    """Configurator for WAF service"""
    
    def configure_waf(self, config: Dict[str, Any]) -> bool:
        """Configure WAF"""
        try:
            print("[CONFIG] Configuring WAF")
            self.wait_for_field()
            
            # Requests per month
            requests = config.get('requests_per_month', 0)
            if requests > 0:
                request_labels = [
                    "Requests", "Requests per month", "Web requests", "HTTP requests"
                ]
                self.try_fill_by_labels(request_labels, str(requests))
            
            # Web ACLs
            webacls = config.get('webacls', 0)
            if webacls > 0:
                acl_labels = [
                    "Web ACLs", "ACLs", "Web Application Firewall ACLs"
                ]
                self.try_fill_by_labels(acl_labels, str(webacls))
            
            # Rules
            rules = config.get('rules', 0)
            if rules > 0:
                rule_labels = [
                    "Rules", "WAF rules", "Rule count"
                ]
                self.try_fill_by_labels(rule_labels, str(rules))
            
            print("[OK] WAF configuration completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to configure WAF: {e}")
            return False


class ServiceConfiguratorFactory:
    """Factory class to create appropriate configurators"""
    
    @staticmethod
    def get_configurator(service_name: str, page: Page) -> BaseServiceConfigurator:
        """Get the appropriate configurator for a service"""
        if 'S3' in service_name:
            return S3Configurator(page)
        elif 'CloudWatch' in service_name:
            return CloudWatchConfigurator(page)
        elif 'Fargate' in service_name or 'ECS' in service_name:
            return FargateConfigurator(page)
        elif 'API Gateway' in service_name:
            return APIGatewayConfigurator(page)
        elif 'Load Balancer' in service_name:
            return ALBConfigurator(page)
        elif 'Bedrock' in service_name:
            return BedrockConfigurator(page)
        elif 'SQS' in service_name:
            return SQSConfigurator(page)
        elif 'KMS' in service_name:
            return KMSConfigurator(page)
        elif 'WAF' in service_name:
            return WAFConfigurator(page)
        else:
            return BaseServiceConfigurator(page)

