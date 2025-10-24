#!/usr/bin/env python3
"""
Simple web interface to display JSON data and generate AWS Calculator links
"""

from flask import Flask, render_template_string, jsonify
import json
from utils.json_parser import JSONParser

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AWS Cost Calculator - {{ project_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .service { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .service-name { font-weight: bold; color: #232f3e; }
        .service-cost { color: #ff9900; font-size: 1.2em; }
        .service-description { color: #666; margin: 5px 0; }
        .config-item { margin: 5px 0; }
        .total-cost { background: #f0f8ff; padding: 20px; border-radius: 5px; text-align: center; }
        .aws-link { background: #ff9900; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }
        .aws-link:hover { background: #e68900; }
    </style>
</head>
<body>
    <h1>AWS Cost Calculator - {{ project_name }}</h1>
    
    <div class="total-cost">
        <h2>Total Estimated Annual Cost: ${{ total_cost:, }}</h2>
        <p>Budget: ${{ max_budget:, }}</p>
        <p>Remaining Budget: ${{ remaining_budget:, }}</p>
    </div>
    
    <a href="https://calculator.aws/#/estimate" class="aws-link" target="_blank">
        Open AWS Pricing Calculator
    </a>
    
    <h2>Services to Configure:</h2>
    {% for service in services %}
    <div class="service">
        <div class="service-name">{{ service.service_name }}</div>
        <div class="service-cost">${{ service.estimated_yearly_price:, }}/year</div>
        <div class="service-description">{{ service.description }}</div>
        
        <h4>Configuration:</h4>
        {% for key, value in service.configurations.items() %}
        <div class="config-item"><strong>{{ key }}:</strong> {{ value }}</div>
        {% endfor %}
    </div>
    {% endfor %}
    
    <h2>Services to Skip (No Cost):</h2>
    {% for service in skipped_services %}
    <div class="service">
        <div class="service-name">{{ service.service_name }}</div>
        <div class="service-cost">${{ service.estimated_yearly_price }}/year</div>
        <div class="service-description">{{ service.description }}</div>
    </div>
    {% endfor %}
    
    <script>
        // Auto-open AWS Calculator in new tab
        setTimeout(function() {
            if (confirm('Would you like to open the AWS Pricing Calculator now?')) {
                window.open('https://calculator.aws/#/estimate', '_blank');
            }
        }, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        parser = JSONParser("sow-analysis-Ody.json")
        data = parser.parse()
        
        services_to_configure = parser.get_services_to_configure()
        services_to_skip = parser.get_services_to_skip()
        
        total_cost = sum(service.estimated_yearly_price for service in services_to_configure)
        remaining_budget = data['max_budget'] - total_cost
        
        return render_template_string(HTML_TEMPLATE,
            project_name=data['project_name'],
            total_cost=total_cost,
            max_budget=data['max_budget'],
            remaining_budget=remaining_budget,
            services=services_to_configure,
            skipped_services=services_to_skip
        )
    except Exception as e:
        return f"Error: {e}"

@app.route('/api/services')
def api_services():
    try:
        parser = JSONParser("sow-analysis-Ody.json")
        data = parser.parse()
        
        services_data = []
        for service in parser.get_services_to_configure():
            services_data.append({
                'name': service.service_name,
                'cost': service.estimated_yearly_price,
                'description': service.description,
                'configurations': service.configurations
            })
        
        return jsonify({
            'project_name': data['project_name'],
            'total_cost': sum(s['cost'] for s in services_data),
            'max_budget': data['max_budget'],
            'services': services_data
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("[INFO] Starting web interface...")
    print("[INFO] Open http://localhost:5000 in your browser")
    print("[INFO] Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)

