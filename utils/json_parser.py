"""
JSON Parser for AWS Calculator Automation
Reads and parses the sow-analysis-Ody.json file to extract service configurations
"""

import json
from typing import List, Dict, Any, Optional


class ServiceConfig:
    """Represents a service configuration from the JSON"""
    
    def __init__(self, service_data: Dict[str, Any]):
        self.service_name = service_data.get('service_name', '')
        self.estimated_yearly_price = service_data.get('estimated_yearly_price', 0)
        self.configurations = service_data.get('configurations', {})
        self.description = service_data.get('description', '')
    
    def __repr__(self):
        return f"ServiceConfig(name='{self.service_name}', price=${self.estimated_yearly_price})"


class JSONParser:
    """Parses the AWS cost analysis JSON file"""
    
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.project_name = ""
        self.max_budget = 0
        self.services: List[ServiceConfig] = []
    
    def parse(self) -> Dict[str, Any]:
        """Parse the JSON file and extract all relevant data"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            result = data.get('result', {})
            self.project_name = result.get('projectName', '')
            self.max_budget = result.get('maxAnnualBudgetUSD', 0)
            
            # Extract services
            estimates = result.get('estimate', [])
            self.services = [ServiceConfig(service) for service in estimates]
            
            print(f"[OK] Parsed JSON: {len(self.services)} services found for project '{self.project_name}'")
            print(f"[INFO] Max budget: ${self.max_budget:,}")
            
            return {
                'project_name': self.project_name,
                'max_budget': self.max_budget,
                'services': self.services,
                'total_estimated_cost': sum(service.estimated_yearly_price for service in self.services)
            }
            
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {self.json_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise Exception(f"Error parsing JSON: {e}")
    
    def get_services_with_cost(self) -> List[ServiceConfig]:
        """Return only services that have a cost > 0"""
        return [service for service in self.services if service.estimated_yearly_price > 0]
    
    def get_services_to_skip(self) -> List[ServiceConfig]:
        """Return services that should be skipped (no cost or no calculator equivalent)"""
        skip_patterns = [
            'IAM', 'Shield', 'VPC', 'Public Subnet', 'Private Subnet'
        ]
        
        services_to_skip = []
        for service in self.services:
            # Skip if no cost
            if service.estimated_yearly_price == 0:
                services_to_skip.append(service)
                continue
            
            # Skip if matches skip patterns
            for pattern in skip_patterns:
                if pattern.lower() in service.service_name.lower():
                    services_to_skip.append(service)
                    break
        
        return services_to_skip
    
    def get_services_to_configure(self) -> List[ServiceConfig]:
        """Return services that should be configured in the calculator"""
        skip_services = self.get_services_to_skip()
        skip_names = {service.service_name for service in skip_services}
        
        return [service for service in self.services if service.service_name not in skip_names]
    
    def print_summary(self):
        """Print a summary of the parsed data"""
        print(f"\n[SUMMARY] Project: {self.project_name}")
        print(f"[INFO] Max Budget: ${self.max_budget:,}")
        print(f"[INFO] Total Services: {len(self.services)}")
        
        services_to_configure = self.get_services_to_configure()
        services_to_skip = self.get_services_to_skip()
        
        print(f"[OK] Services to configure: {len(services_to_configure)}")
        for service in services_to_configure:
            print(f"   - {service.service_name}: ${service.estimated_yearly_price:,}/year")
        
        print(f"[SKIP] Services to skip: {len(services_to_skip)}")
        for service in services_to_skip:
            print(f"   - {service.service_name}: ${service.estimated_yearly_price}/year (no calculator form)")


if __name__ == "__main__":
    # Test the parser
    parser = JSONParser("sow-analysis-Ody.json")
    data = parser.parse()
    parser.print_summary()
