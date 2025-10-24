"""
Bedrock Configuration Example
Shows how to use the mapped elements to configure Bedrock with real-world settings
"""

from playwright.sync_api import sync_playwright
from aws_bedrock_configurator import BedrockConfigurator
import json

def load_element_map(filename: str = "bedrock_elements_map.json") -> dict:
    """Load the element map from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Element map file {filename} not found. Run aws_bedrock_configurator.py first.")
        return {}

def create_bedrock_configs():
    """Create different Bedrock configuration examples"""
    
    configs = {
        "light_usage": {
            "name": "Light Usage - Small App",
            "description": "Small application with minimal AI usage",
            "settings": {
                # Model 1: Claude 3 Haiku (fast, cheap)
                "input_8_text": "10",      # Average requests per minute
                "input_9_text": "8",       # Hours per day at this rate
                "input_10_text": "100",    # Average input tokens per request
                "input_11_text": "50",     # Average output tokens per request
                
                # Model 2: Disabled
                "checkbox_4_2231-1761201177945-8554": False,  # Disable model 2
                
                # Model 3: Disabled  
                "checkbox_5_2232-1761201177945-115": False,   # Disable model 3
            }
        },
        
        "medium_usage": {
            "name": "Medium Usage - Business App",
            "description": "Business application with moderate AI usage",
            "settings": {
                # Model 1: Claude 3 Sonnet (balanced)
                "input_8_text": "50",      # Average requests per minute
                "input_9_text": "12",      # Hours per day at this rate
                "input_10_text": "500",    # Average input tokens per request
                "input_11_text": "200",    # Average output tokens per request
                
                # Model 2: Claude 3 Haiku (for simple tasks)
                "input_12_text": "30",     # Average requests per minute
                "input_13_text": "8",      # Hours per day at this rate
                "input_14_text": "200",    # Average input tokens per request
                "input_15_text": "100",    # Average output tokens per request
                
                # Model 3: Disabled
                "checkbox_5_2232-1761201177945-115": False,   # Disable model 3
            }
        },
        
        "heavy_usage": {
            "name": "Heavy Usage - Enterprise App",
            "description": "Enterprise application with high AI usage",
            "settings": {
                # Model 1: Claude 3 Opus (most capable)
                "input_8_text": "100",     # Average requests per minute
                "input_9_text": "16",      # Hours per day at this rate
                "input_10_text": "2000",   # Average input tokens per request
                "input_11_text": "1000",   # Average output tokens per request
                
                # Model 2: Claude 3 Sonnet (balanced)
                "input_12_text": "80",     # Average requests per minute
                "input_13_text": "12",     # Hours per day at this rate
                "input_14_text": "1000",   # Average input tokens per request
                "input_15_text": "500",    # Average output tokens per request
                
                # Model 3: Claude 3 Haiku (fast tasks)
                "input_16_text": "150",    # Average requests per minute
                "input_17_text": "8",      # Hours per day at this rate
                "input_18_text": "300",    # Average input tokens per request
                "input_19_text": "150",    # Average output tokens per request
            }
        },
        
        "ai_research": {
            "name": "AI Research - High Token Usage",
            "description": "Research project with high token consumption",
            "settings": {
                # Model 1: Claude 3 Opus (for complex analysis)
                "input_8_text": "20",      # Average requests per minute
                "input_9_text": "24",      # Hours per day at this rate
                "input_10_text": "8000",   # Average input tokens per request
                "input_11_text": "4000",   # Average output tokens per request
                
                # Model 2: Disabled
                "checkbox_4_2231-1761201177945-8554": False,  # Disable model 2
                
                # Model 3: Disabled
                "checkbox_5_2232-1761201177945-115": False,   # Disable model 3
            }
        }
    }
    
    return configs

def print_config_summary(configs: dict):
    """Print a summary of available configurations"""
    print("\n" + "="*70)
    print("AVAILABLE BEDROCK CONFIGURATIONS")
    print("="*70)
    
    for config_id, config in configs.items():
        print(f"\n📋 {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Settings: {len(config['settings'])} parameters")
        
        # Show key settings
        settings = config['settings']
        if 'input_8_text' in settings:
            print(f"   - Model 1: {settings['input_8_text']} req/min, {settings['input_9_text']} hrs/day")
        if 'input_12_text' in settings:
            print(f"   - Model 2: {settings['input_12_text']} req/min, {settings['input_13_text']} hrs/day")
        if 'input_16_text' in settings:
            print(f"   - Model 3: {settings['input_16_text']} req/min, {settings['input_17_text']} hrs/day")

def apply_configuration(configurator: BedrockConfigurator, config: dict) -> bool:
    """Apply a specific configuration to Bedrock"""
    try:
        print(f"\n[INFO] Applying configuration: {config['name']}")
        print(f"[INFO] Description: {config['description']}")
        
        # Set description if provided
        if 'description' in config:
            # Find the description input field
            elements = configurator.map_all_elements()
            for input_id, input_details in elements['inputs'].items():
                if 'description' in input_details.get('aria_label', '').lower():
                    configurator.page.fill(input_details['selector'], config['description'])
                    print(f"[OK] Set description: {config['description']}")
                    break
        
        # Apply all settings
        for setting_id, value in config['settings'].items():
            # Find the element and apply the setting
            elements = configurator.map_all_elements()
            
            # Check inputs
            if setting_id in elements['inputs']:
                selector = elements['inputs'][setting_id]['selector']
                configurator.page.fill(selector, str(value))
                print(f"[OK] Set {setting_id} to {value}")
            
            # Check checkboxes
            elif setting_id in elements['checkboxes']:
                selector = elements['checkboxes'][setting_id]['selector']
                if value:
                    configurator.page.check(selector)
                else:
                    configurator.page.uncheck(selector)
                print(f"[OK] Set {setting_id} to {value}")
        
        print(f"[OK] Configuration '{config['name']}' applied successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to apply configuration: {e}")
        return False

def main():
    """Main function to demonstrate Bedrock configuration"""
    print("[INFO] Starting Bedrock Configuration Example")
    
    # Load element map
    element_map = load_element_map()
    if not element_map:
        return
    
    # Create configuration examples
    configs = create_bedrock_configs()
    print_config_summary(configs)
    
    # Let user choose configuration
    print(f"\n[INFO] Available configurations:")
    config_list = list(configs.keys())
    for i, config_id in enumerate(config_list, 1):
        print(f"  {i}. {configs[config_id]['name']}")
    
    try:
        choice = input(f"\nSelect configuration (1-{len(config_list)}) or press Enter for 'light_usage': ").strip()
        if not choice:
            choice = "1"
        
        config_index = int(choice) - 1
        if 0 <= config_index < len(config_list):
            selected_config_id = config_list[config_index]
            selected_config = configs[selected_config_id]
        else:
            print("[ERROR] Invalid selection, using light_usage")
            selected_config = configs['light_usage']
    except (ValueError, KeyboardInterrupt):
        print("[INFO] Using default light_usage configuration")
        selected_config = configs['light_usage']
    
    # Run the configuration
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Create configurator
        configurator = BedrockConfigurator(page)
        
        # Navigate to Bedrock config
        if configurator.navigate_to_bedrock_config():
            # Apply the selected configuration
            if apply_configuration(configurator, selected_config):
                # Save and get URL
                url = configurator.save_and_exit()
                if url:
                    print(f"\n🎉 SUCCESS!")
                    print(f"📋 Configuration: {selected_config['name']}")
                    print(f"🔗 Estimate URL: {url}")
                    
                    # Save URL to file
                    with open(f"bedrock_estimate_{selected_config['name'].lower().replace(' ', '_')}.txt", "w") as f:
                        f.write(url)
                    print(f"💾 URL saved to bedrock_estimate_{selected_config['name'].lower().replace(' ', '_')}.txt")
                else:
                    print("[ERROR] Failed to save configuration")
            else:
                print("[ERROR] Failed to apply configuration")
        
        try:
            input("\nPress Enter to close browser...")
        except EOFError:
            print("[INFO] Closing browser...")
        
        browser.close()

if __name__ == "__main__":
    main()
