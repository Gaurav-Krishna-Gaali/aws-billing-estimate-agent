# VPC Interaction Capabilities

## 🎯 Overview

The VPC configurator provides **comprehensive interaction capabilities** with all types of interactive elements on the AWS VPC configuration page. This includes radios, inputs, dropdowns, checkboxes, and dynamic elements.

## 🔧 Element Types Supported

### 1. Radio Buttons
- **Discovery**: Automatically finds all radio button groups
- **Interaction**: Click by value or label text
- **Dynamic**: Handles radio buttons that show/hide other elements
- **Grouping**: Identifies radio button groups by name attribute

```python
# Click radio button by value
configurator.click_radio_button_by_value("production")

# Click radio button by label text
configurator.click_radio_button_by_text("Multi-AZ Deployment")
```

### 2. Dropdowns/Select Elements
- **Discovery**: Finds all select elements with options
- **Interaction**: Select options by name and value
- **Options**: Maps all available options with text and values
- **Dynamic**: Handles dropdowns that populate based on other selections

```python
# Select dropdown option
configurator.select_dropdown_option("region", "us-east-1")

# Select by aria-label
configurator.select_dropdown_option("availability_zone", "us-east-1a")
```

### 3. Input Fields
- **Discovery**: Finds all text, number, and email inputs
- **Interaction**: Fill by aria-label, name, id, or placeholder
- **Types**: Supports text, number, email, and other input types
- **Visibility**: Checks if fields are visible before filling

```python
# Fill input field by aria-label
configurator.fill_input_field("Number of VPCs", "2")

# Fill by name attribute
configurator.fill_input_field("subnet_count", "4")

# Fill by ID
configurator.fill_input_field("cidr_block", "10.0.0.0/16")
```

### 4. Checkboxes
- **Discovery**: Finds all checkbox elements
- **Interaction**: Toggle by identifier (aria-label, name, or id)
- **State**: Check current state before toggling
- **Labels**: Associates checkboxes with their labels

```python
# Toggle checkbox
configurator.toggle_checkbox("enable_dns_hostnames", True)

# Uncheck checkbox
configurator.toggle_checkbox("enable_vpn_connection", False)
```

## 🚀 Advanced Features

### Dynamic Element Discovery
The configurator can discover all interactive elements dynamically:

```python
# Discover all elements
options = configurator.explore_all_vpc_options()

# Access specific element types
radio_buttons = options['radio_buttons']
dropdowns = options['dropdowns']
input_fields = options['input_fields']
checkboxes = options['checkboxes']
```

### Comprehensive Configuration
Apply complex configurations with all element types:

```python
comprehensive_config = {
    # Radio button selections
    'vpc_type': 'Production',
    'deployment_model': 'Multi-AZ',
    'connectivity_type': 'Internet Gateway',
    
    # Dropdown selections
    'region': 'us-east-1',
    'availability_zone': 'us-east-1a',
    
    # Input field values
    'number_of_vpcs': 2,
    'number_of_subnets': 6,
    'data_processed_gb': 1000,
    'cidr_block': '10.0.0.0/16',
    
    # Checkbox toggles
    'enable_dns_hostnames': True,
    'enable_vpc_flow_logs': True,
    'enable_nat_gateway': True
}

# Apply comprehensive configuration
configurator.apply_comprehensive_vpc_configuration(comprehensive_config)
```

## 🧪 Testing Capabilities

### Element Discovery Test
```bash
python test_vpc_interactions.py
```

This test demonstrates:
- **Radio Button Interactions**: Click all radio buttons by value and text
- **Dropdown Interactions**: Select options from all dropdowns
- **Input Field Interactions**: Fill all visible input fields
- **Checkbox Interactions**: Toggle all checkboxes
- **Comprehensive Configuration**: Apply complex multi-element configuration

### Test Results
The test suite provides detailed output showing:
- Number of elements discovered
- Success/failure for each interaction
- Element details (names, values, labels)
- Configuration application results

## 📊 Element Mapping

### Radio Buttons
- **Name**: Radio button group name
- **Value**: Radio button value
- **Label**: Associated label text
- **Checked**: Current state
- **Aria Label**: Accessibility label

### Dropdowns
- **Name**: Select element name
- **ID**: Element ID
- **Options**: All available options with text and values
- **Aria Label**: Accessibility label

### Input Fields
- **Type**: Input type (text, number, email)
- **Aria Label**: Accessibility label
- **Placeholder**: Placeholder text
- **Name**: Input name attribute
- **ID**: Element ID
- **Visible**: Whether field is visible
- **Value**: Current value

### Checkboxes
- **Name**: Checkbox name
- **ID**: Element ID
- **Aria Label**: Accessibility label
- **Checked**: Current state
- **Label Text**: Associated label text

## 🔍 Selector Strategies

The configurator uses multiple selector strategies for robust element interaction:

### Radio Buttons
```python
# By value
input[type='radio'][value='production']

# By text content
input[type='radio']:has-text('Production')
```

### Dropdowns
```python
# By name
select[name='region']

# By aria-label
select[aria-label*='Region']
```

### Input Fields
```python
# By aria-label
input[aria-label*='Number of VPCs']

# By name
input[name='vpc_count']

# By ID
input[id='vpc-input']

# By placeholder
input[placeholder*='Enter number']
```

### Checkboxes
```python
# By aria-label
input[type='checkbox'][aria-label*='Enable DNS']

# By name
input[type='checkbox'][name='dns_enabled']

# By ID
input[type='checkbox'][id='dns-checkbox']
```

## 🎯 Use Cases

### 1. Basic VPC Configuration
```python
basic_config = {
    'description': 'Basic VPC setup',
    'number_of_vpcs': 1,
    'number_of_subnets': 2,
    'enable_dns_hostnames': True,
    'region': 'us-east-1'
}
```

### 2. Enterprise VPC Configuration
```python
enterprise_config = {
    'description': 'Enterprise VPC with high availability',
    'vpc_type': 'Production',
    'deployment_model': 'Multi-AZ',
    'number_of_vpcs': 4,
    'number_of_subnets': 16,
    'number_of_nat_gateways': 8,
    'enable_vpc_flow_logs': True,
    'enable_vpc_endpoints': True,
    'region': 'us-east-1'
}
```

### 3. Development VPC Configuration
```python
dev_config = {
    'description': 'Development VPC',
    'vpc_type': 'Development',
    'number_of_vpcs': 1,
    'number_of_subnets': 3,
    'enable_dns_hostnames': True,
    'enable_dns_resolution': True,
    'region': 'us-east-1'
}
```

## ✅ Capabilities Summary

The VPC configurator provides **complete interaction capabilities** with:

- ✅ **All Radio Buttons** - Click by value or text
- ✅ **All Dropdowns** - Select options by name and value  
- ✅ **All Input Fields** - Fill by multiple selector strategies
- ✅ **All Checkboxes** - Toggle by identifier
- ✅ **Dynamic Elements** - Discover and interact with elements that appear/disappear
- ✅ **Complex Configurations** - Apply multi-element configurations
- ✅ **Error Handling** - Graceful handling of missing or invalid elements
- ✅ **Element Discovery** - Automatic discovery of all interactive elements
- ✅ **State Management** - Check current state before making changes
- ✅ **Robust Selectors** - Multiple fallback selector strategies

## 🚀 Getting Started

1. **Run Element Discovery**:
   ```bash
   cd aws_services/vpc
   python test_vpc_interactions.py
   ```

2. **Use Enhanced Configurator**:
   ```python
   from enhanced_vpc_configurator import EnhancedVPCConfigurator
   
   configurator = EnhancedVPCConfigurator(page)
   configurator.navigate_to_vpc_config()
   configurator.apply_comprehensive_vpc_configuration(config)
   ```

3. **Explore All Options**:
   ```python
   options = configurator.explore_all_vpc_options()
   print(f"Found {options['total_elements']} interactive elements")
   ```

The VPC configurator provides **complete interaction capabilities** with all types of elements on the AWS VPC configuration page! 🎉
